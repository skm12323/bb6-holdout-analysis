# Invariant Checkpoint — `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`

HALT = F reading 0. Source: bbchallenge 815 holdout list (user-supplied candidate #1).

## ACCEPTED: Reduction Theorem (Stage 3 passed)
Files: `work_r1/RULES.md`, `work_r1/verify_r1.py`.
- Encoding: (h; r1..rk) = `0^∞ 1^h [0]_A 1^r1 0 … 0 1^rk 0^∞`.
- Rules R1–R5 and HALT pattern (0;1,0,r3,…), proved for all parameters; invariant I includes the clause k=1 ⇒ r1≥2; the coverage lemma is exact.
- Base: blank tape reaches (0;3) at t=5. This is the single Class-B item.
- Top map L=(A,b,c,S):
  - A even → (A+b+c+3, S).
  - A odd → odd chain on m = b+(A−3)/2.
- **Halt ⇔ some top step has A odd and A+2b+3 a power of 2.**
- Sum invariant ΣL_n = 3n+3; therefore single-element lists never halt.

## Review trail
- Adversary: fixable gaps (I-K1, DOM, H-EQ).
- Auditor 1: all correct (281,892 rule checks; 67,067 coverage configs).
- Auditor 2: all correct (119,999 top-map cases incl. 11,321 halting; sum invariant to n=10^6; raw TM to 3.1·10^6).
- Patched; targeted re-review: **closed in all states**.

## Open
Non-halting ⇔ A+2b+3 is never a power of 2 at an odd-A top step. Path R4 (inductive closed form for L_n) is in progress.

## Class-C evidence
- No halt for 10^7 top steps (≈1.3·10^21 TM steps).
- Odd-A events occur in nested residue families (n≡33 mod 64, 3 mod 512, 7 mod 8192, …).
- In every observed case X = 2^v·u with u odd and u > 1.

## FINAL ARBITRATION — #1 CLOSED AS FAILED (UNDECIDED)
- R4 (work_r4/PROOF.md): singletons never halt; excursion entry E(w,v) closed form; Lemma E(v) symbolic for v≤2000 ⇒ no halt for top steps n < 2^2001−2. Self-tagged Class-A; NOT Stage-3 audited.
- R5 (work_r5/PROOF.md): generalized F(s) [A, s≤1000]; Lemma R / Corollary M(s') [A, by hand]; F′(s) odd-Z₁ variant [A, s≤300]. Residual gaps G1 (margin bound p(s)), G2 (end-phase with odd perturbed entry at Z′₂…), G3 (initial phase) unclosed.
- Exact residual: end-phase statement ⇔ F(s) ∀s ⇔ E(v) ∀v ⇔ non-halting. Assessed as 2-adically insulated (not Collatz-like) but the recursion never closes into finitely many cases.
- Pre-declared closure rule applied: one final push permitted, gaps remain ⇒ archive. Status: UNDECIDED.

## Reopened attempt R6 (work_r6/) — no closure
- No new Class-A results. Simulation results (no halt n<3·10^5; residue table; near-halt locations) are Class-C (self-tagged B, regraded).
- Simple 2-adic invariant (c) refuted: x=A+2b+3 ≡ 0 mod 2^k occurs for all k≤8, so congruence-only invariants cannot work.
- Near-halts with odd part q≤7 occur only at singleton steps n=2^k−2 (proved non-halting); elsewhere q≥9 observed. Lead: an invariant bounding the odd part of x below, away from singletons.
- Approaches (a) symbolic-v and (b) binary closed form not executed (no viable induction hypothesis found).
- Residual unchanged: Lemma E(v) ∀v>2000 ⇔ R5 gaps G1/G2/G3. R5 judged it "not Collatz-like"; R6 judges it Collatz-like/open — assessments diverge; status remains UNDECIDED.

## Attempt R7 (work_r7/) — odd-part invariant, no closure
- Exact q at singleton steps: q=3w [A]. At Lemma-R steps: q = 3H/2^{s'} + (d+3)/2^{s'} ≥ 7 when j>s' [A by hand, depends on unaudited R5].
- Inside E(w,v), v≤1000: q affine in u with β≥19 [A per v; no new range beyond R4].
- Refuted (C): odd-modulus congruence conditions on x (16 moduli) — residues insufficient; bound must be size/valuation-based.
- Conjecture C7 [C]: at every non-singleton odd step, v2(x) ≤ ½·log2 x (observed min q=19, q ≥ 1.54√x, n<3·10^5).
- "q≥3" not inductive alone; closing it requires exactly R5 gaps G1 (margin j>s') + G2 (nested/end-phase steps).
- Status unchanged: UNDECIDED. Four consecutive paths (R4–R7) converge on the same residual.

## Stage 3 on R4 finite-range theorem — ACCEPTED
- Adversary: `1. closed in all states` (singletons, excursion entry incl. v=1/v=2/w=1 edges re-derived by hand; stop_sym decisions uniform ∀u≥0; RULES §5 fidelity; bound v₂(n+2)≤2000 with no off-by-one).
- Auditor 1: `1. all correct` — independent symbolic executor, v=1..2000, no abort/halt, ℓ(2000)=1780; concrete orbit n<10^6 (339,503 excursions) matches decomposition.
- Auditor 2: `1. all correct` — 204,900 concrete runs (v≤60, adversarial w up to 2^200); min odd part of A+2b+3 = 19; raw TM vs top map first 52 configs.
- **THEOREM (audited): the TM does not halt during top steps n < 2^2001 − 2.** Lemma E(v), v≤2000, is a mechanical certificate (verify_r4.py check1, independently reproduced). Base: RULES.md (audited).
- Note: TM-step equivalent is t(2^2001−2) via exact RULES §5 step costs (≈1.35n³, i.e. ~10^1806 TM steps); no explicit number certified.
- Global status: UNDECIDED (Lemma E(v) ∀v open; gaps G1/G2).
