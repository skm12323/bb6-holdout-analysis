# EGX: the endgame of E(w,v) is the symbolic exit of J = v

2026-10-17, Claude Opus 5.5. Revised after three-way review (record in §9).

**Chain numbering.** Throughout, chains of S(J) are numbered t = 0 (the fire), 1, 2, …, and the
endgame's top-level chains are numbered from t = 1 so that endgame chain t is exit chain t of S(J).

Machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Notation: work_r1/RULES.md (top map),
work_r4/PROOF.md (singletons, excursions), work_g6/PROOF_G6.md §5 (pair map F), work_m/PROOF_M.md
(calls, returns, epochs, Lemma 6.1 symbolic exit), work_el/PROOF_EL.md (Lemma T, Theorem D),
work_tie/PROOF_RESCUE.md §4, work_tie2/PROOF_TIE2.md §5, work_global_clock/PROOF_CLOCK.md,
work_global_endgame/LEMMAS_E.md (E1–E5). Tags: [A] proved for all parameters, [B] finite computation.

## 0. Results

| # | statement | tag |
|---|---|---|
| EGX | For every v ≥ 3, the endgame of E(w,v) is, at top level and pair for pair, the symbolic exit S(J) of PROOF_M Lemma 6.1 with J = v, under (c,λ) ↔ (α,β), i.e. U ↔ λ_u. In particular: the endgame is safe (S1, S2 at every chain) ⇔ S(v) is tie-free; it reaches the singleton ⇔ S(v) reaches an even return; at endgame chain t, v2(c_x) = v − Γ_t. | A |
| H | **The TM does not halt during the first 2^{K′} − 2 top steps**, K′ = 2^(2^(2^499997−3)−2). (Previous audited real-machine range: 2^2001 − 2, work_r4.) | A + imported A+B |
| C2-log | If the epoch of F containing a type-c crossing i is tie-free in the sense of S(J_W) up to that crossing, then ε(i) ≤ max(3, 2J_W − 1) < 2·log2(3i²+4) − 1 (i ≥ 2). | A |
| TR | Transfer: the automaton identities used by the tower proofs (PROOF_EL A1/A2, Lemma T, Theorem B; PROOF_RESCUE (AA) and §4; PROOF_TIE2 §2–§5) hold for S(J) for every integer J, with Θ_t := 2^Jλ_u + 3d_t + 1. | A |
| U | **Single remaining hypothesis.** If (EXT) S(J) is tie-free for every J ≥ K′, then F is defined forever and #1 never halts. No SQRT-EXIT, EG-LEN, (EL) or (C2) hypothesis is used. | A (cond.) |
| L | (LIN-EXIT) "for J ≥ K′, no tie-free prefix of S(J) has more than ⌊J/(3 log2 J)⌋ exit chains" implies (EXT). | A |

Consequences for the open list of CHECKPOINT (2026-10-17): the two open propositions SQRT-EXIT
and EG-LEN are replaced by the single proposition EXT. EG-LEN implies EXT (§7), and EXT implies
SQRT-EXIT for actual fires (§7), so EXT is not harder than the previous pair. The base gap
4·10^6 < v ≤ 10^8 of PROBLEM_ENDGAME §5 disappears: the base of Theorem U is Corollary H.

## 1. The two objects

**Endgame** (LEMMAS_E §0). Fix v ≥ 3, n := v−1, odd U. Run the pair map on E(w,v): originals
E_a = (2^a,0) for a ≤ v−2, the defect δ := (2^{n}, −1) at index n, nothing after it; a missing
second read entry is the zero pair (0,0); the run stops when the list is a singleton. By D5 (queue
determinism) the run equals F through step τ(n); the state there is F's crossing
X(n) = (A_X; P_X; i_X), followed by the unread entries E_{i_X},…,E_{n−1}, δ. The endgame is the
run from this state on.

**Symbolic exit S(J)** (PROOF_M Lemma 6.1; implemented as `verify_m.sym_exit`). For a level fire
of parameter J with odd run base λ_u, every top-level small part is αλ_u+β. The recursion starts
from u_0 = (1,0), λ_{D_0} = (2^{J−1}, −1), and at each top-level step uses only F's crossing data
X(m), m ≤ J−1:

