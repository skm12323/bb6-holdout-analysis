"""revD_7_fast.py -- ADVERSARY-2 attack 7a (fast): cross-check the ENTIRE
cpt table (j = 121..3200) and the 5100 table (5001..5200) against THIS
reviewer's independent concrete tracer (canonical class member, exact big-int;
a different engine from run7's symbolic class-split sim). Deque-based queue:
O(1) pops, labels kept, so each interlude costs O(total pushed entries) ~ O(J).

Usage: python -B revD_7_fast.py
"""
import sys
import json
import time
from collections import deque

def v2(x): return (x & -x).bit_length() - 1


def interlude(J, p_extra=60, tail=90):
    mod = 1 << J
    kh = ((1 << (J - 1)) - 2) * pow(3, -1, mod) % mod
    p = J + p_extra
    P = 1 << p
    x0 = 9 * P + 6 * kh + 4
    u = x0 >> J
    A = u + 1
    Q = deque((u << a, ('R', a)) for a in range(J - 1))
    Q.append((15 * P // 2 + 3 * kh + 1, ('D',)))
    for e in range(2, tail):
        Q.append((3 * (1 << e) * P, ('T', e)))
    while True:
        b, bl = Q.popleft()
        c, cl = Q.popleft()
        if A % 2 == 0:
            A = A + b + c + 3
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3, ('halt-like', J)
        if bl[0] == 'T':
            dk = (x - 9 * (1 << bl[1]) * P - 4 - 6 * kh) // 6
            # canonical re-entry sanity: c is T_{e+1}
            assert cl[0] == 'T' and cl[1] == bl[1] + 1, ('non-canonical', J)
            return (dk, bl[1])
        Q.appendleft((c + (A + 1) // 2, ('d',)))
        Q.extendleft((uu << a, ('M',)) for a in range(j - 2, -1, -1))
        A = uu + 1


def main():
    print('== revD attack 7a (fast): own tracer vs certified tables ==')
    entries = []
    for fn in ('agentD_table_cpt.json', 'agentD_table5100.json'):
        d = json.load(open(fn))
        for k_, v in d.items():
            entries.append((int(k_), tuple(v)))
    entries.sort()
    bad = 0
    t0 = time.time()
    for j, exp in entries:
        mine = interlude(j)
        if mine != exp:
            bad += 1
            if bad < 10:
                print('  MISMATCH j=%d: mine=%s table=%s' % (j, mine, exp))
    print('  cross-checked %d entries in %.0fs; mismatches: %d'
          % (len(entries), time.time() - t0, bad))
    print('VERDICT attack 7a:', 'CONFIRMED' if bad == 0 else 'REFUTED')


if __name__ == '__main__':
    main()
