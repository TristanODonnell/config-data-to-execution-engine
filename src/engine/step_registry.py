# step_registry.py

from .steps.copy_file import CopyFileStep
from .steps.write_file import WriteFileStep

class StepRegistry:
    def __init__(self):
        self._registry = {}


    def register(self, type_name: str, impl) -> None:
        if type_name in self._registry:
            raise ValueError(f"Step type '{type_name}' already registered")

        self._registry[type_name] = impl

    def has(self, type_name: str) -> bool:
        return type_name in self._registry

    def get(self, type_name: str):
        if type_name not in self._registry:
            known = list(self._registry.keys())
            raise ValueError(
                f"Unknown step type '{type_name}'. Known types: {known}"
            )

        return self._registry[type_name]

    def known_types(self):
        return list(self._registry.keys())


def build_default_registry() -> StepRegistry:
    registry = StepRegistry()

    registry.register("write_file", WriteFileStep)
    registry.register("copy_file", CopyFileStep)

    return registry
