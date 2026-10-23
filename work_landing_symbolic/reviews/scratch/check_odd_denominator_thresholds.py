"""Scratch 2: threshold/band arithmetic for ODD_DENOMINATOR section 2, plus
independent gateway checks. Exact integers. Synthetic states only.
"""
import json
import random
from fractions import Fraction as F
from math import gcd
from pathlib import Path

random.seed(7)
N0 = 20_000_000
B = 1 << (N0 // 2)
out = {}

def dq(Q):
    return (Q - 1).bit_length()  # ceil(log2 Q) for Q>1

def Pc(n):
    return 2 * ((6 * n * n + 4).bit_length()) ** 2 + 1345

def kap(j):
    return 3 * (j - 1) * Pc(j - 1) // 2

def size_holds(Q, j):
    return Q * (kap(j) + B) < (1 << (j - 2))

rows = []
for r in (1, 10, 1000, 5_000_000, 10_000_000):
    Q = 3 ** r
    d = dq(Q)
    NQ = max(N0, 4 * (d + 2))
    # analytic boundary: d + j/2 + 1 < j - 2  <=>  j > 2d+6
    nat = 2 * d + 7
    # probe a few j only (big-int cost)
    probes = sorted({N0, max(N0, nat - 2), max(N0, nat), NQ})
    tab = {j: size_holds(Q, j) for j in probes}
    rows.append(dict(r=r, d=d, NQ=NQ, NQ_gt_N0=NQ > N0, nat=nat,
                     genuine_gap=(nat > N0), size_at_probes={str(k): v for k, v in tab.items()}))
out['threshold_table'] = rows

# gateway: independent random check of D'=(15Q-C)/(3Q)+2^m mod 2^(m+1)
cnt = 0
den_ok = 0
for _ in range(4000):
    Q = random.choice([3, 5, 7, 9, 11, 27, 81, 243, 3 ** 6, 5 ** 4, 3 ** 9])
    C = random.randrange(-10 ** 6, 10 ** 6)
    if C == 0 or gcd(C, Q) != 1:
        continue
    H = 40
    d = C * pow(Q, -1, 1 << H) % (1 << H)
    u = random.randrange(1, 10 ** 6, 2)
    x = 32 * u
    th = x + d
    y = 2 * th + 6 - x // 2
    m = (abs(y) & -abs(y)).bit_length() - 1 if y else 999
    if not (0 <= m < H):
        continue
    num, den = 15 * Q - C, 3 * Q
    g = gcd(num, den)
    Ared, R = num // g, den // g
    assert gcd(Ared, R) == 1 and R in (Q, 3 * Q)
    den_ok += 1
    exp = (Ared * pow(R, -1, 1 << (m + 1)) + (1 << m)) % (1 << (m + 1))
    assert (th + 9 - y - exp) % (1 << (m + 1)) == 0
    cnt += 1
out['gateway_random'] = dict(checks=cnt, reduced_denominator_ok=den_ok)

# height map iteration: h -> 5 + h/3 converges to 7.5 from below/above
h = F(0)
seq = []
for _ in range(60):
    h = 5 + h / 3
    seq.append(h)
out['height_map_limit'] = str(seq[-1])
out['height_map_below_8'] = bool(seq[-1] < 8)

# finite count of rationals while N_Q == N0 (the 'infinitely many' sentence)
dmax = N0 // 4 - 2
count = 0
for Q in [1, 3, 5, 7, 9]:  # illustration only; exact count not needed
    if Q > 1 and dq(Q) <= dmax:
        count += 2 * (B * Q) + 1
out['finite_count_note'] = dict(dmax=dmax, Q_max_bits=dmax,
                                bound_on_C_abs='B*Q', finite=True)

Path(__file__).with_name('odd_denominator_scratch2.json').write_text(
    json.dumps(out, indent=2, default=str) + '\n', encoding='utf-8')
print(json.dumps(out, indent=2, default=str))
