from .base_handler import BaseHandler

__all__ = ["MembershipHandler"]


class MembershipHandler(BaseHandler):
    """A handler for interacting with the Authentrics API membership endpoints."""

    def get_users_on_project(self, project_id: str) -> list[dict]:
        """Get all users on a project."""
        return self.get(f"/project/{project_id}/user").json()

    def add_user_to_project(
        self, project_id: str, email: str, permissions: list[str], **kwargs
    ) -> dict:
        """Add a user to a project."""
        return self.post(
            f"/project/{project_id}/user",
            json={"email": email, "permissions": permissions, **kwargs},
        ).json()

    def delete_user_from_project(self, project_id: str, user_id: str) -> None:
        """Delete a user from a project."""
        self.delete(f"/project/{project_id}/user/{user_id}")

    def update_user_permissions(
        self,
        project_id: str,
        user_id: str,
        permissions: list[str],
        **kwargs,
    ) -> dict:
        """Update a user's permissions on a project."""
        data = {"permissions": permissions}
        data.update(kwargs)

        return self.patch(
            f"/project/{project_id}/user/{user_id}",
            json=data,
        ).json()
