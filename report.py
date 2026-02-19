from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from .ingest import FileInfo
from .graph import Graph
from .metrics import Metrics, Action


def build_report_dict(
    path: Path,
    files: List[FileInfo],
    graph: Graph,
    metrics: Metrics,
    action: Action,
) -> Dict[str, Any]:
    """Return a machine-readable report.

    Notes:
    - This MVP keeps the 1/4/7 "octave" visualization as a conceptual proxy.
    - Later versions can replace this with a real 42-state lattice (V-CORE).
    """

    octave_distribution = [
        {"octave": 1, "label": "RED (Base)", "fill": 6, "total": 6},
        {"octave": 4, "label": "GREEN (Actuator)", "fill": 2, "total": 6},
        {"octave": 7, "label": "VIOLET (Apex)", "fill": 0, "total": 6},
    ]

    warnings: List[str] = []
    if action.recommendation == "BLOCK":
        warnings.append("MERU GATE WARNING: Apex is starved. Base is heavy.")
        warnings.append("Axis 1-4-7 Ready: FALSE (Bindu is CLOSED)")

    return {
        "tool": "gitcube-core",
        "engine": "V-CORE SriYantra Engine",
        "path": str(path),
        "file_count": len(files),
        "graph": {
            "nodes": int(len(getattr(graph, "nodes", []))),
            "edges": int(sum(len(v) for v in getattr(graph, "edges", {}).values())),
        },
        "octave_distribution": octave_distribution,
        "bindu": {
            "axis_1_4_7_ready": action.recommendation != "BLOCK",
            "state": "OPEN" if action.recommendation != "BLOCK" else "CLOSED",
        },
        "metrics": {
            "entropy_score": float(metrics.entropy_score),
            "cycle_index": float(metrics.cycle_index),
            "churn_accel": float(metrics.churn_accel),
            "shadow_level": "HIGH" if metrics.entropy_score >= 0.65 else "OK",
        },
        "action": {
            "recommendation": action.recommendation,
            "note": action.note,
            "required": "Refactor cyclic dependencies (imports)."
            if action.recommendation != "ALLOW" and metrics.cycle_index > 0
            else "",
        },
        "warnings": warnings,
    }


def print_report_json(report: Dict[str, Any]) -> None:
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False))

def print_report(path: Path, files: List[FileInfo], graph: Graph, metrics: Metrics, action: Action) -> None:
    print()
    print("[V-CORE SriYantra Engine] Scanning topology...")
    print(f"[+] Ingesting {len(files)} files...")
    print("[+] Building dependency graph...")
    print("[+] Calculating Shadow & Coherence...")
    print()
    print("="*52)
    print(" GitCube Structural Report")
    print("="*52)
    print()
    # very lightweight "octave" placeholder: show 1,4,7 as in screenshot concept
    print("Octave Distribution:")
    print(" 1 RED (Base)        : ⬢⬢⬢⬢⬢⬢ (6/6)")
    print(" 4 GREEN (Actuator)  : ⬢⬢⬡⬡⬡⬡ (2/6)")
    print(" 7 VIOLET (Apex)     : ⬡⬡⬡⬡⬡⬡ (0/6)")
    print()
    if action.recommendation == "BLOCK":
        print("[!] " + action.note)
        print("[!] Axis 1-4-7 Ready: FALSE (Bindu is CLOSED)")
        print()
    print("Metrics:")
    print(f" -> EntropyScore : {metrics.entropy_score:.2f} ({'HIGH SHADOW' if metrics.entropy_score>=0.65 else 'OK'})")
    print(f" -> CycleIndex   : {metrics.cycle_index:.2f} ({'Topological Knots Detected' if metrics.cycle_index>0 else 'No cycles detected'})")
    print(f" -> ChurnAccel   : {metrics.churn_accel:.2f}")
    print()
    print("Action:")
    print(f" -> Recommendation: [ {action.recommendation} MERGE ]")
    if action.recommendation != "ALLOW" and metrics.cycle_index > 0:
        print(" -> Required: Refactor cyclic dependencies (imports).")
    print()
