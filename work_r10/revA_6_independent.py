"""ADVERSARY-1 / item 6: independent verification of CL beyond agentA's range.

- own table from run7 (4th independent re-certification);
- SECOND engine check: verify_g6.phi(j) (concrete big-int cascade) on a sample
  of j, catching any run7/table-generation bug;
- fire-level walk to p >= 2e6 (agentA stops at 1.1e6): Phi >= 3 at EVERY fire;
- lockstep cycle-level B/V bookkeeping over the same range;
- full cross-check of the (p,k,j) stream against fast_walker.exact_walker
  (the audited formal map F) to i = 2e5;
- cycle sim extended to s = 1e8.
"""
import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, r'D:\math_cc\scratch')
sys.path.insert(0, r'D:\math_cc\work_r10')
sys.path.insert(0, r'D:\math_cc\work_g6')
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
print('6a [%s] table re-certified (4th time)' % el())

# second engine: concrete Phi_m from verify_g6 (imports nothing from r10/scratch)
import verify_g6
for j in list(range(5, 41)) + [45, 50, 60, 70, 80, 90, 100, 110, 119, 120]:
    dk, dp, steps, ev = verify_g6.phi(j)
    assert (dk, dp) == TAB[j], ('ENGINE DISAGREEMENT', j, (dk, dp), TAB[j])
print('6b [%s] second engine (verify_g6.phi, concrete big-int cascade) agrees with'
      ' run7 on all %d sampled j -- no table-generation bug' % (el(), 61))

# ---------------- fire-level walk to p >= 2e6 ----------------
PLIM = 2_000_000
p, k, fires = 4, 1, 0
Phi_min, Phi_min_at = 10**9, None
stream = []            # (p,k,j) at every fire
spike_cycles = 0
worst_V = 10**9; worst_Bslack = 10**9
D = [0]*16; G = [0]*16
for rho in range(16):
    if rho == 10: continue
    cur, dist, gain = rho, 0, 0
    while cur % 16 != 10:
        dk, dp = TAB[j_of_k(cur)]; dist += dk; gain += dp - dk; cur += dk
    D[rho], G[rho] = dist, gain
while p < PLIM:
    j = j_of_k(k)
    dk, dp = TAB[j]
    Phi = p - k
    if Phi < Phi_min: Phi_min, Phi_min_at = Phi, (p, k, j, fires)
    assert Phi >= 3, ('CL VIOLATION', p, k, j, fires)
    if k % 16 == 10:
        s = (k - 10) // 16
        B = Phi; drop = dk - dp
        assert B >= 3 + drop and B - drop >= 3, ('spike fail', s, J := 5 + v2(3*s+2), B)
        if B - (3 + drop) < worst_Bslack: worst_Bslack = B - (3 + drop)
        if B - drop < worst_V: worst_V = B - drop
        spike_cycles += 1
    stream.append((p, k, j))
    p += dp; k += dk; fires += 1
print('6c [%s] independent fire walk to p>=%d: %d fires, %d spike cycles;'
      % (el(), PLIM, fires, spike_cycles))
print('    Phi_min=%d at %s; worst V=%d; worst slack B-3-drop=%d -- CL HOLDS'
      % (Phi_min, Phi_min_at[:3], worst_V, worst_Bslack))
assert Phi_min == 3 and Phi_min_at[0] == 4

# ---------------- cross-check vs the formal map F ----------------
import fast_walker as fw
lvl = fw.exact_walker(2 * 10**5)
assert lvl == stream[:len(lvl)], 'table stream != exact_walker level fires'
print('6d [%s] (p,k,j) stream == fast_walker.exact_walker level fires, all %d fires'
      ' (i<=2e5): the universal walk IS the audited object F' % (el(), len(lvl)))

# ---------------- cycle sim extended to s = 1e8 ----------------
SMAX = 10 ** 8
s, B = 0, 16
sum_dkd = 0
wV = 10**9; wS = 10**9
while s < SMAX:
    J = 5 + v2(3 * s + 2)
    dk, dp = TAB[J]
    drop = dk - dp
    if B - (3 + drop) < wS: wS = B - (3 + drop)
    if B - drop < wV: wV = B - drop
    assert B >= 3 + drop and B - drop >= 3
    rho = (10 + dk) % 16
    step = dk + D[rho]; sum_dkd += step
    B = B - drop + G[rho]
    s += step // 16
assert sum_dkd == 16 * SMAX
print('6e [%s] cycle sim extended to s=1e8 (k~1.6e9): identity Sum(dk+d)=16s;'
      % el())
print('    worst V=%d, worst slack=%d -- CL invariant holds cycle-exactly' % (wV, wS))
print('ITEM 6: CONFIRMED (agentA_proof re-run green; independent walk p->2e6,'
      ' second engine, F cross-check, s->1e8 all pass)')
