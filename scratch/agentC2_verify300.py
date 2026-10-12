"""agentC2 -- part 2: general-k verification to k=300 + structural classification.

For each k = 1..KMAX:
  * exact interlude simulation (two r choices, two pads -> identical (dt,di));
  * classify every interlude fire: universal child fire (D == 3*t_n+1 at i_n),
    seam/S fire (huge |D|, small i), or parent re-entry fire;
  * collect END-suffix data keyed by (k_N, G) after the last child fire;
  * verify bounds dt(k) <= k+2 and loss(k) = dt-di <= k-3 for k>=5;
  * record min odd part q over all fires (safety / no halt).

Then the Task-1 drift arithmetic: exact rates for the margin ledger.
"""
import sys
sys.path.insert(0, r"D:\math_cc\scratch")
from agentC2_interlude import interlude, pick_r, v2
from fractions import Fraction

KMAX = 300

table = {}
allfires_qmin = None
rows = []
for k in range(1, KMAX + 1):
    o1 = interlude(k)
    r2 = pick_r(k, 3)
    o2 = interlude(k, r=r2)
    o3 = interlude(k, pad=200)
    assert (o1['dt'], o1['di']) == (o2['dt'], o2['di']) == (o3['dt'], o3['di']), k
    assert not o1['halt'] and not o2['halt'] and not o3['halt']
    table[k] = (o1['dt'], o1['di'])
    rows.append((k, o1['dt'], o1['di'], o1['dt'] - o1['di'], len(o1['fires'])))

print("verified identical (dt,di) under r/pad variation for k=1..%d; no HALT" % KMAX)

# universal sequence (self-consistent: table used only for k <= KMAX)
U = [(2, 4)]
t, i = 2, 4
Uindex = {(2, 4): 0}
while t < 10 ** 9:
    kk = v2(3 * t + 4)
    assert kk in table, (t, kk)
    dt, di = table[kk]
    t, i = t + dt, i + di
    U.append((t, i))
    Uindex[(t, i)] = len(U) - 1
    if kk > KMAX:
        break

# classify fires of each interlude
bad_univ = []
end_data = {}
qmin = None
for k in range(1, KMAX + 1):
    o = interlude(k)
    fires = o['fires']
    kinds = []
    lastu = None
    for (D, ie, kf, isp, e1) in fires:
        # safety: odd part of x at this fire
        xk = kf
        # recompute q from a fresh odd branch? we have e1 and D: x = head+2e1+3 = (e1+D)+2e1+3
        x = 3 * e1 + D + 3
        qq = x >> kf
        if qmin is None or qq < qmin:
            qmin = qq
        if isp:
            kinds.append('P')
        else:
            hit = None
            if (D - 1) % 3 == 0 and D > 0:
                tn = (D - 1) // 3
                if (tn, ie) in Uindex:
                    hit = Uindex[(tn, ie)]
            if hit is not None:
                kinds.append(('u', hit))
                lastu = hit
            else:
                kinds.append(('S', ie, kf))
    # all non-parent fires must be universal or S (definition); count S fires
    ns = sum(1 for c in kinds if c != 'P' and c[0] == 'S')
    if lastu is not None:
        tN, iN = U[lastu]
        kN = v2(3 * tN + 4)
        G = k - 2 - iN
        key = (kN, G)
        val = (o['dt'] - tN, o['di'], tuple(c for c in kinds if c != 'P'))
        if key in end_data and end_data[key][2].rstrip('S') != val[2].rstrip('S'):
            pass  # S-fire detail may differ; compare numeric part below
        end_data.setdefault(key, set()).add((val[0], val[1], ns))
    else:
        end_data.setdefault(('none', k), set()).add((o['dt'], o['di'], ns))

# check END numeric consistency: same (kN,G) -> same (dt - tN, di)
incons = []
for key, vals in end_data.items():
    if key[0] == 'none':
        continue
    if len(vals) > 1:
        incons.append((key, vals))
