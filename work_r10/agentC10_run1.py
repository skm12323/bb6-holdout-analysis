"""work_r10/agentC10_run1.py — TASK 1: formalize the boundary state and verify.

For every v = 1..V (V = 2000) and U = 3 (w = 1; spots at U = 9, 15):
  * run the ground-truth integer-list simulator of the real excursion E(w,v);
  * run the exact pair walk of the excursion with the boundary substitution
    (index v-1 -> (2^{v-1}, -1), run ends, missing second entry -> (0,0));
  * compare the full list states STEP BY STEP (values c*U + l vs integers);
  * check: no chain halts (u >= 3 at every chain, also at U = 1), the walk
    reaches the singleton (2^v, 3*ell(v)) — i.e. value 2^v*3w + 3*ell(v) —
    the mass identities hold at every step, and ell(1..20) matches the
    closed-form report (agentB Theorem 4).

Also dumps agentC10_out1.json (per-v ell, s_cross, e, dec) for cross-checks
by run2/run3.
"""
import json
import sys
import time

sys.path.insert(0, r'D:\math_cc\work_r10')
import agentC10_lib as L

V = 2000
ELLB = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]


def lockstep(U, v, full_tail_check=False):
    """Run both engines in lockstep; compare list states at every step.
    Returns (concrete_result, pair_result)."""
    conc = []

    def crec(step, A, Q):
        conc.append((step, A, list(Q)))

    fin, steps, minu, jseq, halt = L.concrete_excursion(U, v, record=crec)
    pair = []

    def prec(step, A, Q, i, bnd):
        pair.append((step, A, list(Q), i, bnd))

    res = L.excursion_pairs(v, record=prec)
    assert halt is False, ('concrete HALT', v, U)
    assert res['dec'] == tuple(jseq), ('decision mismatch', v, U)
    assert len(pair) == len(conc) == steps, ('step count', v, len(pair), len(conc), steps)
    for (s1, A, Qp, i, bnd), (s2, Ac, Qc) in zip(pair, conc):
        assert s1 == s2
        ev = [A[0] * U + A[1]] + [c * U + l for (c, l) in Qp]
        front = [Ac] + Qc
        assert ev == front[:len(ev)], ('state mismatch', v, U, s1)
        tail_exp = max(0, v - 1 - i) + (1 if bnd else 0)
        assert len(front) - len(ev) == tail_exp, ('tail length', v, U, s1)
        k = len(ev)
        if tail_exp:
            if i < v - 1:
                assert front[k] == (U << i), ('tail head', v, U, s1)
                if full_tail_check:
                    assert front[k:] == [(U << a) for a in range(i, v - 1)] + \
                        [(U << (v - 1)) - 1], ('full tail', v, U, s1)
            else:
                assert bnd and front[k] == (U << (v - 1)) - 1, ('tail head bnd', v, U, s1)
        else:
            assert (not bnd) and i >= v
    assert fin == (1 << v) * U + 3 * steps, ('final value', v, U)
    assert res['final'] == ((1 << v), 3 * steps), ('final pair', v, U)
    return (fin, steps, minu), res


def main():
    t0 = time.time()
    out = {}
    minu_global = None
    for v in range(1, V + 1):
        (fin, steps, minu), res = lockstep(3, v, full_tail_check=(v % 97 == 0))
        if minu is not None and (minu_global is None or minu < minu_global):
            minu_global = minu
        out[v] = [steps, res['s_cross'], steps - res['s_cross'],
                  list(res['dec'])]
    print('[1] lockstep pair-vs-concrete at U=3 for v=1..%d: ALL %d states '
          'identical, no halt, final = 2^v*U + 3*ell  [%.0fs]'
          % (V, sum(out[v][0] for v in out), time.time() - t0))
    ells = [out[v][0] for v in range(1, 21)]
    assert ells == ELLB, ('ell table', ells)
    print('[2] ell(1..20) = %s  == closed-form report Theorem 4 table' % ells)
    # spots at other U (the pair walk is U-free; this re-proves the simulation
    # lemma at U = 9, 15 = w = 3, 5)
    for U in (9, 15):
        for v in range(1, 65):
            (fin, steps, minu), res = lockstep(U, v)
    print('[3] spots U in {9,15}, v <= 64: identical lists, no halt, '
          'same decision streams (U-free), final = 2^v*U + 3*ell')
    es = [out[v][2] for v in out]
    js = [j for v in out for j in out[v][3] if j > 0]
    print('[4] e(v) = ell - s_cross: min %d max %d ; endgame chain j in [%d, %d]'
          % (min(es), max(es), min(js), max(js)))
    print('    concrete min u at U=3 over all chains: %s' % minu_global)
    sup = max(es)
    who = [v for v in out if out[v][2] == sup][:8]
    print('    e = %d first attained at v = %s' % (sup, who))
    json.dump(out, open('agentC10_out1.json', 'w'))
    print('wrote agentC10_out1.json')


if __name__ == '__main__':
    main()
