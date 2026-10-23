"""Independent recheck of ODD_DENOMINATOR.md claims in review E0..E9.

Exact integer / Fraction arithmetic; reads the accepted Calendar only.
No canonical-reachability claim; no writes outside scratch.

Run: python -B work_landing_symbolic/reviews/scratch/check_R_odd.py
"""
import sys, json, math, random
from collections import Counter
from fractions import Fraction as F
from math import gcd
from pathlib import Path

REPO = Path(r"D:/math_cc")
sys.path.insert(0, str(REPO / "work_global_calendar"))
from calendar_oracle import Calendar  # noqa: E402

random.seed(20261023)
N0 = 20_000_000
B = 1 << (N0 // 2)
out = {}

def v2(n):
    n = abs(n)
    if n == 0:
        return 10**30
    return (n & -n).bit_length() - 1

def Pcut(n):
    return 2 * ((6 * n * n + 5 - 1).bit_length()) ** 2 + 1345

def kappa(j):
    return F(3, 2) * (j - 1) * Pcut(j - 1)

# ---------- E0: 'permitted' undefined; height bound fails for BBBAA (Phi-2=4/3) ----------
# c_t = 1/3 + (4/3)t with Q=3, C=1+4t; A=max(1/3,8/3)=8/3.
bad = []
for t in range(0, 12):
    c = F(1, 3) + F(4, 3) * t
    A = F(8, 3)
    if abs(c) > A + t:
        bad.append({"t": t, "c": str(c), "A_plus_t": str(A + t)})
out["BBBAAshift_first_violation"] = bad[0] if bad else None
out["BBBAAshift_violations_0_11"] = len(bad)

# ---------- E1/E5: random a-step identity and height recurrence ----------
a_ok = a_tot = 0
for _ in range(4000):
    Q = random.choice([3, 5, 7, 9, 27, 81, 243, 3**20, random.randrange(3, 10**6, 2)])
    C = random.randrange(-10**6, 10**6)
    if gcd(C, Q) != 1:
        continue
    j = random.randint(5, 60)
    k = random.randint(1, 10**6)
    b = random.randint(0, 1)
    u = random.randrange(1, 10**4, 2)
    p = 1 + v2(3 * Q * k + C)
    if p > j - 2:
        continue
    D0 = (C * pow(Q, -1, 1 << (j + 1)) + b * (1 << j)) % (1 << (j + 1))
    x = (1 << j) * u
    th = x + D0
    xn = 2 * th + 6 * k - x // 2
    tn = th + 6 * k + 3
    a_tot += 1
    if v2(xn) == p and (Q * (tn - xn) - (3 * Q - C)) % (1 << (p + 1)) == 0:
        a_ok += 1
out["a_step_random"] = {"checked": a_tot, "ok": a_ok}

# permitted-step height recurrence: X=|C/Q-3/2| grows by <=1 per step
height_ok = height_tot = 0
for _ in range(3000):
    Q = random.choice([3, 5, 7, 9, 27])
    C = random.randrange(-50, 51)
    if gcd(C, Q) != 1:
        continue
    A = max(abs(F(C, Q)), abs(3 - F(C, Q)))
    c = F(C, Q)
    for t in range(1, 20):
        phi = random.choice([1, 2, 3])
        c += phi - 2
        height_tot += 1
        if abs(c) <= A + t:
            height_ok += 1
out["height_recurrence_permitted"] = {"checked": height_tot, "ok": height_ok}

# ---------- E1(ii): accepted weight grammar is odd >=3 ----------
# quoted from PROOF_ROOT_PHASE.md L22-34 and PROOF_LOW_DEFICIT.md L9-15 (read in this session)
out["weight_grammar"] = {
    "eps_eq_W_plus_1": "PROOF_ROOT_PHASE.md:22",
    "W_always_even_type_c_deficit_odd_at_least_3": "PROOF_ROOT_PHASE.md:34",
    "eps3_iff_A_eps5_iff_AA_or_BA": "PROOF_LOW_DEFICIT.md:9-15",
}

# ---------- E4/E6: parameter five and the k=1 identity ----------
cal = Calendar(512)
r4 = cal.crossing(4)
out["X4"] = {"odd": r4["odd"], "kind": r4["kind"], "time": r4["time"], "k": r4["time"] // 2}
# general a-step identity 3D' = 9+6k-D-y; at k=1 it is 15-D-y
ident = {}
for kk in (1, 2, 3, 20):
    ok_gen = ok_k1 = True
    for u in (1, 3, 5, 7):
        for D in (0, 1, -1, 5, 1234567, -(1 << 20)):
            x = 32 * u; th = x + D
            y = 2 * th + 6 * kk - x // 2
            t = th + 6 * kk + 3
            ok_gen &= (3 * (t - y) == 9 + 6 * kk - D - y)
            if kk == 1:
                ok_k1 &= (3 * (t - y) == 15 - D - y)
    ident[kk] = {"general": ok_gen, "k1_formula": ok_k1}
out["a_step_identity"] = ident

# ---------- E4/E7: gateway map, reduced denominator, output bit, composite ----------
gw = []
for Q in (3, 5, 7, 9, 27, 81, 243, 3**20):
    C = 5 * Q + 16
    if gcd(C, Q) != 1:
        continue
    H = 32
    d = C * pow(Q, -1, 1 << H) % (1 << H)
    num, den = 15 * Q - C, 3 * Q
    g = gcd(num, den)
    A, R = num // g, den // g
    ok_R = R in (Q, 3 * Q) and gcd(A, R) == 1
    m_ok = True; map_ok = True
    for u in range(1, 64, 2):
        x = 32 * u; th = x + d
        y = 2 * th + 6 - x // 2
        t = th + 9
        m = v2(y)
        m_ok &= 5 <= m < H
        expected = (A * pow(R, -1, 1 << (m + 1)) + (1 << m)) % (1 << (m + 1))
        map_ok &= (t - y - expected) % (1 << (m + 1)) == 0
    gw.append({"Q": Q, "R": R, "ok_R": ok_R, "m_range_ok": m_ok, "map_ok": map_ok})
out["gateway"] = gw
out["gateway_all_ok"] = all(g["ok_R"] and g["m_range_ok"] and g["map_ok"] for g in gw)

# composite c -> gateway 5-c/3 -> reflection 3-.
comp = []
for c0 in (F(5), F(0), F(1, 3)):
    c1 = 5 - c0 / 3
    c2 = 3 - c1
    comp.append({"c0": str(c0), "c1": str(c1), "c2": str(c2),
                 "single_step": str((c0 - 6) / 3), "ok": c2 == (c0 - 6) / 3})
out["composite"] = comp
orbit = [F(-3) + F(8, 3**r) for r in range(8)]
out["orbit_c0_5"] = [str(z) for z in orbit]
out["orbit_ok"] = all(z == (F(-3) + F(8, 3**r)) for r, z in enumerate(orbit))
# c_0=5 is Q=1; Q=3^r triples only for r>=1
tri = {}
for r in (0, 1, 2):
    Q = 3**r
    for C in (3, 5, 15, 16):
        if gcd(C, Q) != 1:
            continue
        num, den = 15 * Q - C, 3 * Q
        g = gcd(num, den)
        tri["Q=%d,C=%d" % (Q, C)] = den // g
out["tripling"] = tri

# ---------- E2/E4: thresholds ----------
from decimal import Decimal, getcontext
getcontext().prec = 90
log2_3 = Decimal("1.584962500721156181453738943947816508759814407692481060455752654541098227794")
r = 10**7
lr3 = Decimal(r) * log2_3
d_r = int(lr3) + 1
NQ_r = max(N0, 4 * (d_r + 2))
# kappa(j) at j~2e7 is tiny compared with B; compute log2(Q(κ+B)) boundary with high precision
j_scan = N0
kap = kappa(j_scan)
lkap = math.log2(1.5) + math.log2(j_scan - 1) + math.log2(Pcut(j_scan - 1))
lB = N0 / 2
lkb = max(lkap, lB) + math.log2(1 + 2 ** (-abs(lkap - lB)))
log2_QkB = lr3 + Decimal(lkb)
first_j = int(log2_QkB) + 1  # first integer j with j > log2(Q(κ+B)) + 2? computed below
# solve j > log2_QkB + 2
target = log2_QkB + 2
first_j = int(target) + 1
out["r1e7"] = {"d": d_r, "NQ": NQ_r, "log2QkB_plus2": str(target),
               "first_j_size": first_j, "band_lo": N0, "band_hi": first_j,
               "band_width": first_j - N0,
               "NQ_gt_N0": NQ_r > N0}
# O1 numbers (recomputed in check_R_o1.py; repeated here for one file)
rO1 = 657306078883964
len_O1 = Decimal(rO1) * log2_3
d_O1 = int(len_O1) + 1
NQ_O1 = max(N0, 4 * (d_O1 + 2))
sigma = 1051689726214394
m = sigma - 1
out["O1"] = {"d": d_O1, "NQ": NQ_O1, "m_lb": m, "m_lt_NQ": m < NQ_O1,
             "ratio": float(Decimal(NQ_O1) / Decimal(m)),
             "m_minus_d": m - d_O1,
             "sharp_size_with_B_bits": d_O1 + (N0 // 2) + 3,
             "source_j": 49, "source_ge_NQ": 49 >= NQ_O1}

# ---------- E8: finite residues when NQ=N0 ----------
expQ = N0 // 4 - 2
expC = N0 // 2 + expQ
out["E8_finite"] = {"Q_lt_2_exp": expQ, "C_lt_2_exp": expC,
                    "note": "NQ=N0 => d<=N0/4-2 => Q<2^d<=2^expQ; |C/Q|<=B => |C|<=BQ<2^expC"}
# sanity: NQ=N0 for Q=3 (d=2)
out["E8_NQ_Q3"] = max(N0, 4 * (2 + 2))

# ---------- E9: +4/3 is inside [-12,15] numerically ----------
out["E9_shift_4_3_inside_window"] = (-12 <= F(4, 3) <= 15)
out["E9_shift_4_3_is_integer"] = (F(4, 3).denominator == 1)
out["E9_cumulative_12_steps"] = str(12 * F(4, 3))

# ---------- E5: monotonicity ratio ----------
mon = {}
for j in (2, 5, 6, 7, 8, 20):
    f_j = 2 ** (j / 2) / (1.5 * (j - 1) ** 2)
    ratio = math.sqrt(2) * ((j - 1) / j) ** 2
    doc_crit = 2 * j ** 4 / (j + 1) ** 4
    rev_ratio = math.sqrt(2) * (j / (j - 1)) ** 2
    mon[j] = {"f_gt_1": f_j > 1, "ratio_gt_1": ratio > 1,
              "doc_criterion_gt_1": doc_crit > 1, "reviewer_ratio_gt_1": rev_ratio > 1}
out["monotonicity"] = mon
out["doc_criterion_min_j"] = next(j for j in range(2, 100) if 2 * j ** 4 / (j + 1) ** 4 > 1)
out["ratio_min_j"] = next(j for j in range(2, 100) if math.sqrt(2) * ((j - 1) / j) ** 2 > 1)
out["reviewer_ratio_min_j"] = next(j for j in range(2, 100) if math.sqrt(2) * (j / (j - 1)) ** 2 > 1)

p = Path(__file__).with_name("check_R_odd.json")
p.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
print(json.dumps(out, indent=1, default=str))
print("json:", p)
