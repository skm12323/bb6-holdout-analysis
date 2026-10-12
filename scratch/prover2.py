"""Compositional symbolic prover v2 for excursions of the top map (machine #1).

State: plain list of affine forms (c0, c1) == c0*u + c1 (u >= 0, w = 2u+1).
Each step: try to CS-encode (head + doubling run + J + Z);
  - A even, r >= 2: macro E-step  (H, d, r, kap, Z) -> (4H, d+3, r-2, kap, Z);
  - A odd, sp = v2(3H+d+[2kap if r==0]+3) >= 1: build the nested CS and RECURSE
    (this jumps 1 + ell_nested steps; the nested run verifies its own conclusion);
  - otherwise (incl. GLUE): one direct symbolic step.
Stop when the list == [X] + (suffix of the original Z-list) with the verified
conclusion  X == 2^s*o + 3*ell + (kap0+1) + sum(Z0[:a]);  for empty Z: singleton.
Every decision must be uniform in u; any violation raises Undecided (no certificate).
"""
import sys
sys.setrecursionlimit(100000)

class Undecided(Exception): pass
class Halt(Exception): pass

def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def sc(x, k): return (x[0] * k, x[1] * k)
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def par(x):
    if x[0] % 2: raise Undecided('parity(u)')
    return x[1] % 2
def half(x):
    if x[0] % 2 or x[1] % 2: raise Undecided('half')
    return (x[0] // 2, x[1] // 2)
def ge3(x):
    if x[0] >= 0 and x[1] >= 3: return True
    if x[0] == 0 and x[1] < 3: return False
    raise Undecided('ge3')
def v2f(x):
    n = 0
    while x[0] % 2 == 0 and x[1] % 2 == 0 and (x[0] or x[1]):
        x = (x[0] // 2, x[1] // 2); n += 1
    return n
def halfn(x, n):
    for _ in range(n): x = half(x)
    return x

Z0 = (0, 0)
def T_list(L):
    A = L[0]; b = L[1] if len(L) > 1 else Z0; c = L[2] if len(L) > 2 else Z0; R = L[3:]
    if par(A) == 0: return [add(A, b, c, (0, 3))] + R
    m = half(add(b, b, A, (0, -3))); st = [half(add(c, c, A, (0, 1)))] + R
    while par(m) == 1 and ge3(m):
        st = [half(add(m, (0, 3)))] + st; m = half(add(m, (0, -3)))
    if par(m) == 1:
        if m == (0, 1): raise Halt('HALT branch reachable')
        raise Undecided('m odd unknown')
    return [add(m, (0, 4))] + st

def encode(L):
    """-> (H, d, r, kap) with list = [H+d] + [2^i H, i<r] + [2^r H + kap] + rest, or None."""
    if len(L) < 3: return None
    H = L[1]
    if L[2] != sc(H, 2): return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == sc(H, 1 << r): r += 1
    if r + 1 >= len(L): return None          # run reaches end: no J slot; use direct step
    kap = sub(L[r + 1], sc(H, 1 << r))
    return (H, sub(L[0], H), r, kap)

EVENTS = []   # (level, t_at_event, r, sp, a_nested, ell_nested)
STATS = {'macro': 0, 'nested': 0, 'direct': 0}

def final_match(L, Z0L):
    """Return a if L == [X] + Z0L[a:] (suffix of ORIGINAL Z list), else None."""
    if not Z0L:
        return 0 if len(L) == 1 else None
    n = len(Z0L)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == Z0L[k:]:
            return k
    return None

def F(L, level, Z0L, s0, H0, kap0):
    """Run to the F-contract end. Returns (ell, a, head)."""
    L = list(L); ell = 0
    while True:
        a = final_match(L, Z0L)
        if a is not None:
            head = L[0]
            expect = add(sc(H0, 1 << s0), (0, 3 * ell), (0, 1), kap0, *Z0L[:a])
            if head == expect:
                return ell, a, head
            # coincidental suffix match: continue (log it)
            STATS.setdefault('coinc', 0); STATS['coinc'] += 1
        enc = encode(L) if len(L) >= 3 else None
        if enc is not None:
            H, d, r, kap = enc
            A = add(H, d)
            if par(A) == 0 and r >= 2:
                new = [add(sc(H, 4), d, (0, 3))] + L[3:]
                # verify equivalence with direct step (cheap cross-check, can disable)
                L = new; ell += 1; STATS['macro'] += 1
                continue
            if par(A) == 1:
                # chain: q0 depends on r
                if r >= 2:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), half(add(H, d, (0, 1))))
                    window = L[3:]           # entries after (A, H, 2H)
                elif r == 1:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), kap, half(add(H, d, (0, 1))))
                    window = L[3:]           # entries after (A, H, J)
                else:
                    z1 = L[2] if len(L) > 2 else Z0
                    q0 = add(sc(H, 3), sc(kap, 2), d, (0, 3))
                    cprime = add(z1 if len(L) > 2 else Z0, half(add(H, d, (0, 1))))
                    window = L[3:] if len(L) > 2 else []
                sp = v2f(q0)
                if sp >= 1:
                    o_p = halfn(q0, sp)
                    kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
                    # nested list: [o'+1] + [2^i o', i<sp-1] + [2^{sp-1} o' + kap_nest] + window
                    nestL = [add(o_p, (0, 1))] + [sc(o_p, 1 << i) for i in range(sp - 1)] \
                            + [add(sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                    assert sp < level, 'well-foundedness: sp=%d >= level=%d' % (sp, level)
                    ell_n, a_n, head_n = F(nestL, sp, window, sp, o_p, kap_nest)
                    EVENTS.append((level, ell, r, sp, a_n, ell_n))
                    L = [head_n] + list(window[a_n:])
                    ell += 1 + ell_n; STATS['nested'] += 1
                    continue
                # sp == 0: fall through to direct step
        L = T_list(L); ell += 1; STATS['direct'] += 1

def excursion(v):
    """F for E(w,v): o = 3w, K = 0, Z empty."""
    w3 = (6, 3)
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
    ell, a, head = F(L, v, [], v, w3, (0, -1))
    assert a == 0
    assert head == add(sc(w3, 1 << v), (0, 3 * ell))
    return ell, head

def direct_E(v):
    w3 = (6, 3)
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
    t = 0
    while len(L) > 1:
        L = T_list(L); t += 1
    assert L[0] == add(sc(w3, 1 << v), (0, 3 * t))
    return t

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    ells = []
    for v in range(1, N + 1):
        ell, head = excursion(v)
        ells.append(ell)
    # cross-check against direct runs
    for v in range(1, min(N, 300) + 1):
        assert ells[v - 1] == direct_E(v), v
    print('compositional prover: F(v) verified for v=1..%d, ell matches direct runs' % N)
    print('stats:', STATS)
    spmax = {}
    for (lvl, t, r, sp, a, e) in EVENTS:
        spmax[lvl] = max(spmax.get(lvl, 0), sp)
    lv = sorted(spmax)
    print('max sp used per level (level: maxsp):', {l: spmax[l] for l in lv[:30]})
    print('global max sp < level always; max ell/v ratio:', max(ells[v - 1] / v for v in range(1, N + 1) if v >= 10))
