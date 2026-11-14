# Three-way review of work_gc_t4_horizon (ZCode GLM subagent, R1: T4 horizon transfer), 2026-11-10

Target: work_gc_t4_horizon/NOTES.md (Theorem H-T4, Lemma EXT-T4, Lemma DATA-T4, Lemma HINQ, Lemma
ORD, §6 verification), verify_t4_horizon.py, t4_horizon_checks.json, extended_run_900s.log. Route
claim: F defined for every s with 3s+4 < 2^T4 (s < (2^T4−4)/3) and machine #1 non-halting in the
first 2^T4−2 top steps, from accepted imports only (Theorem T4, I-4, EXT-CLOCK+Lemma MASS, EGX
Corollary H/Lemma TR/U(b), PROOF_EXT H″/U*/RA, CLOCK/STATE-CLOCK, R4 singleton lemma, E1–E4), plus
the first mechanical validation of the H-CLOCK transfer pattern itself. Round-1 reviewers: adversary
= ZCode GLM (attack, re-runs + own implementations); auditor 1 = ZCode GLM-4.6, blind (author's
script unread; own scripts aud1_scratch/); auditor 2 = agy gemini-3.8-flash-high, blind (own scripts
agy_scratch/, per agy_audit_prompt.md rules 1–6). **All three attended; none absent.**

## Round 1 (three-way, 2026-11-10)

- Adversary: `2. fixable gaps`. MEDIUM (F1): Lemma ORD's [B] verification used the wrong K-series —
  the three upper bounds Tw(·,499497) (verify_t4_horizon.py:158/:162/:173 as then; NOTES §2) are not
  upper bounds of the repo constants (499997 series per CHECKPOINT:289, PROOF_CLOCK_HORIZON:8), so
  'K_prime<T3', 'K_clock<T4', 'K_prime<=K_clock' certified nothing about them and §2's printed uppers
  were false (lowers true). LOW: (F2) HINQ slack quadratic is 3H²−12H+10, not +14 (valid H≥3, fails
  at H=2); (F3) H=T4 irrational needs the one-sentence real extension; (F4) §3's "absorbed by Theorem
  RA" predates the residual correction block's net argument; (F5) EXT-T4 stated J≥2 while H-T4(i)
  applies it at J=1 fires (2,724,369 at H0=26). Confirmed: script re-run twice (default ALL PASS
  149.4 s; 900 s ALL PASS 631.5 s, ladder +28; counts match NOTES §6/JSON/log); EXT-T4
  non-circularity (all T4-internal sources Q<T3<K_clock); DATA-T4; H-T4(i)/(ii) replayed
  clause-by-clause vs U(b)/Corollary H/H″/H-CLOCK; the τ(J−1)<τ(ρ) strictness strengthening rebuilt
  from Lemma K; own top map H0=16/18/20; all eight order relations independently re-derived on the
  correct constants; no overclaim.
- Auditor 1: `2. with fixable gaps`. Same MEDIUM found independently (printed §2 uppers judged False
  by own script, lowers true; corrected tops verified); HINQ exact + STATE-CLOCK side condition; EXT-T4
  non-circular; DATA-T4 verbatim; (i) with strictness argument independently re-derived and
  machine-verified (10^5-step full pair walk: 44,688 same-step pairs all (a,b)); (ii) I-3
  instantiation checked; independent machine reproduction at H0=20/22 — ALL counts match the author's
  JSON exactly (incl. all 118,664+474,656 closed epochs == S(J), endgame == S(v), ℓ table,
  off-by-one). LOW: J=1 note; INFO: timing/throughput text; fire_Js second element undocumented.
- Auditor 2 (agy): `1. all correct`. Independent no-float derivations of HINQ (noting the +10 typo
  as benign), ORD on the **correct 499997 series** (all eight relations), EXT-T4 non-circularity,
  DATA-T4, (i)/(ii) clause-by-clause, and an independent machine reproduction at H0=18. No further
  findings.
- Round-1 VERDICT: ACCEPTED in part + 7 patchItems (1 MEDIUM, 4 LOW, 2 INFO); horizon stays
  2^K_clock−2 pending the patch round; summarizer byte-checked the constant defect (log2 K = 2^499997−2:
  < 2^499497 False, < 2^499997 True) and the fire_Js J=1 datum.

## Patches (author) and targeted re-review 1

