# pipeline_spec.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class DefaultsSpec:
    retries: int = 0
    backoff_seconds: int = 0

@dataclass(frozen=True)
class StepSpec:
    id: str
    type: str
    params: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class PipelineSpec:
    name: str
    defaults: DefaultsSpec
    steps: List[StepSpec]
