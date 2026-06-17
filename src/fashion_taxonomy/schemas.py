"""Structured taxonomy schema.

These Pydantic models are the contract for what the AI returns. Using a schema
(instead of free text) means the output is validated, typed, queryable, and
easy to store in a database or serialize to JSON.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class _Section(BaseModel):
    """Base for taxonomy sections — forbids unexpected fields."""

    model_config = ConfigDict(extra="forbid")


class BasicClassification(_Section):
    category: str = Field(
        description="Tops / Bottoms / Dress / Outerwear / Knitwear / Accessories / Footwear"
    )
    sub_category: str = Field(description="e.g. Blouse, Midi Dress, Trench Coat")
    silhouette: str = Field(
        description="A-line / Straight / Oversized / Fitted / Relaxed / Wrap / Asymmetric / Boxy"
    )
    neckline: str = Field(
        description=(
            "V-neck / Round / Square / Off-shoulder / Halter / Collared / "
            "Strapless / Cowl / N/A"
        )
    )
    sleeve: str = Field(
        description="Sleeveless / Short / Long / 3-4 / Puff / Rolled / Cape / Draped / N/A"
    )
    length: str = Field(
        description="Crop / Short / Midi / Maxi / Mini / Standard / Knee / Ankle"
    )


class MaterialAndColour(_Section):
    material: str = Field(
        description=(
            "Cotton / Silk / Linen / Denim / Leather / Knit / Chiffon / "
            "Satin / Wool / Synthetic"
        )
    )
    primary_colour: str = Field(description="Named colour, e.g. Ivory, Navy, Burgundy")
    secondary_colour: str | None = Field(default=None, description="Secondary colour, if any")
    print_texture: str = Field(
        description=(
            "Solid / Floral / Stripe / Check / Abstract / Geometric / "
            "Embroidered / Textured"
        )
    )


class Details(_Section):
    key_detail: str = Field(
        description="The standout detail: Ruffle, Pocket, Belt, Cut-out, Draping, etc."
    )
    fabric_weight: str = Field(description="Lightweight / Medium / Heavyweight")
    finish: str = Field(description="Matte / Glossy / Textured")


class TrendAnalysis(_Section):
    trend_signal: str = Field(
        description=(
            "Utility femininity / Sheer layering / Tactile surfaces / "
            "Oversized tailoring / Quiet luxury / Maximalism / Streetwear / "
            "Heritage / Other"
        )
    )
    trend_confidence: str = Field(description="High / Medium / Low / Edge Case")
    why_this_trend: str = Field(description="1-2 sentence justification")


class MarketPositioning(_Section):
    market_level: str = Field(
        description="Luxury / Premium / Mid-market / Fast-fashion / Accessible"
    )
    target_customer: str = Field(description="Who wears this — age, lifestyle, values")
    season: str = Field(description="SS26 / AW26 / Timeless")
    comparable_brands: list[str] = Field(
        default_factory=list, description="Brands making similar pieces"
    )


class AIAssessment(_Section):
    classification_difficulty: str = Field(description="Easy / Medium / Hard / Edge Case")
    why_difficult: str | None = Field(
        default=None, description="What makes this tricky to classify, if applicable"
    )
    ai_training_recommendation: str = Field(
        description="How an AI should learn from this example"
    )


class FashionTaxonomy(BaseModel):
    """Complete taxonomy breakdown of a single fashion image."""

    model_config = ConfigDict(extra="forbid")

    basic_classification: BasicClassification
    material_and_colour: MaterialAndColour
    details: Details
    trend_analysis: TrendAnalysis
    market_positioning: MarketPositioning
    ai_assessment: AIAssessment
