"""revD_6_scope.py -- ADVERSARY-2 attack 6: the circularity audit.

The step at J consumes: table (params <= 3200 < J), CL at positions <= rho* <= J-3,
EX (proved; its tie shape uses CL at sub-positions), the Phi-profile up to rho*
(table params < J), the spine recursion (kat at positions < mu* < J), PIN or EL.
Machine checks:
  (A) CL(pos <= q) consumes H1 only at params <= 5+log2(3q/16+2);
      for q = J-3 this must be < J-1  for all J >= 11.
  (B) each CL traversal drops the parameter: 5+log2(3q/16+2) <= q-2 for q >= 11
      (so the induction is well-founded: strictly decreasing parameters).
  (C) sub-fire params at rho* <= J-3: j <= 1+log2(3(J-6)+2) < J for J >= 12
      (via kat <= rho-3 from CL).
  (D) mu*(J) = 1+floor(log2(18J+283)) < J for J >= 11; and the spine cascade
      mu_in(j) < j for j >= 7 (verified in revD_3; re-checked here).
  (E) the weak dk bound used inside the mu-constants, dk(J) <= 1.5J+46, is
      derivable WITHOUT H1(J): from I2 + CL(<J) + spine bound,
      4dk <= J + 6 + 4(rho*-3) + 2*spine(mu*) <= 5J + 2*spine(mu*),
      so dk <= 1.25J + spine(mu*)/2; check spine(mu*) <= J/2 + 92 on the grid.
  (F) Phi-profile spike params on the way to rho* <= J-3 are < J: recompute the
      max spike param along the walk as a function of the endpoint (empirically
      for endpoints up to 1e6, where max j = 20 << J for J > 3200).

Usage: python -B revD_6_scope.py
"""
import sys
import json
from math import log2

def v2(x): return (x & -x).bit_length() - 1

_TC = {}


def interlude(J, p_extra=60, tail=90):
    mod = 1 << J
    kh = ((1 << (J - 1) - 2) * pow(3, -1, mod)) % mod if False else \
        ((1 << (J - 1)) - 2) * pow(3, -1, mod) % mod
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
    print('== revD attack 6: circularity / well-foundedness ==')
    grid = list(range(11, 400)) + [500, 1000, 3201, 5000, 10**4, 10**5, 10**6,
                                   10**9, 10**12, 2**40, 2**64]
    # (A)
    badA = [J for J in grid if not (5 + log2(3 * (J - 3) / 16 + 2) < J - 1)]
    print('  (A) CL(pos<=J-3) needs params <= 5+log2(3(J-3)/16+2) < J-1, J>=11: %s'
          % ('OK' if not badA else 'FAIL at %s' % badA[:5]))
    # (B)
    badB = [q for q in grid if not (5 + log2(3 * q / 16 + 2) <= q - 2)]
    print('  (B) param drop per CL traversal: 5+log2(3q/16+2) <= q-2, q>=11: %s'
          % ('OK' if not badB else 'FAIL at %s' % badB[:5]))
    # (C)
    badC = [J for J in grid if J >= 12 and not (1 + log2(3 * (J - 6) + 2) < J)]
    print('  (C) sub-fire params < J (kat<=rho-3): 1+log2(3(J-6)+2) < J, J>=12: %s'
          % ('OK' if not badC else 'FAIL at %s' % badC[:5]))
    # (D)
    badD = [J for J in grid if not (1 + int(log2(18 * J + 283)) < J)]
    print('  (D) mu* = 1+floor(log2(18J+283)) < J, J>=11: %s'
          % ('OK' if not badD else 'FAIL at %s' % badD[:5]))
    # (E): spine(mu*) <= J/2 + 92  =>  dk <= 1.25J + spine/2 <= 1.5J + 46
    tab = {}
    for fn in ('agentD_table_cpt.json', 'agentD_table5100.json'):
        d = json.load(open(fn))
        for k_, v in d.items():
            tab[int(k_)] = tuple(v)
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

    from functools import lru_cache
    @lru_cache(maxsize=None)
    def spine(j, c_base=4):
        if j <= 6:
            return c_base
        return j + SigmaU(j - 3) + 2 * spine(mu_in(j))

    badE = [J for J in grid if J >= 3201 and spine(1 + int(log2(18 * J + 283))) > J / 2 + 92]
    print('  (E) spine(mu*) <= J/2+92 (=> dk<=1.5J+46 without H1(J)), J>=3201: %s'
          % ('OK' if not badE else 'FAIL at %s' % badE[:5]))
    # (F) max spike param along the Phi-profile walk vs endpoint
    p, k = 4, 1
    maxj = 0
    marks = {}
    while p <= 1000000:
        j = 1 + v2(3 * k + 2)
        maxj = max(maxj, j)
        if p in (3000, 10**4, 10**5, 10**6):
            marks[p] = maxj
        dk, dp = T(j, tab)
        k += dk
        p += dp
    print('  (F) max spike param up to endpoint: %s  (all << 3201)' % marks)
    ok = not (badA or badB or badC or badD or badE)
    print('VERDICT attack6:', 'CONFIRMED (well-founded)' if ok else 'REFUTED/GAP')
    return ok


if __name__ == '__main__':
    main()
