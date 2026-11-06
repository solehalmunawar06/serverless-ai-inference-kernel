import os
import time
import wasmtime


class WasmRuntime:
    """Runtime generik untuk menjalankan modul WebAssembly menggunakan Wasmtime."""

    SPECIES = {
        0: "Iris Setosa",
        1: "Iris Versicolor",
        2: "Iris Virginica",
    }

    def __init__(self, wasm_path: str):
        if not os.path.exists(wasm_path):
            raise FileNotFoundError(
                f"WASM module tidak ditemukan: {wasm_path}"
            )

        self.wasm_path = wasm_path
        self.engine = wasmtime.Engine()
        self.module = wasmtime.Module.from_file(
            self.engine,
            self.wasm_path,
        )

    def execute(self, function_name: str, *args):
        """Menjalankan export function dari modul WASM."""
        store = wasmtime.Store(self.engine)

        instance = wasmtime.Instance(
            store,
            self.module,
            [],
        )

        function = instance.exports(store)[function_name]

        start = time.perf_counter()

        result = function(store, *args)

        execution_time_ms = (
            time.perf_counter() - start
        ) * 1000

        return {
            "result": int(result),
            "execution_time_ms": round(
                execution_time_ms,
                4,
            ),
        }

    def classify(
        self,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
    ):
        """Menjalankan klasifikasi Iris melalui iris.wasm."""

        values = [
            sepal_length,
            sepal_width,
            petal_length,
            petal_width,
        ]

        if any(value < 0 for value in values):
            raise ValueError("Nilai input tidak boleh negatif.")

        wasm_inputs = [
            round(sepal_length * 10),
            round(sepal_width * 10),
            round(petal_length * 10),
            round(petal_width * 10),
        ]

        execution = self.execute(
            "classify",
            *wasm_inputs,
        )

        prediction = execution["result"]

        return {
            "prediction": prediction,
            "species": self.SPECIES.get(
                prediction,
                "Unknown",
            ),
            "input": {
                "sepal_length": sepal_length,
                "sepal_width": sepal_width,
                "petal_length": petal_length,
                "petal_width": petal_width,
            },
            "wasm_inputs": wasm_inputs,
            "execution_time_ms": execution[
                "execution_time_ms"
            ],
        }
