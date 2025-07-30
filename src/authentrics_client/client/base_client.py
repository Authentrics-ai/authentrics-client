from typing import Optional

import requests

from .types import MethodType

__all__ = ["BaseClient"]


class BaseClient:
    """A client for interacting with a given URL.

    Usage:
        >>> client = BaseClient("https://api.authentrics.ai")
        >>> client.get("/v3/api-docs")
        >>> client.post("/project", json={"name": "test", "description": "test", "format": "onnx"})
    """

    def __init__(self, base_url: str, proxy_url: Optional[str] = None) -> None:
        """A client for interacting with a given URL.

        Args:
            base_url: The base URL of the API server
            proxy_url: Optional proxy URL (e.g., 'socks5h://localhost:1080')
        """
        self.base_url = base_url
        """The parsed base URL of the API server."""

        self._session = requests.Session()
        """The requests session for the API server."""
        parsed_url = requests.models.parse_url(base_url)
        assert parsed_url.path is None or parsed_url.path == "/"
        assert parsed_url.query is None
        assert parsed_url.fragment is None

        self.base_url = parsed_url.url.rstrip("/")

        if proxy_url:
            self._session.proxies = {"http": proxy_url, "https": proxy_url}

    def _request(self, request_method: MethodType, route: str, **kwargs):
        """A helper method for making requests to the API server."""
        response = self._session.request(
            request_method, self.base_url + route, **kwargs
        )
        response.raise_for_status()
        return response

    # REST methods
    def get(self, route: str, **kwargs):
        return self._request(MethodType.GET, route, **kwargs)

    def post(self, route: str, **kwargs):
        return self._request(MethodType.POST, route, **kwargs)

    def delete(self, route: str, **kwargs):
        return self._request(MethodType.DELETE, route, **kwargs)

    def put(self, route: str, **kwargs):
        return self._request(MethodType.PUT, route, **kwargs)

    def patch(self, route: str, **kwargs):
        return self._request(MethodType.PATCH, route, **kwargs)
