from models.wasm_runtime import WasmRuntime


runtime = WasmRuntime("wasm/inference.wat")


def wasm_add(data):
    return runtime.execute(
        "add",
        int(data["a"]),
        int(data["b"]),
    )


WASM_FUNCTIONS = {
    "wasm_add": wasm_add,
}
