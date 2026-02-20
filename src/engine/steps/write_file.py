# write_file.py
from __future__ import annotations
from pathlib import Path

from engine.paths import resolve_artifact_path
from engine.steps.base_step import BaseStep


class WriteFileStep(BaseStep):
    def run(self, params: dict, context: dict) -> None:
        text = params.get("text")
        if text is None:
            raise ValueError("write_file step requires 'text' param")

        # Optional filename; defaults make toy configs easy.
        rel_path = params.get("path", "output.txt")

        step_dir: Path = context["step_dir"]
        out_path = resolve_artifact_path(step_dir, rel_path)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(str(text), encoding="utf-8")
