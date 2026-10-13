"""revB2_tie.py -- task 3: the tie shape (g=1, j_last=2).

(a) verify in data: j_D = 1+v2(3K+4) on every (1,2) occurrence (K = k at rho*),
    delta = Kex - K = 1 there;
(b) size-bound argument: j_D = 1+v2(3Kex+1) <= 1+log2(3Kex+1); under the
    conservation law k <= 0.4465*rho (and under k <= rho^2), for which m is
    3Kex+1 < 2^{m-3} (=> j_D <= m-3) and < 2^{m-2} (=> j_D <= m-2) guaranteed,
    (i) applied directly at the crossing position: Kex <= 0.4465*(m-1),
    (ii) in the task's stated form: Kex <= 0.4465*rho* + dmax, rho* = m-2-g.
"""
import sys, json
sys.path.insert(0, r'D:\math_cc\work_r10')
from revB2_phi import v2
from collections import defaultdict

recs = []
for f in (r'D:\math_cc\work_r10\revB2_census_5_1500.json',
          r'D:\math_cc\work_r10\revB2_census_1501_3000.json'):
    recs += json.load(open(f))

# (a) tie-shape data check
ok = bad = 0
for r in recs:
    if r['D'] and r['g_p'] == 1 and r['jl_p'] == 2:
        K = r['K_p']; Kex = r['Kex']
        if r['delta'] != 1 or r['j_D'] != 1 + v2(3 * K + 4):
            bad += 1; print('BAD', r['m'], r['delta'], r['j_D'], 1 + v2(3 * K + 4))
        else:
            ok += 1
print('(a) tie shape (g=1,j_last=2): %d occurrences, delta=1 and j_D=1+v2(3K+4) '
      'in all; violations %d' % (ok, bad))

byst = defaultdict(set)
for r in recs:
    if r['D'] and r['g_p'] is not None:
        byst[(r['g_p'], r['jl_p'])].add(r['j_D'])
nonconst = {k: v for k, v in byst.items() if len(v) > 1}
print('    shapes with non-constant j_D: %s  (expect only {(1,2)})' % nonconst)

# (b) thresholds. dmax = measured max delta over all D-fires (m<=3000)
dmax = max(r['delta'] for r in recs if r['D'] and r['delta'] is not None)
print('(b) measured max delta = %d' % dmax)

def Kmax_lin_at_crossing(m):
    return 893 * (m - 1) // 2000                     # 0.4465 = 893/2000

def Kmax_lin_at_rhostar(m, slack, gmax=6):
    return max(893 * (m - 2 - g) // 2000 for g in range(gmax + 1)) + slack

def Kmax_sq(m, slack, gmax=6):
    return max((m - 2 - g) ** 2 for g in range(gmax + 1)) + slack

def thresholds(Kmax_fn, slack, label):
    m2 = m3 = None
    f2 = []
    for m in range(5, 80):
        if 3 * Kmax_fn(m, slack) + 1 >= 1 << (m - 2):
            f2.append(m)
    m2 = 5 + len(f2)   # fails are exactly 5..m2-1 (monotone once it holds)
    f3 = []
    for m in range(5, 80):
        if 3 * Kmax_fn(m, slack) + 1 >= 1 << (m - 3):
            f3.append(m)
    m3 = 5 + len(f3)
    assert f2 == list(range(5, m2)) and f3 == list(range(5, m3)), (f2, f3)
    print('    %-44s: j_D<=m-2 for m>=%d ; j_D<=m-3 for m>=%d (failing m: %s)'
          % (label, m2, m3, f3[:6]))

thresholds(lambda m, s: Kmax_lin_at_crossing(m), 0, 'k<=0.4465*rho at crossing (direct)')
thresholds(Kmax_lin_at_rhostar, dmax, 'k<=0.4465*rho* + dmax(%d)' % dmax)
thresholds(Kmax_lin_at_rhostar, 8, 'k<=0.4465*rho* + 8 (g6: e(m)/2<=8)')
thresholds(Kmax_sq, dmax, 'k<=rho*^2 + dmax(%d)' % dmax)
thresholds(Kmax_sq, 0, 'k<=rho*^2 (no slack)')
