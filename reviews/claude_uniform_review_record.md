# Three-way review of work_claude_uniform (Claude, direction A), 2026-10-24
Target: work_claude_uniform/NOTES.md and margins.py, fullres.py, gates.py, ent.py, real_walks.py.
Reviewers: adversary = Claude subagent (aud77; reran subsets of gates.py, 244k independent integer walks, own full-residue
scan); auditors 1, 2 = agy gemini-3.8-flash-high, blind (aud75, aud76). The author is the coordinating session.

- Adversary: items 1–3 (Lemma NT/LC, full-residue scan and HP transfer, faithfulness of the symbolic gate model)
  `1. all correct`; Lemma GD `2`; Theorem UA `2`, Corollary UA1 `3. wrong`; §6 `3. wrong` (overclaim).
  HIGH: UA1 used Theorem L (work_claude_shift) far outside its proved range (large phase x>=N0, n+1<T4) and its
  rational slack exceeds the G' allowance for x∈[512,1500]; §0/§6 "supersedes / R1, C7, H5_res, RES not needed"
  overclaimed (non-simple sources and source-epoch RES are assumed, not removed). MEDIUM: UA missing the
  "<=3 gates per region" hypothesis and rank counting by non-descents; Lemma GD mechanism wrong (small parts grow via
  additive Theta, b-steps lose 2 bits; Y_A=252 boundary fails; Z_t≠0 not argued). LOW: cap arithmetic, gate counting
  terminology, equality with lift, margins.py assertion, finiteness wording.
- Auditor 1: `2. with simple errors` (overclaim; rank in the region can reach 7, breaking the GD constant; m<=y−4
  unjustified; UA1 label). Auditor 2: `2. with simple errors` (overclaim; UA missing hypothesis; GD summation constant).
  Both recomputed the margins (min 1,048,551 at j=22), the 24 exceptions (lift-independent) and affine walk samples.
- Patches (coordinator): UA1 WITHDRAWN (RH for J<T4 marked [C] open); §0/§6 rewritten as an alternative reduction;
  UA adds (RH-c) <=3 non-descents per region walk and (NZ), ranks counted by non-descents, finiteness via Gamma;
  Lemma GD rewritten (additive Theta growth, |Z_t|<=max(|Z_0|,4max|Theta|+72), 2-bit loss on b-steps, rank<=7,
  threshold y>=216); [B] extended to full caps for y<500 (51.9M walks in total; 4 walks at y=411/422 with rank 4 pass
  two true NT gates, still block-safe); margins.py asserts the lemma inequality. Targeted re-review: all original
  items closed; new issues fixed (the claimed automatic NZ for y>=3.5·10^7 withdrawn — lambda_Y can cancel 3tau;
  Z_0 term restored; double-gate locations; stale text).

VERDICT: ACCEPTED as a conditional reduction. Theorem UA [A+B]: inside the least strict-EXT counterexample induction,
for every J, S(J) is tie-free under RH: (RH-a) 3^r(3k_j+h_j)<2^(j-2) at a-chains j>=19, (RH-b) rank<=4 and height
<=(2048,2048,760,330,190) at every arrival into chains <=18, (RH-c) <=3 non-descents per region walk, (NZ) for arrivals
from y>=500. Ingredients: Lemma NT/LC (no odd-a chain at 19–21; DEPTH margins >=1,048,551 from j=22), full-residue
certify for j<=18 (24 exceptions), gate-block safety ([B] y<500; Lemma GD [A|NZ] y>=216). Not a replacement of the
accepted J<T4 reduction; whether RH holds in any range is open. EXT open; K_clock unchanged.
