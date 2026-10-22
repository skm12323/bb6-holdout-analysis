# The missing five-entry clock condition bounds short-scale gateway trains

2026-10-20. **UNREVIEWED proposed theorem.** Uses the exact recurrence
of GATEWAY_TRAIN, the accepted small canonical base, and C1/clock inputs.
It bounds consecutive all-a gateway trains, not arbitrary return words.

## 1. A necessary clock residue omitted from the first graph

At a five-chain write x=32u with u odd. If its a output y has
parameter m>=5, then

    y=-16u+2Theta+6=0 mod 32,
    Theta=5 mod 16.

For a train 5,m_i,5,m_(i+1), the two five-input clocks both have
that residue. Since their difference is 12+6*k_i,

    k_i=6 mod 8.

The only odd-a label below 8 is m=5 with k=1, which is excluded.
Thus m_i>=8. The exact pair relation from GATEWAY_TRAIN gives

    Theta_i+21+9*k_i=0 mod 2^min(m_i-2,m_(i+1)).

Its modulus includes 16. Substituting Theta_i=5 mod 16 strengthens
the condition to

    k_i=6 mod 16.                                  (ENTRY)

This applies to every catapult label except the last in a finite
train, because it requires the next catapult to occur. The audited
base through index 15 shows such an internal label is at least 17.
At its real source crossing X(m_i-1), half-time k_i has fire parameter
1+v2(3*k_i+2)=3. This is real source provenance, not merely a phase label.

## 2. Exact valuations are stronger than divisibility alone

Recall

    4*y_(i+2)-5*y_(i+1)+y_i=12*Z_i,
    Z_i=4-k_i+3*k_(i+1).

Among the valuations m_i, m_(i+1), m_(i+2)+2 and
2+v2(Z_i), the smallest must occur at least twice (omit the last
term when Z_i=0). The original necessary-condition graph checked
only divisibility and omitted this additional restriction.

In particular, if Z_i=0 then k_i=3*k_(i+1)+4>k_(i+1).
Canonical crossing times are nondecreasing with their original index,
so m_i>m_(i+1). The two terms y_i and 5*y_(i+1) then have distinct
valuations, and the exact equation forces

    m_(i+2)=m_(i+1)-2.                             (DROP2)

If both these latter labels are internal, ENTRY says that both
correspond to actual parameter-three source fires. That is impossible:
the uniform parameter-three kernel advances its original pointer by
five before the next fire. Two such source fires cannot be separated
by only two original positions. Thus a triple of internal labels
cannot have Z_i=0.

## 3. No four catapults in a suitable band

Suppose four consecutive catapult labels all lie in [L,M] with

    4+2*(M-1)^2 < 2^(L-2).

The first three labels are internal. TRAIN and C1 force Z_0=0,
because its absolute value is less than its required divisibility
modulus. Section 2 yields a contradiction. Therefore such a train
has at most three catapult labels. This improves the earlier
logarithmic train bound within the same band hypothesis.

More usefully at small scales, the accepted finite base has
tau(n)<=n for n<10^8. For four labels in [5,16381], their first three
internal labels are >=17 by ENTRY, so TRAIN requires 2^15|Z_0.
Yet k_i<=(16381-1)/2 and hence

    |Z_0| <=4+k_0+3*k_1 <=32764 <2^15.

Again Z_0=0, giving the same contradiction. Thus:

    Every valid all-a train whose catapult labels remain in
    [5,16381] has at most three consecutive catapult labels.

The statement is uniform in the input numerator, clock, odd
denominator, and available precision, provided the displayed valid
returns exist. It is not an assertion that all other continuations end.

## 4. Finite graph verification and its scope

The revised graph checks ENTRY, the pair clock residue, TRAIN and
the repeated-minimum valuation condition. For labels [5,256] it has
532 vertices and 14 edges, is acyclic, and permits at most three
catapult labels. One longest necessary word is (17,125,5); its
shared initial-clock constraints are consistent, but no claim of
full numerator feasibility or canonical reachability is made.

The raw cycle (8,244,81,27) from GATEWAY_TRAIN is excluded already
by ENTRY: the clock for label 8 has k=2, not 6 mod 8. The old graph
was deliberately only an overapproximation; the new result adds
conditions that every real train must satisfy.

    python -B work_c3_drift/verify_clock_filtered_train.py

The checker also recomputes 16,381 linear clock bounds through the
direct lambda walker and 899 parameter-three source pointer gaps.
The general band and no-four proofs rest on the stated identities,
not on extrapolating the finite graph.

## 5. What is still missing for the denominator budget

The 3-adic orbit's consecutive a-gateway/a-return pattern cannot
accumulate arbitrarily many denominator generations while every
catapult remains in this small interval. To continue beyond three,
a trajectory must leave the interval or break the all-a pattern.

This is not yet a bound on the total exponent r: b/c interruptions
can connect separate trains, and larger parameters can re-enter.
Those inter-scale and interrupted histories must be charged to a
shared record budget before the source/depth obstruction is excluded.
Global EXT and the accepted horizon are unchanged.
