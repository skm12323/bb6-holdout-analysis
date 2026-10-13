# -*- coding: utf-8 -*-
"""revC10_t4b_push.py -- extra stress: walk to 10^6, e(v) profile, spike growth.
Records per v: e, endgame maxj; reports max e, argmax, biggest endgame j, and the
joint profile (e vs maxj) for the largest-e cases. Saves revC10_t4b.json."""
import json

import revC10_lib as L


def main():
    NMAX = 1000000
    cadd = L.mk_cadd(64)
    Ac, Al = (0, 1), 1
    P = []
    i = 0
    s = 0
    maxj_run = 0
    maxdef = 0
    ev = {}
    walk_seq_j = {}
    while i <= NMAX:
        snapA = (Ac[0], Ac[1], Al)
        snapP = [(p[0][0], p[0][1], p[1]) for p in P]
        snapi = i
        if len(P) >= 2:
            reads = []
        elif len(P) == 1:
            reads = [i]
        else:
            reads = [i, i + 1]
        minv = min([L.cv2(Ac)] + [L.cv2(p[0]) for p in P])
        Delta = i - minv
        if Delta > maxdef:
            maxdef = Delta
        for idx in reads:
            vb = idx + 1
            if vb > NMAX + 2:
                continue
            r = L._endgame_from_snapshot(snapA, snapP, snapi, vb, 64)
            ev[vb] = (r.get('e'), r['res'], r['maxj'], r['nfires'], r['max_drain'])
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
            assert j < vcx, ('margin', i, s)
            cu = (cx[0] - j, cx[1])
            lu = lx >> j
            cD = cadd(cc, L.chalf(Ac))
            lD = cl + (Al + 1) // 2
            if j >= 15:
                walk_seq_j.setdefault(j, []).append(i)
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
    bad = [v for v in ev if ev[v][1] != 'singleton']
    maxe = max(ev[v][0] for v in ev if ev[v][0] is not None)
    arg = [v for v in sorted(ev) if ev[v][0] == maxe]
    maxjend = max(ev[v][2] for v in ev)
    argj = [v for v in sorted(ev) if ev[v][2] == maxjend][:6]
    print('walk to i=%d: s=%d maxdef=%d maxj_run=%d' % (i, s, maxdef, maxj_run))
    print('v<= %d: non-singleton=%d ; max e=%d at v=%s ; max endgame j=%d at v=%s'
          % (NMAX + 1, len(bad), maxe, arg[:8], maxjend, argj))
    es = {}
    for v in ev:
        es[ev[v][0]] = es.get(ev[v][0], 0) + 1
    print('e histogram (top):', dict(sorted(es.items(), reverse=True)[:8]))
    print('big walk fires (j -> first few i):',
          {j: walk_seq_j[j][:4] for j in sorted(walk_seq_j, reverse=True)})
    json.dump(dict(maxe=maxe, arg=arg[:20], maxjend=maxjend, argj=argj,
                   ehist={str(k): vv for k, vv in es.items()}, bad=bad[:10],
                   walk=dict(final=(i, s), maxdef=maxdef, maxj=maxj_run),
                   bigfires={str(j): vv[:10] for j, vv in walk_seq_j.items()}),
              open('revC10_t4b.json', 'w'))
    print('saved revC10_t4b.json')


if __name__ == '__main__':
    main()
