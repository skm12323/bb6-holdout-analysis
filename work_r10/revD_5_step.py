"""revD_5_step.py -- ADVERSARY-2 attack 5: the induction-step arithmetic.

Recompute both routes at J = 3201, 1e6, 2^64 and on a dense grid:
  target(J, rho*) = 4*Phi(rho*) + 3*(J - rho*) - 4      [report's (I4) form]
  case (a) rho* >= 3000 : Phi >= 1664 (exhaustive to 1e6; counting bound beyond)
  case (b) rho* <= 2999 : J >= 3201 => J - rho* >= 202, Phi >= 3
Route EL: dp + S_win <= 66 (measured max 28).
Route PIN: S_win <= 2*spine(mu*), mu* = 1 + floor(log2(18J+283));
  sub-route (i) dp <= 6 [measured]; sub-route (ii) structural
  dp <= 2 + g + 2*S_win + mu*  =>  dp + S_win <= 2 + g + 3*Sbound + mu*,
  case-(b) target = 3g + 14.
Also: agentA counting-bound constants recomputed (eps, slabs, seam), and the
beyond-1e6 coverage of Phi >= 1664 via the counting bound.

Usage: python -B revD_5_step.py
"""
import sys
import json
from math import log2
from functools import lru_cache

def v2(x): return (x & -x).bit_length() - 1

_TC = {}


