# fail_once.py
from engine.steps.base_step import BaseStep


class FailOnceStep(BaseStep):
    def run(self, params: dict, context: dict) -> None:
        marker_file = context["step_dir"] / "fail_once_marker"

        if not marker_file.exists():
            marker_file.write_text("failed")
            raise RuntimeError("Intentional fail-once error")

        # Second run succeeds