- return after chain t with parameter j (n_t = j−1): head H = M_u(A_X(n_t)) = (c′α_u, c′β_u+λ′),
  list [D_t] (type a), [M_u(E_{n−1}), D_t] (type b), [M_u(Y), D_t] (type c), followed by
  entries whose small part is (0,0) (outer originals);
- H even (α+β even): the epoch ends;
- H odd: chain x = H + 2b + (0,3), b the first listed entry; j = v2(β_x), **required to satisfy
  v2(β_x) < v2(α_x)** (tie-free); u = x/2^j; D_{t+1} = c + (H+(0,1))/2 with c = (0,0) after type a
  and c = D_t after types b, c.

S(J) is **tie-free** if this comparison is strict at every chain it reaches. Γ_t :=
Σ_{t′<t}(1+ε(n_{t′})) with n_0 = J−1, and d_t := s_t − s_0. For any integer J ≥ 2 the recursion is
**defined by these rules**, whether or not J is the parameter of an actual fire; it needs F's
crossing data X(m), m ≤ J−1, and F's own chains at steps ≤ τ(J−1) **inclusive** (a b/c first return
copies F's chain at step τ(J−1)). "F is defined through τ(J−1)" below always includes that step.

**Lemma TR (transfer) [A].** Let J ≥ 2 and suppose F is defined through τ(J−1). Treat λ_u as a
formal odd symbol and put Θ_t := 2^Jλ_u + 3d_t + 1 (for an actual fire this is 3s_t + 5, because
3s_0 + 4 = 2^Jλ_u). Then every identity used in PROOF_EL (A0)–(A3), Lemma T, Theorem B, PROOF_RESCUE
(AA), the rescue macro and §4, and PROOF_TIE2 §2–§5, holds for S(J) as a polynomial identity in
λ_u, with "the λ-part of the current run base" read as the affine form α_uλ_u + β_u.
*Proof.* Those identities are derived from (i) the pair rules of a chain and an even step, (ii) the
return lemma (PROOF_M 2.2–2.3), whose S(J)-version is the definition of the recursion, and (iii)
the mass identities. For (iii), Lemma T(1)–(2) gives the symbolic mass Σα = 2^J, Σβ = 3d − 3
coefficientwise, which is exactly what replaces the real mass λ_A + Σλ = 3s + 1 (the shift by
3s_0 + 4 = 2^Jλ_u is absorbed in Θ_t). Every valuation statement in those proofs is applied to a
real chain value αλ_u + β under the hypothesis h_t ≥ 1, i.e. v2(β) < v2(α); then v2(αλ_u + β) =
v2(β) for every odd λ_u, and the NT test and the a-step bracket agree modulo 2^n with their
β-parts (the α-parts have valuation ≥ n). So each sentence "the real chain has valuation j_t"
becomes "β_{x_t} has valuation j_t", which is what tie-freeness of S(J) asserts. ∎

*Alternative route.* PROOF_SPECTRUM §3 (work_g2_obstruction, accepted) shows that every J with
J + 4 < B is an actual fire parameter inside the horizon; with TIE2's r ≤ 7 its GAP step extends
to every J < K′ − 4, so for those J the imports apply to an actual epoch and Lemma 6.1 identifies
its exit with S(J). This would cost at most a factor 2^4 in Corollary H. Lemma TR avoids that loss.

## 2. Theorem EGX [A]

**Theorem EGX.** Let v ≥ 3, J := v, and assume F is defined through step τ(v−1). Identify a pair
(c,λ) of the endgame with the symbolic pair (α,β). Then, for every t ≥ 0, as long as the endgame
is safe through its first t top-level chains, equivalently S(J) is tie-free through its first t
exit chains:

1. the endgame's top-level state just before its chain t+1 (t = 0: the state X(n)) equals
   S(J)'s return state after chain t (chain 0 = the fire), entry by entry;
2. the next decision is the same: even head ⇔ end (singleton, resp. epoch end); odd head ⇔ chain
   t+1 with the same x-pair; S1 at the endgame chain ⇔ strict comparison in S(J); S2 holds;
3. v2(c_{x_t}) = J − Γ_t at endgame chain t ≥ 1.

Consequently the endgame is safe ⇔ S(v) is tie-free, the endgame reaches the singleton (2^v, 3ℓ(v))
⇔ S(v) reaches an even return, and the two have the same number of chains, the same j's, the same
return types and the same final step count.

