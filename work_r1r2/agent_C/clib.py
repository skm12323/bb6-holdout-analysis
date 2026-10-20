"""clib.py -- shared exact machinery for DIRECTION C (R2 for c-landings), agent_C.

Conventions (accepted corpus):
  PROOF_EXT section 2 walk rules: state (j, Theta, x = 2^j u), u odd, n = j-1, reads X(n).
    X(n) even        -> stop (even return)
    type a (tau = 2k) -> x' = 2 Theta + 3 tau - x/2,  Theta' = Theta + 3 + 3 tau
    type b/c          -> x' = c'_W(n) u + lambda'_W(n), Theta' = Theta + 3 + 3 tau
    loss Gamma += 1 + eps(n), eps = 0 for type a, eps(n) = n - v2(c'_W) for b/c.
  PROOF_EL A1-A3 theta-tilde automaton (j, d): a: j' from 3k+d, d' = 3-d;
    b/c: j' = omega(n) = v2(lambda'_W), d' = d + Phi - 2, Phi = 3 tau + 5 - lambda'_W
    (= 1 for b, = 1 - lambda_Y for c).
  Table (fdata.lam_walk): typ (97/98/99), tau, eps, odd, lY, lA;
    lambda'_W = lA + 2 lY + 3 = 3 tau + 4 + lY  (ENTRY mass identity lambda_A + lambda_Y = 3 tau + 1).

No repository file is written by this module.
"""
import pickle
import sys

REPO = r'D:\math_cc'
sys.path.insert(0, REPO + r'\work_global_ext\route_c')
from fdata import small_full, v2  # noqa: E402  (read-only import, accepted canonical walk)


class Table:
    """Cached canonical crossing table (built by work_deep with fdata.lam_walk)."""

    def __init__(self, path, NS=2048, cW_from=None):
        import os
        if not os.path.exists(path):
            raise SystemExit('missing table %s' % path)
        with open(path, 'rb') as f:
            D = pickle.load(f)
        self.typ = D['typ']
        self.oddb = D['odd']
        self.tau = D['tau']
        self.eps = D['eps']
        self.lY = D['lY']
        self.lA = D['lA']
        self.N = len(self.tau)
        S = small_full(NS)
        self.cW = {}
        for n, r in S.items():
            if r['odd'] and r['typ'] != 'a':
                self.cW[n] = r['x'][0]
                assert r['x'][1] == self.lam(n), ('lambda mismatch', n)
        self.NS = NS

    def kind(self, n):
        return chr(self.typ[n])

    def odd(self, n):
        return self.oddb[n] != 0

    def lam(self, n):
        return self.lA[n] + 2 * self.lY[n] + 3

    def info(self, n):
        """('e',) | ('a', k) | ('b'/'c', omega, Phi, eps)"""
        if not self.oddb[n]:
            return ('e',)
        if self.typ[n] == 97:
            return ('a', self.tau[n] // 2)
        L = self.lam(n)
        return (self.kind(n), v2(L), 3 * self.tau[n] + 5 - L, self.eps[n])

    def sigma(self, n):
        """precision v2(c'_W(n)) = n - eps(n) of W's chain at a b/c crossing."""
        return n - self.eps[n]


def symres(e, bits):
    M = 1 << bits
    r = e % M
    return r - M if r > M // 2 else r


def theta_walk(T, j, d, limit=4000):
    """theta-tilde walk from (j, d mod 2^j).  Returns (path, status);
    status in {'end','ND','nodata','limit'}.  'ND' = NT failure (non-descent, needs higher bits).
    path entries: (j, symbolic defect, letter)."""
    path = []
    for _ in range(limit):
        if j <= 4:
            path.append((j, None, 'e'))
            return path, 'end'
        n = j - 1
        if n >= T.N:
            path.append((j, symres(d, j), '?'))
            return path, 'nodata'
        inf = T.info(n)
        ds = symres(d, j)
        if inf[0] == 'e':
            path.append((j, ds, 'e'))
            return path, 'end'
        if inf[0] == 'a':
            z = 3 * inf[1] + d
            path.append((j, ds, 'A'))
            if z == 0:
                return path, 'ND'
            vz = v2(abs(z))
            if vz == j - 2:
                return path, 'ND'
            j = j - 1 if vz >= j - 1 else 1 + vz
            d = 3 - d
        else:
            path.append((j, ds, 'B' if inf[0] == 'b' else 'C'))
            d = d + inf[2] - 2
            j = inf[1]
    return path, 'limit'


def exact_walk(T, x, theta, ceil, limit=4000):
    """Exact integer walk from state (j = v2(x), Theta = theta, x).  Stops when
    j + Gamma >= ceil ('ceiling'), x == 0 ('zero'), even crossing ('end'), no data.
    Returns (status, word, maxrec)."""
    G = 0
    word = []
    rec = -1
    for _ in range(limit):
        if x == 0:
            return 'zero', word, rec
        j = v2(abs(x))
        word.append(j)
        rec = max(rec, j + G)
        if j + G >= ceil:
            return 'ceiling', word, rec
        n = j - 1
        if n >= T.N:
            return 'nodata', word, rec
        if not T.odd(n):
            return 'end', word, rec
        tau = T.tau[n]
        if T.typ[n] == 97:
            x = 2 * theta + 3 * tau - (x >> 1)
        else:
            if n not in T.cW:
                return 'nodata', word, rec
            x = T.cW[n] * (x >> j) + T.lam(n)
        theta += 3 + 3 * tau
        G += 1 + T.eps[n]
    return 'limit', word, rec


def certify(T, j, delta, ceil=None):
    """certify(j, delta): exact walk from the representative (2^j, 2^j+delta) ends
    with every record <= j (Prop 3.2 / work_deep Thm 3.1).  Optionally with a
    ceiling `ceil` instead of j+1 (relaxed certificate; records <= ceil-1)."""
    C = (j + 1) if ceil is None else ceil
    st, w, r = exact_walk(T, 1 << j, (1 << j) + delta, C)
    return (st == 'end' and r <= C - 1), st, w, r


def first_chain_tie_class(T, j):
    """If X(j-1) is odd type a: the residue 2^(j-2) - 3 k_(j-1) mod 2^(j-1)
    (the class delta for which the representative's first step is a tie).
    Returns None if X(j-1) is not odd type a."""
    n = j - 1
    if n < 0 or n >= T.N or not T.odd(n) or T.typ[n] != 97:
        return None
    k = T.tau[n] // 2
    return (1 << (j - 2)) - 3 * k


def bad_set(T, j, jmax_direct=40):
    """Exhaustive Bad_j = {delta mod 2^(j+1) : certify(j, delta) fails}, j >= 5.
    Cost 2^(j+1) exact walks; only for small j (j <= 27 used here)."""
    M = 1 << (j + 1)
    bad = []
    for d in range(M):
        ok, st, w, r = certify(T, j, d)
        if not ok:
            bad.append(d)
    return bad


# ------------------------------------------------------------------ c-landing class
def c_class(j_u, tau_n, theta, delta_lY=0):
    """Landing class of a c-step at a deep chain with theta_T = theta,
    landing parameter j_u = omega(n_T) = v2(3 tau + 4 + lambda_Y):
        delta = theta + 3 tau + 3 - 2^j_u  (mod 2^(j_u+1)).
    delta_lY is accepted and ignored (documented independence of the higher
    bits of lambda_Y; see NOTES.md Theorem C1(c))."""
    M = 1 << (j_u + 1)
    return (theta + 3 * tau_n + 3 - (1 << j_u)) % M
