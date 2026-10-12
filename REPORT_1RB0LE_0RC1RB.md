# Arbitration Report: `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---`

**Status: UNDECIDED. The machine is reduced exactly to an open arithmetic problem (cryptid-type).** HALT = F reading 1.

## Accepted theorems (Stage 3 passed)

**Theorem 1 (Reduction v2)** (`work_q4/RULES.md`, `verify_q4.py`).
- From blank tape, the TM is at block configuration ([1,1], A, 0) at step 21.
- From then on it is exactly simulated by the block-list map M, which has 12 rules.
- The TM halts ⇔ the M-orbit hits H. H consists of 3 explicit block patterns.

**Theorem 2 (Refined Halting Criterion + Sweep Map)** (`work_q6/LEMMAS.md`, `verify_q6.py`).
- Steady set S is closed. The only exit is H1; R2′/X0/R3″/R6/H2/H2′/H3 never fire after c_9.
- Halting ⇔ some real left-edge arrival (s ≥ 10) has u0 ∈ {2^k − 2 : k ≥ 2}. Halting is always through H1.
- Equivalently, from c_20 on (b_s ≡ 10):

  **TM halts ⇔ ∃ sweep with e_{s−1},…,e_1 all even and e_0 a power of 2 (≥ 4),**

  where e_t = Σ_{r=t}^{s−1} b_r·2^{t−r} + 12·2^{t−s}.
- The sweep-to-sweep map is given exactly by Lemma W.

Gate: Class C = 0, Class B = 1 (B0: c_0..c_20 by exact computation).

## Open problem
Show that the averaging-carry system of Lemma W never produces an all-even chain that ends in a power of 2. It is a growing-dimension 2-adic carry map, and u0 is not a function of the previous u0 alone.

## Evidence (Class-C, not part of the theorem)
- Real arrivals in 3·10^6 sweeps: u0 = 7, 23, 21, 24, 104, 1290, 647, 7146, 93998, 281082. None is of the form 2^k − 2.
- The probability that a chain passes ≥ k positions decays roughly like 2^{−k}, so arrivals become rarer as the block list grows. Heuristically the machine does not halt.

## Review trail
- Round 1: Q1 reduction draft. The adversary reported `structure broke` because the T4 iff missed a halting route, so it was fuse-reset.
- Round 2: Q4 Reduction v2. Adversary: fixable gaps. Auditors: all correct ×2. Patched, then re-reviewed. Accepted.
- Round 3: Q6 RHC + Lemma W. Adversary: fixable gaps (7 editorial). Auditors: all correct ×2. That gave 1.2M Lemma W vs M cases and 1.1M closure configs with 0 mismatches. Patched, then re-reviewed: fixable gaps (2 wording items). The coordinator applied the adversary's prescribed wording verbatim and verify_q6.py re-ran clean. Accepted.

## Side claim (superseded — see Sibling equivalence below)
The siblings `1RB0LD_1LC1RD_0LE1LA_0RB1RD_---0LF_1RA1LF`, `1RB1RA_1LC0RC_1RE0LD_0RE0LF_1RA---_1RB1LF` and `1RB1RC_1LC0LE_1RD1RC_1LB0RA_---0LF_1RD1LF` show matching tapes at left-edge events. This is Class-C only; no equivalence has been proved.

## Sibling equivalence (task B) — ACCEPTED (Stage 3: closed in all states / all correct / all correct)
Files: `work_u1/EQUIV.md`, `work_u1/verify_u1.py` (imports work_q4 prover).
- M1 `1RB0LD_1LC1RD_0LE1LA_0RB1RD_---0LF_1RA1LF`, M2 `1RB1RA_1LC0RC_1RE0LD_0RE0LF_1RA---_1RB1LF`, M3 `1RB1RC_1LC0LE_1RD1RC_1LB0RA_---0LF_1RD1LF` are each simulated by the same block map M via local re-encodings encode_i; all rows proved symbolically per sibling; base: blank → encode_i(c_0) at t=12/11/9.
- **Theorem: M0, M1, M2, M3 all halt or all run forever** (each halts ⇔ M-orbit of c_0 hits H, always via H1). M2 is conjugate to M on all of Inv; M1/M3 rely on Lemma P (proved) and Lemma Q (via audited B0 + Corollary U).
- Audit evidence: 185,550 exhaustive + 30,000 random configs per sibling (0 mismatches); raw orbits of all four machines match encode_i(c_s) to 10^7 TM steps (~30,000 checkpoints each); 150 orbit-point starts agree on halting across all four.
- Consequently the refined criterion (Lemma W / u0 ∉ {2^k−2}) governs all four machines.
