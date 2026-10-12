"""agentF_balance.py -- the universal walk, its balance, and the spike laws.

Walk (level-s frame main phase, from validated model):
  phases i = 1, 2, ...:  fire i at time t_i (even), level sp_i = v2(3 t_i + 4),
  child length L_i = ell(sp_i), separator E iff L_i even (e_i in {0,1}),
  return count a_i = a0(sp_i) (r >= 3) / min(a0(sp_i),1) (r = 2),
  time cost   c_i = 1 + L_i + e_i          (dk_i = c_i / 2),
  r-cost     dp_i = 2 + a_i + 2 e_i.
  k_i := t_i / 2 advances by dk_i; p_i (cumulative r-consumption from r_1
  on, plus 4) advances by dp_i.

Master identity to check per level s:
  ell(s) - 2s = Sum_{i<=i*}(L_i - 3 - 2 a_i - 3 e_i) + End(s) - 2 r_after - 7.

Spike laws (agent B; independent re-derivation here):
  spikes = fires with j >= 5 at k = 16m+10; between consecutive spikes
  Sum dk = 16 exactly, Sum dp >= 22.
"""
import sys, json
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_fast import FastEll, v2_int

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
KCUT = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 7

fe = FastEll()
fe.a0.update({1: 1, 2: 0, 3: 1, 4: 0, 5: 2, 6: 1, 7: 0, 8: 2,
              9: 0, 10: 1, 11: 0, 12: 2, 13: 0, 14: 3})
for s in range(1, N + 1):
    fe.ell_of(s)
ells = fe.ell


def phases():
    """Generate the universal phase stream (t, sp, L, e, a) for r large."""
    t = 2
    r = 10 ** 9        # effectively unbounded r
    while t / 2 < KCUT:
        sp = v2_int(3 * t + 4)
        if sp not in fe.a0:
            fe.a0_of(sp)
        L = ells[sp]
        a = fe.a0[sp]
        e = 1 if L % 2 == 0 else 0
        yield (t, sp, L, e, a)
        t += 1 + L + e
        r -= 2 + a


# ---- walk replay for each level s; check master identity + collect stats ----
ph = list(phases())            # universal phase table
print('phases generated: %d (k up to %d)' % (len(ph), ph[-1][0] // 2))

# index by fire order; for level s replay:
#  t=0 E, t=1 E, then phases while post-event r >= 2.
viol = []
maxB2 = (0, 0)   # (B2 value, i)
trueB = []
B2s = []
B2 = 0
Bt = 0
for i, (t, sp, L, e, a) in enumerate(ph):
    Bt += L - 3 - 2 * a - 3 * e
    B2 += 2 * sp - 3 - 2 * a - 3 * e
    trueB.append(Bt)
    B2s.append(B2)
    if B2 > maxB2[0]:
        maxB2 = (B2, i + 1)
print('max prefix B2 = %d at fire #%d;  B2(end)=%d; Btrue(end)=%d'
      % (maxB2[0], maxB2[1], B2s[-1], trueB[-1]))

# master identity check for every s <= N
# replay: r = s-1, t = 0: E; t=1: E; then use phases
ph_idx = 0
bad_id = []
Ends = {}
for s in range(3, N + 1):
    r = s - 1
    # t=0 E
    if r - 2 < 2:
        continue
    r -= 2
    # t=1 E
    if r - 2 < 2:
        continue
    r -= 2
    t = 2
    sum_bal = 0
    r_after = r
    i = 0
    main = 0
    while True:
        (tt, sp, L, e, a) = ph[i]
        assert tt == t, ('phase desync', s, t, tt)
        a_eff = a if r >= 3 else min(a, 1)
        if r - 2 - a_eff >= 2:
            sum_bal += L - 3 - 2 * a_eff - 3 * e
            r -= 2 + a_eff
            t += 1 + L
            if e:
                # separator E at odd t
                if r - 2 >= 2:
                    r -= 2
                    t += 1
                else:
                    # E ends main: main ends after this E
                    main = t + 1
                    r_after = r - 2
                    t += 1
                    break
            i += 1
            continue
        else:
            # fire ends main; no separator E is executed
            sum_bal += L - 3 - 2 * a_eff
            r_after = r - 2 - a_eff
            main = t + 1 + L
            break
    End = ells[s] - main
    lhs = ells[s] - 2 * s
    rhs = sum_bal + End - 2 * r_after - 8
    Ends[s] = End
    if lhs != rhs:
        bad_id.append((s, lhs, rhs, main, End, r_after))
print('master identity violations (s<=%d): %s' % (N, bad_id[:5] or 'none',
                                                  ))
print('End(s): max=%d at %s' % (max(Ends.values()),
                                [s for s in Ends if Ends[s] == max(Ends.values())][:8]))
# note: r_after recorded after final event incl. separator-E handling

# ---- spike laws ----
# spikes: fires with j >= 5, i.e. v2(3k+2) >= 4, k = t/2
kprev = None
dks = 0
dps = 0
cyc = []
spike_bad = []
mincycB2 = (10 ** 9, 0)
B2run = 0
ncycles = 0
for (t, sp, L, e, a) in ph:
    k = t // 2
    dk = (1 + L + e) // 2
    dp = 2 + a + 2 * e
    B2run += 2 * sp - 3 - 2 * a - 3 * e
    if sp >= 5:
        if kprev is not None:
            cyc.append((kprev, k, dks, dps, B2run))
            if not (dks == 16 and dps >= 22):
                spike_bad.append((kprev, k, dks, dps))
            if B2run < mincycB2[0]:
                mincycB2 = (B2run, kprev)
            ncycles += 1
        kprev = k
        dks = 0
        dps = 0
        B2run = 0
    dks += dk
    dps += dp
print('spike cycles checked: %d  violations: %s' % (ncycles, spike_bad[:5] or 'none'))
print('min per-cycle B2 sum: %d (at k=%d)' % mincycB2)
print('min per-cycle dp sum: %d' % min(c[3] for c in cyc))
# k vs p law
mx = 0
for idx, (t, sp, L, e, a) in enumerate(ph[:200000]):
    k = t // 2
    pass
p = 4
kmax_ratio = (0, 0)
pval = 4
for idx, (t, sp, L, e, a) in enumerate(ph):
    pval += 2 + a + 2 * e
    if idx > 20 and pval > 0 and (t // 2) / pval > kmax_ratio[0]:
        kmax_ratio = ((t // 2) / pval, pval)
print('max k/p over walk: %.4f at p=%d' % kmax_ratio)

# ---- asymptotic drift of B2 ----
for i0 in (100, 1000, 10000, 100000, 1000000):
    if i0 < len(B2s):
        # least eps such that B2(i) <= -eps*i for all i >= i0 in range
        eps = min((B2s[i] / -i) for i in range(i0, len(B2s), max(1, len(B2s) // 400000)))
        print('B2(i) <= %.4f * (-i) for all sampled i >= %d' % (eps, i0))
json.dump({'B2s_last': B2s[-1], 'phases': len(ph), 'maxB2': maxB2,
           'Endmax': max(Ends.values()), 'mincycB2': mincycB2,
           'kmax_ratio': kmax_ratio},
          open(r'D:\math_cc\scratch\agentF_balance_out.json', 'w'))
