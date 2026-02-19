# Metrics (v0.1)

- **CycleIndex**: fraction of nodes that participate in at least one cycle.
- **EntropyScore**: a simple weighted score:
  - graph density term
  - + cycle penalty term
  - mapped/clamped to 0..1
- **ChurnAccel**: placeholder in v0.1 (0.0). In v0.2 it uses git history.

Decision thresholds (default):
- EntropyScore < 0.40 -> ALLOW
- 0.40..0.65 -> WARN
- >= 0.65 -> BLOCK  (prints: MERU GATE WARNING)

Note: v0.1 intentionally keeps math simple and auditable.
