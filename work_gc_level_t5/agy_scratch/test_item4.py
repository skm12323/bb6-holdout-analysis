import sys, json, re
from fractions import Fraction
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table
from rational_certifier import certify_family_full, certify_rational_scalar

print("=== Part 4(a): Arithmetic verification ===")
for r in range(1, 13):
    den = 3**r
    # inv of den mod 16:
    inv_den = pow(den, -1, 16)
    term_plus = (-3 + 8 * inv_den) % 16
    term_minus = (-3 - 8 * inv_den) % 16
    assert term_plus == 5, f"r={r} plus failed: {term_plus}"
    assert term_minus == 5, f"r={r} minus failed: {term_minus}"

    # Emission formula check:
    # (15 - (-3 + 8/3^r)) / 3 = 6 - 8/3^(r+1)
    delta_p = Fraction(-3) + Fraction(8, den)
    delta_m = Fraction(-3) - Fraction(8, den)
    em_p = (Fraction(15) - delta_p) / 3
    em_m = (Fraction(15) - delta_m) / 3
    assert em_p == Fraction(6) - Fraction(8, 3**(r+1))
    assert em_m == Fraction(6) + Fraction(8, 3**(r+1))

    # a-descendant check: 3 - em = next delta
    assert Fraction(3) - em_p == Fraction(-3) + Fraction(8, 3**(r+1))
    assert Fraction(3) - em_m == Fraction(-3) - Fraction(8, 3**(r+1))

print("Part 4(a) verified for all r <= 12!")

print("\n=== Part 4(c): Check JSON orbit_free_entries ===")
with open("work_gc_level_t5/levels_t5_20000000.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

orbit_entries = json_data.get("orbit_free_entries", {})
for r in range(1, 10):
    key = f"5,3^{r+1}"
    assert key in orbit_entries, f"Missing key {key}"
    entries = orbit_entries[key]
    assert len(entries) == 2, f"Expected 2 entries for {key}, got {len(entries)}"
    
    d_p = Fraction(-3) + Fraction(8, 3**r)
    d_m = Fraction(-3) - Fraction(8, 3**r)
    # Expected emission: 6 -/+ 8/3^(r+1), so numerator over 3^(r+1) is 6*3^(r+1) -/+ 8
    em_num_p = 6 * (3**(r+1)) - 8
    em_num_m = 6 * (3**(r+1)) + 8

    # string representations in json: "('-1/3', 46)"
    expected_strs = {
        f"('{d_p.numerator}/{d_p.denominator}', {em_num_p})",
        f"('{d_m.numerator}/{d_m.denominator}', {em_num_m})"
    }
    actual_strs = set(entries)
    assert actual_strs == expected_strs, f"Mismatch for {key}: actual {actual_strs} vs expected {expected_strs}"
    print(f"  {key}: {entries} matches closed form exactly!")

print("Part 4(c) verified: orbit_free_entries matches closed forms perfectly!")

print("\n=== Part 4(b): Certify no-lift vs emission families for r=1..9 ===")
T = Table()
for r in range(1, 10):
    for sign, s_name in [(-1, "minus"), (1, "plus")]:
        val_delta = Fraction(-3) + sign * Fraction(8, 3**r)
        num_d = val_delta.numerator
        den_d = val_delta.denominator

        # 1. no-lift family (-3 +/- 8/3^r): uncert ONLY at chain 5
        res_d = certify_family_full(T, num_d, den_d, lift=False, jhi=300003)
        assert len(res_d['unc_b']) == 0, f"r={r} {s_name} has unc_b: {res_d['unc_b']}"
        assert len(res_d['unc_s']) == 1, f"r={r} {s_name} has unc_s != 1: {res_d['unc_s']}"
        assert res_d['unc_s'][0][0] == 5, f"r={r} {s_name} uncert not at chain 5"
        assert res_d['unc_s'][0][1] == 'ceiling', f"r={r} {s_name} not ceiling"

        # 2. emission family (6 -/+ 8/3^(r+1), lift=True): fully certified
        val_em = Fraction(6) - sign * Fraction(8, 3**(r+1))
        num_e = val_em.numerator
        den_e = val_em.denominator
        res_e = certify_family_full(T, num_e, den_e, lift=True, jhi=300003)
        assert len(res_e['unc_b']) == 0, f"r={r} em {s_name} has unc_b: {res_e['unc_b']}"
        assert len(res_e['unc_s']) == 0, f"r={r} em {s_name} has unc_s: {res_e['unc_s']}"

        print(f"r={r} ({s_name}): delta uncert at [5] only; emission with lift fully certified!")

print("\nALL ITEM 4 CHECKS PASSED SUCCESSFULLY!")
