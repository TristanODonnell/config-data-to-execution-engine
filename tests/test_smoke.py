
from __future__ import annotations

import pytest
from engine.yaml_loader import load_yaml


def test_smoke_load_yaml():
    cfg = load_yaml("configs/config_v1.yaml")

    assert cfg["pipeline"]["name"] == "example_pipeline"