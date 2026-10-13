"""revD_3_spinedec.py -- ADVERSARY-2 attack 3: spine recursion + strict decrease.

(a) Forest strict decrease: tag every pushed entry with the step index of its
    producing chain; check that for EVERY chain of the interlude reading a
    pushed b (('M',pi) or ('d',pi)), the child parameter j_child < j_parent --
    in particular at every window chain, J = 7..N.
(b) All window params < J.
(c) Tree sums vs the spine() upper bound: spine(j) = j + SigmaU(j-3) +
    2*spine(mu(j)) for j > 6, spine(<=6) = c_base = 4, where SigmaU(n) =
    4*kat[r] - r + j(r) at the last universal fire r <= n, mu(j) = 1 + floor(
    log2(3*katUB(j-3) + 6j + 13)). Check tree_sum(root) <= spine(j_root) for
    every window root, and reproduce the reported spine values
    {7:16, 8:41, 10:47, 16:56, 18:108, 26:122, 64:189, 96:256}.
(d) Spot max S_win claims: 21 at J=1539, 22 at J=3066.

Usage: python -B revD_3_spinedec.py [N=500]
"""
import sys
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


def univ(N):
    kat = {}
    fires = []
    p, k = 4, 1
    while p <= N:
        kat[p] = k
        j = 1 + v2(3 * k + 2)
        fires.append((p, k, j))
        dk, dp = T(j)
        k += dk
        p += dp
    return kat, fires


def main(N=500):
    print('== revD attack 3: strict decrease + spine recursion, J = 7..%d ==' % N)
    kat, fires = univ(N + 400)
    fps = sorted(kat)
    import bisect

    def lastfire(n):
        i = bisect.bisect_right(fps, n) - 1
        return fps[i] if i >= 0 else None

    def SigmaU(n):
        r = lastfire(n)
        if r is None or r < 4:
            return 0
        k = kat[r]
        return 4 * k - r + (1 + v2(3 * k + 2))

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

    # mu(j) < j for all j >= 7 (the strict-decrease constant)?
    bad_mu = [j for j in range(7, 400) if mu_in(j) >= j]
    print('  mu(j) < j for j in 7..399: %s (violations: %s)' % (not bad_mu, bad_mu[:5]))
    tbl = {x: spine(x) for x in (7, 8, 10, 16, 18, 26, 64, 96)}
    rep = {7: 16, 8: 41, 10: 47, 16: 56, 18: 108, 26: 122, 64: 189, 96: 256}
    print('  spine table mine  : %s' % tbl)
    print('  spine table report: %s   match: %s' % (rep, tbl == rep))

    edge_viol = []       # (J, child, parent, j_child, j_parent)
    winparam_viol = []
    treesum_viol = []
    worst_slack = None
    n_windows = 0
    for J in range(7, N + 1):
        r = interlude(J)
        st = r['steps']
        chains = [i for i, s in enumerate(st) if s[0] == 'C']
        re_ = chains[-1]
        pure = [i for i in chains if st[i][1][0] == 'R' and st[i][2][0] == 'R']
        i_last = pure[-1]
        win = [i for i in chains if i >= i_last and i != re_]
        # (a) strict decrease on every forest edge of the whole interlude
        for i in chains:
            bl = st[i][1]
            if bl[0] in ('M', 'd'):
                pi = bl[1]
                if st[i][3] >= st[pi][3]:
                    edge_viol.append((J, i, pi, st[i][3], st[pi][3]))
        # (b) window params < J
        for i in win:
            if st[i][3] >= J:
                winparam_viol.append((J, i, st[i][3]))
        # (c) tree sums <= spine(j_root)
        anc = {}

        def root_of(i):
            if i in anc:
                return anc[i]
            bl = st[i][1]
            res = root_of(bl[1]) if bl[0] in ('M', 'd') else i
            anc[i] = res
            return res

        tsum = {}
        for i in win:  # accumulate each chain's j into its root's tree
            rt = root_of(i)
            tsum[rt] = tsum.get(rt, 0) + st[i][3]
        n_windows += 1
        for rt, s in tsum.items():
            jr = st[rt][3]
            if jr <= 6:
                continue  # base case handled by c_base
            ub = spine(jr)
            if worst_slack is None or ub - s < worst_slack[0]:
                worst_slack = (ub - s, J, jr, s, ub)
            if s > ub:
                treesum_viol.append((J, rt, jr, s, ub))
    print('  forest-edge strict decrease violations (whole interlude): %d' % len(edge_viol))
    if edge_viol:
        print('    first: %s' % (edge_viol[:5],))
    print('  window-param >= J violations: %d' % len(winparam_viol))
    print('  tree-sum > spine(j_root) violations: %d (windows checked: %d)'
          % (len(treesum_viol), n_windows))
    if treesum_viol:
        print('    first: %s' % (treesum_viol[:5],))
    print('  worst tree-sum slack (spine_ub - sum): %s' % (worst_slack,))
    # (d) S_win spot claims
    for J, claim in ((1539, 21), (3066, 22)):
        r = interlude(J)
        st = r['steps']
        chains = [i for i, s in enumerate(st) if s[0] == 'C']
        re_ = chains[-1]
        pure = [i for i in chains if st[i][1][0] == 'R' and st[i][2][0] == 'R']
        i_last = pure[-1]
        Sw = sum(st[i][3] for i in chains if i >= i_last and i != re_)
        print('  S_win(%d) = %d (report %d) %s' % (J, Sw, claim, 'OK' if Sw == claim else 'DIFF'))
    ok = (not edge_viol) and (not winparam_viol) and (not treesum_viol) \
        and (not bad_mu) and tbl == rep
    print('VERDICT attack3:', 'CONFIRMED' if ok else 'REFUTED/GAP')
    return ok


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    main(N)
