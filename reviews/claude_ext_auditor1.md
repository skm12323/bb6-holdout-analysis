# Blind auditor 1: work_global_ext/PROOF_EXT.md (2026-10-17)

(Reviewer: Claude subagent, blind auditor 1. Saved by the parent session; subagents cannot write report files.)
Overall: no item refuted. A, C confirmed; B, D need minor fixes. All numerics recomputed with own code (stdlib) in
rev_ext_aud1/; authors' scripts read only for definitions; no other reviewer folder read.

Own code: `fmap.py` (exact big-integer pair map F from G6 §5.1; records X(n) — τ, type, parity, ε, ω, chain pair —
from the run; top-level chains via tagging D entries; no epoch theory). `symexit.py` (exact symbolic S(J)/S\*(J) on
(α,β) per PROOF_EGX §1; Lemma BR β-walk; generic (j, Θ, x) walk of route C §1). Sanity: S(J) counts reproduce
PROOF_EGX for J ≤ 30001 and PROOF_M V4 / route B for J ≤ 10^6+1: {0: 378,392; 1: 574,115; 2: 47,493}.

## A. Theorem RA, Lemmas K, HP, AB — CONFIRMED (two nits)
`checkA.py` to pointer 10^6 (`run_1e6.log`, 643 s), 0 failures throughout. Walk rules A1/A2 at all 23,760
consecutive top-level chain pairs (15,850 a, 7,910 b); σ_{t+1} = σ_t − 1 − ε at every one; every epoch ends at an
even X(n). Lemma K, all odd crossings 4 ≤ n ≤ 10^6: type a (302,879) fire at pointer n, τ even, j = 1 + v2(3k+2),
ε = 0; type b (302,878) same step as the fire at pointer n−1, ω = v2(3τ+4), ε = 1; type c (15,850) exit chain t+1 of
the current epoch, σ = n − ε = σ_t − 1, previous return type a. `checkHP.py` at all 1,274 b/c crossings n ≤ 4000:
v2(c′_n) = n − ε(n), ω(n) ≤ n − ε(n) − 1. Lemma HP: 200,000 random walk pairs (δ with v2 ≥ P), all agree incl.
valuation bounds and ending together; one apparent failure is a starred-walk resonance (x\* = 0 at j0 = 5, u = 1,
Θ = 5), so x\*_i ≠ 0 is genuinely needed. Nit: "the walks end together" → "if the starred walk ends after chain I".
Lemma AB synthetic: every m ≤ 4000 with X(m) odd, start (m+1, Θ = x+2, x = 2^{m+1}u), 6 values of u (1, negative,
up to 2000 bits): 14,910 walks (7,266 a, 7,266 b, 378 c); each copies E from C to its end; first-step offsets exactly
3·2^m u (a) / c′_m u (b/c) in x and 2^{m+1}u in Θ; precision exactly σ_C; later offsets v2 ≥ σ_{C_i}.
Theorem RA on actual S(J), all route-a J ≤ 10^6: 279,144 r = 1; 15,822 copying a type-a epoch; 7,911 type-b; chain 1
β = 3τ+2, j_1 = 1 + v2(3k+1); tail = E from C (same j's), outer Γ = 2 + ε(m) + σ_C − σ_{C_i}; r-formula holds;
offsets v2 ≥ σ_{C_i}. Route-a case c never occurs for J ≤ 10^6 (needs j_1 ≥ 66); covered only by synthetic AB.
Proof read: AB algebra correct; ordering holds (E's fire pointer ≤ J−3, E ends before the P = ∅ state at τ(J−1));
Γ bound j + Γ < σ_C + 2 + ε(m) ≤ m + 2 ≤ J − 1; j_1 ≤ ⌊log2(6(J−1)²+5)⌋ ≤ J−2 checked exactly for 10 ≤ J < 10^6
(needs (C1), unconditional by PROOF_CLOCK).
Extra Prop RB (`checkRB.py`, J ≤ 10^5): all 31,872 route-b/c cases chain 1 = V(C, −1) exactly, copy exact up to the
first real a-step; there outer x = x_real − 2; real j ≥ 2 ⇒ exit ends with j = 1 (1,397); climbs 189.

## B. Theorems L′, L″, Lemma BR — NEEDS FIX (minor)
BR = own exact S(J) (j, β_x, d, Γ at every chain) for all 3 ≤ J ≤ 10^6+1, 0 mismatches; T(1), T(2) at every chain;
continuing chains after the first have j ≥ 5; every b/c step drops j by ≥ 3. h-increments, J ≤ 10^6+1: ≥ 1 at all
15,821 b/c steps, ≥ 0 at all 31,672 descending a-steps, no non-descents, min h_1 = 1. `checkL.py` exact integers,
1,092,072 J (every J in [2^10, 2^20), 2^e + d for e = 10..4096, d ∈ {−3,−1,0,1,2,7}, 20,000 random J < 2^300): L′
d-bound and j ≤ g; h_1 − L(g−4) ≥ 1 (analytic display valid lower bound, > 1; margin 314 at J = 2^10); L″ d-bound,
Γ ≤ J − g − 1, E ≥ 4, E ≤ 4 log2 log2 J + 8, L2 ≥ L. Constants: 1 + eps1 + g1 ≤ 6x + 5.755,
L(g−4) ≤ (J/3)(2 + 1.585/(x−1)). (One flag was a float artefact in own optional cross-check.)
Issue: L′ counts non-descents over s → s+1, s < t, including the step into the tested chain t; ND-EXIT bounds
non-descents only inside a tie-free prefix; at the first tie, prefix 1..t−1 allows L+1. Fix: L′ with L+1, or
ND-EXIT with ≤ L−1. J − 1 − eps1 − g1 − (L+1)(g−4) ≥ 1 holds at all 1,092,072 J; analytically absorbed for x ≥ 10.
L″ correct (relies on C2-log, E ≥ 4 for type-a and type-b crossings).

## C. Theorem U\* / Prop 2.1 — CONFIRMED
Re-derivation: real valuation m for every odd U; μ ≥ 2 (T(2) β > 0); real call from odd base u_r = γU+μ ≥ 3 is
G6 §5.2 with U := u_r (no halt); inside F base has c even, λ odd, S1 since m = J−Γ_t < ρ−Γ_t; parity (γ+μ odd);
next head α = c′γ even for n ≥ 2, run ends for n ≤ 1; b/c cannot tie (v2 β = ω < v2 c′ ≤ v2 α); T(1) j-independent;
Σα = 2^J, Σβ = 3d−3 algebra; α_x even ⇒ ≤ J−1 chains; F margin ≥ ρ − J > 0. No other use of "c_u even"; C2-log
weakening ε ≤ 2J_W + 1 and f(10) = 135.6 > 0 right.
Brute-force integer top map (own reading of RULES §5, reproduces R1–R5): Family 1 (`checkC.py`, `checkC2.py`,
`checkC3.py`) endgames E(v; e0) with defect (2^{v−1}, e0), exhaustive e0 ∈ [−1, 2^{v+6}) for 5 ≤ v ≤ 14 (≈2.1M runs)
and forced chain-1 over-ties; ≈48,000 brute-force comparisons with 8–9 values of U up to 2^127+1; identical chain
values at predicted steps, predicted j (= v2 α at over-ties), identical final singleton time and value; halts only at
exact ties at the predicted chain. Family 2 (`checkC4.py`) 60,000 generic starts from an over-tie base (γ odd, μ even,
70%) or free base, arbitrary D: all 238,348 comparisons agree incl. over-ties at the next chain; 2 halts, both at exact
ties. Caveat: over-ties at chain ≥ 2 inside genuine S(J) structure rarely produced (3 instances).

## D. Theorem S, Corollary 4 — NEEDS FIX (minor); F1–F3 CONFIRMED
Reduction: S covers J ≥ K′ with shallow first return (route a j_1 < K′, b ω < K′, c J_W < K′); exit after the fire
depends only on τ(J−1) or C plus comparisons j + Γ < J; level-4 chain-1 entries cover it; by-product (≥ 10 tie-free
chains vs certificate r ≤ 9) replaces Lemma LM soundly. Corollary 4: for K′ ≤ J < K″, (C1) gives j_1, ω, J_W ≤
log2(6K″²) < K′; induction works; horizon as in Corollary H.
Issues: 1. (b) "v2(1+3k) < J−2" does not follow from ≤ K′−2 at J = K′; true via (C1) (3k+1 ≤ 1.5(J−1)²+1 < 2^{J−2}),
cite it. 2. §6 applies S for J ≥ K″ with only EXT\* below J, but S assumes EXT below J; fix: restate S with "EXT\*
below J" (by-product survives with ε ≤ 2J_W + 1); RA needs neither.
`checkD.py` 0 failures: F2 on 200,000 a-steps ((i) 136,760, (ii) 37,322, (iii) 25,918): j′, λ′ mod stated precision,
Θ′ ≡ P′ + Q′2^{j′}λ′, P′ ≡ 3−P mod 2^{min(j′, j−1)}, v2 Q′ = v2 Q + 1, x′ formula. F2(ii) any-j: in all 300 classes
every e in m..m+3 occurs, no e < m. F1(a) exact identity. Real table: F1(b) 48,440, F1(c) 2,520, F3 50,960.
Nit: F2(ii) "e = e₀" also needs e₀ < p − j + 2 (enough Θ precision); 7 low-precision cases had e undetermined, 5 would
give wrong j′ if precision ignored; route A's PREC = 2048 + assertion handles it; state it in the lemma.
Level-4 generator not rerun (imported [B]).

OVERALL: SOUND WITH MINOR FIXES — A, C confirmed; B, D minor fixes (L′ count, Theorem S under EXT\* in §6, (C1)
citation in S(b)); nothing refuted.
