"""[B] NT gates in actual S(J) words, J<=512 (Calendar(512) kernels): count a-steps with output >= j-1."""
import sys, json
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_ext_roots'))
from search_roots import Calendar
cal = Calendar(512); st = Counter(); ex = []
for J in range(5, 513):
    K = cal.kernels.get(J)
    if not K: continue
    w, ty = K['word'], K['types']; g = 0
    for i in range(len(w) - 1):
        if ty[i] == 'a' and w[i+1] >= w[i] - 1: g += 1
    st[g] += 1
    if g and len(ex) < 12: ex.append(dict(J=J, word=list(w), types=ty))
out = dict(gates_per_walk=dict(st), examples=ex)
HERE.joinpath('real_walks.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
print(dict(st)); [print(e) for e in ex[:8]]
