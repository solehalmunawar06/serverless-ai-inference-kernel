from time import perf_counter
from typing import Any, Callable
from uuid import uuid4


class ExecutionKernel:
    def __init__(self, functions: dict[str, Callable]):
        self.functions = functions
        self.history: list[dict[str, Any]] = []

    def execute(self, function_name: str, data: Any) -> dict[str, Any]:
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

        try:
            result = ai_function(data)
            execution_time = (perf_counter() - start_time) * 1000

            execution = {
                "execution_id": execution_id,
                "function": function_name,
                "result": result,
                "execution_time_ms": round(execution_time, 3),
                "status": "completed",
            }

        except Exception as exc:
            execution_time = (perf_counter() - start_time) * 1000

            execution = {
                "execution_id": execution_id,
                "function": function_name,
                "result": str(exc),
                "execution_time_ms": round(execution_time, 3),
                "status": "error",
            }

        self.history.append(execution)
        return execution

    def get_history(self) -> list[dict[str, Any]]:
        return self.history
