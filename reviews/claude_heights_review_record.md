# Three-way review of work_claude_heights (Claude, height ledger steps 1–2), 2026-10-27/28
Target: work_claude_heights/NOTES.md, hl_stats.py, band.py (+json/log). Reviewers: adversary = Claude subagent (aud87;
independent rechecks on the 10^6 and 10^8 tables); auditors 1, 2 = agy gemini-3.8-flash-high, blind (aud85, aud86). The
author is the coordinating session.

- Adversary: items 1–5, 7 `2. with fixable gaps`; item 6 (the §2 assessment) `3. wrong`. HIGH: Theorem S's precision H is
  not J−Gamma; after a true NT gate with output m >= H_g the post-gate class is uncertified, so HL2/HL1/NL hold only up
  to the first NT gate of S(J) and a propagation problem does exist for S(J); "rank +1 per cycle" conflated the automaton
  value with real integer data. HIGH: NL needs certified copied sources (Corollary S1) — [A-cond]; the "double-log scale"
  claim withdrawn. MEDIUM: SB general constant adds over nested non-descents (A(Phi) <= W/2−1/2+2Σk); HL2 omitted the lift
  term; only true NT gates count for ND-EXIT (catapults are descents in L'); Step 1 misreadings (train tails, S3 heights).
  LOW: D vs theta=3d+1 off by 2^j; band.py allowances. Confirmed: HL1 (MASS), a-descent bound, HL2 A/B/C rules, |s|<=W/2
  catapult-free, L' ⟹ EXT ⟸ ND-EXIT, localisation does not lower L''s cost.
- Auditors 1, 2: `2. with simple errors` (both: the length-2 train tails are not all j→6→1). Both recomputed Step 1
  counts on the 10^6 table, HL1, the HL2/SB/NL algebra and all 20 band-table entries, and agreed with §2–§3 (they did not
  catch the precision error).
- Patches (coordinator): Step 1 lines corrected (shift values 0 and −1 only; train-tail table; S3 height growth, NT gates
  and catapults all at (5,1)); a review-correction block at the head of Step 2 (overrides it). Targeted re-review: one
  slip in the patch (lift/rank condition direction) and one stale bound fixed; closed.

VERDICT: ACCEPTED in part. [A]: HL1 (b/c landing omega <= floor(log2(6tau+5)) from MASS), the a-descent landing bound, the
HL2 ledger rules (with the lift caveat), |s| <= W/2 for catapult-free certified histories and the corrected general
SB bound. [A-cond]: NL localises the FIRST NT gate of S(J), given certified copied sources. [B]: Step 1 statistics as
corrected. Rejected: "no propagation problem for S(J)" and the cycle/rank formulation of §2. ND-EXIT and the post-gate
problem remain open. EXT open; K_clock unchanged.
