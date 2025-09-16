from __future__ import annotations

from typing import Optional

from .base_client import BaseClient
from .handlers import (
    AdminHandler,
    AuthenticationHandler,
    CheckpointHandler,
    DynamicHandler,
    MembershipHandler,
    ProjectHandler,
    StaticHandler,
    UserHandler,
)

__all__ = ["AuthentricsClient"]


class AuthentricsClient(BaseClient):
    """A client for interacting with the Authentrics API.

    Use the built-in handlers to make standard requests to the API. For custom requests,
    use the get/post/etc. methods from :class:`BaseClient`.
    """

    def __init__(self, base_url: str, proxy_url: Optional[str] = None) -> None:
        super().__init__(base_url, proxy_url)
        self._session.headers["clientName"] = "authrx-client"

        self._admin = AdminHandler(self)
        self._auth = AuthenticationHandler(self)
        self._checkpoint = CheckpointHandler(self)
        self._dynamic = DynamicHandler(self)
        self._membership = MembershipHandler(self)
        self._project = ProjectHandler(self)
        self._static = StaticHandler(self)
        self._user = UserHandler(self)

    @property
    def admin(self) -> AdminHandler:
        """The admin handler for the Authentrics API. Can only be used by admins."""
        return self._admin

    @property
    def auth(self) -> AuthenticationHandler:
        """The authentication handler for the Authentrics API."""
        return self._auth

    @property
    def checkpoint(self) -> CheckpointHandler:
        """Handles checkpoint-related operations."""
        return self._checkpoint

    @property
    def dynamic(self) -> DynamicHandler:
        """Handler for running dynamic analysis (analysis during inference) on a
        checkpoint.
        """
        return self._dynamic

    @property
    def membership(self) -> MembershipHandler:
        """Handles membership-related operations."""
        return self._membership

    @property
    def project(self) -> ProjectHandler:
        """Handles project-related operations."""
        return self._project

    @property
    def static(self) -> StaticHandler:
        """Handler for running static analysis on a checkpoint."""
        return self._static

    @property
    def user(self) -> UserHandler:
        """Handles operations a user can perform on their own account."""
        return self._user

    @property
    def client_name(self) -> str:
        """The client name for the session."""
        return str(self._session.headers["clientName"])

    @client_name.setter
    def client_name(self, client_name: str) -> None:
        """Set the client name for the session."""
        self._session.headers["clientName"] = client_name
