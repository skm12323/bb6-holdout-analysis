# R8: compositional analysis of Lemma E(v) — machine `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`

Tags: **[Class-A]** proved for all stated parameters (exact symbolic run, uniform in every
symbol; or by-hand proof as stated); **[Class-B]** finite exhaustive computation;
**[Class-C]** conjecture / empirical. Reviewed 2026-10-12 by an adversary + two blind
auditors (reports in `scratch/review_r8_*.md`); the adversary's refutation of the original
template-closure claim is incorporated below.

Base (audited, work_r1/RULES.md; independently re-verified from the raw TM by the
verification agent, §5): top map T; HALT ⇔ some top step has A odd and x = A+2b+3 = 2^k;
sum(L_n) = 3n+3 on the orbit from L_0=(3) — in particular **every real-orbit list has
sum ≡ 0 (mod 3)** [Class-A]. R4: Lemma E(v) v ≤ 2000 ⟹ no halt for top steps n < 2^2001−2.

## 1. The compositional prover (check1–check4) [Class-A for each s ≤ 1000; auditor-verified]

Lists during an excursion: **canonical** (H+d, H, 2H, …, 2^(r−1)H, J, Z…), J = 2^r·H + kap;
**glue** (head + few leftovers + run + J + Z). One top step, compositionally:
- A even, r ≥ 2 (**E-macro**): → (4H, d+3, r−2, kap, Z) [1 step];
- A odd (**chain**, precondition o' = (A+2b+3)/2^{v2} ≥ 3 asserted): with b, c the next
  entries, q0 = A + 2b + 3, s' = v2(q0): the step starts the nested excursion
  Phi_{s'}(o'; K'; Z') — K' = c' − q0/2 + 1, c' = c + (A+1)/2, Z' = entries from position
  4 — executed by **recursion** at level s' (well-foundedness asserted: s' < level);
  the outer state resumes at [head'] + Z'[a':] [1 + ell(s') steps];
- otherwise: one direct symbolic step.

