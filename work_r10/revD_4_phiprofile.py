"""revD_4_phiprofile.py -- ADVERSARY-2 attack 4: the Phi-profile.

Recompute Phi(p) = p - kat(p) on the universal walk with the certified table
(agentD_table_cpt.json for j in 121..3200, agentD_table5100.json for 5001..5200,
THIS reviewer's independent concrete tracer for j <= 120; engine agreement with
the cpt table is verified separately in revD_7). Walk from (p,k) = (4,1) to
p = 1e6. Questions:
  - Phi >= 1664 on [3000, 1e6]?  where is the minimum of that zone?
  - Phi >= 2750 on [4958, 1e6] (the older threshold claim)?
  - Phi_min = 3 only at p = 4; Phi >= 16 for p >= 26?
Phi is evaluated at EVERY integer position via the last-fire kat (between two
fires kat is constant and p grows, so minima sit at fire positions or at the
zone's left edge).

Usage: python -B revD_4_phiprofile.py [PMAX=1000000]
"""
import sys
import bisect

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
    steps = 0
    while True:
        (b, bl), (c, cl) = Q[0], Q[1]
        if A % 2 == 0:
            steps += 1
            A = A + b + c + 3
            Q = Q[2:]
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3
        if bl[0] == 'T':
            dk = (x - 9 * (1 << bl[1]) * P - 4 - 6 * kh) // 6
            _TC[J] = (dk, bl[1])
            return (dk, bl[1])
        steps += 1
        Q = [(uu << a, ('M',)) for a in range(j - 1)] + \
            [(c + (A + 1) // 2, ('d',))] + Q[2:]
        A = uu + 1


def T(j, tab):
    if j in tab:
        return tab[j]
    if j not in _TC:
        interlude(j)
    return _TC[j]


def main(PMAX=1000000):
    print('== revD attack 4: Phi-profile to p=%g with certified table ==' % float(PMAX))
    tab = {}
    for fn in ('agentD_table_cpt.json', 'agentD_table5100.json'):
        d = __import__('json').load(open(fn))
        for k_, v in d.items():
            tab[int(k_)] = tuple(v)
    print('  table: %d entries (121..3200 + 5001..5200) + own tracer below 121' % len(tab))
    fires = []
    p, k = 4, 1
    maxj = 0
    while p <= PMAX:
        j = 1 + v2(3 * k + 2)
        maxj = max(maxj, j)
        fires.append((p, k, j))
        dk, dp = T(j, tab)
        k += dk
        p += dp
    ps = [f[0] for f in fires]
    print('  fires: %d ; last p=%d ; max spike param encountered j=%d' % (len(fires), ps[-1], maxj))
    print('  (all table lookups satisfied by j<=%d : %s)' % (maxj, maxj <= 3200))

    def kat_at(n):
        i = bisect.bisect_right(ps, n) - 1
        return fires[i][1] if i >= 0 else None

    def Phi_min_zone(lo, hi):
        # min over positions in [lo, hi]: value at lo, then at each fire in zone
        best = None
        where = None
        kl = kat_at(lo)
        if kl is not None:
            best, where = lo - kl, lo
        else:
            best = float('inf')
        for (fp, fk, fj) in fires:
            if fp < lo:
                continue
            if fp > hi:
                break
            if fp - fk < best:
                best, where = fp - fk, fp
        return best, where

    for lo, hi, claim in ((0, PMAX, 'min=3 only at p=4'),
                          (26, PMAX, '>=16'),
                          (3000, PMAX, '>=1664'),
                          (4958, PMAX, '>=2750')):
        m, w = Phi_min_zone(lo, hi)
        print('  zone [%d, %d]: min Phi = %d at p=%d   [claim: %s]' % (lo, hi, m, w, claim))
    # worst spike-exit drop check (context): min of Phi just AFTER a spike fire
    # (position p+dp of a spike) -- the true cycle minima
    m = None; w = None
    for idx, (fp, fk, fj) in enumerate(fires):
        if fj >= 5 and idx + 1 < len(fires):
            np_, nk_, _ = fires[idx + 1]
            if m is None or nk_ - 0 < m:
                pass
            val = np_ - nk_
            if m is None or val < m:
                m, w = val, (fp, fj, np_)
    print('  min Phi at first position after a spike exit: %d at (spike p=%d j=%d, next p=%d)' % (m, w[0], w[1], w[2]))


if __name__ == '__main__':
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    main(PMAX)
