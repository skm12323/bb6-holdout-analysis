import json, sys
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table
from rational_certifier import certify_rational_scalar

with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== Level E ===")
E = data["E"]
print("E keys:", list(E.keys()))
print("E ints:", E["ints"])
print("E n_specific:", E["n_specific"])
print("E uncert_int:", E["uncert_int"])
print("E uncert_spec:", E["uncert_spec"])

print("\n=== Level C7E ===")
C7E = data["C7E"]
print("C7E keys:", list(C7E.keys()))
print("C7E ints:", C7E["ints"])
print("C7E n_specific:", C7E["n_specific"])
print("C7E uncert_int:", C7E["uncert_int"])
print("C7E uncert_spec:", C7E["uncert_spec"])

# Assertions from NOTES §6:
# 1. uncert_spec for E and C7E are [5, 21, -27, -11]
# Note order in json might vary, check set
expected_uncert_spec = [5, 21, -27, -11]
# In json, check how uncert_spec items are structured
print("\nVerifying uncert_spec structure:")
print("E uncert_spec:", E["uncert_spec"])
print("C7E uncert_spec:", C7E["uncert_spec"])

# Check C7E uncert_int:
# [{'kind': 'int', 'cls': 5, 'chains': [5]}]
assert C7E["uncert_int"] == [{'kind': 'int', 'cls': 5, 'chains': [5]}], f"C7E uncert_int mismatch: {C7E['uncert_int']}"
print("C7E uncert_int matches (5, 5) exactly!")

# Check specific entry certification:
# In json, are specific entries listed? Let's check
if "specific" in E:
    print(f"E specific count: {len(E['specific'])}")
if "specific" in C7E:
    print(f"C7E specific count: {len(C7E['specific'])}")

# Check exports in family_status:
# Let's search family_status for 37/9, 7/3, 23/3, 53/9
fstatus = data["family_status"]
print("\nChecking export families:")
for fam_key in ['37/9/0', '7/3/0', '23/3/1', '53/9/0']:
    if fam_key in fstatus:
        print(f"  {fam_key}: {fstatus[fam_key]}")
    else:
        print(f"  {fam_key} not in family_status directly")

# Let's certify some specific entries using our own scalar certifier
T = Table()
# For chain 5:
# class 5: fails (ceiling)
# class 21: fails (ceiling)
# class -27: fails (ceiling)
# class -11: fails (ceiling)
for cls in [5, 21, -27, -11]:
    res = certify_rational_scalar(T, 5, cls, 1, False)
    assert not res['ok'] and res['status'] == 'ceiling'
    print(f"Chain 5, cls={cls}: confirmed uncert (ceiling, word={res['word']})")

# Sample some other classes on chain 5:
for cls in [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, -1, -2, -3]:
    res = certify_rational_scalar(T, 5, cls, 1, False)
    print(f"Chain 5, cls={cls}: ok={res['ok']}, status={res['status']}")

print("\nITEM 5 CHECK COMPLETED.")
