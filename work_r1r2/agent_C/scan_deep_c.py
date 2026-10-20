"""scan_deep_c.py -- canonical deep type-c crossings: landing parameter, class, badness.

For every odd type-c crossing n in [N0, N) of the cached canonical table (fdata.lam_walk
data, N in {2e7, 1e8}), and for theta_T in a window, compute the c-landing class

    delta = theta_T + 3 tau(n) + 3 - 2^omega(n)   (mod 2^(omega+1)),   omega = v2(lambda'_W(n))

(Theorems C1/C2 of NOTES.md) and decide certify(omega, delta).  Bad_omega is computed
exhaustively (all residues mod 2^(omega+1)) for every omega <= 12 that occurs, so the
badness decision is exact, not sampled; for omega > 12 the encountered classes are
decided directly by `certify`.

Also reports: omega distribution, tau mod 2^8/2^16/2^20, the reduced tau-congruence
theta == 2^(omega-2) - 3k_{omega-1} - 3 - 3 tau (mod 2^(omega-1)) at odd-a omega,
gateway size checks at omega = 5, and exact big-int spot checks of the class formula.

Usage: python -B scan_deep_c.py [table.pkl] [N0] [NS] [out.json]
Writes scan_deep_c.json beside this script.  Read-only outside this directory and the
scratch cache directory; no repository file is written.  Standard library only.
"""
import json
import sys
import time
from collections import Counter
from itertools import islice
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import clib  # noqa: E402

TABLE = sys.argv[1] if len(sys.argv) > 1 else r'D:\math_cc_astra\deep1\table_100000000.pkl'
N0 = int(sys.argv[2]) if len(sys.argv) > 2 else 2 * 10**7
NS = int(sys.argv[3]) if len(sys.argv) > 3 else 2048
OUT = Path(sys.argv[4]) if len(sys.argv) > 4 else (HERE / 'scan_deep_c.json')
RES = dict(table=TABLE, N0=N0, NS=NS, stage_seconds={})
T0 = time.time()


def log(*a):
    print(round(time.time() - T0, 2), *a, flush=True)


log('loading', TABLE)
T = clib.Table(TABLE, NS=NS)
N = T.N
RES['N'] = N
log('loaded, N =', N)

# ------------------------------------------------------------------ selection (C-level zip)
t = time.time()
ns = [n for n, (o, ty) in enumerate(zip(islice(T.oddb, N0, N), islice(T.typ, N0, N)), N0)
      if o and ty == 99]
m = len(ns)
RES['n_odd_c_deep'] = m
RES['stage_seconds']['select'] = round(time.time() - t, 1)
log('odd type-c crossings in [N0, N):', m, 'in', RES['stage_seconds']['select'], 's')

t = time.time()
taus_l = [T.tau[n] for n in ns]
lYs_l = [T.lY[n] for n in ns]
lAs_l = [T.lA[n] for n in ns]
epss_l = [T.eps[n] for n in ns]
lams_l = [a + 2 * y + 3 for a, y in zip(lAs_l, lYs_l)]
assert all(l == 3 * t + 4 + y for l, t, y in zip(lams_l, taus_l, lYs_l)), 'ENTRY identity fails'
sn_l = [n - e for n, e in zip(ns, epss_l)]          # sigma = v2(c'_W)
om_l = [clib.v2(l) for l in lams_l]
RES['stage_seconds']['cols'] = round(time.time() - t, 1)
log('columns', RES['stage_seconds']['cols'], 's')

RES['omega_dist'] = {str(k): v for k, v in sorted(Counter(om_l).items())}
RES['omega_all_odd'] = all(w % 2 == 1 for w in om_l)
RES['sigma_minus_omega_min'] = min(s - w for s, w in zip(sn_l, om_l))
RES['sigma_gt_omega_all'] = all(s > w for s, w in zip(sn_l, om_l))
RES['tau_odd_fraction'] = sum(1 for t_ in taus_l if t_ % 2) / m if m else None
RES['lY_parity'] = {str(k): v for k, v in sorted(Counter(y % 2 for y in lYs_l).items())}
RES['omega_x_tau_parity'] = {str(w): {str(p_): v for p_, v in sorted(Counter(
    t_ % 2 for i_, t_ in enumerate(taus_l) if om_l[i_] == w).items())} for w in sorted(set(om_l))}
