"""Abstract end-phase template checker.

Abstracts the exact compositional engine: every form (c0*u + c1) is carried as
  (r0, r1, lb) with r0 = c0 mod 2^K, r1 = c1 mod 2^K, lb = lower bound on value,
  plus a flag z0 = (c0 == 0 exactly).
Decisions: par (needs r0 == 0 mod 2), half, ge3 (lb >= 3 / z0 & upper info).
Nested excursion calls become BRANCHES: sp = v2(q0) capped at K; a in {0,1,2};
ell enters only as 3*(1+e) with e >= 0 unknown residue -> new d residue unknown
(represented by r1 = None meaning 'any'; consumer branches over all).
A state FAILS if any branch raises Undecided/Halt or exceeds the step guard.
The checker enumerates all start states (r in 1..4, d-residue all 2^K values,
J kap-class) and reports whether every path terminates safely.
"""
import sys
from collections import deque

K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
MOD = 1 << K
STEPS_GUARD = 60

# abstract form: (r0 or None, r1 or None, lb)  None = unknown (any residue)
# z0 (c0==0) implied by r0 == 0 and flag 'z'
def mk(r0, r1, lb, z): return (r0 % MOD, r1 % MOD if r1 is not None else None, lb, z)
def a_add(*xs):
    r0 = sum(x[0] for x in xs) % MOD
    if any(x[1] is None for x in xs): r1 = None
    else: r1 = sum(x[1] for x in xs) % MOD
    return (r0, r1, sum(x[2] for x in xs), False)
def a_sc(x, k):  # multiply by small int k
    return (x[0] * k % MOD, None if x[1] is None else x[1] * k % MOD, x[2] * k, x[3] and k == 1)
def a_sub(x, y): return a_add(x, a_sc(y, -1))
def a_par(x):
    if x[0] % 2: return None
    if x[1] is None: return None
    return x[1] % 2

class Fail(Exception): pass

def step_list(L):
    """One direct abstract step; returns list of successors (branching only on unknown par at
    the HALT-critical spot is disallowed -> Fail)."""
    A = L[0]; b = L[1] if len(L) > 1 else (0, 0, 0, True); c = L[2] if len(L) > 2 else (0, 0, 0, True)
    R = L[3:]
    p = a_par(A)
    if p is None: raise Fail('parity of head unknown')
    if p == 0:
        return [ [a_add(A, b, c, (0, 3, 3, True))] + R ]
    m = a_add(b, b, A, (0, -3, -3, True))
    st = [a_add(c, c, A, (0, 1, 1, True))] + R
    while True:
        pm = a_par(m)
        if pm is None: raise Fail('chain parity unknown')
        if pm == 0: break
        # m odd: must have m >= 3 (guaranteed by size lemma; lb check as sanity)
        if m[2] < 3 and m[3]: raise Fail('m small: possible HALT')
        st = [a_add(m, (0, 3, 3, True))] + st
        m = a_add(m, (0, -3, -3, True))
        m = a_half(m)
    return [ [a_add(m, (0, 4, 4, True))] + st ]

def a_half(x):
    if x[0] % 2 or x[1] is None or x[1] % 2: raise Fail('half unknown')
    return (x[0] // 2, x[1] // 2, x[2] // 2, x[3])

def encode_abs(L):
    if len(L) < 3: return None
    H = L[1]
    if L[2] != a_sc(H, 2): return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == a_sc(H, 1 << r): r += 1
    if r + 1 >= len(L): return None
    return (H, r, a_sub(L[r + 1], a_sc(H, 1 << r)))

def canon_abs(L):
    """canonicalize a list for state identity: normalize H to a symbolic 'base' token."""
    e = encode_abs(L)
    if e is None: return ('flat', tuple(L))
    H, r, kap = e
    d = a_sub(L[0], H)
    return ('cs', r, kap, tuple(L[r + 2:]), d)

def abstract_run(L0, table_a, verbose=False):
    """Run the end phase abstractly. table_a: function sp -> set of a-values (from exact data).
    Returns True if all branches terminate within guard, else raises Fail."""
    memo = set()
    stack = [(tuple(L0), 0)]
    while stack:
        Lt, n = stack.pop()
        while True:
            if n > STEPS_GUARD: raise Fail('step guard exceeded')
            L = list(Lt)
            key = (canon_abs(L), n)
            if key in memo: break
            memo.add(key)
            if len(L) == 1:
                break  # terminated (top-level style)
            e = encode_abs(L)
            if e is not None:
                H, r, kap = e
                d = a_sub(L[0], H)
                p = a_par(a_add(H, d))
                if p is 0 and r >= 2:
                    Lt = ([a_add(a_sc(H, 4), d, (0, 3, 3, True))] + L[3:]); n += 1
                    continue
                if p is 1:
                    # build q0
                    if r >= 2:
                        q0 = a_add(a_sc(H, 3), d, (0, 3, 3, True))
                        window = L[3:]
                    else:
                        q0 = a_add(a_sc(H, 3), a_sc(kap, 2), d, (0, 3, 3, True))
                        window = L[3:]
                    # sp from residues (capped)
                    sp = 0
                    qq = q0
                    while qq[0] % 2 == 0 and qq[1] is not None and qq[1] % 2 == 0 and sp < K:
                        qq = a_half(qq); sp += 1
                    if sp >= 1:
                        for a_val in table_a(sp):
                            # head = 2^sp * o' + 3*(1+e) + K' + sum(window[:a]) : residues unknown (e)
                            head = (0, None, 1, False)
                            rest = window[a_val:]
                            stack.append((tuple([head] + list(rest)), n + 1))
                        break  # handled by branches
                    # sp == 0: single step via direct engine
            succ = step_list(L)
            if len(succ) != 1: raise Fail('multi successor in direct step')
            Lt = succ[0]; n += 1
    return True

def table_a_default(sp):
    return (0, 1, 2)

if __name__ == '__main__':
    # start states: canonical (H base, d, r in 1..4, kap = -1), d-residue over ALL values
    bad = 0; total = 0
    for r0 in (1, 2, 3, 4):
        for dres in range(MOD):
            H = (0, 0, 3, True)   # symbolic base with lb 3 (represents 3w*2^j, j large: even)
            d = (0, dres, 0, True)
            kap = (0, MOD - 1, -1, True)
            L = [a_add(H, d)] + [a_sc(H, 1 << i) for i in range(r0)] + [a_add(a_sc(H, 1 << r0), kap)]
            total += 1
            try:
                ok = abstract_run(L, table_a_default)
            except Fail as e:
                bad += 1
                if bad <= 5:
                    print('FAIL r0=%d dres=%d: %s' % (r0, dres, e))
    print('K=%d: checked %d start states, %d failures' % (K, total, bad))
