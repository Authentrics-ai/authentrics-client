from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..types import ComparisonType, MOEAnalysisType, generate_multipart_json
from .base_handler import BaseHandler

__all__ = ["DynamicHandler"]


class DynamicHandler(BaseHandler):
    """A handler for interacting with dynamic analysis in the Authentrics API.

    Dynamic analysis is any analysis that is performed during a model inference.
    """

    def comparative_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_path: str | Path,
        *,
        layer_names: list[str] | None = None,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a comparative analysis for a single stimulus file.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_path: Path to the local stimulus file to analyze.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.

        Returns:
            dict: The analysis results.

        Raises:
            FileNotFoundError: If the stimulus file does not exist.
        """
        stimulus_path = Path(stimulus_path)
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        if not stimulus_path.exists():
            raise FileNotFoundError(f"Stimulus file {stimulus_path} not found")

        data: dict[str, Any] = {
            "projectId": project_id,
            "fileId": checkpoint_id,
        }
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        if layer_names is not None:
            data["layerNames"] = layer_names
        data.update(kwargs)

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
        inference_config: dict | str | None = None,
        batch_size: int = 1,
        **kwargs,
    ) -> dict:
        """Get the dynamic analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.
            batch_size: Number of files to process in each batch. Defaults to 1.

        Returns:
            dict: The analysis results.
        """
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
        }
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        if layer_names is not None:
            data["layerNames"] = layer_names
        data.update(kwargs)

        return self.post("/dynamic_analysis/comparative/batch", json=data).json()

    def contribution_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_path: str | Path,
        *,
        comparison_type: ComparisonType | str = ComparisonType.CHOSEN,
        layer_names: list[str] | None = None,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a contribution analysis for a single stimulus file.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_path: Path to the local stimulus file to analyze.
            comparison_type: The type of comparison to perform.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.
        """
        stimulus_path = Path(stimulus_path)
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        if not stimulus_path.exists():
            raise FileNotFoundError(f"Stimulus file {stimulus_path} not found")

        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "comparisonType": ComparisonType(comparison_type).value,
        }
        if layer_names is not None:
            data["layerNames"] = layer_names
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

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
        comparison_type: ComparisonType | str = ComparisonType.CHOSEN,
        layer_names: list[str] | None = None,
        batch_size: int = 1,
        unchanged_activation_threshold: float = 0.0,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a contribution analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            comparison_type: The type of comparison to perform.
            layer_names: Optional list of layer names to analyze. Default is to use all
            layers.
            batch_size: Number of files to process in each batch. Defaults to 1.
            unchanged_activation_threshold: The threshold for considering a layer
            unchanged. Default is 0.0.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.
        Returns:
            dict: The analysis results.
        """
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
            "comparisonType": ComparisonType(comparison_type).value,
            "unchangedActivationThreshold": str(unchanged_activation_threshold),
        }
        if layer_names is not None:
            data["layerNames"] = layer_names
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

        return self.post(
            "/dynamic_analysis/contribution/batch",
            json=data,
        ).json()

    def batch_correlation_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_paths: list[str],
        *,
        layer_names: list[str] | None = None,
        batch_size: int = 1,
        inference_config: dict | str | None = None,
        **kwargs,
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
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.
        """
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
        }
        if layer_names is not None:
            data["layerNames"] = layer_names
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

        return self.post("/dynamic_analysis/correlation/batch", json=data).json()

    def sensitivity_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_path: str | Path,
        scaling_factor: float,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a sensitivity analysis for a single stimulus file.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_path: Path to the local stimulus file to analyze.
            scaling_factor: The scaling factor of the change to the checkpoint.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.

        Note: For the scaling factor, 0.0 means the influence of the checkpoint is not
        changed, 1.0 means the influence of the checkpoint is fully applied, and -1.0
        means the influence of the checkpoint is fully removed (as in
        `StaticHandler.exclude()`).
        """
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        stimulus_path = Path(stimulus_path)
        if not stimulus_path.exists():
            raise FileNotFoundError(f"Stimulus file {stimulus_path} not found")

        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "scalingFactor": str(scaling_factor),
        }
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

        return self.post(
            "/dynamic_analysis/sensitivity",
            files=generate_multipart_json(stimulus_path, **data),
        ).json()

    def batch_sensitivity_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_paths: list[str],
        scaling_factor: float,
        *,
        batch_size: int = 1,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a sensitivity analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            scaling_factor: The scaling factor of the change to the checkpoint.
            batch_size: Number of files to process in each batch. Defaults to 1.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.
        Returns:
            dict: The analysis results.
        """
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
            "scalingFactor": str(scaling_factor),
        }
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

        return self.post(
            "/dynamic_analysis/sensitivity/batch",
            json=data,
        ).json()

    def mixture_of_experts_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_path: str | Path,
        *,
        layer_names: list[str],
        analysis_type: MOEAnalysisType | str = MOEAnalysisType.EXPERT,
        num_experts: int | None = None,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a mixture of experts analysis for a single stimulus file.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_path: Path to the local stimulus file to analyze.
            layer_names: List of layer names to analyze. Must be either router/gate layers
            or expert layers.
            analysis_type: The type of MoE analysis to perform.
            num_experts: The number of experts to be included in the topK selection when
            analyzing router/gate layers.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.
        """
        stimulus_path = Path(stimulus_path)
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        if not stimulus_path.exists():
            raise FileNotFoundError(f"Stimulus file {stimulus_path} not found")

        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "layerNames": layer_names,
            "analysisType": MOEAnalysisType(analysis_type).value,
        }
        if num_experts is not None:
            data["numExperts"] = num_experts
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

        return self.post(
            "/dynamic_analysis/moe",
            files=generate_multipart_json(stimulus_path, **data),
        ).json()

    def batch_mixture_of_experts_analysis(
        self,
        project_id: str,
        checkpoint_id: str,
        stimulus_paths: list[str],
        *,
        analysis_type: MOEAnalysisType | str = MOEAnalysisType.EXPERT,
        layer_names: list[str],
        num_experts: int | None = None,
        batch_size: int = 1,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a mixture of experts analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            checkpoint_id: The ID of the checkpoint to use for analysis.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            layer_names: List of layer names to analyze. Must be either router/gate layers
            or expert layers.
            analysis_type: The type of MoE analysis to perform.
            num_experts: The number of experts to be included in the topK selection when
            analyzing router/gate layers.
            batch_size: Number of files to process in each batch. Defaults to 1.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.
        Returns:
            dict: The analysis results.
        """
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "stimulusPaths": stimulus_paths,
            "batchSize": batch_size,
            "analysisType": MOEAnalysisType(analysis_type).value,
            "layerNames": layer_names,
        }
        if num_experts is not None:
            data["numExperts"] = num_experts
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

        return self.post(
            "/dynamic_analysis/moe/batch",
            json=data,
        ).json()

    def zero_train_optimizer(
        self,
        project_id: str,
        scaling_factor_limit: float,
        *,
        stimulus_paths: list[str],
        expected_output_path: str,
        batch_size: int = 1,
        inference_config: dict | str | None = None,
        **kwargs,
    ) -> dict:
        """Run a zero-train optimizer analysis for multiple external stimulus files.

        Args:
            project_id: The ID of the project to analyze.
            scaling_factor_limit: The limit on the scaling factor of the change to the
            checkpoint. Must be greater than 0.0.
            stimulus_paths: List of paths to external stimulus files to analyze, stored
            in the same bucket as the checkpoint.
            expected_output_path: Path to the expected output file in the same bucket as
            the checkpoint. Currently must be a CSV file of the expected output tensor.
            batch_size: Number of files to process in each batch. Defaults to 1.
            inference_config: Optional inference configuration to use for the analysis.
            If a string is provided, it is assumed to be a JSON string and will be parsed
            as a dictionary.

        Returns:
            dict: The analysis results.
        """
        if scaling_factor_limit <= 0.0:
            raise ValueError("scaling_factor_limit must be greater than 0.0")
        if isinstance(inference_config, dict):
            inference_config = json.dumps(inference_config)
        data = {
            "projectId": project_id,
            "scalingFactorLimit": scaling_factor_limit,
            "stimulusPaths": stimulus_paths,
            "expectedOutputPath": expected_output_path,
            "batchSize": batch_size,
        }
        if inference_config is not None:
            data["inferenceConfigJson"] = inference_config
        data.update(kwargs)

        return self.post(
            "/dynamic_analysis/zto/batch",
            json=data,
        ).json()
