import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"
DEFAULT_URLS = [
    "https://docs.python.org/3/tutorial/introduction.html",
    "https://docs.python.org/3/tutorial/controlflow.html",
    "https://docs.python.org/3/tutorial/datastructures.html",
]
st.set_page_config(page_title="Knowledge Base Q&A", page_icon="📚", layout="wide",
                   initial_sidebar_state="expanded")
st.markdown("""
<style>
.stApp { background:#f7f8fc; }
[data-testid="stHeader"] { background:rgba(247,248,252,.92); }
.block-container { padding-top:2rem; padding-bottom:3rem; max-width:1320px; }
.hero { background:linear-gradient(125deg,#14213d 0%,#23395d 60%,#315c83 100%);
 padding:1.7rem 1.9rem; border-radius:18px; color:white; margin-bottom:1.1rem;
 box-shadow:0 10px 30px rgba(20,33,61,.12); }
.hero h1 { color:white; font-size:2rem; margin:0 0 .45rem 0; }
.hero p { color:#dce6f3; margin:0; font-size:1rem; }
.eyebrow { color:#9fd3ff; text-transform:uppercase; letter-spacing:.13em;
 font-size:.72rem; font-weight:700; margin-bottom:.5rem; }
.metric-card { background:white; border:1px solid #e7eaf1; border-radius:13px;
 padding:1rem 1.1rem; min-height:100px; }
.metric-label { color:#68758a; font-size:.82rem; margin-bottom:.4rem; }
.metric-value { color:#17243b; font-size:1.65rem; font-weight:750; line-height:1.2; }
.section-label { color:#26344d; font-size:1.08rem; font-weight:700; margin:.6rem 0; }
[data-testid="stSidebar"] { background:#eef1f7; border-right:1px solid #e0e5ef; }
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { color:#17243b; }
div.stButton > button[kind="primary"] { border:0; border-radius:9px; font-weight:650; padding:.65rem 1rem; }
div[data-testid="stChatMessage"] { border-radius:13px; }
.stTextArea textarea { font-size:.84rem; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


def get_json(path, timeout=5):
    response = requests.get(f"{API_BASE}{path}", timeout=timeout)
    response.raise_for_status()
    return response.json()


def show_sources(sources):
    if not sources:
        return
    st.markdown("**Sources used**")
    for source in sources:
        with st.expander(f'{source.get("citation", "")}  {source.get("title", "Source")}  ·  relevance {source.get("relevance", 0):.3f}'):
            st.markdown(f'**[Open source article]({source.get("url", "#")})**')
            st.caption(f'Chunk ID: {source.get("chunk_id", "n/a")}')
            st.write(source.get("excerpt", ""))

with st.sidebar:
    st.markdown("## Knowledge base")
    st.caption("Manage the articles your assistant is allowed to use.")
    url_text = st.text_area("Public article URLs · one per line", value="\n".join(DEFAULT_URLS),
                            height=155, help="Use public HTML pages you are permitted to access. One URL per line.")
    if st.button("↻  Scrape and index", type="primary", use_container_width=True):
        urls = [line.strip() for line in url_text.splitlines() if line.strip()]
        with st.spinner("Fetching pages, cleaning text and rebuilding the index…"):
            try:
                response = requests.post(f"{API_BASE}/ingest", json={"urls": urls}, timeout=300)
                response.raise_for_status()
                result = response.json()
                st.success(f'Indexed {result["documents_ingested"]} articles and {result["chunks_indexed"]} text chunks.')
                for error in result.get("errors", []):
                    st.warning(f'{error["url"]}: {error["error"]}')
            except requests.ConnectionError:
                st.error("The API is not reachable. Start FastAPI in a second terminal.")
            except requests.Timeout:
                st.error("Ingestion timed out. Check the API terminal to see whether indexing completed.")
            except requests.HTTPError:
                try: st.error(response.json().get("detail", "The API rejected the request."))
                except Exception: st.error("The API rejected the request. Check the API terminal.")
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
    st.divider()
    st.markdown("### System status")
    try:
        health = get_json("/health")
        st.success("API connected")
        st.caption("Vector index: ready" if health["vector_store_ready"] else "Vector index: not ready")
        st.caption("Inference: local Ollama")
    except requests.RequestException:
        st.error("API offline")
        st.caption("Start `uvicorn app.main:app --reload` in another terminal.")
    st.divider()
    st.caption("Local-first demo · FastAPI · FAISS · SQLite · Sentence Transformers · Ollama")
    st.caption("Prototype for a local, single-user demonstration.")

st.markdown("""
<div class="hero">
  <div class="eyebrow">Retrieval-Augmented Generation · Local demo</div>
  <h1>Knowledge Base Q&amp;A</h1>
  <p>Ask questions over selected documents. Inspect the evidence behind each answer.</p>
</div>
""", unsafe_allow_html=True)

try:
    health = get_json("/health")
    cols = st.columns(4)
    metrics = [("Indexed articles", health.get("documents", 0)),
               ("Searchable chunks", health.get("chunks", 0)),
               ("Cached answers", health.get("cached_answers", 0)),
               ("Knowledge index", "Ready" if health.get("vector_store_ready") else "Empty")]
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div>'
                        f'<div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
except requests.RequestException:
    st.warning("The API is currently unavailable. Start the backend to use the assistant.")

st.markdown('<div class="section-label">Ask your knowledge base</div>', unsafe_allow_html=True)
st.caption("Answers are grounded in retrieved passages. If evidence is weak, the assistant should say so.")
suggestions = ["What are Python lists used for?", "How does a for statement work?", "What is the purpose of range()?"]
cols = st.columns(3)
for col, suggestion in zip(cols, suggestions):
    with col:
        if st.button(suggestion, use_container_width=True):
            st.session_state["pending_question"] = suggestion

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("cached"):
            st.caption("⚡ Answer served from cache")
        elif message.get("latency_ms") is not None:
            st.caption(f'Processing time: {message["latency_ms"]} ms')
        show_sources(message.get("sources", []))

question = st.chat_input("Ask a question about your indexed documents…")
if not question and st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and preparing an evidence-based answer…"):
            try:
                response = requests.post(f"{API_BASE}/ask", json={"question": question, "top_k": 4}, timeout=300)
                response.raise_for_status()
                result = response.json()
                st.markdown(result["answer"])
                if result.get("cached"):
                    st.caption("⚡ Answer served from cache")
                elif result.get("latency_ms") is not None:
                    st.caption(f'Processing time: {result["latency_ms"]} ms')
                if result.get("mode") == "extractive_fallback":
                    st.info("Ollama was unavailable. This response contains direct document excerpts, not generated prose.")
                show_sources(result.get("sources", []))
                st.session_state.messages.append({"role": "assistant", "content": result["answer"],
                    "sources": result.get("sources", []), "cached": result.get("cached", False),
                    "latency_ms": result.get("latency_ms")})
            except requests.ConnectionError:
                st.error("The API is not reachable. Start FastAPI in a second terminal.")
            except requests.Timeout:
                st.error("The request timed out. Check the FastAPI and Ollama terminals.")
            except requests.HTTPError:
                try: st.error(response.json().get("detail", "The API returned an error."))
                except Exception: st.error("The API returned an error. Check the FastAPI terminal.")

if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()
st.caption("Tip: ask a question covered by the indexed articles, then open the source passages to verify the answer.")
