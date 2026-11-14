"""rwalk_t5.py -- rational-class certificates for LEVEL-T5 (work_gc_level_t5).

Extends the accepted rwalk.py (work_claude_residual, Theorem T4's [B] machinery) to entries whose
class is a rational  num/den  (den odd, gcd(num,den)=1, den = 3^r), optionally with a lift bit at
the chain itself (class = num/den + 2^j mod 2^{j+1}).

Mechanism (identical to rwalk.py = work_claude_shifted Prop 3.2 / HP):
  * j < 64: exact representative (2^j, 2^j + r_j), r_j = num*den^{-1} (+2^j if lift) mod 2^{j+1};
    certified iff the walk ends with every record <= j (ceiling j+1).
  * j >= 64: one-step form with the working truncation  D = num*den^{-1} mod 2^K2  (K2 = 56):
       a  : (x1, th1) = (6k + 2D, 6k + D + 3),   ceiling min(j-1, K2)
       b/c: (x1, th1) = (lam[n], 3tau+3 + D),    ceiling min(j-1-eps, K2)
    The truncation is faithful because the exact first-step output parameter is
    j1 = 1+v2(3*k*den + num)  with |3*k*den+num| <= 3*(j-1)*P(j-1)/2*den + |num| < 2^53
    (CLOCK/C1, den <= 3^9, j < 2*10^7), so every record of the exact walk is <= 53 < K2 and the
    walk from the truncation agrees with the exact representative's walk at every step.
    A lift bit at position j >= 64 is >= 2^64 > 2^{j1+1} and never influences the walk.
Certified(j, num/den(+lift)) => every real state whose defect is == num/den(+2^j) mod 2^{j+1}
follows the same walk (parameters, types, records <= max(j, 53)); the epoch ends (even crossing)
with no tie.  a-outputs along certified walks are recorded (chain, class mod 2^{chain+1}).

bulk_rat: vectorised certify over all jlo <= j < jhi for one (num, den, lift) family.
bulk_rat and certify_rat are cross-checked against each other and against the exact per-j
residues; the integer special case (den=1, lift off) reproduces rwalk.bulk/certify.
"""
import sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
import rwalk as R  # noqa: E402  (accepted T4 machinery; table + certificate)

K2 = 56          # working truncation width; all exact-walk records <= 53 for j < 2e7, den<=3^9
MAXDEN_BITS = 16  # den <= 3^9 = 243*27=6561 needs 13 bits; 16 is a safety cap


def inv2(a, bits):
    """a^{-1} mod 2^bits for odd a."""
    return pow(a, -1, 1 << bits)


def residue(num, den, j, lift=False):
    """exact class residue at chain j: num/den (+2^j) mod 2^{j+1}, in [0, 2^{j+1})."""
    from math import gcd
    if den <= 0 or den % 2 == 0 or gcd(abs(num) if num else den, den) != 1:
        raise ValueError('bad rational class %d/%d' % (num, den))
    M = 1 << (j + 1)
    r = (num * inv2(den, j + 1)) % M
    if lift:
        r = (r + (1 << j)) % M
    return r


def trunc(num, den, bits=K2):
    return (num * inv2(den, bits)) % (1 << bits)


def certify_rat(T, j, num, den, lift=False):
    """certificate of the entry (j, num/den (+lift)).  Returns dict(ok, status, word, aouts, nt)."""
    if den == 1 and not lift:
        return R.certify(T, j, num)
    if j < R.BIG:
        return R.certify(T, j, residue(num, den, j, lift))
    n = j - 1
    t, od, tau, ep, lam = T.row(n)
    if not od:
        return dict(ok=True, status='end', word=[j], aouts=[], nt=[])
    D = trunc(num, den)
    if t == 'a':
        k = tau // 2
        x1 = 6 * k + 2 * D; th1 = 6 * k + D + 3; loss = 1
        first = []
        if x1 != 0:
            j1 = R.v2(x1)
            if j1 >= j:
                return dict(ok=False, status='nt-first', word=[j, j1], aouts=[], nt=[(j, j1)])
            first = [(j1, (th1 - x1) % (1 << (j1 + 1)))]
    else:
        x1 = lam; th1 = 3 * tau + 3 + D; loss = 1 + ep; first = []
    st, w, r, ao, nt = R.tail(T, x1, th1, min(j - loss, K2))
    d = dict(ok=(st == 'end' and r < min(j - loss, K2)), status=st, word=[j] + w,
             aouts=first + ao, nt=nt)
    return d


