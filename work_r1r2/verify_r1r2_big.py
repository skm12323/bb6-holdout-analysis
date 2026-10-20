"""verify_r1r2_big.py -- large-scale exact check of the resolved bare-tie classes (UNREVIEWED).

For every m >= 5 the two-step gateway resolution of the bare ties (5,5) and (5,-11) produces,
at the resolved chain u+1 of parameter m, the defect class
    cls55(m)   = (10 - 2^m)/3   mod 2^(m+1)
    cls5m11(m) = (26 - 2^m)/3   mod 2^(m+1)
(3*cls == 10-2^m resp. 26-2^m mod 2^(m+1)).  Question: does certify(m, cls) hold for every m,
i.e. does the exact walk from the representative (2^m, 2^m+cls) end with all records <= m?

Method.  The walk from the canonical lift cls in [0,2^(m+1)) is run with truncated arithmetic:
the state is tracked modulo 2^P (P = min(m+1, PREC)); an a-step costs 1 precision bit.  A b/c
step at chain parameter j uses only the reference successor lambda'_W(n) and drops the term
c'_W*u (v2(c'_W) = n-eps = j-1-eps), so the new state is known modulo 2^(min(curP, j)-1-eps)
(the HP precision; corrected 2026-10-20 after review -- the earlier version kept curP-1-eps and
thereby overstated the precision at non-first b/c steps).  A step whose valuation reaches the
remaining precision is flagged.  All non-flagged walks end
with records <= ~60 << m, so they are certified.  m < 64 uses full integers.

Usage: python -B verify_r1r2_big.py [table.pkl] [N] [SAMPLE]
Writes verify_r1r2_big_checks.json beside itself.
"""
import sys, json, time, pickle
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'work_global_ext' / 'route_c'))
TBL = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r'D:\math_cc_astra\deep1\table_20000000.pkl')
NS = int(sys.argv[2]) if len(sys.argv) > 2 else 2 * 10**7
SAMPLE = int(sys.argv[3]) if len(sys.argv) > 3 else 0
T0 = time.time(); RES = dict(table=str(TBL), NS=NS, sample=SAMPLE)
def log(*a):
    print(round(time.time() - T0, 2), *a, flush=True)

with open(TBL, 'rb') as f:
    D = pickle.load(f)
typ, tau, eps, odd, lY, lA = D['typ'], D['tau'], D['eps'], D['odd'], D['lY'], D['lA']
N = len(tau)
log('loaded table', N)
lam = lambda n: lA[n] + 2 * lY[n] + 3

def v2(x):
    return (x & -x).bit_length() - 1

PREC = 1024
INV3 = pow(3, -1, 1 << PREC)

def precision_walk(j0, delta, ceil, P, limit=2000):
    """exact reference walk from (2^j0, 2^j0+delta) tracked modulo 2^P; j0 >= P is allowed."""
    if j0 < P:
        xm = 1 << j0
        thm = (xm + delta) % (1 << P)
    else:
        xm = 0
        thm = delta % (1 << P)   # 2^j0 vanishes mod 2^P
    G = 0; rec = -1; word = []; curP = P; j = j0; first = True
    for _ in range(limit):
        rec = max(rec, j + G); word.append(j)
        if rec > ceil:
            return False, 'record', rec, word
        if (not first) and j >= curP:
            return False, 'precision', rec, word
        first = False
        n = j - 1
        if n >= N:
            return False, 'nodata', rec, word
        if not odd[n]:
            return True, 'end', rec, word
        t = chr(typ[n]); T = tau[n]
        if t == 'a':
            xm = (2 * thm + 3 * T - (xm >> 1)) % (1 << (curP - 1))
            thm = (thm + 3 + 3 * T) % (1 << (curP - 1))
            curP -= 1; G += 1
            if xm == 0:
                return False, 'precision', rec, word
            j = v2(xm)
        else:
            lo = lam(n)
            if lo <= 0:
                return False, 'nonpos', rec, word
            curP = min(curP, j) - 1 - eps[n]   # c'_W*u dropped: HP precision
            if curP <= 0:
                return False, 'precision', rec, word
            xm = lo % (1 << curP)
            thm = (thm + 3 + 3 * T) % (1 << curP)
            G += 1 + eps[n]
            j = v2(lo)
    return False, 'limit', rec, word

