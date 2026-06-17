"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.providers.base import VisionProvider
from fashion_taxonomy.schemas import FashionTaxonomy

# A minimal valid 1x1 PNG (so tests need no real image files or network).
_PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c6360000002000154a24f6e0000000049454e44ae426082"
)

SAMPLE_TAXONOMY_DICT = {
    "basic_classification": {
        "category": "Dress",
        "sub_category": "Midi Dress",
        "silhouette": "A-line",
        "neckline": "V-neck",
        "sleeve": "Short",
        "length": "Midi",
    },
    "material_and_colour": {
        "material": "Cotton",
        "primary_colour": "Ivory",
        "secondary_colour": None,
        "print_texture": "Floral",
    },
    "details": {
        "key_detail": "Ruffle hem",
        "fabric_weight": "Lightweight",
        "finish": "Matte",
    },
    "trend_analysis": {
        "trend_signal": "Utility femininity",
        "trend_confidence": "High",
        "why_this_trend": "Soft florals with a practical silhouette.",
    },
    "market_positioning": {
        "market_level": "Premium",
        "target_customer": "Women 25-40, romantic, work-to-weekend.",
        "season": "SS26",
        "comparable_brands": ["Reformation", "Sezane"],
    },
    "ai_assessment": {
        "classification_difficulty": "Easy",
        "why_difficult": None,
        "ai_training_recommendation": "Good canonical example of a floral midi.",
    },
}


@pytest.fixture
def sample_taxonomy() -> FashionTaxonomy:
    return FashionTaxonomy.model_validate(SAMPLE_TAXONOMY_DICT)


@pytest.fixture
def sample_image() -> ImageInput:
    return ImageInput.from_bytes(_PNG_1X1, mime_type="image/png", filename="sample.png")


class FakeProvider(VisionProvider):
    """A provider that returns a canned taxonomy — no network, no keys."""

    name = "fake"

    def __init__(self, taxonomy: FashionTaxonomy) -> None:
        self._taxonomy = taxonomy
        self.calls: list[tuple[str | None, str]] = []

    def analyze(self, image: ImageInput, prompt: str) -> FashionTaxonomy:
        self.calls.append((image.filename, prompt))
        return self._taxonomy


@pytest.fixture
def fake_provider(sample_taxonomy: FashionTaxonomy) -> FakeProvider:
    return FakeProvider(sample_taxonomy)
