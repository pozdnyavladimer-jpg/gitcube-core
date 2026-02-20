from __future__ import annotations

"""Dynamic baselining for GitCube.

Goal: make WARN/BLOCK thresholds adapt to each repository.

We keep this deliberately lightweight:
- Baseline file is a small JSON stored at .gitcube/baseline.json (can be committed).
- It stores recent metric samples (rolling window) and derived robust stats.
- Thresholds are computed as median + k*MAD (robust to outliers).

This is not "ML". It's explainable control logic.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import math
import statistics


def _median(values: List[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def _mad(values: List[float], *, center: Optional[float] = None) -> float:
    """Median absolute deviation (MAD)."""
    if not values:
        return 0.0
    c = _median(values) if center is None else float(center)
    dev = [abs(v - c) for v in values]
    return _median(dev)


@dataclass
class DynamicThresholds:
    warn: float
    block: float
    method: str  # "baseline" or "heuristic"


class RepoBaseline:
    """A small rolling baseline for repo-specific metrics."""

    def __init__(self, *, window: int = 30) -> None:
        self.window = int(window)
        self.samples: Dict[str, List[float]] = {}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RepoBaseline":
        rb = RepoBaseline(window=int(d.get("window", 30)))
        samples = d.get("samples", {}) or {}
        rb.samples = {k: [float(x) for x in (v or [])] for k, v in samples.items()}
        return rb

    def to_dict(self) -> Dict[str, Any]:
        return {"window": self.window, "samples": self.samples}

    def update(self, metrics: Dict[str, float]) -> None:
        """Append a metrics snapshot into rolling baseline."""
        for k, v in metrics.items():
            if v is None:
                continue
            arr = self.samples.setdefault(k, [])
            arr.append(float(v))
            if len(arr) > self.window:
                del arr[: len(arr) - self.window]

    def stats(self, key: str) -> tuple[float, float, int]:
        vals = self.samples.get(key, [])
        m = _median(vals)
        mad = _mad(vals, center=m)
        return m, mad, len(vals)


def load_baseline(path: Path) -> Optional[RepoBaseline]:
    try:
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return RepoBaseline.from_dict(data)
    except Exception:
        return None


def save_baseline(path: Path, baseline: RepoBaseline) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(baseline.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def thresholds_for_metric(
    *,
    key: str,
    value: float,
    n_nodes: int,
    n_edges: int,
    baseline: Optional[RepoBaseline],
    warn_k: float = 1.5,
    block_k: float = 3.0,
) -> DynamicThresholds:
    """Return WARN/BLOCK thresholds for a metric."""

    if baseline is not None:
        med, mad, n = baseline.stats(key)
        if n >= 8:
            warn = med + warn_k * mad
            block = med + block_k * mad
            if mad == 0.0:
                warn = med + 1e-6
                block = med + 2e-6
            return DynamicThresholds(float(warn), float(block), "baseline")

    # Heuristic mode (size-aware)
    size = max(1, int(n_nodes))
    lg = math.log10(size)
    density = (float(n_edges) / float(size)) if size else 0.0

    if key == "entropy_score":
        warn = 0.02 + 0.006 * lg
        block = 0.05 + 0.012 * lg
    elif key == "cycle_index":
        warn = 0.02 + 0.01 * lg
        block = 0.05 + 0.02 * lg
    elif key == "density":
        warn = density * 1.25
        block = density * 1.75
    else:
        warn = float(value) * 1.25
        block = float(value) * 1.75

    return DynamicThresholds(float(warn), float(block), "heuristic")
