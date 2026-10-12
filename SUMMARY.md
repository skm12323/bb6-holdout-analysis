# BB(6) Holdout Campaign: Consolidated Summary

Source list: bbchallenge BB(6) holdouts, 2026-09-24 (815 classes), stored as `data/BB6_holdouts_815.txt`. Triage scan of all 815 machines at 10^6 steps: `triage2/scan.txt` (no halts).

Every result below went through a three-way review: one adversary and two blind auditors. A statement is "audited" only if it passed that review.

## Results by machine

| Machine | Audited results | Halting status | Novelty vs community (2026-10) |
|---|---|---|---|
| `1RB1LC_1RC1LB_1LD0RB_0LE1RD_---0LF_0LA1LF` | none (paths fuse-reset) | undecided | — |
| `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---` | Reduction v2 (block-list map M, halt ⇔ orbit hits H); refined criterion: halt ⇔ some left-edge arrival has u0 ∈ {2^k−2} (Lemma W sweep map) | undecided | likely new; **3 siblings proved equivalent (work_u1, audited)** |
| `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` | Reduction to stack top-map; halt ⇔ some step with A odd and A+2b+3 = 2^k; ΣL_n = 3n+3; **no halt for top steps n < 2^2001 − 2** (audited); R8 (reviewed): compositional + template with sum-class separation; **R9 (2026-10-13): PROVABLY NON-HALTING (audited: 1 adversary + 2 blind auditors, all re-implementing independently — see CHECKPOINT)** via the universal-replay route (one universal (p,k) sequence, x = 3·2^ρ·U + 6k+4, u ≥ 9 at every chain every level; queue-determinism locality; ρ-induction; ell = 2k_b + e) — full three-way review passed 2026-10-13; residual errata are documentation-only (work_r9/THEOREM.md, verify_r9.py) | **non-halting (audited)** | covered in more depth by [CyclingCycloid/bb6-holdout-research](https://github.com/CyclingCycloid/bb6-holdout-research) (as "M1"); community sheet lists it as "Cubic Mess", no notes |
| `1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB` | Phase system + Σ stack machine; Theorem H (halt ⇔ an empty-stack state (p,1;∅) satisfying the stated condition) | undecided | equivalent reduction exists (Racheline, Discord 2024); also treated as "cm2" in CyclingCycloid/bb6-holdout-research |
| `1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD` | 11-row rule table; halt ⇔ orbit visits (0;10,…) | undecided | already covered (Polygon R1–R14; simulated to 10^190,000) |

## Files kept (main theorems + verification closures)

| Machine | Main theorems | Verification scripts | Arbitration record |
|---|---|---|---|
| `1RB0LE` | `work_q4/RULES.md`, `work_q6/LEMMAS.md` | `verify_q4.py`, `verify_q6.py` | `REPORT_1RB0LE_0RC1RB.md`, `CHECKPOINT_1RB0LE_0RC1RB.md` |
| `1RB1LA` (#1) | `work_r1/RULES.md`, `work_r4/PROOF.md`, `work_r8/PROOF.md` | `verify_r1.py`, `verify_r4.py`, `verify_r8.py` | `CHECKPOINT_1RB1LA_0RC0RD.md` |
| `1RB1RA` (#2) | `work_s1/RULES.md`, `work_s3/RULES.md` | `verify_s1.py`, `verify_s3.py` (`verify_s3` imports `verify_s1`) | `REPORT_1RB1RA_1LC0RC.md` |
| `1RB1LE` | `work_t1/RULES.md` | `verify_t1.py` | `REPORT_1RB1LE_1LB1LC.md` |
| `1RB1LC` | — | — | `CHECKPOINT_1RB1LC_1RC1LB.md` |

Notes:
- `verify_q6.py` imports from `work_q4`.
- `work_r5/`, `work_r6/` and `work_r7/` hold unaudited attempts at #1's global non-halting.

## Open problems

- **#1 CLOSED (non-halting, audited).** Remaining niceties: fix the documentation errata in scratch/agentB_closedform.md (§3 j-row typos at two entries; mod-3 "superset" overstatement; e ∈ [0,12] → e ≤ 16; "sum forces progress" → pointer monotonicity; margin-900 wording — the assumption is inert, required margin −3); optionally package the result for the bbchallenge wiki (user posts).
- **`1RB0LE`:** show that the averaging-carry map never yields an all-even chain ending in a power of 2.

## Suggested next work

- ~~B: sibling equivalence~~ — DONE (work_u1/EQUIV.md, audited).
  - `1RB0LD_1LC1RD_0LE1LA_0RB1RD_---0LF_1RA1LF`
  - `1RB1RA_1LC0RC_1RE0LD_0RE0LF_1RA---_1RB1LF`
  - `1RB1RC_1LC0LE_1RD1RC_1LB0RA_---0LF_1RD1LF`
- Package #1's audited results for submission to the bbchallenge wiki or Discord. The user does the posting.

## Related work & attribution
This campaign was suggested by the author of [CyclingCycloid/bb6-holdout-research](https://github.com/CyclingCycloid/bb6-holdout-research). That repository covers #1 (M1) and #2 (cm2) in greater depth and, per its author, includes the equivalence proof. The results here were derived independently and claim no priority; where they overlap, defer to that repository.

All work in this repository was carried out by Claude Opus 5.5 (Anthropic), acting as coordinator of sub-agents via Claude Code under the user's direction.
