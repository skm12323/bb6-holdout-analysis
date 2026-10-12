# T1: `1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD`

Table (state: read0 | read1): A: 1RB | 1LE. B: 1LB | 1LC. C: 1RD | 0LE. D: **halt** | 0RB. E: 1RF | 1LA. F: 0RA | 0RD.
Tags: [Class-A] = symbolic proof for all parameter values (checked mechanically by `verify_t1.py`).
[Class-B] = the single finite base simulation. [Class-C] = simulation or empirical evidence only.

## 1. Exact halting criterion (backward analysis) [Class-A]
The only undefined transition is D on 0. D is entered only by C0 (`1RD`) or F1 (`0RD`). So the TM halts at step t+1
iff at step t either C reads 0 and the right neighbour is 0, or F reads 1 and the right neighbour is 0.
At macro level this is exactly rule H below: `1^X E> 0 1 0` --E0--> `1^{X+1} F> 1 0` --F1--> `D> 0` (halt).
Halting happens on the 3rd step; the run is 2 steps followed by the halting step.

## 2. Configuration family
W(X; B) with B = (b1, b2, …, bk) stands for `0^∞ 1^X [E on 0] 1^{b1} 0 1^{b2} 0 … 1^{bk} 0^∞`.
The head is in state E and reads the 0 just right of the leading block 1^X.
Invariant **Inv**: X ≥ 0, k ≥ 1, b1 ≥ 0, and bi ≥ 1 for i ≥ 2.
Write Y = b1, z = b2, w = b3 (z, w = 0 when the block is absent). T = (b4, …).

**Sweep lemmas** [Class-A, proved by induction on n; the context outside the pattern is arbitrary]:
- D-shift: `D> 1^{n+2}` → `1^{n+1} D> 1` in 3n+3 steps.
- EA-sweep: `1^{2n+2} E> 1` → `E> 1^{2n+3}` in 2n+2 steps.
- AE-sweep: `1^{2n+2} A> 1` → `A> 1^{2n+3}` in 2n+2 steps.

## 3. Macro rules: W(X;B) → W(X';B') in c TM steps [Class-A, each one]
| # | condition | result | steps |
|---|---|---|---|
| S | Y=0, k≥2 | (X+1; z, w, T) | 3 |
| Z | Y=0, k=1, X even | (0; 0, X+1, 3) | X+18 |
| Z'| Y=0, k=1, X odd | (0; X+1, 3) | X+15 |
| H | Y=1 | **HALT** (2 steps + the halting step) | — |
| P0| Y=2, X=0 | (0; [0,] z+2, w+3, T), with the leading 0 iff z odd | 4z+27 (z odd) / 4z+24 (z even) |
| Po| Y=2, X odd | (0; X−1, z+4, w, T) | X+7 |
| Pe| Y=2, X even ≥2 | (0; 0, X−1, z+4, w, T) | X+10 |
| Q | Y=3, s=X+z | (0; [0,] s+2, w+3, T), with the leading 0 iff s odd | X+4z+26 (s odd) / X+4z+23 (s even) |
| R2| Y even ≥4 | (X+1; Y−4, z+3, w, T) | 4Y−3 |
| Oo| Y odd ≥5, X odd | (0; X+1, Y−4, z+3, w, T) | X+4Y+1 |
| Oe| Y odd ≥5, X even | (0; 0, X+1, Y−4, z+3, w, T) | X+4Y+4 |

An absent z or w counts as 0 in the formulas. "w+3" when w is absent means a new block 3 is appended. Blocks beyond the ones the rule names are never read.
**Proof method.** We split the parameters into the classes X∈{0, 2x+1, 2x+2}, Y∈{0,1,2,3,4y+4,…,4y+7}, z∈{absent, 2z+1, 2z+2}, and w∈{absent, w+1 followed by an arbitrary tail}. That gives 120 symbolic start configurations. `explore()` runs each one with a run-length symbolic simulator. The simulator takes one TM step only when the head run has provably length ≥ 1. Otherwise it makes an explicit case split v=0 | v→v+1. It uses only the three sweep lemmas. Every leaf (196 in total) must be W-shaped and equal the table entry under that leaf's substitution. Its exact step count must also match, and it must be the first W-config after the start. No leaf is a "never arises" leaf.

