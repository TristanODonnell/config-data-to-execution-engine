# manifest_writer.py
from __future__ import annotations

import json
from pathlib import Path


from engine.state import StepStatus
def read_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

def write_manifest(path: Path, manifest: dict) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4)

def update_step_status(path: Path, step_id: str, status: StepStatus) -> None:
    manifest = read_manifest(path)
    manifest["steps"][step_id]["status"] = status.value
    write_manifest(path, manifest)