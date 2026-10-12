"""agentB_run8.py — extract cascade structure: labeled abstract runs per j."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_abs import Val, Ctx, v2_val, parity, Ambiguous, NeedsSplit, ZERO
from agentB_run7 import kappa_for, pow2exp, is_T, T_of

def cascade(j, kappa=None, m=None, p=None):
    """Labeled run of the j-aftermath. Returns list of events:
    ('E', lbl_b, lbl_c) or ('C', jmid, lbl_b, lbl_c, midpos or None)"""
    if kappa is None:
        kappa = kappa_for(j); m = j
    ctx = Ctx(p=p or max(200, j + 100), kappa=kappa, m=m)
    u = Val(Fr(9, 1 << j), Fr(6, 1 << j), Fr(4, 1 << j))
    A = u + 1
    queue = [(u * (1 << a), ('R', a)) for a in range(j - 1)]
    queue.append((Val(Fr(15, 2), 3, 1), ('D0',)))
    for e in range(2, 120):
        queue.append((T_of(e), ('T', e)))
    events = []
    midcnt = 0
    guard = 0
    while guard < 800:
        guard += 1
        (b, lb) = queue[0] if queue else (ZERO, 'Z')
        if parity(A, ctx) == 1 and is_T(b):
            return events, ('re-entry', lb)
        (c, lc) = queue[1] if len(queue) > 1 else (ZERO, 'Z')
        rest = queue[2:]
        if parity(A, ctx) == 0:
            A = A + b + c + 3
            queue = rest
            events.append(('E', lb, lc))
        else:
            x = A + b * 2 + 3
            jm = v2_val(x, ctx)
            u2 = x * Fr(1, 1 << jm)
            D = c + (A + 1) * Fr(1, 2)
            midcnt += 1
            queue = [(u2 * (1 << q), ('M%d.%d' % (midcnt, q))) for q in range(jm - 1)]
            queue.append((D, ('DM%d' % midcnt,)))
            queue.extend(rest)
            A = u2 + 1
            events.append(('C', jm, lb, lc))
    return events, ('no-re-entry',)

def main():
    for j in list(range(5, 33)) + [40, 48, 56, 64]:
        ev, end = cascade(j)
        compact = []
        for e in ev:
            if e[0] == 'E':
                compact.append('E')
            else:
                compact.append('C%d@%s' % (e[1], e[2]))
        print('j=%2d: %s | %s' % (j, ' '.join(compact), end[0]))

if __name__ == '__main__':
    main()
