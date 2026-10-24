# Three-way review of work_gateway_trains (external ZCode agent, directions B+C), 2026-10-24
Targets. Group 1: NOTES.md, CONTEXT.md, RECORD_BUDGET.md (+budget_ledger.py), B_rank/B_RANK.md (+train_checks.py),
C_climb/C_CLIMB.md (+climb_checks.py). Group 2: review_trains/REVIEW.md, the dispositions of nine GPT-Astra documents
in work_c3_drift/ (GATEWAY_TRAIN, CLOCK_FILTERED_TRAIN, TRAIN_CLOCK_ORBIT, CROSS_SCALE_TRAIN; DEPTH_CLOCK_BUDGET,
SEED_BUDGET, COPY_BUDGET, JOINT_HEIGHT_BUDGET, STOP_CHECKPOINT_2026_10_21).
Reviewers: adversary 1 = Claude subagent (aud80, group 1; gates rerun PASS, climb_checks 115,121/0); adversary 2 =
Claude subagent (aud81, group 2; ten Astra verifiers rerun PASS, own epoch walk to 2·10^6, own GATEWAY graph,
independent cross-scale replay); auditors 1, 2 = agy gemini-3.8-flash-high, blind on group 1 (aud78, aud79).

- Adversary 1: B, C, RB, consistency, gates all `2. with fixable gaps`. HIGH: RECORD_BUDGET "tower descent" and
  T<=Λ(y_1)+O(1) hold only for the first gate (C4 needs y>=N0 and |D_y|<=5; later gates have y<<N0 and |D|~2^m/3;
  |D_y|<=5 comes from Theorem L, n+1<T4); the failure modes F1–F3 are not exhaustive (F4 large ancestral defect,
  F5 non-tie NT gates at j>=6, F6 empty-run gates that are never run-paid — 45/46 ledger gates are unpaid), so
  "train length bounded by (e)" is circular. MEDIUM: Ledger wording (non-increasing, one-step descent keeps R); toll
  margin ~8·10^4 by averaging, not 2·10^7; C6 conflates two meanings of sigma; B5's "moving residue" is a coordinate
  artefact (fixed residue D≡−3k in class coordinates); B1 corollary only [B]. LOW: C4 uses D2 [B]; B3 structurally [A]
  for b crossings (lambda_Y≡0 mod 16); rigidity labels; weak gate checks. Confirmed: B1 (k≡22/6 mod 32, 5↔21
  alternation), B2/B4/B6, C1, C3 (S≠0), C5 (single residue, w<=1), r=1 degeneration to Lemma CB, Ledger identities,
  and that run-paid ⟹ descent is NOT the refuted tie→tie record law.
- Adversary 2: `2. with fixable gaps`. All nine dispositions (four ACCEPT, five conditional) are right; no refuted
  statement used. Review-text errors: the MED-1 "fill" (2²-jump / weights[2]=10) is a misreading — the original
  reason (a J=3 epoch occupies 5 pointers; odd type-a crossings are fire pointers, proved structurally) is complete;
  CF-8 "crossings of an epoch share the fire time" is false (the reason is monotonicity of s); CS-1 pointer typo.
- Auditor 1: `2. with simple errors` (strict-NT r-period is 2^{j−3−v2(3k)}; B1 corollary [B] not [A]).
  Auditor 2: `1. all correct` (missed the HIGH items). Both recomputed B1, B5, C1/C3/C4, the Ledger on (73515,98094).
- Patches (coordinator): review-correction blocks at the head of RECORD_BUDGET.md, B_RANK.md, C_CLIMB.md, NOTES.md
  (override the body); REVIEW.md MED-1 (downgraded to LOW, reason restored), CF-8, CF-9, CS-1 and status lines fixed.
  Targeted re-reviews: remaining items (C6 restriction to r=1 C entries; (iv) certification set scope; MED-1
  contradiction; NOTES §2 stale phrase) fixed.

VERDICT: ACCEPTED in part.
Group 1: B1 (tie classes alternate 5↔21 mod 32, k≡22/6 mod 32) [A]; B2/B3 (no internal B-return; b crossings
structurally [A], 28 c labels [B]); B5 restated as the fixed residue D≡−3k (mod 2^{j−2}); C1, C3, C5, C4 [A-cond D2]
(first gate only), C6 for r=1 C entries; the Ledger identities; Theorem RB only as a conditional statement for the
first gate plus explicit hypotheses (ii)–(iv) and D5. Failure modes F1–F6 (not exhaustive claims). The unbounded-train
question, later gates, empty-run gates and non-tie NT gates remain open.
Group 2 (work_c3_drift): GATEWAY_TRAIN, CLOCK_FILTERED_TRAIN, TRAIN_CLOCK_ORBIT accepted [A]+[B]; CROSS_SCALE_TRAIN
accepted as a construction (non-canonical start); the five budget documents accepted as conditional/segmentwise
results, not global ranking functions. EXT open; K_clock unchanged.
