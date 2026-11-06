from models.registry import AI_FUNCTIONS
from models.wasm_functions import WASM_FUNCTIONS
from models.execution import ExecutionKernel


def create_kernel():
    return ExecutionKernel(
        {**AI_FUNCTIONS, **WASM_FUNCTIONS},
        wasm_function_names=set(WASM_FUNCTIONS.keys()),
    )


def test_wasm_add_via_kernel():
    kernel = create_kernel()

    result = kernel.execute("wasm_add", {"a": 10, "b": 20})

    assert result["status"] == "completed"
    assert result["runtime"] == "wasm"
    assert result["sandbox"] == "process"
    assert result["result"]["result"] == 30


def test_iris_inference():
    kernel = create_kernel()

    result = kernel.execute(
        "iris",
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )

    assert result["status"] == "completed"
    assert result["runtime"] == "wasm"
    assert result["sandbox"] == "process"


def test_iris_prediction():
    kernel = create_kernel()

    result = kernel.execute(
        "iris",
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )

    assert result["result"]["prediction"] == 0
    assert result["result"]["species"] == "Iris Setosa"


def test_iris_missing_input():
    kernel = create_kernel()

    result = kernel.execute(
        "iris",
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
        },
    )

    assert result["status"] == "error"
