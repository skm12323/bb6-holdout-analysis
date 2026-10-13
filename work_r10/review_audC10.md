# review_audC10.md — BLIND AUDITOR-2 (independent re-implementation) of agentC10 "EG"

Audit of: `work_r10/agentC10_report.md` (+ `agentC10_lib.py`, `agentC10_run1/2/3.py`,
`agentC10_out1/2/3.json`, `agentC10_cross.json`). Claim under audit: the endgame
(first boundary read -> singleton) of the real excursions E(w,v) never halts for all v,
via crossing-state decomposition + symbolic closure on 2^18-cylinders + robustness tests,
with e(v) <= 16.

Method: everything below was re-implemented from scratch BEFORE reading the artifact
(`revC10_lib.py`, `revC10_t1_validate.py`, `revC10_t2_law.py`/`t2b`, `revC10_t3_closure.py`,
`revC10_t4_coverage.py`, `revC10_t4b_push.py`, `revC10_t5_margins.py`; outputs
`revC10_t1..t5.json`). Ground truth chain: audited micro R-rules R1..R5+HALT
(work_r1 RULES.md §3) = closed-form top map (§5) = my pair map with boundary; then the
pair map drives everything. c-arithmetic cross-validated exact-bigint vs (v2, residue
mod 2^64) fast form (identical decision streams, e, ell on v <= 500; the two e=17/20
counterexamples below re-verified with pure exact big-int arithmetic). Total footprint
4.9 MB.

Notation: n = v-1 (boundary index); crossing(v) = walk state just before the first step
reading original index v-2; h := n - i in {0,1,2} = queue slots from pointer to boundary
incl. boundary; d = |P| in {0,1}; class = (i mod M, d, lam_A mod M, lam_front mod M, h).

## Task 1 — own boundary walker vs concrete excursion: PASS

- micro R-rules = closed-form top map: 45/45 runs (v <= 15, U in {3,9,15}), identical
  composite config lists. (Two bugs found and fixed in my own micro runner during
  bring-up: R4 off-by-one, composite boundary must be after R5 only — R4 outputs are
  mid-chain, not top configs. Final runner agrees everywhere.)
- closed-form top map = pair map with boundary (defect (2^{v-1},-1) at index v-1, absent
  c-slot read as (0,0)): v = 1..500, U = 3 — step-by-step list equality at every one of
  the 110,651 states, no halt, singleton = 2^v*3 + 3*ell(v) exactly, (S1)/(S2)/u-form at
  every chain. Spots U = 9, 15 (w = 3, 5): 260 v each — identical.
- ell(1..20) = 1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16 — matches agentC10's
  table exactly. max e(v<=2000) = 12 — matches their [1,12].
