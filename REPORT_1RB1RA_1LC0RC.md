# Arbitration Report — `1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB` (candidate #2)

**Status: UNDECIDED — closed as FAILED.** The machine is reduced exactly to an arithmetic stack machine; the halting condition is open. HALT = C reading 0.

## Accepted theorem (Stage 3 passed)
Files: `work_s1/RULES.md`, `work_s3/RULES.md`, `verify_s1.py`, `verify_s3.py`.

- **Halting criterion [A].** Halt ⇔ the TM reaches `[A]0 1 0` or `0 0 [F]1`.
- **Phase system (S1) [A].** The TM is reduced to phases K/S/P with rules Ka…P5, SH, PH. Coverage holds; the "F runs left forever" branch is vacuous.
- **Σ-machine (S3) [A].**
  - **State.** Σ(p,N,m;W), where W is a stack of entries (g∈{1,2}, d≥1).
  - **Base [B].** The TM reaches Σ(3,0,0;∅) at t=8.
  - **Step table.** 13 rows, each derived by hand from S1 rules. The case split is exhaustive and unique.
  - **Invariants.**
    - I1: p ∈ {3,6,8,9,…} and (p,s) ≠ (3,2). Consequently PH never fires.
    - I2: only the top entry of W is read.
- **Theorem H [A].** The TM halts ⇔ the orbit reaches an empty-stack state (p,1;∅) and either:
  - p ∈ {3,6}; or
  - p ≥ 8 and the run from Σ(6,p−7,0;(2,1)) eventually empties its stack.
- **Lemma N [A].** Predecessors of s=1 at an empty stack have s ∈ {2,5,6,7,9} (⊆ only).
- **Span law [A].** The span never decreases. No conserved quantity rules out halting.

Gate: C=0, B=1.

## Review trail
- Adversary: fixable gaps (D1–D6). Auditor 1: all correct (169,104 Σ states; S1 rules for parameters 0..30). Auditor 2: simple errors (span-law Gs1_3 increment; 7,044,374 coverage states; orbit to 10^7 TM steps).
- Patch by S3, including a hand derivation of all 13 rows (D6).
- Targeted re-review: fixable gaps (blank-top span increments; D3 stated too strongly; S1 §4 closing sentence). The coordinator applied the adversary's prescribed wording verbatim. All 13 rows were re-confirmed by hand and by 3,430 raw runs.
- **Accepted.**

## Open problem
Show that the sequence of empty-stack states never produces the halting configuration of Theorem H.

Evidence (Class-C):
- No halt in 2·10^6 macro events (~9.4·10^16 TM steps).
- Near misses (s ∈ {2,5,6,9}) arrive at a rate of about 1/span, so their expected count grows only like log. A probabilistic argument does not settle the question.
- No congruence invariant mod 2, 3, 4, 8, 12 or 16 excludes the dangerous values.
