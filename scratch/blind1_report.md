# BLIND AUDITOR 1 — independent re-implementation and audit of the closed-form claims

Machine: `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` (never-halts claim).
Audited artifact: `scratch/agentB_closedform.md` sections 0–3 (claims C1–C4 below),
on top of the previously audited reduction `work_r1/RULES.md` (top map).
Everything in this report was re-derived and re-implemented from scratch in
Python 3 stdlib. I did not read `scratch/agentB_*.py`, `reviewB_*`, `review_B_*`,
`mainline_*`, or `agentG2_*`, nor closedform sections 4–8.

My scripts (all in `scratch/`): `blind1_lib.py` (top map per RULES §5, closed
form, annotated stepper), `blind1_explore.py` (orbit-structure validation),
`blind1_c1.py`, `blind1_c2.py`, `blind1_c3.py`, `blind1_c4.py`
(`blind1_c3_symbolic_out.txt` = full symbolic log). Total footprint < 100 KB.

Ground-truth engine: the literal loop of RULES §5 (`top_step_loop`), first
validated against the audited orbit description: from (3), 1361 excursion
entries check (`L_{n+1} = E(w,v)` exactly when `n+2 = 2^v·w`, v ≥ 1; plain
singleton successor when v = 0; every singleton equals 3n+3): **0 mismatches**.
Every faster engine used later (closed-form stepper, deque stepper) was
additionally validated step-by-step against `top_step_loop`.

---

## C1 — step closed form: **PASS**

My derivation (from the audited loop; full text in `blind1_c1.py`): with
`x = A+2b+3 = 2^j·u` (u odd), `m_t = 2^{j-1-t}·u − 3` and the t-th push emits
`2^{j-2-t}·u`, so after the loop the queue is exactly `u, 2u, …, 2^{j-2}u`
(j−1 entries) in front of `D = c+(A+1)/2` and S; successor `A' = u+1`.
Loop outcome: j=1 → 0 iterations, m = u−3; j ≥ 2, u ≥ 3 → exactly j−1
iterations, m = u−3 (even, ≠ 1); j ≥ 3, u = 1 → m ends at 1 (HALT);
(u,j) = (1,2) (x = 4) → m = −1, no halt, successor (3; D, S) — the sole
exception to the formula. Hence HALT ⟺ u = 1 ∧ j ≥ 3. On the top-map domain
(A odd ≥ 3, entries ≥ 0) one has x ≥ 6, so u = 1 forces j ≥ 3 and the audited
statement "HALT iff u = 1" is exact there; x = 2 and x = 4 are off-domain
(need b < 0 or A = 1).

Verification (loop implementation vs my closed form):
- **Orbit**: 100 000 top steps from (3): 37 501 fires, **0 mismatches**
  (successor list and halt flag identical), no halt, sum = 3n+3 at every step.
- **Random states**: 10 000 states (A odd, lengths 1–12, entry magnitudes up
  to ~2^191): **0 mismatches**; the 12 halting states agreed in both engines;
  min x observed on-domain = 6.
- **Crafted**: x = 2^j, j = 3..60 (u = 1): all halt, engines agree; controls
  x = 2^j·u with u ∈ {3, 5, 9, 2^61−1}, j = 1..24: never halt, engines agree
  (0 failures).
- **Off-domain boundary**: states with x ∈ {2, 4} (negative b or A = 1):
  no halt, loop == closed (with the x = 4 successor exception handled exactly)
  — see precision note (a) below.

## C2 — universal sequence: **PASS**

