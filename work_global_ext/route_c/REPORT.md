# Route C report: adversarial and structural attack on EXT (subagent, 2026-10-17)

(Saved by the parent session from the subagent's hand-back; subagents cannot write report files.)
Tags: [A] proved, [B] finite computation (script named), [C] empirical/conjectural.

EXT not broken: no tie and no long exit anywhere (every exit ≤ 6 chains seen). Route a proved without NT
(Theorem RA). Routes b/c reduce exactly to shifted copies of real epochs; the core (bounding climbs inside
nested shifted copies) is open.

## 0. Results
| # | statement | tag |
|---|---|---|
| E1 | S(J) for every 2 ≤ J ≤ 10^8: no ties, no non-descents, r ≤ 3 | B |
| E2 | Deep J: exact automaton tails from every (m, θ), m < 10^8; all real entry classes clean, length ≤ 4 | B |
| K | Classification of odd crossings (a, b, c) | A + B |
| HP | Shadowing: two walks agreeing to precision P have the same parameter word while j\*+Γ\* < P | A |
| AB | Absorption: a chain with exact phase Θ − x = 2 is followed to its end by a copy of a real epoch | A |
| RA | Route a closed, no NT hypothesis | A + B |
| RB | Routes b/c are exact shifted copies; dichotomy at the first real a-step | A + B |
| SC | Shift calculus for an arbitrary state | A |
| CY | The word 17,5,17,5,17 never occurs | A |
| G | 2-adic adversary results | B |
| L′ | Small improvement of Theorem L's by-product | A |
| R1, R2 | Conjectures on exit length | C |

## 1. Setting
State (j, Θ, x = 2^j u, u odd), n = j−1, reads only X(n) (PROOF_EL A1/A2). End: X(n) even or n ≤ 3.
a-step (X(n) odd type a, τ(n) = 2k): x′ = 2(Θ+3k) − 2^n u = 2Θ + 6k − x/2, j′ = v2 x′, Θ′ = Θ + 3 + 6k.
b/c-step (C_n = (c′_n, λ′_n) W's chain at τ(n)): x′ = c′_n u + λ′_n, j′ = ω(n), Θ′ = Θ + 3 + 3τ(n),
v2(c′_n) = n − ε(n) > ω(n). Walks obeying this: real F chains (Θ = 3s+5, x = λ_x); β-walk of S(J) (Θ = 3d+1,
x = β_x, chain 0 = (J, 1, u = 0); tie-free iff j_t < J − Γ_t; `sj.py`, = verify_m.sym_exit for J ≤ 20000);
virtual walks. σ = v2(c_x), S1: j < σ; σ_0 = ρ, σ_{t+1} = σ_t − 1 − ε(n_t); type-c crossing i after chain t:
ε(i) = i − σ_t + 1 (PROOF_M 3.3). Phase φ = Θ − x; real fires have phase 1.

## 2. Empirics [B]
**2.1 all J ≤ 10^8** (`run_all.py 1e8`, 7 min, ~9 GB): r: {0: 37839071, 1: 57411682, 2: 4749245, 3: 1}; the
r = 3 case J = 50148477, chains [J, 27, 6, 1], word aab. No ties, no non-descents. Words "", b, a, ba, c, aa, ab,
bb, ca, aab. Routes a 30288015, b 30288015, c 1584898. max Γ = 6; chains t ≥ 2 have j ≤ 6; θ at chains ∈ {−1..3};
θ before a-step ∈ {0,1,2}. For J ≥ 64 smallest margin h = 58 (J = 65). Tail after chain 1 is a function of
(route, j_1, θ_1), 56 keys. Runs to 10^6, 10^7 reproduce PROOF_M V4.
**2.2 deep J** (`tails.py 1e8`, 21 min; exact (j,θ) automaton from every (m,θ), 5 ≤ m < 10^8; NT failures
reported not resolved): θ=2: tails ≤ 4, first 4 at m = 6131 (6131,14,5,1), 0 NT failures; θ=0: ≤ 3, 0; θ=1: ≤ 4,
one 4 (50148477,27,6,1), 0; θ=3: ≤ 3, 0; θ=4: ≤ 3, 0; θ=−1: 340 NT failures at m = 244875 + ≈293839ℓ (the g2
tower p3 → p2 → 244875 → 17 → 5 → 6); θ=−2: 1393962 failures, e.g. (17,−2) → (5,5) (PROOF_EL F). Real entries:
route a at θ = 2, route b at θ = 0, route c at θ_W − 1 with θ_W ∈ {1,2,3}. Every real entry with parameter < 10^8
is NT-clean with r ≤ 4 (≈ J < 2^(5·10^7), already inside Corollary H: consistency check only).

## 3. Lemma K [A]
X(n), n ≥ 4, odd. (a) type a: X(n) is a level fire at pointer ρ = n, step s = τ(n) = 2k_n, parameter
J = 1 + v2(3k_n + 2). (b) type b: X(n−1) is that fire; W's chain at τ(n) is the fire itself; ω(n) = v2(3τ(n)+4),
θ^W = 1. (c) type c: τ(n) is the a-return after chain t of the current epoch and is chain t+1 of that real epoch;
σ_{t+1} = σ_t − 1 = n − ε(n). *Proof.* Crossings only at top-level states (PROOF_M 3.3); P = ∅ reads E_i, E_{i+1}
(types a, b at the same step); |P| = 1 is exactly an a-return [D_t]. (a) odd with P = ∅ is a level fire, σ_0 = ρ.
(b) originals have λ = 0, λ_x = λ_A + 3 = 3s+4, the fire's own chain. (c) x = H + 2D_t + 3 is chain t+1 (PROOF_M
3.1); ε-formula gives n − ε(n) = σ_t − 1; after an a-return σ_{t+1} = σ_t − 1. ∎
[B] `check_calendar.py` to 10^6: odd crossings a 302878, b 302878, c 15850, 0 bad; first odd type-c at n = 65.
Route a: x_1 = 6k+2, j_1 = 1 + v2(3k+1); r ≥ 2 needs k odd (fire at J−1 has parameter 1).

## 4. Lemma HP (shadowing) [A]
Two walks, same table, j_0 = j\*_0, min(v2 δΘ_0, v2 δx_0) ≥ P, Γ\*_i = Σ_{i′<i}(1+ε(n\*_{i′})); for 0 ≤ i ≤ I the
starred walk reaches chain i with x\*_i ≠ 0 and j\*_i + Γ\*_i < P. Then for i ≤ I: j's, types, parities, ε's agree;
v2 δΘ_i, v2 δx_i ≥ P − Γ\*_i; the walks end together. *Proof.* Induction: δu_i = δx_i/2^{j_i} integer with v2 ≥ 1
(both u odd); a-step δx′ = 2δΘ − δx/2, v2 ≥ P − Γ\* − 1; b/c δx′ = c′_n δu, v2 ≥ n − ε + P − Γ\* − j =
P − Γ\* − 1 − ε; δΘ unchanged; a-step j′ matches since j\*′ < P − Γ\*′ ≤ v2 δx′; b/c j′ = ω(n). ∎
j ≤ log2|x| unless x = 0 (a "resonance", possible only for virtual walks).

## 5. Absorption and Theorem RA [A]
**Lemma AB.** State (j, Θ, x = 2^j u) with exact phase Θ = x + 2, m = j−1 ≥ 4, X(m) odd; C the real chain of Lemma K
((a) fire at pointer m; (b) fire at pointer m−1; (c) chain t_W+1 of the epoch whose a-return is X(m)); F defined
through the end of C's real epoch E. Then the walk copies E from C on to its end (same j's, types, ε's, same even
return). *Proof.* (a) x′ = 6k + 4 + 3·2^m u = x_C + 3·2^m u, Θ′ = Θ_C + 2^j u. (b,c) x′ = x_C + c′_m u,
Θ′ = Θ_C + 2^j u. Precision exactly σ_C ((a) ρ = m; (b) ρ = m−1 = m − ε(m); (c) σ_{t_W+1} = m − ε(m)). Along E,
σ_{C_i} = σ_C − (Γ\*_i − Γ\*_C), so S1 for real chains is HP's hypothesis. ∎ NT never used.
**Theorem RA.** X(J−1) odd type a, F defined through τ(J−1), chain 1 tie-free (j_1 ≤ J−2; under (C1) for J ≥ 10 or
given EXT below J via Theorem L). Then S(J) is tie-free and r = 1 if j_1 ≤ 4 or X(j_1−1) even; r = 2 + r_E if
X(j_1−1) odd type a/b (E the real epoch of the fire at pointer j_1−1 resp. j_1−2); r = 1 + r_W − t_W if type c.
Under EXT below J, r_E = r(J_E). *Proof.* β_x1 = 6k+2, Θ_1 = 6k+4: phase exactly 2. E starts at pointer
≤ m = j_1 − 1 ≤ J−3, so ends before the P = ∅ fire at pointer J−1 at time τ(J−1), where F is defined; apply AB.
Outer Γ at the copy of C_i is 2 + ε(m) + (Γ\*_i − Γ\*_C); S1 gives j\*_i + (Γ\*_i − Γ\*_C) < σ_C ≤ m − ε(m) ≤
J − 3 − ε(m): every copied chain tie-free. ∎
[B] `check_calendar.py` J < 10^6: even 279145, A 15822, B 7911, 0 bad; `check_absorb.py` θ = 2 tails m < 10^6:
A 302878, B 302878, even 378389, C 15850, 0 bad. Case c needs j_1 ≥ 66 (absent for J ≤ 10^8).
Corollary: iterating route-a absorption alone gives r = O(log\* J).

