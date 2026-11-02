"""rwalk.py -- exact representative walks for residual-source classes (Claude, work_claude_residual).

Exact pair-map walks (PROOF_EXT §2; shiftlib.exact_tail of work_claude_shifted) on the canonical table
D:/math_cc_astra/deep1/table_20000000.pkl (fdata.lam_walk, indices n < 2*10^7) plus fdata.small_full for c'_W
at small n.  An *entry* is (j, delta): parameter j, defect class delta mod 2^(j+1).  It is CERTIFIED
(work_claude_shifted Prop 3.2) iff the walk from the representative ends with every record below the trusted
precision; then every real state agreeing mod 2^(j+1) follows the same parameters/types, and (HP) its defect
agrees with the representative's mod 2^(j_t+1) at every later chain t.  So the a-output classes recorded along a
certified representative walk are the real classes of all such states.

  j <  BIG: representative (x, Theta) = (2^j, 2^j + delta), precision j+1          (shiftlib.certify, j < 64)
  j >= BIG: one symbolic step (shiftlib.certify one-step form):
     a  : (x1, Th1) = (6k + 2 delta, 6k + delta + 3), precision j-1
     b/c: (x1, Th1) = (lambda'_W, 3 tau + 3 + delta),  precision j-1-eps
A-OUTPUT = chain produced by an a-step (descent, catapult or NT gate); its class D mod 2^(j'+1) is recorded.
The c shift of a crossing copying that chain is D-2 (mod 2^(j'+1)) [Lemma R0 of NOTES.md].
"""
import sys, pickle, time
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_c'))
from fdata import small_full  # noqa: E402

BIG = 64
TABLE = r'D:/math_cc_astra/deep1/table_20000000.pkl'


def v2(x):
    return (x & -x).bit_length() - 1


class Table:
    def __init__(self, path=TABLE, NS=1100):
        D = pickle.load(open(path, 'rb'))
        self.typ = np.frombuffer(D['typ'], dtype=np.uint8)
        self.odd = np.frombuffer(D['odd'], dtype=np.uint8)
        self.tau = np.frombuffer(D['tau'], dtype=np.int64)
        self.eps = np.frombuffer(D['eps'], dtype=np.int16).astype(np.int64)
        self.lA = np.frombuffer(D['lA'], dtype=np.int64)
        self.lY = np.frombuffer(D['lY'], dtype=np.int64)
        self.N = len(self.tau)
        self.lam = self.lA + 2 * self.lY + 3
        S = small_full(NS)
        self.NS = NS
        self.cW = {}
        for n, r in S.items():
            if r['odd'] and r['typ'] != 'a':
                self.cW[n] = r['x'][0]
                assert r['x'][1] == int(self.lam[n]), ('lambda mismatch', n)
        # python-side small copies
        self.ptyp = [chr(c) for c in self.typ[:NS]]
        self.podd = [int(c) for c in self.odd[:NS]]
        self.ptau = [int(c) for c in self.tau[:NS]]
        self.peps = [int(c) for c in self.eps[:NS]]
        self.plam = [int(c) for c in self.lam[:NS]]

    def row(self, n):
        if n < self.NS:
            return self.ptyp[n], self.podd[n], self.ptau[n], self.peps[n], self.plam[n]
        return chr(self.typ[n]), int(self.odd[n]), int(self.tau[n]), int(self.eps[n]), int(self.lam[n])


def tail(T, x, th, ceil, limit=400):
    """exact walk from (x, th); returns (status, word, record, aouts, nt)
    aouts = list of (chain, class mod 2^(chain+1)) produced by a-steps; nt = list of (j_in, j_out) with j_out >= j_in."""
    G = 0; word = []; rec = -1; aouts = []; nt = []
    for _ in range(limit):
        if x == 0:
            return 'zero', word, rec, aouts, nt
        j = v2(x); word.append(j); rec = max(rec, j + G)
        if j + G >= ceil:
            return 'ceiling', word, rec, aouts, nt
        n = j - 1
        if n >= T.N:
            return 'nodata', word, rec, aouts, nt
        t, od, tau, ep, lam = T.row(n)
        if not od:
            return 'end', word, rec, aouts, nt
        if t == 'a':
            x2 = 2 * th + 3 * tau - (x >> 1)
            th += 3 + 3 * tau; G += 1
            if x2 != 0:
                j2 = v2(x2)
                aouts.append((j2, (th - x2) % (1 << (j2 + 1))))
                if j2 >= j:
                    nt.append((j, j2))
            x = x2
        else:
            if n not in T.cW:
                return 'nodata', word, rec, aouts, nt
            x = T.cW[n] * (x >> j) + lam
            th += 3 + 3 * tau; G += 1 + ep
    return 'limit', word, rec, aouts, nt


