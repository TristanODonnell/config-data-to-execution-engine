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

def update_step(
    path: Path,
    step_id: str,
    status: StepStatus | None = None,
    attempts: int | None = None,
    error_message: str | None = None,
    started_at: str | None = None,
    finished_at: str | None = None,
    max_retries: int | None = None,
    backoff_seconds: int | None = None,
) -> None:
    manifest = read_manifest(path)
    step = manifest["steps"][step_id]

    if status is not None:
        step["status"] = status.value
    if attempts is not None:
        step["attempts"] = attempts
    if error_message is not None:
        step["error_message"] = error_message
    if started_at is not None:
        step["started_at"] = started_at
    if finished_at is not None:
        step["finished_at"] = finished_at
    if max_retries is not None:
        step["max_retries"] = max_retries
    if backoff_seconds is not None:
        step["backoff_seconds"] = backoff_seconds

    write_manifest(path, manifest)

def update_pipeline_status(
        path: Path,
        status: str | None = None,
) -> None:
    manifest = read_manifest(path)
    pipeline = manifest["pipeline"]
    if status is not None:
        pipeline["status"] = status

    write_manifest(path, manifest)


def init_manifest(path: Path, pipeline_name: str, order: list[str]) -> None:
    manifest = {
        "pipeline": {
            "name": pipeline_name,
            "status": "RUNNING"
        },
        "steps": {
            step_id: {
                "status": "PENDING",
                "attempts": 0,
                "max_retries": None,      # set later when step resolves config
                "backoff_seconds": None,  # set later
                "error_message": None,
                "started_at": None,
                "finished_at": None,
            }
            for step_id in order
        }
    }

    write_manifest(path, manifest)