## 6. Routes b and c [A]
V(C, δ) := walk from (j_C, Θ_C + δ, x_C). **Prop RB.** X(J−1) odd type b/c, C = W's chain at τ(J−1).
(1) chain 1 of S(J) = V(C, −1) exactly (x_1 = x_C, Θ_1 = Θ_C − 1), automatically tie-free:
j_1 = j_C < σ_C = (J−1) − ε(J−1) = J − Γ_1. (2) b/c step C_i → C_{i+1}: V(C_i, δ) → V(C_{i+1}, δ) exactly.
(3) a-step: V(C_i, δ) → (v2(x_{C_{i+1}} + 2δ), Θ_{C_{i+1}} + δ, x_{C_{i+1}} + 2δ). (4) dichotomy (δ = −1): S(J)
copies E exactly up to the first real a-step; then j(C_{i+1}) ≥ 2 ⇒ next outer chain has j = 1, exit ends;
j(C_{i+1}) = 1 ⇒ climb to j′ = 1 + v2(u_{C_{i+1}} − 1) at a non-real state; no further a-step ⇒ ends with E.
Example: route b then a-step at a fire with half-time k: j_2 = 1 + v2(k), a climb iff k even.
[B] `check_routes.py` J < 10^6: 302878 route-b and 15850 route-c cases = V(C, −1), 0 bad.
**SC [A].** From any state with centred residue θ, q = θ − 2: the next odd step lands on the real chain C of Lemma K
with Θ-offset q, x-offset 0 (b/c) or 2q (a), neglected parts of valuation ≥ σ_C; by HP the outer walk follows the
shifted copy while it stays below precision σ_C. q = 0 is absorption. The (j,θ) automaton is this offset calculus
mod 2^j. Nesting: pure b-ancestry of depth D gives V(F, 1 − D); each b-step lowers j by ≥ 3, so depth D needs top
parameter ≥ 3D + J_F; such ancestries occur in the real orbit (g2).