*Proof.* **Start (t = 0).** By the definition of S(J) in §1 (for an actual fire this is PROOF_M
Lemmas 2.2–2.3 at w = τ(n)), S(J)'s return state after the fire is head M_{u_0}(A_X) and list M_{u_0}(P_X) ++ [M_{u_0}(E_a) : i_X ≤ a ≤ n−1] ++ [D_0] ++ R.
With u_0 = (1,0), M_{u_0}(c′,λ′) = (c′,λ′); D_0 = (2^{n}, −1) = δ; R consists of outer originals, of
small part (0,0). So the symbolic state is (A_X; P_X ++ [E_{i_X},…,E_{n−1}] ++ [δ]; then (0,0)'s),
which is the endgame state at X(n) with "missing = (0,0)". Its list has one of the three shapes
[δ], [E_{n−1}, δ], [Y, δ] (types a, b, c of X(n)).

**Return lemma in the endgame.** Let an endgame top-level chain at step s₀ satisfy S1 and S2, with
parameter j and base u. S1 gives j < v2(c_x) ≤ v (c_x < 2^{v+1} by the mass identity E4), so
n′ := j−1 ≤ v−2 and X(n′) is a crossing of F reached before X(v−1). The proof of PROOF_M Lemma 2.2
applies verbatim: for w < τ(n′) the W-step w reads only images of P_w ++ [E_{i_w..n′−1}], i.e.
the pushes u·2^t; it never reads D or what follows D. Each such step is the M_u-image of an
earlier defined W-step, hence defined (PROOF_M Lemma 2.1, S1 with the same j, S2 since c_u is even).
At step s₀+1+τ(n′) the state is head M_u(A_X(n′)) and the list of Lemma 2.3 shape (a)/(b)/(c)
with D = c + (A+1)/2, followed by the rest of the endgame list (which is empty or zero-filled after
the defect is consumed). The endgame chain is of type (a) if X(n′) has type a, and so on.

**Induction step.** At a top-level state of shape (a)/(b)/(c) both runs apply the same rule:
- the head parity is (c_H + λ_H) mod 2, resp. (α_H + β_H) mod 2;
- even head: the step adds the first two entries. From [D] the second entry is (0,0) in both. From
  [M(E_{n−1}), D] or [M(Y), D] both entries are present. The list becomes empty. In the endgame
  this is the singleton; in S(J) this is the end of the epoch (PROOF_M Lemma 3.1);
- odd head: x = H + 2b + (0,3) with the same b. Endgame S1 is v2(λ_x) < v2(c_x); S(J)'s condition is
  v2(β_x) < v2(α_x): the same inequality under the identification. S2: c_H = c′_H c_u is even
  because c_u is even (S1 at the previous chain), and at t = 0 c_{A_X} is even for n ≥ 2
  (PROOF_M §1 parity rule; v ≥ 3). The pushes, D_{t+1} = c + (H+1)/2 with c = (0,0) after type a
  (endgame: the zero fill; S(J): an outer original of small part 0) and c = D_t after types b, c,
  and the new head coincide.

Both runs therefore remain equal through the next return (return lemma in the endgame; the
definition of the recursion for S(J)). Item 3 is PROOF_EL Lemma T(1), v2(α_{x_t}) = J − Γ_t, transported by the
identification. The final step count: the endgame step index s corresponds to S(J)'s step
s_0 + 1 + s, so d_t = s_t + 1 (endgame indexing), and E4 gives the final pair (2^v, 3ℓ). ∎

*Remarks.* (i) In the code of PROOF_M, `sym_exit(J, X)` starts with `u=(1,0); D=(1<<(J-1),-1)`:
it **is** the top-level endgame of E(·,J). (ii) The endgame's S1 margin v − Γ_t − j_t is the
quantity h_t = J − Γ_t − j_t of PROOF_EL Theorem B and PROOF_TIE2 ("h ≥ 1 at every chain"). (iii)
agentC10's empirical "closure iff n − D_cross > J" (work_r10) is this margin read at chain 1.
(iv) PROOF_SHADOW §6 noticed that the finite-tail formulas have F's shape, but did not identify
the defect with D_0.

**Data [B]** (`verify_egx.py 30000`, `checks.json`): for 3 ≤ v ≤ 30001 the endgame and S(v) agree
pair for pair at all 20,072 chains (type of the state at which each chain fires, a/b/c:
10,036/9,559/477; by each chain's own return type 15,118/4,744/210), with no tie; exit-chain counts
{0: 11,352; 1: 17,222; 2: 1,425}; Lemma T(1)–(2) hold at every endgame chain; the pair endgame
equals the integer top map (length and final singleton 3w·2^v+3ℓ) for 3 ≤ v < 400 and
w ∈ {1,3,5,7,101,2^61−1}; the j-sequences equal `verify_m.sym_exit` for 3 ≤ v ≤ 20000.
`verify_egx.py 100000`: 0 mismatches for v ≤ 100001 (66,909 chains, exit counts {0: 37,841;
1: 57,407; 2: 4,751}, max endgame steps 16). Reviewers extended this to v ≤ 400,000 (§9).

## 3. Corollary H: the real machine through 2^{K′} − 2 top steps [A + imports]

**Imports.**
- (I-1) R4 §1: singletons never halt; n odd → singleton n+1; n even → E(w,v), n+2 = 2^v w. R4
  Lemma E(v), v ≤ 2000 (audited): covers v ≤ 2.
- (I-2) LEMMAS_E E1–E4 (audited): along a safe pair prefix the real orbit is the pair image for
  every odd U, no chain halts, and a reached singleton is (2^v, 3ℓ).
- (I-3) HORIZON-3 (PROOF_TIE2 §5, audited): F is defined for s < (2^{K′}−4)/3. On the defined
  prefix τ(n) ≤ n² and s ≤ i² (C1, M2′; PROOF_CLOCK §3–4, or Theorem M's induction inside the
  horizon), and (C2) ε(n) ≤ max(7, n/4) at every reached crossing (Theorem M's epoch induction as
  run in TIE2 §5; independently, the corrected Lemma C2-log of §4 by strong induction on J).
  In particular X(m) is reached for every m with m² < (2^{K′}−4)/3: the state at step m²+1 lies
  inside the horizon and has pointer i with i² ≥ s > m², so i > m.
- (I-4) Tie-freeness of S(J) for every J < K′: J < 10^6 by V4 of PROOF_M (Class B, all J); 10^6 ≤
  J < T₁ by PROOF_EL Theorem D (tie-freeness paragraph, via Lemma T); T₁ ≤ J < K by PROOF_RESCUE
  §4 "Margins" (h-induction, symbolic coefficient separation); K ≤ J < K′ by PROOF_TIE2 §5 step 4.
  Each also gives r ≤ 7 and an even return.

**Import audit (what must be true for I-4 to apply to J = v).** The four results are stated for
"fire parameters J" inside Theorem M's induction and are written for an actual epoch (real
Θ = 3s+5, real valuations). By Lemma TR they apply verbatim to S(J) for every integer J in range.
The F-facts they use are: crossing data X(m), m ≤ J−1; the copied W-chains at τ(m), m ≤ J−1 (at
or before τ(J−1)); the location lemma and "rescued chains are never copied" (PROOF_RESCUE §4),
TIE2 §5 step 5; (C1) at J−1 and at the n_t; (C2) at J−1 (Theorem D only). None uses the pointer ρ
or any F step after τ(J−1), except in the separate F-safety step σ_t − j_t = ρ − J + h_t, which
EGX does not need. For J < K′ these F-facts hold by I-3. (Checked by both auditors and the
adversary, §9.)

**Corollary H.** The TM does not halt before the first singleton time n with v2(n+2) ≥ K′; in
particular it does not halt during top steps n < 2^{K′} − 2.

*Proof.* Induction over singleton times n (I-1). At an even n with v = v2(n+2) < K′, v ≥ 3:
X(v−1) is reached with τ(v−1) ≤ (v−1)² < (2^{K′}−4)/3 (I-3), and F's step τ(v−1) itself is
defined, so the excursion agrees with the defined F through X(v−1) (D5). By I-4, S(v) is tie-free and ends at an even return; by EGX the endgame is safe and reaches
the singleton; by I-2 no step halts and the next singleton time is n+1+ℓ(v). v ≤ 2: I-1. ∎

## 4. Lemma C2-log [A]

PROOF_M Lemma 3.3: a type-c crossing i sits at a type-a return after chain t of an epoch of F with
fire J_W at pointer ρ_W < i, and ε(i) = 3 + a_t + t + Σ_{t′<t} ε(n_{t′}) = 3 + a_t + Γ^W_t.

**Lemma C2-log.** If S(J_W) is tie-free through chain t, then
ε(i) ≤ max(3, 2J_W − 1) < 2 log2(3i²+4) − 1 for i ≥ 2.

*Proof.* t = 0 (the crossing sits on the type-a return of the fire itself): a_0 = Γ_0 = 0, so
ε(i) = 3. This case is common: every epoch with J_W = 1 has it. t ≥ 1: tie-free at chain t gives
J_W − Γ^W_t = v2(α_{x_t}) > j_t ≥ 1 (λ_x is even, so j_t ≥ 1). So Γ^W_t ≤ J_W − 2 and
a_t ≤ t ≤ Γ^W_t; hence ε(i) ≤ 3 + 2(J_W − 2). The fire has 2^{J_W} ≤ 3τ(ρ_W)+4 ≤ 3ρ_W²+4 < 3i²+4
by (C1); and 3 < 2 log2(3i²+4) − 1 for i ≥ 2. ∎

(Review: the first version omitted t = 0 and stated ε ≤ 2J_W − 1, false for J_W = 1; the
corrected bound is tight on the walk to n = 2·10^5.)

Types a, b have ε ∈ {0,1}. [B] For n ≤ 30000 the maximum is ε = 7 (V2 of PROOF_M: ε ≤ 7 to 10^8).

## 5. Theorem U: one hypothesis suffices [A, conditional]

**(EXT)** For every J ≥ K′: if F is defined through τ(J−1), then S(J) is tie-free at every chain
it reaches.

Note: S(J) uses only F through τ(J−1) (inclusive), so the hypothesis is meaningful. A tie-free
S(J) ends at an even return after at most max(0, J−2) exit chains: by Lemma T(1) and j_t ≥ 1,
Γ_t ≤ J−2 at every exit chain t ≥ 1, and Γ_t ≥ t.

**Theorem U.** (EXT) implies that F is defined forever, its pointer tends to infinity, and machine
#1 never halts.

*Proof.* **(a) EXT for all J.** For J < K′, S(J) is tie-free by I-4 once F is defined through
τ(J−1), which holds inside HORIZON-3. For J ≥ K′ it is the hypothesis.

**(b) F is defined forever.** Induction over the steps of the maximal defined prefix. By PROOF_M
Corollary 3.5 only level fires and exit chains after type-a returns can fail S1; S2 never fails.
- *Level fire* at pointer ρ, J = v2(3s_0+4), s_0 = τ(ρ). For ρ ≤ N_B = 10^8: audited base V2. For
  ρ > N_B: STATE-CLOCK (PROOF_CLOCK §4, unconditional on the maximal defined prefix) gives
  s_0 ≤ ρP(ρ) < ρ(2ρ+1), so 2^J ≤ 3s_0+4 < 2^ρ and J < ρ = σ_0.
- *Exit chain t ≥ 1.* F is defined through τ(J−1) inclusive, since J−1 < ρ gives τ(J−1) < τ(ρ) = s_0. By (a) S(J) is tie-free;
  by PROOF_M Lemma 6.1 F's top-level small parts are α λ_u + β with S(J)'s pairs, so j_t = v2(β_{x_t})
  < v2(α_{x_t}) = J − Γ_t (Lemma T(1)). F's coefficient valuation is σ_t = ρ − Γ_t (PROOF_M Lemma
  3.2). As ρ > J, σ_t > j_t: S1 holds.
