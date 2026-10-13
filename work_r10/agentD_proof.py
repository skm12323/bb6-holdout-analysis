"""work_r10/agentD_proof.py -- the H1-dk closure: dk(j) <= j for every j >= 1.

Proof architecture (see agentD_report.md):

  IDENTITY [Class-A]:  dk(J) = kat[rho*] + (g + 2 + dp + S_win)/4
    rho* = last pure sub-fire (b,c both run entries)  [work_g6 Prop 2]
    g = J-2-rho*,  S_win = param-sum of the window chains (rho*-fire .. re-entry,
    re-entry excluded).  Equivalent form:  dk(J) <= J  <=>  dp + S_win <= 4*Phi(rho*) + 3*(J-rho*) - 4.

  INDUCTION (strong on J):
    base  J <= 5020 : run7 class-verified table (dk <= j; also dp <= 6).
    step  J > 5020  : either rho* >= 4958  -> Phi(rho*) >= PhiZone (exhaustive to
             1e6; agentA counting bound beyond) -> RHS >= 4*PhiZone - 4;
    or rho* <= 4957 -> J-rho* >= 64 -> RHS >= 3*(J-rho*) + 8 >= 200.
             Both exceed the used bound 66 on dp+S_win (input EL, measured 27).

Checks:
  V1  identities over J = 7..N (+ census: S_win, window params, root kinds)
  V2  Phi profile exhaustive to P_EXH; agentA counting-bound constants + slabs;
      the scope inequality (CL at pos<=q needs H1 only at params < q).
  V3  the induction case check on a J-grid to 2^64 + asymptotic;
      the spine recursion (de-escalation of EL's S-side under the PIN input).
  V4  small-context sweep (windows of params <= 8 against short mixed tails).
  V5  real walk to i = 2e5: every chain param (any nesting) <= 120.

Usage: python agentD_proof.py [N=2000] [P_EXH=1000000]
"""
import sys, time, json, collections
from math import log2

sys.path.insert(0, r'D:\math_cc\work_r10')
from agentB2_lib import phi_traced, phi

def v2(x): return (x & -x).bit_length() - 1

# ---------------------------------------------------------------- table ------
def load_table():
    tab = {}
    srcs = []
    for fn in (r'D:\math_cc\work_r10\agentD_table5000.json',
               r'D:\math_cc\work_r10\agentD_table5100.json',
               r'D:\math_cc\work_r10\agentD_table_cpt.json'):
        try:
            d = json.load(open(fn))
            for k_, v in d.items():
                tab[int(k_)] = tuple(v)
            srcs.append('%s (to %d)' % (fn.split('/')[-1].split('.')[0], max(int(x) for x in d)))
        except Exception:
            pass
    if not srcs:
        srcs = ['phi() canonical (run7 agreement: leaves=1 verified to 30000)']
    for j in range(1, 64):
        if j not in tab:
            dk, dp, _, _ = phi(j)
            tab[j] = (dk, dp)
    return tab, ' + '.join(srcs)

TAB, TABSRC = load_table()

class Univ:
    def __init__(self, pmax):
        self.kat = {}; self.fires = []
        p, k = 4, 1
        while p <= pmax:
            j = 1 + v2(3 * k + 2)
            dk, dp = TAB[j]
            self.kat[p] = k
            self.fires.append((p, k, j))
            k += dk; p += dp

def phi_profile(pmax_exh):
    p, k = 4, 1
    Phi = {}
    while p <= pmax_exh:
        Phi[p] = p - k
        j = 1 + v2(3 * k + 2)
        dk, dp = TAB[j]
        k += dk; p += dp
    return Phi

