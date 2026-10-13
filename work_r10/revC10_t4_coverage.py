# -*- coding: utf-8 -*-
"""revC10_t4_coverage.py -- TASK 4: coverage for all v.

Walk the (v-independent) universal walk far past the Task-2 range:
  * stage 1: i <= 2^17+5000 = 131608 ;
  * stage 2: push to 3*10^5 .
At every first-read event n (= crossing for v=n+2, boundary for v=n+1):
  * crossing class C(v) = (i mod 2^18, d, lamA mod 2^18, lamfront mod 2^18, h=n-i);
  * boundary endgame run: e(v), result, margins (for Task 5);
  * decision sequence from the crossing, kept for v <= WRAPLO and v > 2^18
    (wrap-around test pairs (v, v+2^18) sharing a 2^18-class).
Checks:
  (a) e(v) and no-halt/singletons for all v seen;
  (b) class set S(n<=65534) [v<=65536 sweep] vs classes arising later: new ones?
  (c) eventual periodicity of the class stream;
  (d) non-vacuous 2^18 wrap test: same class => same decseq, for real pairs;
  (e) symbolic closure of any class not seen by the 65536 sweep.
Saves revC10_t4.json.
"""
import json
import sys
from collections import defaultdict

import revC10_lib as L

MOD = 1 << 18
WRAPLO = 37856            # v <= WRAPLO can pair with v + 2^18 <= 3e5


def walk_collect(Nmax, decseq_from, decseq_to, wrap_base):
    cadd = L.mk_cadd(64)
    Ac, Al = (0, 1), 1
    P = []
    i = 0
    s = 0
    maxj_run = 0
    maxdef = 0
    maxdef_at = None
    per_v = {}
    classes = {}
    seqs = {}
    deep = 0
    maxchaindef = 0
    maxchaindef_at = None
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
        minv = L.cv2(Ac)
        for p in P:
            pv = L.cv2(p[0])
            if pv < minv:
                minv = pv
        Delta = i - minv
        if Delta > maxdef:
            maxdef = Delta
            maxdef_at = (i, s)
        for idx in reads:
            vb = idx + 1
            r = L._endgame_from_snapshot(snapA, snapP, snapi, vb, 64)
            per_v[vb] = dict(e=r.get('e'), res=r['res'], nfires=r['nfires'], maxj=r['maxj'],
                             min_margin=r['min_margin'], max_drain=r['max_drain'],
                             Delta=Delta, walk_maxj=maxj_run, i_snap=snapi,
                             d_snap=len(snapP), bad=r['bad'])
            vc = idx + 2
            cls = (snapi % MOD, len(snapP), Al % MOD, (snapP[0][2] if snapP else 0) % MOD,
                   (vc - 1) - snapi)
            classes.setdefault(vc, cls)
            if decseq_from <= vc <= decseq_to:
                rc = L._endgame_from_snapshot(snapA, snapP, snapi, vc, 64)
                seqs[vc] = tuple(rc['seq'])
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
        par = (L.cparity(Ac) + Al) % 2
        if par == 0:
            Ac = cadd(cadd(Ac, bc), cc)
            Al = Al + bl + cl + 3
            newp = []
        else:
            cx = cadd(Ac, (bc[0] + 1, bc[1]))
            lx = Al + 2 * bl + 3
            j = L.v2(lx)
            vcx = L.cv2(cx)
            if not (j < vcx):
                return None, dict(fail=('WALK-MARGIN', i, s, j, vcx))
            cu = (cx[0] - j, cx[1])
            lu = lx >> j
            cD = cadd(cc, L.chalf(Ac))
            lD = cl + (Al + 1) // 2
            if i - vcx > maxchaindef:
                maxchaindef = i - vcx
                maxchaindef_at = (i, s, j)
            newp = [[(cu[0] + t, cu[1]), lu << t] for t in range(j - 1)] + [[cD, lD]]
            Ac, Al = cu, lu + 1
            maxj_run = max(maxj_run, j)
        k = len(P)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k
            P = []
        P = newp + P
        s += 1
    return dict(per_v=per_v, classes=classes, seqs=seqs,
                maxchaindef=maxchaindef, maxchaindef_at=maxchaindef_at,
                walk=dict(final=(i, s), maxdef=maxdef, maxdef_at=maxdef_at, maxj=maxj_run)), None


