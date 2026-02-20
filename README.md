# gitcube-core

![Demo run](/demo_run.png)

**Structural Stability & Entropy Analyzer for Git Repositories**

GitCube Core turns a repo into a **dependency structure** and computes a compact set of **stability / entropy** signals.  
Goal: detect architectural “instability build-up” early and provide an explainable merge gate: **ALLOW / WARN / BLOCK**.

> **Navigator logic ("Shadow is Fuel")**
>
> We do **not** try to eliminate change/entropy. Change is how software evolves.
> GitCube behaves like a **navigator**:
> - **WARN** = healthy working chaos (allowed, but visible)
> - **BLOCK** = structural danger (likely to tear the system)

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

### 2c) Dynamic baseline (adaptive thresholds)
GitCube can learn what's *normal* for your repo (rolling baseline).

```bash
# writes/updates .gitcube/baseline.json
gitcube analyze . --json --update-baseline > gitcube_report.json
```

Then future runs compare against that baseline.

If you want to disable baselining and use size-based heuristics only:
```bash
gitcube analyze . --json --no-baseline > gitcube_report.json
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
- Recommendation: `ALLOW` / `WARN` / `BLOCK`

### Structural DNA (Topological Alphabet)
Every report contains a compact **DNA signature** for quick review in PRs:

Example:
```
G0 P1 C0 D0 S0 R0 K1
```

Symbols (levels: 0 OK, 1 WARN, 2 BLOCK):
- **G**: gate verdict (ALLOW/WARN/BLOCK)
- **P**: pressure (structural entropy)
- **C**: cycles (cyclic mass proxy)
- **D**: dependency density
- **S**: drift (reserved, v0.1 uses 0)
- **R**: risk lead (reserved, v0.1 may be 0)
- **K**: scale bucket (repo size)

### JSON output (machine interface)
`--json` emits a single JSON document with:
- `metrics`: numeric signals
- `thresholds`: per-metric WARN/BLOCK thresholds (adaptive when baseline exists)
- `action`: recommendation + reason
- `dna`: signature + per-symbol details
- `baseline`: where baseline file is and whether it was updated

## Repository structure
- `src/gitcube/` core library
- `src/gitcube/cli.py` command line entry
- `examples/` minimal demos
- `docs/` concept + metrics

## Case study (MVP)

### Apache Airflow (healthy reference)
When run against Apache Airflow, GitCube should typically report **ALLOW** with low structural pressure.
This demonstrates low false-positives: the sensor respects mature architecture.

### Synthetic chaos repo (controlled failure)
Use `examples/demo_repo_generator.py` to generate a small repo with deliberate cyclic imports.
GitCube should report **WARN/BLOCK** depending on the generated severity.

## License
AGPL-3.0
