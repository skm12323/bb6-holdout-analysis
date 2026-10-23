"""Scratch: independent checks for work_c3_drift/ODD_DENOMINATOR.md.

Checks (all exact integer / Fraction arithmetic):
 A. S1(a): a-step successor identity (j'=1+v2(3Qk+C), C'=3Q-C, b'=0) including
    the lift bit and the class mod 2^(j'+1), on random rational-mode states.
 B. S1(b/c): C'=C+Q(Phi-2), b'=0, codimension check on random states.
 C. S1 height recurrence |C_t|/Q <= A+t  for permitted steps (|Phi-2|<=1).
 D. S3 gateway: reduced denominator in {Q,3Q}; map c -> 5-c/3; gate+a -> (c-6)/3;
    height map h -> 5+h/3 and its fixed point.
 E. S2 threshold: Q(kappa+B) < 2^(j-2) at j=N_Q and at j=N_Q-1; find where the
    size hypothesis fails for Q=3^r (j <= 2d+4).
 F. c-orbit c_0=5 -> c_r=-3+8/3^r.
 G. monotonicity 1.5(j-1)^2 < 2^(j/2).

No canonical-reachability claim is made; states are synthetic.
"""
import json
import random
from fractions import Fraction as F
from math import gcd, log2
from pathlib import Path

