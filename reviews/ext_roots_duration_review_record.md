# Three-way review of work_ext_roots duration notes (GPT Astra, 2026-10-19)
Targets: work_ext_roots/PROOF_DURATION_NORMALIZATION.md, PROOF_DURATION_BRANCHES.md (+ verify_duration_reduction.py,
verify_duration_branches.py). Reviewers: adversary = Claude subagent (scratch aud50; both verifiers rerun on copies,
PASS, json byte-identical; residue table recomputed independently); auditor 1 = agy gemini-3.8-flash-high (blind,
aud48, agy_aud48.log); auditor 2 = cmdc deepseek-v4.1-flash (blind, aud49, cmdc_aud49.log).
- Adversary: `2. with fixable gaps`, no structural break. Residue table, predecessor lemma (H>=5, k0≡10, Δ≡5/1 mod 16),
  exact precision H after removing 2^H U, legitimate use of EXT(H) (only to bound Δ_H, never on D-ROOT), PLUS b
  closure, MINUS b words for copied parameters 5/8, PLUS a → Z(q) at precision q−1, and both large-H witnesses
  verified. LOW fixes: q<=4 needs X(0..3) even; HP's x*≠0 via the positive cone; AB edge case p<=4; record wording
  "j+Λ<C for any C>q"; witnesses' entries are hypothetical; beta-evaluator check uses the same oracle.
  **Strengthening:** sections 1–2 of BRANCHES apply directly to the original PLUS(m)/MINUS(m) states (C=m−1),
  not only to D-ROOT; normalization is needed only for the remaining branches.
- Auditor 1 (gemini): `1. all correct` (table, Δ_H<=H³, both exact words, both large-H witnesses).
- Auditor 2 (deepseek): `1. all correct` (2929 k≡15 fires, 653 predecessor cases, 458/461 duration classes, longest
  word (5,2), 363 PLUS b cases, 18 MINUS b words, Z valuations, both witnesses Δ=(2^64−1)/3 and 2^64+1).
- Patch (coordinator) + targeted re-review (adversary): `1. closed in all states`.
VERDICT: ACCEPTED as partial progress on the MINUS/PLUS families. Closed: PLUS b branch; MINUS b copying fire
parameters 5 or 8 (both directly for the original families). Reduced: remaining branches to the D_MINUS/D_PLUS
duration references at precision H (their all-scale j+loss<H is OPEN) and PLUS a to Z(q) (OPEN). Open: PLUS c,
MINUS a/c, MINUS b with other copied parameters. EXT open; accepted horizon K_clock unchanged.
