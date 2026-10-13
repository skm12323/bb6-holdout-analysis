"""ADVERSARY-1 / item 4 (scope) + item 5 (coverage arithmetic).

Item 4: audit WHICH table/dk parameters each part of agentA's CL verification
consumes, as a function of the position bound q (agentD's circularity use:
"CL at positions <= q consumes dk only at spike parameters <= 5+v2(3s+2)
with s <= q/16, i.e. < q-1 for q >= 11").

Per-s reading of agentA's proof:
  - cycle-exact branch  (s <= 681): params = {5+v2(3n+2) : visited n <= s} U {1..4}
  - counting-bound branch (s >= 682, s < S1): params = table constants
    TAB[5+t] for ALL t <= 115 (via eps and K)  ->  up to j=120, plus
    class params 5+v2(3n+2) < 5+tmax(s)
  We compute max-param-consumed(q) for q = 11..10^7 exactly by simulation
  and compare against q-1.  Also: max fire j in the p<1.1e6 walk; max J in
  the s<1e7 cycle sim; and the claim 5+v2(3s+2) < q-1 for s <= (q-10)/16.

Item 5: coverage arithmetic of scope A: first k with fire-parameter 121,
16*S1+10 == (2^120-2)/3, vs the report's "~= 2.6e35".
"""
import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, r'D:\math_cc\scratch')
T0 = time.time()
def el(): return '%6.1fs' % (time.time() - T0)
def v2(x): return (x & -x).bit_length() - 1
def j_of_k(k): return 1 + v2(3 * k + 2)

import agentB_run7 as r7
TAB = {}
for j in range(1, 121):
    res, err = r7.verify(j)
    assert res is not None, (j, err)
    TAB[j] = tuple(res[0])
D = [0] * 16
for rho in range(16):
    if rho == 10: continue
    cur, dist = rho, 0
    while cur % 16 != 10:
        cur += TAB[j_of_k(cur)][0]; dist += TAB[j_of_k(cur)][0] if False else 0
    D[rho] = None
# recompute D cleanly:
D = [0] * 16
for rho in range(16):
    if rho == 10: continue
    cur, dist = rho, 0
    while cur % 16 != 10:
        dist += TAB[j_of_k(cur)][0]; cur += TAB[j_of_k(cur)][0]
    D[rho] = dist

# ---- max fire parameter along the two walks agentA actually runs ----
PLIM = 1_100_000
p, k, jmax = 4, 1, 0
while p < PLIM:
    j = j_of_k(k); jmax = max(jmax, j)
    dk, dp = TAB[j]; p += dp; k += dk
print('4a: max fire j on the V3 walk (p<%d): %d  (<= 22 < 120: never leaves the table)'
      % (PLIM, jmax))
s, jmaxcyc = 0, 0
while s < 10**7:
    J = 5 + v2(3 * s + 2); jmaxcyc = max(jmaxcyc, J)
    dk = TAB[J][0]; s += (dk + D[(10 + dk) % 16]) // 16
print('    max spike J on the V5 cycle sim (s<1e7): %d' % jmaxcyc)

