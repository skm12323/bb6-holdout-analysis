"""Dump the actual end-phase lists (symbolic forms a*u+b) for selected excursions."""
import sys
v2 = lambda x: (x & -x).bit_length() - 1
class Undecided(Exception): pass
def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def sc(x, k): return (x[0] * k, x[1] * k)
def par(x):
    if x[0] % 2: raise Undecided('parity')
    return x[1] % 2
def half(x):
    if x[0] % 2 or x[1] % 2: raise Undecided('half')
    return (x[0] // 2, x[1] // 2)
def ge3(x):
    if x[0] >= 0 and x[1] >= 3: return True
    if x[0] == 0 and x[1] < 3: return False
    raise Undecided('compare')
Z0 = (0, 0)
def T(L):
    A = L[0]; b = L[1] if len(L) > 1 else Z0; c = L[2] if len(L) > 2 else Z0; R = L[3:]
    if par(A) == 0: return [add(A, b, c, (0, 3))] + R
    m = half(add(b, b, A, (0, -3))); st = [half(add(c, c, A, (0, 1)))] + R
    while par(m) == 1 and ge3(m):
        st = [half(add(m, (0, 3)))] + st; m = half(add(m, (0, -3)))
    if par(m) == 1: raise Exception('HALT branch reachable')
    return [add(m, (0, 4))] + st

def show(x):
    a, b = x
    if a == 0: return str(b)
    if b == 0: return '%du' % a
    return '(%du%+d)' % (a, b)

for v in [int(x) for x in sys.argv[1:]] or [127]:
    w3 = (6, 3)
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
    t = 0; start_print = None
    # first find total length by running once
    L2 = list(L); n = 0
    while len(L2) > 1: L2 = T(L2); n += 1
    start_print = max(0, n - 14)
    while len(L) > 1:
        if t >= start_print:
            A = L[0]; b = L[1] if len(L) > 1 else Z0
            x = add(A, b, b, (0, 3))
            print('t=%3d len=%2d %s' % (t, len(L), ' '.join(show(e) for e in L[:8]) + (' ...' if len(L) > 8 else '')))
        L = T(L); t += 1
    print('t=%3d singleton %s  (ell=%d, start_print=%d)' % (t, show(L[0]), n, start_print))
