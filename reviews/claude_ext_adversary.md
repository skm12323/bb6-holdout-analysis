# Adversary review: work_global_ext/PROOF_EXT.md (2026-10-17)

(Reviewer: Claude subagent, adversary role. Saved by the parent session; subagents cannot write report files.)

No claim broken. All five headline items survive with fixes; none major. PROOF_EXT correctly says EXT is open.

## What I ran (rev_ext_adv/)
- Level-4 generator reproduced: route_a copied with paths fixed, `gen.py 4 4` (8 min, `a/run_gen4.txt`); levels 1–4
  match `run_gen5.txt`: 10,035,943 entries, 63,728 ties resolved, 0 failures; one emission (10/3, 2/3) from family
  (5, Q=1) at j = 5, depth 0; max further chains 4.
- `check_family.py`, `validate_psi.py` pass (18,865 integer chains, 0 disagreements).
- `indep.py` (own exact pair-map walk to 2·10^5 crossings, 42 s): (K1) τ(n) ≥ (n−1)/2 holds (type a even τ ≥ n/2;
  tight: min(2τ − (n−1)) = 0; pointer never advances > 2 per step). (K2) Lemma K: every odd crossing (60,575 a,
  60,575 b, 3,171 c) is a top-level chain of the stated kind; type b ω = v2(3τ+4); b/c v2(c′) = n − ε(n),
  ω(n) ≤ n − ε(n) − 1, 0 exceptions. (AB) 248,638 virtual phase-2 states (random 200-bit odd u, every odd m): walk
  always copies E from C to its end; first-difference precision exactly σ_C every time; 0 failures incl. 6,342
  type-c. (RA) all J ≤ 2·10^5 with X(J−1) odd type a (60,573): tie-free, r formula holds.
- `lp_fix.py`: L′ with L+1 non-descents and EXT\* eps1 in exact integers, J = 2^10…2^299, 2^512, 2^1024, 2^4096,
  20,000 random J: pass. `route_b/e8_budget.py` passes.

## Claim 1: Theorem S + Corollary 4 — closed (minor fixes)
Verified: re-implementation matches TIE2 counts at levels 1–4; the only new step at level 4 is the exact Ψ
resolution of (5,5): Θ = 5 + 32λ (F1(a), precision ≥ N−1), k₄ = 1, x′ = 16(1+3λ), Θ′ = 10/3 + (2/3)2^{j′}λ′. F1, F2
re-derived. Emission landing: family (5, Q=1) has one source (big-a from (R₁, θ = −2)); no b/c rule produces P = 5 at
level 4; depth-0 landing check complete. Lemma M: q ≤ 3 margin 4.5q/16 ≤ 0.84 < 1. Chain count r ≤ 9 (longest:
chain 1 in R₃ → R₂ → R₁(−2) → (5,5) → 10/3 entry → 4 more). Reduction of J ∈ [K′, K″): j₁ < K′, J_W < K′, every
chain-1 entry is a level-4 entry. LM replacement valid: by-product "tie-free" is exactly h_t ≥ 1 and covers ≥ 10
chains; gen.py never uses h as pass/fail; the cap min(m, max(h,1)) on copied λ-bits is sound since copier precision
v = σ − j = h_true + (ρ_W − J_W) ≥ max(h_tracked + 1, 1). τ(n) ≥ (n−1)/2 proved (≤ 2 entries read per step), tight;
not needed at level 4 (all large-state θ ≥ −2).
Issues:
1. (minor) S(b): "v2(3k+1) ≤ K′−2 hence NT since < J−2" gives only ≤ J−2 at J = K′. NT follows from (C1):
   1+3k ≤ 1.5(J−1)²+1 < 2^{J−2}. Cite (C1) or write ≤ K′−3. Moot (RA covers type a).
2. (strengthening) Theorem S needs no "EXT below J": the by-product uses EXT below J only via C2-log at i = J−1, and
   in cases (b)–(d) that W-epoch has J_W < K′ (I-4); the certificate only copies epochs of level ≤ 3. So S holds
   unconditionally given F through τ(J−1). Repairs §6.
3. (minor) Route A §3 "Γ_y ≤ J_W/4 + 80" wrong for large J_W (≤ 9 chains add O(log J_W) by C2); harmless since
   v ≥ ρ_W − J_W + 1 is astronomically large. Fix sentence.
4. (low, latent) `gen.py nt_by_size` accepts q < 10^4, but landing "j′ < T_i" valid only for q ≤ 3 (q = 9 exceeds
   by 0.75 bit). Levels 4, 5 unaffected. Assert q ≤ 3.
5. (low) F3: v2 Q′ = v2 Q + j − j_y − v ≪ 0, so "Ψ closed under every transition" only in ℚ₂, not with precision.
   Code does not use F3. Wording.
6. (low) Horizon claim (F defined for s < (2^{K″}−4)/3; no halt in first 2^{K″}−2 top steps) needs a written proof;
   checked Theorem U(b) restricted to that range with Corollary 4 goes through.
7. (repro) `route_a/famlib.py` REPO = HERE.parents[1]/'repo' fails (ModuleNotFoundError verify_el); should be parents[1].

