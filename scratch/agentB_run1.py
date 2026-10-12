"""agentB_run1.py — verification of basics against the audited facts."""
import random
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import *

def main():
    # 1. cross-check fast closed form vs audited reference on the real orbit
    L1 = [3]; L2 = [3]; ok = True
    for i in range(5000):
        L1, d1 = top_step_fast(L1)
        L2, d2 = top_step_ref(L2)
        if L1 != L2 or (d1[0] == 'C') != (d2[0] == 'C'):
            ok = False; print('MISMATCH at step', i); break
        if L1 is None:
            break
    print('[check] closed form == audited spec on orbit from (3), 5000 steps:', ok)

    random.seed(12345); ok2 = True
    for _ in range(20000):
        n = random.randint(1, 8)
        L = [random.randint(0, 60) for _ in range(n)]
        a1, _ = top_step_fast(L)
        a2, _ = top_step_ref(L)
        if a1 != a2:
            ok2 = False; print('rand mismatch', L); break
    print('[check] closed form == audited spec on 20000 random states:', ok2)

    # 2. orbit from (3): sum invariant, no halt, E-formula, ell consistency
    L = [3]; n = 0; sums_ok = True; echecks = 0; N = 100000
    ellmap = {}
    while n < N:
        if sum(L) != 3 * n + 3:
            sums_ok = False; print('SUM FAIL n=', n); break
        if len(L) == 1:
            assert L[0] == 3 * n + 3
            if n % 2 == 0:
                # next state must be E(w,v), n+2 = 2^v w
                m = n + 2; v = v2i(m); w = m >> v
                L2_, _ = top_step_fast(L)
                if L2_ != E_list(w, v):
                    print('E-FORMULA FAIL n=', n); sums_ok = False; break
                echecks += 1
        L, d = top_step_fast(L)
        if d[0] == 'HALT':
            print('HALT at n =', n); break
        n += 1
    print('[check] orbit from (3) for', N, 'steps: sum invariant + E-formula ok:', sums_ok,
          ' (E-checks:', echecks, ')')

    # 3. ell table
    ells = {}
    for v in range(1, 65):
        r = excursion(1, v)
        assert r['result'] == 'singleton', (v, r)
        ells[v] = r['ell']
    known = [1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16]
    print('[check] ell(1..20) matches given:', [ells[v] for v in range(1,21)] == known)
    print('ell(1..64) =', [ells[v] for v in range(1,65)])

    # 4. excursions: w-independence of ell and no halt, v<=300, w in {1,3,5,7,9}
    bad = 0
    for v in range(1, 301):
        for w in (1, 3, 5, 7, 9):
            r = excursion(w, v)
            if r['result'] != 'singleton' or r['ell'] != ells[v if v <= 64 else None] if False else (r['result'] != 'singleton'):
                bad += 1; print('EXCURSION ISSUE v,w=', v, w, r['result'])
            elif v <= 64 and r['ell'] != ells[v]:
                bad += 1; print('ELL DEPENDS ON w: v,w=', v, w, r['ell'], ells[v])
    print('[check] excursions v<=300, w in {1,3,5,7,9}: all singleton, ell w-independent, bad =', bad)

    # 5. symbolic engine: safety + agreement with numeric shapes
    symok = True
    for v in range(1, 301):
        r = excursion_sym(v)
        if r['result'] != 'singleton':
            print('SYM ISSUE v=%d:' % v, r['result'], r.get('msg'))
            symok = False; break
        rn = excursion(1, v)
        if rn['ell'] != r['ell']:
            print('SYM ELL MISMATCH v=', v, rn['ell'], r['ell']); symok = False; break
        # shape: numeric j-sequence (w=1,3,5) equals symbolic
        for w in (1, 3, 5):
            rw = excursion(w, v)
            js_num = [d[1] for d in rw['descs'] if d[0] == 'C']
            js_sym = [c[1] for c in r['chains']]
            if js_num != js_sym:
                print('SHAPE MISMATCH v,w =', v, w); symok = False; break
            # u values: u_w = eval(u_pair, (w-1)/2)
            for (idx, j, up), dn in zip(r['chains'], [d for d in rw['descs'] if d[0]=='C']):
                if eval_pair(up, (w-1)//2) != dn[2]:
                    print('U MISMATCH v,w=', v, w); symok = False; break
            if not symok: break
        if not symok: break
    print('[check] symbolic engine v<=300: safe, ell+shape+u match numeric for w=1,3,5:', symok)

if __name__ == '__main__':
    main()
