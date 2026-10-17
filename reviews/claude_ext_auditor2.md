# Blind auditor 2: work_global_ext/PROOF_EXT.md (2026-10-17)

(Reviewer: Claude subagent, blind auditor 2. Saved by the parent session; subagents cannot write report files.)
Did not read rev_ext_adv, rev_ext_aud1 or scratchpad/tasks. Evidence is own code except the requested gen.py rerun.
Code in rev_ext_aud2/: fam_test.py (F1–F3, (AA)), mywalk.py (own F walk, pair and λ-only), mygen.py (own level
generator, log mygen4.txt), brute_psi.py, xpath.py (brute force vs exact integer dynamics),
route_a/run_gen4_mine.txt (authors' gen.py rerun).

## 1. Theorem S + Corollary 4: CONFIRMED (two wording fixes)
(a) F1–F3 CONFIRMED. Derived by substitution. F1(a): Θ′ − x′ = 3 − Θ + 2^{j_L−1}λ. F1(b): copied chain is W's fire,
Θ_y = 2^{j_y}λ_y + 1, v2(2^{j_y}c_uy) = ρ_y = j_L − 2. F1(c): error term Q_y 2^{j_y}c_uy λ has valuation ≥ j_y + v.
F2: λ = (x′ − 2E)/(2^{j−1}(4Q−1)) gives P′ = 3 + 3k − E/(4Q−1); P′ − (3−P) = 2E(2Q−1)/(4Q−1), valuation ν+1, so
P′ ≡ 3−P mod 2^{min(j′, j−1)}. F2(ii): λ = r + 2^m t, t free, x′/2^{j−1+m} ranges over all 2-adic integers; a tie
with e₀ ≥ m emits exactly one any-j family on j′ ≥ j−1+m with λ′ free; precision preserved (error × −1/(4Q−1), a
unit). F3 identity; implicit fact to state: v2 Q′ = v2 Q + 1 + ε(n) ≥ 1 (σ_y = n − ε(n)); code never uses F3.
fam_test.py seeds 7, 8, 120,000 instances, 0 failures: F2 ≈30k (i), ≈60k (ii), ≈30k (iii) (identity, j′,
P′ ≡ 3−P, v2 Q′ = v2 Q + 1); F3 86k; F1(a),(b),(c) 120k each; (AA) with v2 x₂ = v2 Z 60k. Q_m formula m ≤ 3.
(b) Lemma M CONFIRMED. (AA): λ_{x_{t+2}} = Θ_t + 6 + 9k + 6k₁ + 2^{j_b−2}λ; Z > 0 needs k ≥ (j_b−2)/4 (new τ bound);
6k₁ negligible (j_{t+1} < T_i by S-a). Exact big-integer check at i = 1, worst j_b = T₂ − 1: q = 1 bit length T₁ − 1;
q = 3 bit length exactly T₁ ⇒ j_{t+2} ≤ T₁ − 1, valid with zero integer slack; q = 5 fails. At level 4 Lemma M is used
only with p = −2, q = 1 (5 → 10/3 lands below N; TIE2 §6.2 bound, ample).
(c) τ(n) ≥ (n−1)/2 CONFIRMED [A]: pointer i_s ≤ 2s (advance 2 − |P| ≤ 2 per step); a step reads only E_{i_s},
E_{i_s+1}; so n ≤ 2τ(n) + 1, k_n ≥ (n−1)/4 at odd type-a. Walk to pointer 10^6: min(2τ(n) − (n−1)) = 0 (tight).
Not needed for Corollary 4 (level-4 large states have θ ≥ −2); matters from level 5.
(d) Generator rules and gen.py CONFIRMED (level 4). Rules match TIE2 §3 rule for rule (chain 1: (i,2), (i,0),
AO_lw shifted −1 for lw ≤ l−1; (Ba) 3−θ, (Bb) θ−1, (Bc) AO_lw shifted θ−2 for lw < i; small on real data); additions
are F2(ii) emissions with Lemma M landing check and Q-annotated any-j families. Code: psi bit bookkeeping correct
(B = min(prec+1, j−1+m), tie bits mR, bit-form conversion at the first b/c step); X-record copy with min(m, max(h,1))
λ_u bits conservative (tracked h ≤ true h when true entry margin ≥ 1). Rerun `gen.py 4 4` (7m54s): level 4 10,035,943
entries, {0: 3,793,990; 1: 5,813,924; 2: 404,097; 3: 23,924; 4: 8}, 63,728 ties resolved, 0 failures; one emission
5|1 → 10/3|2/3 at j = 5 depth 0, only origin big-a from R₁ θ = −2; levels 1–3 match TIE2. Independent mygen.py (own
walk, own unified exact automaton): level 0 reproduces V4/E4 {0: 378,392; 1: 574,113; 2: 47,493}; levels 1–4
reproduce every number (entries, distribution, 63,728 exact runs, 0 failures, same single emission, 147 a-output
pairs, 93,489 records); checks each emission's landing against the final origin list. brute_psi.py (exact integer
chain dynamics on the full pair walk, pointer ≤ 3000, b/c steps with exact c_uW): 10 families incl. 5|1, 10/3|2/3,
46/9|2/3, −1/3|1, 40,500 runs: 40,440 match an END path, 60 pass through an emission with j ≥ jmin, 0 mismatches.
Latent gen.py defects (not triggered at level 4): (1) emission-landing check uses origins as of that iteration;
origins added later are not checked; (2) nt_by_size admits q < 10^4 but S-a landing needs q ≤ 5 and Lemma M q ≤ 3;
(3) `assert j−1 <= PREC−64` would crash (not mislead) if E ≡ 0 at large j.
(e) Lemma LM replacement CONFIRMED: "tie-free" same in both (v2 β_x < v2 α_x = J − Γ_t ⇔ h_t ≥ 1, TIE2 §5 step 4);
by-product proves h_t ≥ 1 for t ≤ ⌊J/(3 log2 J)⌋+1 without the automaton; its only dependence on EXT below J is
C2-log at J−1, and for J < K″ that W-epoch has J_W < K′ (I-4): not circular. Chain count: ≤ 3 large chains
(R₃ → R₂ → R₁), entry chain, emitted chain, ≤ 4 further: r ≤ 9 ≤ L+1. Identities (via TR) used only on t ≤ 9, all
tie-free; TIE2's "dips to h = −1" are baseline-1 bookkeeping artefacts, now only reduce record λ-bits to 1.
(f) Reduction CONFIRMED: log2(6(J−1)²+5) < log2 6 + K′ − 4 < K′; J_W ≤ log2(3(J−1)²+4) < K′ − 2.4; route a
j₁ = 1 + v2(3k+1) ≤ log2(3(J−1)²+2) < K′; route b ω(J−1) < K′; chain-1 family precision ≥ J−2. Horizon as in
Corollary H with fires J = v2(3s+4) < K″ and τ(v−1) ≤ (v−1)².
Fixes (wording): S(b) at J = K′: v2(3k+1) ≤ K′−2 does not give < J−2; (C1) does (3k+1 ≤ 1.5(J−1)²+1 < 2^{J−2}).
State in S's proof that "EXT below J" is used only via C2-log at J−1 (needed for §6).

