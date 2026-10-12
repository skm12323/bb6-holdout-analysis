"""agentG_dbg.py -- full step trace of E(1,30) to compare with agentC par.7."""
import sys
sys.path.insert(0, r"D:\math_cc\scratch")
from agentG_lib import *

head, ents = make_E(1, 30)
print("step  headmod  queue front (role,D,i) style")
for n in range(40):
    # current position coordinates: e1 = ents[0] if any
    if ents:
        (r0, v0) = ents[0]
        sig = v0 if r0 in ('R', 'S') else v0 + 1
        D = head - sig
        i = v2(sig) if sig > 0 else 0
        print("n=%2d  A%2d  (%s,%d,%d)%s" % (n, head % 2, r0, D, i, " FIRE" if head % 2 else ""))
    else:
        print("n=%2d  A%2d  EMPTY" % (n, head % 2))
    (head, ents), f = top_step_annot(head, ents)
    if f is not None:
        if f.get('HALT'):
            print("HALT"); break
    if not ents:
        print("n=%2d singleton head=%d" % (n + 1, head))
        break
