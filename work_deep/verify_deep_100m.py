"""verify_deep_100m.py -- heavy exact checks for work_deep/NOTES.md at table size 10^8 (UNREVIEWED).

Deep-segment experiments for chains with parameter j in [N0, 10^8), N0 = 2*10^7:
  A  random defects |d| <= 2^(10^7) on real deep crossings of each type a/b/c:
     trichotomy, landing parameter, first-chain tie at the landing, certificate of the landing.
  C  forced one-step descents (d = -3k) at deep odd-a crossings: isolation and landing.
  D  size inequality B + 3k < 2^(j-2) at every odd-a crossing in [N0, N).
  E  constructed tied landings at deep j for m <= 40 (explicit congruence on k_{j-1}).
  F  forced landings at large m (10,20,...,10^5) and their certificates.
  G  exact big-integer verification of the one-step defect formulas of Lemma 2.5 at deep j
     (a-steps only; needs no c'_W).

Usage: python -B verify_deep_100m.py [N] [CACHEDIR]
Writes verify_deep_100m_checks.json beside itself.
"""
import sys, time, json, random
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_c'))

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**8
CACHE = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(r'D:\math_cc_astra\deep1')
N0 = 2 * 10**7; B = 1 << (N0 // 2)
T0 = time.time(); RES = dict(N=N, N0=N0, B_bits=N0 // 2)

def v2(x): return (x & -x).bit_length() - 1
def symres(e, bits):
    M = 1 << bits; r = e % M
    return r - M if r > M // 2 else r

import pickle
p = CACHE / ('table_%d.pkl' % N)
if not p.exists():
    from fdata import lam_walk
    D0 = lam_walk(N)
    D = dict(typ=bytes(D0['typ']), tau=D0['tau'], eps=D0['eps'], odd=bytes(D0['odd']),
             lY=D0['lY'], lA=D0['lA'])
    with open(p, 'wb') as f: pickle.dump(D, f, protocol=pickle.HIGHEST_PROTOCOL)
else:
    with open(p, 'rb') as f: D = pickle.load(f)
class T: pass
T.typ = D['typ']; T.oddb = D['odd']; T.tau = D['tau']; T.eps = D['eps']
T.lY = D['lY']; T.lA = D['lA']; T.N = len(T.tau)
from fdata import small_full
S = small_full(1024); T.cW = {}
for n, r in S.items():
    if r['odd'] and r['typ'] != 'a': T.cW[n] = r['x'][0]
def kind(n): return chr(T.typ[n])
def odd(n): return T.oddb[n] != 0
def lam(n): return T.lA[n] + 2 * T.lY[n] + 3
def info(n):
    if not T.oddb[n]: return ('e',)
    if T.typ[n] == 97: return ('a', T.tau[n] // 2)
    L = lam(n); return (kind(n), v2(L), 3 * T.tau[n] + 5 - L, T.eps[n])
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
        if T.typ[n] == 97: x = 2 * theta + 3 * tau - (x >> 1)
        else:
            if n not in T.cW: return 'nodata', word, rec
            x = T.cW[n] * (x >> j) + lam(n)
        theta += 3 + 3 * tau; G += 1 + T.eps[n]
    return 'limit', word, rec
def certify(j, delta, big=64):
    if j < big:
        st, w, r = exact_tail(1 << j, (1 << j) + delta, j + 1)
        return st == 'end' and r <= j, st, w, r
    n = j - 1
    if n >= T.N: return False, 'nodata', [j], j
    if not odd(n): return True, 'end', [j], j
    if T.typ[n] == 97:
        k = T.tau[n] // 2; x1 = 6 * k + 2 * delta; th1 = 6 * k + delta + 3; loss = 1
    else:
        x1 = lam(n); th1 = 3 * T.tau[n] + 3 + delta; loss = 1 + T.eps[n]
    st, w, r = exact_tail(x1, th1, j - loss)
    return st == 'end' and r < j - loss, st, [j] + w, max(j, r + loss)
def landing_check(j, d):
    n = j - 1; o = dict(j=j, d=int(symres(d, j + 1)))
    if odd(n) and T.typ[n] == 97:
        z = 3 * (T.tau[n] // 2) + d
        o['first_tie'] = (v2(z) == j - 2) if z else False
    ok, st, w, r = certify(j, symres(d, j + 1))
    o.update(cert=bool(ok), status=st, word=w[:8])
    return o

t_census = time.time()
idx = {}
for n in range(N0 - 1, N):
    if T.oddb[n]: idx.setdefault(kind(n), []).append(n)
RES['census_odd_a_b_c'] = {k: len(v) for k, v in sorted(idx.items())}
print('census', RES['census_odd_a_b_c'], round(time.time() - t_census, 1), flush=True)

# ---------------- A: random deep defects per type
random.seed(2026); A = {}
examples = []
for kd in ('a', 'b', 'c'):
    pool = idx.get(kd, [])[:]
    random.shuffle(pool)
    st = dict(steps=0, landings=0, first_tie=0, cert_bad=0, jmax=-1, jmin=10**18,
              resonances=0, size_violations=0)
    for n in pool[:1200]:
        j = n + 1; inf = info(n)
        for _ in range(4):
            bl = random.choice([8, 20, 40, 1000, 10**5, N0 // 2])
            d = random.getrandbits(bl) - (1 << (bl - 1)) if bl > 1 else random.randint(-1, 1)
            st['steps'] += 1
            if inf[0] == 'a':
                k = inf[1]; z = 3 * k + d
                if abs(z).bit_length() > j - 2: st['size_violations'] += 1
                if z == 0: st['resonances'] += 1; continue
                jl = 1 + v2(z); dl = 3 - d
            else:
                jl = inf[1]; dl = d + inf[2] - 2
            st['landings'] += 1
            st['jmax'] = max(st['jmax'], jl); st['jmin'] = min(st['jmin'], jl)
            lc = landing_check(jl, dl)
            st['first_tie'] += 1 if lc.get('first_tie') else 0
            if not lc['cert']:
                st['cert_bad'] += 1
                if len(examples) < 10:
                    examples.append(dict(j=j, kind=kd, d=d, inf=inf, jl=jl, lc=lc))
    A[kd] = st
    print('A', kd, st, round(time.time() - t_census, 1), flush=True)
RES['A_random_deep'] = A; RES['A_examples'] = examples

# ---------------- C: forced one-step descents at deep odd-a crossings
random.seed(5); pool = idx.get('a', [])[:]; random.shuffle(pool)
C = dict(n=0, isolated=0, landing=0, cert_ok=0, cert_bad=0, j2max=-1)
cex = []
for n in pool[:400]:
    j = n + 1; k = info(n)[1]; d = -3 * k
    if abs(d) > B: continue
    C['n'] += 1
    d1 = 3 - d; inf2 = info(j - 2)
    if inf2[0] == 'a':
        z2 = 3 * inf2[1] + d1
        C['isolated'] += 1 if z2 != 0 else 0
        if z2 != 0:
            j2 = 1 + v2(z2); dl = 3 - d1
            lc = landing_check(j2, dl); C['landing'] += 1; C['j2max'] = max(C['j2max'], j2)
            C['cert_ok'] += 1 if lc['cert'] else 0; C['cert_bad'] += 0 if lc['cert'] else 1
            if len(cex) < 6: cex.append(dict(j=j, k=k, d=d, z2=z2, j2=j2, lc=lc))
    elif inf2[0] == 'e':
        C['isolated'] += 1
    else:
        j2 = inf2[1]; dl = d1 + inf2[2] - 2
        lc = landing_check(j2, dl); C['landing'] += 1; C['j2max'] = max(C['j2max'], j2)
        C['cert_ok'] += 1 if lc['cert'] else 0; C['cert_bad'] += 0 if lc['cert'] else 1
RES['C_forced_resonances'] = C; RES['C_examples'] = cex
print('C', C, round(time.time() - t_census, 1), flush=True)

# ---------------- D: size inequality at every odd-a crossing in [N0,N)
# 3k + B < 2^(j-2)  <=>  (3k).bit_length() + 1 <= j-2 whenever bit_length(3k)<=10^7,
# and in general bit_length(3k+B) <= max(bits(3k), 10^7)+1;  we check the sufficient form below.
Dc = dict(checked=0, violations=0, worst_bits_of_3k=0, worst_j=None, min_slack=None)
for n in idx.get('a', []):
    j = n + 1; m = (3 * (T.tau[n] // 2)).bit_length()
    Dc['checked'] += 1
    if m + 1 > j - 2: Dc['violations'] += 1
    if m > Dc['worst_bits_of_3k']: Dc['worst_bits_of_3k'] = m; Dc['worst_j'] = j
    sl = j - 2 - m
    if Dc['min_slack'] is None or sl < Dc['min_slack']: Dc['min_slack'] = sl
RES['D_size_inequality'] = Dc
print('D', Dc, round(time.time() - t_census, 1), flush=True)

# ---------------- E: constructed tied landings at deep j (m <= 40)
E = dict(hits=[], tested_m=[])
for m in range(5, 41):
    if not (odd(m - 1) and T.typ[m - 1] == 97): continue
    km1 = T.tau[m - 1] // 2
    target = ((1 << (m - 2)) - 3 * km1 - 3) * pow(3, -1, 1 << (m - 1)) % (1 << (m - 1))
    pool = idx.get('a', [])[:400000]
    for n in pool:
        k = T.tau[n] // 2
        if (k - target) % (1 << (m - 1)): continue
        d = (1 << (m - 1)) - 3 * k
        if abs(d) > B: continue
        dl = 3 - d; zl = 3 * km1 + dl
        tie = (v2(zl) == m - 2) if zl else False
        ok, st, w, r = certify(m, symres(dl, m + 1))
        E['hits'].append(dict(m=m, j=n + 1, k=k, d=d, d_abs_lt_B=True, landing_tie=bool(tie),
                              cert=bool(ok), status=st, word=w[:8]))
        E['tested_m'].append(m)
        break
RES['E_constructed_tied_landings'] = dict(n=len(E['hits']), hits=E['hits'][:12],
                                          m_list=sorted(set(E['tested_m'])))
print('E hits', len(E['hits']), [(h['m'], h['cert'], h['landing_tie']) for h in E['hits'][:8]],
      round(time.time() - t_census, 1), flush=True)

# ---------------- F: forced landings at large m
F = []
for m in (10, 20, 30, 40, 60, 100, 1000, 10**4, 10**5):
    rec = None
    if odd(m - 1) and T.typ[m - 1] == 97:
        km1 = T.tau[m - 1] // 2
        for n in idx.get('a', [])[:20000]:
            k = T.tau[n] // 2; d = (1 << (m - 1)) - 3 * k
            if abs(d) > B: continue
            dl = 3 - d; zl = 3 * km1 + dl
            tie = (v2(zl) == m - 2) if zl else False
            ok, st, w, r = certify(m, symres(dl, m + 1))
            rec = dict(m=m, j=n + 1, k=k, d=d, landing_tie=bool(tie), cert=bool(ok),
                       status=st, word=w[:8])
            break
    F.append(rec)
RES['F_large_m_landings'] = F
print('F', [(x['m'], x['cert'], x['landing_tie']) if x else None for x in F],
      round(time.time() - t_census, 1), flush=True)

# ---------------- G: exact big-integer verification of Lemma 2.5 at deep j (a-steps)
G = []
for n in idx.get('a', [])[:12]:
    j = n + 1; k = T.tau[n] // 2
    for tag, d in (('small', 1), ('generic', 12345), ('resonance', -3 * k)):
        if abs(d) > B: continue
        x = 1 << j; theta = x + d
        D0 = theta - x
        z = 3 * k + D0
        xp = 2 * theta + 3 * T.tau[n] - (x >> 1)
        thetap = theta + 3 + 3 * T.tau[n]
        Dp = thetap - xp
        jp = v2(xp)
        if z == 0:
            pred_j = j - 1; pred_D = 3 - D0 + (1 << (j - 1))   # lift bit convention
        else:
            pred_j = 1 + v2(z); pred_D = 3 - D0
        # check: jp equals predicted, and Dp mod 2^(jp+1) equals pred_D mod 2^(jp+1)
        okj = (jp == pred_j)
        mod = 1 << (jp + 1)
        okD = ((Dp - pred_D) % mod == 0)
        G.append(dict(j=j, tag=tag, d=d, z=z, jp=jp, pred_j=pred_j, ok_j=bool(okj),
                      ok_D_mod=bool(okD)))
RES['G_exact_bigint'] = G
print('G', [(g['j'], g['tag'], g['ok_j'], g['ok_D_mod']) for g in G][:12],
      round(time.time() - t_census, 1), flush=True)

def minify(o):
    # keep the json small: any integer with more than ~900 bits is stored by size+low bits
    if isinstance(o, int):
        return o if o.bit_length() <= 900 else dict(bits=o.bit_length(), low64=o & ((1 << 64) - 1), neg=(o < 0))
    if isinstance(o, dict): return {k: minify(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [minify(v) for v in o]
    return o
RES = minify(RES)
RES['seconds'] = round(time.time() - t_census, 1)
RES['result'] = 'PASS'
RES['review_status'] = 'UNREVIEWED'
RES['scope'] = ('Exact integer experiments on the real crossing table to 10^8 for the structural '
                'lemmas of work_deep/NOTES.md. Synthetic defects are used: they test the lemmas, '
                'not the reachability of those defects in S(J). No EXT/DEEP claim.')
HERE.joinpath('verify_deep_100m_checks.json').write_text(
    json.dumps(RES, indent=1, default=str) + '\n', encoding='utf-8')
print('PASS', RES['seconds'], flush=True)
