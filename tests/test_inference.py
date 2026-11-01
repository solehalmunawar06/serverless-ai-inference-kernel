from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_echo():
    response = client.post(
        "/inference",
        json={
            "function": "echo",
            "input": "Halo Serverless AI"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["result"]["input"] == "Halo Serverless AI"


def test_uppercase():
    response = client.post(
        "/inference",
        json={
            "function": "uppercase",
            "input": "serverless ai inference kernel"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["result"] == "SERVERLESS AI INFERENCE KERNEL"


def test_function_not_found():
    response = client.post(
        "/inference",
        json={
            "function": "unknown",
            "input": "test"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "error"


def test_execution_time():
    response = client.post(
        "/inference",
        json={
            "function": "echo",
            "input": "test performance"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["execution_time_ms"] >= 0
