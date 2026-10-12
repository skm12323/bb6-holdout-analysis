# U1 — Sibling equivalence: M1, M2, M3 reduce to the same block map M as M0

Foundation (frozen, not modified): `work_q4/RULES.md` (M0 = `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---`, the block
map M, rows R1,R1',R2,R2',R3,R3',R3'',R3k,R4,R5,R6,X0, halting set H = H1∪H2∪H2'∪H3, Inv I1–I4, L1 coverage, L2
invariants, Reduction Theorem v2, c_0=([1,1],A,0)), and `work_q6/LEMMAS.md` (B0 [Class-B], Corollary U, Theorem RHC).
Checker: `verify_u1.py` imports the run-length prover of `work_q4/verify_q4.py` unchanged (it only swaps the module's
transition table) and adds case splitting on a variable (v:=0 / v:=v+1); in fact no row needed a split.
Notation exactly as RULES.md Sec.0/2: `S>` = head in state S reading the first cell to its right; window principle:
the prover aborts if a step reads outside the written window, so every rule holds in any context.
"Steps" = TM transitions executed; "halts after h" = after h transitions the machine is in its halting (state,symbol).

## 0. Transition tables (read from the bbchallenge strings)

| | M1 `1RB0LD_1LC1RD_0LE1LA_0RB1RD_---0LF_1RA1LF` | M2 `1RB1RA_1LC0RC_1RE0LD_0RE0LF_1RA---_1RB1LF` | M3 `1RB1RC_1LC0LE_1RD1RC_1LB0RA_---0LF_1RD1LF` |
|---|---|---|---|
| A | 0:1RB 1:0LD | 0:1RB 1:1RA | 0:1RB 1:1RC |
| B | 0:1LC 1:1RD | 0:1LC 1:0RC | 0:1LC 1:0LE |
| C | 0:0LE 1:1LA | 0:1RE 1:0LD | 0:1RD 1:1RC |
| D | 0:0RB 1:1RD | 0:0RE 1:0LF | 0:1LB 1:0RA |
| E | 0:**HALT** 1:0LF | 0:1RA 1:**HALT** | 0:**HALT** 1:0LF |
| F | 0:1RA 1:1LF | 0:1RB 1:1LF | 0:1RD 1:1LF |

Halting transition: M1 (E,0); M2 (E,1); M3 (E,0). In all three, F is a left sweep (1LF) whose stop on a 0 plays the
role of M0's A-phase position.

## 1. Encodings [Class-A, definitions]
Block lists, phases, indices and Inv are exactly those of RULES.md Sec.1. encode_i is obtained from M0's encode by a
fixed local change around the head; everything else (blocks, single gaps, 0^inf) is identical.

