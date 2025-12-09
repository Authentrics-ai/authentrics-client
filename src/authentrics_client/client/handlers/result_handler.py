from __future__ import annotations

import warnings
from pathlib import Path

from .base_handler import BaseHandler

__all__ = ["ResultHandler"]


class ResultHandler(BaseHandler):
    """A handler for interacting with analysis results in the Authentrics API."""

    # ---------------------------------------------------------
    # LIST RESULTS (metadata)
    # ---------------------------------------------------------
    def getAnalysisResults(self, project_id: str) -> list[dict]:
        """
        Get all analysis result metadata for a project.
        """
        response = self.get(f"/project/{project_id}/analysis/result")
        response.raise_for_status()
        return response.json()

    # ---------------------------------------------------------
    # GET RESULT BY REQUEST ID (metadata)
    # ---------------------------------------------------------
    def getAnalysisResultByRequestId(
        self, project_id: str, request_id: str
    ) -> list[dict]:
        """
        Get analysis result metadata for a single requestId.
        """
        response = self.get(
            f"/project/{project_id}/analysis/result",
            params={"requestId": request_id},
        )
        response.raise_for_status()
        return response.json()

    # ---------------------------------------------------------
    # GET SIGNED URL (default mode is SIGNED on backend)
    # ---------------------------------------------------------
    def getAnalysisResultArtifactSignedUrl(
        self, project_id: str, request_id: str
    ) -> dict:
        """
        Get a signed URL for downloading the analysis result artifact.
        Backend defaults to SIGNED mode when mode is omitted.
        """
        response = self.get(
            f"/project/{project_id}/analysis/result/artifact",
            params={"requestId": request_id},
        )
        response.raise_for_status()
        return response.json()

    # ---------------------------------------------------------
    # DOWNLOAD ARTIFACT (STREAM mode)
    # ---------------------------------------------------------
    def downloadAnalysisResultArtifact(
        self,
        project_id: str,
        request_id: str,
        file_path: str | Path,
        *,
        overwrite: bool = True,
    ) -> None:
        """
        Download the analysis result artifact (streams bytes).
        """
        file_path = Path(file_path)

        if file_path.exists() and not overwrite:
            raise FileExistsError(f"File {file_path} already exists.")

        response = self.get(
            f"/project/{project_id}/analysis/result/artifact",
            params={"requestId": request_id, "mode": "STREAM"},
            stream=True,
        )

        # Fail early if server returned error JSON
        try:
            response.raise_for_status()
        except Exception:
            print("Error response:", response.text)
            raise

        # Backend sets "application/octet-stream" for streaming mode
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("application"):
            warnings.warn(
                f"Unexpected content type '{content_type}'. "
                f"The response might not be a valid artifact.",
                stacklevel=1,
            )

        # Stream to file
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