RES['tau_min'] = min(taus_l) if m else None
RES['tau_max'] = max(taus_l) if m else None
RES['lam_max'] = max(lams_l) if m else None
log('omega dist', RES['omega_dist'])
log('omega all odd:', RES['omega_all_odd'], ' min(sigma-omega):', RES['sigma_minus_omega_min'],
    ' tau odd fraction:', RES['tau_odd_fraction'])

# ------------------------------------------------------------------ tau mod small powers
t = time.time()
tmd = {}
for k in (8, 16, 20):
    c = Counter(t_ & ((1 << k) - 1) for t_ in taus_l)
    top = sorted(c.items(), key=lambda kv: -kv[1])[:10]
    tmd['2^%d' % k] = dict(n_distinct=len(c), max_count=top[0][1] if top else 0,
                           top10=[[int(a), int(b)] for a, b in top])
RES['tau_mod'] = tmd
RES['stage_seconds']['tau_mod'] = round(time.time() - t, 1)
log('tau mod powers', {k: (v['n_distinct'], v['max_count']) for k, v in tmd.items()},
    'in', RES['stage_seconds']['tau_mod'], 's')

# ------------------------------------------------------------------ exhaustive Bad_omega
t = time.time()
omegas = sorted(set(om_l))
Bad = {}
for w in omegas:
    Bad[w] = set(x % (1 << (w + 1)) for x in clib.bad_set(T, w)) if 5 <= w <= 12 else None
RES['stage_seconds']['bad_sets'] = round(time.time() - t, 1)
RES['bad_sizes'] = {str(w): (len(Bad[w]) if Bad[w] is not None else None) for w in omegas}
RES['bad_exhaustive'] = {str(w): (5 <= w <= 12) for w in omegas}
log('Bad sets', RES['bad_sizes'], 'in', RES['stage_seconds']['bad_sets'], 's')

# ------------------------------------------------------------------ theta sets / tie classes
THETA_WINDOW = list(range(-30, 31))
WINSET = set(THETA_WINDOW)
DRIFT = lambda Lam: sorted(set([1 - b for b in range(0, Lam + 1)] +
                               [2 + b for b in range(0, max(0, Lam - 1))]))
THETA_DRIFT4 = [x for x in DRIFT(4) if x in WINSET]
THETA_DRIFT13 = [x for x in DRIFT(13) if x in WINSET]
RES['theta_window'] = THETA_WINDOW
RES['theta_drift_L4'] = THETA_DRIFT4
RES['theta_drift_L13'] = THETA_DRIFT13


def first_tie_k(w):
    n = w - 1
    if n < 0 or not T.odd(n) or T.typ[n] != 97:
        return None
    return T.tau[n] // 2


tie_k = {w: first_tie_k(w) for w in omegas if 5 <= w < N}
RES['first_chain_tie_k'] = {str(w): v for w, v in tie_k.items()}

# ------------------------------------------------------------------ main scan
t = time.time()
counts = {name: 0 for name in ('window', 'drift_L4', 'drift_L13', 'theta1')}
pairs = {name: 0 for name in ('window', 'drift_L4', 'drift_L13', 'theta1')}
hits = []
cong_hits = Counter()
cong_pairs = Counter()
cong_class = {}                       # omega -> Counter of the bad theta class mod 2^(omega-1)
exact_tested = 0
exact_bad = {}
for i in range(m):
    w = om_l[i]
    if w <= 4:
        continue                          # terminal landing: certify holds, no bad class
    tau_n = taus_l[i]
    M = 1 << (w + 1)
    base = (3 * tau_n + 3 - (1 << w)) % M
    bset = Bad[w]
    if bset is None:                      # omega > 12: decide exactly per encountered class
        bset = set()
        for th in sorted(set(THETA_WINDOW) | set(THETA_DRIFT4) | set(THETA_DRIFT13) | {1, 5, -11, 17}):
            d = (base + th) % M
            ok, st, wd, r = clib.certify(T, w, d)
            exact_tested += 1
            if not ok:
                bset.add(d)
        exact_bad[w] = sorted(bset)
    for b in bset:
        th = (b - base) % M
        if th > M // 2:
            th -= M                             # symmetric representative
        if th in WINSET:
            counts['window'] += 1
            if len(hits) < 200:
                hits.append(dict(n=ns[i], omega=w, theta=th, delta=b, tau=tau_n))
    pairs['window'] += len(THETA_WINDOW)
    if (base + 1) % M in bset:
        counts['theta1'] += 1
    pairs['theta1'] += 1
    for th in THETA_DRIFT4:
        if (base + th) % M in bset:
            counts['drift_L4'] += 1
    pairs['drift_L4'] += len(THETA_DRIFT4)
    for th in THETA_DRIFT13:
        if (base + th) % M in bset:
            counts['drift_L13'] += 1
    pairs['drift_L13'] += len(THETA_DRIFT13)
    k = tie_k.get(w)
    if k is not None:                     # odd-a omega: reduced congruence on tau
        M1 = 1 << (w - 1)
        th_hit = ((1 << (w - 2)) - 3 * k - 3 - 3 * tau_n) % M1
        if th_hit > M1 // 2:
            th_hit -= M1
        cong_pairs[w] += 1
        cc = cong_class.setdefault(w, Counter())
        cc[th_hit] += 1
        if any((base + th) % M in bset for th in THETA_DRIFT13):
            cong_hits[w] += 1
