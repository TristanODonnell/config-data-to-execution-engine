# paths.py

from __future__ import annotations
from pathlib import Path

def resolve_artifact_path(step_dir: Path, rel_path: str) -> Path:
    """
    Resolve rel_path under step_dir and prevent path traversal / absolute writes
    """
    base = step_dir.resolve()
    p = (step_dir / rel_path).resolve()

    if p != base and base not in p.parents:
        raise ValueError(f"Illegal path outside step_dir: {p}")

    return p