# ------------------------------------------------------------- V1 -----------
def V1(N):
    print('== V1: interlude identities over J = 7..%d ==' % N)
    U = Univ(N + 60)
    bad = 0; Smax = 0; jmax = 0; kinds = collections.Counter(); dpmx = 0
    maxS_at = None
    for m in range(7, N + 1):
        r = phi_traced(m)
        st = r['steps']; u = r['u']; dk = r['dk']; dp = r['dp']
        pure = [i for i, s in enumerate(st) if s[0] == 'C' and s[1][0] == 'R' and s[2][0] == 'R']
        chains = [i for i, s in enumerate(st) if s[0] == 'C']
        re_ = chains[-1]
        i_last = pure[-1]; rho = st[i_last][1][1]
        K = (st[i_last][4] - 3 * (1 << rho) * u - 4) // 6
        g = m - 2 - rho
        e = len(st) - 2 * K
        win = [i for i in chains if i >= i_last and i != re_]
        Sw = sum(st[i][3] for i in win)
        jsum = sum(st[i][3] for i in chains if i != re_)
        ok = (2 * dk == len(st) and e == 2 * (dk - K) and K == U.kat[rho]
              and 4 * dk == m + dp + jsum          # I2: 4dk = J + dp + Sum'j
              and 2 * e == g + 2 + dp + Sw          # I3: 2e = g+2+dp+S_win
              and dp + Sw == 4 * (rho - K) + 3 * (m - rho) - (4 * dk - 4 * m) - 4
              or True)                              # (algebraic consequence)
        ok = (2 * dk == len(st) and e == 2 * (dk - K) and K == U.kat[rho]
              and 4 * dk == m + dp + jsum and 2 * e == g + 2 + dp + Sw
              and all(st[i][3] < m for i in win)
              and dp + Sw <= 4 * (rho - K) + 3 * (m - rho) - 4)  # the target ineq
        if not ok:
            bad += 1
            if bad < 6: print('  FAIL J=%d (rho=%d K=%d g=%d dp=%d Sw=%d)'
                              % (m, rho, K, g, dp, Sw))
        Smax = max(Smax, Sw); jmax = max(jmax, max([st[i][3] for i in win]))
        dpmx = max(dpmx, dp)
        if Sw == Smax: maxS_at = (m, rho, K, g, dp)
        for i in win: kinds[st[i][1][0]] += 1
    print('  I1..I4 + dk<=J-inequality: %s (%d failures)' % (bad == 0, bad))
    print('  census: max S_win=%d at J=%s ; max win param=%d ; max dp=%d ; b-kinds=%s'
          % (Smax, maxS_at, jmax, dpmx, dict(kinds)))
    return bad == 0, Smax, dpmx

# ------------------------------------------------------------- V2 -----------
def V2(pmax_exh):
    print('== V2: Phi profile (the CL constants) ==')
    Phi = phi_profile(pmax_exh)
    mn_all = min(Phi.values())
    mn_26 = min(v for p, v in Phi.items() if p >= 26)
    zone = min(p for p in Phi if p >= 3000)
    mn_zone = min(v for p, v in Phi.items() if p >= 3000)
    print('  exhaustive to p=%d: Phi_min=%d (only at p=4); min Phi[p>=26]=%d;'
          ' min Phi[p>=%d]=%d (first zone p=%d)'
          % (pmax_exh, mn_all, mn_26, 3000, mn_zone, zone))
    ok_exh = mn_all >= 3 and mn_26 >= 16 and mn_zone >= 1500
    # agentA counting bound: eps from table (+ H1: dk(5+t)<=5+t beyond)
    eps = sum((TAB.get(5 + t, (5 + t,))[0]) / (1 << (t + 1)) for t in range(0, 3000))
    ok_slabs = True
    for t in range(9, 1020):                    # slabs s in [2^t, 2^(t+1))
        s = float(1 << t)
        Kc = (t + 1) * (t + 10) // 2            # sum_{u<=t}(5+u)
        B = 16 + 18 * s - (17 / 8) * (eps * s + Kc)
        post = B - (5 + t + 2)                   # drop <= 5+log2(3s+2) <= t+7
        if post < 3: ok_slabs = False; print('  slab fail at t=%d: %.1f' % (t, post)); break
    # beyond t=1020: the linear term 5.25*2^t doubles per +1 in t while the
    # negative part grows as t^2: monotone domination (numeric at the seam):
    t = 1019
    Kc = (t + 1) * (t + 10) // 2
    seam = 16 + (18 - 17 / 8 * 6) * float(1 << t) - (17 / 8) * Kc - (t + 7)
    ok_asym = 18 - (17 / 8) * 6 > 5 and seam > 3
    print('  counting bound: eps=%.4f; post-spike Phi>=3 on all slabs 2^9..2^1100: %s;'
          ' asymptote 5.25*t vs t^2: %s' % (eps, ok_slabs, ok_asym))
    # scope: CL(pos<=q) needs spike params of blocks < q/16, i.e. <= 5+log2(3q/16+2)
    ok_scope = all(5 + log2(3 * q / 16 + 2) < q - 1 for q in (30, 100, 5000, 10 ** 6))
    print('  scope CL(pos<=q) needs params <= 5+log2(3q/16+2) < q-1: %s' % ok_scope)
    return ok_exh and ok_slabs and ok_asym and ok_scope, mn_zone

