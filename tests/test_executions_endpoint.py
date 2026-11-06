from fastapi.testclient import TestClient

from app.main import app, execution_kernel

client = TestClient(app)


def test_executions_endpoint():
    execution_kernel.history.clear()

    response = client.post(
        "/inference",
        json={
            "function": "wasm_add",
            "input": {
                "a": 10,
                "b": 20,
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == 30
    assert response.json()["status"] == "completed"

    history_response = client.get("/executions")

    assert history_response.status_code == 200

    data = history_response.json()

    assert data["total"] == 1
    assert data["executions"][0]["function"] == "wasm_add"
    assert data["executions"][0]["result"] == 30
    assert data["executions"][0]["status"] == "completed"
