"""AUDITOR 1 / Task C -- from-scratch end-phase template check, K = 8, canonical starts.

Scope (per audit task): canonical starts with kap = -1 only:
  r0 in 1..5, rho in 0..255, tail patterns [[], [0], [1], [0,0]]  -> 5120 runs.
Symbols u, h, tt, z1, z2, z3 >= 0 (multi-symbol affine forms):
  H    = 6*2^11*u + 2^11*(1+h)          (any multiple of 2^11)
  d    = rho + 2^8*tt                   (all residues mod 2^8)
  tail_i = 2^11*(z_i + 1) - pi_i        (pi_i in {0,1})
Start list: [H+d] + [H*2^i, i=0..r0-1] + [H*2^r0 - 1] + tails.

Engine: symbolic top-map steps with uniformity rules (parity only if all coeffs
even; halving only if all coeffs and const even; >=3 only if uniform).
  - E-macro when head even and L[2] == 2*L[1] (asserted faithful vs direct step);
  - odd head: q0 = A + 2b + 3, sp = v2(q0):
      sp < 8  -> nested excursion frame built and executed recursively
                 (asserted faithful vs direct step);
      sp >= 8 -> DEEP BRANCH: continuation [head] + window[a:], a in 0..2, must be
                 H-run multiples (4H, 8H, ...) then entries each in class 0 or -1
                 (mod 2^11) with nonnegative quotient (J is -1; tails are 0 or -1);
                 treat as covered, stop.
Pass = terminates at verified contract or covered deep branch, no Halt, no
Undecided, all hand-offs in family.

EXTRA (auditor's addition): every symbolic step is cross-checked against a
CONCRETE parallel run (cstep on integers) for 3 symbol instantiations per start
(the all-zero instantiation plus 2 random), asserting the substituted symbolic
state equals the concretely stepped state -- validates that the symbolic
"uniform" decisions are true for real symbol values (no hidden halt/divergence).
"""
import sys, random
sys.setrecursionlimit(100000)

K = 8
MOD = 1 << 11            # 2^{K+3}
NSYM = 6                 # symbols: 0:u 1:h 2:tt 3:z1 4:z2 5:z3


class Undecided(Exception):
    pass


class Halt(Exception):
    pass


class F6:
    """value = sum(coeffs[i]*sym_i) + const, all symbols >= 0 integers"""
    __slots__ = ('v',)

    def __init__(self, *v):
        assert len(v) == NSYM + 1
        self.v = tuple(v)

    def __add__(s, o): return F6(*[a + b for a, b in zip(s.v, o.v)])
    def __sub__(s, o): return F6(*[a - b for a, b in zip(s.v, o.v)])
    def __mul__(s, k): return F6(*[k * a for a in s.v])
    def __eq__(s, o): return type(o) is F6 and s.v == o.v
    def __repr__(s): return 'F6%s' % (s.v,)

    def par(s):
        if any(a & 1 for a in s.v[:NSYM]):
            raise Undecided('par %r' % (s.v,))
        return s.v[NSYM] & 1

    def half(s):
        if any(a & 1 for a in s.v):
            raise Undecided('half %r' % (s.v,))
        return F6(*[a >> 1 for a in s.v])

    def ge3(s):
        if all(a >= 0 for a in s.v[:NSYM]) and s.v[NSYM] >= 3:
            return True
        if all(a == 0 for a in s.v[:NSYM]) and s.v[NSYM] < 3:
            return False
        raise Undecided('ge3 %r' % (s.v,))

    def v2(s):
        n = 0
        w = list(s.v)
        while all(not (a & 1) for a in w) and any(w):
            w = [a >> 1 for a in w]
            n += 1
        return n

    def div2k(s, k):
        x = s
        for _ in range(k):
            x = x.half()
        return x

    def sub_val(s, val):
        return sum(a * b for a, b in zip(s.v[:NSYM], val)) + s.v[NSYM]


