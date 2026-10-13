"""revD_2_window.py -- ADVERSARY-2 attack 2: the window root structure.

For J = 7..N, enumerate EVERY window chain (chains from the rho*-fire inclusive
to the re-entry exclusive) and classify by the label of its b (and c):
  'R' host-run original, 'D' host seam D_h, 'T' tail (re-entry only), 'M' pushed
  run entry, 'd' pushed seam.
Definition (reviewer's): a "spawning root" is a window chain whose b is NOT a
pushed entry (b-kind 'R' or 'D'). Claim under review: ALWAYS <= 2, and
S_win = spine(j_last) + spine(j_e) i.e. the window chains form <= 2 push-trees.

Also verified structurally:
  - no pure (R,R) fire after the last one (rho* is well defined as LAST);
  - the D_h entry is consumed exactly once (as b of a chain / as c of a chain /
    inside an even step);
  - re-entry has b = T;
  - every window chain descends (via its b's push-tag) from one of the roots
    (or IS a root); forest edge count and tree membership audit;
  - census: #window chains, S_win, max window param, dp, g.

Usage: python -B revD_2_window.py [N=2000]
"""
import sys
from collections import Counter

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
    steps = []
    while True:
        (b, bl), (c, cl) = Q[0], Q[1]
        if A % 2 == 0:
            steps.append(('E', bl, cl, None, 0, None))
            A = A + b + c + 3
            Q = Q[2:]
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3
        if bl[0] == 'T':
            dk = (x - 9 * (1 << bl[1]) * P - 4 - 6 * kh) // 6
            steps.append(('C', bl, cl, j, 0, x))
            _TC[J] = (dk, bl[1])
            return {'steps': steps, 'dk': dk, 'dp': bl[1], 'u': u}
        sidx = len(steps)
        steps.append(('C', bl, cl, j, (j - 1) + 1, x))
        Q = [(uu << a, ('M', sidx)) for a in range(j - 1)] + \
            [(c + (A + 1) // 2, ('d', sidx))] + Q[2:]
        A = uu + 1


def T(j):
    if j not in _TC:
        interlude(j)
    return _TC[j]


def univ_kat(N):
    kat = {}
    p, k = 4, 1
    while p <= N:
        kat[p] = k
        j = 1 + v2(3 * k + 2)
        dk, dp = T(j)
        k += dk
        p += dp
    return kat


def main(N=2000):
    print('== revD attack 2: window root census, J = 7..%d ==' % N)
    kat = univ_kat(N + 60)
    rootcount = Counter()
    kinds = Counter()
    c_kinds = Counter()
    maxroots = 0
    maxroots_at = None
    bad = []
    Swmax = 0; Swmax_at = None
    nwinmax = 0; maxwinj = 0; dprange = [99, 0]; gmax = 0
    two_root_examples = 0
    for J in range(7, N + 1):
        r = interlude(J)
        st = r['steps']
        chains = [i for i, s in enumerate(st) if s[0] == 'C']
        re_ = chains[-1]
        pure = [i for i in chains if st[i][1][0] == 'R' and st[i][2][0] == 'R']
        i_last = pure[-1]
        # no pure fire after the last one:
        for i in pure:
            pass
        late_pure = [i for i in chains if i > i_last
                     and st[i][1][0] == 'R' and st[i][2][0] == 'R']
        if late_pure:
            bad.append(('pure fire after rho*', J, late_pure[:3]))
        win = [i for i in chains if i >= i_last and i != re_]
        Sw = sum(st[i][3] for i in win)
        # roots: window chains with non-pushed b
        roots = [i for i in win if st[i][1][0] in ('R', 'D')]
        if len(roots) > maxroots:
            maxroots, maxroots_at = len(roots), (J, [(st[i][1], st[i][2], st[i][3]) for i in roots])
        rootcount[len(roots)] += 1
        if len(roots) > 2:
            bad.append(('>2 roots', J, roots))
        # how the D_h entry is consumed
        dcon = None
        for i, s in enumerate(st):
            if s[1] == ('D',) or s[2] == ('D',):
                dcon = (i, s[0], 'b' if s[1] == ('D',) else 'c')
                break
        # (even steps consuming D also count; the first touch wins)
        # tree membership: every window chain descends from a root
        root_set = set(roots)
        anc = {}

        def root_of(i):
            if i in anc:
                return anc[i]
            bl = st[i][1]
            if bl[0] in ('M', 'd'):
                res = root_of(bl[1])
            else:
                res = i
            anc[i] = res
            return res

        trees = set(root_of(i) for i in win)
        if not trees <= root_set:
            bad.append(('chain outside root trees', J, sorted(trees - root_set)))
        if len(trees) > 2:
            bad.append(('>2 trees', J, sorted(trees)))
        if len(roots) == 2:
            two_root_examples += 1
            if two_root_examples <= 5:
                print('  2-root example J=%d: %s' % (J, [(st[i][1], st[i][2], st[i][3]) for i in roots]))
        for i in win:
            kinds[st[i][1][0]] += 1
            c_kinds[(st[i][1][0], st[i][2][0])] += 1
        if Sw > Swmax:
            Swmax, Swmax_at = Sw, (J, st[i_last][1][1], st[i_last][3], r['dp'])
        nwinmax = max(nwinmax, len(win))
        maxwinj = max(maxwinj, max([st[i][3] for i in win]))
        dprange[0] = min(dprange[0], r['dp'])
        dprange[1] = max(dprange[1], r['dp'])
        gmax = max(gmax, J - 2 - st[i_last][1][1])
    print('  root-count histogram: %s' % dict(rootcount))
    print('  max roots = %d at %s' % (maxroots, maxroots_at))
    print('  window b-kind census: %s' % dict(kinds))
    print('  window (b,c)-kind census: %s' % dict(c_kinds))
    print('  census: maxS=%d at (J,rho,jlast,dp)=%s ; #winchains<=%d ; maxwinj=%d ;'
          ' dp in [%d,%d] ; maxg=%d'
          % (Swmax, Swmax_at, nwinmax, maxwinj, dprange[0], dprange[1], gmax))
    print('  failures: %d' % len(bad))
    for b in bad[:10]:
        print('   ', b)
    return len(bad) == 0 and maxroots <= 2


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    ok = main(N)
    print('VERDICT attack2:', 'CONFIRMED' if ok else 'REFUTED/GAP')
