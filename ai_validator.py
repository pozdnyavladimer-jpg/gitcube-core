import json
import sys

with open("report.json", "r", encoding="utf-8") as f:
    r = json.load(f)

rec = (r.get("action") or {}).get("recommendation", "UNKNOWN")
entropy = (r.get("metrics") or {}).get("entropy_score", 0.0)
cycle = (r.get("metrics") or {}).get("cycle_index", 0.0)

print(f"[AI AGENT] recommendation={rec} entropy_score={entropy:.3f} cycle_index={cycle:.3f}")

if rec == "BLOCK":
    print("[AI AGENT] BLOCK: structural instability detected. Merge should be blocked.")
    sys.exit(1)

print("[AI AGENT] OK: merge can proceed.")
sys.exit(0)
