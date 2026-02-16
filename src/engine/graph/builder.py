# builder.py

from __future__ import annotations
from engine.pipeline_spec import PipelineSpec
from dependency_graph import DependencyGraph

def build_graph(p: PipelineSpec):

    nodes = {s.id for s in p.steps}

    adjacency = {node_id: [] for node_id in nodes}
    indegree = {node_id: 0 for node_id in nodes}

    for s in p.steps:
        for prereq_id in s.depends_on:
            adjacency[prereq_id].append(s.id)
            indegree[s.id] += 1

    return DependencyGraph(
        nodes= nodes,
        adjacency=adjacency,
        indegree=indegree
    )









