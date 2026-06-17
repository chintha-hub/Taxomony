"""Lightweight value objects shared across the package."""

from __future__ import annotations

import base64
import mimetypes
from dataclasses import dataclass
from pathlib import Path

from fashion_taxonomy.exceptions import ImageLoadError

SUPPORTED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@dataclass(frozen=True)
class ImageInput:
    """An in-memory image to be analyzed.

    Attributes:
        data: Raw image bytes.
        mime_type: e.g. ``image/jpeg`` or ``image/png``.
        filename: Optional original filename (for display/logging).
    """

    data: bytes
    mime_type: str
    filename: str | None = None

    def __post_init__(self) -> None:
        if not self.data:
            raise ImageLoadError("Image data is empty.")
        if self.mime_type not in SUPPORTED_MIME_TYPES:
            raise ImageLoadError(
                f"Unsupported image type {self.mime_type!r}. "
                f"Supported: {', '.join(sorted(SUPPORTED_MIME_TYPES))}."
            )

    @classmethod
    def from_path(cls, path: str | Path) -> ImageInput:
        """Load an image from disk, inferring its MIME type."""
        p = Path(path)
        if not p.is_file():
            raise ImageLoadError(f"No such file: {p}")
        mime, _ = mimetypes.guess_type(p.name)
        if mime is None:
            raise ImageLoadError(f"Could not determine image type for {p.name!r}.")
        return cls(data=p.read_bytes(), mime_type=mime, filename=p.name)

    @classmethod
    def from_bytes(cls, data: bytes, mime_type: str, filename: str | None = None) -> ImageInput:
        """Build an :class:`ImageInput` from raw bytes (e.g. a web upload)."""
        return cls(data=data, mime_type=mime_type, filename=filename)

    def to_base64(self) -> str:
        """Return the image as a base64-encoded ASCII string."""
        return base64.standard_b64encode(self.data).decode("utf-8")

    def to_data_url(self) -> str:
        """Return a ``data:`` URL suitable for OpenAI's image_url content."""
        return f"data:{self.mime_type};base64,{self.to_base64()}"
