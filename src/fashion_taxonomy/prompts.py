"""Prompt construction for the taxonomy task."""

from __future__ import annotations

SYSTEM_INSTRUCTIONS = (
    "You are an expert fashion analyst and merchandiser. You classify garments "
    "into a precise, structured taxonomy. If a person or human appears in the "
    "image, ignore the person and focus only on the clothing they are wearing. "
    "Be specific and concise. Never invent details you cannot see; when a field "
    "does not apply, use 'N/A'."
)

ANALYSIS_BRIEF = """\
Analyze this fashion image in complete detail and produce a structured taxonomy.

BASIC CLASSIFICATION
- category: Tops / Bottoms / Dress / Outerwear / Knitwear / Accessories / Footwear
- sub_category: e.g. Blouse, Midi Dress, Trench Coat
- silhouette: A-line / Straight / Oversized / Fitted / Relaxed / Wrap / Asymmetric / Boxy
- neckline: V-neck / Round / Square / Off-shoulder / Halter / Collared / Strapless / Cowl / N/A
- sleeve: Sleeveless / Short / Long / 3-4 / Puff / Rolled / Cape / Draped / N/A
- length: Crop / Short / Midi / Maxi / Mini / Standard / Knee / Ankle

MATERIAL & COLOUR
- material: Cotton / Silk / Linen / Denim / Leather / Knit / Chiffon / Satin / Wool / Synthetic
- primary_colour: name it clearly (Ivory, Navy, Burgundy, ...)
- secondary_colour: if applicable, else null
- print_texture: Solid / Floral / Stripe / Check / Abstract / Geometric / Embroidered / Textured

DETAILS
- key_detail: what stands out (Ruffle, Pocket, Belt, Cut-out, Draping, ...)
- fabric_weight: Lightweight / Medium / Heavyweight
- finish: Matte / Glossy / Textured

TREND ANALYSIS
- trend_signal: Utility femininity / Sheer layering / Tactile surfaces / Oversized tailoring / Quiet luxury / Maximalism / Streetwear / Heritage / Other
- trend_confidence: High / Medium / Low / Edge Case
- why_this_trend: 1-2 sentences

MARKET POSITIONING
- market_level: Luxury / Premium / Mid-market / Fast-fashion / Accessible
- target_customer: who wears this (age, lifestyle, values)
- season: SS26 / AW26 / Timeless
- comparable_brands: list of brands making similar pieces

AI ASSESSMENT
- classification_difficulty: Easy / Medium / Hard / Edge Case
- why_difficult: what makes this tricky to classify (null if Easy)
- ai_training_recommendation: how an AI should learn from this example
"""


def build_analysis_prompt() -> str:
    """Return the full instruction prompt for analyzing one image."""
    return ANALYSIS_BRIEF
