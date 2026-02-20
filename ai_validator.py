"""AI Gate example.

This script reads GitCube JSON report from stdin or from a file and exits:
- 0 on ALLOW/WARN
- 3 on BLOCK

Usage:
  python ai_validator.py report.json
  cat report.json | python ai_validator.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_report(argv: list[str]) -> dict:
    if len(argv) >= 2:
        return json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def main() -> int:
    r = load_report(sys.argv)
    action = r.get("action", {})
    rec = str(action.get("recommendation", "UNKNOWN")).upper()
    dna = (r.get("dna", {}) or {}).get("signature", "")
    entropy = (r.get("metrics", {}) or {}).get("entropy_score", None)

    print(f"[GitCube] recommendation={rec} entropy_score={entropy} dna='{dna}'")
    if rec == "BLOCK":
        print("[GitCube] BLOCK: failing CI.")
        return 3
    print("[GitCube] OK: passing CI.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
