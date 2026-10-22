# Source shifts for arbitrary histories, and a layer bound for simple sources below T4

Claude, 2026-10-23 (Part A of the post-c3_drift plan). Revised after review (reviews/claude_shift_review_record.md). No global EXT or non-halting claim;
K_clock unchanged. Tags: [A] proved here from the listed imports, [A-imp] accepted import, [B] finite exact
computation (range stated), [C] conjecture.

## 0. Summary

1. **Theorem S (shift theorem, no DH needed) [A].** The defect automaton of work_claude_ext_next (fire d=1;
   A: d->3-d; B: d->d-1; C(w): d->d+Phi(w)-2) extends to non-descent a-steps by the exact rule
   d -> 3+2k-(d+2^m)/3, which comes from an exact identity of the pair map. With an explicit
   precision count H, the real defect of every chain equals the automaton value mod 2^H. Whenever the
   source chain is certified (H >= omega+1), the landing shift of a c crossing is
   s(n) = -1-lambda_Y(n) = Phi-2 mod 2^(omega+1). This holds for every source history, including
   catapults and nested c letters. Phi depends on the history w together with the catapult data
   (j, k_j, m). It lies in Z[1/3], and its denominator divides 3^(number of non-descent letters).
   The known shifts are special cases:
   eps=3 (A): 0; AA: -1; BA: +1; BBBAA: +4/3 (one catapult at (j,k)=(5,1)).
2. **Lemma ND [A].** A non-descent at chain j with automaton value d=a/3^r needs either resonance
   6k+2d=0 (so j <= 4|d|/3+2), or 2^(j-1) <= 3^r(3(j-1)P(j-1)+2|d|). So for bounded |d| and r,
   non-descents happen only at finitely many explicit small chains.
3. **Theorem L (layer bound) [A+B, using the accepted window and gateway certificates].** Let n be a
   *simple* c crossing (§4): its source chain is produced while all chains are still >= N0, or is the
   output of a bare-tie gateway entered by an A or B letter, and nested C letters are simple
   recursively. If eps(n)>=7 and omega(n)>=N0, then n+1 >= T4. Each history letter costs one
   exponential layer, except the final catapult, which costs nothing. For eps<=15 this needs an
   exhaustive enumeration [B]; for eps>=17 it follows from counting.
4. **Corollary (H5 below T4) [A+B].** For J<T4, the condition H5 of C5_EXTENSION reduces to
   **H5_res**: H5 for c steps with *residual* sources only. A source is residual when its source chain
   comes after an uncertified small-chain segment:
   - (i) a true entry class outside the window (including lift bits);
   - (ii) a rational entry class;
   - (iii) a bare tie entered by a C letter;
   - (iv) a gateway with output >=10^8;

   or (v) when a nested C letter of the large phase copies a residual crossing (recursive; added in
   review).

   **The layer conjecture from the c3_drift review is proved for simple sources, but is probably
   false in general [C].** Case (iii) has a 2-layer shape whose realisation needs only one congruence
   on lambda'_W (§5). The open core below T4 is therefore H5_res together with C7. Both concern the
   class of a rational or uncertified segment at small chains, which is Part B's domain.

## 1. Setting and imports

* Pair map (PROOF_EXT §2; work_r1r2 §1): chain (x,Theta), x=2^j u, u odd, D:=Theta-x (defect).
  - Type a at X(j-1) with tau=2k: x'=2Theta+6k-x/2, Theta'=Theta+3+6k.
  - Type b/c: x'=c'_W u+lambda'_W, Theta'=Theta+3+3tau.
* [A-imp] CLOCK: tau(n) <= nP(n). tau(n) >= (n-1)/2. C1 on the defined prefix, where used.
* [A-imp] Lemma LOW (work_claude_ext_next §2), and the accepted defect automaton and weight grammar
  (PROOF_LOW_DEFICIT).
