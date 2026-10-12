"""agentB_run12.py — per-template symbolic forms: for each endgame shape class,
fit every chain's u (and the safety of the whole excursion) as
u_b = lam*2^v + mu*k_b + nu with k_b = k-index of the last canonical T-chain
before the boundary; verify fit on all members; report lam (must be >0 or
analyzable) and the worst-case scale drop e = v - log2(lam*2^v)."""
import sys
from fractions import Fraction as Fr
from collections import defaultdict
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import v2i
from agentB_run7 import verify
from agentB_run9 import endgame_run

def main():
    TAB = {}
    for j in range(1, 121):
        res, err = verify(j)
        assert not err
        TAB[j] = res[0]
    def kb_of(v):
        """k-index of last canonical T-chain with p+dp <= v-1 (boundary k)."""
        p, k = 4, 1
        lastk = 1
        while True:
            j = 1 + v2i(3 * k + 2)
            dp = TAB[j][1]
            if p + dp > v - 1:
                return lastk
            p += dp; k += TAB[j][0]; lastk = k
    shapes = defaultdict(list)
    meta = {}
    for v in range(1, 2001):
        steps, events, done = endgame_run(v, TAB)
        assert done
        shp = tuple((e[0], e[1] if e[0] == 'E' else (e[1], e[2], e[3])) for e in events)
        shapes[shp].append(v)
        meta[(shp, v)] = [e[4][1] for e in events if e[0] == 'C']
    print('templates:', len(shapes))
    worst = 0
    for shp, vs in sorted(shapes.items(), key=lambda kv: kv[1][0]):
        nc = len(meta[(shp, vs[0])])
        # fit each chain's u_b as lam*2^v + mu*k + nu using 3 points
        pts = vs[:3] if len(vs) >= 3 else vs
        okfit = True
        info = []
        for ci in range(nc):
            if len(vs) >= 3:
                M = [[Fr(1 << v), Fr(kb_of(v)), Fr(1)] for v in pts]
                rhs = [Fr(meta[(shp, v)][ci]) for v in pts]
                # solve 3x3
                import itertools
                def det3(m):
                    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
                          - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                          + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
                D = det3(M)
                assert D != 0
                sol = []
                for col in range(3):
                    Mc = [row[:] for row in M]
                    for r in range(3):
                        Mc[r][col] = rhs[r]
                    sol.append(det3(Mc) / D)
                lam, mu, nu = sol
                # verify on all members
                for v in vs:
                    if lam * (1 << v) + mu * kb_of(v) + nu != meta[(shp, v)][ci]:
                        okfit = False
                info.append((lam, mu, nu))
            else:
                info.append(None)
        minlam = min((abs(i[0]) for i in info if i), default=None)
        zerolam = [c for c, i in enumerate(info) if i and i[0] == 0]
        if info and all(i for i in info):
            # scale drop: lam = c/2^e
            es = []
            for i in info:
                if i[0] != 0:
                    l = i[0]
                    e = 0
                    while l != int(l):
                        l *= 2; e += 1
                    es.append(e)
            worst = max(worst, max(es) if es else 0)
        if vs[0] <= 30 or zerolam:
            print('  class v0=%-4d n=%-4d chains=%d fit_ok=%s lam=0 at %s' %
                  (vs[0], len(vs), nc, okfit, zerolam))
            for i in info:
                if i: print('      lam=%s mu=%s nu=%s' % i)
    print('worst dyadic denominator exponent across all templates:', worst)

if __name__ == '__main__':
    main()
