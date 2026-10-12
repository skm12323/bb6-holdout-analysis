"""agentF_walk.py -- validate the universal walk against the naive engine.

Hypotheses to validate (for top frames s <= NS, and nested frames):
  H1 (clean Delta): at every fire of the MAIN phase (canonical r >= 2),
     d = 3t+1 exactly, hence q0 = 3H + 3t + 4 and sp = v2(3t+4) whenever
     margin v2(H) > v2(3t+4).
  H2 (fire times): fires occur at even t only; t=0,1 are E-macros (if r>=3
     resp r>=2); phases: t_{i+1} = t_i + 1 + ell(sp_i) + [ell(sp_i) even].
  H3 (r-dynamics): r_1 = s-5; r_{i+1} = r_i - (2 + a_i) - 2*[ell(sp_i) even];
     E-macros at odd t (when r >= 3), fires at even t while r >= 2.
  H4 (a-table): a_i = a(sp_i) depends only on sp.
  H5: endgame fires (r < 2 canonical / glue re-formations) and their levels.
"""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_lib import F_, excursion, STATS, TRACE


def v2_3t4(t):
    n = 3 * t + 4
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


NS = int(sys.argv[1]) if len(sys.argv) > 1 else 300

# --- collect from naive engine: every fire of the TOP frame of each level ---
topfires = {}   # s -> list of (t, sp, r, a, L, margin, Delta)
ends = {}       # s -> (ell, #E, #F, #G, tail-events)
for s in range(1, NS + 1):
    eng = F_(use_cache=False, trace_levels={s})
    ell = excursion(s, eng)
    ev = TRACE[s]
    E = sum(1 for e in ev if e['type'] == 'E')
    Fs = [e for e in ev if e['type'] == 'F']
    G = sum(1 for e in ev if e['type'] == 'g')
    topfires[s] = [(e['t'], e['sp'], e['r'], e['a'], e['ell_child'],
                    e['margin'], e['Delta']) for e in Fs]
    ends[s] = (ell, E, len(Fs), G)

# --- a-table ---
atable = {}
bad_a = []
for s, fl in topfires.items():
    for (t, sp, r, a, L, m, D) in fl:
        if r >= 2:
            if sp in atable and atable[sp] != a:
                bad_a.append((s, t, sp, atable[sp], a))
            atable[sp] = a
print('a-table (main-phase fires, s<=%d):' % NS,
      dict(sorted(atable.items())))
print('a-table conflicts:', bad_a[:10] or 'none')

# --- H1/H2/H3 walk check ---
ells = {s: ends[s][0] for s in ends}
bad_h = []
for s in range(6, NS + 1):
    fl = [f for f in topfires[s] if f[2] >= 2]
    if not fl:
        continue
    t_prev, r_prev = None, s - 5
    for idx, (t, sp, r, a, L, m, D) in enumerate(fl):
        if t % 2:
            bad_h.append(('odd fire time', s, t))
        if v2_3t4(t) != sp:
            bad_h.append(('sp != v2(3t+4)', s, t, sp, v2_3t4(t)))
        if D != 0:
            bad_h.append(('Delta != 0 at main fire', s, t, D))
        if m < 1:
            bad_h.append(('margin < 1', s, t, m))
        if r != r_prev:
            bad_h.append(('r mismatch', s, t, r, r_prev))
        # advance
        r_prev = r - (2 + a) - 2 * (1 if L % 2 == 0 else 0)
        t_prev = t
    # r-dynamics across consecutive fires, accounting for interleaved E's
    # is checked inside the loop via r_prev; also check gap formula
    for idx in range(len(fl) - 1):
        t0_, sp0, r0_, a0, L0 = fl[idx][0], fl[idx][1], fl[idx][2], fl[idx][3], fl[idx][4]
        t1_ = fl[idx + 1][0]
        if t1_ - t0_ != 1 + L0 + (1 if L0 % 2 == 0 else 0):
            bad_h.append(('gap', s, t0_, t1_, L0))
print('walk violations (H1-H3):', bad_h[:10] or 'none', 'total', len(bad_h))