* [A-imp] Window certificate (work_claude_shifted §4): certify(j,delta) holds for 5<=j<2·10^7 and
  delta in [-12,15], except (5,5) and (5,-11). Transfer to real chains with the class known
  mod 2^(j+1) is Prop 3.2 of work_claude_shifted.
* [A-imp] Gateway certificate (work_r1r2 Theorem 2.4): the classes (10-2^m)/3 and (26-2^m)/3 at chain m
  are certified for 5<=m<10^8.
* G(x) := 2log2(x)+3; T1=2^((N0-3)/2), T_{h+1}=2^((T_h-3)/2). Hence G(J)<T_h ⇔ J<T_{h+1}, and
  G(J)<N0 ⇔ J<T1 (work_deep Lemma 2.4).

## 2. Theorem S

**Exact a-step identity [A].** At a type-a step, eliminating x via x'=2D+3x/2+6k gives

    D' = 3 - D - x/2 = 3 + 2k - (D + x')/3.                           (S0)

This is an identity of rationals; no congruence is involved. It is checked at every a-step of
verify_shift.py.

**Reduced automaton.** Phi_0=d_0 (=1 at a fire). For the letter that takes chain j to chain m:
* A, descent (m <= j-2): Phi' = 3-Phi. Local error valuation >= j-1 (the dropped term is x/2).
* A, non-descent (m >= j-1): Phi' = 3+2k-(Phi+2^m)/3. Local error valuation >= m+1 (the dropped term is
  (x'-2^m)/3, since x'=2^m u', u' odd). In particular Phi' ≡ (9+6k-Phi)/3 + 2^m (mod 2^(m+1)):
  - the bounded part is (9+6k-Phi)/3;
  - the "lift bit" 2^m is recorded, because -1/3 ≡ 1 (mod 2).
* B: Phi'=Phi-1. C(n'): Phi'=Phi+s(n'). Local error valuation >= v2(x(1-c'_W/2^j)), which is >= m+1 by S1
  (as in Lemma LOW); for B the copied defect is exactly 1.
* If s(n') is replaced by its own automaton value Phi(w')-2 (the recursive form), the nested error also
  enters. Its valuation is >= the nested precision H(w'), which is >= m+1 when the nested source chain
  is certified. Then H' = min(H, local, H(w')). (Added in review.)

Precision: H_0 = the precision of the start (infinite for an exact start; the root coefficient
valuation for a real epoch). H' = min(H, local error valuation), and also min with H(w') for a
recursively substituted C letter.

**Theorem S [A].** At every chain, D ≡ Phi (mod 2^H). Hence the reduced value is the real class
mod 2^(j+1) whenever H >= j+1 ("certified").

*Proof.* Let E = D - Phi.
- Descent: E' = -E - x/2.
- Non-descent: E' = -E/3 - (x'-2^m)/3.
- b/c: E' = E + (copy error).

