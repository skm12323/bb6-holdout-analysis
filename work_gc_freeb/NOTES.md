# FREE-B: localization of boundary gates (determined but not record-safe)

ZCode agent (R2), 2026-11-10. **Preliminary exploration; three-way review pending
(round-1 adversary/auditor findings patched — see the corrections block below).**
No EXT / non-halting claim; the accepted horizon (2^T4−2 top steps) is unchanged.
Tags: [A] proved here from accepted imports (proof given), [A-cond] under stated hypotheses,
[B] exact computation over a stated finite range (script named), [C] heuristic.
This note closes the FREE-B gap of work_claude_cycle in the *localization* sense fixed by
that note's review corrections (boundary gate = determined and not record-safe): every
boundary gate falls into one of three decidable branches. It does NOT close FREE-EXIT, G1,
CL2 or CL4 (see §7).

> **Review corrections (round 1, 2026-11-10; adversary + auditor 1; they override the
> body where they differ).** All items below are implemented in the note and the script
> as of this revision.
> 1. [MEDIUM] The old PART 1b check `P1b_nondet ... or True` was vacuous. Now PART 1b
>    asserts the full three-way engine equivalence per generic postgate start (j < 60,
>    m < 300): branch.explore's single zero-bit leaf is GATE ⟺ det_walk = GATE with the
>    identical word (7 cases), END ⟺ END (2,823 cases), CUT_BITS (a free step) ⟺ SPLIT
>    (9 cases) with the leaf's realized word matching my determined prefix step for step.
>    The split direction of FB-2 is thereby machine-checked against the accepted engine.
> 2. [MEDIUM] The old PART 8 count identity was true by construction. Now PART 8 asserts:
>    boundary == sum of by_branch == len(sweep_boundary); pairs_free decomposes as
>    pairs_free_nogen + pairs_free_worddiff with worddiff == 0 (any determined-word
>    mismatch between the engines fails P6_worddiff_none); every nogen pair satisfies
>    P6_splitprefix (my engine reproduces the leaf's realized word on the whole determined
>    prefix before the split); pairs_long == 0.
> 3. [MEDIUM] §6 item 1's sentence "the type-b class at m ≈ 1.1·10^12" was wrong — that
>    number is counterexample B (j = 42). Corrected statement (now proved, PART 7c): the
>    j = 24 type-b U_b-class (9τ ≡ −140 mod 2^22) is realized at the class labels
>    (realization machine-checked on the first 200 only — see item 13; first at
>    m = 1,044,747), but the class fixes τ mod 2^8, hence ω(m−1) = v2(3τ+4) = 7
>    throughout, and the landing chain 7 has X(6) even — no a-step at the landing — so the
>    two-step type-b family is EMPTY for j = 24 at every m. (The adversary's independent
>    search to m ≤ 1.89·10^12 found none as well.)
> 4. [LOW] FB-4's razor-edge claim "verified … including m = j and m = j+1 pairs" was an
>    EMPTY-SET verification: m = j two-step pairs do not exist (X(j−1) type a forces
>    E = 2k_j+1 odd, c₁ = 1, END — all 120 such census pairs), and the m = j+1 pairs
>    (120, all type b) all END. The m = j clause of FB-4(a) is unreachable; the razor
>    verification is carried by the seeded u-odd companions (§6 item 5).
> 5. [LOW] Decidability note completed with a termination argument: v2(B) = m+1−ell, so a
>    determined walk with ell ≥ m−3 can only read chains ≤ 3 and ENDs; a determined walk
>    from the post-gate state therefore terminates within m+3 steps. All analyze_pair
>    caps are now m+3 (a priori complete; LIMIT would signal an engine defect, and none
>    occurs), replacing the former 400/200/120/50 caps.
> 6. [LOW] Four precision fixes: (i) FB-2's parity-flip argument now fixes the other
>    variable at 0 explicitly; (ii) FB-4(b)'s value range is stated for determined steps;
>    (iii) §0.4's divisibility is flagged to be read with the u-parity clause (for a
>    determined type-a two-step boundary with m > j the condition is 2^(j−1) | S_a);
>    (iv) FB-0's converse is stated as a bijection from the conditional cylinder
>    {v2(y) = m} onto Z₂ × Z₂^× (not "unimodular"; measure statement corrected in
>    round-2 item 12).
> 7. [LOW] fb.py notes that branch.py's ZERO leaf (identically vanishing output form)
>    falls under its SPLIT status — both mean "not determined"; unreachable on post-gate
>    starts (the V-coefficient never vanishes).
> 8. [LOW] (auditor 1) §6 item 2's population is now stated exactly: 15,525 pairs with a
>    determined first landing and an odd a-crossing at c₁ (NO c₁ ≤ j−2 filter); 15,435 of
>    them have c₁ ≤ j−2; the 90 difference are type-b/c super-escape landings
>    c₁ = ω(m−1) ≥ j. The closed forms hold on both populations (all verified).
> 9. [LOW] (auditor 1) "U_c verified on every type-c two-step pair in the census range"
>    was VACUOUS — the census box contains zero type-c two-step pairs (the first odd
>    c-crossing with ω = 5 and an a-step at c₁ is m = 6133 > 5000; asserted as
>    P7c_census_vacuous). Non-vacuous verification added: PART 7b checks the U_c closed
>    form on the constructed pairs (m = 6133) × 8 gates j ∈ {24, 42, 61, 97, 152, 186,
>    239, 275}.
> 10. [LOW] (auditor 1) §6 item 1's "at every step of every walk (2948 checks)" now reads
>     "at every step of each walk that reaches a determined gate (2,948 steps over the
>     1,474 walks)"; P2_srep = exact integer replay of every 7th determined gate (210),
>     P6_srep = the same for every 97th determined sweep pair with m ≤ 5000 (65).
>
> **Review corrections (round 2, 2026-11-10; adversary).** All items below are
> implemented as of this revision; the full verification was re-run afterwards.
> 11. [LOW] The aggregate check P8_splitprefix_count was true by construction (each nogen
>     pair makes exactly one P6_splitprefix call); it is DELETED. The substantive content
>     is the per-pair P6_splitprefix condition (355,910 checks), which stays.
> 12. [LOW] FB-0's measure parenthetical was wrong: the conditional cylinder {v2(y) = m}
>     has Haar measure 2^−(m−j+1) in the incoming class (not "measure 2^(m−j+1)"), and it
>     maps bijectively onto Z₂ × Z₂^× (the target cylinder {u′ odd} has measure 1/2;
>     magnification 2^(m−j)). Only the qualitative bijection is used downstream.
> 13. [LOW] "realizes at every class label from m = 1,044,747 on" overstated the machine
>     range: the first 200 class labels are verified (all realized, all ω = 7); the
>     emptiness argument does not use realization beyond ω-constancy on the class plus
>     X(6) even. Wording fixed to "at each of the first 200 class labels".
> 14. [LOW] PART 7c's printed "first m" was a hardcoded constant; the script now reports
>     the first realized m from the search itself (and asserts it equals 1,044,747).
>
> **Net result:** the [A] statements (FB-0..FB-5, Theorem FREE-B) are unchanged — every
> review finding in both rounds was a data/wording/verification-coverage issue, not a
> mathematical one. The full verification was re-run after all fixes (see §8).

