"""agentB_abs.py — abstract simulator for the bulk dynamics (v4).

Values are linear forms  V = alpha*P + gamma*k + delta  (exact rational coeffs),
P = 2^p symbolic (p huge), k = kappa + 2^m*s with s a free symbol >= 0.

When a 2-adic decision (parity of A, or v2 of a chain x) is not constant on the
current class (kappa mod 2^m), we raise NeedsSplit; the driver refines the
class into the two halves mod 2^{m+1} and verifies each.  Sound: verification
over the full class covers every actual k in it.
"""
from fractions import Fraction as Fr
from agentB_lib import v2i

INF = 1 << 50

def fv2(x):
    if x == 0:
        return INF
    return v2i(abs(x.numerator)) - v2i(abs(x.denominator))

class Ambiguous(Exception):
    """genuine failure (not splittable)"""
    pass

class NeedsSplit(Exception):
    pass

class Ctx:
    def __init__(self, p=200, kappa=0, m=4):
        self.p = p
        self.kappa = Fr(kappa)
        self.m = m

class Val:
    __slots__ = ('a', 'c', 'd')
    def __init__(self, a=Fr(0), c=Fr(0), d=Fr(0)):
        self.a, self.c, self.d = Fr(a), Fr(c), Fr(d)
    def __add__(self, o):
        o = as_val(o); return Val(self.a + o.a, self.c + o.c, self.d + o.d)
    def __sub__(self, o):
        o = as_val(o); return Val(self.a - o.a, self.c - o.c, self.d - o.d)
    def __mul__(self, f):
        f = Fr(f); return Val(self.a * f, self.c * f, self.d * f)
    def __rmul__(self, f):
        return self * f
    def __eq__(self, o):
        o = as_val(o); return (self.a == o.a and self.c == o.c and self.d == o.d)
    def __repr__(self):
        return '(%s P + %s k + %s)' % (self.a, self.c, self.d)
    def iszero(self):
        return self.a == 0 and self.c == 0 and self.d == 0

ZERO = Val(0, 0, 0)

def as_val(x):
    if isinstance(x, Val):
        return x
    return Val(0, 0, Fr(x))

def _kparts(V, ctx):
    """head = gamma*2^m (s-coefficient), base = gamma*kappa+delta."""
    head = V.c * (1 << ctx.m)
    base = V.c * ctx.kappa + V.d
    return head, base

def parity(V, ctx):
    head, base = _kparts(V, ctx)
    if head != 0:
        if head.denominator != 1:
            raise NeedsSplit('non-integral s-coeff %r' % (V,))
        if head % 2 == 1:
            raise NeedsSplit('parity varies with s: %r' % (V,))
    if base.denominator != 1:
        raise NeedsSplit('non-integral base %r' % (V,))
    par = base % 2
    if V.a != 0:
        pa = V.a * (1 << ctx.p)
        if pa.denominator != 1:
            raise NeedsSplit('non-integral P-part %r' % (V,))
        if fv2(pa) == 0 and par == 0:
            # odd P-part: would flip parity; with p huge only if alpha ~ 2^{-p}
            raise NeedsSplit('P-part parity %r' % (V,))
        # P-part even (v2>=1): no change ... but if v2==0 and par==1 stays odd
    return int(par)

def v2_val(V, ctx):
    if V.iszero():
        raise Ambiguous('v2 of zero')
    head, base = _kparts(V, ctx)
    if V.c == 0:
        if base.denominator != 1:
            raise NeedsSplit('non-integral %r' % (V,))
        vsmall = fv2(base)
    else:
        if head.denominator != 1 or base.denominator != 1:
            raise NeedsSplit('non-integral k-part %r' % (V,))
        vh, vb = fv2(head), fv2(base)
        if vb == 0 and base == 0:
            raise NeedsSplit('k-part zero at s=0 %r' % (V,))
        if vh > vb:
            vsmall = vb
        elif vb > vh:
            # value = 2^vh*(odd*s*.. ) : varies unless ...
            raise NeedsSplit('v2 varies (head<base) %r' % (V,))
        else:
            raise NeedsSplit('v2 varies (tie) %r' % (V,))
    if vsmall < 0:
        raise NeedsSplit('non-integral small part %r' % (V,))
    if V.a != 0:
        pa = V.a * (1 << ctx.p)
        if pa.denominator != 1:
            raise NeedsSplit('non-integral P-part %r' % (V,))
        vP = ctx.p + fv2(V.a)
        if vsmall == vP:
            raise Ambiguous('tie small/P %r' % (V,))
        return min(vsmall, vP)
    return vsmall

def min_value(V, ctx):
    if V.a > 0:
        return 1 << 40
    if V.a < 0:
        raise Ambiguous('negative P part %r' % (V,))
    if V.c < 0:
        raise Ambiguous('negative k part %r' % (V,))
    lo = V.d + (V.c * ctx.kappa if V.c != 0 else 0)
    return int(lo) if lo.denominator == 1 else lo

class Sim:
    def __init__(self, ctx):
        self.ctx = ctx
    def step(self, A, q, trace=None):
        b = q[0] if q else ZERO
        c = q[1] if len(q) > 1 else ZERO
        rest = q[2:]
        if parity(A, self.ctx) == 0:
            A2 = A + b + c + 3
            if trace is not None:
                trace.append(('E',))
            return A2, rest, ('E',)
        x = A + b * 2 + 3
        j = v2_val(x, self.ctx)
        u = x * Fr(1, 1 << j)
        if min_value(u, self.ctx) < 3:
            raise Ambiguous('u < 3 possible: %r' % (u,))
        D = c + (A + 1) * Fr(1, 2)
        newq = [u * (1 << kk) for kk in range(j - 1)] + [D] + rest
        A2 = u + 1
        if trace is not None:
            trace.append(('C', j))
        return A2, newq, ('C', j)
