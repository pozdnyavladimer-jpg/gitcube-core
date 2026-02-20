from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, List
from .graph import Graph
from .ingest import FileInfo

@dataclass
class Metrics:
    entropy_score: float
    cycle_index: float
    churn_accel: float
    density: float
    n_nodes: int
    n_edges: int

@dataclass
class Action:
    recommendation: str  # ALLOW/WARN/BLOCK
    note: str

def _dfs_cycles(graph: Graph) -> Set[str]:
    # Return nodes that are part of at least one cycle (simple DFS back-edge detection)
    visiting: Set[str] = set()
    visited: Set[str] = set()
    in_cycle: Set[str] = set()

    def dfs(u: str, stack: List[str]) -> None:
        visiting.add(u)
        stack.append(u)
        for v in graph.edges.get(u, set()):
            if v not in graph.nodes:
                continue
            if v in visiting:
                # mark cycle nodes in current stack from v onward
                if v in stack:
                    idx = stack.index(v)
                    in_cycle.update(stack[idx:])
            elif v not in visited:
                dfs(v, stack)
        stack.pop()
        visiting.remove(u)
        visited.add(u)

    for n in graph.nodes:
        if n not in visited:
            dfs(n, [])
    return in_cycle

def compute_metrics(graph: Graph, files: List[FileInfo]) -> Metrics:
    n = max(1, len(graph.nodes))
    m = sum(len(v) for v in graph.edges.values())

    # density (0..1-ish) for directed graph without self edges
    density = m / max(1, n*(n-1))

    cyc_nodes = _dfs_cycles(graph)
    cycle_index = len(cyc_nodes) / n

    # entropy_score: simple, explainable weighting
    entropy = min(1.0, 0.35 * density + 0.85 * cycle_index)

    # placeholder: in v0.2 compute from git history
    churn_accel = 0.0
    return Metrics(
        entropy_score=float(entropy),
        cycle_index=float(cycle_index),
        churn_accel=float(churn_accel),
        density=float(density),
        n_nodes=int(n),
        n_edges=int(m),
    )

def decide_action(metrics: Metrics, *, warn=0.40, block=0.65) -> Action:
    if metrics.entropy_score >= block:
        return Action("BLOCK", "MERU GATE WARNING: Apex is starved. Base is heavy.")
    if metrics.entropy_score >= warn:
        return Action("WARN", "MERU GATE: instability rising, consider refactor.")
    return Action("ALLOW", "MERU GATE: stable.")
