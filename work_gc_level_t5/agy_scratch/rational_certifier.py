import sys
from pathlib import Path
import numpy as np

ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table, tail, v2

def lowbit_v2(a):
    lb = a & (-a)
    return np.rint(np.log2(lb.astype(np.float64))).astype(np.int64)

def certify_rational_scalar(T, j, num, den, lift):
    """Exact representative walk for j < 64."""
    mod = 1 << (j + 1)
    inv_den = pow(den, -1, mod)
    delta = (num * inv_den) % mod
    if lift:
        delta = (delta + (1 << j)) % mod
    
    # Representative (x, th) = (2^j, 2^j + delta), ceil = j + 1
    st, w, r, ao, nt = tail(T, 1 << j, (1 << j) + delta, j + 1)
    ok = (st == 'end' and r <= j)
    return dict(ok=ok, status=st, word=w, record=r, aouts=ao, nt=nt)

def bulk_rational(T, num, den, lift=False, jlo=64, jhi=None, maxit=30):
    """Vectorized bulk certification for rational family (num, den, lift) with 56-bit truncation.
    For j >= 64, lift bit (2^j >= 2^64) is 0 mod 2^56, so lift has no effect on lower 56 bits.
    Ceiling is min(j - loss, 56).
    """
    if jhi is None:
        jhi = T.N + 1
    
    mod56 = 1 << 56
    inv_den56 = pow(den, -1, mod56)
    delta56 = (num * inv_den56) % mod56

    js = np.arange(jlo, jhi, dtype=np.int64)
    n = js - 1
    od = T.odd[n].astype(bool)
    js = js[od]
    n = n[od]

    isa = T.typ[n] == 97
    tau = T.tau[n]
    k = tau // 2

    # Step 1:
    x = np.where(isa, 6 * k + 2 * delta56, T.lam[n])
    th = np.where(isa, 6 * k + delta56 + 3, 3 * tau + 3 + delta56)
    loss = np.where(isa, 1, 1 + T.eps[n])
    ceil = np.minimum(js - loss, 56)

    G = np.zeros_like(x)
    origin = js.copy()
    aout = {}

    assert np.all(x != 0)
    j1 = lowbit_v2(x)
    sel = isa
    if sel.any():
        c = j1[sel]
        mod = (np.int64(1) << (c + 1))
        res = np.mod(th[sel] - x[sel], mod)
        keys = np.stack([c, res], axis=1)
        uk, idx, cnt = np.unique(keys, axis=0, return_index=True, return_counts=True)
        o = origin[sel][idx]
        for (cc, rr), oo, nn in zip(uk.tolist(), o.tolist(), cnt.tolist()):
            e = aout.setdefault((cc, rr), [0, oo])
            e[0] += nn

    uncert = []
    alive = np.ones(len(x), dtype=bool)

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
            uncert.extend(origin[idxs[zero]].tolist())
            alive[idxs[zero]] = False
            idxs = idxs[~zero]
            xa = xa[~zero]
        jj = lowbit_v2(xa)
        rec = jj + G[idxs]
        bad = rec >= ceil[idxs]
        if bad.any():
            uncert.extend(origin[idxs[bad]].tolist())
            alive[idxs[bad]] = False
            idxs = idxs[~bad]
            jj = jj[~bad]
            xa = xa[~bad]
        nn = jj - 1
        assert np.all(nn >= 0) and np.all(nn < T.NS)
        odn = T.odd[nn].astype(bool)
        alive[idxs[~odn]] = False
        idxs = idxs[odn]
        jj = jj[odn]
        nn = nn[odn]
        xa = xa[odn]
        if len(idxs) == 0:
            break
        ta = T.typ[nn] == 97
        tauv = T.tau[nn]
        tha = th[idxs]

        # a steps
        ia = idxs[ta]
        if len(ia):
            x2 = 2 * tha[ta] + 3 * tauv[ta] - (xa[ta] >> 1)
            th2 = tha[ta] + 3 + 3 * tauv[ta]
            nz = x2 != 0
            j2 = np.full(len(x2), -1, dtype=np.int64)
            j2[nz] = lowbit_v2(x2[nz])
            c = j2[nz]
            res = np.mod(th2[nz] - x2[nz], (np.int64(1) << (c + 1)))
            keys = np.stack([c, res], axis=1)
            if len(keys):
                uk, idx, cnt = np.unique(keys, axis=0, return_index=True, return_counts=True)
                o = origin[ia[nz]][idx]
                for (cc, rr), oo, nn2 in zip(uk.tolist(), o.tolist(), cnt.tolist()):
                    e = aout.setdefault((cc, rr), [0, oo])
                    e[0] += nn2
            x[ia] = x2
            th[ia] = th2
            G[ia] += 1

        # b/c steps
        ib = idxs[~ta]
        if len(ib):
            nb = nn[~ta]
            jb = jj[~ta]
            assert np.all(nb < 62) and np.all(cW64[nb] != 0)
            u = (xa[~ta] >> jb)
            xn = cW64[nb] * u + T.lam[nb]
            x[ib] = xn
            th[ib] = tha[~ta] + 3 + 3 * tauv[~ta]
            G[ib] += 1 + T.eps[nb]

    assert not alive.any(), 'maxit reached'
    return dict(aout=aout, uncert=uncert, n_odd=int(len(js)))

def certify_family_full(T, num, den, lift=False, jhi=300003):
    """Certify family across all odd chains < jhi."""
    unc_s = []
    # scalar for j < 64
    for j in range(5, 64):
        if T.odd[j - 1]:
            res = certify_rational_scalar(T, j, num, den, lift)
            if not res['ok']:
                unc_s.append([j, res['status'], res['word']])
    
    # bulk for j >= 64
    res_b = bulk_rational(T, num, den, lift, jlo=64, jhi=jhi)
    unc_b = res_b['uncert']
    return dict(unc_s=unc_s, unc_b=unc_b)
