# -*- coding: utf-8 -*-
"""revC10_t1_validate.py -- TASK 1: own boundary walker vs concrete top-map excursion.

1) micro R-rules (audited, RULES.md sect.3) vs closed-form top map, v<=15, U in {3,9,15};
2) closed-form top map vs pair map with boundary, v=1..500, U=3:
   step-by-step list equality, no halt, singleton = 2^v*U + 3*ell(v);
   margin-safety + u-form at every chain;
3) spots w=3 (U=9), w=5 (U=15): same comparison, v=1..250 plus selected larger v.
Saves revC10_t1.json.
"""
import json
import sys

import revC10_lib as L


def compare(U, vlist, tag):
    ok = True
    detail = {}
    eprof = {}
    for v in vlist:
        tm = L.topmap_excursion(U, v)
        pr = L.run_excursion_pairs(v, U=U)
        if tm[0] != 'singleton':
            ok = False
            detail[v] = dict(problem='topmap %s' % tm[0])
            continue
        if pr['res'] != 'singleton':
            ok = False
            detail[v] = dict(problem='pair %s' % pr['res'], bad=pr['bad'])
            continue
        if pr['readouts'] != tm[1]:
            ok = False
            for a, b in zip(pr['readouts'], tm[1]):
                if a != b:
                    detail[v] = dict(problem='list mismatch at step', pair=a, closed=b)
                    break
            else:
                detail[v] = dict(problem='length mismatch', n_pair=len(pr['readouts']),
                                 n_closed=len(tm[1]))
            continue
        ell = len(tm[1]) - 1
        single = tm[1][-1][0]
        if single != (1 << v) * U + 3 * ell:
            ok = False
            detail[v] = dict(problem='singleton formula', single=single,
                             expect=(1 << v) * U + 3 * ell)
            continue
        if pr['lam_single'] != 3 * ell:
            ok = False
            detail[v] = dict(problem='lam_single', got=pr['lam_single'], expect=3 * ell)
            continue
        eprof[v] = dict(e=pr['e'], ell=ell, first_b=pr['first_b'], nfires=pr['nfires'],
                        maxj=pr['maxj'], min_margin=pr['min_margin'],
                        max_drain=pr['max_drain'])
    print('[%s] U=%d v in %s..%s (n=%d): %s' % (tag, U, vlist[0], vlist[-1], len(vlist),
                                                'OK' if ok else 'FAIL'))
    if not ok:
        for k in list(detail)[:10]:
            print('   v=%s %s' % (k, detail[k]))
    return ok, detail, eprof


def main():
    report = {}

    # --- 1) micro vs closed form ---
    ok_micro = True
    nmm = 0
    for U in (3, 9, 15):
        for v in range(1, 16):
            mi = L.micro_excursion(U, v)
            tm = L.topmap_excursion(U, v)
            nmm += 1
            if mi[0] != tm[0] or mi[1] != tm[1] or mi[2] != tm[2]:
                ok_micro = False
                print('micro vs closed mismatch U=%d v=%d: %s vs %s' % (U, v, mi[0], tm[0]))
    print('[micro-vs-closed] %d runs: %s' % (nmm, 'OK' if ok_micro else 'FAIL'))
    report['micro_vs_closed'] = dict(ok=ok_micro, runs=nmm)

    # --- 2) main validation U=3, v=1..500 ---
    ok3, det3, eprof3 = compare(3, list(range(1, 501)), 'main')
    report['U3_v1_500'] = dict(ok=ok3, fails=len(det3), detail=det3)
    report['eprof_U3'] = eprof3

    # --- 3) spots U=9, U=15 ---
    spots = list(range(1, 251)) + [256, 300, 320, 384, 400, 443, 448, 449, 450, 500]
    ok9, det9, _ = compare(9, spots, 'spot')
    ok15, det15, _ = compare(15, spots, 'spot')
    report['U9_spots'] = dict(ok=ok9, fails=len(det9), detail=det9)
    report['U15_spots'] = dict(ok=ok15, fails=len(det15), detail=det15)

    # summary of e(v) on the U=3 data
    es = [eprof3[v]['e'] for v in eprof3]
    report['e_summary_U3_v1_500'] = dict(max_e=max(es), argmax=max(eprof3, key=lambda v: eprof3[v]['e']),
                                         all_singleton=all(eprof3[v]['e'] is not None for v in eprof3))
    report['PASS'] = bool(ok_micro and ok3 and ok9 and ok15)
    print('e(v) max over v<=500 (U=3): %d at v=%s' % (report['e_summary_U3_v1_500']['max_e'],
                                                      report['e_summary_U3_v1_500']['argmax']))
    print('TASK1 VERDICT:', 'PASS' if report['PASS'] else 'FAIL')
    with open('revC10_t1.json', 'w') as f:
        json.dump(report, f)


if __name__ == '__main__':
    main()
