from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.database import document_summary, get_app_stats, init_db
from app.ingestion import DEFAULT_URLS, ingest_urls
from app.rag import answer_question
from app.vector_store import vector_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    vector_store.load()
    yield

app = FastAPI(title="Knowledge Base Q&A", version="1.1.0",
              description="Local-first RAG demo with FAISS retrieval, SQLite persistence and Ollama inference.",
              lifespan=lifespan)

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=4, ge=1, le=10)

class IngestRequest(BaseModel):
    urls: list[str] = Field(default_factory=lambda: DEFAULT_URLS, min_length=1, max_length=10)

@app.get("/")
def root():
    return {"name": "Knowledge Base Q&A", "status": "ok", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok", "vector_store_ready": vector_store.ready,
            "model_backend": "Ollama", **get_app_stats()}

@app.get("/documents")
def documents():
    return {"documents": document_summary()}

@app.post("/ingest")
def ingest(request: IngestRequest):
    try:
        return {"status": "completed", **ingest_urls(request.urls)}
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500,
            detail="Ingestion failed unexpectedly. Check the API terminal for details.") from exc

@app.post("/ask")
def ask(request: AskRequest):
    try:
        return answer_question(request.question, request.top_k)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500,
            detail="Question processing failed. Check the API terminal for details.") from exc
