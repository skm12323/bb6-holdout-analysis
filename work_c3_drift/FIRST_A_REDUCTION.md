# Exact first-a reduction for small common shifts

**Review status (2026-10-23):** reviewed via the work_landing_symbolic three-way review (reviews/landing_symbolic_review_record.md, group 2). Status: §1–§3 accepted as an [A] conditional reduction (integer |eta|<=8, real chain and real tail); L49/L52 should argue via lambda_out=3s_A+3−x_A/2>=1/2 (4 of 84 first a-steps have lambda_in<0, min margin of x_A<=6s_A+5 is 157). §5–§6 [B]. §4 [C], depending on SHIFT_TRANSPORT and Lambda<=4 (J<T4).

2026-10-20. **UNREVIEWED.** Generalizes the eta=-1 first-a argument
in work_claude_ext_next section 6 to the shift range needed by the
current Lambda<=4 drift argument. Unlike the later H-family
normalization, this reduction does not require DH or DH_out.
It does not certify the residual branch or prove global EXT.

## 1. Input: a complete real tail with a strict physical margin

Let C be a reached real chain with scalar state (x,Theta) and physical
coefficient precision sigma. Suppose its real tail is defined, ends,
and has j_t+G_t<sigma throughout, as given by real S1 for a completed
epoch. Consider the shifted state (x,Theta+eta), at the SAME precision
sigma, where

    eta in {-8,-7,...,7,8}.

This includes theta-2 for incoming theta in [-2,4]; it applies to the
uniform ancestry transport of SHIFT_TRANSPORT.md. No source-deficit
bound is needed in this local lemma. A future proof applying it must
still justify both the incoming theta bound and the real-tail input.

Zero shift is already safe. At every b/c return the numerator map
does not read Theta and the clock increment is the same. Therefore,
until the FIRST odd a return, the shifted and real walks have exactly
the same x, parameters, types, and losses, and their phases differ by
exactly eta. No precision approximation is involved in this stretch.
If the real tail stops before any odd a return, the shifted tail stops
with it and is safe. Otherwise let the first a step have input
(x_A,Theta_A), parameter m, prior loss G, and tau(m-1)=2k.

Its two outputs are exactly

    real:    y=2*Theta_A+6k-x_A/2,  T=Theta_A+6k+3,
    shifted: y_eta=y+2*eta,         T_eta=T+eta.          (EXACT)

The remaining precision after this step is sigma-G-1. Thus shifted
safety is equivalent to termination of this explicit residual with
all its relative records <sigma-G-1. The prior stretch is already
safe. This equivalence retains a ceiling failure at the very first
residual state; it never presupposes a descent or crosses a failed tie.

## 2. Positivity and all noncolliding outputs

Positivity is automatic for this range; the previous version's
nonpositive-output exception is unnecessary. An odd a call has m>=5
(X(0..3) are even), hence its real numerator x_A>=32. If its time is
s_A, nonnegative lambda mass gives x_A<=6*s_A+5, so s_A>=5.
The a return occurs at s'=s_A+1+tau(m-1)>=8, because an odd a call
has tau(m-1)>=2. At that a-output the next chain numerator is
y=3*s'+4+lambda_Y>=28. Therefore y+2*eta>=12>0 for |eta|<=8.
This uses only real-chain mass and the canonical small base.

For eta!=0 write h=v2(2*eta), so 1<=h<=4. Let q=v2(y).
If q!=h, exact valuation arithmetic gives

    v2(y_eta)=min(q,h)<=4.

All parameters <=4 have even returns in the canonical base, so the
shifted tail ends at this next chain. Its record is at most the real
output's record q+G+1<sigma, hence the strict margin is preserved.

This argument does not replace the original physical ceiling by m-1.
It also makes no assumption about how large m is or whether the a
step satisfies DH. The only remaining case is equal valuation below.

## 3. The remaining branch is after a real terminal a return

If q=h, then q<=4, so the REAL tail terminates at this first a output.
Its shifted output may have much larger valuation because y and
2*eta cancel at their common lowest bit. The exact remaining task is

    (y+2*eta, T+eta), ceiling sigma-G-1,
    with y the TERMINAL output of the first a return in a real tail,
    v2(y)=v2(2*eta)<=4.                            (TERMINAL-COLLISION)

