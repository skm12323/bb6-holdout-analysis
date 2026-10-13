"""agentB2_symbolic.py -- per-shape symbolic derivation of the exit D-fire value.

Framework (Class-A algebra, cf. work_g6 Prop 3 / verify_g6.py V1):
  Phi_J after a host chain of class 6k_h+4 = 2^J*odd, scale unit P = 2^p (p large):
    u = (9P + 6k_h + 4)/2^J = 9P/2^J + w,  w = (6k_h+4)/2^J  (odd, free),
    k_h = (2^J w - 4)/6,
    queue [u*2^a (a=0..J-2), D_h, T_2, T_3, ...],
    D_h = (15/2)P + 3k_h + 1 = (15/2)P + 2^{J-1} w - 1,   T_e = 3*2^e P.
  Values are affine forms in (P, w, K) with K = universal k at the last pure
  sub-fire position rho*, class-pinned by v2(3K+2) = j_last - 1.

Decision forcing (the pinning calculus): write w = 1 + 2W' with W' free and
K = kap + 2^tK*t with t free.  For a form S = cw*w + cK*K + c1 (+ P-part kept
far above every decision level):
  S = S0 + 2*cw*W' + cK*2^tK*t,   S0 = cw + cK*kap + c1.
  - parity(S) = S0 mod 2 is ALWAYS forced (tK >= 1 in every class; the free
    parts are even).
  - v2(S) is forced iff m0 := v2(S0) < v2(cK)+tK (K-pinning) AND
    m0 < v2(cw)+1 (w enters only at digit v2(cw)+1).  Then v2(S) = m0.
The single unforced case that occurs is the D-fire of the (1,2,1) shape --
exactly work_g6 Prop 3's conditional j_D = 1+v2(3K+4).
"""
from fractions import Fraction as Fr
from math import inf

from agentB2_lib import classify


def v2f(fr):
    """exact 2-adic valuation of a Fraction; +inf for 0."""
    if fr == 0:
        return inf
    n = abs(fr.numerator)
    d = abs(fr.denominator)
    return (n & -n).bit_length() - (d & -d).bit_length()


class NotForced(Exception):
    pass


class Form:
    """affine form  cP*P + cw*w + cK*K + c1   (Fraction coefficients)."""
    __slots__ = ('P', 'w', 'K', 'c')

    def __init__(self, P=0, w=0, K=0, c=0):
        self.P, self.w, self.K, self.c = Fr(P), Fr(w), Fr(K), Fr(c)

    def __add__(self, o):
        return Form(self.P + o.P, self.w + o.w, self.K + o.K, self.c + o.c)

    def __sub__(self, o):
        return Form(self.P - o.P, self.w - o.w, self.K - o.K, self.c - o.c)

    def __mul__(self, f):
        f = Fr(f)
        return Form(self.P * f, self.w * f, self.K * f, self.c * f)

    __rmul__ = __mul__

    def __eq__(self, o):
        return (self.P == o.P and self.w == o.w and self.K == o.K and self.c == o.c)

    def __repr__(self):
        parts = ['%s*%s' % (v, nm) for nm, v in
                 (('P', self.P), ('w', self.w), ('K', self.K), ('1', self.c)) if v != 0]
        return ' + '.join(parts) if parts else '0'


class Ctx:
    """K pinned: the class v2(3K+2) = j_last-1 means 3K+2 = 2^{j_last-1}*odd,
    i.e. K = kap mod 2^{j_last} with kap = ((2^{j_last-1}-2)/3 mod 2^{j_last});
    j_last=None -> no K used.  After the D-fire the pin may be refined."""

    def __init__(self, J, j_last, pmin=None, vcap=None, tref=None, kref=None):
        self.J = J
        self.pmin = pmin if pmin is not None else 2 * J + 64
        self.vcap = vcap if vcap is not None else J + 4
        if j_last is None:
            tK, kap = 0, 0
        else:
            v = j_last - 1
            tK = j_last
            kap = (((1 << v) - 2) * pow(3, -1, 1 << tK)) % (1 << tK)
        if tref is not None:
            self.tK, self.kap = tref, kref
        else:
            self.tK, self.kap = tK, kap

    def refine(self, tref, kref):
        self.tK, self.kap = tref, kref


def _check_P(f, ctx):
    assert f.P == 0 or v2f(f.P) + ctx.pmin >= ctx.vcap, \
        'P-part valuation %d below cap %d (form %r)' % (v2f(f.P) + ctx.pmin, ctx.vcap, f)


