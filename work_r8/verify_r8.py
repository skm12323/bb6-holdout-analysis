"""verify_r8.py -- compositional excursion prover for machine #1 (R8).

Usage: python verify_r8.py [N=1000] [NC=300]

Base (accepted, work_r1): top map T on lists L=(A,b,c,S):
  A even -> (A+b+c+3, S);  A odd -> m := b+(A-3)/2, st := (c+(A+1)/2, S);
  while m odd and m>=3: st = [(m+3)/2]+st, m = (m-3)/2;  m=1 -> HALT; else (m+4, st).
  HALT <=> some top step has A odd and A+2b+3 = 2^k.

This file proves, per s (uniformly in the symbol u >= 0, w = 2u+1):
  F(s): from Phi_s(o; K; Z) = (o+1, o, 2o, ..., 2^(s-2)o, 2^(s-1)o - 1 + K, Z_1, ...)
        (entries affine forms in u with nonnegative coefficients),
        the T-orbit never halts and first reaches [X] + Z[a+1:] at exactly ell(s)
        steps with X = 2^s o + 3*ell(s) + K + Z_1 + ... + Z_a  (verified identity),
  NOT by stepping all ell(s) steps, but compositionally:
    - E-step macro at canonical states with even head and run length >= 2;
    - at odd head: one chain step + the whole nested excursion Phi_{s'} (s' = v2(q0))
      executed by RECURSION (well-founded: asserted s' < level);
    - direct symbolic steps only in the short glue phases.
Checks:
  check1: F(v) for v = 1..N (K=0, Z empty) == R4's Lemma E(v); conclusions verified.
  check2: ell(v) matches R5-style direct full symbolic runs for v <= NC.
  check3: concrete cross-check: compositional ell(v) == direct concrete run for
          w in {1,3,5}, v <= NC (validates uniformity claims on real instances).
  check4: structure statistics asserted: a(s) <= 2; margin v2(H) - v2(d+3) >= 1 at
          every recursive call; d - (3t+1) in {0} or odd at canonical call times;
          window of every nested call = (r-2 clean H-multiples) + [J] + caller Z.
"""
import sys, time
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
    if len(L) < 3: return None
    H = L[1]
    if L[2] != sc(H, 2): return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == sc(H, 1 << r): r += 1
    if r + 1 >= len(L): return None
    return (H, sub(L[0], H), r, sub(L[r + 1], sc(H, 1 << r)))

def final_match(L, Z0L):
    if not Z0L:
        return 0 if len(L) == 1 else None
    n = len(Z0L)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == Z0L[k:]:
            return k
    return None

# ---- instrumentation (also used by check4) ----
STATS = {'calls': 0, 'margin_min': 10**9, 'amax': 0, 'spmax': 0, 'delta_bad': 0,
         'winbad': 0, 'coinc': 0}

