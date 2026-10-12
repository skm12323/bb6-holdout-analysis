"""Blind Auditor 2 — S1: queue-determinism (Lemma L0) + prefix universality.

S1a: 10^4 random pairs of states with equal head A and equal first m queue
     entries step identically until a step consumes an original queue entry
     with index >= m.
S1b: spike fires (j >= 5) in the E(1,2000) excursion: 20-step post-fire
     traces, canonicalized by the level base u (value -> (value//u, value%u)),
     compared across spikes with the same j.
"""
import random
import sys
from collections import deque

sys.path.insert(0, '.')
from blind2_lib import Proc, brole, v2, run_orbit


# ---------------- S1a: queue determinism ----------------

def step_tagged_pair(P):
    """One top step on P = [A, deque[(val, orig_idx)]]; pushed entries get
    orig_idx = -1.  Returns an event tuple fully describing the step."""
    A, q = P
    if A % 2 == 0:
        b = q.popleft() if q else (0, -1)
        c = q.popleft() if q else (0, -1)
        P[0] = A + b[0] + c[0] + 3
        return ('E', P[0], b[0], c[0])
    b = q.popleft() if q else (0, -1)
    c = q.popleft() if q else (0, -1)
    x = A + 2 * b[0] + 3
    m = b[0] + (A - 3) // 2
    pushes = []
    while m % 2 == 1 and m >= 3:
        pushes.append((m + 3) // 2)
        m = (m - 3) // 2
    if m == 1:
        return ('HALT', b[0], c[0])
    q.appendleft((c[0] + (A + 1) // 2, -1))
    for val in pushes:          # pushes[0]=x/4 ... front becomes u = last
        q.appendleft((val, -1))
    P[0] = m + 4
    return ('C', P[0], b[0], c[0], tuple(pushes), m, x)


def sim_pair(A, q1, q2, m, cap=800):
    """Run two processes; queues agree on first m entries.  Both must produce
    identical events until a step would consume an original entry with
    index >= m (in either process).  Returns (steps, stop, mismatch)."""
    P1 = [A, deque((v, i) for i, v in enumerate(q1))]
    P2 = [A, deque((v, i) for i, v in enumerate(q2))]
    for t in range(cap):
        for P in (P1, P2):
            head = list(P[1])[:2]
            if any(oi >= m for (_, oi) in head):
                return t, 'stop', None
        e1 = step_tagged_pair(P1)
        e2 = step_tagged_pair(P2)
        if e1 != e2:
            return t, 'MISMATCH', (e1, e2)
        if e1[0] == 'HALT':
            return t, 'halt-together', None
    return cap, 'cap', None


def s1a(n_pairs=10000, seed=20260101):
    rng = random.Random(seed)
    stats = {'stop': 0, 'halt-together': 0, 'cap': 0}
    mismatches = []
    agree_after_stop = 0
    total_sync_steps = 0
    for _ in range(n_pairs):
        L = rng.randint(2, 12)
        m = rng.randint(1, L - 1)
        style = rng.random()
        if style < 0.5:                      # unstructured values
            q1 = [rng.randint(1, 10 ** 6) for _ in range(L)]
            tail2 = [rng.randint(1, 10 ** 6) for _ in range(L - m)]
        elif style < 0.8:                    # run/defect-structured
            U = rng.randint(1, 999) * 2 + 1
            q1 = [(U << a) for a in range(L - 1)] + \
                 [rng.choice([(U << (L - 1)) - 1, rng.randint(1, 10 ** 6)])]
            tail2 = [rng.randint(1, 10 ** 9) for _ in range(L - m)]
        else:                                # small values (deep chains)
            q1 = [rng.randint(1, 50) for _ in range(L)]
            tail2 = [rng.randint(1, 50) for _ in range(L - m)]
        q2 = list(q1[:m]) + tail2
        A = rng.choice([rng.randint(1, 10 ** 6), rng.randint(1, 60),
                        2 * rng.randint(1, 10 ** 5) + 1])
        t, stop, mm = sim_pair(A, q1, q2, m)
        total_sync_steps += t
        if stop == 'MISMATCH':
            mismatches.append((A, q1, q2, m, t, mm))
        else:
            stats[stop] = stats.get(stop, 0) + 1
    return {
        'n_pairs': n_pairs, 'stats': stats, 'mismatches': mismatches,
        'avg_sync_steps': total_sync_steps / n_pairs,
    }


# ---------------- S1b: spike 20-step traces ----------------

def subtree_of(levels, root):
    """Set of level ids in the subtree rooted at `root` (incl.), by parent
    chain.  Also returns depth of root."""
    ids = {root}
    for lid in list(levels):
        p = lid
        while p is not None and p > root:
            p = levels[p][3]
            if p == root:
                ids.add(lid)
                break
    return ids


def spike_trace(ex, ev, nl_steps=20):
    """From the state right after a spike fire with parameter J (new level S
    with base u), run nl_steps tagged steps and record canonical tokens:
    value -> (value // u, value % u).  Clean = neither consumed entry is the
    spike's own defect nor an entry of an older level (level not in S's
    subtree).  Returns dict with tokens, clean_len, J, u, roles."""
    b, c = ev[1], ev[2]
    x, j, u, nl = ev[3], ev[4], ev[5], ev[7]
    S = nl
    depth_S = ex.levels[S][1]
    sub = subtree_of(ex.levels, S)
    # fresh process continuing the excursion state
    p = Proc(A=ex.A, q=ex.q, levels=dict(ex.levels), nlvl=ex.nlvl)
    sub_local = set(sub)
    tokens = []
    clean = True
    clean_len = None
    roles = []
    for t in range(nl_steps):
        if not p.q:
            tokens.append(('END',))
            roles.append(('END',))
            continue
        Apre = p.A
        evt = p.step()
        if evt[0] == 'HALT':
            tokens.append(('HALT', x if False else evt[3] // u if evt[3] >= u else None))
            roles.append(('HALT',))
            if clean:
                clean_len = t
                clean = False
            continue
        bb, cc = evt[1], evt[2]
        # cleanliness of consumed entries
        def is_atom(e):
            return e is not None and (e[1] not in sub_local or
                                      (e[1] == S and e[2] == 1))
        if clean and (is_atom(bb) or is_atom(cc)):
            clean_len = t
            clean = False
        if evt[0] == 'E':
            tokens.append(('E', (Apre // u, Apre % u),
                           (p.A // u, p.A % u)))
            roles.append(('E', (bb[1] if bb else None, bb[2] if bb else None),
                          (cc[1] if cc else None, cc[2] if cc else None)))
        else:
            xx, jj, uu, nnl = evt[3], evt[4], evt[5], evt[7]
            # register new level in subtree if its parent is
            par = evt[1][1] if evt[1] is not None else None
            if par in sub_local:
                sub_local.add(nnl)
            if evt[1] is not None and evt[1][2] == 0:
                U = p.levels[evt[1][1]][0]
                tt = xx - 3 * (U << evt[1][3]) - 4
                kk = tt // 6 if (tt >= 0 and tt % 6 == 0) else None
                rho = evt[1][3]
            else:
                kk = None
                rho = -1
            tokens.append(('C', jj, kk, rho,
                           (xx // u, xx % u), (p.A // u, p.A % u)))
            roles.append(('C', evt[1][1] if evt[1] is not None else None,
                          evt[1][2] if evt[1] is not None else None,
                          rho))
    if clean:
        clean_len = nl_steps
    return {'J': j, 'u': u, 'tokens': tokens, 'clean_len': clean_len,
            'roles': roles, 'lvl': S, 'depth': depth_S}


def s1b():
    """E(1,2000): collect spikes (j>=5) and compare same-j traces."""
    w, v = 1, 2000
    traces = []
    seen_fires = [0]

    def on_fire(ex, ev, idx):
        seen_fires[0] += 1
        if ev[4] >= 5:
            tr = spike_trace(ex, ev)
            tr['idx'] = idx
            tr['brole'] = brole(ev[1], ex.levels)
            tr['b_rho'] = ev[1][3] if (ev[1] is not None and ev[1][2] == 0) else -1
            traces.append(tr)

    ex, fires, fin, finA, ell = run_orbit(w, v, on_fire=on_fire)
    res = {'fin': fin, 'final_A': finA, 'ell': ell, 'n_fires': seen_fires[0],
           'n_spikes': len(traces)}
    # group by (J, brole)
    groups = {}
    for tr in traces:
        groups.setdefault((tr['J'], tr['brole']), []).append(tr)
    ginfo = {}
    for key, ts in sorted(groups.items()):
        toks = [tuple(t['tokens']) for t in ts]
        common = 0
        maxc = min(len(tk) for tk in toks)
        while common < maxc and all(tk[common] == toks[0][common] for tk in toks):
            common += 1
        # restrict comparison to the clean part of each trace
        cleanlens = [t['clean_len'] for t in ts]
        ginfo['J=%d,role=%s' % key] = {
            'n': len(ts), 'common_prefix': common,
            'min_clean_len': min(cleanlens), 'max_clean_len': max(cleanlens),
            'full20_equal': all(tk == toks[0] for tk in toks),
            'clean_equal': all(
                tk[:t['clean_len']] == toks[0][:t['clean_len']]
                for tk, t in zip(toks, ts)),
            'depths': sorted({t['depth'] for t in ts}),
            'rhos': sorted({t['b_rho'] for t in ts})[:8],
        }
    res['groups'] = ginfo
    # cross-J prefix universality: cascade(J) tokens are a prefix of
    # cascade(J') for J<J' (run-role spikes), up to J's clean end
    runtr = {}
    for tr in traces:
        if tr['brole'] == 'run':
            runtr.setdefault(tr['J'], []).append(tr)
    pref_ok = []
    for J in sorted(runtr):
        if J + 1 in runtr or any(J2 > J for J2 in runtr):
            J2 = min(Jj for Jj in runtr if Jj > J)
            t1 = runtr[J][0]
            t2 = runtr[J2][0]
            L = min(t1['clean_len'], len(t2['tokens']))
            pref_ok.append((J, J2,
                            t1['tokens'][:L] == t2['tokens'][:L],
                            t1['clean_len'], t2['clean_len']))
    res['cross_J_prefix'] = pref_ok
    res['traces'] = traces
    return res


if __name__ == '__main__':
    print('=== S1a: queue-determinism, 10^4 random pairs ===')
    r = s1a()
    print('pairs:', r['n_pairs'], 'stats:', r['stats'],
          'avg synced steps:', round(r['avg_sync_steps'], 2))
    print('mismatches:', len(r['mismatches']))
    for mm in r['mismatches'][:3]:
        print('  MISMATCH detail:', mm)
    print()
    print('=== S1b: spike traces in E(1,2000) ===')
    b = s1b()
    print('finish:', b['fin'], 'final A:', b['final_A'],
          'ell:', b['ell'], 'fires:', b['n_fires'], 'spikes:', b['n_spikes'])
    for g, d in b['groups'].items():
        print(' ', g, 'n=%d common_prefix=%d clean_len=%s..%s full20_equal=%s '
              'clean_equal=%s depths=%s' %
              (d['n'], d['common_prefix'], d['min_clean_len'],
               d['max_clean_len'], d['full20_equal'], d['clean_equal'],
               d['depths']))
    print('cross-J prefix (J, J2, prefix_ok, clean1, clean2):',
          b['cross_J_prefix'])
