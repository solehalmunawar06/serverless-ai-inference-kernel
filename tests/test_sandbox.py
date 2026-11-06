from models.sandbox import ProcessSandbox


def multiply_by_two(x):
    return x * 2


def raise_zero_division(x):
    return 1 / 0


def test_sandbox_success():
    sandbox = ProcessSandbox()

    result = sandbox.execute(multiply_by_two, 21)

    assert result["status"] == "completed"
    assert result["result"] == 42
    assert result["sandbox"] == "process"
    assert result["lifecycle"] == "create → execute → return → terminate"


def test_sandbox_error():
    sandbox = ProcessSandbox()

    result = sandbox.execute(raise_zero_division, None)

    assert result["status"] == "error"
    assert "division by zero" in result["error"]
    assert result["sandbox"] == "process"
