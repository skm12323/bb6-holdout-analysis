"""work_r10/agentC10_lib.py — ENDGAME library (scope D5 of the repaired Theorem R,
work_g6 PROOF_G6.md §5.5).  Adapted from work_r10/fast_walker.py (the formal
pair map F of §5.1), extended from the infinite walk to the REAL EXCURSIONS

    E(w,v) = (3w+1; 3w, 6w, ..., 3w*2^{v-2}, 3w*2^{v-1} - 1),      U = 3w,

i.e. the suffix entry at index v-1 is the DEFECT pair (2^(v-1), -1)  (lambda = -1,
negative), the run ENDS there (no E_v, E_{v+1}, ...), and a missing second read
entry is the ZERO pair (0,0) — the audited top map reads missing entries as 0
(work_r1 RULES.md §5: "missing entries = 0").

All pair arithmetic is U-free: a pair (c, l) denotes the value c*U + l for every
odd U; v2(l) is the exact 2-adic valuation (negative l fine).

Engines
  concrete_excursion(U, v)  ground truth: the audited top map on integer lists;
  excursion_pairs(v, ...)   exact bigint pair walk of the excursion from the start
                            state (per-step checks: S1, S2, u-form, mass identities);
  walk_master(Nmax)         exact pair walk of the INFINITE run F, recording the
                            CROSSING state at every suffix index n (the state just
                            before the first read of E_n) and the level-fire stream;
  endgame_run(v, ...)       the endgame = dynamics from the crossing at v-1 to the
                            singleton.  c-values as exact (odd q, deficit d) pairs
                            c = q * 2^((v-1)-d); lambdas either exact (affine
                            a=0) or affine in t (v = v0 + 2^m*t).  ONE runner for
                            the per-v concrete check and the per-class symbolic
                            proof; every decision must be uniform in t.

Safety logic (proof in agentC10_report.md §2): every chain of the excursion has
u = c_u*U + l_u with c_u even >= 2 and l_u odd >= 1, hence u >= 2U+1 >= 3 for
every odd U >= 1 (u is increasing in U; checked at U=1): NO HALT, provided the
margin (S1) v2(l_x) < v2(c_x) and (S2) c_A even hold at that chain.  The
excursion terminates at the singleton pair (2^v, 3*ell(v)).
"""
from collections import deque


def v2i(x):
    """Exact 2-adic valuation of x != 0 (negative x is fine)."""
    return (x & -x).bit_length() - 1


# ---------------------------------------------------------------------------
# Ground truth: the audited top map on integer lists.
# ---------------------------------------------------------------------------

def concrete_excursion(U, v, cap=200000, record=None):
    """The real excursion E(w,v) (U = 3w) under the audited top map.
    Even: A <- A+b+c+3 (missing entries read as 0).  Chain: x = A+2b+3 = 2^j*u,
    successor (u+1; u,2u,...,2^{j-2}u, c+(A+1)/2, S); HALT iff u == 1.
    Returns (final, steps, min_u, jseq, halted).  record(step, A, Q) per step
    is called with the PRE-step state (A head, Q remaining entries as deque)."""
    A = U + 1
    Q = deque((U << a) for a in range(v - 1))
    Q.append((U << (v - 1)) - 1)
    steps = 0
    minu = None
    jseq = []
    while Q:
        if steps > cap:
            return None, steps, minu, jseq, 'CAP'
        if record is not None:
            record(steps, A, Q)
        b = Q.popleft()
        c = Q.popleft() if Q else 0
        if (A & 1) == 0:
            A = A + b + c + 3
            jseq.append(0)
        else:
            x = A + 2 * b + 3
            j = v2i(x)
            u = x >> j
            if u == 1:
                return None, steps, minu, jseq, True
            if minu is None or u < minu:
                minu = u
            jseq.append(j)
            Q.appendleft(c + ((A + 1) >> 1))
            for t in range(j - 2, -1, -1):
                Q.appendleft(u << t)
            A = u + 1
        steps += 1
    return A, steps, minu, jseq, False


# ---------------------------------------------------------------------------
# Exact pair walk of the excursion (validation engine).
# ---------------------------------------------------------------------------

