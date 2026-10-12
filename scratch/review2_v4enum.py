"""V4: the r=0 deep-branch lineage question.

Arithmetic (H = 0 mod 2^11, canonical states):
  r>=2: kap_child = c' - q0/2 = H - 1                       (class -1 mod 2^11)
  r=1 : kap_child = H + kap - 1                              (class kap - 1)
  r=0 : kap_child = Z0 + (A+1)/2 - q0/2 = Z0 - H - kap - 1   (class Z0 - kap - 1)
q0 = A + 2b + 3 with b = J = H + kap at r=0, so q0 = 3H + 2kap + d + 3
(the deep condition at r=0 shifts: 2kap + d + 3 = 0 mod 2^8).

Part A: enumerate child classes for kap in {-1 mod 2^11} and {-2 mod 2^7},
       Z0 in {0, -1} classes; test membership in family {0,-1} mod 2^11 u
       {-2} mod 2^7.
Part B: concrete instances; run them forward concretely (no halt check).
Part C: targeted synthetic scan for deep r=0/r=1 fires with parent kap in the
       -2 class: starts [H+d, ..., 2^{r0}H + kap] with kap = -2 and kap = 126,
       r0 in {1,2,3}, all rho, tt in {0,1}, w in {1,3}, j in {11,12,13} --
       these are exactly the check5b kapgen=1 family states.
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
from review2_engine import run_tracked, top, v2

FAM = lambda x: (x % 2048 in (0, 2047)) or (x % 128 == 126)

print('=== V4 part A: enumeration of r=0 child classes ===')
print('kap_child = Z0class - kapclass - 1 (mod 2^11), as m ranges:')
for kap_name, kapc in [('-1 mod 2^11', lambda m: -1 + 2048 * m),
                       ('-2 mod 2^7 ', lambda m: -2 + 128 * m)]:
    for z0_name, z0v in [('Z0 = 0 mod 2^11', lambda m: 2048 * m),
                         ('Z0 = -1 mod 2^11', lambda m: 2048 * m - 1)]:
        classes = set()
        for m in range(16):
            for zm in range(2):
                classes.add((z0v(zm) - kapc(m) - 1) % 2048)
        outside = sorted(c for c in classes if not FAM(c))
        inside = sorted(c for c in classes if FAM(c))
        print(' kap %s, %s: %d classes; in-family %s; OUTSIDE %s'
              % (kap_name, z0_name, len(classes), inside, outside))
print(' r=1 comparison: kap_child = H + kap - 1; kap = -2 + 128m -> classes',
      sorted({(0 - 2 + 128 * m - 1) % 2048 for m in range(16)}),
      ' family?', [FAM((128 * m - 3) % 2048) for m in range(2)])

print()
print('=== V4 part B: concrete instances ===')
inst = []
# instance 1: kap = -2 (m=0), Z0 = 2048 (class 0), H = 3*2^11, deep needs d = 1 mod 256
H = 3 * (1 << 11)
for (kap, Z0, d, name) in [(-2, 2048, 1, 'kap=-2(m=0), Z0=0-class'),
                           (-2, 2047, 1, 'kap=-2(m=0), Z0=-1-class'),
                           (126, 2048, 1, 'kap=126(m=1), Z0=0-class'),
                           (126, 2047, 1, 'kap=126(m=1), Z0=-1-class')]:
    A = H + d
    J = H + kap
    L = [A, J, Z0]
    q0 = A + 2 * J + 3
    sp = v2(q0)
    ck = Z0 + (A + 1) // 2 - q0 // 2
    print(' state %s: A=%d odd=%s q0=%d v2=%d deep=%s kap_child=%d class=%d in-family=%s'
          % (L, A, A % 2 == 1, q0, sp, sp >= 8, ck, ck % 2048, FAM(ck)))
    # run it forward concretely
    LL = list(L)
    t = 0
    halted = False
    while t < 3000 and len(LL) > 1:
        LL = top(LL)
        if LL is None:
            halted = True
            break
        t += 1
    print('   -> after %d steps: %s (halted=%s)' % (t, LL[:4], halted))
    inst.append((L, ck))

print()
print('=== V4 part C: targeted synthetic scan (check5b kapgen=1 family states) ===')
t0 = time.time()
deep_r01 = []
deep_outside = 0
deep_total = 0
nrun = 0
halts = 0
for kap in (-2, 126):
    for r0 in (1, 2, 3):
        for rho in range(256):
            for tt in (0, 1):
                d = rho + 256 * tt
                for w in (1, 3):
                    for j in (11, 12, 13):
                        H = 3 * w * (1 << j)
                        L0 = [H + d] + [H << i for i in range(r0)] + [(H << r0) + kap]
                        hits = []
                        def sink(kind, info, L0=L0, hits=hits):
                            if kind == 'fire' and info['r'] in (0, 1):
                                ck = (info['L'][2] if len(info['L']) > 2 else 0) \
                                     + (info['L'][0] + 1) // 2 - info['q0'] // 2
                                if info['sp'] >= 8:
                                    hits.append((info['r'], info['kap'] % 2048, info['sp'],
                                                 ck % 2048, FAM(ck)))
                        res = run_tracked(L0, H, d, kap, r0 + 1, sink, 100000)
                        nrun += 1
                        if res['end'] == 'halt':
                            halts += 1
                        for h in hits:
                            deep_total += 1
                            if not h[4]:
                                deep_outside += 1
                            if len(deep_r01) < 12:
                                deep_r01.append((kap, r0, rho, tt, w, j, h))
print('runs: %d, halts: %d' % (nrun, halts))
print('deep fires at r in {0,1}: %d, of which OUTSIDE-family child: %d' % (deep_total, deep_outside))
for x in deep_r01:
    print('   (kap,r0,rho,tt,w,j, (r, kapclass, sp, childclass, infam)) =', x)
print('elapsed %.1fs' % (time.time() - t0))
