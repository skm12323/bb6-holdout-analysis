# Three-way review of work_claude_cycle (Claude subagent, post-gate structure / G1), 2026-11-02
Target: work_claude_cycle/NOTES.md and its scripts (cyc, branch, verify_engine, postgate, verify_laws, verify_3g, maxgates,
sweep, residue_cont, seeded + json). Reviewers: adversary = Claude subagent (D:/math_cc_astra/adv_cycle; re-runs and two
constructed counterexamples); auditors 1, 2 = agy gemini-3.8-flash-high, blind (aud90 numerical, aud91 logic). The author
is a Claude subagent launched by the coordinating session (it ran one read-only `git status`, contrary to its brief; no
change resulted).

- Adversary: `2. fixable gaps`. HIGH: Lemma DR false — X enters x at the first a-step after the output with coefficient
  2^j, so a determined next gate satisfies only R_after <= R_in+1+L_bc (DR′). Counterexample A (j=24, m=6,268,562:
  record 24→25; replayed exactly by the coordinator with random high bits; the note's own DETREC check fails on it) and
  B (j=42, m≈1.1·10^12, type b: +3). HIGH: §3 FREE-EXIT relied on DR; fix: free := not record-safe; then the reduction is
  bookkeeping and needs FREE-B for boundary gates. MEDIUM: memorylessness threshold/data dependence; localisation only for
  first-landing escapes; [B] scope (small m only). LOW: label-residue pattern refuted (residue 3 and 15 occur); NEXT type-c
  precision; float underflow; counter naming; CLOCK-ORBIT at every j only a sketch. Confirmed: PG, LAND, FREE (first
  landing) and constants, chain-count t<J, CG, 2G/3G/JT, SELF, NEXT (v2(N)<j−2), §6 examples, synthetic starts genuine.
- Auditors 1, 2: `1. all correct` (own engine; PG/LAND/NEXT/SELF/CG/JT; (9194,45901) and climbs replayed; j<300 scan).
  Neither saw the DR failure (their ranges have m<5000).
- Patches (coordinator): review-correction block at the head of NOTES.md (overrides the body). Targeted re-review 1:
  wording (attained only for L_bc∈{0,2}; solvable vs exhibited j; replacement §3 bullet and bookkeeping qualifier;
  dependence wording; scope list; NEXT hypothesis). Targeted re-review 2: one attribution fix (the j<300 scan was auditor 1's;
  the adversary's DR scans were j<120, m<1500 and j<60, m<2·10^5), otherwise closed; applied → closed in all states.

VERDICT: ACCEPTED in part. [A]: PG, LAND, DR′ (R_after <= R_in+1+L_bc), FREE for first-landing escapes (localisation
j <= 3+log2(6mP(m))), NEXT (type c under its precision hypothesis), SELF, CG, 2G/3G/JT; FREE-EXIT ⇒ EXT with "free" =
"not record-safe" (bookkeeping; its value rests on FREE-B and CL2). [B]: the §4 data within the stated small-m ranges;
all multi-gate instances synthetic. Refuted: DR; "determined cascades cost nothing"; "next gate always at 5/8"; "outputs
decrease"; the label-residue avoidance pattern. Open: FREE-B, later escapes (CL2), trains (CL4). G1 not closed; EXT open;
K_clock unchanged.
