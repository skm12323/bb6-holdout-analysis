"""reviewB_probe6.py -- ATTACK 6: endgame domination (Theorem 5 item 2).

Claim: exit/endgame chains keep odd part u >= 2^(v - 2 log2 v - c) >= 3 for
v >= 60.  Extract the exact affine form (in t, w = 2t+1) of every endgame
chain's x for v = 60..300 (superset of {60,61,100,128,200}), verify the odd
part bound, find the worst v and the implied constant c; also count template
shapes and check lam > 0 (scale part survives) with worst dyadic denominator.
"""
import sys, time, math
from collections import defaultdict
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import v2i
from agentB_run9 import endgame_run
from reviewB_lib import tab

def main():
    t0 = time.time()
    TAB = {}
    for j in range(1, 121):
        res, err = None, None
        from agentB_run7 import verify
        res, err = verify(j)
        assert not err, (j, err)
        TAB[j] = res[0]
    shapes = defaultdict(list)
    data = {}     # v -> list of (j, au, bu) per boundary chain (u-forms)
    minu = {}
    for v in range(60, 301):
        steps, events, done = endgame_run(v, TAB)
        assert done is True, (v, done)
        shp = tuple((e[0], e[1] if e[0] == 'E' else (e[1], e[2], e[3])) for e in events)
        shapes[shp].append(v)
        lst = []
        for e in events:
            if e[0] == 'C':
                j, (au, bu) = e[1], e[4]
                assert bu % 2 == 1 and au >= 0, (v, e)
                lst.append((j, au, bu))
        data[v] = lst
        minu[v] = min([bu for (_, _, bu) in lst], default=None)
    print('v=60..300: distinct endgame template shapes: %d' % len(shapes))
    for vv in (60, 61, 100, 128, 200):
        print('  v=%d: %d boundary chains, shapes seen; chains (j, u = au*t+bu):'
              % (vv, len(data[vv])))
        for (j, au, bu) in data[vv]:
            print('     j=%2d  u = %d*t + %d   (x = u*2^j)' % (j, au, bu))
    # worst v
    worst = min(minu.items(), key=lambda kv: kv[1] if kv[1] else 10 ** 9)
    print('worst v (min chain odd-part u(0)=bu): v=%d u=%d' % worst)
    # implied c: bu >= 2^(v - 2 log2 v - c)  ->  c >= v - 2log2 v - log2 bu
    cmax = -10 ** 9
    carg = None
    for v in range(60, 301):
        for (j, au, bu) in data[v]:
            c = v - 2 * math.log2(v) - math.log2(bu)
            if c > cmax:
                cmax, carg = c, (v, j, au, bu)
    print('max implied c = %.2f at (v,j,au,bu)=%s  -> claim u >= 2^(v-2log2v-%.0f)'
          % (cmax, carg, math.ceil(cmax)))
    print('all u(0) >= 3:', all(bu >= 3 for v in range(60, 301)
                                for (_, _, bu) in data[v]))
    print('all u(0) odd:', all(bu % 2 == 1 for v in range(60, 301)
                               for (_, _, bu) in data[v]))
    # lam (scale coefficient): au >= 2^(v - 2 log2 v - c) too?  au = lam*2^v/2^j
    worst_au = min(((au, v, j) for v in range(60, 301)
                    for (j, au, bu) in data[v]), key=lambda x: x[0])
    print('min au (t-coefficient) = %d at (v=%d,j=%d); log2(au) vs v-2log2v-c:'
          % worst_au, '%.1f vs %.1f'
          % (math.log2(worst_au[0]), worst_au[1] - 2 * math.log2(worst_au[1]) - math.ceil(cmax)))
    print('total %.1fs' % (time.time() - t0))

if __name__ == '__main__':
    main()
