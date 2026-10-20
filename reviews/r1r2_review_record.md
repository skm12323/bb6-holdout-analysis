# Three-way review of work_r1r2 (external ZCode agent with three sub-agents), 2026-10-20
Reviewers: adversary = Claude subagent (scratch aud62; corrected rerun of the V6 scan, 13.5M b/c steps, 0 failures);
auditors 1, 2 = agy gemini-3.8-flash-high, both blind (aud60, aud61). Patches applied by a Claude editor subagent;
the corrected verify_r1r2_big.py was rerun on a copy (19,999,995 m, 0 failures, 68 s) and its json installed.
- Adversary: `2. with fixable gaps`. Stands: exact drift θ_t=2i−t+1 under R1 (incl. resonant steps); no resonance
  and <=Λ deep chains (with R1 as hypothesis); R2 automatic for a/b landings when Λ<=13 except bare ties (landing
  non-resonant ⇒ exact class, no lift-bit issue); bare-tie two-step gateway (classes (10−2^m)/3, (26−2^m)/3 mod
  2^{m+1}, strict record descent); [B] certificates; c-landing δ formula and Lemma 5.3; source identity, SIZE/CANCEL.
  Fixes: MAJOR overclaim of Cor 2.6 for T₄<=J<T₁₃ (bare ties with m>=10⁸ uncovered → RES); Thm 2.4 proof for
  N₀<=m<10⁸; code precision bug at b/c steps; R1 ⟸ (CAL-C′)∧(NC) only, R1 ⟸ CAL-C for a single J; R1 needed in
  Lemma 1.2/4.1; small arithmetic/sign statements; scope of the 8,712 count.
- Auditors (gemini ×2): `2. with simple errors` (same overclaim; R1 in Lemma 1.2/4.1; |θ−3/2| bound; CAL-C ⟹
  direction needs Lemma 4.2's drift condition; arithmetic). Recomputed drift words to length 14, 2000 random bare-tie
  states, certificates m<10⁵ and m<10⁶, δ formula and Lemma 5.3 on real c crossings — all matching.
- Targeted re-review (adversary): `1. closed in all states` (new [A] argument for RES vacuity below T₄ verified).
VERDICT: ACCEPTED. For J < T₄ (Λ<=4, includes K_clock): EXT(J) ⟸ R1 ∧ R2_c. For T₄<=J<T₁₃: EXT(J) ⟸ R1 ∧ R2_c ∧ RES
(RES: no a/b bare-tie landing with m>=10⁸). R1 ⟸ CAL-C (no odd c crossing X(n), n>=N₀−1, with 2^{N₀} | 3τ+4+λ_Y);
R2_c ⇔ τ(n_T) avoids an explicit congruence (δ ≡ θ_T+3τ+3−2^{j_u} mod 2^{j_u+1}), with the Lemma 5.3 two-step
bypass. EXT open; K_clock unchanged.
