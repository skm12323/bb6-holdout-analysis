"""work_r10/residue_inv.py — track the head-deficit decomposition
   delta(head) = J_enc - 2k + R
where J_enc = parameter of the enclosing chain (the chain that pushed the current
front run; the spike for a spike interlude), k = run pairs absorbed since that chain,
and R = the residue.  Goal: find R's exact transition law; conjecture R <= 2.

Also tracks, for every live stack entry, delta(v) - (J_enc(v) + 2) <= 0 violations,
with J_enc(v) = the producer chain's j (recorded in an extended tag).
"""
import sys, collections
sys.path.insert(0, r'D:\math_cc\work_r10')
import fast_walker as FW

def run(N):
    # entries: [v, r, l, tag]; tag = ('E', a) | ('M', s, jprod) | ('D', s, jprod)
    A = (0, 1, 1, None)         # (v2, residue, lA, jprod-of-last-absorbed-mix?) — head handled separately
    P = []
    i = 0; s = 0
    J_enc = 0                   # enclosing chain parameter (0 = start)
    k = 0                       # pairs absorbed since the enclosing chain (climb credits)
    R = 0                       # residue: delta(head) - (J_enc - 2k)
    Rtrans = collections.Counter()
    Rmax = -10**9; Rmax_at = None
    viol = []                   # stack entries with delta > Jprod + 2
    while i <= N:
        if len(P) >= 2:
            (vb, rb, lb, tb) = P[0]; (vc_, rc_, lc_, tc_) = P[1]
        elif len(P) == 1:
            (vb, rb, lb, tb) = P[0]; (vc_, rc_, lc_, tc_) = (i, 1, 0, ('E', i))
        else:
            (vb, rb, lb, tb) = (i, 1, 0, ('E', i)); (vc_, rc_, lc_, tc_) = (i + 1, 1, 0, ('E', i + 1))
        # current head deficit
        dA = i - A[0]
        cpar = 0 if A[0] >= 1 else (A[1] & 1)
        if (cpar + A[2]) % 2 == 0:
            t1 = FW.cadd((A[0], A[1]), (vb, rb)); cA = FW.cadd(t1, (vc_, rc_))
            A = (cA[0], cA[1], A[2] + lb + lc_ + 3)
            newp = []
            # climb bookkeeping: absorbing a pure pair of the enclosing run (tags M,same
            # producer, consecutive t) => k += 1.  Detect via equal producers of b,c.
            same = (tb[0] == 'M' and tc_[0] == 'M' and tb[1] == tc_[1])
            if same: k += 1
            # else: mixed absorption (D or originals) — k unchanged; J_enc unchanged
        else:
            tx = FW.cadd((A[0], A[1]), (vb + 1, rb))
            lx = A[2] + 2 * lb + 3
            vcx, rcx = tx; j = FW.v2i(lx)
            vu = vcx - j; ru = rcx; lu = lx >> j
            tD = FW.cadd((vc_, rc_), (A[0] - 1, A[1]))
            lD = lc_ + (A[2] + 1) // 2
            newp = [[vu + t, ru, lu << t, ('M', s, j)] for t in range(j - 1)] + \
                   [[tD[0], tD[1], lD, ('D', s, j)]]
            A = (vu, ru, lu + 1)
            # new enclosing chain
            J_enc = j; k = 0
        k2 = len(P)
        if k2 >= 2: P = P[2:]
        else: i += 2 - k2; P = []
        P = newp + P; s += 1
        # residue update
        dA = i - A[0]
        Rn = dA - (J_enc - 2 * k)
        if Rn != R:
            Rtrans[Rn - R] += 1
            R = Rn
        if R > Rmax:
            Rmax = R; Rmax_at = (i, s, J_enc, k, dA)
        # stack-entry invariant: delta(v) <= jprod(v) + 2
        for p in P[2:]:
            if p[3][0] in ('M', 'D'):
                dv = i - p[0]
                if dv > p[3][2] + 2:
                    viol.append((i, s, p[3], dv))
                    if len(viol) > 5: break
        if len(viol) > 5: break
    return Rmax, Rmax_at, Rtrans, viol[:6], R

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    Rmax, at, tr, viol, Rf = run(N)
    print('head residue R = delta - (J_enc - 2k): max R = %d at (i,s,J_enc,k,delta)=%s' % (Rmax, at))
    print('R transitions (delta_R -> count):', dict(sorted(tr.items())))
    print('stack-entry violations (delta > jprod+2): %d' % len(viol), viol)
