import os
from datetime import datetime
from getpass import getpass

import jwt
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
            self._validate_and_set_token(token)
            return

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
        self._validate_and_set_token(token)

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

    def _validate_and_set_token(self, token: str) -> None:
        """Validate a token.

        If the token is invalid, the old authorization header will be restored.
        """

        decoded = decode_token(token)
        if decoded["exp"] < datetime.now().timestamp():
            raise ValueError("Token has expired")

        old_authorization = self._session.headers.get("Authorization")
        self._session.headers["Authorization"] = f"Bearer {token}"

        # Is this a valid user token?
        try:
            self.get("/api/auth/user")
            return
        except requests.HTTPError:
            pass

        # Is this a valid admin token?
        try:
            self.get("/api/auth/admin")
            return
        except requests.HTTPError:
            pass

        if old_authorization is not None:
            self._session.headers["Authorization"] = old_authorization
        else:
            self._session.headers.pop("Authorization")

        raise ValueError("Invalid token")


def decode_token(token: str) -> dict:
    """Decode a JWT token using the HS384 algorithm.

    Args:
        token: The JWT token to decode

    Returns:
        The decoded token payload as a dictionary

    Raises:
        jwt.InvalidTokenError: If the token is invalid or cannot be decoded
        ValueError: If the token is invalid or cannot be decoded
    """
    try:
        decoded = jwt.decode(
            token,
            algorithms=["HS384"],
            options={"verify_signature": False},
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired") from None
    except jwt.InvalidSignatureError:
        raise ValueError("Invalid token signature") from None
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}") from None
