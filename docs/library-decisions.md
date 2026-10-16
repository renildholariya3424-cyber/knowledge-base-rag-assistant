# Library decisions and trade-offs

| Component | Selection | Why it fits this MVP | Trade-offs |
|---|---|---|---|
| HTTP scraping | Requests + BeautifulSoup | Simple, inspectable, suitable for static HTML | Does not render JavaScript; sites may rate-limit or prohibit automated access |
| Chunking | Custom Python function | Easy to explain, test and tune | Character chunks can split semantic units |
| Embeddings | Sentence Transformers `all-MiniLM-L6-v2` | Small model with useful general semantic similarity | First run downloads weights; quality varies by domain/language |
| Vector retrieval | FAISS `IndexFlatIP` with normalized vectors | Exact local similarity ranking, simple persistence | No built-in metadata filtering or distributed operation |
| LLM inference | Ollama + Qwen2.5 3B | Local model endpoint; avoids hosted inference by default | Quality and speed depend on hardware and quantization |
| Metadata/cache | SQLite | Durable, transactional and zero-admin | Best for a small single-node app, not distributed high-write workloads |
| API | FastAPI + Pydantic | Typed validation and automatic OpenAPI docs | Production needs auth, rate limits and operational controls |
| UI | Streamlit | Fast iteration for a practical-test demo | Less control than a dedicated frontend framework |
| Tests | pytest + FastAPI TestClient | Repeatable checks for behavior and validation | Unit tests do not replace representative retrieval evaluation |

## Key trade-offs

- Local inference improves control over document flow, but the developer owns setup, updates and performance.
- Rebuilding FAISS is straightforward for a small corpus; incremental indexing and metadata filters are future work.
- The similarity threshold is a heuristic, not calibrated confidence. Tune it against a labeled question set.
- Knowledge-base versioning is included in cache keys, and re-ingestion clears cached answers.
- Scraping is restricted to public HTTP(S) URLs and rejects private/local destinations. Respect site terms and robots policies.
