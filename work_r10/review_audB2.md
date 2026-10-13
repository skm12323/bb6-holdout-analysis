# BLIND AUDITOR-1 review of work_r10/agentB2_report.md ("EX": exit class lemma)

Independent re-implementation from scratch (this file's author read only PROOF_G6.md sect.0,
verify_g6.py's phi(), fast_walker.py and scratch/agentB_run7.py BEFORE coding; agentB2_report.md
was read only after all own results below were fixed). Auditor scripts (all in work_r10/):
`revB2_phi.py` (own Phi_m tracer), `revB2_task1.py` (census + all invariant checks),
`revB2_shapes.py`, `revB2_rule.py` (structure), `revB2_tie.py` (tie thresholds),
`revB2_walk.py` (exact walker vs fast_walker), `revB2_extra.py` (new-shape probe + affine
cross-checks). Data: `revB2_census_5_1500.json`, `revB2_census_1501_3000.json` (~1.1 MB total;
footprint well under 30 MB).

## Task 1 — Phi_m tracer, D-fire affine form, j_D formula, j_D <= m-2. **PASS**

m = 5..1500 (1496 runs; every run reached a canonical re-entry, all canonical-form and
no-halt asserts held):
- 453 D-fires (b = D_h). In every one, the D-fire is exactly the chain at a CLEAN crossing
  (queue front = D_h, c = T_2), s_cross even, and
  **x_D = (39/2)P + 9k_h + 6*K_exit + 8 exactly** (integer check 2*x_D), with
  **K_exit = s_cross/2** — 0 violations. (Own derivation, matching their Lemma 1: at a clean
  crossing the sum lemma gives A = 2^{m-1}u + 3s+1.)
- **K_exit = K + delta**, K = universal k at the last pure sub-fire rho* (x_{rho*} =
  3*2^{rho*}u + 6K+4 verified integral); delta distribution {1:287, 2:124, 3:36, 4:4, 5:1}
  (m<=1500; up to 6 by m<=3000, up to 8 at larger m, see Task 2).
- **j_D = 1 + v2(3K_exit+1)** whenever < m-1: applicable in ALL cases (no numerical tie ever
  occurs: 3K_exit+1 < 2^{m-2} everywhere, max log2(3Kex+1)-(m-2) = 0 at m=5, i.e. 4 < 8);
  0 mismatches. **j_D <= m-2 everywhere**; equality only at m=5 (j_D = 3). Max j_D = 11
  (at m=770). Max K_exit/(m-1) = 0.4459 < 0.4465.
- m = 1501..3000 re-run: 0 violations again; 453 more D-fires; max j_D = 10; delta up to 6.

## Task 2 — shape census and enumeration completeness. **PASS on facts; see caveat C1**

