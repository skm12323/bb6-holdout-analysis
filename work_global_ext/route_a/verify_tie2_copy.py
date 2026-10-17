"""verify_tie2.py -- finite certificate for PROOF_TIE2.md.
Run: python -B work_tie2/verify_tie2.py [LMAX=4]
Imports work_el/verify_el.py and work_m/verify_m.py READ-ONLY.
Writes only work_tie2/certificate_tie2.json (and prints a summary).

EXTENDED STATE (j, T, M, u, m):  Theta == T (mod 2^M),  lambda(run base) == u (mod 2^m).
Exact transition identities (PROOF_EL A1/A2, PROOF_M Lemma 3.2, PROOF_RESCUE (AA)):
  a-step, n=j-1, k=tau(n)/2:  x = 2(Theta+3k) - 2^n u   (exact integer, lambda of the new chain)
        j' = v2(x),  u' = x >> j',  Theta' = Theta+3+6k,  h' = h+j-j'-1.
        x is known mod 2^B, B = min(M+1, n+m).  If x == 0 mod 2^B the next unknown bit is
        BRANCHED (both values): an exhaustive split, never a guess.
  b/c-step (n < N, real crossing): the new chain is M_{u_t}(W chain at tau(n)) with
        M_u(c',l') = (c_u c', l_u c' + l'):  j' = j_W,  Theta' = Theta + 3 tau(n) + 3 (exact),
        u' = l_uW + c_uW * u  ==  l_uW + 2^v  (mod 2^(v+1)),  v = v2(c_uW) = sigma_W - j_W
        (l_uW, sigma_W are REAL data of the real walk);  h' >= h+1.
Entry knowledge: Theta == theta (mod 2^j), u odd, h >= 1 (minimal), unless an entry is a copy of
a chain recorded with extended data (records 'X', see PROOF_TIE2 section 3).
"""
from collections import Counter
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'work_m'))
sys.path.insert(0, str(ROOT / 'work_el'))
import verify_el as ve

v2 = ve.v2
N = 10**6
MCAP = 4096          # cap on retained u bits (forgetting bits is conservative)
BRANCH_MAX = 24
LEAF_BUDGET = 4096   # an extended run with more leaves is reported as a failure (EXPLOSION)


