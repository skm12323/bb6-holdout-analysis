"""Exact NT margins at chains j>=19: an integer class delta can be an NT gate only if
|3k_j+delta| >= 2^(j-2) (and nonzero).  M(j) := 2^(j-2)-3k_j-1 (positive side), M-(j) := 2^(j-2)+3k_j-1."""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_ext_roots'))
from search_roots import Calendar
cal = Calendar(512)
P = lambda n: 2*math.ceil(math.log2(6*n*n+5))**2 + 1345
rows = []
for j in range(19, 400):
    r = cal.crossing(j-1)
    if r['odd'] and r['kind'] == 'a':
        k = r['time']//2; rows.append((j, k, 2**(j-2)-3*k-1))
mstar = min(rows, key=lambda t: t[2])
lemma_ok = all(81*(3*k+2048) < 2**(j-2) for j, k, _ in rows)
assert lemma_ok
assert all(cal.crossing(j-1)['kind'] != 'a' or not cal.crossing(j-1)['odd'] for j in (19, 20, 21))
# CLOCK bound beyond 400: 3k <= 1.5 (j-1) P(j-1)
clock_ok = all(2*2**(j-2) - 3*(j-1)*P(j-1) - 2 > 2*mstar[2] for j in range(400, 2000))
print('odd-a chains 19..399:', len(rows)); print('first rows', rows[:6]); print('min margin', mstar, 'clock beyond 400 larger:', clock_ok)
HERE.joinpath('margins.json').write_text(json.dumps(dict(rows=rows[:40], min_margin=mstar, lemma_rank4_h2048_ok=lemma_ok, clock_beyond_400_larger=clock_ok), indent=1), encoding='utf-8')
