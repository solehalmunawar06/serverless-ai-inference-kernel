from statistics import mean


RUNS = 10


def benchmark(kernel, name, function_name, data):
    # Warm-up
    kernel.execute(function_name, data)

    results = []

    for _ in range(RUNS):
        result = kernel.execute(function_name, data)
        results.append(result)

    times = [
        item["execution_time_ms"]
        for item in results
        if item.get("status") == "completed"
    ]

    print()
    print("=" * 50)
    print(name)
    print("=" * 50)

    print(f"Runs       : {RUNS}")
    print(f"Completed  : {len(times)}")

    if times:
        print(f"Average    : {mean(times):.3f} ms")
        print(f"Minimum    : {min(times):.3f} ms")
        print(f"Maximum    : {max(times):.3f} ms")

    last = results[-1]

    print(f"Runtime    : {last.get('runtime', '-')}")
    print(f"Sandbox    : {last.get('sandbox', 'none')}")

    if last.get("pid"):
        print(f"PID        : {last['pid']}")

    print(f"Status     : {last.get('status')}")

    if last.get("status") == "error":
        print(f"Error      : {last.get('error', last.get('result'))}")


def main():
    # Import hanya ketika main process menjalankan benchmark.
    # Ini mencegah forkserver child mengulang benchmark.py.
    from models.registry import AI_FUNCTIONS
    from models.wasm_functions import WASM_FUNCTIONS
    from models.execution import ExecutionKernel

    all_functions = {
        **AI_FUNCTIONS,
        **WASM_FUNCTIONS,
    }

    kernel = ExecutionKernel(
        all_functions,
        wasm_function_names=set(WASM_FUNCTIONS.keys()),
    )

    test_cases = {
        "Python Echo": (
            "echo",
            "Benchmark Serverless Kernel",
        ),
        "WASM Add": (
            "wasm_add",
            {
                "a": 10,
                "b": 20,
            },
        ),
        "Iris AI": (
            "iris",
            {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            },
        ),
    }

    print()
    print("=" * 50)
    print("SERVERLESS AI INFERENCE KERNEL BENCHMARK")
    print("=" * 50)
    print(f"Iterations : {RUNS}")
    print()

    for name, (function_name, data) in test_cases.items():
        benchmark(
            kernel,
            name,
            function_name,
            data,
        )

    print()
    print("=" * 50)
    print("BENCHMARK COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