print()
print("END consistency (same (kN,G) -> same (dt-tN, di)) inconsistencies:",
      incons[:6] if incons else "NONE", " (over %d keys)" % len([k for k in end_data if k[0] != 'none']))

# bounds
b1 = [(k, dt, di) for (k, dt, di, l, f) in rows if dt > k + 2]
b2 = [(k, l) for (k, dt, di, l, f) in rows if k >= 5 and l > k - 3]
print()
print("bound dt(k) <= k+2 violations:", b1 if b1 else "NONE (k=1..%d)" % KMAX)
print("bound loss(k) <= k-3 (k>=5) violations:", b2 if b2 else "NONE (k=1..%d)" % KMAX)
mx = max((l / k, k) for (k, dt, di, l, f) in rows if k >= 5)
print("max loss/k ratio: %.4f at k=%d" % mx)
mxd = max((dt - k, k) for (k, dt, di, l, f) in rows)
print("max dt-k: %d at k=%d" % mxd)
print("min odd part q over ALL fires of ALL interludes k<=300:", qmin)
print()
print("table (k, dt, di, loss) for k=61..120:")
print([(k, dt, di, l) for (k, dt, di, l, f) in rows if 61 <= k <= 120])

# ---------------------------------------------------------------- Task 1 arithmetic
print()
print("=== Task-1 drift arithmetic (exact rates, exact losses for k<=KMAX) ===")
# gain site densities: t = 2 mod 8 -> +1 (k=1 site), t = 12 mod 16 -> +1 (k=3)
gain_rate = Fraction(1, 8) + Fraction(1, 16)
# loss rate: events (k>=5 fires) at sites t = 20 mod 32; parameter j at rate 1/2^{j+1}
loss_rate = Fraction(0)
for j in range(5, KMAX + 1):
    loss_rate += Fraction(table[j][0] - table[j][1], 2 ** (j + 1))
# tail bound k > KMAX with loss(j) <= j-3
tail_loss = sum(Fraction(j - 3, 2 ** (j + 1)) for j in range(KMAX + 1, 4 * KMAX))
# skip rate: after an event with jump dt(j), skipped gain sites:
#   s = 26+8m < 20+dt  -> ceil((dt-6)/8)^+ ;  s = 28+16m < 20+dt -> ceil((dt-8)/16)^+
def skip(dt):
    if dt <= 6:
        return 0
    a = max(0, -((-(dt - 6)) // 8))       # ceil((dt-6)/8)
    b = max(0, -((-(dt - 8)) // 16)) if dt > 8 else 0  # ceil((dt-8)/16)
    return a + b
skip_rate = Fraction(0)
for j in range(5, KMAX + 1):
    skip_rate += Fraction(skip(table[j][0]), 2 ** (j + 1))
tail_skip = sum(Fraction(skip(j + 2), 2 ** (j + 1)) for j in range(KMAX + 1, 4 * KMAX))
net = gain_rate - loss_rate - skip_rate - tail_loss - tail_skip
print("gain rate 3/16          = %s = %.6f" % (gain_rate, float(gain_rate)))
print("loss rate (exact k<=%d) = %s = %.6f" % (KMAX, loss_rate, float(loss_rate)))
print("skip rate (exact k<=%d) = %s = %.6f" % (KMAX, skip_rate, float(skip_rate)))
print("tail bounds (k>%d)      = %.3e" % (KMAX, float(tail_loss + tail_skip)))
print("NET margin growth rate  = %s = %.6f  (per unit of t)" % (net, float(net)))
print()
print("=== universal orbit spot check ===")
print("U[0:30]:", U[:30])
margins = [i - t for (t, i) in U]
print("min margin over U:", min(margins), "at", U[margins.index(min(margins))])
print("margin at t=%d: %d (rate %.4f)" % (U[-1][0], U[-1][1] - U[-1][0],
                                          (U[-1][1] - U[-1][0]) / U[-1][0]))
