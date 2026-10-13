"""revC_pd.py — ADVERSARY-3 audit 4: PD (position dominance) measurements.

4.1  Re-run the coordinator's check_invariants.py at N = 200000 and N = 500000.
4.2  Convention-robustness of the D-entry position. check_invariants assigns a D the
     position tDp = producer j (if b was M), rho+2 (if b was E), b5+2 (if b was D) —
     a GENEROUS convention ("one past the enclosing run" counted from +1).  The
     strictest natural convention puts the D at front-position (producer run length)
     = j_prod - 1 (the run occupies t = 0..j_prod-2).  We measure the PD margin
     t - j at every chain under BOTH conventions (M and E entries are unambiguous:
     t = shift within the run; t = rho for originals) and check t >= j under the
     worst one.
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r10')
import check_invariants as CI
import fast_walker as FW

print('4.1  coordinator\'s check_invariants.py re-runs')
for N in (200000, 500000):
    print('--- N = %d ---' % N)
    CI.run(N)

print()
print('4.2  PD margin under code convention vs strict D convention (to N = 500000)')
def run_pd(N):
    P = []; A = (0, 1, 1, 0); i = 0; s = 0
    min_code = (10**9, None); min_strict = (10**9, None)
    viol_code = viol_strict = 0
    chains = dchains = 0
    while i <= N:
        if len(P) >= 2: b, c = P[0], P[1]
        elif len(P) == 1: b = P[0]; c = [i, 1, 0, ('E', i), 0, i]
        else: b = [i, 1, 0, ('E', i), 0, i]; c = [i + 1, 1, 0, ('E', i + 1), 0, i + 1]
        cpar = 0 if A[0] >= 1 else (A[1] & 1)
        if (cpar + A[2]) % 2 == 0:
            t1 = FW.cadd((A[0], A[1]), (b[0], b[1])); cA = FW.cadd(t1, (c[0], c[1]))
            A = (cA[0], cA[1], A[2] + b[2] + c[2] + 3, max(A[3], b[4], c[4])); newp = []
        else:
            tx = FW.cadd((A[0], A[1]), (b[0] + 1, b[1]))
            lx = A[2] + 2 * b[2] + 3
            vcx, rcx = tx; j = FW.v2i(lx)
            vu = vcx - j; lu = lx >> j
            tD = FW.cadd((c[0], c[1]), (A[0] - 1, A[1]))
            lD = c[2] + (A[2] + 1) // 2
            JLu = max(A[3], b[4], j)
            if b[3][0] == 'M': tDp_code = b[3][2]
            elif b[3][0] == 'E': tDp_code = b[3][1] + 2
            else: tDp_code = b[5] + 2
            tDp_strict = b[3][2] - 1 if b[3][0] in ('M', 'D') else b[3][1]
            newp = [[vu + t, rcx, lu << t, ('M', s, j), JLu, t] for t in range(j - 1)] + \
                   [[tD[0], tD[1], lD, ('D', s, j), max(A[3], b[4], j, c[4]), tDp_code, tDp_strict]]
            A = (vu, rcx, lu + 1, JLu)
            chains += 1
            # PD at this chain: t of the FRONT entry b
            if b[3][0] == 'E':
                t_front_code = b[3][1]; t_front_strict = b[3][1]
            elif b[3][0] == 'M':
                t_front_code = b[5]; t_front_strict = b[5]
            else:
                dchains += 1
                t_front_code = b[5]           # tDp_code
                t_front_strict = b[6]         # j_prod - 1
            m1 = t_front_code - j; m2 = t_front_strict - j
            if m1 < min_code[0]: min_code = (m1, (i, s, b[3][0], j))
            if m2 < min_strict[0]: min_strict = (m2, (i, s, b[3][0], j))
            if m1 < 0: viol_code += 1
            if m2 < 0: viol_strict += 1
        k2 = len(P)
        if k2 >= 2: P = P[2:]
        else: i += 2 - k2; P = []
        P = newp + P; s += 1
    print('chains = %d (of which D-fires = %d)' % (chains, dchains))
    print('  code convention:  min margin t-j = %d at %s ; violations = %d' % (min_code + (viol_code,))[0:2] if False else
          '  code convention:  min margin t-j = %d at %s ; violations (t<j) = %d' % (min_code[0], min_code[1], viol_code))
    print('  strict convention (D at j_prod-1, level-D at rho): min margin = %d at %s ; violations = %d'
          % (min_strict[0], min_strict[1], viol_strict))
    print('  => PD (t >= j at every chain) is convention-robust: %s'
          % (viol_code == 0 and viol_strict == 0))

if __name__ == '__main__':
    run_pd(500000)
