import os
from getpass import getpass

import requests

from .base_handler import BaseHandler

__all__ = ["AuthenticationHandler"]


class AuthenticationHandler(BaseHandler):
    """A handler for interacting with the Authentrics API authentication endpoints."""

    def login(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
    ):
        """Login to the Authentrics API.

        Keyword Args:
            username: Optional username to use for login
            password: Optional password to use for login
            token: Optional token to use for login

        For both username and password, the environment variables `AAI_USERNAME` and
        `AAI_PASSWORD` will be used if they are not provided. If those are not set, the
        user will be prompted for input.
        """

        if token is not None:
            old_authorization = self._session.headers.get("Authorization")
            self._session.headers["Authorization"] = f"Bearer {token}"
            try:
                self.get("/project")
                return
            except requests.HTTPError as e:
                if old_authorization is not None:
                    self._session.headers["Authorization"] = old_authorization
                else:
                    self._session.headers.pop("Authorization")

                if e.response.status_code == 401:
                    raise ValueError("Expired token") from e
                elif e.response.status_code == 403:
                    raise ValueError("Invalid token") from e
                else:
                    raise e

        username = username or os.getenv("AAI_USERNAME")
        password = password or os.getenv("AAI_PASSWORD")
        if username is None:
            username = input("Username: ")
        if password is None:
            password = getpass()

        token = self.post(
            "/api/auth/login",
            json={"username": username, "password": password},
        ).content.decode()
        self._session.headers["Authorization"] = f"Bearer {token}"

    def register(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> None:
        """Register a new user."""
        self.post(
            "/api/auth/register",
            json={
                "username": username,
                "emailAddress": email,
                "password": password,
                "firstName": first_name,
                "lastName": last_name,
            },
        )
