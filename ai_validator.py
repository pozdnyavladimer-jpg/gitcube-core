import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "report.json"

with open(path, "r", encoding="utf-8") as f:
    matrix = json.load(f)

rec = matrix.get("action", {}).get("recommendation", "UNKNOWN")
entropy = matrix.get("metrics", {}).get("entropy_score", 0.0)

print(f"[AI AGENT] entropy_score={entropy} recommendation={rec}")

if rec == "BLOCK":
    print("[AI AGENT] BLOCK -> failing workflow")
    sys.exit(3)

print("[AI AGENT] OK -> passing workflow")
sys.exit(0)
