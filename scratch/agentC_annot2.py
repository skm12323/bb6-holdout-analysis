"""Fire taxonomy v2: for every fire record (role, t=(D-1)/3, i=v2(sigma),
margin, k, q, x formula residue r = x - 3*sigma).  Also dump all 'S' fires
and check global room invariant on R/T steps."""
import agentC_lib as lib
from collections import Counter

N = 4 * 10 ** 6

def step(L, ann):
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
    chain_vals = []
    while m >= 3 and m % 2 == 1:
        chain_vals.append((m + 3) // 2)
        m = (m - 3) // 2
    chain_vals.reverse()
    if m == 1:
        return None, None
    chain_ann = [('R', q, i) for i in range(k - 1)]
    if chain_vals and seam_val == 2 * chain_vals[-1] - 1:
        seam_ann = ('T', chain_vals[-1])
    else:
        seam_ann = ('S',)
    return [m + 4] + chain_vals + [seam_val] + L[3:], chain_ann + [seam_ann] + ann[2:]

L = [3]
ann = []
fire_tax = Counter()        # (role, D, i) -> count at fires
fire_kq = {}                # (role, D, i) -> (min q, max k, example)
S_fires = []
room_fail = 0               # R/T steps where 3t+4 >= 2^i (t=(D-1)/3, D=3t+1) or D%3!=1
room_fail_ex = []
T_pos = Counter()           # (D, i) at T steps overall
R_pos = Counter()           # (D, i) at R steps overall
S_fires_k = Counter()

for n in range(1, N + 1):
    L, ann = step(L, ann)
    if L is None:
        print("HALT", n); break
    if len(L) == 1:
        continue
    role0 = ann[0][0]
    sig = L[1] if role0 != 'T' else L[1] + 1
    i = lib.v2(sig)
    D = L[0] - sig
    if role0 == 'T':
        T_pos[(D, i)] += 1
    elif role0 == 'R':
        R_pos[(D, i)] += 1
    if L[0] % 2 == 1:
        x = L[0] + 2 * L[1] + 3
        k = lib.v2(x)
        q = x >> k
        fire_tax[(role0, D, i)] += 1
        key = (role0, D, i)
        cur = fire_kq.get(key, (q, k, n, list(L)))
        if q < cur[0]:
            cur = (q, k, n, list(L))
        fire_kq[key] = cur
        if role0 == 'S':
            S_fires_k[k] += 1
            if len(S_fires) < 130:
                S_fires.append((n, list(L), x, k, q, i, D))
    else:
        if role0 in ('R', 'T'):
            if D % 3 != 1 or (D + 3) >= (1 << i):
                room_fail += 1
                if len(room_fail_ex) < 20:
                    room_fail_ex.append((n, list(L), D, i, role0))

print("fire taxonomy (role, D, i) -> count, minq, k, n, example:")
for key in sorted(fire_tax, key=lambda z: (str(z[0]), z[1], z[2])):
    q, k, n, Lex = fire_kq[key]
    print("  role=%s D=%-4d i=%-3d count=%-7d minq=%-8d k=%-3d n=%d ex=%s" %
          (key[0], key[1], key[2], fire_tax[key], q, k, n, Lex))
print()
print("S fires k distribution:", dict(S_fires_k))
print("S fires (first 40):")
for f in S_fires[:40]:
    print("   n=%-8d L=%-30s x=%d k=%d q=%d i=%d D=%d" % f)
print()
print("room fails (R/T non-fire steps with D%3!=1 or D+3>=2^i):", room_fail)
for f in room_fail_ex:
    print("   ", f)
print()
print("R steps (D,i) top:", R_pos.most_common(15))
print("T steps (D,i) top:", T_pos.most_common(15))
print("R steps max D per i:", sorted(set((d, i) for d, i in R_pos)))
print("T steps (D,i) set:", sorted(set(T_pos)))