Implementation: provenance-annotated queue (each entry knows whether it is
`2^a·U_L` of the run pushed by fire L, the seam of L, or the excursion defect);
a fire whose consumed b is a run entry of level L at run position ρ must
satisfy x = 3·2^ρ·U_L + 6k+4 with L's current schedule k, j = 1+v2(3k+2),
u = 3·2^{ρ−j}·U_L + odd ≥ 1 and u ≥ 9, and (ρ, j, k) must continue L's
schedule (4,1,1), (7,4,2), (11,2,4), …; each nesting level replays the same
universal sequence from k = 1 (this is the content of Theorem 2's "ONE
universal sequence … replayed recursively"; note a single globally shared
counter would be wrong — the nested first event has x = 3·2^4·u + 6·1+4 with
k = 1 — see precision note (d)).

- Master sequence generated from **my** (dk, dp) table: matches the claimed
  (ρ, j) prefix (4,1),(7,4),(11,2),(13,1),(16,3),(21,2),(23,1),(26,6) and the
  claimed k-sequence 1, 2, 4, 5, 6, 8, 9, 10, 13; it also matches all 21
  printed p and k values of §3 (but not its j-row, see Finding F1).
- **w ∈ {1, 3, 5, 7, 2^31−1, 10^12+1} × v ∈ {300, 1000, 2000}** (18 runs):
  6 276 run-chain events at all nesting levels, **0 mismatches** of any kind
  (position / k-form / j-form / u-form / sequence-prefix). Event trees are
  identical for all six w (steps 264/892/1780; chain events 93/318/635 of
  which top-level 89/302/604; levels with events 5/15/29) — the k-sequence is
  indeed independent of w.
- Extra: E(1, 20000) and E(2^31−1, 20000): 17 842 steps, **6 371** chain
  events each, 0 mismatches (the doc says "6372" — off-by-one convention,
  note (c)).

## C3 — per-j class verifier: **PASS**

- **Empirical table (my own runs)**: for each j = 1..30, 72 synthetic class-j
  hosts (k = smallest class member, k+2^j, k+3·2^j; U ∈ {3, 9, 15, 5, 7,
  3·(2^31−1)}; ρ ∈ {j+2, j+5, 45, 90}), each host built exactly as the
  aftermath of a class-j chain fire (x = 3·2^ρ·U + 6k+4, run u·2^a, seam D,
  host run 2^{ρ+2+s}·U) and run until the next host chain fire. Uniform
  (dk, dp) within every j; **equal to the claimed §3 table for j = 1..20 in
  all 20 entries**; my extension j = 21..30:
  dk = 9, 10, 10, 11, 11, 11, 12, 13, 13, 14; dp = 4, 6, 4, 4, 5, 4, 6, 3, 2, 5.
- **Symbolic class verifier (sound by construction)**: values are
  integer-affine forms in the host parameters (U, q) with q = (6k+4)/2^j
  free odd ≥ 1 — a superset of the class 6k+4 ≡ 2^j (mod 2^{j+1}), so a
  completed run proves the identity for the whole class. Decisions:
  parity = (cU+cq+c) mod 2 (always decidable for odd U, q); exact v2 by
  unique-minimum term analysis (v2(cU), v2(cq), v2(c)); a tie is refused,
  never guessed; divisions only by exact coefficient shifts (proved valid
  whenever the minimum is unique); u ≥ 3 by non-negativity + minimum value.
  **All 30 classes completed with 0 refusals, 0 ties, 0 class-splits**, each
  proving x_next = 3·2^{ρ+dp}·U + 2^j·q + 6·dk with the same constant
  (dp, dk) as the numeric table. ρ-coverage: concrete ρ = j+1 … j+1+2·steps+64
  (≥ j+117 for every j) plus all ρ−j ≥ 37 by the invisibility argument (max
  decision depth 6, max total division drain 30, generic-run min v2 of any
  U-coefficient = 5000 at ρ = j+5000, margin 4994; spot-checked ρ = j+5000,
  j+12000, j+40000 give identical results).
- Honest boundary: the class run does not (and cannot) decide the *next*
  event's j, since j' = 1+v2(3(k+dk)+2) genuinely varies inside a class;
  that schedule consistency is exactly what C2 verifies empirically
  (6 276 + 2·6 371 events, 0 mismatches). The (dk, dp)-functions-of-j claim
  itself is fully proved by the class runs.

