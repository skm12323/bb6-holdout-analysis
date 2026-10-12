"""AUDITOR 1 / extra -- corroborate two PROOF.md section-2 side claims that
verify_r8.py's __main__ does NOT execute (K=10 variant; r0 in 6..8 variant).
Uses the audited module's own engine (import with -B: no bytecode written).
Run: python -B review1_extra.py
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\work_r8')
import verify_r8 as V

# ---- (1) K = 10 variant, sampled residues (their claim: 101376 runs, 0 failures;
#          full scan too slow for the audit; sample 60 of 1024 rho residues) ----
t0 = time.time()
tc = V.TemplateChecker(KK=10)
rhos = sorted(set((37 * i) % 1024 for i in range(60)))
ok, fails = 0, []
for r0 in (1, 2, 3, 4, 5):
    for rho in rhos:
        for tp in tc.tails:
            try:
                tc.run_canonical(rho, r0, tp); ok += 1
            except (V.Undecided, V.Halt, V.MFail) as e:
                fails.append((r0, rho, tuple(tp), repr(e)))
for rho in rhos:
    for tp in tc.tails:
        try:
            tc.run_glue(rho, tp); ok += 1
        except (V.Undecided, V.Halt, V.MFail) as e:
            fails.append((rho, tuple(tp), repr(e)))
print('extra1 K=10 (sampled %d/1024 rho residues, r0=1..5, 11 tails + glue): '
      'runs=%d fails=%d [%.0fs]' % (len(rhos), ok, len(fails), time.time() - t0))
if fails:
    print('  first fails:', fails[:5])

# ---- (2) r0 in 6..8 at K=8, FULL scan: canonical (8448) + lineage generators
#          (2 x 8448 = 16896) = 25344 runs, matching PROOF.md's count ----
t0 = time.time()
tc8 = V.TemplateChecker(KK=8)
ok1, fails1 = 0, []
for r0 in (6, 7, 8):
    for rho in range(256):
        for tp in tc8.tails:
            try:
                tc8.run_canonical(rho, r0, tp); ok1 += 1
            except (V.Undecided, V.Halt, V.MFail) as e:
                fails1.append(('top', r0, rho, tuple(tp), repr(e)))
print('extra2a r0=6..8 canonical K=8 full: runs=%d fails=%d [%.0fs]'
      % (ok1, len(fails1), time.time() - t0))

K, Hp, Hm = 8, 1 << 11, 1 << 7
new_classes = set()


def zlike_lin(x):
    for eps, mod in ((0, Hp), (-1, Hp), (-2, Hm)):
        f = V._sub(x, V._C(eps))
        if all(a % mod == 0 for a in f[0]) and f[1] >= 0 and f[1] % mod == 0:
            return eps
    new_classes.add(x[1] % Hp)
    return 0


tc8.zlike = zlike_lin
ok2, fails2 = 0, []
for kapgen in (0, 1):
    for r0 in (6, 7, 8):
        for rho in range(256):
            for tp in tc8.tails:
                try:
                    tc8.run_canonical_gen(rho, r0, tp, kapgen); ok2 += 1
                except (V.Undecided, V.Halt, V.MFail) as e:
                    fails2.append((kapgen, r0, rho, tuple(tp), repr(e)))
print('extra2b r0=6..8 lineage K=8 full (both kap generators): runs=%d fails=%d '
      'new residue classes=%s' % (ok2, len(fails2), sorted(new_classes)))
print('extra2 total runs = %d (PROOF.md claims 25344)' % (ok1 + ok2))
if fails1 or fails2:
    print('  first fails:', (fails1 + fails2)[:5])
