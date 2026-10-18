# Three-way review of work_global_clock_horizon and work_global_closure_attempt (GPT Astra, 2026-10-18)
Reviewers: adversary = Claude subagent (scratch aud42; scripts rerun on copies, all counts and hashes reproduced);
auditor 1 = agy gemini-3.8-flash-high (blind, aud40, agy_aud40.log); auditor 2 = cmdc deepseek-v4.1-flash (blind,
aud41, cmdc_aud41.log). Both auditors reviewed the pre-patch text (constant 32).
- Adversary: `2. with fixable gaps`.
  (A) CSH case analysis correct (b: Lemma K(b); c: enclosing/copied epoch J_W = Theorem S(d); a: RA); no circularity
  (CLOCK on the maximal defined prefix, no EXT input); integer lemma correct. **MEDIUM gap:** Theorem S's level-4
  certificate only treats later chains with j<K′; for J<K″ this followed from the mass bound, but near K_clock τ(J−1)
  can reach ~2^(K′−2). Fix: constant 32→64 and Lemma MASS. LOW: script's type-c check uses the latest type-a crossing
  as "the fire" without comparing with the copied epoch from pair data (finite check only).
  (B) CAP, conditional closure, ORIGIN/SHIFT, search scoping correct; LOW: "unconditional by-product" wording.
  CHECKPOINT/README: range caveat; README scope wording (true-fire projection; pure-a words).
- Auditor 1 (gemini): `1. all correct` (integer inequalities T=64..1024; CAP/closure bounds; both word cylinders,
  empty fire projections, margins, next parameter 6). Did not detect the range issue.
- Auditor 2 (deepseek): `1. all correct` (CSH premises; integer inequalities at many T; CAP and closure constants;
  filter iff on 3000 random cases; both cylinders H,K,p, δ bounds; lifts; 64-source projections 64/2/0). Note: the
  stated minimum margins 12/8 depend on an unstated σ0 (= K+11, K+7); positive for every σ0>=K+1 — added.
- Patch (coordinator): PROOF_CLOCK_HORIZON constant 64 throughout, new §3a Lemma MASS (2^{j_t}<=β_t<=6d_t−1,
  CLOCK τ(J−1)<=(9/64)2^T, τ(n)<=9T³ for n<T ⇒ 6d_t<2^T for t<=9); verify script updated (MASS inequality per
  exponent; PASS); README/CHECKPOINT wording; closure §1 wording; σ0 notes. Targeted re-reviews: round 1 off-by-one
  (t<=8 → t<=9) and CHECKPOINT wording; final `1. closed in all states`.
- **Recorded latent issue (LOW, pre-existing):** accepted work_global_ext/PROOF_EXT.md §6 applies Theorem S for
  J>=K″ with the same implicit range hypothesis (later chains below K′); any use of Theorem S above K″ must supply a
  MASS-type range argument.
VERDICT: ACCEPTED. **New accepted horizon: K_clock = floor(2^K′/(64K′²)) > K″** — EXT for J<K_clock; the TM does not
halt during the first 2^K_clock − 2 top steps. work_global_closure_attempt accepted as conditional/local results
(the all-Q word-length bound W(Q) remains unproved). Global non-halting of #1 remains UNPROVED.