Census (own; "pure" = last sub-fire with b and c both run entries, g = m-2-rho*,
j_last = its class; matches the report's convention):
- m = 5..1500: 41 distinct (g, j_last) exit combos with g in 1..6, j_last in {1..10}, plus
  the no-sub-fire case (m=5,6). m = 1501..3000 adds the new spike class j_last = 12
  (g in 1..6; D-shape first at m = 1544).
- **Structural rule found and verified: a D-fire occurs iff g = dp(j_last) - 1**
  (dp(j) = re-entry gap of class j from the transition table): 0 violations / 2994 runs.
  This explains the 12-shape table exactly: each D-shape is (dp(jl)-1, jl), one per spike
  class jl that has occurred.
- **What bounds g:** the next universal sub-fire after rho* sits at rho*+dp(j_last); if
  that were <= m-3 it would be another pure sub-fire, contradiction; so g <= dp(j_last).
  dp(j) in [2,6] for every class computed (j <= 18 here) => g <= 6, D-shapes g <= 5.
  **What bounds j_last:** nothing a priori — j_last = 1+v2(3K+2) <= 1+log2(3K+2) is
  unbounded (log-growth). New spike classes DO keep appearing (class 9 at m=966, 10 at
  m=391, 12 at m=1540; the real walk to i=1e5 contains classes 13,14,15,16,18).
- **New shapes at m > 3000 (the completeness test):** for each new class jl at its first
  universal position rho (from the walk), Phi_{rho+dp(jl)+1} realizes D-shape
  (dp(jl)-1, jl): verified concretely
  (4,14) at m=6136, (3,13) at m=15315, (3,16) at m=24499, (4,15) at m=61230, (2,18) at
  m=97959 — D-fire present, x_D affine form OK, j_D = 1+v2(3Kex+1), j_D in {1,3},
  j_D <= m-2 in all five. So the family of D-fire shapes is INFINITE in principle
  (one per occurring spike class); the "12 shapes" is a census for m <= 3000, not an
  enumeration. All claims still held on every new shape (they are shape-independent —
  see verdict).

## Task 3 — the tie shape. **PASS**

- Identified: the single shape with orbit-dependent (non-constant) j_D is **(g, j_last) =
  (1, 2)**, delta = 1 — exactly work_g6 Prop 3's case and agentB2's "(1,2,1)". 250
  occurrences for m <= 3000; **delta = 1 and j_D = 1+v2(3K+4) in all of them** (K =
  k(rho*)); the other 11 shapes have j_D constant in {1, 2, 4} (3 at J=5).
- Size bound (own recomputation; j_D = 1+v2(3Kex+1) <= 1+log2(3Kex+1); sufficient
  conditions 3Kex+1 < 2^{m-2} => j_D <= m-2, < 2^{m-3} => j_D <= m-3):
  - k <= 0.4465*rho applied at the crossing position (Kex <= 0.4465(m-1)):
    j_D <= m-2 for ALL m >= 5; j_D <= m-3 for m >= 6.
  - task's k(rho*) form, Kex <= 0.4465*rho* + dmax with measured dmax = 6:
    j_D <= m-2 for m >= 7 (m=5,6 by direct check — they pass), j_D <= m-3 for m >= 8.
  - under k <= rho*^2 (+dmax): j_D <= m-2 for m >= 10; j_D <= m-3 for m >= 11..12.
  agentB2's own thresholds (delta <= 2J umbrella: J >= 9 linear / J >= 12 quadratic) also
  verify numerically under their stated slack; their exhaustive base "D-fire m's <= 11 are
  {5,8}" matches my census exactly (and Phi_17 = shape (2,1,1), j_D = 1, margin 16 —
  confirmed by direct trace).

## Task 4 — second fire and mixed fires. **PASS**

m = 5..3000 (per-m checks in the census runs):
- Second fires (b = the 'd' pushed by the D-fire): 47 total; all j_seam <= m-2
  (0 violations); j_seam in {1: 42, 4: 5}; the j_seam = 4 cases are exactly the
  j_D = 8 variants at m = 481, 1055, 1628, 2202, 2777 (their "first at m=481" confirmed);
  min margin m - j_seam = 13. Their affine form verified: 47/47 satisfy
  4*x_seam = 153P + 30k_h + 36Kex + 24K' + 48 with K' in {1,2} (K'=1: 42, K'=2: 5).
- Mixed fires (c = D_h): 954 total; all j <= m-2 (0 violations); max j = 12;
  min margin 5. For b = E_{m-2} (906 of them): 4*x = 27P + 18k_h + 24Kmix + 28 with
  Kmix = s_cross/2 in all, and j_mix = v2(6Kmix+4) whenever < m-2 — their V-A identities
  confirmed. All other 'd'-b fires: max j = 4; M-fires: max j = 4 (outside claim scope).

## Task 5 — real-walk cross-check. **PASS**

Own exact big-int walker of the formal map F vs audited fast_walker.py to i = 1e5:
level-fire streams (rho, k, j) IDENTICAL (30286 fires; my I(rho)/margin asserts all held).
1586 chains with b a 'D'-tagged entry: **0 violations of j <= J_enclosing - 2**;
margins J_enc-2-j: 0 x 1394 (J=5, j=3), 5 x 175 (J=8), 7 x 3, 9 x 11, 11 x 3;
enclosing parameters J in {5, 8, 12, 14} — matching their V-C (they ran to 2e5: 3171
D-fires, min margin 2 at (J,j)=(5,3), J-set {5,8,12,14}; my 1e5 numbers are exactly the
prefix: 1586 D-fires, min margin 2). Measured conservation constant max k/rho = 0.4464
< 0.4465.

