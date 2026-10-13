"""agentB2_verify.py -- exhaustive [Class-B] verification of the EXIT CLASS LEMMA.

V-A  all m in 5..N (default 3000): for every exit of Phi_m
       - D-fire (b = D_h):  j_D == 1+v2(3*Kexit+1);
         x_D == (39/2)P + 9*k_h + 6*Kexit + 8 (exact integer check);
         j_D equals the shape's CONSTANT (10 shapes) or 1+v2(3K+4) ((1,2,1));
         j_D <= m-2   <-- THE LEMMA
       - seam fire (b = the D-fire's pushed seam, j_D >= 5 cases):
         x_seam == (153/4)P + (15/2)k_h + 9*Kexit + 6*K' + 12;
         j_seam == v2(9*Kexit+6*K'+7) when < J-2;  j_seam <= m-2
       - mixed fire (c = D_h): j <= m-2 and the crossing identity
         x_mix == (27/4)P + (9/2)k_h + 6*Kmix + 7 with Kmix = steps/2 (b='R' cases)
V-B  class-generic spot-check: each shape's script re-instantiated with random
       k_h in the class (mod 2^J), random K in the class (mod 2^{j_last}),
       random p: all decisions agree with the script and j_D is the constant
       (or the Prop-3 formula)  -- the forcing is class-wide, not per-orbit.
V-C  the real walk (formal map F, exact big-int) to i = 2*10^5: every spike
       (chain j >= 5, any nesting) whose pushed seam is later read as b has
       j_exit <= j_spike - 2; mixed reads recorded; margins reported.
V-D  size-bound thresholds for the tie shape (conservation 0.4465*rho and
       Prop-4 rho^2 inputs) vs the exhaustive small-m check.
"""
import sys
import time
from fractions import Fraction as Fr
from random import randrange

from agentB2_lib import phi_traced, classify, v2, kappa


def v2i(x):
    return (x & -x).bit_length() - 1


# ---------------------------------------------------------------- V-A -------
def verify_phi(N=3000, verbose=True):
    stats = {'D': 0, 'seam': 0, 'mixed': 0, 'none': 0, 'margin_min': None,
             'seam_margin_min': None, 'mixed_margin_min': None}
    shapes_const = {}          # (gap, jlast, delta) -> constant j_D (or None)
    bad = []
    for m in range(5, N + 1):
        c = classify(m)
        tr = c['tr']['steps']
        P = c['tr']['P']
        kh = c['tr']['kh']
        iD = c['iD']
        if iD is not None:
            stats['D'] += 1
            Kexit = iD // 2
            jD = c['jD']
            assert iD % 2 == 0
            # exact form of x_D
            assert tr[iD][4] == Fr(39, 2) * P + 9 * kh + 6 * Kexit + 8, \
                ('x_D form', m)
            # formula
            assert jD == 1 + v2i(3 * Kexit + 1), ('j_D formula', m, Kexit, jD)
            # per-shape constant
            K = c['K']
            delta = Kexit - K if K is not None else None
            key = (c['gap'], c['jlast'], delta)
            if key in shapes_const and shapes_const[key] is not None:
                assert jD == shapes_const[key], ('shape const', m, key, jD)
            # lemma
            assert jD <= m - 2, ('LEMMA FAILS', m, jD)
            mg = m - jD
            if stats['margin_min'] is None or mg < stats['margin_min'][0]:
                stats['margin_min'] = (mg, m)
            # seam fire
            if c['seamfire'] is not None:
                stats['seam'] += 1
                iS = c['seamfire']
                jS = c['jseam']
                # K' = universal k of the sub-sub cascade + delta' (literal):
                # recover from the numeric form check below
                xs = tr[iS][4]
                ok = False
                for Kp in (1, 2, 3, 4, 5):
                    if xs == Fr(153, 4) * P + Fr(15, 2) * kh + 9 * Kexit + 6 * Kp + 12:
                        ok = True
                        break
                assert ok, ('x_seam form', m)
                assert jS == v2i(9 * Kexit + 6 * Kp + 7) or v2i(9 * Kexit + 6 * Kp + 7) >= m - 2, \
                    ('j_seam formula', m, Kexit, Kp, jS)
                assert jS <= m - 2, ('SEAM LEMMA', m, jS)
                mg = m - jS
                if stats['seam_margin_min'] is None or mg < stats['seam_margin_min'][0]:
                    stats['seam_margin_min'] = (mg, m)
        else:
            # mixed fire with c = D_h, or D_h consumed by an even step
            im = next((i for i, s in enumerate(tr)
                       if s[0] == 'C' and s[2][0] == 'D'), None)
            if im is None:
                stats['none'] += 1
                continue
            stats['mixed'] += 1
            jm = tr[im][3]
            assert jm <= m - 2, ('MIXED LEMMA', m, jm)
            mg = m - jm
            if stats['mixed_margin_min'] is None or mg < stats['mixed_margin_min'][0]:
                stats['mixed_margin_min'] = (mg, m)
            if tr[im][1][0] == 'R':
                # clean crossing at J-2: x_mix = (27/4)P + (9/2)k_h + 6*Kmix + 7
                assert im % 2 == 0, ('mixed parity', m)
                Kmix = im // 2
                assert tr[im][4] == Fr(27, 4) * P + Fr(9, 2) * kh + 6 * Kmix + 7, \
                    ('x_mix form', m, tr[im][1])
    if verbose:
        print('V-A ok: m = 5..%d  D-fires %d (all x_D/j_D forms + j_D <= m-2, '
              'min margin %d at m=%d); seam fires %d (forms + j <= m-2, min margin %d '
              'at m=%d); mixed c=D fires %d (j <= m-2, min margin %d at m=%d); '
              'D_h consumed by even steps %d' %
              (N, stats['D'], stats['margin_min'][0], stats['margin_min'][1],
               stats['seam'], stats['seam_margin_min'][0], stats['seam_margin_min'][1],
               stats['mixed'], stats['mixed_margin_min'][0], stats['mixed_margin_min'][1],
               stats['none']))
    return stats


