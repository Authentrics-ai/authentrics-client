from __future__ import annotations

import warnings
from pathlib import Path

from ..types import FileType, generate_multipart_json
from .base_handler import BaseHandler

__all__ = ["CheckpointHandler"]


class CheckpointHandler(BaseHandler):
    """A handler for interacting with model checkpoints in the Authentrics API.

    Several methods return the project dictionary which include a list of checkpoint
    dictionaries.

    The project dictionary contains:
        - id (str): Unique identifier for the project
        - name (str): Project name
        - description (str): Project description
        - format (str): Format of the model (e.g., 'ONNX', 'HF_TEXT_GENERATION')
        - files (list[dict]): List of checkpoint dictionaries
        - createdAt (str): ISO timestamp when the project was created
        - updatedAt (str): ISO timestamp when the project was last updated

    The checkpoint dictionary contains:
        - id (str): Unique identifier for the checkpoint
        - fileName (str): Display name of the checkpoint
        - tag (str): Tag for identifying the checkpoint with training data
        - format (str): Format of the checkpoint file
        - size (int): Size of the checkpoint file in bytes
        - uploadedAt (str): ISO timestamp when the checkpoint was uploaded
        - status (str): Current status of the checkpoint (e.g., 'uploaded',
            'processing')
    """

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
        """Upload a checkpoint to a project.

        Args:
            project_id (str): The ID of the project to upload the checkpoint to
            file_path (str | Path): The path to the checkpoint file
            model_format (str | FileType): The format of the checkpoint file (must match
                the project's model format)
            checkpoint_name (str, optional): The display name of the checkpoint
            tag (str, optional): The tag of the checkpoint, for identifying the checkpoint
                with the data it was trained on
            **kwargs: Additional fields to include in the upload request

        Returns:
            dict: The project dictionary with the new checkpoint added. See
            :class:`CheckpointHandler` or :class:`ProjectHandler` for the structure of the
            project dictionary and the checkpoint dictionary.

        Note:
            If the checkpoint is a directory, e.g., a 🤗 checkpoint, please tar it first.

        Raises:
            ValueError: If the file path is a directory or model_format is invalid
            FileNotFoundError: If the checkpoint file doesn't exist
            HTTPError: If the upload fails
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
        """Download a checkpoint from a project.

        Args:
            project_id (str): The ID of the project to get the checkpoint from
            checkpoint_id (str): The ID of the checkpoint to download
            new_checkpoint_path (str | Path): The path to save the checkpoint to
            overwrite (bool): Whether to overwrite the checkpoint if it already exists.
                If False, an error will be raised if the checkpoint already exists
            **kwargs: Additional parameters to include in the download request

        Raises:
            FileExistsError: If the target file exists and overwrite is False
            HTTPError: If the download fails
            Warning: If the response is not an octet stream (may indicate an error)
        """

        new_checkpoint_path = Path(new_checkpoint_path)
        if new_checkpoint_path.exists() and not overwrite:
            raise FileExistsError(f"File {new_checkpoint_path} already exists")

        new_checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

        with open(new_checkpoint_path, "wb") as f:
            response = self.get(
                f"/project/file/{checkpoint_id}",
                params={"projectId": project_id, **kwargs},
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
        """Download all checkpoints from a project into a zip file.

        Args:
            project_id (str): The ID of the project to get checkpoints from
            zip_file_path (str | Path): The path to save the zip file to
            overwrite (bool): Whether to overwrite the zip file if it already exists.
                If False, an error will be raised if the file already exists
            **kwargs: Additional parameters to include in the download request

        Raises:
            FileExistsError: If the target zip file exists and overwrite is False
            HTTPError: If the download fails
            Warning: If the response is not an octet stream (may indicate an error)
        """

        zip_file_path = Path(zip_file_path)
        if zip_file_path.exists() and not overwrite:
            raise FileExistsError(f"File {zip_file_path} already exists")

        zip_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(zip_file_path, "wb") as f:
            response = self.get(
                "/project/file",
                params={"projectId": project_id, **kwargs},
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
        """Delete a checkpoint from a project.

        Args:
            project_id (str): The ID of the project to delete the checkpoint from
            checkpoint_id (str): The ID of the checkpoint to delete
            hard_delete (bool, optional): Whether to hard delete the checkpoint.
                If not provided, the checkpoint will be soft deleted

        Raises:
            HTTPError: If the deletion fails
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
        """Update a checkpoint in a project.

        Args:
            project_id (str): The ID of the project to update the checkpoint in
            checkpoint_id (str): The ID of the checkpoint to update
            file_path (str | Path, optional): The path to the checkpoint file.
                If None, only the metadata of the checkpoint is updated
            model_format (str | FileType, optional): The format of the checkpoint file
                (must match the project's model format)
            checkpoint_name (str, optional): The display name of the checkpoint
            tag (str, optional): The tag of the checkpoint, for identifying the checkpoint
                with the data it was trained on
            **kwargs: Additional fields to update

        Returns:
            dict: The project with the updated checkpoint. See
            :class:`CheckpointHandler` or :class:`ProjectHandler` for the structure of the
            project dictionary and the checkpoint dictionary.

        Raises:
            ValueError: If file_path is provided but model_format or
                checkpoint_name is None
            HTTPError: If the update fails
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
        """Add an external checkpoint to a project.

        The external checkpoint is saved in the same bucket as the project.

        Args:
            project_id (str): The ID of the project to add the external checkpoint to
            file_path (str): The path to the external checkpoint file
            model_format (str | FileType): The format of the external checkpoint file
                (must match the project's model format)
            file_name (str, optional): The display name of the external checkpoint
            tag (str, optional): The tag of the external checkpoint, for identifying the
                external checkpoint with the data it was trained on
            **kwargs: Additional fields to include in the request

        Returns:
            dict: The project with the new external checkpoint. See
            :class:`CheckpointHandler` or :class:`ProjectHandler` for the structure of the
            project dictionary and the checkpoint dictionary.

        Raises:
            HTTPError: If the addition fails
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
        """Update an external checkpoint in a project.

        Args:
            project_id (str): The ID of the project containing the external checkpoint
            checkpoint_id (str): The ID of the external checkpoint to update
            model_format (str | FileType, optional): The format of the external
                checkpoint file
            file_path (str | Path, optional): The new path to the external checkpoint file
            file_name (str, optional): The new display name of the external checkpoint
            tag (str, optional): The new tag of the external checkpoint
            **kwargs: Additional fields to update

        Returns:
            dict: The project with the updated external checkpoint. See
            :class:`CheckpointHandler` or :class:`ProjectHandler` for the structure of the
            project dictionary and the checkpoint dictionary.

        Raises:
            HTTPError: If the update fails
        """
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
        """Trigger the calculation of summary scores and validation of a checkpoint.

        This method initiates background processing for a checkpoint, including
        calculation of summary scores and validation.

        Args:
            project_id (str): The ID of the project to trigger the file event for
            checkpoint_id (str): The ID of the checkpoint to trigger the file event for
            **kwargs: Additional parameters to include in the request

        Raises:
            HTTPError: If the file event trigger fails
        """
        data = {"projectId": project_id, "fileId": checkpoint_id}
        data.update(kwargs)
        self.post("/project/file_event", json=data)