The factor 1/3 is a 2-adic unit, so v2(E') >= min(v2(E), local). Induct. ∎

**When certification fails.** H stays >= j+1 along descents, because chains decrease. It can fail
only after a non-descent climbs to m >= H. Then the real class at m depends on bits that the reduced
data do not carry (provenance). The synthetic tests confirm that H is never violated. [B]
verify_shift.py:
- 20,000 synthetic exact walks plus 4,000 walks forced through non-descents; 39,633 chains, all
  certified and all matching; 387 walks with a non-descent; 3-denominator exponent up to 1.
- Finite-precision starts with forced non-descents (test design from the review): 3,658 certified
  chains, all matching. 283 chains are uncertified, and 273 of them are wrong. So the bound is sharp,
  and certification is really needed.
- The exact identity (S0) and the bound v2(D-Phi) >= H are asserted at every chain.

Scope of the tests: c steps use the real integer s(n'), so the recursive substitution and rational
nested shifts are tested only through the identities, not end to end.

**Corollary S1 (shift formula) [A].** Let n be an odd c crossing whose source chain is chain t of a
real completed epoch (root defect 1, S1 margins), and suppose that chain is certified (H_t >= omega+1).
Then the real defect of the chain is Phi mod 2^(omega+1), where Phi is computed from w and the catapult
data. The landing shift is s(n)=-1-lambda_Y(n)=Phi-2.

The denominator of Phi divides 3^(#non-descents, recursively). It need not equal it:
- a resonant non-descent such as (j,d)=(5,-3) with k=1 gives (9+6+3)/3=6, an integer (this is the
  history BBBBA);
- nested shifts can cancel, e.g. 4/3+20/3=8.

(Corrected in review.)

Examples:
- A: Phi=2, s=0.
- AA: 1, s=-1.
- BA: 3, s=+1.
- BBBAA: d=-2 before the fourth letter; the first A (descent p->5) gives 5. The catapult at (5,1)
  gives (9+6-5)/3 = 10/3 with lift bit 1, so s=+4/3. These match the accepted / reviewed values
  (C3, C5, BBBAA_COPY_CERTIFICATE §2).

## 3. Lemma ND and the catapult bound

**Lemma ND [A].** Let d=a/3^r be the certified value before an A letter at chain j>=3, with k=tau(j-1)/2.
A non-descent needs v2(3^r(6k+2d)) >= j-1. Either 6k+2d=0, which needs k=-d/3>=(j-2)/4, i.e.
j <= 4|d|/3+2; or 2^(j-1) <= |3^r(6k+2d)| <= 3^r(3(j-1)P(j-1)+2|d|). ∎

**Lemma CB (catapult bound) [A].** Suppose:
- a chain y >= N0 is followed by an entry letter to chain 5 whose automaton value is exactly
  d_5 ∈ {5,-11} (the bare ties);
- the next letter is the catapult at X(4) (k=1).

Then the catapult output is m=v2(Z) with Z = 2d_5 + 6 + (3/2)Z_prev, where Z_prev is
- 2d_y+6k_y for an A entry,
- the copied fire numerator for a B entry,
- lambda'_W(y-1) for a C entry.

Z_prev is exact mod 2^sigma:
- A entry: sigma=y-2 (the error E_y+5x_y/4).
- B entry: sigma=y-3 (the term (3/2)c'u).
- C entry: sigma=y-2-eps(y-1).

(Each corrected by 1 in review.) Inside the least strict-EXT counterexample induction,
  PROOF_EXT_ROOTS (type c, from C2-log and EXT(J_W), J_W<y) gives 1+eps(y-1) <= 4log2(y)+4. So
  sigma >= y-4log2(y)-5.
  Outside that induction, a C entry needs sigma >= G(y)+3 as a hypothesis.

Hence 0 < Z <= 9(y-1)P(y-1)+3|d_y|+24 < 2^(sigma-1), with |d_y| small. In Theorem L, n+1<T4 and m>=N0 force at most 3 layers before y, so W_pre <= 8 and
|d_y| <= 5. For the same reason, a true class ≡ 5 or -11 (mod 64) with a different automaton value
(|value| >= 59) would need W_pre >= 116, which is impossible below T4. Z>0 because
the Z_prev term (>= 6(y-2)/4·(3/2)) dominates |2d_5+6| <= 16. So m is certified and m < G(y)+1. The class at m is (10-2^m)/3 or (26-2^m)/3 for either entry
type, by Theorem S with k=1 — the two gateway families of work_r1r2.

## 4. Theorem L (layer bound)

**Phases [A].** Consider the source epoch's walk up to the source chain C, with omega(C)>=N0.

*Large phase (first-event argument, revised in review).* While chains are >=N0, every B/C letter
descends (j'<=j-3). Let the value before an A letter at chain x>=N0 be d=a/3^r. Call it an *event* if
either
- it is a non-descent (resonant or not, Lemma ND), or
- |d| > x^2/8, or
- 3^r > x.

(Threshold for r corrected in re-review.) Before the first event, every A letter at chain x is a
descent with output y <= log2(3^r(3(x-1)P(x-1)+2|d|)) <= log2(x(3xP(x)+x^2/4)) < Gt(x), where
Gt(x) := 3log2(x)+4. B and C outputs are < G(x) <= Gt(x). So every letter before the event
contributes at least one Gt-layer:
- A and B letters contribute 1 each;
- a nested simple C(w') contributes l*(w') >= 1+W(w')/4.

So W_pre <= 4(l_pre-1). Also |d| <= 1+W_pre/2 (with nested shift heights |Phi(w')-2| <= W(w')/2),
and r <= #nested catapults <= W_pre/10, because each catapult lies in a nested crossing of eps>=11.

The event cases:
- A non-descent with |d|<=x^2/8 and 3^r<=x can only be resonant (Lemma ND; for x>=N0,
  x(3xP(x)+x^2/4) < 2^(x-1)). Resonance needs |d|>=3(x-2)/4, so W_pre >= 1.5x-5.
- |d|>x^2/8 needs W_pre >= x^2/4-2.
- 3^r>x needs W_pre >= 10log3(N0) >= 150.

In every case l_pre >= 38, so x < Gt^(38)(n+1) < N0 for n+1<T4, a contradiction. Here
Gt^(6)(y) < N0 for every y < T4: the iterates stay below 1.5T3+4, 1.5T2+6, 1.5T1+6, ~1.5N0, 79, 23.

Without events, the rational slack r·log2(3) per step occurs only after a nested catapult. Then
l* >= 7: the pointer, the nested crossing with eps>=11 and l*>=5, and the following A. See the
thresholds below.

*Entry.* Let the first chain below N0 be s, entered by letter e from chain y>=N0, with class delta.
- Here delta is the true class mod 2^(s+1). A nested last letter can carry a lift bit, e.g. (5,5+32);
  such a class is outside the window and is residual (i).
- If (s,delta) is window-certified (delta an integer in [-12,15], not a bare tie), the rest of the
  epoch has all parameters < s < N0 (window certificate + Prop 3.2, applied to the true class).
  So C lies in the large phase.
- If (s,delta) is a bare tie at s=5 and e is an A or B letter, the next letter is a catapult to m
  (Lemma CB).
  - If m<10^8, the gateway certificate ends the epoch with all later parameters <= m. So C lies in the
    large phase, or C is chain m or a later chain with parameter <= m. The bound below uses only
    omega(C) <= m.
  - If m>=10^8, C may come later (RES).

**Definition.** A c crossing is **simple** if:
1. its source chain C lies in the large phase, or is the catapult output of a bare tie entered by an A
   or B letter; and
2. every nested C letter of the large phase copies a simple crossing (recursively).

Otherwise the crossing is **residual**. Either condition 1 fails, so C comes after one of:
- (i) a true entry class mod 2^(s+1) outside the window [-12,15] (including lift bits; there is no
  weight bound);
- (ii) a non-integer entry class (from a nested shift with a catapult, e.g. +4/3). Its true class
  mod 2^(s+1) is an integer residue. The part of (ii) whose residue lies outside the window belongs to
  (i). The part whose residue lies inside the window (e.g. -19/3 ≡ 15 mod 64 at s=5) is already
  certified by the window case. Listing all non-integer entries as residual only makes H5_res
  stronger, so the corollary is unaffected;
- (iii) a bare tie entered by a C letter;
- (iv) a gateway with output >=10^8 (RES);

or condition 2 fails:
- (v) a nested C letter of the large phase copies a residual crossing (recursive; added in review).

Example of (v): C(w'')A with w'' of type (iii). This has l*=1+2+1=4 together with a G' step, which
leaves omega in {N0, N0+1} unexcluded below T4.

"Bare tie" means the true class (5,5) or (5,-11) mod 2^6. Other classes are window-certified or
residual (i).

**Layer count [A].** For a simple crossing define l* := 1 (pointer) + sum over the large-phase letters
and the final block, where
- A or B: 1;
- C(w'): l*(w');
- the bare-tie entry letter: 1;
- the catapult: 0.

Then omega(C) < G'^(l*)(n+1), each step being G or G'=G+1 (Lemma CB):
- pointer: P <= log2(3tau(rho)+4) < G(n) for n large; for small n, P < N0 already;
- A descent from x: output <= log2(3^r(3(x-1)P(x-1)+2|d|)) < G(x) + r·log2(3) for x >= N0
  (r=0 unless a nested catapult occurred);
- B: <= log2(3tau+4) < G(x);
- C: by induction on the copied simple crossing;
- catapult: m < G(y)+1 with y the entry letter's input.

Because the only catapult is the final one and it is preceded by its entry letter, l* >= 1 + W/4.
Nested C letters satisfy this by induction: l*(w') >= 1+W(w')/4 >= (2+W(w'))/4.

**Thresholds [A].**
- If no catapult occurs and l* >= 4, then omega >= N0 forces G^(4)(n+1) > N0, so n+1 > T4.
- If a catapult occurs and l* >= 5 (with integer values, r=0): assume n+1 < T4. Then
  G'^(4)(n+1) < N0+2 and G'^(5)(n+1) < G(N0+2)+1 < 56 < N0. So omega >= N0 again forces n+1 >= T4.
- If rational values occur (r>0): every step is bounded by Gt (since 3^r<=x), and l* >= 7.
  Gt^(6)(y) < N0 for y < T4 (computed above), so omega >= N0 forces n+1 >= T4.

**Small eps [B, exhaustive].** layers.py enumerates every history of weight W<=22 (eps<=23) in the
accepted grammar, with nested C letters and all rational outcomes. It allows a catapult at any A letter
whenever v2(6k_j+2d) >= j-1 for some odd-a chain j<400 of the canonical calendar. Beyond 400, Lemma ND
excludes non-descents (asserted with CLOCK). It counts 1 + #descents, with catapults 0 and C letters
l*(w'). For simple crossings this over-approximates the catapult patterns and equals l* on the
matching branch, so its minimum is a lower bound. Results (min):
- eps=3: 2; eps=5: 3;
- eps=7: 4, and no catapult is possible for any of the 5 histories (descent-only);
- eps=9: 5, no catapult possible;
- eps=11..23: >=5; catapults first become possible at eps=11 (BBBAA and one other word);
- the minimum grows to 8 at eps=23.

runs.py also shows that no two consecutive catapults are possible for eps<=21.

**Theorem L [A+B].** Simple crossing, eps>=7, omega>=N0 ⟹ n+1 >= T4.
- eps=7: descent-only with l*=4.
- 9<=eps<=15: enumeration gives l*>=5.
- eps>=17: l* >= 1+W/4 >= 5.

The c3_drift-review constructions are simple, with l*=2 (eps=3) and l*=3 (eps=5), and land below T4.

## 5. Corollary for H5 and the residual

For J<T4, a c step at chain t of the initial deep segment reads X(n_t) with n_t+1=j_t<=J<T4. Theorem L
gives omega(n_t)<N0 for every simple source with eps>=7.

**Corollary [A+B].** Inside the least strict-EXT counterexample induction (needed only for Lemma CB with
C entries, which simple crossings do not use at the top level), for J<T4:

    EXT(J) ⟸ H5_res ∧ C7,

where H5_res is H5 restricted to residual sources (i)-(v). The theorem being sharpened is
C5_EXTENSION §4 (H5 ∧ C7 ⟹ EXT for J<T4), which was accepted in the c3_drift review.

**The residual is real, not an artefact [C, heuristic].**

Case (iii), minimal shape: the root letter of the source epoch is a C letter copying a crossing X(P-1)
with omega(P-1)=5 and shift Phi(w')-2=4. That gives d=5 at chain 5. The catapult output is then
m=v2(16+(3/2)lambda'_W(P-1)+...). It is large exactly when lambda'_W(P-1) ≡ -32/3 (mod 2^(m+1)), and
this class has valuation 5, consistent with omega(P-1)=5. Here l*=2: the nested history's layers are
not on the backward path, because the C letter's output is the small chain 5. If such congruences
occur at the heuristic frequency 2^-m, omega>=N0 appears near n ~ T2..T3. So H5 is probably NOT
automatic below T4. The layer conjecture from the c3_drift review holds for simple crossings but very
likely fails for residual ones.

Cases (i), (ii) and (iv) are uncertified small-chain segments with integer-outside-window or rational
classes. Their catapult outputs obey only omega <= G(y)+0.585r+O(1), with r the segment length.

**Consistency check [B]** (not independent evidence: it essentially re-derives the window
certificate's exceptions). free_search.py starts at every small chain j0<400 with |d0|<=12 and a fully
tunable numerator 2^j0 U. It finds a precision-exhausting ("free") step only at the start (5,5) or
(5,-11) itself. This matches the window certificate's two exceptions and Lemma CB's entry condition.

## 6. What this means for the global problem

* Theorem S is uniform in J. It reduces the c-step part of drift control to the single automaton
  {3-d, d-1, (9+6k_j-d)/3 (+lift), d+s}, whose shifts are themselves outputs of the same automaton on
  earlier epochs.
  - Rational phases arise exactly from non-descents (catapults).
  - For bounded |d| and r, non-descents occur only at the finitely many chains allowed by Lemma ND,
    or at bare-tie-type entries.
* Parameter caps (CAL-C, R1, H3) are false. Theorem L shows that, for simple sources, the
  large-c-parameter mechanism costs exponential layers: one per letter, zero per catapult. A
  residual source can skip layers: a C letter that enters a bare tie hides its nested layers, and an
  uncertified small segment can amplify. So no purely layer-based argument closes H5 globally.
* The open core is now concentrated in one kind of object: **a rational or otherwise uncertified class
  at a small chain** (below N0). It appears in two places:
  1. C7 / R2_c: the landing class of a c step;
  2. the residual sources of H5_res (i)-(v).

  Part B (work_landing_symbolic) addresses exactly this. The two parts meet in a symbolic certificate
  for rational classes at small chains, together with the source shifts produced by Theorem S.

## 7. Files and reproduction

    python -B work_claude_shift/verify_shift.py 20000    # Theorem S checks -> shift_checks.json (~1 s)
    python -B work_claude_shift/layers.py 22             # enumeration eps<=23 -> layers_checks.json (~10 min)
    python -B work_claude_shift/runs.py 20               # longest catapult run, eps=21
    python -B work_claude_shift/free_search.py           # tunable-start precision search -> free_search.json

forced.py builds walks with prescribed outputs by solving affine congruences in U. All starts are
synthetic unless stated; canonical data come from the accepted Calendar(512).

## 8. Review points

1. Precision bookkeeping in Theorem S, especially the b/c copy error and the lift bit.
2. Lemma CB's size bound and certification: Z>0 and Z<2^(sigma-1) for y>=N0. For C entries, check
   the use of the PROOF_EXT_ROOTS type-c bound (Gamma_1 <= 4log2 J+4) and its induction scope.
3. The structure argument in §4: the first-event contradiction, window/gateway transfer inside source
   epochs (not only S(J)), and the position of C after a gateway. Is the list of residual cases
   (i)-(v) complete?
4. Whether layers.py's over-approximation is sound: rational d, nested C outcomes, and the j<400 cutoff
   with the CLOCK assertion.
5. The G' slack computation, and the pointer layer P < G(n).
6. The §5 heuristic for case (iii): is the 2-layer shape consistent with every accepted constraint
   (weight grammar for Phi(w')=6, omega(P-1)=5, S1)?
