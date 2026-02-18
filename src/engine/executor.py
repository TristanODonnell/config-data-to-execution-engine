# executor.py

from __future__ import annotations

from pathlib import Path
from typing import List

from engine.pipeline_spec import PipelineSpec
from engine.step_registry import StepRegistry
from engine.manifest_writer import update_step_status
from engine.state import StepStatus
def execute_pipeline(pipeline_spec: PipelineSpec,
                     order_list: List[str],
                     registry: StepRegistry,
                     manifest_path: Path,
                      ):
    steps_by_id = {s.id: s for s in pipeline_spec.steps}

    for step_id in order_list:
        spec = steps_by_id[step_id]

        handler = registry.get(spec.type)

        update_step_status(manifest_path, step_id, StepStatus.RUNNING)
        try:
            handler.run(spec.params)
            update_step_status(manifest_path, step_id, StepStatus.SUCCESS)
        except Exception:
            update_step_status(manifest_path, step_id, StepStatus.FAILED)
            raise





