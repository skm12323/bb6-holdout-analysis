"""verify_r4.py -- checks for PROOF.md (R4). Usage: python verify_r4.py [V0=2000]"""
import sys
V0 = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
v2 = lambda x: (x & -x).bit_length() - 1

# ---- concrete top map (R1 RULES.md sec.5) ----
def top(L):
    A = L[0]; b = L[1] if len(L) > 1 else 0; c = L[2] if len(L) > 2 else 0; S = L[3:]
    if A % 2 == 0: return [A + b + c + 3] + S
    m = b + (A - 3) // 2; st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st; m = (m - 3) // 2
    if m == 1: return 'HALT'
    return [m + 4] + st

# ---- check 0 [Class-B]: top map == iteration of macro rules R1-R5 (R1 RULES.md sec.3) ----
def rule(h, r):
    r = r + [0, 0, 0]
    if r[0] >= 2 and r[1] >= 1: r[1] -= 1; return h + 1, r                      # R1
    if r[0] >= 2 and r[1] == 0 and (r[2] == 0):                                   # R2 (k=1)
        return h + 1, [r[0] - 2, 0, 1] + r[3:]
    if r[0] >= 2 and r[1] == 0: return h + 1, [r[0] - 2, 0, r[2] + 1] + r[3:]     # R3
    if r[0] == 1 and r[1] == 0 and h >= 1: return 0, [h - 1, 0, 1, r[2] + 1] + r[3:]  # R4
    if r[0] == 1 and r[1] == 0 and h == 0: return None, 'HALT'
    if r[0] == 0 and r[1] == 0: return 0, [h + r[2] + 3] + r[3:]                  # R5
    raise Exception('uncovered %r' % ((h, r),))
def strip(r):
    while r and r[-1] == 0: r = r[:-1]
    return r
h, r, L = 0, [3], [3]
for n in range(3000):
    L = top(L)
    while True:
        h, r = rule(h, r); r = strip(r)
        if h == 0 and (len(r) == 1 or r[1] >= 1): break
    assert r == L, (n, r, L)
print('check0 OK: top map == R1..R5 iteration for 3000 top steps')

# ---- check 1 [Class-A, symbolic]: excursion lemma for v=1..V0, all odd w ----
# entries are affine a*u+b in u>=0 with w=2u+1; every branch must be u-independent.
class Undecided(Exception): pass
def par(x):
    if x[0] % 2: raise Undecided('parity depends on u')
    return x[1] % 2
def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def half(x):
    if x[0] % 2 or x[1] % 2: raise Undecided('non-integral half')
    return (x[0] // 2, x[1] // 2)
def ge3(x):
    if x[0] >= 0 and x[1] >= 3: return True
    if x[0] == 0 and x[1] < 3: return False
    raise Undecided('comparison depends on u')
def stop_sym(L):
    Z = (0, 0); A = L[0]; b = L[1] if len(L) > 1 else Z; c = L[2] if len(L) > 2 else Z; S = L[3:]
    if par(A) == 0: return [add(A, b, c, (0, 3))] + S
    m = half(add(b, b, A, (0, -3))); st = [half(add(c, c, A, (0, 1)))] + S
    while par(m) == 1 and ge3(m):
        st = [half(add(m, (0, 3)))] + st; m = half(add(m, (0, -3)))
    if par(m) == 1: raise Exception('HALT reachable')   # m odd and <3 for all u => m==1
    return [add(m, (0, 4))] + st
def E_sym(v):
    w = (2, 1)
    return [add(w, w, w, (0, 1))] + [(6 << i, 3 << i) for i in range(v - 1)] + [(6 << (v - 1), (3 << (v - 1)) - 1)]
ell = {}
for v in range(1, V0 + 1):
    L = E_sym(v); t = 0
    while len(L) > 1:
        L = stop_sym(L); t += 1
        assert all(x[0] >= 0 and x[1] >= 0 for x in L)
    ell[v] = t
    assert L[0] == (6 << v, (3 << v) + 3 * t), (v, L, t)   # singleton 3w*2^v + 3*ell
print('check1 OK: for every v<=%d and every odd w, E(w,v) reaches a singleton after ell(v) steps, no halt' % V0)
print('  ell(1..40) =', [ell[v] for v in range(1, 41)])

# ---- check 2 [Class-B]: decomposition matches the concrete orbit ----
L = [3]; n = 0; N = 1 << 20
while n < N:
    assert len(L) == 1 and L[0] == 3 * n + 3
    if L[0] % 2 == 0: L = top(L); n += 1; continue
    q = n + 2; v = v2(q); w = q >> v
    L = top(L); n += 1
    assert L == [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
    for _ in range(ell[v]):
        assert L != 'HALT'; L = top(L); n += 1
print('check2 OK: concrete orbit == singleton/excursion decomposition for n <', N)

# ---- check 3 [Class-B]: offset-run normal form at odd multi-element steps (empirical) ----
L = [3]; bad = 0; cnt = 0; minmargin = 99
for n in range(1 << 20):
    if L[0] % 2 and len(L) > 1:
        cnt += 1; A, b = L[0], L[1]
        c = L[2] if len(L) > 2 else None
        if c == 2 * b or c == 2 * b - 1: g, d = b, A - b; mg = v2(g) - v2(d + 3)
        elif c is None: g, d = b + 1, A - b - 1; mg = v2(g) - v2(d + 1)
        else: bad += 1; mg = 99
        minmargin = min(minmargin, mg)
    L = top(L)
print('check3: %d odd multi-element steps, %d outside normal form, min 2-adic margin %d' % (cnt, bad, minmargin))
