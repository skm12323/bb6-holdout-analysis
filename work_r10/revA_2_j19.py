"""ADVERSARY-1 / item 2: concretely exhibit the J=19 obstruction.

(2a) first block s with v2(3s+2) = 14 (claimed 27306), by formula and scan.
(2b) fire-level walk with the run7-certified table up to that spike:
     report B = Phi just before, drop = dk-dp, V = B-drop, net via the walk
     to the NEXT spike; verify drop=6 > net=5 and B_next = B + 5 exactly.
(2c) per-class per-cycle (net, dp_total) minima over the walk; where the
     naive 'net >= +6, dp_total >= 22' first fails; the report's structural
     claims about J >= 23 (2*drop > g), net < 0 from J=28, empty walks at
     J=35..37, first block-skippers J=38..41, J=120 numbers.
Everything recomputed from scratch (own D/G tables, own B0).
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

# own walk tables D/G from first principles (no trust in agentA's json):
D = [0] * 16; G = [0] * 16
for rho in range(16):
    if rho == 10:
        continue
    cur, dist, gain = rho, 0, 0
    while cur % 16 != 10:
        j = j_of_k(cur); dk, dp = TAB[j]
        dist += dk; gain += dp - dk; cur += dk
    D[rho], G[rho] = dist, gain
# B0 via the pre-spike segment k=1 -> 10:
k, Phi = 1, 3
while k % 16 != 10:
    j = j_of_k(k); dk, dp = TAB[j]; Phi += dp - dk; k += dk
B0 = Phi
assert k == 10 and B0 == 16, (k, B0)
print('2-prep [%s] own D=%s' % (el(), D))
print('        own G=%s  B0=%d' % (G, B0))

# ---------------- 2a: first block with t = 14 ----------------
s_first = min(s for s in range(1 << 15) if v2(3 * s + 2) == 14)
print('2a: first s with v2(3s+2)=14: %d  (claimed 27306)  k=%d' %
      (s_first, 16 * s_first + 10))
assert s_first == 27306

# ---------------- 2b: fire-level walk to past that spike ----------------
PLIM = 1_200_000
p, k = 4, 1
spikes = []          # (s, B, J, V, p_at_spike)
prev = None          # (s, net_so_far_marker)
cur_target = None
while p < PLIM:
    j = j_of_k(k)
    dk, dp = TAB[j]
    if k % 16 == 10:
        s = (k - 10) // 16
        B = p - k
        V = B + dp - dk
        spikes.append((s, B, j, V, p))
    p += dp; k += dk
print('2b [%s]: walk to p<%d: %d spikes, s_max=%d' % (el(), PLIM, len(spikes), spikes[-1][0]))
ev = [x for x in spikes if x[2] == 19]
assert ev, 'no J=19 spike in range'
s0, B0at, J, V0, p0 = ev[0]
assert s0 == s_first, (s0, s_first)
# net: from this spike to the next spike
nxt = [x for x in spikes if x[0] > s0][0]
net_actual = nxt[1] - B0at
rho = (10 + TAB[19][0]) % 16
net_struct = TAB[19][1] - TAB[19][0] + G[rho]
drop = TAB[19][0] - TAB[19][1]
dp_tot = TAB[19][1] + (G[rho] + D[rho])
print('    FIRST J=19 SPIKE: s=%d  k=%d  p=%d (~%.3g)  B=%d  V=%d' %
      (s0, 16 * s0 + 10, p0, float(p0), B0at, V0))
print('    drop = dk-dp = %d-%d = %d ; net = %d (structural) = %d (actual B_next-B) ;'
      ' dp_total = %d' % (TAB[19][0], TAB[19][1], drop, net_struct, net_actual, dp_tot))
assert drop == 6 and net_struct == net_actual == 5 and dp_tot == 21
assert drop > net_struct
print('    ==> DROP 6 > NET 5 CONFIRMED (B drops by 6 at the spike, repairs only +5)')
assert V0 >= 3 and B0at >= 3 + drop
print('    invariant at the event: B=%d >= 3+drop=%d ; V=%d >= 3 OK' % (B0at, 3 + drop, V0))
# all J=19 spikes in range behave identically:
assert all(x[3] == x[1] - 6 for x in ev)

# ---------------- 2c: per-cycle minima, naive-law failure points ----------------
# per-cycle (net, dp_total, m) class map over the whole certified table:
def cyc(J):
    dk, dp = TAB[J]
    rho = (10 + dk) % 16
    return dict(drop=dk - dp, net=dp - dk + G[rho], dp_tot=dp + G[rho] + D[rho],
                m=(dk + D[rho]) // 16, dk16=dk % 16)
stats = {}
for (s, B, J, V, pp) in spikes:
    stats.setdefault(J, []).append((s, B, V, pp))
minnet = min((cyc(J)['net'], J) for J in stats)
mindpt = min((cyc(J)['dp_tot'], J) for J in stats)
print('2c: per-cycle minima over visited classes: min net=%d (J=%d); min dp_total=%d (J=%d)'
      % (minnet + (0,) if False else (minnet[0], minnet[1], mindpt[0], mindpt[1])))
# where does 'net >= 6 and dp_total >= 22' first fail along the walk?
first_fail = None
for (s, B, J, V, pp) in spikes:
    c = cyc(J)
    if c['net'] < 6 or c['dp_tot'] < 22:
        first_fail = (s, J, pp, c); break
ff_s, ff_J, ff_p, ff_c = first_fail
print("    first cycle violating 'net>=6 & dp_total>=22': s=%d J=%d p=%d (net=%d, dp_tot=%d)"
      % (ff_s, ff_J, ff_p, ff_c['net'], ff_c['dp_tot']))
below4e5 = [x for x in spikes if x[4] < 400_000]
ok = all(cyc(x[2])['net'] >= 6 and cyc(x[2])['dp_tot'] >= 22 for x in below4e5)
print("    all %d cycles with p<4e5 satisfy net>=6, dp_total>=22: %s"
      % (len(below4e5), ok))
assert ok and ff_J == 19

# report's structural claims about deeper J (table-derived, no walk needed):
two_drop_gt_g = [J for J in range(23, 121) if 2 * (TAB[J][0] - TAB[J][1]) <= G[(10 + TAB[J][0]) % 16]]
neg = [J for J in range(5, 121) if cyc(J)['net'] < 0]
empty = [J for J in range(5, 121) if TAB[J][0] % 16 == 0]
skip = [J for J in range(5, 121) if cyc(J)['m'] >= 2]
print('    J>=23 with 2*drop <= g (depth-1 fails): %s -> %s'
      % (two_drop_gt_g, 'NONE, fails from J=23 on as claimed' if not two_drop_gt_g else 'REFUTED'))
print('    first J with net<0: %d (claimed 28); empty-walk J (dk%%16==0): %s (claimed 35..37)'
      % (neg[0], [J for J in empty if J < 45]))
print('    first block-skippers m>=2: %s (claimed 38..41 first)' % skip[:4])
c120 = cyc(120)
print('    J=120: drop=%d net=%d m=%d (claimed drop 48, net -34, m 4)'
      % (c120['drop'], c120['net'], c120['m']))
assert neg[0] == 28 and all(J in empty for J in (35, 36, 37)) and skip[0] == 38
assert set(skip[:4]) == {38, 39, 40, 41} and (c120['drop'], c120['net'], c120['m']) == (48, -34, 4)
print('ITEM 2: CONFIRMED (J=19 obstruction real: drop 6 > net 5 at s=27306, p=%d)' % p0)
