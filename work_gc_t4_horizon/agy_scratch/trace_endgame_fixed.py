# trace_endgame_fixed.py
from independent_verify import get_Xdata, v2, sym_exit

X = get_Xdata(64)
r4_ell = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]

for v in range(3, 9):
    print(f"\n================ v = {v} ================")
    s_exit = sym_exit(v, X)
    s_js, s_typs, s_r, s_G = s_exit
    print(f"sym_exit({v}): js={s_js}, typs={s_typs}, r={s_r}, G={s_G}")
    
    typ, A_X, Y_X, eps_X, tau_v1 = X[v - 1]
    D0 = (1 << (v - 1), -1)
    if typ == 'a':
        P = [D0]
    else: # type b or c
        P = [Y_X, D0]
    
    A = A_X
    chains_j = []
    endgame_steps = 0
    
    while True:
        # If P is empty, the current list has only 1 entry: A is the singleton!
        if len(P) == 0:
            print(f"Reached singleton at step {endgame_steps}! Head = {A}")
            break
        
        cb = P[0] if len(P) > 0 else (0, 0)
        cc = P[1] if len(P) > 1 else (0, 0)
        
        if (A[0] + A[1]) % 2 == 0:
            # Even step
            A = (A[0] + cb[0] + cc[0], A[1] + cb[1] + cc[1] + 3)
            newp = []
        else:
            # Chain step
            cx = A[0] + 2*cb[0]
            lx = A[1] + 2*cb[1] + 3
            vc, vl = v2(cx), v2(lx)
            assert vl < vc, f"S1 failed in endgame: vl={vl}, vc={vc}"
            assert A[0] % 2 == 0, f"S2 failed in endgame: A[0]={A[0]}"
            j = vl
            chains_j.append(j)
            u = (cx >> j, lx >> j)
            newp = [(u[0] << t, u[1] << t) for t in range(j-1)] + [(cc[0] + A[0]//2, cc[1] + (A[1]+1)//2)]
            A = (u[0], u[1] + 1)
            
        if len(P) >= 2:
            P = P[2:]
        else:
            P = []
        P = newp + P
        endgame_steps += 1
    
    expected_ell = r4_ell[v - 1]
    print(f"v={v}: tau(v-1)={tau_v1}, endgame_steps={endgame_steps}, total={tau_v1 + endgame_steps}, ell(v)={expected_ell}")
    print(f"chains_j: {[v] + chains_j} vs s_js: {list(s_js)}")
    assert tuple([v] + chains_j) == s_js
    assert tau_v1 + endgame_steps == expected_ell
    # Check singleton value (2^v, 3*ell) from Lemma E4
    assert A[0] == (1 << v), f"c part of singleton != 2^{v}: {A[0]}"
    assert A[1] == 3 * expected_ell, f"lambda part of singleton != 3*ell: {A[1]}"
    print(f"v={v} ALL CHECKS PASS!")
