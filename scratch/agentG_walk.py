"""agentG_walk.py -- closed-form dive walk on (t,i) with the generated tables:
  (t,i) = (2,4); at each fire k = v2(3t+4); (t,i) += (dt[k], di[k]).
Verifications:
  1) reproduces the level-0 (E-block) fire stream of every excursion E(1,v),
     v <= 2000 (R-fires with i <= v-2, plus the T-fire at i = v-1);
  2) spike laws: spike times t_s = 32s+20 exactly (k_B = 16s+10 all visited,
     in order, Dk_B = 16) while j <= 34; entry table;
  3) room invariant i - t >= 2 along the walk, to 10^7 spikes;
  4) gain/entry table G(r) for the room induction;
  5) max spike parameter encountered vs depth (unboundedness of emitted k).
"""
import sys, time
from collections import Counter
sys.path.insert(0, r"D:\math_cc\scratch")
from agentG_lib import *

TAB = {}
for line in open(r"D:\math_cc\scratch\agentG_table.txt"):
    a, b, c = line.split()
    TAB[int(a)] = (int(b), int(c))

def walk(nfires):
    t, i = 2, 4
    out = [(t, 4, v2(3 * t + 4))]
    for _ in range(nfires - 1):
        k = v2(3 * t + 4)
        dt, di = TAB[k]
        t += dt
        i += di
        out.append((t, i, v2(3 * t + 4)))
    return out

# ---------- 1) level-0 streams vs excursions ----------
def step_gen(head, ents):
    """annotated step with generation tracking; ents = [(role, val, gen)]."""
    if head % 2 == 0:
        e1 = ents[0][1] if ents else 0
        e2 = ents[1][1] if len(ents) > 1 else 0
        return (head + e1 + e2 + 3, ents[2:]), None
    e1 = ents[0][1] if ents else 0
    role, gen = (ents[0][0], ents[0][2]) if ents else ('X', 0)
    x = head + 2 * e1 + 3
    k = v2(x)
    q = x >> k
    assert q > 1
    c = ents[1][1] if len(ents) > 1 else 0
    seam = c + (head + 1) // 2
    run = [('R', q << a, gen + 1) for a in range(k - 1)]
    sig = e1 if role in ('R', 'S') else e1 + 1
    D = head - sig
    ok_t = ((D - 1) % 3 == 0)
    f = {'role': role, 'gen': gen, 'i': v2(sig) if sig > 0 else None,
         'D': D, 'k': k, 't': (D - 1) // 3 if ok_t else None, 'ok_t': ok_t}
    return (q + 1, run + [('S', seam, gen + 1)] + ents[2:]), f

WK = walk(60000)
t0 = time.time()
nv = 0
for v in range(1, 2001):
    ents = [('R', 3 << a, 0) for a in range(v - 1)] + [('T', (3 << (v - 1)) - 1, 0)]
    head = 4
    lvl0 = []   # (t, i, k, isT)
    for n in range(40 * v + 200):
        (head, ents), f = step_gen(head, ents)
        if f is not None:
            if f['gen'] == 0 and f['ok_t']:
                lvl0.append((f['t'], f['i'], f['k'], f['role'] == 'T'))
        if not ents:
            break
    # expected: walk prefix with i <= v-1
    exp = [(t, i, k, False) for (t, i, k) in WK if i <= v - 2]
    expT = [(t, i, v2(3 * t + 2), True) for (t, i, k) in WK if i == v - 1]
    exp = exp + expT
    assert lvl0 == exp[:len(lvl0)], (v, lvl0[:6], exp[:6])
    nv += 1
print("level-0 dive streams reproduced by the closed walk for all v <= %d (%.1fs)" % (nv, time.time() - t0))

# ---------- 2) spike laws ----------
spikes = [(idx, t, i, k) for idx, (t, i, k) in enumerate(WK) if k >= 5]
gaps = [spikes[m + 1][1] - spikes[m][1] for m in range(len(spikes) - 1)]
print("spikes in walk:", len(spikes), "first 6 (t,j):", [(t, k) for _, t, _, k in spikes[:6]])
print("gap dt between spikes: ", sorted(Counter(gaps).items())[:8])
ok16 = all(g == 32 for g in gaps)
print("all spike gaps = 32 (Dk_B = 16, every k_B==10 mod 16 hit):", ok16)
# t_s = 32 s + 20?
okorder = all(t == 32 * s + 20 for s, (_, t, _, _) in enumerate(spikes))
print("spike times t_s == 32s+20 exactly:", okorder)

# ---------- 3) room invariant + max j ----------
minroom = min(i - t for (t, i, k) in WK)
print("walk (first %d fires): min room i-t = %d, max j = %d" % (len(WK), minroom, max(k for _, _, k in WK)))

t0 = time.time()
S_MAX = 10 ** 7
t, i = 2, 4
minroom2 = 2
maxj = 0
nspk = 0
prev_t = 2
gapset = Counter()
room_at = {}
for m in range(40 * S_MAX):
    k = v2(3 * t + 4)
    if k > maxj:
        maxj = k
    r = i - t
    if r < minroom2:
        minroom2 = r
        room_at = {'t': t, 'i': i, 'k': k}
    if k >= 5:
        nspk += 1
        if nspk > 1:
            gapset[t - prev_t] += 1
        prev_t = t
    dt, di = TAB[k]
    t += dt
    i += di
    if nspk >= S_MAX:
        break
    if k >= 100:
        print("reached table limit at t =", t); break
print("deep walk: %d spikes, max j = %d, min room = %d at %s (%.1fs)" % (
    nspk, maxj, minroom2, room_at, time.time() - t0))
print("deep walk spike gap distribution:", dict(sorted(gapset.items())[:6]))

# ---------- 4) entry/gain table ----------
# entry position r = k_B advance from spike = dk(j); gains = #(k=1)+#(k=3) fires
# between spike s and spike s+1.
# entry dk = dk(j_s) of the spike; gains = #(k in {1,3}) between spike s and s+1
ent = Counter()
gain = Counter()
j_prev = None
g = 0
for (t2, i2, k2) in WK[:60000]:
    if j_prev is None:
        j_prev = k2
        continue
    if k2 >= 5:
        ent[TAB[j_prev][0] // 2] += 1
        gain[g] += 1
        g = 0
        j_prev = k2
    elif k2 in (1, 3):
        g += 1
print("entry dk distribution (observed j regime):", dict(sorted(ent.items())))
print("gain G distribution:", dict(sorted(gain.items())))
# cost c(j) = dt - di per spike class
print("cost c(j) = dt-di for j=5..20:", [(j, TAB[j][0] - TAB[j][1]) for j in range(5, 21)])
# room drift check: room after m-th spike
rms = []
r = 2
room = 2
t, i = 2, 4
for m in range(200000):
    k = v2(3 * t + 4)
    dt, di = TAB[k]
    t += dt; i += di
    room = i - t
    if k >= 5:
        rms.append(room)
ns = len(rms)
print("room after spike s: s=0..9:", rms[:10], " s=100:", rms[min(100,ns-1)], " s=10^3:", rms[min(1000,ns-1)], " last:", rms[-1])
print("min room over first 2e5 spikes:", min(rms))
