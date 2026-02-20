# gitcube-core

![Demo run](demo_run.png)

**Structural Stability & Entropy Analyzer for Git Repositories**

GitCube Core turns a repo into a **dependency structure** and computes a compact set of **stability / entropy** signals.  
Goal: detect architectural “instability build-up” early and provide an explainable merge gate: **ALLOW / WARN / BLOCK**.

## Quick start

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Analyze a repo
```bash
gitcube analyze .
```

### 2b) Analyze and emit JSON (for CI/CD & AI agents)
```bash
gitcube analyze . --json > gitcube_report.json
```

### 3) Generate a tiny demo repo (with a cycle) and analyze it
```bash
python examples/demo_repo_generator.py
gitcube analyze demo_repo
```

## What you get (v0.1 MVP)
- Dependency graph extraction (Python imports)
- Metrics:
  - `EntropyScore` (0..1)
  - `CycleIndex`
  - `ChurnAccel` (placeholder; becomes real when git history is enabled)
- Recommendation:
  - `ALLOW` (<0.40)
  - `WARN` (0.40..0.65)
  - `BLOCK` (>=0.65) → **MERU GATE WARNING**

## Repository structure
- `src/gitcube/` core library
- `src/gitcube/cli.py` command line entry
- `examples/` minimal demos
- `docs/` concept + metrics

## License
AGPL-3.0
## Structural Contrast Demonstration

GitCube is a measurement instrument, not an alarm generator.
To validate signal integrity, we tested it on two opposite scenarios:

### 1️⃣ Real-World Mature Architecture
* **Project:** Apache Airflow
* **Type:** Large-scale production data platform
* **Scale:** 6,669 Python files, 3,332 modules, 20,037 dependency edges

**Result:**
`entropy_score: 0.0128` | `cycle_index: 0.0144` | `recommendation: ALLOW`

**Interpretation:** Minimal cyclic dependency clusters. Low structural entropy. Stable modular layering. No artificial warnings triggered. Airflow serves as a structural baseline for disciplined Python architecture.

---

### 2️⃣ Synthetic Chaos Repository
* **Project:** Generated via `examples/demo_repo_generator.py`
* **Type:** Artificial monolith with dense cyclic dependencies
* **Generated to simulate:** Cross-module circular imports, Layer violations, Strongly connected dependency clusters.

**Result:**
`entropy_score: HIGH` | `cycle_index: HIGH` | `recommendation: BLOCK`

**Interpretation:** Large strongly connected components. High dependency density. Structural instability detected. Automatic BLOCK triggered.

---

### Contrast Summary
| Project | Scale | Entropy | Cycle Index | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Apache Airflow** | 6,669 files | 0.0128 | 0.0144 | **ALLOW** |
| **Synthetic Chaos Repo** | Generated | High | High | **BLOCK** |

**Key Takeaway:** GitCube does not penalize scale. It detects structural degradation. 
Healthy architecture → ALLOW. Topological collapse → BLOCK. No drama. No false alarms. Only measurable structure.
