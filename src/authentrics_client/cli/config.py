"""Configuration module for Authentrics client."""

from pathlib import Path

import platformdirs

# Cache directory configuration
BASE_DIR = Path(
    platformdirs.user_cache_dir(
        "authrx",
        "Authentrics.ai",
        ensure_exists=True,
    )
)
TOKEN_PATH = BASE_DIR / "token.json"
