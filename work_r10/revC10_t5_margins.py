# -*- coding: utf-8 -*-
"""revC10_t5_margins.py -- TASK 5: e(v) bound, e vs maxj+1, margin drain.

Data: revC10_t2.json (v<=8192, per-v endgame stats incl. walk deficit Delta at the
boundary snapshot, walk_maxj) and revC10_t4.json (v<=3e5) if present.
Checks:
  * e(v) <= 16 on all data;
  * e <= maxj+1 for maxj = endgame fire j's / crossing-decseq fire j's / walk maxj;
  * margin drain: for each v, walk deficit Delta (at pointer ~v-1) vs the endgame
    chains' c-deficit (v-1 - v2(c_x)) and margin v2(c_x)-j.
Saves revC10_t5.json.
"""
import json
import os

import revC10_lib as L


def analyse(per_v, cross, label):
    es, dlt, drains, margins, walkmaxj, endmaxj, seqmaxj = [], [], [], [], [], [], []
    ev_bad = []
    for v in sorted(per_v):
        r = per_v[v]
        e = r['e']
        es.append(e)
        if e > 16:
            ev_bad.append(v)
        dlt.append(r['Delta'])
        drains.append(r['max_drain'])
        margins.append(r['min_margin'] if r['min_margin'] is not None else 10**9)
        walkmaxj.append(r['walk_maxj'])
        endmaxj.append(r['maxj'])
        if cross and v in cross:
            seqmaxj.append(max([x for x in cross[v]['seq'] if x > 0] or [0]))
    res = dict(label=label, nv=len(es),
               max_e=max(es), e_gt16=len(ev_bad), e_bad_vs=ev_bad[:10],
               max_Delta=max(dlt), max_endgame_drain=max(drains),
               min_endgame_margin=min(margins),
               max_walk_maxj=max(walkmaxj), max_endgame_maxj=max(endmaxj),
               max_seq_maxj=max(seqmaxj) if seqmaxj else None)
    # e <= maxj+1 tests
    fails_end = [(v, per_v[v]['e'], per_v[v]['maxj']) for v in sorted(per_v)
                 if per_v[v]['maxj'] + 1 < per_v[v]['e']]
    fails_walk = [(v, per_v[v]['e'], per_v[v]['walk_maxj']) for v in sorted(per_v)
                  if per_v[v]['walk_maxj'] + 1 < per_v[v]['e']]
    fails_seq = []
    if cross:
        fails_seq = [(v, cross[v]['e'], max([x for x in cross[v]['seq'] if x > 0] or [0]))
                     for v in sorted(cross) if v in per_v and
                     max([x for x in cross[v]['seq'] if x > 0] or [0]) + 1 < cross[v]['e']]
    res['e_le_maxjend1'] = dict(ok=not fails_end, nfail=len(fails_end), ex=fails_end[:5])
    res['e_le_maxjseq1'] = dict(ok=not fails_seq, nfail=len(fails_seq), ex=fails_seq[:5])
    res['e_le_maxjwalk1'] = dict(ok=not fails_walk, nfail=len(fails_walk), ex=fails_walk[:5])
    # drain vs Delta
    excess = [(v, per_v[v]['max_drain'] - per_v[v]['Delta']) for v in sorted(per_v)]
    res['max_drain_excess_over_Delta'] = max(excess, key=lambda x: x[1])
    res['argmax_e'] = max(per_v, key=lambda v: per_v[v]['e'] or 0)
    return res


def main():
    d2 = json.load(open('revC10_t2.json'))
    per_v = {int(k): v for k, v in d2['per_v'].items()}
    cross = {int(k): v for k, v in d2['cross'].items()}
    out = dict(A=analyse(per_v, cross, 'v<=8192'))
    # recompute crossing decseq maxj from stored seqs
    print(json.dumps(out['A'], indent=1, default=str))
    if os.path.exists('revC10_t4.json'):
        d4 = json.load(open('revC10_t4.json'))
        # stage-2 walk stored only aggregate stats; rebuild per_v for 8192<v<=3e5? use t4 walk stats
        out['t4_summary'] = dict(maxe=d4['stage2']['maxe'], nbadres=d4['stage2']['nbadres'],
                                 walk=d4['stage2']['walk'])
        print('t4: max e over v<=3e5:', d4['stage2']['maxe'],
              'non-singleton:', d4['stage2']['nbadres'],
              'walk maxdef:', d4['stage2']['walk']['maxdef'], 'walk maxj:', d4['stage2']['walk']['maxj'])
    json.dump(out, open('revC10_t5.json', 'w'))
    print('saved revC10_t5.json')


if __name__ == '__main__':
    main()
