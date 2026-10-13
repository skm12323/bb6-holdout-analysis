# M: the deficit is a top-level phenomenon. Reduction of (M1′)+(M2′) to an exit-length lemma

Machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Base: work_r1/RULES.md §5 and the formal
pair map F with its audited lemmas in work_g6/PROOF_G6.md §5 (simulation §5.2, mass identities §5.3,
level fires §5.4, Theorem §5.5). All notation is from G6 §5.1. Checks: `verify_m.py` (V1–V4).

Tags: **[Class-A]** proved for all parameters. **[Class-B]** finite computation (range stated).
**[Class-C]** data or conjecture.

## 0. Results

| # | statement | tag |
|---|---|---|
| R1 | **Call/return decomposition.** Every chain runs a verbatim copy of F's own prefix (a *call*). Steps inside calls inherit (S1),(S2) from earlier steps. Only *top-level chains* (level fires and exit chains) can break (S1); (S2) never breaks after step 0. (§2–3) | A |
| R2 | **Exact margin recursion.** At the top-level chains of one epoch, v2(c_x) is σ_0=ρ and σ_{t+1}=σ_t−1−ε(j_t−1). Here ε(n)∈ℕ is the deficit of F's own crossing state X(n). There is also an exact formula for ε, and the deficit is bounded by Δ ≤ i−σ_t+j_t. (§3) | A |
| R3 | **Cheap certificate.** By R1–R2, F can be certified using the small parts λ alone. F is defined for all i ≤ 10^8 (89,213,562 steps). There r ≤ 2, ε ≤ 7, Γ ≤ 2 and τ(n) ≤ 0.893n. (§4) | A+B |
| R4 | **Theorem M.** Assume (EL): every epoch with ρ>10^8 has at most ⌊log2 ρ⌋² exit chains. Then F is defined forever and the universal walk never halts. The pointer tends to ∞, s ≤ i² holds, which is (M2′), and Δ ≤ (log2 i)³. (§5) | A (cond.) |
| R5 | **Exit depends on J only, if tie-free.** In an epoch whose level fire has parameter J, every top-level small part is affine in one odd symbol. *Assume every valuation comparison met in the recursion of Lemma 6.1 is strict (tie-free).* Then the whole exit (r, the j's, the ε's, Γ) is a computable function of J. V4 certifies tie-freeness for **all J < 10^6**, with r ≤ 2 and Γ ≤ 6. | A (cond. tie-free) + B |
| R6 | **Unconditional finite horizon.** F is defined, and the universal walk does not halt, for every s < (2^{J*+1}−4)/3, where J* = 10^6 − 1. Throughout that range, (M1′) holds literally and so does (M2′). (§6) | A+B |
| R7 | **Remaining lemma.** (EL_J): for every J ≥ 10^6 the symbolic exit is tie-free and has at most ⌊J/2−1⌋² exit chains. This implies (EL) and hence everything in R4. (§8) | open |

So the G6 hypotheses (M1′),(M2′) are no longer the obstruction. (M2′) is derived, (M1′) is replaced by an explicit upper bound
(Lemmas 3.3–3.4), and the open content is one statement about the length of the exit sequence
after a level fire. Under a tie-free hypothesis (certified for J < 10^6) that length is a function of J alone; the observed values are tiny (r ≤ 2), and
it is verified for J < 10^6.

## 1. Notation

F is the formal pair map of G6 §5.1. Its states are Σ_s=(A;P;i), and its start is A=(1,1), P=∅, i=0.
We write W for F itself when it is used as a "subroutine".

- Write v=(c,λ). For a pair u=(c_u,λ_u) with c_u even and λ_u odd, define the linear map
  M_u(c′,λ′) := (c_u c′, λ_u c′ + λ′). Then M_u(E_a)=2^a u, M_u(1,1)=u+(0,1) and M_u(0,1)=(0,1).
- τ(n) is the step at which the original E_n is read for the first time. X(n):=Σ_{τ(n)} is the
  *crossing state*. τ is nondecreasing, and τ(0)=τ(1)=0.
