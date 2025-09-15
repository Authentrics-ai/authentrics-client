from __future__ import annotations

from .base_handler import BaseHandler

__all__ = ["UserHandler"]


class UserHandler(BaseHandler):
    """A handler for interacting with the Authentrics API user endpoints.

    Several methods return user dictionaries which contain current user information.

    The user dictionary contains:
        - id (str): Unique identifier for the user
        - username (str): User's username
        - emailAddress (str): User's email address
        - firstName (str): User's first name
        - lastName (str): User's last name
        - roles (list[str]): List of roles assigned to the user
        - enabled (bool): Whether the user account is enabled
    """

    def get_user(self) -> dict:
        """Get the current authenticated user's information.

        Returns:
            dict: The current user dictionary. See :class:`UserHandler` for
            the structure of the user dictionary.

        Raises:
            HTTPError: If the user is not authenticated or access is denied
        """
        return self.get("/api/auth/user").json()

    def update_user(
        self,
        *,
        username: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        password: str | None = None,
        **kwargs,
    ) -> None:
        """Update the current authenticated user's information.

        Args:
            username (str, optional): New username for the user
            email (str, optional): New email address for the user
            first_name (str, optional): New first name for the user
            last_name (str, optional): New last name for the user
            password (str, optional): New password for the user
            **kwargs: Additional fields to update

        Raises:
            HTTPError: If the update fails (e.g., username/email already exists,
            invalid data, insufficient permissions)

        Note:
            Only the fields that are provided (not None) will be updated.
            All other fields will remain unchanged.
        """
        data = {}
        if username is not None:
            data["username"] = username
        if email is not None:
            data["emailAddress"] = email
        if first_name is not None:
            data["firstName"] = first_name
        if last_name is not None:
            data["lastName"] = last_name
        if password is not None:
            data["password"] = password
        data.update(kwargs)

        self.patch("/api/auth/user", json=data)
