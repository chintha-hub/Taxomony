"""Build the configured vision provider from settings."""

from __future__ import annotations

from fashion_taxonomy.config import Provider, Settings
from fashion_taxonomy.exceptions import ConfigurationError
from fashion_taxonomy.providers.base import VisionProvider


def build_provider(settings: Settings, provider: Provider | None = None) -> VisionProvider:
    """Instantiate the vision provider selected in ``settings``.

    Args:
        settings: Application settings.
        provider: Optional override; defaults to ``settings.provider``.

    Raises:
        ConfigurationError: if the API key for the chosen provider is missing.
    """
    chosen: Provider = provider or settings.provider
    key = settings.key_for(chosen)
    if key is None or not key.get_secret_value():
        env_var = "OPENAI_API_KEY" if chosen == "openai" else "GOOGLE_API_KEY"
        raise ConfigurationError(
            f"No API key configured for provider {chosen!r}. "
            f"Set {env_var} in your .env file or environment."
        )

    secret = key.get_secret_value()
    model = settings.model_for(chosen)
    common = {
        "max_tokens": settings.max_output_tokens,
        "timeout": settings.request_timeout_seconds,
    }

    if chosen == "openai":
        from fashion_taxonomy.providers.openai_provider import OpenAIProvider

        return OpenAIProvider(api_key=secret, model=model, **common)

    from fashion_taxonomy.providers.gemini_provider import GeminiProvider

    return GeminiProvider(api_key=secret, model=model, **common)
