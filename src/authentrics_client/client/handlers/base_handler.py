from ..base_client import BaseClient

__all__ = ["BaseHandler"]


class BaseHandler:
    """Base class for all API handlers.

    This class provides common functionality for making requests to the API
    using the session from the parent client.

    Usage:
        >>> client = BaseClient("https://api.authentrics.ai")
        >>> handler = BaseHandler(client)
        >>> handler.get("/some/endpoint")
    """

    def __init__(self, client: BaseClient) -> None:
        """Initialize the handler with a client instance.

        Args:
            client: The BaseClient instance that provides the session and base URL
        """
        self._client = client

    # Convenience methods for common HTTP methods
    def get(self, route: str, **kwargs):
        """Make a GET request."""
        return self._client.get(route, **kwargs)

    def post(self, route: str, **kwargs):
        """Make a POST request."""
        return self._client.post(route, **kwargs)

    def delete(self, route: str, **kwargs):
        """Make a DELETE request."""
        return self._client.delete(route, **kwargs)

    def put(self, route: str, **kwargs):
        """Make a PUT request."""
        return self._client.put(route, **kwargs)

    def patch(self, route: str, **kwargs):
        """Make a PATCH request."""
        return self._client.patch(route, **kwargs)
