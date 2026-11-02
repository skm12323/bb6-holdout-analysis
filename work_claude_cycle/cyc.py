"""cyc.py -- core library for work_claude_cycle (Claude, 2026-11-02).

Exact scalar pair-map walk (PROOF_EXT section 2 / Lemma BR) on canonical Calendar(512) data:
  a-step at chain j (n=j-1, tau=2k):  x' = 2*Theta + 6k - x/2,   Theta' = Theta + 3 + 6k,  G += 1
  b/c-step:                           x' = R*x + lam,            Theta' = Theta + 3 + 3tau, G += 1+eps
  j' = v2(x'); the walk stops when X(j-1) is even (or j<=4, where X(n) is even).
S(J) is the walk started at (j, Theta, x) = (J, 1, 0) (beta-walk: Theta=3d+1, x=beta_x); tie iff j' >= J-G'.
Event classification of an a-step at chain j (Lemma NT): with v = v2(Theta+3k):
  v <= j-3 : descent to 1+v;   v == j-2 : true NT gate (j' >= j);   v >= j-1 : catapult (j' = j-1).
Standard library only.  Run with PYTHONUTF8=1.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_global_calendar'))
from calendar_oracle import Calendar  # noqa: E402

INF = 10 ** 9


def v2(q):
    q = F(q)
    if q == 0:
        return INF
    n, d = q.numerator, q.denominator
    return ((n & -n).bit_length() - 1) - ((d & -d).bit_length() - 1)


class Cal:
    """cached canonical crossing rows: kind, tau, eps, odd, R (=c'_W/2^j, Fraction), lam (=lambda'_W)."""

    def __init__(self, B=512):
        self.C = Calendar(B)
        self.rows = {}

    def row(self, n):
        r = self.rows.get(n)
        if r is not None:
            return r
        c = self.C.crossing(n)
        kind = c['kind']
        if c['odd'] and kind != 'a':
            R = (c['head_ratio'] + 2 * c['tail_ratio']) / 2
            lam = c['head_lambda'] + 2 * c['tail_lambda'] + 3
        else:
            R = lam = None
        r = dict(kind=kind, tau=c['time'], eps=c['epsilon'], odd=c['odd'], R=R, lam=lam,
                 omega=c['omega'], lY=(c['tail_lambda'] if kind == 'c' else 0))
        if n < 200000:
            self.rows[n] = r
        return r

    def k(self, j):
        """half-time k_j if X(j-1) is odd type a, else None."""
        r = self.row(j - 1)
        return r['tau'] // 2 if (r['odd'] and r['kind'] == 'a') else None


def step(cal, j, Th, x):
    """one exact step from chain j. Returns None if X(j-1) even, else dict."""
    if j <= 4:
        return None
    r = cal.row(j - 1)
    if not r['odd']:
        return None
    tau = r['tau']
    if r['kind'] == 'a':
        k = tau // 2
        v = v2(Th + 3 * k)
        xn = 2 * Th + 6 * k - F(x) / 2
        Thn = Th + 3 + 6 * k
        loss = 1
        ev = 'desc' if v <= j - 3 else ('gate' if v == j - 2 else 'cat')
    else:
        k = None
        xn = r['R'] * x + r['lam']
        Thn = Th + 3 + 3 * tau
        loss = 1 + r['eps']
        ev = r['kind']
    jn = v2(xn)
    return dict(j=j, kind=r['kind'], k=k, tau=tau, jn=jn, x=xn, Th=Thn, loss=loss, ev=ev)


def walk(cal, j, Th, x, G=0, J=None, limit=100000):
    """exact walk; returns (steps, status). status in END, TIE (if J given), NONPOS, LIMIT."""
    out = []
    for _ in range(limit):
        s = step(cal, j, Th, x)
        if s is None:
            return out, 'END'
        G += s['loss']
        s['G'] = G
        out.append(s)
        if s['x'] == 0:
            return out, 'ZERO'
        if J is not None and s['jn'] >= J - G:
            return out, 'TIE'
        j, Th, x = s['jn'], s['Th'], s['x']
    return out, 'LIMIT'


def SJ(cal, J, limit=100000):
    return walk(cal, J, 1, 0, 0, J, limit)


# ---------------------------------------------------------------- symbolic 2-adic forms
# A form is a dict var->Fraction coefficient with key 1 for the constant.  Free variables range over Z_2
# (independent, uniform Haar measure).  Odd unknowns are written 1+2V explicitly by the caller.

def fadd(a, b, cb=1):
    r = dict(a)
    for kk, vv in b.items():
        r[kk] = r.get(kk, 0) + cb * vv
        if r[kk] == 0 and kk != 1:
            del r[kk]
    return r


def fmul(a, c):
    return {kk: c * vv for kk, vv in a.items() if c * vv != 0 or kk == 1}


def fval(a):
    """(v_const, v_free_min, argmin var) for a form."""
    vc = v2(a.get(1, 0))
    vs, var = INF, None
    for kk, vv in a.items():
        if kk == 1:
            continue
        w = v2(vv)
        if w < vs:
            vs, var = w, kk
    return vc, vs, var


def fsubst(a, var, e, newvar):
    """substitute var = e + 2*newvar."""
    if var not in a:
        return dict(a)
    c = a[var]
    r = {kk: vv for kk, vv in a.items() if kk != var}
    r[1] = r.get(1, 0) + e * c
    r[newvar] = r.get(newvar, 0) + 2 * c
    return r
