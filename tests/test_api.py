from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_query_invalid_body():
    response = client.post("/query", json={"not_a_query": "test"})
    assert response.status_code == 422
