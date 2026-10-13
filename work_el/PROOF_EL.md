# EL: the exit after a level fire — an exact automaton, descent, and a certificate for J < 2^499998

Machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Base (audited, used as black boxes):
work_g6/PROOF_G6.md §5 (formal pair map F, mass identities §5.3, level fires §5.4) and
work_m/PROOF_M.md (calls/returns Lemmas 2.1–2.3, epochs Lemmas 3.1–3.3, λ-certificate §4,
Theorem M §5, symbolic exit §6, the open lemma (EL_J) §8). Checks: `verify_el.py` (E1–E7, log
`run_main.txt`). It imports `work_m/verify_m.py` read-only, for the cross-check E2 only.

Tags: **[A]** proved for all parameters. **[B]** finite computation (range stated). **[C]** data/heuristic.
"(C1),(C2)" are the two inductive claims of Theorem M: τ(n) ≤ n², ε(n) ≤ max(7,n/4). Both hold for
n ≤ 10^8 by V2 of PROOF_M. Inside the induction of Theorem M they also hold at every crossing
before the current epoch. Wherever a statement uses them, it says so.

## 0. Results

| # | statement | tag |
|---|---|---|
| A | **Exit automaton.** Let θ_t := (3s_t+5) mod 2^{j_t} at the top-level chain t (step s_t, parameter j_t), and n := j_t−1. Then: b/c-steps have j_{t+1} = ω(n) ≤ j_t−3 and θ_{t+1} = θ^W+θ_t−2. a-steps have j_{t+1} = 1+v2(3s_t+5+3k_n−2^{n−1}λ_{u_t}). The step **descends** (j_{t+1} < j_t) iff (NT_t): θ_t+3k_n ≢ 2^{n−1} (mod 2^n). In that case j_{t+1} is read off θ_t mod 2^n, and θ_{t+1} = 3−θ_t. | A |
| T | **Tie-freeness is a size statement.** In the symbolic recursion of PROOF_M Lemma 6.1, v2(α_x) = J−Γ_t exactly, and 1 ≤ β_x ≤ 6d_t−1. So the exit is tie-free whenever 6d_t ≤ 2^{J−Γ_t}. | A |
| B | **Descent ⇒ (EL_J), with (C1).** If NT holds at every a-step of an epoch, then r ≤ max(1, j_1−3) ≤ max(1, J−4) ≤ ⌊J/2−1⌋² for J ≥ 6. Inside Theorem M’s induction, with (C1) at earlier crossings (in particular J−1), the symbolic exit is tie-free and r ≤ log2(6J²); small cases are certified. | A+B |
| C | **NT criterion.** NT_t holds whenever the integer representative θ̃_t ∈ [−10,4] (uses (C1) at n ≥ 8). NT always holds at the fire (t=0, J ≥ 10). At t=1 it holds for routes a and b, for every J. | A |
| D | **Certificate.** For every 10^6 ≤ J < T₁ := 2^{499998}, the exit (inside Theorem M's induction) is tie-free, descends at every step, and has **r ≤ 4**. So (EL_J) holds on this range. | A+B |
| E | **Extended unconditional horizon.** F is defined, the universal walk does not halt, and (M1′),(M2′) hold literally for all s < (2^{T₁}−4)/3 ≈ 2^{2^{499998}}. This replaces 2^{10^6} in PROOF_M Theorem 6.2. | A+B |
| F | **Where the method stops.** One more tower level admits adversarial tie paths, of which 3 are found. Each needs three nested "fire copies", which drift θ̃ by −3. The path is (j,θ̃): (17,−2) → (5,5) → tie at n=4. | B |
| R | **Sufficient remaining condition: (NT)** at every a-step of every epoch with J ≥ T₁. By B, inside Theorem M’s induction with (C1), it implies (EL), and hence Theorem M without hypotheses; it is not necessary for (EL). | open |

Answer to the brief: the strict decrease of j (approach 1) holds unconditionally on b/c-steps. On
a-steps it holds exactly when the congruence NT holds. Termination by parity (approach 2) is
automatic once j ≤ 4. Tie-freeness by size (approach 3) holds (Lemma T). Inside Theorem M’s
induction with (C1), NT is sufficient for the whole of (EL_J), by Theorem B. NT is proved at t=0,
at t=1 for routes a and b, and everywhere
for J < 2^{499998}.

## 1. Setting

These definitions come from PROOF_M §§1–3.
- An epoch starts with a level fire (chain 0) at step s_0, at pointer ρ, with J := j_0 = v2(3s_0+4).
- Its top-level chains are t = 0,1,…,r. Chain t is at step s_t, has parameter j_t, and has base u_t, with λ_{u_t} odd.
- Put n_t := j_t − 1. The return after chain t is at step s_t+1+τ(n_t) (Lemma 2.3).
- The type of X(n_t) (a/b/c) is the type of that return. Its head is H = M_{u_t}(A_X), where A_X is W's
  head at X(n_t). The epoch continues (chain t+1 sits at the return step) iff H is odd (Lemma 3.1).
- We call a transition an **a-step** or a **b/c-step** after the type of the return.
- k_n := τ(n)/2 when τ(n) is even. ω(n) is the parameter j of W's chain at step τ(n). That chain is
  a top-level chain of W, because crossings occur only at top-level states (Lemma 3.3).
- Θ_t := 3s_t+5 (an integer), and θ_t := Θ_t mod 2^{j_t}.

**Lemma 1 (terminal crossings) [A].** X(0),X(1),X(2),X(3) are even-headed. Hence a chain with
j_t ≤ 4 is the last chain of its epoch.
*Proof.* Step 0 is at the start state A=(1,1), P=∅, i=0. It reads E_0,E_1, so X(0) has type a
and X(1) has type b. Its parity is 1+1 = 0, so the step is even, and A becomes (4,4) with i=2.
Step 1 is at P=∅, i=2. It reads E_2,E_3, so X(2) has type a and X(3) has type b, with head (4,4)
(parity even).
- For n ∈ {2,3}, c_A is even, so the return head H = M_u(A_X) has the parity of λ_A = 4, which is even.
- For n ∈ {0,1}, A_X = (1,1), so H = (c_u, λ_u+1). Here c_u is even and λ_u is odd, so H is even. ∎

## 2. Theorem A (exit automaton) [A]

Assume F is defined through chain t+1.

**(A0) Fire.** Θ_0 = (3s_0+4)+1 ≡ 1 (mod 2^J).

**(A1) b/c-step.** Chain t+1 is the M_{u_t}-image of W's chain at w = τ(n). This is the corollary
to PROOF_M Lemma 3.2. So j_{t+1} = ω(n). The c-part of that W-chain has v2 = n−ε(n), by the proof
of Lemma 3.2. W's own margin (S1) gives ω(n) < n−ε(n), and ε ≥ 1 for types b/c. Hence
**j_{t+1} ≤ j_t − 2 − ε(n) ≤ j_t − 3.** Also s_{t+1} = s_t+1+w, so Θ_{t+1} = (3w+5)+Θ_t−2 =
Θ^W+Θ_t−2. Here Θ^W is the Θ of W's chain. Reducing mod 2^{j_{t+1}} (and j_{t+1} < j_t):
**θ_{t+1} ≡ θ^W + θ_t − 2.**

**(A2) a-step.** At X(n) (type a) W has P=∅ and i=n. By mass, A_X = (2^n, 3τ(n)+1). So
λ_H = 2^nλ_{u_t} + 3τ(n)+1.
- By Lemma 1, n ≥ 4, and H is odd iff τ(n) is even. Write τ(n) = 2k_n.
- The return state is [D_t] ++ originals (Lemma 2.3(a)). The mass identity there gives λ_H+λ_{D_t} = 3s′+1, where s′ = s_t+1+τ(n).
- The chain reads b = D_t, so λ_x = λ_H+2λ_{D_t}+3 = 6s′+5−λ_H. Therefore

  **λ_{x_{t+1}} = 2·(Θ_t + 3k_n − 2^{n−1}λ_{u_t}),  j_{t+1} = 1 + v2(Θ_t + 3k_n − 2^{n−1}λ_{u_t}).**

Since λ_{u_t} is odd, the bracket is ≡ θ_t+3k_n+2^{n−1} (mod 2^n). Two cases:
- If θ_t+3k_n ≢ 2^{n−1} (mod 2^n) (call this **NT_t**), then v2(bracket) ≤ n−1. So
  j_{t+1} ≤ n = j_t−1, and j_{t+1} = 1+v2((θ_t+3k_n+2^{n−1}) mod 2^n).
- Otherwise j_{t+1} ≥ j_t: a **tie** (non-descent), whose value depends on higher bits.

Under NT_t: Θ_{t+1} = Θ_t+3+6k_n = λ_{x_{t+1}} + 2^nλ_{u_t} + 3 − Θ_t. Both of the first two terms are
≡ 0 mod 2^{j_{t+1}} (since j_{t+1} ≤ n), so **θ_{t+1} ≡ 3 − θ_t (mod 2^{j_{t+1}})**. ∎

**(A3) Consequences.** Define integers θ̃ by the following rules:
- θ̃ := 1 at fires;
- θ̃_{t+1} := 3−θ̃_t at a-steps;
- θ̃_{t+1} := θ̃^W + θ̃_t − 2 at b/c-steps, where θ̃^W is the value at W's chain (defined earlier in time).

By induction over time, θ̃_t ≡ Θ_t (mod 2^{j_t}) as long as all a-steps so far satisfy NT. Then every
decision (parity, type, j, θ) depends only on the state (j_t, θ_t mod 2^{j_t}) and on W's crossing table.
In particular the exit is a function of J alone, **provided every encountered a-step satisfies NT**.
This is the conclusion of PROOF_M R5, with NT in place of the tie-free hypothesis. At an NT failure
the automaton yields only an unresolved non-descent: the next parameter needs higher bits absent
from (j,θ), so these rules do not determine an exact continuation.
- [B] E1: every formula above holds at all 302,879 fires, 15,850 a-steps (all descending) and 7,910 b/c-steps of the real walk to i = 10^6.
- [B] E2: the automaton equals `verify_m.sym_exit` for 2 ≤ J < 20000.
- [B] E4: run from every fire state (J,1), J < 10^6, it reproduces V4's distribution {0: 378,392; 1: 574,113; 2: 47,493} exactly (J ≥ 2).

**Remark S (shifted copies) [A].** Suppose a b/c-step starts at chain t. As long as the following
returns are again of type b/c, the outer chains are images of W's *consecutive* top-level chains
from step τ(n) on, and θ_outer = θ_W + δ with constant δ = θ_t−2. The reason is that the next
return is at the same crossing X(j−1) for both, so it has the same type and the same copied
W-chain, and (A1) preserves the offset. Some cases:
- After a fire, δ = −1.
- After θ = 2, δ = 0: an exact copy of W while the returns are b/c. Route a gives θ_1 = 2, and an
  a-step from θ = 2 gives θ = 1, which is the state of a fire.
- At an a-step the outer argument is W's argument plus δ, and the copy ends.
- A b-step copies a W-fire (θ^W = 1), so nested b-routes drift θ̃ by −1 each.

## 3. Lemma T (tie-freeness by size) [A]

Use the symbolic recursion of PROOF_M Lemma 6.1, in which small parts are αλ_u+β. Let d_t := s_t−s_0
and Γ_t := Σ_{t′<t}(1+ε(n_{t′})).
1. **v2(α_{x_t}) = J − Γ_t.**
   - At t=0, α_{x_0} = 2^J.
   - *b/c-step:* α_{x_{t+1}} = α_{u_t}c′_x. Its v2 is (v2 α_{x_t} − j_t) + (n−ε) = v2 α_{x_t} − 1 − ε.
   - *a-step:* use the symbolic mass identity. The algebra of G6 §5.3 is linear and holds coefficientwise. At the fire state Σλ = 2^Jλ_u−3, so Σα = 2^J and Σβ = 3d−3 throughout. At an a-return only H and D_t are non-original, so α_{D_t} = 2^J − α_H with α_H = α_{x_t}/2. Then α_{x_{t+1}} = α_H + 2α_{D_t} = 2^{J+1} − α_{x_t}/2, and its v2 is v2 α_{x_t} − 1 (= −1−ε with ε = 0).
2. **β ≥ 0 for every entry except D_0 (β = −1); 1 ≤ β_{x_t} ≤ 6d_t − 1 (t ≥ 1).**
   - Images have β = c′β_u + λ′ ≥ 0.
   - β_{x} = β_H + 2β_b + 3 ≥ 0 − 2 + 3 = 1.
   - H is odd and α_H is even, so β_H is odd ≥ 1. Hence a new D has β ≥ −1 + 1 = 0.
   - Since Σβ = 3d−3 and only D_0 is negative, β_H + β_b ≤ 3d−2. Therefore β_x ≤ 2(3d−2)+3−β_H ≤ 6d−1.

If 6d_t ≤ 2^{J−Γ_t}, then β_x ≤ 6d_t−1 < 2^{J−Γ_t}, so v2 β_x < J−Γ_t = v2 α_x: tie-free.
In fact equality 6d_t = 2^{J−Γ_t} is impossible for positive integer d_t, since 6d_t is divisible
by 3. This is the margin inequality of Theorem M with ρ replaced by J. E3 confirms both identities
at all 13,379 exit chains for J < 20000. ∎

## 4. Theorem B (descent ⇒ EL) and Lemma C (NT criterion) [A]

**Theorem B.** Suppose NT holds at every a-step of an epoch. By (A1) and (A2) we get
j_1 > j_2 > … > j_r.
- Every chain t < r is followed by an odd return, so j_t ≥ 5 (Lemma 1).
- Hence r ≤ max(1, j_1−3). Also j_1 ≤ J−1, so r ≤ max(1, J−4) ≤ ⌊J/2−1⌋² (J ≥ 6).
- With (C1) at J−1, we have j_1 ≤ log2(6τ(J−1)+5) ≤ log2(6J²). This follows from G6 §5.3: route a has j_1 = 1+v2(3k_{J−1}+1), and routes b/c have j_1 = ω(J−1).

For the **symbolic tie-freeness** part, work inside Theorem M’s induction, with (C1) at all earlier
crossings, in particular τ(J−1) ≤ (J−1)². On the valid symbolic prefix put
**h_t := J−Γ_t−j_t**, so h_0 = 0. By the coefficient recurrence in Lemma T,
- at an a-step (ε = 0), h_{t+1}−h_t = j_t−j_{t+1}−1 ≥ 0 under NT;
- at a b/c-step, h_{t+1}−h_t = j_t−j_{t+1}−1−ε(n_t) ≥ 1 by the stronger bound in (A1).

If the first transition is a b/c-step, this gives h_1 ≥ 1. If it is an a-step, (C1) gives
j_1 ≤ log2(6(J−1)²+5) < J−1 for J ≥ 10, hence j_1 ≤ J−2 and h_1 = J−1−j_1 ≥ 1.
The strict inequality starts at 6·9²+5 = 491 < 512 and persists since
6J²+5 < 2(6(J−1)²+5) for J ≥ 10. Thus every exit chain has h_t ≥ 1: a later first a-step
already inherits a positive margin from the preceding b/c-steps. At each next chain, Lemma T’s
coefficient recurrence gives v2(α_{x_t}) = J−Γ_t > j_t. Since λ_{x_t} = α_{x_t}λ_u+β_{x_t}
has valuation j_t and λ_u is odd, this forces v2(β_{x_t}) = j_t, validating the next symbolic
division and continuing the prefix induction. The small cases J < 10 are covered by V4 of
PROOF_M (and E2–E3 for 2 ≤ J < 10); J = 1 has no exit chain. Hence, with these inductive
hypotheses and certified small cases, NT implies (EL_J). ∎

**Lemma C.** Let chain t be followed by an a-step at n = j_t−1. If θ̃_t ∈ [−10,4], then NT_t holds.
*Proof.* A tie means θ̃_t + 3k_n ≡ 2^{n−1} (mod 2^n). By Lemma 1 and the crossing table (printed by
E1: odd type-a n < 40 are 4,7,11,13,16,…), the odd type-a crossings below 8 are n = 4 (k = 1) and
n = 7 (k = 2).
- n = 4: a tie needs θ̃ ≡ 5 (mod 16).
- n = 7: a tie needs θ̃ ≡ 58 (mod 128).
- n ≥ 8: by (C1), |θ̃+3k_n| ≤ 10+1.5n² < 2^{n−1} (E7), so θ̃+3k_n ≢ ±2^{n−1} (mod 2^n).
∎

**Corollaries [A].**
- (i) NT_0 holds for J ≥ 10, given (C1) at J−1. Here θ̃ = 1 and n = J−1 ≥ 9, which gives the formula j_1 = 1+v2(3k_{J−1}+1) (PROOF_M P3).
- (ii) At t = 1, route a gives θ̃_1 = 2 and route b gives θ̃_1 = θ̃^W+θ̃_0−2 = 1+1−2 = 0. Both lie in [−10,4], so NT_1 holds for every J. Route c gives θ̃_1 = θ̃^W − 1, with θ̃^W the value of a real a-step chain.

## 5. Theorem D (certificate for 10^6 ≤ J < T₁ = 2^{499998}) [A+B] and Corollary E

**Setting.** Take an epoch with 10^6 ≤ J < T₁, inside the induction of Theorem M, so that (C1),(C2)
hold at all crossings before it. Every j_1 satisfies j_1 ≤ log2(6(J−1)²+5) < 10^6. Write Φ for F's
exact data below index 10^6: the types, parities, τ, and the (j,θ̃) of each W-chain. Φ is computed by the
certified λ-walk to i = 10^6.

**Entry states after chain 1 (by (A0)–(A2)):**
- route a: (j_1, 2) for some j_1 < 10^6;
- route b: W fires at J−2, so the state is (j_1, 1+1−2) = (j_1, 0);
- route c: W's chain at τ(J−1) is an a-step chain of a real epoch. That epoch's fire parameter is
  J″ ≤ log2(3(J−1)²+4) < 10^6 (by (C1)). By (A3), its exit is the level-0 run for J″. So the state is
  (j_W, θ̃_W − 1), where (j_W, θ̃_W) is one of the **27 a-step pairs** of level 0 (E4).

All later steps have n < 10^6 and use only Φ.

**[B] E4 (level 0).** Every fire state (J,1), 2 ≤ J < 10^6, runs without a tie, with r ≤ 2.
The a-step pairs are {(j,θ̃): 1 ≤ j ≤ 3, θ̃ ∈ {1,2,3}} ∪ {(4,1),(4,2)} ∪
{(j,2): 5 ≤ j ≤ 21, j ≠ 20}, 27 in all (listed in the log).

**[B] E5 (level 1).** The automaton was run from (j,2) and (j,0) for **every** 1 ≤ j < 10^6, and from
the 27 c-entries. There is no tie, and at most 3 chains follow the entry chain. The distribution is
{0: 756,803; 1: 1,148,292; 2: 94,874; 3: 56}.

Hence every such epoch descends at every step and has **r ≤ 4**.

**Tie-freeness.** Lemma T applies with Γ_t ≤ 4+ε(J−1)+3·7 ≤ 25+(J−1)/4. This uses (C2) at J−1, and
ε ≤ 7 below 10^8 by V2. The first call uses (C1), and the next three use V2’s stronger bound
τ(n) ≤ n below 10^6, giving d_4 ≤ 4+(J−1)²+3·10^6 ≤ 2J². Then log2(12J²) < 3J/4−25. So (EL_J) holds
for 10^6 ≤ J < T₁. For J < 10^6 it was already V4. ∎

**Corollary E [A+B].** F is defined and the universal walk never halts for every s < (2^{T₁}−4)/3.
*Proof.* A fire at step s has J = v2(3s+4) < T₁. Run the induction of Theorem M (PROOF_M §5–6),
using V2 for ρ ≤ 10^8. For ρ > 10^8, Theorem D gives r ≤ 4 ≤ L(ρ), and the margins (I1)–(I3) then
follow as in Theorem M.

Theorem M gives (M2′) s ≤ i². For (M1′), use Lemma 3.3–3.4 with t,a_t ≤ 4, ε(J−1) ≤ 7+J/4, ε ≤ 7
elsewhere, j ≤ 2log2 i+4 and J ≤ 2log2 i+2:
Δ ≤ 31+ε(J−1)+j ≤ 42.5+2.5·log2 i ≤ ⌊log2 i⌋² for i > 10^8. For i ≤ 10^8, V2 gives Δ ≤ 28. ∎

## 6. F: why the bootstrap stops at one level [B]

For J ≥ T₁, j_1 may be ≥ 10^6, where Φ is unknown. One more step must then be treated
adversarially:
- an a-step gives (any j, 3−θ̃);
- a b-step (copy of a fire) gives (any j, θ̃−1);
- a c-step gives (j_W, θ̃+θ̃_W−2).

From the depth-1 states θ̃ ∈ {2,0}, the any-j entries are θ̃ ∈ {−1,0,1,2,3}. E6 finds **3 ties**, all
of the same shape:

  (J ≥ T₁, θ=1) →b→ (J₂, 0) →b→ (244875 | 538715 | 832554, −1) →b (copy of W's fire with j=17)→
  (17, −2) →a (n=16, k=6)→ (5, 5) →a (n=4, k=1): 5+3 ≡ 8 (mod 16): **tie**.

For this to happen, three nested level fires must have b-type first returns, the innermost two at
levels ≥ 10^6−2 with prescribed parameters. That is a congruence condition on F's own k-values far
beyond any computation. It is not excluded by size. A tie means only non-descent, not
non-termination, so this is no evidence against (EL). These adversarial tie paths are automaton
obstructions, not paths shown realizable in F. It does show that the descent method needs
arithmetic information about F at astronomically large levels. Each further level of the
tower T_{h+1} = 2^{(T_h−3)/2} adds at most one adversarial step. With real-chain values θ̃ ∈ {0,1,2},
and exit values in [−1,3] (E4), level 1 is the most the adversarial closure can certify.

## 7. A sufficient remaining condition

**(NT)** In every epoch with J ≥ T₁ = 2^{499998}, every a-step satisfies
θ_t + 3k_{j_t−1} ≢ 2^{j_t−2} (mod 2^{j_t−1}), i.e. j_{t+1} < j_t.

Inside Theorem M’s induction, retaining (C1) at earlier crossings, (NT) for J ≥ T₁ is a
**sufficient condition for (EL), not a necessary one**: a non-descending step may still terminate.
By Theorem B and the certified range J < T₁, it gives (EL_J) for all J with r ≤ log2(6J²),
hence (EL) by PROOF_M §8, and then Theorem M with no hypotheses.

A sufficient condition, by Lemma C, is **(Θ)**: θ̃_t ∈ [−10,4] at every chain that is followed by
an a-step. Data: θ̃ ∈ {0,1,2} at all real chains to i = 10^6, and θ̃ ∈ [−1,3] at all level-0 exit
chains [C]. By Remark S, θ̃ can leave this window only through nested fire-copies (drift −1 each) or
reflections θ ↦ 3−θ. That needs nesting depth ≥ 3 at levels ≥ 10^6, which is exactly the shape in §6.

Proved for all J [A]:
- Theorem A, Lemma T, Theorem B, with their stated hypotheses (and certified small cases for B).
- NT at t=0.
- NT at t=1 for routes a and b.
- Strict descent of every b/c-step by ≥ 3.
- Termination at j ≤ 4.
- Logarithmic descent: under NT with θ̃ bounded, an a-step gives j_{t+1} ≤ 1+log2(|θ̃|+1.5n²), and a b/c-step gives j_{t+1} ≤ log2(6n²+5).

Still open for J ≥ T₁:
- NT at t ≥ 1 in route c;
- NT at t ≥ 2 in general.

## 8. Reproduce

`python -B verify_el.py 1000000 20000 1` runs E1–E7 in about 80 s (log `run_main.txt`).
No git operations were performed, and nothing outside `work_el/` was written.
