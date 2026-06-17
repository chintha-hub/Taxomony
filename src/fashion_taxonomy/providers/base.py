"""Abstract base class for vision providers.

A provider takes an image plus a prompt and returns a validated
:class:`~fashion_taxonomy.schemas.FashionTaxonomy`. Adding a new provider
(e.g. Anthropic Claude) is just a matter of subclassing this and registering
it in :mod:`fashion_taxonomy.providers.factory`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.schemas import FashionTaxonomy


class VisionProvider(ABC):
    """Common interface for an image → taxonomy provider."""

    #: Human-readable provider id, e.g. ``"openai"``.
    name: str = "base"

    @abstractmethod
    def analyze(self, image: ImageInput, prompt: str) -> FashionTaxonomy:
        """Analyze ``image`` against ``prompt`` and return a validated taxonomy.

        Raises:
            fashion_taxonomy.exceptions.ProviderError: on any upstream failure
                or if the response cannot be parsed into the schema.
        """
        raise NotImplementedError
