from .base_handler import BaseHandler

__all__ = ["MembershipHandler"]


class MembershipHandler(BaseHandler):
    """A handler for interacting with the Authentrics API membership endpoints."""

    def get_project_members(self, project_id: str) -> list[dict]:
        """Get all members on a project."""
        return self.get(f"/project/{project_id}/user").json()

    def add_project_member(
        self,
        *,
        project_id: str,
        email: str,
        permissions: list[str],
        **kwargs,
    ) -> dict:
        """Add a member to a project."""
        return self.post(
            f"/project/{project_id}/user",
            json={"emailAddress": email, "permissions": permissions, **kwargs},
        ).json()

    def delete_project_member(self, project_id: str, user_id: str) -> None:
        """Delete a member from a project."""
        self.delete(f"/project/{project_id}/user/{user_id}")

    def update_project_member(
        self,
        *,
        project_id: str,
        user_id: str,
        permissions: list[str],
        **kwargs,
    ) -> dict:
        """Update a member's details on a project."""
        data = {"permissions": permissions}
        data.update(kwargs)

        return self.patch(
            f"/project/{project_id}/user/{user_id}",
            json=data,
        ).json()
