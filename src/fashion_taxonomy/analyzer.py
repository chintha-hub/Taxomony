"""High-level orchestration: image in, validated taxonomy out."""

from __future__ import annotations

from fashion_taxonomy.config import Provider, Settings
from fashion_taxonomy.logging_config import get_logger
from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.prompts import build_analysis_prompt
from fashion_taxonomy.providers.base import VisionProvider
from fashion_taxonomy.providers.factory import build_provider
from fashion_taxonomy.schemas import FashionTaxonomy

logger = get_logger(__name__)


class FashionAnalyzer:
    """Analyze fashion images into a structured taxonomy.

    The provider is built lazily on first use, so constructing an analyzer does
    not require an API key (useful for tests and the web app's startup).

    Example:
        >>> analyzer = FashionAnalyzer(get_settings())
        >>> taxonomy = analyzer.analyze(ImageInput.from_path("dress.jpg"))
    """

    def __init__(
        self,
        settings: Settings,
        provider: VisionProvider | None = None,
    ) -> None:
        self._settings = settings
        self._provider = provider
        self._prompt = build_analysis_prompt()

    @property
    def provider(self) -> VisionProvider:
        """Return the active provider, building it on first access."""
        if self._provider is None:
            self._provider = build_provider(self._settings)
        return self._provider

    def analyze(
        self,
        image: ImageInput,
        provider: Provider | None = None,
    ) -> FashionTaxonomy:
        """Analyze a single image and return its validated taxonomy.

        Args:
            image: The image to analyze.
            provider: Optional one-off provider override (``"openai"`` /
                ``"gemini"``). When given, a fresh provider is built for this
                call instead of using the cached one.
        """
        active = build_provider(self._settings, provider) if provider else self.provider
        logger.info(
            "Analyzing image %s via %s",
            image.filename or "<bytes>",
            active.name,
        )
        result = active.analyze(image, self._prompt)
        logger.info(
            "Done: %s / %s",
            result.basic_classification.category,
            result.basic_classification.sub_category,
        )
        return result
