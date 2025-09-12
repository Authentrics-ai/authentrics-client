from __future__ import annotations

from typing import Optional

from .base_handler import BaseHandler

__all__ = ["AdminHandler"]


class AdminHandler(BaseHandler):
    """Handler for the admin API.

    To access this API, you need to be logged in as an admin user.
    """

    def get_all_admins(self) -> list[dict]:
        """Get the info of all admins."""
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
        """Create a new admin user."""
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
        """Get all users."""
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
        """Create a new user."""
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
        """Delete a user."""
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
        """Update a user."""
        data = {"emailAddress": email}
        if roles is not None:
            data["roles"] = roles
        if enabled is not None:
            data["enabled"] = enabled
        data.update(kwargs)
        self.patch(f"/api/auth/admin/{user_id}", json=data)

    def delete_user(self, user_id: str, email: str) -> None:
        """Delete a user."""
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
        """Update a user."""
        data = {"emailAddress": email}
        if roles is not None:
            data["roles"] = roles
        if enabled is not None:
            data["enabled"] = enabled
        data.update(kwargs)
        self.patch(f"/api/auth/admin/user/{user_id}", json=data)

    def get_user_by_email(self, email: str) -> dict | None:
        """Get a user by email."""
        all_users = self.get_all_users()
        for user in all_users:
            if user["emailAddress"] == email:
                return user
        return None
