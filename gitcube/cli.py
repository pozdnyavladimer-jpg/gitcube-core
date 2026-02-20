from __future__ import annotations

import argparse
from pathlib import Path

from analyze import analyze_repo_dict, analyze_repo_text
from report import print_report_json


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gitcube",
        description="Structural Stability & Entropy Analyzer",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    analyze_parser = sub.add_parser(
        "analyze",
        help="Analyze a repository folder",
    )

    analyze_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to repository",
    )

    analyze_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON report",
    )

    args = parser.parse_args()

    if args.cmd == "analyze":
        path = Path(args.path)

        if args.json:
            report = analyze_repo_dict(path)
            print_report_json(report)
        else:
            analyze_repo_text(path)


if __name__ == "__main__":
    main()
