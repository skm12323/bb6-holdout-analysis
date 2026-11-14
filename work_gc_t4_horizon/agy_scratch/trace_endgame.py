# trace_endgame.py
from independent_verify import get_Xdata, v2, sym_exit

X = get_Xdata(64)

for v in range(3, 7):
    print(f"\n================ v = {v} ================")
    s_exit = sym_exit(v, X)
    print(f"sym_exit({v}): {s_exit}")
    
    typ, A_X, Y_X, eps_X, tau_v1 = X[v - 1]
    print(f"X({v-1}): typ={typ}, A={A_X}, Y={Y_X}, eps={eps_X}, tau={tau_v1}")
    
    # Let's trace the pair endgame from X(v-1)
    D0 = (1 << (v - 1), -1)
    if typ == 'a':
        P = [D0]
    elif typ == 'b':
        P = [Y_X, D0]
    else:
        P = [Y_X, D0]
    
    A = A_X
    step = 0
    while True:
        is_singleton = (len(P) == 0 and (A[0] + A[1]) % 2 == 0)
        print(f"  step {step}: A={A}, P={P}, is_singleton={is_singleton}")
        if is_singleton:
            print(f"Reached singleton at step {step}!")
            break
        
        cb = P[0] if len(P) > 0 else (0, 0)
        cc = P[1] if len(P) > 1 else (0, 0)
        
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb[0] + cc[0], A[1] + cb[1] + cc[1] + 3)
            newp = []
            print(f"    EVEN STEP -> A={A}")
        else:
            cx = A[0] + 2*cb[0]
            lx = A[1] + 2*cb[1] + 3
            vc, vl = v2(cx), v2(lx)
            j = vl
            u = (cx >> j, lx >> j)
            newp = [(u[0] << t, u[1] << t) for t in range(j-1)] + [(cc[0] + A[0]//2, cc[1] + (A[1]+1)//2)]
            A = (u[0], u[1] + 1)
            print(f"    CHAIN STEP j={j}, u={u}")
            
        if len(P) >= 2:
            P = P[2:]
        else:
            P = []
        P = newp + P
        step += 1
        if step > 20:
            break
