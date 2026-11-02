from models.execution import ExecutionKernel
from models.registry import AI_FUNCTIONS


def test_kernel_echo():
    kernel = ExecutionKernel(AI_FUNCTIONS)

    result = kernel.execute("echo", "Halo Kernel")

    assert result["status"] == "completed"
    assert result["function"] == "echo"
    assert result["result"]["input"] == "Halo Kernel"


def test_kernel_uppercase():
    kernel = ExecutionKernel(AI_FUNCTIONS)

    result = kernel.execute("uppercase", "serverless ai")

    assert result["status"] == "completed"
    assert result["function"] == "uppercase"
    assert result["result"] == "SERVERLESS AI"


def test_kernel_unknown_function():
    kernel = ExecutionKernel(AI_FUNCTIONS)

    result = kernel.execute("unknown", "test")

    assert result["status"] == "error"
    assert "not found" in result["result"]


def test_kernel_history():
    kernel = ExecutionKernel(AI_FUNCTIONS)

    kernel.execute("echo", "one")
    kernel.execute("uppercase", "two")

    history = kernel.get_history()

    assert len(history) == 2
