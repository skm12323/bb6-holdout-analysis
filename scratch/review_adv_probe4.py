"""ADVERSARY probe 4: VERIFY THE HALT with three independent engines.

Claim under test: L0 = (2301, 2048, 4094)  [a -2-class lineage-family frame:
  H = 2048 = 2^{K+3}, d = 253 = rho, kap = 4094 - 2*2048 = -2 = -2 + 128*0,
  r0 = 1, empty tail = exactly run_canonical_gen(253, 1, (), kapgen=1) at
  u=h=tt=m=0]  evolves (one top step) to [26, 25, 50, ..., 5245], and THAT
  excursion HALTS after ~2646 top steps.

Engines:
 (1) verify_r8.top  (the artifact's own concrete T)
 (2) an independent re-implementation of T from work_r1/RULES.md section 5
 (3) the R1-R5 MACRO RULES of work_r1/RULES.md section 3, run on the config
     (0; 26, 25, 50, 100, 200, 400, 800, 1600, 5245)  -- ground truth per R1.
Also prints the exact halting configuration.
Run: python -B review_adv_probe4.py
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r8')
import verify_r8 as V

L0 = [2301, 2048, 4094]

# ---- (1) artifact's own concrete top ----
L = list(L0); t = 0; halter = None
while t < 10**7:
    assert L != 'HALT'
    A, b = L[0], (L[1] if len(L) > 1 else 0)
    if A % 2 == 1 and A + 2 * b + 3 in (1 << k for k in range(0, 64)):
        halter = ('engine1', t, list(L), A + 2 * b + 3)
    L = V.top(L); t += 1
    if L == 'HALT': break
print('engine1 (verify_r8.top): HALT after %d top steps; firing config: %s' %
      (t, halter[2] if halter else '??'), '; x = A+2b+3 =', halter[3] if halter else '??')

# ---- (2) independent T from RULES.md section 5 ----
def T2(L):
    A = L[0]; b = L[1] if len(L) > 1 else 0; c = L[2] if len(L) > 2 else 0; S = L[3:]
    if A % 2 == 0: return [A + b + c + 3] + S
    m = b + (A - 3) // 2; st = [c + (A + 1) // 2] + S
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st; m = (m - 3) // 2
    if m == 1: return 'HALT'
    return [m + 4] + st

L = list(L0); t = 0
while t < 10**7:
    L2 = T2(L); t += 1
    if L2 == 'HALT': break
    L = L2
print('engine2 (independent T): HALT after %d top steps' % t)

# ---- (3) R1-R5 macro rules on configs (h; r1..rk) ----
def drop0(rs):
    while rs and rs[-1] == 0: rs.pop()
    return rs

def macro_step(h, rs):
    """one R-row application; returns (h', rs') or 'HALT' (row HALT)."""
    r1 = rs[0]; r2 = rs[1] if len(rs) > 1 else 0
    if r1 >= 2 and len(rs) == 1:
        return h + 1, drop0([r1 - 2, 0, 1])          # R2
    if r1 >= 2 and r2 >= 1:
        return h + 1, drop0([r1 - 1, r2 - 1] + rs[2:])   # R1
    if r1 >= 2 and r2 == 0:
        r3 = rs[2] if len(rs) > 2 else 0
        # (h; x+2, 0, y+1): needs y+1 -> r3 >= 1; y=0 case -> r3=0: REST blank
        # R3 with y+1 = r3: output r3+1
        return h + 1, drop0([r1 - 2, 0, r3 + 1] + rs[3:])   # R3
    if r1 == 1:
        if h == 0:
            return 'HALT'    # (0; 1, 0, y+1) halts (RULES sec.1)
        r3 = rs[2] if len(rs) > 2 else 0
        # R4: (h+1; 1, 0, y+1) -> (0; h, 0, 1, y+2)
        return 0, drop0([h, 0, 1, r3 + 1] + rs[3:])
    # r1 == 0
    r3 = rs[2] if len(rs) > 2 else 0
    return 0, drop0([h + r3 + 4] + rs[3:])            # R5

h, rs = 0, [26, 25, 50, 100, 200, 400, 800, 1600, 5245]
steps = 0; halted = False
while steps < 5 * 10**7:
    nxt = macro_step(h, rs)
    steps += 1
    if nxt == 'HALT': halted = True; break
    h, rs = nxt
print('engine3 (R1-R5 macro rules from (0; 26,25,...,5245)): halted=%s after %d macro steps; final (h; rs) = (%d; %s)'
      % (halted, steps, h, rs[:8]))

# cross-check: macro engine agrees with T2 on the first 5000 top steps from L0
h, rs = 0, list(L0)
L = list(L0); agree = True
for t in range(5000):
    # top config check: h must be 0 at each A0 "top" moment
    tops = 0
    while True:
        nxt = macro_step(h, rs)
        if nxt == 'HALT': break
        h2, rs2 = nxt; h, rs = h2, rs2; tops += 1
        if h == 0 and (len(rs) == 1 or (len(rs) > 1 and rs[1] >= 1)): break
    L = T2(L)
    if L == 'HALT':
        print('   cross-check: T2 HALT at top step %d; macro h=%d rs=%s' % (t, h, rs[:6])); break
    if [0] + list(rs) != [0] + list(L) or rs != list(L):
        agree = False; print('   cross-check MISMATCH at t=%d: macro=%s T2=%s' % (t, rs[:6], L[:6])); break
print('   cross-check macro-vs-T2 (5000 top steps): agree=%s' % agree)
