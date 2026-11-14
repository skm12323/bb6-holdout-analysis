import json

with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys in levels_t5_20000000.json:", list(data.keys()))
for k in data.keys():
    v = data[k]
    if isinstance(v, dict):
        print(f"  {k}: dict with {len(v)} keys: {list(v.keys())[:10]}")
    elif isinstance(v, list):
        print(f"  {k}: list with {len(v)} items: {v[:5]}")
    else:
        print(f"  {k}: {v}")
