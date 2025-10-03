from __future__ import annotations

import json
import logging
import tarfile
from pathlib import Path

from transformers import (
    TrainerCallback,
    TrainerControl,
    TrainerState,
    TrainingArguments,
)

from .. import AuthentricsClient, FileType
from ..cli import TOKEN_PATH


class AuthentricsCallback(TrainerCallback):
    """A custom TrainerCallback for integrating with the Authentrics platform.

    This callback handles project creation, logging, and checkpoint analysis
    for model training runs, and can optionally save statistics locally.

    Args:
        project_name (str): The name of the project to use or create on Authentrics.
        *features: Additional features to enable for the callback.
        save_stats_local (bool, optional): Whether to save statistics locally (default:
        False).
        model_format (str | FileType): The format of the model files.
        logger (logging.Logger | None, optional): Logger instance to use. If None, a
        default logger is created.
    """

    def __init__(
        self,
        project_name: str,
        *features,
        model_format: str | FileType,
        save_stats_local: bool = False,
        logger: logging.Logger | None = None,
    ):
        """Initialize the AuthentricsCallback.

        Checks for authorization, sets up the project, logger, and stores configuration.

        Args:
            project_name (str): The name of the project to use or create on Authentrics.
            save_stats_local (bool, optional): Whether to save statistics locally
            (default: False).
            *features: Additional features to enable for the callback.
            model_format (str | FileType): The format of the model files.
            logger (logging.Logger | None, optional): Logger instance to use. If None, a
            default logger is created.
        """
        # check if we are logged in and already have a token
        self.session = self._check_authorization()
        self.project_name = project_name
        self.save_stats_local = save_stats_local
        self.features = features
        self.model_format = FileType(model_format)
        self.logger = logger

        self.project = self.session.project.get_project_by_name(self.project_name)

        if self.logger is None:
            self.logger = logging.getLogger(__name__)
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        if self.project is None:
            self.logger.info("Project not found, Creating new project")
            self.project = self.session.project.create_project(
                self.project_name,
                "Created from authentrics_integration",
                self.model_format.value,
            )
        else:
            files = self.project["fileList"]
            self.logger.info(
                f"Found project with project name: {self.project_name}."
                " Current analysis of all checkpoints:"
            )
            for file in files:
                self.logger.info(
                    f"File Name: {file['fileName']}\n"
                    f"Weight Contr: {file['totalWeightContribution']}\n"
                    f"Bias Contr: {file['totalBiasContribution']}"
                )
            if len(files) == 0:
                self.logger.info("No checkpoints found")

    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        output_dir = Path(args.output_dir)

        checkpoint_name = self._add_checkpoint(output_dir, state)

        files = self.project["fileList"]
        if len(files) < 2:
            self.logger.info("1st checkpoint, not running the static analysis")
            return

        self.logger.info(f"Running Static Analysis for file: {files[-1]['fileName']}")
        static_analysis = self.session.static.static_analysis(
            project_id=self.project["id"],
            checkpoint_id=files[-1]["id"],
            comparison="PREVIOUS",
        )

        self.logger.info("Summary status of the current saved checkpoint...")
        self.logger.info(
            f"Weight Summary Score: {static_analysis['weight_summary_score']}"
        )
        self.logger.info(f"Bias Summary Score: {static_analysis['bias_summary_score']}")

        if self.save_stats_local:
            self._save_stats(output_dir, checkpoint_name, static_analysis)

    def _add_checkpoint(self, output_dir: Path, state: TrainerState):
        assert self.project is not None, "Project not found, initialization failed"

        ckpt_dir = f"checkpoint-{state.global_step}"
        artifact_path = output_dir / ckpt_dir
        checkpoint_name = f"{ckpt_dir}-{len(self.project['fileList']) + 1}"

        tar_path = output_dir / f"{checkpoint_name}.tar"

        self._tar_directory(artifact_path, tar_path)
        self.logger.info(f"Uploading checkpoint artifacts in {ckpt_dir}...")

        self.project = self.session.checkpoint.add_checkpoint(
            self.project["id"],
            tar_path,
            self.model_format.value,
            checkpoint_name=checkpoint_name,
        )

        return checkpoint_name

    def _save_stats(self, output_dir: Path, checkpoint_name: str, static_analysis: dict):
        final_output = {}

        for feature in self.features:
            if feature in static_analysis:
                final_output[feature] = static_analysis[feature]
            else:
                self.logger.error(f"Feature: {feature} not available for response")

        if len(self.features) == 0:
            final_output = static_analysis

        project_output_dir = self._create_output_dir(output_dir)
        file_name = project_output_dir / f"static_analysis_{checkpoint_name}.json"

        self.logger.info(f"Created analysis response with file name: {file_name}")

        with open(file_name, "w") as file:
            json.dump(final_output, file, indent=4)

    def _tar_directory(self, directory: Path, tar_filename: Path):
        with tarfile.open(tar_filename, "w") as tar:
            tar.add(directory, arcname=directory.name)

    def _check_authorization(self) -> AuthentricsClient:
        if TOKEN_PATH.exists():
            with TOKEN_PATH.open("r", encoding="utf-8") as file:
                data = json.load(file)
                if "token" not in data or "url" not in data:
                    raise ValueError("Invalid token file, please login again")

                return self._check_token_validity(data)

        else:
            raise ValueError(
                "Login required, use `authrx login --username=John --password=***`"
            ) from None

    def _check_token_validity(self, data: dict[str, str]) -> AuthentricsClient:
        try:
            session = AuthentricsClient(data["url"])
            session.auth.login(token=data["token"])
            session.project.get_projects()
            return session
        except Exception:
            raise ValueError("Expired token. Please login again") from None

    def _create_output_dir(self, output_dir: Path) -> Path:
        output_path = output_dir / self.project_name
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path
