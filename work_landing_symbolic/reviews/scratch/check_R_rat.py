"""Independent recheck of the RATIONAL_MODE.md claims cited in review E0..E9.

All computations are exact integers / Fractions; the walk uses the same
accepted Calendar as the document, but the counts and algebra are recomputed
from scratch.  No canonical-reachability claim, no writes outside scratch.

Run: python -B work_landing_symbolic/reviews/scratch/check_R_rat.py
"""
import sys, json, math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

REPO = Path(r"D:/math_cc")
sys.path.insert(0, str(REPO / "work_c3_drift"))
sys.path.insert(0, str(REPO / "work_global_calendar"))
from verify_shift_transport import Calendar, bounded_walk, val  # noqa: E402
from calendar_oracle import Calendar as CanonCalendar  # noqa: E402

N0 = 20_000_000
B = 1 << (N0 // 2)
out = {}

# ---------- numerator closure exactly as in verify_rational_mode.py ----------
levels = {}
allc = set()
for c0 in (10, 26):
    states = {c0}
    levels[c0] = []
    for t in range(5):
        levels[c0].append(sorted(states))
        allc |= states
        states = {z for c in states for z in (9 - c, c - 3, c, c + 3)}
out["n_numerators"] = len(allc)
out["numerators"] = sorted(allc)
out["closure_ok_mod3"] = all(c % 3 != 0 for c in allc)

# ---------- single-lift landing scan (as the document does) ----------
cal = Calendar(256)
single = Counter()
single_fail = []
for j in range(5, 129):
    mod = 1 << (j + 1)
    for c in sorted(allc):
        d = (c * pow(3, -1, mod)) % mod
        st, rows = bounded_walk(cal, 1 << j, (1 << j) + d, j + 1, signed=True)
        single[st] += 1
        if st != "end":
            single_fail.append({"j": j, "C": c, "delta": str(d), "status": st})
out["single_lift"] = dict(single)
out["single_fail"] = single_fail
out["single_total"] = sum(single.values())

# ---------- both lifts ----------
both = {}
for lift in (0, 1):
    cnt = Counter(); fails = []
    for j in range(5, 129):
        mod = 1 << (j + 1)
        for c in sorted(allc):
            d = (c * pow(3, -1, mod)) % mod
            dd = (d + lift * (1 << j)) % mod
            st, rows = bounded_walk(cal, 1 << j, (1 << j) + dd, j + 1, signed=True)
            cnt[st] += 1
            if st != "end":
                fails.append({"j": j, "C": c, "lift": lift, "delta": str(dd),
                              "b_bit": dd >> j, "status": st, "chains": len(rows)})
    both["lift%d" % lift] = {"counts": dict(cnt), "fails": fails}
out["both_lifts"] = both
out["total_classes_C_b_j"] = len(allc) * (128 - 5 + 1) * 2
out["total_states_scanned_both"] = 2 * sum(both["lift0"]["counts"].values())

# doc's single lift is not uniformly b=0: count b bits among the scanned reps
bdist = Counter()
for j in range(5, 129):
    mod = 1 << (j + 1)
    for c in sorted(allc):
        d = (c * pow(3, -1, mod)) % mod
        bdist[d >> j] += 1
out["single_lift_b_bit_hist"] = dict(bdist)
# the two documented failures, with their b bits
doc_fail = []
for (j, c) in ((5, -17), (5, -1)):
    d = (c * pow(3, -1, 1 << (j + 1))) % (1 << (j + 1))
    doc_fail.append({"j": j, "C": c, "delta": str(d), "b_bit": d >> j,
                     "is_a_image_of_gateway": c in (9 - 10, 9 - 26)})
out["doc_failures"] = doc_fail

# accepted bare ties (5,5), (5,-11) correspond to the other lift
other = []
for f in both["lift1"]["fails"]:
    other.append({"j": f["j"], "C": f["C"], "delta": f["delta"],
                  "delta_mod_2j": int(f["delta"]) % (1 << f["j"])})
out["other_lift_failures"] = other

# ---------- gateway classes (10-2^j)/3, (26-2^j)/3 (b=1) ----------
gw = {}
for C in (10, 26):
    cnt = Counter(); fails = []
    for j in range(5, 129):
        mod = 1 << (j + 1)
        delta = ((C - (1 << j)) * pow(3, -1, mod)) % mod
        st, rows = bounded_walk(cal, 1 << j, (1 << j) + delta, j + 1, signed=True)
        cnt[st] += 1
        if st != "end":
            fails.append({"j": j, "delta": str(delta), "status": st})
    gw[str(C)] = {"counts": dict(cnt), "fails": fails}
out["gateway_classes"] = gw

# ---------- exact a-step count 2360 and skipped pairs ----------
checks = 0; skipped = []
for j in range(5, 129):
    r = cal.crossing(j - 1)
    for c in sorted(allc):
        if not r["odd"] or r["kind"] != "a":
            continue
        k = r["time"] // 2
        z = 9 * k + c
        assert z != 0
        q = 1 + val(z)
        if q > j - 2:
            skipped.append({"j": j, "C": c, "q": q})
            continue
        for lift in (0, 1):
            checks += 1
out["a_step_checks"] = checks
out["a_step_skipped_pairs"] = skipped
out["a_step_skipped_lift_checks"] = 2 * len(skipped)

# ---------- exact resonance counterexample to L47 ----------
# j=5, the calendar X(4) is odd a with k=1.  Take theta=-3 (symmetric),
# D=-3, C = 3D mod 2^(j+1) = 55, b=0.  Then C mod 3 = 1, 9k+C=64 != 0,
# but z=3k+theta=0 exactly.
j_res, k_res, D_res = 5, 1, -3
C_res = (3 * D_res) % (1 << (j_res + 1))
b_res = 0
z_res = 3 * k_res + D_res
res = {
    "j": j_res, "k": k_res, "theta": D_res, "C": C_res, "b": b_res,
    "nine_k_plus_C": 9 * k_res + C_res,
    "C_mod_3": C_res % 3,
    "class_identity_3D_eq_C": (3 * D_res - (C_res + 3 * b_res * (1 << j_res))) % (1 << (j_res + 1)) == 0,
    "resonance_z_zero": z_res == 0,
    "nine_k_plus_C_nonzero": 9 * k_res + C_res != 0,
}
# exact a-step from the representative state
x = 1 << j_res
th = x + D_res
xn = 2 * th + 6 * k_res - x // 2
tn = th + 6 * k_res + 3
res["x_prime"] = str(xn); res["theta_prime"] = str(tn); res["D_prime"] = str(tn - xn)
res["j_prime"] = val(xn)
res["RA_would_predict"] = 1 + val(9 * k_res + C_res)
r4 = CanonCalendar(64).crossing(4)
res["X4_is_odd_a_k1"] = (r4["odd"], r4["kind"], r4["time"] // 2)
out["resonance_counterexample"] = res

# ---------- SIZE3 constants ----------
def Pcut(n):
    return 2 * ((6 * n * n + 5 - 1).bit_length()) ** 2 + 1345
kappaN0 = F(3, 2) * (N0 - 1) * Pcut(N0 - 1)
three_kB = 3 * (kappaN0 + B)
out["P_N0m1"] = Pcut(N0 - 1)
out["kappa_N0"] = str(kappaN0)
out["three_kappa_B_lt_2_j_minus_2"] = three_kB < (1 << (N0 - 2))
out["bitlen_floor_three_kB"] = three_kB.numerator.bit_length() - three_kB.denominator.bit_length()
out["SIZE3_rhs_exponent"] = N0 - 2

# ---------- L3 at N0 and the tower bound ----------
def floor_log2_frac(x):
    e = x.numerator.bit_length() - x.denominator.bit_length()
    while F(1 << e) > x:
        e -= 1
    while F(1 << (e + 1)) <= x:
        e += 1
    return e
def L3(j):
    kap = F(3, 2) * (j - 1) * Pcut(j - 1)
    t1 = 1 + floor_log2_frac(3 * (kap + B))
    t2 = floor_log2_frac(6 * (j - 1) * Pcut(j - 1) + 5)
    return max(t1, t2), t1, t2
L_N0 = L3(N0)
out["L3_N0"] = {"L3": L_N0[0], "term1": L_N0[1], "term2": L_N0[2]}
out["L3_N0_lt_N0"] = L_N0[0] < N0
out["L3_N0_gt_128"] = L_N0[0] > 128
out["L3_N0_le_tower_bound"] = L_N0[0] <= max(2 * math.log2(N0) + 5, N0 // 2 + 4)
out["h3_N0"] = 1 if L_N0[0] < N0 else None
out["height_condition_at_N0"] = F(10 + 3, 3) <= B
# lower bound L3(j) >= 1+floor(log2(3B)) for all j>=N0
out["L3_lower_bound"] = 1 + floor_log2_frac(3 * B)
# L3 nondecreasing (sample + argument); P is nondecreasing
Pvals = [Pcut(n) for n in range(N0 - 1, N0 + 20000)]
out["P_nondecreasing_sample"] = all(Pvals[i] <= Pvals[i + 1] for i in range(len(Pvals) - 1))
# U-tower: U1 and U4 vs K_clock (K_clock is a height-4 tower with top 499997)
out["U1_exponent"] = F(N0 - 5, 2)
# numeric comparison is symbolic: U3 is a height-3 tower, K_clock is 2^{K'} (height 4),
# so U3 < K_clock; U4 is a height-4 tower with top 10^7 > 499997, so U4 > K_clock.
out["tower_note"] = "U1=2^{(N0-5)/2}; U3 height 3, K_clock=2^{K'} height 4 -> U3<K_clock; U4 height 4 with top 1e7>499997 -> U4>K_clock"

p = Path(__file__).with_name("check_R_rat.json")
p.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k not in ("numerators", "single_fail")}, indent=1, default=str))
print("json:", p)
