"""Instrumented compositional prover: gathers induction-critical statistics.
Extra logging per nested call: j (=v2f(H)), s'' = v2f(d+3), margin j-s'', r, window
pattern (which window positions are NOT clean multiples of H), a, ell, and the
d-offset class Delta = d - (3*t+1) at canonical moments."""
import sys, time
sys.setrecursionlimit(100000)
from prover2 import add, sc, sub, par, half, ge3, v2f, halfn, Z0, T_list, encode, final_match, F as F2

STATS = {'calls': 0, 'margin_min': 10**9, 'margin_neg': 0, 'Deltas': {}, 'winpat': {},
         'amax': 0, 'ellmax': 0, 'spmax': 0, 'r_at_call': {}}

def F(L, level, Z0L, s0, H0, kap0, t0=0):
    """t0 = top-step count at entry (for Delta bookkeeping)."""
    L = list(L); ell = 0
    while True:
        a = final_match(L, Z0L)
        if a is not None:
            head = L[0]
            expect = add(sc(H0, 1 << s0), (0, 3 * ell), (0, 1), kap0, *Z0L[:a])
            if head == expect:
                return ell, a, head
        enc = encode(L) if len(L) >= 3 else None
        if enc is not None:
            H, d, r, kap = enc
            A = add(H, d)
            if par(A) == 0 and r >= 2:
                L = [add(sc(H, 4), d, (0, 3))] + L[3:]; ell += 1
                continue
            if par(A) == 1:
                if r >= 2:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), half(add(H, d, (0, 1))))
                    window = L[3:]
                elif r == 1:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), kap, half(add(H, d, (0, 1))))
                    window = L[3:]
                else:
                    z1 = L[2] if len(L) > 2 else Z0
                    q0 = add(sc(H, 3), sc(kap, 2), d, (0, 3))
                    cprime = add(z1, half(add(H, d, (0, 1))))
                    window = L[3:]
                sp = v2f(q0)
                if sp >= 1:
                    o_p = halfn(q0, sp)
                    kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
                    nestL = [add(o_p, (0, 1))] + [sc(o_p, 1 << i) for i in range(sp - 1)] \
                            + [add(sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                    assert sp < level
                    # --- statistics ---
                    STATS['calls'] += 1
                    j = v2f(H); s2 = v2f(add(d, (0, 3)))
                    mg = j - s2
                    if mg < STATS['margin_min']: STATS['margin_min'] = mg
                    if mg < 1: STATS['margin_neg'] += 1
                    # window pattern: which of first 6 window entries are not multiples of H
                    pat = []
                    for i, we in enumerate(window[:6]):
                        wh = sub(we, sc(H, 1 << (i + 2))) if r >= 2 else None
                        if r >= 2:
                            pat.append(0 if (wh == (0, 0)) else 1)
                        else:
                            pat.append(-1)
                    key = ('r%d' % r, tuple(pat))
                    STATS['winpat'][key] = STATS['winpat'].get(key, 0) + 1
                    # Delta class: d - (3*(t0+ell) + 1)
                    t_now = t0 + ell
                    Dl = sub(d, (0, 3 * t_now + 1))
                    STATS['Deltas'][Dl] = STATS['Deltas'].get(Dl, 0) + 1
                    ell_n, a_n, head_n = F(nestL, sp, window, sp, o_p, kap_nest, t0 + ell + 1)
                    STATS['amax'] = max(STATS['amax'], a_n)
                    STATS['ellmax'] = max(STATS['ellmax'], ell_n)
                    STATS['spmax'] = max(STATS['spmax'], sp)
                    STATS['r_at_call'][r] = STATS['r_at_call'].get(r, 0) + 1
                    L = [head_n] + list(window[a_n:])
                    ell += 1 + ell_n
                    continue
        L = T_list(L); ell += 1

def excursion(v):
    w3 = (6, 3)
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
    ell, a, head = F(L, v, [], v, w3, (0, -1))
    assert a == 0 and head == add(sc(w3, 1 << v), (0, 3 * ell))
    return ell

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    t0 = time.time()
    ells = [excursion(v) for v in range(1, N + 1)]
    print('F verified for v=1..%d in %.1fs' % (N, time.time() - t0))
    print('stats:', {k: v for k, v in STATS.items() if k not in ('Deltas', 'winpat')})
    print('margin_min =', STATS['margin_min'], ' neg =', STATS['margin_neg'])
    print('max ell/v =', max(ells[v - 1] / v for v in range(10, N + 1)))
    print('r at nested calls:', STATS['r_at_call'])
    print('window patterns (top 12):')
    for k, c in sorted(STATS['winpat'].items(), key=lambda x: -x[1])[:12]:
        print('   %5d  %s' % (c, k))
    print('Delta classes (top 12):')
    for k, c in sorted(STATS['Deltas'].items(), key=lambda x: -x[1])[:12]:
        print('   %5d  d - (3t+1) = %s' % (c, k))
