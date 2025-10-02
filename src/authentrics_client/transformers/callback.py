from __future__ import annotations

import json
import logging
import tarfile
import uuid
from pathlib import Path

from transformers import (
    TrainerCallback,
    TrainerControl,
    TrainerState,
    TrainingArguments,
)

from .. import AuthentricsClient, FileType
from ..cli import TOKEN_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AuthentricsCallback(TrainerCallback):
    def __init__(
        self,
        project_name: str,
        save_stats_local: bool,
        *features,
        model_format: str | FileType = FileType.HF_TEXT,
    ):
        # check if we are logged in and already have a token
        self.session = self._check_authorization()
        self.project_name = project_name
        self.save_stats_local = save_stats_local
        self.model_format = FileType(model_format)
        self.project = self.session.get_project_by_name(self.project_name)
        if self.project is None:
            logging.info("Project not found, Creating new project")
            self.project = self.session.post(
                "/project",
                json={
                    "name": self.project_name,
                    "description": "Created from authentrics_integration",
                },
            )
        else:
            files = self.project["fileList"]
            logging.info(
                f"Found project with project name: {self.project_name}."
                " Current analysis of all checkpoints"
            )
            for file in files:
                logging.info(
                    f"File Name: {file['fileName']}\n"
                    f"Weight Contr: {file['totalWeightContribution']}\n"
                    f"Bias Contr: {file['totalBiasContribution']}"
                )

        self.features = features

    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        output_dir = Path(args.output_dir)

        ckpt_dir = f"checkpoint-{state.global_step}"
        artifact_path = output_dir / ckpt_dir
        checkpoint_name = f"{ckpt_dir}-{str(uuid.uuid4())}"

        tar_path = output_dir / f"{checkpoint_name}.tar.gz"

        self._tar_directory(artifact_path, tar_path)
        logging.info(f"Uploading checkpoint artifacts in {ckpt_dir}...")

        assert self.project is not None

        self.project = self.session.post(
            "/project/file",
            json={
                "projectId": self.project["id"],
                "filePath": tar_path,
                "format": self.model_format.value,
                "fileName": checkpoint_name,
            },
        )

        assert self.project is not None
        files = self.project["fileList"]
        if len(files) < 2:
            logging.info("1st checkpoint, not running the static analysis")
            return

        logging.info(f"Running Static Analysis for file: {files[-1]['fileName']}")
        static_analysis = self.session.post(
            "/static_analysis",
            json={
                "projectId": self.project["id"],
                "fileId": files[-1]["id"],
                "comparison": "PREVIOUS",
            },
        )

        logging.info("Summary status of the current saved checkpoint...")
        logging.info(f"Weight Summary Score: {static_analysis['weight_summary_score']}")
        logging.info(f"Bias Summary Score: {static_analysis['bias_summary_score']}")

        if not self.save_stats_local:
            return

        final_output = {}

        for feature in self.features:
            if feature in static_analysis:
                final_output[feature] = static_analysis[feature]
            else:
                logging.error(f"Feature: {feature} not available for response")
        if len(self.features) == 0:
            final_output = static_analysis

        project_output_dir = self._create_output_dir(args.output_dir)
        file_name = project_output_dir / f"static_analysis_{checkpoint_name}.json"

        logging.info(f"Created analysis response with file name: {file_name}")

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
                    logging.error("Invalid token file, Please login again")
                    raise ValueError("Invalid token file")

                return self._check_token_validity(data)

        else:
            logging.error(
                "Login required, use authrx login --username=John --password=*** command"
            )
            raise ValueError(
                "Login required, use authrx login --username=John --password=*** command "
            ) from None

    def _check_token_validity(self, data: dict[str, str]) -> AuthentricsClient:
        try:
            session = AuthentricsClient(data["url"])
            session.login(data["token"])
            session.get("/project")
            return session
        except Exception:
            logging.error("Expired token. Please login again")
            raise ValueError("Expired token. Please login again") from None

    def _create_output_dir(self, output_dir: str) -> Path:
        output_path = Path(output_dir) / self.project_name
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path
