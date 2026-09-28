# Document AI Enterprise Parser

Production-grade, enterprise-standard Python application and analytics platform for automated PDF document classification, extraction, text inspection, and contextual AI analysis.

---

## Architecture Overview

The repository utilizes a modular `src` layout (`src/pdf_classifier`) adhering to FAANG software engineering practices:

```text
py-pdf-classifier/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI workflow
├── .streamlit/
│   └── config.toml                # Streamlit server and UI theme settings
├── src/
│   └── pdf_classifier/
│       ├── __init__.py
│       ├── app.py                 # Main Streamlit dashboard entrypoint
│       ├── components/            # Isolated UI views and control widgets
│       │   ├── export_view.py
│       │   ├── metrics_bar.py
│       │   ├── pdf_viewer.py
│       │   ├── qa_chat.py
│       │   ├── search_view.py
│       │   ├── sidebar.py
│       │   └── summary_view.py
│       ├── services/              # Core business and API logic
│       │   ├── metrics_service.py # Text analytics calculations
│       │   ├── ollama_service.py  # Local LLM integration
│       │   └── pdf_service.py     # PyMuPDF extraction & page rendering
│       └── utils/                 # Application state and styling helpers
│           ├── state.py
│           └── styles.py
├── tests/
│   ├── unit/                      # Pytest unit testing suite
│   └── e2e/                       # Playwright E2E UI automation suite
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git tracking exclusions
├── LICENSE                        # MIT License declaration
├── pyproject.toml                 # PEP 621 project metadata and dependencies
├── README.md                      # Repository documentation
├── requirements.txt               # Locked production dependencies
└── requirements-dev.txt           # Locked development dependencies
```

---

## Key Capabilities

1. **PDF Text & Image Extraction**: High-performance rendering and parsing powered by PyMuPDF (`fitz`).
2. **Quantitative Analytics**: Instant calculation of word count, page count, character density, and estimated reading duration.
3. **Keyword Search & Highlight**: Dynamic in-memory regex searching with marked UI highlighting.
4. **Contextual Q&A**: Interactive document assistant querying local Ollama LLM models.
5. **Data Export**: Structured JSON and plain text document export capabilities.
6. **Automation Ready**: All UI components are instrumented with predictable DOM identifiers and keys for Playwright E2E testing.

---

## Prerequisites

- **Python**: Version 3.10 or higher (3.12 recommended).
- **Package Manager**: `uv` or standard `pip`.
- **Ollama Engine (Optional)**: Required for local LLM document classification and Q&A (`ollama serve`).

---

## Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-org/py-pdf-classifier.git
cd py-pdf-classifier
```

### 2. Environment Setup

Create and configure environment variables:

```bash
cp .env.example .env
```

### 3. Install Dependencies

Using `uv` (recommended):

```bash
uv sync --all-extras --dev
```

Or using `pip`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

---

## Running the Application

To launch the Streamlit dashboard:

```bash
uv run streamlit run src/pdf_classifier/app.py
```

Alternatively, use the root entrypoint wrapper:

```bash
uv run streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

---

## Testing & Quality Assurance

### Unit Tests

Execute the unit test suite with coverage tracking:

```bash
uv run pytest tests/unit -v --cov=src/pdf_classifier
```

### End-to-End (E2E) UI Automation Tests

Install Playwright browsers (first-time setup):

```bash
uv run playwright install --with-deps chromium
```

Run the Playwright E2E UI tests:

```bash
uv run pytest tests/e2e -v
```

### Code Formatting & Static Analysis

Lint codebase using Ruff:

```bash
uv run ruff check .
```

Verify type safety using Mypy:

```bash
uv run mypy src
```

---

## License

Distributed under the MIT License. See `LICENSE` for full details.