> **Round 3 (2026-11-14, independent Claude adversary; overrides the body and earlier rounds where they differ).**
> 1. [MEDIUM] FB-5 (α) must be read on the walk W, not on the generic tree: (α) := "W has a next gate G″ after G
>    and the W-path from G's output to G″'s output is not determined". A gate on another branch of the tree gives
>    no free gate in W; with the literal tree reading the "if" direction fails.
> 2. [MEDIUM] **The zero-sum cases are vacuous.** All calendar quantities are non-negative, so S_a >= 3, U_b >= 20,
>    k_j+1+k_m >= 1, and by MASS (0 < lambda′ <= 6tau+5) U_c >= 12k+6tau+12k_c1+19 > 0. Delete every "zero sum =
>    exact cancellation" clause and (β0). The j-bounds of (I)/(II) are unconditional, and FB-5 reads
>    "CL2 at B*(g) ⟺ no (α), no (γ)".
> 3. [MEDIUM] **"FREE-B gap closed" is withdrawn.** What is proved: FREE-B for **two-step** boundary gates (explicit
>    sums and unconditional j-bounds). Branch (III) is a definitional catch-all (boundary with a path of >= 2
>    steps, FB-3 restated): deep boundary gates are reduced to FB-3's divisibility and remain open (part of CL2).
>    No instance of (III) is known, and none is excluded.
> 4. [LOW] The trichotomy needs the zero-step case: G′ cannot be the a-step at chain m itself, since a determined
>    output is < v2(A) = j <= m. With that line it is exhaustive and exclusive.
> 5. [LOW] FB-5 is **[A-cond]** (C2-log needs the containing epoch tie-free in S(J_W); H1/H2 are hypotheses);
>    §0.5 "<=" vs §5 "<" to be read as "<". Constants are valid but loose (|U_c| <= 24mP(m)+24; a determined II-a
>    boundary needs 2^(j−1) | S_a).
> 6. [LOW] [B] scope: type c is thin (one tested m in the note; the adversary added 41 type-c determined gates,
>    j < 45, m < 1.5·10^6, none boundary; eps != 3 untested at a two-step gate). No type-c boundary instance exists.
>
> Confirmed by round 3 (hand re-derivation and an independent symbolic engine; 11.19M starts, 41,859 determined
> gates, all two-step, 0 boundary; random m up to 2^500): FB-0..FB-4, the u-parity knife, FB-3, the closed forms
> S_a/U_b/U_c, all j-bounds, B*(g), counterexamples A/B/B2. verify_freeb.py re-run by the coordinator: ALL PASS.

## 0. Summary

1. **Three-part decomposition [A] (Lemma FB-1).** In the generic post-gate state of a true
   NT gate G at odd-a chain j (k = k_j) with output m (Lemma PG, accepted):
   `Theta = 2^(j-2)+3(k+1) + 2^(j-1) X`, `x = 2^m (1+2V)`, X, V ranging over ALL of Z_2^2
   (every real walk through G lands in this cylinder; Lemma FB-0). Along any path with
   total loss ell from G's output, `x = C + A X + B V` with
   **v2(A) = j − ell + L_bc + 1** (A = 0 before the first a-step; A = 2^j exactly at it),
   **v2(B) = m + 1 − ell**, and C = u + β·2^m the X,V-free calendar part with
   v2(β 2^m) = m − ell. Here L_bc is the loss of the maximal b/c run right after the
   output (0 if X(m−1) is type a) — the same L_bc as in the accepted DR′.
2. **Determinacy criterion [A] (Lemma FB-2).** A step's chain is fixed for all (X,V) iff
   `v2(C) < min(v2(A), v2(B))` (min over nonzero coefficients), and then equals v2(C);
   otherwise the step splits. This is exactly the no-split rule of the accepted generic
   tree (work_claude_cycle/branch.py, `vc < vs`).
3. **Boundary = explicit output cancellation [A] (Lemma FB-3).** If G′ is determined by G,
   then `m′ = v2(C_final) < min(j−ell+L_bc+1, m+1−ell)`, so ΔR := m′+1+ell−j ≤ 1+L_bc
   (DR′ recovered), and
   **G′ is a boundary gate ⟺ 2^(j−ell) divides C_final**, with ΔR ∈ {1, …, 1+L_bc}.
   Since m ≥ j for every gate, the V-part never blocks: all content is the divisibility of
   the calendar sum C_final. (In particular a determined G′ is automatically record-safe
   when m < j−1 — but m ≥ j always, so the task's dichotomy "m ≥ j−1 or cancellation"
   degenerates: the first disjunct is automatic for gates and the entire content is the
   cancellation. The real trichotomy is by *where* the cancellation sits.)
