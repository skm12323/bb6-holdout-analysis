# Reduction theorem for `1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---` (Q4)

Transitions: A:(1RB,0LE) B:(0RC,1RB) C:(1LC,1RD) D:(1RF,0LA) E:(0RD,1LE) F:(1RB,HALT). Halting = state F reads 1.
Time unit throughout: **TM steps** (one transition each). "Halts after h steps" = h transitions run, then the
machine is in F reading 1; with the bbchallenge convention (the halting step counts) that is h+1.
Checker: `verify_q4.py` (sections 1-5 below refer to its output sections).

## 0. Tape notation
`x^n` = n copies of symbol x. `0^inf` = all remaining cells on that side are 0.
`S>` = head in state S on the **first cell to its right**; `<S` = head in state S on the **last cell to its left**.
Variables (p,q,n,j,k,a,b,c) are arbitrary integers >= 0.

## 1. Encoding convention (Class-A, a definition)
A *family configuration* is (B, phase, i): B = [b_0,...,b_{m-1}] is a list of integers, phase is A or D.
Tape: `0^inf 1^{b_0} g_1 1^{b_1} g_2 ... g_{m-1} 1^{b_{m-1}} 0^inf`, each gap g_k = `0`, except:
* phase A at i: g_i and g_{i+1} are `0 0` (for i=0 only g_1 is doubled, g_0 is the left 0^inf).
  Head in state A on the **first cell of g_i** (the cell just right of block i-1); for i=0, head is
  **two cells left of block 0's first cell** (cell of block 0 is at head+2 if b_0>=1).
  So the local picture is `1^{b_{i-1}} [0] 0 1^{b_i} 0 0 1^{b_{i+1}}`.
* phase D at i: all gaps single; head in state D on the **second cell of block i** (needs b_i>=2).
Zero-length blocks: only the A-block may have length 0; then g_i 1^0 g_{i+1} is a run of exactly
**four** zeros with the head on the first (e.g. t=1466: `1^11 [0]000 1^4`, B=[10,9,11,0,4,2], i=3).
Any other multi-0 gap is not a family configuration. Encoding is injective (up to tape translation).

**Invariants (Inv):** I1 m>=2. I2 every block except the A-block has length >=1 (A-block >=0).
I3 phase A => 0<=i<=m-2 (A-block never last). I4 phase D => 1<=i<=m-1 and b_i>=2.

## 2. Macro rules (each [Class-A], symbolic over all parameters; verify_q4 sec.1, also raw-TM checked for params 0..7)
Window principle: the prover aborts (OUT) if any step reads outside the stated LHS window, so each
rule holds with arbitrary tape outside the window; the cells beyond a `0^inf` must be 0.

| Rule | LHS (tape) | RHS (tape) | TM steps |
|---|---|---|---|
| R1  | `0 1^p 0 <A 0 1^{n+2} 0 0 1^j` | `0 1^{p+1} 0 <A 0 1^n 0 0 1^{j+1}` | 2n+17 |
| R1' | `0^inf 0 <A 0 1^{n+2} 0 0 1^j` | `0^inf 1 0 <A 0 1^n 0 0 1^{j+1}` | 2n+17 |
| R2  | `0 1^{p+1} 0 <A 0 0 0` | `0 <A 0 1^p 0 0 1 0` | p+10 |
| R2' | `0^inf 0 <A 0 0 0 1^{j+2}` | `0^inf 1^3 0 1 D> 1^{j+1}` | 13 |
| R3  | `0 1^p 0 <A 0 1 0 0 1^j 0 1^{k+2}` | `0 1^{p+1} 0 1^{j+3} 0 1 D> 1^{k+1}` | j+7 |
| R3' | `0^inf 0 <A 0 1 0 0 1^j 0 1^{k+2}` | `0^inf 1 0 1^{j+3} 0 1 D> 1^{k+1}` | j+7 |
| R3''| `0 1^p 0 <A 0 1 0 0 1^j 0^inf` | `0 1^{p+1} 0 <A 0 1^{j+1} 0 0 1 0^inf` | 2j+15 |
| R3k | `0 1^p 0 <A 0 1 0 0 1^j 0 1 0^inf` | `0 1^{p+3} 0 <A 0 1^j 0 0 1^3 0 1^2 0^inf` | 6j+105 |
| R4  | `0 1 D> 1^{a+1} 0 1^{b+2}` | `0 1^{a+2} 0 1 D> 1^{b+1}` | a+7 |
| R5  | `0 1^q 0 1 D> 1^{a+1} 0^inf` | `0 1^q 0 <A 0 1^a 0 0 1 0^inf` | 2a+14 |
| R6 (new, D2) | `0 1 D> 1^{a+1} 0 1 0^inf` | `0 1^{a+4} 0 <A 0 0 0 1^2 0^inf` | a+53 |
| X0 (concrete) | `0^inf 0 <A 0 0 0 1 0^inf` | `0^inf 1^3 0 <A 0 1 0 0 1 0^inf` | 25 |

