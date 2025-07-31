try:
    import click  # noqa: F401
except ImportError:
    raise ImportError(
        "The CLI module requires the 'transformers' extra to be installed."
        " Please install with: pip install authentrics-client[transformers]"
    ) from None

from .cli import cli

__all__ = ["cli"]