## 2. Theorem U\*: CONFIRMED
Re-derived at over-tie x = (α, β), m = v2 α < v2 β, u = (γ, μ): v2(αU+β) = m for every odd U; real successor
(γ, μ), γ odd, μ even, μ ≥ 2 (β ≥ 1 by T(2)). Calls: M_u(c′, λ′) = (γc′, μc′+λ′) keeps S1 with the same j, preserves
parity, fixes (0,1), (0,3); image heads have even c-part except W's step-0 image (even step); D-formula integral;
PROOF_M 2.1–2.3 and the endgame return lemma verbatim. n = m−1 ≤ J−2 (Γ_t ≥ 1); n ≤ 1 ⇒ head (γ, μ+1) even, epoch
ends. T(1) (b/c: v2 α_u = v2 α_x − m; a: α_H = α_x/2); mass changes by (0,3) per chain whatever j, so Σα = 2^J,
Σβ = 3d−3 and T(2) survive. E3 becomes u = γU+μ ≥ 3 (no halt); E1, E4 with modified rule. F margin
σ_t − j_t = (ρ − J) + 0 ≥ 1; STATE-CLOCK F-only. ≤ J−1 exit chains. Places to read in starred form: EGX item 2;
LEMMAS_E E1 (safe prefixes), E2 ("λ_u odd"), E3 ("c_u even"); Theorem U "≤ J−2 chains"; C2-log becomes
max(3, 2J_W+1), Theorem L constants 6l + 9.2, f(10) = 135.6 > 0. Route D Prop 2.1 covers all; no other use found.

## 3. §6 combined statement: CONFIRMED (one wording fix)
Cases: J < K″ Corollary 4; J ≥ K″, X(J−1) even: r = 0; type a: RA (needs only (C1) for chain 1; RA accepted, not
audited); type b/c shallow: Theorem S; rest: hypothesis. Gap: Theorem S is applied with only EXT\* below J; valid
(only C2-log at J−1; case (d) J_W < K′ is I-4; by-product survives under EXT\*). Say so.

OVERALL: Theorem S, Corollary 4 (EXT for all J < K″, horizon 2^{K″} − 2), Theorem U\* and §6 CONFIRMED; two wording
fixes; gen.py defects latent, not affecting level 4.
