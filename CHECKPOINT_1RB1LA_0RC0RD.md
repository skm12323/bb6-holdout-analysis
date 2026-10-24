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

## work_g2 — G2 (b/c→a) partial results ACCEPTED (2026-10-14)
- Audited (reviews/g2_review_record.md): **Lemma A** — after a b-type first step, an a-type second return
  strictly descends: j₂ = 1+v2(k) ≤ q−2 < q, all parameters, no tie assumption (resolves the earlier 38/317
  misapplication). **Lemma B1** — after an a first step every chain-1 b/c return is an exact θ=2 copy;
  **Theorem B** — the tail after such a copy is the suffix of an earlier finished epoch (REDUCTION: needs DL
  or a tail bound for the source; for ρ ≤ 10^8 only the tail-length arm r ≤ 2 is certified).
  **Lemmas C1/C2** — small-offset copies end the epoch except at a collision r = h; offsets δ proved for
  prefixes ∅, a, b, a,a (non-tie), b,a.
- Open: collisions after a b/c prefix (t ≥ 1) and after c-type first steps; offset control after ≥ 3
  returns; G1; endgame. #1 global non-halting remains UNPROVED.

## work_g2_obstruction — DL REFUTED (ACCEPTED, 2026-10-14)
Three-way review: adversary fixable gaps (patched), auditors all correct ×2 (reviews/g2_obstruction_review_record.md).
- Fire-spectrum GAP + BARRIER: every J with J+4<B occurs as an actual fire parameter at time 2T_J.
- Actual epoch (p3,p2,244875,17,5,6,1), r=6 (r≤6 bound sharp), ends safely; 5→6 refutes global DL (G1-type). G2 not unconditionally refuted (12-ancestry 65→5→5 only beyond B).
- Offset invariant {0,±1,−2} fails for one b-copy (δ=−20); proved short-prefix table unaffected.
- Positive: pure-b depths m=1..123 into the parameter-5 source close safely.
- Consequence: DL route to (EL) abandoned; targets are exit-length bounds, correlated core-visit bounds, endgame.

## work_g2_bc_frontier, work_g2_two_blocks, work_g2_mixed_blocks (GPT Astra) — ACCEPTED (2026-10-16)
Review: reviews/g2_frontier_review_record.md (adversary fixable→patched→closed; deepseek and gemini blind auditors all correct).
- Two-block positive identity X2=(alpha/2)X0+(1-beta/2)X1+C for arbitrary b/c mixed prefixes and odd a endpoints;
  0<C<10Q²+18 (pure b) / 0<C<24Q²+6 (mixed) under C1,C2,M2'; two safe entries above the log threshold ⇒ next
  entry safe and back in the core (no three consecutive entries outside it). No core-visit bound.
- Local obstruction: real crossing p=24480 (tau(p-1)=21832) + real fire of parameter p give a compatible (not
  proven reachable) state with arbitrarily high b/a re-ascent. Scope: only epochs with J>=B (excluded below B by
  PROOF_RESCUE §4 and Theorem D). Shows the listed local constraints are insufficient; does not refute COVER-type
  tracking; conflicts with no accepted result.
- Other 10 work_g2_* directories: audited the same day, see next section.
- #1 global non-halting remains UNPROVED.

## Ten work_g2_* notes (GPT Astra, 2026-10-15) — ACCEPTED as conditional/local results (2026-10-16)
Review: reviews/g2_rest_review_record.md (adversary fixable→patched→closed; two blind gemini auditors all correct).
- resonance: parameter-5 source tails closed for all depths except m≡124+2^61 (mod 2^62); pure-b ancestry
  first a-rebound safe with O(log m) retained ancestors (under C1, S1); first odd a-rebound after b/c prefix
  safe with parameter <3log2J+2 (J>=1024; smaller J by certificate).
- after_reset / shift44 / return_block: post-reset tails closed except two k classes mod 2^60 (absent for
  q<=2^29 under C1); depth rule 1+v2(9-m) for m≢9 (mod 16); unresolved block needs q>=16640.
- core_repeats / core_words: equal-parameter repeats end; within core <=1023 no seven consecutive productive
  entries; escapes only from 33 pairs (p=5,8).