## Claim 2: Theorem RA — closed
Lemma K(c) correct (type-c crossing = top-level |P| = 1 = a-return; odd head is chain t+1; σ_{t+1} = σ_t − 1 =
n − ε(n), ε = 0 at type-a returns). AB precision exactly σ_C from min(v2 δΘ, v2 δx): (a) 3·2^m u vs 2^{m+1}u;
(b) 3·2^{m−1}u; (c) c_C u, v2 = m − ε(m). HP induction (a-step v2 δx′ ≥ P − Γ\* − 1; b/c n − ε + v2 δu ≥
P − Γ\*_{i+1}; j's match since S1 of E is HP's hypothesis). Ordering: E's fire at pointer ≤ J−3; P = ∅ only at epoch
boundaries; τ(m) < τ(J−1) strictly (two consecutive entries per step, J−1 ≥ m+2); E ends before the epoch starting
at τ(J−1). Outer tie-free: j\* + Γ\* < σ_C ≤ m − ε(m) ≤ J − 3 − ε(m). All checked numerically.

## Claim 3: Theorem U\* — closed (exposition fixes)
No hidden use of strict tie-freeness or "c_u even" that breaks: inner S1 (v2(μc′+λ′) = v2 λ′); S2 from c′_A even
(n ≥ 2), head (γ, μ+1) even (n ≤ 1); parity (γ+μ odd); b/c never tie; T(1) j-independent, T(2) needs μ ≥ 2; F
margin ρ − J > 0; ≤ J−1 chains; C2-log weakens to 2J_W + 1.
Fix: state extended E1, E3 explicitly (E1's S1 hypothesis literally fails at an over-tie; rule j := v2 c,
u := x/2^m; E3's c_u ≥ 2 becomes base ≥ U+2; EGX's "S2 since c_u even" becomes "c′_A even"). Note Lemma BR's
β-only walk (j = v2 B) is invalid past an over-tie.

## Claim 4: Theorems L′, L″ — needs fix (minor)
Off-by-one: "(ND-EXIT) ⇒ EXT" does not follow from L′ as stated: if chain t is the first tie, prefix 1..t−1 has ≤ L
non-descents but step (t−1) → t may be the (L+1)-th; L′ needs ≤ L among all s < t. Fix: prove L′ with L+1
non-descents and (L+2)(g−4) chains; slack ample; verified exactly incl. EXT\* eps1. Rest verified: b/c gain ≥ 1
(ω ≤ n − ε − 1) at every odd b/c crossing to 2·10^5; descending a ≥ 0; non-descent ≥ −(g−4); block count (j ≥ 5);
d ≤ 2J² induction; closing inequality; L″ (J_W ≤ ⌊log2(3n²+3)⌋ ⇒ 1+ε ≤ E).

## Claim 5: §6 and §5 — needs fix (wording; one formal gap)
1. (moderate, easy) §6 combines under EXT\* below J, but S, the by-product and L′ are stated with EXT below J. Fix:
   S needs no EXT (Claim 1 issue 2); L′ needs its EXT\* version (eps1 + 2), which holds.
2. (minor) §5 "E(w,J) halts iff 3wγ+μ = 2^k" → "halts at chain t\* iff" (later halt possible).
3. (minor) §5 "beyond EXT\*, any sufficient hypothesis must use which w occur" contradicts route D's EG-ALL
   (w-uniform, J-only, strictly weaker than EXT\*). Same in §0 row X.
4. (cosmetic) 3-adic orbit is not 2-adically dense (c_m ≡ 5 or 21 mod 64); ℤ is; Theorem O needs only pigeonhole.
5. (cosmetic) "No monovariant" should be tagged [C].

OVERALL VERDICT: with fixable gaps; nothing broken. Theorem S, Corollary 4 (EXT for all J < K″), Theorem RA and
Theorem U\* hold; L′ needs the L+1 fix; §6/§5 wording fixes incl. "Theorem S needs no EXT hypothesis".
Files: rev_ext_adv/indep.py, lp_fix.py, a/ (patched route_a copy), a/run_gen4.txt.

## Re-review of the revised PROOF_EXT.md (2026-10-17)
1. L′ (L+1 non-descents, (L+2)(g−4) chains): closed; constant −8x−6 correct (extra non-descent costs ≤ g−4 ≤ 2x − 0.415,
   bound ≥ (J/3)(1 − 1.6/(x−1)) − 8x − 5.34; ≈ 194.7 at x = 10, increasing; float check x = 10…40); `lp_fix.py`'s d-bound
   already used (L+2)(g−3); ND-EXIT ⇒ EXT reads correctly; EXT\* form is the case checked.
2. Theorem S with no EXT hypothesis: closed. T(2) needs only the induction hypothesis; ε(n) ≤ n trivial; (C1) unconditional
   (PROOF_CLOCK §3); C2-log at J−1 is the only EXT use (types a/b ε ∈ {0,1}; type c with J_W < K′ by I-4, whose F-facts sit
   at indices < K′, crossed at times ≤ K′², inside HORIZON-3); certificate copies only level ≤ 3 epochs; case (b) fixed.
3. Corollary H″: closed (level fires before (2^{K″}−4)/3 have J < K″; Theorem U(b) on that prefix needs only STATE-CLOCK and
   Corollary 4, induction on time; singletons v < K″ have τ(v−1) ≤ (v−1)² < (2^{K″}−4)/3).
4. §6: closed (J < K″ Cor 4; J ≥ K″ even/RA/shallow S use no hypothesis; tie-free S(J) gives S\*(J) = S(J), so EXT\* below J
   holds inductively and the EXT\*-form L′ remark is legitimate).
5. §1 starred readings, §5 wording: closed (cosmetic: E2 at over-tie bases "c_u odd ≥ 1, λ_u even ≥ 2").
6. Correction of own earlier issue 5: F3 is an honest Ψ-family: v2 c_{uy} = n − ε − j_y, so v2 Q′ = v2 Q + 1 + ε(n) ≥ 1 and
   v2(2^j/c_{uy}) = 1 + ε + j_y ≥ 1, P′ ∈ ℤ₂. Suggested wording applied.
VERDICT: closed in all states.