def excursion_pairs(v, cap=5000, check_mass=True, record=None):
    """Exact bigint pair walk of the excursion with boundary at index v-1, from
    the start state A=(1,1), pointer i=0.  Suffix on demand: index a < v-1 ->
    (2^a, 0); index v-1 -> (2^{v-1}, -1) (once); after that the only fill is the
    ZERO pair (0,0) as the second read entry when the queue has exactly one
    entry left.  Terminates at the singleton; asserts S1/S2/u-form/mass
    identities at every step.  record(step, (cA,lA), list(Q), i, bnd) per step
    with the PRE-step state.  Returns dict(ell, s_cross, dec, final, stats...)."""
    A0 = 1
    A1 = 1
    Q = deque()
    i = 0
    s = 0
    bnd = True          # boundary entry still unread
    dec = []
    s_cross = None
    st = dict(minlx=None, minlu=None, minu1=None, maxj=0)
    while True:
        if not Q and (not bnd) and i >= v:
            break                                     # singleton reached
        assert s <= cap, 'excursion cap'
        if s_cross is None:
            # first step whose read window contains index v-1
            nQ = len(Q)
            if (nQ == 0 and i <= v - 1 <= i + 1) or (nQ == 1 and i == v - 1):
                s_cross = s
        if record is not None:
            record(s, (A0, A1), list(Q), i, bnd)
        # ---- read b, c
        if Q:
            b = Q.popleft()
        elif i < v - 1:
            b = (1 << i, 0); i += 1
        else:
            assert bnd, 'read past the end (b)'
            b = (1 << (v - 1), -1); bnd = False; i += 1
        if Q:
            c = Q.popleft()
        elif i < v - 1:
            c = (1 << i, 0); i += 1
        elif bnd:
            c = (1 << (v - 1), -1); bnd = False; i += 1
        else:
            c = (0, 0)                                # missing entry = 0
        # ---- one top-map step in pair form
        if (A0 + A1) % 2 == 0:
            dec.append(0)
            A0 += b[0] + c[0]
            A1 += b[1] + c[1] + 3
        else:
            assert A0 % 2 == 0, 'S2 (c_A even)'
            cx = A0 + 2 * b[0]
            lx = A1 + 2 * b[1] + 3
            assert lx >= 2 and lx % 2 == 0, ('sign lemma', s, lx)
            j = v2i(lx)
            vcx = v2i(cx)
            assert j < vcx, ('S1 margin', s, j, vcx)
            cu = cx >> j
            lu = lx >> j
            assert cu >= 2 and cu % 2 == 0 and lu >= 1 and lu % 2 == 1, ('u-form', s)
            u1 = cu + lu                               # u at U=1
            if st['minu1'] is None or u1 < st['minu1']:
                st['minu1'] = u1
            if st['minlx'] is None or lx < st['minlx']:
                st['minlx'] = lx
            if st['minlu'] is None or lu < st['minlu']:
                st['minlu'] = lu
            if j > st['maxj']:
                st['maxj'] = j
            Q.appendleft((c[0] + (A0 >> 1), c[1] + ((A1 + 1) >> 1)))
            for t in range(j - 2, -1, -1):
                Q.appendleft((cu << t, lu << t))
            A0 = cu; A1 = lu + 1
            dec.append(j)
        s += 1
        assert A1 >= 0 and all(p[1] >= 0 for p in Q), ('lambda sign', s)
        if check_mass:
            cs = A0 + sum(p[0] for p in Q)
            assert cs == (1 << i), ('c-mass identity', s, i)
            ls = A1 + sum(p[1] for p in Q)
            assert ls == 3 * s + 1 - (0 if bnd else 1), ('l-mass identity', s)
    assert A0 == (1 << v) and A1 == 3 * s, ('final singleton', A0, A1, s)
    return dict(ell=s, s_cross=s_cross, dec=tuple(dec), final=(A0, A1),
                halted=False, **st)


# ---------------------------------------------------------------------------
# The infinite walk F with crossing-state recording.
# ---------------------------------------------------------------------------

