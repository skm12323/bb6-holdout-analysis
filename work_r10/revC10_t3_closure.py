# -*- coding: utf-8 -*-
"""revC10_t3_closure.py -- TASK 3: own symbolic closure on 2^18-cylinders.

For every crossing class arising in the v<=8192 sweep:
  class key = (i, d, rA=lamA mod 2^18, rY=lamfront mod 2^18, h=(v-1)-i);
  symbolic endgame with lam = r + 2^18*t (t free >= 0), boundary lambda = -1 exact,
  originals lambda = 0, c-side carried as deficit lower bounds (dAssume for the
  unknown A/Y split, exact 2^i for d=0);
  checks: every decision uniform in the free t's; every chain margin-safe with
  v2(c_x) >= n - delta; u-form (c even >= 2, lam odd >= 1) => u >= 2U+1 >= 3;
  terminates (no CAP).  Compare with the concrete decision sequence of every
  member v of the class.  Robustness: dAssume in {16, 30, 40}.
Saves revC10_t3.json.
"""
import json
from collections import defaultdict

import revC10_lib as L

N0 = 34          # below this n, the closure is not expected to apply (c-parts small)


def main():
    d = json.load(open('revC10_t2.json'))
    cross = {int(k): v for k, v in d['cross'].items()}
    for v in cross:
        cross[v]['h'] = (v - 1) - cross[v]['cls'][0]
    classes = defaultdict(list)
    for v in sorted(cross):
        i, dd, rA, rF = cross[v]['cls']
        classes[(i, dd, rA, rF, cross[v]['h'])].append(v)
    print('classes from v<=8192 sweep: %d (v=1..8192)' % len(classes))

    out = {}
    nfail = dict(NONUNIFORM=0, MARGIN=0, CPARITY=0, CAP=0, SEQMISMATCH=0)
    small_n = 0
    stats = dict(min_m=99, nmin_needed=0, maxdrain=0)
    for key, vs in sorted(classes.items()):
        i, dd, rA, rY, h = key
        vmin = min(vs)
        n = vmin - 1
        rec = dict(vs=vs[:6] + (['...'] if len(vs) > 6 else []), n=n)
        if n < N0:
            small_n += 1
            # concrete coverage only
            okc = all(cross[v].get('res', 'singleton') == 'singleton' for v in vs)
            rec['mode'] = 'small-n (concrete only)'
            rec['ok'] = okc
            out[str(key)] = rec
            continue
        worst = None
        for dA in (16, 30, 40):
            r = L.symbolic_endgame((i, dd, rA, rY, vmin), dAssume=dA)
            rec['dA%d' % dA] = dict(res=r['res'], fails=r['fails'],
                                    min_m=r.get('min_m'), nmin=r.get('nmin_needed'),
                                    maxdrain=r.get('maxdrain'), e=r.get('e'))
            if r['res'] != 'singleton' or r['fails']:
                worst = (dA, r)
            if r.get('min_m') is not None:
                stats['min_m'] = min(stats['min_m'], r['min_m'])
            stats['nmin_needed'] = max(stats['nmin_needed'], r.get('nmin_needed') or 0)
            stats['maxdrain'] = max(stats['maxdrain'], r.get('maxdrain') or 0)
            # sequence equality vs every concrete member
            for v in vs:
                if cross[v]['seq'] != r['seq']:
                    nfail['SEQMISMATCH'] += 1
                    rec.setdefault('seqmismatch', []).append((v, dA))
                    worst = worst or (dA, r)
        if worst:
            for f in worst[1]['fails'] or [('RES-' + worst[1]['res'],)]:
                tag = f[0] if isinstance(f, tuple) else f
                nfail[tag.split('-')[0] if '-' in tag else tag] = nfail.get(tag, 0) + 1
            rec['ok'] = False
        else:
            rec['ok'] = True
        out[str(key)] = rec
    nbig = sum(1 for r in out.values() if r.get('mode') != 'small-n (concrete only)')
    nok = sum(1 for r in out.values() if r.get('ok'))
    print('classes with n >= %d (closure applies): %d ; small-n (concrete): %d' % (N0, nbig, small_n))
    print('closure OK on %d/%d closure-classes ; failure counts: %s' % (nok, nbig, nfail))
    print('stats: min resolution depth reached m=%d ; max margin requirement nmin_needed=%d ; max c-drain=%d'
          % (stats['min_m'], stats['nmin_needed'], stats['maxdrain']))
    json.dump(dict(classes=out, nfail=nfail, stats=stats, N0=N0,
                   nclasses=len(classes), nbig=nbig, nok=nok, small_n=small_n),
              open('revC10_t3.json', 'w'))
    print('saved revC10_t3.json')


if __name__ == '__main__':
    main()