## C4 — ell formula: **PASS**

ell(v) := number of top-map steps from E(w,v) until the list first becomes a
singleton (deque stepper, validated step-by-step against the audited loop for
v ≤ 250, w ∈ {1,3}: 0 mismatches; and my ell(1..20) reproduces the claimed
1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16 exactly — confirming the
definition).

- v = 1..3000 (w = 1): no halt; with k_b(v) = my master k at the last
  universal position p ≤ v−1 (0 if none): **ell(v) − 2·k_b(v) ∈ [1, 12] for
  every v** (claim 0 ≤ e ≤ 16: PASS; the doc's tighter e ∈ {0,…,12} also
  holds). Histogram of e: {1:2, 2:1485, 3:651, 4:496, 5:167, 6:144, 7:18,
  8:22, 9:6, 10:4, 11:2, 12:3}. Example: ell(3000) = 2672 = 2·1334 + 4.
- w-independence of ell: 437 v-values (all v < 120 and every 97th up to 3000)
  × w ∈ {3, 5, 7, 2^31−1}: identical ell in all 1 748 runs (0 differences).

---

## Findings (mismatches vs claimed values)

**F1 (display typo, no mathematical impact).** In `scratch/agentB_closedform.md`
§3, the printed j_i row of the universal sequence contains two wrong entries:
at p = 34 (k = 14) it prints j = 1, but j = 1+v2(3·14+2) = 1+v2(44) = **3**;
at p = 67 (k = 29) it prints j = 5, but j = 1+v2(89) = **1**. (The two entries
are transposed.) The p-row, the k-row and the (dk, dp) table are all
self-consistent with the *true* j values (e.g. from k = 14, j = 3 gives
k→16, p→39 as printed), and my C2 verification of the audited prefix
(4,1),(7,4),(11,2),(13,1),(16,3),(21,2),(23,1),(26,6) and k-prefix
1,2,4,5,6,8,9,10,13 passes, so the error is confined to that display row.

**Precision notes (no mathematical impact, for completeness):**
(a) §1's "HALT iff u = 1" is exact on the top-map domain (A odd ≥ 3, entries
≥ 0 ⇒ x ≥ 6 ⇒ u = 1 forces j ≥ 3); with arbitrary negative entries, x = 2
(j=1, u=1) also fails to halt. §1's parenthetical discusses x = 4 but not
x = 2 (both are off-domain).
(b) §1 says "x = 4 needs A = 1, which never occurs since A ≥ 4 always":
in fact A = 3 occurs (L_0 = (3) itself); x = 4 is still impossible on-domain
because it needs b < 0.
(c) §3/§0 mention "6372 run-chain events up to position 20000"; I count 6371
in E(1,20000) — a ±1 counting-convention difference, all invariants hold.
(d) The audit brief's tip "ONE shared k-counter" should read "one shared
k-sequence": each nesting level replays the universal sequence from k = 1
(the nested cascade's first event always has x = 3·2^4·u + 6·1+4), exactly as
Theorem 2 states ("replayed recursively"); a single globally-shared counter
would contradict that first nested event.

## Verdict

C1 PASS, C2 PASS, C3 PASS, C4 PASS — every audited claim reproduced exactly
(step closed form; universal (ρ, j, k) sequence with j = 1+v2(3k+2) and
x = 3·2^ρ·U + 6k+4 at every run-chain of every nesting level, independent of
w; the (dk, dp) table as a function of j alone, j = 1..20 matching and
21..30 derived; ell(v) = 2·k_b(v) + e with e ∈ [1,12] ⊂ [0,16]).

FINAL VERDICT: all correct, with one minor artifact finding: two transposed
entries in the printed j-row of closedform §3 (p=34: j should be 3, not 1;
p=67: j should be 1, not 5) — no impact on any audited claim.