def walk_master(Nmax, check_mass=True):
    """Exact pair walk of the INFINITE run (the formal map F of work_g6 §5.1).
    For every suffix index n <= Nmax, records the CROSSING state: the state
    just before the first step that reads E_n, as a tuple
        (qA, dA, lA, qY, dY, lY, i_ptr, s, nP)
    with c_A = qA * 2^(n-dA) (qA odd), and Y = the single pushed entry in front
    of E_n when present (nP = 1), else None (nP = 0).  Also records the
    level-fire stream (rho, s, j) — same convention as fast_walker.st['lvl']
    entries (rho, s//2, j) with pre-step s.  Returns (crossings, fires, info)."""
    A0 = 1; A1 = 1
    Q = deque()
    i = 0; s = 0
    crossings = {}
    fires = []
    chains = 0
    while True:
        nP = len(Q)
        if nP <= 1:
            idxs = (i, i + 1) if nP == 0 else (i,)
            for n in idxs:
                if n > Nmax:
                    break
                vA = v2i(A0)
                if nP == 1:
                    (cY, lY) = Q[0]
                    vY = v2i(cY)
                    crossings[n] = (A0 >> vA, n - vA, A1, cY >> vY, n - vY, lY,
                                    i, s, 1)
                else:
                    crossings[n] = (A0 >> vA, n - vA, A1, None, None, None,
                                    i, s, 0)
            if max(idxs) > Nmax:
                break
        # ---- one F-step (infinite suffix)
        if nP >= 2:
            b = Q.popleft(); c = Q.popleft()
        elif nP == 1:
            b = Q.popleft(); c = (1 << i, 0); i += 1
        else:
            b = (1 << i, 0); c = (1 << (i + 1), 0); i += 2
        if (A0 + A1) % 2 == 0:
            A0 += b[0] + c[0]
            A1 += b[1] + c[1] + 3
        else:
            assert A0 % 2 == 0, 'S2'
            cx = A0 + 2 * b[0]
            lx = A1 + 2 * b[1] + 3
            assert lx >= 2 and lx % 2 == 0, ('walk sign', s, lx)
            j = v2i(lx)
            assert j < v2i(cx), 'S1'
            cu = cx >> j
            lu = lx >> j
            assert cu >= 2 and cu % 2 == 0 and lu >= 1 and lu % 2 == 1, 'u-form'
            if nP == 0:
                fires.append((i - 2, s, j))            # level fire at rho = old i
            chains += 1
            Q.appendleft((c[0] + (A0 >> 1), c[1] + ((A1 + 1) >> 1)))
            for t in range(j - 2, -1, -1):
                Q.appendleft((cu << t, lu << t))
            A0 = cu; A1 = lu + 1
        s += 1
        if check_mass:
            cs = A0 + sum(p[0] for p in Q)
            assert cs == (1 << i), ('c-mass', i, s)
            ls = A1 + sum(p[1] for p in Q)
            assert ls == 3 * s + 1, ('l-mass', s)
        assert s < 4 * Nmax + 2000, 'runaway walk'
    info = dict(steps=s, chains=chains, final_i=i)
    return crossings, fires, info


# ---------------------------------------------------------------------------
# The endgame runner (concrete per-v and symbolic per-class, one engine).
# c-value representation: (q, d) means q * 2^(n-d) with n = v-1 FIXED during the
# run, q odd > 0; d = deficit (class-constant in the symbolic run, so all
# valuation comparisons are t-independent because every value's v2 = n-d moves
# by the common +2^m per t).  lambda representation: (a, b) means a*t + b.
# ---------------------------------------------------------------------------

def _cadd(x, y):
    """(q1,d1)+(q2,d2), normalized; None is the ZERO c-part.
    c_i = q_i * 2^{n-d_i}: the sum's v2 is n - max(d1,d2) (smaller power of 2
    wins), the term with the LARGER deficit (smaller v2) keeps its q unshifted."""
    if x is None:
        return y
    if y is None:
        return x
    q1, d1 = x; q2, d2 = y
    if d1 == d2:
        q = q1 + q2                       # odd+odd = even -> renormalize
        w = v2i(q)
        return (q >> w, d1 - w)
    if d1 > d2:
        return (q1 + (q2 << (d1 - d2)), d1)
    return (q2 + (q1 << (d2 - d1)), d2)


