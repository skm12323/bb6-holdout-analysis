# Final adversary report — audit of `agentB_closedform.md` (machine `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`)

Role: FINAL ADVERSARY, restricted to NEW attack angles (implementation-level and
logic-level). Prior reviews (extreme-w universality, per-J verifier extension,
planted halters, margins arithmetic, mod-3 wording, ell constants — see
`review_B_coordinator.md`) were not redone except where a new angle demanded it.

Artifacts of this audit (all new, all in `scratch/`):
`finaladv_0_core.py` (independent re-implementation of the top map with lineage
labels + pure-integer universal-`U` walker), `finaladv_1_levels.py`
(+`finaladv_1_out.txt`), `finaladv_2_margins.py` (+`finaladv_2_out.txt`),
`finaladv_3_table.py` (+`finaladv_3_out.txt`), `finaladv_4_verifier.py`
(+`finaladv_4_out.txt`, `finaladv_4b_out.txt`). Python 3 stdlib only; peak
footprint well under 50 MB.

---

## Executive summary

**VERDICT: STANDS WITH GAPS.** No mathematical or implementation hole was
found. Six independent adversarial attacks — including a from-scratch
re-implementation of the whole verification stack, exhaustive concrete sweeps,
and two novel "silent-decision" soundness scans of the symbolic engines —
all came back clean, and in several places the evidence base is now strictly
stronger than the report claims. The gaps that remain are (G1)–(G6) below:
three documentation-level (one new erratum in §3's printed table), two
evidence-precision (the deepest one: **no on-orbit instantiation of nesting
depth ≥ 3 has ever been executed anywhere** — the "at every nesting level"
claim is, concretely, a depth ≤ 2 claim), and one logic-wording gap in the
termination argument of §6.

---

## Angle 1 — Level-tracking soundness of the invariant checker. **CONFIRMED-SAFE** (with finding F1)

Attack plan: audit how `agentB_run15.py` tracks nesting levels and relative
positions ρ; a mis-tracked ρ (or a fire at an unchecked ρ) would silently
verify the wrong identity. Then verify 5 consecutive nested-chain events by
direct list computation.

**Code audit.** run15 labels queue entries `('R',a)` (host run) /
`('M',cid,q)` (run pushed by chain `cid`, relative position `q`) / `('D',cid)`;
the level base of an `('M',cid,q)` entry is `level_base[cid]` = the `u` of
chain `cid`, set at push time. The labels are exact by construction (pushed
values are literally `u·2^q`), and the check `x − U·3·2^ρ == 6k_ρ+4` is exact
symbolic arithmetic in the (M, µ) frame — no approximation. Two *potential*
silent holes: (i) fires at ρ ≤ 3, and (ii) run-entry fires at ρ ∉ kpos are
skipped without comment; (iii) the whole loop runs on the symbolic walker, not
on a concrete excursion.

**Independent replication (new).** I re-implemented the engine from the audited
spec (deque-based, own label encoding, pure integers) and:

* built `kpos`/`jpos` (the universal k and j at each fire position) by a
  **pure integer walk with U=1** — no symbolic frame, no transition table;
* ran my labeled walk with U=3 (the excursion host, i.e. true margin
  v2(3w−1)=1 at w=1) to maxpos 20000: **steps 17841, fires 6690, run-chain
  events with ρ ∈ kpos: 6372, invariant failures: 0** — run15's headline
  (6372/6372, max j 14) replicated exactly, including the step and fire
  counts of log item 9;
* **0 fires at ρ ≤ 3 and 0 run-entry fires at ρ ∉ kpos** (to ρ=20000): the
  checker's silent skip zones are empty — nothing is being skipped;
* my full fire stream `(ρ|None, j)` (all 6690 fires, run and defect) is
  **IDENTICAL** to agentB's symbolic mu-Walker's stream — the symbolic frame's
  decisions and level bookkeeping agree with concrete ground truth step for
  step;
* my U=1-walk `kpos` matches the report's (dk,dp) table rows at **all 6087
  consecutive gaps** up to position 20099.

**Deep-nesting manual verification (the requested test) — and finding F1.**
The task asked for "a spike with j=8+ inside E(1,600)" and 5 consecutive
nested-chain events. This configuration **cannot exist, at any v ≤ 5000**:
a spike with parameter j pushes a run of j−1 entries, nested fires occur at
universal sub-positions 4, 7, 11, …, so a spike must have j ≥ 13 for its
replay to contain 3 nested fires and j ≥ 18 for 4. Measured: in E(1,600)
(16 top spikes, j ∈ {5,6,7,8,10}) the 9 nested fires sit only at sub-positions
{4 (j=1), 7 (j=4)}; in E(1,5000) (139 spikes, j ≤ 12) the 79 nested fires sit
only at {4, 7} with j ∈ {1,4} — **no nested spike (j ≥ 5 at a nested level)
exists in any executed concrete range**; the deepest real nesting anywhere is
**depth 2**. I therefore (a) dumped and hand-verified the deepest REAL case —
the j=12 spike at host position 1537 in E(1,5000): its 2 nested fires plus 3
exit-window fires, with raw A, b, c, x and the identities
`x = 3·2^ρ·U + 6k_ρ+4`, `j = j_ρ` exact (including the host-level resumption
fire at position 1543 = 1537+dp(12)=6, k advancing by dk(12)=8) — and (b) ran
**synthetic nesting hops** (justified by the proof's own prefix-universality:
walking with base U = u of a spike is the exact prefix of the replay of any
spike with that u and j ≥ 703): 3 hops × 233 fires, each hop containing its own
depth-2 levels — **222/222 invariant-OK, 0 failures** — with 5 consecutive
nested fires at the deepest level dumped with full raw arithmetic, all exact.
These hops exercise the level-tracking machinery at arbitrary base values and
arbitrary lineage depth of the *construction*, but each hop's internal nesting
is still depth ≤ 2, because a depth-3 fire requires an on-sequence spike with
j ≥ 28, which first occurs at p ≳ 6·10^7 — beyond every executed walk.

**Conclusion.** Level tracking is sound (exact replication + engine-to-engine
stream equality + manual dumps). But the report's "at **every** nesting level
(279 levels checked)" is concretely a depth ≤ 2 statement; depth ≥ 3 is
instantiated only *inside* the per-J abstract verifier at j ≥ 28 (sub-cascade
reaching sub-position 26) — which does pass, now verified by me through
j = 30000 (angle 6) — and by the written ρ-induction. This is finding **F1**
(evidence-precision, not a mathematical error).

## Angle 2 — The mu-walker's MARGIN=900 assumption. **CONFIRMED-SAFE** (with finding F2, wording)

* **Census (new):** in E(1,5000) the 139 top-level spike hosts have true
  margins p−J = {20, 58, 91, 129, 164, 202, 236, 274, …, 4971}; deepest spike
  j=12 at p=1537, margin 1525; smallest occurring margin 20 (p=26, J=6). There
  are **no hosts with margin 12 or 50**, and **137 of 139 hosts violate the
  ≥900 assumption** — the written justification ("p−J ≥ 900 whenever J ≥ 60
  and p ≥ 2^18") is true but vacuous for the range where the walker's results
  are consumed. This is wording finding **F2**: the margin story in §4 does
  not match the actual use.
* **The assumption is nonetheless inert (new, decisive).** Patching
  `agentB_mu.MARGIN` to each of {1,2,4,8,12,20,50,900} reproduces the
  **identical** walker event stream (to N=4000 for all values; to N=20000 for
  MARGIN=1 vs 900: 17841 steps, 6690 fires, stream-equal). Zero "M-only"
  (margin-sensitive) v2_val calls occur in 6690 chain decisions, and the
  required margin — max over all v2_val calls of (s − v2(cM)) — is **−3**:
  every decision is safe for every true margin ≥ 0. Structurally this is
  forced at run-fires (v2(cM)=ρ > j_ρ=s, tie-freeness), so the walker
  transfers to *all* hosts with p > J — which holds at every spike host
  (v2(6k+4)=J < v2(9·2^p·w)=p) — and to the excursion host U=3w=M+µ with
  M=3w−1 (margin v2(3w−1) ≥ 1). Note my angle-1 stream-equality already
  exercised the walker at true margin 1.
* **Vanishing-µ scan (new implementation-level attack, negative).**
  `v2_val` returns min(v2(cµ),v2(e)) for the generic odd µ; if
  cµ·µ0+e = 0 for an *admissible* host value µ0 (odd, ≥1, 3∤µ0 — µ is the odd
  part of 6k+4, hence never divisible by 3; µ0=1 is realized by the excursion
  host of *every* w and by the on-sequence k=10 spike), the generic decision
  is wrong for that host. Scanning all 6690 v2_val inputs of the 20000-walk:
  **zero** vanishing admissible µ0. The analogous hole in the *abstract*
  verifier (`agentB_abs.v2_val`: class member k* = κ+2^m·s0 with vanishing
  k-part) was scanned over j = 1..399 (26067 calls): **zero** vanishing class
  members. Neither engine ever issues a decision that is secretly wrong for a
  member of its certified family in the executed range.
* **Concrete transfer at the smallest occurring margins (new).** At the
  margin-20 (p=26, J=6), margin-58 (p=63, J=5) and margin-91 (p=99, J=8)
  hosts, the concrete cascade segment in E(1,5000) is fire-by-fire identical
  (x and j) to the pure-integer replay with base u_host, and the host level
  resumes exactly at p+dp(j) with k+dk(j) per the table (5/3, 4/3, 6/4).
  For the abstract per-J verifier: **zero** ctx.p-dependent (P-side) v2
  returns; the required minimum true p per j is ≈ j−3 (worst: j=399 needs
  p > 396), while on-sequence hosts of parameter j sit at p ≳ 2^j/2.7 —
  transfer is safe by an enormous margin, and concretely verified for every
  occurring j ≤ 14 by the angle-3 sweep.

## Angle 3 — (dk,dp) table completeness at occurring j. **CONFIRMED-SAFE**

* Enumerated the j-distribution of the walk's own fires: over **all** fires
  (all levels) of E(1,v) for **every** v ≤ 6000, the occurring set is
  j ∈ {1,…,13}; j=14 first appears at v = 6132 (verified: E(1,6132..6135) and
  E(1,6500) all singleton, ell = 5473–5800, max j = 14 — the coordinator's
  e ≤ 16 calibration boundary).
* For every one of the **5,442,032** top-level fires in the v ≤ 6000 sweep
  (and for w ∈ {3,5,7}, v ≤ 400), checked x = 9w·2^ρ + 6k_ρ+4 and j = j_ρ
  against my table-free, frame-free U=1-walk kpos: **0 failures**. This pins
  every occurring consecutive transition (dk,dp) to pure simulation for the
  entire occurring-j set, closing the sampled-j concern completely for the
  concrete range (j=14..1200 remain exercised only by the walker (j ≤ 14 at
  ρ ≤ 20000) and the abstract verifier — see angle 6 residual).

## Angle 4 — "No other chains" / mixed lineage / crossing. **CONFIRMED-SAFE in range**

Classified every fire of E(1,600/3000/5000) by lineage of its consumed b:

| excursion | host-run H | mini-run m | defect d | tail T | zero Z |
|---|---|---|---|---|---|
| E(1,600)  | 181 | 9  | 9  | 0 | 0 |
| E(1,3000) | 906 | 47 | 48 | 0 | 0 |
| E(1,5000) | 1513 | 79 | 79 | 0 | 0 |

* **(i) Mixed-lineage runs:** a run pushed by a seam chain requires a chain
  with b ∈ {d, T, Z} and j ≥ 6; the measured j-distribution of exit fires is
  **{1, 3} only** — **no seam spikes exist** in range, hence no mixed-lineage
  run fires. (If one occurred, its replay prefix would still be universal by
  queue-determinism — L0 needs only the canonical post-chain state — and my
  lineage-blind invariant check would cover it; none occurred to test.)
* **(ii) Crossing (outer tail read during inner replay):** by queue order
  (pushes at the front), a fire's b is always at the innermost active level;
  the excursion's own tail entry T is consumed as the **c** of the final
  host fire (measured: step 531 of E(1,600), fire at H-598), never as b. The
  over-read events are exactly the exit fires with b = d — all concrete-safe
  (j ∈ {1,3}, every u ≥ 73 in E(1,5000); min u = 73/217/361 at w=1/3/5).
* Every run fire (H or m) satisfies the invariant (190/953/1592 checks, 0
  failures — an independent concrete confirmation of run15 on finite
  excursions, not just the infinite walk); no T-b or Z-b fires exist; all
  excursions end in singletons.

## Angle 5 — Termination. **STANDS, with wording GAP (G5)**

* **Concrete:** all v ≤ 6000 plus 6132–6135 and 6500 reach singletons;
  ell(v) ≤ 2·k_b(v)+16 with **0 violations**; max ell/v = 0.9128 — no
  runaway signal anywhere.
* **Logical audit:** the sentence "the sum invariant forces progress to the
  singleton" (§6 item 4) is **vacuous as an argument** — sum(L)=3n+3 holds
  identically on a hypothetical infinite excursion; it cannot force anything.
  The *operative* termination mechanism, all present elsewhere in the write-up,
  is: (1) the pointer strictly advances — dp(j) ≥ 2 at every table entry,
  which I verified via the per-J verifier **through j = 30000**
  (dk ≥ 1, dp ≥ 2 everywhere: j=20000→(8922,6), j=30000→(13384,5)); (2) the
  run is finite, so the pointer crosses v−1 after ≈ v/2·(2.2) fires; (3) the
  endgame is a finite set of verified templates landing at a singleton
  (41 shapes v ≤ 2000, abstract boundary j ≤ 60 × E ∈ 2..8, affine fits
  λ ≥ 9/512 for large v). Given the table for all occurring j and the
  template coverage, this does prove ell < ∞; but the write-up should replace
  the sum-invariant phrase with this pointer-monotonicity argument.
  GAP **G5** (wording; ingredients already in the document).

## Angle 6 — Formal-logic audit of the ρ-induction (§4 item 3). **STANDS with residuals (G6 = report's own §8 residue, plus F1)**

* **Well-foundedness: correct.** The sub-cascade of a fire at position ρ with
  parameter j_ρ consists of fires at sub-positions ≤ j_ρ−2 < ρ once j_ρ < ρ;
  the latter holds for ρ ≥ 32 (k_ρ ≤ ρ³ ⇒ j_ρ ≤ 3log₂ρ+3 < ρ; arithmetic
  checks out, monotone), and ρ ≤ 31 is inside every machine range.
  Sub-sub-cascades occupy strictly smaller naturals at every level, so nesting
  depth terminates; the sub-level positions use the *same* universal
  k-ordering, confirmed concretely (my invariant checks at nested levels use
  the identical kpos). No ordering mismatch exists.
* **No circularity as written:** the induction on ρ consumes dk(j) only for
  j ≤ 3log₂ρ+3 ≪ ρ, and dk(j) comes from the per-J verifier whose own
  recursion is on strictly smaller j (j' ≤ 3log₂(j−2)+3 < j for j ≥ 32,
  machine below) — the two inductions compose into one strong induction on
  (ρ, j) ordered lexicographically via j < ρ. Legitimate.
* **Residuals (unchanged in kind from §8 / coordinator caveat 1, now with
  more evidence):** (a) totality+soundness of verify(j) for **all** j is
  asserted, not proved — machine evidence now extends to j = 30000 (this
  audit; was 20000), with dp ≥ 2 throughout; (b) the k ≤ ρ³ bound is asserted
  with a machine anchor (k ≤ 0.4465ρ to 4·10^5) rather than derived — the
  derivation is routine (k_ρ ≤ Σ dk ≤ (ρ/2)·max_{j≤3L+3} dk(j) with
  dk(j) ≤ j·log₂j by the verifier's own induction; even k ≤ ρ² follows with
  huge slack) but is not spelled out; (c) **F1**: the IH's depth ≥ 3 cases
  are never concretely instantiated on-orbit (needs j ≥ 28 on-sequence,
  p ≳ 6·10^7) — they are exercised only inside verify(j ≥ 28) and in
  synthetic-hop walks.

---

## New errata found in the document (documentation-level)

* **E1 (§3, printed j-row):** the row `j_i : 1 4 2 1 3 2 1 6 1 1 3 2 1 4 2 1
  3 2 1 5 3 …` disagrees with the report's own definition
  j_i = 1+v2(3k_i+2) at several entries (e.g. at p=34 (k=14) the formula and
  my pure simulation give j=3, the row prints 1; at p=39: 2 vs 3; p=67: 1 vs
  5) and is inconsistent with the printed p-row's gaps (dp(1)=3 would give
  34→37, not 34→39). The p-row and k-row are correct (verified independently);
  the j-row is a typo. Non-load-bearing: all code computes j from the formula.
* **E2 (§4 margins):** the "p−J ≥ 900" justification is not the reason the
  walker is sound (it is margin-invariant; angle 2) — precision only.
* **E3 (Theorem 4):** e(v) ∈ {0,…,12} → {0,…,16} (coordinator's v=6132..6135
  finding, confirmed here; ell ≤ 2·k_b+16 holds everywhere to v=6500).

## Gap register (final)

* **G1 (evidence-precision, the substantive one):** no executed concrete
  verification anywhere instantiates nesting depth ≥ 3, nested spikes, or
  run lengths ≥ 28 entries — these first occur on-orbit at p ≳ 6·10^7.
  Coverage is by the written ρ-induction plus the abstract verifier's
  internal structure (verify(j ≥ 28) passes; extended to j=30000 here).
* **G2 (wording):** "the sum invariant forces progress" — replace by the
  pointer-monotonicity (dp ≥ 2) + finite-templates argument.
* **G3 (wording):** §3 j-row typo (E1).
* **G4 (wording):** margin justification vacuous vs actual use (E2); plus the
  coordinator's two flags (planted-halter region phrasing, mod-3 §5 sentence).
* **G5 (calibration):** e ≤ 16 not ≤ 12 (E3).
* **G6 (formalization residue):** per-J verifier totality for all j and the
  k ≤ ρ³ summation remain written arguments whose instantiated cases are
  machine-verified (now: j ≤ 30000, ρ ≤ 20000, v ≤ 6500, plus this audit's
  independent replications) — exactly what §8 already concedes.

## What this audit added beyond prior reviews

1. A from-scratch re-implementation (labels, engine, kpos) reproducing run15's
   headline **exactly** (6372/6372, 0 fail; 17841 steps; 6690 fires) and
   matching agentB's symbolic walker fire-stream-for-fire-stream.
2. Table-free kpos from a pure U=1 walk, cross-validated against the printed
   (dk,dp) rows at all 6087 gaps, and against **5.44M** concrete top-level
   fires over all v ≤ 6000 (0 mismatches), plus w ∈ {3,5,7}.
3. Proof-by-substitution that the walker's MARGIN constant is inert (streams
   identical for MARGIN=1..900; required margin −3), converting the report's
   margin *assumption* into a *verified property*.
