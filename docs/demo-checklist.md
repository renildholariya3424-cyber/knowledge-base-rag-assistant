# Demo rehearsal checklist

Run the following before sharing the project or presenting it.

## Startup

- [ ] Activate the project's virtual environment.
- [ ] Confirm Ollama is running and `ollama list` includes `qwen2.5:3b`.
- [ ] Start `uvicorn app.main:app --reload` in terminal 1.
- [ ] Confirm `http://127.0.0.1:8000/health` returns status `ok`.
- [ ] Start `streamlit run streamlit_app.py` in terminal 2.

## Functional demo

- [ ] Click **Scrape and index** and record how many articles/chunks were indexed.
- [ ] Ask `What are Python lists used for?` and inspect the source passage.
- [ ] Ask `How does a for statement work in Python?` and inspect the source passage.
- [ ] Ask `What is the capital of Japan?` and confirm the assistant declines when evidence is insufficient.
- [ ] Ask the same supported question twice and check for the cache-hit label.
- [ ] Restart FastAPI and confirm the persisted index loads.
- [ ] Run `pytest -q` and record the result.

## Honest presentation notes

- The relevance threshold is heuristic, not a calibrated confidence probability.
- A cache hit is exact-question reuse after whitespace/case normalization, not semantic caching.
- The extractive fallback returns retrieved text and must not be described as an LLM answer.
- This is a local single-user MVP. Do not claim production readiness, guaranteed hallucination prevention, or enterprise security.
