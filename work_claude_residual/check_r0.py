"""check_r0.py -- [B] checks of Lemma R0 (shift = source class - 2 = clock residue) on the canonical table.

(1) every odd b/c crossing n < 2*10^7: s(n) := -1-lambda_Y(n) == 3 tau(n) + 3 + 2^omega  (mod 2^(omega+1)).
(2) every odd c crossing n < NMAX: its source epoch (latest odd type-a crossing rho < n, label J = 1+v2(3k+2),
    k = tau(rho)/2) has, in its kernel S(J) (rwalk.certify(J,1), the exact beta walk), an a-output at chain
    omega(n) with class D == s(n)+2 (mod 2^(omega+1)), and tau(n) - tau(rho) equals the clock sum d of that
    a-output chain (d = number of chains + sum of tau over the input chains, PROOF_EXT Lemma BR).
Writes r0_checks.json.  Usage: python -B check_r0.py [NMAX]
"""
import sys, json, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rwalk as R
import numpy as np

T0 = time.time()
T = R.Table()
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else T.N
# (1) vectorised identity on all odd b/c crossings
n = np.arange(4, T.N)
m = (T.odd[n] == 1) & (T.typ[n] != 97)
n = n[m]
lam = T.lam[n]; om = np.rint(np.log2((lam & -lam).astype(np.float64))).astype(np.int64)
assert np.all(lam % (np.int64(1) << om) == 0) and np.all((lam >> om) % 2 == 1)
mod = np.int64(1) << (om + 1)
lhs = np.mod(-1 - T.lY[n], mod)
rhs = np.mod(3 * T.tau[n] + 3 + (np.int64(1) << om), mod)
bad1 = int(np.sum(lhs != rhs))
nb = int(np.sum(T.typ[n] == 98)); nc = int(np.sum(T.typ[n] == 99))
print('(1) b', nb, 'c', nc, 'bad', bad1, round(time.time() - T0, 1), flush=True)


def kernel(J):
    """exact beta walk of S(J): list of (chain, class mod 2^(chain+1), clock sum d) for a-outputs."""
    j = J; d = 0; beta = 0; G = 0; out = []
    while True:
        nn = j - 1
        t, od, tau, ep, lm = T.row(nn)
        if not od:
            return out
        if t == 'a':
            B = 6 * d + 2 + 3 * tau - (beta >> 1)
        else:
            B = lm if beta == 0 else (beta >> j) * T.cW[nn] + lm
        d += 1 + tau; G += 1 + ep
        j = R.v2(B); beta = B
        assert j + G < J, ('tie', J)
        if t == 'a':
            out.append((j, (3 * d + 1 - beta) % (1 << (j + 1)), d))


# (2) source-kernel link for c crossings
lastA = -1; ok = 0; bad = []; kcache = {}
typ = T.typ; odd = T.odd
for q in range(4, NMAX):
    if odd[q] and typ[q] == 97:
        lastA = q
        continue
    if not (odd[q] and typ[q] == 99):
        continue
    k = int(T.tau[lastA]) // 2
    J = 1 + R.v2(3 * k + 2)
    if J not in kcache:
        kcache[J] = kernel(J)
    lamq = int(T.lam[q]); w = R.v2(lamq); s = (-1 - int(T.lY[q])) % (1 << (w + 1))
    dt = int(T.tau[q]) - int(T.tau[lastA])
    hit = [a for a in kcache[J] if a[0] == w and (a[1] - 2 - s) % (1 << (w + 1)) == 0 and a[2] == dt]
    if hit:
        ok += 1
    elif len(bad) < 20:
        bad.append(dict(n=q, rho=lastA, J=J, omega=w, s=s, dt=dt, kernel=kcache[J]))
print('(2) c crossings checked', ok, 'unmatched', len(bad), round(time.time() - T0, 1), flush=True)
out = dict(identity_bc=dict(b=nb, c=nc, bad=bad1), source_link=dict(nmax=NMAX, matched=ok, unmatched=bad,
           labels=sorted(kcache)), seconds=round(time.time() - T0, 1),
           status='PASS' if bad1 == 0 and not bad else 'FAIL')
HERE.joinpath('r0_checks.json').write_text(json.dumps(out, indent=1, default=str) + '\n', encoding='utf-8')
print(out['status'])
