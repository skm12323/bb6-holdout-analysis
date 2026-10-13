"""revD_gap5200.py -- ADVERSARY-2 extra: census of the uncertified gap zone
J = 3201..5000 (no table file covers it; the induction covers it, but the EL
'measured max 28 over J <= 5200' claim spans it). Records dk, dp, rho*, g,
S_win, max window param; checks dk <= j, dp <= 6, g <= 6, dp+S_win <= 66.

Usage: python -B revD_gap5200.py [LO=3201] [HI=5000]
"""
import sys

def v2(x): return (x & -x).bit_length() - 1

_TC = {}


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
    steps = []
    while True:
        (b, bl), (c, cl) = Q[0], Q[1]
        if A % 2 == 0:
            steps.append(('E', bl, cl, None))
            A = A + b + c + 3
            Q = Q[2:]
            continue
        x = A + 2 * b + 3
        j = v2(x)
        uu = x >> j
        assert uu >= 3
        if bl[0] == 'T':
            dk = (x - 9 * (1 << bl[1]) * P - 4 - 6 * kh) // 6
            steps.append(('C', bl, cl, j))
            return {'steps': steps, 'dk': dk, 'dp': bl[1]}
        steps.append(('C', bl, cl, j))
        Q = [(uu << a, ('M',)) for a in range(j - 1)] + \
            [(c + (A + 1) // 2, ('d',))] + Q[2:]
        A = uu + 1


def main(LO=3201, HI=5000):
    print('== revD extra: gap-zone census J = %d..%d ==' % (LO, HI))
    maxSw = 0; maxSw_at = None; maxE = 0; maxdp = 0; maxg = 0; maxwinj = 0
    mindk_margin = 10**9; mindk_at = None
    maxEL = 0; maxEL_at = None
    bad = []
    for J in range(LO, HI + 1):
        r = interlude(J)
        st = r['steps']
        chains = [i for i, s in enumerate(st) if s[0] == 'C']
        re_ = chains[-1]
        pure = [i for i in chains if st[i][1][0] == 'R' and st[i][2][0] == 'R']
        i_last = pure[-1]
        rho = st[i_last][1][1]
        win = [i for i in chains if i >= i_last and i != re_]
        Sw = sum(st[i][3] for i in win)
        g = J - 2 - rho
        EL = r['dp'] + Sw
        if EL > maxEL:
            maxEL, maxEL_at = EL, (J, rho, g, r['dp'], Sw)
        if Sw > maxSw:
            maxSw, maxSw_at = Sw, (J,)
        maxdp = max(maxdp, r['dp'])
        maxg = max(maxg, g)
        maxwinj = max(maxwinj, max([st[i][3] for i in win]))
        if J - r['dk'] < mindk_margin:
            mindk_margin, mindk_at = J - r['dk'], J
        if r['dp'] > 6 or g > 6 or r['dk'] > J or any(st[i][3] >= J for i in win):
            bad.append((J, r['dk'], r['dp'], g, max(st[i][3] for i in win)))
    print('  max dp+S_win = %d at (J,rho,g,dp,Sw)=%s  [EL claim: <=66, max 28]'
          % (maxEL, maxEL_at))
    print('  max dp=%d ; max g=%d ; max win param=%d ; min J-dk=%d at J=%d'
          % (maxdp, maxg, maxwinj, mindk_margin, mindk_at))
    print('  violations (dp>6|g>6|dk>J|winparam>=J): %d %s' % (len(bad), bad[:5]))


if __name__ == '__main__':
    LO = int(sys.argv[1]) if len(sys.argv) > 1 else 3201
    HI = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    main(LO, HI)