4. **Theorem FREE-B (trichotomy) [A].** Every boundary gate G′ falls into exactly one of
   (I) first-landing escape (c₁ ≥ j−1): accepted FREE localizes j ≤ 3+log2(6mP(m)) ≤
   3+log2(6gP(g)) (m ≤ g inside a tie-free prefix of S(J) under the standing hypotheses of
   Theorem L′);
   (II) the two-step family (c₁ ≤ j−2, G′ = the gate at the first landing): explicit sums
   S_a = k_j+3+3k_m+2k_{c₁} (type a), U_b = 12k_j+12k_{c₁}+9τ_m+20 (type b),
   U_c = 12(k_j+τ_m+k_{c₁}+2) − λ′_c (type c) with boundary ⟺ 2^(j−2)|S_a resp.
   2^(j−2)|U_b, 2^(j−1−ε₁)|U_c — the type-a divisibility to be read with the u-parity
   clause of FB-4 (u = S_a/2^(j−2) odd splits; for a DETERMINED boundary with m > j the
   condition is 2^(j−1) | S_a); nonzero sum + CLOCK/MASS ⟹ j ≤ 2+log2(3mP(m)+3) (a),
   j ≤ 2+log2(21mP(m)+20) (b), j ≤ 1+ε₁+log2(30mP(m)+29) (c); zero sum = exact
   cancellation (decidable);
   (III) the deep family (path of ≥ 2 steps from m to G′'s input): boundary ⟺
   2^(j−ell) | C_final with C_final the iterated calendar sum (explicit recursion,
   decidable membership), with NO size-based exclusion available (the accumulated clock
   enters; CG lower-bounds clocks between gates, nothing accepted upper-bounds them).
   Membership in each branch is decidable from (j, m) and the calendar data along the
   determined path.
5. **FB-5 (CL2 reduction) [A].** Inside a tie-free prefix with gate outputs ≤ g and
   ε ≤ 2⌈log2(3g²+4)⌉ at the b/c crossings read (both hold in the L′ context, the latter
   by C2-log in the least-counterexample induction), CL2 with threshold
   B*(g) = 2+log2(30gP(g)+29)+2⌈log2(3g²+4)⌉ holds iff no gate at chain j > B*(g) has
   (α) a post-gate split whose branch tree reaches a further true NT gate (the
   later-escape / NZ-type cancellation v2(C_i) ≥ min variable valuation at depth ≥ 1),
   (β0) a two-step boundary with S_a = 0 resp. U_b = U_c = 0, or (γ) a deep boundary (III).
   The FREE-EXIT consumers thus reduce to: the first gate, gates at chains ≤ B*(g), and
   the explicit cancellation families (α)/(β0)/(γ).
6. **Data [B]** (verify_freeb.py, §6): counterexamples A (j=24, m=6,268,562, ΔR=1, branch
   II-a, 2^22 | C_final, S_a = 2^23) and B/B2 (j=42/78, ΔR=3, branch II-b, 2^40/2^76 |
   U_b with v2(U_b) = 43/79, m′ = j−1) verified exactly (B/B2 by exact mod-2^P replay; A
   additionally by a full big-integer replay); the DR′ bound is sharp (ΔR = 1+L_bc
   attained for L_bc = 0 and L_bc = 2). New constructed instances: type a j=61 (m =
   2,584,632,671,144,439,708) and j=97 (m ≈ 5.9·10^28), both ΔR=1, m′=j−2; type b j=78
   (m = 18,820,720,748,458,000,207,560) with ΔR=2. Census (j<400 odd-a, j ≤ m < 5000;
   sweep over all forced-gate starts j < 3000 at cylinder depth 3000): every determined
   gate pair satisfies all invariants; boundary instances in these small-m ranges: none
   (the congruence classes force m ≥ 6,268,562 already for j=24), consistent with the
   explicit-sum analysis.

## 1. Setting

Exact scalar pair-map walk on canonical calendar data (accepted: PROOF_EXT §2 / Lemma BR;
same rules as work_claude_cycle/cyc.py). State (q, Θ, x) at chain q reads X(q−1):
- a-step (τ(q−1) = 2k_q): x′ = 2Θ + 6k_q − x/2, Θ′ = Θ + 3 + 6k_q, loss 1;
- b/c-step: x′ = R_q x + λ′_q, Θ′ = Θ + 3 + 3τ(q−1), loss 1+ε(q−1), with v2(R_q) = −1−ε
  exactly (v2 c′_n = n − ε(n)), R_b = 3/4 exactly, λ′_b = 3τ+4, λ′_c = 3τ+4+λ_Y
  (MASS, accepted), 0 < λ′ ≤ 6τ+5.
Γ := cumulative loss; record R := chain + Γ. A **true NT gate** at odd-a chain q is an
a-step whose output valuation m = v2(x′) satisfies m ≥ q. CLOCK (accepted):
τ(n) ≤ nP(n), P(n) = 2⌈log2(6n²+5)⌉² + 1345.

Definitions (work_claude_cycle NOTES, review-corrections block): for consecutive gates G
(chain j, k = k_j, output m ≥ j) and G′ (output m′): **G′ determined by G** := every step
from G's output through G′'s output has its chain fixed by the X,V-free part (no split of
the generic tree); ell := loss from G's output to G′'s output; L_bc := loss of the maximal
b/c run immediately after G's output (0 if X(m−1) type a); **record-safe** := determined
and m′ < j−ell; **free** := every other gate; **boundary gate** := determined and
m′ ≥ j−ell, i.e. ΔR := m′+1+ell−j ≥ 1. Record-safe gates never raise the running maximum
(R_after ≤ R_in ≤ M); this bookkeeping (FREE-EXIT ⇒ EXT) is accepted and is not repeated
here.

## 2. The decomposition lemmas [A]

**Lemma FB-0 (post-gate cylinder).** After a true NT gate at chain j with output m, every
exact walk continues from (m, Θ, x) with Θ = c_Θ + 2^(j−1)X, x = 2^m(1+2V),
c_Θ = 2^(j−2)+3(k_j+1), for some X, V ∈ Z₂; conversely the conditional cylinder
{v2(y) = m} at the gate output has Haar measure 2^−(m−j+1) in the incoming class and maps
BIJECTIVELY onto Z₂ × Z₂^× ⊇ all realizable post-gate states (X free, u′ = x/2^m odd).
*Proof.* Θ_after = Θ_in+3+6k with Θ_in+3k = 2^(j−2)o, o odd (gate condition), so
Θ_after = 2^(j−2)o + 3(k+1) ≡ 2^(j−2)+3(k+1) (mod 2^(j−1)) — this is the accepted Lemma
PG. x_after = y with v2(y) = m ≥ j ≥ 1, so x = 2^m·odd = 2^m(1+2V). For the converse: at
the gate input write Θ_in = 2^(j−2)(1+2X)−3k, x_in = 2^j(1+2V_prev); the output
y = 2Θ_in+6k−x_in/2 = 2^j(X−V_prev); conditioning on v2(y) = m fixes X−V_prev
mod 2^(m−j+1), an event of Haar probability 2^−(m−j+1), and on that cylinder the map
(X, V_prev) ↦ (X, u′ = (X−V_prev)/2^(m−j)) is a bijection onto Z₂ × Z₂^× (affine
unimodular on Z₂², with the condition u′ odd carving out the target cylinder of measure
1/2; magnification factor 2^(m−j)), so (X, u′) — hence (X, V = (u′−1)/2) — realizes every
(X, odd) pair. Only the qualitative bijection is used in this note. ∎

**Lemma FB-1 (three-part decomposition).** Start from the post-gate state and let ell be
the cumulative loss. Write x = C + A·X + B·V and Θ = θ + 2^(j−1)X throughout. Then at all
times: (i) the X-coefficient of Θ is 2^(j−1); (ii) v2(B) = m+1−ell; (iii) A = 0 until the
first a-step, A = 2^j exactly at it, and v2(A) = j − (loss since the first a-step)
afterwards; in particular at any path end v2(A) = j−ell+L_bc+1; (iv) C = u + β·2^m with
v2(β) = −ell, i.e. v2(β·2^m) = m−ell.
*Proof.* Induction over steps. Θ only gains integer increments, giving (i). For x:
a-step: C′ = 2θ+6k_q − C/2, A′ = 2·2^(j−1) − A/2 = 2^j − A/2, B′ = −B/2, β′ = −β/2;
b/c-step: C′ = R_qC + λ′_q, A′ = R_qA, B′ = R_qB, β′ = R_qβ. (ii): v2(B) drops by exactly
1 at an a-step and by exactly 1+ε at a b/c step (v2(R_q) = −1−ε, accepted), starting at
m+1. (iii): A′ = 2^j at the first a-step (A = 0 before it); afterwards v2(A) ≤ j, and at a
later a-step the two terms of 2^j − A/2 have valuations j and v2(A)−1 ≤ j−1, so
v2(A′) = v2(A)−1; b/c steps drop it by 1+ε. Counting: at the first a-step the accumulated
loss is L_bc+1, so at the end v2(A) = j − (ell − L_bc − 1). (iv) is the same linear
recurrence as (ii) for β. ∎

**Lemma FB-2 (determinacy criterion).** A step with input form x = C + A·X + B·V
((X,V) ∈ Z₂² free, A or B possibly 0) has v2(x′) fixed for all (X,V) iff
v2(C) < min{v2(A) : A ≠ 0, v2(B) : B ≠ 0}, and then v2(x′) = v2(C). Otherwise the value
of v2(x′) depends on (X,V) (the generic tree splits). Here C = u + β·2^m is a single
2-adic constant with v2(C) = v2(u+β·2^m) computed exactly (when v2(u) = v2(β2^m) = t the
sum u/2^t + β·2^(m−t) is a small dyadic rational whose valuation is exact).
*Proof.* If v2(C) = t < s := min var-coefficient valuation, then x = 2^t(C/2^t +
(A/2^t)X + (B/2^t)V) with C/2^t odd and all other coefficients in 2Z₂: the bracket is odd
for all (X,V), so v2(x) = t. If v2(C) ≥ s: say the minimum s is attained by A (if only B
attains it, swap the roles of X and V in what follows; if both, use X). Fix V ≡ 0: the
bracket x/2^s = (C/2^s) + aX + b·0 with a = A/2^s odd has, as a function of X, opposite
parity for X ≡ 0 and X ≡ 1 (mod 2): v2(x) takes different values on the two cylinder
halves. C = 0 with a variable present: x = AX + BV is not fixed either (X ≡ 0 vs X ≡ 1
with V ≡ 0, when A ≠ 0; else V ≡ 0 vs V ≡ 1). This is precisely the `vc < vs` rule of
the accepted branch.py engine. ∎

**Lemma FB-3 (boundary = output cancellation; sharp DR′).** Let G′ be determined by G.
Then every step from G's output through G′'s output satisfies FB-2, in particular at the
output of G′:
    m′ = v2(C_final) < min(v2(A_final), v2(B_final)) = min(j−ell+L_bc+1, m+1−ell).
Hence m′ ≤ j−ell+L_bc, i.e. ΔR = m′+1+ell−j ≤ 1+L_bc (the accepted DR′), and
    **G′ is a boundary gate ⟺ 2^(j−ell) | C_final**, in which case
    j−ell ≤ v2(C_final) ≤ j−ell+L_bc, i.e. ΔR ∈ {1, …, 1+L_bc}.
*Proof.* m′ = v2(C_final) is FB-2 at the last step; the valuation formulas are FB-1.
Since m ≥ j (gate output), v2(B_final) = m+1−ell ≥ j+1−ell > j−ell, so the V-part never
blocks a boundary output; the X-part gives the upper end. ∎
*Remark.* m′ < v2(B_final) = m+1−ell also gives m′ ≤ m−ell: a determined G′ is
automatically record-safe when m < j−1. For gates m ≥ j always holds, so this dichotomy
is vacuous as a restriction — the entire content of "boundary" is the divisibility
2^(j−ell) | C_final, and the useful classification is by *where* the divisibility sits
(Theorem FREE-B). The two DR′ counterexamples of the work_claude_cycle review sit exactly
at the two ends: A has v2(C_final) = j−ell (ΔR = 1, L_bc = 0), B has v2(C_final) = j−1 =
j−ell+L_bc (ΔR = 3, L_bc = 2) — see §6.

## 3. Theorem FREE-B (trichotomy) [A]

**Theorem.** Let G be a true NT gate at odd-a chain j (k = k_j) with output m ≥ j and G′
a boundary gate determined by G; let c₁ be the first landing after G's output (determined,
c₁ = v2(C₁)). Then exactly one of the following holds, and membership in each is decidable
from (j, m) and the canonical calendar data along the determined path (which is itself a
computable function of (j, m) along as the path stays determined):

