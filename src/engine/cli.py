# cli.py

from __future__ import annotations

import argparse
import traceback

from engine.yaml_loader import load_yaml
from engine.pipeline_parser import parse_pipeline
from engine.pipeline_validator import validate_pipeline

def cli_parse(argv=None) -> argparse.Namespace :
    parser = argparse.ArgumentParser(
        description="Run a YAML pipeline (dry-run validates + prints plan only).")
    parser.add_argument(
        "pipeline_path",
        type=str,
        help="Path to the pipeline YAML file (e.g., pipelines/example.yaml).",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate + compile + print execution plan; do not execute steps."
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show full traceback on error."
    )
    return parser.parse_args(argv)

def main():
    try:
        args = cli_parse()
        print(f"[cli] args OK: {args.pipeline_path} dry_run={args.dry_run}")

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


        if args.dry_run:
            print("Dry-run OK: pipeline parsed + validated.")
            print(f"Pipeline: {pipeline.name}")
            print(f"Steps: {len(pipeline.steps)}")
            return

        print("Execute not implemented yet.")

    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
    # python -m engine.cli configs/config_v1.yaml --dry-run --debug
