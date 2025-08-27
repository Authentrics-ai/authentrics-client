import warnings
from pathlib import Path

from ..types import FileType, generate_multipart_json
from .base_handler import BaseHandler

__all__ = ["CheckpointHandler"]


class CheckpointHandler(BaseHandler):
    """A handler for interacting with model checkpoints in the Authentrics API."""

    def add_checkpoint(
        self,
        project_id: str,
        file_path: str | Path,
        model_format: str | FileType,
        *,
        checkpoint_name: str | None = None,
        tag: str | None = None,
        **kwargs,
    ) -> dict:
        """Upload a checkpoint.

        Args:
            project_id: The ID of the project to upload the checkpoint to.
            file_path: The path to the checkpoint file.
            model_format: The format of the checkpoint file (must match the project's
            model format).
            checkpoint_name (Optional): The display name of the checkpoint.
            tag (Optional): The tag of the checkpoint, for identifying the checkpoint
            with the data it was trained on.

        Returns:
            The project with the new checkpoint.

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
        data.update(kwargs)
        if checkpoint_name is not None:
            data["fileName"] = checkpoint_name
        if tag is not None:
            data["tag"] = tag

        return self.post(
            "/project/file",
            files=generate_multipart_json(file_path, **data),
        ).json()

    def download_checkpoint(
        self,
        project_id: str,
        checkpoint_id: str,
        new_checkpoint_path: str | Path,
        *,
        overwrite: bool = True,
        **kwargs,
    ) -> None:
        """Download a checkpoint.

        Args:
            project_id: The ID of the project to get the checkpoint from.
            checkpoint_id: The ID of the checkpoint to download.
            new_checkpoint_path: The path to save the checkpoint to.
            overwrite: Whether to overwrite the checkpoint if it already exists.
            If False, an error will be raised if the checkpoint already exists.
        """

        new_checkpoint_path = Path(new_checkpoint_path)
        if new_checkpoint_path.exists() and not overwrite:
            raise FileExistsError(f"File {new_checkpoint_path} already exists")

        new_checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        with open(new_checkpoint_path, "wb") as f:
            response = self.get(
                f"/project/file/{checkpoint_id}",
                params={"projectId": project_id},
                stream=True,
            )
            if response.headers.get("Content-Type") != "application/octet-stream":
                warnings.warn(
                    "The response is not an octet stream. An error may have occurred.",
                    stacklevel=1,
                )
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    def download_all_checkpoints(
        self,
        project_id: str,
        zip_file_path: str | Path,
        *,
        overwrite: bool = True,
        **kwargs,
    ) -> None:
        """Download all checkpoints into a zip file.

        Args:
            project_id: The ID of the project to get the checkpoint from.
            zip_file_path: The path to save the zip file to.
            overwrite: Whether to overwrite the checkpoint if it already exists.
            If False, an error will be raised if the checkpoint already exists.
        """

        zip_file_path = Path(zip_file_path)
        if zip_file_path.exists() and not overwrite:
            raise FileExistsError(f"File {zip_file_path} already exists")

        zip_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(zip_file_path, "wb") as f:
            response = self.get(
                "/project/file",
                params={"projectId": project_id},
                stream=True,
            )
            if response.headers.get("Content-Type") != "application/octet-stream":
                warnings.warn(
                    "The response is not an octet stream. An error may have occurred.",
                    stacklevel=1,
                )
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    def delete_checkpoint(
        self,
        project_id: str,
        checkpoint_id: str,
        *,
        hard_delete: bool | None = None,
    ) -> None:
        """Delete a checkpoint.

        Args:
            project_id: The ID of the project to delete the checkpoint from.
            checkpoint_id: The ID of the checkpoint to delete.
            hard_delete (Optional): Whether to hard delete the checkpoint. If not
            provided, the checkpoint will be soft deleted.
        """
        data = {"projectId": project_id, "fileId": checkpoint_id}
        if hard_delete is not None:
            data["hardDelete"] = bool(hard_delete)

        self.delete("/project/file", json=data)

    def update_checkpoint(
        self,
        project_id: str,
        checkpoint_id: str,
        *,
        file_path: str | Path | None = None,
        model_format: str | FileType | None = None,
        checkpoint_name: str | None = None,
        tag: str | None = None,
        **kwargs,
    ) -> dict:
        """Update a checkpoint.

        Args:
            project_id: The ID of the project to update the checkpoint in.
            checkpoint_id: The ID of the checkpoint to update.
            file_path (Optional): The path to the checkpoint file. If None, only the
            metadata of the checkpoint is updated.
            model_format (Optional): The format of the checkpoint file (must match the
            project's model format).
            checkpoint_name (Optional): The display name of the checkpoint.
            tag (Optional): The tag of the checkpoint, for identifying the checkpoint
            with the data it was trained on.

        Returns:
            The project with the updated checkpoint.
        """
        if file_path is not None:
            if model_format is None:
                raise ValueError("model_format is required if file_path is provided")
            if checkpoint_name is None:
                raise ValueError("checkpoint_name is required if file_path is provided")

        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
        }
        if checkpoint_name is not None:
            data["fileName"] = checkpoint_name
        if tag is not None:
            data["tag"] = tag
        if model_format is not None:
            data["format"] = FileType(model_format).value
        data.update(kwargs)

        return self.patch(
            "/project/file",
            files=generate_multipart_json(file_path, **data),
        ).json()

    def add_external_checkpoint(
        self,
        project_id: str,
        file_path: str,
        model_format: str | FileType,
        *,
        file_name: str | None = None,
        tag: str | None = None,
        **kwargs,
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
        }
        data.update(kwargs)
        if tag is not None:
            data["tag"] = tag

        return self.post(
            "/project/file/external",
            json=data,
        ).json()

    def update_external_checkpoint(
        self,
        project_id: str,
        checkpoint_id: str,
        *,
        model_format: str | FileType | None = None,
        file_path: str | Path | None = None,
        file_name: str | None = None,
        tag: str | None = None,
        **kwargs,
    ) -> dict:
        """Update an external checkpoint."""
        data = {
            "projectId": project_id,
            "fileId": checkpoint_id,
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
        data.update(kwargs)

        return self.patch(
            "/project/file/external",
            json=data,
        ).json()

    def trigger_file_event(self, project_id: str, checkpoint_id: str, **kwargs) -> None:
        """Trigger the calculation of the summary scores and validation of a checkpoint.

        Args:
            project_id: The ID of the project to trigger the file event for.
            checkpoint_id: The ID of the checkpoint to trigger the file event for.
        """
        data = {"projectId": project_id, "fileId": checkpoint_id}
        data.update(kwargs)
        self.post("/project/file_event", json=data)