- Crossing types. The step τ(n) reads E_n, so exactly one of the following holds:
  **(a)** P=∅ and i=n; **(b)** P=∅ and i=n−1 (the step reads E_{n−1}, E_n); **(c)** P=[Y] and i=n.
- The crossing deficit is ε(n) := n − v2(c_A) at X(n). By the mass identity (G6 §5.3), type a has
  c_A=2^n, so ε=0. Type b has c_A=2^{n−1}, so ε=1. In type c we have c_A+c_Y=2^n with both positive. If
  their valuations differed, the smaller one would equal n, which would force c_A+c_Y ≥ 2^{n+1}.
  So v2 c_A = v2 c_Y < n, and ε(n) ≥ 1.
- Parity rule. At every state with s ≥ 1, c_A is even (Lemma 2.1 and §3). So the parity of the real
  head is λ_A mod 2.

## 2. Calls [Class-A]

**Lemma 2.1 (image commutes with F).** M_u is linear, so it commutes with the even update and with
the D-formula: M_u(c′)+(M_u(A′)+(0,1))/2 = M_u(c′+(A′+(0,1))/2). It also preserves parity,
because c_u c′+λ_u c′+λ′ ≡ c′+λ′ (mod 2).
Let a W-step be a chain with x′ satisfying (S1),(S2). Then M_u(x′)=(c_u c′_x, λ_u c′_x+λ′_x) has
v2(λ-part) = v2(λ′_x) = j. This holds because v2(λ_u c′_x)=v2(c′_x)>v2(λ′_x). Moreover
j < v2(c′_x) < v2(c_u c′_x), so (S1) holds with the **same j**. (S2) holds too, since c_u c′_A is even.
The images of the run base, of the pushes and of D are the M_u-images of W's. ∎

**Lemma 2.2 (replay).** Let a chain at step s₀ have parameter j and run base u. Its D is
c+(A+1)/2, and R denotes the list after its (b,c). Put n=j−1 and assume E_n was read before s₀,
i.e. i_{s₀}>n. Then for 0 ≤ w ≤ τ(n) the state at s₀+1+w is
  head M_u(A_w), list M_u(P_w) ++ [M_u(E_a): i_w ≤ a ≤ n−1] ++ [D] ++ R, same pointer as at s₀+1.
Here (A_w;P_w;i_w)=Σ_w. Each step s₀+1+w with w<τ(n) is the M_u-image of W-step w. In particular it
is defined, because W-step w < s₀+1+w is an earlier step. Also, no original of R is read.
*Proof.* Induct on w. At w=0 the state is the image of the start state. The W-step w<τ(n) reads the
first two entries of P_w ++ [E_{i_w},…]. Because w<τ(n), these lie in P_w ++ [E_{i_w..n−1}], whose
images are the first entries of the U-list. Now apply Lemma 2.1. A U-original would be read only if
the part before R had ≤ 1 entry, i.e. P_w=∅ and i_w=n. Then W-step w reads E_n, so w=τ(n). ∎

**Lemma 2.3 (return state).** At U-step s₀+1+τ(n) (the *return step*), the list is
(a) [D] ++ R, (b) [M_u(E_{n−1}), D] ++ R, or (c) [M_u(Y), D] ++ R, according to the type of X(n).
The head is H=M_u(A_X). So the return step always reads D, and the parity of H equals the parity of
W's head at X(n). (Immediate from 2.2 at w=τ(n).) ∎

Inner chains of a call are images of W-chains, and their calls are images of W's calls. By Lemma
3.3, crossings occur only at top-level states of W. So no W-call is open at X(n), and every inner
call window closes inside the outer window. Hence call windows are nested or disjoint. Convention: a call window is the half-open interval of steps from the step after the chain up to, but excluding, its return step. Edge case: when X(n) is a type-(c) crossing sitting on W's own type-(a) return (P=[D_t], Y=D_t; this occurs at every crossing with ε∈{3,5,7}), the image of the inner call returns on the same step as the outer call (step s₀+1+τ(n)); that shared step reads (M_u(D_t), D) and belongs to neither window, so it is not required to be a faithful image of W's return.

## 3. Epochs, top-level chains, margin recursion [Class-A]