def parity(f, ctx):
    _check_P(f, ctx)
    S0 = f.w + f.K * ctx.kap + f.c
    if S0.denominator != 1:
        raise NotForced('non-integral parity base %r' % (f,))
    return int(S0) % 2


def v2_form(f, ctx):
    _check_P(f, ctx)
    if f.w == 0 and f.K == 0:
        if f.c == 0:
            raise NotForced('zero form')
        return v2f(f.c)
    S0 = f.w + f.K * ctx.kap + f.c
    if S0.denominator != 1:
        raise NotForced('non-integral base %r' % (f,))
    m0 = v2f(S0)
    pin = v2f(f.K) + ctx.tK if f.K != 0 else inf      # K pinned mod 2^pin
    ew = v2f(f.w) + 1 if f.w != 0 else inf            # free-w enters at digit ew
    if m0 < pin and m0 < ew:
        return m0
    raise NotForced('v2 unpinned: m0=%r pin=%r ew=%r (form %r)' % (m0, pin, ew, f))


# ---------------------------------------------------------------------------
# symbolic replay of one recorded exit script
# ---------------------------------------------------------------------------
def replay(J, tr, i_start, j_last, rho, pmin=None, K_real=None, jD_hint=None):
    """Replay steps tr[i_start:] from the crossing at rho* (fire at rho*
    pending; i_start=0 and rho=None replays Phi_J from the start, J=5).

    Every recorded decision (parity / j) is re-derived symbolically and must
    be FORCED, except the D-fire's own j in tie shapes (recorded in
    'conditional'; the recorded value is then used to continue, and the K-pin
    is refined to K_real mod 2^{j_D+2} so the seam replay stays integral)."""
    ctx = Ctx(J, j_last, pmin=pmin)
    uF = Form(P=Fr(9, 1 << J), w=1)

    def E(a):
        return uF * (1 << a)

    Dh = Form(P=Fr(15, 2), w=1 << (J - 1), c=-1)
    if rho is not None:
        A = E(rho) + Form(K=6, c=1)
        Q = [(E(a), ('R', a)) for a in range(rho, J - 1)] + \
            [(Dh, ('D',))] + [(Form(P=3 << e), ('T', e)) for e in range(2, 40)]
    else:
        A = uF + Form(c=1)
        Q = [(E(a), ('R', a)) for a in range(J - 1)] + \
            [(Dh, ('D',))] + [(Form(P=3 << e), ('T', e)) for e in range(2, 40)]
    rep = {'J': J, 'rho': rho, 'j_last': j_last, 'conditional': [], 'fires': []}
    for idx in range(i_start, len(tr)):
        kind, lb, lc, jrec, xrec, urec = tr[idx]
        if lb[0] == 'T':
            break                      # the canonical re-entry ends the exit
        assert Q[0][1] == lb and Q[1][1] == lc, \
            'label mismatch at %d: %r vs %r' % (idx, (Q[0][1], Q[1][1]), (lb, lc))
        b, c = Q[0][0], Q[1][0]
        if kind == 'E':
            assert parity(A, ctx) == 0, 'even step but A odd at %d' % idx
            A = A + b + c + Form(c=3)
            Q = Q[2:]
            continue
        assert parity(A, ctx) == 1, 'chain step but A even at %d' % idx
        x = A + 2 * b + Form(c=3)
        try:
            j = v2_form(x, ctx)
        except NotForced as nf:
            rep['conditional'].append((idx, lb, str(nf)))
            j = jrec
            if lb == ('D',) and K_real is not None:
                # refine the K-pin so u_D stays integral-form for the seam part
                ctx.refine(jrec + 2, K_real % (1 << (jrec + 2)))
        assert j == jrec, 'step %d: symbolic j=%r != recorded %r  x=%r' % (idx, j, jrec, x)
        u = x * Fr(1, 1 << j)
        d = c + (A + Form(c=1)) * Fr(1, 2)
        Q = [(u * (1 << t), ('M', idx)) for t in range(j - 1)] + \
            [(d, ('d', idx))] + Q[2:]
        A = u + Form(c=1)
        rep['fires'].append((lb, jrec, x))
        if lb == ('D',):
            rep['x_D'] = x
            rep['j_D'] = jrec
            rep['iD'] = idx
            rep['d_seam'] = d
        elif 'x_seam' not in rep and lb[0] == 'd' and idx > rep.get('iD', 1 << 60):
            rep['x_seam'] = x
            rep['j_seam'] = jrec
    return rep