# ---------------------------------------------------------------- V-B -------
def instantiate(J, tmpl, rho, j_last, kh, K, p, jD_override=None):
    """Concrete replay of a script template (list of (kind, blb, blc, j) with
    labels ('R',offset-from-rho)/'D'/'T2'/'M'/'d' by creation order), starting
    at the crossing at rho.  Returns (x_D, j_D, iD_step) or raises if any
    concrete decision deviates from the template.  jD_override: expected j at
    the D-fire when it is orbit-dependent ((1,2,1): 1+v2(3K+4))."""
    P = 1 << p
    w = (6 * kh + 4) >> J
    assert (6 * kh + 4) >> J != 0 and ((6 * kh + 4) >> J) % 2 == 1
    u = 9 * (P >> J) + w
    Dh = 15 * (P >> 1) + 3 * kh + 1

    def E(a):
        return u << a

    A = E(rho) + 6 * K + 1
    Q = [(E(a), ('R', a - rho)) for a in range(rho, J - 1)] + \
        [(Dh, ('D',))] + [(3 * (P << e), ('T', e)) for e in range(2, 40)]
    nq = 0
    xD = jD = None
    for si, (kind, blb, blc, jrec) in enumerate(tmpl):
        lb, lc = Q[0][1], Q[1][1]
        assert (lb, lc) == (blb, blc), \
            ('template label mismatch at %d: %r vs %r' % (si, (lb, lc), (blb, blc)))
        b, c = Q[0][0], Q[1][0]
        if kind == 'E':
            assert A % 2 == 0, ('template parity', si)
            A = A + b + c + 3
            Q = Q[2:]
            continue
        assert A % 2 == 1, ('template chain parity', si)
        x = A + 2 * b + 3
        j = v2i(x)
        want_j = jrec
        if jD_override is not None and lb == ('D',):
            want_j = jD_override
        assert j == want_j, ('template j at %d: %d vs %d' % (si, j, want_j))
        uu = x >> j
        d = c + (A + 1) // 2
        if lb == ('D',):
            xD, jD = x, j
        Q = [(uu << t, ('M', si)) for t in range(j - 1)] + \
            [(d, ('d', si))] + Q[2:]
        A = uu + 1
        if lb == ('T', 2):
            break
    return xD, jD


def tmpl_from(m):
    c = classify(m)
    tr = c['tr']['steps']
    rho = c['rho']
    if rho is None:
        return None, c
    tmpl = []
    cnt = {}
    for s in tr[c['i_last']:]:
        kind, lb, lc, j = s[0], s[1], s[2], s[3]
        if lb[0] == 'T':
            break

        def norm(l):
            if l[0] == 'R':
                return ('R', l[1] - rho)
            if l[0] in ('M', 'd'):
                return (l[0], l[1] - c['i_last'])   # id = creating fire's step
            return l
        tmpl.append((kind, norm(lb), norm(lc), j))
    return tmpl, c


