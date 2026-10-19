# Three-way review of work_claude_ext_next (Claude subagent, "defect calculus"), 2026-10-19
Reviewers: adversary = Claude subagent (scratch aud53; scripts rerun on a copy, json identical apart from timing);
auditor 1 = agy gemini-3.8-flash-high (blind, aud51, agy_aud51.log); auditor 2 = cmdc deepseek-v4.1-flash (blind,
aud52, cmdc_aud52.log).
- Adversary: `2. with fixable gaps`, no structural break. Stands: SHIFT and the automaton A: d→3−d, B: d→d−1,
  C(w): d→d+Φ(w)−2; LOW, DR, P2 under the descent hypothesis DH (P2 for arbitrary mixed histories; J′ always an
  actual earlier crossing; δ=1 via uniform fire transfer is legitimate); A-SOURCE = P2 at i=1 (unconditional);
  parity/bounds; OB steps 1–3. MEDIUM: §1 consequence wrong for type a with d=1 (gives defect 2, AB); "DH automatic
  for fixed deficit" missed the resonance 6k+2d=0 and z>0 (retagged [C]); DH used silently in the one-step collapse
  and OB step 4 (new hypothesis DH_out). LOW: "two new δ per deficit" argument incomplete (now [A-sketch]); "iff"
  wording; "same remainder as PLUS" → same class; presentation.
- Auditor 1 (gemini): `2. with simple errors` (same §1 point); everything else recomputed.
- Auditor 2 (deepseek): `2. with simple errors`: OB step 4 omitted the u-term (exact x_out=3·2^{m−1}u+2(3k+d−1);
  counterexample (5,1,6,1) is a DH_out failure, so under DH_out the stated parameter holds); |Φ−3/2|<=W/2−1/2 only for
  A-ending histories (prefixes: |Φ−1|<=W/2); z=0 example (12,4), d=−12; r>=3 restriction; δ=0 closure only for DR
  sources. Large recomputation: SHIFT 190,200; grammar ε=3..15; 8,480,572 family scans over m<10^6; 3054 c-source DR
  checks; 14k b entries; 13,669 LOW/descent chains — all consistent.
- Patches applied; targeted re-reviews (adversary): three rounds, final `1. closed in all states`.
VERDICT: ACCEPTED (conditional results under DH / DH_out as stated). Main consequences: every c-source history
reduces (under DH) to the single family G_δ(p)=(6k_p+4−2δ, 6k_p+4−δ), closed for δ∈{0,1,2} and via P2; deficit-by-
deficit casework cannot converge (two new open δ per deficit, [A-sketch]); outer type-b entries reduce (under DH,
DH_out) to H_{4−d}(m) only when the copied fire's exit ends at its first a-step. Remaining target: a uniform theorem
that shifted real chains (δ∉{1,2}, families G_δ/H_δ) end with record below their precision, together with DH at all
scales. EXT open; K_clock unchanged.
