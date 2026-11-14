import sys
from collections import Counter
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2, INF
from fractions import Fraction as F

cal = Cal()

# Find all odd-a j < 40
gj = [j for j in range(5, 40) if cal.k(j) is not None]
print(f"Odd-a chains j < 40: {gj}")

counts = Counter()
n_gates = 0
n_boundary = 0

for j in gj:
    k_j = cal.k(j)
    c_Th = 2**(j - 2) + 3 * (k_j + 1)
    
    for m in range(j, j + 200):
        # We only continue if X(m-1) is odd
        r_m = cal.row(m - 1)
        if not r_m['odd']:
            counts['m_even'] += 1
            continue
        
        counts['pairs_tested'] += 1
        
        # Start state
        Th = F(c_Th)
        C = F(2**m)
        A = F(0)
        B = F(2**(m + 1))
        ell = 0
        L_bc = 0
        run_bc = True
        
        q = m
        terminated = False
        
        for step_idx in range(400):
            if q <= 4:
                counts['END_q_le_4'] += 1
                terminated = True
                break
            r = cal.row(q - 1)
            if not r['odd']:
                counts['END_even'] += 1
                terminated = True
                break
            
            kind = r['kind']
            if kind == 'a':
                k_q = r['tau'] // 2
                loss = 1
                if run_bc:
                    run_bc = False
                C_next = 2 * Th + 6 * k_q - C / 2
                Th_next = Th + 3 + 6 * k_q
                A_next = 2**j - A / 2
                B_next = -B / 2
            else:
                loss = 1 + r['eps']
                if run_bc:
                    L_bc += loss
                C_next = r['R'] * C + r['lam']
                Th_next = Th + 3 + 3 * r['tau']
                A_next = r['R'] * A
                B_next = r['R'] * B
            
            new_ell = ell + loss
            
            # Check FB-1 invariants
            vB = v2(B_next)
            assert vB == m + 1 - new_ell, f"FB-1 B invariant: {vB} != {m + 1 - new_ell}"
            counts['FB1_B_checks'] += 1
            
            if A_next == 0:
                vs = vB
                vA = INF
                counts['FB1_A_zero_checks'] += 1
            else:
                vA = v2(A_next)
                expected_vA = j - new_ell + L_bc + 1
                assert vA == expected_vA, f"FB-1 A invariant: {vA} != {expected_vA}"
                vs = min(vA, vB)
                counts['FB1_A_checks'] += 1
            
            vc = v2(C_next)
            
            # Check FB-2
            if vc < vs:
                # Determined
                counts['FB2_det_steps'] += 1
                q_next = vc
                prev_q = q
                q = q_next
                Th = Th_next
                C = C_next
                A = A_next
                B = B_next
                ell = new_ell
                
                # Check gate
                if kind == 'a' and q_next >= prev_q:
                    # True NT gate G'
                    n_gates += 1
                    counts['GATE_found'] += 1
                    m_prime = q_next
                    assert m_prime == vc < min(vA, vB)
                    dR = m_prime + 1 + ell - j
                    assert dR <= 1 + L_bc, f"DR' failed: dR={dR} > 1+L_bc={1+L_bc}"
                    counts['FB3_DRp_checks'] += 1
                    
                    is_boundary = (dR >= 1)
                    div = (vc >= j - ell)
                    assert is_boundary == div, f"Boundary iff div failed: {is_boundary} != {div}"
                    counts['FB3_boundary_iff_div_checks'] += 1
                    
                    if is_boundary:
                        n_boundary += 1
                        print(f"Boundary gate found! j={j}, m={m}, m'={m_prime}, dR={dR}")
                    terminated = True
                    break
            else:
                # Split
                counts['SPLIT_steps'] += 1
                terminated = True
                break
        
        if not terminated:
            counts['LIMIT'] += 1

print("\n--- Summary of sample census (j<40, m<j+200) ---")
for k, v in sorted(counts.items()):
    print(f"  {k}: {v}")
print(f"Total determined gates: {n_gates}")
print(f"Total boundary gates: {n_boundary}")
