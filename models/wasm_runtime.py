import os
import time
import wasmtime


class WasmRuntime:
    """Runtime untuk menjalankan fungsi AI WebAssembly menggunakan Wasmtime."""

    SPECIES = {
        0: "Iris Setosa",
        1: "Iris Versicolor",
        2: "Iris Virginica",
    }

    def __init__(self, wasm_path: str):
        if not os.path.exists(wasm_path):
            raise FileNotFoundError(f"WASM module tidak ditemukan: {wasm_path}")

        self.wasm_path = wasm_path
        self.engine = wasmtime.Engine()
        self.module = wasmtime.Module.from_file(
            self.engine,
            self.wasm_path,
        )

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

        store = wasmtime.Store(self.engine)

        instance = wasmtime.Instance(
            store,
            self.module,
            [],
        )

        classify_function = instance.exports(store)["classify"]

        # Modul WASM menggunakan integer dengan skala x10.
        wasm_inputs = [
            round(sepal_length * 10),
            round(sepal_width * 10),
            round(petal_length * 10),
            round(petal_width * 10),
        ]

        start = time.perf_counter()

        prediction = classify_function(
            store,
            *wasm_inputs,
        )

        execution_time_ms = (
            time.perf_counter() - start
        ) * 1000

        prediction = int(prediction)

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
            "execution_time_ms": round(
                execution_time_ms,
                4,
            ),
        }
