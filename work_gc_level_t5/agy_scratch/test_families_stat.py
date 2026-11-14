import json
from fractions import Fraction

with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fstatus = data["family_status"]
print(f"Total families: {len(fstatus)}")

uncert_fams = []
clean_fams = []

for k, st in fstatus.items():
    unc_s = st.get("unc_s", [])
    unc_b = st.get("unc_b", [])
    if unc_s or unc_b:
        uncert_fams.append((k, unc_s, unc_b))
    else:
        clean_fams.append(k)

print(f"Number of families with uncert: {len(uncert_fams)}")
print(f"Number of clean families: {len(clean_fams)}")

# Let's check what the uncertified families are:
# NOTES claims: exactly 18 families, which are (-3 +/- 8/3^r) for r=1..9, all no-lift (lift=0), and all uncert ONLY at chain 5 with ceiling!
orbit_no_lift = set()
for r in range(1, 10):
    for sign in [-1, 1]:
        val = Fraction(-3) + sign * Fraction(8, 3**r)
        key = f"{val.numerator}/{val.denominator}/0"
        orbit_no_lift.add(key)

print(f"\nExpected 18 orbit no-lift keys: {len(orbit_no_lift)}")

actual_uncert_keys = set(k for k, _, _ in uncert_fams)
assert actual_uncert_keys == orbit_no_lift, f"Mismatch in uncertified families!\nDiff: {actual_uncert_keys ^ orbit_no_lift}"
print("EXACT MATCH: The 18 uncertified families are EXACTLY the no-lift orbit families (-3 +/- 8/3^r) for r=1..9!")

for k, unc_s, unc_b in uncert_fams:
    assert len(unc_b) == 0, f"{k} has unc_b: {unc_b}"
    assert len(unc_s) == 1, f"{k} has unc_s != 1: {unc_s}"
    chain, status, word = unc_s[0]
    assert chain == 5, f"{k} uncert not at chain 5: {chain}"
    assert status == "ceiling", f"{k} status not ceiling: {status}"

print("EXACT MATCH: All 18 families fail ONLY at chain 5 and ONLY with ceiling!")
