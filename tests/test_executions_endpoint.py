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

    data = response.json()

    assert data["status"] == "completed"
    assert data["function"] == "wasm_add"
    assert data["runtime"] == "wasm"
    assert data["sandbox"] == "process"
    assert data["result"]["result"] == 30

    history_response = client.get("/executions")

    assert history_response.status_code == 200

    history = history_response.json()

    assert history["total"] == 1
    assert history["executions"][0]["function"] == "wasm_add"
