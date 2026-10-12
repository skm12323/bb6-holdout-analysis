"""Final validation sweep (background):
 1) 20M-step top-map orbit: assert no halt; every fire q>=3; collect stats.
 2) 3000 random odd w up to 10^15, v <= 64: master affine law at every fire.
Writes summary to stdout."""
import agentC_lib as lib
import random
from collections import Counter

random.seed(12345)

def step_ann(L, ann):
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    if A % 2 == 0:
        return [A + b + c + 3] + L[3:], ann[2:]
    x = A + 2 * b + 3
    k = lib.v2(x)
    q = x >> k
    m = b + (A - 3) // 2
    seam_val = c + (A + 1) // 2
    chain = []
    while m >= 3 and m % 2 == 1:
        chain.append((m + 3) // 2)
        m = (m - 3) // 2
    chain.reverse()
    if m == 1:
        return None, None
    cann = [('R', q, i) for i in range(k - 1)]
    sann = ('T', chain[-1]) if chain and seam_val == 2 * chain[-1] - 1 else ('S',)
    return [m + 4] + chain + [seam_val] + L[3:], cann + [sann] + ann[2:]

# ---- part 2: random w sweep
badw = 0
nf = 0
for trial in range(3000):
    w = random.randrange(1, 10 ** 15) * 2 + 1
    v = random.randrange(1, 65)
    vals = [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
    L = vals
    f1 = None
    for s in range(10 ** 5):
        if len(L) == 1:
            break
        if L[0] % 2 == 1:
            x = L[0] + 2 * L[1] + 3
            nf += 1
            if (x >> lib.v2(x)) < 3:
                badw += 1
                print("SMALL Q w=%d v=%d" % (w, v))
        L = lib.top_step(L)
        if L is None:
            print("HALT w=%d v=%d" % (w, v)); badw += 1; break
print("random sweep: fires=%d bad=%d" % (nf, badw))

# ---- part 1: 20M orbit
L = [3]
minq = (10 ** 9, None)
fires = 0
for n in range(1, 20 * 10 ** 6 + 1):
    L = lib.top_step(L)
    if L is None:
        print("HALT at", n); break
    if L[0] % 2 == 1:
        x = L[0] + 2 * (L[1] if len(L) > 1 else 0) + 3
        k = lib.v2(x)
        q = x >> k
        fires += 1
        if q < minq[0]:
            minq = (q, n)
        if q < 3:
            print("DANGER q=%d n=%d" % (q, n))
print("orbit 20M steps: fires=%d min q=%d at n=%d" % (fires, minq[0], minq[1]))
