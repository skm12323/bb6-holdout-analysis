"""AUDITOR 1 / Task B -- independent re-implementation (from the task spec, not copied).

Compositional prover for excursions of machine "1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE"
via its audited top map T on lists L = (A, b, c, S...):
  A even -> (A+b+c+3, S)
  A odd  -> m := b + (A-3)/2 ; st := [c + (A+1)/2] + S ;
            while m odd and m >= 3: st := [(m+3)/2] + st ; m := (m-3)/2 ;
            m == 1 -> HALT ; else -> (m+4, st)
HALT <=> some top step has A odd and A+2b+3 == 2^k.

Symbolic values: affine forms a*u + c, u >= 0, w = 2u+1.  Uniformity rules:
  - parity decidable only if coefficient a is even (then parity = c mod 2)
  - halving only if a and c both even
  - "m >= 3" only if uniform (a >= 0 and c >= 3 -> True; a == 0 and c < 3 -> False)

Compositional rules (re-derived by hand for this audit):
  canonical list (H+d, H, 2H, ..., 2^{r-1}H, J, Z...), J = 2^r H + kap, r >= 1:
   * A = H+d even, r >= 2  -> [4H + d + 3] + L[3:]            (1 step, E-macro)
   * A odd: b = H; c = 2H (r>=2) or J (r==1); q0 = A+2b+3; s' = v2(q0);
     o' = q0/2^s'; c' = c + (A+1)/2; kap_child = c' - 2^{s'-1} o';
     nested start  N = [o'+1, o', 2o', ..., 2^{s'-2}o', 2^{s'-1}o' + kap_child] + window
     where window = L[3:];  recurse; resume at [head] + window[a':]   (1 + ell steps)
  Everything else: one direct symbolic step.
Every compositional 1-step construction is ASSERTED equal to the direct stepper
(faithfulness).  Excursion E(w,v) starts at (3w+1, 3w, ..., 2^{v-1}3w, 2^{v-1}3w - 1)
and must end at the singleton 3w*2^v + 3*ell(v).

Cross-checks: ell(v) vs direct full symbolic run for v = 1..150; final singleton
identity; R4's audited ell table for v = 1..20.
"""
import sys
sys.setrecursionlimit(100000)


class Undecided(Exception):
    pass


class Halt(Exception):
    pass


class Af:
    """value = a*u + c, u >= 0 (w = 2u+1)"""
    __slots__ = ('a', 'c')

    def __init__(self, a, c):
        self.a = a
        self.c = c

    def __add__(s, o): return Af(s.a + o.a, s.c + o.c)
    def __sub__(s, o): return Af(s.a - o.a, s.c - o.c)
    def __mul__(s, k): return Af(s.a * k, s.c * k)
    def __eq__(s, o): return type(o) is Af and s.a == o.a and s.c == o.c
    def __hash__(s): return hash((s.a, s.c))
    def __repr__(s): return '%d*u%+d' % (s.a, s.c)

    def par(s):
        if s.a & 1:
            raise Undecided('parity of %r' % (s,))
        return s.c & 1

    def half(s):
        if (s.a & 1) or (s.c & 1):
            raise Undecided('halve %r' % (s,))
        return Af(s.a >> 1, s.c >> 1)

    def ge3(s):
        if s.a >= 0 and s.c >= 3:
            return True
        if s.a == 0 and s.c < 3:
            return False
        raise Undecided('ge3 on %r' % (s,))

    def v2(s):
        n, a, c = 0, s.a, s.c
        while not (a & 1) and not (c & 1) and (a or c):
            a >>= 1; c >>= 1; n += 1
        return n

    def div2k(s, k):
        x = s
        for _ in range(k):
            x = x.half()
        return x


Z, O, T3, M4 = Af(0, 0), Af(0, 1), Af(0, 3), Af(0, 4)


def dstep(L):
    """One top-map step, purely symbolic, no structural assumptions (ground truth)."""
    A = L[0]
    b = L[1] if len(L) > 1 else Z
    c = L[2] if len(L) > 2 else Z
    if A.par() == 0:
        return [A + b + c + T3] + L[3:]
    m = (b + b + A - T3).half()
    st = [(c + c + A + O).half()] + L[3:]
    while m.par() == 1 and m.ge3():
        st = [(m + T3).half()] + st
        m = (m - T3).half()
    if m.par() == 1:
        if m == O:
            raise Halt('HALT reached')
        raise Undecided('odd m not resolved: %r' % (m,))
    return [m + M4] + st


def enc(L):
    """canonical? -> (H, d, r, kap) for L = (H+d, H, 2H, ..., 2^{r-1}H, J, ...), r >= 1."""
    if len(L) < 3:
        return None
    H = L[1]
    if not (L[2] == H * 2):
        return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == H * (1 << r):
        r += 1
    if r + 1 >= len(L):
        return None
    return H, L[0] - H, r, L[r + 1] - H * (1 << r)


