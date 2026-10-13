**1. closed in all states**

**Defects: none.** Item-by-item:

1–2. §2 wording accurate. `verify_tie2.py` `go()` runs the extended automaton *only* when the old run fails; no coincidence check exists (grep-confirmed). `sigma_walk` asserts j<σ (line 60), cross-checks only j against `real_walk`; σ comes from the Lemma-3.2 ε-recursion, not recomputed. ✓

3. θ≥−2 with k≥1 ⟹ θ+3k≥1; θ=−3,k=1 → 0 justifies the fix; level-3 large windows ⊂ R_1[−1,3], R_2{0,2} ≥ −1. ✓

4. 3s+4≥2^J, s≤i² ⟹ log2 i≥J/2−0.8 (needs 2^J≥387, trivial for J≥K); floor > J/2−1.8; 1.3J+100<(J/2−2)² ⟺ J≥27.3; intermediate 1.25J+67+1.5log2 J<1.3J+100 holds for J≥K. ✓

5. 3(J−1)²+4≥2^K ⟹ 3J²≥2^K−4 ⟹ J≥2^(K/2−0.8)=2^1.2·K′>K′; R_4 remark matches §3's "R_i copies lw<i" rule and the J<K′ horizon. ✓

6. (S1)=j<σ (G6 §5.2); at the fire j₀=J, σ₀=ρ gives ρ>J; σ_t−j_t=ρ−J+h_t≥h_t. ✓

7. All five requested entries present; M2′/(S1) used in steps 6/4 are covered by "PROOF_M lemmas cited inline"/Theorem-M framework — naming them would be marginally cleaner, not a gap.

8. 13,943=13,940+3; 13,949=13,943+6; the six δ=−1 extended copies give 36 mod 32=4, 45 mod 64=45, both NT-safe. ✓

9. k≡6 (mod 32): derivation checks (3k≡18, 3⁻¹=11); E1 log: odd type-a n<40 = (4,1),(7,2),(11,4),(13,5),(16,6)… ⟹ first k≡6 (mod 32) is n=16 (stated n≥11 is conservative); 10/3≡14≢30=−2 ✓; post-tie outputs ≡10/3 with j₂≥5 — no re-entry; auditor-verified. ✓

Level 4 confirmed outside: §0.5, §6.3; §5 uses levels ≤3 only.

[exited with code 0]