This is the sole remaining branch. The provenance
condition is stronger than merely asking about arbitrary G_delta or
H_delta states: y,T belong to a particular reached real terminal
chain, and the original physical precision is retained exactly.

The collision cases by shift are:

| eta | required real terminal q |
| --- | --- |
| odd eta in [-8,8] | 1 |
| eta=+-2, +-6 | 2 |
| eta=+-4 | 3 |
| eta=+-8 | 4 |

There is no justification here for transferring the real trajectory
past that point: it has already ended. In particular, real S1 says
nothing about the subsequent shifted suffix. This is the genuine
remaining obligation, not a missing technicality in the shadowing.

## 4. Relation to the current proof route

SHIFT_TRANSPORT reduces later A-initial c sources to earlier real
chains without changing eta. Whenever the incoming drift is [-2,4],
the terminal earlier-chain obligation can now be analyzed by EXACT.
The only positive-output obstruction occurs after a real tail has
ended at its first a return of parameter at most 4. This statement
also applies directly to shifted real fire references.

For eta=-1 it recovers the accepted outer-b stopping dichotomy.
For the other nonzero shifts up to absolute value 8 it supplies the analogous exact dichotomy. It
avoids the unproved DH_out needed to replace EXACT by a small
approximate family. Retaining the exact residual and its physical
ceiling is essential when the shifted output climbs.

Remaining work: prove a uniform record bound for reachable
TERMINAL-COLLISION states, control incoming shifts outside this
bounded range, and close the higher-scale conditions. The accepted
K_clock horizon and global open status are unchanged.

## 5. Exact canonical checks

Run python -B work_c3_drift/verify_first_a.py.

The test selects a canonical fire for every 5<=P<=256 and includes
all odd c crossings in those epochs, using Calendar(512). This gives
336 real source chains and 5,712 source/shift pairs:

* 336 zero shifts;
* 4,032 pairs with no odd a return before termination;
* 852 valuation-mismatch pairs that end at the next chain;
* 492 collision pairs, all of whose exact residual tails end within
  the remaining physical precision in this finite selection.

Every common b/c prefix, exact first-a formula, suffix loss offset,
and classification is checked. The 492 successes do not imply that
all terminal collisions close. first_a_checks.json records examples.
These are actual canonical source chains with counterfactual shifted
phases; the shifted phases are not claimed reachable in S(J).

## 6. Minimal classes versus stronger cylinders

The residuals were also tested using the representative
(2^j,2^j+delta) at precision j+1, delta=(T_eta-y_eta) mod 2^(j+1).
488 of the 492 minimal classes terminate with all records <=j.
Four fail this certificate: all have (j,delta)=(5,5).

Failure of that certificate does not establish a failure of the actual
tail. For each actual terminating suffix, let R be its maximum relative
record and K=R+1. HP says that its residues (x mod 2^K,Theta mod 2^K)
certify the entire corresponding cylinder. The verifier re-executes
these representatives using signed integer arithmetic, as permitted by
accepted HP/Proposition 3.2 (zero is still rejected). All match their
actual suffix words, and K is no larger than the available precision.

The four exceptional examples are:

| source P | eta | K | x mod 2^K | Theta mod 2^K | suffix word |
| --- | --- | --- | --- | --- | --- |
| 17 | -3 | 8 | 32 | 37 | 5,6,1 |
| 90 | -3 | 7 | 96 | 101 | 5,5,1 |
| 161 | -3 | 9 | 416 | 421 | 5,7 |
| 234 | -3 | 7 | 96 | 101 | 5,5,1 |

Thus the tested failures require only 1--3 bits beyond j+1. This
number is a finite observation, not a universal extra-bit bound.
The later targeted construction in TARGETED_PRECISION.md realizes
requirements up to 252 extra bits, while certifying those tails safely
through the parameterized gateway family.
The full residues are kept: conflating these four states merely by
their shared (5,5) class would discard the information needed to
resolve their different continuations.
