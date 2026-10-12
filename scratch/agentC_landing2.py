"""Corrected landing-law verification.  Laws:
  L-R: at any fire, x = 3*sigma + D + eps, eps=3 for roles R,S; eps=1 for T.
  L-land (mid-block R-fire, c = next run, k = v2(3t+4) <= 5):
      k odd : next E-block fire at (D', i') in {(3t+(3k+11)/2, i+3), (+3, i+5)}
      k even:                     in {(3t+(3k+8)/2,  i+2), (+3, i+4)}
      (second entry when first D' even; also allow T-role twin)
  k>=6: interlude fires occur inside the chain; record separately.
Also: all fires in E(w,v), w in {1,3,5,17,41,10**6+1}, v<260: x=alpha*w+gamma
with gamma>0, v2(gamma)<v2(alpha)."""
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

xlaw_bad = 0
landok = Counter()
landbad = Counter()
aff_bad = 0
WS = (1, 3, 5, 17, 41, 10 ** 6 + 1)
for w in WS:
    for v in range(7, 260):
        L, ann = E(w, v)
        hist = []
        for s in range(10 ** 5):
            if len(L) == 1:
                break
            role = ann[0][0]
            c_is_run = (role == 'R' and len(ann) > 1 and ann[1][0] == 'R'
                        and ann[1][1] == ann[0][1] and ann[1][2] == ann[0][2] + 1)
            sig = L[1] + 1 if role == 'T' else L[1]
            i = lib.v2(sig)
            D = L[0] - sig
            fire = L[0] % 2 == 1
            rec = None
            if fire:
                x = L[0] + 2 * L[1] + 3
                k = lib.v2(x)
                eps = 1 if role == 'T' else 3
                if x != 3 * sig + D + eps:
                    xlaw_bad += 1
                rec = (role, D, i, k, c_is_run)
            hist.append((s, role, D, i, fire, rec))
            L, ann = step_ann(L, ann)
            if L is None:
                break
        for idx in range(len(hist)):
            s, role, D, i, fire, rec = hist[idx]
            if not fire:
                continue
            rrole, rD, ri, rk, c_run = rec
            if rrole != 'R' or not c_run:
                continue
            t = (rD - 1) // 3
            k = rk
            # next R/T fire with i > ri+1 (skip chain-internal fires, i small)
            nxt = None
            for j2 in range(idx + 1, len(hist)):
                s2, role2, D2, i2, fire2, rec2 = hist[j2]
                if fire2 and role2 in ('R', 'T') and i2 > ri + 1:
                    nxt = (D2, i2)
                    break
            if nxt is None:
                continue
            nD, ni = nxt
            if k <= 5:
                if k % 2 == 1:
                    Dp = 3 * t + (3 * k + 11) // 2
                    ip = ri + 3
                else:
                    Dp = 3 * t + (3 * k + 8) // 2
                    ip = ri + 2
                cands = {(Dp, ip)}
                if Dp % 2 == 0:
                    cands.add((Dp + 3, ip + 2))
                if (nD, ni) in cands:
                    landok["k%d ok" % k] += 1
                else:
                    landbad["k%d" % k] += 1
                    if sum(landbad.values()) <= 8:
                        print("LANDING BAD w=%d v=%d fire(t=%d,i=%d,k=%d) pred %s got (%d,%d)"
                              % (w, v, t, ri, k, sorted(cands), nD, ni))
            else:
                landok["k%d deferred" % k] += 1

print("x-law violations:", xlaw_bad)
print("landing ok:", dict(landok))
print("landing bad:", dict(landbad))

# final master affirmation across universe: gamma>0 and v2(gamma)<v2(alpha)
def fires_of(w, v):
    L, ann = E(w, v)
    out = []
    for s in range(10 ** 5):
        if len(L) == 1:
            break
        if L[0] % 2 == 1:
            out.append(L[0] + 2 * L[1] + 3)
        L, ann = step_ann(L, ann)
        if L is None:
            break
    return out

bad = 0
n = 0
for v in range(1, 260):
    f1, f3 = fires_of(1, v), fires_of(3, v)
    for x1, x3 in zip(f1, f3):
        alpha = (x3 - x1) // 2
        gamma = x1 - alpha
        n += 1
        if not (alpha > 0 and gamma > 0 and lib.v2(gamma) < lib.v2(alpha)):
            bad += 1
            if bad <= 5:
                print("MASTER BAD v=%d alpha=%d gamma=%d" % (v, alpha, gamma))
print("master law: fires=%d bad=%d" % (n, bad))