4. Two novel silent-decision soundness scans (vanishing µ in the walker;
   vanishing class member k* and P-side returns in the abstract verifier) —
   all negative, i.e. the symbolic engines' generic decisions are valid across
   their certified families throughout the executed range.
5. Per-J verifier extension to j = 30000 with dk ≥ 1, dp ≥ 2 (termination
   linchpin) — beyond the prior 20000.
6. The depth-ceiling finding F1 and the honest deep-nesting verification at
   the deepest realizable case plus synthetic hops.
7. Fire-classification census proving the "no other chains" claim concretely
   (no seam spikes, no mixed lineage, no T/Z-b fires; exit fires j ∈ {1,3},
   all safe).

## Final verdict

**STANDS WITH GAPS** — gaps G1–G6 above, none refuting. Every mathematical
claim that is instantiated in any executable range survived a fully
independent re-derivation; the two symbolic engines contain no silent-decision
defects in the audited ranges; the one substantive evidence limitation (G1:
nesting depth ≥ 3 never concretely on-orbit) is covered by the written
induction and the abstract verifier, and is precisely the kind of residue the
report's own §8 already discloses. The proof remains, as the coordinator put
it, a Class-A argument with machine anchors, now with a second independent
implementation behind it; converting the ρ-induction schema into a
machine-checked artifact is the only step between "stands" and "formalized".
