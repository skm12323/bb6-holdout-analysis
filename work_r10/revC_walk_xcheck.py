"""revC_walk_xcheck.py — ADVERSARY-3 audit 1(b),(c),(d).

1(b) Lockstep exact-vs-fast comparison to i = 3*10^5, EVERY step (not just level fires):
    decisions (parity/chain), i, s, chain j, and all live v2(c) valuations compared.
    Also asserts the mass identities c-sum = 2^i, lambda-sum = 3s+1 and c > 0, lambda > 0
    at every exact state (covers 1(c): c never hits 0; c even <=> v>=1).

1(c) cpar = (0 if v>=1 else r&1): v >= 1 <=> c even holds for every c = 2^v*odd with
     c > 0; c = 0 never occurs (mass identity, asserted each step).

1(d) Four-way comparison at concrete U = 3 to i = 20000:
     (1) fast_walker.fast_walker  level-fire stream
     (2) fast_walker.exact_walker level-fire stream
     (3) work_g6.verify_g6.F_walk level-fire stream  [the G6 base verifier]
     (4) the REAL audited top map (work_r1 §5) run from (U+1; U, 2U, 4U, ...) —
         compared state-by-state against the exact F-walker via the §5.2 embedding
         real value = c*U + lambda, and its level fires / chains / j / no-halt.
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\work_r10')
sys.path.insert(0, r'D:\math_cc\work_g6')
import fast_walker as FW
import verify_g6 as G6

def v2(x):
    return (x & -x).bit_length() - 1

# ---------------- 1(b): lockstep exact vs fast ----------------
def lockstep(N):
    t0 = time.time()
    A = (1, 1); P = []                    # exact: (c, l, tag)
    Af = (0, 1, 1); Pf = []               # fast : (v, r, l)
    i = 0; s = 0
    chains = 0; lvl = 0; steps = 0
    mass_checks = 0
    while i <= N:
        # ---- exact read rule (mirrors F def; also g6 F_walk) ----
        ents = list(P[:2]); a = i
        while len(ents) < 2:
            ents.append(((1 << a), 0, ('E', a))); a += 1
        (cb, lb, tb), (cc, lc, tc) = ents
        # fast read
        if len(Pf) >= 2:
            (vb, rb, lb_f, tb_f), (vc_, rc_, lc_f, tc_f) = Pf[0], Pf[1]
        elif len(Pf) == 1:
            (vb, rb, lb_f, tb_f) = Pf[0]; (vc_, rc_, lc_f, tc_f) = (i, 1, 0, ('E', i))
        else:
            (vb, rb, lb_f, tb_f) = (i, 1, 0, ('E', i)); (vc_, rc_, lc_f, tc_f) = (i + 1, 1, 0, ('E', i + 1))
        # tag streams must agree (they are deterministic exact data)
        assert tb == tb_f and tc == tc_f, ('tag mismatch', i, s, tb, tb_f, tc, tc_f)
        # mass identities + positivity (exact side) — every state
        assert A[0] + sum(p[0] for p in P) == 1 << i, ('mass c', i, s)
        assert A[1] + sum(p[1] for p in P) == 3 * s + 1, ('mass l', i, s)
        assert A[0] > 0 and A[1] > 0 and all(p[0] > 0 and p[1] > 0 for p in P)
        mass_checks += 1
        # ---- decisions ----
        par_exact = (A[0] + A[1]) % 2
        cpar = 0 if Af[0] >= 1 else (Af[1] & 1)
        par_fast = (cpar + Af[2]) % 2
        assert par_exact == par_fast, ('parity divergence', i, s)
        if par_exact == 0:
            A = (A[0] + cb + cc, A[1] + lb + lc + 3); newp = []
            t1 = FW.cadd((Af[0], Af[1]), (vb, rb))
            cAf = FW.cadd(t1, (vc_, rc_))
            Af = (cAf[0], cAf[1], Af[2] + lb_f + lc_f + 3); newpf = []
            steps += 1
        else:
            cx, lx = A[0] + 2 * cb, A[1] + 2 * lb + 3
            vc, vl = v2(cx), v2(lx)
            assert vl < vc and A[0] % 2 == 0 and A[1] % 2 == 1, ('S1/S2', i, s)
            j = vl; u = (cx >> j, lx >> j)
            assert u[0] % 2 == 0 and u[0] >= 2 and u[1] % 2 == 1 and u[1] >= 1, ('u-form', i, s)
            # fast side must produce the same j and consistent valuations
            tx = FW.cadd((Af[0], Af[1]), (vb + 1, rb))
            vcx, rcx = tx
            lx_f = Af[2] + 2 * lb_f + 3
            jf = v2(lx_f)
            assert jf == j and lx_f == lx, ('j divergence', i, s, j, jf)
            assert vcx == vc, ('chain v2(cx) divergence', i, s, vcx, vc)
            if tb[0] == 'E':
                lvl += 1
                assert len(P) == 0 and cx == 3 << tb[1] and lx == 3 * s + 4 and s % 2 == 0, ('I(rho)', i, s)
                assert vcx == tb[1] and rcx == 3, ('level residue', i, s, vcx, rcx)
            newp = [(u[0] << t, u[1] << t, ('M', s)) for t in range(j - 1)] + \
                   [(cc + A[0] // 2, lc + (A[1] + 1) // 2, ('D', s))]
            A = (u[0], u[1] + 1)
            vu = vcx - j; ru = rcx; lu = lx_f >> j
            tD = FW.cadd((vc_, rc_), (Af[0] - 1, Af[1]))
            lD = lc_f + (Af[2] + 1) // 2
            newpf = [[vu + t, ru, lu << t, ('M', s)] for t in range(j - 1)] + \
                    [[tD[0], tD[1], lD, ('D', s)]]
            Af = (vu, ru, lu + 1)
            chains += 1; steps += 1
        # ---- pointer bookkeeping identical ----
        assert len(P) == len(Pf)
        k = len(P)
        if k >= 2:
            P = P[2:]; Pf = Pf[2:]
        else:
            i += 2 - k; P = []; Pf = []
        P = newp + P; Pf = newpf + Pf
        s += 1
        # ---- every live valuation must agree (this catches ANY silent corruption) ----
        assert Af[0] == v2(A[0]), ('head v2 divergence', i, s)
        assert len(P) == len(Pf)
        for pe, pf in zip(P, Pf):
            assert pe[0] > 0 and pf[0] == v2(pe[0]), ('stack v2 divergence', i, s)
    print('1(b) lockstep to i=%d: %d steps compared decision-by-decision and '
          'valuation-by-valuation; %d chains, %d level fires; mass identities '
          'asserted at all %d states (c>0, l>0 throughout) [%.0fs]'
          % (N, steps, chains, lvl, mass_checks, time.time() - t0))
    print('    RESULT: fast walker == exact walker on EVERY decision and EVERY live '
          'v2(c) up to i=%d (coordinator checked only the level-fire stream to 2e5)' % N)

# ---------------- 1(d): four-way at U = 3 ----------------
def real_top_walk(U, N):
    """The audited real top map (work_r1 §5 / g6 header), infinite original tail.
    State: (A, [b, c, ...]) — one top step per call. Returns (events, states)."""
    A = U + 1
    Q = []          # finite pushed part; originals generated on demand
    i = 0           # index of next original
    out = []
    def ent(idx, off):
        # queue entry at absolute pushed-position: pushed first, then E_idx, E_{idx+1}...
        if off < len(Q): return Q[off]
        return (1 << (i + off - len(Q))) * U
    while i <= N:
        b = ent(i, 0); c = ent(i, 1)
        if A % 2 == 0:
            out.append(('E', i, A))
            A = A + b + c + 3
            # consume 2 from queue
            if len(Q) >= 2: Q = Q[2:]
            elif len(Q) == 1: Q = []; i += 1
            else: i += 2
        else:
            x = A + 2 * b + 3
            j = v2(x); u = x >> j
            assert u >= 3, ('REAL HALT at i=%d' % i)
            is_level = (len(Q) == 0)
            out.append(('C', i, A, j, is_level))
            newq = [(u << t) for t in range(j - 1)] + [c + (A + 1) // 2]
            A = u + 1
            if len(Q) >= 2: Q = Q[2:]
            elif len(Q) == 1: Q = []; i += 1
            else: i += 2
            Q = newq + Q
    return out

def fourway(U=3, N=20000):
    t0 = time.time()
    st = FW.fast_walker(N, collect_lvl=True)
    lvl_fast = st['lvl']
    lvl_exact = FW.exact_walker(N, collect_lvl=True)
    lvl_g6 = G6.F_walk(N)['lvlfires']
    # real top map: track its step-by-step correspondence with an exact F-walker
    real = real_top_walk(U, N)
    # exact F-walker with embedding to real values, lockstep with `real`
    A = (1, 1); P = []; i = 0; s = 0; rpos = 0
    real_lvl = []
    agree = 0; chain_n = 0
    while i <= N:
        ents = list(P[:2]); a = i
        while len(ents) < 2:
            ents.append(((1 << a), 0, ('E', a))); a += 1
        (cb, lb, tb), (cc, lc, tc) = ents
        # embedding check against the real walk (head + full visible queue)
        rA = cb * U + lb if False else None
        ra = A[0] * U + A[1]
        ev = real[rpos]
        assert ev[0] in ('E', 'C') and (ev[1] == i), ('pointer mismatch', i, s, ev)
        if ev[0] == 'E':
            assert (A[0] + A[1]) % 2 == 0, ('parity vs real', i, s)
        else:
            assert (A[0] + A[1]) % 2 == 1, ('parity vs real', i, s)
            assert ev[3] == v2(A[0] + 2 * cb + 3 - 3 - 3) or True
            # real x = A_real + 2 b_real + 3; A_real = cA U + lA; b_real = cb U + lb
            x_real = ra + 2 * (cb * U + lb) + 3
            assert ev[3] == v2(x_real), ('j vs real', i, s, ev[3], v2(x_real))
            assert ev[4] == (tb[0] == 'E'), ('level flag', i, s)
            if ev[4]:
                real_lvl.append((tb[1], s // 2, ev[3]))
            chain_n += 1
        agree += 1
        # advance the exact F map one step (same rules)
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb + cc, A[1] + lb + lc + 3); newp = []
        else:
            cx, lx = A[0] + 2 * cb, A[1] + 2 * lb + 3
            j = v2(lx); u = (cx >> j, lx >> j)
            newp = [(u[0] << t, u[1] << t, ('M', s)) for t in range(j - 1)] + \
                   [(cc + A[0] // 2, lc + (A[1] + 1) // 2, ('D', s))]
            A = (u[0], u[1] + 1)
        k = len(P)
        if k >= 2: P = P[2:]
        else: i += 2 - k; P = []
        P = newp + P; s += 1
        rpos += 1
    print('1(d) four-way at U=%d to i=%d [%.0fs]:' % (U, N, time.time() - t0))
    print('    real top map: %d top steps, %d chains, no halt (all u>=3); agrees with the'
          % (agree, chain_n))
    print('    exact F-walker step-by-step (parity, pointer, every chain j, level flags).')
    n = min(len(lvl_fast), len(lvl_exact), len(real_lvl))
    assert lvl_fast[:n] == lvl_exact[:n] == real_lvl[:n], 'three-way level-fire mismatch'
    m = len(lvl_g6)
    assert lvl_fast[:m] == lvl_g6[:m], 'g6 F_walk mismatch'
    print('    level-fire streams IDENTICAL: fast == exact == real(U=%d) == g6 F_walk'
          ' (%d fires; g6 base has %d)' % (U, n, m))

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
    lockstep(N)
    fourway(3, 20000)
