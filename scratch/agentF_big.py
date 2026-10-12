"""agentF_big.py -- ell(s) for s = 1..N (default 5000), ratio analysis,
stratified direct-run cross-validation, endgame statistics."""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_fast import FastEll, direct_ell, naive_ell

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
fe = FastEll()
fe.a0.update({1: 1, 2: 0, 3: 1, 4: 0, 5: 2, 6: 1, 7: 0, 8: 2})
t0 = time.time()
for s in range(1, N + 1):
    fe.ell_of(s)
print('computed ell(1..%d) in %.1fs' % (N, time.time() - t0))
ells = fe.ell

# ratio analysis
best = max((ells[s] / s, s) for s in range(1, N + 1))
print('max ell(s)/s = %.6f at s = %d (ell=%d)' % (best[0], best[1], ells[best[1]]))
v2 = [s for s in range(1, N + 1) if ells[s] > 2 * s]
v11 = [s for s in range(1, N + 1) if ells[s] > 1.1 * s]
v108 = [s for s in range(1, N + 1) if ells[s] > 1.08 * s]
print('ell(s) > 2s   :', v2 or 'none')
print('ell(s) > 1.1s :', v11 or 'none')
print('ell(s) > 1.08s:', v108 or 'none')
top = sorted(((ells[s] / s, s) for s in range(1, N + 1)), reverse=True)[:20]
print('top 20 ratios:', [('s=%d' % s, '%.4f' % r) for r, s in top])
# where the max for s>=10 sits
best10 = max((ells[s] / s, s) for s in range(10, N + 1))
print('max ratio for s>=10: %.6f at s=%d' % best10)

# endgame stats
print('max endgame length over all frames executed: %d' % fe.endmax)

# stratified direct cross-checks (full symbolic T_list runs)
import random
random.seed(12345)
sample = sorted(set(list(range(41, 200, 13)) + list(range(200, N + 1, 173)) +
                    [best[1], best10[1], N, N - 1, N - 2]))
bad = []
t0 = time.time()
for s in sample:
    if ells[s] != direct_ell(s):
        bad.append(s)
print('direct cross-check on %d sampled s in [41,%d]: %s [%.0fs]'
      % (len(sample), N, bad or 'ALL OK', time.time() - t0))
# naive cross-checks on a mid-range sample
bad2 = []
for s in sorted(set(list(range(301, 600, 37)) + [777, 1000, 1333])):
    if ells[s] != naive_ell(s):
        bad2.append(s)
print('naive cross-check sample (301..1333):', bad2 or 'ALL OK')

# save table fragment for the report
import json
with open(r'D:\math_cc\scratch\agentF_ell_table.json', 'w') as f:
    json.dump({str(s): ells[s] for s in range(1, N + 1)}, f)
print('table saved. ell(1..30) =', [ells[s] for s in range(1, 31)])
