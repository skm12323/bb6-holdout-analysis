"""revB2_shapes.py -- per-shape stats from the census JSON + dp(j) table.

For every D-fire shape (g, j_last): j_D statistics, delta stats, j_D formula form.
Also: the 'any'-def census (last b-run fire regardless of c) and the dp(j)
transition-table entries used in the g <= dp(j_last) bound.
"""
import sys, json
from collections import Counter, defaultdict
sys.path.insert(0, r'D:\math_cc\work_r10')
from revB2_phi import phi_trace, v2

recs = json.load(open(r'D:\math_cc\work_r10\revB2_census_5_1500.json'))

# ---- 'any'-def census ----
ca = Counter((r['g_a'], r['jl_a']) for r in recs)
print("'any'-def (g,j_last) census: %d distinct" % len(ca))
for k in sorted(ca, key=lambda t: (t[0] is None, t[0] or 0, t[1] or 0)):
    print('   g=%s jl=%s : %d' % (k[0], k[1], ca[k]))

# ---- per D-fire shape: j_D stats ----
print('\n--- D-fire shapes: (g,j_last) -> count, j_D values, formula 1+v2(3Kex+1) values ---')
byst = defaultdict(list)
for r in recs:
    if r['D']:
        byst[(r['g_p'], r['jl_p'])].append(r)
for k in sorted(byst, key=lambda t: (t[0] is None, t[0] or 0, t[1] or 0)):
    rs = byst[k]
    jds = Counter(r['j_D'] for r in rs)
    frms = Counter(r['form'] for r in rs)
    dls = Counter(r['delta'] for r in rs)
    ties = sum(1 for r in rs if r['formula_ok'] is None)
    ok = all(r['formula_ok'] is not False and r['jd_le_m2'] and r['xok'] for r in rs)
    print('   g=%s jl=%s : n=%d jD dist %s form dist %s delta %s ties %d all-ok %s'
          % (k[0], k[1], len(rs), dict(sorted(jds.items())),
             dict(sorted(frms.items())), dict(sorted(dls.items())), ties, ok))

# ---- mixed / eY / eclean shapes: exit lengths ----
print('\n--- non-D-fire shapes: cross_type, (g,j_last) -> count, e_re dist, dk_re max ---')
byst2 = defaultdict(list)
for r in recs:
    if not r['D']:
        byst2[(r['ct'], r['g_p'], r['jl_p'])].append(r)
for k in sorted(byst2, key=lambda t: (t[0], t[1] is None, t[1] or 0, t[2] or 0)):
    rs = byst2[k]
    print('   %s g=%s jl=%s : n=%d e_re %s maxdk %s maxMj %s maxdj %s' %
          (k[0], k[1], k[2], len(rs), dict(sorted(Counter(r['e_re'] for r in rs).items())),
           max(r['dk_re'] for r in rs),
           max([r['Mmax'] or 0 for r in rs]),
           max([max(r['d_js']) if r['d_js'] else 0 for r in rs])))

# ---- dp table: dp(j) = re-entry tail index e for class j (Prop-1 gap) ----
print('\n--- dp(j), dk(j) transition table for j = 1..12 and the spike j values seen ---')
seen_jl = sorted({r['jl_p'] for r in recs if r['jl_p'] is not None})
for j in sorted(set(list(range(1, 13)) + seen_jl)):
    dk, e, s = phi_trace(j)['re']
    print('   j=%2d : dp=e=%d dk=%d' % (j, e, dk))

# ---- does g <= dp(j_last) - ? hold; max g per jl vs dp ----
print('\n--- max observed g per j_last vs dp(j_last) ---')
dp = {}
for j in sorted(set(list(range(1, 13)) + seen_jl)):
    dp[j] = phi_trace(j)['re'][1]
mx = defaultdict(int)
for r in recs:
    if r['g_p'] is not None:
        mx[r['jl_p']] = max(mx[r['jl_p']], r['g_p'])
for jl in sorted(mx):
    print('   jl=%2d : max g = %d, dp = %d, g<dp: %s' %
          (jl, mx[jl], dp[jl], mx[jl] < dp[jl]))
