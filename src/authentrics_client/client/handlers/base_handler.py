from ..base_client import BaseClient
from ..types import MethodType

__all__ = ["BaseHandler"]


class BaseHandler:
    """Base class for all API handlers.

    This class provides common functionality for making requests to the API
    using the session from the parent client.

    Usage:
        >>> client = BaseClient("https://api.authentrics.ai")
        >>> handler = BaseHandler(client)
        >>> handler._request(MethodType.GET, "/some/endpoint")
    """

    def __init__(self, client: BaseClient) -> None:
        """Initialize the handler with a client instance.

        Args:
            client: The BaseClient instance that provides the session and base URL
        """
        self._client = client
        self._session = client._session
        self._base_url = client.base_url

    def _request(self, request_method: MethodType, route: str, **kwargs):
        """Make a request to the API using the client's session.

        Args:
            request_method: The HTTP method to use
            route: The API route to request
            **kwargs: Additional arguments to pass to requests

        Returns:
            The response from the API

        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        response = self._session.request(
            request_method, self._base_url + route, **kwargs
        )
        response.raise_for_status()
        return response

    # Convenience methods for common HTTP methods
    def get(self, route: str, **kwargs):
        """Make a GET request."""
        return self._request(MethodType.GET, route, **kwargs)

    def post(self, route: str, **kwargs):
        """Make a POST request."""
        return self._request(MethodType.POST, route, **kwargs)

    def delete(self, route: str, **kwargs):
        """Make a DELETE request."""
        return self._request(MethodType.DELETE, route, **kwargs)

    def put(self, route: str, **kwargs):
        """Make a PUT request."""
        return self._request(MethodType.PUT, route, **kwargs)

    def patch(self, route: str, **kwargs):
        """Make a PATCH request."""
        return self._request(MethodType.PATCH, route, **kwargs)
