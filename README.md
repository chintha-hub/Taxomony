# 👗 Fashion Taxonomy AI

AI-powered fashion image analysis. Upload a clothing image and get a complete,
**structured taxonomy** — category, silhouette, material, colour, trend signal,
market positioning, and an AI difficulty assessment — across 23 fields.

Supports **OpenAI (GPT-4o)** and **Google Gemini** vision models behind a clean
provider abstraction, with both a **CLI** and a **Streamlit web app**.

---

## ✨ Features

- **Structured output** — every analysis is validated against a Pydantic schema
  (`FashionTaxonomy`), so you get typed, queryable JSON instead of free text.
- **Pluggable providers** — switch between OpenAI and Gemini via one env var;
  adding a new provider (e.g. Claude) is a single subclass.
- **Two interfaces** — a Streamlit UI for humans and a CLI for scripts/pipelines.
- **Secrets done right** — API keys live in `.env` / Streamlit secrets, never in code.
- **Tested & linted** — pytest suite (no network needed), ruff + mypy configured.

---

## 📦 Project structure

```
.
├── app/
│   └── streamlit_app.py          # Streamlit web UI
├── src/fashion_taxonomy/
│   ├── analyzer.py               # High-level orchestration
│   ├── config.py                 # Typed settings from .env (pydantic-settings)
│   ├── schemas.py                # FashionTaxonomy Pydantic models (the contract)
│   ├── prompts.py                # Prompt construction
│   ├── models.py                 # ImageInput value object
│   ├── rendering.py              # taxonomy -> markdown / text
│   ├── cli.py                    # `fashion-taxonomy` command
│   └── providers/                # openai / gemini + factory + base
├── tests/                        # pytest suite (mock provider, no API key)
├── .env.example                  # copy to .env and add your key
├── pyproject.toml                # packaging, deps, ruff/mypy/pytest config
├── Dockerfile                    # container for the Streamlit app
└── Makefile                      # make install / run / test / lint
```

---

## 🚀 Quick start

### 1. Set up the environment

```bash
make install        # creates .venv and installs the package + dev tools
# ...or manually:
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Add your API key

```bash
cp .env.example .env     # if you don't already have a .env
```

Edit `.env` and set **one** of:

```ini
PROVIDER=openai
OPENAI_API_KEY=sk-...        # from https://platform.openai.com/api-keys
# or
PROVIDER=gemini
GOOGLE_API_KEY=...           # from https://aistudio.google.com/app/apikey
```

> ⚠️ **Never commit `.env`.** It's git-ignored on purpose. Treat API keys like passwords.

### 3. Run it

**Web app:**
```bash
make run                     # streamlit run app/streamlit_app.py
```

**CLI:**
```bash
fashion-taxonomy analyze path/to/image.jpg
fashion-taxonomy analyze path/to/image.jpg --provider gemini --json -o result.json
```

---

## 🐳 Docker

```bash
docker build -t fashion-taxonomy .
docker run -e OPENAI_API_KEY=sk-... -p 8501:8501 fashion-taxonomy
# open http://localhost:8501
```

---

## 🧑‍💻 Library usage

```python
from fashion_taxonomy import FashionAnalyzer, ImageInput, get_settings

analyzer = FashionAnalyzer(get_settings())
taxonomy = analyzer.analyze(ImageInput.from_path("dress.jpg"))

print(taxonomy.basic_classification.category)        # "Dress"
print(taxonomy.market_positioning.comparable_brands) # ["Reformation", ...]
print(taxonomy.model_dump_json(indent=2))            # full structured JSON
```

---

## 🛠️ Development

```bash
make test        # run the test suite
make cov         # tests + coverage report
make lint        # ruff
make typecheck   # mypy
make check       # lint + typecheck + test
```

---

## ⚙️ Configuration reference

| Variable | Default | Description |
|---|---|---|
| `PROVIDER` | `openai` | `openai` or `gemini` |
| `OPENAI_API_KEY` | — | OpenAI key (required if provider=openai) |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI vision model |
| `GOOGLE_API_KEY` | — | Gemini key (required if provider=gemini) |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini vision model |
| `MAX_OUTPUT_TOKENS` | `2000` | Max tokens in the response |
| `REQUEST_TIMEOUT_SECONDS` | `60` | Upstream request timeout |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |

---

## 📄 License

MIT — see [LICENSE](LICENSE).
