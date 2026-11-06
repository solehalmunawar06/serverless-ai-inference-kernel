from time import perf_counter
from typing import Any, Callable
from uuid import uuid4

from models.sandbox import ProcessSandbox


class ExecutionKernel:
    def __init__(
        self,
        functions: dict[str, Callable],
        wasm_function_names: set[str] | None = None,
    ):
        self.functions = functions
        self.wasm_function_names = wasm_function_names or set()
        self.history: list[dict[str, Any]] = []
        self.sandbox = ProcessSandbox(
            timeout_seconds=3.0,
            cpu_limit=2,
        )

    def execute(
        self,
        function_name: str,
        data: Any,
    ) -> dict[str, Any]:

        execution_id = str(uuid4())
        start_time = perf_counter()

        ai_function = self.functions.get(function_name)

        if ai_function is None:
            execution = {
                "execution_id": execution_id,
                "function": function_name,
                "result": f"Function '{function_name}' not found",
                "execution_time_ms": 0,
                "status": "error",
            }

            self.history.append(execution)
            return execution

        is_wasm = function_name in self.wasm_function_names

        try:
            if is_wasm:
                # WASM inference dijalankan di child process.
                sandbox_result = self.sandbox.execute(
                    ai_function,
                    data,
                )

                execution_time = (
                    perf_counter() - start_time
                ) * 1000

                execution = {
                    "execution_id": execution_id,
                    "function": function_name,
                    "result": sandbox_result.get("result"),
                    "execution_time_ms": round(
                        execution_time,
                        3,
                    ),
                    "status": sandbox_result.get(
                        "status",
                        "error",
                    ),
                    "runtime": "wasm",
                    "sandbox": sandbox_result.get(
                        "sandbox",
                        "process",
                    ),
                    "pid": sandbox_result.get("pid"),
                    "lifecycle": sandbox_result.get(
                        "lifecycle",
                        "create → execute → return → terminate",
                    ),
                }

                if sandbox_result.get("error"):
                    execution["error"] = sandbox_result["error"]

            else:
                # Function Python biasa tetap berjalan normal.
                result = ai_function(data)

                execution_time = (
                    perf_counter() - start_time
                ) * 1000

                execution = {
                    "execution_id": execution_id,
                    "function": function_name,
                    "result": result,
                    "execution_time_ms": round(
                        execution_time,
                        3,
                    ),
                    "status": "completed",
                    "runtime": "python",
                    "lifecycle": (
                        "receive → execute → return"
                    ),
                }

        except Exception as exc:
            execution_time = (
                perf_counter() - start_time
            ) * 1000

            execution = {
                "execution_id": execution_id,
                "function": function_name,
                "result": str(exc),
                "execution_time_ms": round(
                    execution_time,
                    3,
                ),
                "status": "error",
            }

            if is_wasm:
                execution["runtime"] = "wasm"
                execution["sandbox"] = "process"
                execution["lifecycle"] = (
                    "create → execute → terminate"
                )
            else:
                execution["runtime"] = "python"

        self.history.append(execution)
        return execution

    def get_history(self) -> list[dict[str, Any]]:
        return self.history
