"""revC_cases.py — ADVERSARY-3 audit 3: PROOF.md §7 case analysis, on the EXACT walk.

(E)  v2(sum) >= min at every even step (ties only shrink delta); also the delta form
     delta_new <= max(delta inputs) with all deltas at the post-step pointer.
(P)  pointer advances iff <= 1 stack entry remained; survivors of an advancing step
     are exactly the fresh pushes.
(C)  pure-stretch climb EXACT: for each maximal stretch of consecutive pair
     absorptions (u*2^t, u*2^{t+1}) from one producer run, the head BEFORE absorbing
     pair #k equals c_u * 4^{k-1} (so after: 4^k).  Stretch-length census.
(Ch) v2(c_x) >= min(v_A, v_b+1): census exact-min vs lifted; post-chain slack
     delta(u) - J(u) <= 0 (INV-L step at chains).
(D)  D-construction: sub-cases v_c <, =, > v_A-1; verify v2(D) in each;
     slack(D) = delta(D) - J_D - 2 <= 0; in the '>' sub-case measure delta_A - J_D
     (the one-line proof needs it <= +1; INV-L alone gives <= +2).
(L)  level fires: delta_x = 0 (c_x = 3*2^rho exactly) and delta(u) = j.
Lineage J convention follows check_invariants.py (no reset at original absorption).
"""
import sys, collections
sys.path.insert(0, r'D:\math_cc\work_r10')

def v2(x):
    return (x & -x).bit_length() - 1

