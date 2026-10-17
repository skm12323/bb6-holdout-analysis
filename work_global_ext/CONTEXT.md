# Shared context for EXT subagents (2026-10-17)

Machine #1 = bbchallenge BB(6) holdout `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`.
A read-only copy of the research repo is at
`/tmp/claude-0/-home-claude/953d4959-da77-5aa9-bfe6-caac149292ed/scratchpad/repo` (call it REPO).

## Where the global proof stands

The whole non-halting proof has been reduced (reviewed, accepted) to ONE open proposition:

**(EXT)** For every integer J ≥ K′ (K′ = 2^(2^(2^499997−3)−2), astronomically large), if the pair map F
is defined through step τ(J−1), then the symbolic exit S(J) is tie-free at every chain it reaches.

Read first, in this order:
1. `REPO/work_global_egx/PROOF_EGX.md` – the reduction (Theorem U: EXT ⇒ never halts), definition of S(J)
   in §1, Theorem L in §6 (LIN-EXIT ⇒ EXT, plus the unconditional by-product: given EXT below J, the first
   ⌊J/(3 log2 J)⌋+1 exit chains of S(J) are automatically tie-free; so EXT(J) can only fail if S(J) runs
   more than J/(3 log2 J) exit chains).
2. `REPO/work_m/PROOF_M.md` (pair map, crossings X(n), τ(n), ε(n), types a/b/c, returns, Lemma 6.1 symbolic exit)
   and `REPO/work_m/verify_m.py` (functions building F, the crossing table `Xdata`, and `sym_exit`).
3. `REPO/work_el/PROOF_EL.md` – exit automaton (j, θ=(3s+5) mod 2^j), Lemma T (tie-free ⇔ v2(β_x) < v2(α_x)=J−Γ_t;
   1 ≤ β_x ≤ 6d_t−1), Theorem B (descent NT ⇒ EL), Theorem D, §6 why bootstrap stops, §7.
4. `REPO/work_tie/PROOF_RESCUE.md` (rescue macro for NT failures, §4 one more tower level) and
   `REPO/work_tie2/PROOF_TIE2.md` (extended automaton, level generator, level-3/4 certificates, §7 the precise
   obstruction: θ windows grow by 2 per tower level; level 5 needs a hidden-k symbolic state; rational 3-adic
   families such as 10/3 appear).
5. `REPO/work_global_egx/verify_egx.py` – self-contained; contains `endgame(v)` and `symexit(J)`; builds F up to N
   crossings (`python -B verify_egx.py 30000` ≈ 4 s). Good starting code for experiments.
Other context: `REPO/CHECKPOINT_1RB1LA_0RC0RD.md` (full history; long), `REPO/work_global_clock/PROOF_CLOCK.md`
(τ(n) ≤ nP(n)), `REPO/work_global_endgame/LEMMAS_E.md`, `REPO/work_r1/RULES.md`, `REPO/work_r4/PROOF.md`,
`REPO/work_g2_obstruction/`, `REPO/work_global_calendar_survey/` (deep-J S(J) survey: longest exit r=4).

Key facts: after the first exit chain, every exit chain has j_t ≤ log2(6 d_t) = O(log J), so it reads crossing
data X(m) only at small indices m = O(log J). α_x = 2^{J−Γ_t}·odd, so parities and valuations of chain values are
determined by the β-parts as long as Γ_t < J. Γ_t = Σ_{t′<t}(1+ε(n_{t′})).

## Rules for you (a research subagent)
- Do NOT call any `mcp__hearthbot__*` or `mcp__remote-devices__*` tool. Do not write under /mnt/project-files.
  Do not modify REPO. Work only in your own folder (given in your task). Python standard library only.
- Mark every claim [A] (proved for all parameters, with proof written out), [B] (finite computation, with the
  script that reproduces it) or [C] (heuristic/empirical/conjectural). Never present [C] as proof.
- Be your own adversary: before reporting a proof, try hard to break each step, check it numerically on small J,
  and say which steps you are least sure about.
- Write your full report as `REPORT.md` in your folder (plus scripts), and also return it (or a faithful,
  complete summary with all key statements and proofs) as your final message. A negative result
  (precise obstruction, counterexample, or "this route reduces to X") is a valuable outcome; report it honestly.
