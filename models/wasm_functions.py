from models.wasm_runtime import WasmRuntime


ADD_RUNTIME = WasmRuntime("wasm/inference.wat")
IRIS_RUNTIME = WasmRuntime("wasm/functions/iris.wasm")


def wasm_add(data):
    """Menjalankan penjumlahan melalui WebAssembly."""

    result = ADD_RUNTIME.execute(
        "add",
        int(data["a"]),
        int(data["b"]),
    )

    return {
        "operation": "WebAssembly Addition",
        "a": int(data["a"]),
        "b": int(data["b"]),
        "result": result["result"],
        "runtime": "Wasmtime",
        "execution_time_ms": result["execution_time_ms"],
    }


def iris_inference(data):
    """Menjalankan klasifikasi Iris melalui WebAssembly."""

    required = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
    ]

    missing = [
        field
        for field in required
        if field not in data
    ]

    if missing:
        raise ValueError(
            f"Input Iris kurang: {', '.join(missing)}"
        )

    return IRIS_RUNTIME.classify(
        float(data["sepal_length"]),
        float(data["sepal_width"]),
        float(data["petal_length"]),
        float(data["petal_width"]),
    )


WASM_FUNCTIONS = {
    "wasm_add": wasm_add,
    "iris": iris_inference,
}