- Patches (author, per the 7 patchItems): review-correction block at the head of NOTES.md; part (b)
  upper tops 499497→499997 in script (:175/:179/:190) and NOTES §2 (:131-132), lower tops kept (all
  true); HINQ quadratic → 3H²−12H+10 with H≥3 scope and H=2 negative control (NOTES:103, script:8,
  §6(a)); Real-H instance paragraph for H=T4 (NOTES:106-113, exact script asserts :81-89); BBBA
  wording aligned with residual correction block item 1 (NOTES:160-168); EXT-T4/DATA-T4 extended to
  J≥1 with the one-line J=1 argument (NOTES:137/:178); throughput/timing numbers refreshed; fire_Js
  format documented in three places.
- Targeted re-review 1 (adversary): `1. closed in all states`. F1 closed by triple verification —
  byte-level extraction confirms the three uppers are the 499997 series and NOTES §2 is in sync; own
  19 exact integer links (tower comparisons reduced to computable integers ≤ 2^9999998, no floats)
  judge every revised bound true for the repo constants and all eight ordering chains valid
  ("ALL 19 LINKS OK"); re-runs of the revised script both budgets ALL PASS (default 151.9 s, ladder
  {20,22,24,26}, per-rung counts identical to round 1; author's 900 s re-run 600.2 s, ladder +28,
  counts consistent). F2–F5 and both INFO items verified applied as prescribed; part (c)
  characteristic lines byte-identical (engines, ladder/0.6 budget ratio, s* formula, assertion
  families), no new changes introduced; round-1 cross-check against this record's 7 patchItems
  one-to-one. One pre-existing, non-blocking LOW remains: the docstring usage line says
  [total_budget_seconds=540] while main defaults to 480 (and NOTES §6/§8 say 480) — cosmetic, does
  not affect any assertion's truth and does not block acceptance.