def certify(T, j, delta):
    """certificate of entry (j, delta mod 2^(j+1)).  Returns dict(ok, status, word, aouts, nt).
    For an a-type first step the first a-output (j1, 3-delta) is included in aouts."""
    if j < BIG:
        d = delta % (1 << (j + 1))
        st, w, r, ao, nt = tail(T, 1 << j, (1 << j) + d, j + 1)
        return dict(ok=(st == 'end' and r <= j), status=st, word=w, aouts=ao, nt=nt)
    n = j - 1
    t, od, tau, ep, lam = T.row(n)
    if not od:
        return dict(ok=True, status='end', word=[j], aouts=[], nt=[])
    if t == 'a':
        k = tau // 2
        x1 = 6 * k + 2 * delta; th1 = 6 * k + delta + 3; loss = 1
        first = []
        if x1 != 0:
            j1 = v2(x1); first = [(j1, (th1 - x1) % (1 << (j1 + 1)))]
    else:
        x1 = lam; th1 = 3 * tau + 3 + delta; loss = 1 + ep; first = []
    st, w, r, ao, nt = tail(T, x1, th1, j - loss)
    return dict(ok=(st == 'end' and r < j - loss), status=st, word=[j] + w, aouts=first + ao, nt=nt)


def bulk(T, delta, jlo=BIG, jhi=None, maxit=30):
    """Vectorised certify(T, j, delta) for integer delta (|delta| small) and all jlo <= j < jhi.
    Returns dict(aout: {(chain, residue): [count, example_j]}, uncert: list of j, nt: Counter-like dict, n_odd)."""
    if jhi is None:
        jhi = T.N + 1
    js = np.arange(jlo, jhi, dtype=np.int64)
    n = js - 1
    od = T.odd[n].astype(bool)
    js = js[od]; n = n[od]
    isa = T.typ[n] == 97
    tau = T.tau[n]
    k = tau // 2
    x = np.where(isa, 6 * k + 2 * delta, T.lam[n])
    th = np.where(isa, 6 * k + delta + 3, 3 * tau + 3 + delta)
    ceil = np.where(isa, js - 1, js - 1 - T.eps[n])
    G = np.zeros_like(x)
    origin = js.copy()
    aout = {}

    def lowbit_v2(a):
        lb = a & (-a)
        return np.rint(np.log2(lb.astype(np.float64))).astype(np.int64)

    # first a-output of a-type entries
    assert np.all(x != 0)
    j1 = lowbit_v2(x)
    sel = isa
    if sel.any():
        c = j1[sel]; mod = (np.int64(1) << (c + 1))
        res = np.mod(th[sel] - x[sel], mod)
        # aggregate with numpy unique for speed
        keys = np.stack([c, res], axis=1)
        uk, idx, cnt = np.unique(keys, axis=0, return_index=True, return_counts=True)
        o = origin[sel][idx]
        for (cc, rr), oo, nn in zip(uk.tolist(), o.tolist(), cnt.tolist()):
            e = aout.setdefault((cc, rr), [0, oo]); e[0] += nn
    uncert = []; ntc = {}
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
            uncert.extend(origin[idxs[zero]].tolist()); alive[idxs[zero]] = False
            idxs = idxs[~zero]; xa = xa[~zero]
        jj = lowbit_v2(xa)
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
        # a steps
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
            assert np.all(np.abs(u) < (1 << 40)) and np.all(np.abs(xn) < (1 << 62))
            x[ib] = xn; th[ib] = tha[~ta] + 3 + 3 * tauv[~ta]; G[ib] += 1 + T.eps[nb]
    assert not alive.any(), 'maxit'
    return dict(aout=aout, uncert=uncert, nt=ntc, n_odd=int(len(js)))
