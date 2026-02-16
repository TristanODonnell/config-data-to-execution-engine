# dependency_graph.py

from dataclasses import dataclass
from typing import Set, Dict, List, Optional

@dataclass(frozen=True)
class DependencyGraph:
    nodes: Set[str]
    adjacency: Dict[str, List[str]]
    indegree: Dict[str, int]






