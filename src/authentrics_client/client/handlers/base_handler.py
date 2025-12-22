import json
from typing import Any

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

    # Private helper methods for data transformation
    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Convert snake_case string to camelCase."""
        components = snake_str.split('_')
        return components[0] + ''.join(x.capitalize() for x in components[1:])

    @staticmethod
    def _convert_dict_to_json(value: Any) -> Any:
        """Convert dict values to JSON strings, leave other types unchanged.

        Args:
            value: Value that may be a dict

        Returns:
            JSON string if value is a dict, otherwise the original value
        """
        if isinstance(value, dict):
            return json.dumps(value)
        return value

    def _convert_kwargs_to_camel_case(self, kwargs: dict) -> dict:
        """Convert snake_case keys in kwargs to camelCase.

        Args:
            kwargs: Dictionary with potentially snake_case keys

        Returns:
            Dictionary with camelCase keys
        """
        result = {}
        for key, value in kwargs.items():
            if '_' in key:
                # Standard camelCase conversion
                camel_key = self._to_camel_case(key)
            else:
                # Already camelCase or no conversion needed
                camel_key = key
            result[camel_key] = value
        return result
