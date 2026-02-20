from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from .ingest import FileInfo
from .graph import Graph
from .metrics import Metrics


def build_report_dict(
    path: Path,
    files: List[FileInfo],
    graph: Graph,
    metrics: Metrics,
    extra: Dict[str, Any],
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

    action = extra.get("action", {})
    recommendation = action.get("recommendation", "UNKNOWN")

    warnings: List[str] = []
    if recommendation == "BLOCK":
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
            "axis_1_4_7_ready": recommendation != "BLOCK",
            "state": "OPEN" if recommendation != "BLOCK" else "CLOSED",
        },
        "metrics": {
            "entropy_score": float(metrics.entropy_score),
            "cycle_index": float(metrics.cycle_index),
            "churn_accel": float(metrics.churn_accel),
            "density": float(metrics.density),
            "n_nodes": int(metrics.n_nodes),
            "n_edges": int(metrics.n_edges),
            "shadow_level": "HIGH" if metrics.entropy_score >= 0.65 else "OK",
        },
        "action": action,
        "thresholds": extra.get("thresholds", {}),
        "dna": extra.get("dna", {}),
        "baseline": extra.get("baseline", {}),
        "warnings": warnings,
    }


def print_report_json(report: Dict[str, Any]) -> None:
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False))

def print_report(path: Path, files: List[FileInfo], graph: Graph, metrics: Metrics, extra: Dict[str, Any]) -> None:
    action = extra.get("action", {})
    recommendation = action.get("recommendation", "UNKNOWN")
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
    if recommendation == "BLOCK":
        print("[!] MERU GATE WARNING: Apex is starved. Base is heavy.")
        print("[!] Axis 1-4-7 Ready: FALSE (Bindu is CLOSED)")
        print()
    print("Metrics:")
    print(f" -> EntropyScore : {metrics.entropy_score:.2f} ({'HIGH SHADOW' if metrics.entropy_score>=0.65 else 'OK'})")
    print(f" -> CycleIndex   : {metrics.cycle_index:.2f} ({'Topological Knots Detected' if metrics.cycle_index>0 else 'No cycles detected'})")
    print(f" -> ChurnAccel   : {metrics.churn_accel:.2f}")
    print(f" -> Density      : {metrics.density:.2f}")
    dna = extra.get("dna", {})
    if isinstance(dna, dict) and dna.get("signature"):
        print(f" -> DNA          : {dna['signature']}")
    print()
    print("Action:")
    print(f" -> Recommendation: [ {recommendation} MERGE ]")
    if recommendation != "ALLOW" and metrics.cycle_index > 0:
        print(" -> Required: Refactor cyclic dependencies (imports).")
    print()
