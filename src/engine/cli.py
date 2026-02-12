# cli.py

import argparse

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
    print("hello world!")

if __name__ == "__main__":
    main()