from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import settings

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(settings.embedding_model, device=None)

def encode_texts(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.empty((0, 0), dtype="float32")
    vectors = get_embedding_model().encode(
        texts, convert_to_numpy=True, normalize_embeddings=True,
        show_progress_bar=len(texts) > 8
    )
    return np.asarray(vectors, dtype="float32")
