from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_valid():
    response = client.post(
        "/generate",
        json={
            "prompt": "A beautiful pink flower",
            "steps": 8,
            "seed": 42
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["image_path"] == "images/generated.png"

def test_generate_invalid_steps():
    response = client.post(
        "/generate",
        json={
            "prompt": "A beautiful pink flower",
            "steps": -5,
            "seed": 42
        }
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert errors[0]["loc"][1] == "steps"