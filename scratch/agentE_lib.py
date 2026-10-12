"""agentE_lib.py -- shared machinery for agent E (corrected end-phase template route).

Copied from work_r8/verify_r8.py:
  * single-symbol exact core (affine forms in u, w = 2u+1): T_list / encode / top;
  * multi-symbol core (12 symbols) of the template engine: _Tm / _encode_run /
    _final_match and the form arithmetic;
  * TemplateChecker -> TemplateCheckerE, hardened per the r8 reviews:
      F3  the chain halting precondition o' >= 3 (nonnegative coefficients,
          const >= 3) is enforced at EVERY sp < K chain construction, and is
          checked + logged (not skipped) at deep branches sp >= K;
      F4  the mid-excursion contract is enforced at nested frames too
          (d0 = 1, the exact child-frame head offset); suffix coincidences
          are counted instead of silently accepted;
      F5  deep branches at nesting depth >= 1 propagate ('DEEP', ell, None)
          cleanly instead of raising TypeError;
      deep branches log their full symbolic context (o', kap_nest, window and
          the symbolic child list nestL) for concrete child-prefix coverage.
    Glue starts are dropped (auditor-2 V5: vacuous).
Added here: concrete symbol instantiation, sum-mod-3-valid assignment
generation, and a full concrete-orbit runner with a deep-fire census.
Python 3 stdlib only.
"""
import sys
sys.setrecursionlimit(100000)


class Undecided(Exception):
    pass


class Halt(Exception):
    pass


class MFail(Exception):
    pass


# ---------------- single-symbol exact core (verbatim from verify_r8.py) ----------------
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


def top(L):
    """Concrete (integer) top map, verbatim from verify_r8.py."""
    A = L[0]; b = L[1] if len(L) > 1 else 0; c = L[2] if len(L) > 2 else 0; S = L[3:]
    if A % 2 == 0: return [A + b + c + 3] + S
    m = b + (A - 3) // 2; st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st; m = (m - 3) // 2
    if m == 1: return 'HALT'
    return [m + 4] + st


# ---------------- multi-symbol core (verbatim from verify_r8.py) ----------------
# NS-symbol affine forms: 0:u 1:h 2:tt 3:kappa 6..11: z1..z6  (all symbols >= 0)
NS = 12


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


# ---------------- hardened template checker ----------------
def build_start_sym(r0, rho, kapgen, tailpat):
    """Symbolic start list of the (K = 8) template family, plus its pieces."""
    Hp = 2048
    H = _add(_C(Hp), _sym(0, 6 * Hp), _sym(1, Hp))
    d = _add(_C(rho), _sym(2, 256))
    kap = _add(_C(-1), _sym(3, Hp)) if kapgen == 0 else _add(_C(-2), _sym(3, 128))
    tail = [_add(_C(Hp - p), _sym(6 + i, Hp)) for i, p in enumerate(tailpat)]
    L = [_add(H, d)] + [_sc(H, 1 << i) for i in range(r0)] \
        + [_add(_sc(H, 1 << r0), kap)] + tail
    return L, tail, H, d, kap


