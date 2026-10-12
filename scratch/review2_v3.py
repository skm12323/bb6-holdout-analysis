"""V3 boundary scan.

Canonical starts: [H+d, H, 2H, ..., 2^{r0-1}H, J=2^{r0}H - 1]  (kap = -1, Z empty),
d = rho + 256*tt, rho = 0..255, r0 in 1..6, H = 3w*2^j, w in {1,3}, j in {11,12,13},
tt in {0,1,2}.  Run the CONCRETE dynamics to the excursion end (single entry).
Check: (i) no HALT, (ii) terminates, (iii) the macro-event shape (sequence of
E / C(level) / G steps) is a function of (rho, r0) alone -- compared across
(w, j) for each fixed tt (primary, per the claim) and across tt (secondary).
Shape-with-returns (E/C/G interleaved with ('R',a) pops) compared as a
stronger secondary variant.
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
from review2_engine import run_tracked, v2

def one_run(L0, H, d, r0, cap=30000):
    steps = []
    def sink(kind, info):
        if kind == 'step':
            steps.append(info['cls'])
        elif kind == 'pop':
            steps.append(('R', info['a']))
    res = run_tracked(L0, H, d, -1, r0 + 1, sink, cap)
    return res, tuple(steps)

def build(H, d, r0):
    return [H + d] + [H << i for i in range(r0)] + [(H << r0) - 1]

t0 = time.time()
groups_mismatch = []        # (r0, rho, tt) with differing shapes across (w,j)
groups_mismatch_ext = []
halt_list = []
timeout_list = []
contract_fail = []
nrun = 0
tt_mismatch = []            # secondary: shape differs across tt at fixed (r0, rho)
maxlen = 0
for r0 in range(1, 7):
    for rho in range(256):
        shapes_by_tt = {}
        for tt in (0, 1, 2):
            d = rho + 256 * tt
            shapes = {}
            exts = {}
            for w in (1, 3):
                for j in (11, 12, 13):
                    H = 3 * w * (1 << j)
                    L0 = build(H, d, r0)
                    res, tr = one_run(L0, H, d, r0)
                    nrun += 1
                    maxlen = max(maxlen, len(tr))
                    if res['end'] == 'halt':
                        halt_list.append((r0, rho, tt, w, j))
                        continue
                    if res['end'] == 'timeout':
                        timeout_list.append((r0, rho, tt, w, j))
                        continue
                    if res['end'] == 'done':
                        # root contract: final head = 2^{r0+1} H + d + 3*ell - 1
                        exp = (H << (r0 + 1)) + d + 3 * res['steps'] - 1
                        if res['head'] != exp:
                            contract_fail.append((r0, rho, tt, w, j, res['head'], exp))
                    base = tuple(x for x in tr if not (isinstance(x, tuple) and x[0] == 'R'))
                    shapes.setdefault(base, []).append((w, j))
                    exts.setdefault(tr, []).append((w, j))
            if len(shapes) > 1:
                groups_mismatch.append((r0, rho, tt, [len(k) for k in shapes]))
            if len(exts) > 1:
                groups_mismatch_ext.append((r0, rho, tt))
            shapes_by_tt[tt] = next(iter(shapes)) if shapes else None
        vals = set(x for x in shapes_by_tt.values() if x is not None)
        if len(vals) > 1:
            tt_mismatch.append((r0, rho, [None if shapes_by_tt[t] is None else len(shapes_by_tt[t]) for t in (0, 1, 2)]))
    print('  r0=%d done [%.1fs]' % (r0, time.time() - t0), file=sys.stderr)

print('=== V3 boundary scan ===')
print('runs: %d, max trace length: %d' % (nrun, maxlen))
print('halts: %d %s' % (len(halt_list), halt_list[:5]))
print('timeouts: %d %s' % (len(timeout_list), timeout_list[:5]))
print('root-contract failures: %d %s' % (len(contract_fail), contract_fail[:3]))
print('(w,j)-shape mismatches (primary claim): %d %s' % (len(groups_mismatch), groups_mismatch[:10]))
print('(w,j)-shape-with-returns mismatches (stronger): %d %s' % (len(groups_mismatch_ext), groups_mismatch_ext[:10]))
print('tt-variation mismatches (secondary, across tt at fixed (r0,rho)): %d %s' % (len(tt_mismatch), tt_mismatch[:15]))
print('elapsed %.1fs' % (time.time() - t0))
