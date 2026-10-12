# R8 review — AUDITOR 2 (structural / arithmetic claims + boundary cases)

Scope: verify V1..V5 of work_r8/PROOF.md against the actual top-map dynamics with code
written from scratch. Scripts: `D:\math_cc\scratch\review2_engine.py` (independent
engine: exact top map + compositional frame tracker with per-frame contracts, window
bookkeeping and tail invariants asserted every step), `review2_v1.py`, `review2_v2arith.py`,
`review2_v3.py`, `review2_v4enum.py`, `review2_v5.py`. Nothing outside `scratch/` was modified.

Framework used throughout (mirrors verify_r8.F): a *fire* = odd-head state; a *nested
excursion frame* is created at a fire with window W = L[3:], contract
head = 2^s0·H0 + d0 + 3·ell + kap0 + ΣW[:a], returns at the first contract-satisfying
state [head] + W[a:]; j = absorbed window entries, state always ends with W[j:] (asserted).
Fires are tagged 'enc' (greedy run parse, r ≥ 2 — verify_r8's own encode) or 'short'
(r ∈ {0,1} short canonical states produced by E-macros at r ∈ {2,3}; verify_r8 treats
these as glue, TemplateChecker recurses on them — both tags measured).

---

## V1 — structure of canonical states in the exact dynamics — **PASS**

1600 excursions E(w,v), w ∈ {1,3,5,7}, v = 1..400; 282280 top() steps; 102948 fires
(96 020 at r ≥ 2, plus 4020 at r = 0 and 2908 at r = 1 short canonical states);
0 halts; every excursion ended at its verified contract (final head = 2^v·3w + 3·ell,
asserted each run); 0 contract-breaking suffix coincidences.

- (1a) windows: at all 96 020 r ≥ 2 fires, L[3:] = [4H, 8H, …, 2^{r−1}H, J] + Z with
  Z exactly the caller's *remaining* window W[j:] (0 shape violations, 0 boundary
  violations). No other shapes occur.
- (1b) absorbed entries a: 'enc' frames a ∈ {0,1,2} (35 492 / 55 536 / 4 992), max 2;
  'short' (r ∈ {0,1}) frames a ∈ {0,1}, max 1. a ≤ 2 confirmed.
- (1c) margin v2(H) − v2(d+3) at fires: minimum **3** (≥ 1 required); 0 fires at t = 0
  (heads at frame starts are even, as claimed); d+3 = 0 never occurs.
- (1d) Δ = d − (3t+1) ∈ {0} ∪ {negative odd}: 0 violations; min Δ = −1023.

Levels at fires: sp ∈ 1..7 dominate; deep fires (sp ≥ 8): 1236, all at r ≥ 2, sp ∈ {8,10}.

## V2 — deep-branch condition — **PASS** (premise nuance noted)

- Arithmetic: v2(3H + d + 3) ≥ 8 ⇔ (d+3) ≡ 0 mod 256, brute-forced exhaustively for
  j ∈ {8,9,10,11,12,13,14}, d ∈ [−4096, 70000), 300 odd w + one large w: **0 mismatches**
  for j ≥ 8. At j = 7 the equivalence genuinely fails (deep ⇔ d+3 ≡ 128 mod 256 there),
  i.e. only 2^8 | 3H is needed — the j ≥ 11 premise is stronger than necessary.
- In dynamics: 91 108 checks at fires with r ≥ 1, v2(H) ≥ 11: **0 mismatches**
  (v2(q0) ≥ 8 ⇔ d ≡ −3 mod 256 held at every such state).
- Premise nuance: 8540/102948 fire-state H are **not** of the form 3w·2^j
  (e.g. H = 36880 = 2^4·2305) — but all of them have v2(H) ≤ 7, and every fire-state H
  with v2(H) ≥ 8 is of 3w·2^j form. So "canonical H = 3w·2^j" is false in general but
  true at every deep-relevant (j ≥ 8) state in the scanned dynamics.

## V3 — boundary scan (rho × r0 × w × j) — **PASS** (with a tt-boundary nuance)

27 648 concrete runs to the excursion end: r0 ∈ 1..6, every rho ∈ 0..255,
d = rho + 256·tt with tt ∈ {0,1,2}, w ∈ {1,3}, j ∈ {11,12,13}, start
[H+d, H, …, 2^{r0−1}H, 2^{r0}H − 1] (kap = −1, Z empty).

