"""Typed application configuration loaded from environment / .env file.

Settings are read (in order of precedence) from real environment variables,
then a local ``.env`` file. Secrets are stored as ``SecretStr`` so they are
never accidentally printed in logs or tracebacks.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Provider = Literal["openai", "gemini"]


class Settings(BaseSettings):
    """Runtime configuration for the analyzer."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    provider: Provider = "openai"

    # OpenAI
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4o"

    # Google Gemini
    google_api_key: SecretStr | None = None
    gemini_model: str = "gemini-1.5-flash"

    # Generation
    max_output_tokens: int = Field(default=2000, ge=256, le=8192)
    request_timeout_seconds: int = Field(default=60, ge=5, le=600)

    # Observability
    log_level: str = "INFO"

    def key_for(self, provider: Provider) -> SecretStr | None:
        """Return the configured API key for the given provider."""
        return self.openai_api_key if provider == "openai" else self.google_api_key

    def model_for(self, provider: Provider) -> str:
        """Return the configured model name for the given provider."""
        return self.openai_model if provider == "openai" else self.gemini_model


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance for the process."""
    return Settings()
