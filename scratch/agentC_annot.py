"""Annotated orbit v2: track structural role of every entry + head offset.

Roles: ('R', beta, i)  geometric run entry, value beta*2^i (beta odd)
       ('T', rho)      tail: value 2*rho-1 == 2*lastrun-1 of preceding chain
       ('S',)          seam (fire-produced value c+(a+1)//2, not of tail form)

Checks:
 G1 values match roles; R-blocks contiguous geometric (beta,i),(beta,i+1)...
 G2 head h = sigma + D with D % 3 == 1, sigma = e1 (R) or e1+1 (T) or e1 (S)
 G3 margin 2^v2(sigma) - (D+3) > 0 logged; worst-case tracked
"""
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
    chain_vals.reverse()   # stack order is ascending q, 2q, ...
    if m == 1:
        return None, None
    assert chain_vals == [q << i for i in range(k - 1)], (L, chain_vals, q, k)
    chain_ann = [('R', q, i) for i in range(k - 1)]
    if chain_vals and seam_val == 2 * chain_vals[-1] - 1:
        seam_ann = ('T', chain_vals[-1])
    else:
        seam_ann = ('S',)
    return [m + 4] + chain_vals + [seam_val] + L[3:], chain_ann + [seam_ann] + ann[2:]

L = [3]
ann = []
fails_G1 = 0
fails_G2 = 0
fail_list = []
D_mod3 = Counter()
role_steps = Counter()
worst_margin = None
type_at_fire = Counter()
fire_dump = []
block_breaks = Counter()

for n in range(1, N + 1):
    L, ann = step(L, ann)
    if L is None:
        print("HALT at", n); break
    if len(L) == 1:
        role_steps['SINGLE'] += 1
        continue
    # G1 value check
    ok = True
    for v, role in zip(L[1:], ann):
        if role[0] == 'R':
            if v != (role[1] << role[2]) or role[1] % 2 != 1: ok = False; break
        elif role[0] == 'T':
            if v != 2 * role[1] - 1: ok = False; break
    if not ok:
        fails_G1 += 1
        if len(fail_list) < 20: fail_list.append(("G1", n, list(L), list(ann)))
        break
    # G1b contiguity: R entries with same beta must have consecutive i
    for i2 in range(1, len(ann)):
        if ann[i2-1][0] == 'R' and ann[i2][0] == 'R':
            if ann[i2-1][1] == ann[i2][1] and ann[i2][2] != ann[i2-1][2] + 1:
                block_breaks['nonconsecutive same beta'] += 1
            if ann[i2-1][1] != ann[i2][1]:
                block_breaks['beta change R->R'] += 1
    role0 = ann[0][0]
    role_steps[role0] += 1
    sig = L[1] if role0 != 'T' else L[1] + 1
    v2sig = lib.v2(sig)
    D = L[0] - sig
    D_mod3[D % 3] += 1
    if D % 3 != 1:
        fails_G2 += 1
        if len(fail_list) < 20: fail_list.append(("G2", n, list(L), list(ann), D, sig))
    margin = (1 << v2sig) - (D + 3)
    if margin <= 0 and L[0] % 2 == 1:
        if len(fail_list) < 25: fail_list.append(("MARGIN<=0 AT FIRE", n, list(L), list(ann), D, v2sig))
    if worst_margin is None or margin < worst_margin[0]:
        worst_margin = (margin, n, D, v2sig, role0, list(L))
    if L[0] % 2 == 1:
        type_at_fire[(role0, D % 3)] += 1
        if len(fire_dump) < 60:
            fire_dump.append((n, list(L), ann[0], D, v2sig, margin))

print("steps:", N)
print("entry roles at non-singleton steps:", dict(role_steps))
print("block structure anomalies:", dict(block_breaks))
print("D mod 3:", dict(D_mod3), " G2 fails:", fails_G2, " G1 fails:", fails_G1)
for f in fail_list: print("  FAIL", f)
print("worst margin:", worst_margin)
print("fire types (role, D mod 3):", dict(type_at_fire))
print()
for f in fire_dump[:50]:
    print("  n=%-6d L=%-40s ann0=%s D=%d v2sig=%d margin=%d" % f)
