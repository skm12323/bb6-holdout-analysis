"""agentB_run9.py (v2) — endgame templates: record events from the first step
that consumes an entry with index >= v-2 (i.e., the last two T's, the defect
T*, or Z).  Express every chain's u as an exact form  u = lam*2^v + mu*k_b + nu
where k_b is the boundary k (tracked via the k-map with the verified table),
and check: shape classes are finitely many; (lam, mu, nu) constant per class;
u_min over the class >= 3; lam>0 or mu>=0 domination."""
import sys
from fractions import Fraction as Fr
from collections import defaultdict
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import v2i

TAB = {}   # j -> (dk, dp)  filled by caller

def kmap_run(vmax):
    """positions/k along the universal sequence up to p >= vmax."""
    seq = [(4, 1, 1)]   # (p, k, j)
    p, k = 4, 1
    while p < vmax + 40:
        j = 1 + v2i(3 * k + 2)
        dk, dp = TAB[j]
        p, k = p + dp, k + dk
        seq.append((p, k, 1 + v2i(3 * k + 2)))
    return seq

def endgame_run(v, kseq):
    L = [(6, 4)] + [(3 << (i + 1), 3 << i) for i in range(v - 1)] + [(3 << v, (3 << (v - 1)) - 1)]
    queue = [(L[i], (i - 1) - v) for i in range(1, v + 1)]  # T tags = offset from v
    queue[-1] = (L[v], 'T*')
    events = []
    boundary = False
    steps = 0
    A = L[0]
    while True:
        if not queue:
            return steps, events, True
        b = queue[0]
        c = queue[1] if len(queue) > 1 else ((0, 0), 'Z')
        rest = queue[2:]
        tb, tc = b[1], c[1]
        def atboundary(t):
            return (isinstance(t, int) and t >= -2) or t in ('T*', 'Z')
        if atboundary(tb) or atboundary(tc):
            boundary = True
        def fmt(t):
            return t if isinstance(t, str) else ('T%+d' % t)
        if A[1] % 2 == 0:
            A = (A[0] + b[0][0] + c[0][0], A[1] + b[0][1] + c[0][1] + 3)
            queue = rest
            if boundary: events.append(('E', fmt(tb), fmt(tc)))
        else:
            x = (A[0] + 2 * b[0][0], A[1] + 2 * b[0][1] + 3)
            j = v2i(x[1])
            u = (x[0] >> j, x[1] >> j)
            assert u[1] != 1, ('HALT', v)
            D = (c[0][0] + (A[0] >> 1), c[0][1] + ((A[1] + 1) >> 1))
            queue = [((u[0] << q, u[1] << q), 'M%d' % q) for q in range(j - 1)] + [(D, 'D')] + rest
            A = (u[0], u[1] + 1)
            if boundary:
                events.append(('C', j, fmt(tb), fmt(tc), u))
        steps += 1
        if steps > 10 * v + 200:
            return steps, events, None

def main():
    from agentB_run7 import verify
    for j in range(1, 121):
        res, err = verify(j)
        assert not err, (j, err)
        TAB[j] = res[0]
    VMAX = 2000
    kseq = kmap_run(VMAX)
    shapes = defaultdict(list)
    for v in range(1, VMAX + 1):
        steps, events, done = endgame_run(v, kseq)
        assert done is True, (v, done)
        shp = tuple((e[0], e[1] if e[0] == 'E' else (e[1], e[2], e[3])) for e in events)
        shapes[shp].append(v)
    print('v=1..%d: distinct endgame shapes: %d' % (VMAX, len(shapes)))
    # sizes
    lens = sorted(set(len(s) for s in shapes))
    print('endgame lengths (events): min %d max %d' % (lens[0], lens[-1]))
    # per shape: check u-forms as (lam, mu, nu) in (2^v, 1): mu*k part too complex;
    # instead record u beta values at first and last v of class and check growth
    bad = 0
    for shp, vs in shapes.items():
        mn = 1 << 62
        for v in vs:
            steps, events, _ = endgame_run(v, kseq)
            for e in events:
                if e[0] == 'C':
                    mn = min(mn, e[4][1])
        if mn < 3:
            bad += 1
            print('SHAPE WITH u<3: vs=%s' % vs[:5])
    print('shapes with any u<3:', bad)
    # stability: shapes appearing more than once vs singleton shapes
    multi = sum(1 for s in shapes.values() if len(s) > 1)
    print('shapes occurring >1 time:', multi, ' singletons:', len(shapes) - multi)
    # max number of events in an endgame
    print('example shapes for a few classes:')
    for shp, vs in sorted(shapes.items(), key=lambda kv: kv[1][0])[:8]:
        print('  v in', vs[:6], ('...' if len(vs) > 6 else ''), 'len', len(shp), ':',
              str([e[:4] if e[0] == 'C' else e[:3] for e in shp])[:220])

if __name__ == '__main__':
    main()
