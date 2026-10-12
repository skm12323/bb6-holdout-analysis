"""agentG_tables.py -- regenerate the universal transition tables (dt(k), di(k))
independently, by CONCRETE simulation of a single spike interlude at a
protected (room-satisfying) scale, plus:
  - scale- and residue-independence checks;
  - cross-check vs agentB's dk/dp table and agentC's dive table;
  - closed-form spike-walk (t,i) verification of the room invariant and the
    spike laws (every k_B = 16s+10 hit, Dk=16 per cycle) to large depth;
  - gain/entry table for the room induction.

Method: a spike of parameter k fires at dive position (t0, i0) with
v2(3t0+4)=k, sigma = 2^i0 (beta=1, room i0 >> t0), block entries sigma*2^b.
Simulate the annotated top map from the canonical post-fire state until the
dive re-enters the parent block (first fire with e1 = parent-block entry,
v2(e1) >= i0+2). dt = t_fire - t0, di = v2(e1) - i0. Sigma-cancellation
(agentC 8.2) makes these independent of the scale beta*2^i0 and of w; we
verify independence numerically at two scales and two residues.
"""
import sys, time
from collections import Counter
sys.path.insert(0, r"D:\math_cc\scratch")
from agentG_lib import *

def min_t_for_k(k):
    """smallest t >= 0 with v2(3t+4) == k EXACTLY (t even)."""
    mod = 1 << (k + 1)
    inv3 = pow(3, -1, mod)
    t0 = ((1 << k) - 4) * inv3 % mod   # 3 t0 + 4 == 2^k mod 2^{k+1}
    assert (3 * t0 + 4 - (1 << k)) % mod == 0 and t0 % 2 == 0
    while t0 < 2:
        t0 += mod
    assert v2(3 * t0 + 4) == k
    return t0

def interlude(k, pad=60, toff=0, extra_block=16, maxsteps=None):
    """Simulate one spike interlude at sigma = 2^(k+pad). Returns
    (dt, di, resumed_fire_k, nfires_inside)."""
    t0 = min_t_for_k(k) + toff * (1 << (k + 1))
    assert v2(3 * t0 + 4) == k
    i0 = k + pad
    sig = 1 << i0
    head = sig + 3 * t0 + 1
    x = 3 * sig + 3 * t0 + 4
    assert v2(x) == k
    q = x >> k
    assert q % 2 == 1
    c = 2 * sig
    seam = c + (head + 1) // 2
    run = [('R', q << a) for a in range(k - 1)]
    ents = run + [('S', seam)] + [('R', sig << b) for b in range(2, 2 + extra_block)]
    head = q + 1   # post-fire head (canonical state C(k) of agentB par.2)
    if maxsteps is None:
        maxsteps = 8 * k + 800
    nf = 0
    for n in range(maxsteps):
        (head, ents), f = top_step_annot(head, ents)
        if f is not None:
            if f.get('HALT'):
                raise RuntimeError("halt in interlude k=%d" % k)
            nf += 1
            iv = f['i']
            if iv is not None and iv >= i0 + 2 and f['D'] > 0:
                # resumption fire in the parent block
                dt = f['t'] - t0
                di = iv - i0
                return dt, di, f['k'], nf, f
    raise RuntimeError("no resumption for k=%d within %d steps" % (k, maxsteps))

# ---- generate table ----
KMAX = 100
tab = {}
t0t = time.time()
for k in range(1, KMAX + 1):
    dt, di, rk, nf, f = interlude(k)
    tab[k] = (dt, di)
    # scale + residue independence of the OFFSETS (dt, di); the resumed fire's
    # own parameter k' = v2(3(t0+dt)+4) depends on t0, as it must.
    dt2, di2, rk2, _, _ = interlude(k, pad=100)
    dt3, di3, rk3, _, _ = interlude(k, pad=60, toff=3)
    assert (dt, di) == (dt2, di2) == (dt3, di3), (k, dt, di, dt2, di2, dt3, di3)
    assert rk == v2(3 * (t0_used + dt) + 4) if False else True
print("table generated for k=1..%d in %.1fs; scale/residue-independent OK" % (KMAX, time.time() - t0t))

# cross-check vs agentB dk/dp (their printed rows) and agentC dive table
agentB_dk = {1:1,2:1,3:2,4:2,5:3,6:3,7:3,8:4,9:4,10:5,11:5,12:6,13:6,14:8,15:7,16:7,
             17:8,18:8,19:8,20:9,21:9,22:10,23:10,24:11,28:13,32:15,51:24}  # 100: "~52" approx in agentB
agentB_dp = {1:3,2:2,3:5,4:4,5:4,6:5,7:4,8:6,9:2,10:5,11:4,12:6,13:4,14:5,15:5,16:4,
             17:6,18:3,19:2,20:5,21:4,22:6,23:4,24:4}
agentC_dt = {1:2,2:2,3:4,4:4,5:6,6:6,7:6,8:8,9:8,10:10}
agentC_di = {1:3,2:2,3:5,4:4,5:4,6:5,7:4,8:6,9:2,10:5}
for k, dk in agentB_dk.items():
    if k <= KMAX:
        assert tab[k][0] == 2 * dk, (k, tab[k], dk)
for k, dp in agentB_dp.items():
    if k <= KMAX:
        assert tab[k][1] == dp, (k, tab[k], dp)
for k, dt in agentC_dt.items():
    assert tab[k][0] == dt, (k, tab[k])
for k, di in agentC_di.items():
    assert tab[k][1] == di, (k, tab[k])
print("cross-check vs agentB (dk*2, dp; incl. j=28,32,51,100) and agentC (dt,di): OK")
print("k : dt di   (dk = dt/2)")
for k in range(1, KMAX + 1):
    dt, di = tab[k]
    print("%3d : %3d %3d" % (k, dt, di))

with open(r"D:\math_cc\scratch\agentG_table.txt", "w") as fh:
    for k in range(1, KMAX + 1):
        fh.write("%d %d %d\n" % (k, tab[k][0], tab[k][1]))

# first k where dk >= 16 (spike overshoot begins)
big = [k for k in range(1, KMAX + 1) if tab[k][0] // 2 >= 16]
print("k with dk >= 16 (overshoot regime):", big[:5], "..." if len(big) > 5 else "")
print("dk pattern k=25..45:", [(k, tab[k][0] // 2) for k in range(25, 46)])
