# -*- coding: utf-8 -*-
"""revC10_t2_law.py -- TASK 2: crossing-state law, v = 1..8192.

For each v: crossing state = walk state just before the first step that reads
original index v-2 (v>=2; for v=1 the initial state). Class (mod M):
   (i mod M, stack depth d, lam_A mod M, lam_front mod M).
Law: equal class => equal endgame decision sequence (steps from the crossing,
i.e. kinds/j's up to the singleton).  Also record boundary endgame stats
(e(v), margins, deficits) for Tasks 3/5.  Scan M for the minimal working modulus.
Saves revC10_t2.json (compact).
"""
import json
import sys

import revC10_lib as L

VMAX = 8192


def main():
    st, per_v, cross_v, wseq = L.universal_walk(VMAX + 2, endgame_limit=VMAX,
                                                decseq_limit=VMAX)
    if 'fail' in st:
        print('WALK FAILED:', st['fail'])
        return
    print('walk to i=%d s=%d maxdef=%d(at %s) maxj=%d' % (st['final'][0], st['final'][1],
                                                           st['maxdef'], st['maxdef_at'],
                                                           st['maxj']))
    # v=1: crossing = initial state (i=0, d=0, lamA=1, front=0); decseq = excursion
    ex1 = L.run_excursion_pairs(1)
    cross_all = {1: dict(cls=(0, 0, 1, 0), seq=ex1['seq'], ell=ex1['ell'],
                         e=ex1['e'], first_b=ex1['first_b'], res=ex1['res'])}
    bad = []
    for v in range(2, VMAX + 1):
        cv = cross_v.get(v)
        if cv is None:
            bad.append(('missing-cross', v))
            continue
        cross_all[v] = cv
        if cv['res'] != 'singleton':
            bad.append(('cross-res', v, cv['res']))
        pv = per_v.get(v)
        if pv is None:
            bad.append(('missing-boundary', v))
        elif pv['res'] != 'singleton':
            bad.append(('boundary-res', v, pv['res'], pv['bad']))
    print('excursions v=1..%d: %d bad %s' % (VMAX, len(bad), bad[:5]))

    es = [cross_all[v]['e'] if cross_all[v]['e'] is not None else -1 for v in cross_all]
    ells = [cross_all[v]['ell'] for v in cross_all]
    print('e(v): max=%d at v=%s ; ell: max=%d' % (max(es), max(cross_all, key=lambda v: cross_all[v]['e'] or 0), max(ells)))

    # ---- the law at various moduli ----
    results = {}
    Ms = sorted(set(list(range(2, 65)) + [2**k for k in range(1, 19)]))
    for M in Ms:
        groups = {}
        clash = []
        for v, cv in cross_all.items():
            i, d, rA, rF = cv['cls']
            key = (i % M, d, rA % M, rF % M)
            if key in groups:
                v0 = groups[key]
                if cross_all[v0]['seq'] != cv['seq']:
                    clash.append((v0, v, key))
                    if len(clash) >= 3:
                        break
            else:
                groups[key] = v
        results[M] = dict(ok=not clash, nclasses=len(groups), clash=clash[:3])
    minM = None
    for M in Ms:
        if results[M]['ok']:
            minM = M
            break
    print('law (equal class => equal crossing-decseq):')
    for M in (2, 4, 8, 16, 32, 64, 256, 1024, 4096, 8192, 2**18):
        if M in results:
            print('   M=%-6d ok=%-5s classes=%d %s' % (M, results[M]['ok'], results[M]['nclasses'],
                                                       results[M]['clash'][:1]))
    print('minimal working modulus (tested set):', minM)

    out = dict(VMAX=VMAX, walk=st, bad=bad,
               e_max=max(es), e_argmax=max(cross_all, key=lambda v: cross_all[v]['e'] or 0),
               law={str(M): results[M] for M in Ms}, minM=minM,
               per_v={str(v): dict(e=per_v[v]['e'], ell=per_v[v]['ell'], first_b=per_v[v]['first_b'],
                                   nfires=per_v[v]['nfires'], maxj=per_v[v]['maxj'],
                                   min_margin=per_v[v]['min_margin'], max_drain=per_v[v]['max_drain'],
                                   Delta=per_v[v]['Delta_at_boundary'], i_snap=per_v[v]['i_snap'],
                                   d_snap=per_v[v]['d_snap'], walk_maxj=per_v[v]['walk_maxj'])
                      for v in sorted(per_v)},
               cross={str(v): dict(cls=cross_all[v]['cls'], seq=cross_all[v]['seq'],
                                   e=cross_all[v]['e'], ell=cross_all[v]['ell'])
                      for v in sorted(cross_all)})
    with open('revC10_t2.json', 'w') as f:
        json.dump(out, f)
    print('saved revC10_t2.json')


if __name__ == '__main__':
    main()
