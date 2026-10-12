"""Extract every fire family as an affine form x = alpha*w + gamma
(w = odd part of excursion parameter), verify affinity, and test whether
x = 2^K can hold for any odd w >= 1 (halting).  Exclusion test:
  - if alpha even and gamma odd: impossible (parity)  [clean]
  - if v2(gamma) < v2(alpha): 2^K = alpha w + gamma requires
        2^K ≡ gamma (mod 2^{v2(alpha)+1}) ... we test all K <= 200 directly
        via 2^K ≡ gamma (mod alpha') for the odd part and 2-adic part.
  Direct approach: for K in 1..400: check (2^K - gamma) % alpha == 0 and
  w = (2^K-gamma)//alpha odd >= 1.  Families with a solution are listed as
  'ARITHMETICALLY POSSIBLE' (then halting needs that w actually occurs at
  that excursion -- cross-check by simulation)."""
import agentC_lib as lib
from collections import defaultdict

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
            out.append((s, L[0] + 2 * L[1] + 3))
        L, ann = step_ann(L, ann)
        if L is None:
            break
    return out

# family = (v, step index) -> (alpha, gamma) via w=1,3; verify on w=5,7,9
fams = {}
affine_fail = 0
VMAX = 400
for v in range(1, VMAX + 1):
    f1 = fires_of(1, v)
    f3 = fires_of(3, v)
    if len(f1) != len(f3):
        print("length mismatch v=%d" % v)
        continue
    for (s1, x1), (s3, x3) in zip(f1, f3):
        if s1 != s3:
            print("step mismatch v=%d" % v)
            break
        if (x3 - x1) % 2 != 0:
            affine_fail += 1
            print("non-integer alpha v=%d s=%d" % (v, s1))
            continue
        alpha = (x3 - x1) // 2
        gamma = x1 - alpha
        fams[(v, s1)] = (alpha, gamma)
# verify affinity on w=5,7,9,11
bad = 0
for w in (5, 7, 9, 11, 21, 101):
    for v in range(1, min(VMAX, 250) + 1):
        for (s, x) in fires_of(w, v):
            key = (v, s)
            if key in fams:
                alpha, gamma = fams[key]
                if x != alpha * w + gamma:
                    bad += 1
                    if bad < 10:
                        print("AFFINITY FAIL w=%d v=%d s=%d: x=%d expect %d" %
                              (w, v, s, x, alpha * w + gamma))
print("families:", len(fams), "affinity failures:", bad)

# exclusion test per family
possible = []
clean = 0
other = 0
for key, (alpha, gamma) in sorted(fams.items()):
    # solve alpha*w + gamma = 2^K, w odd >= 1
    sols = []
    if alpha != 0:
        for K in range(3, 402):
            t = (1 << K) - gamma
            if t % alpha == 0:
                wv = t // alpha
                if wv >= 1 and wv % 2 == 1:
                    sols.append((K, wv))
    if sols:
        possible.append((key, alpha, gamma, sols[:4]))
    else:
        if alpha % 2 == 0 and gamma % 2 == 1:
            clean += 1
        else:
            other += 1
print("clean parity-excluded families:", clean, " other excluded:", other)
print("families with arithmetic solutions:", len(possible))
for key, alpha, gamma, sols in possible[:40]:
    print("   v=%d step=%d alpha=%d gamma=%d sols(K,w)=%s" % (key[0], key[1], alpha, gamma, sols))