def bulk_rat(T, num, den, lift=False, jlo=R.BIG, jhi=None, maxit=30):
    """Vectorised certify_rat for one family over jlo <= j < jhi (lift only matters for jlo<64).
    Returns dict(aout, uncert, nt, n_odd) like rwalk.bulk."""
    if jhi is None:
        jhi = T.N + 1
    assert jlo >= R.BIG, 'use certify_rat below 64'
    D = trunc(num, den)
    js = np.arange(jlo, jhi, dtype=np.int64)
    n = js - 1
    od = T.odd[n].astype(bool)
    js = js[od]; n = n[od]
    isa = T.typ[n] == 97
    tau = T.tau[n]
    k = tau // 2
    x = np.where(isa, 6 * k + 2 * D, T.lam[n])
    th = np.where(isa, 6 * k + D + 3, 3 * tau + 3 + D)
    ceil = np.minimum(np.where(isa, js - 1, js - 1 - T.eps[n]), K2)
    G = np.zeros_like(x)
    origin = js.copy()
    aout = {}

    def lowbit_v2(a):
        lb = a & (-a)
        return np.rint(np.log2(lb.astype(np.float64))).astype(np.int64)

    assert np.all(x != 0)
    j1 = lowbit_v2(x)
    # a-type first steps with j1 >= j-1 are NT at entry -> uncertified
    ntat = isa & (j1 >= js - 1)
    uncert = list(origin[ntat].tolist())
    ntc = {}
    for a_, b_ in zip(js[ntat].tolist(), j1[ntat].tolist()):
        ntc[(int(a_), int(b_))] = ntc.get((int(a_), int(b_)), 0) + 1
    alive = ~ntat
    sel = isa & alive
    if sel.any():
        c = j1[sel]
        mod = (np.int64(1) << (c + 1))
        res = np.mod(th[sel] - x[sel], mod)
        keys = np.stack([c, res], axis=1)
        uk, idx, cnt = np.unique(keys, axis=0, return_index=True, return_counts=True)
        o = origin[sel][idx]
        for (cc, rr), oo, nn2 in zip(uk.tolist(), o.tolist(), cnt.tolist()):
            e = aout.setdefault((cc, rr), [0, oo]); e[0] += nn2
    cW64 = np.zeros(62, dtype=np.int64)
    for nn_, cw in T.cW.items():
        if nn_ < 62:
            cW64[nn_] = cw
    for it in range(maxit):
        if not alive.any():
            break
        idxs = np.nonzero(alive)[0]
        xa = x[idxs]
        zero = xa == 0
        if zero.any():
            uncert.extend(origin[idxs[zero]].tolist()); alive[idxs[zero]] = False
            idxs = idxs[~zero]; xa = xa[~zero]
        jj = lowbit_v2(xa)
        assert np.all(jj < 62), 'walk left the small-chain regime'
        rec = jj + G[idxs]
        bad = rec >= ceil[idxs]
        if bad.any():
            uncert.extend(origin[idxs[bad]].tolist()); alive[idxs[bad]] = False
            idxs = idxs[~bad]; jj = jj[~bad]; xa = xa[~bad]
        nn = jj - 1
        assert np.all(nn >= 0) and np.all(nn < T.NS)
        odn = T.odd[nn].astype(bool)
        alive[idxs[~odn]] = False
        idxs = idxs[odn]; jj = jj[odn]; nn = nn[odn]; xa = xa[odn]
        if len(idxs) == 0:
            break
        ta = T.typ[nn] == 97
        tauv = T.tau[nn]
        tha = th[idxs]
        ia = idxs[ta]
        if len(ia):
            x2 = 2 * tha[ta] + 3 * tauv[ta] - (xa[ta] >> 1)
            th2 = tha[ta] + 3 + 3 * tauv[ta]
            nz = x2 != 0
            j2 = np.full(len(x2), -1, dtype=np.int64)
            j2[nz] = lowbit_v2(x2[nz])
            ndm = nz & (j2 >= jj[ta])
            for a_, b_ in zip(jj[ta][ndm].tolist(), j2[ndm].tolist()):
                ntc[(a_, b_)] = ntc.get((a_, b_), 0) + 1
            c = j2[nz]; res = np.mod(th2[nz] - x2[nz], (np.int64(1) << (c + 1)))
            keys = np.stack([c, res], axis=1)
            if len(keys):
                uk, idx, cnt = np.unique(keys, axis=0, return_index=True, return_counts=True)
                o = origin[ia[nz]][idx]
                for (cc, rr), oo, nn2 in zip(uk.tolist(), o.tolist(), cnt.tolist()):
                    e = aout.setdefault((cc, rr), [0, oo]); e[0] += nn2
            x[ia] = x2; th[ia] = th2; G[ia] += 1
        ib = idxs[~ta]
        if len(ib):
            nb = nn[~ta]; jb = jj[~ta]
            assert np.all(nb < 62) and np.all(cW64[nb] != 0)
            u = (xa[~ta] >> jb)
            xn = cW64[nb] * u + T.lam[nb]
            assert np.all(np.abs(u) < (1 << 52)) and np.all(np.abs(xn) < (1 << 62))
            x[ib] = xn; th[ib] = tha[~ta] + 3 + 3 * tauv[~ta]; G[ib] += 1 + T.eps[nb]
    assert not alive.any(), 'maxit'
    return dict(aout=aout, uncert=uncert, nt=ntc, n_odd=int(len(js)))


# ---------------- drift-class arithmetic (classes in Z[1/3^r]) ----------------

def canon(num, den):
    """canonical (num, den) with den = 3^r >= 1, den | num reduced away."""
    if den == 1:
        return (num, 1)
    while den % 3 == 0 and num % 3 == 0:
        num //= 3; den //= 3
    return (num, den)


def add(n1, d1, n2, d2):
    return canon(n1 * d2 + n2 * d1, d1 * d2)


def maps_a(num, den):
    return canon(3 * den - num, den)      # a: theta -> 3 - theta


def maps_b(num, den):
    return canon(num - den, den)          # b: theta -> theta - 1


def maps_c(num, den, s_num, s_den):
    return add(num, den, s_num, s_den)    # c: theta -> theta + s


def sym_rep(num, den, j):
    """symmetric representative of num/den mod 2^{j+1} (small int when |num/den| < 2^j)."""
    r = residue(num, den, j)
    M = 1 << (j + 1)
    return r - M if r > M // 2 else r
