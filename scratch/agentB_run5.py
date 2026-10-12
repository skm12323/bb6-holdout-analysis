"""agentB_run5.py — test the k-map hypothesis:
at each tail-pair chain at pointer p:  x = 9*2^p * w + (6k+4)   [w=2t+1]
   i.e. x = (9*2^{p+1}) t + (9*2^p + 6k + 4),  j = v2(6k+4) = 1+v2(3k+2)
k follows: k -> k + 1 + min(2, v2(3k+2)//2), k_0 = 1 at p=4.
Also: classify MID chains (U/D-consuming) and get p-increments."""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import *

def full_chain_data(v):
    L = E_sym(v)
    tags = ['A0'] + [('T%d' % i) for i in range(v - 1)] + [('T%d*' % (v - 1))]
    cc = 1
    out = []
    t = 0
    while len(L) > 1:
        A = L[0]
        btag = tags[1] if len(tags) > 1 else 'Z'
        ctag = tags[2] if len(tags) > 2 else 'Z'
        if A[1] % 2 == 0:
            b = L[1] if len(L) > 1 else (0, 0)
            c = L[2] if len(L) > 2 else (0, 0)
            L = [(A[0] + b[0] + c[0], A[1] + b[1] + c[1] + 3)] + L[3:]
            tags = [tags[0]] + tags[3:]
        else:
            b = L[1] if len(L) > 1 else (0, 0)
            c = L[2] if len(L) > 2 else (0, 0)
            ax = A[0] + 2 * b[0]; bx = A[1] + 2 * b[1] + 3
            j = v2i(bx)
            au = ax >> j; bu = bx >> j
            D = (c[0] + (A[0] >> 1), c[1] + ((A[1] + 1) >> 1))
            p = None; o = None; k = None
            if btag.startswith('T') and not btag.endswith('*'):
                p = int(btag[1:])
                o = bx - 9 * (1 << p)
                assert (o - 4) % 6 == 0, (t, o)
                k = (o - 4) // 6
                # check alpha form: x = (9*2^{p+1}) t + (9*2^p + 6k+4)
                assert ax == 9 * (1 << (p + 1)), (t, ax, p)
                assert bx == 9 * (1 << p) + 6 * k + 4
            out.append(dict(step=t, j=j, u=(au, bu), D=D, btag=btag, ctag=ctag,
                            p=p, k=k, o=o, A=A, b=b, c=c, x=(ax, bx)))
            L = ([(au, bu + 1)] + [(au << q, bu << q) for q in range(j - 1)] + [D] + L[3:])
            tags = (['A%d' % cc] + [('U%d.%d' % (cc, q)) for q in range(j - 1)] + [('D%d' % cc)] + tags[3:])
            cc += 1
        t += 1
    return out, t

def kmap(k):
    return k + 1 + min(2, v2i(3 * k + 2) // 2)

def main():
    v = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    chains, ell = full_chain_data(v)
    print('v=%d ell=%d chains=%d' % (v, ell, len(chains)))
    # test k-map on tail-pair chains
    tchains = [c for c in chains if c['p'] is not None]
    ok = True
    kpred = 1
    first = True
    mismatches = []
    for c in tchains:
        if first:
            assert c['k'] == 1
            first = False
        else:
            if c['k'] != kpred:
                ok = False
                mismatches.append((c['step'], c['k'], kpred, c['btag']))
        kpred = kmap(c['k'])
    print('k-map holds for all %d tail-pair chains:' % len(tchains), ok)
    if mismatches:
        print('first mismatches:', mismatches[:10])
    # test j = 1+v2(3k+2) for tail chains
    ok2 = all(c['j'] == 1 + v2i(3 * c['k'] + 2) for c in tchains)
    print('j = 1+v2(3k+2) for all tail-pair chains:', ok2)
    # p increments vs k increments
    incs = {}
    for c1, c2 in zip(tchains, tchains[1:]):
        dk = c2['k'] - c1['k']; dp = c2['p'] - c1['p']; j = c1['j']
        incs.setdefault((j, dk, dp), 0)
        incs[(j, dk, dp)] += 1
    print('(j, dk, dp) -> count:', sorted(incs.items()))
    # MID chains: those with p None (b not a plain T)
    mids = [c for c in chains if c['p'] is None]
    from collections import Counter
    cnt = Counter((c['btag'].split('.')[0][:2] if not c['btag'].startswith('T') else 'T',
                   c['j']) for c in mids)
    print('MID chain (bkind, j) counts:', dict(cnt))
    # spike aftermath details: print chains around spikes j>=5
    idxs = [i for i, c in enumerate(chains) if c['j'] >= 5]
    print('spike chain positions:', idxs[:30])
    for s in idxs[:8]:
        print('--- around spike chain %d (j=%d, p=%s, k=%s):' % (s, chains[s]['j'], chains[s]['p'], chains[s]['k']))
        for c in chains[max(0, s - 1):s + 6]:
            print('   step %5d j=%2d b=%-9s c=%-9s p=%s k=%s ub=%d' %
                  (c['step'], c['j'], c['btag'], c['ctag'], c['p'], c['k'], c['u'][1]))
    # last chains (endgame)
    print('--- last 8 chains:')
    for c in chains[-8:]:
        print('   step %5d j=%2d b=%-9s c=%-9s p=%s k=%s ub=%d Ab=%d xb=%d' %
              (c['step'], c['j'], c['btag'], c['ctag'], c['p'], c['k'], c['u'][1], c['A'][1], c['x'][1]))

if __name__ == '__main__':
    main()
