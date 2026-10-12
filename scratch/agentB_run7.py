"""agentB_run7.py — abstract verification of the bulk transition table (v4).

For each chain parameter j (with k in the class 6k+4 = 2^j*odd, i.e.
k = kappa_j mod 2^j), start from the canonical post-chain state, run until the
next tail-pair chain, and verify (with class-splitting when needed):
  (i) every chain has u >= 3 (huge P-part),
 (ii) the next T-chain has x = 9*2^e P + 6(k+dk) + 4, c = its paired T,
(iii) the new D = (15/2)2^e P + 3(k+dk)+1 (canonical),
 (iv) the queue after it is [run of length j'-1, D, pure T's].
Returns the transition (j -> (dk, dp)); all split branches must agree.
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_abs import Val, Ctx, Sim, v2_val, parity, Ambiguous, NeedsSplit, ZERO

def pow2exp(fr):
    if fr <= 0:
        return None
    n, d = fr.numerator, fr.denominator
    if n != 1 and (n & (n - 1)):
        return None
    if d != 1 and (d & (d - 1)):
        return None
    return (n.bit_length() - 1) - (d.bit_length() - 1)

def is_T(v):
    return (v.c == 0 and v.d == 0 and v.a > 0 and pow2exp(v.a / 3) is not None)

def T_of(e):
    return Val(3 * (1 << e) if e >= 0 else Fr(3, 1 << (-e)), 0, 0)

def kappa_for(j):
    mod = 1 << j
    inv3 = pow(3, -1, mod)
    k0 = ((1 << (j - 1)) - 2) * inv3 % mod
    assert ((6 * k0 + 4) >> j) % 2 == 1
    if j >= 5:
        assert k0 % 16 == 10, (j, k0)
    return k0

def run_once(j, kappa, m, cap):
    """Returns ('OK', dk, dp, trace) | ('SPLIT',) | ('FAIL', msg)."""
    ctx = Ctx(p=max(200, j + 100), kappa=kappa, m=m)
    sim = Sim(ctx)
    u = Val(Fr(9, 1 << j), Fr(6, 1 << j), Fr(4, 1 << j))
    A = u + 1
    queue = [u * (1 << a) for a in range(j - 1)]
    queue.append(Val(Fr(15, 2), 3, 1))
    for e in range(2, 120):
        queue.append(T_of(e))
    trace = []
    guard = 0
    gmax = 8 * j + 400
    try:
        while guard < gmax:
            guard += 1
            b = queue[0] if queue else ZERO
            if parity(A, ctx) == 1 and is_T(b):
                c = queue[1]
                x = A + b * 2 + 3
                e = pow2exp(b.a / 3)
                dk = (x.d - 4) / 6
                if x.c != 6 or dk.denominator != 1 or not is_T(c):
                    return ('FAIL', 're-entry form: x=%r c=%r' % (x, c))
                # D' canonical (independent of j'):
                Dp = c + (A + 1) * Fr(1, 2)
                expD = Val(Fr(15, 2) * (1 << e), 3, 3 * dk + 1)
                if Dp != expD:
                    return ('FAIL', 'D form %r vs %r' % (Dp, expD))
                for rv in queue[2:]:
                    if not is_T(rv):
                        return ('FAIL', 'leftover junk %r' % (rv,))
                return ('OK', int(dk), int(e), trace)
            A, queue, info = sim.step(A, queue, trace)
            if not queue:
                return ('FAIL', 'queue exhausted')
        return ('FAIL', 'no re-entry')
    except NeedsSplit as ns:
        return ('SPLIT', str(ns))
    except Ambiguous as am:
        return ('FAIL', str(am))

def verify(j, mcap_extra=24):
    kap = kappa_for(j)
    m0 = j
    leaves = []
    stack = [(kap, m0)]
    maxm = m0 + mcap_extra
    while stack:
        kappa, m = stack.pop()
        r = run_once(j, kappa, m, maxm)
        if r[0] == 'SPLIT':
            if m >= maxm:
                return None, 'cap exceeded at m=%d: %s' % (m, r[1])
            stack.append((kappa, m + 1))
            stack.append((kappa + (1 << m), m + 1))
        elif r[0] == 'OK':
            leaves.append(r)
        else:
            return None, 'FAIL %s' % (r[1],)
    dks = set((l[1], l[2]) for l in leaves)
    if len(dks) != 1:
        return None, 'branches disagree: %s' % (dks,)
    return (dks.pop(), len(leaves)), None

def main():
    print('regular chains:')
    for j in (1, 2, 3, 4):
        res, err = verify(j)
        print('  j=%d -> %s %s' % (j, res, ('ERR: ' + err) if err else ''))
    print('spikes:')
    for j in range(5, 45):
        res, err = verify(j)
        print('  j=%2d -> %s %s' % (j, res, ('ERR: ' + err) if err else ''))

if __name__ == '__main__':
    main()
