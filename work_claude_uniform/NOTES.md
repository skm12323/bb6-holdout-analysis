# A uniform landing reduction: EXT(J) from a rank–height condition

Claude, 2026-10-24 (direction A after Parts A/B). **Revised after review** (claude_uniform review: adversary
and two blind auditors; the original Corollary UA1 and the "supersedes" claims are WITHDRAWN, see §5–§6). No global EXT or non-halting claim;
K_clock unchanged. Tags: [A] proved here from the listed imports, [A-imp] accepted import, [B] finite exact
computation (range stated), [C] conjecture.

## 0. Summary

The accepted reductions below T4/T13 rely on a fixed computed window: certify(j,delta) for 5<=j<2·10^7 and
|delta|<=15. They also carry a cascade of conditions: R1 (refuted), R2_c/C7, H5/H5_res, RES. This note gives an
**alternative** reduction, valid for every J, from three uniform ingredients. It does not supersede the accepted
J<T4 reduction: whether its hypothesis RH holds for J<T4 is open (§5).

1. **NT-exact [A].** At an a-chain j, a certified class delta=C/Q (Q=3^r) is an NT gate iff
   v2(3Qk_j+C)=j-2. Therefore no NT gate occurs when 0<|3Qk_j+C|<2^(j-2). If 3Qk_j+C=0 the step is a resonant
   catapult (j'=j-1), whose record does not rise.
2. **Large chains [A+B].** The canonical calendar has no odd-a chain at j=19,20,21. For odd-a chains 22<=j<400,
   the exact margins 2^(j-2)-3k_j-1 are at least 1,048,551 (attained at j=22, k=8); CLOCK covers j>=400.
   Hence at every chain j>=19, a class with 3^r(3k_j+h)<2^(j-2) never gates. This holds in particular for
   rank r<=4 and height h<=2048. The CLOCK bound kappa(j) used earlier is very loose: the real k_j are tiny.
3. **Small chains and gate blocks [B + A].**
   - For j<=18 the full-residue certify scan has exactly 24 exceptions E24, lift-independent (independent
     recomputation; it agrees with work_landing_symbolic).
   - Every walk that arrives below 19 from a chain y>=19 has records <= R_y (block-safe) and no uncertified
     step. This is shown by:
     - [B] for 19<=y<500, every class of 3-adic rank r<=4 and height <= HR[r], both lift bits;
     - [A | NZ] (dominance, Lemma GD) for y>=500, assuming at most three non-descents inside one region
       walk. NZ excludes an exact cancellation at a region gate; it is a pure hypothesis (not proved automatic).

   Hence any NT gate is harmless as long as ranks and heights stay in that range.

**Theorem UA [A+B].** Work inside the least strict-EXT counterexample induction. Let J be arbitrary. Suppose
that along the walk of S(J):
- (RH-a) at every a-chain j>=19, 3^(r_j)(3k_j+h_j)<2^(j-2);
- (RH-b) at every arrival into chains <=18 from a chain y>=19, the class at y has rank r<=4 and height
  <=HR[r]=(2048,2048,760,330,190);
- (RH-c) every region walk (after an arrival, while chains stay <=18) has at most three non-descent a-steps;
- (NZ) for arrivals from y>=500, no region gate has an exactly vanishing small part (hypothesis).

Then S(J) is tie-free. Ranks are counted by non-descents (NT gates and catapults), not only by gates.

**Corollary UA1 — WITHDRAWN in review.** The draft claimed that RH holds automatically for J<T'_341 when all
copied sources are simple, except for walks with >=4 gates. Its proof used the layer bound (Theorem L of
work_claude_shift) far outside the range where it is proved (large phase x>=N0, n+1<T4, the N0 window and the
10^8 gateway certificate), and its rational slack exceeds the G' allowance for x in [512,1500]. Whether RH holds
for J<T4 is open [C]: the obstacle is the height that heavy c shifts bring to chains >=19.

## 1. Imports

- Pair map and Theorem A (rational a-step trichotomy, A1–A3) of work_landing_symbolic (accepted; (A4) refuted).
- Theorem S / Lemma ND of work_claude_shift (accepted): the exact a-step identity, the class rules including
  non-descents with the lift bit, and the precision H.
- HP: two states agreeing mod 2^(j+1) follow the same walk while records stay <= j. This is the meaning of
  certify (work_claude_shifted Prop 3.2, accepted).
- CLOCK τ(n)<=nP(n); τ(n)>=(n-1)/2; the PROOF_EXT_ROOTS type-c bound 1+eps(n)<=4log2 n+4 inside the induction.
- (Theorem L of work_claude_shift is not used; the withdrawn Corollary UA1 relied on it outside its range.)

## 2. NT-exact and the large-chain lemma

**Lemma NT [A].** At chain j with X(j-1) odd a (τ=2k) and certified class delta=C/Q:
- x'=2D+3x/2+6k, so Q x' ≡ 2(3Qk+C) + 3·2^(j-1)uQ (mod 2^(j+1)).
- With p=1+v2(3Qk+C): p<=j-2 gives a descent; p=j-1 is the NT gate; p>=j gives a catapult with j'=j-1.

This is Theorem A of work_landing_symbolic restated. ∎

**Lemma LC [A+B].** Let j>=19 and X(j-1) odd a. If 3^r(3k_j+h)<2^(j-2) for the class (rank r, height h), then
the a-step at j is not an NT gate.
- If 3Qk+C≠0, then |3Qk+C| <= 3^r(3k_j+h) < 2^(j-2), so p<=j-2.
- Otherwise it is a resonant catapult.

[B] margins.json: no odd-a chain at 19,20,21. The odd-a chains 22<=j<400 have min(2^(j-2)-3k_j-1) = 1,048,551
at j=22. CLOCK gives larger margins for 400<=j<2000, and they grow monotonically after that.

For rank <=4 and h<=2048: 81·(3·8+2048) = 167,832 < 2^20, and the margin grows with j.

b/c steps never gate: j'=omega<=j-2-eps and R'<=R-1 (Theorem B / Lemma LOW).

## 3. Small chains

**[B] fullres.py.** For 5<=j<=18 and every residue delta mod 2^(j+1), the exact walk from (2^j, 2^j+delta) is
run, with delta lifted to a positive representative and a second, different lift as a check. It is
certified (no x<=0, ends, all records <= j) except for exactly 24 classes:

| j | exceptional classes |
|---|---|
| 5 | 5, 21, −27, −11 (mod 64) |
| 8 | 58, 186, −198, −70 (mod 512) |
| 12 | 1012, 3060, −3084, −1036 |
| 14 | 4081, 12273, −12303, −4111 |
| 17 | 32702, 32750, 98238, 98286, −98370, −98322, −32834, −32786 |

Chains 6, 9, 13, 15, 18 have no exceptions; 7, 10, 11, 16 are even. The result is lift-independent. By HP, a
real chain at j<=18 whose class mod 2^(j+1) is not in E24 has a remaining walk with records <= its own
record. This holds whatever its rank: classes are just residues.

(ent.py shows the different, stronger notion "the class walk passes an NT gate": 8,196 classes at j=17. These
walks pass a gate whose output is still inside the HP precision, so they are certified. Certify, not NT-free,
is the right notion.)

## 4. Gate blocks entered from chains >= 19

Let y>=19 be the last chain >=19 before the walk arrives at a chain s<=18. If the class at s is not in E24,
§3 applies. Otherwise an NT gate occurs in the region, and its output depends on the low bits of x_s.

**[B] gates.py.** Symbolic affine starts at y on canonical data: x=2^y U with U odd and free, and
Theta=x+theta+2^(y+1)W with W free. A step is FREE if its output valuation is not fixed by the constant part.
Ranges:
- 19<=y<252: every theta of 3-adic rank r<=4 and height <= HR[r], both lift bits;
- 252<=y<500: the same full caps (separate run, gates_checks_252_500.json).

In total 25,254,050 + 26,689,264 = 51,943,314 walks.

Result:
- no FREE step at all, and every walk has max_t(j_t+Gamma_t-Gamma_y) <= y;
- equality occurs only for the resonant catapult theta ≡ -3k_y (including its lift theta=-3k_y+2^y);
- 86,950 walks pass exactly one non-descent a-step (NT gate or catapult); counting only true NT gates
  (output m>=j), no walk passes two.
- The extension 252<=y<500 with the full caps was run separately (gates_checks_252_500.json): 26,689,264
  walks, no FREE step, every walk has max relative record <= y (worst: equality at the resonant catapult
  y=256, theta=-336). 95,152 walks pass one non-descent, and 4 pass two true NT gates. They start at y=411 (two)
  and y=422 (two) with rank-4 classes (e.g. y=411, theta=-2578/81, word 5,17,5,5,1, max relative record 19). So "no double gate" is
  false in general, but these walks are still block-safe and within (RH-c).

(Counts and json: gates_checks.json.)

**Lemma GD (dominance) [A | NZ] (rewritten after review).** Let y>=500, let the class at y have rank r<=4 and
height <=2048, and let the region walk have t<=72 steps and at most three non-descents (so rank <=7 in the
region). Integerize by Q=3^7.
- Small parts. The Theta small part grows only additively: Theta' = Theta+3+3tau, with tau<=12 for region
  chains (canonical table). At the entry, Theta_s = theta+3+3tau_(y-1), so |Theta_t| <= |theta|+3tau_(y-1)+50t.
  For a-steps x' = 2Theta+6k-x/2 with k<=6; for b-steps (all region b crossings have eps=1 and ratio 3/4)
  x' = (3/4)x+lambda with lambda<=40. Hence |Z_t| <= max(|Z_0|, 4max_s|Theta_s|+72) (corrected in re-review),
  where |Z_0| <= 6(y-1)P(y-1)+4096 by CLOCK for every entry type; this is <= 24(y-1)P(y-1), so
  |Q Z_t| <= B := 8·3^7·(2048+3tau_(y-1)+50t+50).
- Remainders. Each a-step loses at most 1 bit of remainder valuation and each b-step at most 2. So after t
  steps the remainder has valuation >= sigma_e-2t, where sigma_e is
  - y-2 for an A entry;
  - y-3 for a B entry;
  - y-2-eps for a C entry, with eps<=4log2 y+3 (PROOF_EXT_ROOTS type c, inside the induction).
- Conclusion. If log2 B < sigma_e-2t-1 and log2 B + 2t + eps + 2 < y, every output valuation is that of the
  small part, provided the small part is nonzero. NZ assumes exactly this nonvanishing at gates. Every record of
  the block is then < R_y. With t=72 and CLOCK tau(n)<=nP(n), both inequalities hold for all y>=216 (checked
  to 20,000; the left sides are O(log y)).
- NZ is a hypothesis. A first draft argued it was automatic for y>=3.5·10^7 via the tau_(y-1) coefficient of
  the gate expression. That argument is WITHDRAWN: for a C entry lambda'_W=3tau+4+lambda_Y, and lambda_Y can
  cancel 3tau (work_r1r2 §4: lambda_Y ≡ -3tau-4 mod 2^omega). For a B entry the copied numerator has no
  "tau part + bounded rest" decomposition. NZ is checked [B] for y<500 (no FREE step).

A gate output m>=19 leaves the region with m+ΔΓ<y, and the next instance starts below y. ∎

## 5. Theorem UA

*Proof of UA.* Chain 0 (parameter J, theta=1) does not gate, since 3k_(J-1)+1 < 2^(J-2). By Lemma LC and (RH-a),
every a-step at a chain >=19 descends or is a resonant catapult, and b/c steps descend. So records decrease (or
stay equal at catapults) and stay < J after step 1. At each arrival below 19:
- class not in E24: §3 gives records <= the arrival record;
- class in E24: §4 gives a block with records <= R_y. This uses [B] for y<500, and Lemma GD with (RH-c) and
  (NZ) for y>=500.

The block either ends or continues at a chain m>=19 with records < R_y; the argument repeats there under (RH).
The walk is finite because each step raises Gamma by at least 1 while all records stay < J. (Catapults keep the
record equal, so "records strictly decrease" is not the right reason.) ∎

**Status of RH.** RH is a rank–height condition on S(J)'s own walk. It holds when every class met at a chain
>=19 has small height and rank, and at most three non-descents occur per region walk. Controlling it for all J
splits into two problems:
1. **Rank growth (trains).** Lemma LC fails at j=22 once 3^r·72 ≳ 2^20, i.e. r>=9. This is (SC)/O1,
   direction B (work_gateway_trains).
2. **Heights at chains >=19 from c shifts.** A c step at chain z can add a shift of size up to ~2log2 z. The
   accepted layer bounds control this only in the large phase. This is the old drift-vs-scale problem, with
   margins 2^(j-2) in place of the window 12. Open [C].

## 6. Relation to the accepted framework (corrected in review)

- This note does **not** supersede the accepted J<T4 reduction (EXT ⟸ H5_res ∧ C7). It gives an alternative
  reduction, EXT(J) ⟸ RH(J), valid for every J inside the induction. Whether RH holds in any range is not
  proved here.
- Under RH, the landing classes (C7), deep c steps (R1) and gateway outputs inside S(J)'s own walk need no
  separate certificate.
  - Gateways in **source** epochs are a different matter: RES there is residual type (iv) of work_claude_shift.
  - Non-simple sources enter only through the heights and ranks they create. They are not removed; they are
    part of what RH assumes.
- What the uniform ingredients do achieve:
  - They replace the window [-12,15] by exact DEPTH margins (>=10^6 at j>=22) at large chains and by the full
    residue scan at small chains.
  - They make every NT gate entered from a chain >=19 block-safe under explicit rank/height bounds.

## 7. Files and reproduction

    python -B work_claude_uniform/margins.py      # Lemma LC margins -> margins.json
    python -B work_claude_uniform/fullres.py      # E24 full-residue scan, two lifts -> fullres_checks.json (~2 s)
    python -B work_claude_uniform/gates.py        # y in [19,252) full caps -> gates_checks.json (~8 min, 25.3M walks)
    python -B work_claude_uniform/gates.py 252 500 500   # y in [252,500) full caps -> gates_checks_252_500.json
    python -B work_claude_uniform/ent.py 18       # NT-reaching classes (stronger notion; diagnostic)
    python -B work_claude_uniform/real_walks.py   # NT gates in actual S(J) words J<=512: none

## 8. Review points

1. Lemma LC: the table of odd-a chains 19..399, and CLOCK beyond.
2. The full-residue scan: positive lifts, lift independence, and the HP transfer for arbitrary rank.
3. gates.py: is the symbolic model (free U, W) faithful to a real chain at y with certified class? Is the
   region-walk length bound 18 right? Do equality cases only come from resonance?
4. Lemma GD's constants (rewritten version): additive Theta growth, |Z_t| <= max(|Z_0|,4max|Theta|+72), the
   loss <=2 per region step, the 72-step bound, the C-entry eps bound and its induction scope, and y>=216.
5. The proof of UA: re-entries after gates, the finiteness argument, and catapults keeping records equal.
6. (Corollary UA1 withdrawn.) Is the open status of RH for J<T4 stated correctly?
7. Is anything in §6 overclaimed relative to the accepted T4 reduction?
8. (After review) Lemma GD's rewritten mechanism (additive Theta growth, 2-bit loss on b-steps, rank <=7),
   the y>=216 threshold; NZ is now a hypothesis.