def endgame_run(v, lamA, lamY, cA, cY, i_ptr, s0, m=0, cap=400):
    """The ENDGAME: pair dynamics from the crossing state at suffix index v-1
    (the walk state just before the first read of E_{v-1}), with the boundary
    substitution, until the singleton.

      lamA, lamY : (a, b) = a*t + b   (concrete per-v check: a = 0);
      cA, cY     : (q, d) = q*2^{(v-1)-d};
      v          : the class representative v0 (t = 0 instance); the caller
                   guarantees v = v0 + 2^m*t for the class members;
      s0         : walk step count at the crossing (concrete int).

    Every decision (parity, j) must be uniform in t; every chain margin-safe,
    c_u even >= 2 and l_u odd >= 1 for ALL t >= 0 (u >= 2U+1 >= 3 at U=1).
    Returns dict(OK=True, e, dec, final_l, stats...) or dict(FAILED=reason...)."""
    n = v - 1
    A_c = cA; A_l = lamA
    Q = deque()
    if lamY is not None:
        Q.append((cY, lamY))
    bnd = True
    i = i_ptr
    e = 0
    dec = []
    st = dict(minlx=None, minlu=None, minu1=None, maxj=0, maxd=cA[1],
              min_margin=None)
    while True:
        if not Q and (not bnd) and i >= v:
            break                                     # singleton
        assert e <= cap, 'endgame cap'
        # ---- read b (never ZERO: the run would have ended)
        if Q:
            (bc, bl) = Q.popleft()
        elif i < v - 1:
            assert i == v - 2, 'unexpected original read'
            bc = (1, 1); bl = (0, 0)                  # E_{v-2} = 2^{v-2}
            i += 1
        else:
            assert bnd, 'read past the end (b)'
            bc = (1, 0); bl = (0, -1)                 # the defect (2^{v-1}, -1)
            bnd = False; i += 1
        # ---- read c
        if Q:
            (cc, cl) = Q.popleft()
        elif i < v - 1:
            assert i == v - 2, 'unexpected original read'
            cc = (1, 1); cl = (0, 0)
            i += 1
        elif bnd:
            cc = (1, 0); cl = (0, -1)
            bnd = False; i += 1
        else:
            cc = None; cl = (0, 0)                    # ZERO (missing entry)
        # ---- one step.  Parity of the VALUE = (c_A + l_A) mod 2 (U odd): the
        # c-part contributes its odd q_A exactly when v2(c_A) = 0, i.e. d == n.
        aA, bA = A_l
        codd = (A_c[1] == n)
        if bc[1] > st['maxd']:
            st['maxd'] = bc[1]
        if A_c[1] > st['maxd']:
            st['maxd'] = A_c[1]
        if (aA + bA + (A_c[0] if codd else 0)) % 2 == 0:
            dec.append(0)
            A_c = _cadd(_cadd(A_c, bc), cc)
            A_l = (aA + bl[0] + cl[0], bA + bl[1] + cl[1] + 3)
        else:
            if aA % 2 != 0:
                return dict(FAILED='parity-split', at=e, v=v)
            if codd and m > 0:
                # c_A odd at t=0 but even for t >= 1 (v2(c_A) = n-d grows):
                # the decision would differ across class members.
                return dict(FAILED='c-odd-split', at=e, v=v, q=A_c[0])
            if A_c[1] > n - 1:
                return dict(FAILED='S2', at=e, v=v, d=A_c[1], n=n)
            cx = _cadd(A_c, (bc[0], bc[1] - 1))       # c_x = c_A + 2 c_b
            ax = aA + 2 * bl[0]
            bx = bA + 2 * bl[1] + 3
            if bx < 2 or ax < 0:
                return dict(FAILED='sign', at=e, v=v, lam=(ax, bx))
            if ax == 0:
                j = v2i(bx)
            else:
                if v2i(bx) >= v2i(ax):
                    return dict(FAILED='j-split', at=e, v=v, lam=(ax, bx))
                j = v2i(bx)
            d_x = cx[1]
            margin = (n - d_x) - j                    # grows by 2^m per t
            if margin <= 0:
                return dict(FAILED='S1', at=e, v=v, n=n, d=d_x, j=j)
            if st['min_margin'] is None or margin < st['min_margin']:
                st['min_margin'] = margin
            cu = (cx[0], d_x + j)                     # v2(c_u) = margin >= 1
            lu = (ax >> j, bx >> j)
            if not (lu[1] >= 1 and lu[1] % 2 == 1 and lu[0] >= 0 and lu[0] % 2 == 0):
                return dict(FAILED='lu-form', at=e, v=v, lu=lu)
            u1 = (cx[0] << (n - d_x - j)) + lu[1]     # u at U=1 (t=0; grows in t)
            u1c = u1 if u1 < (1 << 62) else (1 << 62)  # clamp (only >= 3 matters)
            if st['minu1'] is None or u1c < st['minu1']:
                st['minu1'] = u1c
            if st['minlx'] is None or bx < st['minlx']:
                st['minlx'] = bx
            if st['minlu'] is None or lu[1] < st['minlu']:
                st['minlu'] = lu[1]
            if j > st['maxj']:
                st['maxj'] = j
            if d_x > st['maxd']:
                st['maxd'] = d_x
            assert bA % 2 == 1, 'lambda_A odd at chain'
            D_c = _cadd(cc, (A_c[0], A_c[1] + 1))     # c + c_A/2
            D_l = (cl[0] + (aA >> 1), cl[1] + ((bA + 1) >> 1))
            if D_l[0] < 0 or D_l[1] < 0:
                return dict(FAILED='D-sign', at=e, v=v, D=D_l)
            Q.appendleft((D_c, D_l))
            for t in range(j - 2, -1, -1):
                Q.appendleft(((cu[0], cu[1] - t), (lu[0] << t, lu[1] << t)))
                if cu[1] - t > st['maxd']:
                    st['maxd'] = cu[1] - t
            A_c = cu; A_l = (lu[0], lu[1] + 1)
            dec.append(j)
        e += 1
    if A_c != (1, -1):                                # 2^v = 1*2^{n+1}
        return dict(FAILED='final-c', at=e, v=v, c=A_c)
    if A_l[0] == 0 and A_l[1] != 3 * (s0 + e):
        return dict(FAILED='final-l', at=e, v=v, l=A_l, want=3 * (s0 + e))
    return dict(OK=True, e=e, ell=s0 + e, dec=tuple(dec), final_l=A_l,
                final_c=A_c, **st)