## 7. Adversary [A/B]
(P1) a tie needs a long exit (L′ below). (P2) a long exit needs climbs: descending runs ≤ j chains; a climb is an NT
failure; for n ≥ 8 it needs |θ̃| ≳ 2^{n−1}; small classes n = 4, θ ≡ 5 (16); n = 7, θ ≡ 58 (128); plus route-b/c
climb of RB(4). (P3) θ moves only by −1 per fire copy, θ^W − 2 per c-copy, 3 − θ at a-steps; phase 2 does not drift;
second-order route (17, θ ≡ 30 mod 32) → (5, θ ≡ 5 mod 16) gives g2's witness at shift q = −3 above the parameter-17
fire at pointer 244873.
(P4) `gtree.py 300 300`: G(j,q): Θ = q + 2^j λ, u = λ, λ free 2-adic: walk independent of λ in all but 42 of 177295
cases (j < 300, |q| ≤ 300); those 42 are exactly (5, q ≡ 5 mod 16) and (8, q ≡ 58 mod 128), where climb height
depends on λ (unbounded; climb ≥ 300 has measure ≈ 2^−296). Every other case ends within 4 chains; 12838
non-descents, none λ-dependent, no resonances.
(P4′) `gsfam.py 2000 40`: all 1333 chains of S(J′), J′ < 2000, shifted by |δ| ≤ 40: λ-independent, end within 2.
(P5) `sfam.py 1e6 256`: 302878 real fires shifted by |q| ≤ 256 (14301927 walks): all end except 2 resonances; max
r = 4; non-descents only for q ≡ 4 (16) (13939 fires each), q ≡ 57 (128) (≈1743 each), q ≡ 29 (32) (3 each, all
parameter-17 fires); q = −3 tail 17, 5, 6, 1 (g2's tail). `test_sfam.py`: q = 0 equals S(p) for every fire.
Resonances (ρ=63, s=52, q=−124), (ρ=99, s=84, q=−199); the first is the bottom of a depth-124 b-ancestry, parent
j = 65, Θ ≡ −122 (mod 2^65); `resonance_demo.py` splits over free λ_u: deterministic continuation 65 → 5 → 62 → 1
→ end; climb stays below the parent's ceiling (hidden datum at valuation σ − 1 = 62); matches g2 family
"65 → 5 → q" for m ≤ 123.
(P6) `padic.py` (Θ, λ_u free, real table below N0): N0 = 24: longest ending walk 5 further chains
([5,17,5,17,17,1]), no cap hits, climb-past-N0 measure ≈ 1.2e−7. N0 = 28 (stopped after j0 = 5,6,7): at j0 = 5
longest 6 further chains ([5,17,5,17,24,5,1]), climb measure 7.45e−9, no cap hits.
**Lemma CY [A].** 17,5,17,5,17 cannot occur: (AA) of PROOF_RESCUE with k = τ(16)/2 = 6, l = τ(4)/2 = 1 gives
x_2 = Θ + 66 + 2^15 u; returning to 17 forces Θ + 66 ≡ 2^15 (mod 2^16); next pass starts at Θ + 48, so its
x_2 ≡ 48 (mod 2^16), v2 = 4 ≠ 17. ∎
Minimal non-descent pattern: route-b/c entry, then a copy tower of depth ≥ 2–3 above a fire of parameter 5, 8 or 17
landing in one of the classes above, then an a-step into the NT class. Exists in the real orbit (g2, r = 6). A tie
would need ≈ J/log log J nested climbs, each bounded by its enclosing precision. No tie constructed, none excluded.

## 8. Proposition L′ [A]
J = 2^l, l ≥ 10, EXT below J, F through τ(J−1), (C1), B = 4 log2 l + 9: every chain t with
t − 1 ≤ (J − 6l − 8)/B is tie-free. *Proof.* As Theorem L: d_t ≤ 2J² ⇒ j_{t′} < 2l+4, n_{t′} ≤ 2l+3; C2-log
(J_W < J tie-free by EXT below J) ⇒ 1 + ε < 2 log2(3(2l+3)² + 4) ≤ B; 1 + ε(J−1) < 4l + 3.2; a tie needs
J < 6l + 7.2 + (t−1)B. ∎ [B] `improved_L_check.py`: exact for l < 4000, inequality (i) for l ≤ 10^6.
So EXT(J) fails only if r > (J − 6 log2 J − 8)/(4 log2 log2 J + 9).

## 9. Conjectures and obstruction [C]
R1: r(J) satisfies the L′ bound for all J (even O(log J) suffices) ⇒ EXT. R2 (level descent): every climb is bounded
by the hidden precision of the enclosing step; each repeat needs a fresh tower at a strictly lower level ⇒
r = O(log\* J). Obstruction: everything reduces to iterated shifted copies V(C, q); the walk is λ-independent except
in NT classes, where it reads hidden bits (real bases or copy-tower depth); HP/AB control a copy only while the
copied object is real (S1 supplies the inequality); a shifted copy has no S1; closing needs "S1 for shifted copies",
i.e. a uniform bound on climbs inside towers ≈ EXT itself; θ windows grow ≈ 1 per tower level; resonances exist; no
finite closure found.

## 10. Least certain
1. HP b/c valuation v2(c′_n) = n − ε(n) (PROOF_M 3.2); checked by test_sfam, check_absorb, check_routes.
2. AB case (c): uses PROOF_M 3.3's ε-formula; tested only via θ = 2 automaton tails (15850), not exact β-walk.
3. RA ordering ("E ends before τ(J−1)": epochs disjoint in time and pointer order); chain-1 tie-freeness is an input.
4. P4, P5, R2 are data/conjecture. 5. tails.py exact only when NT holds.

## Files (this folder)
fdata.py, sj.py, validate.py; run_all.py (run_1e8.log, stats_\*.json); tails.py (tails_1e8.log);
check_calendar.py, check_absorb.py, check_routes.py; padic.py (padic_28.log, partial); gtree.py
(gtree_300_300.log/.json); gsfam.py (gsfam_2000_40.log); sfam.py (sfam_1e6_256.log/.json), test_sfam.py;
resonance_demo.py; improved_L_check.py.
