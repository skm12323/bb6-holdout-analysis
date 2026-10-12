"""Trace the S-fire families exactly: E(1,14) (mid-dive S fire D=24583)
and E(1,65)/E(1,66) (endgame S fires D<0).  Print every step with role,
sigma, D, and at fires the full algebra.  Also verify affine-in-w formulas."""
import agentC_lib as lib

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

def trace(w, v, upto=200):
    L, ann = E(w, v)
    print("=== E(%d,%d) ===" % (w, v))
    for s in range(upto):
        if len(L) == 1:
            print("  step=%-3d SINGLETON %d" % (s, L[0]))
            return
        role = ann[0][0]
        sig = L[1] + 1 if role == 'T' else L[1]
        i = lib.v2(sig)
        D = L[0] - sig
        fire = ""
        if L[0] % 2 == 1:
            x = L[0] + 2 * L[1] + 3
            k = lib.v2(x)
            q = x >> k
            fire = " FIRE x=%d k=%d q=%d  3sig=%d x-3sig=%d" % (x, k, q, 3 * sig, x - 3 * sig)
        print("  step=%-3d role=%s i=%-3d D=%-25d L=%s%s" % (s, role, i, D, L, fire))
        L, ann = step_ann(L, ann)
        if L is None:
            print("  HALT"); return

trace(1, 14)
trace(1, 65)
trace(1, 66, upto=70)

# affine check of S-fire D across w
print()
print("=== S-fire D as affine function of w (v=14 and v=65,66) ===")
for v in (14, 65, 66):
    ds = []
    for w in (1, 3, 5, 7, 9):
        L, ann = E(w, v)
        dl = []
        for s in range(10 ** 4):
            if len(L) == 1:
                break
            role = ann[0][0]
            sig = L[1] + 1 if role == 'T' else L[1]
            if L[0] % 2 == 1 and role == 'S':
                dl.append(L[0] - sig)
            L, ann = step_ann(L, ann)
            if L is None:
                break
        ds.append((w, dl))
    print(" v=%d:" % v, ds)
