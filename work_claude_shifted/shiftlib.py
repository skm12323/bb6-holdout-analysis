"""shiftlib.py -- shared tables and integer walks for work_claude_shifted (UNREVIEWED).

Walk rules (PROOF_EXT §2, Lemma TR): state (j, Theta, x), x = 2^j u, u odd, n = j-1, read X(n).
  X(n) even        -> stop (even return)
  type a (tau=2k)  -> x' = 2 Theta + 3 tau - x/2
  type b/c         -> x' = c'_W(n) u + lambda'_W(n)        (W's chain at tau(n))
  Theta' = Theta + 3 + 3 tau(n);  loss Gamma += 1 + eps(n).
Data: work_global_ext/route_c/fdata.py (lam_walk for the lambda-only table, small_full for c'_W at small n).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_c'))
from fdata import lam_walk, small_full, v2  # noqa: E402


class Tables:
    def __init__(self, N, NS=1024):
        self.N = N
        D = lam_walk(N)
        self.typ, self.tau, self.eps, self.odd = D['typ'], D['tau'], D['eps'], D['odd']
        self.lA, self.lY = D['lA'], D['lY']
        S = small_full(NS)
        self.NS = NS
        self.cW = {}
        for n, r in S.items():
            if r['odd'] and r['typ'] != 'a':
                self.cW[n] = r['x'][0]
                assert r['x'][1] == self.lam(n), ('lambda mismatch', n)

    def lam(self, n):
        """lambda'_W(n) for odd b/c crossings: lambda_A + 2 lambda_Y + 3."""
        return self.lA[n] + 2 * self.lY[n] + 3

    def kind(self, n):
        return chr(self.typ[n])


def walk(T, j, theta, x, prec=None, limit=10**5):
    """Exact integer walk.  Returns dict(word, types, record, status, nd, steps, a_steps).
    record = max(j_t + Gamma_t); status in end/ceiling/nonpositive/limit/nodata.
    nd = number of non-descents j_{t+1} >= j_t.  dh_fail = a-steps with j' >= j-1."""
    G = 0; word = []; types = ''; rec = 0; nd = 0; dhf = 0; prevj = None
    for _ in range(limit):
        if x <= 0:
            return dict(word=word, types=types, record=rec, status='nonpositive', nd=nd, dh_fail=dhf)
        assert v2(x) == j
        if prevj is not None and j >= prevj:
            nd += 1
        word.append(j); rec = max(rec, j + G)
        if prec is not None and j + G >= prec:
            return dict(word=word, types=types, record=rec, status='ceiling', nd=nd, dh_fail=dhf)
        n = j - 1
        if n >= T.N or (T.kind(n) != 'a' and T.odd[n] and n not in T.cW):
            return dict(word=word, types=types, record=rec, status='nodata', nd=nd, dh_fail=dhf)
        if not T.odd[n]:
            return dict(word=word, types=types, record=rec, status='end', nd=nd, dh_fail=dhf)
        t = T.kind(n); types += t; tau = T.tau[n]
        if t == 'a':
            xn = 2 * theta + 3 * tau - (x >> 1)
        else:
            xn = T.cW[n] * (x >> j) + T.lam(n)
        theta += 3 + 3 * tau; G += 1 + T.eps[n]
        prevj = j; x = xn
        if x > 0:
            j = v2(x)
            if t == 'a' and j >= prevj - 1:
                dhf += 1
    return dict(word=word, types=types, record=rec, status='limit', nd=nd, dh_fail=dhf)


def sym_beta(T, J, limit=200):
    """beta-only walk of S(J) (Lemma BR), valid while tie-free.  Returns list of chains
    (j, d, beta, Gamma, type_of_return) and status.  Theta_beta = 3d+1."""
    j = J; d = 0; beta = 0; G = 0; out = []
    for t in range(limit):
        n = j - 1
        if n >= T.N:
            return out, 'nodata'
        if not T.odd[n]:
            out.append((j, d, beta, G, 'e'))
            return out, 'end'
        k = T.kind(n)
        out.append((j, d, beta, G, k))
        if k == 'a':
            B = 6 * d + 2 + 3 * T.tau[n] - (beta >> 1)
        else:
            if t == 0:
                B = T.lam(n)
            else:
                if n not in T.cW:
                    return out, 'nodata'
                B = (beta >> j) * T.cW[n] + T.lam(n)
        d += 1 + T.tau[n]; G += 1 + T.eps[n]
        j = v2(B); beta = B
        if j + G >= J:
            out.append((j, d, beta, G, '?'))
            return out, 'TIE'
    return out, 'limit'


def symres(e, mod_bits):
    """symmetric residue of e modulo 2^mod_bits."""
    if mod_bits > 62 and -(1 << 60) < e < (1 << 60):
        return e
    M = 1 << mod_bits
    r = e % M
    return r - M if r > M // 2 else r