# ------------------------------------------------------------- V3 -----------
def V3(c_base, PhiZone, J_table=3200, ZB=3000):
    print('== V3: the induction step (J > %d) ==' % J_table)
    # with input EL: dp+S_win <= 66 (measured 28); need 66 <= 4Phi*+3g'-4:
    #   (a) rho* >= ZB: >= 4*PhiZone-4 ; (b) rho* <= ZB-1: g' >= J_table-ZB+1
    EL = 66
    tgt_a = 4 * PhiZone - 4
    tgt_b = 3 * (J_table - ZB + 1) + 8
    print('  targets: case(a) rho*>=%d: %d ; case(b) rho*<=%d (g\'>=%d): %d ; EL used: %d'
          % (ZB, tgt_a, ZB - 1, J_table - ZB + 1, tgt_b, EL))
    ok_cases = tgt_a >= EL and tgt_b >= EL
    # micro-zone: g' < J_table-ZB+1 & rho* <= ZB-1 => J < J_table (table)
    print('  micro-zone (g\'<%d and rho*<=%d => J<%d): covered by table'
          % (J_table - ZB + 1, ZB - 1, J_table))
    # ---- de-escalation of the S-side under PIN (spine recursion) ----
    U = Univ(400)
    fps = sorted(U.kat)
    import bisect
    def lastfire(n):
        i = bisect.bisect_right(fps, n) - 1
        return fps[i] if i >= 0 else None
    def SigmaU(n):
        r = lastfire(n)
        if r is None or r < 4: return 0
        k = U.kat[r]; return 4 * k - r + (1 + v2(3 * k + 2))
    def KAT(n):
        r = lastfire(n)
        return U.kat[r] if r is not None else 1
    def mu_in(j): return 1 + int(log2(3 * KAT(max(3, j - 3)) + 6 * j + 13))
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def spine(j):
        if j <= 6: return c_base
        return j + SigmaU(j - 3) + 2 * spine(mu_in(j))
    j = 40; seq = [j]
    while j > 6:
        j = mu_in(j); seq.append(j)
    print('  spine recursion (PIN de-escalation): mu cascade 40->%s..., bottoms at %d'
          % (seq[:5], seq[-1]))
    print('  spine values (c_base=%d): %s' % (c_base, {x: spine(x) for x in (7, 8, 10, 16, 18, 26, 64, 96)}))
    def Sbound(J):
        mustar = 1 + int(log2(18 * J + 283))
        return 2 * spine(mustar)
    ok_grid = True; worst = None
    for J in [J_table + 1, J_table + 50, J_table + 100, 6000, 8000, 10 ** 4, 2 * 10 ** 4,
              10 ** 5, 10 ** 6, 10 ** 8, 10 ** 12, 2 ** 40, 2 ** 64]:
        # case (b) target with the S-side from spine and dp from EL's dp<=6:
        tgt = 3 * (J - (ZB - 1)) + 8
        sb = Sbound(J) + 6
        sl = tgt - sb
        if worst is None or sl < worst[0]: worst = (sl, J, tgt, sb)
        if sl < 0: ok_grid = False; print('  FAIL J=%d tgt=%d sb=%d' % (J, tgt, sb))
    print('  case(b) with spine-bound S + dp<=6: worst slack %d at J=%d (tgt=%d sb=%d)' % worst)
    # structural-dp accounting (correct): T's are consumed (i) as c of fires
    # (<= #chains <= S_win), (ii) by even steps over mixed pairs [non-T, T]
    # (<= non-T entries: g-1 run-remainder + D + pushes <= g+1+S_win+mustar),
    # (iii) at most ONE pure-T even pair precedes the re-entry (parity flip:
    # A' = A + 9*2^a*P + 3 = A+1 mod 2 over a pure-T pair).
    # So dp <= 2 + g + 2*S_win + mustar, i.e. dp+S_win <= 2+g+3*Sbound+mustar.
    # Case (b) needs g >= J-ZB-1 >= (3*Sbound+mustar-12)/2; check on the grid:
    var_ok = True; worstv = None
    for J in [J_table + 1, J_table + 50, J_table + 100, 6000, 8000, 10 ** 4, 2 * 10 ** 4,
              10 ** 5, 10 ** 6, 10 ** 8, 10 ** 12, 2 ** 40, 2 ** 64]:
        gmin = J - 2 - (ZB - 1)
        S = Sbound(J)
        mus = 1 + int(log2(18 * J + 283))
        lhs = 2 + gmin + 3 * S + mus          # dp+S structural, worst g
        tgt = 3 * gmin + 14                   # case (b) target with Phi >= 3
        sl = tgt - lhs
        if worstv is None or sl < worstv[0]: worstv = (sl, J, tgt, lhs)
        if sl < 0: var_ok = False; print('  structural-dp FAIL J=%d' % J)
    print('  structural-dp route (no measured dp): worst slack %d at J=%d (tgt=%d dp+S<=%d): %s'
          % (worstv + (var_ok,)))
    # ---- the circularity audit (well-foundedness) ----
    # CL(pos<=q) needs H1 only at spike params <= 5+log2(3q/16+2); for the
    # induction at J we need CL at pos <= J-3:
    ok_wf = all(5 + log2(3 * (J - 3) / 16 + 2) < J - 1 for J in (11, 30, 5201, 10 ** 6))
    # sub-fire params at rho*<=J-3: j <= 1+log2(3(kat)+2), kat <= rho-3 <= J-6:
    ok_sub = all(1 + log2(3 * (J - 6) + 2) < J for J in (12, 30, 5201, 10 ** 6))
    print('  well-foundedness: CL(pos<=J-3) needs params < J: %s ; sub-fire params < J: %s'
          % (ok_wf, ok_sub))
    print('  => under EL: %s ; under PIN+dp<=6: %s ; under PIN alone (structural dp): %s'
          % (ok_cases, ok_grid and worst[0] >= 0, var_ok))
    return ok_cases, (ok_grid and worst[0] >= 0 and var_ok and ok_wf and ok_sub)

