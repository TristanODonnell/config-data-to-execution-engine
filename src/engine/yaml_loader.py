# YAML_loader
import sys
from pathlib import Path
import yaml

def load_yaml(pipeline_path: str | Path) -> dict:
    path = Path(pipeline_path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data or {}

if __name__ == "__main__":
    config_path = Path(sys.argv[1])
    config = load_yaml(config_path)
    print(config)

