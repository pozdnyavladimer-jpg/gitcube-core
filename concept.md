# GitCube Concept (plain version)

GitCube Core treats code as a **structure**, not a text.

Pipeline:
1) Ingest repository
2) Build dependency graph
3) Compute stability metrics (entropy, cycles, churn)
4) Convert to a single score (EntropyScore 0..1)
5) Decide: ALLOW / WARN / BLOCK

This is explainable on purpose. The aim is a small, testable core that can later power:
- CI merge gates
- dashboards
- AI agents that refactor towards stability
