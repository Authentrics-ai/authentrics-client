from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Optional

__all__ = ["FileType", "ComparisonType", "MOEAnalysisType"]


class MethodType(Enum):
    """The type of HTTP method to use for a request.

    Attributes:
        GET: GET request
        POST: POST request
        PUT: PUT request
        DELETE: DELETE request
        PATCH: PATCH request
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ComparisonType(Enum):
    """The type of comparison to perform.

    Attributes:
        LATEST: Compare to the latest checkpoint
        CHOSEN: Compare to the chosen checkpoint
    """

    LATEST = "LATEST"
    CHOSEN = "CHOSEN"


class MOEAnalysisType(Enum):
    """The type of MoE analysis to perform.

    Attributes:
        EXPERT: Expert analysis
        ROUTER: Router analysis
    """

    EXPERT = "EXPERT"
    ROUTER = "ROUTER"


def generate_multipart_json(
    filepath: Path | str | None, **kwargs
) -> dict[str, tuple[Optional[str], Any, Optional[str]]]:
    """Generate a multipart/form-data request.

    If the filepath is a directory, it will be tarred and included as a file field.

    Args:
        filepath: The path to the file to include in the request. If None, the file is
        not included in the request.
        **kwargs: Additional form fields to include in the request. By default, the file
        is included as a file field and these are added as text/plain fields.

    Returns:
        A dictionary of form fields to include in the request

    Note:
        The `file` field is always included as the last field as the triple
        `(<filename>, <file>, <content_type=None>)`. The other fields are added as
        `(None, <value>, <content_type="text/plain">)`.
    """

    d: dict[str, tuple[Optional[str], Any, Optional[str]]] = {}

    for name, value in kwargs.items():
        if isinstance(value, (str, bytes, int, float, bool)):
            d[name] = (None, value, "text/plain")
        elif isinstance(value, (list, tuple)):
            d[name] = (None, ",".join(str(v) for v in value), "text/plain")
        elif isinstance(value, dict):
            d[name] = (None, json.dumps(value), "text/plain")
        else:
            raise ValueError(f"Unsupported type: {type(value)}")

    if filepath is None:
        return d

    filepath = Path(filepath)

    if filepath.is_dir():
        raise ValueError("Directory uploads are not supported")
    if not filepath.is_file():
        raise FileNotFoundError(f"Could not locate file at {filepath}")

    # Open the file in binary mode and pass it directly to requests
    d["file"] = (filepath.name, open(filepath, "rb"), None)

    return d


class FileType(Enum):
    """The type of a model checkpoint.

    Attributes:
        ONNX: ONNX file
        KERAS: Keras file
        HF_TEXT: Hugging Face checkpoint file for text generation (e.g., Llama)
        HF_IT2T: Hugging Face checkpoint file for image text to text (e.g., Gemma)
    """

    ONNX = "ONNX"
    """ONNX file"""
    KERAS = "KERAS"
    """Keras file"""
    HF_TEXT = "HF_TEXT_GENERATION"
    """Hugging Face checkpoint file for text generation (e.g., Llama)"""
    HF_IT2T = "HF_IMAGE_TEXT_TO_TEXT"
    """Hugging Face checkpoint file for image text to text (e.g., Gemma)"""
