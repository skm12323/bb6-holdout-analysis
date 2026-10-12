# blind1_c3.py -- C3 PER-J CLASS VERIFIER.
# Part 1 (numeric): derive (dk(j), dp(j)) for j=1..30 from my own runs on
#   synthetic hosts: the aftermath of a class-j chain fire with host
#   parameters (U, rho, k), exactly as defined by the closed form:
#     x = 3*2^rho*U + 6k+4 = 3*2^rho*U + 2^j*q (q=(6k+4)/2^j odd),
#     b = 2^rho*U,  A = 2^rho*U + 2^j*q - 3,
#     u = x/2^j = 3*2^{rho-j}*U + q,
#     successor = (u+1; u,2u,...,2^{j-2}u, D, 2^{rho+2}U, 2^{rho+3}U, ...)
#     with D = c + (A+1)/2 = 2^{rho+1}U + 2^{rho-1}U + 2^{j-1}q - 1.
#   dp = (position of next host chain event) - rho,
#   dk = k(next host chain event) - k = ((x'-3*2^pos*U-4)/6) - k.
# Part 2 (symbolic): sound-by-construction affine class verifier.
#   Values are integer-affine forms cU*U + cq*q + c with U, q free odd >= 1.
#   All decisions (parity, exact v2, divisibility, positivity) are made by
#   term analysis that is uniform over ALL odd U, q:
#     parity(v)   = (cU+cq+c) mod 2                       (always decidable)
#     v2(v): the three terms have v2's a=v2(cU), b=v2(cq), d=v2(c) (inf if 0);
#            if the minimum is attained exactly once, v2(v)=min (uniform);
#            a tie is REFUSED (reported), never guessed.
#     v/2^t: exact coefficient shifts, required integer, else REFUSED.
#     v >= 3: nonneg coefficients + min value cU+cq+c >= 3, else REFUSED.
#   A completed leaf run is a proof for the whole class (U,q odd); since the
#   leaves are the full class, no case-splitting was needed iff zero
#   refusals occur.  (Ties would force a split; we refuse them instead.)
import sys
from blind1_lib import v2 as hv2
from blind1_lib import Stepper, Level

HOSTRUN = 'hostrun'
INF = 10 ** 9


def smallest_k_in_class(j):
    k = 1
    while True:
        if 1 + hv2(3 * k + 2) == j:
            return k
        k += 1


def synth_host(j, U, rho, k, tail=80):
    """Annotated aftermath of a class-j chain fire at host (U,rho,k)."""
    assert rho > j
    assert 1 + hv2(3 * k + 2) == j
    x = 3 * (U << rho) + 6 * k + 4
    u = x >> j
    D = (U << (rho + 1)) + (U << (rho - 1)) + 3 * k + 1
    q = [[u << a, ('run', 1, a)] for a in range(j - 1)]
    q.append([D, ('seam', 1)])
    q += [[U << (rho + 2 + s), (HOSTRUN, rho + 2 + s)] for s in range(tail)]
    st = Stepper(u + 1, q)
    st.levels.append(Level(U, 0))
    return st


def host_transition(j, U, rho, k, tail=80, max_steps=100000):
    """Run until the first fire whose consumed b is a host-run entry."""
    st = synth_host(j, U, rho, k, tail)
    steps = 0
    while True:
        ev = st.step()
        steps += 1
        if steps > max_steps:
            raise RuntimeError("runaway host run j=%d" % j)
        if ev['kind'] == 'halt':
            return ('HALT', ev['x'])
        if ev['kind'] == 'fire':
            b = ev['b']
            if b[1] is not None and b[1][0] == HOSTRUN:
                pos = b[1][1]
                U0 = st.levels[0].base
                kx, r = divmod(ev['x'] - 3 * (U0 << pos) - 4, 6)
                return (pos - rho, kx - k, r, st.n_fires, steps)


def derive_table(jlist=range(1, 31), verbose=False):
    table = {}
    nonuniform = []
    for j in jlist:
        k0 = smallest_k_in_class(j)
        res = set()
        detail = []
        for k in [k0, k0 + (1 << j), k0 + 3 * (1 << j)]:
            for U in (3, 9, 15, 5, 7, 3 * (2 ** 31 - 1)):
                for rho in (j + 2, j + 5, 45, 90):
                    r = host_transition(j, U, rho, k)
                    if isinstance(r, tuple) and r[0] == 'HALT':
                        detail.append(('HALT', j, U, rho, k, r[1]))
                        continue
                    dp, dk, r6, nf, steps = r
                    if r6 != 0:
                        detail.append(('BADREM', j, U, rho, k))
                    res.add((dk, dp))
                    if len(res) > 1:
                        nonuniform.append((j, U, rho, k, sorted(res)))
        if len(res) == 1:
            table[j] = res.pop()
        if detail and verbose:
            print("  details j=%d: %s" % (j, detail[:4]))
    return table, nonuniform


# ------------------------------------------------------------------
# symbolic verifier
# ------------------------------------------------------------------

class Refuse(Exception):
    pass


