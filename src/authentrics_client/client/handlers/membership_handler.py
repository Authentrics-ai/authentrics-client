from .base_handler import BaseHandler

__all__ = ["MembershipHandler"]


class MembershipHandler(BaseHandler):
    """A handler for interacting with the Authentrics API membership endpoints.

    Several methods return user dictionaries which contain user information
    and project-specific permissions.

    The user dictionary contains:
        - id (str): Unique identifier for the user
        - userId (str): User's email address
        - projectId (str): Project's unique identifier
        - permissions (list[str]): List of permissions for the project
        - joinedDate (str): ISO timestamp when the user joined the project
        - lastActivityDate (str): ISO timestamp when the user last interacted with the
            project
    """

    def get_project_members(self, project_id: str) -> list[dict]:
        """Get all members of a project.

        Args:
            project_id (str): The unique identifier of the project

        Returns:
            list[dict]: List of membership dictionaries with project membership
            information. See :class:`MembershipHandler` for the structure of the
            membership dictionary.

        Raises:
            HTTPError: If the project is not found or access is denied
        """
        return self.get(f"/project/{project_id}/user").json()

    def add_project_member(
        self,
        *,
        project_id: str,
        email: str,
        permissions: list[str],
        **kwargs,
    ) -> dict:
        """Add a member to a project.

        Args:
            project_id (str): The unique identifier of the project
            email (str): The email address of the user to add as a member
            permissions (list[str]): List of permissions to grant to the user
                (e.g., 'read', 'write', 'admin')
            **kwargs: Additional fields to include in the membership creation request

        Returns:
            dict: The membership dictionary with project membership information.
            See :class:`MembershipHandler` for the structure of the membership
            dictionary.

        Raises:
            HTTPError: If the user addition fails (e.g., user not found,
                insufficient permissions, user already a member)
        """
        return self.post(
            f"/project/{project_id}/user",
            json={"emailAddress": email, "permissions": permissions, **kwargs},
        ).json()

    def delete_project_member(self, project_id: str, user_id: str) -> None:
        """Remove a member from a project.

        Args:
            project_id (str): The unique identifier of the project
            user_id (str): The unique identifier of the user to remove

        Raises:
            HTTPError: If the removal fails (e.g., user not found, insufficient
                permissions, user not a member)
        """
        self.delete(f"/project/{project_id}/user/{user_id}")

    def update_project_member(
        self,
        *,
        project_id: str,
        user_id: str,
        permissions: list[str],
        **kwargs,
    ) -> dict:
        """Update a member's permissions and details on a project.

        Args:
            project_id (str): The unique identifier of the project
            user_id (str): The unique identifier of the user to update
            permissions (list[str]): New list of permissions for the user
                (e.g., 'read', 'write', 'admin')
            **kwargs: Additional fields to update

        Returns:
            dict: The updated membership dictionary with project membership information.
            See :class:`MembershipHandler` for the structure of the membership
            dictionary.

        Raises:
            HTTPError: If the update fails (e.g., user not found, insufficient
                permissions, invalid permissions)
        """
        data = {"permissions": permissions}
        data.update(kwargs)

        return self.patch(
            f"/project/{project_id}/user/{user_id}",
            json=data,
        ).json()
