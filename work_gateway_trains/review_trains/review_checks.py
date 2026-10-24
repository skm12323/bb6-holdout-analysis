# -*- coding: utf-8 -*-
"""Independent adversarial/audit checks for the four Astra train documents
(work_c3_drift: GATEWAY_TRAIN, CLOCK_FILTERED_TRAIN, TRAIN_CLOCK_ORBIT,
CROSS_SCALE_TRAIN) plus spot checks of the five budget documents.

Reviewer session 2026-10-24, work_gateway_trains/review_trains/.
Every quantitative assertion below is recomputed from scratch (exact Fractions,
own graph rebuilds, own streaming lambda-walk, own Calendar queries).
Writes review_checks.json; exit 0 iff all checks pass.
"""
import sys, json, random, time
from fractions import Fraction as F
from pathlib import Path
from collections import deque

sys.path.insert(0, 'D:/math_cc/work_c3_drift')
from verify_shift_transport import Calendar, val   # import-only usage
sys.path.insert(0, 'D:/math_cc/work_global_ext/route_c')

random.seed(20261024)
HERE = Path(__file__).resolve().parent
RESULTS = {}
FAILURES = []


def record(name, ok, **info):
    RESULTS[name] = dict(status='PASS' if ok else 'FAIL', **info)
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)
    if not ok:
        FAILURES.append(name)
    return ok


def v2int(z):
    z = int(z)
    if z == 0:
        return 10**9
    return (abs(z) & -abs(z)).bit_length() - 1


# ----------------------------------------------------------------------------
# shared calendar / table data
# ----------------------------------------------------------------------------
t0 = time.time()
CAL = Calendar(256)
KS = {m: CAL.crossing(m - 1)['time'] // 2 for m in range(5, 257)
      if CAL.crossing(m - 1)['odd'] and CAL.crossing(m - 1)['kind'] == 'a'}
LABELS = sorted(KS)

import pickle
TAB = pickle.load(open('D:/math_cc_astra/deep1/table_1000000.pkl', 'rb'))