def endgame_from_crossing(v, cross):
    """Concrete per-v endgame from a recorded crossing state
    (qA,dA,lA,qY,dY,lY,i,s,nP) at index v-1."""
    (qA, dA, lA, qY, dY, lY, ip, s, nP) = cross
    return endgame_run(v, (0, lA), (0, lY) if nP == 1 else None,
                       (qA, dA), (qY, dY) if nP == 1 else None,
                       ip, s)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    for v in range(1, 13):
        fin, st_, minu, jseq, halt = concrete_excursion(3, v)
        res = excursion_pairs(v)
        assert not halt and res['dec'] == tuple(jseq), v
        assert fin == 2 ** v * 3 + 3 * st_, v
        print('v=%2d  ell=%2d  e=%2d  dec=%s  final=%s  minu=%s'
              % (v, st_, st_ - res['s_cross'], res['dec'], res['final'], minu))
    cr, fires, info = walk_master(30)
    print('walk_master: steps=%d chains=%d fires=%d crossings=%d'
          % (info['steps'], info['chains'], len(fires), len(cr)))
    print('fires (rho,s,j) first 5:', fires[:5])
    for v in range(1, 13):
        r = endgame_from_crossing(v, cr[v - 1])
        rp = excursion_pairs(v)
        assert r['OK'] and r['dec'] == rp['dec'][rp['s_cross']:] \
            and r['ell'] == rp['ell'], (v, r)
    print('endgame_from_crossing matches excursion_pairs on v=1..12')
