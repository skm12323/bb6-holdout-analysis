"""Scratch 3: quantitative comparison of the ODD_DENOMINATOR threshold N_Q with
the O1 obstruction (ORBIT_SHIFT_OBSTRUCTION) and the exact size threshold.

Exact integers; Q=3^r for moderate r (10^7) and arithmetic-only for the huge r
of the obstruction (no 3^r materialisation there: only bit lengths compared).
"""
import json
from pathlib import Path

N0 = 20_000_000
B = 1 << (N0 // 2)
out = {}

# --- obstruction data (ORBIT_SHIFT_OBSTRUCTION.md section 4) ---
sigma = 1051689726214394
r_obj = 657306078883964
import math
log2_3 = math.log2(3)
d_obj = math.ceil(r_obj * log2_3)          # cannot compute 3^r; d from reals is fine for comparison
NQ_obj = max(N0, 4 * (d_obj + 2))
# output parameter m >= sigma-1 (v2(y_r)=4+v2(A 3^r+1), v2 >= sigma-5)
m_lo = sigma - 1
natural = d_obj + N0 // 2 + 3
out['obstruction'] = dict(sigma=sigma, r=r_obj, d=d_obj, NQ=NQ_obj,
                          m_lower_bound=m_lo, natural_threshold=natural,
                          m_below_NQ=bool(m_lo < NQ_obj),
                          m_above_natural=bool(m_lo >= natural),
                          NQ_over_m=m_lo and NQ_obj / m_lo)

# --- exact size boundary for r = 10^7 ---
def Pc(n):
    return 2 * ((6 * n * n + 4).bit_length()) ** 2 + 1345

def kap(j):
    return 3 * (j - 1) * Pc(j - 1) // 2

r = 10_000_000
Q = 3 ** r
d = (Q - 1).bit_length()
NQ = max(N0, 4 * (d + 2))
Bval = B
def holds(j):
    return Q * (kap(j) + Bval) < (1 << (j - 2))
# natural threshold: smallest j >= N0 with holds(j). holds is monotone in j in this range.
lo, hi = N0, NQ + 10_000_000
assert holds(hi), 'hi too small'
while lo < hi:
    mid = (lo + hi) // 2
    if holds(mid):
        hi = mid
    else:
        lo = mid + 1
out['r1e7'] = dict(d=d, NQ=NQ, exact_first_j=lo, band_lo=N0, band_width=lo - N0,
                   holds_at_N0=holds(N0))

# --- where does N_Q exceed the exact threshold? scan moderate r via bit lengths only ---
rows = []
for rr in (3_000_000, 4_000_000, 5_000_000, 6_000_000, 7_000_000):
    dd = math.ceil(rr * log2_3)
    nq = max(N0, 4 * (dd + 2))
    nat = dd + N0 // 2 + 3
    rows.append(dict(r=rr, d=dd, NQ=nq, nat=nat, NQ_gt_nat=nq > nat,
                     gap=(nat > N0)))
out['threshold_family'] = rows

Path(__file__).with_name('odd_denominator_threshold_numbers.json').write_text(
    json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, indent=2))
