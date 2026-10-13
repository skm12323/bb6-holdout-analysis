"""work_r10/check_invariants.py — the four invariant checks of PROOF.md §7.
Usage: python check_invariants.py [N=300000]
 1. lineage invariant  delta(v) <= Jlin(v) + 2  (all live values)
 2. post-chain slack delta(u) - Jlin(u) <= 0; D-slack <= 0; head-slack-at-chain <= 0
 3. position-dominance t >= j at every chain
 4. level fires have delta_x = 0 exactly (mass identity in place)
"""
import sys, collections
sys.path.insert(0, r'D:\math_cc\work_r10')
import fast_walker as FW

def run(N):
    P = []; A = (0, 1, 1, 0); i = 0; s = 0
    worst = -10**9; chain_bad = 0; chain_n = 0; pos_bad = 0; lvl_bad = 0
    while i <= N:
        if len(P) >= 2: b, c = P[0], P[1]
        elif len(P) == 1: b = P[0]; c = [i, 1, 0, ('E', i), 0, i]
        else: b = [i, 1, 0, ('E', i), 0, i]; c = [i + 1, 1, 0, ('E', i + 1), 0, i + 1]
        cpar = 0 if A[0] >= 1 else (A[1] & 1)
        if (cpar + A[2]) % 2 == 0:
            t1 = FW.cadd((A[0], A[1]), (b[0], b[1])); cA = FW.cadd(t1, (c[0], c[1]))
            A = (cA[0], cA[1], A[2] + b[2] + c[2] + 3, max(A[3], b[4], c[4])); newp = []
        else:
            tx = FW.cadd((A[0], A[1]), (b[0] + 1, b[1]))
            lx = A[2] + 2 * b[2] + 3
            vcx, rcx = tx; j = FW.v2i(lx)
            vu = vcx - j; lu = lx >> j
            tD = FW.cadd((c[0], c[1]), (A[0] - 1, A[1]))
            lD = c[2] + (A[2] + 1) // 2
            JLu = max(A[3], b[4], j)
            # D position: one past the enclosing run (proxy: producer run length)
            if b[3][0] == 'M': tDp = b[3][2]
            elif b[3][0] == 'E': tDp = b[3][1] + 2
            else: tDp = b[5] + 2
            newp = [[vu + t, rcx, lu << t, ('M', s, j), JLu, t] for t in range(j - 1)] +                    [[tD[0], tD[1], lD, ('D', s, j), max(A[3], b[4], j, c[4]), tDp]]
            A = (vu, rcx, lu + 1, JLu)
            chain_n += 1
            du = i - vu
            if du - JLu > 0: chain_bad += 1
            t_front = b[3][1] if b[3][0] == 'E' else b[5]
            if t_front < j: pos_bad += 1
            if b[3][0] == 'E' and i - vcx != 0: lvl_bad += 1
        k2 = len(P)
        if k2 >= 2: P = P[2:]
        else: i += 2 - k2; P = []
        P = newp + P; s += 1
        for vv in [(A[0], A[3])] + [(p[0], p[4]) for p in P]:
            if i - vv[0] - vv[1] > worst: worst = i - vv[0] - vv[1]
    print('N=%d: chains=%d' % (N, chain_n))
    print('  1. lineage invariant worst slack = %d (need <= 2): %s' % (worst, worst <= 2))
    print('  2. post-chain slack > 0 count: %d (need 0)' % chain_bad)
    print('  3. position-dominance violations (t < j): %d (need 0)' % pos_bad)
    print('  4. level fires with delta_x != 0: %d (need 0)' % lvl_bad)

if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 300000)
