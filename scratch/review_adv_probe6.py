"""ADVERSARY probe 6:
 (a) show the symbolic TemplateChecker literally returns ('DEEP', ...) on a
     start whose concrete dynamics HALTS (the certificate is vacuous there);
 (b) concrete scan of the CHECK5 FAMILY ITSELF (kap = -1): starts
     (H+d, H, 2H, ..., 2^{r0}H - 1) + [], d = 253 + 256*tt (the deep residue),
     for many H (incl. 3-divisible) -- do they halt?
 (c) real orbit: deep moments (A odd, v2(A+2b+3) >= 8) by r-shape, and the
     full J-class histogram at canonical 2^11|H frames.
Run: python -B review_adv_probe6.py [ORBIT=6000000] [CAP=400000]
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r8')
import verify_r8 as V

def T2(L):
    A = L[0]; b = L[1] if len(L) > 1 else 0; c = L[2] if len(L) > 2 else 0; S = L[3:]
    if A % 2 == 0: return [A + b + c + 3] + S
    m = b + (A - 3) // 2; st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st; m = (m - 3) // 2
    if m == 1: return 'HALT'
    return [m + 4] + st

# ---- (a) symbolic checker on halting starts ---------------------------------
tc = V.TemplateChecker(KK=8)
for (rho, r0, kapoff) in ((253, 1, -2), (253, 1, -1)):
    if kapoff == -2:
        res = tc.run_canonical_gen(253, r0, (), 1)
    else:
        res = tc.run_canonical(253, r0, ())
    print('(a) symbolic run (rho=%d, r0=%d, kap class %d): result = %s  <-- "passes"'
          % (rho, r0, kapoff, res if not isinstance(res, tuple) else res[:2]))

# ---- (b) concrete scan of the kap=-1 (check5) family at rho=253 -------------
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 400000
print('(b) check5 family (kap=-1), d = 253 + 256*tt, tail = [], cap = %d steps:' % CAP)
halters = 0; total = 0
for r0 in (1, 2, 3, 4, 5):
    for k in range(1, 13):
        H = 2048 * k
        for tt in range(4):
            d = 253 + 256 * tt
            L = [H + d] + [H << i for i in range(r0)] + [(H << r0) - 1]
            t = 0
            while t < CAP:
                L = T2(L); t += 1
                if L == 'HALT': break
            total += 1
            if L == 'HALT':
                halters += 1
                print('    HALT: r0=%d H=%d (3|H:%s) tt=%d d=%d after %d steps'
                      % (r0, H, H % 3 == 0, tt, d, t))
print('    => %d/%d family members (kap=-1, rho=253) HALT' % (halters, total))

# ---- (c) real orbit ----------------------------------------------------------
ORBIT = int(sys.argv[1]) if len(sys.argv) > 1 else 6000000
L = [3]; n = 0
deep_by_r = {}; klass = {}
while n < ORBIT:
    A = L[0]; b = L[1] if len(L) > 1 else 0
    if A % 2 == 1:
        x = A + 2 * b + 3
        if x % 256 == 0:   # v2 >= 8 (deep-ish moment)
            # r-shape
            if len(L) >= 3 and L[2] == 2 * L[1]:
                r = 1
                while r + 1 < len(L) and L[r + 1] == L[1] << r: r += 1
                sh = 'r=%d' % r if r + 1 < len(L) else 'pure'
            else:
                sh = 'noncanon'
            deep_by_r[sh] = deep_by_r.get(sh, 0) + 1
    if len(L) >= 3 and L[2] == 2 * L[1]:
        r = 1
        while r + 1 < len(L) and L[r + 1] == L[1] << r: r += 1
        if r + 1 < len(L) and L[1] % 2048 == 0:
            kap = (L[r + 1] - (L[1] << r)) % 2048
            klass[kap] = klass.get(kap, 0) + 1
    L = T2(L); n += 1
    if L == 'HALT':
        print('!!! ORBIT HALTS at n=%d !!!' % n); break
print('(c) orbit n<%d: deep moments (v2(x)>=8) by shape: %s' % (ORBIT, deep_by_r))
print('    J-classes at canonical 2^11|H frames (class: count): %s' % sorted(klass.items()))
