# compile.py

from __future__ import annotations

from typing import List

from .dependency_graph import DependencyGraph
from ..pipeline_spec import PipelineSpec
from .validator import validate_dependencies
from .builder import build_graph
from .topological_sort import topological_sort

def run_compile(p: PipelineSpec) -> List[str]:
    validate_dependencies(p)
    graph: DependencyGraph = build_graph(p)
    order_list = topological_sort(graph)
    return order_list




