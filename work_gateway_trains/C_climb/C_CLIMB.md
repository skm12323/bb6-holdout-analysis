# C_CLIMB — the climb bound (S3) for general entries: Lemma CB through runs

**Review corrections (2026-10-24, reviews/gateway_trains_review_record.md; override the body)**
1. [MED] C6 mixes two meanings of sigma: PROOF_EXT_ROOTS' y−2−eps is the u-error valuation mu of a C entry at r=1, not the
   precision of the ancestral defect D_y. For r>=2 the relevant quantities are mu=y−1−toll and the Theorem-S precision
   H>=m+1−w. C6's conclusion holds only for r=1 C entries; for r>=2 it is replaced by the conditions m < y−1−toll (RB-toll) and the Theorem-S
   precision H >= m+1−w (PROOF_EXT_ROOTS bounds only the first step's eps, not the whole toll).
2. [LOW-MED] C4 uses D2 (|lambda'_W|<=9tau+9), which is only [B]; label C4 as [A-cond D2] (or cite an accepted lambda' bound).
   Extrapolated slack (r<=10^5, off-grid y) is >=10.947, so "-10" holds; "slack >=10.95" should read ">=10.94".
3. C4 applies to the FIRST gate only (y>=N0, |D_y|<=5); later gates have y<<N0 and |D_y|~2^m/3 (see RECORD_BUDGET correction 1).
4. [LOW] §9 canonical rigidity: the j1=17 rate 2^-5 is the single mod-32 condition v2(3k+theta)=4; j1=18,19 zero follows
   from the entry congruence. The 9 huge-y instances and 167 two-step runs use chosen representatives (D_y, u_y=1):
   label non-canonical (conclusions unaffected since w=-1, m<=7<j1+w).


Task C of work_gateway_trains (2026-10-24). External ZCode agent (课题 C).
Gate: `python -B work_gateway_trains/C_climb/climb_checks.py` → **exit 0, STATUS: PASS,
115,121 checks, 0 failures**, artifact `climb_checks.json`.

**No global EXT or non-halting claim. K_clock unchanged.** Tags: [A] proved here from the
listed imports with all hypotheses stated; [A-imp] accepted import; [A-cond] explicit
conditional; [B] finite exact computation, range stated; [C] heuristic. Synthetic states
(constructed ancestor defects D_y, u_y lifts, and synthetic step data) are marked
non-canonical. The six REFUTED claims listed in CONTEXT §2 are not used.

Imports used ([A-imp], with pointer):
* chain/pair formalism, affine normal form, b/c data (c'_W, λ'_W, σ, ω, ε, S1) —
  work_global_ext PROOF_EXT §2, work_landing_symbolic THEOREM.md §1–§2 (review-correction
  block at head overrides body);
* CLOCK: τ(n) ≤ n·P(n), P(n) = 2⌈log2(6n²+5)⌉²+1345;
* Lemma CB and its σ-packaging — work_claude_shift NOTES §3;
* Theorem E (j=5, k=1 gateway class map) — work_landing_symbolic THEOREM §2.5;
* the two certified gateway classes (10−2^m)/3, (26−2^m)/3 (5 ≤ m < 10^8) — work_r1r2 Thm 2.4;
* PROOF_EXT_ROOTS type-c (1+ε ≤ 4log2(J)+4 inside the least strict-EXT induction);
* canonical calendar Calendar(512) — work_global_calendar.

---

## 0. What this file proves

work_claude_shift Lemma CB bounds the catapult output m of a *bare tie entered directly
from the last big chain y* (entry letter A, B or C; "run length 1"): m = v2(Z),
Z = 2d_5+6+(3/2)Z_prev, Z_prev exact mod σ_y ∈ {y−2, y−3, y−2−ε}, hence m < G(y)+1,
G(x) = 2log2(x)+3. This file generalizes (S3) to **general entries**: a *run* of strong
descent a-steps and b/c steps between y and the bare tie. Summary of results:

1. **Theorem C1** (exact output formula): x'' = A''·u_y + Z_run, with Z_run an explicit
   affine function of the ancestor defect D_y (u_y-free), μ := v2(A'') ≥ r+4, and
   **m = v2(Z_run) whenever v2(Z_run) < μ** — this is (S3)'s affine form v2(β'') < J−Γ−1.
2. **Proposition C2**: no valuation push-up is possible anywhere *inside* the run (strict
   dominance at every step); the only equal-valuation pair in the segment y→5→m is the
   catapult itself, where it is forced by the tie condition θ ≡ 5 (mod 16). The O1-type
   two-term cancellation mechanism lives exactly there.
3. **Lemma C3**: the slope of Z_run in D_y never vanishes (no "identical-cancellation run").
4. **Theorem C4** (climb bound): |Z_run| ≤ B_run(y,r,s,B_D) explicit; with |D_y| ≤ B_D
   ≤ 5 and y ≥ N0 = 2·10^7: **m < G(y) + log2(3/2)·s + 2·log2(r+1) − 10**, where r = run
   length, s = #b/c steps (verified slack ≥ 10.98; crude r-form: m < G(y) + log2(6)·r − 10).
   In particular m < G(y)+1 whenever log2(3/2)·s + 2log2(r+1) ≤ 11 (e.g. r ≤ 30 at s = 0,
   r ≤ 13 at s = 4).
5. **Theorem C5** (cancellation = climb residue): for every level L ≥ 5, the set of
   ancestors with v2(Z_run) ≥ L is empty or a **single residue class mod 2^{L−w}**
   (w = v2(slope) ≤ 1); the run itself pins D_y to a single class mod 2^{j₁}; within it m
   is independent of the free high bits below level j₁+w and a single class per level
   beyond. Excluding the climb is a **source/phase condition** (on D_y, and on u_y only in
   the boundary case v2(Z_run) = μ), not a parameter cap.
6. **Corollary C6** (C-letter entries): same bounds for c-step entries; inside the least
   strict-EXT induction σ_y ≥ y−4log2(y)−5 certifies m and m < G(y)+O(1); outside it this
   is an explicit hypothesis.
7. r = 1 degenerates exactly to Lemma CB (identities Z_CB = Z_run − x_y resp.
   Z_CB = Z_run + 2u(2^y−c'_W); σ_A = y−2 = μ, σ_C = y−2−ε = μ, σ_B = y−3 conservative).
8. Canonical rigidity [B]: multi-step entries are calendar-rigid (two-step runs need
   k(y−1)+k(16) ≡ 15 mod 32; no tie-reaching class exists at any j₁ ∈ [7..19] except
   j₁ = 17 where the fraction is exactly 2^−5); 167 exact canonical two-step runs
   y ∈ [19,12000] and 9 exact canonical runs with y up to 2·10^7 all have m ∈ {5,…,12}.

---

## 1. Setting

Chain state (x, Θ), x = 2^j u (u odd); a-step (τ = 2k): x' = 2Θ+6k−x/2, Θ' = Θ+3+6k;
b/c-step: x' = c'_W u + λ'_W, j' = ω = v2(λ'_W), σ = v2(c'_W) = j−1−ε ≥ ω+1 (S1).
D := Θ − x; record R = j+Γ. G(x) := 2log2(x)+3. N0 = 2·10^7.

**Anchor at y (affine normal form).** x = A·U + β, Θ = 2^y·U + 3d + 1 with U = u_y,
A₀ = 2^y, β₀ = 0, d₀ = (D_y−1)/3 ∈ Z[1/3]. Along steps:

* a-step (k): A' = 2^{y+1} − A/2, β' = 6d+2+6k−β/2, d' = d+1+2k, so v2(A') = v2(A) − 1;
* b/c-step at parameter j: ratio = c'_W/2^j, A' = ratio·A, β' = ratio·β + λ'_W,
  d' = d+1+τ, so v2(A') = v2(A) − (1+ε).

**Run.** A *run of length r ≥ 1 from y* is a sequence of steps with parameters
y = j₀ > j₁ > … > j_r = 5, each an a-step with 1+v2(3k+θ_{i−1}) = j_i ≤ j_{i−1}−2
(strong descent; θ := 3d+1−β is the affine class) or a b/c step (landing j_i = ω_i, S1),
followed by the *catapult* (the k = 1 a-step at parameter 5, X(4) odd a, τ(4) = 2 [B]).
The run ends at the **bare tie**: θ_r ≡ 5 (mod 16) (equivalently v2(3+θ_r) = 3; the four
residues mod 64 are {5, 21, −11, −27}; the window-range bare ties are (5,5), (5,−11)).
Output m := v2(x''). "Run length 1" = Lemma CB's direct entry (A-type if the single step
is an a-step, B/C-type if b/c).

