from __future__ import annotations

from typing import Optional

from .base_client import BaseClient
from .handlers import (
    AdminHandler,
    AuthenticationHandler,
    BaseModelHandler,
    CheckpointHandler,
    DynamicHandler,
    MembershipHandler,
    ProjectHandler,
    ResultHandler,
    StaticHandler,
    UserHandler,
)

__all__ = ["AuthentricsClient"]

API_V2_BASE = "/api/v2"


class AuthentricsClient(BaseClient):
    """A client for interacting with the Authentrics API.

    For requests involving file uploads, use the
    :func:`authentrics_client.generate_multipart_json`
    function as the argument to the `files` keyword argument. For all other requests,
    use the `json` keyword argument.
    """

    def __init__(
        self,
        base_url: str,
        proxy_url: Optional[str] = None,
        api_version: Optional[str] = None,
    ) -> None:
        """Initialize the Authentrics client.

        Args:
            base_url: The base URL of the Authentrics API.
            proxy_url: Optional proxy URL to use for requests. If not provided, no proxy
            will be used.
            api_version: Optional API version (e.g. "v2"). If None, unversioned paths
            are used for backward compatibility.
        """
        super().__init__(base_url, proxy_url)
        self._api_version = (
            api_version.strip().lower() if api_version else None
        )
        self._session.headers["clientName"] = "authrx-client"

        self._admin = AdminHandler(self)
        self._auth = AuthenticationHandler(self)
        self._checkpoint = CheckpointHandler(self)
        self._dynamic = DynamicHandler(self)
        self._membership = MembershipHandler(self)
        self._project = ProjectHandler(self)
        self._static = StaticHandler(self)
        self._user = UserHandler(self)
        self._base_model = BaseModelHandler(self)
        self._result = ResultHandler(self)

    @property
    def api_version(self) -> Optional[str]:
        """The API version in use (e.g. "v2"), or None for unversioned paths."""
        return self._api_version

    def _full_path(self, resource_path: str) -> str:
        """Convert a resource path to the full request path.

        Leading slashes on resource_path are normalized (stripped) before building.
        When api_version is "v2", returns /api/v2/{resource_path}.
        When unversioned, uses legacy two-shape rule: auth* -> /api/{path}, else /{path}.
        """
        path = resource_path.lstrip("/")
        if self._api_version == "v2":
            return f"{API_V2_BASE}/{path}"
        if path.startswith("auth"):
            return f"/api/{path}"
        return f"/{path}"

    def _request(self, request_method, route: str, **kwargs):
        full_route = self._full_path(route)
        return super()._request(request_method, full_route, **kwargs)

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
    def base_model(self) -> BaseModelHandler:
        """Handles base model-related operations."""
        return self._base_model

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
    def result(self) -> ResultHandler:
        """Handler for interacting with analysis results in the Authentrics API."""
        return self._result

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