class TemplateCheckerE(object):
    """Hardened copy of verify_r8.TemplateChecker (glue starts dropped).

    Family (K = 8): canonical(r0, rho, tail, kapgen):
        (H+d, H, 2H, ..., 2^{r0-1}H, 2^{r0}H + kap) + tail,
        H = 6*2^11 u + 2^11 (1+h), d = rho + 2^8 tt,
        kap = -1 + 2^11 kappa (kapgen 0)  or  -2 + 2^7 m (kapgen 1),
        tail_i = 2^11 (z_i + 1) - pi_i.
    Returns (ell, a, head) on verified contract completion, ('DEEP', ell, None)
    at a deep branch (sp >= K) after checking the continuation family.
    """

    def __init__(self, KK=8):
        self.K = KK
        self.Hp = 1 << (KK + 3)
        self.tails = [[], [0], [1], [0, 0], [1, 0], [0, 1], [1, 1],
                      [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.deep_log = []
        self.stats = {'coinc_top': 0, 'coinc_nest': 0, 'nested': 0, 'deep': 0,
                      'tm': 0, 'deep_o_bad': 0}

    def zlike(self, x):
        """Lineage continuation family (corrected): {0, -1} mod 2^{K+3} for the
        z/J entries of -1-class parents, plus {-2} mod 2^{K-1} (the corrected
        family admits kap = -2 + 2^{K-1} m starts, whose window entries keep
        that class).  Anything else is out of family (MFail by the caller)."""
        Hp, Hm = self.Hp, 1 << (self.K - 1)
        for eps, mod in ((0, Hp), (-1, Hp), (-2, Hm)):
            f = _sub(x, _C(eps))
            if all(a % mod == 0 for a in f[0]) and f[1] >= 0 and f[1] % mod == 0:
                return eps
        return None

    def F(self, L, level, Z0L, s0, H0, kap0, ell0=0, d0=None, cfg=None, depth=0):
        K = self.K
        L = list(L); ell = ell0
        while True:
            if ell - ell0 > 20000:
                raise MFail('runaway frame')
            a = _final_match(L, Z0L)
            if a is not None:
                head = L[0]
                if d0 is None:
                    return ell, a, head
                expect = _add(_sc(H0, 1 << s0), d0, _C(3 * ell), kap0, *Z0L[:a])
                if head == expect:
                    return ell, a, head
                # suffix coincidence with wrong head: count, keep stepping
                if depth == 0:
                    self.stats['coinc_top'] += 1
                else:
                    self.stats['coinc_nest'] += 1
            enc = _encode_run(L)
            if enc is not None:
                H, r = enc
                d = _sub(L[0], H)
                if _par(_add(H, d)) == 0:
                    L = [_add(_sc(H, 4), d, _C(3))] + L[3:]
                    ell += 1
                    continue
            A = L[0]
            if _par(A) == 1:
                b = L[1] if len(L) > 1 else _M0
                c = L[2] if len(L) > 2 else _M0
                q0 = _add(A, b, b, _C(3))
                window = L[3:]
                sp = _v2f(q0)
                if sp >= 1:
                    o_p = _halfn(q0, sp)
                    cprime = _add(c, _half(_add(A, _C(1))))
                    kap_nest = _sub(cprime, _sc(o_p, 1 << (sp - 1)))
                    nestL = [_add(o_p, _C(1))] + [_sc(o_p, 1 << i) for i in range(sp - 1)] \
                            + [_add(_sc(o_p, 1 << (sp - 1)), kap_nest)] + list(window)
                    if sp < K:
                        # F3: halting precondition of the chain construction
                        if not (o_p[1] >= 3 and all(x >= 0 for x in o_p[0])):
                            raise MFail("chain precondition o' >= 3 violated: %r" % (o_p,))
                        self.stats['nested'] += 1
                        # F4: contract enforced at nested frames (d0 = 1)
                        res = self.F(nestL, sp, window, sp, o_p, kap_nest,
                                     0, _C(1), cfg, depth + 1)
                        if isinstance(res, tuple) and res[0] == 'DEEP':
                            # F5: propagate deep branch from depth >= 1
                            return ('DEEP', ell + 1 + res[1], None)
                        ell_n, a_n, head_n = res
                        L = [head_n] + list(window[a_n:])
                        ell += 1 + ell_n
                        continue
                    # --- deep branch (sp >= K): log full context, then hand off ---
                    ok_op = (all(x >= 0 for x in o_p[0]) and o_p[1] >= 3)
                    if not ok_op:
                        self.stats['deep_o_bad'] += 1
                    Hb = L[1] if len(L) > 1 else _M0
                    for a_n in (0, 1, 2):
                        rest = window[a_n:]
                        i = 0
                        while i < len(rest) and rest[i] == _sc(Hb, 1 << (i + 2)):
                            i += 1
                        for x in rest[i:]:
                            if self.zlike(x) is None:
                                raise MFail('deep continuation not in family: %s' % (x,))
                    self.stats['deep'] += 1
                    self.deep_log.append({'cfg': cfg, 'depth': depth, 'sp': sp,
                                          'o_p': o_p, 'kap_nest': kap_nest,
                                          'window': list(window), 'nestL': nestL,
                                          'o_ok': ok_op})
                    return ('DEEP', ell + 1, None)
            L = _Tm(L); ell += 1
            self.stats['tm'] += 1

    def run_canonical_gen(self, rho, r0, tailpat, kapgen, cfg=None):
        L, tail, H, d, kap = build_start_sym(r0, rho, kapgen, tailpat)
        return self.F(L, r0 + 1, tail, r0 + 1, H, kap, 0, d, cfg, 0)


# ---------------- concrete helpers ----------------
def eval_form(f, env):
    c, k = f
    s = k
    for i, a in enumerate(c):
        if a:
            s += a * env[i]
    return s


def eval_sym_list(Ls, env):
    return [eval_form(x, env) for x in Ls]


def build_start_conc(r0, rho, kapgen, tailpat, env):
    """Concrete start list; must agree with eval_sym_list(build_start_sym(...))."""
    Hp = 2048
    H = Hp * (6 * env[0] + 1 + env[1])
    d = rho + 256 * env[2]
    kap = (-1 + Hp * env[3]) if kapgen == 0 else (-2 + 128 * env[3])
    L = [H + d] + [H << i for i in range(r0)] + [(H << r0) + kap]
    L += [Hp * (env[6 + i] + 1) - p for i, p in enumerate(tailpat)]
    return L


def gen_sumvalid_envs(r0, rho, kapgen, tailpat, k_want, rng,
                      u_hi=3, h_hi=4, m_hi=2, z_hi=3, tt_hi=6):
    """Deterministic (rng-seeded) sample of symbol assignments with
    sum(start) = 0 mod 3 (the audited orbit sum invariant)."""
    envs = []
    seen = set()
    tries = 0
    while len(envs) < k_want and tries < 1000:
        env = [0] * NS
        env[0] = rng.randrange(u_hi)
        env[1] = rng.randrange(h_hi)
        env[3] = rng.randrange(m_hi)
        for i in range(len(tailpat)):
            env[6 + i] = rng.randrange(z_hi)
        L0 = build_start_conc(r0, rho, kapgen, tailpat, env)  # env[2] = tt = 0
        tt0 = (-sum(L0)) % 3
        for tt in (tt0, tt0 + 3):
            if tt < tt_hi and len(envs) < k_want:
                env[2] = tt
                key = tuple(env)
                if key not in seen:
                    e2 = list(env)
                    Lc = build_start_conc(r0, rho, kapgen, tailpat, e2)
                    assert sum(Lc) % 3 == 0
                    seen.add(key)
                    envs.append(e2)
        tries += 1
    return envs


def v2i(n):
    v = 0
    while n and n % 2 == 0:
        n //= 2
        v += 1
    return v


def run_orbit(L, cap=20000, deep_log=None):
    """Full concrete orbit (past singletons). Returns (status, steps, L).
    status: 'CAP' = no halt within `cap` top steps; 'HALT' = halted at step
    `steps`; 'LONG' = list length exceeded the sanity bound; 'NEG' anomaly.
    deep_log (optional) collects (t, sp, r) at every deep fire (v2(q0) >= 8),
    r = canonical run length at the fire (-1 if not canonical-shaped)."""
    L = list(L)
    t = 0
    while t < cap:
        if len(L) > 30000:
            return ('LONG', t, L)
        A = L[0]
        if A % 2 == 0:
            if len(L) == 1:
                L = [A + 3]
            else:
                b = L[1]
                c = L[2] if len(L) > 2 else 0
                L = [A + b + c + 3] + L[3:]
        else:
            b = L[1] if len(L) > 1 else 0
            if deep_log is not None:
                q0 = A + 2 * b + 3
                if q0 % 256 == 0:
                    deep_log.append((t, v2i(q0), _canon_r(L)))
            c = L[2] if len(L) > 2 else 0
            m = b + (A - 3) // 2
            st = [c + (A + 1) // 2] + L[3:]
            while m % 2 == 1 and m >= 3:
                st = [(m + 3) // 2] + st
                m = (m - 3) // 2
            if m == 1:
                return ('HALT', t + 1, L)
            if m < 0:
                return ('NEG', t + 1, L)
            L = [m + 4] + st
        t += 1
    return ('CAP', t, L)


def _canon_r(L):
    if len(L) < 3 or L[2] != 2 * L[1]:
        return -1
    r = 1
    while r + 1 < len(L) and L[r + 1] == L[1] << r:
        r += 1
    return r
