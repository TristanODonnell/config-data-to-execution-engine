# pipeline_validator.py

from __future__ import annotations

from engine.pipeline_spec import PipelineSpec, StepSpec
from engine.step_registry import StepRegistry
def validate_pipeline(p: PipelineSpec) -> None :

    # name required
    if not p.name or not p.name.strip():
        raise ValueError("Missing/Invalid pipeline name")

    # steps must be a non-empty list
    if not isinstance(p.steps, list):
        raise TypeError("Steps must be a list")
    if len(p.steps) == 0:
        raise ValueError("Pipeline must contain at least one step")

    # each step must be a StepSpec with required fields
    for s in p.steps:
        if not isinstance(s, StepSpec):
            raise TypeError("Each step must be a StepSpec")

        if s.id is None or s.id.strip() == "":
            raise ValueError("Step missing/invalid id")

        if s.type is None or s.type.strip() == "":
            raise ValueError(f"Step '{s.id}' missing/invalid type")

    for s in p.steps:
        if not s.id:
            raise ValueError(f"Missing id inside step {s}")
        if not s.id:
            raise ValueError(f"Missing type inside step {s}")


    # ids must be unique
    all_ids = [s.id for s in p.steps]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Duplicate step ids found")


def validate_step_types(p: PipelineSpec, registry: StepRegistry):
    missing = []

    for s in p.steps:
        if not registry.has(s.type):
            missing.append(s.type)

    if missing:
        missing = sorted(set(missing))
        known = registry.known_types()
        raise ValueError(
            f"Unknown step types: {missing}. "
            f"Known types: {known}"
        )

    return









