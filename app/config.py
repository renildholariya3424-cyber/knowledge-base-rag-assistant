import os
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    database_path: Path = ROOT_DIR / "data" / "app.db"
    vector_store_dir: Path = ROOT_DIR / "vector_store"
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    top_k: int = int(os.getenv("TOP_K", "4"))
    min_relevance_score: float = float(os.getenv("MIN_RELEVANCE_SCORE", "0.25"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "20"))

settings = Settings()