def run(N):
    A = (1, 1, 0)          # (c, l, J_lin)
    P = []                 # [c, l, tag, J, t, base]  (base = shared ref to c_u, M only)
    i = 0; s = 0
    st = collections.Counter()
    max_stretch = 0
    stretch_hist = collections.Counter()
    E_ties = 0; E_worst = (-10**9, None)
    Ch_lift = 0; Ch_exact = 0
    D_sub = collections.Counter()
    D_slack_worst = -10**9
    D_gt_headslack_worst = -10**9
    post_chain_slack_worst = -10**9
    head_slack_worst = -10**9
    pure_prod = None; pure_k = 0
    while i <= N:
        ents = []
        for off in range(2):
            if off < len(P): ents.append(P[off])
            else:
                a = i + off - len(P)
                ents.append([1 << a, 0, ('E', a), 0, a, None])
        (cb, lb, tb, Jb, tb5, cub), (cc, lc, tc, Jc, tc5, cuc) = ents
        dA = i - v2(A[0])
        if (A[0] + A[1]) % 2 == 0:
            st['E'] += 1
            cn = A[0] + cb + cc
            vn = v2(cn); mn = min(v2(A[0]), v2(cb), v2(cc))
            assert vn >= mn, ('E valuation', i, s)
            if vn > mn: E_ties += 1
            is_pair = (tb[0] == 'M' and tc[0] == 'M' and tb[1] == tc[1] and tc5 == tb5 + 1)
            cont = (is_pair and pure_prod is not None and tb[1] == pure_prod
                    and tb5 == 2 * pure_k)
            if cont:
                # pure continuation: head before absorbing pair #(k+1) is c_u*4^k
                assert A[0] == cub << (2 * pure_k), ('C climb', i, s)
                pure_k += 1
                max_stretch = max(max_stretch, pure_k)
            else:
                if pure_prod is not None:
                    stretch_hist[pure_k] += 1; pure_prod = None; pure_k = 0
                if is_pair and tb5 == 0:
                    # fresh stretch at the run's start: head must equal c_u exactly
                    assert A[0] == cub, ('C climb start', i, s, A[0], cub)
                    pure_prod = tb[1]; pure_k = 1
                    max_stretch = max(max_stretch, pure_k)
                elif is_pair:
                    st['C_orphan_midrun_pairs'] += 1
            # pointer bookkeeping to compute the post-step pointer i2
            k2 = len(P)
            if k2 >= 2:
                P2 = P[2:]; i2 = i
            else:
                i2 = i + 2 - k2; P2 = []
            dn = i2 - vn
            dm = max(i2 - v2(A[0]), i2 - v2(cb), i2 - v2(cc))
            worst = dn - dm
            if worst > E_worst[0]: E_worst = (worst, (i, s))
            assert worst <= 0, ('E delta', i, s)
            A = (cn, A[1] + lb + lc + 3, max(A[2], Jb, Jc)); P = P2; i = i2
            newp = []
        else:
            cx = A[0] + 2 * cb; lx = A[1] + 2 * lb + 3
            vcx, vlx = v2(cx), v2(lx)
            assert vlx < vcx and A[0] % 2 == 0 and A[1] % 2 == 1
            j = vlx
            mn = min(v2(A[0]), v2(cb) + 1)
            if vcx == mn: Ch_exact += 1
            else:
                Ch_lift += 1
                assert vcx > mn
            u = cx >> j; lu = lx >> j
            JLu = max(A[2], Jb, j)
            du = i - (vcx - j)
            post_chain_slack_worst = max(post_chain_slack_worst, du - JLu)
            head_slack_worst = max(head_slack_worst, dA - A[2])
            vc = v2(cc); vAh = v2(A[0]) - 1
            cD = cc + A[0] // 2
            vD = v2(cD)
            JD = max(A[2], Jb, j, Jc)
            dD = i - vD
            D_slack_worst = max(D_slack_worst, dD - JD - 2)
            if vc > vAh:
                D_sub['vc_gt_vAh'] += 1
                D_gt_headslack_worst = max(D_gt_headslack_worst, dA - JD)
                assert vD == vAh, ('D min', i, s)
            elif vc == vAh:
                D_sub['vc_eq_vAh'] += 1
                assert vD >= vAh + 1, ('D tie lift', i, s)
            else:
                D_sub['vc_lt_vAh'] += 1
                assert vD == vc, ('D min', i, s)
            st['chains'] += 1
            if tb[0] == 'E':
                st['lvl'] += 1
                assert cx == 3 << tb[1], ('L mass', i, s)
                assert i - vcx == 0 and du == j, ('L delta', i, s)
            newp = [[u << t, lu << t, ('M', s), JLu, t, u] for t in range(j - 1)] + \
                   [[cD, lc + (A[1] + 1) // 2, ('D', s), JD, None, None]]
            A = (u, lu + 1, JLu)
            if pure_prod is not None: stretch_hist[pure_k] += 1
            pure_prod = None; pure_k = 0
            k2 = len(P)
            if k2 >= 2: P = P[2:]
            else: i += 2 - k2; P = []
            st['P_adv' if k2 <= 1 else 'P_stay'] += 1
        P = newp + P; s += 1
    print('exact walk to i=%d: %d steps, %d chains, %d level fires' % (N, s, st['chains'], st['lvl']))
    print('(E) even steps = %d: v2(sum)>=min everywhere; ties lifting v2: %d (delta only shrinks);'
          % (st['E'], E_ties))
    print('    worst delta_new - max(delta inputs at post pointer) = %d at %s (need <= 0): %s'
          % (E_worst[0], E_worst[1], E_worst[0] <= 0))
    print('(P) pointer advanced on %d steps (each with <=1 stack entry), stayed on %d (each with >=2):'
          ' consistent with F read rule + implementation' % (st['P_adv'], st['P_stay']))
    print('(C) orphan mid-run same-producer pairs (identity N/A there): %d' % st['C_orphan_midrun_pairs'])
    print('(C) pure-stretch identity head=c_u*4^(k-1) verified EXACTLY; stretch lengths (pairs):',
          dict(sorted(stretch_hist.items())), '; max = %d' % max_stretch)
    print('(Ch) chains: v2(c_x)=min exactly %d, lifted (tie) %d; worst post-chain slack delta(u)-J(u) = %d (need <= 0)'
          % (Ch_exact, Ch_lift, post_chain_slack_worst))
    print('(D) sub-cases: %s ; worst slack(D)=delta(D)-J_D-2 = %d (need <= 0)' % (dict(D_sub), D_slack_worst))
    print("    in 'v_c > v_A-1' sub-case: worst delta_A - J_D = %d (one-line (D) needs <= +1; INV-L gives <= +2)"
          % D_gt_headslack_worst)
    print('    worst head slack at chains delta(A)-J(A) = %d (INV-L allows +2)' % head_slack_worst)
    print('(L) level fires: delta_x = 0 and delta(u) = j at 100%% of %d fires' % st['lvl'])

if __name__ == '__main__':
    run(60000)
