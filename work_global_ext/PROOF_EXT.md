# EXT attack: four routes, partial results (2026-10-17, Claude Opus 5.5)

Revised after three-way review (record in §8). Machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`.
Starting point: work_global_egx/PROOF_EGX.md (accepted): the whole non-halting proof reduces to **(EXT)** "for every
J ≥ K′ with F defined through τ(J−1), S(J) is tie-free". Four independent routes were run; each route's full report
and scripts are in `route_a/` … `route_d/` (route reports are the authors' text; where this file and a route report
differ, this file is the reviewed version). Tags: [A] proved for all parameters, [B] finite computation,
[C] heuristic. **EXT itself is not proved.**

## 0. Results

| # | statement | source | tag |
|---|---|---|---|
| U\* | EXT can be weakened to EXT\*: only *exact* ties (v2 β_x = v2 α_x) must be excluded; over-ties (v2 β_x > v2 α_x) are harmless. EXT\* ⇒ #1 never halts. | D §1–2 | A (cond.) |
| RA | If X(J−1) is odd of type a, S(J) is tie-free, with no NT and no EXT hypothesis (only F defined through τ(J−1), J ≥ 10). With even X(J−1) (r = 0), EXT reduces to J with X(J−1) of type b or c. | C §3–5 | A |
| L′ | Only non-descents (j_{t+1} ≥ j_t) consume budget: (ND-EXIT) "≤ ⌊J/(3 log2 J)⌋ non-descents in every tie-free prefix of S(J), J ≥ K′" ⇒ EXT (also in the EXT\* form). Chain budget improves to ≈ J/(4 log2 log2 J). | B §2–3 | A |
| S, K″ | Theorem S: if the first return of S(J) is shallow (first parameter or copied epoch below K′), S(J) is tie-free with ≤ 9 chains, **with no EXT hypothesis**. Hence **EXT holds for all J < K″ = 2^{K′/2−2}**, and #1 does not halt during the first 2^{K″} − 2 top steps. | A §1–3, §6 | A + B |
| BR, RB | Exact β-only reduction of S(J) (valid while tie-free); routes b/c are exact shifted copies V(C, −1) of real epochs up to the first real a-step. | B §2, C §6 | A |
| O | No generator-type finite certificate closes the tower (integer drift, 3-adic orbit c_m = −3 + 8·3^{−m}, size failure). | A §2, §4–5 | A (about the method) |
| X | Exact ties are a genuine obstruction: at a solvable first exact tie, infinitely many w make E(w,J) halt at that chain. So no J-only hypothesis can allow such a tie; the weakest w-uniform hypothesis found is EG-ALL (strictly weaker than EXT\*, not a finite check). | D §3, §5–6 | A |
| DATA | S(J) for all J ≤ 10^8: no tie, no non-descent, r ≤ 3; deep tails from every (m,θ), m < 10^8: real entries r ≤ 4. | C §2, B §5 | B |

## 1. Theorem U\* (EXT\*) [A, conditional] — route D §1–2

At a chain x = (α, β) with m = v2 α < v2 β (an **over-tie**), for every odd U the real valuation of αU+β is m.
S\*(J) continues through such a chain with j := m, u := x/2^m = (γ, μ), γ odd, μ even ≥ 2 (β ≥ 1 by Lemma T(2)).

**Prop 2.1.** F defined through τ(J−1). Up to the first exact tie, for every odd U: EGX holds for S\* (endgame of
E_U(J) = S\*(J) pair for pair); no chain halts; PROOF_M Lemma 6.1 holds for S\*; Lemma T(1),(2) hold; S\*(J) ends
within J−1 exit chains and uses X(n) only for n ≤ J−2.
*Proof.* Over-tie chain: real valuation m, u integral, real base γU+μ ≥ U+2 ≥ 3 (no halt); F's λ_x = αλ_u+β has
valuation m, and S1 holds since m = J−Γ_t < ρ−Γ_t = σ_t. The call from a base with odd γ: M_u(c′, λ′) = (γc′, μc′+λ′)
keeps S1 with the same j (v2(μc′_x + λ′_x) = v2 λ′_x < v2 c′_x = v2(γc′_x)), preserves parity (γ odd, μ even) and fixes
(0,1), (0,3); image heads have even c-part except the image of W's step 0, which is an even step; so PROOF_M 2.1–2.3
and the endgame return lemma hold verbatim. Next return: n = m−1 ≤ J−2 (Γ_t ≥ 1); n ≥ 2 ⇒ c′_A even ⇒ S2; n ≤ 1 ⇒ head
(γ, μ+1) even, the run ends. b/c steps never tie (v2 β = ω(n) < v2 c′_x ≤ v2 α). T(1) does not use j_t (b/c:
v2 α_u = v2 α_x − m; a: α_H = α_x/2); the mass changes by (0,3) per chain whatever j is, so Σα = 2^J, Σβ = 3d−3 and
T(2) survive. Termination: α_x even ⇒ J − Γ_t ≥ 1, and Γ_t ≥ t. ∎

**Starred readings** (the places that used strictness, all covered by Prop 2.1): EGX item 2 ("S1 ⇔ strict
comparison") reads "S1 or over-tie"; LEMMAS_E E1 at an over-tie uses the rule j := v2 c_x, u := x/2^m; at over-tie bases E2's
"c_u even, λ_u odd" reads "c_u odd ≥ 1, λ_u even ≥ 2"; E3's "c_u ≥ 2" becomes "base ≥ U + 2"; EGX's "S2 since c_u even" becomes
"c′_A even"; Theorem U's "≤ J−2 chains" becomes "≤ J−1"; C2-log becomes ε ≤ max(3, 2J_W + 1), and Theorem L's
constants become 6l + 9.2 (f(10) = 135.6 > 0). Lemma BR's β-only walk (j = v2 B) is valid only up to the first
over-tie.

**Theorem U\*.** (EXT\*) "for every J ≥ K′ with F defined through τ(J−1), S\*(J) has no exact tie" implies F is
defined forever and #1 never halts. EXT ⇒ EXT\*.
*Proof.* PROOF_EGX Theorem U verbatim with Prop 2.1 and the starred readings replacing the tie-free facts; F margin
σ_t − j_t = (ρ − J) + (J − Γ_t − j_t) ≥ ρ − J > 0; ≤ J−1 exit chains per epoch; STATE-CLOCK concerns F only. ∎
Theorem L's by-product survives under EXT\* below J (with the starred C2-log).

## 2. Theorem RA: route a is closed [A] — route C §1, §3–5

Walk rules (PROOF_EL A1/A2, Lemma TR): state (j, Θ, x = 2^j u), n = j−1, reads only X(n). a-step (τ(n) = 2k):
x′ = 2Θ + 6k − x/2, Θ′ = Θ + 3 + 6k. b/c-step (C_n = (c′_n, λ′_n) W's chain at τ(n)): x′ = c′_n u + λ′_n, j′ = ω(n),
Θ′ = Θ + 3 + 3τ(n), v2 c′_n = n − ε(n) > ω(n). Real chains (Θ = 3s+5, x = λ_x) and the β-walk of S(J) (Θ = 3d+1,
x = β_x) obey these rules.

**Lemma K.** X(n), n ≥ 4, odd: (a) type a ⇔ a level fire at pointer n, s = τ(n) = 2k_n, ε = 0; (b) type b: W's chain at
τ(n) is the fire at pointer n−1, ω(n) = v2(3τ(n)+4), ε = 1; (c) type c: τ(n) is the a-return after chain t of the
current epoch, and its chain is chain t+1 of that real epoch, σ_{t+1} = σ_t − 1 = n − ε(n).
*Proof.* Crossings happen only at top-level states (PROOF_M 3.3). A state with P = ∅ reads E_i, E_{i+1} (types a, b at
the same step); a state with |P| = 1 is exactly an a-return [D_t]. (a) an odd state with P = ∅ is a level fire,
σ_0 = ρ. (b) the originals have λ = 0, so λ_x = λ_A + 3 = 3s+4, the fire's own chain. (c) x = H + 2D_t + 3 is chain
t+1 (PROOF_M 3.1); the ε-formula gives n − ε(n) = σ_t − 1; after an a-return σ_{t+1} = σ_t − 1. ∎

**Lemma HP (shadowing).** Two walks over the same table with equal j_0 and min(v2 δΘ_0, v2 δx_0) ≥ P. If the starred
walk reaches chains 0..I with x\*_i ≠ 0 and j\*_i + Γ\*_i < P, then j's, types, parities, ε's agree through I, and
v2 δΘ_i, v2 δx_i ≥ P − Γ\*_i; if the starred walk ends after chain I, so does the other.
*Proof.* Induction: δu_i = δx_i/2^{j_i} is an integer with v2 ≥ 1, so both u's are odd; a-step δx′ = 2δΘ − δx/2,
v2 ≥ P − Γ\* − 1; b/c δx′ = c′_n δu, v2 ≥ n − ε + P − Γ\* − j = P − Γ\* − 1 − ε; δΘ unchanged; at an a-step j′ matches
because j\*′ < P − Γ\*′ ≤ v2 δx′; at a b/c step j′ = ω(n) for both. ∎ (The hypothesis x\* ≠ 0 is needed: a virtual
"resonance" x\* = 0 exists, e.g. j0 = 5, u = 1, Θ = 5.)

**Lemma AB (absorption).** If a state has exact phase Θ = x + 2, m = j−1 ≥ 4, X(m) odd, and F is defined through the
end of the real epoch E of the chain C given by Lemma K, then the walk copies E from C on to its end (same j's, types,
ε's, ending at the same even return).
*Proof.* Case (a): x′ = 6k + 4 + 3·2^m u = x_C + 3·2^m u, Θ′ = Θ_C + 2^j u. Cases (b, c): x′ = x_C + c′_m u,
Θ′ = Θ_C + 2^j u. The precision min(v2 δΘ, v2 δx) is exactly σ_C ((a) ρ = m; (b) ρ = m−1 = m − ε(m); (c)
σ_{t_W+1} = m − ε(m)). Along E, σ_{C_i} = σ_C − (Γ\*_i − Γ\*_C), so S1 for the real chains is HP's hypothesis. ∎

**Theorem RA.** X(J−1) odd type a, F defined through τ(J−1), J ≥ 10. Then S(J) is tie-free; r = 1 if j_1 ≤ 4 or
X(j_1−1) even; r = 2 + r_E if X(j_1−1) odd a/b (E the epoch of the fire at pointer j_1−1 resp. j_1−2); r = 1 + r_W − t_W
if type c.
*Proof.* β_{x_1} = 6k+2, Θ_1 = 6k+4: phase exactly 2. j_1 = 1 + v2(3k+1) ≤ ⌊log2(6(J−1)²+5)⌋ ≤ J−2 by (C1) (PROOF_CLOCK,
unconditional), so chain 1 is tie-free. E's fire is at a pointer ≤ j_1 − 1 ≤ J−3; P = ∅ occurs only at epoch
boundaries and τ(m) < τ(J−1), so E ends before the P = ∅ fire at pointer J−1 at time τ(J−1), where F is defined; apply
AB. The outer Γ at the copy of C_i is 2 + ε(m) + (Γ\*_i − Γ\*_C), and S1 of E gives j\*_i + (Γ\*_i − Γ\*_C) < σ_C ≤
m − ε(m) ≤ J − 3 − ε(m), so j + Γ < J − 1. ∎
**Corollary.** EXT(J) (and EXT\*(J)) can fail only if X(J−1) is odd of type b or c.

**Prop RB** (route C §6, [A]). If X(J−1) is odd of type b/c and C is W's chain at τ(J−1), chain 1 of S(J) is
V(C, −1) := the walk from (j_C, Θ_C − 1, x_C), automatically tie-free (j_1 = j_C < σ_C = J − Γ_1), and S(J) copies E
exactly up to the first real a-step C_i → C_{i+1}; there the outer x is x_{C_{i+1}} − 2, so the exit ends (j = 1)
unless j(C_{i+1}) = 1, when it climbs to j′ = 1 + v2(u_{C_{i+1}} − 1) at a non-real state.

## 3. Theorem L′ (non-descent budget) [A] — route B §2–3

**Lemma BR.** While S(J) is tie-free, after the fire it is the integer walk on (j, d, b): par(n) = 0 ⇒ stop; type a:
B = 6d + 2 + 3τ(n) − 2^n b; type b/c: B = b c_W(n) + λ_W(n); d ← d + 1 + τ(n), j ← v2 B, b ← B/2^j; started at
(J, 0, 0); chain t is tie-free iff j_t + Γ_t < J. b/c steps always go to j′ = ω(n) and drop j by ≥ 3.

**Theorem L′.** Standing hypotheses of PROOF_EGX Theorem L (J ≥ 2^10, F through τ(J−1), EXT below J, (C1)). Put
L = ⌊J/(3 ⌊log2 J⌋)⌋. If chains 1..t−1 are tie-free and at most **L+1** of the steps s → s+1 (s < t) are non-descents,
chain t is tie-free. Hence (ND-EXIT) ⇒ EXT: if chain t were the first tie, the tie-free prefix 1..t−1 has ≤ L
non-descents by ND-EXIT, so at most L+1 among the steps s < t.
*Proof.* g = ⌊log2(12J²)⌋, g1 = ⌊log2(6(J−1)²+5)⌋, eps1 = max(3, 2⌊log2(3(J−1)²+3)⌋ − 1). Continuing chains have
j ≥ 5 (PROOF_EL Lemma 1), so a tie-free prefix with ≤ L+1 non-descents splits into ≤ L+2 strictly decreasing blocks and
has ≤ (L+2)(g−4) chains; by induction with (C1), d_s ≤ 2J², so j_s ≤ g (Lemma T(2)). h_{s+1} − h_s = j_s − j_{s+1} − 1
− ε(n_s) is ≥ 1 at b/c steps (F's S1: ω(n) ≤ n − ε(n) − 1), ≥ 0 at descending a-steps, ≥ −(g−4) at non-descents.
h_1 ≥ J − 1 − eps1 − g1 (route a: Γ_1 = 1, j_1 ≤ g1; b/c: ε(J−1) ≤ eps1 by C2-log, W-epoch J_W < J tie-free by EXT
below J). So h_t ≥ J − 1 − eps1 − g1 − (L+1)(g−4) ≥ 1. [B] This last inequality, and the d-bound, hold in exact
integers for every J ∈ [2^10, 2^20), J = 2^e + d (e = 10..4096, d ∈ {−3,−1,0,1,2,7}), J = 2^10..2^299, 2^512, 2^1024,
2^4096 and 40,000 random J < 2^300 (auditor 1 `checkL.py`, adversary `lp_fix.py`); analytically the left side is
≥ (J/3)(1 − 1.6/(x−1)) − 8x − 6 > 1 for x = log2 J ≥ 10. ∎
**EXT\* form.** With EXT\* below J (starred C2-log, eps1 + 2) and "tie" read as "exact tie", the same statement holds
(adversary `lp_fix.py`, exact integers on the same J set).
**Theorem L″.** Every chain t ≤ L2 + 1, L2 = ⌊(J − g − 2 − eps1)/E⌋, E = 2⌊log2(3(g−1)²+3)⌋ ≤ 4 log2 log2 J + 8, is
tie-free (C2-log at every small index; E ≥ 4 covers types a, b). ([B] `route_b/e8_budget.py`; auditor 1 `checkL.py`.)

## 4. Theorem S and EXT below K″ [A + B] — route A §1–3, §6

Tower T₁ = 10^6, T_{i+1} = 2^{T_i/2−2}: K = T₃, K′ = T₄, K″ = T₅. The level generator of PROOF_TIE2 §3 is re-implemented
with exact **Ψ-families** Ψ(j; P, Q): Θ ≡ P + Q·2^j λ_u (route A §3, Lemmas F1–F2; a tie emits exactly one any-j family,
F2(ii)), which reproduces TIE2's 10/3 macro automatically. Lemma F2(ii)'s "e = e₀" also needs e₀ < p − j + 2 (enough
precision p of Θ); gen.py works at PREC = 2048 bits and asserts it is never exceeded. F3 gives a family with P′, Q′ ∈ ℤ₂
(v2 Q′ = v2 Q + 1 + ε(n), since v2 c′_n = n − ε(n)); gen.py does not use it (b/c steps are handed to TIE2's bit
automaton). Level 4 re-certified: 10,035,943 entries, 63,728 ties resolved, 0 failures, one emission
5|1 → 10/3|2/3 (route A `gen.py 4 4`; rerun by the adversary and auditor 2; reproduced by auditor 2's independent
generator `mygen.py`). The new constraint τ(n) ≥ (n−1)/2 [A] (the pointer advances ≤ 2 per step and a step reads only
E_i, E_{i+1}; tight) is not needed at level 4 (all large-state θ ≥ −2).

**Theorem S.** J ≥ K′, F defined through τ(J−1), and one of: (a) X(J−1) even; (b) type a and v2(3k_{J−1}+1) ≤ K′−3;
(c) type b, ω(J−1) < K′; (d) type c, copied epoch J_W < K′. Then S(J) is tie-free with ≤ 9 chains. **No EXT hypothesis
is needed.**
*Proof.* (a) r = 0. (b) θ̃ = 1 is NT since v2(1+3k) < J−2 (indeed 1+3k ≤ 1.5(J−1)²+1 < 2^{J−2} by (C1)); j₁ < K′,
θ̃₁ = 2. (c) j₁ = ω < K′, θ̃₁ = 0. (d) location lemma. These are exactly the chain-1 entries of the level-4 generator,
which uses nothing else about J (large steps use (C1) only below K′; copies read epochs of level ≤ 3, tie-free by I-4).
Along tie-free prefixes the certificate gives r ≤ 9 (longest path: chain 1 in R₃ → R₂ → R₁(−2) → (5,5) → the 10/3
entry → 4 more chains). Theorem L's by-product shows the first ⌊J/(3 log2 J)⌋+1 ≥ 10 chains are tie-free; its only
use of "EXT below J" is C2-log at i = J−1, which here is trivial (ε(J−1) ∈ {0, 1} for types a, b) or concerns a
W-epoch with J_W < K′, covered by I-4. "Tie-free" there is h_t ≥ 1, the same sense as TIE2 §5 step 4, so it replaces
TIE2's Lemma LM. ∎
(Case (b) is also covered by RA.)

**Corollary 4.** EXT holds for every J < K″. *Proof.* J < K′: I-4. K′ ≤ J < K″: (C1) gives j₁ ≤ log2(6(J−1)²+5) < K′,
ω(J−1) < K′ and J_W ≤ log2(3(J−1)²+4) < K′, so Theorem S applies. ∎
**Corollary H″ (horizon).** F is defined for s < (2^{K″}−4)/3 and #1 does not halt during the first 2^{K″} − 2 top
steps. *Proof.* As PROOF_EGX Corollary H with K″ for K′: every level fire at s < (2^{K″}−4)/3 has J = v2(3s+4) < K″, so
by Corollary 4 and Theorem U(b) restricted to this prefix its exit is tie-free and terminates; every singleton
n = 2^v w − 2 < 2^{K″} − 2 has v < K″ and τ(v−1) ≤ (v−1)² inside that prefix, so S(v) is tie-free and EGX with E1–E4
excludes a halt up to the next singleton. ∎

## 5. Negative results (what does not work)

- **Theorem O [A, about the method]** (route A §5): no certificate built from real data below a finite N, adversarial
  data above N subject to (C1), τ(n) ≥ (n−1)/2 and the location lemma, and any exact symbolic information, closes the
  tower. The required families include all of ℤ (window Lemma W) and the 3-adic orbit c_m = −3 + 8·3^{−m}
  (Lemma O: 10/3, −1/3, 46/9, …; infinitely many distinct residues, by pigeonhole some agree mod 2^B and split later);
  at level ≈ 2^{N−2} a non-descending large step is consistent with every constraint. Level 5 has exactly one failure
  ('pair', 5, 5) (route A §7). Latent gen.py defects relevant only from level 5–6 on: emission-landing checks use the
  origins present in that iteration; `nt_by_size` admits denominators q < 10^4 while Lemma M's landing needs q ≤ 3.
- **Exact ties are real obstructions [A]** (route D §3): at the first exact tie x = 2^m(γ, μ), E(w,J) halts at that
  chain iff 3wγ + μ = 2^k; if solvable, infinitely many odd w halt there. So a J-only hypothesis must exclude solvable
  exact ties. Route D's EG-ALL (§6 there; w-uniform, J-only, strictly weaker than EXT\*, but not a finite check) is the
  weakest such hypothesis found; with Lemma DENS it also controls F.
- **No monovariant [C]** (route B §6, route C §9): every non-descent is a valuation coincidence or is inherited from a
  smaller epoch (route B Cor CL); after the first own coincidence the walk reads fresh high bits of real data (TIE2's
  hidden-k obstruction). Closing would need "S1 for shifted copies", a uniform bound on climbs inside copy towers.

## 6. Where EXT now stands

Combining U\*, RA and S (each case checked by auditor 2): J < K″ is Corollary 4; for J ≥ K″, X(J−1) even gives r = 0,
type a is RA (no hypothesis), and type b/c with shallow first return is Theorem S (no hypothesis). Hence:

**#1 never halts provided: for every J ≥ K″ with F defined through τ(J−1), X(J−1) odd of type b or c, and
ω(J−1) ≥ K′ (type b) or copied epoch J_W ≥ K′ (type c), S\*(J) has no exact tie.**

By L′ (EXT\* form, applied inductively) such a failure needs > J/(3 log2 J) non-descents; by RB the walk is an exact
shifted copy V(C, −1) of a real epoch until its first real a-step, after which it ends unless that real chain has j = 1.
Data (all J ≤ 10^8, all deep entries < 10^8) show no tie and no non-descent along real entries. The open core is
unchanged: bounding climbs inside nested shifted copies of real epochs.

## 7. Reproduce
See each `route_*/REPORT.md` §Reproduce (scripts find the repo root relative to their own location). Fast checks:
`route_b/e8_budget.py`, `route_c/check_calendar.py`, `check_absorb.py`, `check_routes.py`, `route_d/exp4.py`,
`route_a/check_family.py`, `validate_psi.py`; long: `route_a/gen.py 4 4` (level 4, ≈ 8 min), `route_c/run_all.py 1e8`
(7 min, ≈ 9 GB). Caches (`*.pkl`) are rebuilt on first run.

## 8. Review record (2026-10-17)
Reviewers: reviews/claude_ext_adversary.md, claude_ext_auditor1.md, claude_ext_auditor2.md (auditors mutually blind,
own code). No claim refuted.
- Adversary: Theorem S + Corollary 4, RA, U\* closed; L′ off-by-one; §5/§6 wording. Reran gen.py level 4 (0 failures);
  own pair-map walk to 2·10^5 crossings checks τ bound, Lemma K, AB (248,638 states), RA (60,573 J).
- Auditor 1: RA/K/HP/AB confirmed to pointer 10^6 with own exact pair map; BR = own S(J) for J ≤ 10^6+1; U\* confirmed
  against an own brute-force top map (≈ 2.1M runs, ≈ 286k comparisons); F1–F2 confirmed (200,000 a-steps); L′ off-by-one
  and Theorem S under EXT\* in §6 flagged.
- Auditor 2: F1–F3, Lemma M, τ bound, generator rules and level 4 confirmed (gen.py rerun + independent mygen.py
  reproducing every level-1..4 count + brute force 40,500 runs); Lemma LM replacement and the J ∈ [K′, K″) reduction
  confirmed; U\* and §6 confirmed with wording fixes.
Fixes applied: L′ restated with L+1 non-descents and (L+2)(g−4) chains, plus EXT\* form; Theorem S(b) uses (C1) and
≤ K′−3; Theorem S shown to need no EXT hypothesis (adversary, auditor 2), which also settles auditor 1's §6 point;
starred readings of E1–E3/EGX/C2-log stated; BR's scope stated; HP "end together" wording; F2(ii) precision condition;
F3 wording; horizon proof written (Corollary H″); §5 "halts at that chain", EG-ALL wording, orbit-density wording,
[C] tag; famlib.py path fixed. Adversary re-review of the revised file: closed in all states (F3 wording then
corrected per its point 6: its earlier F3 objection was withdrawn). Route A's sentence "Γ_y ≤ J_W/4 + 80" (route_a REPORT §3) is wrong for large J_W but
harmless (copy precision v ≥ ρ_W − J_W + 1 is astronomically large).

VERDICT: ACCEPTED (Theorem U\* with Prop 2.1; Lemmas K, HP, AB and Theorem RA; Prop RB; Lemma BR, Theorems L′ (as
corrected) and L″; Ψ-lemmas F1–F2, Lemma M, Theorem S, Corollary 4 and Corollary H″). EXT and EXT\* remain open.