**Coverage lemma** [Class-A]: the classes partition every Inv-state, so each state matches exactly one row.
**Inv is preserved** [Class-A]: every new non-leading block is ≥1. Check the table: X+1, z+2, z+3, z+4, w+3, s+2, Y−4 (for Y≥5), and X−1 (only in Pe, where X≥2).
**Base lemma** [Class-B]: from a blank tape in state A, the first W-config occurs at t=12 and is W(0;0,3).
Hence [Class-A, given B] the whole run of the TM is the F-orbit of (0;0,3), where F is the table above. The TM halts iff this orbit reaches Y=1. Times add exactly.

## 4. Derived rules and monotone quantity [Class-A]
- R1-chain (= Oo, then P0, then S): (1; Y, z, T) → (1; Y−2, z+6, T) for Y odd ≥5, in 8Y+16 steps. This is the "a→a−2, b→b+6" behaviour seen in simulation.
- Even checkpoint: C(b; c) := (1; 3, b, c). If b is even, then C(b; c) → C(3b+c+3; ∅), using Q, S, and the R1-chain b/2 times. If b is odd, Q gives (0; b+3, c+3) and the dynamics go into nested R2 chains (division by 4). This involves Pe/Po/Z, which re-feed ⌊·/4⌋ quotients as new blocks. It is a Collatz-like branch.
- Ones on tape = X + Σbi is **non-decreasing**. R2, Oo and Oe leave it unchanged (Δ=0). S, Po and Pe add 1, Q adds 2, P0 adds 3, and Z/Z' add 4. No exact conserved quantity covers all rules.

## 5. Halting condition in arithmetic terms [Class-A]
Read off the table:
- (a) A state with b1=1 is produced only by S applied to (X;0,1,…).
- (b) (X';0,1,…) is produced only from H0=(0;[0]), H1=(0; odd ≥5, …), or H2=(2;2,…).
- (c) Every output with X'=0 has b1 even and B'≠[0], and the base state is (0;0,3). So H0 and H1 are never reached.
- (d) (2;2,…) is produced only from (1;6,…) by R2, or from (1;0,2,…). The second is never an output.
- (e) (1;6,…) is produced only from (0;10,…) by R2, or from (0;0,6,…) by S. The latter comes only from (1;2,2,…) by Po, and (1;2,2,…) comes only from (0;0,2,2,…) by S, which is itself never an output: Pe would need X=3, Oe would need X=1, Z would need X=1 (none even); P0/Q add a leading 0 only when z/s is odd, but z+2=2 or s+2=2 forces 0; other rules produce no leading 0. (Note: (0;0,2,2,5) as a non-output start does halt at t=53 by this route, consistent with the theorem, which concerns the orbit of the base.)

**Theorem.** The TM halts ⇔ the F-orbit of (0;0,3) visits a state (0; 10, …).
The converse direction: (0;10,T) → (1;6,…) → (2;2,…) → (0;0,1,…) → (1;1,…) → halt.
The predecessors of (0;10,…) are: (9;[0]); (0;2,8,…); (11;2,…); (X;3,z,…) with X+z=8; and (9; Y odd ≥5, …).
So non-halting ⇔ the orbit never brings the "small" part of the state into one of these patterns. This is an open Collatz-like reachability question about F. I found no invariant or residue argument that excludes it. **Non-halting is NOT proved.**

## 6. Empirical status [Class-C]
- Raw TM vs F: 2806 consecutive W-transitions agree exactly, including step counts, up to t ≈ 3·10^6.
- Each predecessor claim in §5 was re-checked exhaustively on small states. The criterion was checked on 6090 small orbits.
- The accelerated F-orbit (about 2·10^6 macro events in 20 s, blocks > 10^4300) never visits (0;10,…). States (0; b1≤40, …) with b1>0 occurred only 6 times, all early (b1 ∈ {2,6,12,20,26,34}).
- Checkpoint values b grow by about ×1.5 per checkpoint (e.g. 34→105→203→227→352→1059→…). This is consistent with span ≈ t^0.42.

## 7. Known-cryptid check
The bbchallenge wiki has a page for this machine. It lists it as a BB(6) holdout with no non-halting proof. Its "Polygon" analysis uses a similar block notation A(a,b,c,…), with parity-split rules R1–R14, some of which halt. I could not read the page's exact formulas (only a summary was available), so I did not cross-check them against the table here.
