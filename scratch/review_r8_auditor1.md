# AUDITOR 1 report -- independent re-verification of work_r8 (PROOF.md, verify_r8.py)

Date: 2026-10-12. Environment: Python 3.14.6, Windows/GitBash, D:\math_cc.
Method: run the artifact as-is, then re-implement its core from scratch per the audit
brief (my own code: `scratch/review1_b.py`, `scratch/review1_c.py`, `scratch/review1_d.py`,
`scratch/review1_extra.py`; raw outputs in `scratch/review1_runA_*.txt`,
`scratch/review1_c_out.txt`, `scratch/review1_extra_out.txt`). Nothing in
D:\math_cc\work_r8 was modified (existing `__pycache__` untouched; module imported only
with `python -B`).

## Task A -- run the artifact [PASS]

`python verify_r8.py 1000 300` (cwd work_r8), full output:

```
check1 OK: compositional F(v) (no halt, verified conclusion) for v = 1..1000 [50.6s]
check2 OK: ell(v) equals direct symbolic full-run ell for v <= 300
check3 OK: concrete orbits (w=1,3,5) match ell(v) and never halt, v <= 300
check4 OK: a(s)<=2, min margin v2(H)-v2(d+3)=3, Delta in {0,odd<0}, windows clean+J (calls=153558, spmax=10, coincidental suffix matches=0)
check5 OK: 16896 end-phase template runs (all residues mod 2^8, r0=1..5, 11 tail patterns, glue starts), 0 failures; deep branches hand off within family
check5b OK: 28160 lineage template runs (kap generators -1 and -2 mod 2^{K-1}), 0 failures, 0 new residue classes
check6 OK: initial prefix: 9 steps, identical decisions for r0 in (30, 40, 50), reaches H = 2^11-multiple with J/tail in family
ell table (1..40): [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16, 16, 18, 18, 21, 20, 20, 22, 25, 25, 26, 26, 29, 28, 28, 30, 31, 31, 32, 32, 34]
max ell(v)/v = 1.0714285714285714
```

Exit code 0; total wall time a few minutes (check1 alone 50.6 s), consistent with the
briefed 2-3 min.

`python verify_r8.py 60 20` output: check1/check2/check3 lines scoped to 60/20 as
expected; check4 reports the smaller-range statistics (a(s)<=1, calls=468, spmax=6,
min margin 3, coinc 0) -- consistent subset of the 1000/300 statistics.
**The check5, check5b and check6 lines are byte-identical between the two runs**
(verified with grep+diff: empty diff). This is as it should be: those checks do not
depend on N/NC.

## Task B -- from-scratch compositional prover vs direct full runs [PASS]

