from __future__ import annotations

from pathlib import Path

from ..types import FileType, generate_multipart_json
from .base_handler import BaseHandler

__all__ = ["ProjectHandler"]


class ProjectHandler(BaseHandler):
    """A handler for interacting with the Authentrics API project endpoints.

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

    def get_projects(self) -> list[dict]:
        """Get all projects.

        Returns:
            list[dict]: List of project dictionaries. See :class:`ProjectHandler`
                for the structure of the project dictionary.
        """
        return self.get("/project").json()

    def get_project_by_id(self, project_id: str) -> dict:
        """Get a project by its unique identifier.

        Args:
            project_id (str): The unique identifier of the project to retrieve

        Returns:
            dict: The project dictionary. See :class:`ProjectHandler` for the
                structure of the project dictionary.

        Raises:
            HTTPError: If the project is not found or access is denied
        """
        return self.get(f"/project/{project_id}").json()

    def get_model_metadata(self, project_id: str) -> dict:
        """Get the metadata for a project's model.

        Args:
            project_id (str): The unique identifier of the project

        Returns:
            dict: The model metadata dictionary containing information about
                the model's structure, parameters, and configuration

        Raises:
            HTTPError: If the project is not found or metadata is unavailable
        """
        return self.get(f"/project/{project_id}/metadata").json()

    def get_project_by_name(self, name: str) -> dict | None:
        """Get a project by its name.

        Args:
            name (str): The name of the project to search for

        Returns:
            dict | None: The project dictionary if found, None otherwise.
                See :class:`ProjectHandler` for the structure of the project dictionary.

        Note:
            This method performs a client-side search through all projects.
            For better performance with large numbers of projects, consider
            using :meth:`get_project_by_id` if you have the project ID.
        """
        projects = self.get_projects()
        for project in projects:
            if project["name"] == name:
                return project
        return None

    def create_project(
        self, name: str, description: str, model_format: str | FileType, **kwargs
    ) -> dict:
        """Create a new project.

        Args:
            name (str): The name of the project
            description (str): A description of the project
            model_format (str | FileType): The format of the model (e.g., 'ONNX',
                'HF_TEXT_GENERATION')
            **kwargs: Additional fields to include in the project creation request

        Returns:
            dict: The created project dictionary. See :class:`ProjectHandler` for
                the structure of the project dictionary.

        Raises:
            HTTPError: If the project creation fails (e.g., name already exists)
        """
        return self.post(
            "/project",
            json={
                "name": name,
                "description": description,
                "format": FileType(model_format).value,
                **kwargs,
            },
        ).json()

    def delete_project(self, *project_ids: str, hard_delete: bool | None = None) -> None:
        """Delete one or more projects.

        Args:
            *project_ids (str): One or more project IDs to delete
            hard_delete (bool, optional): Whether to permanently delete the projects.
                If not provided, projects will be soft deleted

        Raises:
            HTTPError: If the deletion fails (e.g., projects not found,
                insufficient permissions)

        Note:
            Soft deletion allows for potential recovery, while hard deletion
            permanently removes the projects and their data.
        """
        data = {"projectIds": list(project_ids)}
        if hard_delete is not None:
            data["hardDelete"] = bool(hard_delete)

        self.delete("/project", json=data)

    def update_project(
        self,
        project_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        model_format: str | FileType | None = None,
        **kwargs,
    ) -> dict:
        """Update a project's information.

        Args:
            project_id (str): The unique identifier of the project to update
            name (str, optional): The new name for the project
            description (str, optional): The new description for the project
            model_format (str | FileType, optional): The new model format for the project
            **kwargs: Additional fields to update

        Returns:
            dict: The updated project dictionary. See :class:`ProjectHandler` for
                the structure of the project dictionary.

        Raises:
            HTTPError: If the update fails (e.g., project not found, invalid data)
        """
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if model_format is not None:
            data["format"] = FileType(model_format).value
        data.update(kwargs)

        return self.patch(
            "/project",
            json={"projectId": project_id, **data},
        ).json()

    def create_classification_file(
        self,
        project_id: str,
        file_path: str | Path,
        **kwargs,
    ) -> dict:
        """Create a classification file for a project.

        Args:
            project_id (str): The unique identifier of the project
            file_path (str | Path): The path to the classification file to upload
            **kwargs: Additional fields to include in the upload request

        Returns:
            dict: The project dictionary with the new classification file.
                See :class:`ProjectHandler` for the structure of the project dictionary.

        Raises:
            FileNotFoundError: If the classification file doesn't exist
            HTTPError: If the upload fails
        """
        file_path = Path(file_path)
        if not file_path.is_file():
            raise FileNotFoundError(f"File {file_path} not found")
        data = {"projectId": project_id}
        data.update(kwargs)

        return self.post(
            "/project/classification_file",
            files=generate_multipart_json(file_path, **data),
        ).json()

    def delete_classification_file(self, project_id: str) -> dict:
        """Delete a classification file from a project.

        Args:
            project_id (str): The unique identifier of the project

        Returns:
            dict: The project dictionary after removing the classification file.
                See :class:`ProjectHandler` for the structure of the project dictionary.

        Raises:
            HTTPError: If the deletion fails (e.g., project not found,
                no classification file exists)
        """
        return self.delete(
            "/project/classification_file",
            json={"projectId": project_id},
        ).json()

    def update_classification_file(
        self,
        project_id: str,
        file_path: str | Path,
        **kwargs,
    ) -> dict:
        """Update a classification file for a project.

        Args:
            project_id (str): The unique identifier of the project
            file_path (str | Path): The path to the new classification file to upload
            **kwargs: Additional fields to include in the update request

        Returns:
            dict: The project dictionary with the updated classification file.
                See :class:`ProjectHandler` for the structure of the project dictionary.

        Raises:
            FileNotFoundError: If the classification file doesn't exist
            HTTPError: If the update fails
        """
        data = {"projectId": project_id}
        data.update(kwargs)

        return self.put(
            "/project/classification_file",
            files=generate_multipart_json(file_path, **data),
        ).json()
