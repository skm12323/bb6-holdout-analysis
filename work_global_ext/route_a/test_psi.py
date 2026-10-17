import famlib as F
from fractions import Fraction as Fr
Xt, typ, par, chain, real, steps = F.walk()
ext = F.t2.make_ext(Xt, typ, par, real)
psi = F.make_psi(Xt, typ, par, real, ext)
for (j, P, Q) in [(5, 5, 1), (5, Fr(-1, 3), 1), (5, Fr(-19, 9), 1), (5, Fr(-73, 27), 1), (5, 37, 1), (5, Fr(10, 3), Fr(2, 3)), (5, 2, 1)]:
    L = psi(j, F.res(P), F.res(Q))
    out = dict(L)
    if 'anyj' in out:
        jm, Pn, Qn = out['anyj']
        # identify Pn, Qn as small rationals
        def ident(x):
            for d in (1, 3, 9, 27, 81, 5, 15, 11):
                for nmr in range(-2000, 2001):
                    if F.res(Fr(nmr, d)) == x: return Fr(nmr, d)
            return None
        out['anyj'] = (jm, ident(Pn), ident(Qn))
    out.pop('ext', None); out.pop('aouts', None)
    print((j, P, Q), out)
