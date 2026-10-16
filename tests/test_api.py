from fastapi.testclient import TestClient
from app.main import app

def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_empty_question_is_rejected():
    with TestClient(app) as client:
        response = client.post("/ask", json={"question": ""})
        assert response.status_code == 422
