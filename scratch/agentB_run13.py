"""agentB_run13.py — abstract endgame verification for all boundary geometries.

Start from the canonical post-chain state C(j) at pointer p (P = 2^p units)
but with a FINITE tail: T entries at offsets 2..E-1, the defect T* = 3*2^{E-1}P
- 1 at offset E, then nothing.  E ranges over 2..8 (dp(j) <= 6), j over
1..JMAX.  Verify: all decisions robust, every chain u >= 3, process reaches the
singleton (queue exhausted).  This covers every way the excursion's tail can
end (Lemma E endgame part) for boundary chains of parameter j <= JMAX."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_abs import Val, Ctx, Sim, v2_val, parity, Ambiguous, NeedsSplit, ZERO
from agentB_run7 import kappa_for, verify

def run_endgame_once(j, E, kappa, m, vshort=None):
    ctx = Ctx(p=max(200, j + E + 60), kappa=kappa, m=m)
    u = Val(Fr(9, 1 << j), Fr(6, 1 << j), Fr(4, 1 << j))
    A = u + 1
    queue = [u * (1 << a) for a in range(j - 1)]
    queue.append(Val(Fr(15, 2), 3, 1))                    # D
    for e in range(2, E):
        queue.append(Val(3 << e, 0, 0))                   # T at offset e
    queue.append(Val(3 * (1 << (E - 1)), 0, 0) + Val(0, 0, -1))  # T* = 3*2^{E-1}P - 1
    sim = Sim(ctx)
    trace = []
    guard = 0
    try:
        while queue and guard < 3000:
            guard += 1
            A, queue, info = sim.step(A, queue, trace)
        if queue:
            return ('FAIL', 'not finished')
        # final singleton A: no further check needed (halting only at chains)
        return ('OK', len(trace), [t[1] for t in trace if t[0] == 'C'])
    except NeedsSplit as ns:
        return ('SPLIT', str(ns))
    except Ambiguous as am:
        return ('FAIL', str(am))

def endgame_verify(j, E):
    kap = kappa_for(j)
    stack = [(kap, j)]
    maxm = j + 30
    leaves = []
    while stack:
        kappa, m = stack.pop()
        r = run_endgame_once(j, E, kappa, m)
        if r[0] == 'SPLIT':
            if m >= maxm:
                return None, 'cap at m=%d: %s' % (m, r[1])
            stack.append((kappa, m + 1))
            stack.append((kappa + (1 << m), m + 1))
        elif r[0] == 'OK':
            leaves.append(r)
        else:
            return None, 'FAIL %s' % (r[1],)
    chains = set(tuple(l[2]) for l in leaves)
    return (len(leaves), [l[1] for l in leaves]), None

def main():
    JMAX = 60
    bad = 0
    for j in range(1, JMAX + 1):
        for E in range(2, 9):
            res, err = endgame_verify(j, E)
            if err:
                print('FAIL j=%d E=%d: %s' % (j, E, err))
                bad += 1
    print('abstract endgame verification j=1..%d, E=2..8: %s' %
          (JMAX, 'ALL OK' if not bad else '%d FAILURES' % bad))

if __name__ == '__main__':
    main()