class DefectTable:
    """Data for the theta-walk (= defect walk) on (j, d mod 2^j), read lazily from Tables T.
    info(n): ('e',) even crossing; ('a', k) odd type a, tau = 2k; (kind, omega, Phi, eps) odd b/c, where
    Phi = 3 tau + 5 - lambda'_W(n) is the exact defect of W's chain at tau(n) (= theta-tilde^W, PROOF_EL A3)."""
    def __init__(self, T):
        self.T = T; self.NT = T.N

    def info(self, n):
        T = self.T
        if not T.odd[n]:
            return ('e',)
        if T.kind(n) == 'a':
            return ('a', T.tau[n] // 2)
        lam = T.lam(n)
        return (T.kind(n), v2(lam), 3 * T.tau[n] + 5 - lam, T.eps[n])


def dw(DT, j, d, limit=10**4):
    """theta-walk (PROOF_EL A1-A3) from (j, d); d stands for its class mod 2^j.
    a-step: z = 3k+d; v2(z) = j-2 -> 'ND' (NT failure, non-descent, PROOF_EL A2);
            v2(z) >= j-1 -> j' = j-1 (one-step descent); else j' = 1+v2(z); d' = 3-d.
    b/c-step: j' = omega(n), d' = d + Phi(n) - 2.   Ends at an even crossing or j <= 4.
    Returns (path, status), path = [(j, d_sym, letter)], status in end/ND/nodata."""
    path = []
    for _ in range(limit):
        if j <= 4:
            path.append((j, None, 'e')); return path, 'end'
        n = j - 1
        if n >= DT.NT:
            path.append((j, symres(d, j), '?')); return path, 'nodata'
        inf = DT.info(n)
        ds = symres(d, j)
        if inf[0] == 'e':
            path.append((j, ds, 'e')); return path, 'end'
        if inf[0] == 'a':
            z = 3 * inf[1] + d
            path.append((j, ds, 'A'))
            vz = v2(z) if z else 10**18          # v2 of z mod 2^(j-1) only matters through min(., j-1)
            if vz == j - 2:
                return path, 'ND'
            j = j - 1 if vz >= j - 1 else 1 + vz
            d = 3 - d
        else:
            path.append((j, ds, 'B' if inf[0] == 'b' else 'C'))
            d = d + inf[2] - 2; j = inf[1]
    return path, 'limit'


def exact_tail(T, x, theta, ceil, limit=500):
    """Exact integer walk from (x, theta) (x != 0, any sign: only valuations and the table matter);
    'ceil' = number of trusted bits (HP precision).
    Returns (status, word, maxrec) where status in end/ceiling/zero/nodata/limit and
    maxrec = max over chains of j + loss (loss counted from this state)."""
    G = 0; word = []; rec = -1
    for _ in range(limit):
        if x == 0:
            return 'zero', word, rec          # HP needs x* != 0; signs are irrelevant to valuations
        j = v2(x); word.append(j); rec = max(rec, j + G)
        if j + G >= ceil:
            return 'ceiling', word, rec
        n = j - 1
        if n >= T.N:
            return 'nodata', word, rec
        if not T.odd[n]:
            return 'end', word, rec
        t = T.kind(n); tau = T.tau[n]
        if t == 'a':
            x = 2 * theta + 3 * tau - (x >> 1)
        else:
            if n not in T.cW:
                return 'nodata', word, rec
            x = T.cW[n] * (x >> j) + T.lam(n)
        theta += 3 + 3 * tau; G += 1 + T.eps[n]
    return 'limit', word, rec


def certify(T, j, delta, big=64):
    """Minimal-information certificate for a start of parameter j and exact defect delta
    (x = 2^j * odd, Theta = x + delta, both known modulo 2^(j+1)).  Certified iff the walk from the
    representative (2^j, 2^j + delta) ends with every record j_t + loss_t <= j (HP with precision j+1).
    For j >= big the first step is taken symbolically (the representative's high term 2^j does not
    affect anything below precision), leaving an exact small state.
    Returns (ok, status, word, maxrec)."""
    if j < big:
        st, w, r = exact_tail(T, 1 << j, (1 << j) + delta, j + 1)
        return st == 'end' and r <= j, st, w, r
    n = j - 1
    if not T.odd[n]:
        return True, 'end', [j], j
    if T.kind(n) == 'a':
        k = T.tau[n] // 2
        x1 = 6 * k + 2 * delta; th1 = 6 * k + delta + 3; loss = 1
    else:
        lam = T.lam(n); x1 = lam; th1 = 3 * T.tau[n] + 3 + delta; loss = 1 + T.eps[n]
    # The small representative (x1, th1) agrees with every true successor modulo 2^(j-loss):
    # a: x1 differs by 3x/2 (valuation j-1); b/c: by c'(x/2^j) (valuation n-eps = j-loss); Theta mod 2^j.
    # HP with precision j-loss: certified iff the tail ends with relative records < j-loss.
    st, w, r = exact_tail(T, x1, th1, j - loss)
    return st == 'end' and r < j - loss, st, [j] + w, max(j, r + loss)
