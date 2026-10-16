import json
import faiss
from app.config import settings
from app.embeddings import encode_texts

class LocalVectorStore:
    def __init__(self):
        self.index = None
        self.records = []

    @property
    def ready(self):
        return self.index is not None and bool(self.records)

    def build(self, records):
        if not records:
            self.index, self.records = None, []
            return
        vectors = encode_texts([record["text"] for record in records])
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        self.index, self.records = index, records
        self.save()

    def save(self):
        if not self.ready:
            return
        settings.vector_store_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(settings.vector_store_dir / "index.faiss"))
        with (settings.vector_store_dir / "records.json").open("w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def load(self):
        index_path = settings.vector_store_dir / "index.faiss"
        records_path = settings.vector_store_dir / "records.json"
        if not index_path.exists() or not records_path.exists():
            return False
        self.index = faiss.read_index(str(index_path))
        with records_path.open(encoding="utf-8") as f:
            self.records = json.load(f)
        return self.ready

    def search(self, query, top_k=4):
        if not self.ready:
            return []
        vector = encode_texts([query])
        scores, ids = self.index.search(vector, min(top_k, len(self.records)))
        results = []
        for score, record_id in zip(scores[0], ids[0]):
            if record_id >= 0:
                item = dict(self.records[int(record_id)])
                item["score"] = float(score)
                results.append(item)
        return results

vector_store = LocalVectorStore()
