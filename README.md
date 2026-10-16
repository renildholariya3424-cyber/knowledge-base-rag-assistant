# Knowledge Base Q&A — RAG MVP

A local-first retrieval-augmented generation demo prepared for the August Infotech AI/ML practical test. It ingests a small set of public articles, splits them into overlapping chunks, embeds them, retrieves relevant passages with FAISS, and uses a local Ollama model to answer with source references.

## What the demo shows

- Public article ingestion with Requests and BeautifulSoup
- Text cleaning and overlapping chunking
- Sentence Transformers embeddings and FAISS similarity search
- Grounded Q&A with source URLs and retrieved excerpts
- A relevance gate that declines questions without enough evidence
- Ollama local inference and an explicitly labeled extractive fallback
- SQLite metadata, persistent index files and version-aware answer caching
- FastAPI endpoints, Streamlit UI, unit tests and design documents

## Tech stack

Python 3.11+ · FastAPI · Streamlit · Sentence Transformers · FAISS · SQLite · Ollama · pytest

Python 3.13 may work if compatible wheels are available for all dependencies. If installation fails on 3.13, use Python 3.11 or 3.12 rather than changing versions at random.

## Setup on Windows

Open this folder in VS Code. In a terminal:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you already have a working Python 3.13 environment, you can try `py -3.13 -m venv .venv`. If a dependency has no compatible wheel, use Python 3.11 or 3.12.

Install Ollama from https://ollama.com/download/windows, then:

```powershell
ollama pull qwen2.5:3b
ollama run qwen2.5:3b
```

Type `/bye` to leave the interactive model. You can verify the Python connection with `python check_model_connection.py`. Ollama should remain running in the background. On first app use, Sentence Transformers downloads `all-MiniLM-L6-v2`.

## Run the demo

Use two VS Code terminals and activate the environment in both.

Terminal 1 — API:

```powershell
uvicorn app.main:app --reload
```

Check `http://127.0.0.1:8000/health` and open `http://127.0.0.1:8000/docs`.

Terminal 2 — UI:

```powershell
streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`. Default Python documentation URLs are prefilled one per line. Click **Scrape and index**, wait for the article/chunk counts, then ask a suggested question.

## API endpoints

- `GET /` — service overview
- `GET /health` — API and knowledge-base status
- `GET /documents` — indexed document metadata
- `POST /ingest` — scrape and index URLs
- `POST /ask` — retrieve evidence and answer a question
- `GET /docs` — interactive API documentation

## Tests

```powershell
pytest -q
```

Tests are a safety net, not proof of production readiness. Manually verify a supported question, an unsupported question, source relevance, repeated-question caching and persistence after restarting the API.

## Design documents

See `docs/` for requirements, HLD, LLD, DFD, architecture, database design, library decisions and the 20-hour implementation plan.

## Known limitations

- Local single-user MVP, not a production service.
- Basic scraping cannot render JavaScript-heavy pages and may fail if a site blocks requests.
- Retrieval threshold is heuristic and should be evaluated with labeled questions.
- Cache hits reuse answers for the same normalized question and knowledge-base version.
- No authentication, user-level access control, advanced reranking or distributed deployment.
- Do not ingest confidential documents unless deployment, logging, access controls and model data flow have been reviewed.
