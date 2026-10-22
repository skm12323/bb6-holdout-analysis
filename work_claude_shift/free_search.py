"""Search small canonical walks that exhaust the precision of a tunable start class.
Start: chain j0 with x = 2^j0 * U (U a free odd 2-adic unit), defect d0 (0 after a root b-letter,
2 after a root a-letter).  Track x = A*U + B exactly; a step is FREE when v2(A) <= v2(B): its output
parameter can be made any m >= v2(A) by choosing U mod 2^(m+1-v2(A)).  Synthetic search; the
realisability of the tuned U by an actual fire is a separate question."""
import sys, json
from fractions import Fraction as F
from pathlib import Path
from layers import cal
from verify_shift import v2
from collections import Counter
HERE = Path(__file__).resolve().parent

def explore(j0, d0, U0=1, s=1, depth=12):
    """Depth-first over forced steps; returns list of (letters, free_step_info)."""
    a, b = F(1 << j0) * (1 << s), F(1 << j0) * U0      # x = a*V + b, U = U0 + 2^s V
    c, e = a, b + d0                                    # Theta = c*V + e  (defect d0)
    j = j0; letters = []; found = []
    for _ in range(depth):
        r = cal.crossing(j - 1)
        if not r['odd']: return found, letters, 'end'
        tau = r['time']
        if r['kind'] == 'a':
            a2, b2 = 2*c - a/2, 2*e + 3*tau - b/2; L = 'A'
        else:
            ratio = (r['head_ratio'] + 2*r['tail_ratio'])/2
            lam = r['head_lambda'] + 2*r['tail_lambda'] + 3
            a2, b2 = ratio*a, ratio*b + lam; L = 'B' if r['kind'] == 'b' else 'C'
        e = e + 3 + 3*tau
        va, vb = v2(a2), v2(b2)
        letters.append((L, j))
        if va <= vb:
            found.append(dict(letters=[l for l, _ in letters], chains=[q for _, q in letters], free_from=va))
            return found, letters, 'free'
        a, b, j = a2, b2, vb
        if j < 2: return found, letters, 'small'
    return found, letters, 'depth'

res = []; st = Counter()
for j0 in range(5, 400):
    for d0 in range(-12, 13):
        for U0, s in ((1, 1), (1, 2), (3, 2), (1, 3), (3, 3), (5, 3), (7, 3)):
            f, lt, how = explore(j0, d0, U0, s)
            st[how] += 1
            for q in f:
                q.update(j0=j0, d0=d0, U_mod=(U0, s), eps=2*(1 + len(q['letters'])) + 1)
                res.append(q)
res.sort(key=lambda q: q['eps'])
print(dict(st)); print(len(res))
for q in res[:15]: print(q)
HERE.joinpath('free_search.json').write_text(json.dumps(dict(stats=dict(st), found=res[:200]), indent=1), encoding='utf-8')