def verify_class_generic(shape_reps, trials=25):
    from agentB2_symbolic import replay  # noqa: F401  (import check)
    rng = randrange
    checked = 0
    for key, m in sorted(shape_reps.items(), key=lambda kv: kv[1]):
        tmpl, c = tmpl_from(m)
        if tmpl is None:
            continue
        gap, j_last, delta = key
        if j_last is None:
            continue
        jD_const = c['jD'] if key != (1, 2, 1) else None
        if key == (1, 2, 1):
            # the post-D-fire script depends on the realized j_D: check to the
            # D-fire only (Prop 3's conditional formula)
            tmpl = tmpl[:next(i2 for i2, t in enumerate(tmpl) if t[1] == ('D',)) + 1]
        J = m
        for _ in range(trials):
            kh = kappa(J) + (1 << J) * rng(0, 1 << 40)
            # K in class j_last: 3K+2 = 2^{j_last-1} * odd
            v = j_last - 1
            kap = (((1 << v) - 2) * pow(3, -1, 1 << (v + 1))) % (1 << (v + 1))
            K = kap + (1 << (v + 1)) * rng(0, 1 << 30)
            if 1 + v2i(3 * K + 2) != j_last:
                continue
            p = 2 * J + 64 + rng(0, 64)
            if key == (1, 2, 1) and 1 + v2i(3 * K + 4) >= J - 1:
                continue      # Prop 3 validity condition: v2 < J-1
            ov = 1 + v2i(3 * K + 4) if key == (1, 2, 1) else None
            xD, jD = instantiate(J, tmpl, J - 2 - gap, j_last, kh, K, p,
                                 jD_override=ov)
            Kexit = None
            # Kexit from the identity: x_D = (39/2)P + 9kh + 6Kexit + 8
            from fractions import Fraction as Fr
            P = 1 << p
            Kexit = (xD - Fr(39, 2) * P - 9 * kh - 8) / 6
            assert Kexit.denominator == 1
            Kexit = int(Kexit)
            assert Kexit == K + delta, ('Kexit', key, K, Kexit)
            assert jD == 1 + v2i(3 * Kexit + 1)
            if jD_const is not None:
                assert jD == jD_const, ('class-generic j_D', key, K, kh, jD, jD_const)
            checked += 1
    print('V-B ok: %d class-generic instantiations (random k_h in class J, K in '
          'class j_last, random p): all decisions follow the script; j_D = shape '
          'constant (or Prop-3 formula for (1,2,1)); Kexit = K+delta' % checked)
    return checked


