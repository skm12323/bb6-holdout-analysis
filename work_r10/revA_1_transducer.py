"""ADVERSARY-1 / item 1: independent transducer mining.

(1a) Re-certify the (dk,dp) table j=1..120 with scratch/agentB_run7.verify
     (sample j=1..40 printed digit-for-digit); record dk<=j, min dp.
(1b) Independently generate the universal fire sequence from the certified
     table, extract the inter-spike (dk,dp) segments for all spikes
     s in [0, 2^14), and test agentA's claim: the segment depends on s only
     through t = v2(3s+2).  Any s-pair with equal t but different segment
     REFUTES.  Also cross-check the class-map rows t=0..14 of the report.
"""
import sys, time, json
sys.dont_write_bytecode = True
sys.path.insert(0, r'D:\math_cc\scratch')
T0 = time.time()
def el(): return '%6.1fs' % (time.time() - T0)

def v2(x): return (x & -x).bit_length() - 1

# ---------------- 1a: re-certify table with run7 ----------------
import agentB_run7 as r7
TAB = {}
for j in range(1, 121):
    res, err = r7.verify(j)
    assert res is not None, ('run7 failed', j, err)
    (dk, dp), nleaves = res
    TAB[j] = (dk, dp)
print('1a [%s] run7 re-certified j=1..120; j=1..40:' % el())
print('    j : (dk,dp)   [nleaves omitted; table = dict j->(dk,dp)]')
row = []
for j in range(1, 41):
    row.append('%d:(%d,%d)' % (j, TAB[j][0], TAB[j][1]))
print('    ' + ' '.join(row))
# hard facts the proof needs from the table:
bad_dk = [j for j in TAB if TAB[j][0] > j]
mindp = min(TAB[j][1] for j in TAB)
print('    dk(j) <= j for all j<=120: %s (violations %s); min dp = %d'
      % (not bad_dk, bad_dk, mindp))
# agreement with agentA's stored json table:
A = json.load(open(r'D:\math_cc\work_r10\agentA_data.json'))
assert {int(k): tuple(v) for k, v in A['table'].items()} == TAB, 'agentA table mismatch'
print('    == agentA_data.json table (120/120 entries) OK')
TASK20 = {1:(1,3),2:(1,2),3:(2,5),4:(2,4),5:(3,4),6:(3,5),7:(3,4),8:(4,6),
          9:(4,2),10:(5,5),11:(5,4),12:(6,6),13:(6,4),14:(8,5),15:(7,5),
          16:(7,4),17:(8,6),18:(8,3),19:(8,2),20:(9,5)}
assert all(TAB[j] == TASK20[j] for j in TASK20)
print('    j=1..20 == task-context table OK')

# ---------------- 1b: independent fire-level walk + segment mining ----------------
# universal sequence from (p,k) = (4,1); j = 1+v2(3k+2); (dk,dp)=TAB[j]
NC = 1 << 14
KMAX = 16 * NC + 16           # enough k to close the last segment
p, k = 4, 1
segs = {}          # s -> inter-spike segment [(j,dk,dp), ...] starting WITH the spike fire
cur_s, cur_seg = None, None
Phi = p - k
minPhi, minPhi_at = Phi, (p, k)
assert Phi == 3
while k <= KMAX:
    j = 1 + v2(3 * k + 2)
    dk, dp = TAB[j]
    if k % 16 == 10:                     # spike fire opens a new segment
        s = (k - 10) // 16
        if cur_s is not None:
            segs[cur_s] = cur_seg
        cur_s, cur_seg = s, [(j, dk, dp)]
    else:
        assert 1 <= j <= 4, ('off-spike j out of range', k, j)
        if cur_seg is not None:      # pre-spike-0 fires (k=1..9) belong to no segment
            cur_seg.append((j, dk, dp))
    Phi = p - k
    if Phi < minPhi: minPhi, minPhi_at = Phi, (p, k, j)
    assert Phi >= 3, ('CL violated', p, k, j)
    p += dp; k += dk
