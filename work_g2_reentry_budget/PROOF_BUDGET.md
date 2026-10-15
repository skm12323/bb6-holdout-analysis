# A repetition budget for the guarded R21--17 reentry pattern

2026-10-15. New conditional result, not independently reviewed.
This bounds consecutive occurrences of one reentry pattern. Leaving
that pattern is not the same as ending the epoch, and no global
non-halting or new unconditional horizon is claimed.

## 1. Retain the integer coordinates, not just a contraction estimate

Use `work_g2_escape_5_17/PROOF_ESCAPE.md`. An R21 entry has

    X=2^Q w, Theta=X/2+2^15 v+21,
    Q>=18, v,w positive odd.

Consider a completed, safe segment

    R21 at Q -> parameter 17 -> R21 at Q_new>=18,       (R)

with both returns odd type a. Its first half-call time is the actual
earlier value k=tau(Q-1)/2; the second is k17=6.

Necessarily v2(k+7)=15. Put

    t=(k+7)/2^15, positive odd;
    delta=X-2^17 v, d=delta/2^17, N=v+d=X/2^17.

Since Q>=18 and v is odd, d is an odd integer, possibly negative,
whereas N is positive and even. The retained entry parameter is

    Q=17+v2(N).

The exact RETURN identities become

    d_new=(d+3t)/4;
    v_new=v+2d_new;
    N_new-N=(9t-d)/4.                              (INT)

For a successful R segment, d_new and v_new must be odd integers.
In particular, the intermediate output has parameter 17 only if

    d+3t=0 mod 4.                                  (17-GUARD)

These are constraints on the same old variables, not independently
chosen congruence representatives at the next entry.

## 2. Equal N forces the next R segment to fail its 17 guard

Suppose one successful segment has N_new=N and the next entry is
eligible for another R segment. Equation INT implies d=9t, hence
d_new=3t. Equality of N implies equality of Q. Because k is the actual
crossing-time function of Q, the next t is the same t, not a new free
odd number. But then

    d_new+3t=6t=2 mod 4,

contradicting the next 17-GUARD. The next a-output has parameter at
least 18 instead of 17; no assertion is made here about its safety or
subsequent termination.

Consequently, two consecutive successful R segments require
N_new!=N. If their entry parameters are Q,Q_new, then both N values
are multiples of 2^(min(Q,Q_new)-17), so

    |9t-d| >= 2^(min(Q,Q_new)-15).                 (GAP)

GAP is an all-scale necessary condition for two consecutive segments.
It explains why the real-size information discarded by a purely
2-adic state description can matter.

## 3. Earlier C1 makes every such entry at least 257

On this pattern k=32761 mod 65536, hence k>=32761. Earlier C1 at Q-1
gives k<=(Q-1)^2/2. Since

    255^2/2<32761<=256^2/2,

every R-segment entry satisfies Q>=257. Thus N at every such entry
is divisible by 2^240.

This lower bound is only necessary. It does not assert that an actual
source with the requisite half-time occurs at Q=257.

## 4. The height window and a concrete scale range

Assume a separately justified finite prefix of consecutive successful
R segments has Q<=g, and C1 holds at the earlier calls it uses. Define

    K_g=(g-1)^2/2;
    T_g=(K_g+7)/2^15;
    M_g=3(K_g+7).

The forcing term in delta_new=delta/4+3(k+7) lies in (0,M_g]. Therefore

    |delta_i|<=4^(-i)|delta_0|+(4/3)M_g(1-4^(-i)).

Put

    n*=ceil(log_4(max(1,|delta_0|/M_g))).

After n* successful segments, if that many occur, the entry satisfies
|delta|<4M_g. This window is invariant under any further successful
segment obeying the same scale bound. In normalized coordinates,

    |d|<3T_g, t<=T_g,
    |N_new-N|=|9t-d|/4<3T_g.                     (SMALL)

For g<=2^127 we have the strict inequality

    3T_g<2^240.

Indeed this is equivalent to
3((g-1)^2/2+7)<2^255, which holds at g=2^127 and hence below it.

Suppose two consecutive successful R segments begin in this window.
Their two entry N values are multiples of 2^240, by section 3, and
their difference has absolute value <2^240, by SMALL. They must be
equal. Section 2 then contradicts the second segment's 17-GUARD.

**Conditional repetition-budget theorem.** With earlier C1 and a
valid finite-prefix cap g<=2^127, any run of consecutive successful
R21 ->17 ->R21 segments with all R21 parameters >=18 contains at most

    n*+1

segments. This covers the positive-delta region as well as negative
delta. The bound follows by a finite-prefix contradiction and does
not assume an already-defined infinite continuation.

The numerical cap is a sufficient bound for this argument, not a
maximal threshold. For arbitrary g the universal GAP condition and
height recurrence remain valid, but the final equality argument need
not apply.

## 5. Cost accounting and the exact meaning of 'pattern ends'

Each successful R segment costs 2k+14 F steps and loses two coefficient
bits. Thus the completed run has cost at most

    (n*+1)((g-1)^2+14)

and coefficient loss at most 2(n*+1). This counts completed R segments;
it does not bound all future work after the path leaves this pattern.

If a legitimate epoch bootstrap also supplies s<=2rho^2 at the initial
entry, nonnegative lambda components give X<=6s+5<=12rho^2+5.
R21 compatibility gives |delta|<=X, so the transient n* is O(log rho).
These statements are conditional on the already justified bootstrap;
they cannot be used to assume C1 for an epoch still being proved.

The pattern can end because an a-output is no longer parameter 17,
because the following R21 parameter is 17 or below, because another
return type is encountered, or because the hypothesized safe segment
is unavailable. The theorem excludes arbitrarily many *safe successful
segments of this exact form* in the stated range. It does not prove
that every departure is safe or terminates.

## 6. What this adds, and what remains

The preceding note had only a contraction toward a bounded positive
region. This note uses the inherited integers and the actual source
clock to show that the specified pattern cannot keep repeating within
that region, for the stated scale range. The crucial extra facts are
the large common divisibility of N and that equal Q forces equal k.

The unresolved work is now the continuation after the pattern breaks:

* the new a-output with parameter >=18 and its physical margin;
* b/c source-output-1 collisions;
* returns to R21 separated by other subpatterns;
* unbounded scales beyond the sufficient g range.

No source-pointer decrease has been inferred. Nor does a bound on a
single consecutive pattern control the number of times it can recur
after an intervening different path.

## 7. Reproduction

    python -B work_g2_reentry_budget/verify_budget.py

The script checks 49152 exact INT identities, 512 equal-entry guard
obstructions, 120 height-envelope instances, and the rational constants
at g=2^127. Algebra inputs can have negative chain values and are not
orbit witnesses; the proof's actual states require positivity. The
all-parameter statements follow from the displayed identities and
inequalities, not extrapolation from those test cases.
