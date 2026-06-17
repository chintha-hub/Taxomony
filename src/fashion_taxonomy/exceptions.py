"""Custom exception hierarchy for the Fashion Taxonomy package.

Catch :class:`FashionTaxonomyError` to handle any error raised by this package.
"""

from __future__ import annotations


class FashionTaxonomyError(Exception):
    """Base class for all errors raised by this package."""


class ConfigurationError(FashionTaxonomyError):
    """Raised when configuration is missing or invalid (e.g. no API key)."""


class ImageLoadError(FashionTaxonomyError):
    """Raised when an image cannot be read or is an unsupported type."""


class ProviderError(FashionTaxonomyError):
    """Raised when an upstream AI provider call fails or returns bad data."""
