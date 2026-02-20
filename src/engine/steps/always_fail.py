# always_fail.py

from engine.steps.base_step import BaseStep

class AlwaysFailStep(BaseStep):
    def run(self, params: dict, context: dict) -> None:
        raise RuntimeError("Intentional always-fail error")