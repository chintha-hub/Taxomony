# Fashion Taxonomy AI — common developer tasks.
# Usage:  make <target>

PYTHON ?= python3
VENV   ?= .venv
BIN     = $(VENV)/bin

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

$(VENV): ## Create the virtual environment
	$(PYTHON) -m venv $(VENV)

.PHONY: install
install: $(VENV) ## Create venv and install the package + dev tools
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"

.PHONY: run
run: ## Launch the Streamlit web app
	$(BIN)/streamlit run app/streamlit_app.py

.PHONY: analyze
analyze: ## Analyze an image from the CLI:  make analyze IMG=path/to/img.jpg
	$(BIN)/fashion-taxonomy analyze "$(IMG)"

.PHONY: test
test: ## Run the test suite
	$(BIN)/pytest

.PHONY: cov
cov: ## Run tests with a coverage report
	$(BIN)/pytest --cov=fashion_taxonomy --cov-report=term-missing

.PHONY: lint
lint: ## Lint with ruff
	$(BIN)/ruff check src tests

.PHONY: fmt
fmt: ## Auto-format / fix with ruff
	$(BIN)/ruff check --fix src tests
	$(BIN)/ruff format src tests

.PHONY: typecheck
typecheck: ## Static type check with mypy
	$(BIN)/mypy

.PHONY: check
check: lint typecheck test ## Run lint + typecheck + tests

.PHONY: clean
clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
