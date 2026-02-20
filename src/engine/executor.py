# executor.py

from __future__ import annotations

from pathlib import Path
from typing import List
import time


from engine.pipeline_spec import PipelineSpec
from engine.step_registry import StepRegistry
from engine.manifest_writer import update_step_status
from engine.state import StepStatus


def execute_pipeline(pipeline_spec: PipelineSpec,
                     order_list: List[str],
                     registry: StepRegistry,
                     manifest_path: Path,
                      ):
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

        update_step_status(manifest_path, step_id, StepStatus.RUNNING)
        attempt = 0
        max_attempts = 1 + step_retries
        while True:
            attempt += 1
            try:
                context = {
                    "run_dir": run_dir,
                    "step_id": step_id,
                    "step_dir": step_dir,
                }
                handler.run(spec.params, context)
                update_step_status(manifest_path, step_id, StepStatus.SUCCESS)
                break

            except Exception:
                if attempt >= max_attempts:
                    update_step_status(manifest_path, step_id, StepStatus.FAILED)
                    raise
                else:
                   time.sleep(step_backoff)







