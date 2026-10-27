"""Height-ledger statistics on the canonical table (Claude, 2026-10-27). [B] data, no proof.

Uses the cached lambda-walk table (D:/math_cc_astra/deep1/table_N.pkl, built by fdata.lam_walk).
S1 shift spectrum: for every odd b/c crossing n, the landing shift s(n) = -1-lambda_Y(n) mod 2^(omega+1)
   (Theorem S of work_claude_shift: s = Phi(w)-2), its least-height rational representative C/3^r (r<=4),
   compared with eps(n).
S2 pure b/c trains: next(j) = omega(j-1) while X(j-1) is odd b/c; longest such chains.
S3 class walks from chains j>=19 with small starting classes, using the minimal shift representatives:
   steps, max height, max 3-adic rank, NT gates at chains >=19.
Usage: python -B hl_stats.py N [sample]
"""
import sys, pickle, json, time, random
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
SAMPLE = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
T0 = time.time()
D = pickle.load(open(r'D:/math_cc_astra/deep1/table_%d.pkl' % N, 'rb'))
typ, odd, tau, eps, lY, lA = D['typ'], D['odd'], D['tau'], D['eps'], D['lY'], D['lA']
print('loaded', round(time.time() - T0, 1), flush=True)
def v2(x): return (x & -x).bit_length() - 1
def minrep(res, bits, rmax=4):
    """least-height representative C/3^r of residue res mod 2^bits."""
    M = 1 << bits; best = None
    for r in range(rmax + 1):
        C = (res * 3**r) % M
        if C > M // 2: C -= M
        h = abs(F(C, 3**r))
        if best is None or h < best[0]: best = (h, F(C, 3**r), r)
    return best
# ---- S1
shift = {}          # n -> (omega, s as Fraction)
s1 = Counter(); viol = []; hist = Counter(); eps_c = Counter()
for n in range(4, N):
    if not odd[n] or typ[n] == 97: continue
    lam = lA[n] + 2*lY[n] + 3; om = v2(lam); e = eps[n]
    if typ[n] == 98:
        assert lY[n] == 0
        shift[n] = (om, F(-1)); s1['b'] += 1; continue
    s1['c'] += 1; eps_c[e] += 1
    h, rep, r = minrep(-1 - lY[n], om + 1)
    shift[n] = (om, rep)
    if om >= 8:
        s1['c_om>=8'] += 1; hist[(r, float(h))] += 1
        bound = F(e - 1, 2) + F(1, 2)
        if h > bound:
            s1['c_height>(eps-1)/2+1/2'] += 1
            if len(viol) < 20: viol.append(dict(n=n, omega=om, eps=e, rep=str(rep), r=r))
print('S1', dict(s1), round(time.time() - T0, 1), flush=True)
# ---- S2
nxt = {}
for n, (om, s) in shift.items(): nxt[n + 1] = om
L = {}
def train(j):
    path = []
    while j in nxt and j not in L:
        path.append(j); j = nxt[j]
    base = L.get(j, 0)
    for q in reversed(path):
        base += 1; L[q] = base
    return
for j in list(nxt): train(j)
maxL = max(L.values()) if L else 0
longest = sorted(((v, j) for j, v in L.items()), reverse=True)[:10]
def chainof(j):
    out = [j]
    while j in nxt: j = nxt[j]; out.append(j)
    return out
s2 = dict(max_train=maxL, dist=dict(sorted(Counter(L.values()).items())),
          longest=[dict(len=v, chain=chainof(j)) for v, j in longest])
print('S2', s2['max_train'], s2['dist'], round(time.time() - T0, 1), flush=True)
# ---- S3
def walk(j, th):
    steps = 0; maxh = abs(th); maxr = 0; nt19 = 0; cat = 0; path = [j]
    while j >= 5 and steps < 400:
        n = j - 1
        if not odd[n]: break
        if typ[n] == 97:
            k = tau[n] // 2; Q = th.denominator; C = th.numerator
            t = 3*Q*k + C
            v = v2(t) if t != 0 else 10**9
            if v + 1 <= j - 2: j2 = v + 1; th = 3 - th
            elif v + 1 == j - 1:
                if j >= 19: nt19 += 1
                break                                   # NT gate: output not class-determined
            else: j2 = j - 1; th = 3 - th; cat += 1     # catapult (lift bit dropped mod 2^(j-1))
        else:
            om, s = shift[n]; j2 = om; th = th + s
        steps += 1; j = j2; path.append(j)
        maxh = max(maxh, abs(th)); r = 0; q = th.denominator
        while q % 3 == 0: q //= 3; r += 1
        maxr = max(maxr, r)
    return steps, maxh, maxr, nt19, cat, path
rnd = random.Random(20261027)
starts = [F(t) for t in range(-3, 5)] + [F(10, 3), F(26, 3), F(4, 3), F(-2, 3)]
s3 = Counter(); worst_h = (0, None); worst_steps = (0, None); ntex = []
js = list(range(19, min(N, 20000))) + [rnd.randrange(20000, N) for _ in range(SAMPLE)]
for j in js:
    for th in starts:
        st, mh, mr, nt, cat, path = walk(j, th)
        s3['walks'] += 1; s3['cat'] += cat
        if nt:
            s3['NT_at_ge19'] += 1
            if len(ntex) < 10: ntex.append(dict(j=j, theta=str(th), path=path))
        if mh > worst_h[0]: worst_h = (mh, dict(j=j, theta=str(th), path=path))
        if st > worst_steps[0]: worst_steps = (st, dict(j=j, theta=str(th), path=path))
        s3['maxr=%d' % mr] += 1
print('S3', dict(s3), float(worst_h[0]), worst_steps[0], round(time.time() - T0, 1), flush=True)
out = dict(N=N, sample=SAMPLE,
           S1=dict(counts=dict(s1), eps_c_dist=dict(sorted(eps_c.items())),
                   minrep_hist_omega_ge8={'r=%d,h=%s' % k: v for k, v in sorted(hist.items())},
                   violations=viol),
           S2=s2,
           S3=dict(counts=dict(s3), worst_height=[str(worst_h[0]), worst_h[1]],
                   worst_steps=[worst_steps[0], worst_steps[1]], NT_examples=ntex),
           seconds=round(time.time() - T0, 1),
           scope='[B] canonical table n<N; S3 class walks use least-height shift representatives (a model of Theorem S), not exact walks.')
HERE.joinpath('hl_stats_%d.json' % N).write_text(json.dumps(out, indent=1, default=str), encoding='utf-8')
