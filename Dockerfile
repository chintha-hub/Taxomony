# ---- Fashion Taxonomy AI — Streamlit app image ----
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching.
COPY pyproject.toml requirements.txt README.md ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

# Copy the application code.
COPY app ./app
COPY .streamlit ./.streamlit

EXPOSE 8501

# Secrets are provided at runtime via environment variables, e.g.:
#   docker run -e OPENAI_API_KEY=sk-... -p 8501:8501 fashion-taxonomy
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app/streamlit_app.py", \
            "--server.port=8501", "--server.address=0.0.0.0"]
