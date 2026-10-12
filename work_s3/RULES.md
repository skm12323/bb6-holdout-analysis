# S3: block-level reduction of `1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB`

This builds on S1 (`D:\math_cc\work_s1\RULES.md`). It uses S1's phase system {K,S,P} and its rules Ka, Kb, Sa, Sb, SH, P1–P5, PH. Importing `verify_s1` inside `verify_s3.py` re-runs every S1 rule proof, and the run aborts if any of them fails.
Notation follows S1: `x^k` is a run, `[A]` marks the head (state A) on that cell, and `..` is the blank half-tape. Step counts are exact TM transitions.

## 1. The block state Σ

**Definition.** For p ≥ 3 and N, m ≥ 0, Σ(p,N,m;W) is the configuration

`.. 1^p 0 1^N [A]1^m W ..`   (phase S: A is on the first cell of `1^m`, or on the first cell of W when m = 0)

W is a stack written top first: W = `0^{g1} 1^{d1} 0^{g2} 1^{d2} … 0^{gk} 1^{dk}` with every g_i ∈ {1,2} and every d_i ≥ 1. Blank tape follows it. When k = 0, the top counts as the virtual entry (2,0). We write s = N+m.

**Σ boundaries.** Σ is not a unique normal form. For example, the tape Σ(3,0,2;∅) one step later can also be read as Σ(3,1,1;∅). The Σ-machine's states are therefore defined to be exactly the configurations at *Σ boundaries*: the base at t = 8, and every moment at which a row of the §2 table produces its result. The result is the tuple written in that row, and the head is where the definition above puts it. Between boundaries the TM is inside one row's S1 rule path.