# ---------------------------------------------------------------- V-C -------
def walk_spikes(N=200000):
    """Exact big-int walk of the formal map F; every chain with j>=5 registers
    its seam; the exit fire reading that seam as b is checked: j <= J-2."""
    A = (1, 1)
    P = []
    i = 0
    s = 0
    spike_seams = {}          # seam step s -> J of the producer (j>=5)
    events = {'spikes': 0, 'Dfire': 0, 'seamfire': 0, 'mixedD': 0, 'evenD': 0}
    margins = []
    smargins = []
    mmargins = []
    lvl = []
    while i <= N:
        ents = [(p[0], p[1], p[2]) for p in P[:2]]
        a = i
        while len(ents) < 2:
            ents.append((1 << a, 0, ('E', a)))
            a += 1
        (cb, lb, tb), (cc, lc, tc) = ents
        if (A[0] + A[1]) % 2 == 0:
            for tg in (tb, tc):
                if tg in spike_seams:
                    events['evenD'] += 1
                    del spike_seams[tg]
            A = (A[0] + cb + cc, A[1] + lb + lc + 3)
            newp = []
        else:
            cx = A[0] + 2 * cb
            lx = A[1] + 2 * lb + 3
            vc, vl = v2i(cx), v2i(lx)
            assert vl < vc and A[0] % 2 == 0 and A[1] % 2 == 1, (i, s)
            j = vl
            if tb[0] == 'E':
                lvl.append((tb[1], s // 2, j))
            # exit accounting
            if tb in spike_seams:
                J = spike_seams.pop(tb)
                events['Dfire'] += 1
                assert j <= J - 2, ('WALK D-FIRE LEMMA', i, s, J, j)
                margins.append((J, j, J - j))
                if tc in spike_seams:
                    pass
            if tc in spike_seams:
                J = spike_seams.pop(tc)
                events['mixedD'] += 1
                assert j <= J - 2, ('WALK MIXED LEMMA', i, s, J, j)
                mmargins.append((J, j))
            u = (cx >> j, lx >> j)
            newp = [(u[0] << t, u[1] << t, ('M', s)) for t in range(j - 1)] + \
                   [(cc + A[0] // 2, lc + (A[1] + 1) // 2, ('D', s))]
            if j >= 5:
                events['spikes'] += 1
                spike_seams[('D', s)] = j
            A = (u[0], u[1] + 1)
        k = len(P)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k
            P = []
        P = newp + P
        s += 1
    # a fire on the seam pushed by an exit D-fire (the 'd' seam of the task)
    # is itself registered above when its j >= 5; for j < 5 it cannot violate
    # j <= J-2 unless J < 7; collect those too by re-walking with all seams:
    return events, margins, mmargins, lvl


def walk_all_seams(N=200000):
    """Variant registering EVERY chain's seam (any j), checking the exit fire
    j <= j_producer - 2 whenever the producer was a spike (j>=5)."""
    A = (1, 1)
    P = []
    i = 0
    s = 0
    seams = {}
    out = []
    lvl = []
    while i <= N:
        ents = [(p[0], p[1], p[2]) for p in P[:2]]
        a = i
        while len(ents) < 2:
            ents.append((1 << a, 0, ('E', a)))
            a += 1
        (cb, lb, tb), (cc, lc, tc) = ents
        if (A[0] + A[1]) % 2 == 0:
            for tg in (tb, tc):
                if tg in seams:
                    del seams[tg]
            A = (A[0] + cb + cc, A[1] + lb + lc + 3)
            newp = []
        else:
            cx = A[0] + 2 * cb
            lx = A[1] + 2 * lb + 3
            j = v2i(lx)
            if tb[0] == 'E':
                lvl.append((tb[1], s // 2, j))
            if tb in seams:
                J = seams.pop(tb)
                if J >= 5:
                    out.append(('b', J, j))
            if tc in seams:
                J = seams.pop(tc)
                if J >= 5:
                    out.append(('c', J, j))
            u = (cx >> j, lx >> j)
            newp = [(u[0] << t, u[1] << t, ('M', s)) for t in range(j - 1)] + \
                   [(cc + A[0] // 2, lc + (A[1] + 1) // 2, ('D', s))]
            seams[('D', s)] = j
            A = (u[0], u[1] + 1)
        k = len(P)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k
            P = []
        P = newp + P
        s += 1
    return out, lvl


# ---------------------------------------------------------------- V-D -------
def thresholds():
    import math
    def f1(J):    # conservation input k_rho <= 0.4465 * rho, rho = J-3
        return math.log2(3 * 0.4465 * (J - 3) + 4) - (J - 3)
    def f2(J):    # Prop 4 input k_rho <= rho^2
        return math.log2(3 * (J - 3) ** 2 + 4) - (J - 3)
    J0a = next(J for J in range(7, 200) if all(f1(x) <= 0 for x in range(J, 200)))
    J0b = next(J for J in range(7, 400) if all(f2(x) <= 0 for x in range(J, 400)))
    # monotonicity check
    assert all(f1(J + 1) < f1(J) for J in range(8, 300)), 'f1 not decreasing'
    assert all(f2(J + 1) < f2(J) for J in range(12, 400)), 'f2 not decreasing'
    print('V-D ok: tie-shape bound v2(3K+4) <= log2(3*k(J-3)+4) <= J-3 for J >= %d '
          '(conservation 0.4465*rho) / J >= %d (Prop 4 rho^2); smaller J covered '
          'exhaustively by V-A' % (J0a, J0b))
    return J0a, J0b


if __name__ == '__main__':
    t0 = time.time()
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    stats = verify_phi(N)
    from agentB2_symbolic import all_shape_reps
    reps = all_shape_reps(N)
    verify_class_generic(reps)
    J0a, J0b = thresholds()
    t1 = time.time()
    print('walk (i <= 2*10^5)...', file=sys.stderr)
    events, margins, mmargins, lvl = walk_spikes(200000)
    print('V-C ok (walk to i=2*10^5): %d spikes (j>=5); exit fires on the seam '
          'as b: %d, ALL with j <= J-2 (min margin %d, (J,j)=%r); seam-as-c reads '
          '%d (all j <= J-2); seam consumed by even steps %d; %d level fires' %
          (events['spikes'], events['Dfire'],
           min(m[2] for m in margins), min(margins, key=lambda t: t[2]),
           events['mixedD'], events['evenD'], len(lvl)))
    # J values seen at spike exits in the walk:
    seen = sorted(set(m[0] for m in margins))
    print('    exit J values in the walk:', seen[:20], '... total %d' % len(seen))
    print('total %.0fs' % (time.time() - t0))
