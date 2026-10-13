# -*- coding: utf-8 -*-
"""revC10_lib.py -- BLIND AUDITOR C10, own re-implementation from scratch.

Context: work_r1/RULES.md (audited top map), work_g6/PROOF_G6.md sect.5 (formal map F).

Objects:
  * micro R-rule runner (R1..R5 + HALT) on configs (h; r1..rk)  -- ground truth;
  * closed-form composite top map on E(w,v) = (U+1; U,2U,...,2^{v-2}U, 2^{v-1}U-1), U=3w odd;
  * pair map F with BOUNDARY: A=(c,lam); queue of pairs; originals E_a=(2^a,0),
    boundary defect B=(2^{v-1},-1) at index v-1, nothing after; absent c-slot = (0,0);
  * fast universal walk (c = (v2, odd residue mod 2^mask)) with first-read events;
  * per-v endgame runs launched from event snapshots;
  * symbolic closure over the 2^18-cylinder of a crossing class (free tA,tY >= 0).

Stdlib only.
"""
from collections import deque


def v2(x):
    return (x & -x).bit_length() - 1


class Deep(Exception):
    pass


def mk_cadd(mask):
    """c = 2^val * res, res odd (val=0,res=0 means exact 0).
    mask=None -> exact big int; mask=K -> residue mod 2^K (val still exact)."""
    if mask:
        M = (1 << mask) - 1

        def cadd(c1, c2):
            v1, r1 = c1
            v2_, r2 = c2
            if v1 == 0 and r1 == 0:
                return c2
            if v2_ == 0 and r2 == 0:
                return c1
            if v1 == v2_:
                s = r1 + r2            # even
                t = v2(s)
                if t >= mask - 12:
                    raise Deep('tie depth %d at val=%d' % (t, v1))
                return (v1 + t, (s >> t) & M)
            if v2_ < v1:
                if v1 - v2_ >= mask:
                    return (v2_, r2)
                return (v2_, (r2 + (r1 << (v1 - v2_))) & M)
            if v1 - v2_ >= mask:
                return (v1, r1)
            return (v1, (r1 + (r2 << (v2_ - v1))) & M)
    else:

        def cadd(c1, c2):
            v1, r1 = c1
            v2_, r2 = c2
            if v1 == 0 and r1 == 0:
                return c2
            if v2_ == 0 and r2 == 0:
                return c1
            if v1 == v2_:
                s = r1 + r2
                t = v2(s)
                return (v1 + t, s >> t)
            if v2_ < v1:
                return (v2_, r2 + (r1 << (v1 - v2_)))
            return (v1, r1 + (r2 << (v2_ - v1)))
    return cadd


def chalf(c):
    v, r = c
    if v == 0 and r == 0:
        return c
    assert v >= 1
    return (v - 1, r)


def cparity(c):
    v, r = c
    if v >= 1:
        return 0
    return r & 1            # exact 0 -> 0; odd residue (v=0) -> 1


def cv2(c):
    v, r = c
    if v == 0 and r == 0:
        return 1 << 30      # "infinity" for margin comparisons
    return v


# ----------------------------------------------------------------------------
# ground truth: micro R-rules (RULES.md sect.3) -- only usable for tiny v
# ----------------------------------------------------------------------------

def micro_excursion(U, v, maxmicro=2 * 10**7):
    """R1..R5+HALT from (0; U+1, U, 2U, ..., 2^{v-2}U, 2^{v-1}U-1), micro level.
    Returns (result, composite_configs, final, nmicro)."""
    r = deque([U + 1] + [(U << a) for a in range(v - 1)] + [(U << (v - 1)) - 1])
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    h = 0
    comps = [list(r)]
    micro = 0
    did_r5 = False
    while True:
        if h == 0 and len(r) == 1 and not did_r5:
            return ('singleton', comps, r[0], micro)
        if micro > maxmicro:
            return ('CAP', comps, None, micro)
        r1 = r[0]
        k = len(r)
        assert r[-1] >= 1
        if r1 <= 1:
            assert k >= 3 and r[1] == 0, ('invariant', h, list(r))
        if r1 >= 2:
            if k >= 2 and r[1] >= 1:                      # R1
                h += 1
                r[1] -= 1
                if k == 2 and r[1] == 0:
                    r.pop()
            elif k == 1:                                  # R2
                h += 1
                r[0] -= 2
                r.append(0)
                r.append(1)
            else:                                         # R3
                assert k >= 3 and r[1] == 0
                h += 1
                r[0] -= 2
                r[2] += 1
        elif r1 == 1:
            if h >= 1:                                    # R4
                y = r[2]                                  # y = y_pattern + 1
                r[0] = h - 1
                r.insert(2, 1)
                r[3] = y + 1                              # y_pattern + 2
                h = 0
            else:
                return ('HALT', comps, None, micro)
        else:                                             # R5
            assert k >= 3 and r[1] == 0
            y1 = r[2]
            r.popleft()
            r.popleft()
            r.popleft()
            r.appendleft(h + y1 + 3)
            h = 0
            did_r5 = True
        micro += 1
        if did_r5:
            did_r5 = False
            while len(r) > 1 and r[-1] == 0:
                r.pop()
            comps.append(list(r))
            if len(r) == 1:
                return ('singleton', comps, r[0], micro)


