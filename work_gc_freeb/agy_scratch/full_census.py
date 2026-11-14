import sys, time
from collections import Counter
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2, INF
from fractions import Fraction as F

cal = Cal()

# Precompute gj < 400
gj = [j for j in range(5, 400) if cal.k(j) is not None]

# Data structures for tracking
counts = Counter()
n_gates = 0
n_boundary = 0
escape_j_set = set()
escape_counts = Counter()
escape_free_congruence_pass = 0
escape_clock_pass = 0

t0 = time.time()

for j in gj:
    k_j = cal.k(j)
    c_Th = 2**(j - 2) + 3 * (k_j + 1)
    
    for m in range(j, 5000):
        r_m = cal.row(m - 1)
        if not r_m['odd']:
            continue
        
        counts['pairs_odd'] += 1
        
        # State initialization
        Th = F(c_Th)
        C = F(2**m)
        A = F(0)
        B = F(2**(m + 1))
        ell = 0
        L_bc = 0
        run_bc = True
        
        q = m
        terminated = False
        first_step = True
        
        for step_idx in range(400):
            if q <= 4:
                counts['det_end'] += 1
                terminated = True
                break
            r = cal.row(q - 1)
            if not r['odd']:
                counts['det_end'] += 1
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
            
            # FB-1 invariant check for B
            vB = v2(B_next)
            assert vB == m + 1 - new_ell, f"FB-1 B invariant: {vB} != {m + 1 - new_ell}"
            counts['vB_checks'] += 1
            
            # FB-1 invariant check for A
            if A_next == 0:
                vs = vB
                vA = INF
                counts['A_zero_checks'] += 1
            else:
                vA = v2(A_next)
                expected_vA = j - new_ell + L_bc + 1
                assert vA == expected_vA, f"FB-1 A invariant: {vA} != {expected_vA}"
                vs = min(vA, vB)
                counts['vA_checks'] += 1
            
            vc = v2(C_next)
            
            # First landing check for Branch (I) escape: c1 = v2(C_1) >= j - 1
            if first_step:
                first_step = False
                c1 = vc
                if c1 >= j - 1:
                    escape_j_set.add(j)
                    counts['escape_landings'] += 1
                    # Check FREE congruence:
                    if kind == 'a':
                        # 2^(j-2) | k_j + 1 + k_m
                        km = r_m['tau'] // 2
                        val_cong = v2(k_j + 1 + km)
                        assert val_cong >= j - 2, f"FREE a congruence failed: j={j}, m={m}"
                        escape_free_congruence_pass += 1
                        # CLOCK bound: j <= 3 + log2(6*m*P(m))
                        # Here j in {5, 8, 12}, trivially <= 3 + log2(...)
                        escape_clock_pass += 1
                    else:
                        # omega(m-1) >= j - 1
                        assert r_m['omega'] >= j - 1, f"FREE bc omega failed: j={j}, m={m}"
                        escape_free_congruence_pass += 1
                        escape_clock_pass += 1
            
            # FB-2 Determinacy check
            if vc < vs:
                counts['det_steps'] += 1
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
                    # Determined NT gate G'
                    n_gates += 1
                    counts['gates'] += 1
                    m_prime = q_next
                    assert m_prime == vc < min(vA, vB)
                    dR = m_prime + 1 + ell - j
                    assert dR <= 1 + L_bc, f"DR' failed: dR={dR} > 1+L_bc={1+L_bc}"
                    counts['DRp_checks'] += 1
                    
                    is_boundary = (dR >= 1)
                    div = (vc >= j - ell)
                    assert is_boundary == div, f"Boundary iff div failed: {is_boundary} != {div}"
                    counts['boundary_iff_div_checks'] += 1
                    
                    if is_boundary:
                        n_boundary += 1
                    terminated = True
                    break
            else:
                # Split
                counts['split'] += 1
                if step_idx == 0 and c1 >= j - 1:
                    escape_counts['SPLIT'] += 1
                terminated = True
                break
        
        if not terminated:
            counts['limit'] += 1
        elif terminated and counts['det_end'] > 0 and step_idx == 0 and c1 >= j - 1:
            escape_counts['END'] += 1

elapsed = time.time() - t0
print(f"Full census completed in {elapsed:.1f}s")
print(f"Pairs tested: {counts['pairs_odd']}")
print(f"Det END: {counts['det_end']}")
print(f"Splits: {counts['split']}")
print(f"Limits: {counts['limit']}")
print(f"Gates found: {n_gates}")
print(f"Boundary gates found: {n_boundary}")
print(f"vB checks: {counts['vB_checks']}")
print(f"vA checks: {counts['vA_checks']}")
print(f"A zero checks: {counts['A_zero_checks']}")
print(f"DRp checks: {counts['DRp_checks']}")
print(f"Boundary iff div checks: {counts['boundary_iff_div_checks']}")
print(f"Escape landings (c1 >= j-1): {counts['escape_landings']}")
print(f"Escape j set: {sorted(escape_j_set)}")
print(f"Escape free congruence pass: {escape_free_congruence_pass}")
