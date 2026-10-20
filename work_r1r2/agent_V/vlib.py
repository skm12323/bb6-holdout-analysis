"""vlib.py -- INDEPENDENT re-implementation (agent_V) of the formal pair map F, the crossing
table access, the exact exit walk, the theta-walk and the minimal-information certificate.

Everything here is written from the definitions in work_g6/PROOF_G6.md 5.1, work_m/PROOF_M.md
1-3, work_global_ext/PROOF_EXT.md 2 and work_el/PROOF_EL.md A1-A3; no repository verifier is
imported.  The large table is treated as data (built by the accepted corpus) and cross-checked
against this file's own pair walk on a prefix.

Pair map F (G6 5.1): state (A;P;i), A=(cA,lA), P a list of (c,l) entries, i first unread
original E_a=(2^a,0).  A step reads the first two entries b,c of P||E_i,E_{i+1},... and
advances i by the number of originals read.  Parity = (cA+lA)%2.  Even: A=(cA+cb+cc,
lA+lb+lc+3), consumed entries dropped.  Chain: cx=cA+2cb, lx=lA+2lb+3; requires
(S1) v2(lx)<v2(cx), (S2) cA even; j=v2(lx), u=(cx>>j,lx>>j), A=(cu,lu+1), push
u*2^t (t=0..j-2) followed by D=(cc+cA//2, lc+(lA+1)//2).  F never halts.
The start is A=(1,1),P=[],i=0.
"""
import pickle
from array import array

MISS = -1

def v2(x):
    """2-adic valuation of a nonzero integer (sign ignored)."""
    if x == 0:
        raise ValueError('v2(0)')
    return (x & -x).bit_length() - 1

def v2nz(x):
    return 10**18 if x == 0 else v2(x)

def symres(e, bits):
    """symmetric representative of e mod 2^bits, in (-2^(bits-1), 2^(bits-1)]-ish (r<=M//2 kept)."""
    if bits > 62 and -(1 << 60) < e < (1 << 60):
        return e
    M = 1 << bits
    r = e % M
    return r - M if r > M // 2 else r