# ----------------------------------------------------------------------------
# closed-form composite top map (RULES.md sect.5) on the excursion
# ----------------------------------------------------------------------------

def topmap_excursion(U, v, maxcomp=200000):
    r = [U + 1] + [(U << a) for a in range(v - 1)] + [(U << (v - 1)) - 1]
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    configs = [list(r)]
    n = 0
    while True:
        if len(r) == 1:
            return ('singleton', configs, r[0])
        if n > maxcomp:
            return ('CAP', configs, None)
        A = r[0]
        b = r[1] if len(r) >= 2 else 0
        c = r[2] if len(r) >= 3 else 0
        if A % 2 == 0:
            r = [A + b + c + 3] + r[3:]
        else:
            x = A + 2 * b + 3
            j = v2(x)
            u = x >> j
            if u == 1:
                return ('HALT', configs, None)
            D = c + (A + 1) // 2
            r = [u + 1] + [u << t for t in range(j - 1)] + [D] + r[3:]
        n += 1
        configs.append(list(r))


# ----------------------------------------------------------------------------
# pair map F with boundary -- exact excursion runner (own implementation)
# ----------------------------------------------------------------------------

def run_excursion_pairs(v, U=None, mask=None, cap=1000000):
    """Excursion E(v) under the pair map: A=(1,1); queue E_a=(2^a,0) for a<=v-2,
    B=(2^{v-1},-1), nothing after. If U is given (mask must be None) also records
    the readout lists [cA*U+lA, c*U+l, ...] at every composite boundary."""
    cadd = mk_cadd(mask)
    Ac, Al = (0, 1), 1
    ents = [[(a, 1), 0, 'O'] for a in range(v - 1)] + [[(v - 1, 1), -1, 'B']]
    seq = []
    first_b = None
    s = 0
    min_margin = None
    max_drain = 0
    maxj = 0
    nf = 0
    bad = []
    readouts = None
    if U is not None:
        def rd():
            out = [((1 << Ac[0]) * Ac[1]) * U + Al]
            for e in ents:
                out.append(((1 << e[0][0]) * e[0][1]) * U + e[1])
            return out
        readouts = [rd()]
    while ents:
        if s > cap:
            return dict(res='CAP', seq=seq, first_b=first_b, s=s, bad=bad + ['CAP'])
        if len(ents) >= 2:
            bc, bl, bt = ents[0]
            cc, cl, ct = ents[1]
            del ents[:2]
        else:
            bc, bl, bt = ents[0]
            cc, cl, ct = (0, 0), 0, '-'
            del ents[:]
        if first_b is None and (bt == 'B' or ct == 'B'):
            first_b = s
        par = (cparity(Ac) + Al) % 2
        if par == 0:
            Ac = cadd(cadd(Ac, bc), cc)
            Al = Al + bl + cl + 3
            seq.append(-1)
        else:
            cx = cadd(Ac, (bc[0] + 1, bc[1]))
            lx = Al + 2 * bl + 3
            j = v2(lx)
            vcx = cv2(cx)
            if not (j < vcx):
                bad.append(('MARGIN', s, j, vcx))
                return dict(res='MARGIN', seq=seq, first_b=first_b, s=s, bad=bad)
            if cparity(Ac) != 0:
                bad.append(('S2', s))
                return dict(res='S2', seq=seq, first_b=first_b, s=s, bad=bad)
            cu = (cx[0] - j, cx[1])
            lu = lx >> j
            if cu[0] < 1 or lu < 1 or (lu & 1) != 1 or (cu == (0, 1) and lu == 1):
                bad.append(('UFORM/HALT', s, cu, lu))
                return dict(res='UFORM', seq=seq, first_b=first_b, s=s, bad=bad)
            nf += 1
            maxj = max(maxj, j)
            marg = vcx - j
            if min_margin is None or marg < min_margin:
                min_margin = marg
            dr = (v - 1) - vcx
            if dr > max_drain:
                max_drain = dr
            cD = cadd(cc, chalf(Ac))
            lD = cl + (Al + 1) // 2
            new = [[(cu[0] + t, cu[1]), lu << t, 'M'] for t in range(j - 1)] + [[cD, lD, 'D']]
            Ac, Al = cu, lu + 1
            ents[0:0] = new
            seq.append(j)
        s += 1
        if U is not None:
            readouts.append(rd())
    e = s - first_b if first_b is not None else None
    return dict(res='singleton', seq=seq, first_b=first_b, e=e, ell=s, s=s,
                lam_single=Al, min_margin=min_margin, max_drain=max_drain,
                nfires=nf, maxj=maxj, bad=bad, readouts=readouts)


