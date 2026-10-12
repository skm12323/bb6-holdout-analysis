# G6: attempt to prove residuals (a) and (b) for all j. Result: partial.

Machine `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Base (audited, work_r1): top map on
lists L=(A;b,c,S). If A is even, L'=(A+b+c+3;S). If A is odd, x=A+2b+3=2^j·u, and
L'=(u+1; u,2u,…,2^{j-2}u, c+(A+1)/2, S). HALT iff u=1. **Sum lemma:** every step adds exactly 3
to A+ΣS.
Tags: [Class-A] proved for all parameters. [Class-B] finite exhaustive or symbolic computation
(range stated). [Class-C] conjecture or empirical. Checks: `verify_g6.py` (V1–V3).

## 0. Objects

*Level process with base U* (U odd): A=U+1, queue = E_0,E_1,… with E_a=2^a·U, then a tail.
A *level fire at position ρ* is a chain with b=E_ρ and c=E_{ρ+1}. Its k is **defined** by
x = 3·2^ρ·U + 6k+4, which is equivalent to A = 2^ρ·U + 6k+1.
*Φ_m* (the per-J object of agentB_run7) is the level process with U=u=(9P+6k_h+4)/2^m.
It has run length m−1, followed by D_h = (15/2)P+3k_h+1 and then T_e = 3·2^e·P (e ≥ 2).
Φ_m is **canonical** if it ends at a fire with b=T_e and c=T_{e+1}, with
x = 9·2^e·P + 6(k_h+dk)+4, D' canonical, and only pure T's left over. In that case dp:=e.

## 1. Proved

**Prop 1 [Class-A].** Suppose a level fire at ρ (value k) is followed, after s steps, by the
next level fire at ρ'. Suppose also that everything pushed in between has been consumed, so the
queue front is E_{ρ'}. Then s is even, k'=k+s/2, dk ≥ 1 and dp=ρ'−ρ ≥ 2.
*Proof.* The material consumed from the level is exactly E_ρ…E_{ρ'−1}, with total
(2^{ρ'}−2^ρ)U. By the sum lemma, A' = A + (2^{ρ'}−2^ρ)U + 3s. With A = 2^ρU+6k+1 this gives
A' = 2^{ρ'}U + 6k+1+3s, so 6k' = 6k+3s. Next, s ≥ 2: after the chain A=u+1 is even, so at least
one even step comes before the next fire. Finally, the fire itself consumes E_ρ and E_{ρ+1},
so ρ' ≥ ρ+2. ∎
The same argument applied to Φ_m (T_e plays the role of E_{ρ+e}) gives this:
**canonical re-entry alone implies dk(m)=s/2 ≥ 1 and dp(m) ≥ 2.** It also gives
L(j)=2dk(j), which was previously Class-B for j ≤ 120, for every canonical j.
The same identity applied from the start of a level gives this: the steps before the level fire
at ρ number exactly 2k_ρ.

**Prop 2 [Class-A] (decomposition).** Lemma L0 (queue determinism) gives the following. Φ_m
coincides with the universal level process with U=u until the first read of queue index m−1
(the entry D_h). Hence its level fires up to that moment are exactly the universal positions ρ
with ρ+1 ≤ m−2, with the universal k_ρ and j_ρ. Let ρ* be the last of these, and set
g = m−2−ρ* and K = k_{ρ*}. Then
  dk(m) = K + e(m)/2,
where e(m) is the number of steps from the fire at ρ* to the host re-entry (Prop 1).
Everything after ρ* is the "exit". If dp is bounded by d, then g < d.

**Prop 3 [Class-A] (one exit type, computed for all m).** Take the case g=1, j_{ρ*}=2. The
chain pushes [u''] and D''. One even step then gives A = 2^{m−1}u + 6K+7, which is odd. The
next chain reads b=D_h and c=T_2, with
  x_D = (39/2)P + 9k_h + 6K + 14.
The class condition is 6k_h+4 ≡ 2^m (mod 2^{m+1}), which gives 9k_h+6 ≡ 3·2^{m−1} (mod 2^m).
Hence **j_D = 1+v2(3K+4)** whenever 1+v2(3K+4) < m−1. Here u_D has P-part
(39/2)·2^{p−j_D}, so u_D ≥ 3 and this chain does not halt. (V1 checks the algebra
symbolically. V3 confirms j_D on 250/250 occurrences for m<3000.)

**Prop 4 [Class-A] (reduction of (b)).** Suppose dk(j) ≤ 4r+4 holds whenever
j ≤ 1+log2(3r²+2). Then k_ρ ≤ ρ² for every universal position ρ.
*Proof.* Induction over fires, with base k=1 at ρ=4. Assume k_i ≤ ρ_i². Then
j_i ≤ 1+log2(3ρ_i²+2), and so
  k_{i+1} ≤ ρ_i²+4ρ_i+4 = (ρ_i+2)² ≤ ρ_{i+1}²,
using dp ≥ 2 (Prop 1). V2 checks the elementary inequality 1+log2(3r²+2) ≤ 4r+4. ∎
Combining with Prop 2: dk(j) ≤ (j−2)² + e(j)/2. So **(b) follows from (a) plus the exit-cost
bound e(j) ≤ 2^{(j−3)/2}** for j beyond the base range. This can be run as one strong induction
together with the ρ-induction, because only j < ρ is used.
Unconditionally, the Class-B table gives dk(j) ≤ j for j ≤ 30000 (re-checked here to 3000).
So k_ρ ≤ ρ² ≤ ρ³ holds for every ρ whose fires have j ≤ 30000, which includes every
ρ < 2^{14999} [Class-A given that Class-B base].

## 2. Not proved: the exit-closure lemma (core of (a))

**Finding [Class-A + Class-B].** By Prop 3, exit chains reading D_h have parameter
1+v2(3K+4). This parameter is not bounded by any finite exit template. It reaches 11 for
m<3000 (V3), and Class-C says it is unbounded along m. Each such chain starts its own nested
cascade Φ_{j_D} with a non-standard D (c=T_2) and the tail T_3,T_4,…. So the review's
statements "finitely many exit types / exit ≤ 6 events" hold only if a nested cascade counts as
one event. As literal templates they are false. The "exit fires j ∈ {1,3}" census must refer
to on-orbit host-level fires only. That should be checked.

The exit outcome is also not a function of the bounded data (g, j_{ρ*}). The table's dp and
dk−K vary within the class (1,2). A recursive signature (g, sig(j_{ρ*})) of depth 3 resolves
everything except exactly that class [Class-B, m<1500]. That class is resolved by v2(3K+4),
as Prop 3 shows.

**What a proof of (a) still needs.** It needs a closure lemma over a finite family 𝓕 of
symbolic exit shapes. A shape σ is given by
- the D-form (canonical, or c+(A+1)/2 with c ∈ {T_e, D_h, d}), and
- the tail prefix (some E's, D_h, T's).

The lemma would state that for every σ ∈ 𝓕 and every j, Φ_j(σ) re-enters on a specified tail
entry. It would give an explicit dk and dp, with every 2-adic decision of the form
v2(aK+b) for fixed (a,b), so the decision is < j and no class split occurs. Each nested
cascade would again be Φ_{j'}(σ') with σ' ∈ 𝓕 and j' = 1+v2(a'K+b') < j. Safety would come
from the P-part: every exit chain has an explicit positive P-coefficient times 2^{p−O(j)}.

I have not constructed 𝓕 or proved its closure. The decisive unproved points are:
(i) dp(j) ≤ 6 for all j, needed to bound g;
(ii) closure of 𝓕 under the recursion, including the Prop 3 type and all its relatives
(g ∈ {0..5}, j_{ρ*} ∈ {1..4} or a spike);
(iii) the parameters j' = 1+v2(aK+b) are < j. This holds automatically once K ≤ ρ², via Prop 4.
Proving (ii) would be a finite symbolic computation over 𝓕 with j kept symbolic. That
computation is feasible but was not done. G1 (depth ≥ 3) is untouched.

## 3. Class-B / Class-C summary
- V3 [Class-B], m<3000, concrete Φ_m with k=κ_m, p=m+60. Results: canonical re-entry,
  s=2dk, dk ≥ 1, dp ∈ [2,6], all u ≥ 3, max e(m)=16, max D-fire j=11, dk ≤ m.
  Note this is one concrete k and p per class. The class-generic version is agentB_run7,
  which reaches j ≤ 30000.
- [Class-C] 𝓕 is finite. dp ≤ 6. e(j)=O(log j). v2(3K+4) is unbounded.

---------------------------------------------------------------------------------------------

## 4. Closure section  (PARTLY SUPERSEDED by §5; see note at the start of §5) (coordinator's follow-up task)

**Outcome.** I did not obtain a finite family 𝓕 of *symbolic exit shapes* that is closed under the
recursion. Literal closure fails: shapes keep appearing. I record the escaping branch
precisely (§4.2). I then give a reformulation (§4.3–4.5) in which the exit shapes become
irrelevant. This reduces (a)+(b) to one explicit margin inequality on a single
parameter-free integer orbit (§4.6). That inequality is **not** proved for all indices. It is
verified symbolically for level index ≤ 4·10^5 [Class-B].

### 4.1 Crossing states [Class-A]
Take the universal level process with generic odd base U. Let "the crossing at n" be the state
just before the first step that reads E_n. Every step reads only the queue front (L0). So at the
crossing at n, everything pushed has been consumed except possibly the partner of E_n in that
step. Hence the queue is either [E_n, …] (clean) or [Y, E_n, …] (one pushed entry Y in front;
in this case E_n is read as c). By the sum lemma, A + (Y) = 2^n·U + 3s + 1, where s is the
number of steps so far.
The exit of Φ_m (§0) is exactly what happens after the crossing at n = m−1, with D_h in place
of E_{m−1} and T's after it. By L0, that crossing equals the universal crossing at m−1 (base u).
Proof: immediate from L0 and the sum lemma. ∎

### 4.2 The escaping branch [Class-B data; failure of finiteness is Class-C]
Normalise the scale coefficients of (A; Y) by 2^n. The symbolic walker (V4) finds these
crossing shapes up to n = 4·10^5:
(1;—), (1/2;—), (3/8;5/8), (9/32;23/32), (13/32;19/32), (51/128;77/128).
The last shape first appears at n = 6134, and only 11 times up to 4·10^5.

How it arises (V4 trace):
1. A level spike j=14 fires at ρ=6130. Its sub-cascade has run length 13.
2. The exit of that sub-cascade fires on pushed entries with j = 1, 4, 2.
3. It then fires on the spike's own D with j=5 (scale coefficient 13/8).
4. That j=5 cascade has its own exit, which produces a crossing with A-coefficient 51/128.

So the shape at a crossing is a composition of shapes of nested exits. Each new
"exit-inside-an-exit" depth produced a new dyadic shape: denominators 8, then 32, then 128.
No finite 𝓕 of symbolic (scale-coefficient) shapes was found.
**The escaping branch is: nested exit fires on a D-entry whose own exit is itself
non-trivial.** The first instance is spike j=14 → D-fire j=5 → exit, at n=6134.

### 4.3 Scale/small superposition [Class-A]
Write every value as v = c_v·U + λ_v, with c_v, λ_v ≥ 0 dyadic rationals. This is true
initially and is preserved, because every operation adds, halves (D = c+(A+1)/2), or divides
by 2^j.
- **Parity.** Assume v2(c_A) ≥ 1. Then the parity of A is the parity of λ_A.
- **Chains.** Call a chain *margin-safe* if v2(λ_x) < v2(c_x). For such a chain,
  j = v2(λ_x) for **every** odd U. Then u = (c_x/2^j)U + λ_x/2^j, where c_x/2^j is a positive
  dyadic with v2 ≥ 1, so c_x/2^j ≥ 2. Also λ_x/2^j is an odd integer ≥ 1. Hence
  **u ≥ 2U+1 ≥ 7 for U ≥ 3: no halt.**
- **Consequence.** While all chains are margin-safe, every decision depends only on the small
  parts. The small parts evolve by the closed-form top map applied to (λ_A; λ_queue), with all
  level entries contributing 0. The scale parts ride along linearly. In particular,
  **the exit shapes of §4.2 are irrelevant to every branch decision.**
  The universal sequence is a single concrete integer orbit (with no symbols), and the
  dk/dp table is read off from it.

### 4.4 Size bound on small parts [Class-A]
The sum lemma, applied separately to scale and small parts, gives:
Σ_v c_v = 2^i (where i = level entries consumed) and Σ_v λ_v = 3s+1, with all terms ≥ 0.
Hence every chain has λ_x = λ_A + 2λ_b + 3 ≤ 6s+5, and so **j ≤ log2(6s+5).**
(Measured: max λ_x/(3s+1) = 1.5.)

### 4.5 Nested levels inherit margins [Class-A]
Consider a chain inside the cascade of a level fire (ρ, j′) with ρ > j′, at sub-index a.
Treating u′ as an atomic odd base, its value is c′u′ + λ′. In U-terms the small part is
c′λ_{u′} + λ′, and v2 of that is min(v2 c′, v2 λ′) when the two differ. The scale part has
valuation v2(c′) + ρ − j′ > v2(c′). So **the U-margin holds at that chain iff the sub-level
(base u′) chain is tie-free.** The sub-level is the universal process at index a < j′ < ρ.
So in U-terms, the only chains that can break the margin are those whose scale valuation drops
to ≤ log2(6s+5). Those are exactly the mixed (exit) chains, whose x combines values from
different levels.

### 4.6 Reduction theorem [Class-A] and residual
**Theorem R.** Suppose the universal walk (generic odd U) satisfies the margin
  (M) v2(c_x) > log2(6s+5) at every chain.
Then:
- (a) holds for every j that occurs: re-entry is clean (Prop 1 + §4.1), with dk ≥ 1, dp ≥ 2,
  and every chain has u ≥ 7·(U/3) ≥ 3 (§4.3). Here dp ≤ 6 is not needed. Termination still needs **progress**: the level pointer i must
  pass every n (there are no infinite runs inside pushed material). This is part of the residual,
  together with (M). It holds for every n ≤ 4·10^5 [Class-B].
- I(ρ) holds for all ρ.
- (b) becomes k_ρ = s_ρ/2.

Write Δ_x := i − v2(c_x) (the deficit at that chain). Then (M) follows from the pair
  (M1) Δ_x ≤ C₁·log2(i) + C₂   and   (M2) s ≤ i^{C₃}
for i ≥ i₀, together with the finite symbolic base i < i₀.
Measured [Class-B, symbolic walker valid for every odd U]:
- tie-free, with j = v2(λ_x) at every chain, for level index ≤ 4·10^5;
- Δ ≤ 14 (Δ = 12 for i ≤ 2·10^4; first Δ=14 at i=24496), i.e. Δ ≤ log2(i);
- s ≈ 0.9·i.
**Not proved:** (M1) and (M2) for all i. (M2) is the same statement as (b), up to a
polynomial. (M1) asks how much a chain's scale valuation can fall below the level index,
which is about the depth of exits inside exits; that depth is exactly what drives §4.2.
I see no route to (M1) that avoids controlling that depth, and I did not obtain a proof.

### 4.7 Cross-checks [Class-C]
V5: the walker's 6053 level fires up to index 2·10^4 equal the universal (p,k,j) sequence
built from the concrete Φ_m table. V3 (m<3000) agrees class by class with §1–§4.1.
Well-foundedness is not used by Theorem R: it is one forward walk, not a recursion on j.

> **Supersession note (after external review, Astra).** Several parts of §4 are withdrawn and
> replaced by §5:
> - §4.3's claim "λ follows the ordinary top map" (false: at s=4, x=384U+16 has λ_x=16, a power
>   of 2, while the real chain has u=24U+1);
> - the bound "u ≥ 7U/3";
> - the "iff" of §4.5 (only "unequal valuations ⇒ U-margin" survives);
> - the form of (M) in §4.6 (it is false at the first chain, x=48U+10);
> - the claim that progress yields clean re-entry.
>
> The crossing classification in §4.1 must allow the partner Y to be an *original* entry
> (E_{n−1}). It is not used in §5. §4.2, the escaping-branch finding, stands.

## 5. Repaired Theorem R

### 5.1 The formal tagged pair map F [definition]
A state is (A; P; i):
- A = (c_A, λ_A) ∈ ℤ²_{>0} is the head;
- P is a finite list of tagged pairs (c, λ, tag), where tag records the producing chain and
  whether the entry is a run entry M or a D;
- i ≥ 0 is the index of the first *unread* original entry E_a = (2^a, 0).

Reading takes the first two entries of P, then continues with E_i, E_{i+1}, … as needed, and
advances i by the number of originals read. The start state is A=(1,1), P=∅, i=0. One step is:
- **Parity** := (c_A + λ_A) mod 2.
- **Even step:** A ← (c_A+c_b+c_c, λ_A+λ_b+λ_c+3).
- **Chain:** let c_x = c_A+2c_b and λ_x = λ_A+2λ_b+3. F is **defined** at this chain only if
  - (S1) v2(λ_x) < v2(c_x), and
  - (S2) c_A is even.
  Then j := v2(λ_x) and u := (c_x/2^j, λ_x/2^j). F pushes u·2^t (t = 0..j−2) and then
  D := (c_c + c_A/2, λ_c + (λ_A+1)/2), and sets A ← (c_u, λ_u + 1).
  F never halts. It allows λ_u = 1 and still emits the prescribed head and stack (this is the
  repair of review defect D2).
- The initial steps need no special case. Parity uses c_A + λ_A, so the start A = U+1
  (c_A = 1) is handled exactly. For example, the first chain is x = 48U+10, which is
  margin-safe with v2(λ_x) = 1 < 4.

### 5.2 Simulation lemma [Class-A]
Fix any odd U ≥ 1 and map the state (A;P;i) to the real list
(c_A U+λ_A; c_p U+λ_p for p ∈ P; 2^i U, 2^{i+1} U, …).
Suppose F is defined on steps 0..s−1. Then the real top-map orbit of (U+1; U, 2U, 4U, …)
passes through exactly the image states. No real chain among these steps halts, and every real
chain has u = c_u U + λ_u with c_u even ≥ 2 and λ_u odd ≥ 1. Hence u ≥ 2U+1 ≥ 3, and u ≥ 7
when U ≥ 3.

*Proof (induction on steps; invariant: integer components, positivity, equal stack lengths).*
- **Parity.** c_A U + λ_A ≡ c_A + λ_A (mod 2), since U is odd.
- **Even step.** Both sides apply the same linear update.
- **Chain.** The real x equals c_x U + λ_x. By (S1), v2(x) = v2(λ_x) = j for every odd U.
  So c_x/2^j is an integer with v2 ≥ 1, hence even ≥ 2, and λ_x/2^j is odd ≥ 1 (because
  λ_x ≥ 3 > 0). This gives u ≥ 2U+1 ≥ 3, so u ≠ 1.
- **Successor.** By the audited closed form (work_r1 / Lemma 1), the real successor is
  (u+1; u, …, 2^{j−2}u, c+(A+1)/2, S). Here A is odd and c_A is even by (S2), so λ_A is odd.
  Therefore D = (c_c + c_A/2)U + (λ_c + (λ_A+1)/2) has integer components.
- **Bookkeeping.** Both sides push j entries. Positivity is preserved because every update is a
  positive combination and λ_x ≥ 3. ∎

### 5.3 Mass identities [Class-A]
At every F-state: c_A + Σ_{p∈P} c_p = 2^i and λ_A + Σ_{p∈P} λ_p = 3s+1. The sums run over the
head and pushed entries only, never over the unread original suffix.
*Proof.* At the start, 1 = 2^0 and 1 = 3·0+1. A step reading originals E_i..E_{i′−1} adds
2^{i′} − 2^i to the c-sum. The small sum gains exactly 3 per step:
- for an even step this is immediate;
- for a chain, the new small sum is (λ_u+1) + λ_u(2^{j−1}−1) + λ_c + (λ_A+1)/2. Using
  λ_u 2^{j−1} = λ_x/2, this equals λ_A + λ_b + λ_c + 3. This is pure algebra and holds even
  when λ_u = 1. ∎

*Corollary.* Every value has λ ≤ 3s+1, so λ_x ≤ 6s+5 and j ≤ log2(6s+5).

### 5.4 Level fires, I(ρ), universality [Class-A, given F defined up to that step]
A **level fire at ρ** is a chain whose b is the original E_ρ. Because P is read first, P = ∅
at that moment and i = ρ. The mass identities then give c_A = 2^ρ and λ_A = 3s+1. By (S2) the
real A is odd with c_A even, so λ_A is odd and s is even. Hence:
**I(ρ):** x = 3·2^ρ U + 6k_ρ + 4 with k_ρ := s/2, and j_ρ = 1 + v2(3k_ρ+2).

F never involves U. So (s, k_ρ, j_ρ) and every decision are the same for all odd U: this is
the universal replay, now as a proved statement.

Now take two consecutive level fires ρ < ρ′. They satisfy:
- dk = (s′−s)/2 ≥ 1. After a chain, A = u+1 with c_u even and λ_u+1 even, so the next step is
  even.
- dp ≥ 2, because the fire reads E_ρ and E_{ρ+1}.
- Every such fire is automatically clean (P = ∅).

These need no Return hypothesis. Return is needed only to assert that a *next* level fire
exists.

### 5.5 Repaired Theorem R [Class-A conditional]
Let N₀ = 20000. For a state with pointer i, define Δ(state) := i − min_{v ∈ {A}∪P} v2(c_v).

**Base [Class-B, symbolic, valid for every odd U; V6].** F is defined at every step with
i ≤ N₀: 17841 states and 6690 chains. In particular (S1) and (S2) hold everywhere, the mass
identities hold, and all 6056 level fires satisfy I(ρ).

**Hypotheses** (only for states with i > N₀):
- (M1′) Δ ≤ ⌊log2 i⌋².
- (M2′) s ≤ i².

**Theorem.** Assume (M1′) and (M2′). Then:
1. F is defined forever.
2. For every odd U ≥ 1, the universal level walk never halts, and every chain has u ≥ 2U+1.
3. I(ρ) holds at every level fire, with the same universal (k_ρ, j_ρ) for all U and all levels.
4. dk ≥ 1 and dp ≥ 2 hold between consecutive level fires.
5. The pointer i → ∞ (progress).
6. k_ρ ≤ ρ²/2.

*Proof.*
- **F defined.** For i > N₀, (M1′) gives v2(c_v) ≥ i − ⌊log2 i⌋² ≥ 1 for every value, so
  (S2) holds. Also v2(c_x) ≥ min(v2 c_A, v2 c_b + 1) ≥ i − ⌊log2 i⌋².
  By §5.3 and (M2′), v2(λ_x) ≤ log2(6i²+5). The function f(i) = i − (log2 i)² − log2(6i²+5)
  is increasing for i ≥ 16 and f(N₀) > 0, so (S1) holds. For i ≤ N₀ the base applies.
- Items 2–4 follow from §§5.2–5.4.
- **Progress.** If i stalled at a value, s would grow without bound while (M2′) bounds it.
- **k_ρ bound.** k_ρ = s/2 ≤ ρ²/2. ∎

Measured on the base [Class-B]:
- Δ ≤ 16 against ⌊log2 i⌋² ≈ 196;
- s ≤ i² holds by a wide margin;
- the longest stretch without pointer advance is 11 steps.

**Remaining explicit hypotheses:**
- (M1′) and (M2′) for i > N₀ (Class-C).
- **(Return)**: after every level fire there is another. This is needed only for the per-class
  (dk, dp) table formulation of (a), not for non-halting of the universal walk (Class-C;
  it holds up to N₀).

**Scope (D5).** The real excursion with run length v−1 coincides with F (U = 3w) only until the
first read of the substituted boundary entry (the defect, index v−1). Behaviour after that
point is the endgame. It is *not* covered here; that remains the separate templates and
domination argument of the closed-form report §6.2. Likewise, the per-class object Φ_m equals
the universal walk only until D_h is read. Nested sub-runs need no separate treatment, because
they are part of the single walk F.
