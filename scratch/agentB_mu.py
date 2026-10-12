"""agentB_mu.py — the mu-walker: universal symbolic engine for cascade prefixes.

Locality frame: at a spike chain with parameter J, pointer p, excess index k
(6k+4 = 2^J * odd), the pushed run entries are 2^a*u with
    u = 9*2^{p-J}*w + mu,   mu = (6k+4)/2^J  (free ODD symbol),
and the process that consumes the run (positions 0..J-2, before the level's
defect D is touched) is a symbolic process in the free odd symbol mu alone:
values are  cM*M + cmu*mu + e  with M = 9*2^{p-J}*w (v2(M) = p-J >= MARGIN),
cM, cmu, e exact rationals (cmu, e integers).  Decisions:
  parity: always constant (parity(cmu*mu+e) = cmu odd ? 1-(e&1) : e&1).
  v2: v2(cmu*mu+e) is constant iff v2(cmu) != v2(e) (or one side 0);
      ties with the M-part are impossible while v2(small) < MARGIN + v2(cM).
Safety: u >= 3 whenever cM > 0 (M dwarfs the mu/const parts), checked.

This walker is J-independent (queue-determinism lemma: cascades of J and J'
agree before position min(J,J')-1), so walking to position N verifies the
common prefix of ALL cascades with J >= N+1.
"""
from fractions import Fraction as Fr
from agentB_lib import v2i

MARGIN = 900

class Amb(Exception):
    pass

def fv2(x):
    if x == 0:
        return None
    return v2i(abs(x.numerator)) - v2i(abs(x.denominator))

class Val:
    __slots__ = ('cM', 'cmu', 'e')
    def __init__(self, cM=Fr(0), cmu=Fr(0), e=Fr(0)):
        self.cM, self.cmu, self.e = Fr(cM), Fr(cmu), Fr(e)
    def __add__(self, o):
        return Val(self.cM + o.cM, self.cmu + o.cmu, self.e + o.e)
    def __sub__(self, o):
        return Val(self.cM - o.cM, self.cmu - o.cmu, self.e - o.e)
    def __mul__(self, f):
        f = Fr(f); return Val(self.cM * f, self.cmu * f, self.e * f)
    def __eq__(self, o):
        return self.cM == o.cM and self.cmu == o.cmu and self.e == o.e
    def __repr__(self):
        return '(%s M + %s mu + %s)' % (self.cM, self.cmu, self.e)

ZERO = Val(0, 0, 0)

def parity(v):
    if v.cmu.denominator != 1 or v.e.denominator != 1:
        raise Amb('non-integral mu/const parts %r' % (v,))
    par = (v.e % 2)
    if v.cmu % 2 == 1:
        par = 1 - par
    # M-part: v2(M)>=MARGIN>=1 and cM dyadic with small denominator
    return int(par)

def v2_val(v):
    a = fv2(v.cmu); b = fv2(v.e)
    if a is not None and a < 0 or b is not None and b < 0:
        raise Amb('non-integral small part %r' % (v,))
    if a is None and b is None:
        # small part identically zero: v2 from M-part
        if v.cM == 0:
            raise Amb('zero value')
        return MARGIN + fv2(v.cM)
    if a is not None and b is not None and a == b:
        raise Amb('TIE cmu/e: %r' % (v,))
    s = a if b is None else (b if a is None else min(a, b))
    m = MARGIN + fv2(v.cM) if v.cM != 0 else None
    if m is not None and s >= m:
        raise Amb('TIE with M part: %r' % (v,))
    return s

def min_val(v):
    """lower bound over mu odd >= 1."""
    if v.cM > 0:
        return 1 << 60
    if v.cM < 0:
        raise Amb('negative M part %r' % (v,))
    if v.cmu < 0:
        raise Amb('negative mu coeff %r' % (v,))
    return int(v.cmu * 1 + v.e)

class Walker:
    def __init__(self, nrun):
        u = Val(1, 1, 0)                 # host u = M + mu
        self.A = u + Val(0, 0, 1)
        self.queue = [(u * (1 << a), ('R', a)) for a in range(nrun)]
        self.chain_id = 0
        self.chain_b = {}                # id -> b-label
        self.events = []                 # (chain_id, b-label, j, u)
        self.maxpos = -1

    def step(self):
        (b, lb) = self.queue[0]
        (c, lc) = self.queue[1] if len(self.queue) > 1 else (ZERO, ('Z',))
        rest = self.queue[2:]
        if lb[0] == 'R':
            self.maxpos = max(self.maxpos, lb[1])
        if lc[0] == 'R':
            self.maxpos = max(self.maxpos, lc[1])
        if parity(self.A) == 0:
            self.A = self.A + b + c + Val(0, 0, 3)
            self.queue = rest
            return ('E',)
        x = self.A + b * 2 + Val(0, 0, 3)
        j = v2_val(x)
        u = x * Fr(1, 1 << j)
        if min_val(u) < 3:
            raise Amb('u < 3 possible: %r' % (u,))
        # integrality of u's mu/const coefficients
        if u.cmu.denominator != 1 or u.e.denominator != 1:
            raise Amb('non-integral u %r' % (u,))
        D = c + (self.A + Val(0, 0, 1)) * Fr(1, 2)
        self.chain_id += 1
        cid = self.chain_id
        self.chain_b[cid] = lb
        self.queue = ([(u * (1 << q), ('M', cid, q)) for q in range(j - 1)]
                      + [(D, ('D', cid))] + rest)
        self.A = u + Val(0, 0, 1)
        self.events.append((cid, lb, j, u))
        return ('C', j)

def walk(n_target, verbose_every=None):
    w = Walker(n_target + 50)
    steps = 0
    while w.maxpos < n_target:
        w.step()
        steps += 1
        if steps > 20 * n_target + 1000:
            raise Amb('walk not progressing')
    return w, steps
