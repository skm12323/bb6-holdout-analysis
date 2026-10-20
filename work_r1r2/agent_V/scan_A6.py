"""A6: certify(m, (D-2^m)/3 mod 2^(m+1)) for D=10 and D=26, all 5 <= m < M.

Own implementation.  For m<64 (and small m where the exact class is cheap) the literal slow
certificate is used.  For m>=64 the first step is evaluated at the truncation level K=192:
  - even crossing: certificate true (walk ends after chain 0);
  - type a: x1 = 3*2^(m-1)+2*delta+6k = (2*delta+6k) mod 2^K, j1=v2(x1); if j1<=4 the chain
    terminates; if j1>=6 the theta-walk from (j1, 3-delta) is independent of m,k and is checked
    NT-good on a precomputed table (Theorem SC then bounds records by j1 < m); j1=5 is the
    (5,-11)/(5,5) bare tie and is resolved by a truncated exact walk;
  - type b/c: x1=lam' mod 2^K, theta1=3*tau+3+delta; the truncated exact walk is run with
    ceiling m-1-eps (HP precision available from x).  It is exact while parameters < K.
A case where a parameter reaches K (or x=0, or the walk never ends) is reported as a failure
(not silently accepted).

Usage: python -B scan_A6.py [M] [K]
Writes scan_A6_<M>.json beside the script.
"""
import json, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
import vlib

M = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10**7
K = int(sys.argv[2]) if len(sys.argv) > 2 else 192
TABLE = (r'D:\math_cc_astra\deep1\table_100000000.pkl' if M > 20000000 else
         r'D:\math_cc_astra\deep1\table_20000000.pkl' if M > 1000000 else
         r'D:\math_cc_astra\deep1\table_1000000.pkl')

t0 = time.time()
T = vlib.Tab(TABLE, NS=1024)
typ, tau, eps, odd, lY, lA = T.typ, T.tau, T.eps, T.odd, T.lY, T.lA
lamarr = [0] * min(M, 64)
print('loaded', TABLE, 'N', T.N, '%.1fs' % (time.time() - t0), flush=True)

MASK_K = (1 << K) - 1
INV3 = pow(3, -1, 1 << K)

def trunc_walk(x, th, j, ceiling, limit=200):
    """Exact walk on truncated representatives; exact while every parameter < K.
    Returns (ok, status, maxrec, maxj)."""
    G = 0; rec = -1; maxj = 0
    for _ in range(limit):
        if x & MASK_K == 0:
            return False, 'zero', rec, maxj
        jj = vlib.v2(x & MASK_K)
        if jj >= K - 1:
            return False, 'overflow', rec, maxj
        maxj = max(maxj, jj)
        rec = max(rec, jj + G)
        if jj + G >= ceiling:
            return False, 'ceiling', rec, maxj
        n = jj - 1
        if n < 0 or not odd[n]:
            return True, 'end', rec, maxj
        t_ = tau[n]
        if typ[n] == 97:
            x = (2 * th + 3 * t_ - (x >> 1)) & MASK_K
        else:
            if n >= T.NS:
                return False, 'nodata', rec, maxj
            x = (T.cW[n] * (x >> jj) + T.lam(n)) & MASK_K
        th = (th + 3 + 3 * t_) & MASK_K
        G += 1 + eps[n]
    return False, 'limit', rec, maxj

# precompute the a-family theta walks for j1>=6: d = -c/3 mod 2^j1
good = {}
for c in (1, 17):
    for j1 in range(5, 60):
        d = (-c * pow(3, -1, 1 << j1)) % (1 << j1)
        d = vlib.symres(d, j1)
        _, st = vlib.theta_walk(T, j1, d, limit=300)
        good[(c, j1)] = (st == 'end')

fails = []
counts = {'even': 0, 'a_term': 0, 'a_sc': 0, 'a_tie5': 0, 'bc': 0, 'bc_ceiling': 0,
          'bc_end': 0, 'small': 0}
maxrec_bc = 0; maxj_bc = 0
minP = 10**18

for m in range(5, M):
    n = m - 1
    for D, c in ((10, 1), (26, 17)):
        if m < 64:
            d = ((D - (1 << m)) * pow(3, -1, 1 << (m + 1))) % (1 << (m + 1))
            d = vlib.symres(d, m + 1)
            ok, st, w, r = vlib.certify_slow(T, m, d)
            counts['small'] += 1
            if not ok:
                fails.append(('slow', m, D, st, w[:8], r))
            continue
        if not odd[n]:
            counts['even'] += 1
            continue
        t_ = tau[n]
        if m <= K + 1:
            dlow = ((D - (1 << m)) * pow(3, -1, 1 << (m + 1))) % (1 << (m + 1))
            dlow = vlib.symres(dlow, m + 1)
        else:
            dlow = (D * INV3) & MASK_K
        if typ[n] == 97:
            k = t_ >> 1
            x1 = 2 * dlow + 6 * k
            if m <= K + 1:
                x1 += 3 << (m - 1)
            if x1 & MASK_K == 0:
                fails.append(('a_x1_zero', m, D)); continue
            j1 = vlib.v2(x1 & MASK_K)
            if j1 <= 4:
                counts['a_term'] += 1
                continue
            if j1 == 5:
                counts['a_tie5'] += 1
                th1 = (dlow + 3 + 6 * k) & MASK_K
                ok, st, rec, mj = trunc_walk(x1, th1, 5, m - 1)
                if not ok:
                    fails.append(('a_tie5', m, D, st, rec, mj))
                continue
            if good[(c, j1)] and j1 < m - 1:
                counts['a_sc'] += 1
                continue
            fails.append(('a_unexpected', m, D, j1, good[(c, j1)]))
        else:
            j1 = vlib.v2(lA[n] + 2 * lY[n] + 3)
            P = m - 1 - eps[n]
            minP = min(minP, P)
            th1 = (dlow + 3 + 3 * t_) & MASK_K
            ok, st, rec, mj = trunc_walk(lA[n] + 2 * lY[n] + 3, th1, j1, P)
            counts['bc'] += 1
            if ok:
                counts['bc_end'] += 1
                maxrec_bc = max(maxrec_bc, rec); maxj_bc = max(maxj_bc, mj)
            else:
                counts['bc_ceiling'] += 1
                fails.append(('bc', m, D, st, rec, mj, P, j1))
        if len(fails) > 50:
            break
    if len(fails) > 50:
        print('too many failures, stopping at m', m, flush=True)
        break

out = dict(M=M, K=K, counts=counts, fails=fails[:50], nfail=len(fails),
           maxrec_bc=maxrec_bc, maxj_bc=maxj_bc, minP=minP,
           t=round(time.time() - t0, 1),
           good_all_6_59=all(good[(c, j)] for c in (1, 17) for j in range(6, 60)))
with open(r'D:\math_cc\work_r1r2\agent_V\scan_A6_%d.json' % M, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1)[:4000])
