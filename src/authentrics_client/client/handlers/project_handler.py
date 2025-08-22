from pathlib import Path

from ..types import FileType, generate_multipart_json
from .base_handler import BaseHandler

__all__ = ["ProjectHandler"]


class ProjectHandler(BaseHandler):
    """A handler for interacting with the Authentrics API."""

    def get_projects(self) -> list[dict]:
        """Get all projects."""
        return self.get("/project").json()

    def get_project_by_id(self, project_id: str) -> dict:
        """Get a project by ID."""
        return self.get(f"/project/{project_id}").json()

    def get_project_metadata(self, project_id: str) -> dict:
        """Get the metadata for a project."""
        return self.get(f"/project/{project_id}/metadata").json()

    def get_project_by_name(self, name: str) -> dict | None:
        """Get a project by name."""
        projects = self.get_projects()
        for project in projects:
            if project["name"] == name:
                return project
        return None

    def create_project(
        self, name: str, description: str, model_format: str | FileType, **kwargs
    ) -> dict:
        """Create a project."""
        return self.post(
            "/project",
            json={
                "name": name,
                "description": description,
                "format": FileType(model_format).value,
                **kwargs,
            },
        ).json()

    def delete_project(self, *project_ids: str) -> None:
        """Delete one or more projects."""
        self.delete("/project", json=list(project_ids))

    def update_project(
        self,
        project_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        model_format: str | FileType | None = None,
        **kwargs,
    ) -> dict:
        """Update a project."""
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
        """Create a classification file."""
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
        """Delete a classification file."""
        return self.delete(
            "/project/classification_file",
        ).json()

    def update_classification_file(
        self,
        project_id: str,
        file_path: str | Path,
        **kwargs,
    ) -> dict:
        """Update a classification file."""
        data = {"projectId": project_id}
        data.update(kwargs)

        return self.put(
            "/project/classification_file",
            files=generate_multipart_json(file_path, **data),
        ).json()
