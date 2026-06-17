"""Google Gemini vision provider using JSON-mode structured output."""

from __future__ import annotations

import json

from fashion_taxonomy.exceptions import ProviderError
from fashion_taxonomy.logging_config import get_logger
from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.prompts import SYSTEM_INSTRUCTIONS
from fashion_taxonomy.providers.base import VisionProvider
from fashion_taxonomy.schemas import FashionTaxonomy

logger = get_logger(__name__)


class GeminiProvider(VisionProvider):
    """Analyze images with Google Gemini vision models (e.g. ``gemini-1.5-flash``).

    Requests ``application/json`` output and embeds the JSON schema in the
    prompt, then validates the response against :class:`FashionTaxonomy`. This
    keeps the provider robust across ``google-generativeai`` versions.
    """

    name = "gemini"

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-1.5-flash",
        *,
        max_tokens: int = 2000,
        timeout: int = 60,
    ) -> None:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        self._genai = genai
        self._max_tokens = max_tokens
        self._timeout = timeout
        self._model = genai.GenerativeModel(
            model_name=model,
            system_instruction=SYSTEM_INSTRUCTIONS,
        )

    def analyze(self, image: ImageInput, prompt: str) -> FashionTaxonomy:
        schema_json = json.dumps(FashionTaxonomy.model_json_schema(), indent=2)
        full_prompt = (
            f"{prompt}\n\n"
            "Return ONLY a single valid JSON object — no markdown, no commentary — "
            "conforming to this JSON Schema:\n"
            f"{schema_json}"
        )
        try:
            response = self._model.generate_content(
                [
                    full_prompt,
                    {"mime_type": image.mime_type, "data": image.data},
                ],
                generation_config=self._genai.GenerationConfig(
                    max_output_tokens=self._max_tokens,
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
                request_options={"timeout": self._timeout},
            )
        except Exception as exc:  # noqa: BLE001 - normalize all SDK errors
            raise ProviderError(f"Gemini request failed: {exc}") from exc

        text = (getattr(response, "text", "") or "").strip()
        if not text:
            raise ProviderError("Gemini returned an empty response.")
        try:
            return FashionTaxonomy.model_validate_json(text)
        except ValueError as exc:
            raise ProviderError(f"Gemini returned data that failed validation: {exc}") from exc
