"""Simulate excursions E(w,v) = (3w+1, 3w, 6w, ..., 3w*2^(v-2), 3w*2^(v-1)-1)
directly under T until they return to a singleton (or halt).  Record the
macro-state sequence (role, D, i) and all fires.  w odd >= 1, v >= 1.

Every excursion of the real orbit arises this way (from a singleton fire),
and singleton fires are trivially safe (x = 3(n+2) => q = 3*odd >= 3).
So non-halting <=> no excursion E(w,v) ever fires with q == 1.
"""
import agentC_lib as lib
from collections import Counter

def E(w, v):
    if v == 1:
        return [3 * w + 1, 3 * w - 1]
    L = [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
    return L

def run_excursion(w, v, maxsteps=10 ** 6):
    L = E(w, v)
    states = []
    fires = []
    for step in range(maxsteps):
        if len(L) == 1:
            return states, fires, L[0], True
        a = L[0]
        e1 = L[1]
        # role of e1
        e2 = L[2] if len(L) > 2 else 0
        if e2 == 2 * e1:
            role = 'R'
        elif e2 == 2 * e1 - 1:
            role = 'T'
        else:
            role = 'S'   # e1 is last run of chain-block (followed by seam) or a seam
        sig = e1 + 1 if role == 'T' else e1
        i = lib.v2(sig)
        D = a - sig
        rec = (step, role, D, i, len(L))
        states.append(rec)
        if a % 2 == 1:
            x = a + 2 * e1 + 3
            k = lib.v2(x)
            q = x >> k
            fires.append((step, role, D, i, x, k, q, list(L)))
        L = lib.top_step(L)
        if L is None:
            return states, fires, None, False
    return states, fires, None, None

print("=== E(1,v) for v=1..40: fires and states ===")
allfiretypes = Counter()
for v in range(1, 41):
    states, fires, final, ended = run_excursion(1, v)
    ft = tuple((f[1], f[2], f[3], f[5]) for f in fires)
    danger = [f for f in fires if f[6] == 1]
    for f in ft:
        allfiretypes[f] += 1
    print("v=%-3d steps=%-3d ended=%s final=%s fires=%s %s" %
          (v, len(states), ended, final, ft, "DANGER" if danger else ""))

print()
print("=== full state sequence for E(1, 30) ===")
states, fires, final, ended = run_excursion(1, 30)
for s in states:
    print("   step=%-3d role=%s D=%-4d i=%-3d len=%d" % s)
print("fires:")
for f in fires:
    print("   step=%d role=%s D=%d i=%d x=%d k=%d q=%d" % f[:8])

print()
print("=== fire type counter over E(1,v), v<=40 ===")
for key, cnt in sorted(allfiretypes.items()):
    print("   role=%s D=%d i=%d k=%d  count=%d" % (key[0], key[1], key[2], key[3], cnt))
