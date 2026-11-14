import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

cf4 = sig['canon_families']['<T4']
print("type of canon_families['<T4']:", type(cf4))
if isinstance(cf4, dict):
    print("Keys len:", len(cf4))
    print("First 20 keys:", list(cf4.keys())[:20])
    for k in list(cf4.keys())[:5]:
        print(f"  cf4[{k}] = {cf4[k]}")

# Also print canon_families for <T1, <T2, <T3:
for sk in ['<T1', '<T2', '<T3']:
    print(f"canon_families[{sk}] keys: {list(sig['canon_families'][sk].keys())}")
