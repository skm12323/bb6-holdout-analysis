import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

print("sig['E']:", sig['E'])
print("sig['E_out_variant']:", sig['E_out_variant'])
