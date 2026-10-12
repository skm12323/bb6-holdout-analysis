"""Confirm the uniform exclusion mechanism: for every fire family
x = alpha*w + gamma, check v2(gamma) < v2(alpha) (gamma>0) or the explicit
gamma<0 exclusion.  Extend to v <= 1500.  Also verify q >= 3 for huge w."""
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

def fires_of(w, v):
    L, ann = E(w, v)
    out = []
    for s in range(10 ** 5):
        if len(L) == 1:
            break
        if L[0] % 2 == 1:
            out.append((s, L[0] + 2 * L[1] + 3, lib.v2(L[0] + 2 * L[1] + 3)))
        L, ann = step_ann(L, ann)
        if L is None:
            break
    return out

mech = Counter()
viol = []
VMAX = 1500
nfam = 0
for v in range(1, VMAX + 1):
    f1 = fires_of(1, v)
    f3 = fires_of(3, v)
    for (s1, x1, k1), (s3, x3, k3) in zip(f1, f3):
        alpha = (x3 - x1) // 2
        gamma = x1 - alpha
        nfam += 1
        assert alpha > 0
        if gamma > 0:
            if lib.v2(gamma) < lib.v2(alpha):
                mech["v2(gamma)<v2(alpha), gamma>0"] += 1
            else:
                mech["VIOLATION gamma>0"] += 1
                viol.append((v, s1, alpha, gamma))
        elif gamma == 0:
            mech["gamma==0"] += 1
            viol.append((v, s1, alpha, gamma))
        else:
            # gamma<0: exclusion iff (1-gamma') not divisible... explicit:
            vv = lib.v2(-gamma)
            # alpha*w + gamma = 2^K  <=>  (alpha>>? ) solve small K brute force
            sol = None
            for K in range(3, 600):
                t = (1 << K) - gamma
                if t % alpha == 0 and (t // alpha) % 2 == 1 and t // alpha >= 1:
                    sol = (K, t // alpha)
                    break
            if sol is None:
                # also check giant solution w=(1-gamma')/alpha' criterion
                g2 = -gamma >> vv
                a2 = alpha >> vv
                # need odd a2*w = ... solution exists iff (g2+1) % a2 == 0 and odd
                if a2 % 2 == 1 and (g2 + 1) % a2 == 0 and ((g2 + 1) // a2) % 2 == 1:
                    mech["gamma<0 ARITH SOLUTION"] += 1
                    viol.append((v, s1, alpha, gamma))
                else:
                    mech["gamma<0 excluded"] += 1
            else:
                mech["gamma<0 SMALL SOLUTION"] += 1
                viol.append((v, s1, alpha, gamma, sol))
print("families analyzed:", nfam)
print("mechanisms:", dict(mech))
print("violations:", len(viol))
for x in viol[:20]:
    print("   ", x)

# huge-w spot check: q>=3 for all fires of E(W,v), W = 10^30+1 odd, v<=300
W = 10 ** 30 + 1
badq = 0
for v in range(1, 301):
    for (s, x, k) in fires_of(W, v):
        if (x >> k) < 3:
            badq += 1
            print("SMALL q at v=%d s=%d q=%d" % (v, s, x >> k))
print("huge-w small-q fires:", badq)
