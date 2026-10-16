import hashlib
import json
import sqlite3
import time
from contextlib import contextmanager
from typing import Any
from app.config import settings

@contextmanager
def connection():
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.database_path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
            fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, content_hash TEXT NOT NULL,
            char_count INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            chunk_index INTEGER NOT NULL, text TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS idx_chunks_document ON chunks(document_id);
        CREATE TABLE IF NOT EXISTS answer_cache (
            cache_key TEXT PRIMARY KEY, question TEXT NOT NULL, answer TEXT NOT NULL,
            sources_json TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """)

def replace_knowledge_base(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    with connection() as conn:
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM documents")
        for doc in documents:
            digest = hashlib.sha256(doc["text"].encode("utf-8")).hexdigest()
            cursor = conn.execute("INSERT INTO documents(url,title,content_hash,char_count) VALUES(?,?,?,?)",
                                  (doc["url"], doc["title"], digest, len(doc["text"])))
            document_id = cursor.lastrowid
            for chunk_index, chunk in enumerate(doc["chunks"]):
                chunk_id = conn.execute("INSERT INTO chunks(document_id,chunk_index,text) VALUES(?,?,?)",
                                        (document_id, chunk_index, chunk)).lastrowid
                records.append({"id": chunk_id, "document_id": document_id, "url": doc["url"],
                                "title": doc["title"], "chunk_index": chunk_index, "text": chunk})
        conn.execute("DELETE FROM answer_cache")
        conn.execute("INSERT INTO app_meta(key,value) VALUES('kb_version',?) "
                     "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(time.time_ns()),))
    return records

def document_summary():
    with connection() as conn:
        rows = conn.execute("SELECT id,url,title,char_count,fetched_at FROM documents ORDER BY id").fetchall()
    return [dict(row) for row in rows]

def get_cache(key):
    with connection() as conn:
        row = conn.execute("SELECT answer,sources_json FROM answer_cache WHERE cache_key=?", (key,)).fetchone()
    return {"answer": row["answer"], "sources": json.loads(row["sources_json"])} if row else None

def set_cache(key, question, answer, sources):
    with connection() as conn:
        conn.execute("INSERT INTO answer_cache(cache_key,question,answer,sources_json) VALUES(?,?,?,?) "
                     "ON CONFLICT(cache_key) DO UPDATE SET answer=excluded.answer,"
                     "sources_json=excluded.sources_json,created_at=CURRENT_TIMESTAMP",
                     (key, question, answer, json.dumps(sources, ensure_ascii=False)))

def get_kb_version():
    with connection() as conn:
        row = conn.execute("SELECT value FROM app_meta WHERE key='kb_version'").fetchone()
    return row["value"] if row else "empty"

def get_app_stats():
    with connection() as conn:
        documents = conn.execute("SELECT COUNT(*) AS n FROM documents").fetchone()["n"]
        chunks = conn.execute("SELECT COUNT(*) AS n FROM chunks").fetchone()["n"]
        cached_answers = conn.execute("SELECT COUNT(*) AS n FROM answer_cache").fetchone()["n"]
    return {"documents": documents, "chunks": chunks, "cached_answers": cached_answers}

def make_cache_key(question, version):
    normalized = " ".join(question.lower().split())
    return hashlib.sha256(f"{version}:{normalized}".encode("utf-8")).hexdigest()
