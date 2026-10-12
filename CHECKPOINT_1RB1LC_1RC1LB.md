# Invariant Checkpoint — `1RB1LC_1RC1LB_1LD0RB_0LE1RD_---0LF_0LA1LF`

Source: bbchallenge BB(6) holdout list, 2026-09-24 (815 classes), entry #2.
Status: **UNRESOLVED** — assembly gate blocked (no main-theorem draft).

## Frozen results
- **K1 [A, cross-verified by P1 & P3, B-checked]** Halting criterion: halts iff F reads 0 at z with tape[z-4..z] = 0,0,0,1,0; forced chain F0→A1→C0→D0→E0. Halt transition is E reading 0.
- **K2 [B]** Blank tape reaches X(4,2) at step 18821, where
  X(n,a) = `0^∞ 1111 0 11 00 1^{2n} 00 1^{2n+1} 0^a 1 0^{2n−a} 1 0^∞`, state E on the 4th 1, a even.
- **K3 [B]** Cycle map f_n: X(n,a) → X(n+1,f_n(a)) | HALT | leaves-shape, computed exhaustively by simulation for n = 3..8. f_n(0) = HALT for all tested n.
- **K4 [B]** Orbit n=4..11: a = 2,6,4,4,10,4,8,12.

## Empirical (Class-C, not admissible)
- Orbit continued to n=24 (~2.1e10 steps): 4,12,20,24,18,30,16,14,26,10,28,38,24; never hits 0, 2n, or exit values.
- No affine/modular closed form for f_n found; behaves pseudo-randomly in n.
- Random-map heuristic suggests eventual hit of bad set (halt or shape exit) — i.e. a probabilistic cryptid.

## Open gap
Symbolic derivation of f_n (intra-cycle block-cascade macro rules); follow-up of shape-exit ("?") values.

## Arbitration log
- P1 symbolic dynamics: undetermined (reduced to f_n orbit).
- P2 invariant/CTL: broken — no invariant.
- P3 rewrite isomorphism: undetermined; produced K1.
- Gate: C>0, B>1 → blocked; Stage 3 not entered.

Verification scripts: `work_p1/verify_p1.py`, `work_p3/verify_p3.py`.
