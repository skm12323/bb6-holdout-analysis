"""Explore the end phase of excursion E(w,v), concrete w=1. Dump full list evolution."""
import sys
v2 = lambda x: (x & -x).bit_length() - 1

def top(L):
    A = L[0]; b = L[1] if len(L) > 1 else 0; c = L[2] if len(L) > 2 else 0; S = L[3:]
    if A % 2 == 0: return [A + b + c + 3] + S
    m = b + (A - 3) // 2; st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st; m = (m - 3) // 2
    if m == 1: return 'HALT'
    return [m + 4] + st

def show(L):
    # compact: try to see (H+d, H, 2H, ..., pert, ...)
    if len(L) > 2 and L[2] == 2 * L[1]:
        H = L[1]; d = L[0] - H
        r = 0
        while r + 2 < len(L) and L[r + 2] == L[1] << (r + 1): r += 1
        # r = number of full run entries after head beyond index 1... report
        return 'can H=%d=3*%d*2^%d d=%d r=%d tail=%s' % (H, H // (3 * (1 << v2(H // 3))) if H % 3 == 0 else -1,
             v2(H // 3) if H % 3 == 0 else -1, d, r + 1, L[r + 2:]) if len(L) > r + 2 else 'can r=%d ALLRUN d=%d H=3w2^j:(%d,%d)' % (r + 1, d, H, v2(H) if H % 3 == 0 else -1)
    return str(L)

v = int(sys.argv[1]) if len(sys.argv) > 1 else 40
w = 1
L = [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
t = 0
print('start E(1,%d): %s' % (v, L[:8], ), '...' if len(L) > 8 else '')
while len(L) > 1:
    A = L[0]; b = L[1] if len(L) > 1 else 0
    x = A + 2 * b + 3
    tag = ''
    if A % 2 == 1:
        q = x >> v2(x)
        tag = ' ODD-A x=%d=2^%d*%d' % (x, v2(x), q)
    print('t=%3d %s%s' % (t, show(L), tag))
    L = top(L); t += 1
print('t=%3d singleton %s' % (t, L))
