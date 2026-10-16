import pytest
from app.chunking import split_text

def test_empty_text_returns_no_chunks():
    assert split_text("   ") == []

def test_chunking_splits_long_text():
    text = " ".join(f"word{i}" for i in range(100))
    chunks = split_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(chunks)

def test_invalid_overlap_is_rejected():
    with pytest.raises(ValueError):
        split_text("hello", chunk_size=10, overlap=10)
