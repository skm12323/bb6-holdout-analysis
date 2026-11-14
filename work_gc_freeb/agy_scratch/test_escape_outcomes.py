import sys
from collections import Counter
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2, INF
from fractions import Fraction as F

cal = Cal()
gj = [5, 8, 12]

escape_outcomes = Counter()

for j in gj:
    k_j = cal.k(j)
    c_Th = 2**(j - 2) + 3 * (k_j + 1)
    for m in range(j, 5000):
        r_m = cal.row(m - 1)
        if not r_m['odd']:
            continue
        
        # step 1 at m
        Th = F(c_Th)
        C = F(2**m)
        A = F(0)
        B = F(2**(m + 1))
        
        kind = r_m['kind']
        if kind == 'a':
            k_m = r_m['tau'] // 2
            loss = 1
            C_next = 2 * Th + 6 * k_m - C / 2
            Th_next = Th + 3 + 6 * k_m
            A_next = 2**j - A / 2
            B_next = -B / 2
        else:
            loss = 1 + r_m['eps']
            C_next = r_m['R'] * C + r_m['lam']
            Th_next = Th + 3 + 3 * r_m['tau']
            A_next = r_m['R'] * A
            B_next = r_m['R'] * B
        
        vc = v2(C_next)
        vB = v2(B_next)
        vA = INF if A_next == 0 else v2(A_next)
        vs = min(vA, vB)
        
        c1 = vc
        if c1 >= j - 1:
            # This is an escape landing
            # What is the outcome of the postgate walk?
            # If vc < vs: determined landing at c1.
            # Then what happens at c1?
            if vc < vs:
                # c1 is determined
                # Does the walk continue from c1?
                q = c1
                Th = Th_next
                C = C_next
                A = A_next
                B = B_next
                ell = loss
                run_bc = False if kind == 'a' else True
                L_bc = 0 if kind == 'a' else loss
                
                # Walk forward until END, SPLIT, or GATE
                status = None
                for _ in range(400):
                    if q <= 4:
                        status = 'END'
                        break
                    r_q = cal.row(q - 1)
                    if not r_q['odd']:
                        status = 'END'
                        break
                    knd = r_q['kind']
                    if knd == 'a':
                        kq = r_q['tau'] // 2
                        ls = 1
                        if run_bc: run_bc = False
                        Cn = 2 * Th + 6 * kq - C / 2
                        Thn = Th + 3 + 6 * kq
                        An = 2**j - A / 2
                        Bn = -B / 2
                    else:
                        ls = 1 + r_q['eps']
                        if run_bc: L_bc += ls
                        Cn = r_q['R'] * C + r_q['lam']
                        Thn = Th + 3 + 3 * r_q['tau']
                        An = r_q['R'] * A
                        Bn = r_q['R'] * B
                    
                    nl = ell + ls
                    v_B = v2(Bn)
                    v_A = INF if An == 0 else v2(An)
                    v_s = min(v_A, v_B)
                    v_c = v2(Cn)
                    if v_c < v_s:
                        prev = q
                        q = v_c
                        Th = Thn; C = Cn; A = An; B = Bn; ell = nl
                        if knd == 'a' and q >= prev:
                            status = 'GATE'
                            break
                    else:
                        status = 'SPLIT'
                        break
                escape_outcomes[status] += 1
            else:
                escape_outcomes['SPLIT'] += 1

print(f"Escape outcomes: {escape_outcomes}")
