"""ADVERSARY probe 8 (final rigor):
 (1) macro-rule (R1-R5) verification that the CHECK5-FAMILY member
     [2301, 2048, 4095] (kap=-1, r0=1, rho=253, u=h=tt=0) halts;
 (2) show the halting child excursion [26,25,...,1600,5246] halts during its
     PREFIX: max canonical v2(H) before the halt stays < 11 (it never reaches
     the template family);
 (3) glue-family member [2301, 2048] (run_glue(253,[0]) at u=h=tt=z=0):
     does it halt?
Run: python -B review_adv_probe8.py
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
    if r1 >= 2 and len(rs) == 1: return h + 1, drop0([r1 - 2, 0, 1])
    if r1 >= 2 and r2 >= 1:     return h + 1, drop0([r1, r2 - 1] + rs[2:])
    if r1 >= 2 and r2 == 0:     return h + 1, drop0([r1 - 2, 0, r3 + 1] + rs[3:])
    if r1 == 1:
        if h == 0: return 'HALT'
        return 0, drop0([h - 1, 0, 1, r3 + 1] + rs[3:])
    return 0, drop0([h + r3 + 3] + rs[3:])

def is_top(h, rs): return h == 0 and (len(rs) == 1 or rs[1] >= 1)

def macro_run(start_list, cap_top=10**6):
    h, rs = 0, list(start_list); t = 0
    assert is_top(h, rs)
    while t < cap_top:
        nxt_expected = T2(rs)
        first = True; halted = False
        while first or not is_top(h, rs):
            nxt = macro_step(h, rs)
            if nxt == 'HALT': halted = True; break
            h, rs = nxt; first = False
        if halted:
            assert nxt_expected == 'HALT'
            return ('HALT', t)
        assert list(rs) == list(nxt_expected), (t, rs[:5], nxt_expected[:5])
        if nxt_expected == 'HALT': return ('HALT', t + 1)
        t += 1
    return ('NOHALT', t)

# (1)
print('(1) macro verification of check5-family member [2301, 2048, 4095]:',
      macro_run([2301, 2048, 4095]))

# (2) prefix analysis of the child [26, 25, 50, 100, 200, 400, 800, 1600, 5246]
L = [26, 25, 50, 100, 200, 400, 800, 1600, 5246]
t = 0; maxv2 = -1; frame = None
while t < 10**6:
    if len(L) >= 3 and L[2] == 2 * L[1]:
        r = 1
        while r + 1 < len(L) and L[r + 1] == L[1] << r: r += 1
        if r + 1 < len(L):
            v2 = 0; x = L[1]
            while x % 2 == 0: v2 += 1; x //= 2
            if v2 > maxv2: maxv2 = v2; frame = (t, L[0], L[1], L[r + 1])
    L = T2(L); t += 1
    if L == 'HALT': break
print('(2) child excursion [26,...,5246]: HALT at step %d; max canonical v2(H) '
      'before halt = %d (family needs >= 11); highest frame %s' % (t, maxv2, frame))

# (3) glue family member
print('(3) glue family member [2301, 2048] = run_glue(253, [0]) at u=h=tt=z=0):',
      macro_run([2301, 2048]))