RES['stage_seconds']['scan'] = round(time.time() - t, 1)
RES['bad_counts'] = counts
RES['pairs'] = pairs
RES['density_measured'] = {k: (counts[k] / pairs[k] if pairs[k] else None) for k in counts}
RES['congruence_hits_by_omega'] = {str(k): [cong_hits[k], cong_pairs[k]] for k in sorted(cong_pairs)}
RES['bad_theta_class_counts'] = {str(k): [[int(a), int(b)] for a, b in sorted(v.items(), key=lambda kv: -kv[1])[:20]]
                                 for k, v in sorted(cong_class.items())}
RES['hits'] = hits
RES['exact_tested'] = exact_tested
RES['exact_bad_large_omega'] = {str(k): v for k, v in exact_bad.items()}
log('scan done', round(time.time() - t, 1), 's')
log('bad counts', counts, 'of pairs', pairs)
log('density', RES['density_measured'])
log('hits (first 5):', hits[:5])
log('congruence', RES['congruence_hits_by_omega'])
RES['density_theoretical'] = {str(w): (len(Bad[w]) / (1 << (w + 1)) if Bad.get(w) is not None else None)
                              for w in omegas}

# ------------------------------------------------------------------ omega=5 gateway size
i5 = [i for i in range(m) if om_l[i] == 5]
size_ok = 0
size_info = []
for i in i5[:2000]:
    tau_n = taus_l[i]
    sig = sn_l[i]
    lam_ = lams_l[i]
    ok = True
    for th in THETA_WINDOW:
        Q = 2 * th + 12 + 6 * tau_n - lam_ // 2
        if Q == 0 or abs(Q).bit_length() > sig - 1:   # |Q| >= 2^(sigma-1)
            ok = False
    size_ok += 1 if ok else 0
    if len(size_info) < 10:
        size_info.append(dict(n=ns[i], tau=tau_n, sigma=sig, lam=lam_, lY=lYs_l[i], eps=epss_l[i]))
RES['omega5'] = dict(count=len(i5), checked=len(i5[:2000]), size_ok=size_ok,
                     min_sigma=(min(sn_l[i] for i in i5) if i5 else None),
                     max_sigma=(max(sn_l[i] for i in i5) if i5 else None),
                     tau_mod16=sorted(Counter(taus_l[i] % 16 for i in i5).items()),
                     tau_mod64=sorted(Counter(taus_l[i] % 64 for i in i5).items()),
                     lY_mod8192=sorted(Counter(lYs_l[i] % 8192 for i in i5).items())[:10],
                     lam_mod64=sorted(Counter(lams_l[i] % 64 for i in i5).items()),
                     eta_mod16=sorted(Counter(epss_l[i] % 16 for i in i5).items()),
                     eps_dist=sorted(Counter(epss_l[i] for i in i5).items())[:10],
                     examples=size_info)
log('omega=5 crossings', len(i5), 'gateway size ok', size_ok, '/', len(i5[:2000]))

# ------------------------------------------------------------------ generalized gateway resolution
# At a bad landing class of an odd-a landing parameter j_u, the two-chain block has
#   x_{u+1} = Q + u_T (2^(j_T+1) - c'/2),  Q = 2 theta + 6 + 6 k + 6 tau - lambda'/2,
#   j_{u+1} = v2(Q) (< sigma-1), theta_{u+1} = theta + 6 + 3 tau + 3 tau(j_u-1) (mod 2^j2),
# and r_{u+1} = j2 + Gamma_T + 2 + eps(n) <= r_T - 1.  We verify the resolution and
# certify(j2, theta2) on every canonical bad class.
gw = dict(cases=0, unresolved=0, resolved=0, cert_ok=0, cert_fail=0, rec_ok=0,
          j2_dist={}, fail_examples=[], ok_examples=[])