- Fast (mod-2^64) walker = exact walker on all v <= 500 (decision seq, e, ell), and its
  level-fire behaviour matches the G6/fast_walker measurements (maxdef 12 at i~503,
  chain deficit <= 16 up to 3*10^5 with first 16 at i = 97957, matching G6's Delta <= 16).

## Task 2 — crossing-state law v = 1..8192: FAIL as literally specified; repaired law holds vacuously at 2^18

- The literal class (i, d, lam_A, lam_front) mod M does NOT determine the endgame: at
  M = 8192 (i exact) there are 1866 clashing pairs; ALL 1866 are explained by the missing
  distance-to-boundary h = n - i (0 non-h-explained). Concrete smallest counterexample:
  v = 1, 2, 3 all have crossing state (i=0, d=0, lam_A=1, front=0) but endgames
  [(-1)], [(-1)], [(-1,-1)] — the state does not record how many originals sit between
  the pointer and the boundary. agentC10's own class ("nP, ip-offset, ...") does include
  the offset, i.e. their class is the repaired one.
- With h appended, scanning ALL M in 2..512: every M <= 510 that has class collisions
  (at least one pair) also has a clash — no M <= 510 works; the smallest working M is 215
  and every working M <= 512 works vacuously (0 collisions). At M = 256: clash (770,
  7938) — lam_A = 2041 vs 21241 agree mod 256 but the 3rd fire has j = 11 vs 8. At
  M = 2^18 the class is injective on v <= 8192 (8192 classes) — the law has no same-class
  pairs to test at the claimed modulus in this range; its content is exactly the symbolic
  closure (Task 3) plus, beyond 2^18, nothing testable (see Task 4).
- agentC10's class convention (d, h, lam_A, lam_Y mod 2^K), verified on my data for
  v <= 65536: K = 15 gives 42570 classes / 22965 multi-member / 4 non-uniform
  (theirs: 42570 / 22966 / 4 — the 1-member difference is their inclusion of v = 1);
  the 4 non-uniform pairs are (2,36734), (3,36735), (12246,48976), (24496,61226) —
  the spike family. K = 18 injective — confirmed.

## Task 3 — own symbolic closure on 2^18-cylinders: PASS on all sweep classes

- Own symbolic runner: lam values carried as r + 2^m*(cA*tA + cY*tY + cK) with free
  tA, tY >= 0 (a 2-parameter cylinder — strictly larger than agentC10's 1-parameter
  shared-t slice), boundary lam = -1 exact, originals 0; c-side as deficit lower bounds.
  Uniformity criterion for a v2-query: r > 0 -> v2(r); r = 0 -> uniform iff
  v2(cK) < min v2 of nonzero free slopes (then j = m + v2(cK)); criterion validated
  numerically on 30,000 random cases (box t in [0,48)^2), including negative constants.
- All 8192 classes of the v <= 8192 sweep: symbolic decision sequence equals the concrete
  sequence of every member (0 mismatches); for the 8158 classes with n >= 34 the closure
  itself passes at deficit assumptions dA = 16 and 30 (the 34 small-n classes are covered
  concretely by Task 1/2). No NONUNIFORM, no MARGIN, no CAP failures; every chain has the
  u-form (c_u even >= 2, lam_u odd >= 1 => u >= 2U+1 >= 3 for all odd U). Robustness at
  dA = 40 flags only 2 classes with n in {34,37} (artifact of assuming a deficit larger
  than n; they pass at 16/30).
- The spike family (v ~ 1538, 3063, 6131/6132) drives the resolution depth m down to 0
  (sum of j's consumes the 18-bit window); the runner stays sound there (m = 0 parity/
  v2 decided by the coefficient criterion). Minimum endgame chain margin over the sweep:
  1 (small v only; >= 31 for v >= 34, growing ~ n - 15).

## Task 4 — coverage for all v: the critical gaps

Walk continued to i = 2^17+5000 and then 3*10^5 (and 4*10^6 for Task 5), collecting the
crossing class at every first-read event and running every boundary endgame:

- All 300,002 excursions v <= 300,001 reach the singleton, no halt, no starvation, no
  CAP; max e = 16 at v = 48976 — exactly agentC10's argmax.
- The class set does NOT close and is not eventually periodic: a NEW class appears at
  essentially every v (70,539 new in (65536, 136074], 163,928 more by 3*10^5; |S| = #v).
  The v <= 65536 sweep saw 65,535 of >= 300,002 classes. So "which crossing states can
  arise for v > 65536": new ones forever, as far as computable; a finite covering class
  set is not obtained by enumeration, and no closure/periodicity of the class stream was
  detected (probe over periods up to 131072 on the tail).
- Symbolic closure of the 234,467 classes the 65536 sweep missed: 234,464 pass, **3
  FAIL** — genuine non-uniformity at tie depth = the cylinder width:
    * class (97955, 0, 262141, 0, h=1) [rep v = 97957]: step 0, lam_x = 2^18*(1 + tA),
      j = 18 + v2(1+tA) — depends on tA. (Concretely lam_A + 3 = 2^18 exactly, j = 18.)
    * class (97955, 0, 262141, 0, h=2) [rep v = 97958]: same tie.
    * class (195891, 0, 262137, 0, h=2) [rep v = 195894]: tie at depth 16 with free
      slope 4 (the concrete endgame fires j = 19 — already outside the 2^18 window).
  These occur because the walk's max j grows: j = 18 at i = 97947/97955, 19 at 979473,
  20 at 391794, 21, 22, 23 at 3,134,283 (measured). agentC10's mechanism sentence
  "slope divisible by 2^18 > every j of the class" needs maxj < 18 — true on v <= 65536
  (maxj = 17), false from v ~ 97957 on. Their own K = 15 experiment (4 non-uniform deep
  ties "resolved one bit higher") exhibits the same phenomenon one level down. No fixed
  cylinder width works for all v.
- Non-vacuous 2^18 wrap test: among the 37,855 candidate pairs (v, v + 2^18) with
  v + 2^18 <= 3*10^5, exactly 0 share a class — the 2^18 class law remains empirically
  untestable even at 3*10^5; its only support is the per-class symbolic closure, which
  fails on the 3 classes above.

## Task 5 — e(v) <= 16 and e <= maxj+1: e <= 16 is FALSE in general (exact)

- v <= 8192: max e = 13 (v = 6132); v <= 3*10^5: max e = 16 (v = 48976) — matches
  agentC10. e <= maxj(endgame fires) + 1: 0 violations on all data (also at 4*10^6);
  e <= walk-maxj + 1 fails at small v (walk has not fired yet) — the correct reading is
  the endgame's own maxj.
- Pushing to 4*10^6: **e(391796) = 17, e(783573) = 17, e(1567152) = 20** (largest
  endgame j = 22 there; j = 23 at v = 3134283; one e = 19 in between). The three values
  were re-verified with exact big-integer arithmetic (no residue representation):
  e(391796): seq [20,-1,-1,1,-1,4,-1,-1,-1,2,-1,1,-1,3,-1,-1,-1]; e(1567152):
  [22,-1,-1,1,-1,4,-1,-1,-1,2,-1,1,-1,3,-1,-1,-1,4,-1,-1]. e grows ~ log2(v) along the
  spike-crossing family, as agentC10's own robustness tests anticipated (their
  adversarial deep ties already showed e up to 26). Their growing bound
  e <= log2(9*ell(v)) + 2 still holds on my data (20 <= 25.6 at v = 1567152).
- Margin drain (v <= 8192): walk deficit at the boundary snapshot max Delta = 7;
  endgame chain deficit (n - v2(c_x)) max 11 (excess over Delta up to 11 at v = 6132);
  min chain margin 1 (v = 5 only; >= 31 for v >= 34). At 3*10^5: state-level max deficit
  20 (i = 97957), chain-level max 16 — consistent with G6's (M1') measurements.

