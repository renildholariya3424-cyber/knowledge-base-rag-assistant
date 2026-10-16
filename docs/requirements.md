# Requirements and acceptance criteria

## Goal

Build a demonstrable knowledge-based Q&A MVP using RAG and an open-weight model, showing Python implementation, system design, storage, caching and testing within the 20-hour practical-test window.

## Assumptions

- Local, single-user demo.
- A few public HTML articles are available to access.
- Ollama and the selected model are installed on the demo machine.
- Embedding weights are downloaded on first use.
- Source excerpts and URLs are sufficient for the proof of concept.

## Functional requirements

1. Accept up to 10 public HTTP(S) article URLs.
2. Extract title and readable article text.
3. Split content into overlapping chunks.
4. Generate normalized embeddings.
5. Persist chunks and document metadata in SQLite.
6. Build and persist a FAISS index.
7. Retrieve relevant passages for a question.
8. Generate an answer using retrieved evidence and source labels.
9. Decline low-relevance questions rather than fabricate an answer.
10. Cache answers by normalized question and knowledge-base version.
11. Expose health, document listing, ingestion and ask endpoints.
12. Provide a Streamlit interface for ingestion and Q&A.

## Non-functional requirements

- Clear errors for unavailable API/model and failed pages.
- Reproducible setup steps.
- Tests for input validation and core helper behavior.
- Local-first inference by default.
- Source traceability for answer verification.

## Deal-breakers

- Application cannot start.
- No article content is indexed.
- Querying fails after successful ingestion.
- Answers have no traceable source passages.
- Unrelated questions receive confident unsupported answers.
- Failed ingestion leaves a misleading ready status.

## Acceptance checklist

- [ ] `GET /health` returns status `ok`.
- [ ] Default articles can be indexed.
- [ ] `/health` reports a ready vector index after ingestion.
- [ ] Supported question returns answer and sources.
- [ ] Unsupported question is declined.
- [ ] Repeated question reports a cache hit.
- [ ] Documents and index persist after API restart.
- [ ] `pytest -q` passes.
- [ ] README and diagrams explain design choices.

## Out of scope

Authentication, multi-user permissions, distributed vector search, scheduled crawling, JavaScript rendering, production deployment and fine-tuning.
