"""Explore macro structure of excursions E(w,v): decompose into canonical macro-steps,
catalog the end phase (glue steps, odd-entry positions), and margin statistics.
Symbolic in u (w=2u+1), R5-style engine, direct stepping."""
import sys
from collections import Counter

v2 = lambda x: (x & -x).bit_length() - 1
class Undecided(Exception): pass

# affine forms in single symbol u (coefficient, constant)
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

def v2f(x):  # guaranteed min valuation of form; also exactness flag
    g = 0
    while x[0] % 2 == 0 and x[1] % 2 == 0 and (x[0] or x[1]):
        x = (x[0] // 2, x[1] // 2); g += 1
    return g

def canon(L):
    """If L = (H+d, H, 2H, ..., 2^(r-1)H, tail...) with H|(6u+3)*2^j form, return (d, H, r)."""
    if len(L) < 3: return None
    H = L[1]
    if L[2] != sc(H, 2): return None
    # H must be (6u+3)*2^j: coeff = 2*const, const = 3*2^j
    if H[0] != 2 * H[1] or H[1] % 3: return None
    r = 1
    while r + 2 < len(L) and L[r + 2] == sc(H, 1 << r): r += 1
    # r = # of entries 2^i H for i=0..r-1 ... L[2]=2H so run length (after head) = r+1
    d = add(L[0], sc(H, -1))
    return d, H, r + 1

S = int(sys.argv[1]) if len(sys.argv) > 1 else 240
templates = Counter(); margins = []; events = Counter()
endphase_log = []
for v in range(1, S + 1):
    w3 = (6, 3)  # 3w = 6u+3
    L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
    t = 0; can_t = 0; last_can = None; phase = 'mid'; log = []
    while len(L) > 1:
        c = canon(L)
        if c:
            d, H, r = c
            j = v2f(H)
            if d == (0, 3 * can_t + 1):
                pass  # d = 3t+1 as expected
            else:
                events['d!=3t+1'] += 1
            if par(d) == 0:
                events['R-even'] += 1; log.append(('R', can_t, r, None))
            else:
                sp = v2f(add(d, (0, 3)))
                margins.append((v, can_t, j, sp))
                events['M(s=%d)' % sp] += 1
                # odd J entry position within the Z-window of the nested call:
                # Z'_i = 2^(i+1) H for i<=r-2, J = 2^r H -1 at position r-1
                log.append(('M', can_t, r, sp, r - 1))
                if r - 1 <= 3: phase = 'end'
            can_t += 1
        else:
            events['noncanon'] += 1
            log.append(('G', t, len(L)))
        L = T(L); t += 1
    templates[tuple(x[0] if x[0] != 'M' else 'M%d@r%d' % (x[3], x[2]) for x in log[-8:])] += 1
    endphase_log.append((v, log[-10:]))
print('events:', dict(events))
mn = min(m[2] - m[3] for m in margins)
print('min margin j - s\': %d ; margins at excursion start (can_t<=2): %s' % (mn, [m for m in margins if m[1] <= 2][:12]))
print('margin<0 count:', sum(1 for m in margins if m[2] - m[3] < 0), 'margin==0:', sum(1 for m in margins if m[2] == m[3]))
# where do small margins occur?
sm = [(v, t, j, sp) for (v, t, j, sp) in margins if j - sp < 3]
print('margins<3 (first 20):', sm[:20])
print('\nlast-8-event templates (top 15):')
for k, c in templates.most_common(15): print('  %4d  %s' % (c, k))
print('\nend phase detail for selected v:')
for v, log in endphase_log:
    if v in (5, 8, 14, 24, 32, 42, 51, 64, 100, 127, 200, 240):
        print(' v=%d: %s' % (v, log))
