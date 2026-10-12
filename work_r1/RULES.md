# R1: macro-rule reduction for `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`

Transitions (state, read) -> (write, move, next):
A0→1RB A1→1LA | B0→0RC B1→0RD | C0→1LC C1→1LA | D0→1RE D1→1RD | E0→1LF E1→0LA | F0→HALT F1→0LE.

Tags: [Class-A] = proved for all parameters (by hand and/or symbolic prover in `verify_r1.py`);
[Class-B] = finite simulation; [Class-C] = conjecture / empirical / open.

## 1. Halting criterion (backward analysis) [Class-A]

Halt ⇔ F reads 0. F is entered only by E0 (E reads 0, writes 1, moves L). E is entered only by
D0 (moving R) or F1 (moving L). So every halt is the end of a maximal leftward "E/F sweep":
E reads 0, F reads 1, E reads 0, F reads 1, …, finally F reads 0. The sweep is stopped harmlessly
(no halt) as soon as E reads 1 (E1→0LA). The sweep starts only with D0 at cell q (write 1, E at q+1).
- E at q+1 reads 1 → no halt. Else F at q reads the 1 just written → E at q−1.
- D reached q either by running over 1s (D1) — then cell q−1 is 1, E1, no halt — or directly from
  B1 at q−1 (B writes 0 there), and B is entered only by A0 at q−2 (A writes 1 there).
- So the sweep reads E:q−1=0 (B wrote it) ✓, F:q−2=1 (A wrote it) → E at q−3 = y−1 where y=q−2.

Hence: **halt ⇔ A reads 0 at y with tape[y+1]=1, tape[y+2]=0, tape[y+3]=0, and the cells
y−1, y−2, … read in pairs (E,F) give (0,1)^j (0,0) for some j≥0 before any pair starting with 1.**
In the configuration family below, left of y is `1^h` then blank, so the pair condition holds iff
h=0 (j=0, both blank). In config notation: **halt ⇔ a configuration (0; 1, 0, r3, …) with r3 ≥ 0 is reached**
(r3=0 also halts, since only tape[y+3]=0 is needed; under I of §4, r2=0 forces r3 ≥ 1)
(after 8 more steps F reads 0). This is also checked symbolically (§4, "PROVED HALT").

## 2. Encoding [definition]

Configuration `(h; r1, …, rk)` (h ≥ 0, k ≥ 1, ri ≥ 0, rk ≥ 1) denotes the tape
`0^∞ 1^h [0] 1^r1 0 1^r2 0 … 0 1^rk 0^∞`, head on the bracketed 0 in state A.
(A trailing run of length 0 is dropped: `(h; …, x, 0)` ≡ `(h; …, x)`.)
Every "A reads 0" moment of the run is such a configuration (A is entered only by left moves).

## 3. Macro rules [Class-A] (proved symbolically, all h,x,y ≥ 0; "REST" = `0 1^r… 0^∞`, never read)

Each rule = run from one A0 event to the next; proven for both "REST present" and "blank after".

| rule | from | to | TM steps |
|---|---|---|---|
| R1 | (h; x+1, y+1, REST) | (h+1; x+1, y, REST) | 2x+5 |
| R2 | (h; x+2) | (h+1; x, 0, 1) | 2x+7 |
| R3 | (h; x+2, 0, y+1, REST) | (h+1; x, 0, y+2, REST) | 2x+7 |
| R4 | (h+1; 1, 0, y+1, REST) | (0; h, 0, 1, y+2, REST) | h+8 |
| R5 | (h; 0, 0, y+1, REST) | (0; h+y+4, REST) | h+5 |
| HALT | (0; 1, 0, y+1, REST) | halts | — |

Note R1–R3 all cost 2·r1+3.
Prover: tape = run-length blocks with linear-expression lengths; a whole block `1^e` is crossed in
e steps only when (state,1)→(1, same direction, same state) (valid for e=0 too); any single-cell
read of a block whose length may be 0 aborts ("case split needed"), so all zero cases are explicit.

## 4. Invariant and coverage [Class-A]