- *Termination.* S(J) ends at an even return after ≤ max(0, J−2) exit chains, so every epoch ends with
  P = ∅ and the pointer advances by ≥ 2. Between epochs only even steps at P = ∅ occur.
So every step is defined and i → ∞.

**(c) No halt.** As in Corollary H, now for every v: F is defined through X(v−1) by (b); S(v) is
tie-free by (a); EGX makes the endgame safe and terminating; E1–E4 exclude a halt. Induction over
singleton times. ∎

Neither (C2) nor an exit-length bound is used: the F margin follows from the J-margin because
ρ > J, and the J-margin is (EXT) itself. This is the reverse of the old direction: previously F
had to be controlled through SQRT-EXIT and the endgame separately; now the endgame statement
controls F.

## 6. Theorem L: a linear exit budget implies EXT [A]

**(LIN-EXIT)** For every J ≥ K′, every tie-free prefix of S(J) has at most L(J) := ⌊J/(3 l)⌋
exit chains, l := log2 J.

**Theorem L.** (LIN-EXIT) implies (EXT).

*Proof.* Strong induction on J; J < K′ is (a) of Theorem U. Fix J ≥ K′; "F defined through
τ(J−1)" is the antecedent of EXT(J), so assume it. (It also follows from EXT at all J′ < J:
every epoch reaching τ(J−1) has fire parameter J′ ≤ log2(3(J−1)²+4) < J, and Theorem U (b)
applies to that prefix.) Let t ≤ L(J)+1 and suppose
chains 1,…,t−1 of S(J) are tie-free. Using Lemma T(2) (1 ≤ β_x ≤ 6d_t − 1), (C1), ε(n) ≤ n and
Lemma C2-log at i = J−1 (its W-epoch has J_W ≤ log2(3J²+4) < J, tie-free by induction):
- d_t ≤ 1 + τ(J−1) + Σ_{t′=1}^{t−1}(1+τ(n_{t′})) ≤ 1 + (J−1)² + L(1 + (2l+4)²) ≤ 2J², by induction
  on t, because each j_{t′} ≤ log2(6d_{t′}) ≤ log2(12J²) < 2l+4;
