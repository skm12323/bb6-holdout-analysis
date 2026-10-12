"""Inventory of end-phase list SHAPES for s <= S: classify each entry relative to a
detected doubling base W; also measure the 2-adic depth actually read by decisions."""
import sys
sys.setrecursionlimit(100000)
from prover2 import add, sc, sub, par, half, ge3, v2f, halfn, Z0, T_list, encode, final_match

def shape(L):
    """Classify list entries: find longest doubling run; mark each entry as
    'h' (2^i W multiple, with i), 'J' (2^i W + odd kap), 'x' (head), 'o' (other, with residue parity)."""
    # find best doubling run: try each start position
    best = None
    for st in range(1, min(len(L) - 1, 6)):
        W = L[st]
        if L[st + 1] != sc(W, 2): continue
        i = 2
        while st + i < len(L) and L[st + i] == sc(W, 1 << i): i += 1
        # run covers [st, st+i)
        kap = sub(L[st + i], sc(W, 1 << i)) if st + i < len(L) else None
        Jis = (kap is not None and kap[0] == 0 and kap[1] % 2 == 1 and abs(kap[1]) < (1 << 20))
        score = i + (1 if Jis else 0)
        if best is None or score > best[0]:
            best = (score, st, i, kap, Jis)
    if best is None:
        return 'flat:' + ','.join('o%d' % (e[1] % 2) if e[0] == 0 else 'O' for e in L)
    _, st, i, kap, Jis = best
    tags = []
    for k in range(st):
        tags.append('x' if k == 0 else ('o%d' % (L[k][1] % 2) if L[k][0] == 0 else 'O'))
    for k in range(i):
        tags.append('r')
    if st + i < len(L):
        tags.append('J' if Jis else 'j%s' % (kap[1] % 2 if kap[0] == 0 else 'U'))
    for k in range(st + i + 1, len(L)):
        e = L[k]
        tags.append('z%d' % (e[1] % 2) if e[0] == 0 else ('Z' if e[0] % 2 == 0 else 'Zu'))
    return ''.join(tags)

def run_shapes(S=120, tail=12):
    from collections import Counter
    shapes = Counter()
    depth_read = 0
    for v in range(2, S + 1):
        w3 = (6, 3)
        L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + [add(sc(w3, 1 << (v - 1)), (0, -1))]
        hist = [list(L)]
        while len(L) > 1:
            L = T_list(L); hist.append(list(L))
        for L in hist[-tail:]:
            shapes[shape(L)] += 1
    return shapes

if __name__ == '__main__':
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    sh = run_shapes(S)
    print('end-phase shapes for v=2..%d (last 12 lists each), %d distinct:' % (S, len(sh)))
    for k, c in sh.most_common(40):
        print('  %5d  %s' % (c, k))
