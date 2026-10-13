2. with fixable gaps  (Adversary: Claude, 2026-10-13; condensed by coordinator)

Holds: reachable entry states equal COVER exactly (any-j θ=2,0,1 first return; θ=3,1,−1 second;
specific (A0∪A1)−1, A0−2, A0); A0/A1 (27/46) match definitions; real-walk data to 10^6: every odd
b-crossing copies a fire (302,878), every odd c-crossing copies an a-output (θ=2: 15,822; θ=1: 28);
H = 2^(N/2−2) exactly; log2(6K²) = H − 1.415; j2 ≤ ~999997.58 < N; rescue crossing data and algebra
exact; h-changes +11,−2,+3; 21 steps; two-a lemma correct (unused by §4); no circularity.

Defects:
1. "c-copied chain is an a-output" unproved for crossings n ≥ N (inherited from EL Thm D, only data
   to 10^6). Fix: PROOF_M Lemma 3.3 + §3: top-level odd step is a fire (empty list) or a return chain;
   Lemma 2.3 return lists have length 1 only for type a with R = ∅ ⇒ odd type-c crossing (P=[Y]) sits on
   an a-return chain. Write into §4.
2. σ > 17 never derived where the macro is invoked. Cite Theorem M's σ_t ≥ ρ − t(1+E) > g ≥ j_t (or
   h ≥ 1 ⇒ J−Γ ≥ 18); note σ−1, σ−2, σ−4 stay above 5, 6, 1.
3. After the non-NT step (5,5)→6 the real Θ₂ = 2^17 z + 46 ≡ 46 (mod 64) but the automaton rule gives
   3−5 ≡ 62. Harmless below K (rescued epochs need J ≥ H; any c-copy from J < K copies J_W ≤
   log2(3(J−1)²+4) < H), but the lemma "rescued chains are never copied below K" must be stated —
   it is exactly the obstruction at the next tower level.
4. Finite-horizon deficit bound not re-derived for r ≤ 6 (EL Cor. E used a_t ≤ 4; constant 31 in
   Δ ≤ 31+ε(J−1)+j changes). Still fits ⌊log2 i⌋² for i > 10^8 — show the recomputation.
5. Tie-freeness switched from Lemma T's size margin (EL Thm D) to Theorem B's h-induction + macro;
   valid, but state the switch (the d-bound of Thm D does not extend to J < K).
6. Wording: §4 c-case "through theta=1" should also cover W-epochs below N whose copied first a-return
   is a specific A0 entry; §3 "prior symbolic margins" → "under the margin hypotheses of §4".
