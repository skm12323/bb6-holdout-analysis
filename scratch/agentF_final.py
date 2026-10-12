"""agentF_final.py -- consolidated numbers for the report.

Computes over the universal walk (k < 10^7):
  (1) max B2 prefix for i >= 1 and i >= 4;
  (2) per-level s <= 5000: i*(s), B2(i*(s)), End(s), r_after(s), and the
      master identity residuals;
  (3) spike-cycle stats: cycles with Sum dk != 16; min Sum dp among
      Sum dk == 16 cycles; min cycle B2 sum;
  (4) threshold for i*(s) >= 4; exact cut positions.
"""
import sys, json
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_fast import FastEll, v2_int

fe = FastEll()
fe.a0.update({1: 1, 2: 0, 3: 1, 4: 0, 5: 2, 6: 1, 7: 0, 8: 2,
              9: 0, 10: 1, 11: 0, 12: 2, 13: 0, 14: 3})
N = 5000
for s in range(1, N + 1):
    fe.ell_of(s)
ells = fe.ell

KCUT = 10 ** 7
t = 2
ph = []
while t // 2 < KCUT:
    sp = v2_int(3 * t + 4)
    if sp not in fe.a0:
        fe.a0_of(sp)
    L = ells[sp]
    e = 1 if L % 2 == 0 else 0
    ph.append((t, sp, L, e, fe.a0[sp]))
    t += 1 + L + e

B2s = []
B2 = 0
for (t, sp, L, e, a) in ph:
    B2 += 2 * sp - 3 - 2 * a - 3 * e
    B2s.append(B2)
print('(1) max B2 prefix i>=1: %d  (i=%d);  i>=4: %d  (i=%d);  i>=10: %d'
      % (max(B2s[0:]), 1 + B2s.index(max(B2s[0:])),
         max(B2s[3:]), 4 + B2s[3:].index(max(B2s[3:])),
         max(B2s[9:])))

# (2) per-level replay
istars = {}
for s in range(3, N + 1):
    r = s - 1
    if r - 2 < 2:
        continue
    r -= 4
    i = 0
    while True:
        (tt, sp, L, e, a) = ph[i]
        a_eff = a if r >= 3 else min(a, 1)
        if r - 2 - a_eff >= 2:
            r -= 2 + a_eff
            if e:
                if r - 2 >= 2:
                    r -= 2
                else:
                    istars[s] = i + 1   # ended at separator E of phase i
                    break
            i += 1
            continue
        istars[s] = i + 1
        break
th = min(s for s in istars if istars[s] >= 4)
print('(4) smallest s with i*(s) >= 4: %d ; i*(s) values 7..30: %s'
      % (th, [istars[s] for s in range(7, 31)]))
need = [(s, B2s[istars[s] - 1]) for s in istars]
mn = min((b, s) for (s, b) in need if s >= th)
print('(2) min B2(i*(s)) over s with i*>=4: %d at s=%d' % (mn[0], mn[1]))
bad = [s for s in istars if s >= th and B2s[istars[s] - 1] > -3]
print('    s >= %d with B2(i*) > -3: %s' % (th, bad[:10] or 'none'))

# (3) spike stats, clean
kprev = None
dks = dps = 0
non16 = []
min_dp16 = 10 ** 9
cnt16 = 0
for (t, sp, L, e, a) in ph:
    k = t // 2
    dk = (1 + L + e) // 2
    dp = 2 + a + 2 * e
    if sp >= 5:
        if kprev is not None:
            if dks == 16:
                cnt16 += 1
                min_dp16 = min(min_dp16, dps)
            else:
                non16.append((kprev, k, dks, dps))
        kprev, dks, dps = k, 0, 0
    dks += dk
    dps += dp
print('(3) spike cycles: %d with Sum dk == 16 (min Sum dp among them: %d); '
      '%d with Sum dk != 16: %s'
      % (cnt16, min_dp16, len(non16), non16[:5] or ''))
