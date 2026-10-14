# Invariant Checkpoint — `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`

HALT = F reading 0. Source: bbchallenge 815 holdout list (user-supplied candidate #1).

> **CURRENT STATUS (2026-10-13): UNDECIDED.** This file is an append-only log; earlier sections
> (e.g. "in progress", "PENDING", "CLAIMED NON-HALTING") are superseded by later ones. Audited:
> reduction; no halt for top steps n < 2^2001−2; conditional Theorems R (work_g6) and M (work_m);
> universal walk F defined and non-halting for s < (2^K′−4)/3, K′ = 2^(2^(2^499997−3)−2) (work_el, work_tie, work_tie2). Global non-halting
> is open — see the last two sections and work_r10/ASSEMBLY.md (GLM's conditional tree).

## ACCEPTED: Reduction Theorem (Stage 3 passed)
Files: `work_r1/RULES.md`, `work_r1/verify_r1.py`.
- Encoding: (h; r1..rk) = `0^∞ 1^h [0]_A 1^r1 0 … 0 1^rk 0^∞`.
- Rules R1–R5 and HALT pattern (0;1,0,r3,…), proved for all parameters; invariant I includes the clause k=1 ⇒ r1≥2; the coverage lemma is exact.
- Base: blank tape reaches (0;3) at t=5. This is the single Class-B item.
- Top map L=(A,b,c,S):
  - A even → (A+b+c+3, S).
  - A odd → odd chain on m = b+(A−3)/2.
- **Halt ⇔ some top step has A odd and A+2b+3 a power of 2.**
- Sum invariant ΣL_n = 3n+3; therefore single-element lists never halt.

## Review trail
- Adversary: fixable gaps (I-K1, DOM, H-EQ).
- Auditor 1: all correct (281,892 rule checks; 67,067 coverage configs).
- Auditor 2: all correct (119,999 top-map cases incl. 11,321 halting; sum invariant to n=10^6; raw TM to 3.1·10^6).
- Patched; targeted re-review: **closed in all states**.

## Open
Non-halting ⇔ A+2b+3 is never a power of 2 at an odd-A top step. Path R4 (inductive closed form for L_n) is in progress.

## Class-C evidence
- No halt for 10^7 top steps (≈1.3·10^21 TM steps).
- Odd-A events occur in nested residue families (n≡33 mod 64, 3 mod 512, 7 mod 8192, …).
- In every observed case X = 2^v·u with u odd and u > 1.

## FINAL ARBITRATION — #1 CLOSED AS FAILED (UNDECIDED)
- R4 (work_r4/PROOF.md): singletons never halt; excursion entry E(w,v) closed form; Lemma E(v) symbolic for v≤2000 ⇒ no halt for top steps n < 2^2001−2. Self-tagged Class-A; NOT Stage-3 audited.
- R5 (work_r5/PROOF.md): generalized F(s) [A, s≤1000]; Lemma R / Corollary M(s') [A, by hand]; F′(s) odd-Z₁ variant [A, s≤300]. Residual gaps G1 (margin bound p(s)), G2 (end-phase with odd perturbed entry at Z′₂…), G3 (initial phase) unclosed.
- Exact residual: end-phase statement ⇔ F(s) ∀s ⇔ E(v) ∀v ⇔ non-halting. Assessed as 2-adically insulated (not Collatz-like) but the recursion never closes into finitely many cases.
- Pre-declared closure rule applied: one final push permitted, gaps remain ⇒ archive. Status: UNDECIDED.

## Reopened attempt R6 (work_r6/) — no closure
- No new Class-A results. Simulation results (no halt n<3·10^5; residue table; near-halt locations) are Class-C (self-tagged B, regraded).
- Simple 2-adic invariant (c) refuted: x=A+2b+3 ≡ 0 mod 2^k occurs for all k≤8, so congruence-only invariants cannot work.
- Near-halts with odd part q≤7 occur only at singleton steps n=2^k−2 (proved non-halting); elsewhere q≥9 observed. Lead: an invariant bounding the odd part of x below, away from singletons.
- Approaches (a) symbolic-v and (b) binary closed form not executed (no viable induction hypothesis found).
- Residual unchanged: Lemma E(v) ∀v>2000 ⇔ R5 gaps G1/G2/G3. R5 judged it "not Collatz-like"; R6 judges it Collatz-like/open — assessments diverge; status remains UNDECIDED.

## Attempt R7 (work_r7/) — odd-part invariant, no closure
- Exact q at singleton steps: q=3w [A]. At Lemma-R steps: q = 3H/2^{s'} + (d+3)/2^{s'} ≥ 7 when j>s' [A by hand, depends on unaudited R5].
- Inside E(w,v), v≤1000: q affine in u with β≥19 [A per v; no new range beyond R4].
- Refuted (C): odd-modulus congruence conditions on x (16 moduli) — residues insufficient; bound must be size/valuation-based.
- Conjecture C7 [C]: at every non-singleton odd step, v2(x) ≤ ½·log2 x (observed min q=19, q ≥ 1.54√x, n<3·10^5).
- "q≥3" not inductive alone; closing it requires exactly R5 gaps G1 (margin j>s') + G2 (nested/end-phase steps).
- Status unchanged: UNDECIDED. Four consecutive paths (R4–R7) converge on the same residual.

## Stage 3 on R4 finite-range theorem — ACCEPTED
- Adversary: `1. closed in all states` (singletons, excursion entry incl. v=1/v=2/w=1 edges re-derived by hand; stop_sym decisions uniform ∀u≥0; RULES §5 fidelity; bound v₂(n+2)≤2000 with no off-by-one).
- Auditor 1: `1. all correct` — independent symbolic executor, v=1..2000, no abort/halt, ℓ(2000)=1780; concrete orbit n<10^6 (339,503 excursions) matches decomposition.
- Auditor 2: `1. all correct` — 204,900 concrete runs (v≤60, adversarial w up to 2^200); min odd part of A+2b+3 = 19; raw TM vs top map first 52 configs.
- **THEOREM (audited): the TM does not halt during top steps n < 2^2001 − 2.** Lemma E(v), v≤2000, is a mechanical certificate (verify_r4.py check1, independently reproduced). Base: RULES.md (audited).
- Note: TM-step equivalent is t(2^2001−2) via exact RULES §5 step costs (≈1.35n³, i.e. ~10^1806 TM steps); no explicit number certified.
- Global status: UNDECIDED (Lemma E(v) ∀v open; gaps G1/G2).

## Attempt R8 (work_r8/) — compositional + template; reviewed (1 adversary + 2 auditors)
- Compositional prover (verify_r8.py check1–4): F(v) re-proved for v ≤ 1000 with verified
  contracts via macro-recursion; structure over 153,558 nested calls: a(s) ≤ 2, margin
  v₂(H)−v₂(d+3) ≥ 3 for t ≥ 1 (G1 measured, never assumed), d−(3t+1) ∈ {0} ∪ neg-odd,
  windows = clean + [J] + Z only, ell ≤ 1.08v. **Auditor 1 (independent re-implementation,
  v ≤ 150 + from-scratch template on 5120 starts): all correct.**
- Template engine (check5/5b): 16,896 + 28,160 multi-symbol runs, 0 failures, lineage
  residue classes closed {0,−1} ∪ {−2 mod 2^7} **for the r ≥ 2 deep branches occurring in
  real excursions**. **Adversary REFUTED the original closure claim**: the deep branch
  does not simulate children, and the product family contains halting members
  ([2301,2048,4095] → HALT t=8108 past the contract singleton; 142/240 sampled at ρ=253).
  Counter-verification: ALL halting members found (104/104 in check5c, incl. every re-tested
  3|H instance) have sum ≢ 0 mod 3 — excluded from the real orbit by the audited sum
  invariant (sum = 3n+3); 520 sum-valid instances: 0 halts ≤ 5000 steps. **Auditor 2**
  reproduced V1–V3/V5 from scratch (margin min 3; windows clean+[J]+Z; 27,648 concrete
  runs 0 halts, shape (w,j)-independent) and found: (i) the −2-generator family contains
  r ∈ {0,1} deep branches with out-of-family children (classes ≡ 1, −3 mod 2^7; 48
  instances; real excursions v ≤ 400 have none — all 1236 deep fires are r ≥ 2);
  (ii) the 2816 glue-start runs are vacuous (match at t=0). Corrected scope:
  check5 = 2-adic non-obstruction; check5c = sum-class separation; glue starts dropped.
  Remaining for ∀v: (L-sum) mod-3 constraint in the symbolic family; (L-coverage)
  level-decreasing induction with child-prefix coverage (family extended/excluded per
  auditor 2); (L-middle) ell ≤ 2s bound.
- Convergent independent routes (scratch/): agent B — universal closed-form event sequence
  x = 9·2^p·w + (6k+4) with universal (Δk,Δp) table, self-similar replay with decreasing
  parameters, 41 endgame templates, ell(v) = 2k_b+e, E(v) ∀ v ≤ 12·2^1194 (residual: one
  locality step of the j-induction); agent C — master law x = αw+γ, v₂(γ)<v₂(α), affine
  exclusion lemma PROVED, 374,114 fire families v ≤ 1500 (residual: preservation induction
  + room invariant i ≥ t+2); agent D — raw-TM re-derivation of R1–R5/coverage/halting
  criterion/E(v) v ≤ 100: all PASS (margin claim holds ∀t ≥ 1; the t=0 "margin −2" is the
  start, where the head is even).
- Status: UNDECIDED; R4 theorem unchanged. Non-halting [Class-C], now with three routes
  each reduced to explicitly stated finite/by-hand lemmas.

## Attempt R9 (work_r9/) — CLAIMED COMPLETE PROOF (universal-replay route); coordinator-reviewed, PENDING BLIND AUDIT
- Route (scratch/agentB_closedform.md, second pass): one universal (p, k) sequence
  governs every run-chain at every nesting level: x = 3·2^ρ·U + (6k_ρ+4), j = 1+v₂(3k_ρ+2),
  u ≥ 9; locality by queue-determinism (L0); ρ-induction (k_ρ ≤ ρ³ ⇒ j_ρ < ρ; U odd at
  every level ⇒ tie-free); ell(v) = 2·k_b(v) + e(v); assembly ⇒ Lemma E(v) ∀v ⇒ the
  machine never halts.
- Review status (scratch/review_B_coordinator.md): 6 adversarial probes + coordinator
  code-audit + two cross-route reconciliations (R8 compositional; agentG fire table —
  identical universal object). Findings: 3 wording-level gaps (mod-3 "superset" overstatement;
  "generically" should say margin-protected/on-sequence — planted halters exist only in the
  never-claimed small-p off-sequence region, unreachable; e ∈ [0,12] → e ≤ 16 at the
  v=6132–35 j=14 boundary). j-extension probe: per-J verifier OK to j = 20000. Anchors
  re-executed: invariant ρ ≤ 20000 (6372 events, 0 failures), ell ≤ 2s to 6500, room
  j−t ≥ 2 at v=4000 w∈{1,3}, extreme-w universality, conservation to p=4·10⁵.
  **Blind-auditor pass NOT run (infrastructure failures killed repeated attempts).**
- work_r9/verify_r9.py: anchor driver (checkA/D/E/C) — all green.
- Global status: **NON-HALTING CLAIMED** [Class-A route with machine anchors; audit
  incomplete]. If the blind audit confirms, #1 closes as PROVABLY NON-HALTING and the
  R4 finite-range theorem is superseded.

## FINAL AUDIT of R9 — ALL THREE REVIEWERS PASS (2026-10-13)
- **Blind auditor 1** (scratch/blind1_report.md; from-scratch re-implementation, no access
  to the artifact's code): C1 step closed form (10^5 orbit steps vs the literal loop,
  0 mismatches), C2 universal sequence (18 runs w ∈ {1,3,5,7,2^31−1,10^12+1} ×
  v ∈ {300,1000,2000}: 6276 events + E(·,20000): 6371 events, ALL levels, 0 mismatches),
  C3 per-J table + class verifier (j = 1..30, 0 refusals/splits), C4 ell formula
  (v ≤ 3000, e ∈ [1,12]). **"all correct"**; one artifact finding: two transposed entries
  in the §3 j-row (p/k rows and the transition table are correct).
- **Blind auditor 2** (scratch/blind2_report.md; from-scratch, cross-validated against a
  fresh R1–R5 macro implementation): S1 queue-determinism (10^4 pairs, 0 mismatches) +
  spike prefix universality (divergence exactly at the defect D, as claimed), S2 non-run
  fire census (2,006 excursions: run 640,108 / seam 32,037 / tail 607 / zero 2,006;
  min u = 3 at the analytic zero-fire, run min 73; affine x = α·w+γ with v₂(γ) < v₂(α)
  at 670,412 fires, 0 violations; ⇒ u ≥ 3 for all odd w, spot-verified to w = 31),
  S3 universal invariant + decrease (j < ρ EVERYWHERE, k ≤ 0.4465ρ, nested sequences are
  universal prefixes, tables match), S4 assembly (fire families complete; margin
  arithmetic exact; nested decrease 0 violations). **No mathematical error found.**
- **Final adversary** (scratch/final_adversary_report.md): **STANDS WITH GAPS — no
  mathematical or implementation hole**: 6372/6372 exact replication, fire-for-fire
  identity with the symbolic walker, 5.44M top-level fires v ≤ 6000 zero failures,
  occurring-j = {1..13}(+14 at v ≥ 6132), chain census clean, dp ≥ 2 evidence extended
  to j = 30000, ρ-induction well-founded non-circular. Findings: F1 (nesting depth ≥ 3
  never occurs on-orbit below v ≈ 6·10^7; covered by L0-justified synthetic hops —
  222/222 — and the per-J verifier at j ≥ 28), margin-900 inert (required −3), plus
  the documentation errata also found by the auditors.
- **Verdict: the R9 non-halting theorem is AUDITED** (one adversary + two blind
  auditors, all re-implementing independently; AI-agent review, not peer review —
  per this repository's standing caveat). Residual documentation errata to fix in
  agentB_closedform.md: §3 j-row typos; mod-3 superset overstatement; e ≤ 16;
  "sum forces progress" → pointer monotonicity; margin wording.
- **#1 GLOBAL STATUS: PROVABLY NON-HALTING (audited).** The machine
  `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` never halts. R4's finite-range theorem
  is superseded. Five prior attempts (R4–R8) are archived with their roles in the
  final assembly (R4: base certificates; R8: compositional cross-route + sum-class
  separation; R5–R7: the residual analyses that guided the route).

## G6 GAP ANALYSIS (external, 2026-10-13) — CONFIRMED; R9 status downgraded
An external review (D:\math_cc_g6\PROOF_G6.md, read-only; its verifier re-run here, all
checks pass) identified a real gap in the R9 write-up's rho-induction, independently
CONFIRMED by the coordinator:
- **The "finitely many interlude/exit types" step is false as stated.** Exit chains
  reading the host D have parameter j_D = 1+v2(3K+4) — measured up to 11 (m < 3000;
  coordinator's own run: 755 D-fires, max j_D = 11 at m = 770), unbounded along the
  class — and each spawns a nested cascade with a NON-STANDARD tail. Exit-inside-exit
  depth keeps generating new scale shapes (denominators 8, 32, 128, ...; first new
  shape at level index n = 6134, from the j = 14 spike at rho = 6130 whose chain trace
  is [(R,4)j=1,(R,7)j=4,(R,11)j=2,(D)j=5,(d)j=1] — re-derived here independently).
  This is the same event region as the ell anomaly e = 13..16 at v = 6132–6135.
- The per-J verifier does NOT verify by type enumeration (it runs the full interlude
  symbolically, covering nested exits), so the verified range (j <= 20000,
  index <= 4·10^5) is sound; what fails is the write-up's argument that the induction
  closes for ALL j. The final adversary had flagged exactly this residual ("verifier
  totality for all j; k <= rho^3 asserted not derived") — the coordinator under-weighted
  it when recording the audit as passed. Corrected here.
- **G6's positive contributions** [Class-A]: Prop 1 (s = 2·dk, dp >= 2, ell = 2·k_rho
  from the sum lemma); Prop 2 (dk = K + e/2 decomposition); Prop 3 (the D-fire formula
  j_D = 1+v2(3K+4), x_D = (39/2)P + 9k + 6K + 14); Prop 4 (k_rho <= rho^2 conditional);
  and the §4.3–4.6 REFORMULATION: margin-safety (v2(lambda_x) < v2(c_x) => u >= 2U+1,
  no halt, decisions U-independent) reduces everything to ONE margin inequality
  (M) v2(c_x) > log2(6s+5) on the single parameter-free universal walk — verified
  symbolically to index 4·10^5 (deficit <= 14, s ~ 0.9i), NOT proved for all i
  (equivalently: (M1) deficit <= C·log i, (M2) s <= i^C).
**REVISED STATUS: #1 = CLAIMED NON-HALTING with a precise residual.** All finite
ranges verified (j <= 20000, rho/walker index <= 4·10^5, v <= 6500, w extreme); the
all-v step requires (M) or an equivalent control of the exit-inside-exit depth.
The R9 theorem package remains as the claim record with this CHECKPOINT entry as the
governing status.

## External review of G6's reformulation by GPT Astra (2026-10-13) — "2. with fixable gaps"
Reviewer: GPT Astra (gpt-6-astra via Codex CLI, read-only sandbox); full text archived at
`reviews/astra_theoremR_review.md`. Coordinator (Claude Opus 5.5) numerically confirmed
defects 1–2 for U ∈ {3, 5, 1001, 2^61−1}.
1. (M) as literally stated fails at the first chain: x = 48U+10, v2(c_x) = 4 < log2 17.
   The chain is safe (v2(λ_x) = 1). Repair: verified finite prefix, then (M).
2. **The small parts do NOT follow the ordinary top map** (critical): the second fire has
   x = 384U+16 (real chain u = 24U+1, safe) but λ_x = 16 is a power of 2, so the plain
   top map on λ would HALT. A formal tagged λ-update is required.
3. Full simulation invariant (integrality, parity, stack length) unstated.
4. Crossing classification omits an original-entry partner.
5. §4.5 "iff" is false (algebraic counterexample); only "unequal valuations ⇒ margin" holds.
6. Progress does not imply clean re-entry; a Return Lemma is needed. dk ≥ 1, dp ≥ 2,
   k_ρ = s_ρ/2 are conditional on it.
Consequence: the reduction "everything ⇔ (M) on one integer orbit" is NOT yet valid as
written. G6 is repairing Theorem R (D:\math_cc_g6, §5). **#1 status: non-halting
UNPROVED; the conditional theorem itself is under repair.**

## Repaired Theorem R (work_g6/PROOF_G6.md §5) — ACCEPTED as a CONDITIONAL theorem (2026-10-13)
- Stage 3: adversary (Claude) `1. closed in all states`; blind auditor 1 (Claude, own R1–R5
  implementation, 9 values of U incl. 2^61−1 and 200-bit, full base i ≤ 20000, analytic proof
  of the margin inequality) `1. all correct`; auditor 2 (GPT Astra, `reviews/astra_theoremR_repair_review.md`)
  `1. all correct` — its own defects D1–D5 FIXED, D6 PARTIALLY FIXED (Return stays a hypothesis).
- **Theorem (audited, conditional).** Formal pair map F (values c·U+λ; defined under (S1)
  v2(λ_x)<v2(c_x), (S2) c_A even) simulates the universal walk exactly for every odd U;
  Σc=2^i, Σλ=3s+1; level fires are clean and satisfy I(ρ): x=3·2^ρ·U+6k_ρ+4, k_ρ=s/2 —
  universality PROVED. Base: F defined at all states i ≤ 20000 (symbolic, every odd U).
  If (M1′) v2(c) ≥ i−⌊log2 i⌋² and (M2′) s ≤ i² hold at every F-state with i > 20000, then
  F is defined forever, the universal walk never halts, the pointer progresses, k_ρ ≤ ρ²/2.
- **Scope (do not misread):** this is about the idealized universal walk. It does NOT by itself
  prove the TM never halts: real excursions equal F only until the defect at v−1 is read;
  Return (another level fire / canonical re-entry) and the endgame remain open.
- **#1 STATUS: non-halting UNPROVED.** Open obligations: (M1′), (M2′) for i > 20000; Return;
  endgame audit. Data (C): max deficit 16 vs allowance 144; s/i² ≤ 0.25.

## work_m (M Agent) — ACCEPTED after local patch (2026-10-13)
- Stage 3: adversary (Claude) `fixable gaps` (T1 wording only; T2 = R10 defects, see work_r10 §9);
  blind auditor (Claude) `all correct` (copy lemma 6690 windows; σ-recursion; λ-certificate to i=10^8,
  30.3M epochs, r ≤ 2; per-J exits J ≤ 19999); GPT Astra `simple errors` (reviews/astra_work_m_review.md).
  Patched (6 items) → targeted re-review `fixable gaps` (half-open window convention; one Class-C tag),
  applied by coordinator with the reviewer's prescribed content. ACCEPTED.
- **Audited results:**
  - **Unconditional finite horizon:** F is defined and the universal walk never halts for all
    s < (2^{10^6} − 4)/3; (M1′), (M2′) hold literally there. (Class-A argument + Class-B per-J
    certificate J < 10^6, tie-free.)
  - **Theorem M (conditional):** if (EL) every epoch with ρ > 10^8 has ≤ ⌊log2 ρ⌋² exit chains, then F is
    defined forever, s ≤ i², deficit ≤ (log2 i)³ ⇒ all conclusions of repaired Theorem R.
  - Exact structure: call/return copy lemma; crossing types a/b/c; epochs; σ_{t+1}=σ_t−1−ε(j_t−1).
- **Open:** (EL_J) for J ≥ 10^6 — tie-free symbolic exit with ≤ ⌊J/2−1⌋² exit chains; plus Return
  and endgame for the real machine. #1 non-halting remains UNPROVED.
- R10 (GLM): "A1 essentially closed" withdrawn (work_r10/PROOF.md §9); Lemma K valid for level fires.

## work_el (EL Agent) — Stage 3 IN PROGRESS (2026-10-13)
- Claims: Theorem A (exit = exact automaton on (j, θ=(3s+5) mod 2^j); b/c-steps drop j by ≥3;
  a-steps descend iff (NT) θ_t+3k_n ≢ 2^{n−1} mod 2^n); Lemma T (tie-freeness ⇔ margin with ρ→J);
  Theorem B (NT at all a-steps ⇒ r ≤ J−4); Theorem D + Cor. E: (EL_J) for 10^6 ≤ J < T₁=2^499998,
  r ≤ 4 ⇒ universal walk defined / no halt for s < (2^{T₁}−4)/3.
- Adversary (GPT Astra, reviews/astra_work_el_review.md): `2. with fixable gaps` — Theorem D and
  Cor. E SURVIVE (no omitted case, no circularity). Patch list: (1) Theorem B must add the margin
  argument via h_t = J−Γ_t−j_t (with (C1)); (2) Theorem A scope: "provided every a-step satisfies NT";
  (3) §5 printed state set has 29 pairs — remove (4,3), (20,2); (4) cite V2's τ(n) ≤ n for d_4;
  (5) Lemma T boundary case β_x ≤ 6d_t−1 < 2^{J−Γ_t}; NT is sufficient, not necessary.
- PENDING: patch + two blind auditors. Until then work_el is NOT audited; finite horizon of record
  remains s < (2^{10^6}−4)/3 (work_m).

## work_el — ACCEPTED (2026-10-13)
- Auditor 1 (codex, blind): `simple errors` (27/29 count only) — Theorem A identities 0 mismatches on the
  real walk i ≤ 2·10^5; automaton J < 2·10^5 no NT failure, r ≤ 2; Lemma C 908,625 checks.
- Auditor 2 (codex, blind): `simple errors` (same count) — independent exact F to X(10^6); all (j,2),(j,0),
  j < 10^6, plus 27 route-c states: no NT failure, ≤ 3 further chains (r ≤ 4); Lemma T 669,099 chains;
  no circularity; Cor. E arithmetic correct.
- Patch (codex; 6 items incl. Theorem B margin argument via h_t) → targeted re-review (codex):
  `1. closed in all states`. Reviews: reviews/astra_work_el_review.md, reviews/codex_work_el_*.md.
- **Audited results:** Theorem A (exit automaton, conditional on NT), Lemma T, Theorem B (NT ⇒ EL_J
  under (C1)), Theorem D + **Corollary E: the universal walk F is defined and never halts for all
  s < (2^{T₁} − 4)/3, T₁ = 2^499998** (supersedes work_m's 2^{10^6} horizon).
- **Open:** (NT) for J ≥ T₁ (sufficient for (EL) ⇒ Theorem M unconditional); then Return and the
  real-machine endgame. #1 non-halting remains UNPROVED.

## (NT) attack, two independent routes (2026-10-13) — NOT closed; route assessed as likely dead
- **Claude (work_nt/, unaudited):** Lemma C′ — an a-step ties iff θ̃ ≡ c_n = 2^{n−1}−3k_n (mod 2^n);
  smallest |c_n|: c_4=5, c_7=58, then ≥1012. No θ-window is invariant (largest tie-free window [−1,4];
  each b-step copy of a fire shifts θ̃ by −1, reaching −2 → (17,−2)→(5,5) ties). Residual (R):
  (R5) j=5 ⇒ θ̃≢5 mod 16; (R8) j=8 ⇒ θ̃≢58 mod 128; (Rs) |θ̃|<1012.
- **GPT Astra (reviews/astra_NT_research.md, unaudited):** ancestry potential L (fire leaves in the
  unfolded copy tree), q=2θ̃−3 ⇒ |q| ≤ 2L−1; NT follows from (A3) "L ≤ 3 at every a-step input".
  **Realized negative θ̃:** first J=28 fire at ρ=100296962 has exit (28,1)→b(6,0)→b(1,−1), so the
  empirical invariant θ̃∈{0,1,2} is false for real F. **Conditional obstruction:** with
  B(h)=1+v2(3k_{h−2}+2), B(244875)=B(538715)=B(832554)=17; any realized fire parameter J with
  B³(J)=17 gives (J,1)→bbb→(17,−2)→a(5,5) and an NT failure. If fire parameters occur with
  sufficient position correlation, **NT is FALSE** for real F at large J.
- Note: an NT failure is an unresolved non-descent, NOT a halt — so this kills the (NT) route,
  not non-halting itself.
- **Assessment (coordinator):** both routes converge: (NT) is a statement about the fire spectrum
  and position–parameter correlations of F at unbounded levels (Collatz-type), and may be false.
  #1 FINAL STATUS: non-halting UNPROVED; audited: reduction, finite horizon s < (2^{T₁}−4)/3,
  T₁ = 2^499998 (work_el), conditional theorems R and M.

## work_tie (GPT Astra) — ACCEPTED (2026-10-13): one more tower level
- Claims: (AA) two-a identity + two-step descent; rescue macro (17,σ)→(5,σ−1)→(6,σ−2)→(1,σ−4)→even
  (21 F-steps) resolving the NT-failure tie at (5,5) via higher bits; complete finite entry
  certificate COVER (5,000,063 entries; only NT failures (244875,−1),(538715,−1),(832554,−1), all
  rescued); every fire J < K = 2^(2^499997−2) has a tie-free exit with r ≤ 6.
- Stage 3: adversary (Claude) `fixable gaps` (6 items; COVER complete, no counterexample);
  blind auditor 1 (codex) `all correct` (independent X(n) to 10^6, A0/A1 = 27/46, all 5,000,063
  entries, histogram and the 3 failures reproduced, 300 bigint rescue instances); blind auditor 2
  (codex) `all correct` (logic of §1/§2/§4, certificate reproduced). Patch by commandcode
  (deepseek-v4.1-flash); targeted re-review (deepseek-v4.1-flash) `fixable gaps` (deficit constant
  31→54, not 49; Lemma-T remark; location-lemma wording) — applied by coordinator with the reviewer's
  prescribed content. Reviews: reviews/*work_tie*.md.
- **Audited result: the universal walk F is defined and never halts for all s < (2^K − 4)/3,
  K = 2^(2^499997−2)** (supersedes work_el's horizon). (M1′) holds there with Δ ≤ 65.5+2.5·log2 i.
- Next-level obstruction (recorded in PROOF_RESCUE §4): above K, rescued chains can be copied and the
  automaton's θ rule fails after a non-NT step (true Θ₂ ≡ 46 vs rule 62 mod 64).
- #1 global non-halting remains UNPROVED.

## Level-3 extension: work_tie2 (Claude TIE2) and work_tie_extension (GPT Astra) — REVIEW IN PROGRESS (2026-10-13)
- Both claim: every J < K′ = 2^(K/2−2) has a tie-free exit with r ≤ 7 ⇒ universal walk F defined and
  non-halting for s < (2^{K′}−4)/3 (level-3 certificate, 7,000,101 entries; all ties at (5, Θ≡5 mod 32)
  resolved by keeping higher bits). work_tie_extension's program is adapted from work_tie2's (not independent).
- work_tie2 Stage 3: adversary (Claude) `fixable gaps`; auditor 1 (codex) `simple errors` (NT failures 13,943,
  not 13,949); auditor 2 (deepseek-v4.1-flash) `all correct`. Patched (9 items, commandcode/deepseek);
  targeted re-review pending. work_tie_extension: review not started.
- Trend (C): entry family grows each level (θ window widens by 2; 6 → 35,801 → 60,068 extended records);
  level 4 only conditional; level 5 needs a hidden-k symbolic state. Horizon of record stays K (work_tie)
  until review completes.

## work_tie2 — ACCEPTED (2026-10-13)
- Targeted re-review (deepseek-v4.1-flash): `1. closed in all states` (reviews/deepseek_tie2_rereview.md).
- **Audited result (Theorem TIE2, level 3): every J < K′ = 2^(K/2−2) = 2^(2^(2^499997−3)−2) has a
  tie-free exit with r ≤ 7; the universal walk F is defined and non-halting for s < (2^{K′} − 4)/3**
  (supersedes work_tie's horizon K). Level 4 remains conditional and is not part of the theorem.
- work_tie_extension (GPT Astra, same level-3 result, program adapted from work_tie2): review next.
- #1 global non-halting remains UNPROVED.

## work_global_core (GPT Astra) — ACCEPTED (2026-10-14); work_tie_extension recorded as supplementary
- Audited (reviews/claude_global_core_review.md): exact two-a identity x(t+2)=(x(t)+x(t+1))/2+6(k+l+1);
  **chains with parameter > K(g)=⌈log2(6g²+6)⌉ occur at most two in a row** (no per-step descent needed);
  exit chains ≤ 3m+1 with m = core (low-parameter) visits; **conditional theorem: CORE2 (no
  bootstrap-justified prefix reaches b+1 core visits, b=⌊g²⌋) ⇒ F globally defined and non-halting.**
- CORE2 is equivalent, up to a factor ~3 in the budget, to the old exit-length lemma — a restatement,
  not a reduction in difficulty. Unproved. The real-machine endgame remains a separate open obligation.
- work_tie_extension: patched; supplementary to TIE2 (exact b/c margin gain, bigint kernel checks,
  information-loss construction); same horizon K′.
- work_global_shadow, work_global_compression: unaudited research material.
- #1 global non-halting remains UNPROVED.

## work_claude_global (Claude) — ACCEPTED (2026-10-14)
- Audited (reviews/claude_global_descent_review.md): **"r ≤ 2" is not universal** — the fire J=50,148,477
  has exit (J,27,6,1), r=3, tie-free (independently recomputed twice). Skeleton computation (Class B):
  all J ≤ 4·10^8 give r ≤ 3 (three r=3 cases; the other two rest on the skeleton only).
- Exact first-step formulas: j1=v2(3τ(J−1)+2) (type a, if < J−1), j1=v2(3τ(J−1)+4) (type b); a→a second
  step j2=min(J(τ(m)),m), m=j1−1 (a-type first step only).
- New target **DL (strict descent of exit parameters per epoch)**: inside Theorem M's induction DL ⇒ (EL).
  Covered: t=0, all b/c returns, first a→a. Open: G1 (a→a POS collisions, t≥2) and G2 (a after b/c);
  b-type canonical state unproved. Conjectured picture: r(J) grows like log* J.
- #1 global non-halting remains UNPROVED; endgame gap unchanged.
