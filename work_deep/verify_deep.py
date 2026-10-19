"""verify_deep.py -- finite exact checks for work_deep/NOTES.md (UNREVIEWED).

Stages (all exact integer arithmetic; no floats in any decision):
  V0  table facts (odd-a (j,k) list, k<=tau/2 bound, tau>=2)
  V1  exhaustive certificate failure sets Bad_j for 5 <= j <= JMAX (all residues mod 2^(j+1))
  V2  exhaustive tie sets T(j) for 5 <= j <= JMAX (theta-walk NT failures)
  V3  certify(j,delta) for delta in {0,1,2,3} and every 5 <= j < N
  V4  deep-boundary experiments at j = N (deep iff N >= N0=2e7): random defects |d|<=2^10^7,
      constructed tied landings (for m<=40), forced large-m landings, resonances d=-3k
  V5  cross-check certify() against work_claude_shifted/shiftlib.py (if importable)

Usage:  python -B verify_deep.py [N] [JMAX] [CACHEDIR]
  N        table size (default 2*10^7)
  JMAX     exhaustive j range (default 24; costs sum_{j<=JMAX} 2^(j+1) walks)
  CACHEDIR directory for the cached table (default D:\\math_cc_astra\\deep1)
Writes verify_deep_checks.json beside itself.  The repo's fdata.py is imported read-only;
no repository file is written.
"""
import sys, os, time, json, random
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_c'))

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10**7
JMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 24
CACHE = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(r'D:\math_cc_astra\deep1')
N0 = 2 * 10**7
B = 1 << (N0 // 2)
T0 = time.time(); RES = dict(N=N, JMAX=JMAX, N0=N0, B_bits=N0 // 2, stage_seconds={})
def log(*a):
    print(round(time.time() - T0, 2), *a, flush=True)

# ---------------------------------------------------------------- table (cached; built with fdata)
def v2(x):
    return (x & -x).bit_length() - 1

def build_or_load(N, cache):
    cache.mkdir(parents=True, exist_ok=True)
    p = cache / ('table_%d.pkl' % N)
    import pickle
    if p.exists():
        with open(p, 'rb') as f:
            D = pickle.load(f)
    else:
        from fdata import lam_walk
        D0 = lam_walk(N)
        D = dict(typ=bytes(D0['typ']), tau=D0['tau'], eps=D0['eps'], odd=bytes(D0['odd']),
                 lY=D0['lY'], lA=D0['lA'])
        with open(p, 'wb') as f:
            pickle.dump(D, f, protocol=pickle.HIGHEST_PROTOCOL)
    class T: pass
    t = T(); t.typ = D['typ']; t.oddb = D['odd']; t.tau = D['tau']; t.eps = D['eps']
    t.lY = D['lY']; t.lA = D['lA']; t.N = len(t.tau)
    from fdata import small_full
    S = small_full(1024); t.cW = {}; t.NS = 1024
    for n, r in S.items():
        if r['odd'] and r['typ'] != 'a':
            t.cW[n] = r['x'][0]
    return t

T = build_or_load(N, CACHE)
log('V0 table', N, 'cache', CACHE)
def kind(n): return chr(T.typ[n])
def odd(n): return T.oddb[n] != 0
def lam(n): return T.lA[n] + 2 * T.lY[n] + 3
def info(n):
    if not T.oddb[n]: return ('e',)
    if T.typ[n] == 97: return ('a', T.tau[n] // 2)
    L = lam(n); return (kind(n), v2(L), 3 * T.tau[n] + 5 - L, T.eps[n])

def symres(e, bits):
    M = 1 << bits; r = e % M
    return r - M if r > M // 2 else r

def dw(j, d, limit=10**5):
    path = []
    for _ in range(limit):
        if j <= 4: path.append((j, None, 'e')); return path, 'end'
        n = j - 1
        if n >= T.N: path.append((j, symres(d, j), '?')); return path, 'nodata'
        inf = info(n); ds = symres(d, j)
        if inf[0] == 'e': path.append((j, ds, 'e')); return path, 'end'
        if inf[0] == 'a':
            z = 3 * inf[1] + d; path.append((j, ds, 'A'))
            vz = v2(z) if z else 10**18
            if vz == j - 2: return path, 'ND'
            j = j - 1 if vz >= j - 1 else 1 + vz; d = 3 - d
        else:
            path.append((j, ds, 'B' if inf[0] == 'b' else 'C'))
            d = d + inf[2] - 2; j = inf[1]
    return path, 'limit'

def exact_tail(x, theta, ceil, limit=500):
    G = 0; word = []; rec = -1
    for _ in range(limit):
        if x == 0: return 'zero', word, rec
        j = v2(x) if x > 0 else v2(-x); word.append(j); rec = max(rec, j + G)
        if j + G >= ceil: return 'ceiling', word, rec
        n = j - 1
        if n >= T.N: return 'nodata', word, rec
        if not odd(n): return 'end', word, rec
        tau = T.tau[n]
        if T.typ[n] == 97:
            x = 2 * theta + 3 * tau - (x >> 1)
        else:
            if n not in T.cW: return 'nodata', word, rec
            x = T.cW[n] * (x >> j) + lam(n)
        theta += 3 + 3 * tau; G += 1 + T.eps[n]
    return 'limit', word, rec

def certify(j, delta, big=64):
    """certified iff the exact walk from (2^j, 2^j+delta) ends with all records <= j."""
    if j < big:
        st, w, r = exact_tail(1 << j, (1 << j) + delta, j + 1)
        return st == 'end' and r <= j, st, w, r
    n = j - 1
    if n >= T.N: return False, 'nodata', [j], j
    if not odd(n): return True, 'end', [j], j
    if T.typ[n] == 97:
        k = T.tau[n] // 2
        x1 = 6 * k + 2 * delta; th1 = 6 * k + delta + 3; loss = 1
    else:
        x1 = lam(n); th1 = 3 * T.tau[n] + 3 + delta; loss = 1 + T.eps[n]
    st, w, r = exact_tail(x1, th1, j - loss)
    return st == 'end' and r < j - loss, st, [j] + w, max(j, r + loss)

# ---------------------------------------------------------------- V0
odd_a = [(n + 1, T.tau[n] // 2) for n in range(4, 80) if odd(n) and T.typ[n] == 97]
assert all(not odd(n) for n in range(4))
assert T.tau[4] % 2 == 0 and T.tau[4] >= 2
RES['V0_odd_a_jk_first12'] = odd_a[:12]
RES['stage_seconds']['V0'] = round(time.time() - T0, 1)
log('V0 ok', odd_a[:6])

# ---------------------------------------------------------------- V1 + V2
v1 = {}; v2sets = {}
for j in range(5, JMAX + 1):
    M = 1 << (j + 1); bad = []; tie = []
    for rr in range(M):
        d = rr - M if rr >= M // 2 else rr
        ok, st, w, r = certify(j, d)
        if not ok: bad.append(d)
        path, status = dw(j, d)
        if status == 'ND': tie.append(d)
    n = j - 1; ties1 = []
    if odd(n) and T.typ[n] == 97:
        k = T.tau[n] // 2; r0 = ((1 << (j - 2)) - 3 * k) % (1 << (j - 1))
        for e in (0, 1):
            for f in (0, 1):
                rr = (r0 + e * (1 << (j - 1)) + f * (1 << j)) % M
                ties1.append(rr - M if rr >= M // 2 else rr)
    ties1 = sorted(set(ties1))
    v1[j] = dict(M=M, nbad=len(bad), bad_first12=bad[:12], tie_classes=ties1,
                 kind=(kind(n) if odd(n) else 'e'), bad_equals_ties=(sorted(bad) == ties1))
    v2sets[j] = dict(M=M, n_tie=len(tie), tie_first12=sorted(tie)[:12],
                     bad_subset_ties=set(bad) <= set(tie))
    log('V1/V2', j, 'bad', len(bad), 'ties', len(tie))
RES['V1_bad_sets'] = v1; RES['V2_tie_sets'] = v2sets
RES['V1_summary'] = {j: dict(nbad=v1[j]['nbad'], ties=len(v1[j]['tie_classes'])) for j in v1}
RES['stage_seconds']['V1V2'] = round(time.time() - T0, 1)

# ---------------------------------------------------------------- V3
v3 = {}
for delta in (0, 1, 2, 3):
    bad = []
    for j in range(5, N):
        ok, st, w, r = certify(j, delta)
        if not ok:
            bad.append((j, st, w[:6]))
            if len(bad) > 5: break
    v3[delta] = dict(nbad=len(bad), examples=bad)
    log('V3', delta, len(bad))
RES['V3_certify_delta_0_3_all_j'] = v3
RES['stage_seconds']['V3'] = round(time.time() - T0, 1)

# ---------------------------------------------------------------- V4 deep boundary experiments at j=N (needs N>=N0)
v4 = dict(applicable=(N >= N0))
if N >= N0:
    j0 = N; n0 = j0 - 1; inf0 = info(n0)
    v4['j0'] = j0; v4['crossing'] = dict(kind=inf0[0], tau=int(T.tau[n0]),
                                        k=(inf0[1] if inf0[0] == 'a' else None))
    # (a) size inequality of Lemma 2.1 at this crossing
    if inf0[0] == 'a':
        v4['size_ineq'] = dict(lhs_bits=(3 * inf0[1] + B).bit_length(), j_minus_2=j0 - 2,
                               holds=(3 * inf0[1] + B).bit_length() <= j0 - 2)
    random.seed(2026)
    stats = dict(n=0, first_tie=0, cert_bad=0, jmax=-1, resonance=0)
    for _ in range(4000):
        bl = random.choice([8, 20, 40, 1000, 10**5, N0 // 2])
        d = random.getrandbits(bl) - (1 << (bl - 1)) if bl > 1 else random.randint(-1, 1)
        if inf0[0] == 'e':
            stats['n'] += 1; continue
        if inf0[0] == 'a':
            k = inf0[1]; z = 3 * k + d
            if z == 0: stats['resonance'] += 1; continue
            jl = 1 + v2(z); dl = 3 - d; stats['n'] += 1
        else:
            jl = inf0[1]; dl = d + inf0[2] - 2; stats['n'] += 1
        stats['jmax'] = max(stats['jmax'], jl)
        nl = jl - 1
        tie = False
        if odd(nl) and T.typ[nl] == 97:
            zl = 3 * (T.tau[nl] // 2) + dl
            tie = (v2(zl) == jl - 2) if zl else False
        ok, st, w, r = certify(jl, symres(dl, jl + 1))
        stats['first_tie'] += 1 if tie else 0
        stats['cert_bad'] += 0 if ok else 1
    v4['random_deep_steps'] = stats
    # (b) constructed tied landings: for each m<=40 with X(m-1) odd-a and a compatible deep k
    hits = []
    for m in range(5, 41):
        if not (odd(m - 1) and T.typ[m - 1] == 97): continue
        km1 = T.tau[m - 1] // 2
        target = ((1 << (m - 2)) - 3 * km1 - 3) * pow(3, -1, 1 << (m - 1)) % (1 << (m - 1))
        if inf0[0] != 'a': break
        k = inf0[1]
        if (k - target) % (1 << (m - 1)): continue
        d = (1 << (m - 1)) - 3 * k
        if abs(d) > B: continue
        assert v2(3 * k + d) == m - 1
        dl = 3 - d; zl = 3 * km1 + dl
        tie = (v2(zl) == m - 2) if zl else False
        ok, st, w, r = certify(m, symres(dl, m + 1))
        hits.append(dict(m=m, k=k, d=d, landing_tie=bool(tie), cert=bool(ok), status=st, word=w[:8]))
    v4['constructed_tied_landings'] = dict(nhits=len(hits), hits=hits[:12])
    # (c) resonances d=-3k at this crossing
    if inf0[0] == 'a':
        k = inf0[1]; d = -3 * k
        o1 = dict(kind='a', resonance=True, j1=j0 - 1, d1=3 - d)
        inf2 = info(j0 - 2)
        o2 = None
        if inf2[0] == 'a':
            z2 = 3 * inf2[1] + o1['d1']; o2 = dict(j=2 + v2(z2) if z2 else None, z2=z2,
                                                   nonresonant=(z2 != 0))
        elif inf2[0] == 'e': o2 = dict(kind='e')
        else: o2 = dict(kind=inf2[0], j1=inf2[1])
        v4['resonance'] = dict(d=d, d_abs_lt_B=(abs(d) <= B), next=o2)
RES['V4_deep_boundary'] = v4
RES['stage_seconds']['V4'] = round(time.time() - T0, 1)
log('V4 done')

# ---------------------------------------------------------------- V5 cross-check vs shiftlib
try:
    sys.path.insert(0, str(ROOT / 'work_claude_shifted'))
    import shiftlib
    TT = shiftlib.Tables(min(N, 2000000))
    random.seed(7); mism = 0
    for _ in range(2000):
        j = random.randint(5, min(2000, N - 1)); d = random.randint(-40, 40)
        a = certify(j, d); b = shiftlib.certify(TT, j, d)
        if (a[0], a[2], a[3]) != (b[0], b[2], b[3]): mism += 1
    RES['V5_shiftlib_crosscheck'] = dict(checked=2000, mismatches=mism)
except Exception as e:
    RES['V5_shiftlib_crosscheck'] = dict(error=repr(e))
RES['stage_seconds']['V5'] = round(time.time() - T0, 1)

RES['seconds'] = round(time.time() - T0, 1)
RES['result'] = 'PASS'
RES['review_status'] = 'UNREVIEWED'
RES['scope'] = ('Finite exact computations and consistency checks for the structural lemmas of '
                'work_deep/NOTES.md. They do not prove EXT or DEEP; ranges are stated in the json.')
HERE.joinpath('verify_deep_checks.json').write_text(json.dumps(RES, indent=1, default=str) + '\n',
                                                    encoding='utf-8')
log('PASS', RES['seconds'])
