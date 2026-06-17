"""Tests for the analyzer orchestration and provider factory."""

from __future__ import annotations

import pytest

from fashion_taxonomy.analyzer import FashionAnalyzer
from fashion_taxonomy.config import Settings
from fashion_taxonomy.exceptions import ConfigurationError
from fashion_taxonomy.models import ImageInput
from fashion_taxonomy.providers.factory import build_provider
from tests.conftest import FakeProvider


def test_analyze_uses_injected_provider(
    fake_provider: FakeProvider, sample_image: ImageInput
) -> None:
    analyzer = FashionAnalyzer(Settings(_env_file=None), provider=fake_provider)
    result = analyzer.analyze(sample_image)
    assert result.basic_classification.category == "Dress"
    assert len(fake_provider.calls) == 1
    # The prompt should have been passed to the provider.
    assert "BASIC CLASSIFICATION" in fake_provider.calls[0][1]


def test_build_provider_without_key_raises() -> None:
    settings = Settings(_env_file=None, openai_api_key=None, google_api_key=None)
    with pytest.raises(ConfigurationError):
        build_provider(settings, "openai")
    with pytest.raises(ConfigurationError):
        build_provider(settings, "gemini")


def test_provider_property_is_lazy(
    fake_provider: FakeProvider, sample_image: ImageInput
) -> None:
    # No key configured, but injecting a provider means no build is attempted.
    analyzer = FashionAnalyzer(Settings(_env_file=None), provider=fake_provider)
    assert analyzer.provider is fake_provider
