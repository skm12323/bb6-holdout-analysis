# Invariant Checkpoint — `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---`

Source: user-supplied candidate list (in bbchallenge 815 holdouts). HALT = F reading 1.
Status: **UNRESOLVED (non-halting not proved)**; reduction theorem draft submitted to Stage 3.

## Main-theorem draft (Reduction Theorem) — admissible set: A=3, B=1, C=0
- **T1 [A] Macro rules** R1, R2, R2′, R3, R3″, R3k, R4, R5 on block lists (blocks of 1s separated by single 0s; A-phase / D-phase), symbolically proved for all parameters with exact step counts (`work_q1/verify_q1.py`).
- **T2 [A] Halting lemmas**: halt ⇔ `D> 0 1`; entry patterns `B> 0101` and `0 1 <A 1`; D-wave halts on `0 1 D> 1^{a+1} 0 1 0 1`.
- **T3 [B] Reduction**: from t=1466 (blocks [10,9,11,0,4,2], A at block 3) the abstract map matches the TM at all 14,526 checkpoints to t=3·10^6; uncovered cases (D-wave meets last block of length 1; R2′ with j=1) never arise in that range.
- **T4 [A | T1–T3] Block halting criterion**: halts iff a D-wave meets a non-last block of length 1 to its right (incl. R3 with k=1 not last).

## Excluded from draft (Class-C)
- No halt in 3·10^6 macro steps (~2.09·10^10 TM steps); 26,766 D-waves; min interior block right of a wave start = 4.
- Conjectured invariant: a 1-block is never left right of A when a D-wave starts — Collatz-like dependence on parities of n-blocks; open.

## Open gaps
- Non-halting invariant (main open problem).
- Uncovered cases of the map beyond 3·10^6 macro steps must be handled symbolically (or shown unreachable) for T4 to be unconditional.
- Equivalence of siblings `1RB0LD_1LC1RD_0LE1LA_0RB1RD_---0LF_1RA1LF`, `1RB1RA_1LC0RC_1RE0LD_0RE0LF_1RA---_1RB1LF`, `1RB1RC_1LC0LE_1RD1RC_1LB0RA_---0LF_1RD1LF` — only Class-C evidence (same tapes at left-edge events).

## Stage 3 result — FUSE RESET (draft discarded)
- Adversary: `3. structure broke`. T4 "iff" false as stated: R2′ with B[1]=1 (`0^∞ 0 <A 000 1 0 1^{m+1}`) halts in 14 steps for all m but was filed "uncovered/never arises" (D1); D-wave meeting last block of length 1 unresolved (D2); T3 is finite (B), so T4 is at most B (D3); T2 entry-pattern list incomplete — keep only `halt ⇔ D> 0 1` (D4); block invariants (non-A blocks ≥1, A never last) unstated (D5).
- Auditor 1: `2. with simple errors` — rule statements missing from checkpoint; `0 1 <A 1` head position ambiguous; t=1466 tape has a 4-zero gap vs stated [10,9,11,0,4,2] (encoding unstated).
- Auditor 2 (arrived after reset): `2. with simple errors` — independent jump-vs-raw comparison matches at 1,572 points to t=3·10^6, no halt (to 10^8 TM steps); under its wave definition, D-waves meeting a last block of length 1 occur 540/810 times (non-halting), contradicting "uncovered case never arises" unless conventions differ; interior block set to 1 → 75/75 halt (supports T4 core); block immediately after `00100` set to 1 → 27/27 no halt (T4 wording too broad); "3·10^6" ambiguous (TM vs macro steps).
- Surviving material (reusable, not a theorem): T1 macro rules (adversary found no error), `halt ⇔ D> 0 1`, `B> 0101` halts, D-wave halt lemma (audited a=0..30, a-independent path).

## Arbitration log
- Q1 symbolic: produced T1–T4; non-halting open.
- Q2 CTL/RepWL: broken (fixpoints n=1..20 reach halt); lemma `B> 0101` halts, confirmed by Q1.
- Q3 isomorphism: Class-C only.

## Round 2 (after fuse reset)
- **Q4 Reduction Theorem v2** — full statement in `work_q4/RULES.md`, checker `work_q4/verify_q4.py`. Gate: A=all, B≤1 (L3 base, 21 steps), C=0 → **PASSED, submitted to Stage 3**.
  Halting set H (block terms): (A,i=0,b0=0,b1=1,m≥3) | (A, b_i=1, i+2≤m−2, b_{i+2}=1) | (D, i+1≤m−2, b_{i+1}=1).
- **Q5 abstract-map lemmas** (built on Q1 rule set, NOT yet re-based on Q4 rules incl. R6/X0/H2): I (blocks ≥1, tail `4,2`), G (right-end gadget), S (sweep leaves blocks ≥2), E (left-edge halts iff u0+2 = 2^k). Claimed: halting ⇔ some left-edge arrival u0 ∈ {2^k−2}. Held back from draft pending re-basing.
- Class-C: 7 left-edge arrivals in 3·10^6 macro steps, u0 = 23,21,24,104,1290,647,7146 — none of form 2^k−2.

## Round 2 Stage 3 — arbitration
- Adversary: `2. with fixable gaps` (STEP-BOUND, L1-SCOPE). Auditor 1: `1. all correct` (12 rules × params 0..25; 29,300 configs; 14,583 checkpoints to t=3,000,078). Auditor 2: `1. all correct` (30,001 checkpoints to t=9,999,753; 3,896,712 configs m≤7, blocks≤6; all 15 rows exercised).
- Local patch (Q4): STEP-BOUND (≥7), L1-SCOPE decision tree, CONV, SEM, R3-IDX.
- Targeted re-review: `2. with fixable gaps` — SEM note wrongly called [1,2,1,1] A@2 "H2-shaped" (it is R3''-shaped; i+2≤m−2 fails); R3-IDX clause needed "for i≥1". Both fixed by coordinator using the adversary's prescribed wording verbatim; verify_q4.py re-run clean.
- **VERDICT: Reduction Theorem v2 ACCEPTED** (C=0, B≤1). Machine halts ⇔ M-orbit from ([1,1],A,0) hits H.
- **Machine status: still UNDECIDED** — non-halting requires proving the orbit avoids H (open; Q5 indicates reduction to left-edge values u0 ∉ {2^k−2}, to be re-based on v2 rules).
