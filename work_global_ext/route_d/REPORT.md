# Route D report: weakening EXT by handling ties (subagent, 2026-10-17)

(Saved by the parent session from the subagent's hand-back; subagents cannot write report files.)

**Verdict.** EXT can be weakened to **EXT\*** (over-ties — v2 β > v2 α — are harmless; Theorem U goes
through with EXT\*). Exact ties are a genuine obstruction: at a solvable exact tie specific w do halt, so no
J-only hypothesis can allow an exact tie with a solvable congruence (§3). The weakest w-uniform hypothesis
is EG-ALL; anything weaker needs information on which w occur. Non-halting not proved; EXT\*, EG-ALL open.
Tags: [A] proved, [B] finite computation (script named), [C] heuristic.

## 0. Summary

| # | statement | tag |
|---|---|---|
| 1 | **Over-ties are harmless.** If v2(β_x) > v2(α_x) =: m, the real valuation is m for every odd symbol. S(J) extended through over-ties = S\*(J). EGX, E1–E4, Lemma 6.1, Lemma T(1)/(2) and the F margin hold for S\*; S\*(J) ends within J−1 exit chains. | A |
| 2 | **Theorem U\*.** (EXT\*) "for every J ≥ K′, S\*(J) has no exact tie (v2 β_x = v2 α_x)" ⇒ F defined forever and #1 never halts. EXT ⇒ EXT\*. | A (cond.) |
| 3 | **Exact ties are a real obstruction.** At the first exact tie x = 2^m(γ, μ), γ, μ odd: E(w,J) halts there iff 3wγ+μ = 2^k; if 2^k ≡ μ (mod 3γ) is solvable, infinitely many odd w halt. | A |
| 4 | **RIGID.** If F is defined, every halt is at a top step N whose whole list is (H, D), H = 6N+9−2^K, D = 2^K−3N−6, 2^K ∈ [3N+7, 6N+6]. In an endgame these are exactly type-a returns; b/c returns never halt; ties occur only at a-steps. | A |
| 5 | **F part.** F's S1 at a chain is insensitive to symbolic ties; the first ≈ρ/(2 log2 ρ) exit chains of every epoch are unconditionally safe (PROOF_CLOCK §5). Only an epoch-length bound R-EXIT is missing. | A (import) |
| 6 | **DENS.** If for every odd w the endgame of E(w,J) has ≤ L chains, then every F-epoch of parameter J has ≤ L exit chains (2-adic density of 3ℤ; F's λ_u ≡ 2^J mod 3 is never 3w). | A |
| 7 | **Theorem U-ALL.** (EG-ALL) "for every J ≥ K′ and every odd w the endgame of E(w,J) reaches its singleton within 2^{J/3} chains with no power-of-2 chain value" ⇒ non-halting. EXT ⇒ EXT\* ⇒ EG-ALL. | A (cond.) |
| 8 | Halting configurations are compatible with all mass identities and Lemma T bounds (explicit mass-consistent state with U = 3w halts under brute-force top map). | B |
| 9 | Synthetic data: over-ties : exact ties ≈ 1:1, 0 violations; ≈11% of first exact ties admit a halting w, smallest such w median 35,702 bits; after a tie the refinement tree is one 2-adic spine with side branches ending within ≤ 3 chains. | B/C |

## 1. Real top-level recursion

**Lemma R [A].** Assume F defined through τ(j−1). A real top-level chain with parameter j, odd base u ≥ 1,
entry D, rest R: list after the chain is (u+1; u, …, 2^{j−2}u, D, R); for w ≤ τ(j−1) the list is F's state
Σ_w evaluated at U = u followed by unread [E_{i_w..j−2}](u), D, R; at the return w = τ(j−1) the head is
H = c_A u + λ_A with (c_A, λ_A) = A_X(j−1), list [D]++R (type a), [2^{j−2}u, D]++R (b), [Y(u), D]++R (c);
no chain inside the call halts. *Proof.* PROOF_M 2.2–2.3 in integers: F's pair run is the real top map for
every odd U (G6 §5.2); inner chains are F chains at u with base c′u+λ′ ≥ 2u+1 ≥ 3. ∎

In an endgame R = ∅: returns are [H; D] (a) or [H; b, D] (b, c). H even ⇒ singleton H+b+c+3. H odd ⇒
X′ = H+2b+3, j′ = v2 X′, u′ = X′/2^{j′}, D′ = c+(H+1)/2, with (b,c) = (D,0) (a), (2^{n−1}u, D) (b),
(Y(u), D) (c). S(J) is the same recursion with u, D affine in a formal odd U.
[B] vs brute-force integer top map: 0 mismatches in ≈1.2·10^4 synthetic-defect runs and 32,740 late-stage
runs (`tielab.realrec`/`realstate` vs `toplist`/`toprun`).

## 2. Over-ties

Chain x = (α, β), m = v2 α < v2 β. For every odd U, αU/2^m odd, β/2^m even, so v2(αU+β) = m. S\*: at such a
chain j := m, u := x/2^m = (γ, μ), γ odd, μ even ≥ 2.

**Prop 2.1 [A].** F defined through τ(J−1). Up to the first exact tie, for every odd U: endgame of E_U(J)
= S\*(J) pair for pair (EGX\*); no chain halts; F's top-level small parts are S\*(J)'s pairs at λ_u (6.1\*);
Lemma T(1),(2) hold; S\*(J) ends within J−1 exit chains and uses X(n) only for n ≤ J−2.
*Proof.* Over-tie chain: real valuation m, u integral, real base γU+μ ≥ U+2 ≥ 3; F's λ_x = αλ_u+β has
valuation m; S1 since m = J−Γ_t < ρ−Γ_t = σ_t. Call from base with odd γ: v2(λ_u c′_x + λ′_x) = v2(λ′_x) <
v2(c′_x) = v2(γc′_x) so every W-chain image keeps S1 with the same j; inner heads have c-part c′_A γ even;
W's step 0 image is even; parity preserved (γ+μ odd); so 2.2–2.3 verbatim. Next return: n = m−1 ≥ 2 ⇒
c_A(X(n)) even ⇒ S2; n ∈ {0,1} ⇒ head (γ, μ+1) even, run ends. b/c steps: v2 β = ω(n) < v2(c′_x) ≤ v2 α,
so **b/c steps never tie in any representation**. T(1) does not use j_t (b/c: v2 α_{x_{t+1}} =
(v2 α_{x_t} − j_t) + (j_t − 1 − ε); a: mass gives α_{x_{t+1}} = 2^{J+1} − α_{x_t}/2). T(2) uses signs and
Σβ = 3d−3, both survive (μ ≥ 2, β_H odd). Termination: α_x = α_H + 2α_b even ⇒ J−Γ_t ≥ 1, Γ_t ≥ t ⇒ ≤ J−1
chains. E1, E2, E4 survive (E2 weakens c_u ≥ 2 to "c_u ≥ 1 odd" at over-tie bases). ∎

**Theorem U\* [A, cond. EXT\*].** Theorem U with Prop 2.1 replacing tie-free facts: (a) J < K′ by I-4
(S\* = S), J ≥ K′ hypothesis; (b) margin σ_t − j_t = (ρ−J) + (J−Γ_t−j_t) > 0, ≤ J−1 exit chains per epoch;
(c) EGX\* + E1–E4\* for v ≥ K′, Corollary H for v < K′. ∎
Remarks: Theorem L by-product survives with EXT\* below J (C2-log becomes ε ≤ max(3, 2J_W+1); Γ budget
4l+5.2+L(2l+4); f(l) = 2^l(l−4)/(3l) − 6l − 9.2 > 0 for l ≥ 10) ⇒ any tie, over or exact, at J ≥ K′ needs
> J/(3 log2 J) exit chains. EXT\* is a genuine but modest weakening [C]. NT failures need higher β bits
(known symbolically); over-ties need only symbol parity; exact ties need bits of U = 3w itself ⇒ no
further J-only rescue.

## 3. Exact ties

First exact tie x = 2^m(γ, μ) at chain t\*; by 2.1 it is an a-step at a 2-list.
**Prop 3.1 [A].** (1) every odd U follows S\* through t\*−1; real chain value X = 2^m(γU+μ). (2) halts iff
γU+μ is a power of 2; for U = 3w iff 3wγ+μ = 2^k (needs 3∤μ, gcd(μ,γ) = 1, μ ∈ ⟨2⟩ mod 3γ); conversely
if 2^k ≡ μ (mod 3γ), 2^k > μ, then w = (2^k−μ)/(3γ) is a positive odd integer and E(w,J) halts at t\*; also
for k + i·ord_{3γ}(2). (3) otherwise j = m + k(U), k(U) = v2(γU+μ) ≥ 1; continuation depends on U mod
2^{k+1}; with U = r + 2^{k+1}V pairs become (2^{k+1}c, λ + c r); a strictly resolved chain can halt only at
V = 0 with λ_u = 1 (V ≥ 1 ⇒ u ≥ 2V+λ_u ≥ 3). ∎
**Cor 3.2 [A].** If the first exact tie of S\*(J) has a solvable congruence, "E(w,J) does not halt for every
odd w" is false; a J-only hypothesis must exclude this; otherwise one needs which singleton times
n = 2^J w − 2 are visited. "No two consecutive ties"/"bounded tie depth": irrelevant for over-ties,
insufficient for exact ties.

Data [B] (`run_main.txt`): synthetic defects (last entry 2^{J−1}U − e) 2,303,025 runs (3 ≤ J ≤ 40,
1 ≤ e ≤ 300), 0 violations, all 51 halts at t\* exactly where αU+β = 2^K; 22,826,825 runs (|e| ≤ 300, odd
U < 2000): all 126 halts at type-a returns at chain 1 (`exp7.py`). Example J=5, e=13: x = (48, −16), halts
for U = (2^{2k+1}+1)/3 (incl. U = 3, 171, 10923…); one halt at 2-list (55, 35), N = 29, 55 = 6·29+9−2^7.
Late-stage mass-consistent states (`tielab.late_state`): of 200,000, 662 exact-tie, 590 over-tie only;
494,374 real + 32,740 brute-force runs, 0 violations; 800/800 refinement trees single spine + side branches
ending ≤ 3 chains; halting set for odd U < 2^13 equals tree prediction (150/150). First exact ties (300):
267 with no halting w (3|μ: 103; gcd>1: 20; μ∉⟨2⟩: 144), 33 solvable, smallest halting w 155..3.4·10^7 bits
(median 35,702). `example.py`: J = 17, x = 2^5(4339, 73), w = 1383913229583, 3wγ+μ = 2^54; brute-force halts
at a 2-list with H+2D+3 = 2^59; w±2 do not. [C] at a real J ≥ K′ tie, γ ≈ 2^{J−m}, halting w doubly
exponential in J or absent (~89%).

## 4. RIGID
**Prop 4.1 [A].** F defined through every index read ⇒ every halt is at a 2-list (H, D) at top step N with
H+2D+3 = 2^K, i.e. H = 6N+9−2^K, D = 2^K−3N−6, 3N+7 ≤ 2^K ≤ 6N+6; in an endgame these are type-a returns.
Proof: singletons (R4 S2), excursion steps before X(v−1) (F at U), steps inside calls (Lemma R), chains after
b/c returns (base ≥ 2u+1), first endgame chain if X(v−1) is b/c, cannot halt; sum lemma H+D = 3N+3. ∎
[B] `exp4.py` 3·10^6 real-orbit steps: odd-head steps 1,018,505 singletons, 53,295 2-lists, 53,201 longer;
X = 6N+9−H at every 2-list. Halting is consistent with mass and Lemma T (example.py); what excludes halting
in the tie-free case is β < 2^{v2 α}, which is exactly what a tie breaks.

## 5. F part without EXT
PROOF_CLOCK §5 (accepted, unconditional): at a fire at ρ > N_B every candidate j_t ≤ log2(6s+5) ≤ H(ρ) ≤
2 log2 ρ + 1, σ_t ≥ ρ − tH(ρ), so chains with index ≤ R(ρ) are safe. (R-EXIT: no epoch at ρ > N_B has more
than L_F(ρ) = ⌊ρ/H(ρ)⌋ − 3 exit chains) ⇒ F defined forever [A] (PROOF_CLOCK §6 with L_F for √ρ).
STATE-CLOCK 2^J < 7ρ² ⇒ L_F(ρ) > 2^{J/3} for J ≥ 60. Missing without EXT: an exit-length bound for epochs
with an exact tie. [C] synthetic: end ≤ 3 chains after the tie.
**Lemma DENS [A].** If for every odd w the real recursion of E(w,J) ends within L chains with no power-of-2
chain value (reading only defined crossing data), then for every odd U, R(U,J) (no halting check) ends within
L chains; every F-epoch of parameter J has ≤ L exit chains. Proof: first min(L+1, end) chains determined by
U mod 2^B (affine forms over ℤ[1/2]; X(U\*)−X(U) = p(U\*−U)); CRT gives U\* = 3w, w odd, in that class; same
types/parameters; L+1 chains for U ⇒ L+1 for E(w,J). F's epoch = R(λ_u, J) through its safe prefix. ∎
Endgame bound supplies (b) iff proved for all odd w (λ_u ≡ 2^J ≢ 0 mod 3: an F-epoch is a 2-adic limit of
excursion endgames, never one).

## 6. Weakest w-uniform hypothesis
**Theorem U-ALL [A, cond.].** EG-ALL ⇒ non-halting. (b) epochs J < K′ by I-4; J ≥ K′: first L_F(ρ) chains
safe, read indices < ρ; DENS with L = 2^{J/3} < L_F(ρ) bounds the epoch; R-EXIT. (c) excursions v ≥ K′ by
EG-ALL at own w, Lemma R excludes halts inside calls, Cor H for v < K′. EXT\* ⇒ EG-ALL by 2.1. ∎
EG-ALL allows exact ties whose refinement tree is halting-free and bounded; fails at any J whose first exact
tie has a solvable congruence; not a finite check (spine infinite, reads X(n) for all n ≥ m). Non-uniform
weakest: R-EXIT for F + "no actual endgame 2-list equals (6N+9−2^K, 2^K−3N−6)" ≈ the conclusion.

## 7. Least sure
1. Theorem U\*: possible hidden use of "c_u even" elsewhere; the new case (odd c_u after over-tie) handled in 2.1.
2. DENS data clause / no circularity in (b) induction — reviewer should confirm.
3. RIGID needs F through τ(j−1) for j up to ≈ J + log2 w after an exact tie.
4. Synthetic data are not reachable data (no real tie known; V4 none for J < 10^6); row 9 is [C].
5. No proof of EXT\*, EG-ALL, or non-halting claimed.

## 8. Files (this folder)
`tielab.py` (F walk, S\*, real recursion, brute-force top map, refinement tree, late-stage generator);
`exp1.py` … `exp7.py`, `exp5_helpers.py`, `example.py`; `run_main.txt`. Reproduce:
`python3 -B exp1.py 40 300; python3 -B exp3.py 1 200000; python3 -B exp4.py 3000000; python3 -B exp5.py;
python3 -B exp6.py 7 400 30; python3 -B example.py; python3 -B exp7.py`.
