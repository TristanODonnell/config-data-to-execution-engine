# copy_file.py

import shutil
from pathlib import Path


class CopyFileStep:
    def run(self, params: dict, context: dict) -> None:
        source_path = params.get("path")
        if source_path is None:
            raise ValueError("copy_file step requires 'path' param")

        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(f"Source file does not exist: {source}")

        run_dir: Path = context["run_dir"]
        step_id: str = context["step_id"]

        artifacts_dir = run_dir / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        destination = artifacts_dir / f"{step_id}_{source.name}"

        shutil.copy2(source, destination)
