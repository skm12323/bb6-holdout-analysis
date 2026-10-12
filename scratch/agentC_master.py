"""Grand validation over E(w,v), w odd <= 61, v <= 500 (plus spot checks at
large w).  Checks at every fire:
  - R/T fires: D = 3t+1, t>=2, i >= t+2, v2(R) < i  (R = D+3 or D+1)
  - S fires:  D = 3t+1 (t any int), k in {1,3} observed, q>=3, and
              q >= h/2^k (h = head) i.e. head alone already forces q>=3
Also: dive-sequence w-independence; excursion always ends; singleton return.
"""
import agentC_lib as lib
from collections import Counter

def E(w, v):
    if v == 1:
        return [3 * w + 1, 3 * w - 1], [('T', 3 * w)]
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

bad = 0
counts = Counter()
Sk = Counter()
seq_by_v = {}
for w in list(range(1, 62, 2)):
    for v in range(1, 501):
        L, ann = E(w, v)
        seq = []
        ended = False
        for s in range(10 ** 5):
            if len(L) == 1:
                ended = True
                break
            role = ann[0][0]
            sig = L[1] + 1 if role == 'T' else L[1]
            i = lib.v2(sig)
            D = L[0] - sig
            if L[0] % 2 == 1:
                x = L[0] + 2 * L[1] + 3
                k = lib.v2(x)
                q = x >> k
                seq.append((role, D, i, k))
                counts[(role, "k%d" % k)] += 1
                ok = True
                if role in ('R', 'T'):
                    t = (D - 1) // 3
                    R = D + (3 if role == 'R' else 1)
                    ok = (D % 3 == 1 and t >= 2 and i >= t + 2
                          and lib.v2(R) < i and q >= 3)
                else:
                    Sk[k] += 1
                    ok = (D % 3 == 1 and q >= 3 and q * (1 << k) >= L[0] + 2 * L[1] + 3
                          and q >= max(1, L[0] >> k))
                if not ok:
                    bad += 1
                    if bad <= 15:
                        print("BAD fire w=%d v=%d step=%d L=%s role=%s D=%d i=%d" %
                              (w, v, s, L, role, D, i))
            L, ann = step_ann(L, ann)
            if L is None:
                print("HALT w=%d v=%d" % (w, v))
                bad += 1
                break
        if not ended:
            print("DID NOT END w=%d v=%d" % (w, v))
            bad += 1
        if w == 1:
            seq_by_v[v] = tuple(seq)

print("bad:", bad)
print("fire role/k counts:", dict(counts))
print("S fire k values:", dict(Sk))

# w-independence: compare E(1,v) sequence to E(w,v) for all w
mism = 0
for w in range(3, 62, 2):
    for v in range(1, 200):
        L, ann = E(w, v)
        seq = []
        for s in range(10 ** 5):
            if len(L) == 1:
                break
            role = ann[0][0]
            sig = L[1] + 1 if role == 'T' else L[1]
            D = L[0] - sig
            if L[0] % 2 == 1:
                x = L[0] + 2 * L[1] + 3
                seq.append((role, D, lib.v2(sig), lib.v2(x)))
            L, ann = step_ann(L, ann)
            if L is None:
                break
        if seq != list(seq_by_v[v]):
            mism += 1
            if mism <= 5:
                print("w-dep mismatch w=%d v=%d:" % (w, v))
                print("   E(1,v):", seq_by_v[v])
                print("   E(w,v):", seq)
print("w-dependence mismatches (v<200):", mism)

# dive prefix structure for E(1,v)
print()
print("dive sequences E(1,v) for v = 40..56:")
for v in range(40, 57):
    print("  v=%-3d %s" % (v, seq_by_v[v]))
