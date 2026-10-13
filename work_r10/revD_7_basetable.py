"""revD_7_basetable.py -- ADVERSARY-2 attack 7: re-certify the base table.

Part 1: cross-check the ENTIRE cpt table (j = 121..3200) against THIS
reviewer's independent concrete tracer (canonical class member, exact big-int;
a different engine from run7's symbolic class-split sim).
Part 2 (separate invocation 'run7'): stratified run7 re-certification:
every 100th j + boundaries; verify (dk,dp) match the table and leaves == 1.

Usage:
  python -B revD_7_basetable.py cross     # part 1
  python -B revD_7_basetable.py run7      # part 2 (needs scratch on sys.path)
"""
import sys
import json

def v2(x): return (x & -x).bit_length() - 1


def interlude(J, p_extra=60, tail=90):
    mod = 1 << J
    kh = ((1 << (J - 1)) - 2) * pow(3, -1, mod) % mod
    p = J + p_extra
    P = 1 << p
    x0 = 9 * P + 6 * kh + 4
    u = x0 >> J
    A = u + 1
    Q = [(u << a, ('R', a)) for a in range(J - 1)]
    Q.append((15 * P // 2 + 3 * kh + 1, ('D',)))
    Q += [(3 * (1 << e) * P, ('T', e)) for e in range(2, tail)]
    while True:
        (b, bl), (c, cl) = Q[0], Q[1]
        if A % 2 == 0:
            A = A + b + c + 3
            Q = Q[2:]
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3, ('halt-like', J)
        if bl[0] == 'T':
            return ((x - 9 * (1 << bl[1]) * P - 4 - 6 * kh) // 6, bl[1])


def cross():
    print('== revD attack 7a: own tracer vs agentD_table_cpt.json (121..3200) ==')
    d = json.load(open('agentD_table_cpt.json'))
    d5 = json.load(open('agentD_table5100.json'))
    bad = 0
    n = 0
    for src in (d, d5):
        for k_, v in sorted(src.items(), key=lambda kv: int(kv[0])):
            j = int(k_)
            mine = interlude(j)
            n += 1
            if mine != tuple(v):
                bad += 1
                if bad < 10:
                    print('  MISMATCH j=%d: mine=%s table=%s' % (j, mine, v))
    print('  cross-checked %d entries; mismatches: %d' % (n, bad))
    # margins
    mm = min(int(k_) - v[0] for k_, v in d.items())
    mm2 = min(int(k_) - v[0] for k_, v in d5.items())
    print('  min margin j-dk: cpt %d ; 5100 %d ; max dp: %d ; dk(3200)=%s dk(5100)=%s'
          % (mm, mm2, max(v[1] for v in d.values()), d['3200'], d5['5100']))
    print('VERDICT attack 7a:', 'CONFIRMED' if bad == 0 else 'REFUTED')


def run7():
    print('== revD attack 7b: run7 stratified re-certification ==')
    sys.path.insert(0, r'D:\math_cc\scratch')
    from agentB_run7 import verify
    d = json.load(open('agentD_table_cpt.json'))
    d5 = json.load(open('agentD_table5100.json'))
    tab = {}
    tab.update({int(k_): tuple(v) for k_, v in d.items()})
    tab.update({int(k_): tuple(v) for k_, v in d5.items()})
    strat = sorted(set(list(range(121, 3201, 100)) + [121, 122, 3199, 3200, 1539, 3066]
                       + [5, 8, 12, 14, 19, 20, 38, 64, 120]))
    bad = 0
    nleaves_not1 = []
    for j in strat:
        res, err = verify(j)
        if err is not None:
            print('  j=%d ERROR: %s' % (j, err))
            bad += 1
            continue
        (pair, leaves) = res
        if leaves != 1:
            nleaves_not1.append((j, leaves))
        if j in tab and pair != tab[j]:
            print('  j=%d run7=%s table=%s MISMATCH' % (j, pair, tab[j]))
            bad += 1
        elif j not in tab:
            print('  j=%d run7=%s (no table entry; dk<=j: %s)' % (j, pair, pair[0] <= j))
    print('  verified %d stratified j; mismatches vs table: %d; leaves!=1: %s'
          % (len(strat), bad, nleaves_not1 or 'none'))
    # far spot values
    for j, exp_dk in ((20000, 8922), (30000, 13384)):
        res, err = verify(j)
        if err is not None:
            print('  j=%d ERROR: %s' % (j, err))
            bad += 1
        else:
            (pair, leaves) = res
            print('  j=%d run7 (dk,dp)=%s leaves=%d  [report dk=%d: %s; dk<=j: %s]'
                  % (j, pair, leaves, exp_dk, 'OK' if pair[0] == exp_dk else 'DIFF',
                     pair[0] <= j))
            if leaves != 1:
                nleaves_not1.append((j, leaves))
            bad += 0 if pair[0] == exp_dk else 1
    print('VERDICT attack 7b:', 'CONFIRMED' if bad == 0 and not nleaves_not1 else 'GAP/REFUTED')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'cross'
    if mode == 'cross':
        cross()
    else:
        run7()