An **epoch** starts at a state with P=∅ (pointer ρ, head (2^ρ, 3s+1)). If the head is even, one even
step leads again to P=∅. If the head is odd, step 0 is a *level fire* (chain 0, σ_0:=v2(c_x)=ρ).

**Lemma 3.1 (epoch structure).** Suppose top-level chain t has R = originals only, and suppose
j_t<σ_t:=v2(c_{x_t}) holds. Then σ_t ≤ ρ ≤ i, so E_{j_t−1} has already been read and Lemma 2.2 applies. The
return step reads (D_t,E_i), (M(E_{n−1}),D_t) or (M(Y),D_t), and after it R is again originals only.
If H is even, the return step is an even step and leaves P=∅, which ends the epoch.
If H is odd, the return step is the next top-level chain t+1 (an *exit chain*), and its R is
originals only. So an epoch is: level fire, call, return, (exit chain, call, return)^r, even step.
Every step that is not top-level lies inside a call window. ∎

**Lemma 3.2 (σ-recursion; S2).** Write n=j_t−1 and ε=ε(n). Then σ_{t+1} = σ_t − 1 − ε. Also
c_{H} = c'_H c_{u_t} is even, so (S2) holds at every top-level chain.
*Proof.* Recall v2(c_{u_t}) = σ_t − j_t.
- (a) H has c_H=2^n c_u=c_{x_t}/2. The return state has P=[D_t], so the mass identity gives
  c_H+c_{D_t}=2^i, and c_{x_{t+1}}=c_H+2c_{D_t}=2^{i+1}−c_H. Since σ_t−1<i, its v2 is σ_t−1.
- (b),(c) x_{t+1} = M_u(x′_W), where x′_W is W's chain at step τ(n). Its c-part is
  c_u(2^{n−1}+2^n) in case (b) and c_u(2^{n+1}−c′_A) in case (c). The v2 is σ_t−j_t+n−ε. ∎

Corollary: in cases (b) and (c), exit chain t+1 is an image of an earlier W-chain. So it is
automatically safe (Lemma 2.1), and j_{t+1} is W's j at τ(n).

**Lemma 3.3 (bookkeeping; ε-formula).**
- Chain t′ ≥ 1 reads an original iff the return of chain t′−1 had type (a). Hence at the return
  after chain t, i = ρ+2+a_t, where a_t ≤ t counts those type-(a) returns.
- Crossings happen only at top-level states. By 2.2, no original is read inside a call window.
  A top-level state with |P|=1 is exactly a type-(a) return state P=[D_t].
- Such a crossing has v2(c_H)=σ_t−1. Therefore
  **ε(i) = i−σ_t+1 = 3 + a_t + t + Σ_{t′<t} ε(j_{t′}−1) ≤ 3 + 2t + Σ_{t′<t} ε(j_{t′}−1).**
  All other crossings have ε ∈ {0,1}. ∎

**Lemma 3.4 (deficit).** Consider a state between chain t and its return step (inclusive).
- Every entry other than D_t and the originals is an M_{u_t}-image, so it has v2 ≥ σ_t−j_t.
- D_t has v2(c_{D_t}) = σ_t−1. This follows from mass at the return state: c_{D_t} = 2^i − c_{x_t}/2.
- Hence **Δ ≤ i − σ_t + j_t**, and Δ=0 at P=∅. ∎

**Corollary 3.5 (localization).** F is defined at all steps ⇔ j_t<σ_t at every level fire and at
every exit chain that follows a type-(a) return. (⇒ is trivial. For ⇐, induct on time using
2.2, 3.1, 3.2.)

## 4. λ-certificate [Class-A validity, Class-B run]

The walker of V2 runs only on the λ-parts. It uses parity λ_A mod 2 (s ≥ 1), j=v2(λ_x), pushes
λ_u2^t and λ_D=λ_c+(λ_A+1)/2, and computes σ_t by Lemma 3.2 and ε by Lemma 3.3. At each top-level
chain it asserts j<σ.

**Theorem 4.1.** If the walker runs to pointer N without failing an assertion, then F is defined
there.
*Proof.* Induct on time. Inside call windows, Lemma 2.2 applies. At top-level chains, the computed
σ equals v2(c_x) (Lemma 3.2), so the assertion is (S1); (S2) holds by Lemma 3.2. While F is
defined, the λ-parts and the decisions are exactly the walker's. ∎