**(I) First-landing escape: c₁ ≥ j−1.** (For a type-a first step a determined landing
satisfies c₁ < min(v2(A₁), v2(B₁)) = j, so branch (I) means c₁ = j−1 exactly there; for
b/c first steps c₁ = ω(m−1) can exceed j−1 while staying below m−ε₁.) Then the accepted
Lemma FREE applies (its hypothesis "the first landing is not a determined landing below
j−1" holds): type a — 2^(j−2) | k_j + 1 + k_m; type b/c — ω(m−1) ≥ j−1 and
2^(j−1) ≤ λ′ ≤ 6τ(m−1)+5. If the relevant quantity is nonzero, CLOCK gives
j ≤ 3+log2(6mP(m)); inside a tie-free prefix of S(J) under the standing hypotheses of
Theorem L′ every chain is ≤ g = ⌊log2(12J²)⌋, so m ≤ g and j ≤ 3+log2(6gP(g)). (The zero
case k_j+1+k_m = 0 is an exact cancellation, decidable.)

**(II) Two-step family: c₁ ≤ j−2 and the path from m to G′'s input is the single step
m → c₁** (G′ is the gate at the first landing; ell = 2 for a type-a first step,
ell = 2+ε₁ for b/c; L_bc = 0 resp. 1+ε₁). Then FB-4 applies: the boundary condition is
the explicit divisibility of the calendar sums S_a / U_b / U_c (§4), and if the sum is
nonzero, CLOCK/MASS give j ≤ 2+log2(3mP(m)+3) (type a), j ≤ 2+log2(21mP(m)+20) (type b),
j ≤ 1+ε₁+log2(30mP(m)+29) (type c) — hence with m ≤ g:
    j ≤ 2+log2(3gP(g)+3)   (a),   j ≤ 2+log2(21gP(g)+20)   (b),
    j ≤ 1+ε₁+log2(30gP(g)+29)   (c)   with ε₁ < 2⌈log2(3g²+4)⌉ by C2-log in the
least-counterexample induction. The instances with S_a = 0 resp. U_b = 0, U_c = 0 are
exact cancellations (decidable; in the type-a case S_a = 0 gives the determined boundary
m′ = j−2 with ΔR = 1 exactly when m > j, while at m = j the quotient u = 0 is even and the
step splits). Note on constants: the single form j ≤ 3+log2(6gP(g)) is attained for
branch (I) and for type (a) of branch (II) (indeed j ≤ 2+log2(6gP(g)) there); types (b)
and (c) of branch (II) carry the constants above, all of the form
log2 g + 2·log2 log2 g + O(1).

**(III) Deep family: c₁ ≤ j−2 and the path from m to G′'s input has ≥ 2 steps.** The
boundary condition is 2^(j−ell) | C_final where C_final is the iterated calendar sum along
the determined path, computed by the explicit recursion
    C₀ = 2^m, θ₀ = c_Θ; at a step at chain q:  a: C ← 2θ+6k_q − C/2, θ ← θ+3+6k_q;
    b/c: C ← R_q·C + λ′_q, θ ← θ+3+3τ(q−1),
and C_final = u + β·2^m with v2(β2^m) = m−ell ≥ j−ell, so for m > j the condition is
2^(j−ell) | u (the pure calendar part; for m = j the sum u + β2^m is evaluated exactly).
Membership is decidable; no size-based exclusion is claimed: u involves the accumulated
clock Σ(1+τ) of the path, and no accepted result upper-bounds clocks between gates (CG
lower-bounds them). Excluding deep cancellations is precisely the CL2/NZ-type problem
(§5).

*Proof.* The three cases are exhaustive and mutually exclusive by construction (the value
of c₁ and the path length). (I): c₁ = v2(C₁) with C₁ = 2^(j−1)+6(k_j+1+k_m)−2^(m−1)
(type a) — for m ≥ j the last term is ≡ 0 mod 2^(j−1), so c₁ ≥ j−1 forces 2^(j−1) |
6(k_j+1+k_m), i.e. 2^(j−2) | k_j+1+k_m (FREE(a)); type b/c: c₁ = ω(m−1) (LAND) — FREE(b/c).
These are the accepted FREE conclusions; the CLOCK bounds are FREE's (nonzero case).
(II): Lemma FB-4 (§4). (III): Lemma FB-3 plus the recursion, which is the step rule
applied to the constant part; v2(β2^m) = m−ell ≥ j−ell makes the 2^m-part of C_final
automatically divisible by 2^(j−ell) when m ≥ j (equality m = j handled exactly). ∎

*Decidability note (with termination).* Along a determined path every chain equals v2 of
a computable constant, so the path, ell, L_bc, C_final and the branch are computable from
(j, m). Termination: v2(B) = m+1−ell at all times (FB-1), so once ell ≥ m−3 every further
determined chain is < v2(B) ≤ 4, i.e. ≤ 3, and the next step ends the walk; since ell
grows by at least 1 per step, a determined walk from the post-gate state terminates
within m+3 steps. The computation thus always ends at a split, a gate or END, and the
branch question only arises when a gate is reached. All three membership tests are
implemented in work_gc_freeb/fb.py (det_walk / fb4, caps m+3 — a priori complete) and
exercised exhaustively in the stated ranges [B].

## 4. Lemma FB-4: the two-step explicit forms [A]

**Lemma.** G at (j, k, m) with X(m−1) odd, determined first landing c₁ = v2(C₁) ≤ j−2, and
X(c₁−1) an odd a-crossing with half-time k_{c₁} (so the step at c₁ is an a-step; write
K = k_m, τ_m = τ(m−1), ε₁ = ε(m−1)). Then the output of the a-step at c₁ has the form
y′ = C_final + A_final·X + B_final·V with v2(A_final) = j−1 (type-a first step; the a-step
at c₁ is then the second a-step) resp. j (b/c first step; the a-step at c₁ is the first),
and v2(B_final) = m+1−ell (i.e. m−1 for a type-a first step, m−2 for type b, m−1−ε₁ for
type c), and

  (a)  C_final = 3·S_a + 2^(j−2) + 2^(m−2),      S_a = k + 3 + 3K + 2k_{c₁};
  (b)  C_final = 2^(j−1) − 3·2^(m−3) + U_b/2,    U_b = 12k + 12k_{c₁} + 9τ_m + 20;
  (c)  C_final = 2^(j−1) + 6(k+τ_m+k_{c₁}+2) − λ′_c/2 − R_c·2^(m−1),
       equivalently 2·C_final = 2^j + U_c − R_c·2^m,  U_c = 12(k+τ_m+k_{c₁}+2) − λ′_c.

Boundary equivalences (m ≥ j):
  (a) v2(C_final) ≥ j−2 ⟺ 2^(j−2) | S_a. If m > j: writing u = S_a/2^(j−2) (when
      2^(j−2) | S_a), the a-step at c₁ is determined with m′ = j−2 exactly when u is even
      (including S_a = 0) — then ΔR = 1 — and it splits when u is odd (then G′ is not
      determined; a free gate, CL2's business). For m = j the parities swap (u odd gives
      the determined boundary m′ = j−2; u even splits).
  (b) v2(C_final) ≥ j−3 ⟺ 2^(j−2) | U_b (the terms 2^j and 3·2^(m−2) of 2·C_final are
      ≡ 0 mod 2^(j−2) because m ≥ j). Then m′ = v2(2^j − 3·2^(m−2) + U_b) − 1, an
      explicit computable value; for a DETERMINED step it lies in {j−3, j−2, j−1}
      (larger values would collide with v2(A) = j and split); the extreme m′ = j−1
      (ΔR = 3, the sharp DR′ case) needs m ≥ j+2 and is attained by counterexample B.
  (c) v2(C_final) ≥ j−2−ε₁ ⟺ 2^(j−1−ε₁) | U_c (2^j and R_c·2^m, of valuations j and
      m−1−ε₁ ≥ j−1−ε₁, drop out).
Size bounds (CLOCK + MASS, q ≤ m, P monotone): |S_a| ≤ 3mP(m)+3; |U_b| ≤ 21mP(m)+20;
|U_c| ≤ 30mP(m)+29. Hence for a boundary instance with nonzero sum: 2^(j−2) ≤ |S_a| resp.
2^(j−2) ≤ |U_b|, 2^(j−1−ε₁) ≤ |U_c|, giving the j-bounds of Theorem FREE-B (II).

*Proof.* Two step computations from (c_Θ, 2^m). (The m = j clause of (a) is consistent
but unreachable in practice: an m = j type-a two-step pair would need X(m−1) = X(j−1)
type a, forcing E = k+1+k_m = 2k_j+1 odd and c₁ = 1, so the walk ends before any gate —
all 120 such census pairs do exactly that; the razor verification below is carried by the
seeded u-odd companions of §6 item 5.)
(a): C₁ = 2c_Θ + 6K − 2^(m−1); the a-step at c₁: C_final = 2(c_Θ+3+6K) + 6k_{c₁} − C₁/2
= c_Θ + 9K + 6k_{c₁} + 6 + 2^(m−2) = 3(k+3K+2k_{c₁}+3) + 2^(j−2) + 2^(m−2) (using
c_Θ = 2^(j−2)+3(k+1)). Division by 2^(j−2): C_final/2^(j−2) = 3u + 1 + 2^(m−j) with
u = S_a/2^(j−2); for m > j the last term is even, so the bracket is odd iff u is even —
m′ = j−2 iff u even; u odd makes the bracket even, m′ ≥ j−1 = v2(A_final), and the step
splits (FB-2). For m = j: C_final/2^(j−2) = 3u+2, odd iff u odd. The divisibility
equivalence: 2^(j−2) and 2^(m−2) are ≡ 0 mod 2^(j−2).
(b): C₁ = (3/4)2^m + λ′_b = 3·2^(m−2) + 3τ_m+4 (R_b = 3/4, MASS-b); C_final =
2(c_Θ+3+3τ_m) + 6k_{c₁} − C₁/2 = 2^(j−1) + 6(k+τ_m+k_{c₁}+2) − 3·2^(m−3) − (3τ_m+4)/2;
multiplying by 2 and collecting: 2C_final = 2^j + 12(k+τ_m+k_{c₁}+2) − 3·2^(m−2) −
(3τ_m+4) = 2^j − 3·2^(m−2) + (12k + 12k_{c₁} + 9τ_m + 20) = 2^j − 3·2^(m−2) + U_b.
(c): C₁ = R_c·2^m + λ′_c with v2(R_c 2^m) = m−1−ε₁; C_final = 2(c_Θ+3+3τ_m)+6k_{c₁} − C₁/2
= 2^(j−1) + 6(k+τ_m+k_{c₁}+2) − λ′_c/2 − R_c·2^(m−1), and 2C_final = 2^j + U_c − R_c·2^m.
All razor-edge parity statements are also verified by machine in the stated ranges [B]
(verify_freeb.py PART 2/3 over the census population, plus the seeded u-odd companions of
PART 7 — the m = j subcase is an empty set, see the note above). ∎

*Remark (relation to NEXT).* In the record-safe regime v2(S_a) < j−2 the output formula
reduces to the accepted NEXT output m′ = v2(k+3+3k_m+2k_c): the two-step family is the
boundary continuation of NEXT exactly at the threshold v2(S_a) ≥ j−2, with the parity of
S_a/2^(j−2) deciding determined (u even) vs split (u odd).

## 5. Proposition FB-5: the CL2 reduction [A]

**Proposition.** Fix g and a finite walk W on canonical data in which (H1) every true NT
gate output is ≤ g, and (H2) every b/c crossing read has ε < 2⌈log2(3g²+4)⌉. (Both hold
for a tie-free prefix of S(J) inside the least strict-EXT counterexample induction with
the standing hypotheses of Theorem L′: all chains ≤ g = ⌊log2(12J²)⌋ by Lemma T(2), and
ε ≤ 2log2(3i²+4)−1 at index i by C2-log.) Put
    B*(g) := 2 + log2(30 g P(g) + 29) + 2⌈log2(3g²+4)⌉.
Then every free gate of W other than the first gate of W is either
  (α) reached through a split of the post-gate tree of its predecessor gate G (the path
      from G's output to it is not determined; the first split is the explicit
      cancellation v2(C_i) ≥ min(v2(A_i), v2(B_i)) of the X-free part against the
      variable threshold — CL2's stated failure mode), or
  (β) a boundary gate of G, hence of type (I), (II) or (III) by Theorem FREE-B;
and no type-(I) instance and no type-(II) instance with nonzero explicit sum can occur at
a predecessor chain j > B*(g). Consequently, with "CL2 at threshold B*(g)" meaning "every
free gate of W after the first follows a gate at chain ≤ B*(g)":
    CL2 at B*(g) holds  ⟺  no gate G of W at chain j > B*(g) admits
      (α) a post-gate split whose branch tree reaches a further true NT gate,
      (β0) a two-step boundary with S_a = 0 resp. U_b = 0 or U_c = 0, or
      (γ) a deep boundary (III).
*Proof.* Let G″ be a free gate of W after the first, with predecessor G at chain j. If the
path from G's output to G″'s output is not determined, its first split, followed through
the branch that reaches G″, is an instance (α) at G. If it is determined, freeness means
G″ is a boundary gate, i.e. (β); by FREE-B it is of type (I), (II) or (III). At
j > B*(g) ≥ 3+log2(6gP(g)): type (I) contradicts its CLOCK/MASS bound with m ≤ g (H1);
type (II) with nonzero sum contradicts 2+log2(3gP(g)+3) ≤ 2+log2(21gP(g)+20) ≤
2+log2(30gP(g)+29) ≤ B*(g) (types a, b) and 1+ε₁+log2(30gP(g)+29) ≤ B*(g) (type c, using
ε₁ < 2⌈log2(3g²+4)⌉ from H2). So at j > B*(g) only (β0) and (γ) — and (α) — remain,
which proves the "only if" direction; the "if" direction is immediate since each listed
instance produces a free gate after G (for (α), the gate reached through the split; for
(β0)/(γ), the boundary gate itself). ∎

*Remarks.* (1) The first gate of W is free by definition; its chain is ≤ g (Theorem L′
standing hypotheses) and it consumes one unit of the FREE-EXIT budget; CL2 as in
work_claude_cycle §5 concerns the gates after it. (2) The obstruction set {(α), (β0), (γ)}
consists of explicit X-free calendar cancellations from the fully explicit PG/LAND start
state; this is the promised characterization "later escape ⟺ explicit cancellation
congruence" — it does not exclude them, and FB-5 does not close FREE-EXIT: nothing bounds
how often such cancellations occur (that is the CL2/NZ problem, and consecutive free
gates are the CL4 train problem, which this batch does not touch).

## 6. Data [B] (verify_freeb.py)

All starts are SYNTHETIC (free 2-adic cylinders on canonical Calendar(512) crossing
data); no claim about canonical reachability. Engine: fb.py (form walk with symbolic
2^m), cross-checked three ways: against the accepted cyc.walk by exact integer replays
with random lifts (PART 1/2/6 samples; every counterexample and seed), against the
accepted branch.py engine by word-identity on all determined sweep pairs AND on the whole
determined prefix of every split pair (item 4), by three-way status equivalence on generic
postgate starts (PART 1b), and against the hand-derived closed forms (item 2).
Full run after the round-2 patches: 546,301 checks, 0 failures (freeb_checks.json has
every count; last line ALL PASS, exit 0; 428 s).

1. **Invariants + census (postgate range).** Every odd-a j < 400 with j ≤ m < 5000 and
   X(m−1) odd (357,821 pairs; the remaining 217,823 of the 575,644 (j,m) pairs have
   X(m−1) even and end at once): the determined walk to the first gate/split/end (cap
   m+3, a priori complete — see the decidability note) gives 356,191 deterministic END,
   156 splits, 1,474 determined next gates — zero LIMIT. At every step of each walk that
   reaches a determined gate (2,948 steps over the 1,474 walks): v2(B) = m+1−ell, v2(A) =
   j−ell+L_bc+1 (or A = 0 before the first a-step); at every determined gate: m′ =
   v2(C_final) < min(v2(A), v2(B)), ΔR ≤ 1+L_bc (DR′), and boundary ⟺ 2^(j−ell) |
   C_final. Sampled exact integer replays: every 7th determined gate (P2_srep, 210).
   **Boundary instances in this range: none** — consistent with FB-4: for j = 24 the
   type-a class (k_m ≡ −(k_j+5)/3 mod 2^(j−1)) first occurs at m = 6,268,562 > 5000, and
   the type-b two-step family for j = 24 is empty at EVERY m (PART 7c: at each of the
   first 200 class labels — first at m = 1,044,747 — the U_b-class is realized with
   ω(m−1) = 7, which the class fixes for ALL its members, and X(6) is even, so the
   landing has no a-step; the adversary's independent search to m ≤ 1.89·10^12 agrees).
1b. **Extended scan.** j ∈ {24, 42}, m < 150,000 (186,442 odd pairs): 4,181 determined
   gates, all of them two-step (no gate at path depth ≥ 2 in this scan), 0 boundary; all
   invariants hold.
2. **Two-step closed forms.** 15,525 pairs with a determined first landing and an odd
   a-crossing at c₁ (gate or not; NO c₁ ≤ j−2 filter — 15,435 of them have c₁ ≤ j−2, the
   90 difference being type-b/c super-escape landings c₁ = ω(m−1) ≥ j): C_final equals
   the closed forms (a)/(b)/(c) exactly, and v2(C_final) equals the FB-4 predictions,
   including the razor-edge parities (u odd vs even) that occur in the range (the m = j
   subcase is an empty set; see FB-4).
3. **Counterexamples (exact).** A: j=24, m=6,268,562 (type a): word 24→m→5, gate at 5
   with output 22 = j−2; ell = 2, L_bc = 0, ΔR = 1, v2(A) = 23 = j−ell+L_bc+1,
   2^22 | C_final, S_a = 8,388,608 = 2^23 (u = 2 even). Verified by the form engine AND a
   full big-integer replay AND an exact mod-2^200 replay. B: j=42, m=1,095,510,131,453
   (type b): gate at 5, output 41 = j−1; ell = 3, L_bc = 2, ΔR = 3,
   U_b = 8,796,093,022,208, v2(U_b) = 43 ≥ 40. B2: j=78, m=526,980,180,956,824,005,813,092:
   gate at 5, output 77, ΔR = 3, v2(U_b) = 79. (B/B2 by exact mod-2^P integer replay,
   P = 200 ≫ all chains visited.) Both DR′ endpoints L_bc ∈ {0, 2} are attained.
4. **Sweep census.** All forced-gate starts G(j), j odd-a < 3000 (906 starts), branching
   to cylinder depth 3000 with the accepted branch.py engine — 3,072,713 leaves, the same
   total as the accepted sweep_3000_3000. 362,868 consecutive true-gate pairs in the
   resolved leaves: 6,958 are generically determined (my det_walk reproduces the leaf's
   word exactly, and all invariants of item 1 hold; every 97th such pair with m ≤ 5000
   additionally integer-replayed, P6_srep, 65), 355,910 are reached through a split (the
   (α) cases of FB-5) — for every one of them my engine reproduces the leaf's realized
   word on the entire determined prefix before the split position (P6_splitprefix,
   355,910 checks) — no engine word-disagreement and no LIMIT occurs (both would fail the
   run), and **no boundary instance occurs**.
5. **Seeded constructions (NEW instances, all replayed exactly mod 2^P).** Type a
   (k_j ≡ 9 mod 16; k_m ≡ −(k_j+5)/3 mod 2^(j−1)): j=24 → m=6,268,562 (counterexample A
   recovered by the congruence search at i=0), j=61 → m=2,584,632,671,144,439,708,
   j=97 → m=59,204,868,238,605,288,077,091,907,182; all: determined 5-gate, m′ = j−2,
   ΔR = 1, 2^(j−1) | S_a, CLOCK bound checked numerically. Razor companions (u odd, k_m =
   k_m(gate) ± 2^(j−2), v2(S_a) = j−2 exactly): for j = 24 (m = 15,671,400, k_m =
   6,990,502), j = 61 (m = 1,292,316,335,572,219,845) and j = 97 (m ≈ 1.48·10^29) the walk
   SPLITS at the gate step, demonstrated concretely by two exact mod-2^P replays in the
   same cylinder whose phase bits X₀ have opposite parity: both land identically at c₁ = 5
   and their gate-step outputs differ (one reads exactly v2(A) = j−1, the other ≥ j) —
   FB-4(a)'s u-odd clause. Type b (k_j ≡ 1 mod 16; 9τ_m ≡ −(12k_j+32) mod 2^(j−2)): j=42 →
   m=1,095,510,131,453 (counterexample B recovered at i=0; ΔR=3, m′=41), j=78 →
   m=18,820,720,748,458,000,207,560 (ΔR=2, m′=76 — the intermediate v2(U_b) = j−1 case).
   Type-c: the census box contains ZERO type-c two-step pairs (asserted:
   census typec_two_step = 0; the first odd c-crossing with ω = 5 and an a-step at c₁ is
   m = 6133 > 5000), so the earlier sentence "verified on every type-c pair in range" was
   vacuous; PART 7b verifies the U_c closed form on the constructed pairs
   (m = 6133) × 8 gates j ∈ {24, 42, 61, 97, 152, 186, 239, 275} instead.
6. **Branch-(I) data.** First-landing escapes occur only at small j in the census range:
   623 pairs (all with j ∈ {5, 8, 12}) have an escaping first landing c₁ ≥ j−1 by the
   accepted LAND formula. At every one of them the script re-verifies the FREE
   congruences (type a: v2(k_j+1+k_m) ≥ j−2; type b/c: ω(m−1) ≥ j−1 and
   2^(j−1) ≤ 6τ+5) and the CLOCK bound — all pass. Their outcomes: 467 deterministic END
   and 156 first-step splits (exactly the census's 156 splits — the split set consists
   precisely of the super-escapes c₁ ≥ j); NONE of them reaches a gate, so no boundary
   gate of branch (I) arises in range. Beyond small j the escape congruence
   2^(j−2) | k_j+1+k_m needs |k_j+1+k_m| ≥ 2^(j−2) > (m−1)P(m−1)/2 for m < 5000 once
   j ≥ 25; at j = 24 the only candidate label in range, k_m = 2^22−10, is not realized
   below m = 5000.

## 7. What is NOT claimed

- FREE-EXIT is not closed: FB-5 leaves the cancellation families (α)/(β0)/(γ) unexcluded,
  and their frequency is unbounded a priori. G1 is not closed; CL2 (exclusion of the
  cancellations) and CL4 (trains) remain open; this batch does not touch CL4.
- No new EXT range, no horizon change, no non-halting claim.
- The census claims are exactly over the stated ranges (j < 400 odd-a with j ≤ m < 5000;
  starts j < 3000 at depth 3000; determined-walk caps m+3, a priori complete by the
  ell ≥ m−3 termination argument), on canonical Calendar(512) data; boundary instances
  beyond those ranges are accessible only through the seeded constructions (§6 item 5).

## 8. Files and reproduction

Run from D:\math_cc with
`PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B work_gc_freeb/verify_freeb.py`
(full run, ASCII output, last line ALL PASS iff zero failures; writes
work_gc_freeb/freeb_checks.json). `--quick` shrinks the ranges (postgate 120×1500, sweep
400×400) for a fast audit pass. Libraries: fb.py (this note's engine; standard library
only), plus the accepted work_claude_cycle engine (cyc.py, branch.py) and the canonical
calendar oracle (work_global_calendar/calendar_oracle.py, certified kernels J ≤ 512).
