from models.wasm_runtime import WasmRuntime


def test_wasm_runtime_add():
    runtime = WasmRuntime("wasm/inference.wat")

    result = runtime.execute("add", 10, 20)

    assert result["result"] == 30
    assert result["execution_time_ms"] >= 0
