# Three-way review of work_mixed_bridge (global strict-EXT / non-halting proof draft, BB(6) holdout #1), 2026-11-22

Target: work_mixed_bridge/PROOF.md (§§1–5: mixed-block bridge theorem and the two strict-EXT
assemblies) and work_mixed_bridge/SMALL_BASE.md (J=1024 small-base assembly), with the author's
verify_bridge.py, verify_source_prefix.py, audit_bridge.py. Route claim: in the strict
least-counterexample induction every productive mixed-block word with input chains in [5,Q] has
length at most Q for Q≥64; hence strict EXT for every J (PROOF.md main line from K′; SMALL_BASE
from J=1024); by the accepted Theorem U (PROOF_EGX §5) machine #1 never halts on the blank tape.
work_direct_phase is declared a non-dependency and was out of scope (non-dependency confirmed by
the adversary: no reference from either draft).

Reviewers, all ZCode GLM 5.3 subagents, parallel and mutually blind (no reviewer read another
reviewer's file; auditors additionally did not read the author's three new scripts):

- Adversary (`gc_mixed_bridge_adversary.md`, scratch/mb_review_adv/): full attack — hand-derived
  all key algebra, re-ran the author's scripts, wrote a third independent enumeration plus
  independent walk/sym_exit/witness/lift machinery, and ran adversarial counterexample searches.
- Auditor 1 (`gc_mixed_bridge_auditor1.md`, scratch/mb_review_a1/): blind mechanical/numerical
  recomputation — own enumerator (own two-dimensional congruence solver), own S(J) recursion
  checked against the accepted sym_exit, own constants/grid/arithmetic checks, own witness replay
  including an explicit integer lift.
- Auditor 2 (`gc_mixed_bridge_auditor2.md`, scratch/mb_review_a2/): blind algebraic
  re-derivation from the accepted imports (PROOF_MIXED STATE/BLOCK, PROOF_CLOCK, PROOF_EGX,
  PROOF_EXT_ROOTS), clause-level consistency of SMALL_BASE's downstream section, non-circularity
  analysis, own formal walker and witness replay with a Hensel/CRT lift.

**All three attended; none absent.**

## Round 1 (three-way, 2026-11-22)

- **Adversary: `1. all correct`.** Every key derivation upheld under hand attack: §1 block map
  and bounds (1) (C2-log per-step 4log₂q+4, successor ≤√q, geometric sum, tail ≤3; replayed on
  1,300 random integer lifts); §2 composition (β∈[1,2], γ∈[0,2t], per-block product clearing),
  congruence (3), Z_i a pure integer combination (mixing distinct per-bridge s_i is legal —
  attack point (i)), |Z_i|≤12T·2^(2S), (4)⟹Z=0, p-halving, r≤2+⌊log₂(2T)⌋, ledger (5)
  (1+2F+r(F+1) fits (F+1)(4+⌊log₂(2T)⌋)); §3 constants; §4 obligations proven for **all**
  integers e≥20 via positive-coefficient gap polynomials (576e²+3192e+3316 etc.), not just the
  sampled grid; §5 counting and direct assembly 18l²+61l+31≤32l²<2^(l−2); SMALL_BASE clock
  induction (τ-increment bound verified for all n=0..1021) and two-range closing. Three-way
  computational agreement on the base: {325, 105625, 25438, 17378, 6271, 504, 0}, max block loss
  3 (author's cylinder verifier, the original lattice enumerator re-run, and the adversary's
  third unmasked-cylinder enumeration over raw pair data). Witness 661128→17→661128→857036
  independently replayed: (p₀,t₀,p₁)=(2654187,1769472,884715), p₀=t₀+p₁, and additionally both
  (3) congruences hold mod 2^1024, Θ₁=Θ₀+t₀ (elapsed-clock sign, attack point (ii)), Z₀=0 with
  distinct clearing factors s₀=2≠s₁=1. Attack point (iii): no circularity — every C2-log use
  sits at J_W≤log₂(3(q−1)²+4)<J with large margin (all use-points enumerated; PROOF_EGX §6's
  prefix estimate confirmed to precede LIN-EXIT from the original text). Attack point (iv):
  productive-input counting at corridor truncations is sound (the unfinished tail is charged
  ≤g by descent in both assemblies without reading the next row). Adversarial search: all
  4-high words with repeated bridges are 2-adically infeasible — exactly what the theorem
  predicts (equal bridges force Z=b²t>0), positive evidence for the (4)–Z mechanism; cap-8191
  live test of (1): no violations; 20,000 random multi-block composition chains: all
  invariants pass. Import checklist (MASS/CONE, core_words, mixed_blocks, CLOCK/C1, corrected
  C2-log, Theorem U/EGX §§4–6, EXT_ROOTS §4, W(Q), sym_exit/Xdata, Calendar) checked against
  the CHECKPOINT acceptance records — all accepted and used in scope. Findings: **no
  HIGH/MEDIUM**; F1 [LOW] audit_bridge.py needs z3 (absent here) — substitute z3-free exact
  integer checks were written and all pass; recommend publishing a z3-free variant; F2 [LOW]
  verify_bridge.py scale_checks samples only 7 grid exponents — embed the four gap polynomials
  instead; F3 [INFO] 497 vs tight 490; F4 [INFO] 22 vs 21 small replays; F5 [INFO] only one
  adjacent-bridge pair is machine-tested (the witness pair); F6 [INFO] escapes, deterministic
  corridor input-independence, and row-formula cross-checks all pass; F7 [INFO] three
  derivations are compressed and would each merit one more line.
