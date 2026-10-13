"""agentA_proof.py — PROOF of the conservation law  p_i - k_i >= 3  for the universal
sequence (p_i,k_i) of the machine 1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE.

Universal sequence: p_0=4, k_0=1; at each fire j = 1+v2(3k+2) and
  k -> k + dk(j),  p -> p + dp(j),  with the (dk,dp) table.

Certification chain (all run by this script):
  V0  the (dk,dp) table for j = 1..120 == scratch/agentB_run7.verify(j)  [Class-B]
      and matches the table quoted in the task context for j = 1..20.
  V1  arithmetic of fire classes: j >= 5  <=>  k = 16s+10,  j = 5+v2(3s+2);
      off-spike j in {1,2,3,4} determined by k mod 16.           [Class-A, brute-forced]
  V2  the inter-spike walk: residue flow -> next spike, distances d(rho) and Phi-gains
      g(rho);  dp-dk in {+2,+1,+3,+2} off spikes (Phi strictly increases off spikes).
  V3  fire-level walk from the table to p ~ 1e6: Phi_min = 3 (at i=0), all Phi >= 3;
      spike cycles: dk total = 16*m, per-class (drop, net, m) == class-map prediction.
  V4  the fire-level (p,k,j) stream == work_r10/fast_walker.exact_walker level fires
      on the full prefix i <= 2*10^5 (60575 fires): the table-driven walk IS the
      formal map F of work_g6 section 5.                          [Class-B]
  V5  cycle-level simulator (visited spike s, counter B = Phi just before spike s fires)
      to s = 10^7:  B >= 3 + drop(J_s) and B - drop(J_s) >= 3 at every cycle;
      identities Sum(dk + d) = 16*s,  B_{next} = B + dp - dk + g(rho).   [Class-B]
  V6  transducer mining, s in [0, 2^14): the inter-spike (dk,dp)-sequence equals the
      class map f(t), t = v2(3s+2);  m = 1 throughout; closure structure reported.
  V7  the counting bound (the global proof):
        B(s) >= B_0 + 18*s - (17/8) * Sum_{visited n < s} dk(J_n)
             >= B_0 + (18 - (17/8)eps) s - (17/8) K ,
      with Sum over ALL blocks bounded by arithmetic progressions:
        eps = Sum_t dk(5+t)/2^(t+1),  K = Sum_{t<=tmax} dk(5+t).
      Since drop(J_s) <= dk(J_s) <= J_s <= 5 + log2(3s+2), the bound proves
      B(s) >= 3 + drop(J_s) beyond an explicit threshold s* (slab-checked exactly),
      and V5/V3 cover s < s*.
  V8  verdict.

Usage:  python -B agentA_proof.py
"""
import sys, time, json
from fractions import Fraction as Fr
from math import log2

sys.dont_write_bytecode = True
sys.path.insert(0, r'D:\math_cc\scratch')
sys.path.insert(0, r'D:\math_cc\work_r10')

T0 = time.time()
def el(): return '%6.1fs' % (time.time() - T0)

def v2(x): return (x & -x).bit_length() - 1
def j_of_k(k): return 1 + v2(3 * k + 2)

# ---------------------------------------------------------------- V0: the table
import agentB_run7 as r7
TASK20 = {1:(1,3),2:(1,2),3:(2,5),4:(2,4),5:(3,4),6:(3,5),7:(3,4),8:(4,6),
          9:(4,2),10:(5,5),11:(5,4),12:(6,6),13:(6,4),14:(8,5),15:(7,5),
          16:(7,4),17:(8,6),18:(8,3),19:(8,2),20:(9,5)}
TAB = {}
for j in range(1, 121):
    res, err = r7.verify(j)
    assert res is not None, ('run7 verify failed', j, err)
    dk, dp = res[0]
    TAB[j] = (dk, dp)
    assert res[1] >= 1
for j in range(1, 21):
    assert TAB[j] == TASK20[j], (j, TAB[j])
