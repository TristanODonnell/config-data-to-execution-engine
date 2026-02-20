# copy_file.py
from __future__ import annotations

import shutil
from pathlib import Path

from engine.steps.base_step import BaseStep
from engine.paths import resolve_artifact_path


class CopyFileStep(BaseStep):
    def run(self, params: dict, context: dict) -> None:
        rel_path = params.get("path")
        if rel_path is None:
            raise ValueError("copy_file step requires 'path' param")

        run_dir: Path = context["run_dir"]

        from_step = params.get("from_step")

        if from_step:
            source = run_dir / "artifacts" / from_step / rel_path
        else:
            source = Path(rel_path)

        if not source.exists():
            raise FileNotFoundError(f"Source file does not exist: {source}")

        # Write destination ONLY inside this step's folder
        dest_rel = params.get("dest", Path(rel_path).name)
        artifacts_dir: Path = context["artifacts_dir"]
        destination = resolve_artifact_path(artifacts_dir, dest_rel)

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
