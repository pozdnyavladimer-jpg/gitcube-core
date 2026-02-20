from __future__ import annotations

import argparse
from pathlib import Path

from .analyze import analyze_repo_dict, analyze_repo_text
from .report import print_report_json

def main() -> None:
    p = argparse.ArgumentParser(prog="gitcube", description="Structural Stability & Entropy Analyzer for Git Repositories")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="Analyze a repository folder")
    a.add_argument("path", nargs="?", default=".", help="Path to repo (default: .)")
    a.add_argument("--json", action="store_true", help="Emit a JSON report (for CI/agents)")
    a.add_argument(
        "--baseline",
        default=None,
        help="Path to baseline file (default: .gitcube/baseline.json inside repo)",
    )
    a.add_argument(
        "--update-baseline",
        action="store_true",
        help="Update baseline with current metrics (writes baseline JSON)",
    )
    a.add_argument(
        "--no-baseline",
        action="store_true",
        help="Disable baselining (use size heuristics only)",
    )

    args = p.parse_args()
    if args.cmd == "analyze":
        path = Path(args.path)
        if args.json:
            report = analyze_repo_dict(
                path,
                baseline_path=Path(args.baseline) if args.baseline else None,
                update_baseline=bool(args.update_baseline),
                disable_baseline=bool(args.no_baseline),
            )
            print_report_json(report)
        else:
            analyze_repo_text(
                path,
                baseline_path=Path(args.baseline) if args.baseline else None,
                update_baseline=bool(args.update_baseline),
                disable_baseline=bool(args.no_baseline),
            )

if __name__ == "__main__":
    main()
