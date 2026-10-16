from app.chunking import split_text
from app.config import settings
from app.database import init_db, replace_knowledge_base
from app.scraper import scrape_article
from app.vector_store import vector_store

DEFAULT_URLS = [
    "https://docs.python.org/3/tutorial/introduction.html",
    "https://docs.python.org/3/tutorial/controlflow.html",
    "https://docs.python.org/3/tutorial/datastructures.html",
]

def ingest_urls(urls: list[str]) -> dict:
    urls = list(dict.fromkeys(url.strip() for url in urls if url.strip()))
    if not urls:
        raise ValueError("Add at least one article URL.")
    init_db()
    documents, errors = [], []
    for url in urls:
        try:
            article = scrape_article(url, timeout=settings.request_timeout)
            article["chunks"] = split_text(article["text"], settings.chunk_size, settings.chunk_overlap)
            documents.append(article)
        except Exception as exc:
            errors.append({"url": url, "error": str(exc)})
    if not documents:
        details = "; ".join(f"{e['url']}: {e['error']}" for e in errors)
        raise RuntimeError("No articles could be ingested. " + details)
    records = replace_knowledge_base(documents)
    vector_store.build(records)
    return {
        "documents_ingested": len(documents), "chunks_indexed": len(records),
        "documents": [{"title": d["title"], "url": d["url"]} for d in documents],
        "errors": errors
    }
