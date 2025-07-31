from pathlib import Path
from typing import Any

from ..types import Comparison, generate_multipart_json
from .base_handler import BaseHandler

__all__ = ["DynamicHandler"]


class DynamicHandler(BaseHandler):
    """A handler for interacting with dynamic analysis in the Authentrics API.

    Dynamic analysis is any analysis that is performed during a model inference.
    """

    def single_comparative_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_path: str | Path,
        *,
        layer_names: list[str] | None = None,
    ) -> dict:
        """Run a comparative analysis for a single stimulus file.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_path: Path to the local stimulus file to analyze.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.

        Returns:
            dict: The analysis results.

        Raises:
            FileNotFoundError: If the stimulus file does not exist.
        """
        stimulus_path = Path(stimulus_path)
        if not stimulus_path.exists():
            raise FileNotFoundError(f"Stimulus file {stimulus_path} not found")

        data: dict[str, Any] = {
            "projectId": project_id,
            "fileId": checkpoint_id,
        }
        if layer_names is not None:
            data["layerNames"] = layer_names

        return self.post(
            "/dynamic_analysis/comparative",
            files=generate_multipart_json(stimulus_path, **data),
        ).json()

    def batch_comparative_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_paths: list[str],
        *,
        layer_names: list[str] | None = None,
        batch_size: int = 1,
    ) -> dict:
        """Get the dynamic analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            batch_size: Number of files to process in each batch. Defaults to 1.

        Returns:
            dict: The analysis results.
        """
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
        }
        if layer_names is not None:
            data["layerNames"] = layer_names

        return self.post("/dynamic_analysis/comparative/batch", json=data).json()

    def single_contribution_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_path: str | Path,
        *,
        comparison: Comparison | str = Comparison.PREVIOUS,
        layer_names: list[str] | None = None,
    ) -> dict:
        """Run a contribution analysis for a single stimulus file.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_path: Path to the local stimulus file to analyze.
            comparison: The type of comparison to perform.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
        """
        stimulus_path = Path(stimulus_path)
        if not stimulus_path.exists():
            raise FileNotFoundError(f"Stimulus file {stimulus_path} not found")

        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "comparisonType": Comparison(comparison).value,
        }
        if layer_names is not None:
            data["layerNames"] = layer_names

        return self.post(
            "/dynamic_analysis/contribution",
            files=generate_multipart_json(stimulus_path, **data),
        ).json()

    def batch_contribution_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_paths: list[str],
        *,
        comparison: Comparison | str = Comparison.PREVIOUS,
        layer_names: list[str] | None = None,
        batch_size: int = 1,
    ) -> dict:
        """Run a contribution analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            comparison: The type of comparison to perform.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
            batch_size: Number of files to process in each batch. Defaults to 1.

        Returns:
            dict: The analysis results.
        """
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
            "comparisonType": Comparison(comparison).value,
        }
        if layer_names is not None:
            data["layerNames"] = layer_names

        return self.post(
            "/dynamic_analysis/contribution/batch",
            json=data,
        ).json()

    def correlation_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_paths: list[str],
        *,
        layer_names: list[str] | None = None,
        batch_size: int = 1,
    ) -> dict:
        """Run a correlation analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
            batch_size: Number of files to process in each batch. Defaults to 1.
        """
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
        }
        if layer_names is not None:
            data["layerNames"] = layer_names

        return self.post("/dynamic_analysis/correlation/batch", json=data).json()

    def single_sensitivity_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_path: str | Path,
        amplitude: float,
    ) -> dict:
        """Run a sensitivity analysis for a single stimulus file.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_path: Path to the local stimulus file to analyze.
            amplitude: The amplitude of the change to the checkpoint.

        Note: For the amplitude, 0.0 means the influence of the checkpoint is not changed,
        1.0 means the influence of the checkpoint is fully applied, and -1.0 means the
        influence of the checkpoint is fully removed (as in `StaticHandler.exclude()`).
        """
        stimulus_path = Path(stimulus_path)
        if not stimulus_path.exists():
            raise FileNotFoundError(f"Stimulus file {stimulus_path} not found")

        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "parameter": amplitude,
        }

        return self.post(
            "/dynamic_analysis/sensitivity",
            files=generate_multipart_json(stimulus_path, **data),
        ).json()

    def batch_sensitivity_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_paths: list[str],
        amplitude: float,
        *,
        batch_size: int = 1,
    ) -> dict:
        """Run a sensitivity analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            amplitude: The amplitude of the change to the checkpoint.
            batch_size: Number of files to process in each batch. Defaults to 1.

        Returns:
            dict: The analysis results.
        """
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
            "parameter": amplitude,
        }

        return self.post(
            "/dynamic_analysis/sensitivity/batch",
            json=data,
        ).json()
