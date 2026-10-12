# blind1_explore.py -- sanity checks of my simulator against the audited
# reduction's stated orbit structure, and a first independent look at the
# chain-event schedule of an excursion (no agentB code read).
from blind1_lib import (top_step_loop, top_step_closed, excursion_state,
                         run_excursion, Stepper, v2)

# 1) orbit from (3): singletons (3n+3) and excursions E(w,v) entered when
#    n+2 = 2^v w  (n = number of top steps taken so far).
L = (3,)
n = 0
checked_exc = 0
mism = 0
while n < 4000:
    L, halted = top_step_closed(L)
    assert not halted
    n += 1
    if len(L) == 1:
        if L[0] != 3 * n + 3:
            print("singleton sum mismatch at n=%d: %s" % (n, L))
            mism += 1
        # predict next excursion from n+2 = 2^v w  (v=0 -> plain singleton)
        t = n + 2
        v = 0
        while t % 2 == 0:
            t //= 2
            v += 1
        w = t
        L2, _ = top_step_closed(L)
        if v == 0:
            if L2 != (3 * (n + 1) + 3, ):
                print("expected singleton successor at n=%d: %s" % (n, L2))
                mism += 1
        else:
            exp = excursion_state(w, v)
            if L2 != exp:
                print("excursion mismatch n=%d w=%d v=%d:\n  got %s\n  exp %s"
                      % (n, w, v, L2, exp))
                mism += 1
            checked_exc += 1
print("structure check: %d excursion entries checked, mismatches=%d"
      % (checked_exc, mism))

# 2) master schedule from a long excursion: level-0 chain events
def level0_schedule(w, v, upto=None):
    E = excursion_state(w, v)
    A, entries = E[0], list(E[1:])
    q = [[entries[a], ('run', 0, a)] for a in range(v - 1)]
    q.append([entries[-1], ('defect',)])
    st = Stepper(A, q)
    st.levels.append(__import__('blind1_lib').Level(3 * w, 0))
    out = []
    steps = 0
    while len(st.q) > 0 or steps == 0:
        ev = st.step()
        steps += 1
        if ev['kind'] == 'fire':
            b = ev['b']
            if b[1] is not None and b[1][0] == 'run' and b[1][1] == 0:
                rho = b[1][2]
                U = st.levels[0].base
                x = ev['x']
                k, r = divmod(x - 3 * (U << rho) - 4, 6)
                out.append((rho, ev['j'], k, r))
        if ev['kind'] == 'halt':
            print("HALT in excursion!")
            break
        if len(st.q) == 0:
            break
        if steps > 10 * v + 1000:
            raise RuntimeError("runaway")
    return out, steps

sched, steps = level0_schedule(1, 3200)
print("w=1 v=3200: %d level-0 chain events, %d steps" % (len(sched), steps))
print("first 21 (rho, j, k, x%6resid):", sched[:21])
bad = [t for t in sched if t[3] != 0]
print("events with (x - 3*2^rho*U - 4) not divisible by 6:", len(bad))
jk_bad = [t for t in sched if t[1] != 1 + v2(3 * t[2] + 2)]
print("events with j != 1+v2(3k+2):", len(jk_bad), jk_bad[:5])
# claimed (p, k, j) from closedform.md section 3
claim_p = [4,7,11,13,16,21,23,26,31,34,39,41,44,48,50,53,58,60,63,67,70]
claim_k = [1,2,4,5,6,8,9,10,13,14,16,17,18,20,21,22,24,25,26,29,30]
claim_j = [1,4,2,1,3,2,1,6,1,1,3,2,1,4,2,1,3,2,1,5,3]
mine_p = [t[0] for t in sched[:21]]
mine_k = [t[2] for t in sched[:21]]
mine_j = [t[1] for t in sched[:21]]
print("mine p == claim:", mine_p == claim_p)
print("mine k == claim:", mine_k == claim_k)
print("mine j == claim:", mine_j == claim_j)
if mine_p != claim_p or mine_k != claim_k or mine_j != claim_j:
    print(" mine p:", mine_p)
    print(" mine k:", mine_k)
    print(" mine j:", mine_j)
# derive dk/dp from schedule deltas by j
from collections import defaultdict
dks, dps = {}, {}
for i in range(len(sched) - 1):
    rho, j, k, _ = sched[i]
    rho2, j2, k2, _ = sched[i + 1]
    if rho2 <= rho:
        continue
    if j in dks and (dks[j] != k2 - k or dps[j] != rho2 - rho):
        print("NON-UNIFORM transition for j=%d: %s vs %s"
              % (j, (dks[j], dps[j]), (k2 - k, rho2 - rho)))
    dks[j] = k2 - k
    dps[j] = rho2 - rho
print("schedule-derived dk/dp by j:",
      {j: (dks[j], dps[j]) for j in sorted(dks)})
# ell for small v
ells = []
for v in range(1, 21):
    s, fin, halted = run_excursion(excursion_state(1, v))
    ells.append(s)
print("ell(1..20) mine:", ells)
print("ell(1..20) claim: [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]")
