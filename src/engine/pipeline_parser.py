# pipeline_parser.py

from __future__ import annotations

from typing import List, Dict

from engine.pipeline_spec import DefaultsSpec, StepSpec, PipelineSpec

def parse_pipeline(pipeline_raw: Dict) -> PipelineSpec :

    steps_raw = pipeline_raw["steps"]
    steps: List[StepSpec] = []

    # parse steps
    for step_dict in steps_raw:
        step = StepSpec(
            id=step_dict["id"],
            type=step_dict["type"],
            params=step_dict.get("params", {}),
            depends_on=step_dict.get("depends_on", [])
        )
        steps.append(step)

    # parse defaults
    defaults_raw = pipeline_raw.get("defaults", {})
    defaults = DefaultsSpec(
        retries=defaults_raw.get("retries", DefaultsSpec().retries),
        backoff_seconds=defaults_raw.get("backoff_seconds", DefaultsSpec().backoff_seconds)
    )

    # return pipeline spec
    return PipelineSpec(
        name=pipeline_raw["name"],
        defaults=defaults,
        steps=steps,
    )