- 0 halts, 0 timeouts, 0 root-contract failures.
- Shape = sequence of macro events (E / C(level) / G): identical across (w,j) for every
  (r0, rho, tt) — **0 mismatches**; also 0 mismatches for the stronger variant
  interleaving return events ('R', a). This includes the deep residues (rho = 253 etc.),
  i.e. the post-deep-branch child prefix behaves (w,j)-uniformly in all scanned cases.
- Nuance (report-only): the shape is **not** a function of (rho, r0) alone in general —
  it also depends on the higher bits of d: 16 (r0, rho) combinations (rho ∈
  {253, 250, 247, 244, 241} depending on r0) give different shapes for tt ∈ {0,1,2},
  because the deep level is v2(9w·2^{j−8} + tt + 1) + 8, which varies with tt.
  (w,j)-invariance is unaffected; but "predicted by the residue rho alone" needs the
  deep-level refinement, not just rho mod 2^8.

## V4 — r = 0 deep-branch lineage question — **issues found**

Child kap arithmetic (all verified numerically in-dynamics, 0 identity mismatches):
r ≥ 2: kap_child = H − 1; r = 1: H + kap − 1; r = 0: **Z0 − H − kap − 1**
(class Z0class − kapclass − 1 mod 2^11). Note q0 = 3H + 2kap + d + 3 at r = 0, so the
deep condition there is 2kap + d + 3 ≡ 0 mod 256 (shifted; e.g. kap = −2 needs d ≡ 1 mod 256).

Enumeration (H ≡ 0 mod 2^11):
- kap ∈ {−1 mod 2^11}: children {0} (Z0 = 0) and {−1} (Z0 = −1) — in family.
- kap ∈ {−2 mod 2^7}, Z0 ∈ {0}: children = all 16 classes ≡ 1 mod 128 — **ALL OUTSIDE**
  {0,−1 mod 2^11} ∪ {−2 mod 2^7}. Z0 ∈ {−1}: children ≡ 0 mod 128 — only 0 is in
  family, 15 classes outside.
- Same defect at r = 1: kap ∈ −2-class gives kap_child ≡ −3 mod 128 — all 16 classes outside.

Concrete instances (H = 3·2^11 = 6144):
- [6145, 6142, 2048] (kap = −2, d = 1, Z0 class 0): q0 = 18432 = 2^11·9, sp = 11 (deep),
  kap_child = −4095 ≡ 1 mod 2048 — outside family. Runs 9 steps to [14362], no halt.
- [6145, 6270, 2047] (kap = 126, Z0 class −1): q0 = 18688, sp = 8, kap_child class 1920
  — outside. Similarly [6145, 6142, 2047] (class 0, in family) and [6145, 6270, 2048]
  (class 1921, outside). None halt.

Occurrence:
- In real excursions (w ∈ {1,3,5,7}, v ≤ 400): **zero** deep fires at r ∈ {0,1}. All
  1236 deep fires are at r ≥ 2 with child class −1 mod 2048 (in family). −2-class kaps
  do occur at r ∈ {0,1} fires (r=0: 20, r=1: 12) but only with sp ≤ 1; −1-class kap
  r ∈ {0,1} fires reach at most sp = 4. The gap is never exercised in range.
- Inside PROOF's own check5b start family (kapgen = 1, i.e. kap = −2 + 128m): deep
  r ∈ {0,1} fires **do** occur — 48 in a targeted scan (r0 = 2 with rho = 254 → r = 0
  fires, sp ∈ {8,9}, child class 1 or 1921 ≡ 1 mod 128; r0 = 3 with rho = 250 → r = 1
  fires, child class 2045 or 125 ≡ −3 mod 128), for every (w,j) ∈ {1,3} × {11,12,13},
  tt ∈ {0,1}. All 48 children are outside the claimed family; all 18 432 runs still
  complete without halting.

