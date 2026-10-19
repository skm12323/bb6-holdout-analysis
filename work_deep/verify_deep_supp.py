"""verify_deep_supp.py -- supplementary checks for work_deep/NOTES.md (UNREVIEWED).

S1  all first-chain tie classes are certificate failures, for 18 <= j <= 80
S2  random (j,delta) with j in [18,80] and defects up to 2^(10^7): every certificate failure is a
    first-chain tie (i.e. Bad_j = Tie_j on the sample); later ties do not break certification
S3  (5,5)-landing preimages at j <= 400 with k_{j-1} == 6 (mod 16): all have an NT failure and all certify

Usage: python -B verify_deep_supp.py [N] [CACHEDIR]   (default N=2*10^7)
Writes verify_deep_supp_checks.json beside itself.
"""
import sys, time, json, random
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_c'))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10**7
CACHE = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(r'D:\math_cc_astra\deep1')
import pickle
p = CACHE / ('table_%d.pkl' % N)
with open(p, 'rb') as f: D = pickle.load(f)
class T: pass
T.typ = D['typ']; T.oddb = D['odd']; T.tau = D['tau']; T.eps = D['eps']; T.lY = D['lY']; T.lA = D['lA']
T.N = len(T.tau)
from fdata import small_full
S = small_full(1024); T.cW = {}
for n, r in S.items():
    if r['odd'] and r['typ'] != 'a': T.cW[n] = r['x'][0]
def v2(x): return (x & -x).bit_length() - 1
def odd(n): return T.oddb[n] != 0
def lam(n): return T.lA[n] + 2 * T.lY[n] + 3
def symres(e, bits):
    M = 1 << bits; r = e % M
    return r - M if r > M // 2 else r
def info(n):
    if not T.oddb[n]: return ('e',)
    if T.typ[n] == 97: return ('a', T.tau[n] // 2)
    L = lam(n); return (chr(T.typ[n]), v2(L), 3 * T.tau[n] + 5 - L, T.eps[n])
def dw(j, d):
    path = []
    for _ in range(10**5):
        if j <= 4: return path, 'end'
        n = j - 1
        if n >= T.N or n < 0: return path, 'nodata'
        inf = info(n)
        if inf[0] == 'e': return path, 'end'
        if inf[0] == 'a':
            z = 3 * inf[1] + d
            if z and v2(z) == j - 2: return path, 'ND'
            vz = v2(z) if z else 10**18
            j = j - 1 if vz >= j - 1 else 1 + vz; d = 3 - d
        else:
            d = d + inf[2] - 2; j = inf[1]
    return path, 'limit'
def exact_tail(x, theta, ceil):
    G = 0; word = []; rec = -1
    for _ in range(500):
        if x == 0: return 'zero', word, rec
        j = v2(x) if x > 0 else v2(-x); word.append(j); rec = max(rec, j + G)
        if j + G >= ceil: return 'ceiling', word, rec
        n = j - 1
        if n >= T.N: return 'nodata', word, rec
        if not odd(n): return 'end', word, rec
        tau = T.tau[n]
        if T.typ[n] == 97: x = 2 * theta + 3 * tau - (x >> 1)
        else:
            if n not in T.cW: return 'nodata', word, rec
            x = T.cW[n] * (x >> j) + lam(n)
        theta += 3 + 3 * tau; G += 1 + T.eps[n]
    return 'limit', word, rec
def certify(j, delta, big=64):
    if j < big:
        st, w, r = exact_tail(1 << j, (1 << j) + delta, j + 1)
        return st == 'end' and r <= j, st, w
    n = j - 1
    if n >= T.N: return False, 'nodata', [j]
    if not odd(n): return True, 'end', [j]
    if T.typ[n] == 97:
        k = T.tau[n] // 2; x1 = 6 * k + 2 * delta; th1 = 6 * k + delta + 3; loss = 1
    else:
        x1 = lam(n); th1 = 3 * T.tau[n] + 3 + delta; loss = 1 + T.eps[n]
    st, w, r = exact_tail(x1, th1, j - loss)
    return st == 'end' and r < j - loss, st, [j] + w
def first_tie(j, d):
    n = j - 1
    if not (odd(n) and T.typ[n] == 97): return False
    z = 3 * (T.tau[n] // 2) + d
    return (v2(z) == j - 2) if z else False

T0 = time.time(); res = {}
# S1
mis = []
for j in range(18, 81):
    n = j - 1
    if not (odd(n) and T.typ[n] == 97): continue
    k = T.tau[n] // 2; r0 = ((1 << (j - 2)) - 3 * k) % (1 << (j - 1))
    for e in (0, 1):
        d = r0 + e * (1 << (j - 1))
        ok, _, _ = certify(j, d)
        if ok: mis.append((j, d))
res['S1_first_tie_classes_are_bad'] = dict(range='18..80', mismatches=len(mis), examples=mis[:5])
print('S1', len(mis), round(time.time() - T0, 1), flush=True)
# S2
random.seed(99)
stats = dict(tried=0, ties=0, bad=0, bad_not_first_tie=[], first_tie_not_bad=[])
for _ in range(30000):
    j = random.randint(18, 80)
    bl = random.choice([6, 10, 20, 30, 40, 60, 200, 1000, 10**7])
    d = random.getrandbits(bl) - (1 << (bl - 1)) if bl > 1 else random.randint(-1, 1)
    ft = first_tie(j, d)
    _, st = dw(j, d)
    ok, cst, w = certify(j, d)
    stats['tried'] += 1; stats['ties'] += 1 if st == 'ND' else 0; stats['bad'] += 0 if ok else 1
    if (not ok) and not ft: stats['bad_not_first_tie'].append(dict(j=j))
    if ft and ok: stats['first_tie_not_bad'].append(dict(j=j))
res['S2_random_bad_equals_first_tie'] = dict(tried=stats['tried'], ties=stats['ties'], bad=stats['bad'],
                                             bad_not_first_tie=len(stats['bad_not_first_tie']),
                                             first_tie_not_bad=len(stats['first_tie_not_bad']))
print('S2', {k: v for k, v in stats.items() if not isinstance(v, list)}, round(time.time() - T0, 1), flush=True)
# S3
hits = []
for n in range(17, 400):
    if not (odd(n) and T.typ[n] == 97): continue
    j = n + 1; k = T.tau[n] // 2
    if k % 16 != 6: continue
    d0 = (16 - 3 * k) % 32
    for lift in range(0, 8):
        d = d0 + lift * 32
        if v2(3 * k + d) != 4: continue
        _, st = dw(j, d); ok, cst, w = certify(j, d)
        hits.append(dict(j=j, k=k, d=d, status=st, cert=bool(ok), word=w[:8]))
        break
res['S3_55_preimages'] = dict(n=len(hits), cert_failures=sum(1 for h in hits if not h['cert']),
                              nd_count=sum(1 for h in hits if h['status'] == 'ND'), examples=hits[:8])
print('S3', res['S3_55_preimages']['n'], res['S3_55_preimages']['cert_failures'],
      res['S3_55_preimages']['nd_count'], round(time.time() - T0, 1), flush=True)
res['seconds'] = round(time.time() - T0, 1); res['review_status'] = 'UNREVIEWED'
res['scope'] = 'Finite exact sampling; supports Bad_j = Tie_j for j>=18 in the stated ranges only.'
HERE.joinpath('verify_deep_supp_checks.json').write_text(json.dumps(res, indent=1, default=str) + '\n',
                                                         encoding='utf-8')
print('PASS', res['seconds'])
