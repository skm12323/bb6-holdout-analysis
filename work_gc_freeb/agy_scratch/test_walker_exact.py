import sys
from fractions import Fraction as F

sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2, INF

cal = Cal()

class SymbolicWalker:
    def __init__(self, cal):
        self.cal = cal

    def walk(self, j, m, max_steps=400):
        """
        Runs the generic post-gate walk from (j, k_j, m).
        Tracks exact C, A, B, theta, ell, L_bc.
        Returns dict with status, steps, etc.
        """
        k_j = self.cal.k(j)
        assert k_j is not None
        
        # c_Th = 2^(j-2) + 3(k+1)
        c_Th = 2**(j - 2) + 3 * (k_j + 1)
        Th = F(c_Th)
        
        # x = 2^m (1 + 2V) = 2^m + 2^(m+1)*V
        # In general, C = u + beta * 2^m.
        # But for m < 100000, we can also compute exact C directly as a Fraction!
        C = F(2**m)
        A = F(0)
        B = F(2**(m + 1))
        
        ell = 0
        L_bc = 0
        run_bc = True
        
        q = m
        steps = []
        
        for step_idx in range(max_steps):
            if q <= 4:
                return {'status': 'END', 'steps': steps, 'reason': 'q<=4', 'ell': ell, 'L_bc': L_bc}
            r = self.cal.row(q - 1)
            if not r['odd']:
                return {'status': 'END', 'steps': steps, 'reason': 'even', 'ell': ell, 'L_bc': L_bc}
            
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
            
            # Verify FB-1 invariants:
            # v2(B_next) == m + 1 - new_ell
            # v2(A_next): if A_next != 0: v2(A_next) == j - new_ell + L_bc + 1
            vB = v2(B_next)
            assert vB == m + 1 - new_ell, f"FB-1 B invariant violated: {vB} != {m + 1 - new_ell}"
            
            if A_next == 0:
                vs = vB
                vA = INF
            else:
                vA = v2(A_next)
                expected_vA = j - new_ell + L_bc + 1
                assert vA == expected_vA, f"FB-1 A invariant violated: {vA} != {expected_vA}"
                vs = min(vA, vB)
            
            vc = v2(C_next)
            
            # Determinacy (FB-2):
            if vc < vs:
                # Determined
                q_next = vc
                steps.append((q, kind, q_next, new_ell))
                q = q_next
                Th = Th_next
                C = C_next
                A = A_next
                B = B_next
                ell = new_ell
                
                # Check if true NT gate
                if kind == 'a' and q_next >= steps[-1][0]:
                    # This is a true NT gate G'!
                    # Verify FB-3:
                    m_prime = q_next
                    assert m_prime == vc < min(vA, vB)
                    dR = m_prime + 1 + ell - j
                    assert dR <= 1 + L_bc, f"DR' violated: dR={dR} > 1+L_bc={1+L_bc}"
                    is_boundary = (dR >= 1)
                    div = (vc >= j - ell)
                    assert is_boundary == div, f"Boundary iff div violated: is_b={is_boundary}, div={div}"
                    return {
                        'status': 'GATE', 'steps': steps, 'ell': ell, 'L_bc': L_bc,
                        'm_prime': m_prime, 'dR': dR, 'is_boundary': is_boundary,
                        'C_final': C, 'vA': vA, 'vB': vB
                    }
            else:
                # Split!
                return {
                    'status': 'SPLIT', 'steps': steps, 'ell': new_ell, 'L_bc': L_bc,
                    'vc': vc, 'vs': vs, 'vA': vA, 'vB': vB, 'at_chain': q
                }
        
        return {'status': 'LIMIT', 'steps': steps, 'ell': ell, 'L_bc': L_bc}

sw = SymbolicWalker(cal)

# Test counterexample A with exact Fraction:
print("Testing counterexample A with exact Fraction...")
resA = sw.walk(24, 6268562)
print(f"Status: {resA['status']}")
print(f"Steps: {resA['steps']}")
print(f"m': {resA['m_prime']}, dR: {resA['dR']}, is_boundary: {resA['is_boundary']}")
print(f"ell: {resA['ell']}, L_bc: {resA['L_bc']}")
print(f"v2(C_final): {v2(resA['C_final'])}, v2(A): {resA['vA']}, v2(B): {resA['vB']}")
