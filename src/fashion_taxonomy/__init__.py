"""Fashion Taxonomy AI — analyze fashion images into a structured taxonomy.

Public API:
    >>> from fashion_taxonomy import FashionAnalyzer, ImageInput, get_settings
    >>> analyzer = FashionAnalyzer(get_settings())
    >>> taxonomy = analyzer.analyze(ImageInput.from_path("dress.jpg"))
    >>> print(taxonomy.basic_classification.category)
"""

from fashion_taxonomy.analyzer import FashionAnalyzer
from fashion_taxonomy.config import Settings, get_settings
from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.schemas import FashionTaxonomy

__version__ = "0.1.0"

__all__ = [
    "FashionAnalyzer",
    "FashionTaxonomy",
    "ImageInput",
    "Settings",
    "get_settings",
    "__version__",
]
