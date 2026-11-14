"""fb.py -- symbolic post-gate form engine for FREE-B (ZCode agent, 2026-11-10).

Exact walk of the scalar pair map (PROOF_EXT section 2 rules, same rules as cyc.py) on the
GENERIC POST-GATE state of a true NT gate G at odd-a chain j (k = k_j) with output m:

    Theta = c_Theta + 2^(j-1) X,   c_Theta = 2^(j-2) + 3(k+1),        (Lemma PG, accepted)
    x     = 2^m (1 + 2V),          X, V free 2-adic variables.

Every exact walk through such a gate lands in this cylinder (Lemma FB-0): (X, V) range over
all of Z_2^2, so identities proved for all (X, V) hold for every real walk through G.

x is carried as an affine form with SMALL dyadic-rational coefficients:

    x = u + beta*T + a*X + gamma*T*V,      T = 2^m kept SYMBOLIC (m may be ~10^12),

which is exact: the initial 2^m and 2^(m+1)V live in beta/gamma, all calendar data in u
(moderate), and X enters only through Theta (coefficient 2^j at the first a-step).
Theta is (theta, xth): Theta = theta + xth*X with xth = 2^(j-1) initially.

v2 of the constant part u + beta*T is computed exactly with small arithmetic.  Equality of
T-forms p + q*T vs p' + q'*T: coefficient equality when m > SAFE_M (all integers that occur
are below 2^380 in absolute value, so |p-p'| = |q-q'|*2^m is impossible unless both sides
vanish); exact materialization otherwise.

Step rules (n = q-1, canonical crossing row):
  a-step (tau = 2 k_q):  x' = 2Theta + 6k_q - x/2,  Theta' = Theta + 3 + 6k_q,  loss 1
  b/c-step:              x' = R x + lam',           Theta' = Theta + 3 + 3tau,  loss 1+eps

Determinacy (Lemma FB-2): the next chain is fixed for ALL (X, V) iff
    v2(u + beta*T) < min( v2(a) [a != 0], m + v2(gamma) ),
and then equals v2(u + beta*T); otherwise the step splits on X or V.

Standard library only.  Run from D:/math_cc with PYTHONUTF8=1.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_claude_cycle'))
from cyc import Cal, v2, INF  # noqa: E402

SAFE_M = 420  # T-form equality = coefficient equality above this m (see module docstring)


class Rows:
    """cal.row with an unbounded cache (cyc.Cal only caches n < 200000)."""

    def __init__(self, cal=None):
        self.cal = cal if cal is not None else Cal()
        self.cache = {}

    def __call__(self, n):
        r = self.cache.get(n)
        if r is None:
            r = self.cal.row(n)
            self.cache[n] = r
        return r


def tf_v2(u, beta, m):
    """exact v2 of u + beta*2^m (dyadic Fractions)."""
    if beta == 0:
        return v2(u)
    if u == 0:
        return m + v2(beta)
    tu, tb = v2(u), m + v2(beta)
    if tu != tb:
        return min(tu, tb)
    e = u / F(2) ** tu + beta * F(2) ** (m - tu)   # small dyadic rational, odd parts combine
    return tu + v2(e)


def tf_eq(p, q, p2, q2, m):
    """exact equality of p + q*T and p2 + q2*T."""
    if p == p2 and q == q2:
        return True
    if m <= SAFE_M:
        return p + q * F(2) ** m == p2 + q2 * F(2) ** m
    # m > SAFE_M: |p - p2| and |q - q2| are calendar-sized (< 2^300 in all uses), so
    # |p - p2| = |q - q2| * 2^m is impossible unless both vanish.
    d0, d1 = abs(p - p2), abs(q - q2)
    assert max(d0.numerator.bit_length(), d0.denominator.bit_length(),
               d1.numerator.bit_length(), d1.denominator.bit_length()) < 400, 'tf_eq range'
    return False


class FSt:
    """form state: chain q, Theta = theta + xth*X, x = u + beta*T + a*X + gamma*T*V."""

    __slots__ = ('j', 'm', 'q', 'theta', 'xth', 'u', 'beta', 'a', 'gamma', 'ell', 'Lbc')

    def __init__(self, j, k, m):
        self.j, self.m = j, m
        self.q = m
        self.theta = F(2 ** (j - 2) + 3 * (k + 1))
        self.xth = F(2 ** (j - 1))
        if m <= SAFE_M:
            self.u, self.beta = F(2) ** m, F(0)
        else:
            self.u, self.beta = F(0), F(1)
        self.a, self.gamma = F(0), F(2)      # V-coefficient 2^(m+1) = 2*T
        self.ell = 0
        self.Lbc = 0       # loss of the maximal b/c run right after G's output (0 if type a)

    def var_min(self):
        r = INF
        if self.a != 0:
            r = v2(self.a)
        if self.gamma != 0:
            r = min(r, self.m + v2(self.gamma))
        return r

    def const_v2(self):
        return tf_v2(self.u, self.beta, self.m)

    def sub_e(self, var, e):
        """substitute var -> e + 2*var' in place (e integer 0/1)."""
        if var == 'X':
            self.theta = self.theta + self.xth * e
            self.u = self.u + self.a * e
            self.xth = 2 * self.xth
            self.a = 2 * self.a
        else:
            self.beta = self.beta + self.gamma * e
            self.gamma = 2 * self.gamma


