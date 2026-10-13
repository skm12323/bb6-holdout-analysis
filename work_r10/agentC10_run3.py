"""work_r10/agentC10_run3.py — TASKS 3/4/5: class-symbolic endgame verification.

Measured facts feeding in (run2):
  * the endgame decision sequence is NOT a function of v mod 2^m for any
    m <= 16 (minimal m on [1,4096] is the trivial 12; on [1,65536] the
    trivial 16) — the walk's crossing data is quasi-injective in v, with
    log-periodic (not periodic) structure;
  * max chain parameter over all endgames v <= 65536 is maxj = 17.

Class machinery that DOES close: with the global modulus K = maxj + 1 = 18,
    class(v) = (nP, ip_off, l_A mod 2^K, l_Y mod 2^K)   at the crossing v-1
is (by measurement) injective on v <= 65536, and per class the SYMBOLIC
endgame run in the pair calculus with
    l_A = 2^K*t + r_A,   l_Y = 2^K*t + r_Y    (t >= 0 arbitrary)
proves: every decision is uniform in t (all j = v2(l_x) < K = v2(slope)),
every chain margin-safe for all t >= 0, c_u even >= 2 and l_u odd >= 1 for
all t — hence u >= 2U+1 >= 3 for every odd U: NO HALT on the whole cylinder
2^K*N + r, and termination at the singleton with the same step count e.

Also measured/verified here:
  * e <= maxj + 1 on all real endgames (and in all robustness samples):
    with maxj <= log2(9s+6) (mass identity) this bounds e(v) for all v
    given the walk's growth bound (M2');
  * coarser structure at K=15 (42574 classes, 22962 with 2 members, 4
    deep-tie splits) — reported as the near-injectivity finding;
  * robustness on ARBITRARY legal crossings (mass identities enforced):
    exhaustive small-lambda, random large-lambda, adversarial deep ties.
"""
import json
import random
import sys
import time
from collections import defaultdict

sys.path.insert(0, r'D:\math_cc\work_r10')
import agentC10_lib as L


