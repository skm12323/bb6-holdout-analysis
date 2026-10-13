"""Extended copied-state experiment, adapted from work_tie2/verify_tie2.py.
Snapshot SHA256: DA278BF3A463743540009319816A4E95EC7ADD35E17E6ACC6CAE3B79D6893DF8
Run: python -B work_tie_extension/explore_layers.py [LMAX=3]
Imports work_el/verify_el.py and work_m/verify_m.py READ-ONLY.
Writes only this directory. Existing source and certificates are read-only.
Changes: exact b/c margin gain, bounded path length, strict margin rejection,
full output-family export, checkpoint summaries, stop after an incomplete layer.

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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_m'))
sys.path.insert(0, str(ROOT / 'work_el'))
import verify_el as ve

v2 = ve.v2
N = 10**6
MCAP = 4096          # cap on retained u bits (forgetting bits is conservative)
BRANCH_MAX = 24
LEAF_BUDGET = 4096   # an extended run with more leaves is reported as a failure (EXPLOSION)
PATH_CAP = 256


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
                if h <= 0:
                    leaves.append(dict(res='INSUFFICIENT_MARGIN', path=path, hmin=hmin, branches=br)); break
                if len(path) >= PATH_CAP:
                    leaves.append(dict(res='PATH_CAP', path=path, hmin=hmin, branches=br)); break
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
                    # sigma_W=n-epsilon(n); h gain is n-epsilon(n)-j_W = vv.
                    assert vv >= 1
                    T = T + 3 * tau + 3; j = jw; h = h + vv
                    m = min(vv + 1, MCAP); u = (luw + (1 << vv)) % (1 << m)
                    kind = 'c'
                path.append((j, T, M, u, m, h, kind))
                hmin = min(hmin, h)
        return leaves
    return ext


def main():
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    Xt, typ, par, chain, st, steps = ve.real_walk(N)
    real = sigma_walk(N, chain)
    print('walk: steps', steps, 'top-level chains', len(real), flush=True)
    run = ve.make_run(Xt, typ, par, chain)
    ext = make_ext(Xt, typ, par, real)
    memo = {}

    def canon(j, t):
        return (j, t % (1 << j))

    def xkey(j, T, M, u, m):
        # retain at most MCAP bits of Theta (forgetting bits is conservative); symmetric residue
        M = min(M, MCAP)
        r = T % (1 << M)
        if r >= 1 << (M - 1):
            r -= 1 << M
        return (j, r, M, u % (1 << m), m)

    def finish(entry, leaves, old):
        bad = [L for L in leaves if L['res'] != 'END' or L['hmin'] <= 0]
        xrec = set(); mx = 0
        for L in leaves:
            mx = max(mx, len(L['path']))
            for (a, T, M, u, m, h, kd) in L['path']:
                if kd in 'aA':
                    xrec.add(xkey(a, T, M, u, min(m, max(h, 1))))   # copier knows u mod 2^min(m, v), v>=h
        info = dict(entry=entry, old=old, n_leaves=len(leaves),
                    minh=min(L['hmin'] for L in leaves),
                    max_branches=max(L['branches'] for L in leaves),
                    leaves=[dict(res=L['res'], path=[(a, T % (1 << a), kd, h) for a, T, M, u, m, h, kd in L['path']])
                            for L in leaves[:8]],
                    FAIL=bool(bad))
        return ([], sorted(xrec), mx, info)

    def go(j, th):
        """minimal-information entry (j, theta)"""
        if (j, th) in memo:
            return memo[(j, th)]
        out, f = run(j, th)
        if f is None:
            return ([canon(a, b) for a, b, kd in out if kd == 'a'], [], len(out), None)
        r = finish(['pair', j, th], ext(j, th, j, 1, 1), [(a, b) for a, b, _ in out])
        memo[(j, th)] = r
        return r

    def gox(key):
        """extended entry"""
        if ('X',) + key in memo:
            return memo[('X',) + key]
        j, T, M, u, m = key
        r = finish(['X'] + list(key), ext(j, T, M, u, m), None)
        memo[('X',) + key] = r
        return r

    A0 = set()
    for J in range(2, N):
        ao, xo, mx, info = go(J, 1)
        assert info is None and mx <= 2
        A0 |= set(ao)
    AO = {0: (set(), set(A0), set())}   # (any-j outputs {(range,theta)}, pairs, X-records)
    report = {}
    for l in range(1, LMAX + 1):
        big = {i: set() for i in range(1, l)}
        small_any = set(); small_spec = {}; small_x = {}; aany = set()

        def add(i, th, spec_j=None, why=None):
            if spec_j is not None:
                small_spec.setdefault(canon(spec_j, th), []).append(why)
            elif i == 0:
                small_any.add(th)
            else:
                big[i].add(th)

        def addx(rec, shift, Mcap, why):
            j, T, M, u, m = rec
            M2 = min(M, Mcap)
            small_x.setdefault(xkey(j, T + shift, M2, u, m), []).append(why)
        for i in range(0, l):                      # chain 1, routes a and b
            add(i, 2); add(i, 0); aany.add((i, 2))
        for lw in range(0, l):                     # chain 1, route c: Theta_fire == 1 mod 2^J
            anyw, specw, xw = AO[lw]
            for (i, tw) in anyw: add(i, tw - 1)
            for (jw, tw) in specw: add(0, tw - 1, jw, ('chain1-c', lw, jw, tw))
            for rec in xw: addx(rec, -1, 10**9, ('chain1-cX', lw) + rec[:2])
        for i in range(l - 1, 0, -1):              # bounded-theta states with j in R_i
            for th in sorted(big[i]):
                for i2 in range(0, i):
                    add(i2, 3 - th); aany.add((i2, 3 - th)); add(i2, th - 1)
                for lw in range(0, i):
                    anyw, specw, xw = AO[lw]
                    for (i2, tw) in anyw: add(i2, th + tw - 2)
                    for (jw, tw) in specw: add(0, th + tw - 2, jw, ('big-c', i, th, lw, jw, tw))
                    for rec in xw: addx(rec, th - 2, N, ('big-cX', i, th, lw) + rec[:2])
        pairs_out = set(); x_out = set(); dist = Counter(); infos = []; nent = 0

        def take(res, prov):
            nonlocal nent
            ao, xo, mx, info = res
            pairs_out.update(ao); x_out.update(xo); dist[mx] += 1; nent += 1
            if info:
                info = dict(info); info['provenance'] = prov; infos.append(info)
        for th in sorted(small_any):
            print('CHECK level', l, 'theta', th, flush=True)
            for j in range(1, N):
                take(go(j, th), 'any-j theta=%d' % th)
        for (j, th), why in sorted(small_spec.items()):
            take(go(j, th), why[:3])
        for key, why in sorted(small_x.items()):
            take(gox(key), why[:3])
        AO[l] = (aany, pairs_out, x_out)
        fails = [r for r in infos if r['FAIL']]
        ok = [r for r in infos if not r['FAIL']]
        pats = Counter(json.dumps([(a, b, kd) for a, b, kd, h in L['path']][-3:])
                       for r in ok for L in r['leaves'])
        rep = dict(big={i: sorted(v) for i, v in big.items()}, small_any=sorted(small_any),
                   n_small_spec=len(small_spec), n_small_x=len(small_x), entries=nent,
                   dist=dict(sorted(dist.items())), max_further=max(dist),
                   n_extended_runs=len(infos), n_resolved=len(ok), n_failed=len(fails),
                   resolved_min_h_from_baseline_1=min([r['minh'] for r in ok], default=None),
                   resolved_max_branches=max([r['max_branches'] for r in ok], default=0),
                   resolved_tail_patterns=dict(pats.most_common()),
                   failures=fails[:40], resolved_examples=ok[:5],
                   resolved_entries=[r['entry'] for r in ok],
                   n_aout_pairs=len(pairs_out), n_aout_x=len(x_out), aout_any=sorted(aany),
                   x_out_sample=sorted(x_out)[:50])
        report[l] = rep
        print('LEVEL', l, json.dumps({k: rep[k] for k in ('big', 'small_any', 'n_small_spec', 'n_small_x',
              'entries', 'dist', 'max_further', 'n_extended_runs', 'n_resolved', 'n_failed',
              'resolved_min_h_from_baseline_1', 'resolved_max_branches', 'n_aout_pairs', 'n_aout_x')},
              default=str), flush=True)
        for r in fails[:12]:
            print('   FAIL', r['entry'], r['provenance'], r['n_leaves'], 'leaves; e.g.',
                  [(L['res'], L['path'][:3]) for L in r['leaves'][:3]], flush=True)
        rep['aout_pairs'] = sorted(pairs_out)
        rep['aout_extended'] = sorted(x_out)
        rep['specific_entries'] = sorted(small_spec)
        rep['extended_entries'] = sorted(small_x)
        Path(__file__).with_name('certificate_layers.json').write_text(
            json.dumps(dict(N=N, walk_steps=steps, A0=sorted(A0), levels=report), indent=1,
                       default=str) + '\n', encoding='utf-8')
        if fails:
            print('STOP: incomplete covering layer; not evidence of an actual orbit failure.', flush=True)
            break


if __name__ == '__main__':
    main()
