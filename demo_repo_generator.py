"""Generate a tiny synthetic repo with a cycle to demo GitCube."""
from pathlib import Path

def main() -> None:
    out = Path("demo_repo")
    out.mkdir(exist_ok=True)
    (out / "a.py").write_text("import b\n", encoding="utf-8")
    (out / "b.py").write_text("import a\n", encoding="utf-8")
    (out / "auth.py").write_text("import a\n", encoding="utf-8")
    (out / "README.md").write_text("# demo_repo\n", encoding="utf-8")
    print("Generated demo_repo with a circular import: a <-> b")

if __name__ == "__main__":
    main()