## Task 6 — comparison with agentB2_report.md

**Agreements (all exact):** exit accounting m=5..3000 D/mixed/even = 906/954/1136 (=2996);
the 12-row shape table — every row's first-m, count, delta, j_D constant and margin column
match my census digit for digit ((no-sub J=5): m=5, j_D=3; (2,1,1): m=8, 325, j_D=1;
(3,4,2): m=12, 84, 1; (1,2,1): m=14, 250, 1+v2(3K+4); (4,3,2): m=22, 163, 1; (4,6,3):
m=32, 21, 4; (3,5,3): m=68, 41, 4; (5,8,4): m=106, 6, 1; (3,7,3): m=248, 10, 4;
(4,10,5): m=394, 2, 2; (1,9,4): m=966, 2, 1; (5,12,6): m=1544, 1, 1); the h-vs-v class
arithmetic (j_D = 1+v2(3K+3delta+1), 3K+2 = 2^{jl-1}*odd, h = v2(3delta-1)) reproduces all
my constants and singles out (1,2,1) as the only h=v case; Lemma 1 (clean-crossing
identity), Lemma 2 (class reduction), Lemma 3 (Kex = K+delta) all reproduced; second-fire
x_seam/j_seam formulas and mixed x_mix/j_mix formulas verified above; Phi_17 claim
confirmed; tie thresholds re-derived.

**Issues found:**
1. **C1 (framing, substantive for the proof strategy): the "12 exit shapes" enumeration is
   a census over m <= 3000, not an exhaustive list.** Five further D-fire shapes occur and
   were verified by me ((4,14) m=6136, (3,13) m=15315, (3,16) m=24499, (4,15) m=61230,
   (2,18) m=97959); structurally a new shape (dp(jl)-1, jl, delta) arises for every new
   spike class jl, and jl is unbounded. The report's header "PROVED ... 12 shapes" and
   sect.5 "(i) the map J -> shape (which of the 12 scripts occurs)" overstate closure.
   Mitigation (why the lemma itself survives): Lemmas 1-2 are shape-free — j_D <= J-2 is
   exactly v2(3Kex+1) <= J-3 — and the size argument used for the tie shape needs no shape
   information, so it closes every shape at once given the k-growth input (my Task 3
   thresholds). All five new shapes pass every check. A hypothetical NEW tie (h = v) among
   future shapes would not be covered by the per-shape table, only by that uniform size
   argument.
2. **C2 (trivial miscount):** sect.3 "K'=1 ... j_seam = 1 constant (44/47 cases)" — the
   correct split is 42/47 (K'=2 occurs 5 times: m = 481, 1055, 1628, 2202, 2777), as
   verified by direct K'-fit of all 47 second fires.
3. **C3 (nit):** sect.2 "structurally, rho* = J-3 <= 7" should read <= 8 (J <= 11);
   vacuous in effect because 8 is not a universal fire position (positions ..., 4, 7, 11,
   ...), so the conclusion "no tie shape for J < 12" stands.

## Verdict

Every audited numerical claim and formula — x_D = (39/2)P+9k_h+6Kex+8, j_D =
1+v2(3Kex+1), j_D <= m-2 on all 906+5 D-fires (m = 5..3000 plus 5 out-of-table shapes up
to m ~ 9.8e4), second-fire and mixed-fire forms and bounds, walk cross-check to i = 1e5 —
reproduced exactly, 0 counterexamples. **all correct**, with caveats: (C1) the 12-shape
enumeration is an m <= 3000 census, not a closure — new D-fire shapes provably occur at
larger m (5 exhibited and verified compliant); the "PROVED" status of the exit class lemma
therefore rests on the shape-free Lemmas 1-2 plus a size input (k <= 0.4465*rho, itself
[Class-B] to 4e5), not on the 12-row table; (C2) 44/47 should read 42/47; (C3) rho* <= 7
should read <= 8.
