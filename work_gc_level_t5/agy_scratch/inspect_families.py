import json

with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Number of families:", len(data["families"]))
sample_fams = list(data["families"].items())[:10]
for k, v in sample_fams:
    print(f"Family {k}: {v}")

print("\nFamily status sample:")
for k in list(data["family_status"].keys())[:10]:
    print(f"Status for {k}: {data['family_status'][k]}")

# Check uncert families in family_status
uncert_fams = [k for k, v in data["family_status"].items() if v.get("uncert") or not v.get("ok", True)]
print(f"\nTotal uncertified families: {len(uncert_fams)}")
for k in uncert_fams:
    print(f"  {k}: {data['family_status'][k]}")

# Check specific families mentioned in prompt:
# 10/3+lift, -1/3, 46/9+lift, 7/3
prompt_fams = ['10/3/1', '-1/3/0', '46/9/1', '7/3/0', '10/3/0', '46/9/0']
for pf in prompt_fams:
    if pf in data["family_status"]:
        print(f"Prompt family {pf}: {data['family_status'][pf]}")
    else:
        print(f"Prompt family {pf} not in family_status directly, searching...")
        matches = [k for k in data["family_status"] if k.startswith(pf[:4])]
        print(f"  Matches: {matches}")