Halting lemmas [Class-A] (verify_q4 sec.2): from the LHS the TM reaches F-reading-1 after the stated steps.

| Lemma | LHS | steps |
|---|---|---|
| H1 (D1) | `0^inf 0 <A 0 0 0 1 0 1^{c+1}` | 14 |
| H2  | `0 1^p 0 <A 0 1 0 0 1^j 0 1 0 1^{c+1}` | j+8 |
| H2' | `0^inf 0 <A 0 1 0 0 1^j 0 1 0 1^{c+1}` | j+8 |
| H3  | `0 1 D> 1^{a+1} 0 1 0 1^{c+1}` | a+8 |

## 3. Abstract map M in block terms (Class-A: each line = a rule above read through Sec.1)
Phase A at i, n=b_i, p=b_{i-1}, j=b_{i+1}, k=b_{i+2}; "…" = unchanged blocks.

| Case (conditions) | Rule | Result | steps |
|---|---|---|---|
| n>=2, i>=1 | R1 | b_{i-1}+1, b_i-2, b_{i+1}+1; A at i | 2n+13 |
| n>=2, i=0 | R1' | [1, n-2, j+1, …]; A at 1 | 2n+13 |
| n=0, i>=1 | R2 | b_{i-1}=p-1, b_i=1; A at i-1 | p+9 |
| n=0, i=0, j>=2 | R2' | b_0=3; D at 1 | 13 |
| n=0, i=0, j=1, m=2 (B=[0,1]) | X0 | [3,1,1]; A at 1 | 25 |
| n=0, i=0, j=1, m>=3 | **H1** | halt | 14 |
| n=1, i+1=m-1 | R3'' | (…,p,1,j)->(…,p+1,j+1,1), A at i; i=0: [1,j]->[1,j+1,1], A at 1 | 2j+15 |
| n=1, i+2<=m-1, k>=2 | R3/R3' | (…,p,1,j,k,…)->(…,p+1,j+3,k,…), D at old k-block, whose index, for i>=1, in the NEW (one-shorter) list is i+1; i=0: [1,j,k,…]->[1,j+3,k,…], D at 2 | j+7 |
| n=1, i+2=m-1, k=1 | R3k | (…,p,1,j,1)->(…,p+3,j,3,2), A at i; i=0: [1,j,1]->[3,j,3,2], A at 1 | 6j+105 |
| n=1, i+2<=m-2, k=1 | **H2/H2'** | halt | j+8 |

Phase D at i, L=b_i>=2:

| Case | Rule | Result | steps |
|---|---|---|---|
| i=m-1 | R5 | (…,q,L)->(…,q,L-2,1), A at i | 2L+10 |
| i<=m-2, b_{i+1}>=2 | R4 | D at i+1 | L+5 |
| i+1=m-1, b_{i+1}=1 | R6 | (…,L,1)->(…,L+2,0,2), A at i+1 (D2: no split on a=0/a>=1 needed; prover is uniform in a) | L+51 |
| i+1<=m-2, b_{i+1}=1 | **H3** | halt | L+6 |

**Step-count conversion (Sec.2 parameters -> Sec.3 block lengths).** R1/R1': A-block length is n+2 in Sec.2, so
with block length n: 2(n-2)+17 = 2n+13. R2: b_{i-1}=p+1 in Sec.2, so with p=b_{i-1}: (p-1)+10 = p+9.
R2', X0: constants 13, 25. R3/R3', R3'', R3k: j = b_{i+1} unchanged (j+7, 2j+15, 6j+105). H1, H2: unchanged (14, j+8).
D-block L = a+2: R4 a+7 = L+5; R5 2a+14 = 2L+10; R6 a+53 = L+51; H3 a+8 = L+6.

(Left-edge forms are the p=0 instances read with b_0 inserted; the A-block at i=0 matching `0 1^p 0 <A` with p=0 is exactly `0^inf 0 <A`.)

**H** = {A, i=0, b_0=0, b_1=1, m>=3} ∪ {A, b_i=1, i+2<=m-2, b_{i+2}=1} ∪ {D, i+1<=m-2, b_{i+1}=1}.

