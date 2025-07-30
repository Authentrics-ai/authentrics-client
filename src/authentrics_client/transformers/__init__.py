try:
    import click  # noqa: F401
    import transformers  # noqa: F401
except ImportError:
    raise ImportError(
        "The transformers module requires the 'transformers' extra to be installed. "
        "Please install with: pip install authentrics-client[transformers]"
    ) from None

from .callback import AuthentricsCallback

__all__ = ["AuthentricsCallback"]