- Γ_t ≤ (1 + ε(J−1)) + (t−1)·max(1+ε(n_{t′})) ≤ (4l + 3.2) + L·(2l + 4);
- v2(β_{x_t}) ≤ log2(6d_t) < 2l + 4.
A tie at chain t needs v2(β_{x_t}) ≥ J − Γ_t, i.e. J < 6l + 7.2 + L(2l+4) ≤ 2J/3 + 4J/(3l) + 6l + 7.2,
i.e. (J/3)(1 − 4/l) < 6l + 7.2. With J = 2^l the left side minus the right side is
f(l) = 2^l(l−4)/(3l) − 6l − 7.2; f(10) = 204.8 − 67.2 = 137.6 > 0, and f′(l) > 0 for l ≥ 10 because
the exponential term's derivative exceeds 2^l·ln2·0.2 > 6. So the tie condition is false for
l ≥ 10 (and J ≥ K′ has l astronomically large). So chain t is tie-free. If
S(J) had a chain L+1, the prefix through it would be tie-free with L+1 chains, contradicting
LIN-EXIT. Hence S(J) ends within L chains, all tie-free. ∎

[B] `verify_egx.py` C5 checks the two displayed inequalities with integer arithmetic at
J = 2^10, …, 2^4096 (using the stronger integer form J > 6l + 7 + L(2l+4) with integer l);
auditor 1 checked J = 2^10..2^199 exactly and 20,000 random J. The proof above is analytic.