def suffix_a(L, ZL):
    """a if L == [X] + ZL[a:] for some a (largest a preferred); else None."""
    n = len(ZL)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == ZL[k:]:
            return k
    return None


STATS = dict(macro=0, chain=0, glue=0, coinc=0, calls=0, spmax=0, maxdepth=0)


def prover(L, level, ZL, s0, H0, kap0, depth=0):
    """Run compositionally until first reaching [X] + ZL[a:] with the contract
    X = 2^s0*H0 + 3*ell + 1 + kap0 + sum(ZL[:a]).  Returns (ell, a, X)."""
    STATS['maxdepth'] = max(STATS['maxdepth'], depth)
    L = list(L)
    ell = 0
    while True:
        a = suffix_a(L, ZL)
        if a is not None:
            exp = H0 * (1 << s0) + Af(0, 3 * ell) + O + kap0
            for z in ZL[:a]:
                exp = exp + z
            if L[0] == exp:
                return ell, a, L[0]
            STATS['coinc'] += 1          # spurious suffix match: run continues
        e = enc(L)
        if e is not None:
            H, d, r, kap = e
            A = H + d
            if A.par() == 0 and r >= 2:
                nxt = [H * 4 + d + T3] + L[3:]
                assert dstep(L) == nxt, 'E-macro construction unfaithful at %r' % (L,)
                STATS['macro'] += 1
                L = nxt
                ell += 1
                continue
            if A.par() == 1:
                b = H
                c = H * 2 if r >= 2 else L[2]          # r == 1 -> c = J
                q0 = A + b + b + T3
                sp = q0.v2()
                assert sp >= 1, 'q0 not even despite odd A'
                o1 = q0.div2k(sp)
                cp = c + (A + O).half()
                kapn = cp - o1 * (1 << (sp - 1))
                window = L[3:]
                nest = [o1 + O] + [o1 * (1 << i) for i in range(sp - 1)] \
                       + [o1 * (1 << (sp - 1)) + kapn] + list(window)
                assert dstep(L) == nest, 'chain construction unfaithful at %r' % (L,)
                assert sp < level, 'well-foundedness violated: sp=%d level=%d' % (sp, level)
                STATS['chain'] += 1
                STATS['calls'] += 1
                STATS['spmax'] = max(STATS['spmax'], sp)
                en, an, hn = prover(nest, sp, window, sp, o1, kapn, depth + 1)
                L = [hn] + list(window[an:])
                ell += 1 + en
                continue
        STATS['glue'] += 1
        L = dstep(L)
        ell += 1


def excursion_compositional(v):
    W = Af(6, 3)                                    # 3w = 6u+3
    L = [W + O] + [W * (1 << i) for i in range(v - 1)] + [W * (1 << (v - 1)) - O]
    ell, a, head = prover(L, v, [], v, W, Af(0, -1))
    assert a == 0, ('not singleton', a)
    exp = W * (1 << v) + Af(0, 3 * ell)
    assert head == exp, ('final singleton contract', v, head, exp)
    return ell, head


def excursion_direct(v):
    W = Af(6, 3)
    L = [W + O] + [W * (1 << i) for i in range(v - 1)] + [W * (1 << (v - 1)) - O]
    t = 0
    while len(L) > 1:
        L = dstep(L)
        t += 1
    exp = W * (1 << v) + Af(0, 3 * t)
    assert L[0] == exp, ('direct final singleton', v, L[0], exp)
    return t, L[0]


R4_TABLE = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]

if __name__ == '__main__':
    NB = 150
    comp, direct = {}, {}
    for v in range(1, NB + 1):
        comp[v] = excursion_compositional(v)
        direct[v] = excursion_direct(v)
        assert comp[v] == direct[v], (v, comp[v], direct[v])
    print('TaskB: compositional ell == direct full-run ell AND final singleton '
          '3w*2^v+3*ell verified symbolically for all v = 1..%d  [PASS]' % NB)
    bad = [v for v in range(1, 21) if comp[v][0] != R4_TABLE[v - 1]]
    print('TaskB: R4 audited table ell(1..20) agreement: %s (mismatches: %s)'
          % ('PASS' if not bad else 'FAIL', bad))
    print('TaskB: ell(1..20) =', [comp[v][0] for v in range(1, 21)])
    print('TaskB: ell(141..150) =', [comp[v][0] for v in range(141, 151)])
    print('TaskB: max ell(v)/v over v=10..%d = %.6f' % (NB, max(comp[v][0] / v for v in range(10, NB + 1))))
    print('TaskB: stats:', STATS)
