# Database Design

## `documents`
- `id`: integer primary key
- `url`: unique source URL
- `title`: extracted title
- `fetched_at`: ingestion timestamp
- `content_hash`: SHA-256 hash of cleaned content
- `char_count`: cleaned text length

## `chunks`
- `id`: integer primary key
- `document_id`: foreign key to `documents.id`
- `chunk_index`: zero-based chunk position
- `text`: chunk content

Relationship: one document has many chunks.

## `answer_cache`
- `cache_key`: hash of normalized question + knowledge-base version
- `question`: original question
- `answer`: cached answer
- `sources_json`: serialized source metadata
- `created_at`: timestamp

## `app_meta`
Stores key/value metadata, including the knowledge-base version.

FAISS vectors are persisted in `vector_store/index.faiss`; matching records are persisted in `vector_store/records.json`. SQLite stores structured metadata and cache entries.