**V2 result [Class-B].** F is defined up to i=10^8 (89,213,562 steps), up to the end of the last
epoch. Other figures over this range:
- epochs: 30,288,015;
- r distribution: {0: 27,914,754; 1: 2,370,538; 2: 2,723};
- max Γ = max(ρ−σ_r) = 2 and ε ∈ {0,1,3,5,7};
- max(i−σ+j) = 28 and max j = 26;
- s/i ≤ 0.8928, hence τ(n) ≤ n.
V1 checks every Class-A lemma above against the full pair map for i ≤ 20000. The checks are:
- the return state equals the image of X(j−1) followed by D (6531 returns);
- the σ-recursion and the ε-formula;
- crossings occur only at top-level states;
- Δ ≤ i−σ_t+j_t at every epoch state.

## 5. Theorem M [Class-A, conditional on (EL)]

**(EL)** Every epoch whose level fire is at ρ>N_B=10^8 contains at most L(ρ):=⌊log2 ρ⌋² exit chains.

Write g:=2log2ρ+4 and E:=max(7,g/4). The following inequalities are used for ρ ≥ 10^6:
(I1) L(1+E)+g<ρ; (I2) 3+L(2+E) ≤ ρ/4; (I3) (L+1)(1+g²) ≤ 2ρ; (I4) 2+L(2+E)+g ≤ (log2ρ)³.

*Proof of (I1)–(I4) (analytic).* Put x=log2ρ ≥ x₀:=log2 10^6 > 19.93. Then L ≤ x² and
g=2x+4. Since x ≥ 12, g/4=x/2+1 ≥ 7, so E=x/2+1. Each left side is increasing in L, so it is
enough to prove the inequalities with L=x²:
- (I4): the residual is x³−2−x²(x/2+3)−2x−4 = ½x³−3x²−2x−6 = x²(x/2−3)−2x−6. For x ≥ 10 this is
  ≥ 2x²−2x−6 > 0.
- (I1)–(I3) have the form 2^x > P(x), with P a polynomial of degree ≤ 4 and positive coefficients:
  - (I1): P(x) = ½x³+2x²+2x+4;
  - (I2): P(x) = 2x³+12x²+12;
  - (I3): P(x) = ½(x²+1)(4x²+16x+17).

  Positive coefficients give xP′ ≤ 4P, so d/dx ln(P(x)/2^x) ≤ 4/x − ln2 < 0 for x > 5.78. Hence
  P(x)/2^x decreases on [x₀,∞). At x₀ (2^x₀ = 10^6) the values are P < 4.8·10^3, P < 2.1·10^4 and
  P < 3.9·10^5 respectively, all below 10^6. ∎

V3 evaluates these residuals at x₀ and also does a numeric grid check; neither is needed for the
proof.

**Theorem M.** Assume (EL). Then F is defined forever, and so the G6 Theorem conclusions 1–6 hold
(universal walk never halts, u ≥ 2U+1, I(ρ), dk ≥ 1, dp ≥ 2, i→∞, k_ρ ≤ ρ²/2). Moreover:
- **(M2′)** s ≤ i² at every state;
- every state with i>N_B has Δ ≤ (log2 i)³.

*Proof.* Proceed by induction over epochs, with these claims for every reached crossing n ≥ 1:
**(C1)** τ(n) ≤ n²; **(C2)** ε(n) ≤ max(7,n/4).
The base for ρ ≤ N_B is V2, with τ(n) ≤ n and ε ≤ 7.

Take an epoch at ρ>N_B with s_0=τ(ρ) ≤ ρ². For t ≤ r ≤ L (EL), induct on t:
- Suppose s_t ≤ ρ²+t(1+g²) ≤ 2ρ² (using (I3)). Then j_t ≤ log2(6s_t+5) ≤ log2(16ρ²) = g
  (G6 §5.3 corollary).
- By 3.2 and (C2) at indices <g: σ_t ≥ ρ−t(1+E) ≥ ρ−L(1+E) > g ≥ j_t (I1). So chain t is defined.
- Its call lasts τ(j_t−1) ≤ g² steps (C1), so s_{t+1} ≤ s_t+1+g².

