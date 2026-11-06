import multiprocessing as mp
import os
import resource
import time
from typing import Any, Callable


class SandboxError(Exception):
    pass


def _worker(conn, function: Callable, data: Any, cpu_limit: int):
    """Worker process untuk menjalankan satu inference secara terisolasi."""
    try:
        # Batasi CPU process.
        resource.setrlimit(
            resource.RLIMIT_CPU,
            (cpu_limit, cpu_limit)
        )

        start = time.perf_counter()

        result = function(data)

        execution_time_ms = (time.perf_counter() - start) * 1000

        conn.send({
            "status": "completed",
            "result": result,
            "execution_time_ms": round(execution_time_ms, 4),
            "pid": os.getpid(),
        })

    except Exception as exc:
        conn.send({
            "status": "error",
            "error": str(exc),
            "pid": os.getpid(),
        })

    finally:
        conn.close()


class ProcessSandbox:
    """
    Menjalankan inference di child process.

    Setiap request:
    1. membuat process
    2. menjalankan function
    3. menerima hasil
    4. process dihentikan
    """

    def __init__(self, timeout_seconds: float = 3.0, cpu_limit: int = 2):
        self.timeout_seconds = timeout_seconds
        self.cpu_limit = cpu_limit
        self.context = mp.get_context("forkserver")

    def execute(self, function: Callable, data: Any) -> dict:
        parent_conn, child_conn = mp.Pipe(duplex=False)

        process = self.context.Process(
            target=_worker,
            args=(child_conn, function, data, self.cpu_limit),
        )

        start = time.perf_counter()
        process.start()
        child_conn.close()

        process.join(self.timeout_seconds)

        if process.is_alive():
            process.terminate()
            process.join()

            parent_conn.close()

            return {
                "status": "timeout",
                "error": (
                    f"Execution exceeded "
                    f"{self.timeout_seconds} seconds"
                ),
                "execution_time_ms": round(
                    (time.perf_counter() - start) * 1000,
                    4,
                ),
            }

        if parent_conn.poll():
            result = parent_conn.recv()
        else:
            result = {
                "status": "error",
                "error": (
                    f"Sandbox process exited with code "
                    f"{process.exitcode}"
                ),
            }

        parent_conn.close()

        result["sandbox"] = "process"
        result["lifecycle"] = (
            "create → execute → return → terminate"
        )

        return result
