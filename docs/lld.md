# Low-Level Design (LLD)

## Modules
- `app/config.py`: runtime settings and paths.
- `app/scraper.py`: URL validation, HTTP fetch, HTML cleanup and extraction.
- `app/chunking.py`: overlapping text segmentation.
- `app/embeddings.py`: cached embedding model and vector encoding.
- `app/database.py`: SQLite schema, document/chunk persistence and answer cache.
- `app/vector_store.py`: build, persist, load and search FAISS index.
- `app/ingestion.py`: scrape → chunk → persist → embed/index.
- `app/rag.py`: cache lookup → retrieval → relevance gate → LLM prompt → answer.
- `app/main.py`: FastAPI routes and validation.
- `streamlit_app.py`: chat and ingestion UI.

## Main functions
- `scrape_article(url)`: title, URL and cleaned text.
- `split_text(text, chunk_size, overlap)`: chunk list.
- `encode_texts(texts)`: normalized float32 vectors.
- `LocalVectorStore.build(records)`: create FAISS index.
- `LocalVectorStore.search(question, top_k)`: retrieve passages with scores.
- `ingest_urls(urls)`: full ingestion pipeline.
- `answer_question(question, top_k)`: answer, sources, cache flag and backend mode.

## Retrieval
Vectors are normalized; FAISS `IndexFlatIP` ranks by inner product, equivalent to cosine similarity for normalized vectors. The relevance threshold is a heuristic, not a calibrated confidence score.

## Error handling
Invalid URLs and thin pages produce errors. One failed URL does not prevent other URLs from ingesting. Empty KB gives a clear message. Ollama failures trigger a clearly labeled extractive fallback. Pydantic validates API requests.
