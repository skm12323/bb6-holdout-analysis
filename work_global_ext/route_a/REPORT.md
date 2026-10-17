# Route A report: can the tower be closed uniformly? (subagent, 2026-10-17)

(Saved by the parent session from the subagent's hand-back; subagents cannot write report files.)
Tags: [A] proved, [B] finite computation (script named), [C] heuristic.

## Files (this folder)
`verify_tie2_copy.py` (REPO work_tie2/verify_tie2.py with ROOT changed; `run_tie2_reproduction.txt` matches REPO:
level 4 9,035,944 entries, 49,788 ties resolved, 1 failure ['pair', 5, 5]; 10/3 macro family 999,999 entries, 0
failures). `famlib.py` (cached real crossing data `_walk.pkl`, exact Ψ-family automaton `make_psi`).
`check_family.py` [B] (F1–F3 on 130,000 random instances: F2 29,806 NT, 24,096 ties, 6,098 j−1 cases; F1a/b/c, F3
20,000 each; all pass). `validate_psi.py` [B] (Ψ-automaton vs 18,865 brute-force integer chains from 11 families,
incl. 40 tie entries; all agree: 4,019 END, 1,974 EXT, 2 ANYJ). `orbit.py` [B] (§4). `gen.py` [B] (level generator
with exact Ψ-families; `python3 -B gen.py 5 4`; log `run_gen5.txt`, data `gen_certificate.json`; 22m42s, 4 workers).
`test_psi.py`.

## 0. Verdict
1. **Negative: no finite symbolic state space is closed under the level generator** (Theorem O, §5, [A]); not a
   state-design issue (item 2 removes information loss). Growth mechanisms: integer drift (Lemma W: level l small
   any-j families contain all of [−(l−1), l+1]); a 3-adic orbit (Lemma O: c₀ = 5, c_{m+1} = (c_m − 6)/3,
   c_m = −3 + 8·3^{−m}, v2(c_m+3) = 3, ties at X(4); level l contains c_m for m ≤ l−4; = TIE2 §7's rational
   families 10/3, −1/3, 46/9, …); size failure at level ≈ 2^{N−2} (S-a fails).
2. **The hidden-k state of TIE2 §7 exists and is exact** ([A], §3): Ψ(j; P, Q): Θ ≡ P + Q·2^j λ_u, P, Q 2-adic;
   closed under every transition; a tie emits one any-j family by explicit formulas.
3. **Uniform positive statements.** Theorem S [A + imported TIE2 B]: every J whose first return is "shallow" exits
   tie-free with ≤ 7 chains (≤ 9 with level 4); EXT can fail only at J where some s ≤ τ(J−1) has 3s+2 ≡ 0 or
   3s+4 ≡ 0 mod 2^{K′}. Corollary 4: EXT for all J < K″ ([A + B]; Lemma LM replacement needs audit, §8.1; does not
   use Lemma LM; level 4 independently re-certified with exact families, 0 failures).
4. Level 5 not certified: one failure, pair (5,5) with minimal information, from copies of specific a-output pairs
   (§7); cure described, not cheap, not pursued.

## 1. Level generator (TIE2 §3)
Tower T₁ = N = 10^6, T_{i+1} = 2^{T_i/2 − 2}; H = T₂, K = T₃, K′ = T₄, K″ = T₅, K‴ = T₆. R₀ = [1, N),
R_i = [T_i, T_{i+1}); S(J) has level l if J ∈ R_l. Chains with j ≥ N are "large": X(j−1) adversarial, constrained
only by (C1) τ(n) ≤ n², the location lemma, and **new lower bound τ(n) ≥ (n−1)/2** (pointer advances ≤ 2 per step,
so k_n ≥ (n−1)/4; fixes TIE2's θ ≥ −2 restriction in S-a).
Rules of G_l from AO₀..AO_{l−1}: (C1) chain 1 puts (R_i, 2) [route a] and (R_i, 0) [route b] in every i ≤ l−1;
route c adds a-outputs of AO_{lw}, lw ≤ l−1, shifted by −1. (Ba) big θ ∈ B(i) gives 3−θ in every R_{i₂}, i₂ < i.
(Bb) gives θ−1. (Bc) gives each a-output of AO_{lw}, lw < i, shifted by θ−2. (S) small entries run on real data;
their a-outputs with any-j outputs of (C1a), (Ba) form AO_l. Large-state rules are shift-invariant i ↦ i+1, so
G_l = G_{l−1} shifted + new top range {0, 2} + copies of AO_{l−1}; each window grows by 1 on each side.
| level | big states (top first) | small any-j | entries | ties resolved | failures |
|---|---|---|---:|---:|---:|
| 1 | — | {0,2} | 2,000,024 | 0 | 0 |
| 2 | {0,2} | [−1,3] | 5,000,059 | 3 | 0 |
| 3 | {0,2},[−1,3] | [−2,4] | 7,000,101 | 13,949 | 0 |
| 4 | {0,2},[−1,3],[−2,4] | [−3,5] + 10/3 (Q=2/3) | 10,035,943 | 63,728 | 0 |
| 5 | {0,2},[−1,3],[−2,4],[−3,5]∪{10/3} | [−4,6] + −1/3, 7/3, 7/3 (Q=2/3), 10/3 (Q=2/3), 46/9 (Q=2/3) | 16,165,294 | 220,927 | 1 |
Level 4 count = TIE2's 9,035,944 + 999,999 of the 10/3 family (now automatic). Further-chain counts: level 4
{0: 3,793,990, 1: 5,813,924, 2: 404,097, 3: 23,924, 4: 8}; level 5 {0: 6,116,194, 1: 9,348,851, 2: 652,448,
3: 47,791, 4: 10}. Tie emissions: level 4 one (5 → 10/3); level 5 adds −1/3 → 46/9.

## 2. Lemma W [A]
For l ≥ 2, 0 ≤ i ≤ l−2 (i = 0 the small any-j set): B_l(i) ⊇ [−(l−1−i), l+1−i]; B_l(l−1) ⊇ {0, 2}. Downward
induction: base i = l−2 from {0,2}: (Bb) {−1,1}, (Ba) {3,1} ⇒ [−1,3]; step B(i+1) ⊇ [a,b], a = −(l−2−i), b = l−i:
(Bb) [a−1, b−1], (Ba) [3−b, 3−a] = [3−l+i, l+1−i], overlapping ⇒ [−(l−1−i), l+1−i]. ∎ Matches data l ≤ 5.
Consequence: minimal-information pair (5,5) unavoidable by any finite window (TIE2 §6.1: unresolvable).

## 3. Ψ-families [A]
a-step at n = j−1, k = k_n: x′ = 2(Θ+3k) − 2^{j−1}λ_u, j′ = v2 x′, λ_{u′} = x′/2^{j′}, Θ′ = Θ + 3 + 6k.
b/c-step: Θ′ = Θ + 3τ + 3 = Θ + Θ_y − 2, λ_{u′} = λ_{uy} + c_{uy}λ_u, j′ = j_y, v := v2(c_{uy}) = σ_y − j_y.
Ψ(j; P, Q; r, m) to precision p: λ_u ≡ r (mod 2^m), Θ ≡ P + Q 2^j λ_u (mod 2^p). Any-j family Ψ(·; P, Q).
**F1.** Θ_t ≡ P mod 2^{j_L}. (a) after odd a-return with j′ < j_L − 1: Θ′ − 2^{j′}λ_{u′} = 3 − Θ_t +
2^{j_L−1}λ_{u_t}: Ψ(j′; 3−P, 1) to precision j_L − 1. (b) after b-return: Θ′ − 2^{j′}λ_{u′} = Θ_t − 1 −
2^{j′}c_{uW}λ_{u_t}: Ψ(j′; P−1, 1) to precision j_L − 2. (c) c-copy of y ∈ Ψ(j_y; P_y, Q_y) (prec p_y):
Ψ(j_y; P+P_y−2, Q_y) to precision min(j_L, p_y, j_y+v). (d) the fire is Ψ(J; 1, 1) exactly. Proof by substitution. ∎
Precision: any-j families come from (C1) (j_L = J ≥ N), a large state (j_L ≥ N), or a copy of an a-output of an
epoch of level ≥ 1 (v = σ_y − j_y ≥ J_W − Γ_y − j_y ≥ 7·10^5, using Γ_y ≤ J_W/4 + 80, j_y ≤ 2 log2 J_W + 4).
Automaton works at 2048 bits and asserts it never needs more.
**F2.** E = P + 3k, ν = v2 E, P′ = P + 3 + 6k − 4QE/(4Q−1), Q′ = 2Q/(4Q−1); x′ = 2E + 2^{j−1}(4Q−1)λ_u.
(i) ν ≤ j−3 (NT): j′ = ν+1, Ψ(j′; P′, Q′; r′, m+j−1−j′). (ii) ν = j−2 (tie): j′ = j−1+e,
e = v2(E/2^{j−2} + (4Q−1)λ_u) ≥ 1; if e₀ := v2(E/2^{j−2} + (4Q−1)r) < m then e = e₀; else every e ≥ m occurs, each
in unrestricted Ψ(j′; P′, Q′) — **a tie emits exactly one any-j family** on j′ ≥ j−1+m. (iii) ν ≥ j−1: j′ = j−1.
Always P′ ≡ 3−P mod 2^{min(j′, j−1)}, v2 Q′ = v2 Q + 1. Proof: λ = (2^{j′}λ_{u′} − 2E)/(2^{j−1}(4Q−1)) into
Θ′ = P + 3 + 6k + Q2^jλ. ∎ Q_m = 3·2^m/(2^{m+2} − (−1)^m): 1, 2/3, 4/5, …
**F3.** b/c on Ψ: Q′ = Q 2^{j−j_y}/c_{uy}, P′ = P + 3τ + 3 − Q 2^j λ_{uy}/c_{uy}. ∎ (code hands this step
conservatively to TIE2's extended automaton in bit form.)
Corollary: the TIE2 §7 obstruction for copies of AO₄ chain (5,5) disappears: copy is Ψ(5; 5, 1) to precision
≥ 7·10^5; by F2(ii) its tie emits Ψ(·; 10/3, 2/3) = TIE2's macro, now for every source.

## 4. Catapult landing and 3-adic orbit [A + B]
**Lemma M.** Large chain t, j_b ≥ N, Θ_t ≡ p/q, |p| ≤ 10^5, q odd; followed by an a-return (NT by S-a) then an
a-return at n₀ with k₁ ≤ n₀²/2: j_{t+2} = v2(p + q(6 + 9k + 6k₁)) ≤ log2(|p| + q(6 + 6k₁ + 4.5(j_b−1)²)). So
j_b < T_{i+1}, q ≤ 3 ⇒ j_{t+2} < T_i. Same from the fire. Proof: (AA) λ_{x_{t+2}} = Θ_t + 6 + 9k + 6k₁ +
2^{j_b−2}λ_{u_t}, so qλ ≡ Z := p + q(6+9k+6k₁) mod 2^{j_b−2}; k ≥ (j_b−2)/4 ⇒ Z > 0; (C1) ⇒ Z < 2^{j_b−2};
log2(4.5q) < 4 for q ≤ 3. ∎ (margin log2 13.5 ≈ 3.755.)
**Lemma O.** c_m = −3 + 8·3^{−m}, P_m = (15 − c_m)/3 = 3 − c_{m+1}. (i) v2(c_m + 3) = 3: Ψ(5; c_m, 1) ties at
X(4) (k₄ = 1), emits Ψ(·; P_m, 2/3). (ii) a large a-step from P_m (NT by S-a) can land at j = 5 as
Ψ(5; c_{m+1}, 1). (iii) −2 ∈ B(i) by W; its a-step gives Ψ(5; 5, 1), emission lands below by M; level l contains
c_m for m ≤ l−4. (iv) c_m mod 2^B pairwise distinct for m < 2^{B−5}. [B] `orbit.py`: c_m (m < 12) alternate 5, 21
mod 32; emissions as predicted; distinct for B = 6..16; level 5 shows −1/3 = c₁, 46/9 = P₁.

## 5. Theorem O [A]
Any generator-type certificate (real data below any finite N; adversarial above N subject to (C1), τ(n) ≥ (n−1)/2,
location lemma; arbitrary exact symbolic info incl. Ψ): (1) required families infinite, representatives ⊇ ℤ and
{c_m}, {P_m}, 2-adically dense; for every B some families agree mod 2^B, differ mod 2^{B+1}, behave differently at
the first a-step with v2(P+3k_n) ≥ B (such crossings occur in the real table for B ≤ 18 [B]); no finite union of
residue-class families is closed. (2) 2-adic closure not closed: minimal (5,5) emits Ψ(·; P′, 2/3) for every
P′ ≡ 10/3 mod 32 (TIE2 §6.1: branching to depth 24 never closes). (3) size step breaks: j ≥ N,
k\* = ⌈(j−2)/4⌉, l_j = 2^{j−2} + 3k\* + 2; at level l_j the state (j ∈ R₁, θ = −(l_j − 2)) is present by W and
θ + 3k\* = −2^{j−2}, v2 = j−2; k\* admissible; a non-descending large step is consistent with all constraints; no
certificate of this type reaches level 2^{N−2} + O(N). ∎ [C] A uniform proof needs arithmetic info on F's table at
large indices, or a height-aware argument (r ≤ C(level + log height) would suffice; not from small-j 2-adic info).
Each single level is a finite computation (≈ 2–6·10^6 runs + O(1) new rational families).

## 6. Uniform statements
**Theorem S [A + imported TIE2 B].** J ≥ K′, EXT for all J′ < J, F through τ(J−1), and one of (a) X(J−1) even head;
(b) type a, v2(3k_{J−1}+1) ≤ K−2; (c) type b, ω(J−1) < K; (d) type c, copied epoch J_W < K. Then S(J) tie-free with
≤ 7 chains. Proof: (a) r = 0. (b) θ̃ = 1 NT since v2(1+3k) ≤ K−2 < J−2; j₁ = 1 + v2(1+3k) < K, θ̃₁ = 2. (c) j₁ =
ω(J−1) < K, θ̃₁ = 0. (d) location lemma (all indices): copied chain is an a-output of an epoch of level ≤ 2. These
are exactly the level-3 generator's chain-1 entries; TIE2 §5 uses nothing else about J (large steps from R₂, R₁ use
(C1) only below K; copies read levels ≤ 1). Along tie-free prefixes the certificate gives r ≤ 7; Theorem L
by-product (EXT below J) makes the first ⌊J/(3 log2 J)⌋+1 ≥ 8 chains tie-free. ∎ Level-4 version: K → K′, r ≤ 9.
Reading: EXT(J) can fail only if some s ≤ τ(J−1) has 3s+2 or 3s+4 ≡ 0 mod 2^T, T = K′; by (C1) J ≳ 2^{T/2}.
**Corollary 4 [A + B; §8.1 audit].** EXT for all J < K″. J < K′: I-4. K′ ≤ J < K″ by induction: (C1) gives
j₁ ≤ log2(6(J−1)²+5) < K′ and J_W < K′, so Theorem S (level 4) applies. ∎ As in PROOF_EGX Corollary H with K″:
F defined for s < (2^{K″}−4)/3; no halt in the first 2^{K″}−2 top steps (horizon not re-audited).
Changes vs TIE2: Lemma LM replaced by Theorem L by-product; source tracking + 10/3 macro replaced by F2(ii); level 4
re-certified, 0 failures.

## 7. Level 5 [B]: not certified
`gen.py 5 4`: 16,165,294 entries, 220,927 ties resolved via Ψ, max_further 4, 4 iterations; big-state checks
(S-a NT, Lemma M landings) all pass. Exactly 1 failure ('pair', 5, 5), origins chain1-c from lw = 4 (copy of AO₄
pair (5,6) shifted −1); big-c from range 2, θ = 4 (AO₁ pair (5,3)); big-c from range 1, θ = 5 (AO₀ pair (5,2));
θ = 5 newly in B₅(1) by drift. Cause: copies of specific pair a-outputs carried at bit level. Cure [C]: annotate each
pair a-output with Ψ data (NT a-output at real k: Ψ(5; (9 − P + 6k)/3, 2/3) for Q = 1; copy Ψ(5; P_c, 2/3),
P_c ≡ 5 mod 32, ties at X(4), emits Ψ(·; P_c + 9 − (8/5)(P_c+3), Q″)); each source (k up to ≈10^{12}) a new family,
≈10^6 runs each; not cheap; stopped. EXT certified only for J < K″.

## 8. Least sure
1. Lemma LM replacement: Theorem L by-product's "tie-free" must match the automaton's assumption along the first
   r ≤ 9 chains; needs line-by-line audit vs PROOF_EGX §6. 2. Lemma M, q = 3 thin margin; gen.py admits depth-0
   emissions with denominator ≤ 3 or chain-1 origins. 3. Imported TIE2 automaton soundness (ext, go, gox,
   conservative X-record, h caps, F3 hand-off). 4. PREC = 2048 asserted; fixed bugs (r′ precision, tie R0, E = 0).
5. Theorem O is about the method, not F. 6. Corollary 4 horizon not re-audited.

## 9. Reproduce
python3 -B verify_tie2_copy.py 4 4; check_family.py; validate_psi.py; orbit.py; gen.py 5 4 (~23 min, 4 workers).
Unrun change: gen.py now adds catapult landings to the any-j a-output set (only matters at level ≥ 6).