Let s_fin := s_r+1+τ(j_r−1) be the final step of the epoch (the even return step). Then
s_fin ≤ ρ²+(r+1)(1+g²) ≤ ρ²+(L+1)(1+g²) ≤ ρ²+2ρ by (I3). Every crossing of the epoch is read at
a step ≤ s_fin.
- So new crossings n>ρ satisfy τ(n) ≤ ρ²+2ρ < (ρ+1)² ≤ n². This gives (C1).
- The epoch-end state (P=∅, pointer ρ′ ≥ ρ+2) is reached at time s_fin+1 ≤ (ρ+1)² < ρ′², so
  τ(ρ′) ≤ ρ′² for the next level fire.
- An even step at P=∅ gives τ(ρ+1)=τ(ρ) and τ(ρ+2)=τ(ρ)+1 ≤ (ρ+2)².
- ε(n) ≤ 3+L(2+E) ≤ ρ/4 by Lemma 3.3 and (I2), which gives (C2).

Even steps at P=∅ advance i by 2 in one step. Every epoch ends and advances i, so F is defined
forever and i→∞. A state with pointer i has s ≤ τ(i) ≤ i². By 3.4, 3.3 and (I4),
Δ ≤ 2+t+a_t+Σε+j_t ≤ 2+L(2+E)+g ≤ (log2 i)³. ∎

Remarks:
- (M1′) is used nowhere. The deficit is *controlled* by 3.3–3.4. It is bounded above by
(i−σ_t)+j_t, i.e. 2+a_t+(epoch cost Σ(1+ε))+j_t. This is an upper bound only.
  [Class-C observation] The G6 record values Δ=2,…,16 at i=(4^m−1)/3-type spikes were observed to be the j of a level fire plus at most 2.
- (EL) is far weaker than the observed r ≤ 2. The proof only needs r = o(ρ/log ρ) in the same way;
  L=log² was chosen so that the inequalities stay elementary.

## 6. Exits are a function of J (when tie-free); verification for J < 10^6 [Class-A + Class-B]

Fix a level fire with s_0 and J=v2(3s_0+4), and put λ_u:=(3s_0+4)/2^J (odd).

**Lemma 6.1.** During the epoch, every top-level small part has the form αλ_u+β. Here α,β∈ℤ are
produced by the following recursion, which uses only J and W's crossing data X(n):
- start: x_0=(2^J,0)·λ_u, u_0=1·λ_u, λ_{D_0}=2^{J−1}λ_u−1;
- at a return: H, Y = M-images, so (c′α_u, c′β_u+λ′);
- at an exit chain: x = H+2b+3, j = v2(β_x) **provided v2(β_x) < v2(α_x)** (then v2(αλ_u+β)=v2(β)
  for every odd λ_u), u = x/2^j;
- D_{t+1} = c+(H+1)/2, with c=0 in type (a) and c=D_t in types (b),(c).
Parity is decided as α+β mod 2. **Hypothesis (tie-free):** every valuation comparison
encountered is strict (v2 β_x < v2 α_x). Under it, the exit is the same for every
level fire with this J and every ρ. That includes r, the j's, the types, the ε's and Γ=Σ(1+ε).
(Proof: induction over top-level steps with 2.3 and 3.1. λ_A=3s_0+1=2^Jλ_u−3 enters only via D_0.) ∎

**V4 [Class-B].** The recursion was run for every J < 10^6, using the
exact crossing data X(n) from the full pair walk. Results:
- no ties, so the tie-free hypothesis of 6.1 holds for every J < 10^6 and Theorem 6.2 is
  unaffected; no long exits;
- r ∈ {0,1,2}, with counts {0: 378,393; 1: 574,113; 2: 47,493} (log `run_v4_1e6.txt`; 12 min);
- max Γ = 6 and max exit-chain j = 21;
- the V4 patterns equal V2's empirical patterns for every J seen in V2 (J ≤ 26).

