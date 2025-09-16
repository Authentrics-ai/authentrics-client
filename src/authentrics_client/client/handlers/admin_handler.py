from __future__ import annotations

from typing import Optional

from .base_handler import BaseHandler

__all__ = ["AdminHandler"]


class AdminHandler(BaseHandler):
    """Handler for the admin API.

    To access this API, you need to be logged in as an admin user.
    """

    def get_all_admins(self) -> list[dict]:
        """Get information about all admin users.

        Returns:
            list[dict]: List of admin user dictionaries. Each dictionary contains:
                - id (str): Unique identifier for the admin
                - username (str): Admin's username
                - emailAddress (str): Admin's email address
                - firstName (str): Admin's first name
                - lastName (str): Admin's last name
                - roles (list[str]): List of roles assigned to the admin
                - enabled (bool): Whether the admin account is enabled
        """
        return self.get("/api/auth/admin").json()

    def create_admin(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **kwargs,
    ) -> None:
        """Create a new admin user.

        Args:
            username (str): Unique username for the admin user
            email (str): Email address for the admin user
            password (str): Password for the admin user
            first_name (str): First name of the admin user
            last_name (str): Last name of the admin user
            **kwargs: Additional fields to include in the admin creation request

        Raises:
            HTTPError: If the admin creation fails (e.g., username/email already exists)
        """
        self.post(
            "/api/auth/admin",
            json={
                "username": username,
                "emailAddress": email,
                "password": password,
                "firstName": first_name,
                "lastName": last_name,
                **kwargs,
            },
        )

    def get_all_users(self) -> list[dict]:
        """Get information about all regular users.

        Returns:
            list[dict]: List of user dictionaries. Each dictionary contains:
                - id (str): Unique identifier for the user
                - username (str): User's username
                - emailAddress (str): User's email address
                - firstName (str): User's first name
                - lastName (str): User's last name
                - roles (list[str]): List of roles assigned to the user
                - enabled (bool): Whether the user account is enabled
        """
        return self.get("/api/auth/admin/user").json()

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **kwargs,
    ) -> None:
        """Create a new regular user.

        Args:
            username (str): Unique username for the user
            email (str): Email address for the user
            password (str): Password for the user
            first_name (str): First name of the user
            last_name (str): Last name of the user
            **kwargs: Additional fields to include in the user creation request

        Raises:
            HTTPError: If the user creation fails (e.g., username/email already exists)
        """
        self.post(
            "/api/auth/admin/user",
            json={
                "username": username,
                "emailAddress": email,
                "password": password,
                "firstName": first_name,
                "lastName": last_name,
                **kwargs,
            },
        )

    def delete_admin(self, user_id: str, email: str) -> None:
        """Delete an admin user.

        Args:
            user_id (str): Unique identifier of the admin to delete
            email (str): Email address of the admin to delete (for verification)

        Raises:
            HTTPError: If the admin deletion fails (e.g., admin not found,
                insufficient permissions)
        """
        self.delete(f"/api/auth/admin/{user_id}", json={"emailAddress": email})

    def update_admin(
        self,
        user_id: str,
        email: str,
        *,
        roles: Optional[list[str]] = None,
        enabled: Optional[bool] = None,
        **kwargs,
    ) -> None:
        """Update an admin user's information.

        Args:
            user_id (str): Unique identifier of the admin to update
            email (str): Email address of the admin to update (for verification)
            roles (list[str], optional): New list of roles to assign to the admin
            enabled (bool, optional): Whether to enable or disable the admin account
            **kwargs: Additional fields to update

        Raises:
            HTTPError: If the admin update fails (e.g., admin not found, invalid data)
        """
        data = {"emailAddress": email}
        if roles is not None:
            data["roles"] = roles
        if enabled is not None:
            data["enabled"] = enabled
        data.update(kwargs)
        self.patch(f"/api/auth/admin/{user_id}", json=data)

    def delete_user(self, user_id: str, email: str) -> None:
        """Delete a regular user.

        Args:
            user_id (str): Unique identifier of the user to delete
            email (str): Email address of the user to delete (for verification)

        Raises:
            HTTPError: If the user deletion fails (e.g., user not found,
                insufficient permissions)
        """
        self.delete(f"/api/auth/admin/user/{user_id}", json={"emailAddress": email})

    def update_user(
        self,
        user_id: str,
        email: str,
        *,
        roles: list[str] | None = None,
        enabled: bool | None = None,
        **kwargs,
    ) -> None:
        """Update a regular user's information.

        Args:
            user_id (str): Unique identifier of the user to update
            email (str): Email address of the user to update (for verification)
            roles (list[str], optional): New list of roles to assign to the user
            enabled (bool, optional): Whether to enable or disable the user account
            **kwargs: Additional fields to update

        Raises:
            HTTPError: If the user update fails (e.g., user not found, invalid data)
        """
        data = {"emailAddress": email}
        if roles is not None:
            data["roles"] = roles
        if enabled is not None:
            data["enabled"] = enabled
        data.update(kwargs)
        self.patch(f"/api/auth/admin/user/{user_id}", json=data)

    def get_user_by_email(self, email: str) -> dict | None:
        """Get a user by their email address.

        Args:
            email (str): Email address to search for

        Returns:
            dict | None: User dictionary if found, None otherwise.
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user["emailAddress"] == email:
                return user
        return None
