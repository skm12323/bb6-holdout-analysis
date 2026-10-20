未经审查 / unreviewed — REPORT (DIRECTION B, R1), 2026-10-20. Details: NOTES.md; scripts+JSON in this directory.

# REPORT: R1 (no deep -> deep c-step)

**Headline.** R1 is not proved, and no counterexample or obstruction was found. It is replaced by a
strictly sharper [A] reduction (a pure canonical-calendar congruence, with the λ_Y-dependent part
eliminated in the case realized by all data) plus [B] evidence at N = 10^8: R1 holds with a margin of
2^{2·10^7-5}, and at deep type-c crossings the relevant valuation is never larger than 5. No claim on
EXT, on K_clock, or on the machine.

## Proved [A] (hypotheses stated in NOTES)
1. **c-step ledger** (Lemma 1). At a type-c step: R_{T+1} = R_T − (v₂(c'_W) − ω) ≤ R_T − 1, loss
   1+ε(n_T), parameter j_{T+1} = ω ≤ L(j_T) < j_T−2. So a deep→deep c-step is never an EXT-tie and
   never breaks the deep-chain count (work_deep Lemma 2.4 does not use R1).
2. **Exact new defect** (Lemma 2). θ_{T+1} ≡ θ_T + 3τ+3 (mod 2^ω); with ρ_ω its least residue,
   chain T+1 is deep ⟺ ω ≥ N₀ and ρ_ω ≤ B or ρ_ω ≥ 2^ω−B. Hence |θ_{T+1}| > B is **not** forced
   (Lemma 3 gives an explicit model satisfying every accepted constraint with ω = N₀ and
   |θ_{T+1}| ≤ B). R1 is therefore **not** equivalent to DEEP(i) failing; the exact drift hypothesis
   is R1* (c-step lands non-deep) or R1-C (|θ_{T+1}| ≤ B−6Λ−3), and R1-C ⟹ DEEP(i) on the initial
   deep segment (Prop. 4).
3. **R1 is a pure calendar statement** (Lemma 6). R1 ⟺ (CAL-C): no n ≥ N₀−1 with X(n) odd of type c
   has 2^{N₀} | (3τ(n)+4+λ_Y(n)). Proof: take J = n+1 (chain 0 is deep). Also ¬R1-at-T ⟹
   τ(n_T) ≥ (2^{N₀}−5)/6, so R1 is automatic for n < 2^{N₀−64}. (The task's "R1 ⟹ τ < (2^{N₀}−5)/6"
   is false; the true direction is the contrapositive.)
4. **Source identity and dichotomy** (Lemmas 9, 10; Cor. 11). For a type-c crossing with source
   parameter n' = j_{t'}−1 and odd base λ_u:
   λ'_W(n) = A − 2^{n'}λ_u, A := 6τ(n)+4−3τ(n'), with n' ≤ log₂(6τ(n)+5).
   Hence if v₂(A) < n' then ω = v₂(A) ≤ log₂A, else ω ≥ n'. If 2^{n'}∤A then R1 at n ⟺ 2^{N₀}∤A.
   Consequently R1's failure is **SIZE** (2^{N₀}|A, forcing τ(n) ≥ (2^{N₀}−4)/6) or **CANCEL**
   (2^{n'}|A and λ_u ≡ A/2^{n'} mod 2^{N₀−n'}).
5. **Minimality gives no contradiction** (NOTES §5.1): at a least counterexample the source epoch has
   J_W < J and is tie-free, giving ω < J_W ≤ log₂(3n_T P(n_T)+4); this is compatible with ω ≥ N₀
   (Lemma 3's model). The "descent tower" of source epochs terminates without contradiction — it is
   the PROOF_EXT §5 nested-copies obstruction.

## Reduced to what
R1 ⟺ (CAL-C) [A] ⟺ (CAL-C′) ∧ (NC), where (CAL-C′) is the pure τ-congruence
"2^{N₀} ∤ (6τ(n)+4−3τ(n')) at every type-c crossing n ≥ N₀−1" and (NC) is v₂(6τ(n)+4−3τ(n')) < n'
("no cancellation"). (NC) is what removes λ_u; it is a statement about the crossing calendar.

## Data [B] (canonical tables via fdata.lam_walk, N = 10^8; deep range [2·10^7,10^8))
- 1,267,918 deep odd type-c crossings (1,584,898 in all n < 10^8). ω = v₂(λ'_W) ∈ {1,3,5}:
  {1: 150569, 3: 1115171, 5: 2178} deep; max ω = **5**. #{ω ≥ 16,20,...,64} = 0. Type-b control:
  max ω = 26 with a geometric law — the type-c cap is structural, not generic.
- λ_Y ≤ 3τ+1: 0 violations (deep max λ_Y−3τ = −26,764,118). max τ = 89,213,529; max λ_Y/(3τ+4) ≈ 0.5.
- Lemma 9's two identities verified exactly at **all** 1,584,898 crossings (source chain obtained from
  an instrumented walk). 2^{n'}|A: **0 occurrences**; monotone: v₂(A) < n' always, min(n'−v₂(A)) = 1.
  So (NC) holds throughout and ω = v₂(A) ≤ 29 (A ≤ 535,281,166). Every ω=5 crossing has n'=13 and
  τ(n) ≡ 31 (mod 64).
- Direction-C datum: deep type-c landing classes with θ_T ∈ [−30,30]: certify fails only at ω=5,
  with θ_T ≡ 6 (mod 16) (all 2,178 ω=5 crossings, since base ≡ 0 mod 64 there); θ_T=1 never fails
  (0/1,267,918); Bad₁=Bad₃=∅, Bad₅={5,21,37,53} mod 64.

## Single most promising next step
Prove **(NC)**: v₂(6τ(n)+4−3τ(n')) < n' at every type-c crossing (n' ≤ log₂(6τ(n)+5)). That would
turn R1 into (CAL-C′), a congruence in τ alone, with no λ-data — a target of the same type as the
already-accepted CLOCK/calendar statements and directly testable by any future calendar generator.
Second choice: prove R1* instead of R1 via the landing-residue form of Lemma 2 (ρ_ω near 0 mod 2^ω),
which is weaker than R1 and still suffices for Theorem 3.4.