for i in range(m):
    w = om_l[i]
    kk = tie_k.get(w)
    if kk is None or w < 5:
        continue
    tau_n = taus_l[i]
    sig = sn_l[i]
    lam_ = lams_l[i]
    M = 1 << (w + 1)
    base = (3 * tau_n + 3 - (1 << w)) % M
    bset = Bad.get(w)
    if bset is None:
        continue
    tau_prev = T.tau[w - 1]
    for th in sorted(set(THETA_WINDOW) | set(THETA_DRIFT13)):
        if (base + th) % M not in bset:
            continue
        gw['cases'] += 1
        Q = 2 * th + 6 + 6 * kk + 6 * tau_n - lam_ // 2
        if Q == 0:
            gw['unresolved'] += 1
            continue
        j2 = clib.v2(abs(Q))
        if j2 >= sig - 1:
            gw['unresolved'] += 1
            continue
        gw['resolved'] += 1
        gw['j2_dist'][str(j2)] = gw['j2_dist'].get(str(j2), 0) + 1
        if j2 + 2 + epss_l[i] <= ns[i] + 1:   # j2+2+eps <= j_T = n+1
            gw['rec_ok'] += 1
        # class of chain u+1: mod 2^j2 it is theta+6+3tau+3tau(j_u-1); mod 2^(j2+1) it is
        # (theta+6+3tau+3tau(j_u-1) - Q) because x_{u+1} == Q mod 2^(sigma-1) and j2+1 <= sigma-1.
        th2 = (th + 6 + 3 * tau_n + 3 * tau_prev - Q) % (1 << (j2 + 1))
        ok = True if j2 <= 4 else clib.certify(T, j2, th2)[0]
        if ok:
            gw['cert_ok'] += 1
            if len(gw['ok_examples']) < 5:
                gw['ok_examples'].append(dict(n=ns[i], omega=w, theta=th, j2=j2, theta2=th2))
        else:
            gw['cert_fail'] += 1
            if len(gw['fail_examples']) < 20:
                gw['fail_examples'].append(dict(n=ns[i], omega=w, theta=th, j2=j2, theta2=th2,
                                                tau=tau_n, lam=lam_))
RES['gateway_resolution'] = gw
log('gateway resolution', {k: v for k, v in gw.items() if k not in ('ok_examples', 'fail_examples')})

# ------------------------------------------------------------------ exact spot checks
t = time.time()
odd_c_small = [n for n in range(6, min(NS, N)) if T.odd(n) and T.typ[n] == 99]
spot = []
for n in odd_c_small[:200]:
    w = clib.v2(T.lam(n))
    cW = T.cW.get(n)
    if cW is None:
        continue
    for th in (1, 0, -1, 2, -2, 5):
        u = (1 << 50) + 12345
        x = (1 << (n + 1)) * u
        xp = cW * u + T.lam(n)
        Thp = x + th + 3 + 3 * T.tau[n]
        jp = clib.v2(xp)
        M = 1 << (jp + 1)
        ok = (jp == w) and ((Thp - xp) % M == (th + 3 * T.tau[n] + 3 - (1 << jp)) % M)
        spot.append(ok)
RES['class_formula_exact_spot'] = dict(n=len(spot), all_ok=bool(all(spot)))
log('class formula spot', len(spot), all(spot))

import random
random.seed(12345)
idx = random.sample(range(m), min(300, m))
agree = 0
tested = 0
for i in idx:
    w = om_l[i]
    if w < 5 or Bad.get(w) is None:
        continue
    M = 1 << (w + 1)
    base = (3 * taus_l[i] + 3 - (1 << w)) % M
    for th in (1, 0, -1, 2, -2, 3, -3, 5, 17, -11):
        d = (base + th) % M
        ok, st, wd, r = clib.certify(T, w, d)
        tested += 1
        if ok == (d not in Bad[w]):
            agree += 1
RES['certify_vs_bad_membership'] = dict(tested=tested, agree=agree)
log('certify vs Bad membership', tested, agree)

RES['stage_seconds']['spot'] = round(time.time() - t, 1)
RES['seconds_total'] = round(time.time() - T0, 1)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(RES, f, indent=1)
log('written', OUT, 'total', RES['seconds_total'], 's')
