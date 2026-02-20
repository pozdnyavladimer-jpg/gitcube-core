import json
import sys

with open("report.json", "r", encoding="utf-8") as f:
    report = json.load(f)

rec = report.get("action", {}).get("recommendation", "UNKNOWN")
entropy = report.get("metrics", {}).get("entropy_score", 0.0)

print(f"[AI] recommendation={rec} entropy={entropy}")

if rec == "BLOCK":
    print("[AI] BLOCK -> failing job")
    sys.exit(3)

print("[AI] OK")
sys.exit(0)
