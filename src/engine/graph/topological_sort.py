# topological_sort.py

from __future__ import annotations

from collections import deque
from typing import List

from .dependency_graph import DependencyGraph

def topological_sort(d: DependencyGraph) -> List[str]:
    indegree = dict(d.indegree)
    ready = deque()

    for n in d.nodes:
        if indegree[n] == 0:
            ready.append(n)

    order = []
    while ready:
        popped = ready.popleft()
        order.append(popped)

        neighbors = d.adjacency.get(popped, [])  # default empty list
        for n in neighbors:
            indegree[n] -= 1
            if indegree[n] == 0:
                ready.append(n)

    if len(order) != len(d.nodes):
        remaining = [n for n in d.nodes if indegree[n] > 0]
        raise ValueError(f"Cycle detected involving: {remaining}")

    return order



























