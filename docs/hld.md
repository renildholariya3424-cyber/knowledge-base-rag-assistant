# High-Level Design (HLD)

## Components
- Streamlit: user-facing chat and ingestion controls.
- FastAPI: request validation and coordination.
- Scraper: fetches public HTML and extracts readable text.
- Chunker: creates overlapping chunks.
- Sentence Transformers: embeds chunks and questions.
- FAISS: local dense-vector search.
- SQLite: document metadata, chunks, KB version and answer cache.
- Ollama: local open-weight LLM inference.

## Flow
1. User submits URLs through Streamlit.
2. FastAPI calls the ingestion pipeline.
3. Scraper extracts article content; chunker splits it.
4. Embeddings are generated and FAISS is built.
5. Document/chunk metadata is persisted in SQLite.
6. User asks a question; cache is checked.
7. On a cache miss, the question is embedded and top-k passages retrieved.
8. Passages are sent to Ollama with grounding and citation instructions.
9. Answer and source metadata are returned to the UI.

## Decisions
Local-first keeps the demo independent of paid hosted inference APIs. SQLite is sufficient for a small single-user MVP. FAISS is a vector search library, not a relational database, so metadata is stored separately. Keeping API and UI separate allows independent testing.