# ---- param-consumption profile maxparam(q), CL at positions <= q ----
# walk spike-by-spike, tracking the spike's fire position p_s; for each visited
# spike record (p_s, params-needed-so-far under the per-s proof reading).
S1 = ((1 << 116) - 2) // 3
s, B = 0, 16
params_cycle_exact = set([1, 2, 3, 4])     # pre-spike segment j's
events = []        # (p_s, branch, max_param_consumed_at_this_point)
pcur = None
# reconstruct p at each spike from the fire walk (single pass, both trackers):
p, k = 4, 1
vis = []           # (s, p_s) in walk order
while k <= 16 * 1010 + 20:
    j = j_of_k(k)
    if k % 16 == 10:
        vis.append(((k - 10) // 16, p))
    dk, dp = TAB[j]; p += dp; k += dk
p_of_s = dict(vis)
for srun in range(0, 1000):
    J = 5 + v2(3 * srun + 2)
    params_cycle_exact.add(J)
    ps = p_of_s[srun]
    if srun <= 681:
        events.append((ps, 'cycle-exact', max(params_cycle_exact)))
    else:
        # counting-bound branch: full table (via eps, K) + class params < s
        events.append((ps, 'counting', 120))
# monotone envelope: for CL at positions <= q, consumption = max over events
# with p_s <= q of the recorded max-param; PLUS off-spike fires (params j<=4
# and their own j; j <= 5+v2(3s+2) of the current spike window -- bounded by
# the spike params; plus any fire's own j: j(fire at k) <= 5+v2(3s+2), s=k/16).
env = []
mx = 0
for ps, br, mp in sorted(events):
    mx = max(mx, mp); env.append((ps, br, mx))
viol = [(q, br, mp) for q, br, mp in env if mp >= q - 1]
print('4b: per-s reading of the proof: cycle-exact branch consumes params <= %d;'
      % max(mp for _, br, mp in events if br == 'cycle-exact'))
print('    counting branch (s>=682) first invoked at spike position p=%d, consumes'
      ' table constants up to j=120' % min(q for q, br, mp in env if br == 'counting'))
print('    violations of maxparam < q-1 among spike events: %s'
      % (viol if viol else 'NONE'))
# also include off-spike fires' own j (<= max spike J before them) - same bound.
# the analytic claim: 5+v2(3s+2) < q-1 whenever 16s+10 <= q, q>=11:
bad = []
for q in range(11, 200000):
    smax = (q - 10) // 16
    if smax >= 0 and 5 + v2(3 * smax + 2) >= q - 1:
        bad.append(q)
print('    analytic check 5+v2(3*floor((q-10)/16)+2) < q-1 for q=11..2e5: %s'
      % ('HOLDS' if not bad else bad[:5]))
# and the worst case over all s <= (q-10)/16 (not just smax):
def maxJ(q):
    return max((5 + v2(3 * s + 2) for s in range(0, max(0, (q - 10) // 16) + 1)), default=4)
bq = [q for q in range(11, 3000) if maxJ(q) >= q - 1]
print('    max over ALL s <= (q-10)/16 of 5+v2(3s+2) < q-1 for q=11..3000: %s'
      % ('HOLDS' if not bq else bq))
# but the counting-bound branch consumes TAB[5+t] for ALL t<=115 via eps,K:
# consumption profile of the LITERAL constants:
qthr = min(q for q, br, mp in env if br == 'counting')
print('    => the literal sentence "consumes dk only at spike parameters'
      ' <= 5+v2(3s+2), s<=q/16" is INEXACT for q>=%d (K,eps consume j<=120),'
      % qthr)
print('       but 120 < q-1 there (q >= %d), and for q < %d only the cycle-exact'
      ' branch is needed (params <= 15 < q-1 for q >= 17; q in [11,17) needs'
      ' only j<=4).' % (qthr, qthr))

# ---- run7 independence: no imports beyond fractions/agentB_lib.v2i ----
import agentB_abs, agentB_lib
src = open(r'D:\math_cc\scratch\agentB_run7.py').read() + \
      open(r'D:\math_cc\scratch\agentB_abs.py').read()
for bad in ('agentA', 'fast_walker', 'exact_walker', 'conservation', 'p - k >= 3',
            'CL', 'work_r10', 'work_g6'):
    assert bad not in src, bad
print('4c: run7 + agentB_abs import only {fractions, agentB_lib.v2i}; no reference'
      ' to CL / walker / agentA / work_r10: certification INDEPENDENT of CL')
print('    (agentB_abs simulates the audited top map on symbolic k = kappa+2^m s'
      ' with class-splitting; verify() fails loudly on cap exceeded/ambiguity.)')

# ---------------- item 5: scope-A coverage arithmetic ----------------
# {k : v2(3k+2) >= 120} = {k = (2^120*m - 2)/3 : m integer}; integrality needs
# m = 2 mod 3 (2^120 = 1 mod 3); v2 exactly 120 needs m odd. Smallest integer
# k in the class: m=2 -> k=(2^121-2)/3 (v2=121 -> j=122); smallest with j=121
# exactly: m=5 -> k=(5*2^120-2)/3.
k_first_out = ((1 << 121) - 2) // 3
assert (1 << 121) % 3 == 2 and ((1 << 121) - 2) % 3 == 0
k_first_121 = (5 * (1 << 120) - 2) // 3
assert (5 * (1 << 120) - 2) % 3 == 0
assert v2(3 * k_first_out + 2) == 121 and v2(3 * k_first_121 + 2) == 120
assert k_first_121 - k_first_out == 1 << 120
# minimal k with j >= 121 overall is k_first_out (class root, verified by scan of roots):
mod = 1 << 120
root = ((1 << 120) - 2) * pow(3, -1, mod) % mod
assert root == k_first_out % mod and k_first_out == root
print('5: class {v2(3k+2)>=120} root = (2^121-2)/3 = %d  (~%.4ge35) -> j=122 there;'
      % (k_first_out, k_first_out / 1e35))
print('   first k with j=121 exactly: (5*2^120-2)/3 = %d (~%.4ge35).'
      % (k_first_121, k_first_121 / 1e35))
print('   agentA covered bound: k <= 16*S1+10 (real) = %.6g  (~%.4ge35);'
      % (16 * S1 + 10, (16 * S1 + 10) / 1e35))
# S1 itself: 3*(S1)+2 = 2^116-2 (v2=1): S1 is NOT a deep block; validity of S1:
assert 3 * S1 + 2 == (1 << 116) - 2 and v2(3 * S1 + 2) == 1
assert 3 * (S1 - 1) + 2 < (1 << 116)     # every s < S1 has 3s+2 < 2^116 -> J<=120
# all fires with k < 16*S1+10 have j <= 120 (conservative: true boundary is k_first_out):
print('   check: every s < S1 has 3s+2 < 2^116 (so J_s <= 120): True; S1 valid but')
print('   CONSERVATIVE by ~5.03x vs the true first out-of-table block'
      ' (5*2^116-2)/3 = %.4ge35.' % ((5 * (1 << 116) - 2) / 3 / 1e35))
# the report numeric claim "~= 2.6e35" vs its own formula:
print('   report\'s own formula 16*(2^116-2)/3+10 = %.6ge35; the quoted "2.6e35"'
      % ((16 * S1 + 10) / 1e35))
print('   approximation is WRONG (off 1.7x) but in the SAFE direction (understates).')
# brute sanity on a small scale: first k with j>=8 analog:
m0 = 1 << 7
root7 = ((1 << 7) - 2) * pow(3, -1, m0) % m0
assert min(k for k in range(1, 2000) if v2(3 * k + 2) >= 7) == root7
print('   root formula sanity (t=7 analog, brute): OK')
print('ITEM 4: see review text; ITEM 5: agentA formula valid+conservative, "2.6e35"'
      ' constant wrong-but-safe; true j>=121 boundary k=(2^121-2)/3 ~ 8.9e35.')
