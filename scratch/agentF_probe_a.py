"""agentF_probe_a.py -- what determines the return count a at a fire?"""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_lib import F_, excursion, STATS, TRACE

NS = 300
rows = []
for s in range(6, NS + 1):
    eng = F_(use_cache=False, trace_levels={s})
    excursion(s, eng)
    ev = TRACE[s]
    for e in ev:
        if e['type'] == 'F' and e['Delta'] == 0 and e['t'] % 2 == 0:
            rows.append((s, e['t'], e['sp'], e['r'], e['a'], e['ell_child']))

# group by sp: list (a, r, s, t)
from collections import defaultdict
bysp = defaultdict(list)
for (s, t, sp, r, a, L) in rows:
    bysp[sp].append((a, r, s, t, L))
for sp in sorted(bysp):
    rs = sorted(set((a, r % 8) for (a, r, s, t, L) in bysp[sp]))
    rs2 = sorted(set((a, r) for (a, r, s, t, L) in bysp[sp]))
    print('sp=%2d  n=%4d  (a, r%%8) seen: %s   (a, r) min/max per a: %s'
          % (sp, len(bysp[sp]), rs,
             [(a, min(r for (aa, r, *_ ) in [(x[0], x[1]) for x in bysp[sp]] if aa == a),
               max(r for (aa, r, *_ ) in [(x[0], x[1]) for x in bysp[sp]] if aa == a))
              for a in sorted(set(x[0] for x in bysp[sp]))]))
# focus: sp=5 and sp=8 rows
for sp in (5, 8):
    print('--- sp=%d rows (a, r, s, t):' % sp,
          sorted(set((a, r) for (a, r, s, t, L) in bysp[sp])))
