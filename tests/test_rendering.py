"""Tests for taxonomy rendering."""

from __future__ import annotations

from fashion_taxonomy.rendering import to_markdown, to_text
from fashion_taxonomy.schemas import FashionTaxonomy


def test_markdown_contains_sections_and_values(sample_taxonomy: FashionTaxonomy) -> None:
    md = to_markdown(sample_taxonomy)
    assert "## Fashion Taxonomy Analysis" in md
    assert "### Basic Classification" in md
    assert "Midi Dress" in md
    # list values are joined
    assert "Reformation, Sezane" in md


def test_text_handles_none_as_na(sample_taxonomy: FashionTaxonomy) -> None:
    txt = to_text(sample_taxonomy)
    assert "FASHION TAXONOMY ANALYSIS" in txt
    # secondary_colour is None -> rendered as N/A
    assert "N/A" in txt


def test_prompt_is_nonempty() -> None:
    from fashion_taxonomy.prompts import build_analysis_prompt

    assert "TREND ANALYSIS" in build_analysis_prompt()