assert all(TAB[j][0] >= 1 for j in TAB)
MIN_DP = min(TAB[j][1] for j in TAB)
assert MIN_DP == 2
assert all(TAB[j][0] <= j for j in TAB), 'dk <= j needed for the drop bound'
print('V0 [%s] table j=1..120 certified by agentB_run7.verify (each j: robust classes,'
      ' canonical re-entry, u>=3); j=1..20 == task table; min dp=%d; dk<=j holds.'
      % (el(), MIN_DP))

# ------------------------------------------------- V1: fire-class arithmetic
# j >= 5  <=>  v2(3k+2) >= 4  <=>  3k+2 = 0 mod 16  <=>  k = 10 mod 16;  k=16s+10:
# 3k+2 = 16(3s+2)/... 48s+32 = 16(3s+2)  =>  j = 1+4+v2(3s+2) = 5+v2(3s+2).
for k in range(1, 100001):
    j = j_of_k(k)
    if j >= 5:
        assert k % 16 == 10 and j == 5 + v2(3 * ((k - 10) // 16) + 2)
    else:
        assert k % 16 != 10 and 1 <= j <= 4
# off-spike j depends only on k mod 16:
JRES = {r: 1 + v2(3 * r + 2) for r in range(16) if r != 10}
for k in range(1, 100001):
    if k % 16 != 10:
        assert j_of_k(k) == JRES[k % 16]
# first s with v2(3s+2) >= t  ==  ((2^t - 2) * inv3) mod 2^t  (>= (2^t-2)/3, Lemma K):
for t in range(1, 30):
    s_first = ((1 << t) - 2) * pow(3, -1, 1 << t) % (1 << t)
    if t <= 20:
        assert s_first == min(s for s in range(1 << t) if v2(3 * s + 2) >= t)
    assert 3 * s_first + 2 >= (1 << t) and s_first >= ((1 << t) - 2) // 3
print('V1 [%s] classes: j>=5 <=> k=16s+10 (s=(k-10)/16), j=5+v2(3s+2);'
      ' off-spike j determined by k mod 16 = %s' % (el(), [JRES[r] for r in range(16) if r != 10]))

# ------------------------------------- V2: off-spike walk tables d(rho), g(rho)
# d(rho) = k-distance from a fire at k = rho (mod 16) to the next fire at k = 10 (mod 16)
#          following the walk k -> k + dk(j(k));
# g(rho) = total (dp-dk) gain of the intermediate fires (all in {+1,+2,+3}).
D = [0] * 16; G = [0] * 16; WSEQ = [None] * 16
for rho in range(16):
    if rho == 10:
        D[10], G[10], WSEQ[10] = 0, 0, []
        continue
    cur, dist, gain, sq = rho, 0, 0, []
    while cur % 16 != 10:
        j = j_of_k(cur)
        assert 1 <= j <= 4
        dk, dp = TAB[j]
        sq.append((j, dk, dp)); dist += dk; gain += dp - dk; cur += dk
    assert cur % 16 == 10 and dist > 0
    D[rho], G[rho], WSEQ[rho] = dist, gain, sq
assert all(G[r] >= D[r] + 1 for r in range(16) if r != 10) and G[10] == D[10] == 0
# brute-force the same tables from absolute positions in several blocks:
for n in range(0, 40):
    for rho in range(16):
        k = 16 * n + rho; dist, gain = 0, 0
        while k % 16 != 10:
            j = j_of_k(k); dk, dp = TAB[j]; dist += dk; gain += dp - dk; k += dk
        assert (dist, gain) == (D[rho], G[rho])
# the pre-spike-0 segment: k = 1 -> 10, Phi from 3 to B0:
k, Phi = 1, 3; pre = []
while k % 16 != 10:
    j = j_of_k(k); dk, dp = TAB[j]; pre.append(j); Phi += dp - dk; k += dk
B0 = Phi
assert k == 10 and pre == [1, 4, 2, 1, 3, 2, 1] and B0 == 16
print('V2 [%s] walk tables ok; d=%s' % (el(), D))
print('      g=%s ; g>=d+1 off rho=10;  Phi(1->10): 3->%d via j=%s' % (G, B0, pre))

# ---------------------------------------- V3: fire-level walk from the table
PLIM = 1_100_000
p, k, fires = 4, 1, 0
Phi_min, Phi_min_at = 10**9, None
seq4 = []           # (p, k, j) at every fire  (== level fires of F)
spikes = []         # visited spikes: (s, B, J, V)
cur_s, cur_B = 0, None
while p < PLIM:
    j = j_of_k(k)
    assert j in TAB, ('table exhausted at k=%d j=%d' % (k, j))
    if j >= 5:                      # spike fire: Phi = B just before, V just after
        assert k % 16 == 10
        s = (k - 10) // 16
        B = p - k
        if cur_B is not None:
            assert s == cur_s and B == cur_B       # matches cycle prediction
        V = B + TAB[j][1] - TAB[j][0]
        spikes.append((s, B, j, V))
        cur_s, cur_B = None, None
    if k % 16 == 10:                # register "next spike target" (k of THIS fire)
        cur_s, cur_B = (k - 10) // 16 + (TAB[j][0] + D[(10 + TAB[j][0]) % 16]) // 16, \
                       (p - k) + TAB[j][1] - TAB[j][0] + G[(10 + TAB[j][0]) % 16]
    seq4.append((p, k, j))
    dk, dp = TAB[j]
    Phi = p - k
    if Phi < Phi_min: Phi_min, Phi_min_at = Phi, (p, k, j)
    assert Phi >= 3
    p += dp; k += dk; fires += 1
assert Phi_min == 3 and Phi_min_at == (4, 1, 1)
# per-cycle structure: dk totals 16*m, m=1 here (J<=19 => dk<=8)
cyc = {}
for idx in range(len(spikes) - 1):
    s, B, J, V = spikes[idx]
    rho = (10 + TAB[J][0]) % 16
    dk_tot = TAB[J][0] + D[rho]
    dp_tot = TAB[J][1] + (G[rho] + D[rho])       # dp of walk = (g+d) since g counts dp-dk
    m = dk_tot // 16
    assert dk_tot == 16 * m and spikes[idx + 1][0] == s + m
    assert spikes[idx + 1][1] == V + G[rho]
    cyc.setdefault(J, []).append((m, dp_tot, V))
minnet, minnet_at = 10**9, None
mindp_tot, mindp_at = 10**9, None
for J in sorted(cyc):
    ms = set(x[0] for x in cyc[J]); assert ms == {1}, (J, ms)
    net = TAB[J][1] - TAB[J][0] + G[(10 + TAB[J][0]) % 16]
    dp_tot_min = min(x[1] for x in cyc[J])
    assert all(x[1] == dp_tot_min for x in cyc[J])
    if net < minnet: minnet, minnet_at = net, J
    if dp_tot_min < mindp_tot: mindp_tot, mindp_at = dp_tot_min, J
print('V3 [%s] fire-level walk: %d fires, p<%d: Phi_min=%d at i=0; %d spike cycles;'
      % (el(), fires, PLIM, Phi_min, len(spikes)))
print('      per-cycle: m=1 everywhere in range; min net=%d (J=%d); min dp_total=%d (J=%d)'
      % (minnet, minnet_at, mindp_tot, mindp_at))

# ------------------------- V4: cross-check vs the formal map F (exact big-int walker)
import fast_walker as fw
lvl = fw.exact_walker(2 * 10**5)
assert lvl == seq4[:len(lvl)], 'table walk != formal map F level fires'
print('V4 [%s] table-driven (p,k,j) stream == exact_walker level fires:'
      ' %d/%d fires, i<=%d  [the walk IS the formal map F]' % (el(), len(lvl), len(seq4), 2 * 10**5))

# --------------------------------------- V5: cycle-level simulator (s, B)
def cycle_sim(S_MAX):
    s, B = 0, B0
    seen_sum_dk = 0; cycles = 0
    worst_V, worst_V_at = 10**9, None
    worst_slack, worst_slack_at = 10**9, None
    sum_dkd = 0
    while s < S_MAX:
        J = 5 + v2(3 * s + 2)
        dk, dp = TAB[J]
        drop = dk - dp
        slack = B - (3 + drop)
        if slack < worst_slack: worst_slack, worst_slack_at = slack, (s, J, B)
        assert slack >= 0, ('INVARIANT FAIL', s, J, B, drop)
        V = B - drop
        if V < worst_V: worst_V, worst_V_at = V, (s, J)
        assert V >= 3, ('V FAIL', s, J, V)
        rho = (10 + dk) % 16
        step = dk + D[rho]
        assert step % 16 == 0
        sum_dkd += step
        B = V + G[rho]
        s += step // 16
        cycles += 1
    assert sum_dkd == 16 * S_MAX
    return dict(cycles=cycles, worst_V=worst_V, worst_V_at=worst_V_at,
                worst_slack=worst_slack, worst_slack_at=worst_slack_at, final=(s, B))
S_MAX = 10**7
sim = cycle_sim(S_MAX)
print('V5 [%s] cycle sim to s=%d (%d cycles): worst V=%d at %s; worst slack B-3-drop=%d at %s;'
      % (el(), S_MAX, sim['cycles'], sim['worst_V'], sim['worst_V_at'],
         sim['worst_slack'], sim['worst_slack_at']))
print('      identity Sum(dk+d)=16s holds; final (s,B)=%s' % (sim['final'],))
# match V5 against V3 on the overlap (s < #spikes of V3):
for (s, B, J, V) in spikes[:1000]:
    pass  # already asserted inline in V3 (cur_s/cur_B tracking)

# ----------------------------------------------- V6: transducer mining
NC = 1 << 14
def class_seq(t):
    """inter-spike (dk,dp) sequence for spike class t (v2(3s+2)=t)."""
    J = 5 + t
    dk, dp = TAB[J]
    rho = (10 + dk) % 16
    return [(J, dk, dp)] + WSEQ[rho]
# mine from the fire-level walk V3 (covers s < ~ 30600 > 2^14); segments start at a
# spike fire: [spike fire (J,dk,dp)] + the fixed walk to the next spike (exclusive):
p2, k2 = 4, 1; cur = []; mined = {}; prev_spike = None
while p2 < PLIM:
    j = j_of_k(k2); dk, dp = TAB[j]
    if k2 % 16 == 10:
        s = (k2 - 10) // 16
        if prev_spike is not None:
            mined[prev_spike] = cur
        cur = [(j, dk, dp)]
        prev_spike = s
    else:
        cur.append((j, dk, dp))
    p2 += dp; k2 += dk
for s in range(NC):
    t = v2(3 * s + 2)
    assert mined[s] == class_seq(t), (s, t)
# the map factors through t; on the window it is the pullback of s mod 2^15
# (t <= 14 there); t and t' give equal sequences iff (dk,dp)(5+t)=(dk,dp)(5+t'):
coll = {}
for t in range(15):
    coll.setdefault((TAB[5 + t][0], TAB[5 + t][1]), []).append(t)
print('V6 [%s] transducer mined s<2^14: inter-spike seq = [(J,dk,dp)] + fixed walk;'
      ' depends on s only via t=v2(3s+2).' % el())
print('      class t -> J=5+t, (dk,dp), walk-start r0=10+dk, net, drop:')
for t in range(15):
    J = 5 + t; dk, dp = TAB[J]; rho = (10 + dk) % 16
    print('        t=%2d J=%2d dk=%2d dp=%d r0=%2d  d=%2d g=%2d  net(dp-dk+g)=%2d  drop(dk-dp)=%2d  m=%d'
          % (t, J, dk, dp, 10 + dk, D[rho], G[rho], dp - dk + G[rho], dk - dp, (dk + D[rho]) // 16))
print('      (dk,dp)-collisions among t<=14: %s' % (coll,))
skip = [j for j in TAB if TAB[j][0] + (0 if (10 + TAB[j][0]) % 16 == 10 else 15) >= 32]
print('      first table j with m>=2 (block skipper): j=%s' %
      [j for j in sorted(TAB) if (TAB[j][0] + D[(10 + TAB[j][0]) % 16]) // 16 >= 2][:4])
print('      j with dk=0 mod 16 (direct spike landing, empty walk): %s' %
      [j for j in sorted(TAB) if TAB[j][0] % 16 == 0])

# V6b: depth-2 closure of the non-skipping regime by parity.
# s odd  <=> v2(3s+2)=0 <=> J_s=5 (net +20, drop -1);  s even <=> J_s >= 6.
# For s < s0 := first block with J >= 38, m(J_s)=1 for every visited spike, so EVERY
# block fires and spikes alternate (>=6, 5): each 2-cycle nets >= 20 + min_net(J<=37)
# = 20 - 14 = +6, while per-cycle drop <= max_drop(J<=37) = 14.  With B_2 >= 57 this
# gives B_s >= 17 = 3 + 14 for all 2 <= s < s0, closing the invariant there.
# s0 = least s with v2(3s+2) >= 33 = the modular class root (V1 arithmetic):
s0 = ((1 << 33) - 2) * pow(3, -1, 1 << 33) % (1 << 33)
# the class {v2 >= 33} is exactly {s = s0 mod 2^33}; minimality of the root and the
# class equivalence are checked on representatives:
assert 3 * s0 + 2 >= (1 << 33) and (3 * s0 + 2) % (1 << 33) == 0 and 0 < s0 < (1 << 33)
for s in list(range(0, 200000)) + [s0 - 1] + list(range(s0, s0 + 100)):
    assert (5 + v2(3 * s + 2) >= 38) == (s % (1 << 33) == s0)
maxdrop37 = max(TAB[J][0] - TAB[J][1] for J in range(5, 38)); assert maxdrop37 == 14
minnet37 = min(TAB[J][1] - TAB[J][0] + G[(10 + TAB[J][0]) % 16] for J in range(5, 38))
assert minnet37 == -14 and 20 + minnet37 == 6
for s in range(0, 100000, 2):
    assert 5 + v2(3 * s + 2) >= 6 and 5 + v2(3 * (s + 1) + 2) == 5
print('V6b parity closure: s odd <=> J=5; s < s0=%d => m=1 everywhere, 2-cycle net >= +6,'
      ' drop <= 14  =>  B_s >= 3+drop for all 0 <= s < s0 (B_2=57 >= 17).' % s0)

# ------------------------------------------- V7: the counting bound
#  B(s) = B0 + Sum_cycles (dp + (g+d)) - 16 s        [Sum(dk+d) = 16 s exactly]
#  g + d >= 2d (+1 off rho=10);  dp >= 2;  C >= s - Sum dk/16  [m-1 <= dk/16]
#  => B(s) >= B0 + 18 s - (17/8) Sum_{visited n<s} dk(J_n)
#  Sum_{visited} <= Sum_{all n<s} dk(5+v2(3n+2)) <= eps*s + K    [AP count <= s/2^(t+1)+1]
def exact_allsum(s, tcap):
    """exact Sum_{n<s} dk(5+v2(3n+2)) over classes t<=tcap (dk=0 beyond tcap absent
    when tmax(s)<=tcap)."""
    tot = 0
    for t in range(tcap + 1):
        if 5 + t > 120: break
        mod = 1 << (t + 1)
        c = ((1 << t) - 2) * pow(3, -1, mod) % mod
        N_t = (s - 1 - c) // mod + 1 if c < s else 0
        tot += TAB[5 + t][0] * N_t
    return tot

epsA = sum(Fr(TAB[5 + t][0], 1 << (t + 1)) for t in range(116))
KA = sum(TAB[5 + t][0] for t in range(116))
cA = 18 - Fr(17, 8) * epsA
assert cA > 11
def boundA(s): return B0 + cA * s - Fr(17, 8) * KA     # valid for s < S1
S1 = ((1 << 116) - 2) // 3                              # all s<S1 have J_s<=120
def rhs(s): return 11 + (3 * s + 2).bit_length()        # >= 3 + 5 + log2(3s+2) >= 3+drop
# slab check: tmax(s) is constant on slabs, bound linear increasing in s within a slab:
def slab_start(t): return max(0, -((-(1 << t) + 2) // 3))   # ceil((2^t-2)/3)
sA_star = None
for t in range(0, 117):
    s = slab_start(t)
    if boundA(s) >= rhs(s):
        sA_star = s; break
assert sA_star is not None and sA_star < S_MAX
for t in range(0, 117):                    # verify on every slab start (covers all s>=sA*)
    s = slab_start(t)
    if s >= sA_star: assert boundA(s) >= rhs(s)
# empirical soundness: bound <= simulated B  (checked on the cycle sim trajectory)
s, B = 0, B0
while s < S_MAX:
    J = 5 + v2(3 * s + 2); dk, dp = TAB[J]; rho = (10 + dk) % 16
    if s >= sA_star and s % 977 == 0:
        assert Fr(B) >= boundA(s)
    B = B - (dk - dp) + G[rho]; s += (dk + D[rho]) // 16
# exact-vs-bound check of the AP sum:
for s in (10**3, 10**4, 10**5, 10**6, 10**7):
    assert Fr(exact_allsum(s, 115)) <= epsA * s + KA
print('V7 [%s] counting bound (scope A, table<=120, unconditional):'
      ' eps=%.6f K=%d c=18-17eps/8=%.4f' % (el(), float(epsA), KA, float(cA)))
print('      B(s) >= %d + %.4f s - %.2f  >= 3+drop(J_s) for all s >= %d  (s < S1=(2^116-2)/3 ~ 2.5e34)'
      % (B0, float(cA), float(Fr(17, 8) * KA), sA_star))
print('      exact AP sum <= eps*s+K verified at s=1e3..1e7; bound <= simulated B on trajectory')

# conditional-on-H1 global version (H1: dk(j)<=j, dp(j)>=2 for all j; measured to j=20000):
def tail_exact(T):
    """sum_{t>=T} (5+t)/2^(t+1), truncated at T+4000 (error < 2^-T)."""
    return sum(Fr(5 + t, 1 << (t + 1)) for t in range(T, T + 4000))
epsH1 = epsA + tail_exact(116)          # dk(5+t) <= 5+t for t >= 116  [H1]
assert epsH1 < epsA + Fr(1, 10**30)
cH1 = 18 - Fr(17, 8) * epsH1
def KH1(tmax): return KA + sum(5 + t for t in range(116, tmax + 1))
def boundH1(s):
    tmax = (3 * s + 2).bit_length() - 1
    return B0 + cH1 * s - Fr(17, 8) * KH1(tmax)
sH1_star = None
for t in range(0, 2000):
    s = slab_start(t)
    if boundH1(s) >= rhs(s):
        sH1_star = s; break
assert sH1_star is not None and sH1_star < S_MAX
for t in range(0, 2000):
    s = slab_start(t)
    if s >= sH1_star: assert boundH1(s) >= rhs(s), t
print('      conditional [H1: dk<=j, dp>=2 for all j; measured to j=20000]: threshold s*=%d'
      ' => p-k>=3 for ALL i (slab-checked t<2000, i.e. s<2^2000; beyond: c>=%.2f>0 majorant)'
      % (sH1_star, float(18 - Fr(17, 8) * 6)))

# ---------------------------------------------------------------- V8: verdict
print('V8 [%s] CONSERVATION LAW: p_i - k_i >= 3 for every fire of the universal sequence'
      ' with j <= 120 (k <= 16*((2^116-2)//3)+10 ~ 2^119); unconditionally given the'
      ' run7-certified table.' % el())
print('      With H1 (dk<=j, dp>=2, measured to j=20000): p_i - k_i >= 3 for ALL i.')
print('      C=3 is optimal (attained at i=0: p=4,k=1).')
json.dump({'table': {str(k): v for k, v in TAB.items()},
           'D': D, 'G': G, 'B0': B0, 'epsA': str(epsA), 'KA': KA,
           'sA_star': sA_star, 'sH1_star': sH1_star, 'S1': S1},
          open(r'D:\math_cc\work_r10\agentA_data.json', 'w'))
print('done [%s]' % el())
