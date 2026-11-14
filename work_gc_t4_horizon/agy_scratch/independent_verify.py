# independent_verify.py
# Blind audit independent verification script for Theorem H-T4
# Written by auditor 2 (agy) without reading verify_t4_horizon.py

import sys

def v2(x):
    return (x & -x).bit_length() - 1

# -------------------------------------------------------------
# Part 1: Top map simulation according to work_r1 / work_r4
# -------------------------------------------------------------
def top_step(L):
    # L is a list of integers
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    S = L[3:] if len(L) > 3 else []
    
    # Halting check: A odd and A + 2*b + 3 is a power of 2
    if A % 2 == 1:
        val = A + 2*b + 3
        if (val & (val - 1)) == 0 and val > 0:
            return 'HALT', L
        
        m = b + (A - 3) // 2
        stack = [c + (A + 1) // 2] + S
        while m % 2 == 1 and m >= 3:
            stack.insert(0, (m + 3) // 2)
            m = (m - 3) // 2
        if m == 1:
            return 'HALT', L
        new_L = [m + 4] + stack
    else:
        new_L = [A + b + c + 3] + S
    
    # Strip trailing zeros
    while len(new_L) > 1 and new_L[-1] == 0:
        new_L.pop()
    return 'OK', new_L

def run_top_map(H0):
    total_steps = (1 << H0) - 2
    print(f"Running top map for H0 = {H0} (total steps = {total_steps})...")
    L = [3]
    n = 0
    singletons = 0
    gaps_by_v = {}
    last_singleton = None
    last_v = None
    
    while n < total_steps:
        # Check sum law
        assert sum(L) == 3*n + 3, f"Sum law failed at n={n}"
        
        # Check if singleton
        if len(L) == 1:
            singletons += 1
            if last_singleton is not None and last_v is not None:
                gap = n - last_singleton - 1
                if last_v not in gaps_by_v:
                    gaps_by_v[last_v] = set()
                gaps_by_v[last_v].add(gap)
            
            # Record current singleton
            if n % 2 == 0: # even singleton
                v = v2(n + 2)
                assert v < H0, f"v >= H0 at even singleton n={n}: v={v}"
                last_singleton = n
                last_v = v
            else:
                last_singleton = None
                last_v = None
        
        status, L = top_step(L)
        if status == 'HALT':
            raise AssertionError(f"Top map halted at step n={n}!")
        n += 1
        
    print(f"Top map completed {total_steps} steps without halt. Singletons seen: {singletons}.")
    # Check that gap depends only on v
    print("Verifying gap(v) consistency across all observed occurrences:")
    ell_table = {}
    for v in sorted(gaps_by_v.keys()):
        assert len(gaps_by_v[v]) == 1, f"v={v} has inconsistent gaps: {gaps_by_v[v]}"
        gap_val = next(iter(gaps_by_v[v]))
        ell_table[v] = gap_val
        print(f"  v={v:2d}: unique gap = {gap_val}")
    return ell_table

# -------------------------------------------------------------
# Part 2: F pair walk & Xdata from work_m
# -------------------------------------------------------------
def get_Xdata(max_n):
    A = (1, 1); P = []; i = 0; s = 0
    X = {}; seen = -1
    while seen < max_n:
        ents = [(p[0], p[1]) for p in P[:2]]
        a = i
        while len(ents) < 2:
            ents.append((1 << a, 0))
            a += 1
        (cb_, lb), (cc, lc) = ents
        k = len(P)
        for n in ([i] if k == 1 else [i, i+1] if k == 0 else []):
            if n > seen and n <= max_n:
                seen = n
                if k == 0 and i == n:
                    d = ('a', A, None, 0, s)
                elif k == 0:
                    d = ('b', A, (1 << (n-1), 0), 1, s)
                else:
                    d = ('c', A, P[0], n - v2(A[0]), s)
                X[n] = d
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb_ + cc, A[1] + lb + lc + 3)
            newp = []
        else:
            cx, lx = A[0] + 2*cb_, A[1] + 2*lb + 3
            vc, vl = v2(cx), v2(lx)
            assert vl < vc and A[0] % 2 == 0
            j = vl
            u = (cx >> j, lx >> j)
            newp = [(u[0] << t, u[1] << t) for t in range(j-1)] + [(cc + A[0]//2, lc + (A[1]+1)//2)]
            A = (u[0], u[1] + 1)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k
            P = []
        P = newp + P
        s += 1
    return X

# -------------------------------------------------------------
# Part 3: Symbolic exit S(J) from work_m/verify_m.py
# -------------------------------------------------------------
def sym_exit(J, X):
    INF = 10**18
    vv = lambda z: INF if z == 0 else v2(z)
    js = [J]; typs = ''; G = 0
    u = (1, 0); D = (1 << (J-1), -1); j = J
    for t in range(60):
        n = j - 1
        typ, (cH, lH), Y, eps, tau_n = X[n]
        typs += typ
        H = (cH * u[0], cH * u[1] + lH)
        if Y is not None:
            Yv = (Y[0] * u[0], Y[0] * u[1] + Y[1])
        if (H[0] + H[1]) % 2 == 0:
            return tuple(js), typs, len(js) - 1, G
        G += 1 + eps
        b = D if typ == 'a' else Yv
        x = (H[0] + 2*b[0], H[1] + 2*b[1] + 3)
        va, vb = vv(x[0]), vv(x[1])
        if not vb < va:
            return ('TIE', J, t)
        assert H[0] % 2 == 0 and H[1] % 2 == 1
        j = vb
        u = (x[0] >> j, x[1] >> j)
        Dn = (H[0] // 2, (H[1] + 1) // 2)
        D = Dn if typ == 'a' else (D[0] + Dn[0], D[1] + Dn[1])
        js.append(j)
    return ('LONG', J)

# -------------------------------------------------------------
# Part 4: Pair endgame of E(w, v) starting from X(v-1)
# -------------------------------------------------------------
def run_pair_endgame(v, X):
    typ, A_X, Y_X, eps_X, tau_v1 = X[v - 1]
    s_exit = sym_exit(v, X)
    assert not isinstance(s_exit[0], str), f"S({v}) tie or long: {s_exit}"
    s_js, s_typs, s_r, s_G = s_exit
    
    D0 = (1 << (v - 1), -1)
    if typ == 'a':
        P = [D0]
    else:
        P = [Y_X, D0]
    
    A = A_X
    chains_j = []
    endgame_steps = 0
    
    while True:
        # If queue P is empty, the list has length 1: singleton reached!
        if len(P) == 0:
            break
        
        cb = P[0] if len(P) > 0 else (0, 0)
        cc = P[1] if len(P) > 1 else (0, 0)
        
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb[0] + cc[0], A[1] + cb[1] + cc[1] + 3)
            newp = []
        else:
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
        if endgame_steps > 500:
            raise AssertionError(f"Endgame runaway for v={v}")
            
    assert tuple([v] + chains_j) == s_js, f"v={v} endgame chains {chains_j} != S(v) {s_js}"
    return tau_v1, endgame_steps, tau_v1 + endgame_steps, A

# -------------------------------------------------------------
# Main driver
# -------------------------------------------------------------
if __name__ == '__main__':
    H0 = 18
    print(f"=== 1. Top map verification at H0 = {H0} ===")
    ell_table = run_top_map(H0)
    
    print("\n=== 2. Crossings data computation ===")
    X = get_Xdata(64)
    print("Recorded crossings up to n=64.")
    
    print("\n=== 3. Endgame vs S(v) cross-check for v = 3..8 ===")
    for v in range(3, 9):
        tau_v1, eg_len, total_gap, final_A = run_pair_endgame(v, X)
        expected_gap = ell_table[v]
        print(f"  v={v}: tau(v-1)={tau_v1}, endgame_len={eg_len}, total_gap={total_gap}, top_map_gap={expected_gap}, final_A={final_A}")
        assert total_gap == expected_gap, f"v={v} gap mismatch: total={total_gap} != top_map={expected_gap}"
        assert final_A[0] == (1 << v)
        assert final_A[1] == 3 * expected_gap
    print("All pair endgame runs match S(v) chain-for-chain, and gap == tau(v-1) + endgame_len!")
    
    print("\n=== 4. Check ell(1..20) against work_r4/PROOF.md:40 ===")
    r4_ell = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]
    for v in range(1, len(r4_ell) + 1):
        if v in ell_table:
            assert ell_table[v] == r4_ell[v-1], f"ell({v})={ell_table[v]} != r4_ell={r4_ell[v-1]}"
            print(f"  ell({v:2d}) = {ell_table[v]} == R4 table {r4_ell[v-1]}: PASS")
    print("ALL INDEPENDENT VERIFICATIONS SUCCEEDED (H0=18 scale).")