def sigma_walk(NB, chain):
    """Second pass of the certified lambda walk (same loop as verify_el.real_walk) recording, at
    every top-level chain time s: (j, l_u, sigma) with sigma by PROOF_M Lemma 3.2 (as verify_m.V2)."""
    CAP = NB + 10
    Xt = [None] * CAP; Xeps = [0] * CAP
    lA = 1; S = []; i = 0; s = 0; calls = []; first = True; sig_last = None; jl = None
    data = {}
    while i <= NB:
        while calls and calls[-1] < s: calls.pop()
        k = len(S)
        if k >= 2: lb = S[-1]; lc = S[-2]; nb = nc = None
        elif k == 1: lb = S[-1]; lc = 0; nb = None; nc = i
        else: lb = lc = 0; nb = i; nc = i + 1
        par = (lA + (1 if first else 0)) & 1
        for n in (nb, nc):
            if n is not None and n < CAP and Xt[n] is None:
                Xt[n] = s
                Xeps[n] = 0 if (k == 0 and i == n) else 1 if k == 0 else n - (sig_last - 1)
        if par == 0:
            lA = lA + lb + lc + 3; push = None
        else:
            lx = lA + 2 * lb + 3; j = v2(lx); u = lx >> j
            if not calls:
                sg = i if k == 0 else sig_last - 1 - Xeps[jl - 1]
                assert j < sg and chain[s][0] == j
                data[s] = (j, u, sg)
                sig_last = sg; jl = j
            T = Xt[j - 1]
            if T > 0: calls.append(s + T)
            push = (u, j, lc + (lA + 1) // 2); lA = u + 1
        if k >= 2: del S[-2:]
        else: i += 2 - k; S.clear()
        if push:
            u, j, D = push; S.append(D)
            for t in range(j - 2, -1, -1): S.append(u << t)
        s += 1; first = False
    assert set(data) == set(chain)
    return data


def make_ext(Xt, typ, par, real):
    def ext(j, T, M, u, m, h=1):
        leaves = []
        stack = [(j, T, M, u, m, h, [], 0, h)]
        while stack:
            if len(leaves) >= LEAF_BUDGET:
                leaves.append(dict(res='EXPLOSION', path=[], hmin=h, branches=BRANCH_MAX)); break
            j, T, M, u, m, h, path, br, hmin = stack.pop()
            while True:
                n = j - 1
                if n >= N:
                    leaves.append(dict(res='NODATA', path=path, hmin=hmin, branches=br)); break
                if par[n] == 0:
                    leaves.append(dict(res='END', path=path, hmin=hmin, branches=br)); break
                if typ[n] == 'a':
                    k = Xt[n] // 2
                    B = min(M + 1, n + m)
                    x = (2 * (T + 3 * k) - (u << n)) % (1 << B)
                    if x == 0:
                        if br >= BRANCH_MAX:
                            leaves.append(dict(res='UNRESOLVED', path=path, hmin=hmin, branches=br)); break
                        if M + 1 <= n + m:
                            stack.append((j, T + (1 << M), M + 1, u, m, h, list(path), br + 1, hmin)); M += 1
                        else:
                            stack.append((j, T, M, u + (1 << m), m + 1, h, list(path), br + 1, hmin)); m += 1
                        br += 1
                        continue
                    jn = v2(x)
                    mn = min(B - jn, MCAP)
                    u = (x >> jn) % (1 << mn); m = mn
                    kind = 'a' if jn < j else 'A'          # 'A' = non-NT a-step
                    h = h + j - jn - 1; T = T + 3 + 6 * k; j = jn
                else:
                    tau = Xt[n]; jw, luw, sgw = real[tau]
                    vv = sgw - jw
                    T = T + 3 * tau + 3; j = jw; h = h + 1
                    m = min(vv + 1, MCAP); u = (luw + (1 << vv)) % (1 << m)
                    kind = 'c'
                path.append((j, T, M, u, m, h, kind))
                hmin = min(hmin, h)
        return leaves
    return ext


def canon(j, t):
    return (j, t % (1 << j))


def xkey(j, T, M, u, m):
    # retain at most MCAP bits of Theta (forgetting bits is conservative); symmetric residue
    M = min(M, MCAP)
    r = T % (1 << M)
    if r >= 1 << (M - 1):
        r -= 1 << M
    return (j, r, M, u % (1 << m), m)


G = {}


def _init(cache):
    import pickle
    with open(cache, 'rb') as f:
        Xt, typ, par, chain, real = pickle.load(f)
    G['run'] = ve.make_run(Xt, typ, par, chain)
    G['ext'] = make_ext(Xt, typ, par, real)


def finish(entry, leaves, old):
    bad = [L for L in leaves if L['res'] != 'END']
    xrec = set(); mx = 0; ties = set(); a_vals = set()
    for L in leaves:
        mx = max(mx, len(L['path']))
        prev = None
        for (a, T, M, u, m, h, kd) in L['path']:
            if kd == 'A':
                a_vals.add((3 * T - 10) % (1 << a) == 0)     # non-NT output == 10/3 mod 2^j ?
                ties.add(prev if prev is not None else ('entry', entry[1]))
            prev = (a, T % 32)
        for (a, T, M, u, m, h, kd) in L['path']:
            if kd in 'aA':
                # a later copier knows u mod 2^min(m, v) with v = sigma - j >= h
                xrec.add(xkey(a, T, M, u, min(m, max(h, 1))))
    info = dict(entry=entry, old=old, n_leaves=len(leaves),
                minh=min(L['hmin'] for L in leaves),
                max_branches=max(L['branches'] for L in leaves),
                leaves=[dict(res=L['res'], path=[(a, T % (1 << a), kd, h) for a, T, M, u, m, h, kd in L['path']])
                        for L in leaves[:8]],
                FAIL=bool(bad), tie_states=sorted(ties, key=str), A_is_10_3=sorted(a_vals))
    return ([], sorted(xrec), mx, info)


def go(j, th):
    out, f = G['run'](j, th)
    if f is None:
        return ([canon(a, b) for a, b, kd in out if kd == 'a'], [], len(out), None)
    return finish(['pair', j, th], G['ext'](j, th, j, 1, 1), [(a, b) for a, b, _ in out])


def gox(key):
    j, T, M, u, m = key
    return finish(['X'] + list(key), G['ext'](j, T, M, u, m), None)


def ratrep(pq, qq, j):
    """the integer in [0, 2^j) congruent to pq/qq mod 2^j (qq odd), computed in O(j)"""
    t = (-pq * pow(pow(2, j, qq), -1, qq)) % qq if qq > 1 else 0
    r = (pq + (t << j)) // qq
    assert r * qq == pq + (t << j)
    return r % (1 << j)


def task(t):
    kind, payload = t
    pairs = set(); xo = set(); dist = Counter(); infos = []
    if kind == 'any':
        th, j0, j1 = payload
        items = [(go(j, th), 'any-j theta=%d' % th) for j in range(j0, j1)]
    elif kind == 'anyq':                       # 2-adic rational family theta = p/q (q odd)
        pq, qq, j0, j1 = payload
        items = [(go(j, ratrep(pq, qq, j)), 'any-j theta=%d/%d' % (pq, qq)) for j in range(j0, j1)]
    elif kind == 'pair':
        items = [(go(j, th), why) for (j, th), why in payload]
    else:
        items = [(gox(key), why) for key, why in payload]
    for (ao, xr, mx, info), prov in items:
        pairs.update(ao); xo.update(xr); dist[mx] += 1
        if info:
            info['provenance'] = prov; infos.append(info)
    return pairs, xo, dist, infos


def main():
    import multiprocessing as mp
    import pickle
    import time
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    NPROC = int(sys.argv[2]) if len(sys.argv) > 2 else max(1, min(16, mp.cpu_count() - 2))
    t0 = time.time()
    Xt, typ, par, chain, st, steps = ve.real_walk(N)
    real = sigma_walk(N, chain)
    cache = str(Path(__file__).with_name('_walkcache.pkl'))
    with open(cache, 'wb') as f:
        pickle.dump((Xt, typ, par, chain, real), f, protocol=pickle.HIGHEST_PROTOCOL)
    del Xt, typ, par, chain, real
    print('walk: steps', steps, 'workers', NPROC, flush=True)
    CH = 25000
    pool = mp.Pool(NPROC, initializer=_init, initargs=(cache,))

    def runall(tasks):
        pairs = set(); xo = set(); dist = Counter(); infos = []
        for p, x, d, inf in pool.imap_unordered(task, tasks, chunksize=1):
            pairs |= p; xo |= x; dist.update(d); infos += inf
        return pairs, xo, dist, infos, sum(dist.values())
    # level 0: fires (J,1), 2 <= J < N
    A0, _, d0, inf0, _ = runall([('any', (1, j, min(j + CH, N))) for j in range(2, N, CH)])
    assert not inf0 and max(d0) <= 2
    AO = {0: (set(), set(A0), set())}   # (any-j outputs {(range,theta)}, pairs, X-records)
    report = {}
    for l in range(1, LMAX + 1):
        big = {i: set() for i in range(1, l)}
        small_any = set(); small_spec = {}; small_x = {}; aany = set(); any_src = {}

        def add(i, th, spec_j=None, why=None):
            if spec_j is not None:
                small_spec.setdefault(canon(spec_j, th), []).append(why)
            elif i == 0:
                small_any.add(th); any_src.setdefault(th, []).append(why)
            else:
                big[i].add(th)

        def addx(rec, shift, Mcap, why):
            j, T, M, u, m = rec
            small_x.setdefault(xkey(j, T + shift, min(M, Mcap), u, m), []).append(why)
        for i in range(0, l):                      # chain 1, routes a and b
            add(i, 2, why=('chain1-a',)); add(i, 0, why=('chain1-b',)); aany.add((i, 2))
        for lw in range(0, l):                     # chain 1, route c: Theta_fire == 1 mod 2^J
            anyw, specw, xw = AO[lw]
            for (i, tw) in anyw: add(i, tw - 1, why=('chain1-c-any', lw, i, tw))
            for (jw, tw) in specw: add(0, tw - 1, jw, ('chain1-c', lw, jw, tw))
            for rec in xw: addx(rec, -1, 10**9, ('chain1-cX', lw) + rec[:2])
        for i in range(l - 1, 0, -1):              # bounded-theta states with j in R_i
            for th in sorted(big[i]):
                for i2 in range(0, i):
                    add(i2, 3 - th, why=('big-a', i, th)); aany.add((i2, 3 - th))
                    add(i2, th - 1, why=('big-b', i, th))
                for lw in range(0, i):
                    anyw, specw, xw = AO[lw]
                    for (i2, tw) in anyw: add(i2, th + tw - 2, why=('big-c-any', i, th, lw, i2, tw))
                    for (jw, tw) in specw: add(0, th + tw - 2, jw, ('big-c', i, th, lw, jw, tw))
                    for rec in xw: addx(rec, th - 2, N, ('big-cX', i, th, lw) + rec[:2])
        tasks = [('any', (th, j, min(j + CH, N))) for th in sorted(small_any) for j in range(1, N, CH)]
        sp = sorted((k, v[:3]) for k, v in small_spec.items())
        tasks += [('pair', sp[a:a + 20]) for a in range(0, len(sp), 20)]
        sx = sorted((k, v[:3]) for k, v in small_x.items())
        tasks += [('x', sx[a:a + 5]) for a in range(0, len(sx), 5)]
        pairs_out, x_out, dist, infos, nent = runall(tasks)
        AO[l] = (aany, pairs_out, x_out)
        fails = [r for r in infos if r['FAIL']]
        ok = [r for r in infos if not r['FAIL']]
        pats = Counter(json.dumps([(a, b, kd) for a, b, kd, h in L['path']][-3:])
                       for r in ok for L in r['leaves'])
        rep = dict(big={i: sorted(v) for i, v in big.items()}, small_any=sorted(small_any),
                   any_sources={th: v for th, v in any_src.items()},
                   n_small_spec=len(small_spec), n_small_x=len(small_x), entries=nent,
                   dist=dict(sorted(dist.items())), max_further=max(dist),
                   n_extended_runs=len(infos), n_resolved=len(ok), n_failed=len(fails),
                   resolved_min_h_from_baseline_1=min([r['minh'] for r in ok], default=None),
                   resolved_max_branches=max([r['max_branches'] for r in ok], default=0),
                   resolved_tail_patterns=dict(pats.most_common()),
                   tie_states=sorted({str(t) for r in ok for t in r['tie_states']}),
                   nonNT_outputs_all_10_3=sorted({v for r in ok for v in r['A_is_10_3']}),
                   failures=fails[:60],
                   n_fail_by_provenance=dict(Counter(str(r['provenance'])[:70] for r in fails)),
                   resolved_examples=ok[:5], resolved_entries=sorted(r['entry'] for r in ok),
                   n_aout_pairs=len(pairs_out), aout_pairs=sorted(pairs_out), n_aout_x=len(x_out),
                   aout_any=sorted(aany), x_out_sample=sorted(x_out)[:80],
                   seconds=round(time.time() - t0))
        report[l] = rep
        print('LEVEL', l, json.dumps({k: rep[k] for k in (
            'big', 'small_any', 'n_small_spec', 'n_small_x', 'entries', 'dist', 'max_further',
            'n_extended_runs', 'n_resolved', 'n_failed', 'resolved_min_h_from_baseline_1',
            'resolved_max_branches', 'n_aout_pairs', 'n_aout_x', 'tie_states', 'nonNT_outputs_all_10_3', 'seconds')}, default=str), flush=True)
        for r in fails[:12]:
            print('   FAIL', r['entry'], r['provenance'], r['n_leaves'], 'leaves; e.g.',
                  [(L['res'], L['path'][:3]) for L in r['leaves'][:3]], flush=True)
        Path(__file__).with_name('certificate_tie2.json').write_text(
            json.dumps(dict(N=N, walk_steps=steps, A0=sorted(A0), levels=report), indent=1,
                       default=str) + '\n', encoding='utf-8')
    if LMAX >= 4:
        # Section 6: the symbolic (AA) macro replaces the failing minimal entry (5,5) by the
        # 2-adic rational family theta = 10/3, any j in [1, N).  Run it.
        tasks = [('anyq', (10, 3, j, min(j + CH, N))) for j in range(1, N, CH)]
        pq_pairs, pq_x, pq_dist, pq_infos, pq_n = runall(tasks)
        pf = [r for r in pq_infos if r['FAIL']]
        mac = dict(family='theta=10/3, 1<=j<N', entries=pq_n, dist=dict(sorted(pq_dist.items())),
                   n_extended_runs=len(pq_infos), n_failed=len(pf), failures=pf[:20],
                   resolved_min_h=min([r['minh'] for r in pq_infos if not r['FAIL']], default=None),
                   tie_states=sorted({str(t) for r in pq_infos for t in r['tie_states']}),
                   nonNT_outputs_all_10_3=sorted({v for r in pq_infos for v in r['A_is_10_3']}),
                   aout_pairs=sorted(pq_pairs)[:200], n_aout_x=len(pq_x))
        print('MACRO-FAMILY 10/3', json.dumps({k: mac[k] for k in ('entries', 'dist', 'n_extended_runs',
              'n_failed', 'resolved_min_h', 'n_aout_x', 'tie_states', 'nonNT_outputs_all_10_3')}), flush=True)
        for r in pf[:12]:
            print('   FAIL', r['entry'][:2], r['n_leaves'], [(L['res'], L['path'][:3]) for L in r['leaves'][:3]], flush=True)
        report['macro_10_3'] = mac
        Path(__file__).with_name('certificate_tie2.json').write_text(
            json.dumps(dict(N=N, walk_steps=steps, A0=sorted(A0), levels=report), indent=1,
                       default=str) + '\n', encoding='utf-8')
    pool.close(); pool.join()
    Path(cache).unlink()


if __name__ == '__main__':
    main()
