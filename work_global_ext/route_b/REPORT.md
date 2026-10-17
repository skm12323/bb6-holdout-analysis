# Route B report: bounding the exit length of S(J) (subagent, 2026-10-17)

(Saved by the parent session from the subagent's hand-back; subagents cannot write report files.)
Tags: [A] proved, [B] finite computation (script named), [C] heuristic.

## 0. Verdict
No proof of LIN-EXIT or any o(J/log J) exit bound. Obtained: an exact β-only reduction, two strictly weaker
sufficient conditions for EXT (L′, L″), a local valuation calculus classifying every non-descent, a
self-similarity identity for route a, and the r(J) profile to J = 10^6+1 plus deep tails to m = 10^6+1.

| # | statement | tag |
|---|---|---|
| BR | After the fire, S(J) is an explicit integer walk on (j, d, β_u), using only F's crossing table; α enters only via v2(α_x) = J − Γ_t. | A, B |
| L′ | Given EXT below J, every chain of S(J) preceded by ≤ ⌊J/(3 log2 J)⌋ **non-descents** is tie-free. (ND-EXIT) ⇒ EXT. Descending steps cost nothing. | A |
| L″ | LIN-EXIT weakens to r ≤ (J − 6 log2 J − 8)/(4 log2 log2 J + 8) − 1. | A |
| P | Pins: exact clock relations; control only the first non-descent. | A |
| Q | Three-term rule for a–a transitions; ties after an a-step are a pure crossing-table condition. | A, B |
| O | Three-term rule at the end of a b/c run (offset junction). | A, B |
| CL | Every non-descent is a valuation coincidence or inherited from a smaller F-epoch. | A |
| SS | Route a: r(J) = 2 + r(j_2), conditional on NT along both exits. | A (cond.), B |
| DATA | J ≤ 1,000,001: r ≤ 2, no tie, no non-descent. Deep route-a/b tails to m ≤ 1,000,001: tail ≤ 3, so r ≤ 4. | B |
| OBS | EXT reduces to a *rarity* bound on coincidences per exit; coincidences read fresh high bits (TIE2 hidden-k obstruction); no monovariant. | — |

## 1. Notation
Chains t = 0 (fire), 1, 2, …, n_t = j_t − 1; d_0 = 0, d_{t+1} = d_t + 1 + τ(n_t); Γ_t = Σ_{s<t}(1+ε(n_s));
h_t = J − Γ_t − j_t; Θ_t = 2^Jλ_u + 3d_t + 1 (β-part 3d_t+1); k_n = τ(n)/2 at odd type-a crossings; ω(n) the
parameter of F's chain at step τ(n), (c_W(n), λ_W(n)) its pair; par(n) parity of F's head at X(n) (X(0..3)
even). Chain t tie-free ⇔ h_t ≥ 1. Step t → t+1 is a **non-descent** if j_{t+1} ≥ j_t (for an a-step exactly
an NT failure; b/c steps always drop by ≥ 3). Standing hypotheses for L′, L″ (as PROOF_EGX Theorem L):
J ≥ 2^10, F defined through τ(J−1), EXT for all J′ < J, (C1) τ(n) ≤ n².

## 2. Lemma BR [A]
β-walk on (j, d, b), n = j−1: par(n) = 0 ⇒ stop; type a: B := 6d + 2 + 3τ(n) − 2^n b; type b/c:
B := b c_W(n) + λ_W(n); then d ← d+1+τ(n), j ← v2 B, b ← B/2^j. Started at (J, 0, 0) it reproduces
(j_t, β_{x_t}, d_t), t ≥ 1, while S(J) is tie-free and stops exactly at the even return; chain t tie-free iff
j_t + Γ_t < J. *Proof.* Parity: H = M_u(A_X); n ≥ 2 ⇒ c_A even ⇒ parity = par(n); n ≤ 1 ⇒ A_X = (1,1), H even.
Type a: Lemma T(2) mass at the return, β_H + β_{D_t} = 3d_{t+1} − 3, A_X = (2^n, 3τ+1) ⇒
β_x = 6d_t + 2 + 3τ − 2^n β_u. b/c: x = M_u(A_X + 2b_W + (0,3)) = M_u(x_W). Tie: Lemma T(1). ∎
Forced b/c parameter: v2(c_W) = n − ε(n) > ω(n) (F's S1 at τ(n)), so a b/c step goes to j′ = ω(n) whatever
the state; only a-steps depend on the state.
**Cor BR′ [A]** (τ = τ(J−1)): route a (j_1, d_1, β_x) = (v2(3τ+2), 1+τ, 3τ+2); route b (ω, 1+τ, 3τ+4), F's
chain at τ(J−1) being the level fire at pointer J−2; route c (ω, 1+τ, λ_W(J−1)). For routes a, b the whole
exit after the fire is a function of τ(J−1) alone; later steps read F only at indices ≤ log2(6d).
[B] `e1_check.py`, `e3_profile.py 30000`: BR = symexit for 3 ≤ J ≤ 30001. `lazy.py a|b 64` enumerates all
even τ < 2^64 lazily: the tail depends on τ only through m = v2(3τ+off), exactly 64 cylinders.

## 3. Budget theorems [A]
l = ⌊log2 J⌋, g = ⌊log2(12J²)⌋, g1 = ⌊log2(6(J−1)²+5)⌋, eps1 = max(3, 2⌊log2(3(J−1)²+3)⌋ − 1).
**Theorem L′.** L = ⌊J/(3l)⌋. If chains 1..t−1 are tie-free and ≤ L steps s → s+1 (s < t) are non-descents,
chain t is tie-free. Hence (ND-EXIT: for J ≥ K′ every tie-free prefix of S(J) has ≤ ⌊J/(3 log2 J)⌋
non-descents) ⇒ EXT; by-product given EXT below J: every chain preceded by ≤ L non-descents is tie-free.
*Proof.* (1) Sizes: continuing chains have j ≥ 5 (PROOF_EL Lemma 1); maximal strictly decreasing blocks:
≤ L+1 blocks of ≤ g−4 elements, so ≤ (L+1)(g−4) chains; by induction with (C1)
d_s ≤ 1 + (J−1)² + (L+1)(g−4)(1+(g−1)²) ≤ 2J², T(2) ⇒ j_s ≤ g. (2) h_{s+1} − h_s = j_s − j_{s+1} − 1 − ε(n_s):
≥ 1 at b/c steps (ω(n) ≤ n − ε(n) − 1, F's S1, PROOF_M 3.2); ≥ 0 at descending a-steps; ≥ −(g−4) at a
non-descent. (3) h_1 ≥ J − 1 − eps1 − g1 (route a: Γ_1 = 1, j_1 ≤ g1; b/c: ε(J−1) ≤ eps1 by C2-log, W-epoch
J_W < J tie-free by EXT below J, j_1 = ω ≤ g1). (4) h_t ≥ h_1 − L(g−4) ≥ (J/3)(1 − 1.6/(x−1)) − 6x − 5.8 > 1
for x = log2 J ≥ 10, increasing in x. ND-EXIT ⇒ EXT: Theorem L's strong induction with chains → non-descents. ∎
**Theorem L″.** E = 2⌊log2(3(g−1)²+3)⌋, L2 = ⌊(J − g − 2 − eps1)/E⌋: every chain t ≤ L2+1 is tie-free.
*Proof.* every index n ≤ g−1; at type-c, C2-log ε(n) ≤ max(3, 2J_W − 1), J_W ≤ ⌊log2(3n²+3)⌋ < J ⇒ 1+ε ≤ E;
Γ_t ≤ 1 + eps1 + L2 E ≤ J − g − 1 ⇒ J − Γ_t > g ≥ j_t. ∎ E ≤ 4 log2 log2 J + 8.
[B] `e8_budget.py`: both inequalities in exact integer form at J = 2^10…2^199, 2^256, 2^512, 2^1024, 2^2048,
2^4096 and 20,000 random J ∈ [2^10, 2^300): pass. L2 vs J/(3l): J/21.8 vs J/30 (2^10); J/30 vs J/192 (2^64);
J/54 vs J/12288 (2^4096).

## 4. Local valuation calculus
**Lemma P [A].** (a) Θ_t − Θ_s = 3(d_t − d_s). (b) Θ_1 ≡ 2 (a), 0 (b), θ^W − 1 (c) mod 2^{j_1}. (c) chain s
created by a descending a-step ⇒ Θ_s ≡ 3 + 3k_{n_{s−1}} mod 2^{j_s − 1}. (d) Θ_s ≡ ρ mod 2^μ, n_t ≤ μ, non-descent
at t ⇒ R := ρ + 3(d_t − d_s) + 3k_{n_t} ≡ 2^{n_t−1} mod 2^{n_t}, so |R| ≥ 2^{n_t−1}. Consequence: the first
non-descent can only occur at j ≤ 2 + log2(|θ̃_1| + 3j_1(1+g²) + 1.5g²) = O(log log J) for routes a, b; after it
the new pin 3 + 3k + β_x/4 has size O(d). Example RESCUE tie (17) → (5,5): ρ = 21 ≡ 5, R = 24 ≡ 8 mod 16.
**Lemma Q [A].** Chains t, t+1 both followed by odd type-a returns, k = k_{n_t}, k′ = k_{n_{t+1}}:
β_x(t+2) = β_x(t+1)/2 + 2^{n_t}β_u(t) + 6(1+k+k′), valuations j_{t+1}−1, n_t, 1+v2(1+k+k′); min attained once
or thrice ⇒ j_{t+2} = min; exactly twice ⇒ larger. (PROOF_RESCUE (AA) in β-form.) Q2: after a descending a-step,
chain t+1 non-descent iff v2(1+k_{n_t}+k_{n_{t+1}}) = n_{t+1} − 1 (a "tie pair"; forces n_{t+1} ≤ 2 log2 n_t + O(1)).
Q3: after a strict rise an immediate a-return falls to j_{t+2} < j_t unless v2(1+k+k′) = n_t − 1. Q4: after an
equal tie then a-return: j_{t+2} = 1+v2(1+k+k′) if < n_t; = n_t if equal; else ≥ j_t (another non-descent).
[B] `e6_lemmaQ.py` 70,000 random a–a pairs (5,823 Q2 non-descents, 804 Q3 fall-backs), no failure.
[B] `e9_tiepairs.py` n ≤ 30000: n′ = 4: 836 partners (16, 53, 89, …); n′ = 7: 105 (138, 424, …); n′ = 13: 2
(9170, 27536). RESCUE tie = pair (16,4): 1+6+1 = 8.
**Lemma O [A].** Chain s fire or a-created, s+1..t b/c-created, t followed by odd type-a return: chain s+i =
M_{u_s}(C^W_i) (F's consecutive chains from τ(n_s)); Θ_{s+i} = Θ^W_i + δ_s, δ_s := Θ_s − 2;
x(t+1) = x^W + 2δ_s − 2^{n_t} c_{u^W} β_u(s), v2(c_{u^W}) ≥ 1; j_{t+1} = unique min of (j^W, 1+v2 δ_s,
n_t + v2 c_{u^W}). s = 0 (routes b, c): x(t+1) = x^W − 2 ⇒ j_{t+1} = 1 (exit ends) unless j^W = 1.
[B] `e7_lemmaO.py` 658 junctions, no failure.
**Cor CL [A].** A non-descent t → t+1 (t ≥ 1) needs an odd type-a return after chain t plus one of (Na) two-way
min coincidence in Q; (Nb1) inherited non-descent of the copied F-epoch (J_W ≤ log2(3n²+4)) with 1+v2 δ_s ≥ j_t;
(Nb2) j^W = 1 + v2(Θ_s − 2).
**Lemma Z [A].** At a-steps z := 3β_x − 12d − 4 satisfies z′ = −z/2 − 6k − 12; b/c steps reset z to size ≈ d; no
monovariant. [B] 31,672 a-steps.
**Lemma SS [A, cond. NT on both exits].** X(J−1) odd type a and X(j_1−1) odd type a or b ⇒ automaton state at
chain 2 is (j_2, 1), a fire state, so r(J) = 2 + r(j_2), j_2 ≤ log2(3j_1²+4). X(j_1−1) type c ⇒ exact copy
(δ = 0) of an F-exit. Routes b, c start at θ = 0, θ^W − 1 (TIE2 drifting windows). [B] 11 instances J ≤ 4000.

## 5. Empirical profile [B] (`stream.py N`; all checks zero violations)
| range | r=0 | r=1 | r=2 | ties | non-desc | max Γ | min h | max j_1 | max j_t (t≥2) |
|---|---|---|---|---|---|---|---|---|---|
| J ≤ 30,001 | 11,352 | 17,222 | 1,425 | 0 | 0 | 6 | 1 | 16 | 4 |
| J ≤ 300,001 | 113,517 | 172,234 | 14,249 | 0 | 0 | 6 | 1 | 19 | 4 |
| J ≤ 1,000,001 | 378,392 | 574,115 | 47,493 | 0 | 0 | 6 | 1 | 21 | 4 |
(10^6 run 1750 s; agrees with PROOF_M V4.) Deep tails m ≤ 1,000,001 from route-a/b chain-1 states (canonical
residue + random lift): route a tails 0/1/2/3 = 378,393 / 574,116 / 47,436 / 56; route b 378,393 / 574,171 /
47,437 / 0; no τ-dependence, no non-descent; tail 3 first at m = 6131 (6131 → 14 → 5 → 1, r = 4). By BR′ these
are exactly the exits of S(J) for **every** J (incl. J ≥ K′) whose first step is route a/b with j_1 = m ≤ 10^6+1.
Generic states: [B] `lazy2.py` max non-descents 1 (B=12), 2 (16), 3 (20, 24); [C] `e5_generic.py` 200,000 random
200-bit states: 0.31% one non-descent, none two.

## 6. Precise obstruction
1. EXT needs only a rarity statement (≤ J/(3 log2 J) non-descents per exit, or ≤ J/O(log log J) chains; even
   polylog would do). 2. Every non-descent is a valuation coincidence of explicit integers or inherited from a
   smaller F-epoch (nesting ≈ log* J). 3. Before the first own coincidence Lemma P pins everything; after one, the
   next parameter reads bits above the pin (TIE2 §7 hidden-k bits). 4. No monovariant. 5. A size-only universal
   statement ("from any β-state with d < 2^B, at most C·B non-descents") would suffice and fits the data [C], but
   needs equidistribution of valuations along a deterministic orbit.

## 7. Least sure
L′ b/c gain (ω(n) ≤ n − ε(n) − 1; checked at 15,821 b/c steps); L′ block count (j ≥ 5, d-bound in induction);
L″ uses C2-log as accepted; Lemma O needs shared returns; SS conditional; generic enumerations over-approximate.
Nothing proves LIN-EXIT, ND-EXIT, NT or EXT for J ≥ K′.

## 8. Reproduce (in ext/b)
python3 -B e1_check.py 30000; e3_profile.py 30000; stream.py 300000 (~3 min); stream.py 1000000 (~30 min);
lazy.py a 64; lazy.py b 64; lazy2.py 24 20 5,8,12,14,17; e5_generic.py 200000 200; e6_lemmaQ.py; e7_lemmaO.py;
e8_budget.py; e9_tiepairs.py. `core.py` caches F as walk_30000.pkl (~80 MB).