Root cause: TemplateChecker.F's deep-branch check inspects only the continuation's
window entries (J/Z residue classes) and never evaluates the child frame's kap, so
check5b's "0 new residue classes" cannot see these children. PROOF.md §2's claim
"the reachable lineage is therefore generated by {−1+2^{K+3}κ} ∪ {−2+2^{K−1}m}" is
thus (i) not established by the computation and (ii) false as an arithmetic closure
statement at r = 0 (formula absent from §2) and at r = 1 for −2-class parents.
This is exactly the input the by-hand lemma L-coverage ("one line per branch case
r ∈ {0,1,≥2}") would need — as stated, that lemma cannot be completed with the
current family.

## V5 — verify_r8.py checks 5/5b and the numbers 16896 / 28160 — **PASS, with findings**

Reran the shipped code (read first) with independent instrumentation:
- check5 (run_all, K = 8): ok = **16896**, 0 failures. Enumeration counted myself:
  5 r0 × 256 rho × 11 tails = 14080 canonical + 256 × 11 = 2816 glue = **16896** ✓.
- check5b (run_lineage): ok = **28160**, 0 failures, new_classes = ∅. Enumeration:
  2 kapgen × 5 r0 × 256 rho × 11 tails = **28160** ✓.
- Secondary numbers reconcile and pass: K = 10 canonical r0 ∈ 1..9 = 9·1024·11 =
  **101376** runs, 0 failures; r0 ∈ 6..8 canonical + lineage =
  3·256·11 + 2·3·256·11 = **25344** runs, 0 failures, 0 new classes. (45056 = 4·1024·11
  is consistent with a K = 10 lineage-style variant but is not uniquely reconstructible.)
- FINDING (check5): the **2816 glue-start runs are vacuous**. run_glue calls
  F([head]+tail, Z0L=tail), and final_match succeeds immediately at k = 0, ell = 0:
  every glue run returns (0,0) without executing a single step (instrumented _Tm count:
  26288 steps over all 16896 check5 runs, all from canonical starts, ≈1.9 steps each).
  "Glue starts: zero failures" in PROOF.md is true but empty — glue-start coverage
  does not exist (glue *states* are still exercised inside canonical runs).
- Minor observations: nested frames inside template runs skip the contract check
  (d0 = None path — "contract verified" applies to top frames only); verify_r8.F's
  r = 0 and r = 1 q0-branches are dead code (encode cannot return r < 2); HALT
  criterion holds as m == 1 ⇔ A+2b+3 = 2^k with k ≥ 3 (the q0 = 4 edge gives head 3,
  no halt — unreachable in dynamics).

---

## Verdict

V1 PASS, V2 PASS, V3 PASS, V5 PASS (numbers exact), V4 **FAIL of the §2 lineage-closure
claim**. Issue list:

1. **Lineage closure is false as stated.** At deep branches from r = 0 states (and from
   r = 1 states with parent kap ∈ −2 mod 2^7) the child frames' J-offset classes
   (≡ 1 mod 128, ≡ 0 mod 128 except 0, ≡ −3 mod 128) fall outside
   {0,−1 mod 2^11} ∪ {−2 mod 2^7}; such branches are reachable within check5b's own
   kapgen = 1 start family (48 concrete instances found, none halting). The r = 0 line
   is missing from §2's case analysis, and the check5b computation cannot detect this
   because it never evaluates the child kap. L-coverage as described cannot be proved
   with the current family — it needs a repaired family (adding the classes above and
   re-closing) or a reachability argument excluding deep r ∈ {0,1} fires. Mitigating
   evidence: 0 occurrences in real excursions (v ≤ 400) and no halts anywhere scanned.
2. **check5's glue-start component is a no-op** (2816 runs execute zero steps); the
   claimed glue-start coverage should be removed or implemented.
3. Minor: "canonical H = 3w·2^j" fails for 8.3% of fire-states (all with v2(H) ≤ 7;
   harmless for the deep-branch claim, which needs only 2^8 | 3H); the shape at deep
   residues (rho = 253, 250, 247, …) is not a function of rho mod 2^8 alone (depends on
   d's higher bits); PROOF's "margin ≥ 3" is confirmed exactly (min 3).

All empirical/finite claims that were checked (V1 statistics, V2 equivalence, V3
invariance, V5 enumerations and zero-failure runs) reproduce. The single substantive
defect is the r = 0 / −2-class hole in the lineage-closure argument (issue 1), plus the
vacuous glue coverage (issue 2).
