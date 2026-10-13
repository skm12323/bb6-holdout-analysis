2. with fixable gaps  (Adversary: Claude, 2026-10-13; condensed by coordinator)
Holds: verifier rerun byte-identical (levels 1–3: 7,000,101 entries, 0 failures, 0 branches, min h=1);
copy rule λ_u′ ≡ λ_uW + 2^v (mod 2^{v+1}) is EXACT (v2(c_u)=σ−j is a PROOF_M 3.2 identity), checked on all
7,910 real b/c steps; applied with real-walk parameters only at n < N; resolved ties re-run with random
high bits ×3 each — deterministic, ≤4 further chains, min h=1; COVER 68 raw entries = 64 classes mod 2^j
(the 5,000,063 vs 5,000,059 difference is 4 duplicate classes).
Defects:
1. §2 claims extended = old automaton wherever old reports no tie, but the script never checks it (sampled
   check agrees) — drop "checked" or add the check.
2. σ cross-check overstated: sigma_walk checks only j; σ rests on PROOF_M 3.2/3.3.
3. S-a lower end: θ ≥ −3 insufficient for θ+3k ≥ 1 (θ=−3,k=1 → 0); need θ ≥ −2 (harmless at level 3).
4. Deficit step 6: ⌊log2 i⌋ ≥ J/2−2 (not J/2−1); inequality survives (1.3J+100 < (J/2−2)²).
5. No-circularity: use J ≥ 2^(K/2−0.8) (from 3J² ≥ 2^K−4); state that large-state copies of a level-3 W
   need j ∈ R_4, outside the horizon.
6. Margin step 4: cite ρ > J (S1 at the fire) for σ_t−j_t = ρ−J+h_t ≥ h_t.
7. List inherited, not re-proved imports (PROOF_RESCUE location lemma and §4, (C1)/(C2), 10^8 base).
