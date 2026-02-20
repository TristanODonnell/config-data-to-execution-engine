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

def update_step_artifacts(
    path: Path,
    step_id: str,
    outputs: list[str] | None = None,
    log_path: str | None = None,
    metrics_path: str | None = None,
) -> None:
    manifest = read_manifest(path)

    step = manifest["steps"][step_id]
    artifacts = step["artifacts"]

    if outputs is not None:
        artifacts["outputs"] = outputs
    if log_path is not None:
        artifacts["log_path"] = log_path
    if metrics_path is not None:
        artifacts["metrics_path"] = metrics_path

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

def update_pipeline_end(
    path: Path,
    status: str,
    finished_at: str,
    duration_seconds: float,
) -> None:
    manifest = read_manifest(path)
    pipeline = manifest["pipeline"]

    pipeline["status"] = status
    pipeline["finished_at"] = finished_at
    pipeline["duration_seconds"] = duration_seconds

    write_manifest(path, manifest)




def init_manifest(
        path: Path,
        pipeline_name: str,
        order: list[str],
        created_at: str,
    ) -> None:
    manifest = {
        "pipeline": {
            "name": pipeline_name,
            "status": "RUNNING",
            "created_at": created_at,
            "finished_at": None,
            "duration_seconds": None,
        },
        "steps": {
            step_id: {
                "status": "PENDING",
                "attempts": 0,
                "max_retries": None,
                "backoff_seconds": None,
                "error_message": None,
                "started_at": None,
                "finished_at": None,

                "artifacts": {
                    "outputs": [],
                    "log_path": None,
                    "metrics_path": None,
                }
            }
            for step_id in order
        }
    }

    write_manifest(path, manifest)