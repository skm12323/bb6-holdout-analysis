"""famlib.py -- shared library for Route A (work in ext/a).  Python stdlib only.
Imports REPO/work_el/verify_el.py and the local copy verify_tie2_copy.py READ-ONLY (functions only).

Psi-families (REPORT.md section 3):  Psi(j; P, Q; r, m) :=
    { chains with parameter j, lambda_u == r (mod 2^m) odd, Theta == P + Q*2^j*lambda_u (mod 2^PREC) }
P, Q are 2-adic numbers (here: rationals with odd denominators, stored as residues mod 2^PREC).
Exact a-step rule (Lemma F2):  E = P+3k,  P' = P+3+6k-4QE/(4Q-1),  Q' = 2Q/(4Q-1),
    j' = min(1+v2(E), j-1) if v2(E) != j-2;  tie (v2(E) = j-2): j' = j-1+v2(E/2^(j-2)+(4Q-1)*lambda_u).
"""
import os, sys, pickle
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / 'work_m'))
sys.path.insert(0, str(REPO / 'work_el'))
sys.path.insert(0, str(HERE))
import verify_el as ve
import verify_tie2_copy as t2

N = 10**6
PREC = 2048
MOD = 1 << PREC
v2 = ve.v2
CACHE = HERE / '_walk.pkl'


def walk():
    if CACHE.exists():
        with open(CACHE, 'rb') as f:
            return pickle.load(f)
    Xt, typ, par, chain, st, steps = ve.real_walk(N)
    real = t2.sigma_walk(N, chain)
    D = (Xt, typ, par, chain, real, steps)
    with open(CACHE, 'wb') as f:
        pickle.dump(D, f, protocol=pickle.HIGHEST_PROTOCOL)
    return D


def res(x, M=PREC):
    """2-adic residue of a Fraction / int with odd denominator, mod 2^M"""
    x = Fraction(x)
    assert x.denominator % 2 == 1
    return (x.numerator * pow(x.denominator, -1, 1 << M)) % (1 << M)


def v2m(x, M=PREC):
    x %= (1 << M)
    return M if x == 0 else v2(x)


def make_psi(Xt, typ, par, real, ext):
    """psi(j,P,Q): exact run of the family Psi(j;P,Q;1,1) (lambda_u free odd).
    Returns list of leaves: dict(res=END|ANYJ|EXT, path=[(j,T mod 2^j,kind,h)], anyj=(jmin,P,Q), ...).
    a-steps exact; at the first b/c step the knowledge is converted to bit knowledge
    (Theta mod 2^M, lambda_u mod 2^m) and the TIE2 extended automaton `ext` continues."""
    def psi(j, P, Q, h=1):
        r, m = 1, 1
        P %= MOD; Q %= MOD
        path = []; aouts = []
        while True:
            n = j - 1
            if n >= N:
                return dict(res='NODATA', path=path, aouts=aouts)
            if par[n] == 0:
                return dict(res='END', path=path, aouts=aouts)
            if typ[n] == 'a':
                k = Xt[n] // 2
                E = (P + 3 * k) % MOD
                nu = v2m(E)
                if nu >= PREC - 64:                       # E == 0 mod 2^(PREC-64): only case (iii) is decidable
                    assert j - 1 <= PREC - 64, 'precision'
                    nu = PREC
                iq = pow((4 * Q - 1) % MOD, -1, MOD)
                Pn = (P + 3 + 6 * k - 4 * Q * E * iq) % MOD
                Qn = (2 * Q * iq) % MOD
                if nu != j - 2:
                    jn = min(nu + 1, j - 1)
                    # lambda' = x'/2^j',  x' = 2E + 2^(j-1)(4Q-1) lambda,  lambda == r mod 2^m
                    xr = (2 * E + ((4 * Q - 1) << (j - 1)) * r) % MOD
                    mn = min(m + j - 1, PREC) - jn          # xr is known mod 2^min(m+j-1, PREC)
                    assert v2m(xr) == jn and mn >= 1
                    r = (xr >> jn) % (1 << mn); m = mn
                    kind = 'a'
                else:
                    R0 = (E >> (j - 2)) + (4 * Q - 1) * r
                    e = v2m(R0)
                    mR = min(m, PREC - (j - 2))            # R0 is known mod 2^mR
                    if e < mR:
                        jn = j - 1 + e
                        r = (R0 >> e) % (1 << (mR - e)); m = mR - e
                        kind = 'A'
                    else:
                        # tie with free part: every e >= m occurs; output Psi(j';P',Q') for all j' >= j-1+m
                        return dict(res='ANYJ', path=path, aouts=aouts, anyj=(j - 1 + mR, Pn, Qn), at=(j, P % (1 << j)))
                h = h + j - jn - 1
                P, Q, j = Pn, Qn, jn
                T = (P + (Q << j) * r)            # Theta mod 2^(j+v2(Q)+m)
                M = min(j + v2m(Q) + m, PREC - 64)
                path.append((j, T % (1 << j), kind, h))
                aouts.append((j, T % (1 << M), M, r, min(m, max(h, 1))))
            else:
                tau = Xt[n]; jw, luw, sgw = real[tau]
                vv = sgw - jw
                M = min(j + v2m(Q) + m, PREC - 64)
                T = (P + (Q << j) * r + 3 * tau + 3) % (1 << M)
                mm = min(vv + 1, 4096); u = (luw + (1 << vv)) % (1 << mm)
                path.append((jw, T % (1 << jw), 'c', h + 1))
                leaves = ext(jw, T, M, u, mm, h + 1)
                return dict(res='EXT', path=path, aouts=aouts, ext=leaves)
    return psi
