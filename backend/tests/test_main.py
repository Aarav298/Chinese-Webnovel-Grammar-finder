from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_analyze():
    response = client.post("/analyze", json={"text": "This is test string"})
    assert response.status_code == 200
    assert response.json() == {"analyses" : [{
        "sentence": "This is test string",
        "pattern": "pattern works",
        "hsk_level": 3,
        "explanation": "explanation works"
    }]}

def test_analyze_missing_text():
    response = client.post("/analyze", json={})
    assert response.status_code == 422

def test_analyze_wrong_type():
    response = client.post("/analyze", json={"text": 123})
    assert response.status_code == 422

def test_analyze_whitespace():
    response = client.post("/analyze", json={"text": " "})
    assert response.status_code == 422