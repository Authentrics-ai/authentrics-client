from .base_handler import BaseHandler

__all__ = ["UserHandler"]


class UserHandler(BaseHandler):
    """A handler for interacting with the Authentrics API user endpoints."""

    def get_user(self) -> dict:
        """Get the current user."""
        return self.get("/api/auth/user").json()

    def update_user(
        self,
        username: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        password: str | None = None,
    ) -> None:
        """Update the current user."""
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

        self.patch(
            "/api/auth/user",
            json=data,
        )
