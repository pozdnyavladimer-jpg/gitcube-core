import json
import sys

with open("report.json", "r") as f:
    data = json.load(f)

rec = data.get("action", {}).get("recommendation", "UNKNOWN")
entropy = data.get("metrics", {}).get("entropy_score", 0.0)

print(f"[V-CORE AGENT] Стан: {rec} | Ентропія: {entropy}")

if rec == "BLOCK":
    print("!!! ВХІД ЗАБОРОНЕНО: СТРУКТУРНИЙ ХАОС !!!")
    sys.exit(1)
sys.exit(0)
