"""agentF_lib.py -- instrumented copy of work_r8/verify_r8.py's compositional engine.

Purpose: collect the exact per-frame decomposition of ell(s) needed to prove
ell(s) <= 2 s:
  ell(s) = (#E-macros) + sum over fires (1 + ell(sp_i)) + (#glue steps)
with per-fire records: frame time t, level sp, run length r at fire, return a',
Delta = d - (3t+1), head-parity pattern.

The engine is a verbatim copy of verify_r8.F (single-symbol affine forms in u,
w = 2u+1) plus:
  - ELLCACHE: level -> (ell, contract-relevant data) with the contract asserted
    at every cached use (so caching cannot hide a uniformity failure);
  - a TRACE mode that records the macro-event stream of a frame.

Nothing in work_r8 is modified.
"""
import sys
sys.setrecursionlimit(1000000)


class Undecided(Exception):
    pass


class Halt(Exception):
    pass


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def sc(x, k):
    return (x[0] * k, x[1] * k)


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def par(x):
    if x[0] % 2:
        raise Undecided('parity(u)')
    return x[1] % 2


def half(x):
    if x[0] % 2 or x[1] % 2:
        raise Undecided('half')
    return (x[0] // 2, x[1] // 2)


def ge3(x):
    if x[0] >= 0 and x[1] >= 3:
        return True
    if x[0] == 0 and x[1] < 3:
        return False
    raise Undecided('ge3')


def v2f(x):
    n = 0
    while x[0] % 2 == 0 and x[1] % 2 == 0 and (x[0] or x[1]):
        x = (x[0] // 2, x[1] // 2)
        n += 1
    return n


def halfn(x, n):
    for _ in range(n):
        x = half(x)
    return x


Z0 = (0, 0)


def T_list(L):
    A = L[0]
    b = L[1] if len(L) > 1 else Z0
    c = L[2] if len(L) > 2 else Z0
    R = L[3:]
    if par(A) == 0:
        return [add(A, b, c, (0, 3))] + R
    m = half(add(b, b, A, (0, -3)))
    st = [half(add(c, c, A, (0, 1)))] + R
    while par(m) == 1 and ge3(m):
        st = [half(add(m, (0, 3)))] + st
        m = half(add(m, (0, -3)))
    if par(m) == 1:
        if m == (0, 1):
            raise Halt('HALT branch reachable')
        raise Undecided('m odd unknown')
    return [add(m, (0, 4))] + st


def encode(L):
    if len(L) < 3:
        return None
    H = L[1]
    if L[2] != sc(H, 2):
        return None
    r = 1
    while r + 1 < len(L) and L[r + 1] == sc(H, 1 << r):
        r += 1
    if r + 1 >= len(L):
        return None
    return (H, sub(L[0], H), r, sub(L[r + 1], sc(H, 1 << r)))


def final_match(L, Z0L):
    if not Z0L:
        return 0 if len(L) == 1 else None
    n = len(Z0L)
    for k in range(n, -1, -1):
        if len(L) == 1 + n - k and L[1:] == Z0L[k:]:
            return k
    return None


# ---------------- instrumentation ----------------
STATS = {'calls': 0, 'margin_min': 10 ** 9, 'amax': 0, 'spmax': 0,
         'delta_bad': 0, 'winbad': 0, 'coinc': 0, 'cache_uses': 0}

# level -> list of event dicts for the frame of that level (trace of the
# canonical top excursion of that level); only filled when TRACE[level] set.
TRACE = {}

# level -> {'events': [...], 'ell': int, 'E': int, 'F': int, 'G': int}
FRAME = {}


class F_(object):
    """Frame executor with optional trace and ell-cache."""

    def __init__(self, use_cache=True, trace_levels=None):
        self.use_cache = use_cache
        self.trace_levels = trace_levels or set()
        self.cache = {}          # level -> ell  (contract checked at each use)

    def F(self, L, level, Z0L, s0, H0, kap0, t0=0):
        L = list(L)
        ell = 0
        ev = [] if level in self.trace_levels else None
        while True:
            a = final_match(L, Z0L)
            if a is not None:
                head = L[0]
                expect = add(sc(H0, 1 << s0), (0, 3 * ell), (0, 1), kap0, *Z0L[:a])
                if head == expect:
                    return self._finish(level, ell, a, head, ev)
                STATS['coinc'] += 1
            enc = encode(L) if len(L) >= 3 else None
            if enc is not None:
                H, d, r, kap = enc
                A = add(H, d)
                pA = par(A)
                if pA == 0 and r >= 2:
                    if ev is not None:
                        ev.append({'type': 'E', 't': ell, 'r': r, 'd': d,
                                   'j': v2f(H)})
                    L = [add(sc(H, 4), d, (0, 3))] + L[3:]
                    ell += 1
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
                        cprime = add(L[2] if len(L) > 2 else Z0,
                                     half(add(H, d, (0, 1))))
                        window = L[3:]
                    sp = v2f(q0)
                    if sp >= 1:
                        o_p = halfn(q0, sp)
                        kap_nest = sub(cprime, sc(o_p, 1 << (sp - 1)))
                        nestL = [add(o_p, (0, 1))] + \
                                [sc(o_p, 1 << i) for i in range(sp - 1)] + \
                                [add(sc(o_p, 1 << (sp - 1)), kap_nest)] + \
                                list(window)
                        assert sp < level, \
                            'well-foundedness violated (sp=%d, level=%d)' % (sp, level)
                        STATS['calls'] += 1
                        j = v2f(H)
                        s2 = v2f(add(d, (0, 3)))
                        if j - s2 < STATS['margin_min']:
                            STATS['margin_min'] = j - s2
                        Dl = sub(d, (0, 3 * (t0 + ell) + 1))
                        if not (Dl == (0, 0) or
                                (Dl[0] == 0 and Dl[1] % 2 == 1 and Dl[1] < 0)):
                            STATS['delta_bad'] += 1
                        if r >= 2:
                            okwin = all(sub(window[i], sc(H, 1 << (i + 2))) == (0, 0)
                                        for i in range(r - 2)) and \
                                    sub(window[r - 2] if len(window) > r - 2 else Z0,
                                        add(sc(H, 1 << r), kap)) == (0, 0)
                            if not okwin:
                                STATS['winbad'] += 1
                        if ev is not None:
                            ev.append({'type': 'F', 't': ell, 'r': r, 'sp': sp,
                                       'd': d, 'j': j, 'margin': j - s2,
                                       'Delta': Dl[1] if Dl[0] == 0 else None,
                                       'q0': q0})
                        # ---- child: exact-input memoization (pure function) ----
                        key = (tuple(nestL), tuple(window))
                        if self.use_cache and key in self.cache:
                            ell_n, a_n, head_n = self.cache[key]
                            STATS['cache_uses'] += 1
                        else:
                            ell_n, a_n, head_n = self.F(
                                nestL, sp, window, sp, o_p, kap_nest,
                                t0 + ell + 1)
                            if self.use_cache:
                                self.cache[key] = (ell_n, a_n, head_n)
                        STATS['amax'] = max(STATS['amax'], a_n)
                        STATS['spmax'] = max(STATS['spmax'], sp)
                        if ev is not None and ev[-1]['type'] == 'F':
                            ev[-1]['a'] = a_n
                            ev[-1]['ell_child'] = ell_n
                        L = [head_n] + list(window[a_n:])
                        ell += 1 + ell_n
                        continue
            if ev is not None:
                ev.append({'type': 'g', 't': ell,
                           'r': enc[2] if enc is not None else None,
                           'canon': enc is not None})
            L = T_list(L)
            ell += 1

    def _finish(self, level, ell, a, head, ev):
        if ev is not None:
            TRACE[level] = ev
        return ell, a, head


def excursion(v, engine):
    w3 = (6, 3)
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + \
        [add(sc(w3, 1 << (v - 1)), (0, -1))]
    ell, a, head = engine.F(L, v, [], v, w3, (0, -1))
    assert a == 0, a
    assert head == add(sc(w3, 1 << v), (0, 3 * ell))
    return ell


def top(L):
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    S = L[3:]
    if A % 2 == 0:
        return [A + b + c + 3] + S
    m = b + (A - 3) // 2
    st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st
        m = (m - 3) // 2
    if m == 1:
        return 'HALT'
    return [m + 4] + st