def C(c):
    return F6(0, 0, 0, 0, 0, 0, c)


Z0, O1, T3, M4 = C(0), C(1), C(3), C(4)


def dstep(L):
    """direct symbolic top-map step (ground truth for faithfulness asserts)"""
    A = L[0]
    b = L[1] if len(L) > 1 else Z0
    c = L[2] if len(L) > 2 else Z0
    if A.par() == 0:
        return [A + b + c + T3] + L[3:]
    m = (b + b + A - T3).half()
    st = [(c + c + A + O1).half()] + L[3:]
    while m.par() == 1 and m.ge3():
        st = [(m + T3).half()] + st
        m = (m - T3).half()
    if m.par() == 1:
        if m == O1:
            raise Halt('HALT branch')
        raise Undecided('odd m unresolved %r' % (m.v,))
    return [m + M4] + st


def cstep(L):
    """concrete top-map step on Python ints"""
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    if A % 2 == 0:
        return [A + b + c + 3] + L[3:]
    m = b + (A - 3) // 2
    st = [c + (A + 1) // 2] + L[3:]
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st
        m = (m - 3) // 2
    if m == 1:
        return 'HALT'
    return [m + 4] + st


def zlike(x):
    """class 0 or -1 (mod 2^11) with nonnegative quotient"""
    for eps in (0, -1):
        f = x - C(eps)
        if all(a % MOD == 0 for a in f.v[:NSYM]) and f.v[NSYM] >= 0 and f.v[NSYM] % MOD == 0:
            return eps
    return None


def suffix_a(L, ZL):
    n = len(ZL)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == ZL[k:]:
            return k
    return None


STATS = dict(runs=0, final=0, deep=0, macro=0, chain=0, glue=0, coinc=0,
             nest_spurious=0, top_spurious=0, deepest_sp=0, ell_max=0)
BADNEST = []


def prover(L, ZL, s0, H0, kap0, d0, LC, val, nested, cap=100000):
    """returns ('FINAL', ell, a, head) or ('DEEP', ell, None, None);
    LC = concrete parallel list under symbol assignment val;
    d0 = None disables the contract check (never used here; always checked)."""
    L = list(L)
    ell = 0
    while True:
        assert ell < cap, 'step cap exceeded'
        a = suffix_a(L, ZL)
        if a is not None:
            exp = H0 * (1 << s0) + d0 + C(3 * ell) + O1 + kap0
            for z in ZL[:a]:
                exp = exp + z
            if L[0] == exp:
                assert LC == [x.sub_val(val) for x in L], 'concrete desync at final'
                return ('FINAL', ell, a, L[0])
            if nested:
                STATS['nest_spurious'] += 1
            else:
                STATS['top_spurious'] += 1
            STATS['coinc'] += 1
        A = L[0]
        try:
            pA = A.par()
        except Undecided:
            pA = None
        Hb = L[1] if len(L) > 1 else Z0
        if pA == 0 and len(L) >= 3 and L[2] == Hb * 2:
            nxt = [Hb * 4 + (L[0] - Hb) + T3] + L[3:]
            assert dstep(L) == nxt, 'macro unfaithful'
            LC = cstep(LC)
            assert LC != 'HALT' and LC == [x.sub_val(val) for x in nxt], 'concrete desync (macro)'
            STATS['macro'] += 1
            L, ell = nxt, ell + 1
            continue
        if pA == 1:
            b = L[1] if len(L) > 1 else Z0
            c = L[2] if len(L) > 2 else Z0
            q0 = A + b + b + T3
            sp = q0.v2()
            assert sp >= 1, 'q0 odd with odd A impossible'
            window = list(L[3:])
            if sp >= K:
                # ---- DEEP BRANCH: continuation must hand off within the family
                for a_n in (0, 1, 2):
                    rest = window[a_n:]
                    i = 0
                    while i < len(rest) and rest[i] == b * (1 << (i + 2)):
                        i += 1
                    for x in rest[i:]:
                        if zlike(x) is None:
                            raise AssertionError('deep continuation out of family: %r' % (x.v,))
                STATS['deep'] += 1
                STATS['deepest_sp'] = max(STATS['deepest_sp'], sp)
                return ('DEEP', ell + 1, None, None)
            # ---- shallow branch: nested excursion, executed recursively
            o1 = q0.div2k(sp)
            cp = c + (A + O1).half()
            kapn = cp - o1 * (1 << (sp - 1))
            nest = [o1 + O1] + [o1 * (1 << i) for i in range(sp - 1)] \
                   + [o1 * (1 << (sp - 1)) + kapn] + window
            assert dstep(L) == nest, 'chain unfaithful'
            LCn = cstep(LC)
            assert LCn != 'HALT' and LCn == [x.sub_val(val) for x in nest], 'concrete desync (chain)'
            STATS['chain'] += 1
            kind, en, an, hn = prover(nest, window, sp, o1, kapn, O1, LCn, val, True, cap)
            if kind == 'DEEP':
                return ('DEEP', ell + 1 + en, None, None)
            LC = [hn.sub_val(val)] + [w.sub_val(val) for w in window[an:]]
            L = [hn] + window[an:]
            ell += 1 + en
            continue
        STATS['glue'] += 1
        nxt = dstep(L)
        LC = cstep(LC)
        assert LC != 'HALT' and LC == [x.sub_val(val) for x in nxt], 'concrete desync (glue)'
        L, ell = nxt, ell + 1


def make_start(rho, r0, tailpat):
    H = F6(6 * MOD, MOD, 0, 0, 0, 0, MOD)          # 6*2^11 u + 2^11 h + 2^11
    d = F6(0, 0, 1 << K, 0, 0, 0, rho)             # 2^8 tt + rho
    kap = C(-1)
    tail = []
    for i, pi in enumerate(tailpat):
        co = [0] * (NSYM + 1)
        co[3 + i] = MOD                              # z_{i+1} symbol at index 3+i
        co[NSYM] = MOD - pi
        tail.append(F6(*co))
    L = [H + d] + [H * (1 << i) for i in range(r0)] + [H * (1 << r0) + kap] + list(tail)
    return L, H, d, tail


if __name__ == '__main__':
    random.seed(20261012)
    tails4 = [[], [0], [1], [0, 0]]
    fails = []
    nr = 0
    for r0 in (1, 2, 3, 4, 5):
        for rho in range(256):
            for tp in tails4:
                nr += 1
                L, H, d, tail = make_start(rho, r0, tp)
                try:
                    for iv in range(3):
                        if iv == 0:
                            val = (0, 0, 0, 0, 0, 0)
                        elif iv == 1:
                            val = tuple(random.randrange(0, 1 << 20) for _ in range(NSYM))
                        else:
                            val = tuple(random.randrange(0, 1 << 40) for _ in range(NSYM))
                        LC = [x.sub_val(val) for x in L]
                        kind, ell, a, head = prover(L, tail, r0 + 1, H, C(-1), d,
                                                    LC, val, False)
                        STATS['runs'] += 1
                        if kind == 'FINAL':
                            STATS['final'] += 1
                        else:
                            STATS['deep'] = STATS['deep']  # counted in prover
                        STATS['ell_max'] = max(STATS['ell_max'], ell)
                except Exception as ex:
                    fails.append((r0, rho, tuple(tp), repr(ex)))
    print('TaskC: starts=%d  symbolic-runs(incl. concrete parallels)=%d  failures=%d'
          % (nr, STATS['runs'], len(fails)))
    if fails:
        print('TaskC: FAIL -- first failures:', fails[:10])
    else:
        print('TaskC: PASS -- 0 failures over all %d canonical starts '
              '(kap=-1, r0=1..5, rho=0..255, 4 tail patterns)' % nr)
    print('TaskC stats:', STATS)
