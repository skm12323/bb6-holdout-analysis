"""revB2_rule.py -- verify structural rule: D-fire <=> g = dp(j_last)-1;
new shapes in 1501..3000 (j_last=12); j_D constancy per shape."""
import sys, json
from collections import Counter, defaultdict
sys.path.insert(0, r'D:\math_cc\work_r10')
from revB2_phi import phi_trace

recs = []
for f in (r'D:\math_cc\work_r10\revB2_census_5_1500.json',
          r'D:\math_cc\work_r10\revB2_census_1501_3000.json'):
    recs += json.load(open(f))

dp = {}
def D(j):
    if j not in dp:
        dp[j] = phi_trace(j)['re'][1]
    return dp[j]

bad = []
for r in recs:
    if r['g_p'] is None:
        continue
    shouldBeD = (r['g_p'] == D(r['jl_p']) - 1)
    if shouldBeD != r['D']:
        bad.append((r['m'], r['g_p'], r['jl_p'], r['ct'], D(r['jl_p'])))
print('rule "D-fire <=> g = dp(j_last)-1" violations: %d / %d' %
      (len(bad), sum(1 for r in recs if r['g_p'] is not None)))
for b in bad[:10]:
    print('   ', b)

print('\nD-fire shapes over m=5..3000, with j_D distribution:')
byst = defaultdict(list)
for r in recs:
    if r['D']:
        byst[(r['g_p'], r['jl_p'])].append(r)
for k in sorted(byst, key=lambda t: (t[0] is None, t[0] or 0, t[1] or 0)):
    rs = byst[k]
    print('   g=%s jl=%s : n=%d jD %s delta %s  [dp(jl)=%s]' %
          (k[0], k[1], len(rs), dict(sorted(Counter(x['j_D'] for x in rs).items())),
           dict(sorted(Counter(x['delta'] for x in rs).items())),
           D(k[1]) if k[1] else '-'))
print('total D-fire shapes: %d (+ the None/no-sub-fire case)' % len(byst))

# all j_last values occurring anywhere
jls = Counter(r['jl_p'] for r in recs)
print('\nj_last values over m=5..3000:', dict(sorted(jls.items(), key=lambda t: (t[0] is None, t[0] or 0))))

# per-m: j_D <= m-2 recheck across both files; and m where j_D = m-2 exactly
tight = [(r['m'], r['j_D']) for r in recs if r['D'] and r['j_D'] == r['m'] - 2]
print('boundary cases j_D == m-2:', tight)
# Kex vs 2^{m-2}/3 margin (tie never realized numerically?)
worst = max((3 * r['Kex'] + 1).bit_length() - (r['m'] - 2) for r in recs if r['D'])
print('max over m of [log2(3Kex+1) - (m-2)] = %d (negative => 3Kex+1 < 2^{m-2} always)' % worst)
