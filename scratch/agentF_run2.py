"""agentF_run2.py -- trace the frame decomposition for selected levels."""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentF_lib import F_, excursion

for s in [5, 14, 15, 20, 30, 51]:
    eng = F_(use_cache=False, trace_levels={s})
    ell = excursion(s, eng)
    ev = __import__('agentF_lib').TRACE[s]
    E = sum(1 for e in ev if e['type'] == 'E')
    F = [e for e in ev if e['type'] == 'F']
    G = sum(1 for e in ev if e['type'] == 'g')
    print('=== level %d: ell=%d, |ev|=%d, E=%d, F=%d, G=%d, sum(1+ell_child)=%d'
          % (s, ell, len(ev), E, len(F), G, sum(1 + e['ell_child'] for e in F)))
    for e in ev:
        if e['type'] == 'F':
            print('  t=%3d FIRE  r=%2d sp=%2d a=%d ell_child=%3d margin=%2d Delta=%s'
                  % (e['t'], e['r'], e['sp'], e['a'], e['ell_child'], e['margin'],
                     e['Delta']))
        elif e['type'] == 'E':
            print('  t=%3d E     r=%2d' % (e['t'], e['r']))
        else:
            print('  t=%3d glue  r=%s canon=%s' % (e['t'], e['r'], e['canon']))