- escape_5_17 / reentry_budget / escape_two_phase: (5,17) escape closed except k≡32761 (mod 65536); repetition
  bound for the R21→17 pattern (g<=2^127); two-phase closure for R/E/D families (entries 1024..2^500, first
  resonant output's safety assumed). b/c branch at R21 remains open (= bc_frontier obstruction).
- paths: roadmap; general-d shifted-copy rule stated as an unproved lemma.
- Open: core-visit / escape–re-entry bound, high b/c branches (reachability invariant or cross-boundary
  termination needed), G1, endgame. #1 global non-halting remains UNPROVED.

## Eleven work_global_* notes (GPT Astra) — ACCEPTED (2026-10-17)
Review: reviews/global_astra11_review_record.md (two adversaries fixable→patched→closed; gemini and deepseek blind auditors all correct).
- **work_global_clock (key):** on the maximal defined canonical prefix of F (incl. a first-failure inspection),
  τ(n) <= n·P(n), P(n)=2g(n)²+1345, g(n)=⌈log2(6n²+5)⌉, with NO exit-length, C2 or termination hypothesis.
  Consequently **F is defined forever (universal walk never halts) ⇐ SQRT-EXIT**: every epoch at pointer ρ>10^8 ends
  before ⌊√ρ⌋+1 exit chains. This replaces (EL)/CORE2 by a much weaker target. Endgame still separate.
- failure_budget: exponential-in-J coefficient-loss safety budgets; first-failure candidates finitely bounded.
- root_phase / rescue_ladder / mixed_precision / weight16 / transfer: rooted phase grammar (ε=W+1), rescue ladder
  δ_n=6−8/3^n, mixed-path root-precision budget, conditional safety through weight 18. No all-weight result.
- period / clock_words: repeated mixed-block words need clock divisibility; six-entry alternation excluded at every
  scale; arbitrary-word clock projection and spacing.
- long_witness / ancestry: local word 5,17,5,122436,5,17,5 exists, but its fixed-clock state needs loss ≥244913 and is
  excluded canonically; unbounded clocks open.
- calendar: exact canonical crossing queries (time, type, ε) up to ~2^4096 from certified kernels J<=4096.
- Open: SQRT-EXIT (exit termination within ~√ρ chains), high b/c branches, endgame. #1 global non-halting UNPROVED.

## work_global_calendar_survey (Claude) — ACCEPTED as Class-B evidence (2026-10-17)
Review: §6 of work_global_calendar_survey/NOTES.md (adversary fixable→patched→closed; gemini all correct; deepseek simple errors, patched).
- Canonical projected exits via the accepted calendar: 40000 random J<2^257 and deep targets (first exit parameter
  exactly m, J≈2^m) for m≤4000: all closed, no NT tie, no non-descent.
- Deep-target tails depend only on (type, m) (state after first step is (m,θ=2) for a, (m,0) for b). Scan m≤60000:
  r=3 first at m=27, **r=4 first at a-type m=6131**; canonical instance J (6130 bits) with exit (J,6131,14,5,1).
  No r≥5 in that range. (Not a record: work_g2_obstruction has an actual r=6 epoch.)
- Finite evidence only; no bearing on SQRT-EXIT as a proof. #1 global non-halting remains UNPROVED.

## work_global_endgame — endgame lemmas E1–E5 ACCEPTED (revised), problem statement (2026-10-17)
Review: §7 of work_global_endgame/LEMMAS_E.md (adversary fixable→patched twice→closed; gemini and deepseek blind auditors simple errors, patched).
- LEMMAS_E.md restates work_r10/agentC10_report.md §1 (original unchanged): E1 boundary simulation (defined-prefix form),
  E2 signs (c_A≥1, defect only read as b/c), E3 no halt under S1, E4 mass identities (termination NOT claimed;
  j<=log2(6s+5)), **E5 prefix form: S1∧S2 hold at endgame chain k whenever n−ε(n) > Σ_{i<=k} j_i** (n=v−1).
- PROBLEM_ENDGAME.md: non-halting of #1 needs (i) F safe (⇐ SQRT-EXIT, PROOF_CLOCK) and (ii) EG-SAFE; endgame
  termination is not needed. With E5 + PROOF_CLOCK this reduces to **EG-LEN**: Σj over any endgame prefix < 3(v−1)/4
  (≈ v/log v chains). Rigorous assembly (constants, 4·10^6<v<=10^8 base gap) still to be written.
- #1 global non-halting remains UNPROVED: open = SQRT-EXIT, EG-LEN (+ rigorous assembly).

## work_global_egx (Claude) — EGX ACCEPTED; real-machine horizon 2^{K′}; open list reduced to EXT (2026-10-17)
Review: §9 of work_global_egx/PROOF_EGX.md; reviews/claude_egx_{adversary,auditor1,auditor2}.md (adversary fixable→patched→closed in all states; two blind auditors simple errors, patched).
- **Theorem EGX [A]:** for every v ≥ 3 the endgame of E(w,v) is, at top level and pair for pair, the symbolic exit S(J) of
  PROOF_M Lemma 6.1 with J = v ((c,λ) ↔ (α,β), U ↔ λ_u; the defect (2^{v−1},−1) is D_0, the zero fill is the outer originals).
  Endgame safe ⇔ S(v) tie-free; endgame reaches the singleton ⇔ S(v) ends at an even return; endgame margin = h_t = J−Γ_t−j_t.
  Data: identical for 3 ≤ v ≤ 400,000 (auditor 1, own code); ~29,000 perturbed start states: identity structural.
- **Lemma TR [A]:** the tower proofs' identities hold for S(J) for every integer J (Θ_t := 2^Jλ_u+3d_t+1), not only for fire parameters.
- **Corollary H [A + imported A+B]: the TM does not halt during the first 2^{K′}−2 top steps**, K′ = 2^(2^(2^499997−3)−2)
  (supersedes R4's 2^2001−2 for the real machine; uses V4, EL Theorem D, PROOF_RESCUE §4, TIE2, HORIZON-3).
- **Lemma C2-log [A]:** ε(i) ≤ max(3, 2J_W−1) < 2log2(3i²+4)−1 when the containing epoch is tie-free in S(J_W).
- **Theorem U [A, cond.]:** (EXT) "S(J) tie-free for every J ≥ K′" ⇒ F defined forever and #1 never halts. No SQRT-EXIT, EG-LEN, EL or C2.
  EG-LEN (any V₀ ≤ K′) ⇒ EXT; EXT ⇒ SQRT-EXIT on actual fires. The 4·10^6<v≤10^8 base gap disappears; Theorem U is the rigorous assembly.
- **Theorem L [A]:** LIN-EXIT (≤ ⌊J/(3log2 J)⌋ exit chains in any tie-free prefix of S(J), J ≥ K′) ⇒ EXT; unconditionally, given EXT below J,
  the first ⌊J/(3log2 J)⌋+1 exit chains of S(J) are tie-free.
- #1 global non-halting remains UNPROVED: the single open proposition is **EXT** (same arithmetic core as NT / EL_J; unbounded nesting of fire copies).

## work_global_ext (Claude) — EXT partial results ACCEPTED; EXT below K″; open core = exact ties at deep b/c entries (2026-10-17)
Review: §8 of work_global_ext/PROOF_EXT.md; reviews/claude_ext_{adversary,auditor1,auditor2}.md (no claim refuted; minor fixes applied; adversary re-review closed in all states).
Four routes (reports + scripts in work_global_ext/route_{a,b,c,d}):
- **Theorem U\* [A, cond.] (route d):** over-ties (v2 β_x > v2 α_x) are harmless (Prop 2.1: EGX, E1–E4, Lemma 6.1, T(1)/(2), F margin all
  hold with j := v2 α_x). (EXT\*) "S\*(J) has no *exact* tie for J ≥ K′" ⇒ #1 never halts. Exact ties are genuine obstructions: at a solvable
  first exact tie x = 2^m(γ,μ), infinitely many odd w make E(w,J) halt there (3wγ+μ = 2^k).
- **Theorem RA [A] (route c):** if X(J−1) is odd type a, S(J) is tie-free with no NT/EXT hypothesis (Lemma K classification, HP shadowing,
  AB absorption: a phase-2 state copies a real epoch to its end). EXT reduces to J with X(J−1) of type b/c; Prop RB: those are exact shifted
  copies V(C,−1) of real epochs up to the first real a-step.
- **Theorem L′ [A] (route b):** only non-descents (j_{t+1} ≥ j_t) cost budget: ND-EXIT (≤ ⌊J/(3log2 J)⌋ non-descents per tie-free prefix)
  ⇒ EXT (also EXT\* form). L″: chain budget ≈ J/(4 log2 log2 J). Lemma BR: exact β-only walk.
- **Theorem S + Corollary 4 [A+B] (route a):** level-4 generator redone with exact Ψ-families Ψ(j;P,Q): Θ ≡ P + Q·2^jλ_u (0 failures;
  reproduced by an independent generator). Shallow first return ⇒ S(J) tie-free, ≤ 9 chains, no EXT hypothesis.
  **EXT holds for all J < K″ = 2^{K′/2−2}; the TM does not halt during the first 2^{K″}−2 top steps** (Corollary H″).
- **Theorem O [A, about the method]:** no generator-type finite certificate closes the tower (integer drift + 3-adic orbit
  c_m = −3+8·3^{−m}); level 5 has one failure ('pair',5,5).
- Data [B]: all J ≤ 10^8: no tie, no non-descent, r ≤ 3; deep tails from every (m,θ), m < 10^8: real entries r ≤ 4.
- #1 global non-halting remains UNPROVED. Open: for J ≥ K″ with X(J−1) odd of type b/c and ω(J−1) ≥ K′ (b) or J_W ≥ K′ (c),
  S\*(J) has no exact tie (equivalently: bound climbs inside nested shifted copies of real epochs).

## work_global_clock_horizon — stronger finite cutoff ACCEPTED (2026-10-18; review: reviews/global_clock_horizon_closure_review_record.md)

- New argument in `work_global_clock_horizon/PROOF_CLOCK_HORIZON.md`: combine accepted CLOCK with RA and Theorem S.
  At n=J−1, the exact sufficient filter is `3nP(n)+4 < 2^K′`. For type b it bounds omega; for type c it bounds
  the parameter of the enclosing fire, not merely the current chain. Type a uses RA directly.
- Explicit new cutoff: `K_clock = floor(2^K′ / (64(K′)^2)) > K″` (32 → 64 after review). For T>=64, n<=floor(2^T/(64T²)) implies
  `P(n)<=9T²` and `3nP(n)+4<2^T`; Lemma MASS (added after review) keeps the at most nine chains certified by Theorem S below K′
  (induction along the certificate), the range hypothesis behind Theorem S's level-4 certificate. Proposed consequence: EXT below K_clock; the original machine does not halt
  during the first `2^K_clock−2` top steps, using the accepted finite-prefix EGX/U/H″ assembly.
- Verification: 4,035 exponent cases, 20,175 clock endpoint checks, 8,188 finite real crossings, 2,611 b/c source
  checks, and 4,081 horizon-transfer inequalities; all PASS. All-scale constants have analytic proofs.
- Status: **ACCEPTED after three-way review**; the accepted horizon is now K_clock (was K″). Does not certify level 5,
  change Theorem S's source cutoff K′, or prove global non-halting. The improved horizon cannot be iterated by
  simply substituting K_clock for K′ in Theorem S.

## work_global_closure_attempt — all-scale target sharpened, ACCEPTED as conditional/local results; global proof still OPEN (2026-10-18)

- CAP (accepted): for l=ceil(log2 J)>=64, the first at most J valid symbolic-exit chains have parameters
  <=g=l+2ceil(log2 l)+7, using CLOCK, C1, and the beta mass bound.
- Conditional closure: if every congruence-feasible productive mixed-block word over available canonical sources
  with parameters <=Q has length <=2^ceil(Q/2), for all Q>=64, then CAP and Theorem L's safe-prefix budget imply
  global EXT and non-halting. **The required all-Q word bound is unproved.**
- Targeted exact-lattice search over eight actual pure-A sources found the nine-entry word
  (5,367354,5,17,5,122436,5,17,5). A positive safe pair lift passes nine macro checks (minimum margin 12);
  its last eight entries are a-outputs. The exact fire projection is empty. It is a local continuation,
  not a canonical-orbit witness. Omitted parameter branches are explicitly retained as open.
- 12,105 integer parameter checks and 9,991 finite symbolic exits pass. No global proof, level-5 closure,
  or new accepted horizon is claimed. Details: `work_global_closure_attempt/PROOF_CLOSURE_TARGET.md`.

### Continuation: exact phase-origin filter and 64-source pure-A search (2026-10-18, accepted with the above)

- For a clock cylinder Theta=t mod 2^H, x=pTheta+r mod 2^K (p even, K>=H), an exact initial defect
  c=Theta-x is congruence-feasible iff c=(1-p)t-r mod 2^H. A shifted real fire requires c=1+delta.
- The prior nine-entry word requires |delta|>=2^122438-3244676. This excludes small shifted-fire origins,
  not arbitrary later canonical ancestry or shifted non-fire c sources.
- A 64-source search exhausts 1,050,560 candidate extensions: free maximum 11, fire-compatible maximum 2.
  Other parameters and mixed b/c transitions are outside this finite certificate.
- A longest word (5,17,5,17,661128,17,661128,857036,5,17,5) has a positive safe local pair lift:
  eleven a returns, ten a-output entries, minimum margin 8, next parameter 6. Its true-fire projection is empty.
- 308 general-solver comparisons, 64 independent calendar source checks and 26,832 phase-filter tests pass.
  Global EXT, W(Q), and canonical ancestry of the local example remain open. See `PROOF_ORIGIN_FILTER.md`.

## work_ext_roots — direct EXT entry constraints (2026-10-18; ACCEPTED 2026-10-19, review: reviews/ext_roots_review_record.md)

- ENTRY: at an odd b/c source X(J−1), chain 1 of S(J) has Theta=3tau+4 and x=3tau+4+lambda_Y.
  Thus b has exact defect zero (not the real-fire defect one), while c has defect −lambda_Y from the actual source.
- A word cylinder imposes Theta=t mod 2^H and (1−p)(3tau+4)+lambda_Y=r mod 2^K on canonical source data.
  A one-variable exact solver retains a fixed defect through arbitrary productive mixed b/c corridors and a endpoints.
- Finite selection: all parameters <=8191 plus 35 larger parameters, 2621 productive kernels. At defect zero,
  productive words have length at most two and no branches escape this source selection. Other defects and all
  larger initial parameters are not covered by that statement; no outer physical-margin theorem is inferred.
- For a fixed first-tie word let E be accumulated block loss, q its final parameter, M=E+q and R the previous
  maximum of E_i+q_i. Necessarily M>R. Type b gives R+3<=J<=M+2. Type c at a least EXT counterexample J>=128
  gives J<=2M, using accepted C2-log under EXT below J. Exact source correlation remains to be checked.
- Checks: 2479 b and 132 c full-pair entry identities; 112112 integer endpoint inequalities; 170 comparisons
  with the general word projector. All PASS. Global exclusion of the unbounded candidate-word family is OPEN.
- Details: `work_ext_roots/PROOF_EXT_ROOTS.md`. Accepted K_clock (constant 64) is unchanged.

### Complete last-step filter for a fixed EXT prefix (2026-10-18, accepted)

- For prefix loss E and duration T, a first-tie final valuation is bounded by
  min(max(14,bit_length(48E²+6T+5)), max(19,floor(log2(203E³)))) for a least counterexample J>=128.
  Combined with J<=2(E+q), both final valuation and outer source are finite for each fixed prefix.
- Implemented exact record/cylinder/source/margin/mass filtering. All 504 feasible productive prefixes over
  the 18 kernels in 5..63 were checked; 8064 final-parameter diagnostic checks, no canonical candidates (sources
  were only inspected in the already certified J<128 diagnostic range; for J>=128 no source index is reachable here).
  J<128 diagnostics use a separate mass endpoint rather than misapplying the asymptotic bound.
- Positive control: an invented c source X(9), time 27, H=(64,7), Y=(448,75), passes local mass/C1/safety
  constraints and makes the next S(10) chain (1568,96), an exact tie. It is NOT the canonical source X(9).
  The filter retains this control, establishing that canonical source correlation is essential.
- Fixed-prefix completeness does not bound all prefixes or their loss. Global EXT remains open; no horizon
  change. Details: `work_ext_roots/PROOF_LAST_TIE.md`; verifier `verify_last_tie.py`, all checks PASS.

### Low-deficit c-source reductions (2026-10-18, accepted)

- C3: epsilon=3 forces a source history A. Its outer shifted chain differs from a virtual fire of parameter
  q=v2(6k+2)<P−1 by precision P−1. Assuming EXT(q), HP and the outer coefficient margin imply termination
  and strict safety. Since q<J, this excludes the branch at a least EXT counterexample if the proof is accepted.
- C5-BA: epsilon=5 permits AA or BA. For BA, the exact outer state has phase difference from Theta=x+2
  equal to −5x0/8−y/2, with valuation p−1>q. Earlier real-epoch absorption plus HP closes this whole tail.
  The AA case is NOT covered here (superseded: handled by A-SOURCE below); a zero phase residue alone is insufficient to replace it by an earlier b source.
- Checks: 76 actual A-source and four actual BA-source calendar crossings, 86 shadow states; 18 explicitly
  noncanonical outer algebra lifts with nonterminal references, 36 states; 4087 size inequalities. All PASS.
- Proposed remaining c frontier: epsilon=5 with AA, or epsilon>=7 (superseded below: AA handled by A-SOURCE); b sources remain open. No global EXT claim,
  no accepted-horizon change. See `work_ext_roots/PROOF_LOW_DEFICIT.md`.

### A-initial source ancestry descent (2026-10-18, accepted)

- AA is now reduced to an actual earlier b source: if the first A yields parameter p, the shifted second
  A-output shadows chain 1 of S(p+1) to precision p−1. The two exact scalar differences have valuations p−1,p.
  EXT(p+1), with p+1<J, closes this branch in least-counterexample induction.
- Proposed A-SOURCE theorem (induction on strict EXT): any later c source in an epoch whose first odd return is a shadows a chain in an
  already completed earlier real epoch. AB/HP preserve that chain's coefficient precision. Its b/c crossing
  supplies J'<J; both clocks shifted by −1 still agree, and EXT(J') transfers termination/safety to the outer exit.
- If accepted, this excludes all c deficits 3 and 5, and all A-initial source epochs at arbitrary deficit.
  Remaining c frontier: epsilon>=7, first source return b/c. Outer b entries remain open. This supersedes the
  previous AA-open statement but does not close EXT or change the accepted horizon.
- Four canonical AA comparisons pass in the finite calendar selection; mixed histories are untested. The general mixed-history
  claim depends on the written AB/HP precision proof, not those samples. `PROOF_A_SOURCE_DESCENT.md` (accepted).

### Deficit-seven source frontier (2026-10-18, accepted; MINUS/PLUS families unproved)

- Weight grammar gives exactly AAA, ABA, BAA, BBA, CA. A-SOURCE covers AAA/ABA. New CA descent uses the
  copied deficit-three source's actual A history and shadows a virtual fire of smaller parameter q; EXT(q)
  closes it in least-counterexample induction. A canonical outer source with root parameter 6133 and a
  6134-bit EXT index was verified exactly (inner parameter 14, intermediate 5, reduced 3).
- BAA and BBA reduce to correlated reference families MINUS(m): (x,Theta)=(6k_m+6,6k_m+5) and PLUS(m):
  (6k_m−2,6k_m+1), where k_m=tau(m−1)/2 at an actual odd a crossing. Their required bound is
  j+relative loss<m−1 through termination. This all-scale family property is NOT proved.
- Each family passes 302878 sources below 10^6 and 3024 deeper canonical calendar cases; 240 additional
  explicitly noncanonical outer algebra lifts verify the normal forms. Deep cases disprove the naive
  extrapolation that PLUS always ends immediately. No actual tie or global closure was obtained.
- See `work_ext_roots/PROOF_DEFICIT_SEVEN.md`. Outer b entries and higher c deficits remain open;
  the reductions are accepted (review record above); the accepted horizon is unchanged.

## Duration normalization of MINUS/PLUS (2026-10-19; ACCEPTED, review: reviews/ext_roots_duration_review_record.md)

- New predecessor lemma: a MINUS/PLUS entry of parameter >=5 immediately follows an actual epoch H>=5.
  All 15 small-kernel residues exclude these landings. Delta_H=5 mod16 for MINUS, or 1 mod16 for PLUS.
- Subtracting the predecessor fire numerator 2^H U from both x and Theta gives exact precision H.
  References: D_MINUS=(6Delta_H+2,6Delta_H+1), D_PLUS=(6Delta_H−6,6Delta_H−3), with initial parameter <H.
- Smaller EXT(H) supplies Delta_H<=H^3. HP transfers termination if the new reference satisfies
  j+loss<H throughout. This all-scale property is OPEN: D_ROOT is not S(H), so no closed induction is claimed.
- Checks: 15 residue transitions; 653 direct and 28 deep predecessor cases; 458 MINUS and 461 PLUS
  duration cases for H<=8192. All PASS. No global EXT closure or accepted-horizon change.
- Details: `work_ext_roots/PROOF_DURATION_NORMALIZATION.md` and `verify_duration_reduction.py`.

### Duration-reference branch closure (2026-10-19, accepted)

- Generic PLUS state Theta=x+3 with initial parameter q and ceiling C>q: an odd b return lands within
  precision q−2 of an exact-phase-two reference. AB and HP close the entire branch, with all records <=q.
- Generic MINUS Theta=x−1: b copies of fire parameter 5 or 8 have exact words (q,5,1)/(q,8,3); every record j+Λ<C
  for any ceiling C>q. Sections 1–2 apply directly to the original PLUS(m)/MINUS(m) states (C=m−1), not only to D-ROOT.
- PLUS a returns reduce to Z(q)=(6k_q+6,6k_q+6) at precision q−1. Z's all-scale margin/termination remains
  open; equal defect zero is not enough to identify it with an actual b entry. PLUS c and other MINUS cases remain.
- Genuine S(H) duration kernels at H=13784707579437011870 (MINUS) and H=41354122738311035613 (PLUS) give
  word (65,5,1) (the corresponding MINUS/PLUS entries are hypothetical). They refute a universal two-parameter shortcut, not safety. Both are analytically covered above.
- Checks: 7437 PLUS b lifts, 387 selected MINUS b lifts, 7437 finite PLUS a-to-Z lifts, 508 beta-evaluator
  cross-checks (same oracle), two exact large-index duration witnesses; all PASS. See `PROOF_DURATION_BRANCHES.md`.

### Open next steps proposed after the work_ext_roots review (Claude, 2026-10-19) — not yet done
Proposed after commit 5119184: (1) outer type-b entries, (2) all-scale MINUS/PLUS, (3) ε>=9 grammar convergence.
The duration work above (GPT Astra, accepted 2026-10-19) addresses (2) only partially. Still undone:
1. **Outer type-b entries** of a least strict-EXT counterexample: not touched by any note. Natural attempt: the
   same shadowing/ancestry framework as A-SOURCE, starting from ENTRY (b defect 0, Θ=x=3τ+4) and Lemma K(b).
2. **MINUS/PLUS remainder**: Z(q)=(6k_q+6,6k_q+6) all-scale margin/termination; PLUS c returns; MINUS b copies of
   fire parameters other than 5, 8, and MINUS a/c returns; the D_ROOT references' all-scale property j+loss<H.
3. **Convergence check for c deficits ε>=9**: enumerate the weight grammar at ε=9,11,… and test whether every new
   word reduces (A-SOURCE / CA-type descent) or new reference families keep appearing; i.e. whether this route
   can close at all, or needs a uniform argument instead of deficit-by-deficit casework.

## work_claude_ext_next — defect calculus (Claude subagent) — ACCEPTED (2026-10-19)
Review: reviews/claude_ext_next_review_record.md (adversary fixable→patched→closed; gemini and deepseek simple errors, patched).
- Defect d=Θ−x; SHIFT lemma and automaton (fire d=1; A: d→3−d; B: d→d−1; C(w): d→d+Φ(w)−2). Under the descent
  hypothesis DH: every c-source history reduces to one family G_δ(p)=(6k_p+4−2δ,6k_p+4−δ), δ=Φ(w)−1, closed for
  δ∈{0,1,2}; P2 (an intermediate chain with d=2 excludes the source) generalizes A-SOURCE (= P2 at i=1, unconditional).
  C3, BA, AA, CA, MINUS (G_{−1}), PLUS (G_3) are special cases.
- Item 3 answered: the deficit-by-deficit route does NOT converge (Catalan word counts; two new open δ per deficit,
  [A-sketch]); all open families merge into G_δ/H_δ, H_e=(6k+6−2e,6k+6−e).
- Item 1 (outer type-b entries): EXT(ω) transfers through the copied fire's b/c returns; under DH, DH_out the only
  residue is when that exit ends at its first a-step, giving H_{4−d}(m) (main case H_3, same class as PLUS).
- **Remaining target (replaces the casework):** a uniform theorem that shifted real chains (δ∉{1,2}, G_δ/H_δ) end with
  record below their precision, plus DH at all scales. #1 global non-halting remains UNPROVED; K_clock unchanged.

## work_claude_shifted — shifted chains are θ̃-walks (Claude subagent) — ACCEPTED (2026-10-20)
Review: reviews/claude_shifted_review_record.md (adversary fixable→patched→closed; gemini all correct; deepseek simple errors, patched).
- The defect calculus is PROOF_EL's θ̃ automaton; DH weakens to PROOF_EL's NT (Lemma 1.3: a resonant one-step descent
  keeps the record), except at DR's final letter and OB's DH_out.
- The previous target "no non-descent in shifted copies" is FALSE: the accepted WITNESS epoch yields H_5(17) with a real
  5→6 non-descent (records stay below precision). Correct target: records below precision, ties resolved.
- Theorem SC; gateway-tie lemma (b/c extension of PROOF_RESCUE's two-a lemma); finite certificate to index 2·10^7,
  defect window [−12,15], only (5,5),(5,−11) uncertified [B]; Theorem W: X(J−1) odd c, ω(J−1)<2·10^7, −λ_Y certified
  ⇒ S(J) tie-free (no EXT below J, J_W or DH needed).
- **Remaining sufficient condition DEEP:** on the deep segment of S(J) (parameters >= 2·10^7; ~log* J chains when
  θ̃≠−3k_j) the θ̃ drift stays bounded and the first chain below 2·10^7 lands in the certified set. Suggested routes:
  a uniform gateway-tie lemma for deep predecessors with avoidance of the sparse uncertified classes; a calendar-arithmetic
  bound on consecutive deep b/c copies. EXT open; K_clock unchanged.

## work_deep — structure of the deep segment, sharper remainder for DEEP (external ZCode agent) — ACCEPTED (2026-10-20)
Review: reviews/deep_review_record.md (Claude adversary fixable→patched→closed; two agy gemini auditors simple errors, patched).
- Deep-segment trichotomy (no NT failure when j>=N₀=2·10^7 and |θ|<=B=2^{10^7}); resonance isolation (deep segment
  <= 2Λ+1 chains); landing defect class known mod 2^{j+1}; Λ(K_clock)=4 (tower bound Λ(J)<=h for J<T_h).
- For every J < T_{⌊(B−4)/6⌋} (covers the K_clock scale): EXT(J) ⟸ R1 ∧ R2, R1 = no deep→deep c-step (a c-step at a
  deep chain with ω(j_t−1)>=N₀, needs τ(j_t−1)>=(2^{N₀}−5)/6), R2 = landing class certified. Above that range DEEP(i)
  stays a hypothesis.
- Next concrete lead (Remark 2.8 [C]): with Λ small, resonance is impossible under R1 and a/b landings have δ in the
  certified window [−12,15] except the bare ties (5,5),(5,−11) — R2 may be automatic for a/b landings.
- Open: R1, R2 (c landings; bare ties), J beyond T_{⌊(B−4)/6⌋}. EXT open; K_clock unchanged.

## work_r1r2 — R2 for a/b landings, sharper R1 and c-landing R2 (external ZCode agent) — ACCEPTED (2026-10-20)
Review: reviews/r1r2_review_record.md (Claude adversary fixable→patched→closed; two agy gemini auditors simple errors, patched).
- Under R1 the initial deep segment has exact drift θ_t=2i−t+1, no resonance, <=Λ deep chains. For Λ<=13, R2 holds
  automatically for a/b landings except the bare ties (5,5),(5,−11); these reduce by a two-step gateway to classes
  (10−2^m)/3, (26−2^m)/3 mod 2^{m+1}, certified for all 5<=m<10⁸ [B] and closed for j_T<2^{10⁸}/(4.5P).
- **Current reduction:** J < T₄ (Λ<=4, includes K_clock): EXT(J) ⟸ R1 ∧ R2_c. T₄<=J<T₁₃: EXT(J) ⟸ R1 ∧ R2_c ∧ RES
  (RES = no a/b bare-tie landing with m>=10⁸). Above T₁₃: work_deep's reduction only.
- R1 ⟸ CAL-C: no n>=N₀−1 with X(n) odd type c and 2^{N₀} | 3τ(n)+4+λ_Y(n). R2_c: the c-landing class
  δ ≡ θ_T+3τ+3−2^{j_u} (mod 2^{j_u+1}) depends only on (θ_T, τ mod 2^{j_u+1}, j_u), i.e. τ(n_T) must avoid an
  explicit congruence; Lemma 5.3 bypasses bad classes in two steps when its hypothesis holds.
- Open: CAL-C (or R1), R2_c, RES above T₄. These are deep calendar-arithmetic statements. EXT open; K_clock unchanged.
  (Superseded 2026-10-23: CAL-C is false and R1 fails somewhere in [K_clock,T₄); see the work_c3_drift section below.)

## work_c3_drift (GPT Astra) — ε=3/ε=5 c-step identities; CAL-C and R1 refuted as targets — ACCEPTED in part (2026-10-23)
Review: reviews/c3_drift_review_record.md (Claude adversary fixable→review note; two agy gemini auditors all correct;
targeted re-review of the adversary note by two agy auditors: all correct / simple errors, patched).
Accepted: work_c3_drift/NOTES.md §1–4, C5_EXTENSION.md, UNBOUNDED_C_PARAMETER_IF_EXT.md, CONGRUENCE_TARGET_NOTE.md.
All other files in work_c3_drift/ are an unreviewed exploration record.
- c-step class identities (extra bit kept, δ' mod 2^{q+1}): ε=3 (history A) δ'≡θ; AA δ'≡θ−1; BA δ'≡θ+1.
  Hence these c steps act on small drift as 0, ∓1 and may stay deep.
- J<T₄: H5 ∧ C7 ⟹ EXT(J). H5 = every odd c step with ε>=7 in the initial deep segment has next parameter <N₀;
  C7 = certified class for an ε>=7 c landing. The BA bare tie (5,5) closes via the first gateway family (m<=50).
  (The weaker H3 ∧ C_rest version is a valid implication but H3 fails somewhere in [K_clock,T₄).)
- **Correction to the work_r1r2 frontier:** CAL-C is FALSE relative to accepted EXT(<K_clock) (congruence-target
  fire 3k*+1≡0 mod 2^M, ε=3 source with ω>=M+1; CONGRUENCE_TARGET_NOTE §1–2), and R1(J) fails for some
  J in [K_clock,T₄). The implication EXT ⟸ R1 ∧ R2_c stays true, but R1 is not a viable uniform target.
  Under global strict EXT every m>=5 also occurs as an ε=11 (BBBAA) c parameter (at n+1>=T₄; shift +4/3).
- Open: H5 (conjectured automatic for J<T₄: ε>=7 and ω>=N₀ ⟹ n>=T₄−1 [C]), C7, R2-type landing classes; beyond T₄
  classify c steps by source shift (integer {0,±1} vs bounded-height rational) instead of parameter caps.
  EXT open; K_clock unchanged.

## work_claude_shift (Claude, Part A) — general source shifts; layer bound; H5 reduced to residual sources — ACCEPTED (2026-10-23)
Review: reviews/claude_shift_review_record.md (Claude adversary fixable→2 targeted re-reviews→closed; two agy gemini
auditors all correct).
- Theorem S: exact identity D'=3+2k-(D+x')/3 at a-steps. The defect automaton extends to non-descents
  (catapults): d -> (9+6k-d)/3 with lift bit 2^m, with explicit precision H. At certified chains the c shift
  is s(n)=-1-lambda_Y=Phi-2 for every history (incl. catapults, nested c); Phi in Z[1/3] with denominator
  dividing 3^(#non-descents). Recovers 0, -1, +1, +4/3.
- Lemma ND (non-descents only at explicit small chains for bounded |d|, r); Lemma CB (bare-tie catapult output
  m<G(y)+1, class (10-2^m)/3 or (26-2^m)/3).
- Theorem L [A+B]: for a *simple* c crossing (source chain produced while chains >=N0, or the output of an A/B-
  entered bare-tie gateway; nested C letters simple), eps>=7 and omega>=N0 ⟹ n+1>=T4 (enumeration eps<=15,
  counting l*>=1+W/4 beyond).
- Corollary (inside the least strict-EXT counterexample induction): J<T4: EXT(J) ⟸ H5_res ∧ C7, H5_res = H5 for
  residual sources only: (i) true entry class outside the window, (ii) rational entry class, (iii) bare tie
  entered by a C letter, (iv) gateway output >=10^8, (v) nested residual C letter.
- [C] A 2-layer case-(iii) shape suggests H5 is probably NOT automatic below T4; the open core below T4 is
  "rational/uncertified class at a small chain" (C7 and H5_res), i.e. Part B's domain. EXT open; K_clock unchanged.

## work_landing_symbolic (external workflow agent, Part B) — symbolic landing: conditional results — ACCEPTED in part (2026-10-23)
Review: reviews/landing_symbolic_review_record.md (two Claude adversaries fixable→patched→targeted re-review closed;
two agy gemini auditors simple errors). THEOREM.md carries a 10-item review-correction block that overrides its body.
- Accepted: rational a-step trichotomy (A1–A3; the claim "Q>1 ⇒ x'≠0" is refuted); b/c class recursion; Theorem D/L
  [A | S2*]: if every a-chain satisfies 3Q_t k_t+C_t ≢ 0 (mod 2^(j_t−2)), the walk ends within j0−4 chains, records
  <= R0 <= J, classes determined mod 2^(j0+1); j=5 gateway class map (15Q−C−32bQ)/(3Q)+2^m (consistent with
  work_claude_shift Theorem S and the r1r2 families); affine A5 (no tie + certified terminal + σ>J ⇒ records<σ;
  tie record J+e); O1/O2/O3 mechanisms; 36 bad classes [B].
- Refuted (do not reuse): tie→tie record law (counterexample (73515,98094)); Z[1/3] extension of the deep no-tie
  lemma; strong a-steps preserving ht; universal catapult height constant; "record <= entry record" on the 36
  representatives; rational (A4).
- Not achieved: unconditional J-independent landing for arbitrary θ+s; a J-independent bound on gateway chains;
  the terminal certificate still uses the [B] window 5<=j<2·10^7.
- work_c3_drift group 2 now reviewed (status lines at the head of each file): RATIONAL_MODE (§1 [A] minus a false
  resonance sentence; §2 conditional; §3 [B]), ODD_DENOMINATOR ([A-cond], §1 only for integer shifts),
  SHIFT_TRANSPORT (§2–§4 [A] conditional, integer eta), FIRST_A_REDUCTION (§1–§3 [A] conditional; §4 [C]).
- Open core unchanged in kind: rational/uncertified classes at small chains — (S3) gateway output vs precision,
  (SC) dangerous residues, the 24 certify exceptions and the bare ties, j>=6 gateways needing affine provenance.
  EXT open; K_clock unchanged.

## work_claude_uniform (Claude, direction A) — EXT(J) from a rank–height condition — ACCEPTED as conditional (2026-10-24)
Review: reviews/claude_uniform_review_record.md (Claude adversary: UA1 and "supersedes" claims wrong → withdrawn; Lemma GD
rewritten; targeted re-review closed; two agy auditors simple errors).
- Lemma NT/LC: at an a-chain, NT gate ⟺ v2(3Qk_j+C)=j−2. The canonical calendar has no odd-a chain at j=19,20,21 and DEPTH
  margins 2^(j−2)−3k_j−1 >= 1,048,551 from j=22 (CLOCK beyond 400): classes with 3^r(3k_j+h)<2^(j−2) never gate.
- Full-residue certify for 5<=j<=18: exactly 24 exceptional classes (lift-independent, independent recomputation).
- Gate blocks entered from y>=19 are block-safe: [B] 51.9M symbolic walks for y<500 (rank<=4, heights <=(2048,2048,760,330,190));
  Lemma GD [A|NZ] for y>=216.
- Theorem UA [A+B]: inside the least strict-EXT counterexample induction, for every J, S(J) is tie-free under RH
  ((RH-a) DEPTH at chains >=19, (RH-b) rank/height caps at arrivals, (RH-c) <=3 non-descents per region walk, (NZ)).
  An alternative reduction; it does NOT replace the accepted J<T4 reduction, and whether RH holds in any range is open.

## work_gateway_trains (external ZCode agent, directions B+C) — gateway trains and climbs — ACCEPTED in part (2026-10-24)
Review: reviews/gateway_trains_review_record.md (two Claude adversaries; RECORD_BUDGET conclusions corrected; two agy auditors).
Review-correction blocks at the head of RECORD_BUDGET.md, B_RANK.md, C_CLIMB.md, NOTES.md override their bodies.
- B1: gate tie classes alternate 5↔21 (mod 32) with internal labels k≡22/6 (mod 32) [A]; b crossings cannot return to a tie
  (lambda_Y≡0 mod 16) [A]; B5 = the fixed residue D≡−3k (mod 2^(j−2)) in class coordinates; class-level constraints alone do
  not bound consecutive gateway blocks.
- C1/C3/C5: climbs through arbitrary runs into a bare tie: x''=A''u_y+Z_run, no identically cancelling run (S≠0), over-bound
  climbs form a single residue; C4 climb bound [A-cond D2] for the FIRST gate (y>=N0, |D_y|<=5); C6 for r=1 C entries.
- Ledger identities [A]; Theorem RB only for the first gate under explicit hypotheses. Failure modes F1–F6 (later gates,
  empty-run gates, non-tie NT gates at j>=6, large ancestral defects) remain open: the train problem is not closed.
- work_c3_drift train/budget documents now reviewed (status lines at their heads): GATEWAY_TRAIN, CLOCK_FILTERED_TRAIN,
  TRAIN_CLOCK_ORBIT accepted; CROSS_SCALE_TRAIN as a construction; five budget documents as conditional results.
- Open core (both directions): NT gates after the first gate / gateway trains, i.e. avoiding the tie residue at later gates.
  EXT open; K_clock unchanged.