class Sym:
    __slots__ = ('cU', 'cq', 'c')

    def __init__(self, cU=0, cq=0, c=0):
        self.cU, self.cq, self.c = cU, cq, c

    def __add__(self, o):
        return Sym(self.cU + o.cU, self.cq + o.cq, self.c + o.c)

    def __sub__(self, o):
        return Sym(self.cU - o.cU, self.cq - o.cq, self.c - o.c)

    def __mul__(self, t):
        return Sym(self.cU * t, self.cq * t, self.c * t)

    def shift(self, a):
        if a < 0:
            raise Refuse("negative shift 2^%d" % a)
        return Sym(self.cU << a if self.cU else 0,
                   self.cq << a if self.cq else 0,
                   self.c << a if self.c else 0)

    def is_zero(self):
        return self.cU == 0 and self.cq == 0 and self.c == 0

    def __repr__(self):
        return "Sym(%d*U+%d*q+%d)" % (self.cU, self.cq, self.c)


def _v2c(v):
    return INF if v == 0 else hv2(v)


class SymRun:
    """Symbolic run of the class-j transition, U and q free odd >= 1."""

    def __init__(self, j, rho, max_steps=4000):
        if rho <= j:
            raise Refuse("need rho > j")
        self.j = j
        self.rho = rho
        self.max_steps = max_steps
        self.n_fires = 0
        self.steps = 0
        self.max_depth = 0
        self.divisions = 0
        self.min_v2U = INF      # min v2 of |cU| over forms with cU != 0
        U = Sym(1, 0, 0)
        Q = Sym(0, 1, 0)
        self.U, self.Q = U, Q
        # x = 3*2^rho*U + 2^j*q ;  u = x/2^j = 3*2^{rho-j} U + q
        u = U.shift(rho - j) * 3 + Q
        self.u0 = u
        # D = 2^{rho+1}U + 2^{rho-1}U + 2^{j-1}q - 1
        D = U.shift(rho + 1) + U.shift(rho - 1) + Q.shift(j - 1) \
            + Sym(0, 0, -1)
        self.A = u + Sym(0, 0, 1)
        self.queue = [[u.shift(a), None] for a in range(j - 1)]
        self.queue.append([D, None])
        self.host_next = rho + 2

    # ---------- decisions (uniform over all odd U, q >= 1) ----------
    def parity(self, s):
        return (s.cU + s.cq + s.c) & 1

    def v2_of(self, s):
        a, b, d = _v2c(s.cU), _v2c(s.cq), _v2c(s.c)
        m = min(a, b, d)
        n_min = (a == m) + (b == m) + (d == m)
        if n_min == 0:
            raise Refuse("all terms zero in %r" % (s,))
        if n_min == 1:
            self.max_depth = max(self.max_depth, m)
            return m
        raise Refuse("TIE in v2(%r): term v2s (%d,%d,%d)"
                     % (s, a, b, d))

    def div2(self, s, t):
        """s / 2^t by exact coefficient shift (sound: required integer)."""
        mask = (1 << t) - 1
        if (s.cU & mask) or (s.cq & mask) or (s.c & mask):
            raise Refuse("coefficients not divisible by 2^%d in %r"
                         % (t, s))
        self.divisions += t
        return Sym(s.cU >> t if s.cU else 0, s.cq >> t if s.cq else 0,
                   s.c >> t if s.c else 0)

    def positivity(self, s, need=3):
        if s.cU < 0 or s.cq < 0:
            raise Refuse("negative coefficient in %r" % (s,))
        if s.cU == 0 and s.cq == 0:
            if s.c < need:
                raise Refuse("constant %d < %d" % (s.c, need))
            return
        if s.cU + s.cq + s.c < need:
            raise Refuse("min value %d < %d in %r" % (s.cU + s.cq + s.c,
                                                      need, s))

    # ---------- the map ----------
    def track(self, *syms):
        for s in syms:
            if s.cU:
                a = hv2(abs(s.cU))
                if a < self.min_v2U:
                    self.min_v2U = a

    def pop2(self):
        b = self.queue.pop(0)
        c = self.queue.pop(0) if self.queue else [Sym(0, 0, 0), None]
        return b, c

    def ensure_host(self):
        while len(self.queue) < 2:
            self.queue.append([self.U.shift(self.host_next),
                               ('host', self.host_next)])
            self.host_next += 1

    def step(self):
        self.steps += 1
        if self.steps > self.max_steps:
            raise Refuse("too many steps")
        self.ensure_host()
        self.track(self.A)
        if self.parity(self.A) == 0:
            b, c = self.pop2()
            self.track(b[0], c[0])
            self.A = self.A + b[0] + c[0] + Sym(0, 0, 3)
            return {'kind': 'even'}
        b, c = self.pop2()
        self.track(b[0], c[0])
        x = self.A + (b[0] * 2) + Sym(0, 0, 3)
        if b[1] is not None and b[1][0] == 'host':
            return {'kind': 'hostchain', 'pos': b[1][1], 'x': x}
        j = self.v2_of(x)
        u = self.div2(x, j)
        self.track(x, u)
        # u must be an odd >= 3 (odd is automatic: v2(x)=j); HALT impossible
        self.positivity(u, 3)
        pre = [[u.shift(t), None] for t in range(j - 1)]
        for p_ in pre:
            self.track(p_[0])
        D = c[0] + self.div2(self.A + Sym(0, 0, 1), 1)
        self.track(D)
        self.queue = pre + [[D, None]] + self.queue
        self.A = u + Sym(0, 0, 1)
        self.n_fires += 1
        return {'kind': 'fire', 'x': x, 'j': j}

    def run(self):
        while True:
            ev = self.step()
            if ev['kind'] == 'hostchain':
                pos = ev['pos']
                x = ev['x']
                # claimed identity: x = 3*2^pos*U + 6(k+dk)+4
                #                 = 3*2^pos*U + 2^j*q + 6*dk   (2^j q = 6k+4)
                target = (self.U.shift(pos) * 3) + self.Q.shift(self.j)
                diff = x - target
                if diff.cU != 0 or diff.cq != 0:
                    return ('FORM-FAIL', pos, diff)
                if diff.c % 6:
                    return ('DK-NONINT', pos, diff.c)
                dk = diff.c // 6
                return ('OK', pos - self.rho, dk, self.n_fires, self.steps,
                        self.max_depth, self.divisions, self.min_v2U)
            if ev['kind'] == 'HALT!':
                return ('HALT',)


