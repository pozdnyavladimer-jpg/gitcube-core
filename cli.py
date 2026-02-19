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

    args = p.parse_args()
    if args.cmd == "analyze":
            if args.cmd == "analyze":
        path = Path(args.path)
        
        # 1. Скануємо і отримуємо дані у вигляді словника
        report_data = analyze_repo_dict(path)
        
        # 2. Виводимо результат (JSON або текст)
        if args.json:
            print_report_json(report_data)
        else:
            analyze_repo_text(path)
            
        # 3. ДОДАЄМО "М'ЯЗИ" (EXIT CODES)
        import sys
        # Дістаємо рекомендацію зі структури report_data
        rec = report_data.get("action", {}).get("recommendation", "ALLOW")
        
        if rec == "BLOCK":
            sys.exit(3)  # Зупиняє GitHub Action як помилку
        elif rec == "WARN":
            sys.exit(2)  # Попереджує, але не вбиває
        else:
            sys.exit(0)  # Все чисто (Зелений спектр)
            

if __name__ == "__main__":
    main()
