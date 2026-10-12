"""finaladv_4_verifier.py — ANGLES 5/6: per-J verifier stress + soundness scans.

(1) EXTENSION: run agentB_run7.verify(j) at large j (well beyond the report's
    1200 and probe3's 20000): totality, and dk>=1 / dp>=2 (the termination
    linchpin: pointer strictly advances => excursions end).
(2) VANISHING-MEMBER SCAN of agentB_abs.v2_val: when V.c != 0 and vh > vb the
    code returns vb for ALL class members k = kappa + 2^m s — but if the k-part
    vanishes at a nonneg integer s0 (base + head*s0 == 0, i.e. member
    k* = kappa + 2^m s0), the true v2 for THAT member is the P-side valuation,
    not vb.  Collect all such k* over j = 1..JMAX and intersect with the
    on-sequence k set (from the independent U=1 walk, k <= ~9000).
(3) P-SENSITIVITY: v2_val returns min(vsmall, ctx.p + fv2(V.a)).  A return on
    the P-side (vsmall > vP) would be ctx.p-dependent => not transferable to
    true host positions; count them, and record per-j the required minimum
    true p (max vsmall - fv2(V.a)) for transfer.
(4) j=14 spot check at the ell-anomaly boundary v=6132..6135, 6500.
"""
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
import agentB_abs
import agentB_run7
import finaladv_0_core as C
import finaladv_1_levels as F1
from collections import deque


def v2f(x):
    return (x & -x).bit_length() - 1


def fast_run(w, v):
    A = 3 * w + 1
    q = deque(((3 * w) << a for a in range(v - 1)))
    q.append(((3 * w) << (v - 1)) - 1)
    steps = 0
    jset = set()
    while q:
        steps += 1
        b = q[0]
        c = q[1] if len(q) > 1 else 0
        if (A & 1) == 0:
            A = A + b + c + 3
            q.popleft()
            if q:
                q.popleft()
            continue
        x = A + 2 * b + 3
        j = v2f(x)
        u = x >> j
        assert u > 1
        D = c + (A + 1) // 2
        q.popleft()
        if q:
            q.popleft()
        q.appendleft(D)
        for t in range(j - 2, -1, -1):
            q.appendleft(u << t)
        A = u + 1
        jset.add(j)
    return steps, jset


def spy_install():
    calls = {'n': 0, 'vanish': [], 'pside': 0, 'reqp': {}}

    orig = agentB_abs.v2_val

    def spy(V, ctx):
        calls['n'] += 1
        head = V.c * (1 << ctx.m)
        base = V.c * ctx.kappa + V.d
        want = None
        if V.c != 0 and head.denominator == 1 and base.denominator == 1:
            vh = agentB_abs.fv2(head)
            vb = agentB_abs.fv2(base)
            if vh > vb and base != 0:
                # generic return vb; vanishing member?
                if head != 0 and (base % head == 0):
                    s0 = -(base // head)
                    if s0 >= 0:
                        kstar = ctx.kappa + (1 << ctx.m) * s0
                        calls['vanish'].append((int(kstar), int(ctx.kappa),
                                                ctx.m))
            want = 'small'
        r = orig(V, ctx)
        if V.a != 0 and V.c == 0:
            vsmall = agentB_abs.fv2(base) if base != 0 else None
        elif V.a != 0:
            vsmall = None
        # p-side / required-p bookkeeping only for successful min(vsmall,vP):
        try:
            head2 = V.c * (1 << ctx.m)
            base2 = V.c * ctx.kappa + V.d
            if V.c == 0:
                vs = agentB_abs.fv2(base2)
            else:
                vh2, vb2 = agentB_abs.fv2(head2), agentB_abs.fv2(base2)
                vs = vb2 if vh2 > vb2 else None
            if vs is not None and V.a != 0:
                vP = ctx.p + agentB_abs.fv2(V.a)
                if vs > vP:
                    calls['pside'] += 1
                else:
                    need = vs - agentB_abs.fv2(V.a)
                    jj = calls.get('_curj', 0)
                    if need > calls['reqp'].get(jj, -10 ** 9):
                        calls['reqp'][jj] = need
        except Exception:
            pass
        return r
    agentB_abs.v2_val = spy
    return calls, orig


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if mode in ('all', 'spot'):
        part4(t0)
    if mode in ('all', 'ext'):
        part1(t0)
    part23(t0)
    print('elapsed %.1fs' % (time.time() - t0))


def part4(t0):
    print('=== (4) j=14 boundary spot check ===')
    for v in (6132, 6133, 6134, 6135, 6500):
        ell, js = fast_run(1, v)
        print('  E(1,%d): ell=%d, j-set max=%d' % (v, ell, max(js)))


def part1(t0):
    print('=== (1) verifier extension to large j ===')
    for j in (28, 60, 200, 500, 1200, 5000, 20000, 30000, 50000):
        if time.time() - t0 > 430:
            print('  (global time guard before j=%d)' % j)
            break
        t1 = time.time()
        try:
            res, err = agentB_run7.verify(j)
        except Exception as ex:
            print('  j=%-7d EXCEPTION %r' % (j, ex))
            continue
        dt = time.time() - t1
        if err:
            print('  j=%-7d ERR %s (%.1fs)' % (j, err, dt))
        else:
            (dk, dp), nleaf = res
            print('  j=%-7d OK dk=%d dp=%d leaves=%d (%.1fs) %s'
                  % (j, dk, dp, nleaf, dt,
                     'dp>=2,dk>=1 OK' if (dp >= 2 and dk >= 1)
                     else '*** TERMINATION LINCHPIN FAIL ***'))
        sys.stdout.flush()


def part23(t0):
    print('=== (2)+(3) vanishing-member + p-sensitivity scan, j=1..JMAX ===')
    calls, orig = spy_install()
    JMAX = 0
    try:
        for j in range(1, 400):
            calls['_curj'] = j
            agentB_run7.verify(j)
            if j % 100 == 0:
                print('  scanned j<=%d (%.0fs), vanish-members=%d, '
                      'p-side returns=%d' % (j, time.time() - t0,
                                             len(calls['vanish']),
                                             calls['pside']))
                sys.stdout.flush()
            if time.time() - t0 > 500:
                JMAX = j
                break
        else:
            JMAX = 399
    finally:
        agentB_abs.v2_val = orig
    print('  scanned j=1..%d; v2_val calls=%d' % (JMAX, calls['n']))
    print('  P-SIDE (ctx.p-dependent) v2 returns: %d' % calls['pside'])
    reqp = calls['reqp']
    if reqp:
        mx = max(reqp.items(), key=lambda t: t[1])
        print('  required min true p per j (max over calls): worst j=%d '
              'needs p > %d' % mx)
        small = {j: r for j, r in reqp.items() if r <= 60}
        print('  j<=60 required-p entries (<=60): %s'
              % (dict(sorted(small.items())[:20]),))
    van = calls['vanish']
    print('  vanishing class members found: %d %s'
          % (len(van), van[:8] if van else ''))
    if van:
        kpos, jpos, _, _ = F1.build_kpos()
        onseq = set(kpos.values())
        hits = [v for v in van if v[0] in onseq]
        print('  on-sequence k hit by a vanishing member: %s'
              % (hits if hits else 'NONE (independent kpos up to k=%d)'
                 % max(onseq)))


if __name__ == '__main__':
    main()
