# write_file.py
from __future__ import annotations

from pathlib import Path

class WriteFileStep:
    def run(self, params: dict, context: dict) -> None:
        text = params.get("text")
        if text is None:
            raise ValueError("write_file step requires 'text' param")

        run_dir: Path = context["run_dir"]
        step_id: str = context["step_id"]

        artifacts_dir = run_dir / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_dir / f"{step_id}.txt"

        output_path.write_text(text, encoding="utf-8")