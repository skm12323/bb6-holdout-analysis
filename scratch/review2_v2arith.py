"""Follow-up: distribution of H forms at canonical fires; plus V2 pure arithmetic.

V2 claim: for canonical states with H divisible by 2^11 (H = 3w*2^j, j >= 11),
A+2b+3 = 3H+d+3 (b = H, r >= 1), and v2(3H+d+3) >= 8  <=>  v2(d+3) >= 8
(<=> d = -3 mod 256).  Pure arithmetic: only needs 256 | 3H, i.e. v2(H) >= 8
(w odd).  We brute-force it and locate the exact j-boundary.
"""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from review2_engine import run_tracked, excursion_start, v2

# ---------- part 1: H-form stats at fires (from the V1 scan range) ----------
Hform = {}
def sink(kind, info):
    if kind == 'fire':
        H = info['H']; jH = v2(H)
        odd = H >> jH
        key = (jH, odd % 6 == 3)
        Hform[key] = Hform.get(key, 0) + 1

for w in (1, 3, 5, 7):
    for v in range(1, 401):
        run_tracked(excursion_start(w, v), 3 * w, 1, -1, v, sink, 200000)

bad_hi = {k: c for k, c in Hform.items() if (not k[1]) and k[0] >= 8}
print('fire-state H: (v2(H), is_3w_form) -> count; entries with v2>=11:',
      {k: c for k, c in sorted(Hform.items()) if k[0] >= 11})
print('H not of form 3*odd*2^j AND v2(H) >= 8:', bad_hi)
tot_bad = sum(c for k, c in Hform.items() if not k[1])
print('total non-3w-form H at fires:', tot_bad, 'of', sum(Hform.values()))

# ---------- part 2: pure arithmetic ----------
def check(j, wlo=1, whi=20001, dlo=-4096, dhi=70000):
    H = 3 * wlo * (1 << j)
    bad = 0
    # exhaustive over d residues mod 2^13 and several w
    for w in list(range(wlo, 301, 2)) + [whi]:
        H = 3 * w * (1 << j)
        for d in range(dlo, dhi):
            q0 = 3 * H + d + 3
            lhs = (q0 % 256 == 0)        # v2(q0) >= 8
            rhs = ((d + 3) % 256 == 0)   # v2(d+3) >= 8
            if lhs != rhs:
                bad += 1
                if bad < 4:
                    print('   counterexample j=%d w=%d d=%d q0=%d' % (j, w, d, q0))
    return bad

print('V2 arithmetic: v2(3H+d+3)>=8 <=> (d+3)%256==0')
for j in (11, 12, 13, 14):
    bad = check(j)
    print('  j=%d: exhaustive d in [-4096, 70000), w in 300 odd values + big: %d mismatches' % (j, bad))
# boundary: where does it break?
for j in (7, 8, 9, 10):
    bad = check(j, wlo=1, whi=101, dlo=-2048, dhi=20000)
    print('  j=%d: %d mismatches (expected %s)' % (j, bad, 'MANY' if j < 8 else '0'))
