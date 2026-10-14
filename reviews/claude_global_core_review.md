# Three-way review of work_global_core (2026-10-14; all reviewers Claude subagents; condensed)
- Adversary: `1. closed in all states`. Two-a identity re-derived (no residues, no NT); "no three
  consecutive large chains" proved (b/c return lands below K via (C1) at j−1<g; two odd a-returns ⇒ next
  j<K); count 3m+2; conditional theorem inequalities (156515, 666216, 16984837.5; deficit cubic ≤ 9x³ at
  x=26) and bootstrap verified; verify_core.py rerun identical. Editorial: CORE2 is equivalent (×3 budget)
  to the old exit-length lemma, not easier; CORE2 first wording circular; real-orbit checks barely test
  the claims; 17,5,17,17,1 shows two-in-a-row attained, not 3m+2 tightness; §3 notation; script rewrites
  its own json.
- Auditor 1 (blind, own F rebuilt from PROOF_M/EL/RESCUE): `1. all correct`. Real orbit to pointer 10^6:
  302,878 epochs, r ≤ 2; 28 real two-a cases all exact (equal parity ⇒ next j=1); 30 chains above cutoff,
  none adjacent (vacuous on real data); N ≤ 3m+2 everywhere; max m = 3, m/g² ≤ 0.0156 (C);
  independently constructed 44/179 states realizing 17,5,17,17,1.
- Auditor 2 (logic): `1. all correct`. All hypotheses ((C1) only at earlier crossings; b/c bound valid for
  rescued/non-NT chains; POS exact) available in the induction; theorem scoped to F.
- Patch (Claude subagent): 7 wording/scope fixes applied; coordinator spot-checked.
