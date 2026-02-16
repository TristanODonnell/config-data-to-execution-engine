# validator.py

from __future__ import annotations

from engine.pipeline_spec import PipelineSpec

def validate_dependencies(p: PipelineSpec):
    step_ids = {s.id for s in p.steps}

    for s in p.steps:
        for prereq_id in s.depends_on:
            if prereq_id not in step_ids:
                raise ValueError(
                    f"Step '{s.id}' depends_on unknown step '{prereq_id}'"
                )

        if s.id in s.depends_on:
            raise ValueError(
                f"Step '{s.id}' cannot depend on itself"
            )