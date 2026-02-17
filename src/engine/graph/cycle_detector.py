# cycle_detector.py

from __future__ import annotations

from collections import deque

from dependency_graph import DependencyGraph

def detect_cycle(d: DependencyGraph):
    indegree = dict(d.indegree)
    ready = deque()

    for n in d.nodes:
        if d.indegree[n] == 0:
            ready.append(n)

    order = []
    while ready:
        popped = ready.popleft()
        order.append(popped)

        neighbors = d.adjacency.get(popped, [])   # default empty list
        for n in neighbors:
            indegree[n] -= 1
            if d.indegree[n] == 0:
                ready.append(n)

    if len(order) != len(d.nodes):
        raise Exception("Cycle Exists")

    return























    