def interlude(J, p_extra=60, tail=90):
    mod = 1 << J
    kh = ((1 << (J - 1)) - 2) * pow(3, -1, mod) % mod
    p = J + p_extra
    P = 1 << p
    x0 = 9 * P + 6 * kh + 4
    u = x0 >> J
    A = u + 1
    Q = [(u << a, ('R', a)) for a in range(J - 1)]
    Q.append((15 * P // 2 + 3 * kh + 1, ('D',)))
    Q += [(3 * (1 << e) * P, ('T', e)) for e in range(2, tail)]
    while True:
        (b, bl), (c, cl) = Q[0], Q[1]
        if A % 2 == 0:
            A = A + b + c + 3
            Q = Q[2:]
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3
        if bl[0] == 'T':
            _TC[J] = ((x - 9 * (1 << bl[1]) * P - 4 - 6 * kh) // 6, bl[1])
            return _TC[J]
        Q = [(uu << a, ('M',)) for a in range(j - 1)] + \
            [(c + (A + 1) // 2, ('d',))] + Q[2:]
        A = uu + 1


def T(j, tab):
    if j in tab:
        return tab[j]
    if j not in _TC:
        interlude(j)
    return _TC[j]


def main():
    tab = {}
    for fn in ('agentD_table_cpt.json', 'agentD_table5100.json'):
        d = json.load(open(fn))
        for k_, v in d.items():
            tab[int(k_)] = tuple(v)
    # universal kat for SigmaU
    kat = {}
    p, k = 4, 1
    while p <= 100000:
        kat[p] = k
        j = 1 + v2(3 * k + 2)
        dk, dp = T(j, tab)
        k += dk
        p += dp
    fps = sorted(kat)
    import bisect

    def lastfire(n):
        i = bisect.bisect_right(fps, n) - 1
        return fps[i] if i >= 0 else None

    def SigmaU(n):
        r = lastfire(n)
        if r is None or r < 4:
            return 0
        kk = kat[r]
        return 4 * kk - r + (1 + v2(3 * kk + 2))

    def KAT(n):
        r = lastfire(n)
        return kat[r] if r is not None else 1

    def mu_in(j):
        return 1 + int(log2(3 * KAT(max(3, j - 3)) + 6 * j + 13))

    @lru_cache(maxsize=None)
    def spine(j, c_base=4):
        if j <= 6:
            return c_base
        return j + SigmaU(j - 3) + 2 * spine(mu_in(j))

    def mustar(J):
        return 1 + int(log2(18 * J + 283))

    def Sbound(J):
        return 2 * spine(mustar(J))

    print('== revD attack 5: step arithmetic ==')
    EL = 66
    PhiA, ZB, JT = 1664, 3000, 3200
    tgt_a = 4 * PhiA - 4            # J-rho* >= 0 (most conservative)
    tgt_a_min = 4 * PhiA + 3 * 3 - 4  # with rho* <= J-3
    tgt_b = 3 * (JT + 1 - ZB) + 4 * 3 - 4
    print('  EL route: case(a) target >= %d (report 6652; with J-rho*>=3: %d);'
          ' case(b) target >= %d (report says 614 and 611 in different places)'
          % (tgt_a, tgt_a_min, tgt_b))
    print('    EL=66 <= min(%d,%d): %s' % (tgt_a, tgt_b, EL <= min(tgt_a, tgt_b)))
    # PIN route
    print('  PIN route: spine values used: 16:%d 18:%d 26:%d 64:%d 96:%d'
          % (spine(16), spine(18), spine(26), spine(64), spine(96)))
    grid = [3201, 3202, 3210, 3250, 3300, 3400, 3500, 4000, 5000, 6000, 8000,
            10000, 20000, 100000, 10**6, 10**8, 10**12, 2**40, 2**64] + \
           [2**e for e in range(13, 64, 7)]
    worst_i = None; worst_ii = None; worst_a = None
    print('   J      mu*  Sbd   | (i) dp<=6: lhs tgt slack | (ii) struct: lhs tgt slack | case(a) struct slack')
    for J in sorted(set(grid)):
        g = J - 2 - (ZB - 1)         # case (b): rho* <= ZB-1
        S = Sbound(J)
        mus = mustar(J)
        lhs_i = S + 6
        tgt_i = 3 * g + 14 - 2 + 2   # = 4*3 + 3*(g+2) - 4 ; g+2 = J - rho*
        tgt_i = 4 * 3 + 3 * (J - (ZB - 1)) - 4
        lhs_ii = 2 + g + 3 * S + mus
        tgt_ii = 3 * g + 14
        sl_i = tgt_i - lhs_i
        sl_ii = tgt_ii - lhs_ii
        if worst_i is None or sl_i < worst_i[0]:
            worst_i = (sl_i, J)
        if worst_ii is None or sl_ii < worst_ii[0]:
            worst_ii = (sl_ii, J)
        # case (a) with structural dp: rho* >= ZB, Phi >= PhiA, g >= 1
        lhs_a = 2 + 1 + 3 * S + mus
        tgt_aJ = 4 * PhiA + 3 * 1 - 4
        sl_a = tgt_aJ - lhs_a
        if worst_a is None or sl_a < worst_a[0]:
            worst_a = (sl_a, J)
        if J in (3201, 10**6, 2**64):
            print('  %-18d %-3d %-4d | %4d %4d %+5d | %4d %4d %+5d | %+6d'
                  % (J, mus, S, lhs_i, tgt_i, sl_i, lhs_ii, tgt_ii, sl_ii, sl_a))
    print('  worst slack (i) dp<=6+spine : %d at J=%d' % worst_i)
    print('  worst slack (ii) structural : %d at J=%d   [report: +60 at J=3201]' % worst_ii)
    print('  worst slack case(a) struct  : %d at J=%d' % worst_a)
    # dense grid 3201..20000
    bad = [J for J in range(3201, 20001)
           if 3 * (J - 2 - (ZB - 1)) + 14 < 2 + (J - 2 - (ZB - 1)) + 3 * Sbound(J) + mustar(J)]
    print('  dense grid 3201..20000 structural-route failures: %d' % len(bad))
    # ---- agentA counting bound, recomputed ----
    eps = sum(tab.get(5 + t, (5 + t,))[0] / (1 << (t + 1)) for t in range(0, 3000))
    ok_slabs = True; worst_post = None
    for t in range(9, 1020):
        s = float(1 << t)
        Kc = (t + 1) * (t + 10) // 2
        B = 16 + 18 * s - (17 / 8) * (eps * s + Kc)
        post = B - (5 + t + 2)
        if worst_post is None or post < worst_post[0]:
            worst_post = (post, t)
        if post < 3:
            ok_slabs = False
    t = 1019; Kc = (t + 1) * (t + 10) // 2
    seam = 16 + (18 - 17 / 8 * 6) * float(1 << t) - (17 / 8) * Kc - (t + 7)
    print('  counting bound: eps=%.4f; worst post-spike bound %.1f at slab t=%d;'
          ' all slabs 2^9..2^1020 >= 3: %s; seam(t=1019)=%.1f'
          % (eps, worst_post[0], worst_post[1], ok_slabs, seam))
    # beyond 1e6: Phi >= 1664 via counting bound?
    # s at p=1e6 from the walk: use kat at last fire <= 1e6
    p_, k_ = fps[-1], kat[fps[-1]]
    print('  walk: last fire <= 1e6 at p=%d k=%d -> block s=(k-10)/16=%d'
          % (p_, k_, (k_ - 10) // 16))
    for s in ((k_ - 10) // 16, 10 * ((k_ - 10) // 16), 2**40):
        tt = s.bit_length()
        Kc = (tt + 1) * (tt + 10) // 2
        B = 16 + 11.2695 * s - 6860
        V = B - (5 + log2(3 * s + 2))
        print('    s=%d: B~%.0f, V~%.0f >= 1664: %s' % (s, B, V, V >= 1664))
    ok = (EL <= min(tgt_a, tgt_b)) and worst_i[0] >= 0 and worst_ii[0] >= 0 \
        and worst_a[0] >= 0 and not bad and ok_slabs
    print('VERDICT attack5:', 'CONFIRMED' if ok else 'REFUTED/GAP')


if __name__ == '__main__':
    main()
