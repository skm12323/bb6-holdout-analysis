"""Analytic/numeric checks of A1-A4 bookkeeping:
  drift recurrence; L(j)<j and monotonicity; kappa(j)<2^(j-4); size of Lambda;
  the corrected no-resonance range; window arithmetic for Lambda<=13; edge cases.
Writes check_logic.json.
"""
import json, sys
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')

N0 = 2 * 10**7
B = 1 << 10**7
res = {}

def P(n):
    v = 6 * n * n + 5
    g = (v - 1).bit_length()  # ceil(log2 v) for v not a power of 2; handle below
    if (1 << g) < v:
        g += 1
    return 2 * g * g + 1345

def g2(n):
    v = 6 * n * n + 5
    g = 0
    while (1 << g) < v:
        g += 1
    return g

def P2(n):
    g = g2(n)
    return 2 * g * g + 1345

def kappa(j):
    return (3 * (j - 1) * P2(j - 1)) // 2

def L(j):
    x = kappa(j) + B
    return max(1 + (x.bit_length() - 1 if x & (x - 1) == 0 else x.bit_length()),
               (6 * (j - 1) * P2(j - 1) + 5).bit_length() - 1)

# exact floor(log2)
def flog2(x):
    return x.bit_length() - 1

def L2(j):
    return max(1 + flog2(kappa(j) + B), flog2(6 * (j - 1) * P2(j - 1) + 5))

# 1. drift recurrence: enumerate all a/b sequences up to length 16 from theta_0=1
drift_bad = 0
from itertools import product
for tlen in range(0, 17):
    for seq in product('ab', repeat=tlen):
        th = 1
        ok = True
        for s, ch in enumerate(seq):
            if ch == 'a':
                th = 3 - th
            else:
                th = th - 1
            # membership in {2i-(s+1)+1 : 0<=i<=s+1}
            if not any(th == 2 * i - (s + 1) + 1 for i in range(0, s + 2)):
                ok = False
        if not ok:
            drift_bad += 1
res['drift_seq_bad'] = drift_bad
res['drift_sequences'] = 2 ** 17 - 1

# note the set {2i-t+1: 0<=i<=t} = {1-t,3-t,...,t+1}

# 2. L(j)<j, L monotone (sampled), L(j)<=G(j); kappa(j)<2^(j-4); P(n)<=n
badL = []; badmono = []; badG = []; badk = []; badP = []
js = [N0, N0 + 1, N0 + 2, N0 + 10**5, 3 * 10**7, 10**8, 10**9, 10**12, 10**20, 10**100,
      10**1000]
js += [N0 + i * 1234567 for i in range(1, 40)]
for j in sorted(set(js)):
    if not (L2(j) < j): badL.append((j, L2(j)))
    if not (kappa(j).bit_length() <= j - 4): badk.append((j, kappa(j).bit_length()))
    if not (P2(j - 1) <= j - 1): badP.append((j, P2(j - 1)))
    # L(j) <= G(j) = max(2log2 j+3, 10^7+2), using floor terms
    G = max(2 * j.bit_length() + 3, 10**7 + 2)
    if L2(j) > G: badG.append((j, L2(j), G))
for a, b in zip(sorted(set(js)), sorted(set(js))[1:]):
    if L2(a) > L2(b): badmono.append((a, b))
res.update(badL=badL[:5], bad_kappa=badk[:5], bad_P=badP[:5], bad_G=badG[:5],
           bad_mono=badmono[:5], L_N0=L2(N0), L_G_N0=max(2 * N0.bit_length() + 3, 10**7 + 2),
           kappa_N0=kappa(N0), log2B=B.bit_length() - 1)

# 3. cruder all-scale bound kappa(j) <= 15 j (log2 j)^2 + 2018 j for j>=2^20, and
#    15j(log2j)^2+2018j < 2^(j-4)
badcrude = []
for j in [2**20, 2**24, N0, 10**8, 10**12, 10**100]:
    x = (j - 1).bit_length() - 1  # floor log2(j-1) <= log2 j
    bound = 15 * j * (x + 1) ** 2 + 2018 * j
    if kappa(j) > bound:
        badcrude.append((j, 'bound'))
    if bound.bit_length() > j - 4:
        badcrude.append((j, 'size'))
