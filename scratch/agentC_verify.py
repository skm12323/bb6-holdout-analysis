"""Verify the audited reduction v2: orbit element (A,b,c,...) <-> TM moment
(0, A, b, c, ...)  [h=0, all runs >=1].  Check they appear in order and that
the top map equals the return map on these 'clean left-edge' moments."""
import agentC_lib as lib
from collections import Counter

print("== generating TM moments ==")
moments, halted, steps = lib.tm_moments(max_moments=400000, max_steps=6 * 10 ** 7)
print("moments:", len(moments), "halted:", halted, "tm steps:", steps)


def is_clean(m):
    return m[0] == 0 and len(m) >= 2 and all(e >= 1 for e in m[1:])


clean = [(i, m[1:]) for i, m in enumerate(moments) if is_clean(m)]
print("clean moments:", len(clean))
print("first 30 clean:", clean[:30])

N = min(len(clean), 100000)
orb_ok = True
for n in range(N):
    if tuple(clean[n][1]) != tuple([L for _, L in lib.orbit(0)]) if False else False:
        break
# compare against generated orbit
orbits = []
for _, L in lib.orbit(N + 5):
    orbits.append(tuple(L))
mismatch = None
for n in range(min(N, len(orbits))):
    if tuple(clean[n][1]) != orbits[n]:
        mismatch = n
        break
print("compared", min(N, len(orbits)), "elements; first mismatch:", mismatch)
if mismatch is not None:
    print("orbit[%d] = %s  vs clean[%d] = %s" %
          (mismatch, orbits[mismatch], mismatch, clean[mismatch][1]))

# analyze skipped moments: between clean[i] and clean[i+1]
kinds = Counter()
maxgap = 0
for i in range(min(len(clean) - 1, N)):
    lo, hi = clean[i][0], clean[i + 1][0]
    maxgap = max(maxgap, hi - lo)
    for t in range(lo + 1, hi):
        m = moments[t]
        if m[0] > 0 and all(e >= 1 for e in m[1:]):
            kinds["h>0 clean-right"] += 1
        elif m[0] == 0:
            kinds["h=0 dirty (interior 0-runs)"] += 1
        else:
            kinds["mixed"] += 1
print("max moment-gap:", maxgap)
print("skipped moment kinds:", dict(kinds))

# sample windows
for w in (0, 2, 9):
    lo, hi = clean[w][0], clean[w + 1][0]
    print("window %d..%d around orbit step %d:" % (lo, hi, w))
    for t in range(lo, hi + 1):
        print("   m[%d]=%s%s" % (t, moments[t], "  <== clean" if is_clean(moments[t]) else ""))
