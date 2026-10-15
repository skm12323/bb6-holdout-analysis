# Three-way review of work_g2_bc_frontier, work_g2_two_blocks, work_g2_mixed_blocks (GPT Astra), 2026-10-16
Reviewers: adversary = Claude subagent; auditor 1 = cmdc deepseek/deepseek-v4.1-flash (blind, scratch
D:/math_cc_astra/aud24, log cmdc_aud24.log); auditor 2 = agy gemini-3.8-flash-high (blind, aud25, agy_aud25.log).
- Adversary: `2. with fixable gaps`. Algebra and the three verify scripts pass (scripts rewrite their own json,
  deterministic). (A) A1 scope: by M2' Q>2^12239, and by PROOF_RESCUE §4 + Theorem D no epoch with J<B contains
  17,5,17,Q,24480,R — obstruction concerns J>=B only, shows the listed local envelopes insufficient, conflicts with
  no accepted result; A2 AUTONOMOUS_RESULT overclaimed "current method"; A3 coefficient data asserted, not derived.
  (B) correct as stated; B1 a_i bound is M2' not C1; B2 "drop >=3" needs eps>=1 table citation; B3 hypotheses into
  theorem statements. Correction G<=J-q-m confirmed.
- Auditor 1 (deepseek): `1. all correct`. Own F: X(24479) odd type a, tau=21832, k=10916, 6k+40=2^16; BA, NEW,
  RATIO, BAND, WIT verified exactly (Q=p+2 control fails, so Q>=p+3 is needed); POS identity 260 cases, C bounds
  600 random cases, corridor 736 cases, 1977 real b/c returns satisfy j_next<=j-2-eps. Nits: RATIO needs w>=11;
  "four classified phases" not checkable from cited dependencies.
- Auditor 2 (gemini): `1. all correct` (own F reproduces CLOCK; algebra and bounds pass).
- Patch (coordinator): all items applied (OBSTRUCTION §3/§4/§5 Scope, AUTONOMOUS_RESULT wording, PROOF_TWO M2'
  citation + hypotheses, PROOF_MIXED eps table + hypotheses).
- Targeted re-review (adversary): `1. closed in all states`.
VERDICT: ACCEPTED. Global non-halting of #1 remains UNPROVED.
