# Three-way review of work_claude_global (2026-10-14; all reviewers Claude subagents, low effort; condensed)
- Adversary: `2. with fixable gaps` — b/c first-step residue unproved; precision checked at step 1 only;
  only one r=3 case independently checked; (ii) b/c descent bound lacked justification; gap list missed
  b/c→a; DL⇒(EL) silently uses (C1); wording (s vs s′, "[A] hand-derived").
- Auditor 1 (numeric, blind; own C λ-walker + bigint F in aud20/): `2. with simple errors`. Confirmed
  tau(50148476)=44,739,242, type a, head λ=2^27−1; exit (50148477,27,6,1), types aaba, r=3, no tie.
  j1 formulas hold in 12,111 cases (J=2 degenerate); a→a j2 formula 316/316; with b-type first step it
  fails 38/317 (formula was only derived for type a — now stated). 3,200 sampled J<10^6: r≤2, no ties.
- Auditor 2 (logic, blind): `2. with simple errors` — all algebra verified (m≥8 no-tie threshold sharp);
  required explicit validity conditions, fix of "1 and ν(s) respectively", DL⇒(EL) placed inside the
  Theorem M induction, b-type canonical state marked unproved.
- Patch (coordinator): all items applied; b-type residue c_X=3·2^{n−1} ⇒ x1≡λ_X mod 2^{J−2}; c-type via
  Lemma 3.2/2.1; skeleton now checks precision at every step (rerun to 4·10^8 unchanged; 7 uncertified
  n≤13, covered by V4); gap split into G1 (a→a collision) and G2 (a after b/c).
- Targeted re-review (adversary): `1. closed in all states` (optional citation for τ(n)≤n added).