random.seed(20261023)
N0 = 20_000_000
B = 1 << (N0 // 2)
out = {}

def v2(n):
    n = abs(n)
    assert n
    return (n & -n).bit_length() - 1

def P_clock(n):
    # 2*ceil(log2(6n^2+5))^2 + 1345 ; ceil(log2 m) = (m-1).bit_length()
    return 2 * ((6 * n * n + 5 - 1).bit_length()) ** 2 + 1345

def kappa(j):
    return 3 * (j - 1) * P_clock(j - 1) // 2

def ceil_log2(q):
    return (q - 1).bit_length()

# ---------- A. a-step identity on random synthetic rational states ----------
def a_step_check(trials=4000):
    cnt = 0
    for _ in range(trials):
        Q = random.choice([3, 5, 7, 9, 27, 81, 243, 3 ** 5, 3 ** 7, 5 ** 3, 11 * 13])
        C = random.randrange(1, 2000)
        if gcd(C, Q) != 1:
            continue
        j = random.randrange(5, 80)
        k = random.randrange(1, 10 ** 6)
        z = 3 * Q * k + C
        if z == 0:
            continue
        p = 1 + v2(z)
        if p > j - 2:
            continue
        b = random.randrange(2)
        # exact defect D = C/Q + b*2^j + M*2^(j+1) as an integer requires Q | (C + b*2^j Q + ...);
        # instead work with the class: the identity only needs D mod 2^{j+1}.
        d = (C * pow(Q, -1, 1 << (j + 1)) + b * (1 << j)) % (1 << (j + 1))
        x = 1 << j          # u = 1
        th = x + d
        y = 2 * th + 6 * k - x // 2
        t = th + 6 * k + 3
        assert v2(y) == p, (Q, C, j, k, p, v2(y))
        assert (Q * (t - y) - (3 * Q - C)) % (1 << (p + 1)) == 0
        cnt += 1
    return cnt


def bc_step_check(trials=4000):
    cnt = 0
    for _ in range(trials):
        Q = random.choice([3, 5, 7, 9, 27, 81, 243, 3 ** 5])
        C = random.randrange(-2000, 2000)
        if C == 0 or gcd(C, Q) != 1:
            continue
        j = random.randrange(8, 80)
        jp = random.randrange(1, j - 2)
        eps = random.randrange(1, 6)
        # a class C/Q mod 2^{j+1}; Phi-2 = s in {-1,0,1} (permitted) or arbitrary
        s = random.choice([-1, 0, 1])
        b = random.randrange(2)
        d = (C * pow(Q, -1, 1 << (j + 1)) + b * (1 << j)) % (1 << (j + 1))
        Cp = C + Q * s
        # membership: on the class level the relation D' = D + s mod 2^{j'+1}
        # is an identity; check the numerator/denominator bookkeeping.
        assert gcd(Cp, Q) == 1
        dp = Cp * pow(Q, -1, 1 << (jp + 1)) % (1 << (jp + 1))
        assert (dp - (d + s)) % (1 << (jp + 1)) == 0
        cnt += 1
    return cnt

out['a_step_random_checks'] = a_step_check()
out['bc_step_random_checks'] = bc_step_check()

# ---------- C. height recurrence ----------
worst = F(0)
cnt = 0
for _ in range(2000):
    Q = random.choice([3, 5, 9, 27, 81])
    A = F(random.randrange(-300, 300), Q)
    c = A
    tmax = 0
    C0 = A * Q
    assert C0.denominator == 1
    Amp = max(abs(A), abs(3 - A))
    for t in range(1, 200):
        if random.random() < 0.5:
            c = 3 - c            # reflection
        else:
            c = c + random.choice([-1, 0, 1])
        assert abs(c) <= Amp + t, (A, c, t)
        worst = max(worst, abs(c) - (Amp + t))
        tmax = t
    cnt += 1
out['height_recurrence_states'] = cnt
out['height_recurrence_max_slack'] = str(worst)

# ---------- D. gateway ----------
gw = dict(denominator_choices_ok=0, gcd_fail=0, q_power_of_three_triples=0)
for _ in range(3000):
    Q = random.choice([3, 5, 7, 9, 11, 27, 81, 243, 3 ** 6, 5 ** 4])
    C = random.randrange(-5000, 5000)
    if C == 0 or gcd(C, Q) != 1:
        continue
    num, den = 15 * Q - C, 3 * Q
    g = gcd(num, den)
    assert g in (1, 3), (Q, C, g)
    Ared, R = num // g, den // g
    assert gcd(Ared, R) == 1
    assert R in (Q, 3 * Q)
    gw['denominator_choices_ok'] += 1
for r in range(1, 9):
    Q = 3 ** r
    for C in range(-200, 201):
        if C == 0 or gcd(C, 3) != 0:
            continue
        g = gcd(15 * Q - C, 3 * Q)
        assert g == 1, (Q, C, g)
        gw['q_power_of_three_triples'] += 1

# c -> 5 - c/3 (gateway), then reflection 3 - c -> (c-6)/3
for c in (F(5), F(-3), F(7, 2), F(-11, 4), F(100)):
    g1 = 5 - c / 3
    g2 = 3 - g1
    assert g2 == (c - 6) / 3
gw['map_ok'] = True
# height map h -> 5 + h/3, fixed point 7.5
hs = [F(10 ** 6)]
for _ in range(40):
    hs.append(5 + hs[-1] / 3)
assert hs[-1] < F(15, 2) + 1
gw['height_limit'] = str(hs[-1])
out['gateway'] = gw

# ---------- E. size threshold around N_Q ----------
def size_ok(Q, j):
    d = ceil_log2(Q)
    return Q * (kappa(j) + B) < (1 << (j - 2)), d

rows = []
for r in (1, 3, 10, 100, 10 ** 4, 10 ** 6, 3_200_000):
    Q = 3 ** r
    d = ceil_log2(Q)
    NQ = max(N0, 4 * (d + 2))
    ok_at, _ = size_ok(Q, NQ)
    ok_below, _ = size_ok(Q, NQ - 1)
    # first j (from below) where the size hypothesis fails: need d + j/2 + 1 > j-2
    # i.e. j < 2d+6 (roughly). Test j = 2*d+4 and j = 2*d+6.
    jstar = 2 * d + 4
    rows.append(dict(r=r, d=d, NQ=NQ, ok_at_NQ=bool(ok_at), ok_at_NQ_minus_1=bool(ok_below),
                     size_at_2d4=bool(size_ok(Q, jstar)[0]),
                     size_at_2d6=bool(size_ok(Q, jstar + 2)[0]),
                     band_width=NQ - max(N0, 2 * d + 4)))
out['size_threshold'] = rows

# explicit witness that the a-size bound can fail inside the band (synthetic C with |C/Q|<=B):
# take Q=3^r huge is impractical; instead take moderate Q and a small j, which is the same
# arithmetic regime d > j/2. Demonstrates the bound is not a formal consequence of |C/Q|<=B.
wit = []
for (Q, j) in [(3 ** 20, 40), (3 ** 40, 60), (3 ** 60, 80)]:
    d = ceil_log2(Q)
    k = kappa(j)  # maximal 3k
    C = Q * B  # |C/Q| = B exactly
    val_ = Q * k + C
    wit.append(dict(Q_bits=d, j=j, Qkappa_plus_QB_lt_2j2=val_ < (1 << (j - 2)),
                    excess_bits=(val_.bit_length() - (j - 2))))
out['size_failure_witnesses'] = wit

# ---------- F. c orbit ----------
cr = [F(5)]
for _ in range(12):
    cr.append((cr[-1] - 6) / 3)
ref = [F(-3) + F(8, 3 ** r) for r in range(13)]
assert cr == ref
out['c_orbit'] = [str(x) for x in cr]

# ---------- G. monotonicity ----------
def mono_check():
    # 1.5(j-1)^2 < 2^(j/2)  <=>  9(j-1)^4 < 2^(j+2)   (exact integers)
    bad = [j for j in range(5, 400) if 9 * (j - 1) ** 4 >= (1 << (j + 2))]
    # the document's ratio 2*j^4/(j+1)^4 > 1
    crit = [j for j in range(1, 100) if 2 * j ** 4 <= (j + 1) ** 4]
    return bad, crit
bad, crit = mono_check()
out['poly_vs_exp_violations'] = bad
out['ratio_criterion_first_valid_j'] = (crit[-1] + 1) if crit else 1

Path(__file__).with_name('odd_denominator_scratch.json').write_text(
    json.dumps(out, indent=2, default=str) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in out.items() if k != 'c_orbit'}, indent=2, default=str))