# ---------------------------------------------------------------------------------------------
# 1. Own full pair walk, n < NS.  Returns the same record layout as fdata.small_full but is an
#    independent implementation from the definition above.
# ---------------------------------------------------------------------------------------------
def my_small_full(NS):
    A = (1, 1); P = []; i = 0; s = 0; X = {}; seen = -1
    while seen < NS - 1:
        # read the first two entries
        ents = P[:2]
        a = i
        while len(ents) < 2:
            ents.append((1 << a, 0)); a += 1
        (cb, lb), (cc, lc) = ents
        ka = len(P)
        Ypend = ents[0] if ka == 1 else None
        # consume the two read entries (they are the first two of P if P was nonempty)
        P = P[2:]
        for n in ([i] if ka == 1 else [i, i + 1] if ka == 0 else []):
            if n > seen and n < NS:
                seen = n
                t = 'a' if (ka == 0 and i == n) else ('b' if ka == 0 else 'c')
                Y = Ypend if t == 'c' else None
                rec = dict(typ=t, tau=s, A=A, odd=(A[0] + A[1]) % 2, eps=n - v2(A[0]))
                if t == 'c':
                    rec['Y'] = Y
                if rec['odd'] and t != 'a':
                    x = (A[0] + 2 * cb, A[1] + 2 * lb + 3)
                    om = v2(x[1])
                    rec['x'] = x; rec['omega'] = om
                    rec['uW'] = (x[0] >> om, x[1] >> om)
                X[n] = rec
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb + cc, A[1] + lb + lc + 3)
        else:
            cx = A[0] + 2 * cb; lx = A[1] + 2 * lb + 3
            assert v2(lx) < v2(cx), ('S1', s)
            assert A[0] % 2 == 0, ('S2', s)
            j = v2(lx); u = (cx >> j, lx >> j)
            D = (cc + A[0] // 2, lc + (A[1] + 1) // 2)
            P = [(u[0] << t_, u[1] << t_) for t_ in range(j - 1)] + [D] + P
            A = (u[0], u[1] + 1)
        if ka == 0:
            i += 2
        elif ka == 1:
            i += 1
        s += 1
    return X


# ---------------------------------------------------------------------------------------------
# 2. Table: cached crossing data (accepted data input), plus own c'_W for small n.
# ---------------------------------------------------------------------------------------------
class Tab:
    def __init__(self, path, NS=1024, small=None):
        with open(path, 'rb') as f:
            D = pickle.load(f)
        self.typ = D['typ']; self.tau = D['tau']; self.eps = D['eps']
        self.odd = D['odd']; self.lY = D['lY']; self.lA = D['lA']
        self.N = len(self.tau)
        self.NS = NS
        if small is None:
            small = my_small_full(NS)
        self.small = small
        self.cW = {}
        for n, r in small.items():
            if r['typ'] != 'a' and r['odd']:
                self.cW[n] = r['x'][0]

    def lam(self, n):
        return self.lA[n] + 2 * self.lY[n] + 3

    def kind(self, n):
        return 'abc'[self.typ[n] - 97]

    def info(self, n):
        """('e',) even | ('a', k) | ('b'/'c', omega, Phi, eps)."""
        if not self.odd[n]:
            return ('e',)
        if self.typ[n] == 97:
            return ('a', self.tau[n] // 2)
        lam = self.lam(n)
        return (self.kind(n), v2(lam), 3 * self.tau[n] + 5 - lam, self.eps[n])


# ---------------------------------------------------------------------------------------------
# 3. Theta-walk (PROOF_EL A1-A3).  d is an integer; only d mod 2^j matters.
# ---------------------------------------------------------------------------------------------
def theta_walk(T, j, d, limit=10**5):
    path = []
    for _ in range(limit):
        if j <= 4:
            path.append((j, None, 'e')); return path, 'end'
        n = j - 1
        if n >= T.N:
            path.append((j, symres(d, j), '?')); return path, 'nodata'
        inf = T.info(n)
        ds = symres(d, j)
        if inf[0] == 'e':
            path.append((j, ds, 'e')); return path, 'end'
        if inf[0] == 'a':
            z = 3 * inf[1] + d
            path.append((j, ds, 'A'))
            vz = v2nz(z)
            if vz == j - 2:
                return path, 'ND'
            j = j - 1 if vz >= j - 1 else 1 + vz
            d = 3 - d
        else:
            path.append((j, ds, 'B' if inf[0] == 'b' else 'C'))
            d = d + inf[2] - 2
            j = inf[1]
    return path, 'limit'


# ---------------------------------------------------------------------------------------------
# 4. Exact walk on (x, theta) with ceiling (HP precision).  Own implementation.
# ---------------------------------------------------------------------------------------------
def exact_walk(T, x, theta, ceiling, limit=2000):
    """Returns (status, word, maxrec).  status: end / ceiling / zero / nodata / limit.
    x may be negative; only |x| valuations and the recurrence matter (HP signs)."""
    G = 0; word = []; rec = -1
    for _ in range(limit):
        if x == 0:
            return 'zero', word, rec
        j = v2(x); word.append(j); rec = max(rec, j + G)
        if j + G >= ceiling:
            return 'ceiling', word, rec
        n = j - 1
        if n >= T.N:
            return 'nodata', word, rec
        if not T.odd[n]:
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


def certify_slow(T, j, delta, limit=2000):
    """Exact certificate from the literal representative (2^j, 2^j+delta), precision j+1.
    (Only usable for modest j: numbers of size 2^j.)"""
    st, w, r = exact_walk(T, 1 << j, (1 << j) + delta, j + 1, limit)
    return (st == 'end' and r <= j), st, w, r


def certify_fast(T, j, delta, big=64):
    """One symbolic step from the representative (2^j,2^j+delta) to a small state, then the
    exact walk with the reduced precision j-loss.  Same convention as the accepted certify:
    success iff the tail ends with relative records < j-loss."""
    if j < big:
        return certify_slow(T, j, delta)
    n = j - 1
    if n >= T.N:
        return False, 'nodata', [j], j
    if not T.odd[n]:
        return True, 'end', [j], j
    if T.typ[n] == 97:
        k = T.tau[n] // 2
        x1 = 6 * k + 2 * delta
        th1 = 6 * k + delta + 3
        loss = 1
    else:
        lam = T.lam(n)
        x1 = lam                       # low bits of c'u+lam, u=1: c' vanishes below precision
        th1 = 3 * T.tau[n] + 3 + delta
        loss = 1 + T.eps[n]
    st, w, r = exact_walk(T, x1, th1, j - loss)
    return (st == 'end' and r < j - loss), st, [j] + w, max(j, r + loss)


# ---------------------------------------------------------------------------------------------
# 5. Exact S(J) beta-walk (Lemma BR), own implementation.  Returns chains.
# ---------------------------------------------------------------------------------------------
def beta_walk(T, J, limit=10**5):
    """beta-only walk of S(J): Theta=3d+1, x=beta, starting d=0,beta=0,j=J.
    chain 0 is the fire (d=0,beta=0); chain t>=1 has beta=beta_t = lambda_{x_t}.
    Returns list of dicts and status; a chain with j>=? and record >= J is reported."""
    j = J; d = 0; beta = 0; G = 0; out = []
    for t in range(limit):
        n = j - 1
        rec = j + G
        if n >= T.N:
            out.append(dict(t=t, j=j, d=d, beta=beta, G=G, rec=rec, typ='?', n=n))
            return out, 'nodata'
        if not T.odd[n]:
            out.append(dict(t=t, j=j, d=d, beta=beta, G=G, rec=rec, typ='e', n=n))
            return out, 'end'
        k = T.kind(n)
        out.append(dict(t=t, j=j, d=d, beta=beta, G=G, rec=rec, typ=k, n=n))
        if k == 'a':
            B = 6 * d + 2 + 3 * T.tau[n] - (beta >> 1)
        else:
            if t == 0:
                B = T.lam(n)
            else:
                if n not in T.cW:
                    out.append(dict(t=t + 1, j=None, d=None, beta=None, G=None, rec=None,
                                    typ='?', n=n))
                    return out, 'nodata'
                B = (beta >> j) * T.cW[n] + T.lam(n)
        d += 1 + T.tau[n]
        G += 1 + T.eps[n]
        j = v2(B); beta = B
        if j + G >= J:
            out.append(dict(t=t + 1, j=j, d=d, beta=beta, G=G, rec=j + G, typ='TIE', n=j - 1))
            return out, 'TIE'
    return out, 'limit'


# Theta/d from beta: Theta_t = 3d_t+1, x_t = beta_t, so defect D_t = 3d_t+1-beta_t.