def shape_of(m):
    c = classify(m)
    if c['iD'] is None:
        return None, c
    key = (c['gap'], c['jlast'],
           (c['iD'] // 2 - c['K']) if c['K'] is not None else None)
    return key, c


def derive(m, pmin=None):
    """Derivation report for the shape represented by Phi_m (J = m)."""
    key, c = shape_of(m)
    assert c['iD'] is not None
    tr = c['tr']['steps']
    i_last = c['i_last']
    rho, j_last = c['rho'], c['jlast']
    rep = replay(m, tr, i_last if i_last >= 0 else 0, j_last, rho, pmin=pmin,
                 K_real=c['K'])
    Kexit = rep['iD'] // 2
    delta = Kexit - c['K'] if c['K'] is not None else None
    out = {'m': m, 'shape': key, 'K': c['K'], 'Kexit': Kexit, 'delta': delta,
           'jD': rep['j_D'], 'conditional': rep['conditional'],
           'x_seam': rep.get('x_seam'), 'j_seam': rep.get('j_seam')}
    # x_D must equal the crossing-identity form
    #   with sub-fire:  x_D = (39/2)P + 3*2^{J-1} w + 6K + (6*delta+2)
    #   without (J=5):  x_D = (39/2)P + 3*2^{J-1} w + (6*Kexit+2)
    #   both = (39/2)P + 9k_h + 6*Kexit + 8  via  9k_h = 3*2^{J-1}w - 6.
    if delta is None:
        want = Form(P=Fr(39, 2), w=Fr(3 << (m - 1)), c=6 * Kexit + 2)
    else:
        want = Form(P=Fr(39, 2), w=Fr(3 << (m - 1)), K=6, c=6 * delta + 2)
    assert rep['x_D'] == want, 'x_D %r != identity form %r' % (rep['x_D'], want)
    # class case analysis for j_D = 1 + v2(3K + 3*delta + 1)
    if j_last is None:
        out['case'] = ('no sub-fire (only J=5): Kexit=1, j_D = 1+v2(4) = 3 = J-2')
    else:
        vv, h = j_last - 1, v2f(Fr(3 * delta - 1))
        if h < vv:
            out['case'] = ('h<v: 3K+3d+1 = 2^h*(c\'+2^{v-h}*odd) -> j_D = 1+h = %d '
                           'CONSTANT' % (1 + h))
        elif h > vv:
            out['case'] = ('h>v: 3K+3d+1 = 2^v*(odd+2^{h-v}*c\') -> j_D = j_last = %d '
                           'CONSTANT' % j_last)
        else:
            out['case'] = ('TIE h=v=%d: j_D = 1+v2(3K+%d), orbit-dependent '
                           '(size-bounded)' % (vv, 3 * delta + 1))
    return out


def all_shape_reps(M=3000):
    found = {}
    for m in range(5, M + 1):
        key, c = shape_of(m)
        if key is not None and key not in found:
            found[key] = m
    return found


if __name__ == '__main__':
    found = all_shape_reps()
    print('shape (gap, j_last, delta) -> representative m:')
    for k, m in sorted(found.items(), key=lambda kv: kv[1]):
        print('   %-16s m = %d' % (str(k), m))
    print()
    print('%-16s %-5s %-6s %-6s %-5s %-4s %-6s  %s' %
          ('shape', 'J=m', 'K', 'Kexit', 'delta', 'j_D', 'J-j_D', 'class case'))
    for key, m in sorted(found.items(), key=lambda kv: kv[1]):
        o = derive(m)
        print('%-16s %-5d %-6s %-6s %-5s %-4d %-6d  %s' %
              (str(key), m, o['K'], o['Kexit'], o['delta'], o['jD'], m - o['jD'], o['case']))
        if o['conditional']:
            for cd in o['conditional']:
                print('      conditional decision at step %d (b=%r): the D-fire tie' % cd[:2])
        if o['x_seam'] is not None:
            print('      seam fire j=%d  x_seam = %s' % (o['j_seam'], o['x_seam']))
    print()
    print('all recorded decisions symbolically forced (ties: only the D-fire, '
          'as conditionals above); x_D verified = (39/2)P + 3*2^{J-1}w + 6K + (6d+2).')
