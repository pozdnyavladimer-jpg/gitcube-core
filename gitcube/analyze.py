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
from .metrics import compute_metrics, decide_action
from .report import build_report_dict, print_report


def analyze_repo_dict(path: Path) -> Dict[str, Any]:
    files = ingest_files(path)
    graph = build_import_graph(files)
    metrics = compute_metrics(graph, files)
    action = decide_action(metrics)
    return build_report_dict(path, files, graph, metrics, action)


def analyze_repo_text(path: Path) -> Dict[str, Any]:
    """Print the pretty report and also return the dict (useful for tests/CI)."""
    files = ingest_files(path)
    graph = build_import_graph(files)
    metrics = compute_metrics(graph, files)
    action = decide_action(metrics)
    print_report(path, files, graph, metrics, action)
    return build_report_dict(path, files, graph, metrics, action)