## 4. Lemmas
**L1 Coverage [Class-A].** Every family config satisfying Inv matches exactly one row above. Proof: A-phase,
trichotomy on n. n>=2: R1/R1' by i. n=0: i>=1 -> R2 (p>=1 by I2, so p-1>=0). i=0: b_1 exists (I1) and >=1 (I2):
b_1>=2 R2'; b_1=1: m=2 X0, m>=3 H1 (b_2>=1 = c+1). n=1: b_{i+1} exists (I3). i+1=m-1 R3''; else b_{i+2}>=1:
>=2 R3; =1 and last R3k; =1 not last H2 (b_{i+3}>=1). D-phase: i=m-1 R5 (i>=1 by I4); else b_{i+1}>=1: >=2 R4,
=1 last R6, =1 not last H3. Decision tree (each leaf = one row; branches at every node are complementary, hence the rows are
pairwise disjoint and exhaustive):
```
phase A (I3: 0<=i<=m-2, so b_{i+1} exists)
 ├ n>=2 ── i>=1: R1 | i=0: R1'
 ├ n=0 ─── i>=1: R2
 │         i=0 ── b_1>=2: R2'
 │                b_1=1 ── m=2: X0 | m>=3: H1
 └ n=1 ─── i+1=m-1: R3''
           i+1<=m-2 (b_{i+2} exists, >=1 by I2)
             ├ b_{i+2}>=2: R3 (i>=1) | R3' (i=0)
             └ b_{i+2}=1 ── i+2=m-1: R3k | i+2<=m-2: H2 (i>=1) | H2' (i=0)
phase D (I4: 1<=i<=m-1, b_i>=2)
 ├ i=m-1: R5
 └ i<=m-2 (b_{i+1}>=1 by I2)
     ├ b_{i+1}>=2: R4
     └ b_{i+1}=1 ── i+1=m-1: R6 | i+1<=m-2: H3
```
n ∈ {0,1,>=2} is exhaustive since n>=0 (I2); b_{i+1}, b_{i+2} ∈ {1,>=2} since >=1 (I2). LHS match: substitute Sec.1 tape (gaps single
except the two `00` around the A-block; 0^inf outside). No case is "uncovered/never arises".
(Sanity, not proof: sec.4 checks all 185,550 Inv configs with m<=6, blocks<=5 against raw TM.)

**L2 Invariants [Class-A].** Each non-halting row maps Inv to Inv: R1 decreases only the A-block (to n>=0),
neighbours grow, i<=m-2 kept (R1' inserts block 1 and shifts i). R2: new A-block p-1>=0, old A-block becomes 1.
R2': b_0=3, D at 1 with b_1>=2. X0: [3,1,1] A at 1. R3/R3': new blocks p+1, j+3 >=1, D-block k>=2, D index>=1.
R3'': A at j+1, last block 1 after it. R3k: A at j, followed by 3,2. R4: next block >=2. R5: A-block L-2>=0, last
block 1. R6: A-block 0 at i+1, last block 2. All blocks created are >=1 except the new A-block; I1 never drops.

**L3 Base [Class-A as a finite symbolic computation; count as the one Class-B if preferred].** From blank tape
(state A) the TM is after exactly 21 steps in the family config [1,1], phase A, i=0, which satisfies Inv
(sec.3: `0^inf <A 0^inf -> 0^inf 0 <A 0 1 0 0 1 0^inf`, 21; also raw; 21 is the first family time).

**L4 Halting of H [Class-A].** Configs in H halt after 14, j+8, a+8 = L+6 steps respectively (H1-H3).

## 5. Reduction Theorem [Class-A | L3]
Let c_0 = ([1,1], A, 0) and c_{s+1} = M(c_s) while c_s ∉ H, with τ_s = 21 + Σ_{r<s} steps(c_r).
Then (i) at TM time τ_s the tape/state/head equal encode(c_s) exactly; (ii) the TM halts iff some c_s ∈ H, and
then it halts (reaches F reading 1) at time τ_s + h(c_s) with h from L4 (bbchallenge count +1).
Proof: L3 gives s=0; L1+L2 give that each c_s is in Inv and matches exactly one rule or H; the rule
(Sec.2) gives (i) for s+1. Every rule takes >=7 TM steps (minimum: R4 at L=2, L+5=7; others: R3/R3' j+7>=8, R2 p+9>=10, R2' 13, R5 2L+10>=14, R1/R1' 2n+13>=17, R3'' >=17, X0 25, R6 >=53, R3k >=111), so if no c_s ∈ H then τ_s→∞ and the TM never
halts; conversely if c_s ∈ H, L4. □
Semantics: c_s is the trajectory of M (macro shortcuts), NOT "the s-th time the TM tape is family-shaped".
Inside one macro step the TM may pass through family-shaped tapes (R3k, R6; e.g. R6 from [1,2,1] D@1 passes
[1,2,1,1] A@2 at step 19 and [1,3,2,1] A@2 at step 36 -- both non-H: R3''-shaped and R1-shaped respectively). H-membership is claimed and decisive only along M's trajectory.

Cross-check (sec.5, not part of the proof): M from c_0 matched the raw TM at all 14,583 macro checkpoints
for t in [21, 3·10^6] TM steps (incl. t=1466 = [10,9,11,0,4,2], A at 3); no H hit; R2', R6, X0 never fired.
Corrections vs Q1: D1 -> H1/X0 (split on m); D2 -> new rule R6; A2-2: the block right after `00100`
(= b_{i+1}=j) has no restriction (j=1 is an ordinary R3/R3''/R3k instance); halt needs b_{i+2}=1 non-last.
Non-halting (that H is never reached) is NOT claimed.
