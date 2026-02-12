# cli.py

from __future__ import annotations

import argparse

from yaml_loader import load_yaml
from pipeline_parser import parse_pipeline
from pipeline_validator import validate_pipeline

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
    return parser.parse_args(argv)

def main():
    args = cli_parse()

    pipeline_raw = load_yaml(args.pipeline_path)

    pipeline = parse_pipeline(pipeline_raw)

    validate_pipeline(pipeline)

    if args.dry_run:
        print("Dry-run OK: pipeline parsed + validated.")
        return

    print("Execute not implemented yet.")
    return


if __name__ == "__main__":
    main()