# run_context.py

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class RunContext:
    run_id: str
    run_dir: Path
    artifacts_dir: Path
    steps_dir: Path
    manifest_path: Path
    created_at: str
