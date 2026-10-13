"""revB2_walk.py -- task 5: cross-check against the REAL universal walk.

Runs work_r10/fast_walker.py (audited, residue arithmetic) to i = 1e5, and an
INDEPENDENT exact big-int walker of the formal map F (same semantics, written
from scratch by the auditor) over the same range. Checks:
  - level-fire streams (rho, k, j) of the two walkers agree (my impl = audited impl);
  - every chain whose b is a 'D'-tagged (pushed seam) entry satisfies
    j <= J_enclosing - 2, where J_enclosing = parameter of the most recent
    level fire (b tagged 'E') -- the walk-level analogue of j_D <= m-2;
  - measured conservation constant max k/rho.
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\work_r10')
from fast_walker import fast_walker
from collections import Counter, defaultdict


def v2(x):
    return (x & -x).bit_length() - 1


def my_exact_walk(N):
    """Exact walker of the formal map F (work_g6 sect.5): A=(c,l), queue of
    (c,l,tag) pushed entries followed by originals E_a=(2^a,0), a>=i."""
    A = (1, 1); P = []; i = 0; s = 0
    lvl = []; Dfires = []
    Jenc = None
    while i <= N:
        if len(P) >= 2:
            (cb, lb, tb), (cc, lc, tc) = P[0], P[1]
        elif len(P) == 1:
            (cb, lb, tb) = P[0]; (cc, lc, tc) = (1 << i, 0, ('E', i))
        else:
            (cb, lb, tb) = (1 << i, 0, ('E', i)); (cc, lc, tc) = (1 << (i + 1), 0, ('E', i + 1))
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb + cc, A[1] + lb + lc + 3); newp = []
        else:
            cx = A[0] + 2 * cb; lx = A[1] + 2 * lb + 3
            vc, vl = v2(cx), v2(lx)
            assert vl < vc, ('margin S1 fails', i, s, vl, vc)
            assert A[0] % 2 == 0 and A[1] % 2 == 1, ('parity invariant', i, s)
            j = vl
            u = (cx >> j, lx >> j)
            assert u[0] % 2 == 0 and u[0] >= 2 and u[1] % 2 == 1 and u[1] >= 1
            if tb[0] == 'D':
                Dfires.append((i, s, j, Jenc, j <= Jenc - 2))
            if tb[0] == 'E':
                # level fire (b is an original E: pushed queue must be empty)
                assert len(P) == 0, ('level fire with nonempty pushed queue', i, s)
                assert vc == tb[1] and cx == 3 * (1 << tb[1]) and (lx - 4) % 6 == 0 \
                    and s % 2 == 0 and lx == 3 * s + 4, ('I(rho) fails', tb[1], s)
                lvl.append((tb[1], s // 2, j))
                Jenc = j
            newp = [(u[0] << t, u[1] << t, ('M', s)) for t in range(j - 1)] + \
                   [(cc + A[0] // 2, lc + (A[1] + 1) // 2, ('D', s))]
            A = (u[0], u[1] + 1)
        k = len(P)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k; P = []
        P = newp + P
        s += 1
    return lvl, Dfires, (i, s)


t0 = time.time()
lvl_mine, Dfires, fin = my_exact_walk(100000)
t1 = time.time()
st = fast_walker(100000, collect_lvl=True)
t2 = time.time()
print('my exact walker: %d level fires, %d D-fires, final (i,s)=%s [%.1fs]'
      % (len(lvl_mine), len(Dfires), fin, t1 - t0))
print('audited fast_walker: %d level fires, %d chains [%.1fs]'
      % (len(st['lvl']), st['chains'], t2 - t1))
assert lvl_mine == st['lvl'], 'level-fire stream mismatch between walkers'
print('CROSS-CHECK OK: identical (rho, k, j) level-fire streams to i=1e5')

bad = [d for d in Dfires if not d[4]]
print('D-tagged-b fires: %d ; violations of j <= J_enc-2: %d' % (len(Dfires), len(bad)))
for b in bad[:10]:
    print('   ', b)
marg = Counter(Jenc - 2 - j for (i_, s_, j, Jenc, ok) in Dfires)
print('margin (J_enc - 2 - j) distribution:', dict(sorted(marg.items())))
byJ = defaultdict(Counter)
for (i_, s_, j, Jenc, ok) in Dfires:
    byJ[Jenc][j] += 1
print('D-fire j distribution per enclosing level-fire parameter J:')
for J in sorted(byJ):
    print('   J=%2d : n=%d  j-distribution %s  max j=%d <= J-2=%d'
          % (J, sum(byJ[J].values()), dict(sorted(byJ[J].items())),
             max(byJ[J]), J - 2))
# level-fire parameters that occur at all
Js = Counter(j for (_, _, j) in lvl_mine)
print('level-fire parameter values seen (walk to i=1e5):', dict(sorted(Js.items())))
# conservation constant
mr = max(k / rho for (rho, k, j) in lvl_mine if rho >= 100)
mr_all = max(k / rho for (rho, k, j) in lvl_mine)
print('max k/rho (all fires) = %.4f ; (rho>=100) = %.4f' % (mr_all, mr))
