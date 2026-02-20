from __future__ import annotations
import ast
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
from .ingest import FileInfo

@dataclass
class Graph:
    nodes: Set[str]
    edges: Dict[str, Set[str]]  # src -> {dst}

def _module_name_from_path(p) -> str:
    # very simple mapping: file name without suffix
    return p.stem

def build_import_graph(files: List[FileInfo]) -> Graph:
    nodes: Set[str] = set()
    edges: Dict[str, Set[str]] = {}

    for f in files:
        mod = _module_name_from_path(f.path)
        nodes.add(mod)
        edges.setdefault(mod, set())

        try:
            tree = ast.parse(f.text)
        except SyntaxError:
            continue

        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    dst = alias.name.split(".")[0]
                    edges[mod].add(dst)
                    nodes.add(dst)
            elif isinstance(n, ast.ImportFrom):
                if n.module:
                    dst = n.module.split(".")[0]
                    edges[mod].add(dst)
                    nodes.add(dst)

    # ensure all nodes exist in edges dict
    for n in list(nodes):
        edges.setdefault(n, set())
    return Graph(nodes=nodes, edges=edges)
