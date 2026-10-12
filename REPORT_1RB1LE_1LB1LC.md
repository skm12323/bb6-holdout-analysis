# Arbitration Report: `1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD`

**Status: UNDECIDED.** The machine is reduced exactly to an integer map, and the open question is a Collatz-like reachability problem. HALT = D reading 0. This machine is listed on the bbchallenge wiki as an unproved holdout (there is a "Polygon" block analysis, R1–R14). The page could not be fetched for a line-by-line comparison.

## Accepted theorem (Stage 3 passed)
Files: `work_t1/RULES.md`, `work_t1/verify_t1.py`.

- **Family.** W(X; b1,…) = `0^∞ 1^X [E on 0] 1^b1 0 1^b2 0 … 0^∞`, where b1 ≥ 0 and the later blocks are ≥ 1.
- **Macro rules.** An 11-row table with exact step counts, proved by symbolic run-length execution over 120 start shapes (196 leaves). Coverage is exact and the invariant is preserved.
- **Base [B].** Blank tape → W(0;0,3) at t=12.
- **Halting pattern.** `1^X E> 0 1 0` is the only one.
- **Theorem.** Starting from the base, **the TM halts ⇔ the orbit visits (0;10,…)**.
  - Forced route: (0;10) → (1;6) → (2;2) → (0;0,1) → (1;1) → halt.
  - Every X=0 output has an even first block, which excludes the other halting routes.
  - The predecessor list of (0;10,…) is complete.
- **Derived rule.** (1;Y,z) → (1;Y−2,z+6) in 8Y+16 steps, for odd Y ≥ 5.

## Review trail
- Adversary: `1. closed in all states`. Rule table checked by brute force on 6156 configs; symbolic split sound; §5 re-derived.
- Auditor 1: `1. all correct`. 13,127 rule cases; exact coverage; base and derived rule checked.
- Auditor 2: `2. with simple errors`.
  - Orbit vs raw TM: 2824 transitions to t ≈ 3.1·10^6.
  - 269,555 small orbits.
  - Predecessor list confirmed complete.
  - One error: §5(e) wrongly claimed (1;2,2,…) is never an output. It is S's image of (0;0,2,2,…), which is itself never an output, so the theorem stands.
  - Local patch: the coordinator applied the auditor's prescribed correction verbatim. **ACCEPTED.**

## Open problem
Does the orbit of (0;0,3) ever reach (0;10,…)?
- For even b, the checkpoint map is C(b;c) → C(3b+c+3).
- For odd b, it enters nested divide-by-4 chains. This is Collatz-like, and no invariant is known.

Evidence (Class-C):
- About 2·10^6 accelerated macro events, with blocks above 10^4300, never visit (0;10,…).
- The number of 1s never decreases.
