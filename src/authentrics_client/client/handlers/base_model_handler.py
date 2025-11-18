from __future__ import annotations

from pathlib import Path

from ..types import FileType, generate_multipart_json
from .base_handler import BaseHandler

__all__ = ["BaseModelHandler"]


class BaseModelHandler(BaseHandler):
    """A handler for interacting with model checkpoints in the Authentrics API."""

    def upload_base_model(
        self,
        project_id: str,
        file_path: str | Path,
        model_format: str | FileType,
        *,
        base_model_name: str | None = None,
        tag: str | None = None,
    ) -> dict:
        """Upload a base model.

        Args:
            project_id: The ID of the project to upload the base model to.
            file_path: The path to the base model file.
            model_format: The format of the base model file (must match the project's
            model format).
            base_model_name (Optional): The display name of the base model.
            tag (Optional): The tag of the base model, for identifying the base model
            with the data it was trained on.

        Returns:
            The project with the new base model.

        Note:
            If the checkpoint is a directory, e.g., a 🤗 checkpoint, please tar it first.
        """
        file_path = Path(file_path)
        if file_path.is_dir():
            raise ValueError(
                f"File {file_path} is a directory."
                " If this is a 🤗 checkpoint, please tar it first."
            )
        if not file_path.is_file():
            raise FileNotFoundError(f"File {file_path} not found")

        data = {
            "projectId": project_id,
            "format": FileType(model_format).value,
        }
        if base_model_name is not None:
            data["fileName"] = base_model_name
        if tag is not None:
            data["tag"] = tag

        return self.post(
            "/project/base-model",
            files=generate_multipart_json(file_path, **data),
        ).json()

    def delete_base_model(self, project_id: str, base_model_id: str) -> dict:
        """Delete a base model.

        Args:
            project_id: The ID of the project to delete the base model from.
            base_model_id: The ID of the base model to delete.
        Returns:
            The project without the deleted base model.
        """
        return self.delete(
            "/project/base-model",
            json={"projectId": project_id, "fileId": base_model_id},
        ).json()

    def update_base_model(
        self,
        project_id: str,
        base_model_id: str,
        *,
        file_path: str | Path | None = None,
        base_model_name: str | None = None,
        tag: str | None = None,
    ) -> dict:
        """Update a base model.

        Args:
            project_id: The ID of the project to update the base model in.
            base_model_id: The ID of the base model to update.
            file_path (Optional): The path to the base model file. If None, only the
            metadata of the base model is updated.
            base_model_name (Optional): The display name of the base model.
            tag (Optional): The tag of the base model, for identifying the base model
            with the data it was trained on.

        Returns:
            The project with the updated base model.
        """
        data = {
            "projectId": project_id,
            "fileId": base_model_id,
        }
        if base_model_name is not None:
            data["fileName"] = base_model_name
        if tag is not None:
            data["tag"] = tag
        return self.patch(
            "/project/base-model",
            files=generate_multipart_json(file_path, **data),
        ).json()

    def add_external_base_model(
        self,
        project_id: str,
        file_path: str,
        model_format: str | FileType,
        *,
        file_name: str | None = None,
        tag: str | None = None,
    ) -> dict:
        """Add an external checkpoint to a project, saved in the same bucket as the
        project.

        Args:
            project_id: The ID of the project to add the external checkpoint to.
            file_path: The path to the external checkpoint file.
            model_format: The format of the external checkpoint file (must match the
            project's model format).
            file_name (Optional): The display name of the external checkpoint.
            tag (Optional): The tag of the external checkpoint, for identifying the
            external checkpoint with the data it was trained on.

        Returns:
            The project with the new external checkpoint.
        """
        data = {
            "projectId": project_id,
            "filePath": file_path,
            "format": FileType(model_format).value,
            "fileName": file_name or file_path.rsplit("/", 1)[-1],
            "baseModel": True,
        }
        if tag is not None:
            data["tag"] = tag

        return self.post(
            "/project/file/external",
            json=data,
        ).json()

    def update_external_base_model(
        self,
        project_id: str,
        base_model_id: str,
        *,
        model_format: str | FileType | None = None,
        file_path: str | Path | None = None,
        file_name: str | None = None,
        tag: str | None = None,
    ) -> dict:
        """Update an external checkpoint."""
        data = {
            "projectId": project_id,
            "fileId": base_model_id,
            "baseModel": True,
        }
        if model_format is not None:
            data["format"] = FileType(model_format).value
        if file_path is not None:
            data["filePath"] = file_path
            data["fileName"] = file_name or file_path.rsplit("/", 1)[-1]
        if file_name is not None:
            data["fileName"] = file_name
        if tag is not None:
            data["tag"] = tag

        return self.patch(
            "/project/file/external",
            json=data,
        ).json()
