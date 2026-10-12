"""ADVERSARY probe 5:
 (1) corrected R1-R5 macro engine (R1: r1 preserved; R4: h-1; R5: h+r3+3),
     cross-checked step-by-step against T2 for the halting trajectory, then
     full macro-run to the halt.
 (2) family halt scan: which concrete (-2-class) frames halt? incl. H
     divisible by 3 (real-looking H = 3w 2^j is 3-divisible).
 (3) real-orbit scan from (3): do -2-class canonical frames (2^11 | H)
     ever occur, with what (r0, rho); is the halting combo
     (r0=1, kap=-2 mod 2^7, rho=253) ever hit?
Run: python -B review_adv_probe5.py [ORBIT=3000000]
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

def drop0(rs):
    while rs and rs[-1] == 0: rs.pop()
    return rs

def macro_step(h, rs):
    r1 = rs[0]; r2 = rs[1] if len(rs) > 1 else 0
    r3 = rs[2] if len(rs) > 2 else 0
    if r1 >= 2 and len(rs) == 1:
        return h + 1, drop0([r1 - 2, 0, 1])                     # R2
    if r1 >= 2 and r2 >= 1:
        return h + 1, drop0([r1, r2 - 1] + rs[2:])              # R1
    if r1 >= 2 and r2 == 0:
        return h + 1, drop0([r1 - 2, 0, r3 + 1] + rs[3:])       # R3
    if r1 == 1:
        if h == 0: return 'HALT'
        return 0, drop0([h - 1, 0, 1, r3 + 1] + rs[3:])         # R4
    return 0, drop0([h + r3 + 3] + rs[3:])                      # R5

def is_top(h, rs):
    return h == 0 and (len(rs) == 1 or rs[1] >= 1)

# ---- (1) macro-run from the child excursion, cross-checked vs T2 ----------
L0 = V.top([2301, 2048, 4094])
h, rs = 0, list(L0)
L = list(L0); t_top = 0; msteps = 0; halted = False
while t_top < 10**5:
    if list(rs) != list(L):
        print('MISMATCH top step %d: macro=%s T2=%s' % (t_top, rs[:6], L[:6])); sys.exit(1)
    Lnext = T2(L)
    if Lnext == 'HALT':
        # confirm the macro engine also hits the HALT row from here
        hh, rr = h, rs; got = None
        for _ in range(10**7):
            nxt = macro_step(hh, rr)
            if nxt == 'HALT': got = True; break
            hh, rr = nxt
        print('   T2 says HALT from %s; macro engine says HALT=%s' % (L[:6], got))
        halted = True; break
    # advance macros to the next top config
    first = True
    while first or not is_top(h, rs):
        nxt = macro_step(h, rs); msteps += 1
        if nxt == 'HALT': halted = True; break
        h, rs = nxt; first = False
    if halted:
        print('   macro engine hit HALT row before the next top config'); break
    L = Lnext; t_top += 1
print('(1) macro engine: matches T2 for %d top steps; HALT=%s after %d macro steps '
      '(final top config %s)' % (t_top, halted, msteps, rs[:6]))

# ---- (2) family halt scan ---------------------------------------------------
print('(2) concrete -2-class canonical frames (H+d, H, 2H-2), r0=1, d=253+256tt:')
for H in (2048, 4096, 6144, 8192, 10240, 12288, 20480, 61440):
    row = []
    for tt in range(4):
        d = 253 + 256 * tt
        L = [H + d, H, 2 * H - 2]; t = 0
        while t < 300000:
            L = T2(L); t += 1
            if L == 'HALT': break
        row.append('HALT@%d' % t if L == 'HALT' else 'no(%d%s)' % (t, '' if len(L) > 1 else ',single'))
    print('    H=%6d (3|H: %s): d=253,509,765,1021 -> %s' % (H, H % 3 == 0, row))

# ---- (3) real-orbit scan from (3) -------------------------------------------
ORBIT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000000
L = [3]; n = 0
hist = {}; hits22 = []
jmax_seen = 0
while n < ORBIT:
    # canonical frame?
    if len(L) >= 3 and L[2] == 2 * L[1]:
        r = 1
        while r + 1 < len(L) and L[r + 1] == L[1] << r: r += 1
        if r + 1 < len(L):
            H = L[1]; kap = L[r + 1] - (H << r); d = L[0] - H
            if H % 2048 == 0:
                key = (min(r, 6), kap % 128, d % 256)
                hist[key] = hist.get(key, 0) + 1
                if (kap + 2) % 128 == 0:
                    hits22.append((n, r, H, d, kap))
                    if len(hits22) <= 5:
                        print('    -2-class frame at n=%d: r=%d H=%d d=%d kap=%d  (rho=%d)'
                              % (n, r, H, d, kap, d % 256))
    L = T2(L); n += 1
    if L == 'HALT':
        print('!!! REAL ORBIT FROM (3) HALTS at top step %d !!!' % n); break
print('(3) orbit scan n < %d: no halt; %d canonical 2^11|H frames; -2-class frames: %d'
      % (ORBIT, sum(hist.values()), len(hits22)))
m2 = [k for k in hist if (k[1] + 2) % 128 == 0]
print('    kap-class=-2 (mod 2^7) frames by (r0capped, kapclass, rho): %s'
      % sorted(m2)[:20])
combo = [k for k in hist if k[0] == 1 and (k[1] + 2) % 128 == 0 and k[2] == 253]
print('    HALTING COMBO (r=1, kap=-2, rho=253) seen: %s' % (combo or 'NO'))