# ----------------------------------------------------------------------------
# fast universal walk with first-read events
# ----------------------------------------------------------------------------

def _endgame_from_snapshot(snapA, snapP, snapi, v, mask):
    """Excursion for parameter v started at snapshot state (pointer snapi):
    queue = snapshot-P + originals E_a (snapi <= a <= v-2) + B=(2^{v-1},-1)."""
    cadd = mk_cadd(mask)
    Ac = (snapA[0], snapA[1])
    Al = snapA[2]
    ents = [[(p[0], p[1]), p[2], 'P'] for p in snapP]
    ents += [[(a, 1), 0, 'O'] for a in range(snapi, v - 1)]
    ents += [[(v - 1, 1), -1, 'B']]
    seq = []
    first_b = None
    s = 0
    min_margin = None
    max_drain = 0
    maxj = 0
    nf = 0
    bad = []
    while ents:
        if s > 200:
            return dict(res='CAP', seq=seq, first_b=first_b, ell=None, bad=bad + ['CAP'])
        if len(ents) >= 2:
            bc, bl, bt = ents[0]
            cc, cl, ct = ents[1]
            del ents[:2]
        else:
            bc, bl, bt = ents[0]
            cc, cl, ct = (0, 0), 0, '-'
            del ents[:]
        if first_b is None and (bt == 'B' or ct == 'B'):
            first_b = s
        par = (cparity(Ac) + Al) % 2
        if par == 0:
            Ac = cadd(cadd(Ac, bc), cc)
            Al = Al + bl + cl + 3
            seq.append(-1)
        else:
            cx = cadd(Ac, (bc[0] + 1, bc[1]))
            lx = Al + 2 * bl + 3
            j = v2(lx)
            vcx = cv2(cx)
            if not (j < vcx):
                bad.append(('MARGIN', s, j, vcx))
                return dict(res='MARGIN', seq=seq, first_b=first_b, ell=s, bad=bad)
            cu = (cx[0] - j, cx[1])
            lu = lx >> j
            if cu[0] < 1 or lu < 1 or (lu & 1) != 1 or (cu == (0, 1) and lu == 1):
                bad.append(('UFORM/HALT', s, cu, lu))
                return dict(res='UFORM', seq=seq, first_b=first_b, ell=s, bad=bad)
            nf += 1
            maxj = max(maxj, j)
            marg = vcx - j
            if min_margin is None or marg < min_margin:
                min_margin = marg
            dr = (v - 1) - vcx
            if dr > max_drain:
                max_drain = dr
            cD = cadd(cc, chalf(Ac))
            lD = cl + (Al + 1) // 2
            new = [[(cu[0] + t, cu[1]), lu << t, 'M'] for t in range(j - 1)] + [[cD, lD, 'D']]
            Ac, Al = cu, lu + 1
            ents[0:0] = new
            seq.append(j)
        s += 1
    e = s - first_b if first_b is not None else None
    return dict(res='singleton', seq=seq, first_b=first_b, e=e, ell=s,
                min_margin=min_margin, max_drain=max_drain, nfires=nf, maxj=maxj,
                lam_single=Al, bad=bad)


