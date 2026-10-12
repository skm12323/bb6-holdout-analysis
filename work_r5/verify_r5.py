"""verify_r5.py -- checks for work_r5/PROOF.md.  Usage: python verify_r5.py [S=300] [V=600]"""
import sys
S = int(sys.argv[1]) if len(sys.argv) > 1 else 300
V = int(sys.argv[2]) if len(sys.argv) > 2 else 600
NS = 8   # symbols: 0:u (o=2u+1), 1:k (K=2^p k), 2..7: z_i (Z_i=2^p z_i); all symbols range over integers >= 0
class Undecided(Exception): pass
def C(c, *co): co = list(co) + [0] * (NS - len(co)); return (tuple(co), c)
def add(*xs): return (tuple(sum(x[0][i] for x in xs) for i in range(NS)), sum(x[1] for x in xs))
def sc(x, k): return (tuple(k * a for a in x[0]), k * x[1])
def par(x):
    if any(a % 2 for a in x[0]): raise Undecided('parity')
    return x[1] % 2
def half(x):
    if any(a % 2 for a in x[0]) or x[1] % 2: raise Undecided('half')
    return (tuple(a // 2 for a in x[0]), x[1] // 2)
def ge3(x):   # decide x>=3 for ALL symbol values >=0
    if all(a >= 0 for a in x[0]) and x[1] >= 3: return True
    if all(a == 0 for a in x[0]): return False
    raise Undecided('compare')
Z0 = C(0)
def T(L):     # top map of R1 RULES.md, executed uniformly in the symbols
    A = L[0]; b = L[1] if len(L) > 1 else Z0; c = L[2] if len(L) > 2 else Z0; R = L[3:]
    if par(A) == 0: return [add(A, b, c, C(3))] + R
    m = half(add(b, b, A, C(-3))); st = [half(add(c, c, A, C(1)))] + R
    while par(m) == 1 and ge3(m):
        st = [half(add(m, C(3)))] + st; m = half(add(m, C(-3)))
    if par(m) == 1: raise Exception('HALT branch reachable')
    return [add(m, C(4))] + st

# ---- check 1 [Class-A per s]: Lemma F(s) ----
NZ = 5
def F(s, p):
    o = C(1, 2); K = C(0, 0, 2 ** p)
    Zs = [C(0, *([0, 0] + [0] * i + [2 ** p])) for i in range(NZ)]
    L = [add(o, C(1))] + [sc(o, 1 << i) for i in range(s - 1)] + [add(sc(o, 1 << (s - 1)), C(-1), K)] + Zs
    t = 0
    while not any(L[1:] == Zs[a:] for a in range(NZ + 1)):
        L = T(L); t += 1
        for x in L: assert all(a >= 0 for a in x[0]) and x[1] >= 0
    a = NZ - (len(L) - 1)
    assert a < NZ - 1                                   # Z_{a+1} was never read (still in place, untouched)
    assert L[0] == add(sc(o, 1 << s), C(3 * t), K, *Zs[:a])
    return t, a
ell, aa, pp = {}, {}, {}
for s in range(1, S + 1):
    for p in range(0, 40):
        try: ell[s], aa[s] = F(s, p); pp[s] = p; break
        except Undecided: pass
    else: raise SystemExit('F(%d) undecided for p<40' % s)
print('check1 OK: Lemma F(s) holds for s=1..%d; max a(s)=%d; margin p(s) max=%d' % (S, max(aa.values()), max(pp.values())))
print('  p(s)>0 at:', {s: pp[s] for s in pp if pp[s] > 0 and s <= 120})
print('  ell(1..30)=', [ell[s] for s in range(1, 31)])
print('  a(1..30)  =', [aa[s] for s in range(1, 31)])

# ---- check 2 [Class-A per v, cross-check]: K=0, no Z  ==  R4 excursion lemma, same ell ----
def E1(v):  # R4's form, w=2u+1 -> 3w = 6u+3
    x = C(3, 6); L = [add(x, C(1))] + [sc(x, 1 << i) for i in range(v - 1)] + [add(sc(x, 1 << (v - 1)), C(-1))]; t = 0
    while len(L) > 1: L = T(L); t += 1
    assert L[0] == add(sc(x, 1 << v), C(3 * t)); return t
for v in range(1, min(S, 300) + 1): assert E1(v) == ell[v], v
print('check2 OK: R4 ell(v) == ell_F(v) for v<=%d' % min(S, 300))

# ---- check 3 [Class-B]: canonical macro-steps inside E(v), v<=V ----
v2 = lambda x: (x & -x).bit_length() - 1
cnt = 0
for v in range(1, V + 1):
    x = C(3, 6); L = [add(x, C(1))] + [sc(x, 1 << i) for i in range(v - 1)] + [add(sc(x, 1 << (v - 1)), C(-1))]
    t = 0; can = []
    while len(L) > 1:
        if len(L) > 3 and L[0][0] == L[1][0] and L[2] == sc(L[1], 2) and L[1][0][0] == 2 * L[1][1]:
            j = (L[1][1] // 3).bit_length() - 1; d = L[0][1] - L[1][1]
            assert d == 3 * t + 1 and L[1][1] == 3 << j; can.append((t, j, len(L)))
        L = T(L); t += 1
    for (t0, j0, n0), (t1, j1, n1) in zip(can, can[1:]):
        if t0 == 0: continue
        d = 3 * t0 + 1
        if d % 2 == 0: assert (t1 - t0, j1 - j0) == (1, 2)
        else:
            s = v2(d + 3); assert (t1 - t0, j1 - j0) == (ell[s] + 1, 2 + aa[s]), (v, t0, s)
        assert n0 - n1 == j1 - j0; cnt += 1
print('check3 OK: %d canonical transitions in E(v), v<=%d, all = R-even or M(s) with (dt,dj)=(ell(s)+1, 2+a(s))' % (cnt, V))

# ---- check 4 [Class-A per s]: F'(s): as F(s) but Z_1 = 2^p z_1 + (2^p - 1)  (i.e. Z_1 == -1 mod 2^p, odd if p>=1)
def Fp(s, p):
    o = C(1, 2); K = C(0, 0, 2 ** p)
    Zs = [C(0, *([0, 0] + [0] * i + [2 ** p])) for i in range(NZ)]; Zs[0] = add(Zs[0], C((1 << p) - 1))
    L = [add(o, C(1))] + [sc(o, 1 << i) for i in range(s - 1)] + [add(sc(o, 1 << (s - 1)), C(-1), K)] + Zs; t = 0
    while not any(L[1:] == Zs[a:] for a in range(NZ + 1)): L = T(L); t += 1
    a = NZ - (len(L) - 1); assert a < NZ - 1 and L[0] == add(sc(o, 1 << s), C(3 * t), K, *Zs[:a]); return t, a
pq = {}
for s in range(1, S + 1):
    for p in range(0, 40):
        try: pq[s] = (p,) + Fp(s, p); break
        except Undecided: pass
    else: raise SystemExit("F'(%d) undecided" % s)
diff = [s for s in pq if pq[s][1:] != (ell[s], aa[s])]
print("check4 OK: F'(s) (Z_1 == -1 mod 2^p) holds (no halt, uniform) for s<=%d; max margin %d; (ell,a) differ from F at %d values, e.g. %s" % (S, max(x[0] for x in pq.values()), len(diff), [(s, pq[s][1:], (ell[s], aa[s])) for s in diff[:4]]))