- Summarizer checks this round (byte-exact + own runs, Python312 −I): the three bound tuples at
  script:175/:179/:190 read `K = (Tw(2, 499996), Tw(2, 499997))`, `Kp = (Tw(3, 499996),
  Tw(3, 499997))`, `Kc = (Tw(4, 499495), Tw(4, 499997))` — all three uppers byte-extracted as the
  499,997 series (4-9-9-9-9-7), lowers 499,996/499,996/499,495 kept (true bounds);
  NOTES:131-132 uppers 499,997 series; exact integer spot check: 2^499,996 < log2 K = 2^499,997−2 <
  2^499,997 True; HINQ +10 at NOTES:103/:289 and script:8; J≥1 at NOTES:137/:178; docstring 540 at
  script:4 with `else 480.0` at :600 (the re-review cited :5; same line, count differs by one).
  Own full re-run of the patched script at the default budget
  (`PYTHONUTF8=1 <Python312> -B work_gc_t4_horizon/verify_t4_horizon.py` from D:/math_cc):
  **ALL PASS, exit 0, 150.4 s, ladder {20,22,24,26}**, every per-rung count identical to round 1
  (H0=26: 22,369,619/25,074,248/7,594,491/595,760/7,594,490/67,108,862/29,990,130/22,783,474/
  max v 25). The 900 s extended re-run was not repeated by the summarizer (re-reviewer verified the
  author's 600.2 s run).

## Patches (author) and targeted re-review 2 (final; round cap 2)

- Patches (author): docstring usage line `[total_budget_seconds=540]` → `[total_budget_seconds=480]`
  (verify_t4_horizon.py:4); Round-2 entry (8 lines, :51-57) appended to the NOTES correction block;
  body of NOTES otherwise untouched (line numbers shifted by 8).
- Targeted re-review 2 (adversary): `1. closed in all states`. Docstring fix verified by
  byte-level check ('540' absent from the script) plus double no-other-change confirmation (file
  size identical at 29,160 bytes — equal-length replacement; all Round-1 feature lines verbatim:
  part (a) assertion family, the three part (b) upper tuples, part (c) engines/ladder/budget
  ratio/s*/fire assertions/ℓ table); own re-run of the default budget: ALL PASS, exit 0, 150.6 s,
  ladder {20,22,24,26}, H0=26 counts identical to all rounds. One nit newly introduced by the
  Round-2 correction entry itself: NOTES:57 hard-codes the shipped JSON's wall clock ("150.7 s")
  while that JSON is overwritten by every run (153.3 s at 03:40 after NOTES finalised 03:37; 150.6 s
  after the re-reviewer's run) — per-rung counts are deterministic and never change, only c_total_s
  refreshes; non-load-bearing, does not block acceptance, one-line fix. All Round-1 findings (1
  MEDIUM + 4 LOW + 2 INFO) and the Round-2 docstring item are closed; no load-bearing reservations.
- Summarizer checks this round (byte-exact, Python312 −I; full script NOT re-run by the summarizer
  this round — the only script delta is the one-line docstring string, and the re-reviewer's ALL
  PASS 150.6 s run plus the verification gate cover it; the summarizer's own 150.4 s run of the
  round-1-revised script is on record above): script:4 reads
  `[total_budget_seconds=480]` and the string '540' occurs nowhere in the script; script size
  29,160 bytes; NOTES:51-57 is the Round-2 correction entry with the "150.7 s" hard-coded wall
  clock at :57; shipped t4_horizon_checks.json: result PASS, c_total_s 150.6, ladder {20,22,24,26},
  H0=26 counts 22,369,619/25,074,248/7,594,491/595,760/7,594,490/67,108,862/29,990,130/22,783,474/
  max v 25 — identical to every round (deterministic; only the wall-clock field churns, confirming
  the nit's diagnosis).

VERDICT: ACCEPTED (round-1 acceptance-in-part discharged: all 7 patchItems applied and verified,
targeted re-review 1 `1. closed in all states`; round-2 docstring item applied and verified,
targeted re-review 2 `1. closed in all states`, no load-bearing reservations; verification gate
ALL PASS on re-run). [A] Theorem H-T4 — F defined for every s with 3s+4 < 2^T4 and #1 non-halting in
the first 2^T4−2 top steps, relative to the accepted imports (EXT-T4 non-circular three-range
composition, DATA-T4 locality, the U(b)/Corollary H replay, and the τ(J−1)<τ(ρ) strictness
strengthening all confirmed); [A] Lemma EXT-T4 (J≥1), Lemma DATA-T4, Lemma HINQ (H≥16, real-H
instance at T4); Lemma ORD's eight order relations on the repo constants — now with the note's own
[B] verification valid on the corrected series. [B] the machine-level validation of the H-CLOCK
transfer pattern at H0∈{20,22,24,26} (extended 28), independently reproduced by both blind auditors.
**On this acceptance the repository's accepted horizon becomes 2^T4−2 top steps / (2^T4−4)/3
F-steps** (superseding 2^K_clock−2), per NOTES §7's stated condition. Route R1's gap is closed.
Remaining for a future touch (non-blocking; round cap 2 reached, no further re-review round):
NOTES:57's hard-coded "150.7 s" wall clock for the shipped JSON should be dropped or replaced by
"see its c_total_s" (the JSON's c_total_s refreshes on every run; the per-rung counts are
deterministic). No claims beyond J<T4: no T5, no J≥T4, no global EXT*/non-halting; the level method
beyond T4 still does not stabilise.

## Round 3 addendum (2026-11-14): independent Claude adversary (coordinating session)
Rounds 1–2 above used a GLM adversary and a GLM auditor (same family as the author) plus one agy auditor. The
coordinating Claude session re-ran the verifier and added an independent Claude adversary.
- Claude adversary: `2. fixable gaps`, no fatal flaw. MEDIUM: tag must be [A + imported A+B] (Theorem T4's zero-margin
  [B] level computation); MEDIUM/LOW: "T4 irrational" unproved and "v <= T4−1" false for non-integer H — replaced by an
  argument valid for any real T4. LOW: ladder one F-step short (s* fixed to M; re-run ALL PASS, ladder {20..28}); the [B]
  ladder exercises only range 1; uniform non-circularity paragraph; comment typos. Confirmed: induction order, range
  hypotheses, ORD by hand, HINQ, off-by-ones.
- Patch: Round-3 block in NOTES.md; script line fixed.

REVISED VERDICT: ACCEPTED. **Theorem H-T4 [A + imported A+B]**: F is defined for every s with 3s+4 < 2^T4 and #1 does
not halt in the first 2^T4−2 top steps. The accepted horizon becomes 2^T4−2 (was 2^K_clock−2), inheriting Theorem T4's
[B] level computation and its zero margin.
