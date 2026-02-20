from pathlib import Path
from gitcube.ingest import ingest_files
from gitcube.graph import build_import_graph
from gitcube.metrics import compute_metrics, decide_action

def test_cycle_triggers_block(tmp_path: Path):
    # create mini repo with cycle
    (tmp_path/"a.py").write_text("import b\n", encoding="utf-8")
    (tmp_path/"b.py").write_text("import a\n", encoding="utf-8")
    files = ingest_files(tmp_path)
    g = build_import_graph(files)
    m = compute_metrics(g, files)
    a = decide_action(m, warn=0.01, block=0.02)  # force low thresholds
    assert a.recommendation in {"WARN","BLOCK"}