Everything below is [A] for arbitrary integer/calendar data satisfying the stated size
hypotheses; the canonical range is verified [B] in §8.

## 2. Lemma CB reproduced [A-imp + B]

Lemma CB (work_claude_shift NOTES §3): bare-tie entry from chain y ≥ N0 by an A/B/C
letter, next letter the catapult ⟹ m = v2(Z), Z = 2d₅+6+(3/2)Z_prev with Z_prev exact
mod σ_y = y−2 (A), y−3 (B), y−2−ε(y−1) (C), so 0 < Z < 2^{σ−1} and m < G(y)+1; the class
at m is (10−2^m)/3 or (26−2^m)/3.

Reproduction ([B], non-canonical ancestor lifts on canonical calendar):
* A-type: 2,380 exact instances over 111 parameters y ∈ [7,4000) with τ(y−1)/2 ≡ 6
  (mod 16) (smallest such parameter: 17) and 8 parameters near {10^5, 10^6, 10^7, 2·10^7};
  D_y ≡ 16−3k mod 32 lifted to five representatives (incl. −2 and 14), u_y ∈ {1,3,5,2^20+1}.
  All: landing at 5 with class ≡ 5 (mod 16); m = v2(Z_CB) = v2(Z_run) whenever < y−2;
  identity Z_CB = Z_run − x_y exact; reduced d₅ ∈ {5,−11} exact mod 2^7; on the 716
  instances with |D_y| ≤ 14: m < G(y)+1 (max m−G(y) = −5.17); v2(Z) stable under
  D_y → D_y + odd·2^{y−2} (the σ_A = y−2 stability).
