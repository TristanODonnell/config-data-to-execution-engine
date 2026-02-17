# cli.py

from __future__ import annotations

import argparse

from engine.yaml_loader import load_yaml
from engine.pipeline_parser import parse_pipeline
from engine.pipeline_validator import validate_pipeline, validate_step_types
from engine.graph.compile import run_compile
from engine.step_registry import build_default_registry
def cli_parse(argv=None) -> argparse.Namespace :
    parser = argparse.ArgumentParser(
        description="Run a YAML pipeline (plan validates + prints plan only).")
    parser.add_argument(
        "pipeline_path",
        type=str,
        help="Path to the pipeline YAML file (e.g., pipelines/example.yaml).",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show full traceback on error."
    )

    parser.add_argument(
        "--plan",
        action="store_true",
        help="Show execution plan (do not execute pipeline)"
    )
    return parser.parse_args(argv)

def main():
    args = None
    try:
        args = cli_parse()
        print(f"[cli] args OK: {args.pipeline_path} plan={args.plan}")

        print("[cli] loading yaml...")
        cfg = load_yaml(args.pipeline_path)
        pipeline_raw = cfg["pipeline"]
        print("[cli] yaml loaded")

        print("[cli] parsing pipeline...")
        pipeline = parse_pipeline(pipeline_raw)
        print("[cli] pipeline parsed")

        print("[cli] validating pipeline...")
        validate_pipeline(pipeline)
        print("[cli] pipeline validated")

        # PLAN MODE (dry-run + ordering)
        if args.plan:
            step_registry = build_default_registry()
            validate_step_types(pipeline, step_registry)
            order = run_compile(pipeline)

            steps_by_id = {s.id: s for s in pipeline.steps}
            for i, step_id in enumerate(order, start=1):
                s = steps_by_id[step_id]
                deps = ", ".join(s.depends_on) if s.depends_on else "-"
                print(f"{i:02d}. {s.id}  [{s.type}]  deps: {deps}")

            return

    except Exception as e:
        if args is not None and getattr(args, "debug", False):
            raise
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
    # python -m engine.cli configs/config_v1.yaml --debug --plan

