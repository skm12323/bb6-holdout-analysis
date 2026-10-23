"""Independent recheck of the O1 numbers used in review E4 (ODD_DENOMINATOR).

Reads only work_global_calendar/calendar_oracle.py. No claims of reachability,
no writes outside this scratch directory.

Run: python -B work_landing_symbolic/reviews/scratch/check_R_o1.py
"""
import sys, json, math
from decimal import Decimal, getcontext
from pathlib import Path

REPO = Path(r"D:/math_cc")
sys.path.insert(0, str(REPO / "work_global_calendar"))
from calendar_oracle import Calendar

getcontext().prec = 90
N0 = 20_000_000
BLOG = N0 // 2
k_fire = 469124961184426
sigma_claim = 1051689726214394
r_O1 = 657306078883964
log2_3 = Decimal("1.584962500721156181453738943947816508759814407692481060455752654541098227794")

out = {}

# --- canonical source, checked against Calendar(512) ---
cal = Calendar(512)
c48 = cal.crossing(48)
out["X48"] = {k: c48[k] for k in ("kind", "time", "epsilon", "odd", "omega")}
fire = cal.preceding_fire_by_time(2 * k_fire)
out["fire"] = {k: str(fire[k]) for k in ("k", "pointer", "J", "index", "jumps")}
out["fire_matches_claim"] = (fire["k"] == k_fire and fire["pointer"] == sigma_claim)
x0 = 5 * (1 << 49)
theta0 = x0 + 1
k = c48["time"] // 2
y = 2 * theta0 + 6 * k - x0 // 2
A = (y - 10) // 16
out["x0_eq_5_2_49"] = (x0 == 5 * (1 << 49))
out["theta0"] = str(theta0)
out["k_at_X48"] = k
out["y"] = str(y)
out["A"] = str(A)
out["A_mod8"] = A % 8
out["y_eq_16A_plus_10"] = (y == 16 * A + 10)
out["v2_y"] = (y & -y).bit_length() - 1
out["A_plus_1_lt_2_48"] = (A + 1 < (1 << 48))

# --- exact d = ceil(r log2 3) ---
x = Decimal(r_O1) * log2_3
d = int(x) + 1
out["r_log2_3"] = str(x)
out["d"] = d
out["d_float_agree"] = (d == math.ceil(r_O1 * 1.5849625007211562))
NQ = max(N0, 4 * (d + 2))
out["NQ"] = NQ
sigma = int(fire["pointer"])
m_lb = sigma - 1
out["sigma"] = sigma
out["m_lower_bound"] = m_lb
out["m_lt_NQ"] = (m_lb < NQ)
out["NQ_over_m"] = float(Decimal(NQ) / Decimal(m_lb))
out["m_minus_d_bits"] = m_lb - d

# --- where does the *size* inequality Q*(kappa+B) < 2^(j-2) actually start? ---
# At j ~ 1e15, kappa(j) = (3/2)(j-1)P(j-1) with P(n)=2*ceil(log2(6n^2+5))^2+1345.
# Compare logs, no huge integers.
def log2_kappa(j):
    n = j - 1
    g = math.ceil(math.log2(6 * n * n + 5)) if n < 10**15 else 2 * math.log2(n) + 1
    # exact ceil via bit_length for the sizes we actually use is impossible for
    # n~1e15 only because 6n^2 is still small (6e30) -> fine
    g = (6 * n * n + 5 - 1).bit_length()
    P = 2 * g * g + 1345
    return math.log2(1.5) + math.log2(n) + math.log2(P)
log2Q = float(x)  # log2(3^r)
out["log2Q"] = log2Q
# with B
out["log2QkB_with_B"] = log2Q + max(math.log2(3 * (2**BLOG)) if False else BLOG + math.log2(3),
                                    math.log2(3 * (2 ** log2_kappa(m_lb)))) if False else None
# compute: log2(Q*(kappa+B)) = log2Q + log2(kappa+B)
lk = log2_kappa(m_lb)
lB = BLOG
lkB = max(lk, lB) + math.log2(1 + 2 ** (-abs(lk - lB)))
out["log2_kappa_at_m"] = lk
out["log2_QkB_with_B"] = log2Q + lkB
out["size_B_first_j_approx"] = out["log2_QkB_with_B"] + 2
# with h = 5
lkh = math.log2(2 ** lk + 5)
out["log2_Qkh_with_h5"] = log2Q + lkh
out["size_h_first_j_approx"] = out["log2_Qkh_with_h5"] + 2
out["m_above_sharp_B_threshold"] = (m_lb > out["size_B_first_j_approx"])

# --- c_r orbit check: c_r = -3+8/3^r, eta_r = c_r-2 = -5+8/3^r ---
from fractions import Fraction as F
for rr in range(0, 4):
    c = F(-3) + F(8, 3**rr)
    eta = c - 2
    out["c_%d" % rr] = str(c)
    out["eta_%d" % rr] = str(eta)
out["eta_formula_ok"] = all(F(-5) + F(8, 3**rr) == (F(-3) + F(8, 3**rr)) - 2 for rr in range(6))

p = Path(__file__).with_name("check_R_o1.json")
p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if not k.startswith(("c_", "eta_"))}, indent=1))
print("json:", p)
