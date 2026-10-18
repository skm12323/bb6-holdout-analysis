# Three-way review of work_ext_roots (GPT Astra, 2026-10-18), 2026-10-19
Targets: PROOF_EXT_ROOTS, PROOF_LAST_TIE (group 1); PROOF_LOW_DEFICIT, PROOF_A_SOURCE_DESCENT, PROOF_DEFICIT_SEVEN
(group 2). Reviewers: adversaries = two Claude subagents (scratch aud45, aud46; all verifiers rerun on copies, PASS,
json identical apart from timing); auditor 1 = agy gemini-3.8-flash-high (blind, aud43, agy_aud43.log); auditor 2 =
cmdc deepseek-v4.1-flash (blind, aud44, cmdc_aud44.log; a first run stalled with no output and was restarted).

- Adversary group 1: `2. with fixable gaps`. ENTRY (b defect 0, c defect −λ_Y), ROOT, RECORD, B-INTERVAL,
  C-ENDPOINT (Γ_1<=J/2 at J>=128) and LAST_TIE bounds (203=203 at E=1) all hold; least-counterexample induction
  legitimate (C2-log needs only EXT(J_W), J_W<J, and unconditional CLOCK). MEDIUM: in the J>=128 mode the 504-prefix
  check reaches no source (max M=16) — all source rejections and the positive control are J<128 diagnostics.
  LOW: missing-source silent skip in last_tie_filter; growth-ratio formula; Prop 2.1/L′ citation; root search
  bounds continuation not safety and covers no relevant start; EXT* version; 170 projector checks = spot check;
  README/CHECKPOINT "no canonical candidates" scope.
- Adversary group 2: `2. with fixable gaps`. **A-SOURCE stands**: the precision chain is sound and uses EXT(J′)
  tie-freeness (= loss < precision), not mere termination; induction legitimate (J′ always an actual crossing of an
  earlier completed epoch; EXT never applied to virtual fires); C3, C5-BA, AA→S(p+1), CA, weight grammar
  {AAA,ABA,BAA,BBA,CA} and BAA/BBA normal forms verified; MINUS/PLUS correctly unproved. Minor: X(p) odd type b
  justification; AB edge cases; strict EXT only (does not transfer to EXT*); verifier's mixed-history branch wrong
  but never reached (only four AA instances exercised; reviewer sweep P<300 met only a, aa, ab); stale AA-open text.
- Auditor 1 (gemini): `1. all correct` (ENTRY, bounds, 76 A + 4 BA calendar sources, AA P=14/n=6133, grammar,
  normal forms).
- Auditor 2 (deepseek): `2. with simple errors` (ENTRY on 3995 odd crossings, bounds, positive control, 317 ε=3
  sources, AA, normal forms, grammar, MINUS/PLUS on m<2·10^4 with min margin 2). Fixes: C1 needs the finite base
  τ(n)<=n for small n; first-entry chain bookkeeping in T<=E(1+J²) (resolved: already counted in the first block);
  notation p in LOW_DEFICIT §2; provenance wording for the R=6133 instance.
- Patch (coordinator): all items applied; last_tie_filter raises on a missing canonical source unless
  noncanonical=True; verify_low_deficit ancestry comparison restricted to i==0 (both rerun, PASS). A wrong
  parenthetical introduced in one patch round was caught and removed. Targeted re-reviews: both groups
  `1. closed in all states`.

VERDICT: ACCEPTED as conditional reductions inside a least-strict-EXT-counterexample induction:
ENTRY constraints and index bounds; fixed-prefix last-step completeness; c sources with ε=3 and ε=5 (AA, BA),
and every c source in an A-initial source epoch (A-SOURCE), are excluded; ε=7 reduces to the MINUS/PLUS reference
families (unproved). Remaining frontier: c sources with ε>=7 in b/c-first source epochs (incl. MINUS/PLUS), and all
outer type-b entries. EXT remains open; accepted horizon K_clock unchanged.
