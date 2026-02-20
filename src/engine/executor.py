# executor.py

from __future__ import annotations

from pathlib import Path
from typing import List
import time
from datetime import datetime, timezone

from engine.pipeline_spec import PipelineSpec
from engine.step_registry import StepRegistry
from engine.state import StepStatus
from engine.manifest_writer import (
    update_step,
    update_step_artifacts,
    update_pipeline_end,
)


def execute_pipeline(pipeline_spec: PipelineSpec,
                     order_list: List[str],
                     registry: StepRegistry,
                     manifest_path: Path,
                      ):
    run_started = time.time()
    run_dir = manifest_path.parent
    steps_by_id = {s.id: s for s in pipeline_spec.steps}

    for step_id in order_list:

        spec = steps_by_id[step_id]
        step_retries = (
            spec.retries
            if spec.retries is not None
            else pipeline_spec.defaults.retries
        )

        step_backoff = (
            spec.backoff_seconds
            if spec.backoff_seconds is not None
            else pipeline_spec.defaults.backoff_seconds
        )

        handler = registry.get(spec.type)

        step_dir = run_dir / "steps" / step_id
        step_dir.mkdir(parents=True, exist_ok=True)

        artifacts_step_dir = run_dir / "artifacts" / step_id
        artifacts_step_dir.mkdir(parents=True, exist_ok=True)

        attempt = 0
        max_attempts = 1 + step_retries
        started_at = datetime.now(timezone.utc).isoformat()

        update_step(
            path=manifest_path,
            step_id=step_id,
            status=StepStatus.RUNNING,
            started_at=started_at,
            max_retries=step_retries,
            backoff_seconds=step_backoff,
            attempts=0,
        )
        while True:
            attempt += 1
            update_step(
                path=manifest_path,
                step_id=step_id,
                attempts=attempt,
            )
            try:
                context = {
                    "run_dir": run_dir,
                    "step_id": step_id,
                    "step_dir": step_dir,
                    "artifacts_dir": artifacts_step_dir,
                }
                handler.run(spec.params, context)
                finished_at = datetime.now(timezone.utc).isoformat()

                step_log_path = step_dir / "step.log"
                metrics_path = step_dir / "metrics.json"

                outputs = sorted(
                    str(p.relative_to(run_dir))
                    for p in artifacts_step_dir.rglob("*")
                    if p.is_file()
                )

                log_path_str = str(step_log_path.relative_to(run_dir))

                metrics_path_str = (
                    str(metrics_path.relative_to(run_dir))
                    if metrics_path.exists()
                    else None
                )

                update_step_artifacts(
                    path=manifest_path,
                    step_id=step_id,
                    outputs=outputs,
                    log_path=log_path_str,
                    metrics_path=metrics_path_str,
                )

                update_step(
                    path=manifest_path,
                    step_id=step_id,
                    status=StepStatus.SUCCESS,
                    finished_at=finished_at
                )
                break

            except Exception as e:
                if attempt >= max_attempts:
                    finished_at = datetime.now(timezone.utc).isoformat()
                    update_step(
                        path=manifest_path,
                        step_id=step_id,
                        status=StepStatus.FAILED,
                        finished_at=finished_at,
                        error_message=str(e)
                    )
                    run_finished = datetime.now(timezone.utc).isoformat()
                    duration_seconds = time.time() - run_started

                    update_pipeline_end(
                        path=manifest_path,
                        status="FAILED",
                        finished_at=run_finished,
                        duration_seconds=duration_seconds,
                    )
                    raise
                else:
                   time.sleep(step_backoff)

    run_finished = datetime.now(timezone.utc).isoformat()
    duration_seconds = time.time() - run_started

    update_pipeline_end(
        path=manifest_path,
        status="SUCCESS",
        finished_at=run_finished,
        duration_seconds=duration_seconds,
    )






