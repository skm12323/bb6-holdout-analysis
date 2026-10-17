"""check_family.py -- [B] exact-integer checks of the family-calculus identities (REPORT.md section 3).
Pure algebra: random integers, no F data.  Lemma F1 (a,b,c outputs of a large chain), Lemma F2 (a-step on
Psi(j;P,Q), including ties), Lemma F3 (b/c step).  Prints counts; asserts every identity."""
import random
from fractions import Fraction as Fr
random.seed(20261017)
def v2(x): return (x & -x).bit_length() - 1
B = 600
MODB = 1 << B
def res(x, M=B):
    x = Fr(x); return (x.numerator * pow(x.denominator, -1, 1 << M)) % (1 << M)
def rnd_rat(hmax=200, dens=(1, 3, 9, 27, 5, 11)):
    return Fr(random.randint(-hmax, hmax), random.choice(dens))
cnt = dict(F2_nt=0, F2_tie=0, F2_jm1=0, F1a=0, F1b=0, F1c=0, F3=0)
# ---- Lemma F2 -------------------------------------------------------------------------
for it in range(60000):
    j = random.randint(5, 80)
    Q = random.choice([Fr(1), Fr(2, 3), Fr(4, 5), Fr(8, 11), rnd_rat(50, (1, 3, 5, 7))])
    k = random.randint(1, 10**6)
    mode = random.random()
    if mode < 0.4:            # force a tie: v2(P+3k) = j-2
        P = Fr(-3 * k + (2**(j - 2)) * random.choice([1, 3, 5, -1, -7]), 1) + Fr(2**j * random.randint(-9, 9), random.choice([1, 3, 9]))
    elif mode < 0.5:          # force v2(P+3k) >= j-1
        P = Fr(-3 * k + (2**(j - 1)) * random.randint(-5, 5), 1)
    else:
        P = rnd_rat()
    lam = 2 * random.randint(-10**30, 10**30) + 1
    Th = (res(P) + res(Q) * (lam << j)) % MODB          # an integer chain in Psi(j;P,Q) to precision B
    x = 2 * (Th + 3 * k) - (lam << (j - 1))
    jn = v2(x); lamn = x >> jn; Thn = Th + 3 + 6 * k
    E = P + 3 * k; nu = v2(res(E)) if res(E) else 10**9
    Pn = P + 3 + 6 * k - 4 * Q * E / (4 * Q - 1); Qn = 2 * Q / (4 * Q - 1)
    if nu != j - 2:
        assert jn == min(nu + 1, j - 1), (j, P, Q, k)
        cnt['F2_nt' if nu + 1 < j - 1 else 'F2_jm1'] += 1
    else:
        assert jn >= j; cnt['F2_tie'] += 1
        e = jn - j + 1
        assert e == v2(res(E / 2**(j - 2) + (4 * Q - 1) * lam))
    prec = B - jn - 2
    assert (Thn - res(Pn) - res(Qn) * (lamn << jn)) % (1 << prec) == 0, ('F2', j, P, Q, k)
    assert (res(Pn) - res(3 - P)) % (1 << min(jn, j - 1)) == 0       # P' == 3-P mod 2^min(j',j-1)
# ---- Lemma F1 (large chain, Theta_L == P mod 2^jL, arbitrary otherwise) ----------------
for it in range(20000):
    jL = random.randint(60, 300); P = rnd_rat()
    Th = (res(P, jL) + (random.randint(0, 2**200) << jL))
    lam = 2 * random.randint(0, 2**250) + 1
    # (a) a-step with NT
    k = random.randint(1, jL * jL // 2)
    x = 2 * (Th + 3 * k) - (lam << (jL - 1)); jn = v2(x)
    if jn < jL - 1:
        lamn = x >> jn; Thn = Th + 3 + 6 * k
        assert (Thn - (lamn << jn) - res(3 - P)) % (1 << (jL - 1)) == 0; cnt['F1a'] += 1
    # (b) b-step: copy of a W-fire at pointer n-1 = jL-2 with parameter jp: 3tau+4 = 2^jp * odd
    jp = random.randint(5, 40)
    while True:
        tau = random.randint(1, 2**60)
        if (3 * tau + 4) % (1 << jp) == 0 and ((3 * tau + 4) >> jp) & 1: break
        tau = ((-4 * pow(3, -1, 1 << (jp + 1))) % (1 << (jp + 1)))
        if ((3 * tau + 4) >> jp) & 1 == 0: tau += 1 << jp
        tau += (random.randint(0, 2**40) << (jp + 1))
        if (3 * tau + 4) % (1 << jp) == 0 and ((3 * tau + 4) >> jp) & 1: break
    luW = (3 * tau + 4) >> jp
    cuW = (2 * random.randint(0, 2**80) + 1) << (jL - 2 - jp)
    Thn = Th + 3 * tau + 3; lamn = luW + cuW * lam
    assert (Thn - (lamn << jp) - res(P - 1)) % (1 << (jL - 2)) == 0; cnt['F1b'] += 1
    # (c) c-step copying a chain y in Psi(jy;Py,Qy) with c_uy of valuation v
    jy = random.randint(5, 40); Py = rnd_rat(); Qy = random.choice([Fr(1), Fr(2, 3)])
    luy = 2 * random.randint(0, 2**100) + 1
    py = 400
    Thy = (res(Py, py) + res(Qy, py) * (luy << jy)) % (1 << py)
    vv = random.randint(1, 300); cuy = (2 * random.randint(0, 2**50) + 1) << vv
    Thn = Th + Thy - 2; lamn = luy + cuy * lam
    pr = min(jL, py, jy + vv)
    assert (Thn - res(Qy, pr) * (lamn << jy) - res(P + Py - 2, pr)) % (1 << pr) == 0; cnt['F1c'] += 1
# ---- Lemma F3 (b/c step from Psi(j;P,Q) with real-type data) -------------------------------
for it in range(20000):
    j = random.randint(8, 60); P = rnd_rat(); Q = random.choice([Fr(1), Fr(2, 3), Fr(4, 5)])
    lam = 2 * random.randint(0, 2**100) + 1
    Th = (res(P) + res(Q) * (lam << j)) % MODB
    tau = random.randint(1, 10**9); jw = random.randint(1, j - 3); eps = random.randint(1, j - 2 - jw)
    vv = j - 1 - eps - jw                     # v = sigma_W - j_W with sigma_W = n - eps
    luW = 2 * random.randint(0, 2**60) + 1; omega = 2 * random.randint(0, 2**60) + 1
    cuW = omega << vv
    Thn = Th + 3 * tau + 3; lamn = luW + cuW * lam
    Qn = Q * Fr(2**(j - jw)) / cuW; Pn = P + 3 * tau + 3 - Q * 2**j * Fr(luW) / cuW
    assert Qn.denominator % 2 == 1 and Pn.denominator % 2 == 1
    assert (Thn - res(Pn) - res(Qn) * (lamn << jw)) % (1 << (B - 8)) == 0
    assert v2(res(Qn)) >= v2(res(Q)) + 1 + eps; cnt['F3'] += 1
print('check_family: all identities hold;', cnt)