def main():
    cross = {int(k): v for k, v in json.load(open('agentC10_cross.json')).items()}
    o2 = json.load(open('agentC10_out2.json'))
    decs = {int(v): (d[2], tuple(d[3])) for v, d in o2.items()}
    VMAX = max(decs)
    maxj_all = max(j for v in decs for j in decs[v][1])
    K = maxj_all + 1
    print('loaded %d endgames (v <= %d); maxj = %d -> global K = %d'
          % (len(decs), VMAX, maxj_all, K))

    # e <= maxj + 1 on all real endgames
    bad_e = [v for v in decs if o2[str(v)][1] > o2[str(v)][4][0] + 1]
    print('[e-bound] e(v) <= maxj(v)+1 violations on real data: %d' % len(bad_e))

    # ---------- coarser K0 view (near-injectivity finding) ----------
    K0 = 15
    keys0 = defaultdict(list)
    for v in range(1, VMAX + 1):
        c = cross[v - 1]
        keys0[(c[8], c[6] - (v - 1), c[2] % (1 << K0),
               (c[5] % (1 << K0)) if c[8] else None)].append(v)
    nonuni0 = [k for k, vs in keys0.items()
               if len(set(decs[v] for v in vs)) > 1]
    print('[coarse] K0=%d: %d classes, %d with >1 member (max %d), '
          '%d non-uniform (deep ties j >= %d)'
          % (K0, len(keys0), sum(1 for vs in keys0.values() if len(vs) > 1),
             max(len(vs) for vs in keys0.values()), len(nonuni0), K0))

    # ---------- global-K classes + per-class symbolic verification ----------
    t0 = time.time()
    classes = defaultdict(list)
    for v in range(1, VMAX + 1):
        c = cross[v - 1]
        classes[(c[8], c[6] - (v - 1), c[2] % (1 << K),
                 (c[5] % (1 << K)) if c[8] else None)].append(v)
    collisions = sum(1 for vs in classes.values() if len(vs) > 1)
    print('[class] K=%d: %d classes, %d with >1 member (measured injectivity)'
          % (K, len(classes), collisions))
    fails = []
    okr = []
    emax = margmin = 99
    u1min = (1 << 62)
    for k, vs in classes.items():
        (nP, ipoff, rA, rY) = k
        v0 = min(vs)
        c = cross[v0 - 1]
        qA, dA = c[0], c[1]
        qY, dY = (c[3], c[4]) if nP else (None, None)
        r = L.endgame_run(v0, (1 << K, rA), (1 << K, rY) if nP else None,
                          (qA, dA), (qY, dY) if nP else None,
                          v0 - 1 + ipoff, c[7], m=K)
        if not r.get('OK'):
            fails.append((k, r))
            continue
        if any(r['dec'] != decs[v][1] for v in vs):
            fails.append((k, 'dec mismatch'))
            continue
        okr.append(r)
        emax = min(emax, r['e'])      # placeholder (min over classes below)
    es = [r['e'] for r in okr]
    print('[symbolic] %d/%d classes closed on their full 2^K-cylinder '
          '(t >= 0 arbitrary): %d failures  [%.0fs]'
          % (len(okr), len(classes), len(fails), time.time() - t0))
    for f in fails[:8]:
        print('   FAIL:', str(f)[:200])
    okrs = okr
    print('[symbolic] per-class e in [%d, %d]; max chain j = %d; '
          'min margin (at t=0; grows +1 per 2^K of scale) = %s; min u@U=1 = %d'
          % (min(es), max(es), max(r['maxj'] for r in okrs),
             min(r['min_margin'] for r in okrs if r['min_margin'] is not None),
             min(r['minu1'] for r in okrs if r['minu1'] is not None)))
    bad = sum(1 for k, vs in classes.items() for v in vs
              if o2[str(v)][1] != o2[str(v)][4][0] + 1
              and False)  # (e<=maxj+1 already checked globally)

    # ---------- robustness: arbitrary LEGAL crossings ----------
    # legal = mass identities at the crossing: c_A (+ c_Y) = 2^n,
    # l_A (+ l_Y) = 3 s0 + 1 with all l >= 0; nP=1 forces pointer v-1.
    rng = random.Random(20261013)

    def mk_cross(la, ly, nP, ipoff, v, dY, qY):
        ssum = la + (ly if nP else 0) - 1
        if ssum < 0 or ssum % 3:
            return None
        s0 = ssum // 3
        n = v - 1
        if nP:
            if ipoff != 0:
                return None        # nP=1 crossings always sit at pointer v-1
            if not (1 <= dY <= 20 and 1 <= qY < (1 << dY) and qY % 2 == 1):
                return None
            cy = qY << (n - dY)                    # c_Y = qY*2^{n-dY} < 2^n
            cA = (1 << n) - cy
            va = L.v2i(cA)
            return L.endgame_run(v, (0, la), (0, ly),
                                 (cA >> va, n - va), (qY, dY),
                                 v - 1 + ipoff, s0, m=0)
        # nP=0: pointer v-1 (ipoff 0) has c_A = 2^{v-1}; pointer v-2
        # (ipoff -1) has c_A = 2^{v-2} = the mass identity at that pointer
        cA_def = 0 if ipoff == 0 else 1
        return L.endgame_run(v, (0, la), None, (1, cA_def), None,
                             v - 1 + ipoff, s0, m=0)

    # (a) exhaustive small lambdas
    t0 = time.time()
    cnt = ok = 0
    fails_a = defaultdict(int)
    emax = 0
    gap = -99
    for la in range(1, 900):
        for nP in (0, 1):
            lys = range(0, 60) if nP else [0]
            for ly in lys:
                for ipoff in ((0,) if nP else (0, -1)):
                    for (dY, qY) in (((2, 3), (3, 5), (5, 9)) if nP
                                     else ((0, 0),)):
                        r = mk_cross(la, ly, nP, ipoff, 101, dY, qY)
                        if r is None:
                            continue
                        cnt += 1
                        if r.get('OK'):
                            ok += 1
                            emax = max(emax, r['e'])
                            gap = max(gap, r['e'] - r['maxj'])
                        else:
                            fails_a[r['FAILED']] += 1
    print('[robust-a] exhaustive small-lambda legal crossings: %d, %d OK '
          '(%.2f%%), max e = %d, max(e-maxj) = %d, failures %s  [%.0fs]'
          % (cnt, ok, 100.0 * ok / max(cnt, 1), emax, gap, dict(fails_a),
             time.time() - t0))

    # (a-wide) widened exhaustive sweep: l_A < 2048, l_Y < 256, 5 shapes
    t0 = time.time()
    cnt = ok = 0
    emax = 0
    gap = -99
    fails_aw = defaultdict(int)
    for la in range(1, 2048):
        for nP in (0, 1):
            for ly in (range(256) if nP else [0]):
                for ipoff in ((0,) if nP else (0, -1)):
                    for (dY, qY) in (((1, 1), (2, 3), (3, 5), (5, 9), (8, 17))
                                     if nP else ((0, 0),)):
                        r = mk_cross(la, ly, nP, ipoff, 101, dY, qY)
                        if r is None:
                            continue
                        cnt += 1
                        if r.get('OK'):
                            ok += 1
                            emax = max(emax, r['e'])
                            gap = max(gap, r['e'] - r['maxj'])
                        else:
                            fails_aw[r['FAILED']] += 1
    print('[robust-a-wide] widened exhaustive (l_A<2048, l_Y<256): %d legal, '
          '%d OK (%.4f%%), max e = %d, max(e-maxj) = %d, failures %s  [%.0fs]'
          % (cnt, ok, 100.0 * ok / cnt, emax, gap, dict(fails_aw),
             time.time() - t0))

    # (b) random large lambdas
    cnt = ok = 0
    fails_b = defaultdict(int)
    emax = 0
    gap = -99
    margmin = 99
    for _ in range(200000):
        v = rng.randrange(80, 4000)
        nP = rng.randrange(2)
        la = rng.randrange(1, 10 ** 7)
        ly = rng.randrange(0, 10 ** 7) if nP else 0
        if (la + ly - 1) % 3:
            la += 3 - (la + ly - 1) % 3
        dY = rng.randrange(1, 21)
        qY = 2 * rng.randrange(0, 1 << (dY - 1)) + 1
        r = mk_cross(la, ly, nP, 0 if nP else -rng.randrange(2), v, dY, qY)
        if r is None:
            continue
        cnt += 1
        if r.get('OK'):
            ok += 1
            emax = max(emax, r['e'])
            gap = max(gap, r['e'] - r['maxj'])
            if r['min_margin'] is not None:
                margmin = min(margmin, r['min_margin'])
        else:
            fails_b[r['FAILED']] += 1
    print('[robust-b] 200k random legal crossings (l < 10^7, dY <= 20): '
          '%d OK (%.3f%%), max e = %d, max(e-maxj) = %d, min margin = %d, '
          'failures %s' % (ok, 100.0 * ok / cnt, emax, gap, margmin,
                           dict(fails_b)))

    # (c) adversarial deep ties at the first chain: l_A + 2*l_b + 3 = 2^J*odd
    cnt = ok = 0
    fails_c = defaultdict(int)
    emax = 0
    gap = -99
    for J in range(3, 30):
        for _ in range(400):
            odd = 2 * rng.randrange(1, 2000) + 1
            la = (1 << J) * odd - 3
            if la < 1:
                continue
            la += (-((la - 1) % 3)) % 3
            for ipoff in (0, -1):
                r = mk_cross(la, 0, 0, ipoff, rng.randrange(max(200, J * 8),
                                                            4000), 0, 0)
                if r is None:
                    continue
                cnt += 1
                if r.get('OK'):
                    ok += 1
                    emax = max(emax, r['e'])
                    gap = max(gap, r['e'] - r['maxj'])
                else:
                    fails_c[r['FAILED']] += 1
    print('[robust-c] adversarial deep ties (l_A+3 = 2^J*odd, J < 30): %d '
          'tries, %d OK, max e = %d, max(e-maxj) = %d, failures %s'
          % (cnt, ok, emax, gap, dict(fails_c)))
    json.dump(dict(K=K, n_classes=len(classes), failures=[str(f)[:300]
                                                          for f in fails]),
              open('agentC10_out3.json', 'w'), indent=1)
    print('wrote agentC10_out3.json')


if __name__ == '__main__':
    main()