- **Auditor 1: `1. all correct`.** Own enumerator (own kernel/congruence solver, brute-force
  validated on 30,000 small cases; 400-node unpruned full-alphabet cross-check with zero
  mismatch): productive inputs **325** (q∈[5,1021]), word counts **105625/25438/17378/6271/504/0**,
  max productive block loss **3**, plus the PROOF_WORDS anchors (duration 909, terminal loss 4,
  duration 912) and escape nodes 66/66/33 (total 165); multiplier-assignment formula
  v₂(c_H+2c_Y)−(n+1)=−(1+ε) zero violations over all rows. Own S(J) recursion vs the accepted
  sym_exit on the same fresh Xdata prefix, J=1..1023, zero mismatch: splits **{0:389,1:586,2:48}**,
  all even-head terminations, max exit loss **4**, τ(1022)=**910**, τ(n)≤n, max τ(≤62)=**51**,
  q+Γ<J per chain. §3 constants exact (S=201, 12T·2^402<2^1024); §4 dual-route (exact big
  integers n≤16; polynomial implications n=0..40) all pass, including the n=0 equality
  1024=48·20+64 and the squaring invariant; §5 arithmetic all pass (l=64 direct-assembly left
  side 13,025 ≤ 131,072); SMALL_BASE numerics all pass (G=23, 5551/3<2045, 5935<6144, 137<256,
  range switch at l=510 consistent, J=1024 bootstrap 577≤1024). Witness: walked the raw pairs to
  row 661127 (68 s), bridges exact, **p₀=t₀+p₁**, and an explicit integer lift (u∈{1,3}, CRT
  value of Θ₀) replays the parameter list [17,661128,857036] exactly with Θ integral throughout.
  LOW-1: ⌊log₂(2T)⌋=66 so (5) actually gives N≤490 (the draft's 497 is a true but loose bound);
  LOW-2: the exponent decomposition 4+66 vs the tight bit length 69 — both true. Scope honestly
  declared: the [A]-level structural text was sampled, not sentence-by-sentence re-proved (the
  adversary's direction).
- **Auditor 2: `1. all correct`.** Re-derived from PROOF_MIXED's STATE/BLOCK identities:
  x′=−αx/2+2Θ+c, c=6d+6k−B/2∈[0,2t], 2^l clearing; bounds (1) term by term. §2 in full:
  composition update, per-block clearing, and the legality of subtracting congruences carrying
  different s_i (attack point (i)) — after clearing each congruence is an integer divisibility
  statement, so multiplication and subtraction of integers preserve it; |Z|≤12T·2^(2S) with
  cᵢ≤2^S·2T; (4)⟹Z=0⟹p_{i+1}=p_i−t_i≤p_i/2 (attack point (ii): all ordinary rational
  inequalities, signs preserved by bᵢ>0); ledger (5) valid and conservative (could tighten to
  (F+1)(3+⌊log₂(2T)⌋)). §4 tower algebra verified by own script for e=20..1280. §5 both
  assemblies re-derived, including the direct first-tie bound and the t=1 case; the EGX §6
  prefix estimate confirmed to precede LIN-EXIT. SMALL_BASE fully re-derived: own formal walker
  matches the accepted Xdata on all n≤1022; the clock-increment constants (4G²/3 geometric sum,
  ≤21+1 small replays ×52 +1 terminal = 1145), the k≥10 doubling inequality, the two-range
  closing (10l+37<2^(l−2) from l=10; 32l² for l≥510), and clause-level consistency of the
  downstream section with U(b)/I-1/I-2/E1–E4 and the blank-tape singleton reduction.
  Non-circularity (attack point (iii)): every C2-log use point has J_W<J with large margin; the
  J=1024 start needs only rows ≤X(1022), present. Witness (item 7): own 589,811-step walk;
  bridge 0 is the **composite** block through the low entry 17 (s₀=2, β₀=1, γ₀=2654187,
  t₀=1769472), bridge 1 the escape block (s₁=1, β₁=2, γ₁=1769430) — triple exact, Z₀=0 as an
  integer (not only mod 2^(h+1)), and a Hensel/CRT integer lift Θ₀ (mod 2^857038) replays
  (661128,17,661128,857036) integrally. Findings: F1 [LOW] the witness sentence should say
  bridge 0 is composite (readability); F2 [LOW] (5) conservative; F3 [LOW] the first-corridor-
  from-b/c case of (1) is brief but correct. No mathematical defect.

Coordinator byte-checks (this record): ⌊log₂(2T)⌋ with T=42·2^60 equals **66** (draft's 67 loose;
(5) gives N≤490≤497≤√M); worst-case ledger 1+2F+r(F+1)=489≤(F+1)(4+66)=490 at r=2+66, F=6;
3·64·134·133=3,421,824<2^63; witness identity 2654187=1769472+884715 exact. The §4 grid
obligations were additionally verified in-session for e=20·2ⁿ, n=0..11 (exponent comparison).
Side effects: re-running the accepted word_search.py rewrote work_g2_core_words/words_1023.json
(depth_limit field); restored via git checkout — working tree now shows only the pre-existing
uncommitted CHECKPOINT diff and untracked directories.

## Round-1 verdict

**Unanimous `1. all correct` (adversary, auditor 1, auditor 2). No HIGH or MEDIUM findings; no
mathematical defect located in PROOF.md §§1–5 or SMALL_BASE.md.** The four author-designated
attack points (i)–(iv) are all upheld; the import checklist is entirely accepted prior work used
in scope; the draft's non-dependency on work_direct_phase is confirmed. Patch items (all LOW/INFO,
optional): (P1) publish a z3-free exact-integer variant of audit_bridge.py (or record z3 as a
dependency); (P2) embed the four all-e gap polynomials in verify_bridge.py instead of 7-point
sampling; (P3) one-line expansions for the three derivations flagged F7; (P4) witness wording
(composite bridge 0); (P5) replace 497→490 and 22→21 (or mark both as loose bounds). Per repo
policy the acceptance decision, CHECKPOINT entry and commit belong to the user. All three reviews
explicitly note — as does the draft — that the structural lemmas identifying the pair process
with the original machine are covered only by their prior accepted reviews and were not
re-reviewed here.

## Patches (coordinator-executed) and targeted re-review, 2026-11-22

- Patches (per the five patch items; only work_mixed_bridge/ files touched):
  **P1** audit_bridge.py fully rewritten as a z3-free exact-integer/fraction audit — polynomial
  identities in a 12-variate ring (determinant = threshold × integral witness), box-corner
  enumeration where targets are multilinear (composition bounds, normalized |Z| with exact
  extrema (−4,8)), and the four grid obligations as gap polynomials at r=48e+64 with
  nonnegative coefficients and positive constant terms plus r-monotonicity beyond the
  invariant (derivative lower bound 2(48e+64)−c1 with nonnegative coefficients); all sixteen
  check subjects of the old z3 version are covered. One drafting error (obligation 2 initially
  dropped the 6r term) was caught by the built-in e=20 polynomial↔arithmetic cross-check and
  fixed before review. **P2** verify_bridge.py now imports gap_polynomials() and asserts the
  all-scale obligations exactly (sampling loop retained as spot checks); the N bound assert is
  now the exact ⌊log₂(2T)⌋=66, 7·70=490. **P3** three one-line derivations added in PROOF.md
  (t≤6M³ via d≤M(1+M²) and 2k=τ≤M² at the terminal a-row; the γ invariant distinguishing the
  accumulated phase; the 12<2^4 step of (4)). **P4** the witness sentence now states bridge 0
  is the composite block through 17 (s₀=2, β₀=1) and bridge 1 the escape block (s₁=1, β₁=2).
  **P5** 497→490 (two places) and "at most 22"→"at most 21 … charging 22·52+1=1145" in
  SMALL_BASE.md. The "With z3-solver installed" phrase is gone.
- Targeted re-review (adversary, appended to gc_mixed_bridge_adversary.md): **P1–P5 all
  closed; verdict `1` (no new issues).** The rewritten audit was attacked line by line —
  corner completeness of the bilinear substitutions, 300 random integer points on the
  determinant identity, independent re-derivation of all four gap polynomials and derivative
  bounds coefficient-by-coefficient (confirming no missing terms), and mutation tests (dropping
  the 6r term or flipping a sign is caught by the cross-check). Both INFO hardening suggestions
  (R1 comment on the illustrative micro-loops, R2 extending the polynomial↔arithmetic
  cross-check to e=40,80) were applied and re-run: verify_bridge.py all PASS with round-1
  outputs verbatim; audit_bridge.py 8/8 EXACT; verify_source_prefix.py unchanged and passing.
  One residual INFO (non-blocking) on P4 wording: 857036 is a word entry rather than an
  above-cap output in the §3 sense.
- Panel state after the patch round: unanimous `1` from round 1 stands, all patch items
  closed, no open defects. Acceptance, CHECKPOINT entry and commit remain with the user.

## Follow-up correction to P1 (2026-11-22)

The original P1 corner loop used β endpoints 0 and 1, and its targeted
recheck sampled the same interval. Both missed the lower output at
(α,β)=(1,2). The corrected audit enumerates the closed box with
β endpoints 1 and 2 and asserts both exact output extrema, 1 and 2.
The targeted recheck now checks all four (α,β) corners explicitly and
samples β over [1,2]. The gap-polynomial docstring now states D≥0
and identifies its minimum at the invariant boundary.

The audit, targeted recheck, mixed-word base and source-prefix scripts
all passed after correction. Two in-memory mutations were rejected:
restoring the old β endpoints, and replacing the update by 2−3αβ/4.
This follow-up was performed by Codex after the GLM panel review.
