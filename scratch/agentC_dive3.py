"""Extract the dive map: from E(1,v_big), the sequence of E-block fires
(t_j, i_j, k_j). Fit (delta_t, delta_i) as a function of k_j (and check
whether k_j alone determines them, including interludes).  Verify i>=t+2,
and compute the drift statistics of i-t."""
import agentC_lib as lib
from collections import Counter, defaultdict

def E(w, v):
    vals = [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
    ann = [('R', 3 * w, i) for i in range(v - 1)] + [('T', 3 * w << (v - 2))]
    return vals, ann

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

v = 1200
L, ann = E(1, v)
dive = []      # fires whose scale sigma = 3*2^p (pure E-block)
for s in range(10 ** 6):
    if len(L) == 1:
        break
    role = ann[0][0]
    if role == 'R' and ann[0][1] == 3 and L[0] % 2 == 1:
        sig = L[1]
        t = (L[0] - sig - 1) // 3
        x = L[0] + 2 * L[1] + 3
        k = lib.v2(x)
        dive.append((t, lib.v2(sig), k))
    L, ann = step_ann(L, ann)
    if L is None:
        break

print("E-block fires in E(1,%d): %d" % (v, len(dive)))
print("first 40:", dive[:40])
print("last 5:", dive[-5:])

# fit delta as function of k
byk = defaultdict(Counter)
for j in range(len(dive) - 1):
    (t1, i1, k1), (t2, i2, k2) = dive[j], dive[j + 1]
    byk[k1][(t2 - t1, i2 - i1)] += 1
print()
print("delta (dt, di) by k:")
for k in sorted(byk):
    print("   k=%-3d %s" % (k, dict(byk[k])))

# check i>=t+2 and drift
mind = min(i - t for t, i, k in dive)
print("min i-t:", mind, "at", [d for d in dive if d[1] - d[0] == mind][:5])
print("final i-t:", dive[-1][1] - dive[-1][0], "t:", dive[-1][0])
print("i/t at end: %.4f" % (dive[-1][1] / dive[-1][0]))
# max k vs t: check v2(3t+4) < i always
bad = [d for d in dive if lib.v2(3 * d[0] + 4) >= d[1]]
print("fires with v2(3t+4) >= i:", len(bad), bad[:5])
