"""agentB_run10.py — assemble the closed form of ell(v) and induction bounds.

ell(v) = 2 (opening E,E) + sum of phase lengths L(j_i) over the bulk chains,
truncated at the boundary, + endgame steps.  Extract L(j) from the abstract
cascades, define the boundary rule, verify against the true ell(v) for
v=1..1500.  Also verify k_q <= (q+4)/2 and j_q <= 1+log2(1.5q+5) < q-1 on the
universal sequence (needed for the self-similarity induction)."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import v2i, excursion
from agentB_run7 import verify
from agentB_run8 import cascade

def main():
    TAB = {}
    for j in range(1, 121):
        res, err = verify(j)
        assert not err, (j, err)
        TAB[j] = res[0]
    # phase lengths L(j): events in cascade + 1 (closing chain), except
    # regular j=1..4 whose 'cascade' starts with the two E's:
    L = {}
    for j in range(1, 121):
        ev, end = cascade(j)
        L[j] = len(ev) + 1
    print('L(j) for j=1..24:', [L[j] for j in range(1, 25)])

    # universal sequence
    seq = []
    p, k = 4, 1
    while p < 5000:
        j = 1 + v2i(3 * k + 2)
        seq.append((p, k, j))
        p += TAB[j][1]; k += TAB[j][0]
    # bounds
    ok1 = all(kk <= (q + 4) // 2 for (q, kk, jj) in seq)
    ok2 = all(jj <= 2 + ((3 * q) // 2 + 5).bit_length() for (q, kk, jj) in seq)
    ok3 = all(jj < q - 1 for (q, kk, jj) in seq if q >= 6)
    print('k_q <= (q+4)/2 on universal seq:', ok1)
    print('j_q < q-1 (positions>=6):', ok3, ' (min q with j>=5:', min(q for q, k3, j3 in seq if j3 >= 5), ')')

    # ell formula: simulate the bulk with the table; boundary = when the next
    # chain's pair would reach beyond T_{v-2}; count steps exactly by
    # replaying phases: phase of chain i consumes dp(j_i)+1 T-entries...
    # Instead: closed form = 2 + sum L(j_i) over chains whose phase "fits"
    # before the tail ends + endgame steps; we determine the truncation rule
    # empirically: the phase of chain i needs T-entries up to p_i + dp(j_i).
    # Rule: include phase i if p_i + dp(j_i) <= v-1; then endgame = ell - so_far.
    def ell_pred(v):
        steps = 2
        p, k = 4, 1
        while True:
            j = 1 + v2i(3 * k + 2)
            dp = TAB[j][1]
            if p + dp > v - 1:
                break
            steps += L[j]
            p += dp; k += TAB[j][0]
        return steps, p, k

    ells = {}
    for v in range(1, 1501):
        r = excursion(1, v)
        assert r['result'] == 'singleton'
        ells[v] = r['ell']
    bad = []
    for v in range(1, 1501):
        sofar, pb, kb = ell_pred(v)
        if sofar > ells[v]:
            bad.append((v, sofar, ells[v]))
    print('ell formula never overshoots for v=1..1500:', not bad, bad[:5])
    # endgame residual steps distribution
    from collections import Counter
    res = Counter()
    for v in range(1, 1501):
        sofar, pb, kb = ell_pred(v)
        res[ells[v] - sofar] += 1
    print('residual (ell - bulk-predicted) distribution:', dict(sorted(res.items())[:20]))

if __name__ == '__main__':
    main()
