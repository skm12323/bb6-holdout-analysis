# Three-way review of eleven work_global_* notes (GPT Astra, 2026-10-16/17), 2026-10-17
Targets: clock, root_phase, rescue_ladder, mixed_precision, weight16, transfer (group 1); period, clock_words
(+failure budget), long_witness, ancestry (+local realization), calendar (group 2).
Reviewers: adversaries = two Claude subagents (scratch aud32, aud33; verify scripts run on copies, all pass, json
byte-identical); auditor 1 = agy gemini-3.8-flash-high (blind, aud30, agy_aud30.log); auditor 2 = cmdc
deepseek/deepseek-v4.1-flash (blind, aud31, cmdc_aud31.log). An earlier auditor-2 attempt with dsh (deepseek-flash)
was aborted: its Windows sandbox could not run a shell (aud31_dsh_aborted).
- Adversary group 1: `2. with fixable gaps`. **PROOF_CLOCK main theorem stands**: no circularity (corridor chains are
  copies of earlier W-chains, safe, j_next<=j-3; first-failure inspection sound; no exit-length/C2/termination
  assumption; constants HALF, 1345, INC, SAFE checked); SQRT-EXIT ⇒ F defined forever (base 10^8), F only.
  Fixes: §6.1 "level fire"; §3 count wording; WEIGHT16/TRANSFER §2 numerator inference (θ=N/D); MIXED_PRECISION §4
  scope (V4 r<=2 for J<1024, C2); LADDER odd-n remark.
- Adversary group 2: `2. with fixable gaps`. No algebra/congruence error. Fixes: PERIOD hypotheses; CLOCK_WORDS
  SPACING states + §5 citations; FAILURE_BUDGET MASS via A-CONE, Q_loss wording; LONG_WITNESS base citation;
  ANCESTRY cited unaudited compression (medium) → accepted sources, §5 scope (unconditional relative to accepted
  work); LOCAL_REALIZATION iff hypotheses; CALENDAR check description, automaton citation, and new verifier loop.
- Auditor 1 (gemini): `1. all correct` (own F: τ(n)<=nP(n) for n<8191, max gap 11; key identities; parameter-17
  fire 218452/244873).
- Auditor 2 (deepseek): `1. all correct` (own F; PROOF_CLOCK constants H(10^8)=44, R=2272726; NO-SKIP on 121150
  epochs; ρ_B, C(h_B−1) at B=16,18; 244913 exact; phase tables by BFS).
- Patch (coordinator): all items applied; verify_calendar.py now runs epoch_crossings at one actual fire of every
  J<=4096 (PASS). Targeted re-reviews: group 1 and group 2 both `1. closed in all states`.
VERDICT: ACCEPTED. PROOF_CLOCK: global non-halting of F reduces to SQRT-EXIT (unconditional reduction).
Global non-halting of #1 remains UNPROVED; endgame unchanged.