def universal_walk(Nmax, endgame_limit=None, decseq_limit=None, mask=64):
    """Walk F (infinite originals) until pointer i > Nmax.  At each step, every
    original index idx read now (first read) fires:
       v=idx+1: boundary endgame from the pre-step snapshot (into per_v);
       v=idx+2: crossing class + decision sequence (into cross_v).
    Returns (walk_stats, per_v, cross_v, walk_seq)."""
    cadd = mk_cadd(mask)
    Ac, Al = (0, 1), 1
    P = []
    i = 0
    s = 0
    maxj_run = 0
    maxdef = 0
    maxdef_at = None
    per_v = {}
    cross_v = {}
    walk_seq = []
    if endgame_limit is None:
        endgame_limit = Nmax + 10
    if decseq_limit is None:
        decseq_limit = Nmax + 10
    while i <= Nmax:
        snapA = (Ac[0], Ac[1], Al)
        snapP = [(p[0][0], p[0][1], p[1]) for p in P]
        snapi = i
        if len(P) >= 2:
            reads = []
        elif len(P) == 1:
            reads = [i]
        else:
            reads = [i, i + 1]
        minv = cv2(Ac)
        for p in P:
            pv = cv2(p[0])
            if pv < minv:
                minv = pv
        Delta = i - minv
        if Delta > maxdef:
            maxdef = Delta
            maxdef_at = (i, s)
        for idx in reads:
            vb = idx + 1
            if vb <= endgame_limit:
                r = _endgame_from_snapshot(snapA, snapP, snapi, vb, mask)
                r['Delta_at_boundary'] = Delta
                r['i_snap'] = snapi
                r['d_snap'] = len(snapP)
                r['walk_maxj'] = maxj_run
                per_v[vb] = r
            vc = idx + 2
            if vc <= decseq_limit:
                r2 = _endgame_from_snapshot(snapA, snapP, snapi, vc, mask)
                cls = (snapi, len(snapP), Al, snapP[0][2] if snapP else 0)
                cross_v[vc] = dict(cls=cls, seq=r2['seq'], res=r2['res'],
                                   e=r2.get('e'), ell=r2['ell'], first_b=r2['first_b'])
        # ---- one universal step ----
        if len(P) >= 2:
            bc, bl = P[0][0], P[0][1]
            cc, cl = P[1][0], P[1][1]
        elif len(P) == 1:
            bc, bl = P[0][0], P[0][1]
            cc, cl = (i, 1), 0
        else:
            bc, bl = (i, 1), 0
            cc, cl = (i + 1, 1), 0
        par = (cparity(Ac) + Al) % 2
        if par == 0:
            Ac = cadd(cadd(Ac, bc), cc)
            Al = Al + bl + cl + 3
            newp = []
            walk_seq.append(-1)
        else:
            cx = cadd(Ac, (bc[0] + 1, bc[1]))
            lx = Al + 2 * bl + 3
            j = v2(lx)
            vcx = cv2(cx)
            if not (j < vcx):
                return dict(fail=('WALK-MARGIN', i, s, j, vcx)), per_v, cross_v, walk_seq
            cu = (cx[0] - j, cx[1])
            lu = lx >> j
            cD = cadd(cc, chalf(Ac))
            lD = cl + (Al + 1) // 2
            newp = [[(cu[0] + t, cu[1]), lu << t] for t in range(j - 1)] + [[cD, lD]]
            Ac, Al = cu, lu + 1
            maxj_run = max(maxj_run, j)
            walk_seq.append(j)
        k = len(P)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k
            P = []
        P = newp + P
        s += 1
    st = dict(final=(i, s), maxdef=maxdef, maxdef_at=maxdef_at, maxj=maxj_run)
    return st, per_v, cross_v, walk_seq


# ----------------------------------------------------------------------------
# symbolic closure over the 2^18 cylinder (free tA, tY >= 0)
# ----------------------------------------------------------------------------

class SL(object):
    """value = r + 2^m * (cA*tA + cY*tY + cK), 0 <= r < 2^m."""
    __slots__ = ('r', 'm', 'cA', 'cY', 'cK')

    def __init__(self, r, m, cA=0, cY=0, cK=0):
        self.r = r
        self.m = m
        self.cA = cA
        self.cY = cY
        self.cK = cK


