"""Tests for ImageInput value object."""

from __future__ import annotations

import pytest

from fashion_taxonomy.exceptions import ImageLoadError
from fashion_taxonomy.models import ImageInput


def test_from_bytes_and_data_url(sample_image: ImageInput) -> None:
    assert sample_image.mime_type == "image/png"
    assert sample_image.to_data_url().startswith("data:image/png;base64,")


def test_empty_data_rejected() -> None:
    with pytest.raises(ImageLoadError):
        ImageInput.from_bytes(b"", mime_type="image/png")


def test_unsupported_mime_rejected() -> None:
    with pytest.raises(ImageLoadError):
        ImageInput.from_bytes(b"abc", mime_type="image/tiff")


def test_from_path_missing_file() -> None:
    with pytest.raises(ImageLoadError):
        ImageInput.from_path("/no/such/image.jpg")


def test_from_path_reads_file(tmp_path, sample_image: ImageInput) -> None:
    p = tmp_path / "pic.png"
    p.write_bytes(sample_image.data)
    loaded = ImageInput.from_path(p)
    assert loaded.mime_type == "image/png"
    assert loaded.filename == "pic.png"
