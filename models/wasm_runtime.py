from pathlib import Path

from wasmtime import Instance, Module, Store


class WasmRuntime:
    def __init__(self, module_path: str):
        self.module_path = Path(module_path)

    def execute(self, function_name: str, *args):
        store = Store()

        module = Module.from_file(
            store.engine,
            str(self.module_path),
        )

        instance = Instance(store, module, [])

        function = instance.exports(store)[function_name]

        result = function(store, *args)

        return result