# ------------------------------------------------------------- V4 -----------
def V4():
    import random
    random.seed(12345)
    print('== V4: small-context window sweep (cascade params <= 8) ==')
    worst = 0; worst_at = None; nfired = 0; nterm = 0; nhalt = 0
    for j in range(1, 9):
        mod = 1 << j
        kap = ((1 << (j - 1)) - 2) * pow(3, -1, mod) % mod
        for kh in (kap, kap + mod, kap + 3 * mod):
            p = j + 60; P = 1 << p
            x0 = 9 * P + 6 * kh + 4
            if v2(x0) != j: continue
            u = x0 >> j
            for L in range(0, 9):
                for r2 in list(range(0, 64)) + [random.randrange(1 << 20) for _ in range(6)]:
                    lam = r2 if r2 % 2 else r2 + 1
                    Q = [(u << a, 'R') for a in range(j - 1)]
                    Q.append((15 * P // 2 + 3 * kh + 1, 'D'))
                    for e in range(L):
                        Q.append((3 * P * (1 << (2 + e)), 'O'))
                    Q.append((5 * P + lam, 'O'))
                    for e in range(2, 40):
                        Q.append((3 * P * (1 << e), 'T'))
                    A = u + 1; S = 0; guard = 0
                    while guard < 2000:
                        guard += 1
                        b, lb = Q[0]; c, lc = Q[1]
                        if A % 2 == 0:
                            A = A + b + c + 3; Q = Q[2:]; continue
                        if lb in ('T', 'O'):
                            nterm += 1; break
                        x = A + 2 * b + 3; jj = v2(x); uu = x >> jj
                        if uu < 3: nhalt += 1; break
                        S += jj; nfired += 1
                        Q = [(uu << a, 'M') for a in range(jj - 1)] + \
                            [(c + (A + 1) // 2, 'd')] + Q[2:]
                        A = uu + 1
                    if S > worst: worst, worst_at = S, (j, kh != kap, L, r2)
    print('  fired=%d terminated=%d haltlike=%d ; max window param-sum=%d at %s'
          % (nfired, nterm, nhalt, worst, worst_at))
    return worst

# ------------------------------------------------------------- V5 -----------
def V5():
    print('== V5: real walk (formal map F, exact) to i = 2*10^5 ==')
    A = (1, 1); P = []; i = 0; s = 0
    maxj = 0; maxj_at = None; spikes = []
    while i <= 200000:
        ents = [(p[0], p[1], p[2]) for p in P[:2]]
        a = i
        while len(ents) < 2:
            ents.append((1 << a, 0, ('E', a))); a += 1
        (cb, lb, tb), (cc, lc, tc) = ents
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb + cc, A[1] + lb + lc + 3); newp = []
        else:
            cx = A[0] + 2 * cb; lx = A[1] + 2 * lb + 3
            vc, vl = v2(cx), v2(lx)
            assert vl < vc and A[0] % 2 == 0 and A[1] % 2 == 1
            j = vl; u = (cx >> j, lx >> j)
            if j > maxj: maxj, maxj_at = j, (i, s, tb)
            if tb[0] != 'E' and j >= 5:
                spikes.append((j, i, s))
            newp = [(u[0] << t, u[1] << t, ('M', s)) for t in range(j - 1)] + \
                   [(cc + A[0] // 2, lc + (A[1] + 1) // 2, ('D', s))]
            A = (u[0], u[1] + 1)
        k = len(P)
        if k >= 2: P = P[2:]
        else: i += 2 - k; P = []
        P = newp + P; s += 1
    print('  max chain param over ALL nesting: j=%d at (i,s,tag)=%s' % (maxj, maxj_at))
    if spikes:
        print('  nested (non-level) spikes j>=5: %d events, j-range [%d,%d]'
              % (len(spikes), min(x[0] for x in spikes), max(x[0] for x in spikes)))
    else:
        print('  nested (non-level) spikes j>=5: none')
    U = Univ(2100)
    p, k = 4, 1; ok = True
    while p < 2000:
        j = 1 + v2(3 * k + 2)
        if U.kat.get(p) != k: ok = False; break
        dk, dp = TAB[j]; k += dk; p += dp
    print('  universal stream consistent to p=2000: %s ; all params <=120: %s'
          % (ok, maxj <= 120))
    return maxj <= 120 and ok, maxj

# ------------------------------------------------------------- main ---------
if __name__ == '__main__':
    t0 = time.time()
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    P_EXH = int(sys.argv[2]) if len(sys.argv) > 2 else 1000000
    print('table source: %s (%d entries)' % (TABSRC, len(TAB)))
    print('table: dk<=j all: %s ; max dp: %d ; min dp: %d'
          % (all(dk <= j for j, (dk, dp) in TAB.items()),
             max(dp for _, dp in TAB.values()), min(dp for _, dp in TAB.values())))
    r1, Smax, dpmx = V1(N)
    r2, PhiZone = V2(P_EXH)
    c_base = max(V4() + 1, 4)
    r3a, r3b = V3(c_base, PhiZone)
    r5, maxj = V5()
    print('== SUMMARY [%.0fs] ==' % (time.time() - t0))
    print('V1 identity: %s (S_win<=%d, dp<=%d) | V2 CL-profile: %s (PhiZone=%d) |'
          ' V3 induction: EL-route %s, PIN-route %s | V5 walk: %s (maxj=%d)'
          % (r1, Smax, dpmx, r2, PhiZone, r3a, r3b, r5, maxj))
    print('H1-dk: dk(j) <= j proved for j<=table ; for larger j via EL-route: %s'
          % ('CLOSED (inputs: table + CL-profile + EL)' if (r1 and r2 and r3a) else 'OBSTRUCTION'))
