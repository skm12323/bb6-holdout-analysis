import json
import os

path = "work_gc_sigma/sigma4_20000000.json"
size = os.path.getsize(path)
print(f"File size: {size} bytes ({size / (1024*1024):.2f} MB)")

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Top-level keys:", list(data.keys()))
for k in data.keys():
    v = data[k]
    if isinstance(v, dict):
        print(f"Key {k}: dict with keys {list(v.keys())[:10]} (len={len(v)})")
    elif isinstance(v, list):
        print(f"Key {k}: list of len={len(v)}")
    else:
        print(f"Key {k}: {type(v)} = {v}")