def main():
    N1 = (1 << 17) + 5000
    N2 = 300000
    print('stage 1: walk to i=%d ...' % N1)
    res1, err = walk_collect(N1, 1, WRAPLO, MOD)
    if err:
        print('WALK FAILED:', err)
        return
    per_v, classes, seqs = res1['per_v'], res1['classes'], res1['seqs']
    print('  walk: final=%s maxdef=%d(at %s) maxj=%d chaindef=%d(at %s) ; events=%d' %
          (res1['walk']['final'], res1['walk']['maxdef'], res1['walk']['maxdef_at'],
           res1['walk']['maxj'], res1['maxchaindef'], res1['maxchaindef_at'], len(classes)))
    es = [r['e'] for r in per_v.values() if r['e'] is not None]
    badres = [v for v, r in per_v.items() if r['res'] != 'singleton']
    print('  v<= %d: %d endgames, non-singleton: %d %s ; max e=%d (v=%s)' %
          (N1 + 1, len(per_v), len(badres), badres[:3], max(es),
           max(per_v, key=lambda v: per_v[v]['e'] or 0)))
    S64 = set(classes[v] for v in classes if v <= 65536)
    S1 = set(classes[v] for v in classes)
    new1 = S1 - S64
    print('  classes: |S(v<=65536)|=%d |S(all %d)|=%d NEW-after-65536=%d' %
          (len(S64), len(classes), len(S1), len(new1)))
    # periodicity probe on the class stream restricted to its (i mod 2^18) etc:
    # check whether class(v) for v>65536 ever repeats earlier classes with period dividing T
    reps_new = {}
    for v in sorted(classes):
        if v > 65536 and classes[v] in new1:
            reps_new.setdefault(classes[v], v)
    print('  first v of each new class:', sorted(reps_new.values())[:20])

    print('stage 2: push to i=%d ...' % N2)
    res2, err = walk_collect(N2, 1, 0, MOD)   # no decseqs needed in stage 2 pre-pass
    if err:
        print('WALK FAILED:', err)
        return
    per_v2, classes2 = res2['per_v'], res2['classes']
    S2 = set(classes2.values())
    new2 = S2 - S64
    es2 = [r['e'] for r in per_v2.values() if r['e'] is not None]
    bad2 = [v for v, r in per_v2.items() if r['res'] != 'singleton']
    print('  walk: final=%s maxdef=%d(at %s) maxj=%d chaindef=%d(at %s)' %
          (res2['walk']['final'], res2['walk']['maxdef'], res2['walk']['maxdef_at'],
           res2['walk']['maxj'], res2['maxchaindef'], res2['maxchaindef_at']))
    print('  v<= %d: %d endgames, non-singleton: %d %s ; max e=%d (v=%s)' %
          (N2 + 1, len(per_v2), len(bad2), bad2[:3], max(es2),
           max(per_v2, key=lambda v: per_v2[v]['e'] or 0)))
    print('  classes: |S(all)|=%d ; new-after-65536=%d ; new-after-%d=%d' %
          (len(S2), len(new2), N1, len(S2 - S1)))
    firstv = {}
    for v in sorted(classes2):
        firstv.setdefault(classes2[v], v)
    new_first = sorted(v for c, v in firstv.items() if c in new2)
    print('  new classes first appear at v:', new_first[:30])

    # symbolic closure of every class NOT seen by the 65536 sweep
    print('symbolically closing new classes (dAssume=16,30) ...')
    clos = {}
    nbad = 0
    for c in sorted(new2):
        v0 = firstv[c]
        i18, dd, rA, rY, h = c
        # recover exact i for the representative: i = (v0-1) - h
        iex = (v0 - 1) - h
        assert iex % MOD == i18
        r = L.symbolic_endgame((iex, dd, rA, rY, v0), dAssume=16)
        r30 = L.symbolic_endgame((iex, dd, rA, rY, v0), dAssume=30)
        okc = (r['res'] == 'singleton' and not r['fails'] and
               r30['res'] == 'singleton' and not r30['fails'] and v0 >= 34)
        clos[str(c)] = dict(rep=v0, res=r['res'], fails=r['fails'], fails30=r30['fails'],
                            seq=r['seq'], ok=okc)
        if not okc:
            nbad += 1
    print('  closed %d new classes; failures: %d' % (len(clos), nbad))

    # wrap-around 2^18 test: pairs (v, v+2^18), both walked, same class?
    print('wrap-around test (v, v+2^18) with 2^18-classes ...')
    npairs = 0
    nagree = 0
    mism = []
    # need classes + seqs for v > 2^18 as well: rerun lean pass for seqs only
    res3, err = walk_collect(N2, MOD + 3, N2 + 2, MOD)
    seqs3, classes3 = res3['seqs'], res3['classes']
    for v in range(1, WRAPLO + 1):
        w = v + MOD
        if w in classes3 and v in classes:
            npairs += 1
            if classes3[w] == classes[v]:
                if w in seqs3 and v in seqs:
                    if seqs3[w] == seqs[v]:
                        nagree += 1
                    else:
                        mism.append((v, w))
                # if seqs missing (out of stored range) note as class-only pair
    nsameclass = sum(1 for v in range(1, WRAPLO + 1)
                     if (v + MOD) in classes3 and v in classes and classes3[v + MOD] == classes[v])
    print('  candidate pairs=%d ; same-class pairs=%d ; seq-compared agree=%d ; mismatches=%d %s'
          % (npairs, nsameclass, nagree, len(mism), mism[:5]))

    # periodicity probe: class stream segment vs shifted
    per = None
    stream = [classes2[v] for v in sorted(classes2)]
    for T in (2, 4, 6, 8, 12, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072):
        n = len(stream)
        ok = all(stream[k] == stream[k - T] for k in range(max(T, n - 5000), n))
        if ok:
            per = T
            break
    print('eventual periodicity (tail 5000, T in tested set):', per)

    out = dict(stage1=dict(walk=res1['walk'], chaindef=res1['maxchaindef'], maxe=max(es), nbadres=len(badres),
                           nclasses=len(S1), new_after_65536=len(new1)),
               stage2=dict(walk=res2['walk'], chaindef=res2['maxchaindef'], maxe=max(es2), nbadres=len(bad2),
                           nclasses=len(S2), new_after_65536=len(new2),
                           new_first_v=new_first[:50]),
               closure=clos, closure_fail=nbad,
               wrap=dict(npairs=npairs, nsameclass=nsameclass, nagree=nagree, mism=mism[:20]),
               periodicity=per)
    json.dump(out, open('revC10_t4.json', 'w'))
    print('saved revC10_t4.json')


if __name__ == '__main__':
    main()