def verify_class_full(j, table=None, generic=5000, extra_margin=64):
    """Verify class j for rho = j+1 .. j+R (R = 2*steps(numeric)+margin)
    and for one generic large rho; all must give the same (dp, dk).
    Returns (results, refusals, n_rhos, max_depth, max_divisions)."""
    probe_rho = j + 2
    r = host_transition(j, 3, probe_rho, smallest_k_in_class(j))
    steps = r[4] if not (isinstance(r, tuple) and r[0] == 'HALT') else 0
    R = 2 * steps + extra_margin
    rhos = list(range(j + 1, j + 1 + R)) + [j + generic]
    results = {}
    refusals = []
    max_depth = 0
    max_div = 0
    min_margin = INF
    for rho in rhos:
        try:
            res = SymRun(j, rho).run()
        except Refuse as rf:
            refusals.append((rho, str(rf)))
            continue
        if res[0] != 'OK':
            refusals.append((rho, res))
            continue
        dp, dk = res[1], res[2]
        max_depth = max(max_depth, res[5])
        max_div = max(max_div, res[6])
        min_margin = min(min_margin, res[7] - res[5])
        results.setdefault((dp, dk), []).append(rho)
    return results, refusals, len(rhos), max_depth, max_div, min_margin


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'table'
    if mode == 'table':
        tbl, nonun = derive_table()
        print("empirical (dk, dp) table, j=1..30 (mine):")
        for j in range(1, 31):
            if j in tbl:
                print("  j=%2d  dk=%2d dp=%2d" % (j, tbl[j][0], tbl[j][1]))
            else:
                print("  j=%2d  NON-UNIFORM/FAILED %s" % (j, nonun[:3]))
        print("as dict:", tbl)
        claim_dk = {1:1,2:1,3:2,4:2,5:3,6:3,7:3,8:4,9:4,10:5,11:5,12:6,13:6,
                    14:8,15:7,16:7,17:8,18:8,19:8,20:9}
        claim_dp = {1:3,2:2,3:5,4:4,5:4,6:5,7:4,8:6,9:2,10:5,11:4,12:6,13:4,
                    14:5,15:5,16:4,17:6,18:3,19:2,20:5}
        bad = [(j, tbl.get(j), (claim_dk[j], claim_dp[j]))
               for j in range(1, 21)
               if j in tbl and tbl[j] != (claim_dk[j], claim_dp[j])]
        print("mismatches vs claimed table (j=1..20):", bad if bad else "none")
    elif mode == 'symbolic':
        lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        hi = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        tbl, _ = derive_table(range(lo, hi + 1))
        allok = True
        gdepth = 0
        gdiv = 0
        gmargin = INF
        for j in range(lo, hi + 1):
            results, refusals, nrho, mdep, mdiv, mmarg = \
                verify_class_full(j, tbl)
            gdepth = max(gdepth, mdep)
            gdiv = max(gdiv, mdiv)
            gmargin = min(gmargin, mmarg)
            if len(results) == 1 and not refusals:
                (dp, dk), _ = next(iter(results.items()))
                match = (dk, dp) == tbl.get(j)
                allok = allok and match
                print("j=%2d SYMBOLIC-PROVED dk=%d dp=%d  (%d rhos, "
                      "0 refusals) matches-empirical=%s"
                      % (j, dk, dp, nrho, match))
            else:
                allok = False
                print("j=%2d SYMBOLIC ISSUE: results=%s refusals=%s"
                      % (j, {k: len(v) for k, v in results.items()},
                         refusals[:3]))
        print("ALL SYMBOLIC OK:", allok)
        print("global max v2-decision depth=%d, max total divisions=%d, "
              "min margin (min_v2U - max_depth) = %d"
              % (gdepth, gdiv, gmargin))
