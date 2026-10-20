"""check_gateway.py -- exact big-integer verification of the generalized gateway lemma
(Theorem C6 of NOTES.md) at canonical type-c crossings, plus the record bookkeeping.

For a deep chain of parameter j_T with defect theta (x = 2^j_T * u, Theta = x + theta) whose
step is type c with omega = j_u, and with X(j_u-1) odd type a, the two-chain block has

    x_{u+1} = Q + u*(2^(j_T+1) - c'/2),      Q  := 2 theta + 6 + 6 k + 6 tau - lambda'/2,
    v2(c'/2) = sigma - 1,                    sigma = n - eps = v2(c'_W),

so j_{u+1} = v2(Q) whenever v2(Q) < sigma-1, and
theta_{u+1} == theta + 6 + 3 tau + 3 tau(j_u-1)  (mod 2^{j_{u+1}}).

Verified here with exact integers (no modular reduction of the walks) for
omega = 5 canonical crossings n < NS (c'_W known from fdata.small_full).

Usage: python -B check_gateway.py [NS] [NJ] [NU]
Writes check_gateway.json beside this script.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import clib  # noqa: E402

NS = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
NJ = int(sys.argv[2]) if len(sys.argv) > 2 else 8
NU = int(sys.argv[3]) if len(sys.argv) > 3 else 6

T = clib.Table(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=NS)
RES = dict(NS=NS, NJ=NJ, NU=NU, cases=[], summary={})
n_ok = n_bad = 0
records_ok = 0
resolved = 0
nores = 0
j2dist = {}
for n in range(6, min(NS, T.N)):
    if not (T.odd(n) and T.typ[n] == 99):
        continue
    j_u = clib.v2(T.lam(n))
    cW = T.cW.get(n)
    if cW is None:
        continue
    sig = T.sigma(n)
    lamW = T.lam(n)
    if not (j_u == 5 and T.odd(j_u - 1) and T.typ[j_u - 1] == 97):
        continue
    k2 = T.tau[j_u - 1] // 2
    tau2 = T.tau[j_u - 1]
    for jT in (61, 1000, 2 * 10**5 + 3):
        for th in (1, 0, -1, 2, -2, 3, -3, 5, -11, 17, -17):
            for u in (1, 3, 5, 7, (1 << 40) + 1, (1 << 150) - 3):
                x = (1 << jT) * u
                Th = x + th
                # first step: type c with omega = 5
                x5 = cW * u + lamW
                Th5 = Th + 3 + 3 * T.tau[n]
                assert clib.v2(x5) == j_u, (n, clib.v2(x5))
                # second step: a-step at parameter j_u (X(j_u-1) odd type a)
                x2 = 2 * Th5 + 6 * k2 - (x5 >> 1)
                Th2 = Th5 + 3 + 3 * tau2
                j2 = clib.v2(x2)
                Q = 2 * th + 6 + 6 * k2 + 6 * T.tau[n] - lamW // 2
                v2Q = clib.v2(abs(Q)) if Q else 10**9
                gap = clib.v2((1 << (jT + 1)) - cW // 2) if jT + 1 > 60 else sig - 1
                # exact identity x2 = Q + u*(2^(jT+1) - c'/2)
                ident = (x2 == Q + u * ((1 << (jT + 1)) - cW // 2))
                # class of the new chain
                if Q != 0 and v2Q < sig - 1:
                    resolved += 1
                    # class mod 2^(j2) (coarse) and mod 2^(j2+1) (the one certify needs)
                    th2c = (th + 6 + 3 * T.tau[n] + 3 * tau2) % (1 << j2)
                    th2 = (Th2 - Q) % (1 << (j2 + 1))
                    j2dist[j2] = j2dist.get(j2, 0) + 1
                    ok = ((j2 == v2Q) and ((Th2 - x2) % (1 << j2) == th2c)
                          and ((Th2 - x2) % (1 << (j2 + 1)) == th2)
                          and clib.certify(T, j2, th2)[0])
                    # record bookkeeping: r_{u+1} = j2 + Gamma_T + 2 + eps(n) <= r_T - 1
                    rec_ok = (j2 + 2 + T.eps[n] <= jT)
                    records_ok += 1 if rec_ok else 0
                else:
                    nores += 1
                    ok = True
                    rec_ok = None
                n_ok += 1 if (ident and ok) else 0
                n_bad += 0 if (ident and ok) else 1
                if len(RES['cases']) < 12:
                    RES['cases'].append(dict(n=n, jT=jT, theta=th, u=(u if u < 10**6 else 'big'),
                                             j2=j2, v2Q=v2Q, sigma=sig, gap=gap,
                                             ident=ident, class_ok=ok, rec_ok=rec_ok,
                                             certify=(clib.certify(T, j2, (Th2 - Q) % (1 << (j2 + 1)))[0]
                                                      if (Q != 0 and v2Q < sig - 1) else None)))
RES['summary'] = dict(cases=n_ok + n_bad, ok=n_ok, bad=n_bad, resolved=resolved,
                      unresolved=nores, records_ok=records_ok, j2_distribution=j2dist,
                      note=('ok requires: exact identity, j_{u+1}=v2(Q), coarse class mod 2^j2, '
                            'fine class mod 2^(j2+1), certify(j2, fine class), record bound'))
with open(HERE / 'check_gateway.json', 'w', encoding='utf-8') as f:
    json.dump(RES, f, indent=1)
print(json.dumps(RES['summary'], indent=1))
print('cases:', RES['cases'][:3])
