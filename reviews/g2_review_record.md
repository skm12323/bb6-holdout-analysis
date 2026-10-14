# Three-way review of work_g2 (2026-10-14; condensed)
- Adversary (Claude): `2. with fixable gaps` — (A) valuations exact and distinct, q−1=1+v2(k) excluded by
  τ bound; table for J ≤ 11 necessary (J=12 first good); B1 and copy lemma sound; Theorem B not circular;
  C1/C2 re-derived. 7 items: (C1) indices < ρ; σ^R_t undefined; Theorem B base; J=50148477 non-sequitur;
  "Consequence" overclaims; C2 rows a,a / b,a untested; q ≤ J−4 and F1/F2 citations.
- Auditor 1 (Claude, blind, own F): `1. all correct` — 60,575 epochs recurrence = F; 424,025 symbolic
  b-first steps, 22,155 b→a cases (j₂ ≤ q−2), 366,615 B1 runs, 9,498 exact copies, 2,262 collisions all
  ending; no real b→a or a→b/c epochs below 2·10^5 (symbolic only).
- Auditor 2 (deepseek-v4.1-flash, by hand): `1. all correct`.
- Patch (Claude subagent, 8 items) → targeted re-review (deepseek): `2. with fixable gaps` — collision count
  40→39; Theorem B base: V2 certifies only r ≤ 2 (tail-length arm), not descent; (S1) citation for the
  source fire. Applied by coordinator with the reviewer's content. ACCEPTED.
