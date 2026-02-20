# setup_run.py
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import secrets
from typing import List
import yaml

from engine.pipeline_spec import PipelineSpec
from engine.run_context import RunContext
from engine.manifest_writer import init_manifest

def setup_run(p: PipelineSpec, order: List[str]) -> RunContext:

    ctx = init_run_context()
    spec_dict = asdict(p)

    init_manifest(
        ctx.manifest_path,
        p.name,
        order
    )
    snapshot_path = ctx.run_dir / "pipeline_snapshot.yaml"

    with snapshot_path.open("w") as f:
        yaml.safe_dump(spec_dict, f, sort_keys=False)

    for step_id in order:
        (ctx.steps_dir / step_id).mkdir(exist_ok=False)
        (ctx.artifacts_dir / step_id).mkdir(exist_ok=False)

    return ctx


def init_run_context() -> RunContext:
    now = datetime.now(timezone.utc)

    run_id = generate_run_id(now)

    run_dir = Path("runs") / run_id

    artifacts_dir = run_dir / "artifacts"
    steps_dir = run_dir / "steps"

    run_dir.mkdir(parents=True, exist_ok=False)
    steps_dir.mkdir(parents=True, exist_ok=False)
    artifacts_dir.mkdir(parents=True, exist_ok=False)

    manifest_path = run_dir / "manifest.json"

    return RunContext(
        run_id=run_id,
        run_dir=run_dir,
        steps_dir=steps_dir,
        artifacts_dir=artifacts_dir,
        created_at=now.isoformat(),
        manifest_path=manifest_path
    )


def generate_run_id(now: datetime) -> str:
    ts = now.strftime("%Y%m%d_%H%M%S")
    rand = secrets.token_hex(4)
    return f"{ts}_{rand}"