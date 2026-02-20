from __future__ import annotations

"""Topological Alphabet (Structural DNA) for GitCube.

We compress structural state into an 8-symbol signature suitable for PR comments
and AI agents.

Levels:
  0 = OK
  1 = WARN
  2 = BLOCK
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class DNAPiece:
    symbol: str
    level: int
    value: float
    warn: float
    block: float
    note: str


def _level(value: float, warn: float, block: float) -> int:
    # If thresholds are not defined (0/0), treat as OK.
    if warn == 0.0 and block == 0.0:
        return 0
    if value >= block:
        return 2
    if value >= warn:
        return 1
    return 0


def build_structural_dna(
    *,
    metrics: Dict[str, float],
    thresholds: Dict[str, Dict[str, float]],
    gate: str,
    n_nodes: int,
) -> Dict[str, Any]:
    pieces: Dict[str, DNAPiece] = {}

    def add(metric_key: str, symbol: str, note: str) -> None:
        v = float(metrics.get(metric_key, 0.0) or 0.0)
        th = thresholds.get(metric_key, {})
        w = float(th.get("warn", 0.0) or 0.0)
        b = float(th.get("block", 0.0) or 0.0)
        pieces[symbol] = DNAPiece(
            symbol=symbol,
            level=_level(v, w, b),
            value=v,
            warn=w,
            block=b,
            note=note,
        )

    # 8 symbols: G,P,C,D,S,R,K (+L reserved for future)
    add("entropy_score", "P", "Pressure (structural entropy)")
    add("cycle_index", "C", "Cycles (SCC/cyclic mass proxy)")
    add("density", "D", "Dependency density (edges per node)")
    add("change_score", "S", "Structural drift (graph delta / churn)")
    add("churn_accel", "R", "Risk lead (entropy acceleration; v0.1 may be 0)")

    # K: scale bucket
    if n_nodes < 200:
        k = 0
    elif n_nodes < 2_000:
        k = 1
    elif n_nodes < 20_000:
        k = 2
    else:
        k = 3
    pieces["K"] = DNAPiece("K", k, float(n_nodes), 0.0, 0.0, "Scale bucket")

    # G: gate verdict
    g_map = {"ALLOW": "A", "WARN": "W", "BLOCK": "B"}
    g = g_map.get(gate.upper(), "?")
    pieces["G"] = DNAPiece("G", {"A": 0, "W": 1, "B": 2}.get(g, 0), 0.0, 0.0, 0.0, f"Meru gate verdict={gate}")

    order = ["G", "P", "C", "D", "S", "R", "K"]
    sig = " ".join([f"{s}{pieces[s].level}" for s in order if s in pieces])

    return {
        "signature": sig,
        "gate": gate,
        "symbols": {
            s: {
                "level": p.level,
                "value": p.value,
                "warn": p.warn,
                "block": p.block,
                "note": p.note,
            }
            for s, p in pieces.items()
        },
    }