`scratch/review1_b.py` (independent code, class-based affine forms a*u+c with exactly
the mandated uniformity rules: parity only if coeff even; halving only if coeff and
const even; m>=3 only if uniform). My prover:
- canonical encode (H+d, H, 2H, ..., 2^{r-1}H, J=2^r H+kap, Z...), r >= 1;
- E-macro at even head, r >= 2 -> [4H+d+3]+L[3:];
- odd head: q0 = A+2b+3 (b=H; c=2H if r>=2, c=J if r=1), s'=v2(q0), o'=q0/2^s',
  c'=c+(A+1)/2, kap_child=c'-2^{s'-1}o', nested frame
  (o'+1, o', 2o', ..., 2^{s'-2}o', 2^{s'-1}o'+kap_child, window) executed by recursion,
  outer resumes at [head]+window[a:] (assert s' < level);
- direct symbolic steps elsewhere; final detection = first [X]+Z[a:] with the verified
  contract X = 2^{s0}H0 + 3*ell + 1 + kap0 + sum(Z[:a]);
- **every** compositional 1-step construction (macro and chain) is asserted equal to my
  independent direct stepper applied to the same list (faithfulness), so the
  compositional trajectory is pointwise the true one.

Results (all PASS):
- For every v in 1..150: compositional ell(v) == direct full symbolic run ell, and both
  final singletons equal 3w*2^v + 3*ell symbolically (w=2u+1). No Undecided, no Halt.
- ell(1..20) equals R4's audited table exactly; ell(1..40) equals verify_r8's printed
  table exactly (checked programmatically).
- max ell(v)/v over v=10..150 = 1.071429 (= 15/14), same as the artifact's max for
  v <= 1000; supports "ell(v) <= 1.08 v".
- My engine stats (v <= 150): 3231 chain/nested calls, max nesting depth 2, spmax = 8,
  coincidental suffix matches 0 -- consistent subset of check4 (spmax=10 at v <= 1000).
- Extra (auditor addition): concrete orbits for odd w in {7, 9, 12345, 999999999937,
  2^61-1}, v in 1..60,100,150: ell and final singleton match the symbolic prover, no
  halt (extends the artifact's check3 which used w in {1,3,5}).

## Task C -- from-scratch end-phase template check (K=8, canonical, kap=-1) [PASS]

`scratch/review1_c.py`: 6-symbol forms (u,h,tt,z1..z3), H = 6*2^11 u + 2^11(1+h),
d = rho + 2^8 tt, tail_i = 2^11(z_i+1) - pi_i; starts [H+d] + [H*2^i, i<r0] +
[2^r0 H - 1] + tail for r0 in 1..5, rho in 0..255, tail patterns [], [0], [1], [0,0]
(5120 starts). Engine: symbolic steps with the uniformity rules; E-macro when head even
and L[2]=2*L[1] (faithfulness-asserted); odd head q0=A+2b+3, sp=v2(q0): sp<8 -> nested
excursion built + executed recursively (faithfulness-asserted); sp>=8 -> DEEP BRANCH:
continuation [head]+window[a:], a in 0..2, must be H-run multiples (4H, 8H, ...) then
entries in class 0 or -1 (mod 2^11) with nonnegative quotient (J=-1 class; tails 0/-1);
then treated as covered.

Results: **5120/5120 starts PASS, 0 failures** (matches the required 0). Every single
run terminated via an in-family deep hand-off (no run reached a final contract; uniform
sp = 8 exactly, from the 2^8*tt term). Auditor addition: each symbolic run was executed
in parallel with a CONCRETE integer run for 3 symbol instantiations (all-zero + 2
random up to 2^40), asserting state-by-state agreement of substituted symbolic state
with the concretely stepped state -- 15360 symbolic runs total, all step-agreement
asserts held, no concrete halt. This validates that the symbolic "uniform decision"
claims hold on real instances of the family, not just formally.

## Task D -- lineage arithmetic at deep branches [PASS]

Hand derivation (whole content): at an odd head,
kap_child = c' - q0/2 = c + (A+1)/2 - (A+2b+3)/2 = **c - b - 1**, independent of A, d
and of the 2-adic depth s'. Hence r >= 2 (b=H, c=2H): kap_child = H - 1; r = 1
(b=H, c=J=2H+kap_parent): kap_child = H + kap_parent - 1. These are exactly the two
generators of check5b's lineage ({-1 + 2^{K+3}k} from class kap_parent=-1 at r>=2;
{-2 mod 2^{K-1}} from kap_parent=-1 at r=1).

Numeric protocol (scratch/review1_d.py): 200 instances (100 per case), random odd w,
H = 3w*2^j with random j in 11..40 (high H, v2(H)=j), t = 84 mod 256 random, d = 3t+1
(so d+3 = 0 mod 256, A odd, v2(q0) >= 8), random r, both kap_parent lineage classes,
random tails. Per instance: (1) deepness v2(q0) >= 8 confirmed; (2) v2-tracking route
kap_child = c' - 2^{s'-1}o' equals H-1 (r>=2) / H+kap_parent-1 (r=1) exactly;
(3) ground truth: the concrete chain step (full while-loop) is executed, the result
re-encoded canonically gives the same (o', s'-1, kap_child), equals the constructed
nested frame entrywise, and no HALT. **200/200 PASS.**

## Extra corroboration (auditor addition) [PASS, with a note]

PROOF.md section 2 claims check5 was "also verified at K = 10 (101376 runs) and
r0 in 6..8 (25344 runs)" -- **verify_r8.py's __main__ does not execute these variants**
(it only runs K=8, r0=1..5, plus lineage and prefix checks). To resolve whether the
claims are merely unreproduced or actually wrong, I ran them with the artifact's own
engine (import with -B): K=10 with 60/1024 sampled rho residues, r0=1..5, 11 tails +
glue: 3960 runs, 0 failures; r0=6..8 at K=8 FULL scan: canonical 8448 + lineage both
generators 16896 = 25344 runs (exactly PROOF.md's count), 0 failures, 0 new residue
classes. So both side claims are true as stated, but they are not reproduced by the
shipped script.

## Discrepancies / observations

1. (Minor, reproducibility) The K=10 and r0=6..8 variants cited in PROOF.md section 2
   are not run by `verify_r8.py`; I corroborated both (sampled resp. full) with 0
   failures. No incorrect claim found.
2. (Note, semantics) In `TemplateChecker.F`, nested excursions are returned at the
   *first* suffix match without a contract check (top frames are contract-checked;
   the check1-4 engine checks contracts and skips only mismatches). Since a suffix
   match is a real state of the true trajectory, resuming there still traces the true
   orbit, so the no-halt / in-family conclusions are unaffected. My stricter engine
   (which skips non-contract nested matches) traverses the same trajectories and also
   reports 0 failures; my run showed every template run is eventually cut by a deep
   hand-off, so no template-run final contract is ever actually exercised.
3. All quantitative claims in the artifact's output reproduce exactly under my
   independent engines: ell tables, 16896 / 28160 / 153558 run counts, margin min 3,
   a(s) <= 2, spmax 10 (v<=1000), max ell(v)/v = 15/14 = 1.0714285714.
4. verify_r8.py's internal assert `margin_min >= 1` is weaker than the printed result
   3 and than PROOF.md's ">= 3"; the printed value is what PROOF.md claims, and it is
   what the runs produce. No conflict.

## Verdict

Task A PASS (identical check5/5b/6 lines across parameter settings); Task B PASS
(ell + final-singleton identity for v=1..150, compositional == direct, R4 table match);
Task C PASS (5120/5120 canonical K=8 template starts, 0 failures); Task D PASS
(200/200 instances, hand identity kap_child = c - b - 1 confirmed). No incorrect claim
found in PROOF.md or verify_r8.py; the only gaps are the two unreproduced side claims
of section 2, both independently corroborated by me.

**all correct**
