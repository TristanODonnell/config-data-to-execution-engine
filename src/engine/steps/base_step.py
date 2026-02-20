# base_step.py

class BaseStep:
    def run(self, params: dict, context: dict) -> None:
        raise NotImplementedError