## Task 6 — comparison with agentC10_report.md

Confirmed exactly by independent replication (same numbers, different code):
- ell table (1..20); ell/e/dec per v (0 mismatches on v <= 500; e column 0 mismatches);
  total lockstep states 1,780,141 = sum of their per-v ell for v <= 2000 = my sum;
  e in [1,16] and argmax v = 48976, e = 1 count 24,803; 44,882 endgame chains with
  min lam_x = 8, min lam_u = 1, min u@U=1 = 7, min u@U=3 = 19; class census at K = 15
  (42570/22965+1/4) and injectivity at K = 18 on v <= 65536; template census scales
  exactly x8 from my 8192-range to their 65536-range on every common template; their
  "v mod 2^m fails" negative result is consistent with my modulus scan.
- The endgame never halts and always reaches the singleton (2^v, 3*ell(v)): confirmed
  60x beyond their range (4*10^6 vs 65536), U-generic (pair-side decisions never see U
  given margins; my E1-equivalent induction reproduced).

Discrepancies:
1. [Material] "e(v) <= 16" is false as a universal statement: e = 17 at v = 391796 and
   783573, e = 19 and e = 20 up to 4*10^6 (exact arithmetic). agentC10's report scopes
   the constant to v <= 65536 (true) and states the growing bound e <= log2(9 ell)+2
   (survives), but the headline constant is a range artifact and the task-level claim
   is refuted.
2. [Material] The STATUS claim that the all-v extension "inherits exactly the walk's own
   residual ((M1'),(M2')) and nothing else" is wrong: the per-class 2^18-cylinder
   closure itself fails at classes first occurring at v = 97957/97958/195894 (tie depth
   = 18/16 with free slope; j reaches 23 by 3.1*10^6). Closing all v needs an additional
   tie-depth condition (maxj of the class < K), which is a further unbounded walk-side
   residual, not implied by (M1')/(M2'). Their safety-only all-v route (E5 margins +
   robustness on sampled legal crossings incl. deep ties) is not refuted by my data, but
   it is Class-B sampled, and it abandons the cylinder mechanism the claim names.
3. [Material] Coverage: no closed/periodic class set; new classes at every v; the
   65536-sweep saw ~22% of the classes arising by 3*10^5; the 2^18 class law has zero
   same-class pairs to test even at 3*10^5 (wrap test vacuous). A finite-class
   enumeration cannot cover all v.
4. [Minor] Their symbolic cylinder is a 1-parameter slice (one shared t for lam_A and
   lam_Y); same-class states form a 2-parameter family. My 2-parameter closure passes
   on their entire range and fails on the same 3 classes, so this does not change any
   verdict, but the printed mechanism is weaker than claimed.
5. [Minor] §5 wording "'e <= 16' ... holds whenever maxj <= 15" contradicts their own
   table (v = 48976 has maxj = 17, e = 16).
6. [Minor] K = 15 multi-member count 22966 vs my 22965 (v = 1 inclusion convention).

## Verdict

Per task: T1 PASS; T2 FAIL-as-specified (class must include h = n - i; with h, no modulus
<= 510 works non-vacuously, 2^18 is injective/vacuous in range); T3 PASS on all sweep
classes (own, stronger 2-parameter closure); T4 FAIL of the coverage method (class set
never closes; 3 classes break the 2^18 closure; wrap test vacuous) though every computed
excursion is safe; T5 e <= maxj+1 PASS, e(v) <= 16 FAIL (exact counterexamples from
v = 391796).

**NOT all correct — issues: (1) e(v) <= 16 is false (e = 17/20 exact, grows ~ log2 v);
(2) the 2^18-cylinder symbolic closure fails on classes occurring from v = 97957 on, so
the all-v claim inherits an extra unbounded tie-depth residual beyond (M1')/(M2');
(3) the crossing-class set never closes, so finite class enumeration cannot cover all v.
The endgame's non-halting itself is confirmed on every computed v (to 4*10^6, 60x the
artifact's range) and all of agentC10's in-range statistics reproduce exactly.**