**Unconditional by-product.** The induction did not use LIN-EXIT until its last sentence: given
EXT below J, the first ⌊J/(3 log2 J)⌋ + 1 exit chains of S(J), if they exist, are tie-free. So
EXT(J) fails only if S(J) runs more than J/(3 log2 J) chains.

## 7. Relation to the previous targets

- **EG-LEN ⇒ EXT.** EG-LEN at v (Σj < 3(v−1)/4 on every endgame prefix) with E5 (prefix form)
  gives S1 at every endgame chain provided D_cross = ε(v−1) < (v−1)/4 minus the candidate chain's
  own j_k (E5's sum includes j_k, EG-LEN covers only valid prefixes). By Lemma C2-log and strong
  induction (EXT below v) ε(v−1) = O(log v), and j_k ≤ log2(6d_k) = O(log v) by Lemma T(2) and
  (C1); the slack n/4 − ε(v−1) absorbs both. By EGX this is EXT(v). So EG-LEN with any V₀ ≤ K′
  alone implies non-halting; **SQRT-EXIT is no longer needed**.
- **EXT ⇒ SQRT-EXIT on actual fires.** A tie-free S(J) has r ≤ J−2, and an actual fire of
  parameter J sits at pointer ρ ≥ 2^J/O(J²) (PROOF_CLOCK §6.1), so r < √ρ.
- **Base gap.** PROBLEM_ENDGAME §5 needed endgame data for 4·10^6 < v ≤ 10^8. Corollary H covers
  every v < K′.
- **Endgame survey.** work_global_calendar_survey (accepted, Class B) computed S(J) for deep J
  (first exit parameter m ≤ 60000, J ≈ 2^m): by EGX these are endgames of E(w,J). The longest
  found there has r = 4 (m = 6131); all are tie-free with large margin. The accepted
  work_g2_obstruction has an actual epoch (p3, p2, 244875, 17, 5, 6, 1) with r = 6; by EGX the
  endgame of E(·, p3) has 6 chains, still far inside the budget.
- **Not claimed.** EXT for J ≥ K′ is open. It is a statement about F's crossing table at indices
  < J (the same arithmetic object as (NT), (EL_J), CORE2), so the difficulty identified in
  PROOF_EL §6 and PROOF_TIE2 §7 (unbounded nesting of fire copies) is unchanged. Theorem U removes
  bookkeeping hypotheses; it does not touch that core.

## 8. Reproduce

    python -B work_global_egx/verify_egx.py 30000     # ~4 s; writes checks.json

C3 imports `work_m/verify_m.py` read-only; everything else is self-contained.

## 9. Review record (2026-10-17)

Reviewers (Claude subagents, each with its own code; auditors did not read `verify_egx.py`):
adversary, auditor 1 (re-implementation of the numerics), auditor 2 (logic and import audit).
Full texts: `reviews/claude_egx_adversary.md`, `reviews/claude_egx_auditor1.md`,
`reviews/claude_egx_auditor2.md`.

- **Adversary: `2. with fixable gaps`.** EGX holds (essentially an identity); U and L follow
  without circularity. Findings: (1) Lemma C2-log false at t = 0, J_W = 1 (ε = 3 > 1; 21,730 of
  40,527 type-c crossings to 2·10^5); (2) the transfer of the tower imports to non-fire J was
  asserted, not shown; (3) (C2) source and "X(v−1) reached" missing in Corollary H; (4) r ≤ J−2
  fails at J = 1; (5) chain indexing off by one; for non-fire J the appeal to PROOF_M 2.2–2.3 should
  be "by definition"; (6) Theorem L persistence argument and C5 docstring; (7) mention the actual
  r = 6 epoch; V₀ ≤ K′. Verified: N = 300000 run, 0 mismatches (200,731 chains); integer top map
  vs prediction for 26,992 runs (v ≤ 12000); walk to 2·10^5: σ = ρ − Γ, min h = 1, r ≤ max(0, J−2).
- **Auditor 1: `2. with simple errors`.** Same C2-log counterexample (43,462 instances to 4·10^5,
  all (J_W, t, ε) = (1, 0, 3)); EGX proof no gap; Theorem L correct (tie condition impossible for
  J ≥ 327). Own code: EGX pair for pair for 3 ≤ v ≤ 400,000 (267,637 chains, 0 mismatches,
  final (2^v, 3ℓ) always); integer top map v ≤ 400 for 9 values of w up to 2^127+1; ~29,000
  perturbed (non-occurring) start states: identity is structural, endgame-unsafe ⇔ S-tie.
- **Auditor 2: `2. with simple errors`.** Imports are per-J statements about S(J) using only F
  at indices ≤ J−1; no circularity, no (C2)/SQRT-EXIT/EG-LEN in Theorem U. Findings: "through
  τ(J−1)" must be inclusive; (C1)/(C2) at J−1 and the reached step; Θ substitution for the
  automata; E5 needs the candidate's own j_k in §7; cosmetic label of type counts.
- **Patch (author):** all items applied: Lemma C2-log now max(3, 2J_W−1) with the t = 0 case;
  new Lemma TR (transfer, Θ_t := 2^Jλ_u + 3d_t + 1) plus the PROOF_SPECTRUM alternative route;
  I-3 now lists (C2), M2′ and the reached-crossing argument; inclusive τ(J−1); max(0, J−2);
  uniform chain numbering; "by definition" for S(J); analytic persistence in Theorem L and its
  unconditional by-product; §7 j_k term, V₀ ≤ K′, r = 6 epoch; data labels.
- **Targeted re-review (adversary): `1. closed in all states`.** All seven findings closed, Lemma TR sound
  (b/c copy identity algebraic; valuation steps under h_t ≥ 1), recount of the per-chain type labels
  reproduced; one arithmetic slip f(10) = 204.8 − 67.2 (was 409.6), fixed.

VERDICT: ACCEPTED (EGX, Corollary H, Lemma TR, Lemma C2-log as corrected, Theorems U and L).
