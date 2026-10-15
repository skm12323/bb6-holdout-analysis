# Three-way review of ten work_g2_* research notes (GPT Astra, 2026-10-15), 2026-10-16
Targets: resonance, after_reset, shift44, return_block, core_repeats, core_words, paths, escape_5_17,
reentry_budget, escape_two_phase. Reviewers: adversary = Claude subagent (scratch aud29, ran verify scripts on
copies only); auditors 1,2 = agy gemini-3.8-flash-high, blind (aud27, aud28; logs agy_aud27.log, agy_aud28.log).
(An aborted earlier auditor-2 run on claude-opus-4-6-thinking was discarded: aud28_opus_aborted.)
- Adversary: `2. with fixable gaps` — no algebra/congruence/certificate error; reproduced small table, corridor
  stats, both exceptional residues mod 2^60; 12 verify scripts rerun on copies, outputs match; solver logic of
  modular.py/word_search.py sound. Fixes: RESONANCE ρ<=2s+2, explicit hypotheses (S1, ρ=63 fire, C1 at ρ_i),
  G-correction changelog, J>=1024 scope; AFTER_RESET §4 restricted to s=52/parameter-65 ancestries; SHIFT44
  cited unaudited work_global_shadow (replace by accepted copy lemma) + script comment; PATHS §2.3 general-d rule
  unproved; ESCAPE b/c branch relied on d=2 shortcut while R21 has d=0 — residual collision = accepted
  bc_frontier construction, branch open. BLOCK, REPEATS, WORDS, BUDGET, TWO_PHASE: no defects.
- Auditor 1 (gemini): `1. all correct` (key formulas/counts recomputed; large enumerations not rerun, listed).
- Auditor 2 (gemini): `1. all correct` (all ten notes; exceptional classes, word counts 105625/…/0, 165 escape
  nodes, budget and two-phase identities recomputed).
- Patch (coordinator) + targeted re-review (adversary): one residual (SHIFT44 §1 shadow citations) fixed;
  final `1. closed in all states`.
VERDICT: ACCEPTED as conditional/local results. No global non-halting, reachability, or horizon claim.
