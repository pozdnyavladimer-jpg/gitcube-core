from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class FileInfo:
    path: Path
    text: str

def ingest_files(root: Path) -> List[FileInfo]:
    root = root.resolve()
    out: List[FileInfo] = []
    for p in root.rglob("*.py"):
        if any(part.startswith(".") for part in p.parts):
            continue
        try:
            out.append(FileInfo(path=p, text=p.read_text(encoding="utf-8", errors="ignore")))
        except Exception:
            continue
    return out
