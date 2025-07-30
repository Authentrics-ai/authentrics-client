try:
    import transformers  # noqa: F401
    import click  # noqa: F401
except ImportError:
    raise ImportError(
        "The transformers module requires the 'transformers' extra to be installed. "
        "Please install with: pip install authentrics-api[transformers]"
    )

from .callback import AuthentricsCallback

__all__ = ["AuthentricsCallback"]
