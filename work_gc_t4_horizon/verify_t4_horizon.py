"""verify_t4_horizon.py -- finite checks for work_gc_t4_horizon/NOTES.md (Theorem H-T4).

Usage (from the repository root D:/math_cc):
    python -B work_gc_t4_horizon/verify_t4_horizon.py [total_budget_seconds=480]

Parts (all decisions in exact integer arithmetic; no floats):
 (a) horizon inequality 3(H-1)^2+4 < 2^H: exact for H=16..4096, plus the all-scale
     base + single-step constants (slack 6H-3 < L(H) <=> 3H^2-12H+10 > 0, true for
     every integer H >= 3), so it holds for every integer H >= 16.  The application
     at the irrational H = T4 goes through the real-H chain 3*T4^2 = 3*2^(T3-3) <
     2^(T3+2) < 2^T4 ((T3+2)^2 < 2^(T3-3) checked for T3 = 16..4096; T3 > 2^64 by
     (b)).  Also the derived inequalities used by Theorem H-T4:
     3(H-2)^2+7 < 2^H (F-steps (v-1)^2 and (v-1)^2+1 inside the prefix for v <= H-1)
     and (v-1)^2 < (2^H-4)/3.
 (b) tower ordering with a pure-tower strip comparator (exact integers only):
     T1 < K, T2 < K', K' < T3, T3 < K_clock, K_clock < T4, K' <= K_clock, T4 > 2^64,
     where N0=2e7, T_{h+1}=2^((T_h-3)/2), K=2^(2^499997-2), K'=2^(K/2-2),
     K_clock = floor(2^K'/(64 K'^2)).  Independently re-derives T3 < K_clock < T4.
 (c) machine-level validation of the Corollary H-CLOCK transfer pattern itself, at an
     adaptive ladder of small horizons H0 (top steps 2^H0-2, F prefix (2^H0-5)//3):
     for each achieved H0 --
       * lambda-only walker of the universal walk F (verify_m V2 engine) through the
         whole prefix: margin j < sigma at every top-level chain (F defined), the
         sigma recursion sigma_t = rho - Gamma_t, s <= i^2 (PROOF_CLOCK sec.4),
         tau(n) <= n^2 at recorded crossings (C1), CLOCK s <= i*P(i) at the end;
       * every level fire: J = v2(3s0+4) < rho, J < H0, tau(J-1) <= (J-1)^2;
       * every J in 1..32: S(J) tie-free with r <= max(0, J-2) exit chains, per-chain
         margin h_t = J-Gamma_t-j_t >= 1 and Lemma T(1) identity v2(alpha_x)=J-Gamma_t;
         epoch pattern of the real walk equals the symbolic exit j-sequence
         (PROOF_M Lemma 6.1); cross-checked against work_m/verify_m.sym_exit
         (read-only import, verify_egx.py C3 precedent);
       * top map (work_r1 rules, work_r4 form) through all top steps n < 2^H0-2: no
         halt, sum law 3n+3; every even singleton time n has v = v2(n+2) < H0; for
         every v in 1..32 the pair endgame of E(w,v) equals S(v) chain for chain
         (j and pair x), final singleton (2^v, 3*ell), and the machine gap
         n'-n-1 = ell(v) at EVERY occurrence (D5 + EGX timing); ell(1..20) equals
         the R4 table (work_r4/PROOF.md sec.2);
       * horizon off-by-one: no top step n < 2^H0-2 has v2(n+2) >= H0, and the first
         such top step is exactly 2^H0-2.
     The achieved H0 ladder is adaptive (measured throughput vs the time budget) and
     reported honestly; the analytic theorem does not depend on H0.

Output: ASCII, last line ALL PASS exactly, exit code 0 on success.
Writes t4_horizon_checks.json beside itself.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def v2i(x):
    return (x & -x).bit_length() - 1


# =====================================================================================
# Part (a): horizon inequality 3(H-1)^2 + 4 < 2^H, all integer H >= 16
# =====================================================================================
def part_a(rep):
    # L(H) = 3(H-1)^2+4;  L(H+1) = L(H) + 6H - 3 (exact identity, checked below).
    # Step: L(H+1) < 2*L(H) whenever 6H-3 < L(H); the slack is equivalent to
    # 3H^2-12H+10 > 0, which holds for every integer H >= 3 (discriminant 24, roots
    # 2 +- sqrt(6)/3, minimum 1 at H = 3).  HINQ starts at H = 16, so the step is
    # valid at every stage of the induction (H = 2 would fail the slack: 9 > 7 is
    # false; it is irrelevant to the range).
    assert 12 ** 2 - 4 * 3 * 10 == 24 > 0
    for H in range(3, 4000):
        assert 3 * H * H - 12 * H + 10 > 0            # exact for every integer H >= 3
    assert 3 * 3 * 3 - 12 * 3 + 10 == 1               # minimum over H >= 3, at H = 3
    assert 6 * 2 - 3 > 3 * (2 - 1) ** 2 + 4           # the only failing integer, H = 2
    for H in range(16, 4097):
        assert 3 * (H - 1) ** 2 + 4 < (1 << H)        # base + direct range check
        assert 3 * H * H + 4 == 3 * (H - 1) ** 2 + 4 + 6 * H - 3     # step identity
        assert 6 * H - 3 < 3 * (H - 1) ** 2 + 4                       # step slack
        assert (H - 1) ** 2 - (H - 2) ** 2 - 1 == 2 * H - 4 > 0      # (H-2)^2+1<(H-1)^2
        assert 3 * (H - 2) ** 2 + 7 < (1 << H)        # 3((v-1)^2+1)+4 < 2^H, v <= H-1
        assert 3 * (H - 2) ** 2 + 4 < (1 << H)        # (v-1)^2 < (2^H-4)/3, v <= H-1
    # Real-H instance used at H = T4 (irrational): log2 T4 = (T3-3)/2, so
    # 3*T4^2 = 3*2^(T3-3) < 2^(T3+2) < 2^T4, the last step by T3+2 < 2^((T3-3)/2);
    # the latter holds for all T3 >= 16 ((T3+2)^2 < 2^(T3-3) below: true at 16, and
    # the right side doubles per +1 while the left grows by ((T3+3)/(T3+2))^2 < 2),
    # and T3 > 2^64 by part (b).  Hence 3(T4-1)^2+4 < 3T4^2 < 2^T4, and a fortiori
    # 3(T4-2)^2+7 < 2^T4 and (v-1)^2 < (2^T4-4)/3 for v <= T4-1.
    for T3 in range(16, 4097):
        assert (T3 + 2) ** 2 < (1 << (T3 - 3))
        assert 3 * (1 << (T3 - 3)) < (1 << (T3 + 2))
    rep['a'] = dict(horizon_inequality_H_range=[16, 4096],
                    step_constant='slack 6H-3<L(H) <=> 3H^2-12H+10>0, true for every '
                                  'integer H>=3 (disc 24, min 1 at H=3); HINQ starts at 16',
                    real_H_instance='3T4^2=3*2^(T3-3)<2^(T3+2)<2^T4 via (T3+2)^2<2^(T3-3), '
                                    'T3>=16 (checked 16..4096; T3>2^64 by part b)',
                    derived='3(H-2)^2+7<2^H and (v-1)^2<(2^H-4)/3 for v<=H-1, H>=16')


# =====================================================================================
# Part (b): tower ordering, exact.  Pure tower Tw(k,q) = 2^(2^(...^q)) with k twos.
# tw_cmp: two towers -> compare exponents (2^x strictly increasing, both sides are
# literally 2^something); tower vs small integer b (< 2^24): the tower side is
# 2^(something provably > 64) hence > 2^64 > b; recursion bottoms out in exact
# integer comparisons.  No float is ever computed.
# =====================================================================================
class Tw:
    __slots__ = ('k', 'q')

    def __init__(self, k, q):
        self.k = k
        self.q = q


def tw_cmp(a, b):
    """Exact comparison.  Tw(k,q) is the value 2^(2^(...^q)) (k twos).  Rules:
    - two towers of equal height: strip all k twos on both sides -> compare q's;
    - both towers of height >= 1 (any heights): both are 2^something -> strip one
      level from each and recurse (the shorter side's exponent is Tw(k-1,q), or the
      bare q when it has height 1);
    - tower vs small integer b < 2^24: decide by value (exact when the tower is
      2^q with q <= 23, else the tower is >= 2^24 > b once its exponent is >= 24,
      which is itself decided recursively);
    - integer vs integer: direct."""
    if isinstance(b, int):
        assert 0 <= b < (1 << 24)
        if isinstance(a, int):
            return (a > b) - (a < b)
        if a.k == 0:
            return (a.q > b) - (a.q < b)
        if a.k == 1:
            if a.q < 24:
                v = 1 << a.q                      # exact, small
                return (v > b) - (v < b)
            return 1                              # 2^a.q >= 2^24 > b
        c = tw_cmp(Tw(a.k - 1, a.q), 24)          # exponent >= 24 ?
        assert c > 0, 'tower-vs-integer case outside designed range'
        return 1                                  # 2^(>=24) >= 2^24 > b
    if isinstance(a, int):
        return -tw_cmp(b, a)
    if a.k == b.k:
        return (a.q > b.q) - (a.q < b.q)
    if a.k > b.k:
        if b.k >= 1:
            return tw_cmp(Tw(a.k - 1, a.q), Tw(b.k - 1, b.q))
        return tw_cmp(a, b.q)                     # b's value is the integer b.q
    return -tw_cmp(b, a)


def t_lt(a, b):
    return tw_cmp(a, b) < 0


def part_b(rep):
    # small exact facts used in the bound derivations
    assert (1 << 24) - 3 > 9999999          # 2^24 = 16777216 > 10^7-sized exponents
    # ---- T-side bounds; every step is an exact integer/tower comparison.
    # B1: 2^9999998 < T1 < 2^9999999 (squaring: T1^2 = 2^19999997, T1 = 2^(19999997/2)).
    assert 2 * 9999998 < 19999997 < 2 * 9999999
    T1lo, T1hi = Tw(1, 9999998), Tw(1, 9999999)
    # B2: log2 T2 = (T1-3)/2: lower > (2^9999998-3)/2 = 2^9999997 - 1.5 > 2^9999996;
    #     upper < 2^9999999/2 < 2^9999998.
    assert (1 << 9999997) - 2 > (1 << 9999996)
    T2lo, T2hi = Tw(2, 9999996), Tw(2, 9999998)
    # B3: log2 T3 = (T2-3)/2 > (2^(2^9999996)-3)/2 > 2^(2^9999996-1) - 2
    #     > 2^(2^9999996-2) > 2^(2^9999994)   [A > 4 => 2^(A-1)-2 > 2^(A-2);
    #     upper < 2^(2^9999998-1) < 2^(2^9999998).
    assert (1 << 9999996) > 4
    assert (1 << 9999996) - 2 > (1 << 9999994)
    T3lo, T3hi = Tw(3, 9999994), Tw(3, 9999998)
    # B4: log2 T4 = (T3-3)/2 > (T3lo-3)/2 > 2^(2^(2^9999994)-1) - 2
    #     > 2^(2^(2^9999994)-2) > 2^(2^(2^9999990)); upper < 2^(2^(2^9999998)).
    assert (1 << 9999994) - 1 > (1 << 9999990)
    T4lo, T4hi = Tw(4, 9999990), Tw(4, 9999998)
    # ---- K-side bounds.  K = 2^(2^499997-2): 2^(2^499996) < K < 2^(2^499997).
    assert (1 << 499996) > 2
    K = (Tw(2, 499996), Tw(2, 499997))
    # log2 K' = K/2-2 = 2^(2^499997-3)-2: 2^(2^499997-4) < log2 K' < 2^(2^499997-3),
    # and 2^499997-4 > 2^499496, so 2^(2^(2^499496)) < K' < 2^(2^(2^499997)).
    assert (1 << 499997) - 4 > (1 << 499996)
    Kp = (Tw(3, 499996), Tw(3, 499997))
    # K_clock = floor(2^K'/(64 K'^2)):
    #   upper: K_clock < 2^K'/(64K'^2) < 2^K' < 2^(t(3,499997)).
    #   lower: log2 x <= x/8 for x >= 2^7 (exact for integer y=log2 x >= 7: 8y <= 2^y,
    #   monotone tail checked), so K'-6-2log2K' >= K'-6-K'/4 > K'/2; with x >= 2 also
    #   floor(x) > x/2, hence K_clock > 2^(K'/2) > 2^(2^(2^2^499496)/2) > 2^(2^(2^2^499495))
    #   (2^499496-1 > 2^499495).
    for y in range(7, 64):
        assert 8 * y <= (1 << y)
        assert (1 << (y + 1)) - 8 * (y + 1) > (1 << y) - 8 * y
    assert (1 << 499996) - 1 > (1 << 499495)
    Kc = (Tw(4, 499495), Tw(4, 499997))

    checks = {
        'T1 < K': t_lt(T1hi, K[0]),
        'T2 < K_prime': t_lt(T2hi, Kp[0]),
        'K_prime < T3': t_lt(Kp[1], T3lo),
        'T3 < K_clock': t_lt(T3hi, Kc[0]),
        'K_clock < T4': t_lt(Kc[1], T4lo),
        'K_prime <= K_clock': t_lt(Kp[1], Kc[0]),
        'T4 > 2^64': t_lt(Tw(1, 64), T4lo),
        'K_clock > 2^64': t_lt(Tw(1, 64), Kc[0]),
    }
    for name, ok in checks.items():
        assert ok, name
    # comparator self-tests with known outcomes
    assert t_lt(Tw(1, 5), Tw(1, 6))               # 32 < 64
    assert t_lt(Tw(2, 5), Tw(1, 10 ** 6))         # 2^32 < 2^1000000
    assert not t_lt(Tw(1, 64), Tw(2, 5))          # 2^64 > 2^32
    assert t_lt(Tw(4, 2), Tw(3, 100))             # 2^(2^16) < 2^(2^(2^100))
    assert tw_cmp(Tw(1, 5), 33) < 0 and tw_cmp(Tw(1, 5), 31) > 0
    assert tw_cmp(Tw(0, 7), 7) == 0 and tw_cmp(Tw(2, 5), (1 << 20)) > 0  # 2^32 > 2^20
    rep['b'] = dict(order='T1 < K, T2 < K_prime, K_prime < T3, T3 < K_clock, '
                          'K_clock < T4 (hence K_prime <= K_clock, T4 > 2^64)',
                    method='exact integer exponents + pure-tower strip comparator; no floats')


# =====================================================================================
# Part (c): machine-level transfer validation.
# =====================================================================================
CAP = 4096          # crossing-table size for tau/eps (only indices <= ~32 are read)


def walkA(ncross):
    """Full pair walk (verify_egx.walk engine) until ncross crossings are recorded.
    X: n -> (typ, head pair, Y or None, eps, pointer, full pending list); tau: n -> s.
    Fires and epochs of its short run are recorded and self-checked."""
    A = (1, 1); P = []; i = 0; s = 0
    X = {}; tau = {}; calls = []
    fires = []; epochs = []
    cur = None; ep = None; epJ = None; epRho = None
    while len(X) < ncross:
        while calls and calls[-1] < s:
            calls.pop()
        top = not calls
        k = len(P)
        reads = [] if k >= 2 else ([i] if k == 1 else [i, i + 1])
        for n in reads:
            if n not in X:
                typ = 'a' if (k == 0 and i == n) else ('b' if k == 0 else 'c')
                # Y follows verify_m.Xdata: None (a), the original E_{n-1} (b), the
                # pending entry (c)
                Y = None if typ == 'a' else ((1 << (n - 1), 0) if typ == 'b' else P[0])
                eps = 0 if typ == 'a' else (1 if typ == 'b' else n - v2i(A[0]))
                X[n] = (typ, A, Y, eps, i, list(P))
                tau[n] = s
        ents = list(P[:2]); a = i
        while len(ents) < 2:
            ents.append((1 << a, 0)); a += 1
        b, c = ents
        if (A[0] + A[1]) % 2 == 0:
            if top and k >= 1 and ep is not None:      # even return closes the epoch
                epochs.append((epJ, epRho, ep)); ep = None
            A = (A[0] + b[0] + c[0], A[1] + b[1] + c[1] + 3); newp = []
        else:
            x = (A[0] + 2 * b[0], A[1] + 2 * b[1] + 3)
            vc = v2i(x[0]); j = v2i(x[1])
            assert j < vc and A[0] % 2 == 0, ('chain S1/S2 fails', s)
            u = (x[0] >> j, x[1] >> j)
            if top:
                if k == 0:                              # level fire
                    assert vc == i, ('fire sigma_0 = rho', s)
                    assert j == v2i(3 * s + 4), ('fire J = v2(3s+4)', s)
                    fires.append((i, s, j))
                    ep = []; epJ = j; epRho = i
                    cur = (vc, j)
                else:                                   # exit chain
                    sig = vc
                    assert sig == cur[0] - 1 - X[cur[1] - 1][3], ('sigma recursion', s)
                    ep.append((j, sig))
                    cur = (sig, j)
                assert j < cur[0], ('margin', s)
            T = tau.get(j - 1)
            if T > 0:
                calls.append(s + T)
            newp = [(u[0] << t, u[1] << t) for t in range(j - 1)] + \
                   [(c[0] + A[0] // 2, c[1] + (A[1] + 1) // 2)]
            A = (u[0], u[1] + 1)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k; P = []
        P = newp + P; s += 1
    # an epoch still open at the cut is partial (its recorded chains were checked
    # inline); it is not appended to `epochs`, whose entries are closed epochs only.
    return X, tau, fires, epochs


def sym_walk(J, X):
    """Symbolic exit S(J) per PROOF_M Lemma 6.1 (verify_egx.symexit engine).
    Returns (chains list of dicts, types string, None) or (..., ('TIE'|'NODATA', ...))."""
    u = (1, 0); D = (1 << (J - 1), -1); j = J
    out = []; G = 0; typs = ''
    while True:
        n = j - 1
        if n not in X:
            return out, typs, ('NODATA', n)
        typ, AX, Y, eps = X[n][0], X[n][1], X[n][2], X[n][3]
        typs += typ
        H = (AX[0] * u[0], AX[0] * u[1] + AX[1])
        if (H[0] + H[1]) % 2 == 0:
            return out, typs, None
        bb = D if typ == 'a' else (Y[0] * u[0], Y[0] * u[1] + Y[1])
        G += 1 + eps
        x = (H[0] + 2 * bb[0], H[1] + 2 * bb[1] + 3)
        va = 10 ** 18 if x[0] == 0 else v2i(x[0])
        vb = 10 ** 18 if x[1] == 0 else v2i(x[1])
        assert va == J - G, ('Lemma T(1): v2(alpha_x) = J - Gamma', J, va, J - G)
        if not vb < va:
            return out, typs, ('TIE', J, len(out))
        assert H[0] % 2 == 0 and H[1] % 2 == 1, ('S2', J)
        j = vb; u = (x[0] >> j, x[1] >> j)
        Dn = (H[0] // 2, (H[1] + 1) // 2)
        D = Dn if typ == 'a' else (D[0] + Dn[0], D[1] + Dn[1])
        assert J - G - j >= 1, ('margin h_t >= 1', J)
        out.append(dict(j=j, x=x, typ=typ, G=G, h=J - G - j))
        if len(out) > 64:
            return out, typs, ('LONG', J)


def endgame_run(v, X, tau):
    """Pair endgame of E(w,v) from F's state X(v-1) (verify_egx.endgame engine).
    Returns (chains [(j,x)], final pair, final absolute step count)."""
    typ, A, Y, eps, ix, Q = X[v - 1]
    Q = list(Q); s = tau[v - 1]; chains = []
    while True:
        ents = list(Q[:2]); a = ix
        while len(ents) < 2 and a <= v - 1:
            ents.append((1 << a, 0) if a < v - 1 else (1 << (v - 1), -1)); a += 1
        if not ents:
            return chains, A, s
        if len(ents) == 1:
            ents.append((0, 0))
        b, c = ents
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + b[0] + c[0], A[1] + b[1] + c[1] + 3); newp = []
        else:
            x = (A[0] + 2 * b[0], A[1] + 2 * b[1] + 3); j = v2i(x[1])
            if not (j < v2i(x[0]) and A[0] % 2 == 0):
                return None, ('UNSAFE', v), s
            chains.append((j, x))
            u = (x[0] >> j, x[1] >> j)
            newp = [(u[0] << t, u[1] << t) for t in range(j - 1)] + \
                   [(c[0] + A[0] // 2, c[1] + (A[1] + 1) // 2)]
            A = (u[0], u[1] + 1)
        if len(Q) >= 2:
            Q = Q[2:]
        else:
            ix = a; Q = []
        Q = newp + Q; s += 1


def lam_walkB(s_star, H0, sym_by_J):
    """Lambda-only walker of the universal walk F through steps 0..s_star-1
    (verify_m V2 engine) with per-fire bookkeeping and pattern checks."""
    lA = 1; S = []; i = 0; s = 0
    Xt = [None] * CAP; Xeps = [0] * CAP
    calls = []; sig_last = None; jl = None
    first = True
    H0pow = 1 << H0
    nfires = 0; nchains = 0; nepochs = 0
    fireJ = {}
    ep = None; epJ = None; epRho = None
    while s < s_star:
        while calls and calls[-1] < s:
            calls.pop()
        k = len(S)
        lb = S[-1] if k >= 1 else 0
        lc = S[-2] if k >= 2 else 0
        nb = None if k >= 2 else i
        nc = None if k >= 1 else i + 1
        for n in (nb, nc):
            if n is not None and n < CAP and Xt[n] is None:
                assert not calls
                Xt[n] = s
                assert s <= n * n, ('C1: tau(n) <= n^2', n, s)
                if k == 0 and i == n:
                    e = 0
                elif k == 0:
                    e = 1
                else:
                    e = n - (sig_last - 1)
                Xeps[n] = e
        if i >= 16:
            assert s <= i * i, ('state clock: s <= i^2', s, i)
        par = (lA + (1 if first else 0)) & 1
        push = None
        if par == 0:
            if not calls and k >= 1 and ep is not None:      # even return: epoch end
                nepochs += 1
                js, hs = sym_by_J[epJ]
                assert tuple(j for j, _ in ep) == js[1:], ('epoch pattern != S(J)', epJ, s)
                assert len(ep) <= max(0, epJ - 2), ('r <= max(0,J-2)', epJ)
                ep = None
            lA = lA + lb + lc + 3
        else:
            lx = lA + 2 * lb + 3; j = v2i(lx); u = lx >> j
            if not calls:
                if k == 0:                                    # level fire
                    assert ep is None, ('fire with open epoch', s)
                    assert j == v2i(3 * s + 4), ('fire J', s)
                    assert 3 * s + 4 < H0pow, ('fire beyond horizon', s, j)
                    gP = (6 * i * i + 5).bit_length()
                    assert s <= i * (2 * gP * gP + 1345), ('CLOCK s<=iP(i) at fire', s, i)
                    nfires += 1
                    sg = i
                    rec = fireJ.get(j)
                    if rec is None:
                        fireJ[j] = [1, i - j]
                    else:
                        rec[0] += 1; rec[1] = min(rec[1], i - j)
                    assert j < sg, ('fire margin J < rho', i, s, j)
                    assert Xt[j - 1] is not None and Xt[j - 1] <= (j - 1) * (j - 1), \
                        ('tau(J-1) <= (J-1)^2', j)
                    ep = []; epJ = j; epRho = i
                else:                                         # exit chain
                    sg = sig_last - 1 - Xeps[jl - 1]
                    nchains += 1
                    ep.append((j, sg))
                assert j < sg, ('margin j < sigma', i, s, j, sg)
                sig_last = sg; jl = j
            assert j - 1 < CAP and Xt[j - 1] is not None, ('replay data', j)
            T = Xt[j - 1]
            if T > 0:
                calls.append(s + T)
            push = (u, j, lc + (lA + 1) // 2)
            lA = u + 1
        if k >= 2:
            del S[-2:]
        else:
            i += 2 - k; S.clear()
        if push:
            u, j, D = push
            S.append(D)
            for t in range(j - 2, -1, -1):
                S.append(u << t)
        s += 1; first = False
    g = (6 * i * i + 5).bit_length()
    assert s <= i * (2 * g * g + 1345), ('CLOCK: s <= i*P(i)', s, i)
    if ep is not None:                                        # epoch cut by s_star
        js, hs = sym_by_J[epJ]
        assert tuple(j for j, _ in ep) == js[1:1 + len(ep)]
    return dict(fires=nfires, chains=nchains, epochs=nepochs, fireJ=fireJ,
                ptr=i, steps=s, Xt=Xt, Xeps=Xeps)


def top_map_run(H0, ell_of_v):
    """Top map from (3) through top steps n = 0..2^H0-3 (work_r1 rules; work_r4 form).
    No halt; sum law; singleton structure; gap == ell(v) at every even-singleton
    excursion; v < H0; horizon off-by-one."""
    N = (1 << H0) - 2
    L = [3]; n = 0
    singles = 0; vcount = {}
    last = None
    maxv = 0; gapchecks = 0
    while n < N:
        A = L[0]
        if A & 1:
            b = L[1] if len(L) > 1 else 0
            X = A + 2 * b + 3
            if X & (X - 1) == 0:
                return dict(HALT=True, n=n, X=X)
        if len(L) == 1:
            singles += 1
            if last is not None and last[1] is not None:
                gap = n - last[0] - 1
                assert gap == ell_of_v[last[1]], ('gap != ell(v)', last, gap)
                gapchecks += 1
            if n % 2 == 0:
                v = v2i(n + 2)
                assert v < H0, ('singleton v >= H0', n, v)
                maxv = max(maxv, v)
                vcount[v] = vcount.get(v, 0) + 1
                last = (n, v)
            else:
                last = (n, None)
        b = L[1] if len(L) > 1 else 0
        c = L[2] if len(L) > 2 else 0
        if A % 2 == 0:
            L = [A + b + c + 3] + L[3:]
        else:
            m = b + (A - 3) // 2
            St = [c + (A + 1) // 2] + L[3:]
            while m & 1:
                assert m >= 3, ('halt m==1', n)
                St = [(m + 3) // 2] + St
                m = (m - 3) // 2
            L = [m + 4] + St
        n += 1
        assert sum(L) == 3 * n + 3, ('sum law', n)
    assert v2i(((1 << H0) - 2) + 2) >= H0          # first n with v2(n+2)>=H0 is 2^H0-2
    assert v2i(((1 << H0) - 3) + 2) < H0
    return dict(HALT=False, singles=singles, vcount=vcount, maxv=maxv,
                topsteps=N, gapchecks=gapchecks)


symJA = {}        # global for walkA's epoch check (filled in part_c)


def part_c(rep, budget_total):
    t0 = time.time()
    XA, tauA, firesA, epochsA = walkA(64)
    Xm = {n: (XA[n][0], XA[n][1], XA[n][2], XA[n][3]) for n in XA}

    # S(J) for all J that can arise (fires and singleton v's are < H0 <= 30)
    sym_by_J = {}
    for J in range(1, 33):
        chains, typs, bad = sym_walk(J, Xm)
        assert bad is None, ('S(J) not closed/tie-free', J, bad)
        assert len(chains) <= max(0, J - 2), ('r <= max(0,J-2)', J)
        sym_by_J[J] = ((J,) + tuple(c['j'] for c in chains),
                       tuple(c['h'] for c in chains))
    # walkA's own closed epochs must match the symbolic patterns (full-pair engine)
    for (eJ, eRho, echains) in epochsA:
        assert tuple(j for j, _ in echains) == sym_by_J[eJ][0][1:], \
            ('walkA epoch != S(J)', eJ)
        assert len(echains) <= max(0, eJ - 2)

    # read-only cross-check against work_m/verify_m.sym_exit (verify_egx C3 precedent)
    sys.path.insert(0, str(ROOT / 'work_m'))
    try:
        import verify_m as vm
        for J in range(1, 33):
            chains, typs, bad = sym_walk(J, Xm)
            r = vm.sym_exit(J, {n: Xm[n] for n in range(J)})
            assert r == ((J,) + tuple(c['j'] for c in chains), typs, len(chains),
                         chains[-1]['G'] if chains else 0), ('sym_exit mismatch', J, r)
        rep['c_symexit_crosscheck'] = ('own walker == work_m.verify_m.sym_exit '
                                       'for 1 <= J <= 32 (j-sequence, types, r, Gamma)')
    except ImportError:
        rep['c_symexit_crosscheck'] = 'skipped (work_m not importable)'

    # ell(v) and endgame == S(v) chain for chain, v = 1..32; R4 table cross-check
    ell_of_v = {}
    for v in range(1, 33):
        chains, final, slen = endgame_run(v, XA, tauA)
        assert chains is not None, ('endgame unsafe', v)
        sch, typs, bad = sym_walk(v, Xm)
        assert bad is None
        assert chains == [(c['j'], c['x']) for c in sch], \
            ('endgame != S(v) chain for chain', v)
        assert final == (1 << v, 3 * slen), ('E4 final singleton', v)
        ell_of_v[v] = slen
    r4ell = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16]
    assert [ell_of_v[v] for v in range(1, 21)] == r4ell, 'ell != R4 table'
    rep['c_endgame'] = ('pair endgame == S(v) chain for chain (j, x) for 1 <= v <= 32; '
                        'ell(1..20) == R4 table')

    # adaptive ladder
    ladder = [20, 22, 24, 26, 28, 30]
    per_run_budget = budget_total * 0.6
    achieved = []
    rates = {'lam': None, 'top': None}
    rep['c_runs'] = []
    for idx, H0 in enumerate(ladder):
        s_star = ((1 << H0) - 2) // 3   # = M = (2^H0-4)/3 for even H0: steps 0..M-1
        ntop = (1 << H0) - 2
        pred = 0.0
        if rates['lam']:
            pred += s_star / rates['lam']
        if rates['top']:
            pred += ntop / rates['top']
        if idx > 0 and (pred > per_run_budget or time.time() - t0 + pred > budget_total):
            rep['c_stop'] = 'budget stop before H0=%d (predicted %.0f s)' % (H0, pred)
            break
        t1 = time.time()
        walkrec = lam_walkB(s_star, H0, sym_by_J)
        t2 = time.time()
        top = top_map_run(H0, ell_of_v)
        t3 = time.time()
        assert top['HALT'] is False, ('machine halted', H0)
        rates['lam'] = s_star / max(1e-9, t2 - t1)
        rates['top'] = ntop / max(1e-9, t3 - t2)
        for n in range(64):
            assert walkrec['Xt'][n] == tauA[n], ('tau A/B mismatch', n)
            assert walkrec['Xeps'][n] == XA[n][3], ('eps A/B mismatch', n)
        for J in walkrec['fireJ']:
            assert J in sym_by_J and J < H0, ('fire J unprepared', J)
        for v in top['vcount']:
            assert v in ell_of_v and v < H0
        achieved.append(H0)
        rep['c_runs'].append(dict(
            H0=H0, f_steps=s_star, top_steps=ntop, ptr=walkrec['ptr'],
            fires=walkrec['fires'], chains=walkrec['chains'],
            fire_Js=sorted(walkrec['fireJ'].items()),
            min_margin=min(rec[1] for rec in walkrec['fireJ'].values()),
            epochs_closed=walkrec['epochs'],
            singletons=top['singles'], distinct_v=sorted(top['vcount'].items()),
            max_singleton_v=top['maxv'], gap_checks=top['gapchecks'],
            lam_s=round(t2 - t1, 2), top_s=round(t3 - t2, 2)))
    rep['c_achieved_H0'] = achieved
    rep['c_total_s'] = round(time.time() - t0, 1)
    rep['c_claim'] = ('machine-level H-CLOCK transfer pattern verified for every achieved '
                      'H0: F defined on the whole prefix (margin j<sigma at every '
                      'top-level chain), every fire J<rho with J<H0, tau(J-1)<=(J-1)^2, '
                      'epoch pattern == S(J) with r<=max(0,J-2) and h>=1, no halt in '
                      '2^H0-2 top steps, every singleton v<H0 with gap==ell(v), '
                      'endgame == S(v) chain for chain')


def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 480.0
    rep = {}
    part_a(rep)
    print('[a] horizon inequality 3(H-1)^2+4<2^H exact H=16..4096 + all-scale step: OK')
    part_b(rep)
    print('[b] tower order T1<K, T2<Kp, Kp<T3, T3<Kclock, Kclock<T4 (exact): OK')
    part_c(rep, budget)
    for r in rep.get('c_runs', []):
        print('[c] H0=%d: F prefix %d steps (ptr %d, %d fires, %d chains, %d epochs), '
              '%d top steps, %d singletons, max v %d, %d gap checks (%.1fs + %.1fs)' % (
                  r['H0'], r['f_steps'], r['ptr'], r['fires'], r['chains'],
                  r['epochs_closed'], r['top_steps'], r['singletons'],
                  r['max_singleton_v'], r['gap_checks'], r['lam_s'], r['top_s']))
    print('[c] achieved H0 ladder: %s (total %.1f s)' % (
        rep.get('c_achieved_H0'), rep.get('c_total_s', 0.0)))
    rep['result'] = 'PASS'
    HERE.joinpath('t4_horizon_checks.json').write_text(json.dumps(rep, indent=1) + '\n')
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
