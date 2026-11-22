# Final independent review of work_mixed_bridge (global strict-EXT / non-halting proof), 2026-11-22
Target: work_mixed_bridge/PROOF.md (§§1–5) and SMALL_BASE.md, with verify_bridge.py, audit_bridge.py,
verify_source_prefix.py and the base enumeration work_g2_core_words/ (word_search.py, words_1023.json). Author: GPT-6.2
Astra (commit 4d80eab); earlier panel: three ZCode GLM 5.3 reviewers, unanimous `1` (reviews/gc_mixed_bridge_*.md),
plus a Codex follow-up correcting an audit loop. This round used reviewers of other model families, none of whom read
the GLM panel's conclusions before forming their own.

- **Adversary A (Claude Opus 5.5; §§1–4 and word semantics; D:/math_cc_astra/final_advA): `1. closed in all states`.**
  Own rank-2 lattice/HNF enumerator with block maps fitted from the exact walk: 325 productive inputs; word counts
  325/105625/25438/17378/6271/504/0 (lengths 1..7); max block loss 3; escape-node distribution; cap 63 matches
  words_63.json. Integer lifts of all 24,153 base words of length 4–6 replayed exactly; for h ∈ {5,…,60}, 89,853
  adjacent bridge pairs: Z_i ≡ 0 mod 2^(h+1) always, and p_(i+1) = p_i − t_i in all 83,608 pairs with Z_i = 0; mixed
  s_i legitimate; no counterexample, and the algebra excludes one. Bound (1) on all canonical rows q <= 20000 with
  large slack; MASS on every b/c row. §§3–4 arithmetic and the scale induction re-derived. Low stretches are covered
  (free initial state). The eternal synthetic 7,9,… trains are impossible on the canonical calendar (7, 9 are not
  productive; productive alphabet 5, 8, 12, 14, …). LOW: findings 1, 3, 4, 5, 8 of the review block.
- **Adversary B (Claude Opus 5.5; §5 and SMALL_BASE; D:/math_cc_astra/final_advB): `1. closed in all states`.**
  λ_u = 0 lift of S(J) is an integer walk; the count A <= g+1 handles catapults, non-descents, the root, an unfinished
  tail and the candidate transition; j_t + Γ_t < J excludes over-ties too, so strict EXT (Theorem U's hypothesis) is
  proved; the strict induction is non-circular (every EXT use at J_W < J, antecedents inherited); direct-bound
  arithmetic (18l²+61l+31 <= 32l² < 2^(l−2)); SMALL_BASE clock induction; Theorem U chain. All three author scripts
  re-run: PASS. LOW: findings 2, 6, 7 of the review block.
- **Auditor 1 (DeepSeek v4.1 flash via cmdc, blind, numerical; aud96): `1. all correct`.** Own 2-adic lattice
  enumeration reproduces 325 / 105625 / 25438 / 17378 / 6271 / 504 / 0 and max loss 3 (16 blocks with loss 3);
  4,890 random integer lifts confirm the block map and its bounds; (1) on 63,746 blocks q < 2·10^5; 3,000 random
  bridges confirm (2); on real feasible words with >= 3 highs Z_i = 0 and the p-recursion exactly; the §3 witness
  reproduced; SMALL_BASE statistics 389/586/48, max loss 4, τ(n) <= n, τ(1022) = 910; 4,779 numerical inequalities.
- **Auditor 2 (DeepSeek v4.1 flash via cmdc, blind, logic; aud97): `1. all correct`.** §§2–5 and SMALL_BASE checked;
  C2-log used in its accepted J_W < J form; MASS, C1 conditions met; the bypass of the small-chain train obstruction
  holds via the canonical finite core F = 6 [B]. Remarks = review-block items 2, 4, 7.
- (The planned blind agy gemini auditors could not run: the service refused the location and then required a new
  Google sign-in; replaced by cmdc at the user's request.)
- Patches (coordinator): final review block at the head of PROOF.md (LOW clarifications only); status line updated.

VERDICT: **ACCEPTED.** Relative to the repository's accepted imports, the bridge theorem holds — every productive
mixed-block word with input chains in [5,Q], Q >= 64, has length at most Q in the strict induction — and with it strict
EXT for every J (both assemblies: §5 from K′ and SMALL_BASE from J = 1024), hence by the accepted Theorem U the universal
walk F is defined forever and machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` never halts on the blank tape.
Load-bearing computations [B]: the base certificate at cap 1023 (F = 6; reproduced by three independent enumerators)
and the SMALL_BASE prefix checks. Caveat: the imported structural lemmas (RULES reduction, PROOF_M, EGX, E1–E4,
CLOCK/C1, C2-log, MASS, Theorem U) rest on their earlier acceptance records and were not re-reviewed in this round.
