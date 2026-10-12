"""agentF_run1.py -- ell(s) for s = 1..N, ratios, timing/scale check."""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_lib import F_, excursion

N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
eng = F_(use_cache=True)
t0 = time.time()
ells = {}
for v in range(1, N + 1):
    ells[v] = excursion(v, eng)
dt = time.time() - t0
known = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]
assert [ells[v] for v in range(1, 21)] == known, [ells[v] for v in range(1, 21)]
print('N=%d  time=%.1fs  cache_uses=%d' % (N, dt, __import__('agentF_lib').STATS['cache_uses']))
best = max((ells[v] / v, v) for v in range(1, N + 1))
print('max ell(s)/s = %.4f at s=%d' % best)
viol2 = [v for v in range(1, N + 1) if ells[v] > 2 * v]
viol11 = [v for v in range(1, N + 1) if ells[v] > 1.1 * v]
print('violations of <=2s:', viol10 if (viol10 := viol2) else 'none')
print('violations of <=1.1s (s>=10):', [v for v in viol11 if v >= 10] or 'none')
# top-15 ratios
top = sorted(((ells[v] / v, v) for v in range(1, N + 1)), reverse=True)[:15]
print('top ratios:', [('s=%d' % v, '%.4f' % r) for r, v in top])
