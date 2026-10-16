from app.database import make_cache_key
from app.chunking import split_text


def test_cache_key_normalizes_whitespace_and_case():
    assert make_cache_key("  What is Python? ", "v1") == make_cache_key("what is python?", "v1")


def test_cache_key_changes_when_knowledge_base_changes():
    assert make_cache_key("what is python?", "v1") != make_cache_key("what is python?", "v2")


def test_chunking_preserves_non_empty_content():
    text = "Python lists are mutable sequences. " * 40
    chunks = split_text(text, chunk_size=120, overlap=20)
    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)
