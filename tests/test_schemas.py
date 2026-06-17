"""Tests for the taxonomy schema."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from fashion_taxonomy.schemas import FashionTaxonomy
from tests.conftest import SAMPLE_TAXONOMY_DICT


def test_valid_taxonomy_parses(sample_taxonomy: FashionTaxonomy) -> None:
    assert sample_taxonomy.basic_classification.category == "Dress"
    assert sample_taxonomy.material_and_colour.secondary_colour is None
    assert sample_taxonomy.market_positioning.comparable_brands == ["Reformation", "Sezane"]


def test_missing_required_field_raises() -> None:
    bad = {k: v for k, v in SAMPLE_TAXONOMY_DICT.items() if k != "details"}
    with pytest.raises(ValidationError):
        FashionTaxonomy.model_validate(bad)


def test_extra_field_is_forbidden() -> None:
    bad = {**SAMPLE_TAXONOMY_DICT, "unexpected": 123}
    with pytest.raises(ValidationError):
        FashionTaxonomy.model_validate(bad)


def test_roundtrip_json(sample_taxonomy: FashionTaxonomy) -> None:
    restored = FashionTaxonomy.model_validate_json(sample_taxonomy.model_dump_json())
    assert restored == sample_taxonomy


def test_json_schema_is_generatable() -> None:
    schema = FashionTaxonomy.model_json_schema()
    assert "basic_classification" in schema["properties"]
