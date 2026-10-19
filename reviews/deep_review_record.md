# Three-way review of work_deep (external ZCode agent), 2026-10-20
Reviewers: adversary = Claude subagent (scratch aud59; Bad_j recomputed independently for j=5..27); auditors 1, 2 =
agy gemini-3.8-flash-high, both blind (aud57, aud58). Patches applied by a Claude editor subagent at the coordinator's
request; final two wording leftovers applied verbatim by the coordinator.
- Adversary: `2. with fixable gaps`. Stands [A]: Lemma 2.2 (deep-segment trichotomy; CLOCK applies at reached n_t),
  Lemma 2.3 (resonance isolation: θ′=3+3k>0, next z>=9), Lemma 2.4 count <=2Λ+1, Lemma 2.5 (lift bit −2^{j′} ≡ +2^{j′}
  mod 2^{j′+1}), Lemma 2.6 (τ = τ(j_t−1), bounded by CLOCK), Cor 2.7 on the initial deep segment, Thm 3.1, Thm 3.4 as
  conditioned. [B] (6) confirmed. Fixes: Thm 3.4 scope (6Λ(J)+4<=B; DEEP(i) a hypothesis above); Λ(K_clock)=4, not
  5·10⁵; L(j) off-by-one; Lemma 2.1 constants; Cor 2.7 scope; R1 formula 3τ+4+λ_Y; Remark 3.2 not a theorem; Lemma 3.1
  at t=0; Thm 3.1 wording; overclaims of the "single congruence" equivalence.
- Auditors 1, 2 (gemini): both `2. with simple errors` (L(j) off-by-one; single-congruence overclaim); Bad_j
  recomputed for j<=20/22 and j<=18 plus j=19..27 step types, all matching.
- Patch: all items applied; new [A] "Size of Λ" block (tower T_h; Λ(J)<=h for J<T_h; Λ(K_clock)=4; Thm 3.4 holds for
  J<T_{⌊(B−4)/6⌋}); reviewer observation as Remark 2.8 [C]. Targeted re-review: new [A] material verified rigorous
  (bounds on L, tower recursion, both bounds on Λ(K_clock)); one justification reworded (P(n)<=n for n>=N₀−1 via the
  Lemma 2.1 log-derivative bound). Final: closed.
VERDICT: ACCEPTED. For every J < T_{⌊(B−4)/6⌋} (includes J≈K_clock, where Λ=4): EXT(J) ⟸ R1 ∧ R2, with R1 = no
deep→deep c-step, R2 = landing class certified (exhaustively a single first-chain-tie congruence only for odd-a j_u
in 22, 24, 27 within 18..27). Remark 2.8 [C]: with Λ small, a/b landings may make R2 automatic — open. EXT open;
K_clock unchanged.
