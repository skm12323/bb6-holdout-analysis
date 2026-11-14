import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

print("Invariants:", json.dumps(sig['invariants'], indent=2))
print("Unexplained4:", json.dumps(sig['unexplained4'], indent=2))
