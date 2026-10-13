1. all correct

1. Copy rule: DERIVED, not measured. λ_{u′} = λ_{u_W} + (c_W/2^{j_W})·λ_u is exact M_u-image algebra at every index; v2(c_W/2^{j_W}) = σ_W−j_W, and λ_u odd gives the ≡ λ_uW + 2^v (mod 2^{v+1}) congruence. Real-walk values (w, ω, λ_uW, σ_W) enter only as parameters, used at n < N. It IS applied at n ≥ 10^6: a level-3 fire's c-copy sits at n = J−1 ∈ [K−1, K′−1), but there only the derived θ-shift/δ-record form and S-c bounds are used (S-c re-checked: j ∈ R_2 ⇒ log2(3K²) = H−2.415 < H). Sound.

2. Coverage: the entry windows are exactly the shift-closure — R_1 min = −1+1−2 = −2, max = 3+3−2 = 4 (level-≤0 a-outputs θ_W ∈ {1,2,3}); R_2 {0,2} only from chain-1 a/b routes; post-large chains have i′ < i, so ≤ 2 large chains ⇒ r ≤ 2+1+4 = 7. θ = −3, 5 can appear only inside runs, never as entries; excluding θ = 5 is exactly what dodges the level-4 failure. Records: z-independence confirmed numerically (Θ1 = 2^17z+37, Θ2 = 2^17z+46, u1 ≡ 2049 mod 2^12, u2 ≡ 513 mod 2^10), and j2 = 6 ≪ 17 pins 46 (not the rule's 62). Counts "6", 13,949, 7,000,101 are [B] bookkeeping (unreproducible blind); "64 vs 68" is dedup drift vs PROOF_RESCUE §3 — cosmetic.

3. Bounds ✓: log2(3K²) = H−2.415 (since log2 K = H/2−2, not K−2.4≈log2(3K²)); log2(6K′²) = K−1.415 < K; R_2→J_W < H, R_1→J_W < N (log2(3H²) = 999997.6 < N); the no-copy threshold 2^{(K−2)/2} = 2^{1.21}·K′ > K′.

4. Margins: landing on (5,5) forces k_{j_e−1} ≡ 6 (mod 32) (verified: v2(x1) = 5 + Θ1 ≡ 5 mod 32 force it), hence n ≥ 11, j_e ≥ 12, so the (AA) two-step range applies. h(5,5) = h_e+j_e−6 ≥ 1, and the tie step gives h_2 ≥ h_e+1 ≥ 2 since j2 ≤ j_e−3: no dip below baseline. No-circularity ✓ (item 3).

5. Deficit ✓: Δ ≤ 16+49+(J+3log2(6J²))/4+J ≈ 1.25J+67+1.5log2J < 1.3J+100 < (J/2−1)² for J ≥ ~26 (checked at 10^6, 2^20, 10^12), and log2 i ≥ J/2−1 from 3s+4 ≥ 2^J, s ≤ i².

6. Re-derived & verified numerically: (AA) with l = 1 gives x2 = Θ+12+9k+2^{j_e−2}u, B = Θ+12+9k ∈ (0, 2^{j_e−2}) ⇒ j2 = v2(B) = v2(θ_e+12+9k) ≤ j_e−3. Since 2B ≡ 0 (mod 2^{j2+1}), 3Θ2 ≡ θ_e+12 (mod 2^{j2}), i.e. Θ2 ≡ (θ_e+12)/3. For 10/3: every tie entry has Θ_e ≡ −2 (mod 2^{j_e}) (minimal θ_e = −2; the records (5, 37+δ) give j1 ∈ {2,6}, NT, never a tie), so outputs ≡ 46 = 10/3 (mod 2^{j2}); 3·46 = 138 ≡ 10 (mod 64), and 10/3 mod 2^14, 2^19 = 10926, 174766 matches §7. Corollary: 10/3 ≡ 14 ≢ −2 (mod 32), so no post-tie chain re-enters (5,5) — one tie per run.

Caveats: the j_e ≥ 12 / |θ_e| ≤ 10 side condition for the two-step bound is implicit (satisfied by the actual tie list); [B] counts not re-verified (no .py/.json/log read or run, per instructions).
