"""V5: run verify_r8.py checks 5 and 5b, confirm the run counts 16896 / 28160,
and audit what those runs actually execute.

Enumeration counts (independent arithmetic):
  check5 run_all:  canonical r0 in 1..5 x 256 rho x 11 tails = 14080
                   glue 256 rho x 11 tails                     =  2816  -> 16896
  check5b run_lineage: 2 kapgen x 5 r0 x 256 rho x 11 tails    = 28160
Also: (i) instrument _Tm to count symbolic steps per run -- a glue start
returns at t=0 (final_match on [head]+tail vs tail succeeds immediately),
so the 2816 glue runs are no-ops; (ii) reproduce the PROOF.md secondary
variants: K=10 canonical r0 in 1..9 (9*1024*11 = 101376) and r0 in 6..8
canonical + lineage (3*256*11 + 2*3*256*11 = 8448 + 16896 = 25344).
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\work_r8')
sys.setrecursionlimit(100000)
import verify_r8 as V

t0 = time.time()
# ---------- count the enumerations ourselves ----------
n_can = 5 * (1 << 8) * 11
n_glue = (1 << 8) * 11
print('check5 enumeration: 5 r0 * 256 rho * 11 tails = %d canonical + %d glue = %d'
      % (n_can, n_glue, n_can + n_glue))
print('check5b enumeration: 2 kapgen * 5 r0 * 256 rho * 11 tails = %d'
      % (2 * 5 * (1 << 8) * 11))

# ---------- glue runs: do they execute any steps? ----------
steps = {'n': 0}
orig_Tm = V._Tm
def counting_Tm(L):
    steps['n'] += 1
    return orig_Tm(L)
V._Tm = counting_Tm
glue_results = set()
for rho in range(0, 256, 16):
    for tp in V.TemplateChecker(8).tails:
        r = V.TemplateChecker(8).run_glue(rho, tp)
        glue_results.add(tuple(x if not isinstance(x, tuple) else 'DEEP' for x in r[:2]))
print('glue-start probe (17 rho x 11 tails): distinct (ell, a) results =', glue_results)

# ---------- check5 ----------
V._Tm = counting_Tm
tmpl = V.TemplateChecker(KK=8)
steps['n'] = 0
t1 = time.time()
nr, nf = tmpl.run_all()
print('check5 run_all: ok=%d fails=%d(%s)  [%.1fs, %d _Tm steps executed]'
      % (nr, len(nf), nf[:2], time.time() - t1, steps['n']))
assert (nr, len(nf)) == (16896, 0), (nr, nf)

# ---------- check5b ----------
t1 = time.time()
nr2, nf2 = tmpl.run_lineage()
print('check5b run_lineage: ok=%d fails=%d(%s) new_classes=%s  [%.1fs]'
      % (nr2, len(nf2), nf2[:2], sorted(tmpl.new_classes), time.time() - t1))
assert (nr2, len(nf2)) == (28160, 0) and not tmpl.new_classes

# ---------- secondary variants from PROOF.md ----------
t1 = time.time()
okK10 = 0; failK10 = []
tc10 = V.TemplateChecker(KK=10)
for r0 in range(1, 10):
    for rho in range(1 << 10):
        for tp in tc10.tails:
            try:
                tc10.run_canonical(rho, r0, tp); okK10 += 1
            except (V.Undecided, V.Halt, V.MFail):
                failK10.append((r0, rho, tp))
print('K=10 canonical r0 in 1..9: %d runs (= 9*1024*11 = %d), fails=%d %s  [%.1fs]'
      % (okK10, 9 * 1024 * 11, len(failK10), failK10[:3], time.time() - t1))
t1 = time.time()
ok68 = 0; fail68 = []
tc8 = V.TemplateChecker(KK=8)
for r0 in (6, 7, 8):
    for rho in range(1 << 8):
        for tp in tc8.tails:
            try:
                tc8.run_canonical(rho, r0, tp); ok68 += 1
            except (V.Undecided, V.Halt, V.MFail):
                fail68.append(('can', r0, rho, tp))
# lineage part must run under run_lineage's zlike patch (accept {-2} mod 2^{K-1});
# calling run_canonical_gen without it spuriously fails (auditor's initial mistake).
Hm = 1 << (tc8.K - 1)
def zlike_lin(x):
    for eps, mod in ((0, tc8.Hp), (-1, tc8.Hp), (-2, Hm)):
        f = V._sub(x, V._C(eps))
        if all(a % mod == 0 for a in f[0]) and f[1] >= 0 and f[1] % mod == 0:
            return eps
    tc8.new_classes.add(x[1] % tc8.Hp)
    return 0
saved_z = tc8.zlike
tc8.zlike = zlike_lin
tc8.new_classes = set()
try:
    for kapgen in (0, 1):
        for r0 in (6, 7, 8):
            for rho in range(1 << 8):
                for tp in tc8.tails:
                    try:
                        tc8.run_canonical_gen(rho, r0, tp, kapgen); ok68 += 1
                    except (V.Undecided, V.Halt, V.MFail):
                        fail68.append(('lin', kapgen, r0, rho, tp))
finally:
    tc8.zlike = saved_z
print('r0 in 6..8 canonical+lineage: %d runs (= 3*256*11 + 2*3*256*11 = %d), fails=%d %s  [%.1fs]'
      % (ok68, 3 * 256 * 11 + 2 * 3 * 256 * 11, len(fail68), fail68[:3], time.time() - t1))
print('total elapsed %.1fs' % (time.time() - t0))
