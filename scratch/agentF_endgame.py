"""agentF_endgame.py -- endgame / second-life statistics and large-sp a0 table.

Collects, for top frames s <= N:
  End(s) (endgame length), r_after(s), the levels of chains fired inside the
  endgame (second-life levels sp''), and their Delta magnitudes; plus the a0
  table for sp up to 26 and the walk margin law p_{i-1} > sp_i.
"""
import sys, json
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_lib import add, sc, T_list, par, v2f
from agentF_fast import FastEll, top_c, v2_int, W3

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000


def window_entries(H, r, kap):
    return [sc(H, 2 << i) for i in range(r - 2)] + [add(sc(H, 1 << r), kap)]


class Instr(FastEll):
    """FastEll with endgame instrumentation (chain levels inside endgame)."""

    def __init__(self):
        FastEll.__init__(self)
        self.chain_levels = []      # (s, level) of endgame chains w/ level>=2
        self.endstats = {}          # s -> (End, r_after)

    def endgame_instr(self, L, s):
        n = 0
        while len(L) > 1:
            A = L[0]
            b = L[1] if len(L) > 1 else (0, 0)
            if par(A) == 1 and len(L) >= 2:
                x = add(A, b, b, (0, 3))
                q = v2f(x)
                if q >= 2:
                    self.chain_levels.append((s, q))
            L = T_list(L)
            n += 1
            assert n < 10 ** 6
        return n

    def ell_of_instr(self, s):
        if s in self.ell:
            return self.ell[s]
        kap = (0, -1)
        if s <= 2:
            L = [add(W3, (0, 1))] + [sc(W3, 1 << i) for i in range(s - 1)] + \
                [add(sc(W3, 1 << (s - 1)), (0, -1))]
            e = self.endgame_instr(L, s)
            self.endstats[s] = (e, 0)
            self.ell[s] = e
            return e
        r = s - 1
        t = 0
        while True:
            if t == 0 or t % 2 == 1:
                if r - 2 >= 2:
                    t += 1
                    r -= 2
                    continue
                H = sc(W3, 1 << (s - 1 - r))
                d = 3 * t + 1
                post = [add(sc(H, 4), (0, d + 3))] + window_entries(H, r, kap)
                e = (t + 1) + self.endgame_instr(post, s)
                self.endstats[s] = (e - (t + 1), r - 2)
                self.ell[s] = e
                return e
            sp = v2_int(3 * t + 4)
            Lc = self.ell[sp]
            a = self.a0_of(sp) if r >= 3 else min(self.a0_of(sp), 1)
            if r - 2 - a >= 2:
                t += 1 + Lc
                r -= 2 + a
                continue
            H = sc(W3, 1 << (s - 1 - r))
            d = 3 * t + 1
            win = window_entries(H, r, kap)
            head = add(sc(H, 4), (0, d + 3 + 3 * Lc), *win[:a])
            post = [head] + win[a:]
            e = (t + 1 + Lc) + self.endgame_instr(post, s)
            self.endstats[s] = (e - (t + 1 + Lc), r - 2 - a)
            self.ell[s] = e
            return e


fe = Instr()
fe.a0.update({1: 1, 2: 0, 3: 1, 4: 0, 5: 2, 6: 1, 7: 0, 8: 2})
for s in range(1, N + 1):
    fe.ell_of_instr(s)
ells = fe.ell

# a0 for sp up to 26 via concrete method
a0big = {}
for sp in range(1, 27):
    a0big[sp] = fe.a0_of(sp)
print('a0(1..26):', [a0big[i] for i in range(1, 27)])
print('max a0 over sp<=26:', max(a0big.values()))

# End / r_after / correlation
Ends = {s: v[0] for s, v in fe.endstats.items()}
ras = {s: v[1] for s, v in fe.endstats.items()}
print('End: max=%d at %s' % (max(Ends.values()),
      [s for s in Ends if Ends[s] == max(Ends.values())][:12]))
print('r_after range: [%d, %d]' % (min(ras.values()), max(ras.values())))
worst = max((Ends[s] - 2 * ras[s], s) for s in Ends)
print('max End - 2*r_after = %d at s=%d  (need <= 8 given B2<=0)' % worst)
cl = fe.chain_levels
print('endgame chain levels >=2: n=%d  distinct=%s  max=%d'
      % (len(cl), sorted(set(q for _, q in cl))[:30],
         max(q for _, q in cl) if cl else 0))
from collections import Counter
print('level histogram:', dict(sorted(Counter(q for _, q in cl).items())))

# margin law on the walk: p_{i-1} > sp_i
t = 2
p = 4
minmarg = 10 ** 9
i = 0
while t // 2 < 10 ** 7:
    sp = v2_int(3 * t + 4)
    if p - sp < minmarg:
        minmarg = p - sp
        mm = (i, t, sp, p)
    L = ells[sp] if sp < N else 4
    a = a0big.get(sp, 1)
    e = 1 if L % 2 == 0 else 0
    t += 1 + L + e
    p += 2 + a + 2 * e
    i += 1
print('walk margin min p_{i-1}-sp_i = %d at %s' % (minmarg, mm))
json.dump({'a0': a0big, 'Endmax': max(Ends.values()),
           'worst': worst, 'minmarg': minmarg,
           'chain_levels': sorted(set(q for _, q in cl))},
          open(r'D:\math_cc\scratch\agentF_endgame_out.json', 'w'))
