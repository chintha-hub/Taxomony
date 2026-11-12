"""Streamlit web app for the Fashion Taxonomy AI analyzer.

Run with:  streamlit run app/streamlit_app.py

Configuration is read from (in order): Streamlit secrets (.streamlit/secrets.toml),
then environment variables / .env. Set OPENAI_API_KEY or GOOGLE_API_KEY in either.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Make the src/ layout importable even when the package isn't pip-installed.
# Streamlit Community Cloud only installs requirements.txt (not the local
# package), so without this the `fashion_taxonomy` import would fail.
_SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if _SRC_DIR.is_dir() and str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import streamlit as st

# --- Bridge Streamlit secrets into the environment BEFORE importing config ---
# This lets the same Settings object work locally (.env) and on Streamlit Cloud.
_SECRET_KEYS = (
    "PROVIDER",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "GOOGLE_API_KEY",
    "GEMINI_MODEL",
)
try:
    for _k in _SECRET_KEYS:
        if _k in st.secrets and st.secrets[_k]:
            os.environ.setdefault(_k, str(st.secrets[_k]))
except Exception:  # noqa: BLE001 - no secrets file is a perfectly valid setup
    pass

from fashion_taxonomy.analyzer import FashionAnalyzer  # noqa: E402
from fashion_taxonomy.config import Settings  # noqa: E402
from fashion_taxonomy.exceptions import FashionTaxonomyError  # noqa: E402
from fashion_taxonomy.models import ImageInput  # noqa: E402
from fashion_taxonomy.rendering import to_markdown, to_text  # noqa: E402

st.set_page_config(page_title="Fashion Taxonomy AI", page_icon="👗", layout="wide")


@st.cache_resource
def _get_analyzer() -> FashionAnalyzer:
    # Settings re-read here (after secrets bridged) and cached for the session.
    return FashionAnalyzer(Settings())


def _provider_ready(settings: Settings, provider: str) -> bool:
    key = settings.key_for(provider)  # type: ignore[arg-type]
    return key is not None and bool(key.get_secret_value())


def main() -> None:
    st.title("👗 Fashion Taxonomy AI Analyzer")
    st.caption("Upload a fashion image to generate a complete, structured taxonomy breakdown.")

    settings = Settings()

    with st.sidebar:
        st.header("Settings")
        provider = st.radio(
            "Vision provider",
            options=["openai", "gemini"],
            index=0 if settings.provider == "openai" else 1,
            format_func=lambda p: {"openai": "OpenAI (GPT-4o)", "gemini": "Google Gemini"}[p],
        )
        ready = _provider_ready(settings, provider)
        if ready:
            st.success(f"{provider.title()} API key detected.")
        else:
            env_var = "OPENAI_API_KEY" if provider == "openai" else "GOOGLE_API_KEY"
            st.error(f"No key for {provider}. Set {env_var} in .env or Streamlit secrets.")
        st.divider()
        st.caption("Tip: never commit your API key. Use .env or .streamlit/secrets.toml.")

    uploaded = st.file_uploader(
        "Choose a fashion image", type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded is None:
        st.info("Upload an image above to see the taxonomy breakdown.")
        return

    col_img, col_out = st.columns([1, 2])
    with col_img:
        st.image(uploaded, caption=uploaded.name, use_container_width=True)

    with col_out:
        if not ready:
            st.warning("Add an API key for the selected provider to run the analysis.")
            return
        with st.spinner("Analysing fashion taxonomy…"):
            try:
                image = ImageInput.from_bytes(
                    uploaded.getvalue(),
                    mime_type=uploaded.type or "image/jpeg",
                    filename=uploaded.name,
                )
                taxonomy = _get_analyzer().analyze(image, provider=provider)  # type: ignore[arg-type]
            except FashionTaxonomyError as exc:
                st.error(f"Analysis failed: {exc}")
                return

        st.markdown(to_markdown(taxonomy))
        st.divider()
        c1, c2 = st.columns(2)
        stem = uploaded.name.rsplit(".", 1)[0]
        c1.download_button(
            "⬇️ Download JSON",
            data=taxonomy.model_dump_json(indent=2),
            file_name=f"{stem}_taxonomy.json",
            mime="application/json",
            on_click="ignore",
        )
        c2.download_button(
            "⬇️ Download text",
            data=to_text(taxonomy),
            file_name=f"{stem}_taxonomy.txt",
            mime="text/plain",
            on_click="ignore",
        )


if __name__ == "__main__":
    main()