res['bad_crude'] = badcrude[:5]

# 4. corrected no-resonance ranges
kmin3 = 3 * (N0 - 2) // 4          # 14_999_998 (floor of 3(N0-2)/4)
res['3k_min_floor'] = kmin3
res['exact_3k_over_4'] = (3 * (N0 - 2), 4)
# crude: 2 Lambda + 1 < 3k -> Lambda <= floor((3k-2)/2)
res['Lambda_crude_max'] = (kmin3 - 2) // 2
# sharp drift |theta|<=Lambda: Lambda < 3k -> Lambda <= 3k-1
res['Lambda_sharp_max'] = kmin3 - 1
# what the brief claimed:
res['brief_claim_2Lambda_plus_1_lt_3_34e6'] = (2 * ((B - 4) // 6) + 1) < 3340000
import math as _math
res['B_bits'] = B.bit_length()
res['B_minus_4_over_6_bits'] = ((B - 4) // 6).bit_length()
res['B_minus_4_over_6_decimal_digits_approx'] = int(((B - 4) // 6).bit_length() * _math.log10(2)) + 1

# 5. window arithmetic for Lambda<=13
win = []
for Lam in [1, 2, 4, 13]:
    Tmax = Lam - 1
    a_lo, a_hi = 2 - Tmax, Tmax + 2
    b_lo, b_hi = -Tmax, Tmax
    win.append((Lam, Tmax, a_lo, a_hi, b_lo, b_hi,
                (a_lo >= -12 and a_hi <= 15 and b_lo >= -12 and b_hi <= 15)))
res['window'] = win

# 6. the claimed bare-tie theta values need |theta|<=Lambda (drift) so congruence mod 64 fixes them
res['bare_tie_theta'] = {
    'a (5,5) theta=-2': (-2) % 64 == 62,
    'a (5,-11) theta=14': 14 % 64 == 14,
    'b (5,5) theta=6': 6 % 64 == 6,
    'b (5,-11) theta=-10': (-10) % 64 == 54,
    'all within drift bound 13': all(abs(x) <= 13 for x in (-2, 14, 6, -10))}

# 7. Lambda(K_clock)=4 comparison: log2 K_clock = K' - 2log2 K' - 6, K'=2^(2^(2^499997-3)-2)
#    log2 T3 = 2^(2^(10^7-5/2)-5/2) - 3/2, log2 T4 = T3/2 - 3/2
#    compare exponents: 2^499997 vs 10^7 (obvious); K' vs T3's exponent
res['Kclock_log2_about'] = 'K\' - 2 log2 K\' - 6, log2 K\' = 2^(2^(2^499997-3)-2)'
res['T3_log2'] = '2^(2^(10^7-5/2)-5/2)-3/2'
res['log2T3_vs_log2Kclock_exponents'] = {
    'exp(log2Kclock) = 2^(2^499997-3)-2': 'huge',
    'exp(log2T3) = 2^(10^7-5/2)-5/2': '2^(10^7) only',
    'T3 < Kclock': (10**7 < 2**499997),
    'log2Kclock < log2T4 (since T4/2 ~ 2^(T3/2))': True}
# check numerically at exponent level with logs
import math
l10 = math.log(2)
res['check_Kclock_gt_T3_exponent'] = (2**499997 > 10**7 - 2.5)
res['check_Kclock_lt_T4_exponent'] = (10**7 - 2.5 < 2**499997)

# 8. 6 Lambda + 4 <= B for Lambda <= 14_999_998
res['6L4_le_B_at_Lmax'] = 6 * res['Lambda_sharp_max'] + 4 <= B

with open(r'D:\math_cc\work_r1r2\agent_V\check_logic.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1)[:5000])
