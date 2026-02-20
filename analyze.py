# -*- coding: utf-8 -*-
"""Repository analyzer entrypoint.

This module keeps the MVP intentionally small:
- Ingest Python files
- Build a lightweight dependency graph
- Compute a few stability metrics
- Decide ALLOW/BLOCK ("Meru gate")
- Produce both a human report and a machine-readable JSON report
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .ingest import ingest_files
from .graph import build_import_graph
from .metrics import compute_metrics
from .report import build_report_dict, print_report
from .baseline import load_baseline, save_baseline, thresholds_for_metric, RepoBaseline
from .dna import build_structural_dna


def _action_with_dynamic_thresholds(
    *,
    metrics,
    repo_root: Path,
    baseline_path: Path,
    update_baseline: bool,
    disable_baseline: bool,
) -> Dict[str, Any]:
    baseline = None if disable_baseline else load_baseline(baseline_path)
    if baseline is None and not disable_baseline:
        baseline = RepoBaseline(window=30)

    thresholds: Dict[str, Dict[str, float]] = {}
    # NOTE: v0.1 computes entropy_score/cycle_index/density.
    # churn_accel is reserved for future and is excluded from gating to avoid false BLOCK.
    for k in ["entropy_score", "cycle_index", "density"]:
        v = float(getattr(metrics, k))
        th = thresholds_for_metric(
            key=k,
            value=v,
            n_nodes=metrics.n_nodes,
            n_edges=metrics.n_edges,
            baseline=None if disable_baseline else baseline,
        )
        thresholds[k] = {"warn": th.warn, "block": th.block, "method": th.method}

    warn_count = 0
    block_hit = False
    for k, th in thresholds.items():
        v = float(getattr(metrics, k))
        if v >= float(th["block"]):
            block_hit = True
        elif v >= float(th["warn"]):
            warn_count += 1

    if block_hit:
        recommendation = "BLOCK"
        reason = "threshold_block"
    elif warn_count >= 2:
        recommendation = "WARN"
        reason = "threshold_warn_accumulated"
    elif warn_count == 1:
        recommendation = "WARN"
        reason = "threshold_warn"
    else:
        recommendation = "ALLOW"
        reason = "below_threshold"

    if (baseline is not None) and update_baseline and not disable_baseline:
        baseline.update({k: float(getattr(metrics, k)) for k in thresholds.keys()})
        save_baseline(baseline_path, baseline)

    dna = build_structural_dna(
        metrics={
            "entropy_score": metrics.entropy_score,
            "cycle_index": metrics.cycle_index,
            "density": metrics.density,
            "change_score": 0.0,
            "churn_accel": metrics.churn_accel,
        },
        thresholds=thresholds,
        gate=recommendation,
        n_nodes=metrics.n_nodes,
    )

    return {
        "action": {"recommendation": recommendation, "reason": reason},
        "thresholds": thresholds,
        "dna": dna,
        "baseline": {"path": str(baseline_path), "enabled": (not disable_baseline), "updated": bool(update_baseline)},
    }


def analyze_repo_dict(
    path: Path,
    *,
    baseline_path: Path | None = None,
    update_baseline: bool = False,
    disable_baseline: bool = False,
) -> Dict[str, Any]:
    files = ingest_files(path)
    graph = build_import_graph(files)
    metrics = compute_metrics(graph, files)
    bp = baseline_path or (path / ".gitcube" / "baseline.json")
    extra = _action_with_dynamic_thresholds(
        metrics=metrics,
        repo_root=path,
        baseline_path=bp,
        update_baseline=update_baseline,
        disable_baseline=disable_baseline,
    )
    return build_report_dict(path, files, graph, metrics, extra)


def analyze_repo_text(
    path: Path,
    *,
    baseline_path: Path | None = None,
    update_baseline: bool = False,
    disable_baseline: bool = False,
) -> Dict[str, Any]:
    """Print the pretty report and also return the dict (useful for tests/CI)."""
    files = ingest_files(path)
    graph = build_import_graph(files)
    metrics = compute_metrics(graph, files)
    bp = baseline_path or (path / ".gitcube" / "baseline.json")
    extra = _action_with_dynamic_thresholds(
        metrics=metrics,
        repo_root=path,
        baseline_path=bp,
        update_baseline=update_baseline,
        disable_baseline=disable_baseline,
    )
    print_report(path, files, graph, metrics, extra)
    return build_report_dict(path, files, graph, metrics, extra)