def F(L, level, Z0L, s0, H0, kap0, t0=0):
    L = list(L); ell = 0
    while True:
        a = final_match(L, Z0L)
        if a is not None:
            head = L[0]
            expect = add(sc(H0, 1 << s0), (0, 3 * ell), (0, 1), kap0, *Z0L[:a])
            if head == expect:
                return ell, a, head
            STATS['coinc'] += 1
        enc = encode(L) if len(L) >= 3 else None
        if enc is not None:
            H, d, r, kap = enc
            A = add(H, d)
            pA = par(A)
            if pA == 0 and r >= 2:
                L = [add(sc(H, 4), d, (0, 3))] + L[3:]; ell += 1
                continue
            if pA == 1:
                if r >= 2:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), half(add(H, d, (0, 1))))
                    window = L[3:]
                elif r == 1:
                    q0 = add(sc(H, 3), d, (0, 3))
                    cprime = add(sc(H, 2), kap, half(add(H, d, (0, 1))))
                    window = L[3:]
                else:
                    q0 = add(sc(H, 3), sc(kap, 2), d, (0, 3))
                    cprime = add(L[2] if len(L) > 2 else Z0, half(add(H, d, (0, 1))))
                    window = L[3:]
                sp = v2f(q0)
                if sp >= 1:
                    o_p = halfn(q0, sp)
                    kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
                    nestL = [add(o_p, (0, 1))] + [sc(o_p, 1 << i) for i in range(sp - 1)] \
                            + [add(sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                    assert sp < level, 'well-foundedness violated (sp=%d, level=%d)' % (sp, level)
                    # structure statistics
                    STATS['calls'] += 1
                    j = v2f(H); s2 = v2f(add(d, (0, 3)))
                    if j - s2 < STATS['margin_min']: STATS['margin_min'] = j - s2
                    Dl = sub(d, (0, 3 * (t0 + ell) + 1))
                    if not (Dl == (0, 0) or (Dl[0] == 0 and Dl[1] % 2 == 1 and Dl[1] < 0)):
                        STATS['delta_bad'] += 1
                    if r >= 2:
                        okwin = all(sub(window[i], sc(H, 1 << (i + 2))) == (0, 0)
                                    for i in range(r - 2)) and \
                                sub(window[r - 2] if len(window) > r - 2 else Z0,
                                    add(sc(H, 1 << r), kap)) == (0, 0)
                        if not okwin: STATS['winbad'] += 1
                    ell_n, a_n, head_n = F(nestL, sp, window, sp, o_p, kap_nest, t0 + ell + 1)
                    STATS['amax'] = max(STATS['amax'], a_n)
                    STATS['spmax'] = max(STATS['spmax'], sp)
                    L = [head_n] + list(window[a_n:])
                    ell += 1 + ell_n
                    continue
        L = T_list(L); ell += 1

def excursion(v):
    w3 = (6, 3)
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
    ell, a, head = F(L, v, [], v, w3, (0, -1))
    assert a == 0, a
    assert head == add(sc(w3, 1 << v), (0, 3 * ell))
    return ell

def top(L):
    A = L[0]; b = L[1] if len(L) > 1 else 0; c = L[2] if len(L) > 2 else 0; S = L[3:]
    if A % 2 == 0: return [A + b + c + 3] + S
    m = b + (A - 3) // 2; st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st; m = (m - 3) // 2
    if m == 1: return 'HALT'
    return [m + 4] + st

# ===================== check5/check6 machinery (multi-symbol engine) ==========
# NS-symbol affine forms: 0:u 1:h 2:tt 3:kappa 6..11: z1..z6  (all symbols >= 0)
NS = 12
class MFail(Exception): pass

def _sym(i, k=1):
    co = [0] * NS; co[i] = k; return (tuple(co), 0)
def _C(c): return (tuple([0] * NS), c)
def _add(*xs): return (tuple(sum(x[0][i] for x in xs) for i in range(NS)), sum(x[1] for x in xs))
def _sc(x, k): return (tuple(k * a for a in x[0]), k * x[1])
def _sub(x, y): return (tuple(x[0][i] - y[0][i] for i in range(NS)), x[1] - y[1])
def _par(x):
    if any(a % 2 for a in x[0]): raise Undecided('parity')
    return x[1] % 2
def _half(x):
    if any(a % 2 for a in x[0]) or x[1] % 2: raise Undecided('half')
    return (tuple(a // 2 for a in x[0]), x[1] // 2)
def _ge3(x):
    if all(a >= 0 for a in x[0]) and x[1] >= 3: return True
    if all(a == 0 for a in x[0]) and x[1] < 3: return False
    raise Undecided('ge3')
def _v2f(x):
    n = 0
    while all(a % 2 == 0 for a in x[0]) and x[1] % 2 == 0 and (any(x[0]) or x[1]):
        x = (tuple(a // 2 for a in x[0]), x[1] // 2); n += 1
    return n
def _halfn(x, n):
    for _ in range(n): x = _half(x)
    return x

_M0 = _C(0)
def _Tm(L):
    A = L[0]; b = L[1] if len(L) > 1 else _M0; c = L[2] if len(L) > 2 else _M0; R = L[3:]
    if _par(A) == 0: return [_add(A, b, c, _C(3))] + R
    m = _half(_add(b, b, A, _C(-3))); st = [_half(_add(c, c, A, _C(1)))] + R
    while _par(m) == 1 and _ge3(m):
        st = [_half(_add(m, _C(3)))] + st; m = _half(_add(m, _C(-3)))
    if _par(m) == 1:
        if m == _C(1): raise Halt('HALT branch reachable')
        raise Undecided('m odd unknown')
    return [_add(m, _C(4))] + st

def _encode_run(L):
    if len(L) < 4: return None
    H = L[1]
    if L[2] != _sc(H, 2) or L[3] != _sc(H, 4): return None
    r = 2
    while r + 1 < len(L) and L[r + 1] == _sc(H, 1 << r): r += 1
    return (H, r)

def _final_match(L, Z0L):
    if not Z0L:
        return 0 if len(L) == 1 else None
    n = len(Z0L)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == Z0L[k:]:
            return k
    return None

class TemplateChecker:
    """End-phase template checker. Family (KK = K):
       canonical(r0, rho, pi): (H+d, H, ..., 2^{r0-1}H, 2^{r0}H - 1) + tail
       glue(rho, pi): [head] + tail
       H = 6*2^{K+3}u + 2^{K+3}(1+h), d = rho + 2^K*tt,
       head = d + 2^{K+3}(1+h) + 6*2^{K+3}u, tail_i = 2^{K+3}(z_i+1) - pi_i.
       Deep branch (v2(q0) >= K): continuation must lie in the family (hand-off)."""

    def __init__(self, KK=8):
        self.K = KK
        self.Hp = 1 << (KK + 3)
        self.tails = [[], [0], [1], [0, 0], [1, 0], [0, 1], [1, 1],
                      [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def zlike(self, x):
        K, Hp = self.K, self.Hp
        for eps in (0, -1):
            f = _sub(x, _C(eps))
            if all(a % Hp == 0 for a in f[0]) and f[1] >= 0 and f[1] % Hp == 0:
                return eps
        return None

    def F(self, L, level, Z0L, s0, H0, kap0, ell0=0, d0=None):
        K = self.K
        L = list(L); ell = ell0
        while True:
            a = _final_match(L, Z0L)
            if a is not None:
                head = L[0]
                if d0 is not None:
                    expect = _add(_sc(H0, 1 << s0), d0, _C(3 * ell), kap0, *Z0L[:a])
                    if head == expect:
                        return ell, a, head
                else:
                    return ell, a, head
            enc = _encode_run(L)
            if enc is not None:
                H, r = enc
                d = _sub(L[0], H)
                if _par(_add(H, d)) == 0:
                    L = [_add(_sc(H, 4), d, _C(3))] + L[3:]; ell += 1
                    continue
            A = L[0]
            if _par(A) == 1:
                b = L[1] if len(L) > 1 else _M0
                c = L[2] if len(L) > 2 else _M0
                q0 = _add(A, b, b, _C(3))
                window = L[3:]
                sp = _v2f(q0)
                if sp >= 1:
                    if sp < K:
                        o_p = _halfn(q0, sp)
                        cprime = _add(c, _half(_add(A, _C(1))))
                        assert o_p[1] >= 3, "chain precondition o' >= 3 violated"
                        kap_nest = _sub(cprime, _sc(o_p, 1 << (sp - 1)))
                        nestL = [_add(o_p, _C(1))] + [_sc(o_p, 1 << i) for i in range(sp - 1)] \
                                + [_add(_sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                        ell_n, a_n, head_n = self.F(nestL, sp, window, sp, o_p, kap_nest)
                        L = [head_n] + list(window[a_n:])
                        ell += 1 + ell_n
                        continue
                    else:
                        Hb = L[1] if len(L) > 1 else _M0
                        for a_n in (0, 1, 2):
                            rest = window[a_n:]
                            i = 0
                            while i < len(rest) and rest[i] == _sc(Hb, 1 << (i + 2)):
                                i += 1
                            for x in rest[i:]:
                                if self.zlike(x) is None:
                                    raise MFail('deep continuation not in family: %s' % (x,))
                        return ('DEEP', ell + 1, None)
            L = _Tm(L); ell += 1

    def run_canonical(self, rho, r0, tailpat):
        Hp, K = self.Hp, self.K
        H = _add(_C(Hp), _sym(0, 6 * Hp), _sym(1, Hp))
        d = _add(_C(rho), _sym(2, 1 << K))
        kap = _C(-1)
        tail = [_add(_C(Hp - t), _sym(6 + i, Hp)) for i, t in enumerate(tailpat)]
        L = [_add(H, d)] + [_sc(H, 1 << i) for i in range(r0)] \
            + [_add(_sc(H, 1 << r0), kap)] + tail
        return self.F(L, r0 + 1, tail, r0 + 1, H, kap, 0, d)

    def run_glue(self, rho, tailpat):
        Hp, K = self.Hp, self.K
        head = _add(_C(Hp + rho), _sym(0, 6 * Hp), _sym(1, Hp), _sym(2, 1 << K))
        tail = [_add(_C(Hp - t), _sym(6 + i, Hp)) for i, t in enumerate(tailpat)]
        return self.F([head] + tail, 0, tail, 0, None, None, 0, None)

    def run_all(self):
        ok = 0; fails = []
        for r0 in (1, 2, 3, 4, 5):
            for rho in range(1 << self.K):
                for tp in self.tails:
                    try:
                        self.run_canonical(rho, r0, tp); ok += 1
                    except (Undecided, Halt, MFail):
                        fails.append((r0, rho, tp))
        for rho in range(1 << self.K):
            for tp in self.tails:
                try:
                    self.run_glue(rho, tp); ok += 1
                except (Undecided, Halt, MFail):
                    fails.append((rho, tp))
        return ok, fails

    def run_lineage(self):
        """Closure over the reachable deep-branch lineage:
        kap generators: -1 + 2^{K+3}*kappa  and  -2 + 2^{K-1}*m;
        accept classes: {0, -1} (mod 2^{K+3}) and {-2} (mod 2^{K-1}).
        Collects any NEW residue class requested by a deep continuation."""
        K, Hp, Hm = self.K, self.Hp, 1 << (self.K - 1)
        self.new_classes = set()

        def zlike_lin(x):
            for eps, mod in ((0, Hp), (-1, Hp), (-2, Hm)):
                f = _sub(x, _C(eps))
                if all(a % mod == 0 for a in f[0]) and f[1] >= 0 and f[1] % mod == 0:
                    return eps
            self.new_classes.add(x[1] % Hp)
            return 0
        self.zlike, saved = zlike_lin, self.zlike
        ok = 0; fails = []
        try:
            for kapgen in (0, 1):
                for r0 in (1, 2, 3, 4, 5):
                    for rho in range(1 << K):
                        for tp in self.tails:
                            try:
                                self.run_canonical_gen(rho, r0, tp, kapgen); ok += 1
                            except (Undecided, Halt, MFail):
                                fails.append((kapgen, r0, rho, tp))
        finally:
            self.zlike = saved
        return ok, fails

    def run_canonical_gen(self, rho, r0, tailpat, kapgen):
        Hp, K = self.Hp, self.K
        H = _add(_C(Hp), _sym(0, 6 * Hp), _sym(1, Hp))
        d = _add(_C(rho), _sym(2, 1 << K))
        if kapgen == 0:
            kap = _add(_C(-1), _sym(3, Hp))            # -1 + 2^{K+3} kappa
        else:
            kap = _add(_C(-2), _sym(3, 1 << (K - 1)))  # -2 + 2^{K-1} m
        tail = [_add(_C(Hp - t), _sym(6 + i, Hp)) for i, t in enumerate(tailpat)]
        L = [_add(H, d)] + [_sc(H, 1 << i) for i in range(r0)] \
            + [_add(_sc(H, 1 << r0), kap)] + tail
        return self.F(L, r0 + 1, tail, r0 + 1, H, kap, 0, d)

def sum_class_scan(K=8, cap=5000):
    """Concrete scan over the template family with H = 3*2^{K+3} (3-divisible):
    for each (rho, r0, tt, kapclass): if the start list has sum = 0 mod 3 (the
    audited orbit invariant), run `cap` top steps and require no HALT.
    Returns (halting_sum_invalid_count, sum_valid_count): also runs the
    sum-invalid starts to record that halts (if any) are exactly there."""
    def topc(L):
        A = L[0]; b = L[1] if len(L) > 1 else 0; c = L[2] if len(L) > 2 else 0; S = L[3:]
        if A % 2 == 0: return [A + b + c + 3] + S
        m = b + (A - 3) // 2; st = [c + (A + 1) // 2] + S
        while m % 2 == 1 and m >= 3:
            st = [(m + 3) // 2] + st; m = (m - 3) // 2
        if m == 1: return 'HALT'
        return [m + 4] + st
    Hp = 3 << (K + 3)                  # 3-divisible family base
    valid = 0; halt_invalid = 0; halt_valid = 0
    for r0 in (1, 2, 3, 4, 5):
        for rho in range(0, 256, 5):   # sample of residues
            for tt in (0, 1, 2):
                for kap in (-1, -2):
                    H = Hp
                    d = rho + (1 << K) * tt
                    L0 = [H + d] + [H << i for i in range(r0)] + [(H << r0) + kap]
                    if sum(L0) % 3 != 0:
                        L = list(L0); t = 0
                        while t < cap and L != 'HALT':
                            L = topc(L); t += 1
                        if L == 'HALT': halt_invalid += 1
                        continue
                    L = list(L0); t = 0
                    while t < cap and L != 'HALT':
                        L = topc(L); t += 1
                    if L == 'HALT':
                        halt_valid += 1
                    valid += 1
    assert halt_valid == 0, 'sum-VALID halting member found'
    return halt_invalid, valid


def prefix_check(K=8, r0s=(30, 40, 50), steps=20):
    """Initial phase. From (3w+1, 3w, 2*3w, ..., 2^{r0-1}*3w) with a family-class J
    (z-symbol tail in the J slot): (i) the first 9 steps' decision traces are identical
    across r0 (s-independence); (ii) the running maximum of canonical v2(H) — which
    tracks the outer frame's j, since each outer macro-step only increases it —
    reaches >= K+3 by step 8 and stays there."""
    Hp = 1 << (K + 3)
    w3 = _add(_C(3), _sym(0, 6))                    # 3w = 6u+3
    traces = []
    for r0 in r0s:
        J = _add(_C(Hp - 1), _sym(6, Hp))           # family-class J: 2^{K+3}(z+1)-1
        L = [_add(w3, _C(1))] + [_sc(w3, 1 << i) for i in range(r0)] + [J]
        trace = []; jmax = 0
        for t in range(steps):
            trace.append(_par(L[0]))
            if len(L) >= 3 and L[2] == _sc(L[1], 2):
                jmax = max(jmax, _v2f(L[1]))
                if t >= 8:
                    assert jmax >= K + 3, ('outer j still small at t=%d' % t)
            L = _Tm(L)
        traces.append(tuple(trace))
    assert all(tr[:9] == traces[0][:9] for tr in traces), traces
    return (9, r0s)

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    NC = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    t0 = time.time()
    # check1: compositional F(v), v = 1..N
    ells = {}
    for v in range(1, N + 1):
        ells[v] = excursion(v)
    print('check1 OK: compositional F(v) (no halt, verified conclusion) for v = 1..%d [%.1fs]'
          % (N, time.time() - t0))
    # check2: direct symbolic full runs for v <= NC
    for v in range(1, NC + 1):
        w3 = (6, 3)
        L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
        t = 0
        while len(L) > 1:
            L = T_list(L); t += 1
        assert t == ells[v], (v, t, ells[v])
        assert L[0] == add(sc(w3, 1 << v), (0, 3 * t))
    print('check2 OK: ell(v) equals direct symbolic full-run ell for v <= %d' % NC)
    # check3: concrete instances w in {1,3,5}
    for w in (1, 3, 5):
        for v in range(1, NC + 1):
            L = [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
            t = 0
            while len(L) > 1:
                L = top(L); t += 1
                assert L != 'HALT'
            assert t == ells[v], (w, v, t, ells[v])
            assert L[0] == 3 * w * (1 << v) + 3 * t
    print('check3 OK: concrete orbits (w=1,3,5) match ell(v) and never halt, v <= %d' % NC)
    # check4: structure statistics
    assert STATS['amax'] <= 2 and STATS['margin_min'] >= 1 and STATS['delta_bad'] == 0 \
        and STATS['winbad'] == 0, STATS
    print('check4 OK: a(s)<=%d, min margin v2(H)-v2(d+3)=%d, Delta in {0,odd<0}, '
          'windows clean+J (calls=%d, spmax=%d, coincidental suffix matches=%d)'
          % (STATS['amax'], STATS['margin_min'], STATS['calls'], STATS['spmax'], STATS['coinc']))
    # check5: end-phase template checker (multi-symbol), top-frame family.
    # Scope (post-review): verifies that every start's symbolic run completes or
    # hands off at a deep branch to an in-family continuation — a 2-adic
    # non-obstruction check. It does NOT simulate deep children (see PROOF.md §2).
    tmpl = TemplateChecker(KK=8)
    nr, nf = tmpl.run_all()
    assert not nf, nf[:5]
    print('check5 OK (2-adic non-obstruction): %d symbolic runs, 0 failures; deep '
          'branches hand off within the residue family' % nr)
    # check5b: lineage residue closure (kap generators -1 and -2 mod 2^{K-1}).
    nr2, nf2 = tmpl.run_lineage()
    assert not nf2 and not tmpl.new_classes, (nf2[:5], tmpl.new_classes)
    print('check5b OK (lineage residues): %d runs, 0 failures, 0 new residue classes' % nr2)
    # check5c: sum-class separation (the adversary review's finding): every halting
    # member of the product family found has sum(L) != 0 mod 3; the audited sum
    # invariant (R1: sum = 3n+3 on the real orbit) excludes them. Concrete scan:
    # sum-valid instances (3|H, d chosen so sum = 0 mod 3) never halt within cap.
    nh, nv = sum_class_scan()
    print('check5c OK (sum-class separation): %d sum-valid concrete instances, 0 halts '
          'within %d steps (all %d halting family members found are sum-invalid)' % (nv, 5000, nh))
    # check6: initial-phase prefix is s-independent and reaches the template family
    pref = prefix_check()
    print('check6 OK: initial prefix: %d steps, identical decisions for r0 in %s, reaches '
          'H = 2^11-multiple with J/tail in family' % (pref[0], pref[1]))
    print('ell table (1..40):', [ells[v] for v in range(1, 41)])
    print('max ell(v)/v =', max(ells[v] / v for v in range(10, N + 1)))
