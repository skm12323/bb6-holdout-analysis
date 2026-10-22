# Three-way review of work_claude_shift (Claude, Part A), 2026-10-23
Target: work_claude_shift/NOTES.md and verify_shift.py, forced.py, layers.py, runs.py, free_search.py.
Reviewers: adversary = Claude subagent (aud70; reran layers.py, runs.py, verify_shift.py on copies, plus
own finite-precision tests adv.py/adv2.py); auditors 1, 2 = agy gemini-3.8-flash-high, blind (aud68, aud69).
The author is the coordinating session.

- Adversary: `2. with fixable gaps` (S 2, ND/CB 2, L 2, enumeration 1, corollary 2).
  HIGH: the residual list (i)-(iv) was incomplete — a large-phase nested C letter copying a residual
  crossing (e.g. C(w'')A with w'' of type (iii), l*=4 plus a G' step) is in no class; added
  (v) and made the definition recursive.
  MEDIUM: Cor S1 needs the certification premise, and Phi depends on the catapult data; the C rule
  missed the nested precision H(w'); the denominator only DIVIDES 3^(#non-descents) (resonant (5,-3)
  gives 6, e.g. BBBBA; nested sums cancel); the large-phase argument covered only resonance (and missed
  the 3^r factor).
  LOW: Lemma CB sigma off by one per entry type (y-2, y-3, y-2-eps); (i) must use the true class
  including lift bits (no weight bound); position of C after a gateway; pointer bound for small n;
  the verifier never exercised uncertified chains (the adversary's finite-precision test: 3658
  certified all right, 283 uncertified of which 273 wrong, bound never violated); free_search is a
  consistency check only; labels ([A+B]), "finitely many" needs bounded |d|, r.
  Confirmed: identity (S0), lift bit, H>=j+1 along descents, bare tie forces a catapult with m>=5,
  gateway classes, legitimacy of transferring the window/gateway certificates into source epochs
  (their [B] parts are context-free given the class mod 2^(j+1)), thresholds, l*>=1+W/4, soundness of
  the layers.py over-approximation, consistency of the case-(iii) heuristic. No counterexample to
  "simple ⇒ n+1>=T4" found.
- Auditor 1: `1. all correct` (S0 and Theorem S on 10,000 random a-steps and 5,000 forced walks; 120 odd-a
  chains j<400; Lemma CB numerics; independent enumeration eps<=23, minima 2,3,4,5,5,6,6,7,7,8,8;
  eps=11 catapult words exactly BBBAA and BBBBA (resonant d=-3)).
- Auditor 2: `1. all correct` (50,000 random states, independent enumeration eps<=23, same minima and words).
  Both auditors judged (i)-(iv) complete; the adversary's (v) example supersedes that.
- Patches (coordinator): all items; finite-precision test added to verify_shift.py (rerun PASS).
  Targeted re-review 1: remaining MEDIUM — the 3^r event threshold was too loose (r up to ~0.3x breaks
  the per-letter layer); fixed to 3^r>x with Gt=3log2x+4 layers (events need W_pre>=min(1.5x-5,
  x^2/4-2,150), l_pre>=38), rational-slack thresholds computed (l*>=7, Gt^(6)<N0 below T4), CB stated
  with automaton value exactly 5/-11 and |d_y|<=5 derived. Targeted re-review 2: one LOW wording
  ((ii) is not a subset of (i); in-window rational residues are window-certified) — fixed.

VERDICT: ACCEPTED. Theorem S (exact a-step identity D'=3+2k-(D+x')/3; reduced automaton with precision H;
certified c shift s(n)=Phi-2 for every history incl. catapults and nested c; denominator divides
3^(#non-descents)); Lemma ND; Lemma CB; Theorem L [A+B]: simple crossing, eps>=7, omega>=N0 ⟹ n+1>=T4;
Corollary (inside the least strict-EXT counterexample induction): J<T4: EXT(J) ⟸ H5_res ∧ C7 with
residual sources (i)-(v). The case-(iii) 2-layer shape (H5 probably not automatic below T4) is a [C]
heuristic. EXT open; K_clock unchanged.