Contracts verified exactly per run (uniform in u, w = 2u+1):
mid-excursion head_final = 2^{r0+1}H + d + 3·ell + kap + ΣZ[:a]; nested head_final =
2^{s}o + 3·ell + K + ΣZ[:a]. (The adversary notes the nested/glue returns skip the
contract check in the multi-symbol engine — in the single-symbol engine of check1 it is
checked at every frame; auditor 1's stricter re-implementation agrees on all v ≤ 150.)

- **check1**: F(v) for v = 1..1000 — re-proves R4's Lemma E(v) in range, compositionally.
- **check2/3**: ell(v) equals the direct symbolic engine (v ≤ 300) and concrete orbits
  w ∈ {1,3,5} (never halt, exact final singletons).
- **check4** [Class-B, 153558 nested calls]: a(s) ≤ 2; margin v2(H) − v2(d+3) ≥ 3 at every
  A-odd canonical step with t ≥ 1 (at t = 0 the head is even, no chain; agent D concurs);
  d − (3t+1) ∈ {0} ∪ {negative odd}; every window = (r−2 clean H-multiples) + [J] + caller
  Z; ell(v) ≤ 1.08·v.

## 2. The end-phase template engine (check5/5b/5c) — scope corrected after review

Multi-symbol exact engine over the start family: canonical(r0 ∈ 1..5, ρ ∈ [0, 2^8),
11 tail patterns), H = 6·2^{11}u + 2^{11}(1+h), d = ρ + 2^8·tt,
tail_i = 2^{11}(z_i+1) − π_i. **What the runs verify** (16896 + 28160 runs, 0 failures,
0 new residue classes): every symbolic run either completes with the verified contract or
reaches a **deep branch** (v2(q0) ≥ 8) whose continuations [head] + window[a:] are in the
residue family {0, −1} (mod 2^{11}) ∪ {−2} (mod 2^7) — i.e. there is no 2-adic
obstruction, and the deep-branch residue lineage of the starts actually occurring in
real excursions is finite. K = 10 and r0 ∈ 6..8 variants (scratch, re-run by both
auditors) agree. (The 2816 "glue starts" of check5 are vacuous — they match the terminal
form at t = 0 — and are dropped from any claim.)

**What they do NOT verify** (adversary's refutation + auditor 2's hole, both accepted):
(a) the deep branch does not simulate the nested child, and the *product* family contains
members that halt when run as concrete orbits (e.g. [2301, 2048, 4095] → HALT at t = 8108
past the contract singleton). All halting members found (104/104 in check5c's scan;
142/240 sampled at ρ = 253 by the adversary — including every re-tested 3|H instance)
have **sum ≢ 0 (mod 3)** — excluded from the real orbit by the audited sum invariant.
Check5c [Class-B]: 520 sum-valid concrete instances (3 | H): 0 halts within 5000 top
steps. (b) The lineage-closure statement holds for the r ≥ 2 deep branches that occur in
real excursions (auditor 2: all 1236 deep fires in v ≤ 400 are r ≥ 2, child class −1),
but the −2-generator family itself contains r ∈ {0,1} deep branches whose children leave
the family (classes ≡ 1, −3 mod 2^7; 48 instances inside check5b's own starts) — the
corrected family must either exclude those (real-orbit arithmetic) or carry the wider
class set. The halts of (a) live precisely in child *prefixes* of sum-invalid starts
(max canonical v2(H) = 9 < 11 there).

## 3. Status after review

**Stands:** compositional Lemma E(v) for v ≤ 1000 (check1–4, two independent engines +
concrete cross-checks; auditor 1: "all correct"; auditor 2 reproduced V1–V3, V5);
structure theorems of §1; check6 (initial prefix s-independence; G3); the residue-lineage
finiteness for real-excursion deep branches (r ≥ 2); the sum-class separation (check5c).
**Withdrawn:** the claims that check5/5b certify non-halting of the family and that the
glue starts add coverage.
**Remaining for all v (corrected residual):**
- (L-sum) build the mod-3 sum constraint into the symbolic family (substitute each
  symbol s = 3s' + ε over valid ε-vectors; the 2-adic decision paths are unaffected,
  so the existing runs carry over; only the deep-child starts change class);
- (L-coverage) the level-decreasing induction with child-prefix coverage (halts occur
  only in child prefixes of sum-invalid starts; for sum-valid starts no prefix halt was
  found in any scan), with the family extended or constrained per auditor 2's finding
  (exclude r ∈ {0,1} deep branches with −2-class parents, or add the ≡ 1 / ≡ −3 mod 2^7
  child classes);
- (L-middle) recursion well-foundedness bound (ell ≤ 2s, Class-B to s = 1000).

## 4. Convergent independent routes (R8 agents, scratch/)

- **Closed form (agent B, scratch/agentB_closedform.md):** every excursion is driven by a
  universal w-independent event sequence: x = 9·2^p·w + (6k+4), j = 1+v2(3k+2), with a
  universal (Δk, Δp) table; spike aftermaths replay the same sequence self-similarly with
  strictly decreasing parameters (proved j_q < j); 41 endgame templates; ell(v) = 2·k_b(v)
  + e(v); E(v) proved for all v ≤ 12·2^1194. Residual: formalize one "locality" step of
  the j-induction (no counterexample signal in 1200 full abstract runs).
- **Invariant (agent C, scratch/agentC_invariant.md):** master law x = α·w + γ with
  v₂(γ) < v₂(α) at every fire; the affine exclusion lemma (αw + γ ≠ 2^K for all odd w)
  is proved; verified on 374,114 fire families (v ≤ 1500). Residual: the preservation
  induction (dive map; k ≥ 5 interludes; room invariant i ≥ t+2 by a finite 2-adic
  periodic induction).
- **Verification (agent D, scratch/agentD_verify.md):** raw-TM re-derivation of R1–R5,
  coverage, halting criterion, top-map equivalence, E(v) v ≤ 100 — **all PASS**.

## 5. Verdict

The R4 theorem (no halt for top steps n < 2^2001 − 2) stands, re-proved compositionally
for v ≤ 1000 with structure theorems (audited by three reviewers; the compositional core
survives intact). Three independent routes (compositional templates + sum-class;
closed-form universal table; affine master law) now reduce the all-v statement to three
explicitly stated finite/by-hand lemmas each, with no counterexample signal in any scan.
Non-halting of the machine remains **[Class-C]**.