Invariant I(h; r1..rk): k ≥ 1, rk ≥ 1, ri ≥ 1 for all i ≥ 3, (r1 ≥ 2 or r2 = 0), and k=1 ⇒ r1 ≥ 2.
(So r1 ≤ 1 ⇒ r2 = 0 ⇒ k ≥ 3 and r3 ≥ 1. Without the last clause, (h;1) would match no row:
(0;1) halts, and (2;1) → (0;1,0,1,1) in 9 steps.)
**Coverage**: a config satisfying I matches exactly one row: r1≥2,k=1→R2; r1≥2,r2≥1→R1;
r1≥2,r2=0→R3; r1=1(r2=0),h≥1→R4; r1=1,h=0→HALT; r1=0(r2=0)→R5. No other shapes exist under I.
**Preservation** (check each row): R1 keeps r1≥2, r2 may become 0 (then k≥3); R2/R3 output
(h+1; r1−2, 0, ≥1, …), which has k≥3, r2=0, r3≥1, so every clause holds even if r1−2 ≤ 1; R4 gives r2=0, r3=1, r4≥2; R5 gives r1≥4 (so k=1 is allowed) and shifts r4.. (all ≥1) to r2...
**Base** [Class-B]: from the blank tape, the run reaches (0; 3) at t=5, which satisfies I.
**Corollary** [Class-A]: the TM halts ⇔ the rule iteration from (0;3) reaches (0; 1, 0, …).

## 5. Abstract (top-level) map [Class-A]

Top configs: h=0 and (k=1 or r2≥1) — the outputs of R5, plus (0;3). Write L=(A, b, c, S),
b=r2, c=r3 (missing entries = 0, S = rest). Domain: under I with h=0, A=r1≥2 (k=1 ⇒ r1≥2;
k≥2 ⇒ r2≥1 ⇒ r1≥2), so A odd ⇒ A≥3 and m is a well-defined integer ≥ 0. A=1 cannot occur. From (0;L): b×R1 gives (b; A, 0, c, S); then:
- A even: ⌊A/2⌋ × R3/R2, then R5 → **L' = (A+b+c+3, S)**.
- A odd: ⌊A/2⌋ × R3/R2, then R4 → (0; m, 0, 1, c+(A+1)/2, S) with **m = b+(A−3)/2**; then repeat:
  m odd, m≥3: ⌊m/2⌋×R3, R4: push (m+3)/2 to the front of the stack and m ← (m−3)/2;
  m = 1: HALT; m even: R3s then R5 → L' = (m+4, stack).
Lemma (halting) [Class-A]: in the chain, m+3 is halved each step and the chain stops at the first
m with m+3 odd; m=1 ⇔ m+3=4. Hence **halt ⇔ some top step has A odd and A+2b+3 a power of 2.**
Lemma (sum) [Class-A]: Σ L' = Σ L + 3 (even case direct; odd case: m+Σstack is preserved by the
chain, start −1, end +4). So Σ L_n = 3n+3 from L_0=(3); tape ones = Σ+h ⇒ span ≈ 3n.
Corollary [Class-A]: a step with k=1 (L=(A), A=3n+3) never halts (A+3 ≡ 0 mod 3).
Step costs (exact, implemented in `G`/`top`): first phase b(2A+3); a block of q R3/R2 from r1=a
costs q(2a+3)−2q(q−1); then R5 (h+5) / R4 (h+7) with the current h. Empirically TM time ≈ 1.35n³,
matching span ∝ t^{1/3}.

## 6. Cross-checks [Class-B]
- Raw TM vs rule-level: every A0 event up to t≈3·10^6 (15264 events): identical configs and times.
- Rule-level vs top-level map: 3000 top steps, identical lists and TM times (t=36,507,403,950).
- Top map: no halt for n < 10^7 top steps (≈1.3·10^21 TM steps); t(200000) = 10,786,696,691,567,311.
  (Informational; not used in any proof.)

## 7. Status of non-halting [Class-C — OPEN]
Non-halting ⇔ for every top step with A odd, A+2b+3 is not a power of 2. Not proved. Observed:
L_n behaves like a binary counter (stack ≈ (…, 3·2^j·const−1)), with odd-chain events in nested
arithmetic families: n ≡ 33 (mod 64) [L=(55+96k, 47+96k), X=8(19+36k)], n ≡ 3 (mod 512),
n ≡ 7 (mod 8192), n ≡ 9 (mod 32768), n ≡ 11 (first at 262155), …; in every observed case
X=A+2b+3 = 2^v·u with odd u > 1. A proof would need an exact inductive description of all
hierarchy levels (it looks like a deterministic counter, not Collatz-random), not attempted here.