BIG = 64          # constants carried exactly


def _sl_align(x, m):
    d = x.m - m
    if d == 0:
        return x.r, x.cA, x.cY, x.cK
    return (x.r & ((1 << m) - 1), x.cA << d, x.cY << d, (x.r >> m) + (x.cK << d))


def sl_add(x, y):
    m = min(x.m, y.m)
    rx, ax, yx, kx = _sl_align(x, m)
    ry, ay, yy, ky = _sl_align(y, m)
    r = rx + ry
    carry = 0
    if r >= (1 << m):
        r -= 1 << m
        carry = 1
    return SL(r, m, ax + ay, yx + yy, kx + ky + carry)


def sl_const(k):
    assert 0 <= k < (1 << BIG)
    return SL(k, BIG)


def sl_half_inc(x):
    """(x+1)/2, requires x odd uniformly."""
    if x.m >= 1:
        assert x.r & 1
        return SL((x.r + 1) >> 1, x.m - 1, x.cA, x.cY, x.cK)
    # m == 0: value = cK + cA tA + cY tY, must be odd for all t
    assert x.r == 0
    if not ((x.cK & 1) == 1 and x.cA % 2 == 0 and x.cY % 2 == 0):
        raise ValueError('half_inc non-uniform')
    return SL(0, 0, x.cA // 2, x.cY // 2, (x.cK + 1) // 2)


def sl_div2j(x, j):
    if x.r > 0:
        assert j < x.m and (x.r >> j) & 1
        return SL(x.r >> j, x.m - j, x.cA, x.cY, x.cK)
    # r==0: value = 2^m*(cK + cA tA + cY tY), j = m + w, w = v2(cK) < g (uniform)
    w = j - x.m
    assert w >= 0 and x.cK != 0 and w == _v2int(x.cK)
    g = min(_v2int(x.cA), _v2int(x.cY))
    assert w < g
    m2 = min(g - w, 30)
    assert m2 >= 1
    cK1 = x.cK >> w                 # cK >= 0 in practice
    if x.cK < 0:
        cK1 = -((-x.cK) >> w)
    sh = w + m2
    r2 = cK1 % (1 << m2)
    cK2 = (cK1 - r2) >> m2
    cA2 = (x.cA >> sh) if x.cA >= 0 else -((-x.cA) >> sh)
    cY2 = (x.cY >> sh) if x.cY >= 0 else -((-x.cY) >> sh)
    return SL(r2, m2, cA2, cY2, cK2)


def sl_mul2t(x, t):
    """value * 2^t (t >= 0)."""
    if t == 0:
        return SL(x.r, x.m, x.cA, x.cY, x.cK)
    r2 = x.r << t
    return SL(r2 & ((1 << x.m) - 1), x.m, x.cA << t, x.cY << t,
              (r2 >> x.m) + (x.cK << t))


def sl_parity(x):
    """uniform parity of the value over all tA,tY>=0; None if non-uniform."""
    if x.m >= 1:
        return x.r & 1
    # m == 0: value = cK + cA tA + cY tY; uniform iff both free coeffs even
    if x.cA % 2 == 0 and x.cY % 2 == 0:
        return x.cK & 1
    return None


def _v2int(k):
    if k == 0:
        return 1 << 30      # "infinity"
    return v2(abs(k))


def sl_v2(x):
    """v2 of the value, uniform over all tA,tY>=0:
    r>0  -> v2(r) (< m, always uniform);
    r==0 -> value = 2^m*(cK + cA tA + cY tY): with g = min v2 of nonzero free
            coefficients, uniform iff v2(cK) < g, then j = m + v2(cK);
            (cK==0 with g=inf would mean the value is identically 0: None)."""
    if x.r > 0:
        return v2(x.r)
    g = min(_v2int(x.cA), _v2int(x.cY))
    w = _v2int(x.cK)
    if x.cK == 0 and g >= (1 << 30):
        return None                     # identically zero
    if w < g:
        return x.m + w
    return None


def sl_free(x):
    return (x.cA != 0) or (x.cY != 0)


def symbolic_endgame(cls_v, dAssume=16, cap=200):
    """Symbolic endgame from a crossing class.
    cls_v = (i, d, rA, rY, vref): concrete crossing snapshot had pointer i, stack
    depth d in {0,1}, lamA = rA + 2^18 tA, (if d=1) lamY = rY + 2^18 tY, free
    tA,tY >= 0; queue = P + originals E_i..E_{vref-2} + B at index vref-1.
    dAssume: assumed deficit (vref-1 - v2(c)) for the unknown c-parts of A and Y.
    Returns dict(res, seq, e, ell, fails, maxdrain, min_m, nmin_needed)."""
    i, d, rA, rY, vref = cls_v
    n = vref - 1
    fails = []
    nmin_needed = 0
    lamA = SL(rA, 18, cA=1)
    dA = (n - i) if d == 0 else dAssume
    slots = []
    if d == 1:
        slots.append([dAssume, SL(rY, 18, cY=1), 'P'])
    for a in range(i, vref - 1):
        slots.append([n - a, SL(0, BIG), 'O'])
    slots.append([0, SL((1 << BIG) - 1, BIG, cK=-1), 'B'])   # lam = -1 exactly
    seq = []
    s = 0
    first_b = None
    maxdrain = 0
    min_m = 18
    Ac = (dA, lamA)
    while slots:
        if s > cap:
            return dict(res='CAP', seq=seq, e=None, ell=None,
                        fails=fails + ['CAP'], maxdrain=maxdrain, min_m=min_m,
                        nmin_needed=nmin_needed)
        if len(slots) >= 2:
            db, lb, tb = slots[0]
            dc, lc, tc = slots[1]
            del slots[:2]
        else:
            db, lb, tb = slots[0]
            dc, lc, tc = 0, SL(0, BIG), '-'
            del slots[:]
        if first_b is None and (tb == 'B' or tc == 'B'):
            first_b = s
        par = sl_parity(Ac[1])
        if par is None:
            fails.append(('LPARITY', s, Ac[1].m))
            return dict(res='NONUNIFORM', seq=seq, e=None, ell=None, fails=fails,
                        maxdrain=maxdrain, min_m=min_m, nmin_needed=nmin_needed)
        if Ac[0] >= n and s >= 0:
            # c_A parity not forced even -> parity decision non-uniform
            fails.append(('CPARITY', s, Ac[0], n))
        if par == 0:
            dA = max(Ac[0], db, dc)
            lam = sl_add(sl_add(Ac[1], lb), lc)
            lam = sl_add(lam, sl_const(3))
            Ac = (dA, lam)
            seq.append(-1)
        else:
            lx = sl_add(sl_add(Ac[1], sl_add(lb, lb)), sl_const(3))
            j = sl_v2(lx)
            if j is None:
                fails.append(('NONUNIFORM', s, lx.m, lx.r, lx.cA, lx.cY, lx.cK))
                return dict(res='NONUNIFORM', seq=seq, e=None, ell=None, fails=fails,
                            maxdrain=maxdrain, min_m=min_m, nmin_needed=nmin_needed)
            dx = max(Ac[0], db - 1)
            if n - dx < j + 1:
                fails.append(('MARGIN', s, j, n - dx))
            nmin_needed = max(nmin_needed, dx + j + 1)
            cu_d = dx + j
            lu = sl_div2j(lx, j)
            dD = max(dc, Ac[0] + 1)
            try:
                lD = sl_add(lc, sl_half_inc(Ac[1]))
            except ValueError:
                fails.append(('HALFINC', s))
                return dict(res='NONUNIFORM', seq=seq, e=None, ell=None, fails=fails,
                            maxdrain=maxdrain, min_m=min_m, nmin_needed=nmin_needed)
            new = [[cu_d - t, sl_mul2t(lu, t), 'M'] for t in range(0, j - 1)] + [[dD, lD, 'D']]
            Ac = (cu_d, sl_add(lu, sl_const(1)))
            slots[0:0] = new
            seq.append(j)
            maxdrain = max(maxdrain, dx, cu_d)
        if Ac[1].m < min_m:
            min_m = Ac[1].m
        for sl_ in slots:
            if sl_[1].m < min_m:
                min_m = sl_[1].m
        s += 1
    e = s - first_b if first_b is not None else None
    return dict(res='singleton', seq=seq, e=e, ell=s, fails=fails,
                maxdrain=maxdrain, min_m=min_m, nmin_needed=nmin_needed)
