# S1: symbolic macro-rule reduction of `1RB1RA_1LC0RC_---0LD_0LE0RF_1RE0RA_0LF1LB`

Table: A0→1RB A1→1RA | B0→1LC B1→0RC | C0→HALT C1→0LD | D0→0LE D1→0RF | E0→1RE E1→0RA | F0→0LF F1→1LB.
Notation: `[S]b` = head in state S on a cell containing b; words are read left→right; `x^p` = run of p≥0 copies of x;
`?` = a cell that is never read. All step counts are exact TM transitions. Proof engine: `verify_s1.py`.

## 1. Halting criterion [Class-A]
C0 is the only undefined entry. C is entered only from B (B0→1LC, B1→0RC); B is entered only from A0 (1RB) and F1 (1LB).
- A0 at x → B at x+1. If x+1=0: B writes 1 and moves left onto x, which A just made 1 → C1, safe. If x+1=1: B writes 0, moves right, C reads x+2.
- F1 at x → B at x−1. If x−1=1: B writes 0, moves right onto x (=1) → safe. If x−1=0: B writes 1, moves left, C reads x−2.

**Halt ⇔ the machine reaches `[A]0 1 0` or `0 0 [F]1`** (it then halts 2 transitions later). The verifier checks this table logic and exhaustively checks every 7-cell window in every state.

## 2. Phases (canonical configurations)
- **K**: `[A]0 0` (A on x, x and x+1 are 0). Every tape cell is arbitrary otherwise.
- **S**: A on cell x, moving right (the sweep).
- **P**: `[F]0 0 1` (F on w, w=w+1=0, w+2=1).

Base [Class-A]: the start configuration (blank tape, A) is K.

## 3. Macro rules [Class-A, proved symbolically for all p≥0]
The prover crosses a run in a single event only if the transition keeps the state and the direction (runs of length 0 included). It fails if the head leaves the window or reads `?`, so each rule holds whatever lies outside the window. Where the head would end on a run that could be empty, I split the cases explicitly (P5).

| rule | before | after | steps |
|---|---|---|---|
| α (lemma) | `1 0 [A]0 0` | `0 [A]0 0 1` | 5 |
| β (lemma) | `0 0 [A]0 0 ?` | `1 1 1 0 [A]?` | 8 |
| **Ka(n)** | `0 1^n 0 [A]0 0 ?` | `1 1 1 0 1^n [A]?` (→S) | 6n+8 |
| **Kb** | `1 [A]0 0` | `[F]0 0 1` (→P) | 5 |
| **Sa(m)** | `[A]1^m 0 0` | `1^m [A]0 0` (→K) | m |
| **Sb(m)** | `[A]1^m 0 1 1` | `1^m 0 [A]0 0` (→K) | m+5 |
| **SH(m)** | `[A]1^m 0 1 0` | HALT (in C0 after m+2 steps) | m+2 |
| **P1(i)** | `1 1 1 0^i [F]0 0 1` | `0 [A]0 0 0^i 0 0 1` (→K) | i+6 |
| **P2(i)** | `0 1 1 0^i [F]0 0 1 ?` | `1 1 1 1^i 1 1 0 [A]?` (→S) | 2i+11 |
| **PH(i)** | `0 0 1 0^i [F]0 0 1` | HALT (in C0 after i+3 steps) | i+3 |
| **P3(i)** | `1 1 0 1 0^i [F]0 0 1` | `[F]0 0 1 1 0^i 0 0 1` (→P) | i+6 |
| **P4(i)** | `1 0 1 0 1 0^i [F]0 0 1` | `0 [A]0 0 1 1 0^i 0 0 1` (→K) | i+6 |
| **P5(0)** | `0 0 1 0 1 [F]0 0 1` | `1 1 1 0 1 [A]0 0 1` (→K) | 10 |
| **P5(k+1)** | `0 0 1 0 1 0 0^k [F]0 0 1` | `1 1 1 0 1 [A]0 0^k 0 0 1` (→K) | k+11 |

Proof of Ka(n): the α lemma is window-closed, so `1^k 1 0[A]00 W → 1^k 0[A]00 1 W` for every k and W. By induction, `1^n 0[A]00 → 0[A]00 1^n` takes 5n steps. Two zeros now sit to the left of A, so β applies (8 steps), and A then crosses `1^n` (n steps). The verifier also checks concrete cases n=0..40.

## 4. Coverage lemma [Class-A]
- K: if x−1=1, Kb applies. If x−1=0, let n≥0 be the length of the maximal 1-run that ends at x−2. The cell to its left is 0 (the tape is finite), so Ka(n) applies. These cases are exclusive and exhaustive.
- S: let m≥0 be the length of the 1-run starting at the head. The next two cells after it, (b,c), select Sa (b=0), Sb (1,1) or SH (1,0).
- P: **Lemma (vacuous branch).** In every P-phase produced by the S3 Σ-table rows, at least one 1 lies to the left of w (witnesses: S3 §2 "Hand derivation"; holds unconditionally, incl. the I1-excluded p=4/5 rows, where the witness is `1 1` or a lone `1`). Remark: under I1 the left block is in fact `1^q` with q ≥ 3. So the all-zero-left branch never occurs. Let z be the nearest 1 left of w, so i = w−z−1 ≥ 0. The cells (z−1, z−2, z−3, z−4) select exactly one case: (1,1,·,·)→P1, (1,0,·,·)→P2, (0,0,·,·)→PH, (0,1,1,·)→P3, (0,1,0,1)→P4, (0,1,0,0)→P5.

So every reachable configuration matches exactly one rule, a halting pattern, or the non-halting left run. The P case uses the vacuity lemma above, a reachability fact established by the S3 hand derivation; no other "never arises" assumption is used.

## 5. Abstract map and cross-check
The abstract machine is the phase system {K, S, P} on a concrete tape, and it uses only the rules above (`macro_run`). The verifier compares it with the raw TM at every macro boundary (same tape, head, state and step count). [Class-A for the finite range checked: 24 264 boundaries, t ≤ 3·10^6.]

**Reduction [Class-A]:** the TM halts ⇔ the phase system started at K on a blank tape reaches an SH or PH instance.

## 6. Observations [Class-C]
Rule usage up to 10^10 steps: Ka 1 378 498, Sa 1 378 422, Kb 1 377 441, P1 1 376 407, Sb 1 109, P2 1 034, P3 941. P4, P5, SH and PH are never used, and the machine does not halt.

Almost all of the time is the 4-cycle Ka→Sa→Kb→P1. The rare branches (Sb, P2, P3) are the near-misses:
- Sb: the sweep meets `0 1 1`; SH would need `0 1 0`.
- P3: F meets an isolated 1 with a single 0 on its left; PH needs two 0s there.

Gap lengths seen in snapshots are 1, 2, 3 and 5. The patterns `010` and `00100` do appear on the tape. So no invariant of the form "pattern X is absent from the tape" can exclude PH or SH; any such invariant has to be relative to the head phase.

## 7. Status
Non-halting is **not proved**. The open question is exact: does the phase system in §3 ever present `[A]1^m 0 1 0` in phase S, or `0 0 1 0^i [F]0 0 1` in phase P? The reduction does not collapse to an arithmetic (Collatz-type) map. The configuration is an unbounded word whose blocks are rewritten by the 4-cycle plus rare branches. A proof would need a head-relative regular invariant (CTL-style) or a further acceleration of the Ka-Sa-Kb-P1 cycle into a block-level counter. Neither was achieved here.