def step_form(rows, st):
    """one step from chain st.q; returns None if the walk ends (X even or q <= 4).
    Mutates st.  Result dict: kind, k, tau, loss, and either jn (determined next chain)
    or split in {'X','V'} (the step is free)."""
    q = st.q
    if q <= 4:
        return None
    r = rows(q - 1)
    if not r['odd']:
        return None
    tau = r['tau']
    if r['kind'] == 'a':
        kk = tau // 2
        u2 = 2 * st.theta + 6 * kk - st.u / 2
        b2 = -st.beta / 2
        a2 = 2 * st.xth - st.a / 2
        g2 = -st.gamma / 2
        th2 = st.theta + 3 + 6 * kk
        loss = 1
    else:
        R, lam = r['R'], r['lam']
        u2 = R * st.u + lam
        b2 = R * st.beta
        a2 = R * st.a
        g2 = R * st.gamma
        th2 = st.theta + 3 + 3 * tau
        loss = 1 + r['eps']
        if st.a == 0:
            st.Lbc = st.Lbc + loss      # initial b/c run extends (X not yet entered)
    st.u, st.beta, st.a, st.gamma, st.theta = u2, b2, a2, g2, th2
    st.ell += loss
    tc = tf_v2(st.u, st.beta, st.m)
    tv = st.var_min()
    d = dict(kind=r['kind'], k=(tau // 2 if r['kind'] == 'a' else None), tau=tau, loss=loss)
    if tc < tv:
        st.q = tc
        d['jn'] = tc
    else:
        d['jn'] = None
        d['split'] = 'X' if (st.a != 0 and v2(st.a) <= st.m + v2(st.gamma)) else 'V'
    return d


def det_walk(rows, j, k, m, max_steps=None, stop_at_gate=True):
    """deterministic walk from the post-gate state of gate (j, k, m).
    Returns (trace, status, st): trace = list of (q_in, stepdict, tag); status in
    END / SPLIT / GATE / LIMIT.  A step is a true NT gate iff kind a and jn >= q_in.
    max_steps = None means m+3, which is a priori complete: v2(B) = m+1-ell, so a
    determined walk with ell >= m-3 can only read chains <= 3 and ENDs; hence LIMIT is
    impossible for determined walks.  (branch.py's ZERO leaf = an identically vanishing
    output form; here that case falls under SPLIT — both mean 'not determined'; it is
    unreachable on post-gate starts because the V-coefficient never vanishes.)"""
    if max_steps is None:
        max_steps = m + 3
    st = FSt(j, k, m)
    trace = []
    for _ in range(max_steps):
        q_in = st.q
        s = step_form(rows, st)
        if s is None:
            return trace, 'END', st
        if s['jn'] is None:
            trace.append((q_in, s, 'free'))
            return trace, 'SPLIT', st
        gate = s['kind'] == 'a' and s['jn'] >= q_in
        trace.append((q_in, s, 'gate' if gate else ''))
        if gate and stop_at_gate:
            return trace, 'GATE', st
    return trace, 'LIMIT', st


def fb4(rows, j, k, m):
    """explicit two-step data for X(m-1) odd with DETERMINED first landing c1 and an a-step
    at c1.  Returns None if the first step ends the walk or splits.  If X(c1-1) is not an
    odd a-crossing, returns dict(no_astep=True).  Otherwise dict with:
      kind, c1, kc = k_{c1}, ell, Lbc, mprime = v2(C_final) or None if the a-step at c1
      splits (det2 = False), Cform = (u, beta) with C_final = u + beta*T (always exact),
      vA = v2(A) or INF, vB = v2(B), gate (= True iff a determined true NT gate at c1),
      S (type a) / U (types b, c) = the explicit FB-4 integer sums."""
    r = rows(m - 1)
    if not r['odd']:
        return None
    st = FSt(j, k, m)
    s1 = step_form(rows, st)
    if s1 is None or s1['jn'] is None:
        return None
    c1 = s1['jn']
    r1 = rows(c1 - 1)
    if not r1['odd'] or r1['kind'] != 'a':
        return dict(kind=r['kind'], c1=c1, no_astep=True)
    kc = r1['tau'] // 2
    q_in = st.q
    s2 = step_form(rows, st)
    if s2 is None:
        return None
    det2 = s2['jn'] is not None
    d = dict(kind=r['kind'], c1=c1, kc=kc, ell=st.ell, Lbc=st.Lbc,
             mprime=s2['jn'], det2=det2, Cform=(st.u, st.beta),
             vA=(v2(st.a) if st.a != 0 else INF), vB=st.m + v2(st.gamma), q_in=q_in,
             gate=(det2 and s2['jn'] >= q_in))
    if r['kind'] == 'a':
        d['S'] = k + 3 + 3 * (r['tau'] // 2) + 2 * kc
    elif r['kind'] == 'b':
        d['U'] = 12 * k + 12 * kc + 9 * r['tau'] + 20
    else:
        d['U'] = 12 * (k + r['tau'] + kc + 2) - r['lam']
    return d


def fb4_Cform_ab(k, kind, tau_m, kc, j, m, Km=None):
    """closed-form C_final of FB-4 as (u, beta) with T = 2^m symbolic.
      (a) C_final = 3*S_a + 2^(j-2) + 2^(m-2)          -> (3 S_a + 2^(j-2), 1/4)
      (b) C_final = 2^(j-1) - 3*2^(m-3) + U_b/2        -> (2^(j-1) + U_b/2, -3/8)
    (type a needs Km = k_m; type b needs tau_m = tau(m-1).)"""
    if kind == 'a':
        S = k + 3 + 3 * Km + 2 * kc
        return (F(3 * S + 2 ** (j - 2)), F(1, 4))
    U = 12 * k + 12 * kc + 9 * tau_m + 20
    return (F(2 ** (j - 1)) + F(U, 2), F(-3, 8))


def fb4_Cform_c(k, tau_m, kc, j, m, Rc, lam_c):
    u = F(2 ** (j - 1)) + 6 * (k + tau_m + kc + 2) - F(lam_c, 2)
    return (u, F(-1, 2) * Rc)


def Pc(n):
    """P(n) = 2 ceil(log2(6 n^2 + 5))^2 + 1345 (accepted CLOCK, work_global_clock)."""
    x = 6 * n * n + 5
    lg = max(0, (x - 1).bit_length())
    return 2 * lg * lg + 1345
