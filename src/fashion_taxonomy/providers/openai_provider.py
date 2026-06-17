"""OpenAI vision provider using native structured outputs."""

from __future__ import annotations

from fashion_taxonomy.exceptions import ProviderError
from fashion_taxonomy.logging_config import get_logger
from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.prompts import SYSTEM_INSTRUCTIONS
from fashion_taxonomy.providers.base import VisionProvider
from fashion_taxonomy.schemas import FashionTaxonomy

logger = get_logger(__name__)


class OpenAIProvider(VisionProvider):
    """Analyze images with OpenAI vision models (e.g. ``gpt-4o``).

    Uses the SDK's structured-output parsing so the model is constrained to the
    :class:`FashionTaxonomy` schema and we get a validated object back.
    """

    name = "openai"

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        *,
        max_tokens: int = 2000,
        timeout: int = 60,
    ) -> None:
        # Imported lazily so the package can be imported without the dep present.
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key, timeout=timeout)
        self._model = model
        self._max_tokens = max_tokens

    def analyze(self, image: ImageInput, prompt: str) -> FashionTaxonomy:
        try:
            completion = self._client.beta.chat.completions.parse(
                model=self._model,
                max_tokens=self._max_tokens,
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image.to_data_url()},
                            },
                        ],
                    },
                ],
                response_format=FashionTaxonomy,
            )
        except Exception as exc:  # noqa: BLE001 - normalize all SDK errors
            raise ProviderError(f"OpenAI request failed: {exc}") from exc

        parsed = completion.choices[0].message.parsed
        if parsed is None:
            refusal = completion.choices[0].message.refusal
            raise ProviderError(f"OpenAI returned no structured output (refusal: {refusal!r}).")
        return parsed
