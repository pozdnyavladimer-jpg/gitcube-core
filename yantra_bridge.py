"""Yantra bridge (experiment).

This file demonstrates how a GitCube JSON report can be mapped into the
VSriYantraCore packet model you shared.

It does NOT require any metaphysics: it's a deterministic mapping.

Input: report.json from `gitcube analyze . --json`
Output: a minimal VPacket-like dict (octave/strength/coherence/shadow)

Run:
  gitcube analyze . --json > report.json
  python examples/yantra_bridge.py report.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x


def map_to_octave(rec: str) -> int:
    rec = rec.upper()
    return {"ALLOW": 5, "WARN": 3, "BLOCK": 1}.get(rec, 2)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python examples/yantra_bridge.py report.json")
        return 2

    r = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    rec = r.get("action", {}).get("recommendation", "UNKNOWN")
    m = r.get("metrics", {})

    entropy = float(m.get("entropy_score", 0.0) or 0.0)
    cycles = float(m.get("cycle_index", 0.0) or 0.0)
    density = float(m.get("density", 0.0) or 0.0)

    # Shadow as a bounded combination of key "instability" signals.
    shadow = clamp(0.7 * entropy + 0.2 * cycles + 0.1 * clamp(density / 5.0))
    coherence = clamp(1.0 - shadow)

    # Strength = how decisive the structure is (low entropy -> strong).
    strength = clamp(0.15 + 0.85 * coherence)

    pkt = {
        "content": "gitcube_report",
        "topic": "logic",
        "octave": map_to_octave(str(rec)),
        "strength": strength,
        "coherence": coherence,
        "shadow": shadow,
        "note": {
            "recommendation": rec,
            "entropy_score": entropy,
            "cycle_index": cycles,
            "density": density,
            "dna": (r.get("dna", {}) or {}).get("signature", ""),
        },
    }

    print(json.dumps(pkt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
