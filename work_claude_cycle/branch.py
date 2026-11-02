"""branch.py -- exact 2-adic branching walk on canonical calendar data (Claude, 2026-11-02).

A start is a pair of affine forms (Theta, x) in independent Haar-uniform 2-adic variables.  The walk is run on
forms; whenever the output valuation of a step is not fixed by the constant part (FREE), the variable with the
smallest coefficient valuation is split into its two residue classes (measure halves).  Every leaf is either
  END (X(j-1) even, all steps determined), CUT (measure below threshold / depth limit), ZERO (x'=0 identically).
Leaves carry exact data: the event word, gate list, records, and the cylinder (fixed low bits of each variable).
All statements about measure are exact for the 2-adic (Haar) model; they say nothing about canonical starts.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cyc import Cal, v2, INF, fadd, fmul, fval, fsubst  # noqa


def step_forms(cal, j, Th, x):
    r = cal.row(j - 1)
    if j <= 4 or not r['odd']:
        return None
    tau = r['tau']
    if r['kind'] == 'a':
        k = tau // 2
        xn = fadd(fmul(Th, 2), fadd({1: F(6 * k)}, fmul(x, F(-1, 2))))
        Thn = fadd(Th, {1: F(3 + 6 * k)})
        loss = 1
    else:
        k = None
        xn = fadd(fmul(x, r['R']), {1: F(r['lam'])})
        Thn = fadd(Th, {1: F(3 + 3 * tau)})
        loss = 1 + r['eps']
    return r['kind'], k, xn, Thn, loss


def fsub_expr(a, p, expr):
    """substitute variable p by the form expr."""
    if p not in a:
        return dict(a)
    c = a[p]
    r = {kk: vv for kk, vv in a.items() if kk != p}
    return fadd(r, expr, c)


def explore(cal, j0, Th0, x0, G0=0, min_bits=24, max_steps=400, max_leaves=10 ** 6, stop_at_gate=False,
            max_gates=None):
    """DFS over the branching tree.  Returns list of leaves; each leaf is a dict with
    status, bits (= -log2 measure), steps (list of (j, kind, k, jn, G)), omap (original variable -> form in the
    leaf's variables; evaluating it at any 2-adic point of the leaf's variables gives a start in the leaf cylinder).
    At a FREE step the free part F = sum c_v v of the output is first made a single variable by the unimodular
    (Haar-measure-preserving) substitution p -> (W - sum_{v!=p} u_v v)/u_p, u_v = c_v/2^s, then W is split."""
    leaves = []
    vars0 = sorted({kk for f in (Th0, x0) for kk in f if kk != 1}, key=str)
    omap0 = {v: {v: F(1)} for v in vars0}
    stack = [(j0, Th0, x0, G0, 0, [], omap0)]
    while stack:
        j, Th, x, G, bits, steps, omap = stack.pop()
        while True:
            if len(steps) >= max_steps:
                leaves.append(dict(status='CUT_STEPS', bits=bits, steps=steps, omap=omap, Th=Th, x=x, j=j)); break
            s = step_forms(cal, j, Th, x)
            if s is None:
                leaves.append(dict(status='END', bits=bits, steps=steps, omap=omap, Th=Th, x=x, j=j)); break
            kind, k, xn, Thn, loss = s
            vc, vs, var = fval(xn)
            if vc < vs:
                jn = vc
                steps = steps + [(j, kind, k, jn, G + loss)]
                j, Th, x, G = jn, Thn, xn, G + loss
                if kind == 'a' and jn >= steps[-1][0]:
                    if stop_at_gate or (max_gates is not None and
                                        sum(1 for t in steps if t[1] == 'a' and t[3] >= t[0]) >= max_gates):
                        leaves.append(dict(status='GATE', bits=bits, steps=steps, omap=omap, Th=Th, x=x, j=j)); break
                continue
            if var is None:            # identically zero
                leaves.append(dict(status='ZERO', bits=bits, steps=steps, omap=omap, Th=Th, x=x, j=j)); break
            if bits >= min_bits:
                leaves.append(dict(status='CUT_BITS', bits=bits, steps=steps, omap=omap, Th=Th, x=x, j=j,
                                   free_at=j, free_from=vs)); break
            # unimodular change of variables making the free part of xn equal to 2^vs * var
            up = xn[var] / F(2) ** vs
            expr = {var: 1 / up}
            for kk, vv in xn.items():
                if kk != 1 and kk != var:
                    expr[kk] = -(vv / F(2) ** vs) / up
            Th1 = fsub_expr(Th, var, expr); x1 = fsub_expr(x, var, expr)
            om1 = {o: fsub_expr(f, var, expr) for o, f in omap.items()}
            for e in (1, 0):
                sub = {1: F(e), var: F(2)}
                stack.append((j, fsub_expr(Th1, var, sub), fsub_expr(x1, var, sub), G, bits + 1, steps,
                              {o: fsub_expr(f, var, sub) for o, f in om1.items()}))
            break
        if len(leaves) >= max_leaves:
            break
    return leaves


def lift(leaf, P):
    """integer values of the original variables mod 2^P at the leaf's base point (current vars = 0)."""
    M = 1 << P
    out = {}
    for o, f in leaf['omap'].items():
        c = F(f.get(1, 0))
        assert c.denominator % 2 == 1
        out[o] = (c.numerator * pow(c.denominator, -1, M)) % M
    return out


def evalf(f, vals):
    return sum(vv * (1 if kk == 1 else vals[kk]) for kk, vv in f.items())


def gate_list(steps):
    """true NT gates: a-steps with jn >= j. returns list of (index, j, k, m, G_after)."""
    return [(i, s[0], s[2], s[3], s[4]) for i, s in enumerate(steps) if s[1] == 'a' and s[3] >= s[0]]


