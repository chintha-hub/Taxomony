"""Render a :class:`FashionTaxonomy` into human-friendly text / markdown."""

from __future__ import annotations

from fashion_taxonomy.schemas import FashionTaxonomy

_SECTIONS: list[tuple[str, str]] = [
    ("Basic Classification", "basic_classification"),
    ("Material & Colour", "material_and_colour"),
    ("Details", "details"),
    ("Trend Analysis", "trend_analysis"),
    ("Market Positioning", "market_positioning"),
    ("AI Assessment", "ai_assessment"),
]


def _humanize(field: str) -> str:
    return field.replace("_", " ").title()


def _format_value(value: object) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "N/A"
    return str(value)


def to_markdown(taxonomy: FashionTaxonomy) -> str:
    """Render the taxonomy as Markdown (used by the Streamlit app)."""
    lines: list[str] = ["## Fashion Taxonomy Analysis"]
    for title, attr in _SECTIONS:
        section = getattr(taxonomy, attr)
        lines.append(f"\n### {title}")
        for field, value in section.model_dump().items():
            lines.append(f"- **{_humanize(field)}:** {_format_value(value)}")
    return "\n".join(lines)


def to_text(taxonomy: FashionTaxonomy) -> str:
    """Render the taxonomy as plain text (used by the CLI / .txt export)."""
    width = 72
    lines: list[str] = ["=" * width, "FASHION TAXONOMY ANALYSIS", "=" * width]
    for title, attr in _SECTIONS:
        section = getattr(taxonomy, attr)
        lines.append(f"\n{title.upper()}")
        lines.append("-" * len(title))
        for field, value in section.model_dump().items():
            lines.append(f"  {_humanize(field):<26}: {_format_value(value)}")
    lines.append("\n" + "=" * width)
    return "\n".join(lines)
