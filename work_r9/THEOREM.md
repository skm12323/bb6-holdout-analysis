# R9: the non-halting theorem for `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`

**Claim.** The machine never halts.

**Status (2026-10-13): CLAIMED, NOT PROVED.** The all-j induction step is false as written (G6 gap, confirmed); the proposed repair via margin inequality (M) itself has open defects (GPT Astra review). Governing status: CHECKPOINT_1RB1LA_0RC0RD.md (last sections). The text below is the original claim record. The proof route
(agent B's closed-form/universal-replay route, scratch/agentB_closedform.md) survived
six adversarial probes, the coordinator's code audit of its verification engines, and
two independent cross-route reconciliations (compositional frames; 2-adic fire table).
The full three-way review per this repository's methodology is incomplete (adversary
and auditor instances were repeatedly killed by infrastructure failures); see
scratch/review_B_coordinator.md for exactly what was checked and by whom.

## Proof architecture (all anchors re-executed by the coordinator)

Base (audited, work_r1): top map; HALT <=> fire with x = A+2b+3 = 2^k; sum = 3n+3;
singletons safe; excursions E(w,v) with n+2 = 2^v w.

1. **Step closed form** [A]: every chain step has x = 2^j·u (u odd), successor
   (u+1; u, 2u, ..., 2^{j-2}u, c+(A+1)/2, S); HALT iff u = 1.
2. **Universal replay** [A, machine base B]: every run-chain at relative position rho
   with odd level base U has x = 3·2^rho·U + (6k_rho+4), j = 1+v2(3k_rho+2), with ONE
   universal sequence (k_rho) (w- and level-independent; (dk, dp) table; verified:
   6372 events rho <= 20000 all levels; extreme w; E(1,v) v <= 4000 cross-route).
3. **Locality** [A, Lemma L0]: queue-determinism — replays never read past their own
   run (front-3 locality of the top map); exits over-read <= 4 tail entries, <= 6 events.
4. **rho-induction** [A, written; instances machine-verified to rho <= 20000,
   j <= 20000]: decrease k_rho <= rho^3 => j_rho < rho (rho >= 32); tie-freeness
   v2(x) = j_rho (U odd at every level: nested U = even + odd); step = finitely many
   interlude/exit identity types.
5. **Safety**: u = 3·2^{rho-j}·U + odd >= 9 at every run chain, every level, every w.
   Exit/endgame chains: scale-part domination (margins p-J >= 900 at deep hosts);
   41 endgame templates verified (v <= 2000); boundary chains affine with positive
   leading coefficients.
6. **ell(v) = 2·k_b(v) + e(v)** [A given the table; verified v <= 5000 with
   e in [0,12]; at v = 6132-6135 e reaches 16 (j=14 spike boundary) — the constant is
   e <= 16; ell <= 2s verified to 6500, max ell/s = 1.0714].
7. **Assembly** => Lemma E(v) for all v, all odd w => (audited reduction) the machine
   never halts.

## Known wording-level gaps (from the review; none load-bearing)

- Section 5 of the proof report overstates the mod-3 "automatic superset" property
  (the no-defect bulk family has sum = 1 mod 3); safety never uses mod 3.
- "Finitely many types verified generically" should read "for margin-protected
  (p >= max(200, j+100)) and on-sequence instantiations": planted halters exist in
  the never-claimed region (small p + off-sequence k), unreachable on the real orbit.
- e(v) in [0,12] -> e(v) <= 16 (see item 6).

## Verification anchors (re-executable)

- python verify_r9.py            — runs the key anchors below (~3-6 min).
- scratch/agentB_run15.py 20000  — invariant I(rho), all levels (0 failures).
- scratch/agentB_run7.py         — per-J abstract verifier (j <= 44 default; extendable).
- scratch/reviewB_probe1..6.py   — adversarial probes (extreme w, j extension,
                                   off-sequence safety, margins, endgame forms).
- scratch/mainline_ell6500.json  — exact ell table to 6500 (formula + ell <= 2s).
- work_r8/verify_r8.py 1000 300  — independent compositional route, v <= 1000.
