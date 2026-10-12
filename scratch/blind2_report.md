# Blind Auditor 2 — report on the structural core of the non-halting proof

Machine `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`; claims audited from
`scratch/agentB_closedform.md` against the audited reduction in
`work_r1/RULES.md`.  Everything below was re-derived from scratch with own
code (`scratch/blind2_lib.py`, `blind2_s1.py`, `blind2_sweep.py`,
`blind2_fits.py`, `blind2_s4.py`; aggregates in `blind2_sweep.json`,
`blind2_fits.json`, `blind2_s4.json`).  No other scratch artifacts were read.
Python 3.14.6, stdlib only; total runtime of all scripts ≈ 40 s; footprint
≪ 50 MB.

## 0. Independent validation of the GIVEN (before using it)

* My verbatim implementation of the top map was cross-checked against an
  independent from-scratch implementation of the RULES.md §3 macro rules
  R1–R5 (+ HALT row, coverage and normalization exactly as §4): the first
  **400 top configs from (0;3) are identical** (`blind2_lib.cross_check_top_vs_rules`).
* Excursion construction re-derived: from the odd singleton
  `L = (3·2^v·w − 3)` (n+2 = 2^v·w) the first top step is the b=c=0 chain
  (x = 3·2^v·w, j = v, u = 3w) whose pushed level is exactly
  `E(w,v) = (3w+1; 3w, 6w, …, 3w·2^{v−2}, 3w·2^{v−1}−1)`.  All runs start
  from this singleton, so the "zero" fire (b=0) is inside every census below.
* ell(1..20) = 1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16 — **reproduced
  exactly** (independent replication of Theorem 4's base and of the audited
  range).  Spot check of the ell formula at v=2000: ell = 1780 =
  2·k_b + e with k_b = 889 (universal k at rho = 1998), e = 2 ∈ [0,12].
* Lemma 1 (closed form of a chain: x = 2^j·u, pushes x/4…x/2^j, final m = u−3,
  halt iff u = 1) checked at **every one of the 674,758 chain events** of the
  main census — 0 failures.  Sum ≡ 0 (mod 3) and sum = s0 + 3·steps verified
  at every state for v ≤ 120, w ∈ {1,3,5}.

## 1. S1 — queue-determinism + prefix universality

**S1a (Lemma L0): PASS.**  10,000 random pairs of states with equal head A and
equal first m queue entries (m ∈ [1, len−1]; unstructured, run/defect-structured
and small-value queues; A up to 10^6, both parities) were simulated in lockstep
with per-entry original-index tracking.  Result: **0 mismatches**.  9,989 pairs
stopped exactly at the first step that would consume an original entry with
index ≥ m; 11 pairs halted together with byte-identical events (the halt
decision depends only on A, b, which agree).  Average number of synchronized
steps before the boundary: 2.23.