segs[cur_s] = cur_seg
assert min(segs) == 0 and max(segs) >= NC - 1, (min(segs), max(segs))

# the claim: segment(s) = f(t) with t = v2(3s+2)
by_t = {}
mismatch = []
for s in range(NC):
    t = v2(3 * s + 2)
    by_t.setdefault(t, set()).add(tuple(segs[s]))
    if len(by_t[t]) > 1:
        mismatch.append(s)
print('1b [%s] mined %d segments s in [0,2^14); classes t seen: %s'
      % (el(), NC, sorted(by_t)))
print('    REFUTATION TEST (equal t, different segment): %s'
      % ('NONE - depends only on t CONFIRMED' if not mismatch else mismatch[:5]))
for t in sorted(by_t):
    assert len(by_t[t]) == 1
    seg = list(by_t[t])[0]
    J, dk, dp = seg[0]
    assert J == 5 + t, (t, J)
    # landing residue walk check, fully independent of agentA's D/G tables:
    r0 = (10 + dk) % 16
    cur = 10 + dk
    walk = []
    while cur % 16 != 10:
        jj = 1 + v2(3 * cur + 2)
        walk.append((jj,) + TAB[jj])
        cur += TAB[jj][0]
    assert tuple(walk) == tuple(seg[1:]), (t, walk, seg)
    print('    t=%2d J=%2d (dk,dp)=(%2d,%2d) walklen=%2d net=%+d drop=%+d m=%d'
          % (t, J, dk, dp, len(walk),
             dp - dk + sum(x[2] - x[1] for x in walk),
             dk - dp, (dk + sum(x[1] for x in walk)) // 16))

# report's class-map rows (t, J, dk, dp, r0, d, g, net, drop, m) for t=0..14:
REP = {0:(5,3,4,13,13,19,20,-1,1), 1:(6,3,5,13,13,19,21,-2,1), 2:(7,3,4,13,13,19,20,-1,1),
       3:(8,4,6,14,12,17,19,-2,1), 4:(9,4,2,14,12,17,15,2,1), 5:(10,5,5,15,11,16,16,0,1),
       6:(11,5,4,15,11,16,15,1,1), 7:(12,6,6,16,10,14,14,0,1), 8:(13,6,4,16,10,14,12,2,1),
       9:(14,8,5,18,8,11,8,3,1), 10:(15,7,5,17,9,13,11,2,1), 11:(16,7,4,17,9,13,10,3,1),
       12:(17,8,6,18,8,11,9,2,1), 13:(18,8,3,18,8,11,6,5,1), 14:(19,8,2,18,8,11,5,6,1)}
for t, (J, dk, dp, r0, d, g, net, drop, m) in REP.items():
    if t not in by_t:
        print('    [t=%d (J=%d) first occurs beyond s=2^14 - row checked in item 2]' % (t, J))
        continue
    seg = list(by_t[t])[0] if t in by_t else None
    assert seg is not None and seg[0] == (J, dk, dp), (t, seg)
    d_my = sum(x[1] for x in seg[1:]); g_my = sum(x[2] - x[1] for x in seg[1:])
    net_my = dp - dk + g_my; drop_my = dk - dp; m_my = (dk + d_my) // 16
    assert (d_my, g_my, net_my, drop_my, m_my) == (d, g, net, drop, m), \
        (t, d_my, g_my, net_my, drop_my, m_my)
print('    class-map rows t=0..14 == report table (d,g,net,drop,m) OK')
# (dk,dp)-collision classes t in {0,2}:
coll = {}
for t in sorted(by_t):
    if t <= 14:
        coll.setdefault(TAB[5 + t], []).append(t)
print('    (dk,dp)-collisions among t<=14: %s' % coll)
print('1c CL on the mining window: Phi_min=%d at %s' % (minPhi, minPhi_at))
print('ITEM 1: CONFIRMED (transducer depends only on t; table re-certified)')