**Base [Class-B, finite simulation].** From the blank tape, the TM reaches Σ(3,0,0;∅) at t = 8 (S1's Ka(0); `verify_s3` §6.3 also computes this directly).

## 2. The Σ-step theorem [Class-A]

Let the top be (g,d) and the rest W'. Each Σ state goes to the next Σ state, or halts, by exactly one row of the table below. If the stack is empty, then d = 0 and W' = ∅. In that case a pushed (2,d+1) is (2,1), a pushed (1,d+1) is (1,1), and G0/Gs3 give m' = 0.

| rule | condition | result | TM steps | S1 rule path |
|---|---|---|---|---|
| **G1** | g=2, s≥4 | Σ(p+3, s−4, 0; (2,d+1)W') | m+6s−5 | Sa Kb P1 Ka |
| **G2** | g=1, d≥2 | Σ(p+3, s, d−2; W') | m+6s+13 | Sb Ka |
| **SH** | g=1, d=1 | HALT | m+2 | SH |
| G0 | g=2, s=0 | Σ(3, p, d; W') | 6p+8 | Sa Ka |
| Gs3 | g=2, s=3 | Σ(p+5, 0, d; W') | m+16 | Sa Kb P2 |
| Gs1 | g=2, s=1, p≥7 | Σ(6, p−7, 0; (2,1)(1,d+1)W') | m+12p−21 | Sa Kb P1 Ka Sa Kb P1 Ka |
| Gs1_6 | g=2, s=1, p=6 | Σ(8,0,0; (1,d+1)W') | m+54 | Sa Kb P1 Ka Sa Kb P2 |
| PH | g=2, s=1, p=5 | HALT | m+46 | Sa Kb P1 Ka Sa Kb P3 PH |
| Gs1_4 | g=2, s=1, p=4 | Σ(3,3,0; (1,1)(1,d+1)W') | m+72 | Sa Kb P1 Ka Sa Kb P1 Ka Sa Ka |
| Gs1_3 | g=2, s=1, p=3 | Σ(3,3,0; (1,d+1)W') | m+46 | Sa Kb P1 Ka Sa Ka |
| Gs2 | g=2, s=2, p≥5 | Σ(3, p−5, 0; (2,2)(2,d+1)W') | m+6p−5 | Sa Kb P3 P1 Ka |
| Gs2_4 | g=2, s=2, p=4 | Σ(5,0,1; (2,d+1)W') | m+22 | Sa Kb P3 P2 |
| PH | g=2, s=2, p=3 | HALT | m+14 | Sa Kb P3 PH |

**Hand derivation of all 13 rows [Class-A, uses only S1's audited rules].**
Conventions:
- The left block `1^p`, p ≥ 3, always has blank to its left.
- "Ka(n)" uses as its left 0 the 0 just left of the n-run. That is the separator after `1^p` (or after a freshly written `1^3`), or the blank.
- P-rule selection uses S1 §4. z is the nearest 1 left of F, i is the number of 0s between z and F, and the selector is (z−1, z−2, z−3).
- Each P below lists the cells to its left. The 1-block shown there is the witness for the S1 lemma that the all-zero-left branch is vacuous: with Inv (§3) it is `1^q`, q ≥ 3, in every reachable case.

**Step 0: the S-rule is chosen by the top.** By S1, the head sweeps `1^m` (m steps) and then reads the top.
- Gap 1 with d ≥ 2 gives `0 1 1`, so **Sb**.
- Gap 1 with d = 1 gives `0 1 0`, because a gap or blank always follows. That is **SH**.
- Gap 2 or a blank top gives `0 0`, so **Sa**.

These three cases are exhaustive.

- **G2 / SH (g=1).**
  - d=1: SH, m+2 steps.
  - d ≥ 2: Sb gives `1^p 0 1^s 0 [A]0 0 1^{d−2}W'`. Then x−1 = 0, the run ending at x−2 is `1^s`, and its left 0 is the separator. Ka(s) gives `1^{p+3} 0 1^s [A]1^{d−2}W'`, with s = 0 allowed. Steps: m+5+6s+8.
- **g=2 (or blank).** Sa gives K at `1^p 0 1^s [A]0 0 1^d W'`. Split on s:
  - **s=0 (G0).** x−1 = 0 and the run ending at x−2 is `1^p`, with blank to its left. Ka(p) gives `1^3 0 1^p [A]1^d W'` = Σ(3,p,d;W') in 6p+8 steps.
  - **s ≥ 1.** Kb gives `1^p 0 1^{s−1} [F]0 0 1^{d+1}W'` in 5 steps; F's cell was the last 1. Split on s ≥ 4 / 3 / 2 / 1.
    - **s ≥ 4 (G1).** Left of F is `1^{s−1}`, with s−1 ≥ 3, so (1,1) selects P1(0). That gives `1^p 0 1^{s−4} 0 [A]0 0 0 1^{d+1}`. Then Ka(s−4) gives `1^{p+3} 0 1^{s−4} [A]0 0 1^{d+1}W'`. Steps: m+5+6+6(s−4)+8 = m+6s−5.
    - **s=3 (Gs3).** Left of F is `1^p 0 1 1`, so (z−1, z−2) = (1,0) selects P2(0). Cells z−2..f+1 become 1, cell f+2 becomes 0, and the head moves to f+3. That gives `1^{p+5} 0 [A]1^d W'`. Steps: m+5+11.
    - **s=2.** Left of F is `1^p 0 1`, so (0,1,1) selects P3(0). That gives `1^{p−2} [F]0 0 1 1 0 0 1^{d+1}W'` in 6 steps. Next, z is the last 1 of `1^{p−2}`. Split on p:
      - p ≥ 5 (Gs2): `1^{p−2}` has length ≥ 3, so P1(0) applies, then Ka(p−5). That gives `1^3 0 1^{p−5} [A]0 0 1 1 0 0 1^{d+1}` = Σ(3,p−5,0;(2,2)(2,d+1)W'). Steps: m+5+6+6+6(p−5)+8.
      - p=4: `1 1` followed by blank gives (1,0), so P2(0). That gives `1^5 0 [A]1 0 0 1^{d+1}` = Σ(5,0,1;(2,d+1)W'). Steps: m+5+6+11.
      - p=3: `1` followed by blank gives (0,0), so PH. Steps: m+5+6+3.
    - **s=1.** Left of F is `1^p 0`, so i=1. p ≥ 3 gives (1,1), so P1(1): `1^{p−3} 0 [A]0^4 1^{d+1}`. Then Ka(p−3) gives `1^3 0 1^{p−3} [A]0 0 0 1^{d+1}`. This is a non-boundary S configuration with a 3-gap. Then Sa (m=0). Steps so far: m+5+7+6(p−3)+8. Split on p:
      - p=3 (Gs1_3): x−1 = 0, so Ka(3). That gives `1^3 0 1^3 [A]0 1^{d+1}`. Total: m+46.
      - p ≥ 4: Kb gives `1^3 0 1^{p−4} [F]0 0 1 0 1^{d+1}`. Then:
        - p ≥ 7 (Gs1): `1^{p−4}` has length ≥ 3, so P1(0), then Ka(p−7). That gives `1^6 0 1^{p−7} [A]0 0 1 0 1^{d+1}`. Total: m+12p−21.
        - p=6 (Gs1_6): `1 1` after the 0 gives (1,0), so P2(0). That gives `1^8 0 [A]0 1^{d+1}`. Total: m+54.
        - p=5: `1 0 1 1` gives (0,1,1), so P3. Then the lone 1 has two blank cells to its left, so PH. Total: m+46.
        - p=4 (Gs1_4): i=1 and `1^3` give P1(1), then Ka(0), Sa, Ka(3). That gives `1^3 0 1^3 [A]0 1 0 1^{d+1}`. Total: m+72.

The splits are exhaustive: g ∈ {1,2}; d = 1 or d ≥ 2; s = 0, 1, 2, 3, or ≥ 4; and the p ranges are complete for p ≥ 3. A blank top is the d = 0 case of g = 2, because Kb's 1 then lands on blank and gives `1^{0+1}`. S1 §4 makes every selection unique. This gives the whole table. The symbolic engine below is an independent mechanical re-check.

**Mechanical proof of the whole table.** `verify_s3` §1–2 contains a symbolic engine that executes S1's phase system on run-length tapes whose run lengths are linear forms in parameters ≥ 0.
- It mirrors S1's `macro_run` line for line: same case tests, same rewrites, same step counts.
- When a comparison is undetermined (for example whether a run is empty, or whether p ≥ 7), it splits the parameter q into q=0 or q→q+1.
- When it reads the unknown stack tail, it splits it three ways: blank, `0 1^{d+1} W`, or `00 1^{d+1} W`.

The engine starts from 12 shapes that together cover every Σ state with p ≥ 3: N ∈ {0, ≥1} × m ∈ {0, ≥1} × top ∈ {blank, gap 1, gap 2}. It explores every branch until the next Σ form or a halt. All 108 leaves agree exactly with the table (result, stack and step count), and every table row is hit. None of the leaves is TOOLONG or INFLEFT, so the table covers every case.

The engine's correctness is a code-audit matter. As a validation [Class-C], run on concrete tapes it reproduces S1's `macro_run` rule sequence for 6 134 rules.

**Corollary (reduction) [Class-A].** The TM halts ⇔ the Σ-machine started from Σ(3,0,0;∅) reaches SH or PH. The Σ state is a closed language: every result is again a Σ form with gaps in {1,2} and runs ≥ 1.

**Accelerated cycle [Class-A, induction on k].** For k ≤ s/4 and a gap-2 top:

G1^k: Σ(p,N,m;(2,d)W') → Σ(p+3k, s−4k, 0; (2,d+k)W')

The step count is m + 6ks − 12k(k−1) − 5k. After the burst, k = ⌊s/4⌋ and r = s mod 4 selects G0 (r=0), Gs1 (r=1), Gs2 (r=2) or Gs3 (r=3). G1 conserves p+s+d (the ones in the block).

**Span law [Class-A, read off the table].** Let span = p+1+s+Σ(g_i+d_i). 
- On a real top entry: G1, G2 and Gs3 add 0; G0, Gs1, Gs1_6, Gs2 and Gs2_4 add +1; Gs1_3 adds +2 (for example (3,1,0;(2,d)) has span 7+d and (3,3,0;(1,d+1)) has span 9+d); Gs1_4 adds +3.
- On a blank top: G1 and Gs3 add +2; G0, Gs1, Gs1_6 and Gs2 add +3; Gs1_3 adds +4; Gs2_4 adds +3 and Gs1_4 adds +5 (these two are excluded by I1).
- So span never decreases.

## 3. Invariants and when halting can happen [Class-A]

- **Lemma I1.** Inv := (p ∈ P = {3,6} ∪ {8,9,10,…}) and (p,s) ≠ (3,2). Inv holds at the base and every rule preserves it:
  - The possible new p values are p+3, p+5, 3, 6 and 8.
  - p = 3 comes out only of G0 (s' = p+d ≥ 3), Gs2 (s' = p−5 with p ∈ P, p ≥ 5, so s' ∈ {1} ∪ [3,∞)) and Gs1_3 (s' = 3).

  Consequently PH, Gs1_4 and Gs2_4 never fire. `verify_s3` §6.5 also checks this by enumeration.
- **Lemma I2.** Only the top entry is ever read or changed. A (1,1) entry is created only by Gs1, Gs1_6 or Gs1_3 when the top is blank (d = 0), that is, at a state (p, s=1, W=∅). Every real entry has d ≥ 1, so pushing (1,d+1) gives d+1 ≥ 2. Gs1_4 is excluded by I1, and no other rule creates a gap-1 entry. SH fires exactly when a (1,1) entry is on top.

**Theorem H.** Call a state with W = ∅ a Z-state. The TM halts ⇔ the Σ-orbit contains a Z-state (p,1;∅) together with one of the following:
- p ∈ {3,6}. The halt then comes within 2 macro steps.
- p ≥ 8, and the Σ-run from Σ(6, p−7, 0; (2,1)) over a blank bottom eventually empties its stack. Every row's result depends only on (p,N,m) and the top entry (g,d), and buried entries are never read. So the real run, which has (1,1) underneath, coincides with that mirror run until the stack is exposed. At the moment the mirror run empties, the real run sees (1,1) on top and hits SH.

**Lemma N (necessary condition).** Let Z_j have s = 1. Then the previous Z-state has s ∈ {2, 5, 6, 7, 9}. This is a containment (⊆), not an equality.

Proof. Let Z = (p,s;∅) be that previous state. Its excursion starts as follows, with k = ⌊s/4⌋ and r = s mod 4:
- s=0: G0 gives the next Z with s' = p ≥ 3.
- s=1: (1,1) is pushed, so the run either halts or never returns to an empty stack.
- s=2: the bottom is (2,1).
- s=3: Gs3 gives s' = 0.
- s ≥ 4, after G1^k, which leaves the bottom at (2,k):
  - r=0: s' = p'+k ≥ 4.
  - r=3: s' = k, which equals 1 only when s = 7.
  - r=1: the bottom becomes (1,k+1).
  - r=2: the bottom becomes (2,k+1).

When a bottom (2,e) is on top in state s':
- s' ≥ 4: G1^{k'} gives (2,e+k'), then by r' = s' mod 4: r'=0 gives Z with s'' ≥ 4; r'=3 gives s'' = e+k' ≥ 2; r'=1 gives (1,e+k'+1); r'=2 gives (2,e+k'+1).
- s'=0 gives s'' = p'+e ≥ 4.
- s'=3 gives s'' = e.
- s'=1 gives (1,e+1).
- s'=2 gives (2,e+1).

When a bottom (1,e) is on top, it ends the excursion with s'' = s'+e−2.

So s'' = 1 needs one of the following:
- (a) bottom (2,1) with s'=3, and the bottom never grew;
- (b) bottom (1,2) with s'=1;
- (c) bottom (1,3) with s'=0.

Bottoms only grow, so the starting bottom is constrained:
- (a) needs the starting bottom (2,1): s=2.
- (b) needs (1,2): either directly (s=5, k=1), or from (2,1) by s'=1 (s=2).
- (c) needs (1,3): either directly (s=9, k=2); or from (2,2) by s'=1, where (2,2) comes from s=6 or from (2,1) (s=2); or from (2,1) by G1^1 with r'=1 (s=2).

Together with the immediate case s=7, the possible predecessor values are contained in {2,5,6,7,9}. A direct witness exists for 7 (G1 then Gs3). For 2, 5, 6 and 9 these are possible paths only, and no orbit witness is claimed.

In particular, Z with s = 7 leads deterministically to Z' = (p+8, 1) through G1 and then Gs3. So s = 7 at an empty stack is sufficient for reaching an s = 1 Z-state.

## 4. Observations [Class-C]

- The raw TM matches the Σ-machine (tape, head and state) at all 6 071 macro boundaries up to t = 3·10^6.
- Accelerated run of 2·10^6 macro events, t ≈ 9.4·10^16 TM steps, no halt:
  - Rule counts: G1 bursts 876 045, G2 247 900, Gs1 247 903, Gs3 213 209, G0 209 250, Gs2 205 692, Gs1_3 1.
  - Maximum stack depth 26; 216 769 Z-states.
- Z-states with s ≤ 15 are rare and become rarer over time. Their indices are 1–24, then 106, 165, 166, 712, 893, 2886, 2887, 16188, 16189, 45079, 46464 and 47538.
- Dangerous predecessors seen: s=2 four times (each one right after an s=11 Z, by G1², Gs3), s=5 once, s=6 once, s=9 once. s=7 never occurred, and s=1 never occurred.
- s mod 2,3,4,8,12,16 at Z-states shows no forbidden residue. So no simple congruence invariant excludes s ∈ {2,5,6,7,9}.

## 5. Status

Non-halting is **not proved.** The problem is reduced exactly to the arithmetic stack machine in §2, and Theorem H says precisely when it halts: some empty-stack state has s = 1. Lemma N says this needs a near-miss Z-state with s ∈ {2,5,6,7,9} first. Heuristically, near-misses happen at a rate that falls roughly like 1/span, so their expected count grows only logarithmically. A probabilistic heuristic therefore does not rule out halting, and a proof would need an invariant on Z-orbits that is not merely a congruence.
