# Agent E — corrected end-phase template route ((L-sum) + (L-coverage))

Scripts (all in `scratch/`, nothing else in `D:\math_cc` modified): `agentE_lib.py`
(shared machinery), `agentE_task1.py`, `agentE_task2.py`, `agentE_task3.py`;
outputs `agentE_R.json`, `agentE_task2out.json`, `agentE_task3out.json`.
Python 3 stdlib only; every run < 1 min; peak footprint a few MB.

`agentE_lib.py` copies verify_r8's single-symbol core, multi-symbol core and
`TemplateChecker` (as `TemplateCheckerE`) with the review-mandated hardening:
**F3** chain precondition o' >= 3 (nonnegative coefficients, const >= 3)
enforced at every sp < K chain and checked+logged at deep branches;
**F4** contract enforced at nested frames (d0 = 1) with coincidence counting;
**F5** deep branches at nesting depth >= 1 propagate `('DEEP', ell, None)`
instead of raising TypeError; glue starts dropped (vacuous, auditor-2 V5).
Deep continuation family = the lineage family {0, -1} mod 2^11 U {-2} mod 2^7
(check5's stricter {0,-1} alone rejects 55 in-family configs — auditor-2 V4's
finding, materializing benignly at the continuation level).

## Item 1 — reachable set R(L), joint (L, rho), deep census

