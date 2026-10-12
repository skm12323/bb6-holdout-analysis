"""Collect fire (odd-step) data along the top-map orbit and test candidate
invariants. Fire = step whose list has odd head a; x = a+2b+3; x = 2^k q.
Safety target: q >= 3 at every fire (halting <=> q == 1, x >= 8)."""
import agentC_lib as lib
from collections import Counter, defaultdict
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 4 * 10 ** 6

fires = 0
sing_fires = 0
min_q = None
min_q_rec = None
min_q_over_2k = None
min_q_over_2k_rec = None
per_k = {}          # k -> (min q, count, example n)
k_hist = Counter()
failA = failB = 0   # Lemma-H decomposition failures
mech = Counter()    # which mechanism saves each fire
worst = []          # (q, n, a, b, c, x, k, len)
first_fires = []
nonsing_smallk = Counter()   # k values at non-singleton fires
maxA_at_fire = 0
neg_delta = 0
delta_mod3 = Counter()
v2b_vs_k = []
dump = []

L = [3]
for n in range(1, N + 1):
    L = lib.top_step(L)
    a = L[0]
    if a % 2 == 0:
        continue
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    x = a + 2 * b + 3
    k = lib.v2(x)
    q = x >> k
    fires += 1
    nonsing = len(L) > 1
    if not nonsing:
        sing_fires += 1
    if q < 3:
        print("!!! DANGER FIRE q=%d at n=%d L=%s" % (q, n, L))
    if nonsing:
        if min_q is None or q < min_q[0]:
            min_q = (q, n, list(L), x, k)
        r = q / float(2 ** k)
        if min_q_over_2k is None or r < min_q_over_2k[0]:
            min_q_over_2k = (r, q, 2 ** k, n, x)
        if q <= 200:
            worst.append((q, n, a, b, c, x, k, len(L)))
        nonsing_smallk[k] += 1
        d = a - b
        delta_mod3[d % 3] += 1
        if d <= 0:
            neg_delta += 1
        if k <= 2:
            mech["k<=2 auto"] += 1
        else:
            # Lemma-H candidates: BIG = m*E for entries E
            saved = None
            for idx in range(min(len(L), 6)):
                for mult in (1, 2, 3):
                    E = mult * L[idx]
                    V = lib.v2(E)
                    r2 = x - E
                    if 0 < r2 < (1 << V):
                        saved = (idx, mult, V, r2)
                        break
                if saved:
                    break
            if saved:
                mech["LemmaH entry %d*%d" % (saved[0], saved[1])] += 1
            else:
                mech["NO DECOMP FOUND"] += 1
                if len(dump) < 400:
                    dump.append((n, list(L), x, k, q))
    if len(first_fires) < 400:
        first_fires.append((n, list(L), x, k, q))
    kk = per_k.setdefault(k, [q, 0, n])
    kk[1] += 1
    if q < kk[0]:
        kk[0] = q
        kk[2] = n
    k_hist[k] += 1
    maxA_at_fire = max(maxA_at_fire, a)
    if fires % 200000 == 0:
        print("... n=%d fires=%d minq=%s" % (n, fires, min_q[:2] if min_q else None))

print()
print("steps:", N, "fires:", fires, "singleton fires:", sing_fires)
print("min q at non-singleton fires:", min_q)
print("min q/2^k:", min_q_over_2k)
print("max k:", max(k_hist), " k hist (top):", k_hist.most_common(12))
print("per-k min q (k: minq count n):", {k: tuple(v) for k, v in sorted(per_k.items()) if k <= 24})
print("delta=a-b mod3 at nonsing fires:", dict(delta_mod3), " delta<=0:", neg_delta)
print("mechanisms:", dict(mech))
print("max head at fire:", maxA_at_fire)
print()
print("=== fires with q<=200 (non-singleton), first 120 by q ===")
for rec in sorted(worst)[:120]:
    print(rec)
print()
print("=== no-decomposition fires (first 60) ===")
for rec in dump[:60]:
    print(rec)
