"""ADVERSARY probe 7: is check6's assertion vacuous?
prefix_check asserts jmax >= K+3 for t >= 8 ONLY at steps where the list is
canonical-shaped (len>=3 and L[2]==2*L[1]).  If the list is not canonical at
those steps, the assert never fires and the check passes vacuously.
Instrument and count.  Also verify the s-independence claim is only tested
at 3 values of r0 for 9 steps.
Run: python -B review_adv_probe7.py
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r8')
import verify_r8 as V

Hp = 1 << 11
w3 = V._add(V._C(3), V._sym(0, 6))
for r0 in (30, 40, 50):
    J = V._add(V._C(Hp - 1), V._sym(6, Hp))
    L = [V._add(w3, V._C(1))] + [V._sc(w3, 1 << i) for i in range(r0)] + [J]
    canon_ts = []; jmax = 0; fired = 0
    for t in range(20):
        if len(L) >= 3 and L[2] == V._sc(L[1], 2):
            jmax = max(jmax, V._v2f(L[1]))
            canon_ts.append((t, len(L), jmax))
            if t >= 8:
                fired += 1
        L = V._Tm(L)
    print('r0=%2d: canonical-shaped steps (t,len,jmax): %s' % (r0, canon_ts))
    print('        assert fired at %d steps (t>=8); final jmax=%d (need >= 11)' % (fired, jmax))
