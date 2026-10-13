"""revB2_extra.py -- completeness probe + affine cross-checks of agentB2 formulas.

(1) Find, in the REAL walk (exact, ground truth), the first universal positions of
    spike classes 13,14,15,16,18 (not among the j_last of agentB2's 12-row table,
    which has j_last in {1..10,12}). For each, predict the Phi_m D-shape
    (g,jl) = (dp(jl)-1, jl) at m = rho + dp(jl) + 1, run the concrete Phi_m there,
    and check: D-fire exists, x_D affine form, j_D = 1+v2(3Kex+1), j_D <= m-2.
    This tests whether the 12-shape enumeration is complete (it should NOT be).
(2) Second-fire affine form (agentB2 sect.3): for D-fires in m=5..300 whose second
    fire exists: 4*x_seam == 153P + 30k_h + 36Kex + 24K' + 48 with K' in {1,2}.
(3) Mixed-fire affine form (agentB2 sect.4 V-A): for mixed fires with b = E_{m-2}
    (tagged R at index m-2): 4*x_mix == 27P + 18k_h + 24Kmix + 28, Kmix = s_cross/2.
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r10')
from revB2_phi import phi_trace, v2
from revB2_walk import my_exact_walk   # reuse my exact walker (runs to 1e5 on import? no: function)


def v2i(x):
    return (x & -x).bit_length() - 1


# ---------- (1) locate spike classes in the real walk ----------
N = 100000
lvl, _, _ = my_exact_walk(N)
want = {13, 14, 15, 16, 18}
firsts = {}
for (rho, k, j) in lvl:
    if j in want and j not in firsts:
        firsts[j] = (rho, k)
print('(1) first universal positions of classes 13..18 in the real walk (i<=%d):' % N)
for j in sorted(firsts):
    print('    class %2d first at rho=%d (k=%d)' % (j, firsts[j][0], firsts[j][1]))

dp = {}
def D(j):
    if j not in dp:
        dp[j] = phi_trace(j)['re'][1]
    return dp[j]

print('\n    predicted vs actual Phi_m at m = rho + dp(j) + 1:')
newrows = []
for j in sorted(firsts):
    rho, k = firsts[j]
    m = rho + D(j) + 1
    r = phi_trace(m)
    ch = r['chains']; cross = r['cross']
    DF = [c for c in ch if c[1][0] == 'Dh']
    pure = [c for c in ch if c[1][0] == 'R' and c[2][0] == 'R']
    rho_p = pure[-1][1][1] if pure else None
    g = m - 2 - rho_p if rho_p is not None else None
    jl = pure[-1][3] if pure else None
    if DF:
        sD, tbD, tcD, jD, xD = DF[0]
        assert cross['clean'] and cross['s'] == sD
        Kex = cross['s'] // 2
        a = v2(3 * Kex + 1)
        xok = (2 * xD == 39 * r['P'] + 18 * r['k'] + 12 * Kex + 16)
        K = (pure[-1][4] - 3 * (r['u'] << rho_p) - 4) // 6 if pure else None
        delta = Kex - K if pure else None
        ok = xok and jD == 1 + a and jD <= m - 2
        print('    class %2d -> m=%d: D-fire, shape (g=%s, jl=%s) [predicted (dp-1=%d, %d)], '
              'delta=%s, j_D=%d (=1+v2(3Kex+1)? %s), xok=%s, j_D<=m-2: %s'
              % (j, m, g, jl, D(j) - 1, j, delta, jD, jD == 1 + a, xok, jD <= m - 2))
        newrows.append((j, m, g, jl, delta, jD, ok))
    else:
        print('    class %2d -> m=%d: NO D-fire (cross type %s)' %
              (j, m, 'clean' if cross['clean'] else 'Y'))
print('    all new-shape checks passed: %s' % all(r[6] for r in newrows))
print('    shapes NOT in agentB2 12-row table: %s' %
      [(g, jl) for (j, m, g, jl, d, jd, ok) in newrows if jl not in
       (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12)])

# ---------- (2) second-fire affine form, m = 5..300 ----------
print('\n(2) second-fire affine check (m=5..300):')
n2 = ok2 = 0
kp1 = kp2 = 0
for m in range(5, 301):
    r = phi_trace(m)
    ch = r['chains']; cross = r['cross']
    DF = [c for c in ch if c[1][0] == 'Dh']
    if not DF:
        continue
    sD = DF[0][0]
    Kex = cross['s'] // 2
    P = r['P']; k = r['k']
    for c in ch:
        if c[1] == ('d', sD):
            s, tb, tc, j, x = c
            num = 4 * x - 153 * P - 30 * k - 36 * Kex - 48
            n2 += 1
            if num % 24 == 0 and num // 24 in (1, 2):
                ok2 += 1
                if num // 24 == 1:
                    kp1 += 1
                else:
                    kp2 += 1
            else:
                print('    m=%d: K-fit fails: %s/24' % (m, num))
print('    second fires: %d, affine with K\' in {1,2}: %d (K\'=1: %d, K\'=2: %d)'
      % (n2, ok2, kp1, kp2))

# ---------- (3) mixed-fire affine form, b = E_{m-2}, m = 5..300 ----------
print('\n(3) mixed-fire affine check (b = E_{m-2}, m=5..300):')
n3 = ok3 = 0
for m in range(5, 301):
    r = phi_trace(m)
    ch = r['chains']; cross = r['cross']
    MIX = [c for c in ch if c[2][0] == 'Dh']
    if not MIX:
        continue
    s, tb, tc, j, x = MIX[0]
    if tb != ('R', m - 2):
        continue
    P = r['P']; k = r['k']
    assert cross['s'] == s and not cross['clean']
    Kmix = cross['s'] // 2 if cross['s'] % 2 == 0 else None
    n3 += 1
    if Kmix is not None and 4 * x == 27 * P + 18 * k + 24 * Kmix + 28:
        ok3 += 1
    else:
        print('    m=%d: mixed affine fails (Kmix=%s)' % (m, Kmix))
print('    b=E_{m-2} mixed fires: %d, affine x=(27/4)P+(9/2)k+6Kmix+7: %d' % (n3, ok3))