cW = None
def exact_walk_small(j, delta, ceil, limit=4000):
    global cW
    if cW is None:
        from fdata import small_full
        S = small_full(1024)
        cW = {n: r['x'][0] for n, r in S.items() if r['odd'] and r['typ'] != 'a'}
    x = 1 << j; th = x + delta; G = 0; rec = -1; word = []
    for _ in range(limit):
        if x <= 0:
            return False, 'nonpos', rec, word
        if v2(x) != j:
            return False, 'error', rec, word
        rec = max(rec, j + G); word.append(j)
        if rec > ceil:
            return False, 'record', rec, word
        n = j - 1
        if n >= N:
            return False, 'nodata', rec, word
        if not odd[n]:
            return True, 'end', rec, word
        t = chr(typ[n]); T = tau[n]
        if t == 'a':
            x = 2 * th + 3 * T - (x >> 1)
        else:
            if n not in cW:
                return False, 'nodata_cw', rec, word
            x = cW[n] * (x >> j) + lam(n)
        th += 3 + 3 * T; G += 1 + eps[n]
        if x <= 0:
            return False, 'nonpos', rec, word
        j = v2(x)
    return False, 'limit', rec, word

_DCACHE = {}
def delta_at(m, c):
    """class (c-2^m)/3 mod 2^min(m+1,PREC) as an integer in [0,2^P)"""
    P = min(m + 1, PREC)
    key = (P, c)
    if key not in _DCACHE:
        _DCACHE[key] = (c - (1 << m)) * pow(3, -1, 1 << P) % (1 << P)
    return _DCACHE[key], P

def check_m(m):
    out = []
    if m < 64:
        M = 1 << (m + 1)
        for name, c in (('55', 10), ('5m11', 26)):
            cls = (c - (1 << m)) * pow(3, -1, M) % M
            ok, st, rec, w = exact_walk_small(m, cls, m)
            out.append((name, ok, st, rec, len(w)))
        return all(o[1] for o in out), out
    for name, c in (('55', 10), ('5m11', 26)):
        delta, P = delta_at(m, c)
        ok, st, rec, w = precision_walk(m, delta, m, P)
        out.append((name, ok, st, rec, len(w)))
    return all(o[1] for o in out), out

# validation: precision walk vs full exact walk for 64 <= m < 3000
if SAMPLE:
    bad = []
    for m in range(64, 3000, 7):
        M = 1 << (m + 1)
        for name, c in (('55', 10), ('5m11', 26)):
            cls = (c - (1 << m)) * pow(3, -1, M) % M
            ok1, st1, r1, w1 = exact_walk_small(m, cls, m)
            ok2, st2, r2, w2 = precision_walk(m, cls, m, min(m + 1, PREC))
            if st1 == 'nodata_cw':
                continue   # exact walk lacks c'_W beyond n=1024; precision walk is the reference
            if (ok1, st1) != (ok2, st2) or len(w1) != len(w2):
                bad.append((m, name, st1, st2, len(w1), len(w2)))
    RES['validation_bad'] = bad[:10]
    log('validation mismatches', len(bad))

if SAMPLE:
    import random
    random.seed(7)
    ms = list(range(5, 300)) + [random.randrange(300, NS) for _ in range(SAMPLE)]
else:
    ms = range(5, NS)
fails = []
cnt = 0
t0 = time.time()
progress = max(1, len(ms) // 20) if not SAMPLE else 10**9
for i, m in enumerate(ms):
    ok, info = check_m(m)
    cnt += 1
    if not ok:
        fails.append((m, info))
        if len(fails) <= 25:
            log('FAIL', m, info)
    if not SAMPLE and i % progress == 0:
        log('progress', i, '/', len(ms), 'fails', len(fails), '%.0fs' % (time.time() - t0))
RES.update(count=cnt, fails=fails[:200], n_fails=len(fails), seconds=round(time.time() - t0, 1))
log('done', cnt, 'fails', len(fails))
with open(HERE / 'verify_r1r2_big_checks.json', 'w', encoding='utf-8') as f:
    json.dump(RES, f, indent=1, default=str)
