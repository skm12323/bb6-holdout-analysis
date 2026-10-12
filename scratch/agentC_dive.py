"""Annotated excursion simulation: E(w,v) for various odd w and large v.
Proper construction-time roles (R/T/S).  Goals:
 (a) all excursions end at a singleton, no danger fires;
 (b) every fire satisfies the safety predicate:
       R-role: x = 3*sigma + (D+3), v2(D+3) < i   [sigma=beta*2^i, beta odd]
       T-role: x = 3*sigma + (D+1), v2(D+1) < i   [sigma = tail+1]
       S-role: v2(D+3) == 1 and 3*sigma > D+3     (sigma = e1)
 (c) w-independence of the (role, D, i, k) fire sequence;
 (d) the dive law: relation between t=(D-1)/3 and i.
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

def run(w, v, maxsteps=10 ** 5):
    L, ann = E(w, v)
    log = []
    fires = []
    for s in range(maxsteps):
        if len(L) == 1:
            return log, fires, L[0], True
        role = ann[0][0]
        sig = L[1] + 1 if role == 'T' else L[1]
        i = lib.v2(sig)
        D = L[0] - sig
        beta = sig >> i
        log.append((s, role, D, i))
        if L[0] % 2 == 1:
            x = L[0] + 2 * L[1] + 3
            k = lib.v2(x)
            q = x >> k
            if role == 'R':
                R = D + 3
            elif role == 'T':
                R = D + 1
            else:
                R = None
            safe = "?"
            if role in ('R', 'T'):
                safe = (lib.v2(R) < i)
            else:
                safe = (lib.v2(D + 3) == 1 and 3 * sig > D + 3)
            fires.append((s, role, D, i, k, q, beta, R, safe))
        L, ann = step_ann(L, ann)
        if L is None:
            return log, fires, None, False
    return log, fires, None, None

print("=== safety + dive law over E(w,v), w in 1..15 odd, v in 1..160 ===")
unsafe = 0
notend = 0
dive = {}     # (role,D,i) -> k  (unique mapping check)
dive_seq = {} # v -> tuple of (role,D,i,k) for w=1
for w in range(1, 16, 2):
    for v in range(1, 161):
        log, fires, final, ended = run(w, v)
        if not ended:
            notend += 1
            print("NOT ENDED", w, v)
        for f in fires:
            role, D, i, k, q, beta, R, safe = f[1:]
            if not safe:
                unsafe += 1
                if unsafe < 20:
                    print("UNSAFE fire w=%d v=%d: %s" % (w, v, f))
            key = (role, D, i)
            if key in dive and dive[key] != k:
                print("k mismatch for", key, dive[key], k)
            dive[key] = k
        if w == 1:
            dive_seq[v] = tuple((f[1], f[2], f[3], f[4]) for f in fires)
print("unsafe fires:", unsafe, " not ended:", notend)
print("distinct fire types (role,D,i)->k:", len(dive))
for key in sorted(dive, key=lambda z: z[2]):
    print("   %s D=%-4d i=%-3d k=%d" % (key[0], key[1], key[2], dive[key]))

print()
print("=== dive sequence for E(1,v), v=80 (fires with t and margin) ===")
for f in dive_seq[80]:
    role, D, i, k = f
    t = (D - 1) // 3 if D % 3 == 1 else None
    print("   role=%s D=%-4d t=%-4s i=%-3d k=%d  2^i=%d 3t+4=%s" %
          (role, D, t, i, k, 1 << i, 3 * t + 4 if t else "-"))
print()
print("prefix-extension check (E(1,v) fire seq prefix of E(1,v') for v'>v):")
bad = 0
for v in range(1, 160):
    a, b = dive_seq[v], dive_seq[v + 1]
    if not (a == b[:len(a)] or a[:len(b)] == b):
        bad += 1
print("non-nested consecutive pairs:", bad)
