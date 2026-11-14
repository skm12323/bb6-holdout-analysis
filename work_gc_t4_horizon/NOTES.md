# Theorem H-T4: machine-level transfer of the EXT(<T4) horizon

攻坚·R1 (ZCode GLM-4.6 subagent), 2026-11-09. **Pending three-way review.** Machine #1
`1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Tags: [A] proof from the listed accepted
imports; [B] exhaustive exact computation over the stated finite range (script named,
range stated); no [C] content. **No claim beyond J < T4 and no claim about T5, G1
(FREE-B/CL2/CL4) or global non-halting.** Until this note passes three-way review, the
repository's accepted machine-level horizon remains `2^K_clock − 2` (work_claude_residual
review-correction item 7, NOTES.md:55-59; reviews/claude_residual_review_record.md:29-31).

> **Review corrections (round 1, 2026-11-10; adversary + 2 blind auditors; this block
> overrides the body below where they differ).**
> 1. [MEDIUM] The [B] verification of Lemma ORD used a wrong K-series constant in the
>    three UPPER bounds: 499,497 instead of 499,997 (script lines :158/:162/:173 of the
>    first version and NOTES §2's printed upper bounds), while the definition and all
>    lower bounds used the correct series. With the typo, the passing checks
>    ('K_prime<T3', 'K_clock<T4', 'K_prime<=K_clock') did not cover the repository's
>    actual constants. Fixed: all upper tops now 499,997 (lower tops 499,996/499,996/
>    499,495 and the slack asserts were re-verified correct by the auditors and are
>    unchanged); part (b) re-run ALL PASS on the corrected series with the same ladder
>    and counts. The eight orderings themselves were re-derived independently by all
>    three reviewers on the correct series and hold with huge exact slack.
> 2. [LOW] The HINQ step-slack equivalence was misquoted as 3H²−12H+14 > 0; the correct
>    equivalent of 6H−3 < L(H) is **3H²−12H+10 > 0** (discriminant 24, roots 2±√6/3),
>    true for every integer H ≥ 3 (minimum 1 at H = 3; H = 2 fails the slack, since
>    6H−3 = 9 > 7 = L(2)). HINQ starts at H = 16, so the induction step is valid at
>    every stage; §1 and the script are corrected (the direct range checks
>    6H−3 < L(H), H = 16..4096, were always correct).
> 3. [LOW] H = T4 is irrational, so the integer-H statement needs the one-line real
>    extension now in §1: 3·T4² = 3·2^(T3−3) < 2^(T3+2) < 2^T4 via (T3+2)² < 2^(T3−3)
>    (T3 ≥ 16, checked exactly 16..4096 in (a); T3 > 2^64 by Lemma ORD), whence
>    3(T4−1)²+4 < 3T4² < 2^T4 and the derived inequalities a fortiori.
> 4. [LOW] §3's wording on the (5,5) landing ("absorbed by Theorem RA") echoed the
>    withdrawn AB′ absorption of residual §5.4. Replaced by the residual
>    review-correction item 1 net argument: (5,5) occurs only with X(J−1) of type a,
>    where Theorem RA gives EXT(J) outright; with X(J−1) of type b/c it is unreachable.
> 5. [LOW] Lemma EXT-T4 (and DATA-T4) were stated for J ≥ 2, but J = 1 fires exist in
>    the millions and I-4's accepted base is "every J < K′" (all J, including 1).
>    Both lemmas are now stated for J ≥ 1; the J = 1 case is the all-J base (S(1)
>    closes at once with an even head, r = 0 — confirmed by every J = 1 epoch in §6(c)).
> 6. [LOW] Timings/throughput figures updated to the latest runs; the shipped
>    `t4_horizon_checks.json` is from the final default-budget run (its `c_total_s`
>    field); `extended_run_900s.log` records the 900 s probe re-run on the corrected
>    script (600.2 s, ladder {20,22,24,26,28}, same per-rung counts).
>    `fire_Js` entries in the json are `[J, [fire_count, min_margin_rho_minus_J]]`.
>
> Confirmed unchanged by the review: the proofs of Lemma EXT-T4 (composition and
> non-circularity), Lemma DATA-T4, Theorem H-T4 (i)/(ii), the off-by-one checklist,
> parts (a)/(c) of the verification, and the conclusion.
>
> **Round 2 (2026-11-10, targeted re-review, adversary).** [LOW] Pre-existing typo,
> present already in the round-1 version: the script's docstring usage line said
> `[total_budget_seconds=540]` while `main` defaults to 480.0 and NOTES §6/§8 say 480.
> Fixed to `[total_budget_seconds=480]`. The budget parameter only caps the adaptive
> ladder's wall time; it affects no assertion, so no re-run was required (per the
> re-review) and the shipped `t4_horizon_checks.json` (final default-budget run,
> 150.7 s, ladder {20,22,24,26}) remains the record of the last full run.

> **Round 3 (2026-11-14, independent Claude adversary; reviews/gc_t4_horizon_review_record.md addendum; overrides
> the body and the earlier rounds where they differ).**
> 1. [MEDIUM] **Tags.** Theorem H-T4 and Lemma EXT-T4 are **[A + imported A+B]**, not [A]. On [K_clock, T4) they
>    rest on Theorem T4, which is [A+B]: the level computation of work_claude_residual (zero margin: widening any
>    drift range by 1 creates an uncertified entry), the window certificate to 2·10^7 and the gateway certificate
>    5 <= m < 10^8; levels C/D rest on a hand case split with no real data. Ranges 1–2 also import [B] (V4, the
>    level-4 certificate), as Corollary H does.
> 2. [MEDIUM/LOW] **Non-integer H.** "T4 is irrational" is unproved and is not needed; delete it everywhere. The
>    steps "v <= T4−1", "J <= T4−1 so (J−1)² <= (T4−2)²" and "(v−1)²+1 <= (T4−2)²+1" are false for non-integer H.
>    Correct argument, valid whether or not T4 is an integer: for an integer v < T4, v−1 < T4−1, so
>    3((v−1)²+1)+4 < 3(T4−1)²+7 = 3T4²−6T4+10 < 3T4² < 2^T4 (T4 > 2). Likewise tau(J−1) <= (J−1)² < (T4−1)² and
>    3(T4−1)²+4 < 3T4² < 2^T4. This is the only place where Corollary H-CLOCK used a property specific to K_clock
>    (integrality). The conclusions are unchanged.
> 3. [LOW] The [B] ladder walked one F-step too few: for even H0, M = (2^H0−4)/3 and claim (i) covers steps
>    0..M−1, but the script used s* = (2^H0−5)//3 = M−1 and walked 0..M−2. Fixed to s* = (2^H0−2)//3 = M; re-run.
> 4. [LOW] **Scope of the [B] ladder.** All fire labels J and singleton v are <= 27, inside range 1 of Lemma
>    EXT-T4. The ladder gives no evidence about [K′, T4), the ORD-based composition, or item 2. Nothing [B] is used
>    as [A] in the proof.
> 5. [LOW] **Non-circularity, stated uniformly.** Every upstream appeal to "EXT below J" (work_claude_shift Lemma
>    CB at C entries; work_claude_shifted §5 c-gateway via C2-log; work_deep §4 source epochs) is at the label Q
>    of a real epoch fired at time <= tau(J−1). So 2^Q <= 3tau(J−1)+4 <= 3(J−1)²+4 and Q < G(J−1) < T3 < K_clock,
>    and its antecedent "F defined through tau(Q−1)" holds because the epoch is real. Later chain parameters
>    j_t < G(J) < T3 as well. No appeal lands in [K_clock, J).
> 6. [LOW] §2 and script comments quote lower bounds with 499496 where the code uses 499996 (both true).
>
> Confirmed by round 3: the induction order (F through tau(J−1) is supplied before S(J)'s tie-freeness is used);
> range hypotheses (Theorem S's cutoff K′ only in range 2; no substitution of K_clock into Theorem S); Lemma ORD
> re-derived by hand; HINQ; all off-by-ones.

## 0. Result

**Theorem H-T4 [A].** With H := T4 (tower below): **(i)** F is defined at every step s
with 3s+4 < 2^T4 (i.e. for all s < (2^T4−4)/3); **(ii)** machine #1 halts at no top-level
step n with n+2 < 2^T4 — the first 2^T4−2 top steps, in the horizon convention of
Corollary H'' (work_global_ext/PROOF_EXT.md:149-153) and Corollary H-CLOCK
(work_global_clock_horizon/PROOF_CLOCK_HORIZON.md:141-144). (T4 is irrational; "first
2^T4−2 top steps" is read as the set {n : n+2 < 2^T4}, exactly the H''/H-CLOCK reading.)

This is the missing transfer named by work_claude_residual's review-correction item 7
("The machine-level horizon ... is *expected* to follow by the Corollary H-CLOCK pattern
with H = T4; this is not separately verified") — supplied here as Theorem H-T4, with the
two bookkeeping lemmas that H-CLOCK left implicit made explicit (Lemma EXT-T4: the
globalisation of the tie-free range; Lemma DATA-T4: the data-locality/prefix-closure
statement), and with the transfer pattern itself validated mechanically for the first
time at small scales (§6(c): default H0 in {20,22,24,26} — 6.7·10^7 top steps; extended
budget reaches H0 = 28, 2.7·10^8 top steps).

New statements: Lemma EXT-T4 [A], Lemma DATA-T4 [A], Theorem H-T4 [A], Lemma ORD
[tower comparisons, exact, (b) of the script]. Everything else is imported.

## 1. Objects, constants, imports

Machine, top map, halting criterion: work_r1/RULES.md (Class-A), quoted in
work_r4/PROOF.md:5-14 — T halts on a list L iff A odd and A+2b+3 is a power of 2;
sum(L_n) = 3n+3, L_0 = (3). Singletons S1/S2/S3 and Lemma E(v) (Class-A, v ≤ 2000):
work_r4/PROOF.md:16-41. Pair map F, crossings X(n), τ(n), fire/exit-chain structure,
Lemma 6.1 (F's top-level small parts are α λ_u + β with S(J)'s pairs), Lemma 3.2
(σ_t = ρ−Γ_t), replay Lemmas 2.1–2.3, Corollary 3.5 (only level fires and exit chains
can fail S1; S2 never fails), Theorem 4.1 (the lambda-only certificate): work_m (accepted
2026-10-13; engine verify_m.py, V1/V2). Endgame E1–E4: work_global_endgame/LEMMAS_E
(I-2). EGX, Lemma TR, Lemma C2-log, Theorem U, Corollary H: work_global_egx/PROOF_EGX.md
(accepted 2026-10-17); the import audit at §3 (lines 163-171) is used verbatim. Theorem
U\*/Prop 2.1, Lemma K/HP/AB, Theorem RA, Theorem S, Corollary 4, Corollary H'':
work_global_ext/PROOF_EXT.md (accepted 2026-10-17). CLOCK, C1, STATE-CLOCK, s ≤ i²:
work_global_clock/PROOF_CLOCK.md §3-4 (accepted). CSH, BOUND, EXT-CLOCK, Lemma MASS,
Corollary H-CLOCK: work_global_clock_horizon/PROOF_CLOCK_HORIZON.md (accepted 2026-10-18).
Theorem T4: work_claude_residual/NOTES.md:79-81 (net result; review-correction block
items 1, 2, 7 govern), accepted 2026-11-02 — "for every J with K_clock ≤ J < T4 and F
defined through tau(J−1), S(J) is tie-free", relative to the accepted EXT(<K_clock) and
the imports (C5_EXTENSION §4, CLOCK/C1, gateway/window certificates).

Tower constants (as in the checkpoint): N0 = 2·10^7; T1 = 2^((N0−3)/2);
T_{h+1} = 2^((T_h−3)/2); G(x) = 2·log2(x)+3 (G(J) < T_h ⟺ J < T_{h+1}); K = 2^(2^499997−2),
K′ = 2^(K/2−2), K″ = 2^(K′/2−2); K_clock = ⌊2^K′/(64 K′²)⌋ (constant 64 from Lemma MASS).
S(J), tie-free, "F defined through τ(J−1) inclusive", the defect D_0, the endgame:
PROOF_EGX §1-2. Notation j_t, Γ_t, σ_t, h_t, r as there.

**Lemma HINQ [A, checked exactly in (a)].** For every integer H ≥ 16: 3(H−1)²+4 < 2^H;
moreover 3(H−2)²+7 < 2^H, so for every v ≤ H−1 both F-steps (v−1)² and (v−1)²+1 satisfy
3s+4 < 2^H, and (v−1)² < (2^H−4)/3. Proof: base direct at H = 16; L(H) := 3(H−1)²+4 and
L(H+1) = L(H) + 6H−3 < 2·L(H) whenever 6H−3 < L(H); this slack is equivalent to
3H²−12H+10 > 0, which holds for every integer H ≥ 3 (discriminant 24, roots 2±√6/3,
minimum 1 at H = 3) — in particular at every H ≥ 16 of the induction. This is the
argument of PROOF_CLOCK_HORIZON §4:157-160; the script (a) checks H = 16..4096 exactly
plus the all-scale slack constant, and (b) gives T4 > 2^64 ≥ 16. *Real-H instance*
(H = T4 is irrational): log2 T4 = (T3−3)/2 gives 3·T4² = 3·2^(T3−3) < 2^(T3+2) < 2^T4,
where the last step is T3+2 < 2^((T3−3)/2), instantiated exactly as (T3+2)² < 2^(T3−3)
(true at T3 = 16 — 324 < 8192 — and preserved for all larger T3 since the right side
doubles per increment while the left grows by ((T3+3)/(T3+2))² < 2; checked exactly for
T3 = 16..4096, and T3 > 2^64 by Lemma ORD). Hence 3(T4−1)²+4 < 3T4² < 2^T4 and a
fortiori 3(T4−2)²+7 < 2^T4, (v−1)² < (2^T4−4)/3 for v ≤ T4−1 — this is how HINQ is
applied at H = T4 in §5; none of it depends on a finite range.

## 2. Lemma ORD (tower ordering) [exact, script part (b)]

T1 < K, T2 < K′, K′ < T3, **T3 < K_clock**, **K_clock < T4**; also K′ ≤ K_clock and
T4 > 2^64. In particular T3 < K_clock < T4 — independently re-deriving the ordering
confirmed by the residual review (reviews/claude_residual_review_record.md:15) — and the
EXT coverage below is non-degenerate.
*Method (no floats).* Pure towers Tw(k,q) := 2^(2^(...^q)) (k twos) are compared by
stripping: two towers of equal height compare by their top exponents; two towers of
height ≥ 1 are both 2^(something), so one level is stripped from each; a tower vs a
bounded integer (< 2^24) is decided by value (exact when the tower is 2^q with q ≤ 23,
else the tower is ≥ 2^24 once its exponent is ≥ 24, decided recursively). Each bound
below strips the (−3)/2 and floor losses with explicit slack; every intermediate step is
an exact integer inequality between computable integers (exponents of size ≤ 10^7·2^20)
or a tower comparison as above. Bounds used:
2^9999998 < T1 < 2^9999999 (squaring); 2^(2^9999996) < T2 < 2^(2^9999998);
2^(2^(2^9999994)) < T3 < 2^(2^(2^9999998)); 2^(2^(2^(2^9999990))) < T4 < 2^(2^(2^(2^9999998)));
2^(2^499496) < K < 2^(2^499997); 2^(2^(2^499496)) < K′ < 2^(2^(2^499997));
2^(2^(2^(2^499495))) < K_clock < 2^(2^(2^(2^499997))) (lower bound via log2 x ≤ x/8 for
x ≥ 2^7, checked exactly with monotone tail). Script: verify_t4_horizon.py part (b).

## 3. Lemma EXT-T4 (globalisation of the tie-free range) [A]

**Statement.** For every integer J ≥ 1 with J < T4: if F is defined through τ(J−1)
(inclusive), then S(J) is tie-free and ends at an even return after at most max(0, J−2)
exit chains.

*Proof.* Three ranges, each an accepted per-J statement under exactly this hypothesis:
1. 1 ≤ J < K′: import I-4 (PROOF_EGX §3:158-161), stated for **every** J < K′ (all-J
   base, including J = 1: S(1) closes at once — its data X(0) is the initial state
   A = (1,1), an even head, so r = 0; every J = 1 epoch in the machine data of §6(c)
   closes with zero exit chains), as read by the accepted EXT-CLOCK proof: "J < T is
   the accepted base I-4" with T = K′ (PROOF_CLOCK_HORIZON §3:92); for the F-facts it
   only needs F through τ(J−1) (the §3 import audit, PROOF_EGX:163-171).
2. K′ ≤ J < K_clock: EXT-CLOCK (PROOF_CLOCK_HORIZON §3:89-94) — "for every J < K_clock,
   if F is defined through tau(J−1), S(J) is tie-free" (CSH + Lemma MASS).
3. K_clock ≤ J < T4: Theorem T4 (work_claude_residual/NOTES.md:79-81), whose reviewed
   statement is exactly this range and hypothesis.
   *Non-circularity of the union.* T4 is stated relative to the accepted EXT(<K_clock),
   and its original §6 phrasing ran inside a "least strict-EXT counterexample
   induction". What that induction supplies is tie-freeness of the **source epochs**
   S(Q) invoked inside the proof, at labels Q strictly below the J under consideration.
   By the residual note's own scale lemma every such source has Q < T3: DL(i)
   (NOTES.md:162-163) bounds the label of the source epoch of a crossing at index n by
   Q < G(n); DL(iv) (NOTES.md:174-177) gives, for S(J) with J < T4, that a c step at
   deep chain t ∈ {0,1,2,3} has source Q < T3, T2, T1, N0 respectively; shallow
   crossings (n < N0) have Q < G(N0) < 60; the one uncertified landing entry (5,5)
   (whose source family, residual §5.4, has T1 ≤ Q < T2) can occur only with X(J−1)
   of type **a**, in which case the accepted Theorem RA gives EXT(J) outright — RA's
   only F-hypothesis is "F defined through τ(J−1), inclusive" (as reviewed in
   PROOF_CLOCK_HORIZON §1 item 2; its internal use of Lemma AB is self-contained) —
   while with X(J−1) of type b or c the (5,5) entry is unreachable (route c: the
   chain j₁ = ω(J−1) of the a-output of a source Q′ < G(J−1) < T3 satisfies j₁ < T2,
   contradicting the j₁−1 > T2 needed at the t = 1 position; route b gives θ₁ = 0 ≠ 2;
   residual review-correction item 1); C5_EXTENSION §4's induction is over the ≤ 4
   deep steps inside one S(J), not over J.
   By Lemma ORD, T3 < K_clock, so **every** source label Q < T3 lies in ranges 1-2,
   which are already established unconditionally of J. Hence no appeal to EXT at any
   J′ ∈ [K_clock, J) is needed, and the three ranges compose into a plain per-J
   statement. The termination clause (even return, ≤ max(0, J−2) chains) is
   PROOF_EGX §5:206-208 (Lemma T(1), j_t ≥ 1, Γ_t ≥ t ⟹ t ≤ Γ_t ≤ J−2). ∎

## 4. Lemma DATA-T4 (data locality / prefix closure) [A]

**Statement.** Let J ≥ 1 with F defined through τ(J−1) inclusive (for J = 1 this is
step τ(0) = 0, the initial state). Then:
(a) the recursion S(J) consults only crossing data X(m), m ≤ J−1, and copied W-chains at
    F-times ≤ τ(J−1) (the b/c first return copies F's chain at step τ(J−1) itself);
(b) X(J−1) is reached, and C1 gives τ(J−1) ≤ (J−1)²;
(c) if moreover J < T4, then every F-step S(J) consults lies at time
    ≤ (J−1)² ≤ (T4−2)² < (2^T4−4)/3 (Lemma HINQ at H = T4 ≥ 16).

*Proof.* (a) is the definition of S(J) (PROOF_EGX §1:53-56: "it needs F's crossing data
X(m), m ≤ J−1, and F's own chains at steps ≤ τ(J−1) **inclusive**") together with the
accepted import audit (PROOF_EGX §3:163-171: "The F-facts they use are: crossing data
X(m), m ≤ J−1; the copied W-chains at τ(m), m ≤ J−1 (at or before τ(J−1)) ... None uses
the pointer ρ or any F step after τ(J−1)"). (b): τ(J−1) is by definition the time at
which X(J−1) is reached, and F is defined at that step, so C1 (PROOF_CLOCK §3: "C1 for
every reached crossing, without an exit-length or C2 hypothesis") applies. (c): J ≤ T4−1
so (J−1)² ≤ (T4−2)², and 3(T4−2)²+4 < 3(T4−1)²+4 < 2^T4 by Lemma HINQ. ∎

*Role.* H-CLOCK's transfer says "Its replay source X(J−1) is earlier and defined" in one
clause; Lemma DATA-T4 makes the anti-circularity bookkeeping explicit: in the induction
of Theorem H-T4(i) every application of Lemma EXT-T4 at a level fire reads only F-times
≤ τ(J−1) < t (strictness in the proof below), i.e. strictly inside the prefix already
constructed — and the same for the endgame applications in (ii) (data X(m), m ≤ v−1,
times ≤ τ(v−1)). This closes the "记账循环" risk named in the route instructions.

## 5. Theorem H-T4 [A]

*Proof of (i): F defined for all s with 3s+4 < 2^T4.* Induction over the steps of the
maximal defined prefix, i.e. Theorem U(b) (PROOF_EGX §5:215-226) with I-4 replaced by
Lemma EXT-T4. Assume all steps < t are defined (t ≥ 1) and 3t+4 < 2^T4; show step t is
defined. By PROOF_M Corollary 3.5 (as used in U(b)) only level fires and exit chains can
fail S1; S2 never fails; internal steps are M_u-images of earlier defined W-steps
(replay Lemmas 2.1-2.3) and even steps are defined — all accepted.

*Level fire at step t*: pointer ρ, s₀ = τ(ρ) = t, J := v2(3s₀+4). Then 2^J ≤ 3s₀+4 < 2^T4,
so J < T4. S1 at the fire is J < ρ = σ₀: for ρ ≤ 10^8 this is the audited base (PROOF_EGX
§5:217-218, "For ρ ≤ N_B = 10^8: audited base V2" — the V2 margin certificate j < σ at
every top-level chain, run to 10^8); for ρ > 10^8, STATE-CLOCK (PROOF_CLOCK §4:133,
quoted in U(b):217-219) gives
s₀ = τ(ρ) ≤ ρ·P(ρ) < ρ(2ρ+1), hence 2^J ≤ 3s₀+4 < 2^ρ and J < ρ.

*Exit chain t′ ≥ 1 of that epoch*: J−1 < ρ, and τ(J−1) < τ(ρ) = t. Strictness: crossings
occur in pointer order (τ nondecreasing), and τ(m) = τ(m+1) happens only for the pair
(X(m) type a, X(m+1) type b) recorded at one P = ∅ step (work_m crossing structure,
Lemma K(a,b)); X(ρ) is type a (a level fire, Lemma K(a)), so ρ is not the second element
of such a pair, whence τ(ρ−1) < τ(ρ) and therefore τ(J−1) ≤ τ(ρ−1) < t. So F is defined
through τ(J−1) inclusive (induction hypothesis), and Lemma EXT-T4 applies: S(J) is
tie-free. By PROOF_M Lemma 6.1 (the identification behind U(b):220-223), the epoch's
chain parameters are S(J)'s: j_{t′} = v2(β_{x_{t′}}) < v2(α_{x_{t′}}) = J−Γ_{t′}
(Lemma T(1)); F's coefficient valuation is σ_{t′} = ρ−Γ_{t′} (PROOF_M Lemma 3.2). Hence
σ_{t′} − j_{t′} = (ρ−J) + (J−Γ_{t′}−j_{t′}) = (ρ−J) + h_{t′} with ρ−J ≥ 1 and h_{t′} ≥ 1:
S1 holds at every exit chain. Lemma DATA-T4(a,c): all data read sits at times < t.

*Termination*: S(J) ends at an even return within max(0, J−2) exit chains (Lemma EXT-T4),
so the epoch closes with P = ∅, the pointer advances by ≥ 2, and between epochs only
even steps at P = ∅ occur (U(b):224-226). Step t is defined; the induction runs through
every t with 3t+4 < 2^T4. ∎

*Proof of (ii): no halt in the first 2^T4−2 top steps.* Induction over singleton times,
i.e. Corollary H (PROOF_EGX §3:173-179) with K′ replaced by T4. L₀ = (3) is a singleton
at n = 0 and 2 < 2^T4. Let n be a singleton time with n+2 < 2^T4.
- No halt at n: S2 (work_r4:18-19) — A+2b+3 = 3(n+2) is divisible by 3, hence not a
  power of 2 (halting criterion, work_r4:11-12).
- n odd: the next singleton is n+1 (S1, work_r4:18).
- n even: v := v2(n+2) ∈ [1, T4) (2^v ≤ n+2 < 2^T4), w := (n+2)/2^v odd ≥ 1, and
  L_{n+1} = E(w,v) (S3, work_r4:20-26).
  * v ≤ 2000: Lemma E(v) (work_r4 §2, audited Class-A): the excursion never halts and
    reaches the singleton at n+1+ℓ(v).
  * v ≥ 3:
    - *F defined through τ(v−1) inclusive.* (v−1)² + 1 ≤ (T4−2)² + 1 < (T4−1)², so
      3((v−1)²+1)+4 < 3(T4−1)²+4 < 2^T4 (Lemma HINQ, H = T4 > 2^64 by Lemma ORD): the
      F-steps (v−1)² and (v−1)²+1 are inside the prefix (i). At the state of F-step
      (v−1)²+1 the original pointer i satisfies i² ≥ s > (v−1)² (PROOF_CLOCK §4: s ≤ i²
      at every state of the maximal prefix), so i > v−1 and the crossing X(v−1) was
      reached at τ(v−1) ≤ (v−1)² < (2^T4−4)/3 (Lemma HINQ); F is defined at step
      τ(v−1) itself. (This is the I-3 reached-crossing argument, PROOF_EGX §3:156-158,
      instantiated with H = T4.)
    - Lemma EXT-T4 at J = v: S(v) is tie-free and ends at an even return.
    - D5 (queue determinism; PROOF_EGX §1:33-35): the pair run of E(w,v) equals F
      through step τ(v−1); from that state Theorem EGX (PROOF_EGX §2) identifies the
      endgame of E(w,v) with S(v) pair for pair **for every odd w**; the endgame is
      safe and reaches the singleton (2^v, 3ℓ(v)) at top step n+1+ℓ(v).
    - E1-E4 (I-2): along the safe pair prefix the real orbit is the pair image for
      every odd w and no step halts.
  The next singleton time is n′ = n+1+ℓ(v) (resp. n+1); if n′+2 < 2^T4 the induction
  continues.
- *Coverage.* Every top step n* with n*+2 < 2^T4 either is a singleton time or lies
  strictly between consecutive singleton times n < n′ with n+2 ≤ n*+2 < 2^T4; the
  excursion from n (or the odd-singleton step) covers it. Singleton times are defined
  for ever by the induction (each case produces the next one). So no top step n with
  n+2 < 2^T4 halts. ∎

**Off-by-one checklist** (the transfer's sensitive points, matched to the precedents):

| item | here | precedent |
|---|---|---|
| horizon inequality | 3(H−1)²+4 < 2^H, H ≥ 16 ⟹ (v−1)² < (2^H−4)/3 for v ≤ H−1 | PROOF_CLOCK_HORIZON §4:157-160 |
| singleton coverage | first n with v2(n+2) ≥ H is exactly n = 2^H−2; "first 2^H−2 top steps" = {n : n+2 < 2^H} | PROOF_EXT §4:149-153; PROOF_CLOCK_HORIZON §4:141-144 |
| fire bound | 2^J ≤ 3s₀+4 < 2^H ⟹ J < H | H-CLOCK §4:150-152 |
| "through τ(J−1) inclusive" | τ(J−1) < τ(ρ) = s₀ (same-step pairs are (a,b) only; X(ρ) is type a) | PROOF_EGX §1:56 + auditor-2 fix (§9) |
| excursion bookkeeping | singleton n even ⟹ L_{n+1} = E(w,v) ⟹ next singleton n+1+ℓ(v) | Corollary H, PROOF_EGX §3:176-179 |

## 6. Verification [B] — verify_t4_horizon.py

Run from D:/math_cc with
`PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B
work_gc_t4_horizon/verify_t4_horizon.py [total_budget_seconds]` (default 480). ASCII
output, last line `ALL PASS`, exit 0; writes `t4_horizon_checks.json` beside itself.
Read-only import: `work_m/verify_m.py` (precedent: work_global_egx/verify_egx.py:137-147,
check C3). All decisions in exact integer arithmetic; **no floats**.

**(a) Lemma HINQ.** 3(H−1)²+4 < 2^H verified exactly for H = 16..4096, the step identity
L(H+1) = L(H)+6H−3, the slack 6H−3 < L(H) (via its equivalent 3H²−12H+10 > 0, checked
for all integers H = 3..3999 — discriminant 24, minimum 1 at H = 3; H = 2 fails the
slack but is outside the induction range), the derived 3(H−2)²+7 < 2^H, 3(H−2)²+4 < 2^H,
and the real-H chain of §1 ((T3+2)² < 2^(T3−3) and 3·2^(T3−3) < 2^(T3+2), exactly for
T3 = 16..4096, plus the H = 2 slack counterexample as a negative control).

**(b) Lemma ORD.** The eight orderings of §2 by the pure-tower strip comparator, with
each intermediate bound an exact integer assertion; comparator self-tests included.
This re-derives T3 < K_clock < T4 independently of the residual review's confirmation.

**(c) Machine-level validation of the H-CLOCK transfer pattern itself** — the pattern
was asserted in PROOF_CLOCK_HORIZON §4 but never mechanically checked; here it is, for
the first time, end to end at small H0. Engines: lambda-only walker of F (the verify_m
V2 engine; measured throughput ~6-9·10^5 steps/s with all checks on, machine-load
dependent), full-pair walk for the first 64 crossings (X data in the verify_m.Xdata
format), symbolic-exit walker (verify_egx.symexit engine) cross-checked against the
imported `verify_m.sym_exit` (work_m/verify_m.py:230) for every J used, pair-endgame
runner (verify_egx.endgame engine), and the integer top map (work_r1 rules in the
work_r4 form; ~7-12·10^5 steps/s with checks on). The ladder H0 ∈ {20,22,24,26,28,30}
is adaptive: each next rung is run only if its cost predicted from the measured
throughput fits the budget (default: per-run ≤ 0.6·480 s = 288 s, total ≤ 480 s).

**Achieved with the default budget: H0 = 20, 22, 24, 26** (stable across all runs of
2026-11-09/10; total wall time 98-150 s depending on machine load; per-rung counts are
deterministic). Largest rung: F prefix s* = (2^26−5)//3 = 22,369,619 steps (pointer
25,074,248), 7,594,491 level fires, 595,760 exit chains, 7,594,490 closed epochs; top
map 2^26−2 = 67,108,862 top steps, 29,990,130 singletons, 22,783,474 gap checks; max
singleton v = 25 = H0−1; min fire margin ρ−J = 3. **Extended-budget run (900 s,
extended_run_900s.log, 600.2 s total, corrected script of round 1): additionally
H0 = 28** — 2^28−2 = 268,435,454 top steps with no halt, F prefix 89,478,483 steps
(pointer 100,296,961), 30,377,959 fires, 119,960,495 singletons, 91,133,877 gap
checks, all PASS with every assert of items 1-6 below active.
The shipped `t4_horizon_checks.json` is written by the **final default-budget run**
(see its `c_total_s`); `fire_Js` entries there are `[J, [fire_count,
min_margin_rho_minus_J]]`. For each achieved H0 the following hold, exhaustively over
the stated ranges:

1. *F prefix defined*: margin j < σ at every top-level chain of the whole prefix
   (verify_m Theorem 4.1 certificate); σ-recursion σ_{t} = σ_{t−1}−1−ε verified at
   every exit chain (verify_m V1 identity); s ≤ i² at every state with i ≥ 16
   (PROOF_CLOCK §4); τ(n) ≤ n² at every recorded crossing n < 4096 (C1); CLOCK
   s ≤ i·P(i) asserted at every level fire and at the final pointer
   (P(n) = 2⌈log2(6n²+5)⌉²+1345).
2. *Per level fire* (all of them): J = v2(3s₀+4) (asserted), J < ρ, 3s₀+4 < 2^H0
   (so J < H0), τ(J−1) ≤ (J−1)².
3. *Per J ∈ {1..32}* (covers every fire J and every singleton v < H0 ≤ 30): S(J)
   tie-free, r ≤ max(0, J−2), per-chain h_t = J−Γ_t−j_t ≥ 1, Lemma T(1) identity
   v2(α_{x_t}) = J−Γ_t; own walker == work_m.sym_exit (j-sequence, type string, r, Γ).
   Per closed epoch of the walk: the recorded (j_t) equals S(J)'s j-sequence and
   σ_t = ρ−Γ_t (so σ_t−j_t = (ρ−J)+h_t > 0) — PROOF_M Lemma 6.1/3.2 at machine level,
   for every epoch of the prefix (7,594,490 closed epochs at H0 = 26).
4. *Top map*: no halt at any of the 2^H0−2 top steps (R1 criterion checked at every
   step); sum law 3n+3 at every step; every even singleton time n has v = v2(n+2) <
   H0; per distinct v ∈ {1..32}: the pair endgame of E(w,v) equals S(v) chain for
   chain (j and the pair x), final singleton (2^v, 3ℓ), and the **machine** gap
   n′−n−1 equals ℓ(v) = τ(v−1)+endgame length at **every occurrence** (D5 + EGX
   timing, 22,783,474 occurrences checked at H0 = 26); ℓ(1..20) equals the R4 table
   (work_r4/PROOF.md:40).
5. *Off-by-one*: no top step n < 2^H0−2 has v2(n+2) ≥ H0 (in data: max v = H0−1), and
   the first n with v2(n+2) ≥ H0 is exactly 2^H0−2 (exact arithmetic check).
6. *Engine consistency*: full-pair vs lambda-only walker agree on τ(n) and ε(n) for
   all n < 64.

Scope statement (honest limits): part (c) is [B] evidence about the transfer *pattern*
at H0 ≤ 28 (default budget: H0 ≤ 26; top steps < 2.7·10^8 at H0 = 28; for comparison,
R4's audited machine check covered n < 2^20, work_r4 §3 check2). The pure-Python list
engines' throughput is the binding
constraint (~10^6 steps/s each; the full-pair engine is not usable beyond ~2·10^6 steps
because the pointer races at i ≈ 1.12·s and the c-parts grow like 2^i). The analytic
Theorem H-T4 does not depend on H0 or on part (c).

## 7. What is not claimed

- No statement about J ≥ T4, T5, or global EXT*/non-halting. The level method beyond T4
  does not stabilise (work_claude_residual §7); nothing here changes that.
- G1 (FREE-B, CL2, CL4) untouched; this note is pure transfer/bookkeeping.
- No new level-5 certificate; Theorem S's source cutoff K′ is unchanged; K_clock's
  arithmetic is untouched.
- Until three-way review accepts this note, the repository's accepted horizon stays
  2^K_clock−2 (the checkpoint's work_claude_residual section governs). On acceptance,
  the accepted horizon becomes 2^T4−2 top steps / (2^T4−4)/3 F-steps.
- Part (c)'s checks validate ingredients of the proof at small scale; they are not a
  proof of Theorem H-T4 (which is [A], from imports).

## 8. Reproduction

    cd D:/math_cc
    PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe \
        -B work_gc_t4_horizon/verify_t4_horizon.py          # default 480 s -> H0 20..26
    # optional extended probe: append 900   (see extended_run_900s.log)

Runtime ~100-150 s at default budget (machine-load dependent; the achieved ladder
{20,22,24,26} and all per-rung counts are deterministic and were stable across every
run). The shipped `t4_horizon_checks.json` is written by the final default-budget run
of 2026-11-10 and holds the full record: per-H0 counts, per-J fire counts and margins
(`fire_Js` entries `[J, [fire_count, min_margin_rho_minus_J]]`), singleton v histogram.
