# 20-hour implementation plan

| Time | Work | Evidence of completion |
|---|---|---|
| 1–2 h | Requirements and design | Requirements, HLD, LLD, DFD, architecture |
| 3–5 h | Article ingestion and chunking | Clean article text and chunk counts |
| 6–9 h | Embeddings, FAISS and RAG | Supported questions retrieve relevant evidence |
| 10–12 h | API and UI | Ingestion and chat work in browser |
| 13–14 h | SQLite and cache | Metadata persists; repeat question is cached |
| 15–17 h | Tests and manual evaluation | Unit tests and supported/unsupported test questions |
| 18–20 h | Demo rehearsal and docs | Clean startup, README, diagrams and known limitations |

## Prioritization

**P0 — Must work:** startup, ingestion, retrieval, grounded answers, citations, unsupported-query refusal.

**P1 — Must demonstrate:** SQLite persistence, cache hit, API docs, unit tests and setup instructions.

**P2 — If time permits:** reranking, multiple corpora, authentication, analytics and production deployment.

Do not sacrifice a reliable demo to add advanced features. Record test outcomes honestly; do not claim a criterion passed until it has been exercised.
