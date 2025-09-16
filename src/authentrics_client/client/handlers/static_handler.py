from __future__ import annotations

from pathlib import Path
from typing import Any

from ..types import Comparison
from .base_handler import BaseHandler

__all__ = ["StaticHandler"]


class StaticHandler(BaseHandler):
    """A handler for running static analysis on a project.

    Static analysis is a collective term for any Authentrics.ai analysis that does not
    perform inference on a model.
    """

    def static_analysis(
        self,
        *,
        project_id: str,
        checkpoint_id: str,
        comparison: Comparison | str = Comparison.PREVIOUS,
        weight_names: list[str] | None = None,
        bias_names: list[str] | None = None,
        **kwargs,
    ) -> dict:
        """Run static analysis on a checkpoint.

        This will describe the differences between the selected checkpoint and the
        previous one, optionally with respect to the latest checkpoint.

        Args:
            project_id (str): The ID of the project to run static analysis on.
            checkpoint_id (str): The ID of the checkpoint to run static analysis on.
            comparison (:class:`Comparison` | str): The comparison to perform (default:
                'PREVIOUS').
            weight_names (list[str]): The names of the weights to include in the analysis.
                By default, all weights are included.
            bias_names (list[str]): The names of the biases to include in the analysis.
                By default, all biases are included.
            **kwargs: Additional keyword arguments to pass to the analysis.

        Returns:
            A dictionary containing the static analysis results. The structure of the
            dictionary is as follows:

            - metadata (dict): The metadata of the analysis.
            - weight_summary_score (float): The score of the weight summary.
            - bias_summary_score (float): The score of the bias summary.
            - absolute_weight_difference (`dict[str, np.ndarray]`): The weight
              difference for each layer.
            - absolute_bias_difference (`dict[str, np.ndarray]`): The bias difference
              for each layer.
            - relative_weight_difference (`dict[str, np.ndarray]`): The weight
              difference for each layer normalized by that layer's weight in the
              original checkpoint (if comparison is 'PREVIOUS') or the latest
              checkpoint (if comparison is 'ALL').
            - relative_bias_difference (`dict[str, np.ndarray]`): The bias difference
              for each layer normalized by that layer's bias in the original
              checkpoint (if comparison is 'PREVIOUS') or the latest checkpoint
              (if comparison is 'ALL').
        """
        data: dict[str, Any] = {
            "projectId": project_id,
            "fileId": checkpoint_id,
            "comparisonType": Comparison(comparison).value,
        }
        if weight_names is not None:
            data["weightNames"] = weight_names
        if bias_names is not None:
            data["biasNames"] = bias_names
        data.update(kwargs)

        return self.post("/static_analysis", json=data).json()

    def exclude(
        self,
        *,
        project_id: str,
        checkpoints_to_exclude: list[str],
        new_checkpoint_path: str | Path,
        overwrite: bool = False,
        **kwargs,
    ):
        """Edit the latest checkpoint to exclude the selected checkpoints.

        Args:
            project_id: The ID of the project to edit the latest checkpoint of.
            checkpoints_to_exclude: The IDs of the checkpoints to exclude.
            new_checkpoint_path: The path to save the new checkpoint to.
            overwrite: Whether to overwrite the new checkpoint if it already exists.
                If False, an error will be raised if the new checkpoint already exists.
            **kwargs: Additional keyword arguments to pass to the analysis.
        """
        new_checkpoint_path = Path(new_checkpoint_path)
        if new_checkpoint_path.exists() and not overwrite:
            raise FileExistsError(f"File {new_checkpoint_path} already exists")

        data = {
            "projectId": project_id,
            "fileId": checkpoints_to_exclude,
        }
        data.update(kwargs)

        new_checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        with open(new_checkpoint_path, "wb") as f:
            response = self.post(
                "/edit",
                json=data,
                stream=True,
            )
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    def metatune(
        self,
        *,
        project_id: str,
        checkpoints_to_tune: list[str],
        amplitudes: list[float],
        new_checkpoint_path: str | Path,
        overwrite: bool = False,
        **kwargs,
    ) -> None:
        """Edit the latest checkpoint to vary the influence of the selected checkpoints.

        Args:
            project_id: The ID of the project to edit the latest checkpoint of.
            checkpoints_to_tune: The IDs of the checkpoints to tune.
            amplitudes: The amplitudes of the tunings, must be the same length as
                `checkpoints_to_tune`.
            new_checkpoint_path: The path to save the new checkpoint to.
            overwrite: Whether to overwrite the new checkpoint if it already exists.
                If False, an error will be raised if the new checkpoint already exists.

        Note: For the amplitudes, 0.0 means the influence of the checkpoint is not
        changed, 1.0 means the influence of the checkpoint is fully applied, and -1.0
        means the influence of the checkpoint is fully removed (as in
        :class:`StaticHandler.exclude()`).
        """
        if len(checkpoints_to_tune) != len(amplitudes):
            raise ValueError("checkpoints_to_tune and amplitudes must be the same length")

        data = {
            "projectId": project_id,
            "fileId": checkpoints_to_tune,
            "parameterList": amplitudes,
        }
        data.update(kwargs)

        new_checkpoint_path = Path(new_checkpoint_path)
        if new_checkpoint_path.exists() and not overwrite:
            raise FileExistsError(f"File {new_checkpoint_path} already exists")

        new_checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        with open(new_checkpoint_path, "wb") as f:
            response = self.post(
                "/metatune",
                json=data,
                stream=True,
            )
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
