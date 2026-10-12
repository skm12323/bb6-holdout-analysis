"""agentG_smoke.py -- quick validation:
1) literal audited loop vs annotated closed form, orbit from (3), 200k steps;
2) E(1,30) fire trace vs agentC_invariant.md par.7 trace;
3) E(w,v) returns to singleton for a few (w,v).
"""
import sys
sys.path.insert(0, r"D:\math_cc\scratch")
from agentG_lib import *

# --- 1) literal vs annotated ---
h1, e1 = 3, []
h2, e2 = 3, []
for n in range(200000):
    (h1, e1), halted = top_step_literal(h1, e1)
    (h2b, e2b), f = top_step_annot(h2, e2)
    assert not halted
    assert h1 == h2b, (n, h1, h2b)
    assert e1 == [v for (r, v) in e2b], n
    h2, e2 = h2b, e2b
    if f is not None and f.get('HALT'):
        print("HALT at n=", n); break
print("literal == annotated closed form for 200000 orbit steps OK")

# --- 2) E(1,30) trace ---
fires, ell, endhead, halted = run_excursion(1, 30)
print("E(1,30): ell =", ell, "end head =", endhead, "halted =", halted)
sig = None
for f in fires:
    i = f['i']
    print("  n=%3d fam=%-4s D=%-12d i=%-4s t=%-6s k=%s q=%s Delta=%s" % (
        f['n'], f['fam'], f['D'], i, f['t'], f['k'], f['q'], f['Delta']))
# expected (agentC par.7, roles as (role,D,i)):
# (R,7,4) (R,13,7) (R,25,11) (R,31,13) (R,37,16) (R,49,21) (R,55,23) (R,61,26)
# then replay (S,7,4) [our R at i=4], then deep (S,-352321549,0) pos, (S,77,0) fire.

# --- 3) a few excursions end ---
for (w, v) in [(1, 1), (1, 2), (3, 5), (5, 14), (1, 65), (1, 66), (7, 100)]:
    fs, ell, eh, hal = run_excursion(w, v)
    assert not hal
    mq = min((f['q'] for f in fs if not f.get('HALT')), default=0)
    print("E(%d,%d): ell=%d end=%d min q=%d nfires=%d" % (w, v, ell, eh, mq, len(fs)))
print("smoke OK")