**Theorem 6.2 (unconditional finite horizon).** F is defined, and the universal walk never halts,
for all s < (2^{J*+1}−4)/3, where J*=10^6−1.
*Proof.* A level fire at step s has J=v2(3s+4), and J>J* forces 3s+4 ≥ 2^{J*+1}. Before that
step, every epoch with ρ ≤ N_B is covered by V2, and every epoch with ρ>N_B has J ≤ J*. By V4 such
an epoch has r ≤ 2 ≤ L(ρ), so the induction of Theorem M runs unchanged. ∎

In this range r ≤ 2 and E=7 (indices < g ≤ N_B, because ρ ≤ 2s+2). So Δ ≤ 2+2(2+7)+g = 24+2log2ρ ≤
⌊log2 i⌋² for i>N_B. For 2·10^4<i ≤ N_B, V2 gives Δ ≤ max(i−σ+j) = 28 ≤ ⌊log2 i⌋². **(M1′) and (M2′) therefore hold literally for all states up to that step.**

## 7. Partial structure of exits [Class-A]

Let J be the parameter of the level fire and n=J−1.

- **P1.** r ≥ 1 iff W's head at X(J−1) is odd (Lemma 2.3).
  In types (a)/(b) this means W itself fires at J−1, respectively J−2.
- **P2.** After a type-(b)/(c) return, the exit chain is W's chain at τ(n). Its j is W's j there,
  ≤ log2(6τ(n)+5), and its margin is automatic.
- **P3.** After a type-(a) return following the level fire, λ_{x_1} = 3·2^nλ_u + 3τ(n)+2, with
  τ(n)=2k_n.
  - So j_1 = 1+v2(3k_n+1) whenever this is < n.
  - **Conditional on (C1)** for n=J−1 (i.e. 3τ(n)+2 ≤ 3n²+2 < 2^n):
    - the condition holds for J ≥ 10;
    - then the first exit chain has j_1 ≤ log2(3J²+4), a strict logarithmic descent.
  - (C1) is proved for n ≤ 10^8 (V2: τ(n) ≤ n) and for all n under (EL) (Theorem M).
  - J < 10 is covered by data only (V2/V4 patterns), not by this argument.
  - Examples: J=14 → k_13=5 → j_1=5; J=5 → j_1=3.
- **Not proved:** descent for later type-(a) exits, and termination. The later residues mix
  τ(j_t−1) and k_n modulo 2^{O(log J)}. There is no finite closure: j_1 grows like log J.

## 8. Remaining lemma (exact)

**(EL_J)** For every J ≥ 10^6, the recursion of Lemma 6.1 is tie-free and reaches an even return
after at most ⌊J/2−1⌋² exit chains.

(EL_J) ⇒ (EL). By (C1), a fire with parameter J has 2^J ≤ 3s_0+4 ≤ 3ρ²+4, so log2ρ ≥ J/2−1.
Hence Theorem M applies: non-halting of the universal walk, with (M2′), Δ ≤ (log2 i)³ and
k_ρ ≤ ρ²/2.

If a tie ever occurred, (EL) would have to be shown per fire instead of per J.

(EL_J) is a statement about F's own crossing data at index J−1 and at indices O(log J). It is
arithmetic: it concerns 2-adic valuations of combinations of τ(·) and k(·), as in P3. I did not find
a structural reason for termination; the exit can continue whenever an odd crossing is hit, which
happens at about 60% of indices.

[Class-C] Observations: the exit pattern is a function of J (Lemma 6.1, under the tie-free hypothesis, which V4 certifies
for J < 10^6). r ≤ 2 for
every J < 10^6. In every r=2 exit the last exit chain has j ≤ 4 (checked for J < 6·10^4). Max Γ = 6.

## 9. Scope

- Everything concerns F, i.e. the universal walk (G6 §5).
- The D5 scope note of G6 (endgame of modified-tail excursions) is unchanged and not addressed.
- Return/next-fire existence is now proved under (EL): every epoch ends and the next P=∅ state
  follows.
- No git operations were performed. Files: `PROOF_M.md`, `verify_m.py`, run logs `run_*.txt`.

Reproduce:
- `python -B verify_m.py 20000 100000000 200000` runs V1–V4 in about 2 min.
- `python -B -c "import verify_m as v; v.V4(1000000)"` runs V4 to 10^6.