* B/C-type: 2,016 instances over 168 canonical crossings with ω = 5 (all kind b, plus the
  c-crossing X(6132) at parameter 6133); D_y ≡ 7−Φ mod 16 lifted. All: landing checks;
  Z_prev = λ'_W packaging: m = v2(2D₅+6+(3/2)λ') whenever v2 < σ−1; identity
  2D₅+6+(3/2)λ' = Z_run + 2u(2^y−c'_W) (error term 2u(2^y−c'_W) of valuation σ+1);
  σ−1 = y−2−ε (so σ_B = y−3 is the conservative uniform bound, σ_C = y−2−ε exact).
  Zero u-dependent instances occurred (v2(Z_CB) ≥ σ−1 never hit in this pool).
* Output class: on all 1,350 checked instances D'' ≡ (15−D₅+2^m)/3 (mod 2^{m+1}) exact;
  on the 425 instances where the tie class is the constant 5 or −11 to all m+1 bits
  (Theorem E's m < H hypothesis): D'' ∈ {(10−2^m)/3, (26−2^m)/3} (mod 2^{m+1}).
  Remark (not an error in the accepted material): tie classes ≡ 5 (mod 16) with other
  high bits (e.g. 21, −27, 37 mod 64) give the shifted families (15−D₅+2^m)/3; the two
  certified r1r2 families are the b = 0, all-bits case.

## 3. Theorem C1 (exact output formula at a general entry) [A]

**Hypotheses.** (H0) y ≥ 7, x_y = 2^y u_y, u_y odd, D_y = Θ_y−x_y ∈ Z.
(H1) a run of r ≥ 1 steps from y as in §1. (H2) θ_r ≡ 5 (mod 16). (H3) the catapult.

**Definitions.** Run the anchor recursion of §1 along the run (r steps), then set
**Z_run := 6d_r + 8 − β_r/2** (= the catapult's β-update, k = 1) and
**μ := v2(A'') = y − 1 − #a-steps − Σ_{b/c}(1+ε_i)** (= a_r − 1, the catapult's
J−Γ−1).

**Conclusions.**
(i) x'' = A''·u_y + Z_run exactly; v2(A''·u_y) = μ; **μ ≥ r + 4**.
(ii) v2(Z_run) ≥ 5 and m ≥ 5 always (the tie forces v2(2(3+θ_r)) = 4 = v2((3/2)β_r), the
NT gate). **m = v2(Z_run) whenever v2(Z_run) < μ** (then m is independent of u_y);
if v2(Z_run) > μ then m = μ exactly; if v2(Z_run) = μ then m = μ + v2((A''/2^μ)u_y +
Z_run/2^μ) ≥ μ+1 is u_y-dependent (the O2 mechanism; see C5).
(iii) For 1 ≤ i ≤ r: v2(β_i) = j_i (parameters are β-determined along the whole run) and
a_i − j_i ≥ i, where a_i = v2(A_i).

*Proof.* (i) is the affine recursion (each step is affine in (x,Θ); the anchor has β₀ = 0,
θ₀ = D_y; A'' = 2^{y+1} − A_r/2, and v2(A'') = a_r−1 because a_r−1 < y+1). For (iii):
induction. Step 1: a-step ⟹ β₁ = 2(D_y+3k), v2 = j₁; b/c ⟹ β₁ = λ', v2 = ω. Step i ≥ 2:
a-step: β_i = 2(3k+θ_{i−1}) + (3/2)β_{i−1} with v2(2(3k+θ_{i−1})) = j_i ≤ j_{i−1}−2 <
j_{i−1}−1 = v2((3/2)β_{i−1}) (Prop C2); b/c: v2(ratio·β_{i−1}) = σ_i > ω_i. The gap
a_i − j_i increases by ≥ 1 per step from ≥ 1 at i = 1. For (ii): a_r ≥ j_r + r = 5 + r
forces v2(β_r) = 5 exactly (j_r = 5 = v2(x_r) = v2(A_r u + β_r) with v2(A_r) = a_r ≥ 6);
then β'' = 2(3+θ_r) + (3/2)β_r = 16·(odd + odd), so v2(Z_run) ≥ 5; and x'' = A''u + Z_run
with v2(A''u) = μ gives the case split. ∎

[Z.run.identity: 2,218 exact equalities x'' = A''·u + Z_run at y ≤ 2000; Z.run.m_eq:
5,762 instances all with v2(Z_run) < μ and m = v2(Z_run); zero exceptions.]

## 4. Proposition C2 (strict dominance; no internal cancellation) [A]

At every run a-step the two terms of β' have valuations j_i ≤ j_{i−1}−2 and j_{i−1}−1
(gap ≥ 1); at every b/c step, σ_i > ω_i (S1). Hence **no cancellation inside the run can
push v2(β) above the class-determined landing parameter**: each step's leading term
(6d+2+6k, resp. λ'_W — both of size O(y·P(y)), with v2 equal to the landing parameter)
strictly dominates, and the "high-order pollution" (the halved/scaled old β) stays ≥ 1
valuation above the current parameter at every chain (it is ≥ j_i+1 at chain i, ≥ j_i+2
after the next halving, etc.). The **only equal-valuation pair** in the segment y→5→m is
the catapult step, where the tie condition itself creates it (both terms valuation 4).
This is precisely where the O1 mechanism (two same-v2 dominant terms cancelling) can
appear; see C5.

[Z.run.v2beta: 8,855 per-step checks v2(β_i) = j_i, 0 failures.]

## 5. Lemma C3 (slope never vanishes; no identical-cancellation run) [A]

Track the D_y-free part: β_i = q_i·D_y + b_i, d_i = (D_y−1)/3 + N_i with
q₀ = b₀ = N₀ = 0 and

* a-step: q ← 2 − q/2, b ← 6N+6k − b/2, N ← N+1+2k;
* b/c-step: q ← ratio·q, b ← ratio·b + λ'_W, N ← N+1+τ.

Then **Z_run = S·D_y + Cst** with S := 2 − q_r/2, Cst := 6 + 6N_r − b_r/2.
Valuation structure: q_i = 2^v·(2-adic unit) with v ≤ 1, v = 1 only immediately after the
first a-step (q = 2); an a-step from v = 1 gives v = 0, from v = 0 gives v = −1, from
v ≤ −1 gives v−1; a b/c-step gives v − (1+ε). Consequently **S ≠ 0 always** (q_r = 4 is
unreachable: it would need v = 2), and w := v2(S) ≤ 1 with: w = 1 iff the run has no
a-step; w = 0 iff the run's only a-step is its last step; w ≤ −1 otherwise.

So there is **no run for which Z_run ≡ 0 identically** — the worst conceivable climb
driver (m = μ for every ancestor) does not exist. The exact zero Z_run = 0 happens only
for the single ancestor value D_y = −Cst/S (a rational point), and every climb beyond a
given level is a single residue class:

## 6. Theorem C4 (size bound and climb bound) [A; constants verified B]

**Hypotheses (data bounds).** (D1) |ratio_i| = c''_{W,i}/2^{1+ε_i} ≤ 3/2 (canonical:
c''_W ≤ 3·2^ε follows from head_ratio, tail_ratio ∈ [0,1]; verified on all 7,713
crossings used); (D2) |λ'_W| ≤ 9τ+9 (verified [B] on all used canonical crossings);
(D3) τ ≤ (j−1)P(j−1) (CLOCK). Let τ̃ := (y−1)P(y−1), B_D ≥ |D_y|, s = #b/c steps.

**Claim.** |Z_run| ≤ **B_run(y,r,s,B_D) := (2+2·(3/2)^s)·B_D + 6 + 6r(1+τ̃) +
(3/2)^s·r·(B_D + 11 + 12r·τ̃)**; hence, if Z_run ≠ 0 and v2(Z_run) < μ,
m = v2(Z_run) ≤ ⌊log2 B_run⌋.

*Proof sketch.* |q_r| ≤ 4·(3/2)^s (a-steps: |q| ↦ |2−q/2| ≤ 2+|q|/2; fixed point 4;
b/c: ×3/2). Unroll β's recursion: each step's constant (6d+2+6k resp. λ') is scaled by
≤ (3/2)^s and the old part is halved at each later a-step; |d_i| ≤ (B_D+2)/3 + r(1+τ̃);
Σ constants ≤ r·(2B_D + 21 + 24rτ̃); |Cst| ≤ 6+6r(1+τ̃) + (3/2)^s r(B_D+11+12rτ̃)/2·…;
collect. [Z.run.size: 5,952 instances, 0 failures; Z.run.m_le_size ✓.]

**Corollary (climb bound).** For y ≥ N0 = 2·10^7 and B_D ≤ 5:

  **m < G(y) + log2(3/2)·s + 2·log2(r+1) − 10.**

The slack G(y)+log2(3/2)s+2log2(r+1)−log2(B_run) is minimized on the grid
y ∈ {N0,10^8,10^10,10^12,2^50,2^100} × r ∈ {1..64} × s ∈ {0,⌊r/2⌋,r} at **10.98**
(at y = N0, r = 64, s = 0) and increases in y (log2 B_run ~ log y + 2log2log y, G ~ 2log y)
[Z.const.slack, B]. Crude r-only form: m < G(y) + log2(6)·r − 10. In particular
**m < G(y)+1 whenever log2(3/2)·s + 2log2(r+1) ≤ 11**: r ≤ 30 (s = 0), 24 (s = 1), 20
(s = 2), 16 (s = 3), 13 (s = 4) [r*-table with one unit of margin]. This is the Lemma CB
budget for all runs of moderate length; the per-b/c-step cost is log2(3/2) ≈ 0.585
(rank/ rational-step growth), the per-a-step cost is only the additive 2log2(r+1).

**Degeneration to Lemma CB (r = 1).** A-entry: Z_run = D_y + 9k_y + 12 and
Z_CB := 2d₅+6+(3/2)(2d_y+6k_y) (exact defects) equals **Z_run − x_y**; μ = y−2 = σ_A;
m = v2(Z_CB) = v2(Z_run) for v2 < y−2. B/C-entry: Z_run = 2D_y + 6τ + 12 − λ'/2 and
Z_CB := 2D₅+6+(3/2)λ'_W (Z_prev = λ'_W) equals **Z_run + 2u_y(2^y−c'_W)**; μ = σ−1,
equal to y−2−ε (σ_C exact, σ_B = y−3 conservative). [Z.run.deg.*: 2,380 + 2,016 exact
identity checks, 0 failures.] (Audit fix 2026-10-24: the original count double-added the
canonical c-crossing X(6132); deduplicated and rerun.)

## 7. Theorem C5 (cancellation = single residue class; frequency) [A + B]

**Characterization.** For L ≥ 5: {D_y ∈ Z : v2(Z_run) ≥ L} = {D_y : S·D_y ≡ −Cst
(mod 2^L)}. This set is: **empty** if v2(Cst) < w (then m = v2(Z_run) = v2(Cst) for every
ancestor — the run is unconditionally safe); otherwise a **single residue class mod
2^{L−w}**, w = v2(S) ≤ 1. The climb depth e = m−4 for v2(Z_run) < μ satisfies
e ≥ E ⟺ D_y ≡ δ_E (mod 2^{4+E−w}) with δ_E explicit. In the boundary case v2(Z_run) = μ,
m ≥ μ+1 needs, additionally, u_y in a single class mod 2^{L−μ} (the O2 family is exactly
this at the trivial anchor y = 5). *Excluding the climb is a source/phase condition on the
ancestor (D_y, and u_y only at the boundary) — not a parameter cap, and not a consequence
of any height/class bound (O2).*

**Canonical-run specialization (t-structure).** The run itself pins the ancestor:
realizing the run forces D_y ≡ δ₁ (mod 2^{j₁}) (δ₁ = 2^{j₁−1} − 3k₁), a **single residue
class** — the "dangerous class at the first a-chain is a single residue mod 2^{j₁−2}…"
statement of the task (here mod 2^{j₁}, one step coarser than the NT-exclusion level).
Within the run class, Z_run = Z₀ + 2^{j₁+w}·(unit)·t with t = (D_y−δ₁)/2^{j₁} free: **m is
t-independent below level j₁+w** (the climb depth is then a calendar-determined number
m₀ = v2(Z₀), |Z₀| ≤ B_run) and each level beyond j₁+w is a single t-class mod
2^{L−w−j₁}. [Z.run.huge.t_struct: verified on all 9 huge-y canonical runs over t < 48.]

**Frequency [B].** Sampling D_y uniformly (synthetic runs, 1358 runs of lengths 1..6,
512–256 samples each): P(e ≥ E) = 0.0082, 0.0040, 0.0020, 0.00097, 0.00051, 0.00021,
0.00013, 6e-5, 2e-5, 2e-5, 1e-5, 0 for E = 1..12 — geometric with ratio 1/2, matching
a geometric decay of ratio 1/2. (Per-run theory: at a solvable level L the hit set is a
single class mod 2^{L−w}, rate 2^{−(L−w)}; the aggregate table mixes solvable and empty
("never") runs and w ∈ {−1,0}, so no single closed rate is claimed.) The single-class
prediction matched the sampled hit set exactly, accumulated over every run and level
[Z.run.synth.residue, after audit fix].

## 8. Corollary C6 (C-letter entries) [A-cond]

If the run's entry step into the tie is a c-step (residual case (iii)), Theorems C1–C5
apply verbatim (nothing in them distinguishes the step kinds). The additional content is
*certification from ancestor precision*: m = v2(Z_run) is determined by D_y mod 2^{σ_y}
iff σ_y ≥ m+1−w. Inside the least strict-EXT counterexample induction, PROOF_EXT_ROOTS
type-c gives 1+ε ≤ 4log2(y)+4, hence **σ_y ≥ y − 4log2(y) − 5**; combined with C4's
m < G(y) + log2(3/2)s + 2log2(r+1) − 10 < y − 4log2(y) − 5 + w for y ≥ N0 (slack > 7·10^6
at y = N0), σ_y certifies m and **m < G(y) + O(1)** with O(1) = log2(3/2)s+2log2(r+1)−10.
Outside the induction this is the explicit hypothesis **(Hσ): σ_y ≥ m+1−w** (for B-entries
σ_B = y−3 is the u-free uniform version; for C-entries σ_C = y−2−ε).
[Z.centry.*: 10 exact instances at the canonical c-crossing X(6132) (parameter 6133,
τ = 5471, ω = 5, σ = 6129, ε = 3, σ_C = 6128): 1+ε = 4 ≤ 4log2(6133)+4 = 51.4 ✓,
σ_C = 6128 ≥ 6133−4log2(6133)−5 = 6081.6 ✓, cert-fit ✓, m = v2(Z_run) ✓.]

## 9. Canonical rigidity and real instances [B]

* **Entry parameters.** A tie can be entered only by an a-step with v2(3k+θ) = 4 (needs
  τ(j−1)/2 ≡ 6 mod 16; smallest parameter 17: 17, 54, 90, 125, 161, 198, …) or a b/c step
  with ω = 5 (smallest parameter 65; all ω = 5 crossings in [7,12000] are kind b, plus the
  single c-crossing X(6132)). Hence **no tie-reaching class exists at j₁ ∈ [7..16]**
  (excluded by these entry necessary conditions; j₁ ∈ {17,18,19} additionally by full
enumeration), i.e. every multi-step run has j₁ ≥ 17.
* **TIE_REACH statistics.** At j₁ = 17: exactly 8,192 = 2^13 of 2^18 classes reach the
  bare tie (fraction exactly 2^−5 — the single residue condition θ ≡ 2^4−3k(16) mod 32;
  k(16) = 6); at j₁ = 18 and 19: **0** (full enumeration); at j₁ ∈ [20..40]: 0 of 4,000
  sampled each. The dangerous/tie-reaching set is low-dimensional (2^{−t} type) at every
  scale examined.
* **Two-step calendar constraint.** A length-2 run y → 17 → 5 requires
  **k(y−1) + k(16) ≡ 15 (mod 32)**; all 167 canonical hits satisfy it (independent
  verification of the TRAIN-type rigidity; the Astra train identities themselves remain
  unreviewed and are not used here).
* **Systematic scan.** y ∈ [19,12000] with odd-a crossings (3,627 of them) × j₁ ∈ [17..40]:
  167 realizable runs, **all at j₁ = 17, all of length exactly 2**; each verified by an
  exact integer walk from the pinned class (D_y = symmetric representative of δ₁ mod
  2^18, |D_y| ∈ [49573, 65509], u_y = 1): parameters follow, m = v2(Z_run), |Z_run| ≤
  B_run. Output m distribution: {5: 84, 6: 42, 7: 21, 8: 10, 9: 5, 10: 3, 11: 1, 12: 1}
  — geometric decay.
* **Huge-y canonical runs.** 9 exact instances (big-integer walks, x = 2^y):
  y ∈ {99987, 100023, 999977, 1000013, 9999974, 10000010, 19999961, 19999997, 20000034},
  j₁ ∈ {17, 54}, r = 2, s = 0, m ∈ {5,6,7}, always m = v2(Z_run) < μ ≈ y−3. For the
  j₁ = 54 instances |D_y| ≈ 9.0·10^15 ≈ 2^53 (the pinned class mod 2^55) yet m ≤ 7: the
  generic valuation of the ~2^53-sized Z₀ is tiny; the climb is the residue event, not the
  default. [Z.run.huge.*: 9/9 realize + t-structure, 0 failures.]
* **Replay of accepted walks.** The 36 bad-class representative walks plus the window
  grid (j ∈ [5..60], δ ∈ [−12..15]): 6 tie visits, all with the Z-formula verified
  (m = v2(Z_run) < μ). 5 of the 36 walks hit x'' = 0 at the catapult — the A3 exact-zero
  virtual resonance, exactly at the negative-residue representatives (5,−27), (8,−198),
  (12,−3084), (14,−12303), (17,−98322); m is undefined there (excluded by (S2*)/zero
  handling; consistent with C1 only via Z_run = −A''u_y, the same residue structure).
* **B-entry multi-step runs:** no canonical b/c crossing with ω ≥ 17 exists in
  [9,12000], so canonical B-entry *runs* (as opposed to direct ω = 5 entries) have no
  instance in range; coverage of r ≥ 1 with b/c steps inside is synthetic
  (non-canonical data; 1358 runs, lengths 1..6, all identities exact).
* e-histogram over all 5,762 run instances: max e = 14 (m = 18, an A-entry with
  |D_y| ≈ 3.2·10^7 lift — consistent with m ≤ log2|D_y| + O(1)); canonical instances:
  max m = 12.

## 10. Relation to the obstacles and conditions

* **O2** (no h-only record bound): consistent — C4's bound uses (y, r, s, |D_y|), i.e.
  ancestor *size* and run shape, not the phase class. The O2 family itself is the
  boundary case v2(Z_run) = μ (u_y-residue) at the trivial anchor.
* **O1** (two same-v2 terms cancelling): the mechanism is the same, but here the
  equal-valuation pair at the catapult is *forced* by the tie condition rather than
  arising from a rank-r numerator. The exclusion in both cases is a single residue class
  on the source data: O1's (SC) 3^r ≢ −A^{−1} (mod 2^{σ−5}) ↔ C5's S·D_y ≢ −Cst
  (mod 2^{μ+1}). The frequency statements are the same shape (2^{−t}).
* **(S3)** gateway output vs precision: the affine form v2(β'') < J−Γ−1 at the tie is
  exactly v2(Z_run) < μ. Theorem C4 proves it with margin
  μ − log2 B_run ≥ (y−1−#a−Σε) − (G(y)+0.585s+2log2(r+1)−10) > 0 for every run with
  #a + Σε ≤ y−G(y)−0.585s−2log2(r+1)+9 — all runs of moderate length; longer runs have
  μ ≤ log2 B_run, where m = μ (v2(Z_run) > μ) is *also* within budget, and only the
  boundary v2(Z_run) = μ (u-dependent) plus the residue class of C5 remain.
* **Window/gateway certificates** apply after m exactly as in Lemma CB (class families of
  §2, r1r2 certification for m < 10^8), unchanged by the run.

## 11. Hypothesis ledger (every condition, classified)

| # | Condition | Content | Class | Status |
|---|---|---|---|---|
| H0–H3 | run + tie + catapult as in §1 | structural | — | [A] |
| D1 | c''_W ≤ 3·2^ε (⇒ ratio ≤ 3/2) | calendar arithmetic | source/data | [A] from calendar structure; verified 7,713 crossings [B] |
| D2 | |λ'_W| ≤ 9τ+9 | calendar arithmetic | source/data | [B] on used range |
| D3 | τ ≤ (j−1)P(j−1) | CLOCK | [A-imp] | verified [B] |
| D4 | Z_run ≠ 0 and v2(Z_run) < μ | the (S3)-affine condition | source/phase (single residue + rational point; C5) | excluded set characterized [A]; not provably avoidable |
| D5 | \|D_y\| ≤ B_D | ancestor defect size | source (Theorem L: \|d_y\| ≤ 5) | hypothesis of the G(y)-form |
| Hσ | σ_y ≥ m+1−w | ancestor precision certifies m | source/precision | [A-cond]; automatic inside least strict-EXT induction for y ≥ N0 (C6) |
| (Hσ-C) | 1+ε ≤ 4log2(y)+4 | PROOF_EXT_ROOTS type-c | induction-scoped | [A-imp] inside induction; hypothesis outside |

Not used anywhere: parameter caps (CAL-C, R1, H3), fixed windows, the six REFUTED claims.

## 12. Honesty: remaining gaps

1. The G(y)-form of the climb bound needs the ancestor defect bounded (D5). Without it
   the honest bound is m ≤ ⌊log2 B_run(y,r,s,|D_y|)⌋; canonical-realizable runs pin
   |D_y| ~ 2^{j₁} (e.g. 2^53 at j₁ = 54), giving m ≤ j₁ + 0.585s + O(log r) — a bound in
   terms of the first landing parameter, still far below y, but not G(y).
2. The residue class of C5 is nonempty in general (synthetic hits occur at every level,
   at the expected 2^{−E} rate). Excluding it in real walks is a source/phase input of
   the same kind as (SC) for O1; no structural avoidance is proved here.
3. The boundary case v2(Z_run) = μ (u_y-dependent climb, the O2 mechanism) is
   characterized (single (D_y,u_y)-class per level) but not excluded.
4. Certification of m needs σ_y ≥ m+1−w; w ≤ −1 for most runs with ≥ 2 a-steps, and can
   be very negative for b/c-heavy runs — then the required ancestor precision grows; the
   C6 packaging covers it for y ≥ N0 with the C4 budget, but the fit is an inequality to
   be checked per use.
5. Canonical multi-step runs of length ≥ 3 were not found (TIE_REACH rigidity; §9).
   Length ≥ 3 formula coverage is synthetic-data only (non-canonical), plus the [A]
   identities which are data-uniform.
6. No canonical B-entry *runs* (b/c step from y into the run) exist in the scanned range
   (ω ≥ 17 absent below 12000); the ω = 5 direct entries are covered.
7. 5 of the 36 representative walks end in x'' = 0 at the catapult (A3 zero); m is
   undefined there and those walks are outside the run theorem's scope (Z_run = −A''u_y
   residue structure only).

## 13. Files and reproduction

```
python -B work_gateway_trains/C_climb/climb_checks.py     # -> climb_checks.json, exit 0
```

Blocks: Z.CB.A (2,380), Z.CB.BC (2,016), Z.CB.class/class.families (1,350/425),
Z.run.deg (4,396 identities), Z.run.synth (1,358 runs, lengths 1–6, residue+frequency),
Z.run.canon (167 exact canonical runs + TIE_REACH statistics), Z.run.huge (9 exact runs,
y ≤ 2·10^7), Z.replay (6 tie visits, 5 zero-walks counted), Z.centry (10), Z.const
(slack grid), Z.data (7,713 crossings), shared Z.run.* (5,952 instances). Total 115,121
checks, 0 failures, 17.7 s. Only files in work_gateway_trains/C_climb/ were written; no
other directory modified; no git operations.