**S1b (spike traces): PASS for the claimed prefix universality; the literal
"20-step traces coincide" FAILS for small J (see Finding 2).**  E(1,2000)
reaches a singleton (no halt), ell = 1780, 668 fires, 56 fires with j ≥ 5.
Canonicalization value → (value // u, value % u) with u = the spike's level
base; spikes grouped by j:

| J (run spikes) | n | clean length | clean traces equal | full 20-step equal |
|---|---|---|---|---|
| 5 | 27 | 2 | yes | **no** (common prefix 2) |
| 6 | 14 | 2 | yes | **no** (common prefix 3) |
| 7 | 7 | 3 | yes | **no** (common prefix 3) |
| 8 | 4 | 4 | yes | **no** (common prefix 4) |
| 9, 10, 12 | 1 each | 4, 7, 8 | yes | vacuous (n=1) |
| 2000 (the zero fire) | 1 | 20 | yes | vacuous |

The clean part (before the spike's own defect D is consumed) is **identical**
within every group, and the cross-J prefix property holds in all 6 tested pairs
(J, J'): cascade(J) is a prefix of cascade(J') — e.g. (5,6), (6,7), (7,8),
(8,9), (9,10), (10,12) all True.  The first non-clean step consumes exactly
the spike's own D, at **queue index J−1** (run positions 0..J−2 first), never
an entry beyond it — precisely the doc's Corollary.  Divergence afterwards is
fully explained: for two J=5 spikes (host run positions 63 and 134) steps 0–1
are identical ((`E`,(1,1),(4,4)), (`E`,(4,4),(16,7))); step 2 is in both a
chain with b = D, j = 3, quotient x//u = 69 equal, but the **residuals**
x % u differ (D = c+(A+1)/2 of the creating fire encodes the host position),
and from there on the traces differ (the subsequent host-level replay resumes
at universal positions 67 vs 138 with k = 29 vs 61 — the universal sequence
itself, correctly position-indexed).

## 2. S2 — non-run-chain fire safety

Census over v = 1..2000 (w = 1) plus v ∈ {2500, 4000} × w ∈ {1, 3, 5}
(2,006 excursion runs; 674,758 fires; **every excursion reaches a singleton,
zero halts**):

| role of b | fires | min u | max j |
|---|---|---|---|
| run (b = run entry of its level) | 640,108 | **73** | 12 |
| seam (b = defect D = c+(A+1)/2 of a prior fire, level ≥ 1) | 32,037 | **30,749** | 4 |
| tail (b = D0, the excursion's own defect 3w·2^{v−1}−1) | 607 | **19** | 11 |
| zero (b = 0; the excursion-entering singleton chain, x = 3·2^v·w, u = 3w) | 2,006 | **3** (= 3w at w=1) | 4000 (= v) |

**u ≥ 3 at every fire of every role** (minimum overall u = 3, attained only by
the zero fire, whose u = 3w ≥ 3 analytically since x = 3·2^v·w has odd part
exactly 3w).  Role coverage is exhaustive — see S4(a).  The c-entry census
(w = 1 runs, 2,002 excursions) confirms the queue structure: run fires always
consume a same-level c
(run@rho+1: 619,714; own D: 16,260 — never an over-read); seam fires consume
an older-level c (run: 31,736; D: 32; 0: 63); tail fires always have c = 0
(D0 is the last queue entry); zero fires have c = 0.

**Family fits (w = 1, 3, 5; 670,412 fires fitted): PASS.**
* structural identity across w (role, rho, j of the i-th fire identical for
  w = 1, 3, 5): 0 violations — the decision tree is w-independent;
* exact affine law x = alpha·w + gamma: 0 violations (alpha = (x3−x1)/2
  integral, and x5 = 5·alpha + gamma always);
* **v2(gamma) < v2(alpha): 0 violations** — hence u(w) = (alpha·w+gamma)/2^v2(gamma)
  = even·w + odd ≥ 3 for every odd w ≥ 1 (verified numerically for all odd
  w ≤ 31: v2(x(w)) = v2(gamma) and u(w) ≥ 3, odd, always);
* 2,036 distinct families: run 1,305 (fires 635,974), seam 126 (31,831),
  tail 605 (605), zero 0 (the 2,002 zero fires have gamma = 0, i.e.
  x = 3·2^v·w exactly — safe separately as above).
* The recurring families are exactly the closed form: top run family
  alpha = 9·2^4 = 144, gamma = 10 = 6·1+4 (n = 1,997 of 2,002 runs, i.e. it
  fires in essentially every excursion), then alpha = 9·2^7, gamma = 16 (n =
  1,994), alpha = 9·2^11, gamma = 28 (n = 1,990), … — alpha = 9·2^rho,
  gamma = 6k+4 with v2(gamma) = j < rho = v2(alpha); nested-level families
  such as alpha = 27·2^24 also appear.  Tail fires (endgame) are
  individually affine with the v2 property (605 distinct (alpha, gamma),
  e.g. the j = 11 tail fire at v = 770 has astronomically large u).

## 3. S3 — decrease

Own level tracking via the pushed-run stack (every chain creates a level;
640,108 run-chain events, all levels):

* **Universal replay invariant I(rho): 0 violations.** At every run chain at
  every nesting level, x − 3·2^rho·U = 6k+4 with integer k ≥ 0 (k integrality:
  0 failures), j = 1 + v2(3k+2) (0 failures), and the map rho → (k, j) is
  **globally consistent**: 1,210 distinct positions (host fires up to
  rho = 3,996), 0 mismatches across all levels, all v, all w.
* **j < rho: 0 violations — at every run fire, not only rho ≥ 32.**  Max j
  among run fires = 12 (at rho = 1537, k = 682); max j/rho = 4/7 ≈ 0.571
  (j = 4 at rho = 7); for rho ≥ 32, j ≤ 3·log2(rho)+3: 0 violations (max j
  at rho ≥ 32 is 12).
* **k vs rho: linear, k ≤ 0.4465·rho with 0 violations**; max observed k/rho
  = 0.44621 (k = 1,781 at rho = 3,996; k = 889 at rho = 1,998; k = 445 at
  rho = 998 — ratio ≈ 0.445 throughout).  The structural cruder bound
  k ≤ rho^3 also holds everywhere, with huge margin.
* Host-level fire sequence (rho, k, j) for v = 4000 starts
  (4,1,1), (7,2,4), (11,4,2), (13,5,1), (16,6,3), (21,8,2), (23,9,1),
  (26,10,6), (31,13,1), (34,14,3), … — the p and k rows of the doc's §3
  table match **exactly** (first 21 entries compared; the doc's j row does
  not — Finding 1).  The derived transition table (finite differences of
  (p_i), (k_i) grouped by j_i) matches the doc's dk/dp table with **zero
  mismatches** for all j ∈ {1..12} occurring in range, with no
  within-class inconsistencies.
* Every nested level's own fire sequence (57 non-empty level sequences in the
  v = 4000 run, lengths up to 1,210) is a **prefix of the universal host
  sequence**: 57/57 match, 0 mismatches — the recursive replay claim.

## 4. S4 — assembly

**(a) Role coverage: PASS.** Every one of the 674,758 fires has b ∈ {run
entry, seam D, tail D0, zero}; nothing outside the three claimed families
(run chains / seam chains / tail-endgame chains incl. the zero fire), and the
c-entry roles are exactly as claimed (§2 above).

**(b) Spike margins: PASS.** Max spike parameter J (run fires with j ≥ 5) at
v ≤ 4000 is **J = 12** (at rho = 1537, k = 682); J-histogram over the whole
census: J=5: 27,437; 6: 14,736; 7: 6,355; 8: 4,202; 9: 1,056; 10: 1,623;
11: 4; 12: 470.  All 55,703 spikes sit in the class k = 16s+10 with
j = 5 + v2(3s+2) — 0 violations; 2^J ≤ 6k+4 — 0 violations; k ≤ 0.4465·rho —
0 violations.  Margin arithmetic (exact integer computation): from
2^J ≤ 6k+4 ≤ 6·0.4465·rho + 4 one gets rho ≥ (2^J−4)·1000/2679, so
rho − J ≥ 3.2·10^9 already at J = 33; even with only the structural bound
k ≤ rho^3, rho − J ≥ 1,095 at J = 33 and ≥ 576,994 at J = 60, i.e. the claimed
"p − J ≥ 900 whenever J ≥ 60" holds with enormous margin.  Empirical
min(rho − J) per J: {6: 20, 5: 58, 8: 91, 7: 236, 10: 378, 9: 954, 12: 1525,
11: 3822} — positive and growing.

**(c) Nested parameter decrease: PASS.** At every run fire of every nested
level (level created by a fire with parameter J_parent): rho ≤ J_parent − 2
(structural: the pushed run has J_parent − 1 entries) and j < J_parent —
**0 violations in 640,108 run fires**.  No nested spikes (j ≥ 5 at depth ≥ 1)
exist in the whole audited range — structurally impossible there, since a
nested spike would need a run reaching position 26, i.e. J_parent ≥ 30 > max
observed J = 12.  The recursion is well-founded in the verified range.

## 5. Findings

1. **Transcription error in `agentB_closedform.md` §3, the j_i row.** The
   printed row "1 4 2 1 3 2 1 6 1 **1 3 2 1 4 2 1 3 2 1 5** 3" is wrong at
   indices 9–19. The correct row (from my data and from the doc's own k row
   via j_i = 1+v2(3k_i+2)) is "1 4 2 1 3 2 1 6 1 **3 2 1 4 2 1 3 2 1 5 1** 3".
   The p_i and k_i rows and the dk/dp table are correct and match my
   from-scratch derivation exactly, so this is a display typo, not a
   mathematical error — but anyone using the printed j row verbatim would be
   misled.
2. **The literal "20-step post-fire traces of same-j spikes coincide" is
   false for small J.** For J ∈ {5, 6, 7, 8} (the groups with n ≥ 2 in
   E(1,2000)) the traces coincide only for the first 2, 2, 3, 4 steps
   respectively — exactly up to the step that first consumes the spike's own
   defect D (queue index J−1) — and then diverge, because D = c+(A+1)/2 of
   the creating fire depends on the host position (quotient parts continue to
   agree; the residuals differ).  This is **consistent with the doc's actual
   claim** (Lemma L0 + Corollary: cascades of spikes with the same J coincide
   until the J-cascade first touches its D at queue index J−1, and the replay
   never reads past its own run before that), which my data confirms exactly,
   including the cross-J prefix property; only the blanket 20-step reading
   over-claims.  For J ≥ 9 in this range the groups have a single member, so
   the 20-step comparison is vacuous there.

## 6. Verdict

S1a PASS; S1b PASS for the claimed prefix-universality (with Finding 2
qualifying the literal 20-step reading); S2 PASS; S3 PASS; S4 PASS.  The
structural core of the proof — queue-determinism, the universal replay
invariant x = 3·2^rho·U + 6k+4 with one position-indexed (k, j) sequence at
every nesting level, j < rho / k ≤ 0.4465·rho decrease, exhaustive role
coverage with u ≥ 3 (and the w-affine safety law v2(gamma) < v2(alpha)), and
the spike margin arithmetic — is confirmed by from-scratch computation on
674,758 chain events / 670,412 fitted fires with zero mathematical
violations and zero halts in the audited range.

VERDICT: all correct except two documentation-level findings — the §3 j_i-row
typo (Finding 1) and the over-strong literal 20-step trace claim, which holds
only up to the spike's own defect exactly as the doc's own Corollary states
(Finding 2); no mathematical error found.