* **Phase A at i.**  M0: `1^{b_{i-1}} [0] 0 1^{b_i} 0 0 1^{b_{i+1}}` (head A on first cell of g_i, g_i,g_{i+1} doubled).
  * **M1**: `1^{b_{i-1}} [0] 1^{b_i+1} 0 0 1^{b_{i+1}}` — g_i single, A-block stored with length **b_i+1**, state **F** on g_i.
    (This is literally M0's own tape 2 steps earlier, in state E — hence the "identical tapes at left-edge events".)
  * **M2, M3**: `1^{b_{i-1}} [0] 1^{b_i} 0 0 1^{b_{i+1}}` — g_i single, A-block length b_i, state **F** on g_i
    (hence "first block one shorter" relative to M1/M0-E; for b_i=0 three zeros, head on the first).
  * i=0: the left neighbour is 0^inf; the head cell is the 0 immediately left of block 0 (block 0 starts at head+1).
* **Phase D at i** (b_i≥2). M0: all gaps single, head D on the second cell of block i.
  * **M1**: identical to M0 (state D, second cell of block i).
  * **M2** (state **B**) / **M3** (state **D**): all gaps single **except g_{i+1}, which is absent** (block i and block
    i+1 are contiguous); head on the cell right after block i, i.e. the first cell of block i+1 (for i=m-1: the 0
    after the last block).
Each encode_i is injective up to translation (the head/state mark the modified gap). Symbolically, the LHS/RHS of each
sibling rule below is the image of M0's RULES.md Sec.2 window under this substitution (`verify_u1.conv`); for M2/M3 the
D-windows whose RHS ends at the D-block are extended by one trailing cell (the gap g_{i+1}), which is required since
those machines write it.

## 2. Rules [Class-A, symbolic for all parameters ≥0; verify_u1 Sec.1]
Sec.2 parameters (p,n,j,k,a,b,q as in RULES.md Sec.2). Every listed rule maps encode_i(c) to encode_i(M(c)) exactly.

| Row | M1 window → (steps) | M2 (steps) | M3 (steps) |
|---|---|---|---|
| R1 | `0 1^p F> 0 1^{n+3} 0 0 1^j` → `0 1^{p+1} F> 0 1^{n+1} 0 0 1^{j+1}` (2n+11) | `0 1^p F> 0 1^{n+2} 0 0 1^j`→`0 1^{p+1} F> 0 1^n 0 0 1^{j+1}` (2n+9) | same window (2n+7) |
| R1' | p-block → 0^inf, RHS `0^inf 1 F> …` (2n+11) | (2n+9) | (2n+7) |
| R2 | `0 1^{p+1} F> 0 1 0 0` → `F> 0 1^{p+1} 0 0 1 0` (p+8) | `0 1^{p+1} F> 0 0 0`→`F> 0 1^p 0 0 1 0` (p+4) | (p+4) |
| R2' | **halts** after 15 (row not realised) | `0^inf F> 0 0 0 1^{j+2} 0`→`0^inf 1^3 0 1^{j+2} B>` (j+12) | **halts** after 3 |
| R3, R3' | → `… 0 1^{j+3} 0 1 D> 1^{k+1}` (j+21) | `… 1^j 0 1^{k+2} 0`→`0 1^{p+1} 0 1^{j+3} 0 1^{k+2} B>` (j+k+10) | (state D) (j+k+10) |
| R3'' | (2j+25) | (2j+9) | (2j+11) |
| R3k | (6j+117) | (6j+63) | (6j+63) |
| R4 | `0 1 D> 1^{a+1} 0 1^{b+2}` → `0 1^{a+2} 0 1 D> 1^{b+1}` (a+3) | `0 1^{a+2} B> 1^{b+2} 0`→`0 1^{a+2} 0 1^{b+2} B>` (b+5) | (state D) (b+3) |
| R5 | (2a+6) | `0 1^q 0 1^{a+2} B> 0^inf`→`0 1^q F> 0 1^a 0 0 1 0^inf` (a+3) | (a+3) |
| R6 | (a+61) | (28) | (30) |
| X0 | **halts** after 15 | (15) | **halts** after 3 |

(The exact windows of every cell are printed by `verify_u1.py`; all are encode_i images of RULES.md Sec.2.)
Block-term step counts (RULES.md Sec.3 convention: n=b_i, L=b_i in D, p=b_{i-1}):

| Row | M0 | M1 | M2 | M3 |
|---|---|---|---|---|
| R1/R1' | 2n+13 | 2n+7 | 2n+5 | 2n+3 |
| R2 | p+9 | p+7 | p+3 | p+3 |
| R2' | 13 | halt 15 | b_1+10 | halt 3 |
| R3/R3' | b_{i+1}+7 | b_{i+1}+21 | b_{i+1}+b_{i+2}+8 | b_{i+1}+b_{i+2}+8 |
| R3'' | 2b_{i+1}+15 | 2b_{i+1}+25 | 2b_{i+1}+9 | 2b_{i+1}+11 |
| R3k | 6b_{i+1}+105 | 6b_{i+1}+117 | 6b_{i+1}+63 | 6b_{i+1}+63 |
| R4 | L+5 | L+1 | b_{i+1}+3 | b_{i+1}+1 |
| R5 | 2L+10 | 2L+2 | L+1 | L+1 |
| R6 | L+51 | L+59 | 28 | 30 |
| X0 | 25 | halt 15 | 15 | halt 3 |

All realised rows take ≥3 steps.

## 3. Halting correspondence [Class-A, verify_u1 Sec.2]
| H-part | M0 | M1 | M2 | M3 |
|---|---|---|---|---|
| H1 (A,0,b_0=0,b_1=1,m≥3) | halts 14 | **halts 15** | **halts 9** | **halts 3** |
| H2/H2' | j+8 | not claimed (no halt in window) | **halts j+7** | not claimed (mixed/undetermined branches) |
| H3 | L+6 | not claimed (D passes 1-blocks; leaves window) | **halts 2** | not claimed |

* **M2: H_2 = H exactly**, and all twelve rows are realised: M2 is a full conjugate of M on Inv.
* **M1, M3**: H1 halts; additionally the sibling halts on the whole domains of R2' and X0 (all (A,0) with b_0=0), so
  their halting set contains H1 ∪ dom(R2') ∪ dom(X0); on H2, H2', H3 their behaviour is not claimed (M1 provably does
  not halt inside the window; M3 is branch-dependent). Every other row agrees with M.

## 4. Base lemmas [Class-A as finite symbolic computations; verify_u1 Sec.3]
From blank tape in state A: M1 reaches encode_1(c_0) after **12** steps, M2 encode_2(c_0) after **11**, M3
encode_3(c_0) after **9**, with c_0 = ([1,1],A,0), the same starting point as M0 (21 steps).

## 5. Unused-row lemma [Class-A | B0]
**Lemma P [Class-A].** Along the M-orbit (c_s) from c_0, rows R2' and X0 never apply. Proof: the only row whose result
is phase (A,0) is R2 from (A,1) (R1',R3''/R3k at i=0, X0 go to A at 1; R1,R3'',R3k keep i≥1; R5,R6 put A at ≥1; R3/R3'/R2'
go to D). R2 sets the old A-block b_1:=1, so R2' (needs b_1≥2) is excluded; X0 needs m=2 at (A,0), which would come
from (A,1) with m=2, violating I3. c_0 has b_0=1. □
**Lemma Q [Class-A | B0].** Along the orbit, H2, H2', H3 (and R6) never apply: B0 lists the rows of c_0..c_20 and
finds none in H; Corollary U (LEMMAS.md) excludes them after c_9. Hence the first H-hit, if any, is H1 (also RHC).

## 6. Theorem (sibling equivalence)
**[Class-A | Q4-L3-style base, B0 for M1/M3].** For i∈{1,2,3} let τ^i_0 = 12/11/9 and τ^i_{s+1} = τ^i_s + steps_i(c_s).
(i) At time τ^i_s the tape/state/head of Mi equal encode_i(c_s), for every s up to the first H-hit;
(ii) **Mi halts ⇔ the M-orbit of c_0 hits H ⇔ M0 halts.** On a hit (always H1) Mi halts h_i=15/9/3 steps after τ^i_s.
Proof. Base (Sec.4); induction: c_s ∈ Inv matches exactly one row (RULES L1, L2 for M alone); if it is not in H, the row
is realised by Mi (Sec.2) — for M2 unconditionally, for M1/M3 because R2', X0 are never used (Lemma P). If c_s∈H it is in
H1 (Lemma Q; for M2 not needed) and Mi halts (Sec.3). Every realised row takes ≥3 steps, so with no hit τ^i_s→∞ and Mi
never halts. M0 side: RULES.md Reduction Theorem v2. □
For **M2** the statement holds for every Inv starting configuration (exact conjugacy, no B0 needed); for **M1, M3** it is a
statement about the orbit of c_0 (on arbitrary Inv configs they differ from M on dom(R2'), dom(X0), and possibly H2,H2',H3).
Consequently every orbit-level result about M0 (B0, Corollary U, Lemma E, Theorem RHC, Lemma W and its Corollary, P1;
and the Class-C observations P2) transfers verbatim to M1, M2, M3; only the TM-time bookkeeping changes (tables above).

## 7. Checks [Class-C]
* verify_u1 Sec.4: every Inv config with m≤5, blocks≤4 (≈9.4–10k per machine) run raw from encode_i(c) lands exactly on
  encode_i(M(c)) at the claimed step (or halts at the claimed step).
* Sec.5/6: raw Mi vs the abstract orbit with Mi's step counts, t ≤ 3·10^6 Mi-steps: M1 14,624, M2 14,652, M3 14,668
  checkpoints matched exactly (= c_0..c_{N} of M0's orbit, compared list-for-list with verify_q4's macro); no halt.
* Run: `python verify_u1.py [N]` (default N=3·10^6, ~10 s).
