"""Data checks for the deep segment (task item 5):
 (i)  at every odd type-a crossing n in the table: 3k = 3*tau(n)/2, its minimum, bit length,
      and the no-resonance margin j-2-bitlen(3k) (j=n+1);
 (ii) B+kappa(j) < 2^(j-3) for j>=N0 (bit-length form, table + analytic spot checks);
 (iii) tau(n) >= (n-1)/2 and CLOCK tau(n) <= n*P(n) at every odd crossing;
 (iv) lambda_Y <= 3*tau+1 at odd type-c crossings; omega < n-eps at odd b/c crossings.
Usage: python -B check_data.py <table.pkl> [nsample]
Writes check_data_<basename>.json.
"""
import json, os, pickle, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
import vlib

path = sys.argv[1] if len(sys.argv) > 1 else r'D:\math_cc_astra\deep1\table_20000000.pkl'
NSAMP = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
t0 = time.time()
with open(path, 'rb') as f:
    D = pickle.load(f)
typ, tau, eps, odd, lY, lA = D['typ'], D['tau'], D['eps'], D['odd'], D['lY'], D['lA']
N = len(tau)
print('loaded', N, '%.1fs' % (time.time() - t0), flush=True)

N0 = 2 * 10**7
B = 1 << 10**7
Bbits = B.bit_length()

def P(n):
    g = (6 * n * n + 5).bit_length()  # ceil(log2(6n^2+5)) = bit_length except when a power of 2
    if (1 << (g - 1)) == 6 * n * n + 5:
        g -= 1
    return 2 * g * g + 1345

def kappa(j):
    return (3 * (j - 1) * P(j - 1)) // 2

res = dict(path=os.path.basename(path), N=N, t_load=round(time.time() - t0, 1))
# (ii) analytic/table size inequality: B+kappa(j) < 2^(j-3)  <=> bitlen <= j-3
bad_size = []
min_margin = 10**18
for j in list(range(N0, min(N, N0 + NSAMP))) + [N0 + 10**6, 3 * 10**7, 5 * 10**7,
                                                min(N - 1, 99999999), 10**8, 10**9, 10**12]:
    if j < N0:
        continue
    x = B + kappa(j)
    if x.bit_length() > j - 3:
        bad_size.append((j, x.bit_length()))
    min_margin = min(min_margin, j - 3 - x.bit_length())
res['bad_size'] = bad_size[:5]; res['size_margin_min'] = min_margin
print('size', res['bad_size'][:2], 'min margin', min_margin, flush=True)

# per-index checks
t1 = time.time()
n_a = 0; min3k = None; maxbl = 0; min_margin_a = 10**18
n_bad_tau_lb = 0; n_bad_clock = 0; n_bad_lamY = 0; n_bad_om = 0
first = {}
n_bc = 0; n_c = 0; n_odd = 0
for n in range(N):
    if not odd[n]:
        continue
    n_odd += 1
    ta = tau[n]; ep = eps[n]
    # (iii) tau >= (n-1)/2 and CLOCK
    if 2 * ta < n - 1:
        n_bad_tau_lb += 1
        if 'tau_lb' not in first: first['tau_lb'] = (n, ta)
    if ta > n * P(n):
        n_bad_clock += 1
        if 'clock' not in first: first['clock'] = (n, ta, n * P(n))
    if typ[n] == 97:
        if ep != 0:
            n_bad_lamY += 1
        k = ta // 2
        v = 3 * k
        if min3k is None or v < min3k:
            min3k = v
        bl = v.bit_length()
        if bl > maxbl: maxbl = bl
        j = n + 1
        if j - 2 - bl < min_margin_a:
            min_margin_a = j - 2 - bl
        n_a += 1
    else:
        n_bc += 1
        lam = lA[n] + 2 * lY[n] + 3
        om = vlib.v2(lam)
        if not (om < n - ep):
            n_bad_om += 1
            if 'om' not in first: first['om'] = (n, om, n - ep)
        if typ[n] == 99:
            n_c += 1
            if lY[n] > 3 * ta + 1:
                n_bad_lamY += 1
                if 'lamY' not in first: first['lamY'] = (n, lY[n], 3 * ta + 1)
        elif lam != 3 * ta + 4:
            n_bad_lamY += 1
print('scan %.1fs' % (time.time() - t1), flush=True)
res.update(n_odd=n_odd, n_a=n_a, n_bc=n_bc, n_c=n_c, min3k=min3k, maxbitlen3k=maxbl,
           min_margin_a=min_margin_a, bad_tau_lower=n_bad_tau_lb,
           bad_clock=n_bad_clock, bad_lambda=n_bad_lamY, bad_omega=n_bad_om,
           first_bad=first, t=round(time.time() - t0, 1))
out = r'D:\math_cc\work_r1r2\agent_V\check_data_%s.json' % os.path.basename(path).replace('.pkl', '')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1)[:2000])
print('written', out)
