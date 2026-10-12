"""Derive the Delta-update law exactly: at every event of a real excursion, log
(before-Delta, event type, fire level sp, r, after-Delta) and fit the correction.
Delta = d - (3t+1) at canonical states; updates happen at absorptions (a>=...) and
glue collapses. Goal: |Delta| growth law + the exact correction formula."""
import sys
sys.setrecursionlimit(100000)
from prover2 import add, sc, sub, par, half, v2f, halfn, T_list, encode, final_match

def F(L, level, Z0L, s0, H0, kap0, t0=0, log=None, depth=0):
    L = list(L); ell = 0; last_D = None
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
            pA = par(A)
            t_now = t0 + ell
            Dl = sub(d, (0, 3 * t_now + 1))
            if pA == 0 and r >= 2:
                L = [add(sc(H, 4), d, (0, 3))] + L[3:]; ell += 1
                continue
            if pA == 1:
                if r >= 2:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), half(add(H, d, (0, 1))))
                elif r == 1:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), kap, half(add(H, d, (0, 1))))
                else:
                    q0 = add(sc(H, 3), sc(kap, 2), d, (0, 3))
                    cprime = add(L[2] if len(L) > 2 else (0, 0), half(add(H, d, (0, 1))))
                window = L[3:]
                sp = v2f(q0)
                if sp >= 1:
                    o_p = halfn(q0, sp)
                    kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
                    nestL = [add(o_p, (0, 1))] + [sc(o_p, 1 << i) for i in range(sp - 1)] \
                            + [add(sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                    ell_n, a_n, head_n = F(nestL, sp, window, sp, o_p, kap_nest,
                                           t0 + ell + 1, log, depth + 1)
                    if log is not None:
                        log.append((depth, t_now, r, sp, a_n, ell_n, Dl[1],
                                    'kap_nest const', kap_nest[1] if kap_nest[0] == 0 else None))
                    L = [head_n] + list(window[a_n:])
                    ell += 1 + ell_n
                    continue
        L = T_list(L); ell += 1

if __name__ == '__main__':
    log = []
    w3 = (6, 3)
    for v in list(range(2, 300)):
        L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
        F(L, v, [], v, w3, (0, -1), 0, log)
    from collections import Counter
    # Delta transitions: before-Delta -> set of (event params)
    upd = Counter()
    for row in log:
        upd[(row[6] is not None and row[6] != 0, row[2] >= 2, row[4] > 0)] += 1
    print('event classes (Delta!=0?, r>=2?, a>0?):', dict(upd))
    # fit: for r>=2, a>0 (clean absorption): Delta stays? check via pairs in time order per excursion—
    # simpler: correlate kap_nest const with Delta updates:
    # print distinct (D, r, sp, a, kapc) with counts, only where D != 0
    cc = Counter((row[6], row[2], row[3], row[4], row[7]) for row in log if row[6] not in (None, 0))
    for k, c in sorted(cc.items(), key=lambda x: -x[1])[:20]:
        print('  Delta=%6d r=%d sp=%d a=%d kapnest=%s : %d' % (k[0], k[1], k[2], k[3], k[4], c))
    # and the zero-Delta events' kapnest:
    cc0 = Counter((row[2], row[3], row[4], row[7]) for row in log if row[6] in (None, 0))
    print('zero-Delta events (r,sp,a,kapnest) top10:', cc0.most_common(10))