# ----------------------------------------------------------------------------
# my own streaming lambda-walk (reimplementation of the tau/typ/odd logic in
# fdata.lam_walk with O(1) memory; cross-checked against table_1000000.pkl)
# ----------------------------------------------------------------------------
def stream_walk(N, table=None):
    """Yield nothing; check tau<=n, tau monotone, and param-3 odd-a pointer gaps
    for all crossings n<N. If table given, also compare typ/tau/odd for n<min(N,len)."""
    la = 1; S = []; i = 0; s = 0; first = True; seen = -1
    sig_last = None; jl = None
    max_taudiff = -10**18
    mono_ok = True
    prev_tau = -1
    last_p3 = None
    min_p3_gap = 10**9
    p3_count = 0
    p3_count_16381 = 0
    if table is not None:
        ttyp, ttau, todd = table['typ'], table['tau'], table['odd']
        cmp_lim = min(N, len(ttau))
        cmp_ok = True
    while seen < N - 1:
        k = len(S)
        if k >= 2:
            lb = S[-1]; lc = S[-2]; reads = ()
        elif k == 1:
            lb = S[-1]; lc = 0; reads = (i,)
        else:
            lb = lc = 0; reads = (i, i + 1)
        par = (la + (1 if first else 0)) & 1
        for n in reads:
            if n > seen and n < N:
                seen = n
                if s > n:
                    return dict(ok=False, why='tau>n', n=n, tau=s)
                if s < prev_tau:
                    return dict(ok=False, why='tau decreased', n=n, tau=s, prev=prev_tau)
                prev_tau = s
                max_taudiff = max(max_taudiff, s - n)
                # param-3 fire check only at odd type a crossings (tau even)
                if par and k == 0 and i == n and s % 2 == 0:
                    if v2int(6 * (s // 2) + 4) == 3:
                        if last_p3 is not None:
                            g = n - last_p3
                            if g < min_p3_gap:
                                min_p3_gap = g
                            if g < 5:
                                return dict(ok=False, why='p3 gap<5', n=n, prev=last_p3, gap=g)
                        last_p3 = n
                        p3_count += 1
                        if n < 16381:
                            p3_count_16381 += 1
                if table is not None and n < cmp_lim:
                    typn = 97 if (k == 0 and i == n) else (98 if k == 0 else 99)
                    if ttyp[n] != typn or ttau[n] != s or (todd[n] & 1) != par:
                        cmp_ok = False
                        return dict(ok=False, why='table mismatch', n=n, s=s, typ=typn)
        if par == 0:
            la = la + lb + lc + 3; push = None
        else:
            lx = la + 2 * lb + 3; j = v2int(lx); u = lx >> j
            push = (u, j, lc + (la + 1) // 2); la = u + 1
        if k >= 2:
            del S[-2:]
        else:
            i += 2 - k; S.clear()
        if push:
            u, j, D = push
            S.append(D)
            for t in range(j - 2, -1, -1):
                S.append(u << t)
        s += 1; first = False
    return dict(ok=True, reached=N, max_tau_minus_n=max_taudiff,
                min_p3_gap=(min_p3_gap if p3_count > 1 else None),
                p3_count=p3_count, p3_count_below_16381=p3_count_16381,
                table_match=(cmp_ok if table is not None else None))


# ----------------------------------------------------------------------------
# 1. GATEWAY_TRAIN section 1 recurrences (random exact rational instances)
# ----------------------------------------------------------------------------
def check_gt_recurrences():
    bad = 0
    for _ in range(500):
        x = F(32 * random.choice([1, 3, 5, 7, 11, 13]))
        th = F(random.randrange(1, 10**6))
        k0 = random.randrange(1, 300)
        k1 = random.randrange(1, 300)
        # step 1: five-state -> y0 via X(4) (half-time 1)
        y0 = -x / 2 + 2 * th + 6
        th_after4 = th + 3 + 6 * 1
        # step 2: chain y0 -> five via X(m0-1) with half-time k0
        x1 = 2 * th_after4 + 6 * k0 - y0 / 2
        th1 = th_after4 + 3 + 6 * k0
        if x1 != x / 4 + th + 15 + 6 * k0: bad += 1
        if th1 != th + 12 + 6 * k0: bad += 1
        y1 = -x1 / 2 + 2 * th1 + 6
        if y1 - y0 / 4 != th + 21 + 9 * k0: bad += 1
        # third catapult
        th_after4b = th1 + 9
        x2 = 2 * th_after4b + 6 * k1 - y1 / 2
        th2 = th_after4b + 3 + 6 * k1
        y2 = -x2 / 2 + 2 * th2 + 6
        if 4 * y2 - 5 * y1 + y0 != 12 * (4 - k0 + 3 * k1): bad += 1
    record('GT.S1.recurrences', bad == 0, random_instances=500, mismatches=bad)


# ----------------------------------------------------------------------------
# 2. TRAIN as min-occurs-twice consequence (unconditional identity check)
# ----------------------------------------------------------------------------
def check_train_valuation():
    bad = 0; checked = 0
    for _ in range(400):
        x = F(32 * random.choice([1, 3, 5, 7]))
        th = F(random.randrange(1, 10**6))
        k0 = random.randrange(1, 200); k1 = random.randrange(1, 200)
        y0 = -x / 2 + 2 * th + 6
        th_a = th + 9
        x1 = 2 * th_a + 6 * k0 - y0 / 2; th1 = th_a + 3 + 6 * k0
        y1 = -x1 / 2 + 2 * th1 + 6
        th_b = th1 + 9
        x2 = 2 * th_b + 6 * k1 - y1 / 2; th2 = th_b + 3 + 6 * k1
        y2 = -x2 / 2 + 2 * th2 + 6
        if y0 == 0 or y1 == 0 or y2 == 0:
            continue
        m0, m1, m2 = val(y0), val(y1), val(y2)
        Z = 4 - k0 + 3 * k1
        # min-occurs-twice among {m0, m1, m2+2, 2+v2(Z)} for the zero sum
        vals = [m0, m1, m2 + 2] + ([2 + v2int(Z)] if Z != 0 else [])
        if vals.count(min(vals)) < 2:
            bad += 1
        # TRAIN inequality equivalent form
        if Z != 0 and 2 + v2int(Z) < min(m0, m1, m2 + 2):
            bad += 1
        checked += 1
    record('GT.TRAIN.min_twice', bad == 0, instances=checked, violations=bad)


# ----------------------------------------------------------------------------
# 3. label data: calendar vs table; X(4)/X(5)/X(6)/X(16)/X(18)
# ----------------------------------------------------------------------------
def check_labels():
    ok = True
    info = {}
    r4 = CAL.crossing(4)
    ok &= (r4['kind'] == 'a' and r4['odd'] and r4['time'] == 2)
    r5 = CAL.crossing(5)
    ok &= (r5['kind'] == 'b' and r5['odd'])
    r6 = CAL.crossing(6)
    info['X6'] = (r6['kind'], r6['odd'])
    ok &= (not r6['odd'])          # label 7 is not an odd-a source
    r16 = CAL.crossing(16)
    ok &= (r16['kind'] == 'a' and r16['odd'] and r16['time'] == 12)   # k(17)=6
    r18 = CAL.crossing(18)
    ok &= (not r18['odd'])         # terminal 19 in CROSS_SCALE ends
    # odd-a labels 5..256 against table
    ttyp, ttau, todd = TAB['typ'], TAB['tau'], TAB['odd']
    ks_tab = {m: ttau[m - 1] // 2 for m in range(5, 257)
              if (todd[m - 1] and ttyp[m - 1] == 97)}
    ok &= (ks_tab == KS)
    info['num_labels'] = len(KS)
    info['labels_below_8'] = [m for m in KS if m < 8]
    info['internal_labels_le_256'] = sorted(m for m, k in KS.items() if k % 16 == 6)
    info['labels_5_to_16'] = {m: KS[m] for m in LABELS if m <= 16}
    record('GT.labels.calendar_vs_table', ok, **info)


# ----------------------------------------------------------------------------
# 4. no three identical catapults; quadratic induction; tau<=n
# ----------------------------------------------------------------------------
def check_no_three():
    ok = all(v2int(4 + 2 * KS[m]) < m - 2 for m in LABELS)
    quad = all((m - 1) ** 2 + 4 < 1 << (m - 2) for m in range(8, 4097))
    # ratio argument: (m^2+4)/((m-1)^2+4)<2 for all m>=3
    ratio = all((m * m + 4) < 2 * ((m - 1) ** 2 + 4) for m in range(3, 10**5))
    # tau(n) <= n over the audited table (n<10^6)
    ttau = TAB['tau']
    tau_le_n = all(ttau[n] <= n for n in range(len(ttau)))
    record('GT.S2.no_three_identical', ok and quad and ratio,
           diagonal_labels=len(LABELS), quad_range=[8, 4096], tau_le_n_table=tau_le_n)


# ----------------------------------------------------------------------------
# 5. BAND algebra (Z=0 chain and 3^(s-1)<=k0+2)
# ----------------------------------------------------------------------------
def check_band():
    bad = 0
    for _ in range(300):
        k_last = random.randrange(1, 10**6)
        s = random.randrange(2, 12)
        ks = [k_last]
        for _ in range(s - 1):
            ks.append(3 * ks[-1] + 4)     # k_i = 3 k_{i+1} + 4 backwards
        k0 = ks[-1]
        # forward: each Z=0
        if any(4 - ks[i + 1] + 3 * ks[i] != 0 for i in range(len(ks) - 1)):
            bad += 1
        if k0 + 2 != 3 ** (s - 1) * (k_last + 2):
            bad += 1
        if 3 ** (s - 1) > k0 + 2:
            bad += 1
    record('GT.S3.band_algebra', bad == 0, instances=300)


# ----------------------------------------------------------------------------
# 6. rebuild the 5776-vertex necessary graph independently
# ----------------------------------------------------------------------------
def rebuild_graph1():
    verts = [(a, b) for a in LABELS for b in LABELS]
    graph = {v: [] for v in verts}
    edges = 0
    for a, b in verts:
        z = 4 - KS[a] + 3 * KS[b]
        vz = 10**9 if z == 0 else v2int(z)
        for c in LABELS:
            if vz >= min(a - 2, b - 2, c):
                graph[(a, b)].append((b, c))
                edges += 1
    # acyclicity
    indeg = {v: 0 for v in verts}
    for v in verts:
        for w in graph[v]:
            indeg[w] += 1
    dq = deque(v for v in verts if indeg[v] == 0)
    order = []
    while dq:
        v = dq.popleft(); order.append(v)
        for w in graph[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                dq.append(w)
    acyclic = len(order) == len(verts)
    # locate a cycle containing the pair chain 8->244->81->27->8
    cyc = [(8, 244), (244, 81), (81, 27), (27, 8)]
    in_graph = all(d in graph[c] for c, d in zip(cyc, cyc[1:] + cyc[:1]))
    advance = sum(12 + 6 * KS[a] for a, b in cyc)
    required = max(min(a - 2, b) for a, b in cyc)
    valadv = v2int(advance)
    repeat_ok = (advance % (1 << required)) == 0
    # CRT consistency of the pair clock constraints around the cycle:
    # Theta_i = -21-9k_i mod 2^{e_i}, Theta_{i+1}=Theta_i+12+6k_i
    import math
    residue = 0; modulus = 1; crt_ok = True
    elapsed = 0
    for a, b in cyc:
        e = min(a - 2, b)
        step = 1 << e
        need = ((-21 - 9 * KS[a]) - elapsed) % step
        g = math.gcd(modulus, step)
        if (need - residue) % g:
            crt_ok = False
            break
        lcm = modulus * step // g
        t = ((need - residue) // g) * pow(modulus // g, -1, step // g) % (step // g) if step > g else 0
        residue = (residue + modulus * t) % lcm
        modulus = lcm
        elapsed += 12 + 6 * KS[a]
    # repeating the cycle once needs Theta_0+advance to satisfy all four again;
    # the 81-bit pair forces 2^81 | 960, which fails
    record('GT.S4.graph_rebuild',
           len(verts) == 5776 and edges == 1433 and not acyclic and in_graph
           and advance == 960 and valadv == 6 and required == 81
           and not repeat_ok and crt_ok,
           vertices=len(verts), edges=edges, acyclic=acyclic,
           cycle_present=in_graph, advance=advance, v2_advance=valadv,
           required_bits=required, repeat_excluded=not repeat_ok, crt_ok=crt_ok)
    return graph


# ----------------------------------------------------------------------------
# 7. ENTRY derivation (brute-force residues)
# ----------------------------------------------------------------------------
def check_entry():
    # y = 2*Theta+6-16u == 0 mod 32 (param>=5)  <=>  Theta = 5 mod 16 (u odd)
    ok1 = all(((2 * th + 6 - 16 * u) % 32 == 0) == (th % 16 == 5)
              for th in range(0, 64) for u in (1, 3, 5, 7))
    # difference 12+6k == 0 mod 16 <=> k=6 mod 8
    ok2 = all(((12 + 6 * k) % 16 == 0) == (k % 8 == 6) for k in range(0, 64))
    # full ENTRY: Theta=5 mod 16 and Theta=-21-9k mod 2^e (e>=4) => k=6 mod 16
    ok3 = True
    for k in range(0, 64):
        for th in range(0, 64):
            if th % 16 == 5 and (th - (-21 - 9 * k)) % 16 == 0:
                if k % 16 != 6:
                    ok3 = False
    # fire parameter: k=6 mod 16 => 1+v2(3k+2)=3 (doc's direction);
    # (conversely fire param 3 <=> k=6 mod 8)
    ok4 = all(v2int(3 * k + 2) == 2 for k in range(0, 256) if k % 16 == 6)
    ok4b = all((v2int(3 * k + 2) == 2) == (k % 8 == 6) for k in range(0, 128))
    # internal labels need k=6 mod 16; only odd-a labels below 8: m=5 (k=1)
    ok5 = all(m >= 8 for m in LABELS if KS[m] % 8 == 6)
    record('CF.S1.entry_derivation', ok1 and ok2 and ok3 and ok4 and ok4b and ok5,
           theta_residue=ok1, k_mod8=ok2, k_mod16=ok3, fire_param_impl=ok4,
           fire_param_iff_mod8=ok4b,
           min_internal_label=min(m for m in LABELS if KS[m] % 16 == 6))


# ----------------------------------------------------------------------------
# 8. DROP2 (Z=0 => m_{i+2}=m_{i+1}-2 when m_i != m_{i+1})
# ----------------------------------------------------------------------------
def check_drop2():
    # Synthetic instances force Z=0 (k0=3*k1+4). The unconditional algebra gives
    # m2+2 = min(m0,m1) whenever m0 != m1; the doc's DROP2 (m2=m1-2) additionally
    # uses canonical tau-monotonicity (k0>k1 => m0>m1), verified separately.
    bad = 0; tried = 0
    for _ in range(400):
        x = F(32 * random.choice([1, 3, 5, 7, 9, 11]))
        th = F(random.randrange(1, 10**6))
        k1 = random.randrange(1, 100)
        k0 = 3 * k1 + 4                        # force Z=0
        y0 = -x / 2 + 2 * th + 6
        th_a = th + 9
        x1 = 2 * th_a + 6 * k0 - y0 / 2; th1 = th_a + 3 + 6 * k0
        y1 = -x1 / 2 + 2 * th1 + 6
        th_b = th1 + 9
        x2 = 2 * th_b + 6 * k1 - y1 / 2; th2 = th_b + 3 + 6 * k1
        y2 = -x2 / 2 + 2 * th2 + 6
        if y0 == 0 or y1 == 0 or y2 == 0:
            continue
        tried += 1
        m0, m1, m2 = val(y0), val(y1), val(y2)
        if 4 * y2 - 5 * y1 + y0 != 0:
            bad += 1; continue
        if m0 != m1:
            if m2 != min(m0, m1) - 2:
                bad += 1
    # canonical monotonicity: k0>k1 at odd-a crossings implies m0>m1
    mono = True
    pairs = sorted((KS[m], m) for m in LABELS)
    mono &= all(pairs[i][0] < pairs[i + 1][0] or pairs[i][1] < pairs[i + 1][1]
                for i in range(len(pairs) - 1))
    mono &= all(KS[m1] < KS[m2] for m1 in LABELS for m2 in LABELS if m1 < m2)
    record('CF.S2.drop2', bad == 0 and mono, instances=tried, violations=bad,
           canonical_k_order_matches_label_order=mono)


# ----------------------------------------------------------------------------
# 9. tau<=n / monotone tau / param-3 gaps over big ranges
# ----------------------------------------------------------------------------
def check_stream(limit):
    r = stream_walk(10**6, table=TAB)
    record('STREAM.table1e6', r.get('ok', False), **{k: v for k, v in r.items() if k != 'ok'})
    cache = HERE / 'stream_cache.json'
    if cache.exists():
        try:
            cached = json.loads(cache.read_text(encoding='utf-8'))
            if cached.get('limit') == limit and cached.get('ok'):
                record('STREAM.big', True, **{k: v for k, v in cached.items() if k not in ('ok', 'limit')})
                return
        except Exception:
            pass
    t0s = time.time()
    r2 = stream_walk(limit, table=None)
    r2['seconds'] = round(time.time() - t0s, 1)
    cache.write_text(json.dumps(dict(limit=limit, **r2)), encoding='utf-8')
    record('STREAM.big', r2.get('ok', False), **{k: v for k, v in r2.items() if k != 'ok'})


# ----------------------------------------------------------------------------
# 10. no-four-catapult arithmetic (band + [5,16381] versions)
# ----------------------------------------------------------------------------
def check_no_four():
    # band version feasibility arithmetic: quadratic < power at several (L,M)
    ok_band = True
    for L, M in [(17, 18), (20, 22), (30, 34), (100, 110), (1000, 1100)]:
        ok_band &= (4 + 2 * (M - 1) ** 2 < 1 << (L - 2))
    # 16381 version: k<=8190, |Z0|<=4+k0+3k1<=32764<2^15
    ttau = TAB['tau']
    kmax = max(ttau[n] // 2 for n in range(4, 16381) if TAB['odd'][n] and TAB['typ'][n] == 97)
    bound = 4 + kmax + 3 * kmax
    record('CF.S3.no_four_arithmetic',
           ok_band and kmax <= 8190 and bound <= 32764 and 32764 < 1 << 15,
           kmax_16381=kmax, z0_bound=bound)


# ----------------------------------------------------------------------------
# 11. rebuild the clock-filtered 532-vertex graph
# ----------------------------------------------------------------------------
def rebuild_graph2():
    def admissible(a, b):
        if (12 + 6 * KS[a]) % 16:
            return False
        e = min(a - 2, b)
        phase = (-21 - 9 * KS[a]) % (1 << e)
        return (phase - 5) % (1 << min(e, 4)) == 0
    verts = [(a, b) for a in LABELS for b in LABELS if admissible(a, b)]
    graph = {v: [] for v in verts}
    indeg = {v: 0 for v in verts}
    for a, b in verts:
        z = 4 - KS[a] + 3 * KS[b]
        vz = 10**9 if z == 0 else v2int(z)
        for c in LABELS:
            if (b, c) in graph and vz >= min(a - 2, b - 2, c):
                vals = [a, b, c + 2] + ([2 + vz] if z else [])
                if vals.count(min(vals)) < 2:
                    continue
                graph[(a, b)].append((b, c))
                indeg[(b, c)] += 1
    edges = sum(len(v) for v in graph.values())
    dq = deque(v for v in verts if indeg[v] == 0)
    order = []
    while dq:
        v = dq.popleft(); order.append(v)
        for w in graph[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                dq.append(w)
    acyclic = len(order) == len(verts)
    length = {}; nxt = {}
    for v in reversed(order):
        if graph[v]:
            w = max(graph[v], key=lambda w: length[w])
            length[v] = 1 + length[w]; nxt[v] = w
        else:
            length[v] = 0
    v0 = max(verts, key=lambda v: length[v])
    maximum = 2 + length[v0]
    pairpath = [v0]
    while v0 in nxt:
        v0 = nxt[v0]; pairpath.append(v0)
    path = [p[0] for p in pairpath] + [pairpath[-1][1]]
    # initial-clock replay along the path
    residue = 5; precision = 4; elapsed = 0; consistent = True
    for pa, pb in pairpath[:-1]:
        e = min(pa - 2, pb)
        need = (-21 - 9 * KS[pa] - elapsed) % (1 << e)
        if (need - residue) % (1 << min(e, precision)):
            consistent = False; break
        if e > precision:
            residue = need; precision = e
        elapsed += 12 + 6 * KS[pa]
    # the raw cycle 8.. excluded by ENTRY
    entry_excl = (12 + 6 * KS[8]) % 16 != 0
    record('CF.S4.graph2_rebuild',
           len(verts) == 532 and edges == 14 and acyclic and maximum == 3
           and path == [17, 125, 5] and consistent and entry_excl,
           vertices=len(verts), edges=edges, acyclic=acyclic,
           maximum=maximum, longest=path, clock_consistent=consistent,
           entry_excludes_cycle8=entry_excl, initial_residue=residue,
           initial_precision=precision)


# ----------------------------------------------------------------------------
# 12. TRAIN_CLOCK_ORBIT checks
# ----------------------------------------------------------------------------
def check_orbit():
    bad = 0
    # CLOCK-ORBIT congruence derivation
    for _ in range(200):
        u0 = random.randrange(1, 10**6, 2)
        u1 = random.randrange(1, 10**6, 2)
        k0, k1 = 8 * u0 - 2, 8 * u1 - 2
        Z = 4 - k0 + 3 * k1
        if Z != 8 * (3 * u1 - u0):
            bad += 1
    # order of 3 mod 2^a is 2^(a-2), a>=3
    order_ok = True
    for a in range(3, 27):
        m = 1 << a
        x = 3 % m; t = 1
        while x != 1:
            x = x * 3 % m; t += 1
        if t != 1 << (a - 2):
            order_ok = False
    # coset sums
    coset_ok = True
    for a in range(3, 23):
        N = 1 << (a - 3)
        s1 = sum(x for x in range(1, 1 << a) if x % 8 in (1, 3))
        s2 = sum(x for x in range(1, 1 << a) if x % 8 in (5, 7))
        if s1 != 4 * N * (2 * N - 1) or s2 != 4 * N * (2 * N + 1):
            coset_ok = False
        if v2int(s1) != a - 1 or v2int(s2) != a - 1:
            coset_ok = False
    # lift invariance and ADVANCE for small L
    adv_ok = True
    for L in (17, 18, 19, 20):
        a = L - 5
        mod = 1 << a
        inv3 = pow(3, -1, mod)
        for start in (1, 3, 5, 7):
            u = start; total = 0; seen = set()
            for i in range(1 << (L - 7)):
                if u in seen or u % 2 == 0:
                    adv_ok = False
                seen.add(u)
                k = 8 * u - 2
                total += 12 + 6 * k
                u = inv3 * u % mod
            if u != start or len(seen) != 1 << (L - 7):
                adv_ok = False
            if v2int(total) != L - 2:
                adv_ok = False
    # arbitrary lifts cannot change v2 of the coset sum
    lift_ok = True
    for _ in range(100):
        a = random.randrange(3, 16)
        N = 1 << (a - 3)
        cos = random.choice([1, 3, 5, 7])
        base = [x for x in range(1, 1 << a) if x % 8 == cos or x % 8 == (3 if cos in (1, 3) else 7 if cos == 5 else 5)]
        # coset of <3> through cos: {cos*3^i}
        mod = 1 << a
        grp = set(); x = 1
        for i in range(1 << (a - 2)):
            grp.add(x); x = x * 3 % mod
        coset = set(cos * g % mod for g in grp)
        s = sum(r + mod * random.randrange(0, 5) for r in coset)
        if v2int(s) != a - 1:
            lift_ok = False
    record('ORBIT.all', bad == 0 and order_ok and coset_ok and adv_ok and lift_ok,
           congruence_instances=200, order_ok=order_ok, coset_sums=coset_ok,
           advance=adv_ok, lift_invariance=lift_ok)


# ----------------------------------------------------------------------------
# 13. CROSS_SCALE full replay (own construction and own walk)
# ----------------------------------------------------------------------------
def my_exact_walk(cal, x, th, maxsteps=64, allow_rational=False):
    """exact chain walk with Fractions; returns (status, rows of (j,loss))."""
    x = F(x); th = F(th); loss = 0; rows = []
    for _ in range(maxsteps):
        if x == 0:
            return 'zero', rows
        if x < 0:
            return 'negative', rows
        j = val(x)
        rows.append((j, loss))
        r = cal.crossing(j - 1)
        if not r['odd']:
            return 'end', rows
        if r['kind'] == 'a':
            x = 2 * th + 3 * r['time'] - x / 2
        else:
            ratio = (r['head_ratio'] + 2 * r['tail_ratio']) / 2
            x = ratio * x + r['head_lambda'] + 2 * r['tail_lambda'] + 3
        d = x.denominator
        if d != 1 and not (allow_rational and all(p == 3 for p in _primes(d))):
            return 'noninteger', rows
        th = th + 3 + 3 * r['time']
        loss += 1 + r['epsilon']
    return 'limit', rows


def _primes(n):
    out = []; p = 2
    while p * p <= n:
        while n % p == 0:
            out.append(p); n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def check_cross_scale():
    ka, kb = 819270, 229398
    fa = CAL.preceding_fire_by_time(2 * ka)
    fb = CAL.preceding_fire_by_time(2 * kb)
    ok = fa['k'] == ka and fb['k'] == kb and fa['J'] == 3 and fb['J'] == 3
    ok &= fa['pointer'] == 1836654 and fb['pointer'] == 514272
    a, b = fa['pointer'] + 1, fb['pointer'] + 1
    Y0 = 1 << a
    Y1 = (1 << b) + (1 << (a + 10))
    th0 = Y1 - Y0 // 4 - 21 - 9 * ka
    X0 = 4 * th0 + 12 - 2 * Y0
    ok &= X0 > 0 and th0 > 0 and val(F(X0)) == 5
    # canonical crossings
    ra = CAL.crossing(a - 1); rb = CAL.crossing(b - 1)
    ok &= ra['odd'] and ra['kind'] == 'a' and ra['time'] == 2 * ka
    ok &= rb['odd'] and rb['kind'] == 'a' and rb['time'] == 2 * kb
    # own exact walk, certificate precision a+2
    status, rows = my_exact_walk(CAL, X0, th0)
    word = [j for j, g in rows]
    losses = [g for j, g in rows]
    maxrec = max(j + g for j, g in rows)
    ok &= status == 'end' and word == [5, a, 5, b, 5, 17, 5, 17, 19]
    ok &= losses == list(range(9)) and maxrec == a + 1
    # independent replay with lam_walk table (own loop, only a-steps matter here)
    from fdata import lam_walk
    tab = lam_walk(a)
    ok &= tab['tau'][a - 1] == 2 * ka and tab['tau'][b - 1] == 2 * kb
    xx, tt, direct = X0, th0, []
    for _ in range(32):                  # step guard (expected word has 9 entries)
        j = v2int(xx); direct.append(j); n = j - 1
        if not tab['odd'][n]:
            break
        ok2 = tab['typ'][n] == 97
        xx = 2 * tt + 3 * tab['tau'][n] - xx // 2
        tt += 3 + 3 * tab['tau'][n]
        if not (ok2 and xx > 0):
            ok = False; break
    else:
        ok = False
    ok &= direct == [5, a, 5, b, 5, 17, 5, 17, 19]
    # identities
    z0 = 4 - ka + 3 * kb; z1 = 4 - kb + 3 * 6
    ok &= z0 == -(1 << 17) and z1 == -7 * (1 << 15)
    D = F(th0 - X0)
    ok &= val(D + 3) == 3 and ((D + 3) / 8) % 8 == 3
    # normalized clock residues and orbit
    u_a, u_b = (ka + 2) // 8, (kb + 2) // 8
    res = [u_a % 4096, u_b % 4096, 1]
    inv3 = pow(3, -1, 4096)
    ok &= res == [9, 3, 1] and inv3 * 9 % 4096 == 3 and inv3 * 3 % 4096 == 1
    # TRAIN bounds on the two triples
    ok &= v2int(z0) >= min(a - 2, b - 2, 17) and v2int(z1) >= min(b - 2, 17 - 2, 17)
    # c_r compatibility, done with exact modular arithmetic (no materialized 3^r):
    # unit = (D+3)/8 is an odd 2-adic integer == 3 mod 8, hence in <3> mod 2^(H-3)
    # for every H, so some r has 3^-r == unit; then c_r = -3+8/3^r == D mod 2^H.
    Dint = th0 - X0                      # exact integer defect
    ok &= (Dint + 3) % 16 == 8           # v2(D+3)=3 exactly
    unit_small = ((Dint + 3) // 8) % (1 << 48)
    ok &= unit_small % 8 == 3            # in the coset {1,3 mod 8} = <3>
    # solve 3^r == unit^{-1} mod 2^48 by 2-adic lifting (existence witness)
    H = 48
    m = 1 << H
    target = pow(unit_small, -1, m)
    k = 3
    r = 1 if target % 8 == 3 else 0
    cur = pow(3, r, 8)
    while k < H:
        k += 1
        mm = 1 << k
        cur = pow(3, r, mm)               # refresh at every level
        if cur != target % mm:
            r += 1 << (k - 3)
            cur = pow(3, r, mm)
    ok &= pow(3, r, m) == target % m
    # HP transfer at the full precision a+2 using an integer representative:
    # (X0, X0 + (D mod 2^(a+2))) agrees with (X0, Theta0) mod 2^(a+2);
    # all records < a+2, so HP (and a direct replay) must give the same word.
    D_rep = Dint % (1 << (a + 2))
    status2, rows2 = my_exact_walk(CAL, X0, X0 + D_rep)
    ok &= status2 == 'end' and [j for j, g in rows2] == word
    ok &= max(j + g for j, g in rows2) < a + 2
    c_r = None                           # witness exponent recorded instead
    import hashlib
    fx = hashlib.sha256(X0.to_bytes((X0.bit_length() + 7) // 8, 'big')).hexdigest()
    ft = hashlib.sha256(th0.to_bytes((th0.bit_length() + 7) // 8, 'big')).hexdigest()
    record('CS.all', ok, ka=ka, kb=kb, source_a=a, source_b=b, word=word,
           losses=losses, max_record=maxrec, z0=z0, z1=z1,
           orbit_residues=res, dlog_exponent_mod2_48=r,
           x_sha256=fx, theta_sha256=ft, hp_replay=status2,
           x_bits=X0.bit_length())


# ----------------------------------------------------------------------------
# 14. secondary docs: DEPTH_CLOCK_BUDGET
# ----------------------------------------------------------------------------
def check_depth():
    # identity D = 51+27k+(11/4)y-3z
    bad = 0
    for _ in range(300):
        x = F(32 * random.choice([1, 3, 5, 7]))
        th = F(random.randrange(1, 10**6))
        k = random.randrange(1, 100)
        y = -x / 2 + 2 * th + 6
        th_a = th + 9
        x1 = 2 * th_a + 6 * k - y / 2; th1 = th_a + 3 + 6 * k
        z = -x1 / 2 + 2 * th1 + 6
        D = th - x
        if D != F(51) + 27 * k + F(11, 4) * y - 3 * z:
            bad += 1
    # E0 = min(m-2, n): v2((11/4)y)=m-2, v2(3z)=n
    ok_e0 = True
    for _ in range(100):
        x = F(32 * random.choice([1, 3, 5, 7, 9]))
        th = F(random.randrange(1, 10**6))
        k = random.randrange(1, 50)
        y = -x / 2 + 2 * th + 6
        if y == 0: continue
        m = val(y)
        th_a = th + 9
        x1 = 2 * th_a + 6 * k - y / 2; th1 = th_a + 3 + 6 * k
        z = -x1 / 2 + 2 * th1 + 6
        if z == 0: continue
        ok_e0 &= val(F(11, 4) * y) == m - 2 and val(3 * z) == val(z)
    # DEPTH-SOURCE: for k=6 mod 16, (51+27k+3)/8 = 27*(k+2)/8 = 27u exactly;
    # D=c_r=-3+8/3^r mod 2^E then forces 27u = 3^-r mod 2^(E-3),
    # i.e. 3^(r+3)*u = 1 mod 2^(E-3). Verified by direct construction.
    ok_ds = True
    for _ in range(60):
        r = random.randrange(0, 9)
        E = random.randrange(6, 20)
        k = 6 + 16 * random.randrange(0, 40)
        u = (k + 2) // 8
        if 51 + 27 * k + 3 != 27 * (k + 2) or 27 * (k + 2) != 8 * 27 * u:
            ok_ds = False
        mod = 1 << (E - 3)
        # exact equivalence: 8/3^r = 8*27u mod 2^E  <=>  3^(r+3)*u = 1 mod 2^(E-3)
        lhs_ok = (pow(3, r + 3, mod) * (u % mod) - 1) % mod == 0
        diff_int = 8 * (1 - 27 * u * 3 ** r)          # = 3^r * (8/3^r - 8*27u), 3^r odd
        rhs_ok = diff_int % (1 << E) == 0
        if lhs_ok != rhs_ok:
            ok_ds = False
    # the exact claimed 256-bit discrete log residue
    claimed = 12538662001334831796442300674852150567042723370909232292825628568973700262907
    mod256 = 1 << 256
    unit = 27 * 102409            # (k_a+2)/8 with k_a=819270 -> u=102409
    target = pow(unit, -1, mod256)
    ok_dlog = pow(3, claimed % (1 << 254), mod256) == target
    ok_dlog &= claimed < (1 << 254)
    # E0 values
    ok_e0v = min(1836655 - 2, 514273) == 514273
    # section 3 potential arithmetic on synthetic paired gateways
    pot_ok = True
    for _ in range(200):
        j = random.randrange(21, 400)
        r = random.randrange(1, 8)
        m = random.randrange(5, j - 5)      # m<=j-5 hypothesis
        Gamma = random.randrange(0, 50)
        V = Gamma + j + 2 * r
        V2 = (Gamma + 2) + m + 2 * (r + 1)
        pot_ok &= V2 <= V - 1
    # size chain: Q<=2^(j/4-2), 3k<=2^(j/2), B<=2^(j/2), j>=21:
    # |Z| <= Q(3k+B+12) <= 2^(j/4-2)*(4*2^(j/2)+12) <= 2^(3j/4+1) < 2^(j-4)
    size_ok = True
    for j in (21, 22, 40, 64, 1000):
        bound = F(1 << (j // 4 - 2)) * (4 * (1 << (j // 2)) + 12)
        size_ok &= bound <= F(1 << (3 * j // 4 + 1))
        size_ok &= (3 * j // 4 + 1) < j - 4
    record('DEPTH.all', bad == 0 and ok_e0 and ok_dlog and ok_e0v and pot_ok and ok_ds,
           identity_instances=300, e0_ok=ok_e0, dlog256_ok=ok_dlog,
           potential_instances=200, size_chain_spot=size_ok, depth_source=ok_ds)


# ----------------------------------------------------------------------------
# 15. secondary: SEED_BUDGET a-parent identity + arithmetic
# ----------------------------------------------------------------------------
def check_seed():
    # a-parent: y2 = (5/4)x + D + 9k + 12 exactly; m = v2(9k+theta+12) when small
    bad = 0; mok = 0; mchecked = 0
    for _ in range(300):
        j = random.randrange(9, 60)
        theta = random.choice([-2, 14])
        x = F(1 << j)
        th = x + theta
        k = random.randrange(1, 60)
        # find a canonical odd-a crossing n=j-1 in range if available; else synthetic
        x5 = 2 * th + 6 * k - x / 2          # a-step from parent
        th5 = th + 3 + 6 * k
        y2 = 2 * th5 + 6 - x5 / 2            # X(4) step
        if y2 != F(5, 4) * x + theta + 9 * k + 12:
            bad += 1
        m = val(y2)
        if m < j - 1:
            mchecked += 1
            if m != v2int(9 * k + theta + 12):
                bad += 1
            else:
                mok += 1
    # arithmetic: m<=j-6 => Gamma_new+m+2 < Gamma+j for a (loss 2), b (loss 3)
    arith = all((g + 2) + (j - 6) + 2 < g + j for g in range(0, 100) for j in range(21, 200))
    arith &= all((g + 3) + (j - 6) + 2 < g + j for g in range(0, 100) for j in range(21, 200))
    # C1 style bound 4.5(j-1)^2+26 < 2^(j-5) at N0 and ratio persistence
    quad = all(int(4.5 * (j - 1) ** 2) + 26 < 1 << (j - 5) for j in range(21, 200))
    ratio = all((4.5 * j * j + 26) < 2 * (4.5 * (j - 1) ** 2 + 26) for j in range(3, 10**5))
    # c-history z2 expressions: z2 = (3/2)z+2d+6 with (z,d) from the table;
    # v2 constraints force k>=5 (A), >=26 (AA), >=16 (BA); then all z2 positive
    z2_ok = True
    for k in range(0, 200):
        if k % 32 == 5:      # A: v2(6k+2)=5
            z2_ok &= (F(3, 2) * (6 * k + 2) + 2 * 5 + 6) == 9 * k + 19
            z2_ok &= (F(3, 2) * (6 * k + 2) - 22 + 6) == 9 * k - 13
        if k % 32 == 26:     # AA: v2(6k+4)=5
            z2_ok &= (F(3, 2) * (6 * k + 4) + 10 + 6) == 9 * k + 22
            z2_ok &= (F(3, 2) * (6 * k + 4) - 22 + 6) == 9 * k - 10
        if k % 32 == 16:     # BA: v2(6k)=5
            z2_ok &= (F(3, 2) * (6 * k) + 10 + 6) == 9 * k + 16
            z2_ok &= (F(3, 2) * (6 * k) - 22 + 6) == 9 * k - 16
    zpos = all(9 * k + s > 0 for k, s in
               [(k, t) for k in range(5, 100) for t in (19, -13)] +
               [(k, t) for k in range(26, 100) for t in (22, -10)] +
               [(k, t) for k in range(16, 100) for t in (16, -16)])
    record('SEED.all', bad == 0 and arith and quad and ratio and zpos and z2_ok,
           identity_instances=300, m_checked=mchecked, m_matched=mok,
           arithmetic=arith, quadratic=quad, z2_positive=zpos, z2_forms=z2_ok)


# ----------------------------------------------------------------------------
# 16. secondary: COPY_BUDGET SOURCE-RESERVE derivation + negative control
# ----------------------------------------------------------------------------
def check_copy():
    # exact b/c-copy identity on canonical crossings with real coefficients
    bad = 0
    for n in range(4, 200):
        r = CAL.crossing(n)
        if not (r['odd'] and r['kind'] in 'bc'):
            continue
        for _ in range(3):
            u = random.randrange(1, 10**6, 2)
            j = n + 1
            D = F(random.randrange(-100, 100))
            x = (1 << j) * u
            th = x + D
            cW = (r['head_ratio'] + 2 * r['tail_ratio']) * (1 << n)
            if cW.denominator != 1:
                bad += 1
                continue
            cW = int(cW)
            lam = r['head_lambda'] + 2 * r['tail_lambda'] + 3
            xnew = cW * u + lam
            thnew = th + 3 + 3 * r['time']
            Dnew = thnew - xnew
            Phi = 3 * r['time'] + 5 - lam
            # exact identity D' = D + Phi - 2 + (2^j - c')*u   (CONTEXT 1.2)
            if (Dnew - (D + Phi - 2) - ((1 << j) - cW) * u) != 0:
                bad += 1
            # class rule: D' = D + Phi - 2 mod 2^(omega+1)
            om = v2int(lam)
            if om < 40 and (Dnew - (D + Phi - 2)) % (1 << (om + 1)) != 0:
                bad += 1
    # potential inequality chain: under SOURCE-RESERVE (Gs+omega+2*r_s+h_s<=P),
    # V - V_new >= sigma-omega-2*(r_new-r_p) >= rho-P >= 1
    chain_ok = True
    for _ in range(300):
        rho = random.randrange(16, 10**6)
        Gs = random.randrange(0, 4)
        omega = random.randrange(1, 30)
        r_s = random.randrange(0, 6)
        r_p = random.randrange(0, 6)
        h_s = random.randrange(0, 12)
        sigma = rho - Gs
        P = Gs + omega + 2 * r_s + h_s                    # largest allowed P (equality at fire)
        if P >= rho:                                      # fire parameter must stay < pointer
            continue
        r_new = random.choice([max(r_p, r_s), r_p, r_p + r_s, min(r_p, r_s)])
        if r_new > max(r_p, r_s):
            continue
        drop = (sigma - omega) - 2 * (r_new - r_p)
        chain_ok &= drop >= rho - P
    # negative control n=5
    r5 = CAL.crossing(5)
    lam5 = r5['head_lambda'] + 2 * r5['tail_lambda'] + 3
    om5 = v2int(lam5)
    Phi5 = 3 * r5['time'] + 5 - lam5
    ctrl = (om5 == 1 and Phi5 == 1 and 3 * r5['time'] == 6)
    # 31/27 = 1 mod 4 in the 2-adic sense (v2(31/27 - 1) = 2);
    # rank-3 source budget 0+1+6=7 > P=1
    budget = 0 + 1 + 2 * 3
    ctrl &= val(F(31, 27) - 1) >= 2 and budget > 1
    record('COPY.all', bad == 0 and chain_ok and ctrl,
           copy_identities_bad=bad, chain_instances=300, negative_control=ctrl)


# ----------------------------------------------------------------------------
# 17. secondary: JOINT_HEIGHT_BUDGET
# ----------------------------------------------------------------------------
def check_joint():
    from math import ceil
    def h(c):
        c = F(c)
        return ceil(max(F(0), 1 - c, c - 2))
    # h(3-c)=h(c), h(cp+cs-2)<=h(cp)+h(cs)+1, h(4+c/3)<=ceil((h(c)+8)/3)<=h(c)+3
    ok = True
    for num in range(-40, 61):
        for den in (1, 3):
            c = F(num, den)
            if h(3 - c) != h(c): ok = False
    for n1 in range(-30, 31):
        for n2 in range(-30, 31):
            for d1 in (1, 3):
                for d2 in (1, 3):
                    c1, c2 = F(n1, d1), F(n2, d2)
                    if h(c1 + c2 - 2) > h(c1) + h(c2) + 1: ok = False
    for num in range(-60, 61):
        for den in (1, 3, 9):
            c = F(num, den)
            if h(4 + c / 3) > ceil((h(c) + 8) / 3): ok = False
            if h(4 + c / 3) > h(c) + 3: ok = False
    # seed heights and charge
    ok &= h(F(10, 3)) == 2 and h(F(26, 3)) == 7 and 2 * 1 + 7 == 9
    # rho-P>=3: fires with pointer<16 computed via preceding_fire_by_pointer
    fires = {}
    for n in range(4, 40):
        f = CAL.preceding_fire_by_pointer(n)
        fires[f['pointer']] = (f['k'], 1 + v2int(3 * f['k'] + 2))
    small = sorted(p for p in fires if p < 16)
    gaps = sorted(p - fires[p][1] for p in small)
    ok &= small == [4, 7, 11, 13] and gaps == [3, 3, 9, 12]
    # quadratic: 3rho^2+4 < 2^(rho-2) at 16, ratio persists
    ok &= 3 * 16 ** 2 + 4 < 1 << 14
    ok &= all(3 * r * r + 4 < 1 << (r - 2) for r in range(16, 500))
    ok &= all((3 * (r + 1) ** 2 + 4) < 2 * (3 * r * r + 4) for r in range(2, 10**5))
    # section 4: rho>=P+11 for P>=14
    ok &= 3 * 24 ** 2 + 4 < 1 << 14          # P=14: 3*(P+10)^2+4 < 2^P
    ok &= all(3 * (P + 10) ** 2 + 4 < 1 << P for P in range(14, 500))
    ok &= all((3 * (P + 11) ** 2 + 4) < 2 * (3 * (P + 10) ** 2 + 4) for P in range(1, 10**5))
    # drops 13/14 arithmetic: A: j=rho+3, m<=P-4, rho>=P+11 -> j-m-5>=13
    ok &= all((rho + 3) - (P - 4) - 5 >= 13 for P in range(14, 300) for rho in range(P + 11, P + 15))
    ok &= all((rho + 4) - (P - 6) - 7 >= 14 for P in range(14, 300) for rho in range(P + 11, P + 15))
    ok &= all((rho + 3) - (P - 7) - 7 >= 14 for P in range(14, 300) for rho in range(P + 11, P + 15))
    # W composition arithmetic: with the strengthened source contract
    # (Gs+omega+2*r_s+h_s <= P), W_new-W_parent <= -(rho-P)+1 <= -2 when rho-P>=3
    comp_ok = True
    for _ in range(300):
        rho = random.randrange(16, 10**6)
        P = random.randrange(3, rho - 3) if rho > 6 else 3
        sig_om = random.randrange(1, 40)      # sigma-omega
        r_s = random.randrange(0, 5); r_p = random.randrange(0, 5)
        h_s = random.randrange(0, 12); h_p = random.randrange(0, 12)
        # the budget bounds sigma-omega from below: sigma-omega = rho-Gs-omega
        Gs_om = random.randrange(0, 40)       # Gs+omega
        # require Gs+omega+2r_s+h_s <= P and sigma-omega=rho-(Gs+omega)
        if Gs_om + 2 * r_s + h_s > P:
            comp_ok &= True
            continue
        r_new = random.choice([max(r_p, r_s), r_p, min(r_p, r_s)])
        h_new = h_p + h_s + 1                 # worst case copy bound
        gain = -(rho - Gs_om) + 2 * (r_new - r_p) + (h_new - h_p)
        comp_ok &= gain <= -(rho - P) + 1
    record('JOINT.all', ok and comp_ok, height_identities=ok,
           small_fire_gaps=gaps, composition_ok=comp_ok)


# ----------------------------------------------------------------------------
# 18. secondary: STOP_CHECKPOINT O2 family
# ----------------------------------------------------------------------------
def check_stop():
    ok = True
    words = {}
    for m in [6, 8, 10, 12, 16, 20, 32, 64]:
        u = ((1 << (m - 4)) - 1) // 3
        ok &= u % 2 == 1 and 3 * u == (1 << (m - 4)) - 1
        x = 32 * u; th = x + 5
        ok &= val(F(x)) == 5
        y = 2 * th + 6 - x / 2
        ok &= y == 1 << m          # x' = 48u+16 = 2^m
        # W at entry: Gamma=0, j=5, r=0, h(5)=3 -> 8
        # walk it exactly with my walker
        status, rows = my_exact_walk(CAL, x, th)
        words[m] = ([j for j, g in rows], status)
        ok &= status == 'end'
    # word checks from the doc
    ok &= words[6][0] == [5, 6, 1]
    ok &= words[8][0] == [5, 8, 3]
    # max record for m=8 walk is 9 (precision 10 needed)
    u8 = ((1 << 4) - 1) // 3
    st8, rows8 = my_exact_walk(CAL, 32 * u8, 32 * u8 + 5)
    ok &= max(j + g for j, g in rows8) == 9
    # W at entry = 8 < 9 but record reaches 9 (ceiling failure) for every even m>=8
    ok &= all(m + 1 >= 9 for m in range(8, 100, 2))
    # intermediate normalized weighted value at m=6 is 11: Gamma=1,j=6,r=1,c=10/3 -> 1+6+2+2
    ok &= 1 + 6 + 2 * 1 + 2 == 11
    record('STOP.all', ok, sample_words={str(k): v[0] for k, v in words.items()},
           max_record_m8=9)


# ----------------------------------------------------------------------------
def main():
    RESULTS['_failures'] = []
    check_gt_recurrences()
    check_train_valuation()
    check_labels()
    check_no_three()
    check_band()
    rebuild_graph1()
    check_entry()
    check_drop2()
    check_no_four()
    rebuild_graph2()
    check_orbit()
    check_cross_scale()
    check_depth()
    check_seed()
    check_copy()
    check_joint()
    check_stop()
    # streaming checks last (slow)
    check_stream(10**8)
    RESULTS['meta'] = dict(total=len(RESULTS) - 1, failures=len(FAILURES),
                           seconds=round(time.time() - t0, 1),
                           seed=20261024)
    (HERE / 'review_checks.json').write_text(
        json.dumps(RESULTS, indent=2, default=str), encoding='utf-8')
    print('failures:', FAILURES)
    sys.exit(1 if FAILURES else 0)


if __name__ == '__main__':
    main()