Exact symbolic E(w,v) (affine in u, w = 2u+1, verify_r8's `T_list`/`encode`),
v = 1..600: 159,565 top steps, 58,693 fires, **0 Undecided/Halt events**,
0 d-u-coefficient anomalies (d is a constant at every canonical A-odd state,
confirming Delta = d - (3t+1) with Delta in {0} U {negative odd}), 0
short-canonical birth-tracker mismatches (r in {0,1} states tracked from
E-macro/chain births; sp=1 chain children are r=0, sp=2 are r=1 — the naive
assumption "sp <= 2 gives r=1" is wrong and was fixed).

**Cross-validation against auditor 2 (independent engine), v <= 400:**
fires 25,737 = 102,948/4 exactly; deep fires 309 = 1,236/4 exactly.

- R(L) (d mod 256 at canonical A-odd states; task's rho convention
  (d+3) mod 256 is the same set shifted by 3): |R(1)| = |R(2)| = **30**,
  |R(3)| = ... = |R(10)| = **88** (saturated; same 88-set up to L = 596).
  R(2) = {1,7,17,21,25,27,33,49,...,241,249} (no 253); R(3+) includes 253.
- Delta min per level: -1569 (L=1), -1473, -1407, -1281, -513 (L=5), -1023
  (L=6), **0 for every L >= 7** (d = 3t+1 exactly there). Max t at fire ~ 528.
- **Deep-fire census (v2(q0) >= 8, uniform in w): 709 fires**, sp in {8 (499),
  10 (210)}, run length r at the fire in [2, 500] — **all r >= 2**, none at
  r in {0,1}, none at glue shapes inside excursions (4 glue-shape deep moments
  total, e.g. (v=101,t=84) — the same arithmetic event as the canonical ones
  at v = 102..110). **Every deep child has kap class -1 mod 2048 with
  u-coefficient = 0 mod 2048** (and -1 mod 128) — no -2-class child is ever
  generated on the real orbit in v <= 600, extending auditor 2's v <= 400
  census to v <= 600 and to symbolic w.
- **CLAIM "(L <= 5, rho = -3 mod 256) never occurs": FAIL — 6 occurrences.**
  Exactly two event families: t = 84 in E(v) for v = 102, 103, 104 (r = v-100,
  j = 99, sp = 8) and t = 340 in E(v) for v = 391, 392, 393 (r = v-388, j =
  388, sp = 10); child class -1 mod 2048 in all six. So the time-covariance
  claim holds only in the weakened form "no deep fire at r in {0,1} or at
  glue shapes" (auditor 2's actual statement); R(3), R(4), R(5) must contain
  253. Item 1 is otherwise complete: R(L) as computed is the empirical
  reachable set used by items 2-3.

## Item 2 — corrected template family (L-sum) [Class-B]

Family: starts (r0 in 1..5, rho in R(r0+1) — 30 + 4*88 = 382 (r0, rho) pairs,
kap in {-1 mod 2^11} U {-2 mod 2^7}, 11 tails) = **8404 configs**.

- **Symbolic (hardened engine): 8250 contract-complete + 154 DEEP hand-offs
  (all continuations in the lineage family), 0 failures.** Hardening stats:
  15,081 nested frames contract-enforced (0 violations, 0 suffix
  coincidences), 0 o' >= 3 violations at chains and at deep branches, all
  deep branches at depth 0 (F5 propagation present but untriggered, as in
  the original enumeration). Deep configs: 14 (r0, rho, kapgen) combinations
  — (2,249,k0), (2,253,k0/k1), (3,253,k0/k1), (4,247,k0/k1), (4,253,k0/k1),
  (5,245,k1), (5,247,k0/k1), (5,253,k0/k1) — x 11 tails; all sp = 8.
- **Concrete sum-valid full orbits: 8712 runs (every config >= 1
  instantiation; deep configs x 3), 20000 top steps each = 174,240,000 steps,
  0 halts.** 680,872 deep fires were traversed inside these orbits (all
  survived); max final list length 11. Sum-validity by construction
  (sum(start) = 0 mod 3; each top step adds 3).
- Sanity anchors (adversary's halters, all sum-invalid) reproduce with the
  same engine: [2301,2048,4095] HALT at call 8108; [2301,2048,4094] at 2647;
  [2301,2048] at 1281 (= adversary's "1280 steps" + the halting call).

**PASS**: zero failures symbolic + concrete. This is the corrected (L-sum)
evidence, now at full-orbit depth (20000 steps past singletons, vs check5c's
5000) and over the reachable-residue-restricted family.

## Item 3 — child-prefix coverage (L-coverage)

All 154 deep contexts instantiated concretely with sum-valid parameters
(3 envs each = 462 instantiations, spread over 8 (rho, r0) pairs: (245,5),
(247,4), (247,5), (249,2), (253,2), (253,3), (253,4), (253,5); >= 200 required).

**Faithfulness issue discovered and handled (load-bearing).** The symbolic
engine divides q0 by the guaranteed-for-all-u valuation sp = v2f(q0). At a
concrete env the TRUE valuation can be higher (o'(env) even); there the
symbolic child is a *fictional composite* the dynamics never visits (its head
is odd at t = 0). Classification: 252 faithful, 210 fictional. True child in
both cases (faithful: eval(nestL); fictional: re-divide — ts = sp + v2(o'),
o'' = odd part, same c' and window). Construction validated against raw
dynamics: 28/28 exact matches (14 of them re-divided), 0 mismatches.

- **TRUE children: 462 full orbits (cap 20000), 0 halts** (36,036 deep fires
  inside them).
- **TRUE parents (ground truth): 462 full orbits, 0 halts.**
- **FICTIONAL composites (separate class): 210 runs, 4 HALT.**

**Finding (report, not an architecture failure — but a real limitation of
the sum invariant).** The four halting fictional composites are
**sum-valid** (sum = 0 mod 3) states that halt at step 1:

| cfg (r0, rho, kapgen, tail) | env (u,h,tt,kap,z...) | child list | halt |
|---|---|---|---|
| (3,253,0,[0,0]) | (2,1,3,0,1,1) | [341, 340, 680, 1360, 2720, 5440, 10880, 21760, 72191, 114688, 229375, 4096, 4096] | t=1, x=1024=2^10 |
| (4,253,1,...) | (2,1,3,1,0,2) | same head [341, 340, ...] | t=1 |
| (3,253,1,...) | (2,1,3,1,2,1,1) | same head | t=1 |
| (3,253,1,...) | (2,1,3,1,0,2,2) | same head | t=1 |

Mechanism: the fictional child's own first-step q0 = 3*o' + 4; it halts iff
o' = (2^k - 4)/3 (k even). In the sampled symbol ranges (u<3, h<4, tt<6,
m<2, z<3) the only realizable member is o' = 340 = (2^10-4)/3, forced to
(u,h,tt) = (2,1,3) (o' = 24(6u+1+h) + tt + 1; the sum-mod-3 constraint fixes
tt's parity per config, so faithful/fictional is a per-config property).
Their true parents fire with q0 = 2^10 * 85: the true dynamics re-divides by
2^10 and produces the well-formed child [86, 85, 170, ...] (o'' = 85 >= 3),
which never halts (verified). The composites have v2(H) = 2 — far below the
family's v2(H) >= 11, i.e., they live precisely in the child-prefix segment
where the adversary's (sum-invalid) halts lived, but now sum-valid.

**Consequences for the corrected route:**
1. **(L-sum) separation is regime-bound**: sum = 0 mod 3 excludes halts for
   the family's v2(H) >= 11 starts (8712 + 462 + 462 orbits, 0 halts) but NOT
   for shallow-H excursion-shaped states. The child-prefix segment cannot be
   certified by the sum invariant alone.
2. **(L-coverage) must be stated for true children**: the chain hand-off is
   faithful exactly when o' is odd (true sp = v2f(q0)); the child-prefix
   lemma applies to children with o' odd and >= 3. All 462 true children
   (o'' odd, >= 3) survived. The engine-level precondition o' >= 3 (F3 fix)
   must be strengthened to o' odd when instantiating symbolically-built
   children concretely.
3. **Generic-vs-specific valuation gap**: verify_r8's compositional engine
   (both engines) simulates the *generic-u* trajectory; at envs with
   v2(q0(env)) > v2f(q0) the true trajectory differs (more pushes). This does
   not affect the concrete runs or check1-4's generic-u conclusions, but
   Class-A wording "uniformly in every symbol" for the compositional
   simulation needs this caveat.

## Item 4 — verdicts

| item | verdict |
|---|---|
| 1 reachable set R(L), deep census | **PASS** (with the (L<=5, rho=-3) claim **FALSIFIED**: 6 occurrences, all child class -1 mod 2^11; auditor 2's r >= 2 / no-glue statement extended to v<=600 symbolic and confirmed exactly) |
| 2 corrected template (L-sum) | **PASS**: 8404 symbolic runs 0 failures (8250 contract + 154 in-family deep hand-offs); 8712 sum-valid full orbits x 20000 steps = 174.24M steps, 0 halts |
| 3 child-prefix coverage (L-coverage) | **PASS on true dynamics**: 462 true children + 462 true parents, 0 halts, construction validated 28/28 vs raw dynamics; **FINDING**: 4 sum-valid halting fictional composites (o'=340, halt at step 1) — sum-validity alone does not certify the child-prefix segment; faithful-decomposition (o' odd) required |

No sum-valid halting configuration *reachable from the corrected family by
true dynamics* was found: 9,636 full orbits (8712 + 462 + 462), ~192.7M top
steps, 0 halts, > 750k deep fires traversed. The corrected residual for the
all-v statement is now: (i) R(L) must include rho = 253 at L in {3,4,5}
(covariance claim weakened to "r >= 2 and no glue"); (ii) L-coverage carries
the o'-odd faithfulness condition and the shallow-H regime; (iii) the
generic-vs-specific valuation caveat on compositional uniformity claims.
