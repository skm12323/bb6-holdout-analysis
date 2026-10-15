# The (5,17) escape: retained variable, closure, and one reentry map

2026-10-15. New continuation of route A in `work_g2_paths`.
No independent review initiated. The full escape--reentry problem is
not closed; the exceptional branch and all safety guards are explicit.

## 1. Exact reduction with the old parameter-17 base retained

Take consecutive direct odd a blocks with entry values

    X0=32u, X1=2^17 v, u,v positive odd,
    k5=1, k17=6.

Their next chain value X and phase are

    X=16u+2^16 v+48;
    Theta=X-X0/4-3.

If v2(X)=Q>=18, put X=2^Q w. Eliminating u gives

    u=2^(Q-4)w-4096v-3;
    Theta=X/2+2^15 v+21.                         (R21)

The old v has not been reset: it is exactly the original parameter-17
odd base. Actual escapes from the cap-1023 certificate have Q>1023;
the following local result works for all Q>=18.

The original first-chain phase is Theta0=X/2+2^15 v-27. Nonnegative
lambda components at that chain imply the additional inequalities

    lambda_A0=196608v-X+37>=0,
    lambda_b0=3X/2-163840v-68>=0,

or equivalently

    ceil((X-37)/196608)<=v<=floor((3X-136)/327680). (BAND)

There is also the integral-time condition Theta0=2 mod 3. These are
necessary local compatibility constraints, not orbit reachability.
The uniform theorem below enlarges this set to all compatible R21
states; further analysis can keep BAND and the original lattice.

## 2. An arbitrary-height odd-a suffix theorem

Suppose a compatible R21 chain is safe, Q>=18, and its return is odd
type a with k=tau(Q-1)/2. The exact next state is

    Y=X/2+2^16 v+6(k+7);
    Theta1=X/2+2^15 v+24+6k.                    (A)

**Theorem (finite affine certificate).** If

    k !=32761 mod 65536,

the epoch ends safely in at most 13 further F steps following this
return. Including the Q chain, the bound is 1+tau(Q-1)+13. No upper
bound on Q, k, or the odd bases is imposed; the necessary earlier
prefix/replay assumptions remain in force.

Proof by certificate. Write X=2^18 U, with U any positive integer,
v=1+2b, and k=r+2^L z. Substitute U=1+a into (A). Both coordinates
are affine in independent nonnegative integers a,b,z. Starting with
the conservative post-return coefficient valuation sigma=18, propagate
the exact a/b/c updates. At each continued chain, compare the valuation
of the constant with all variable slopes; a strict comparison proves
one next parameter for every lift. End only at the known even-return
condition, with physical margin checked at every step.

`a_certificate.py` exhaustively splits only unresolved k cylinders up
to depth 16. It produces 16 closed cylinders and exactly one unresolved
cylinder, r=32761. Their disjoint weights sum to 65536. Closed suffixes
have at most two chains, at most 13 steps, and minimum margin 2.
The complete affine records are in `a_certificate.json`.

An even return at Q ends directly. An odd b/c return is covered by the
general-d shifted-copy rule (R21 has d=v2(Theta-2)=0; the earlier
shortcut was proved only for d=2, and the general-d rule is stated, not yet
proved, in work_g2_paths/RESEARCH_PATHS.md section 2.3) unless its first
source odd-a output is 1. That residual collision is exactly the accepted
work_g2_bc_frontier construction (the p=24480 source fire's a-output has
valuation 1), so this branch remains open, consistently with that note.
The same applies when another already stated source-shadowing hypothesis is
unavailable. That collision is not settled by the a-certificate.

## 3. The remaining a cylinder retains an exact new relation

The exceptional condition is precisely v2(k+7)=15. Since Q>=18 and v
is odd, formula (A) then implies v2(Y)>=17, with a possible high-bit
collision between the terms. Crucially, eliminating k gives

    Theta1=Y-2^15 v-18.                          (E)

This is the same old v, with its inherited constraints. The uncertainty
is not replaced by a fresh free phase. Neither the valuation nor safety
of a very large Y is established in this unresolved cylinder.

## 4. If the collision reenters at 17: an exact return map

Consider the subbranch v2(Y)=17. Its next return is the known odd a
with k17=6. Let its output be Z. Using (E),

    Z=3Y/2-2^16 v;
    v_new=Y/2^17 (positive odd);
    Theta2=Z/2+2^15 v_new+21.                   (RETURN)

Thus this subbranch returns exactly to R21. Also v2(Z)>=17. If the
new parameter is 17 and its margin is sufficient, its R21 a-return
produces parameter 1 and terminates. If it is >=18, another R21 cycle
is possible, but only if the new physical safety guard holds.

This two-return segment costs 2k+14 F steps and loses exactly two
coefficient bits. Safety of Y=parameter 17 follows from the input
margin when Q>=18. Safety of Z must still be checked: sigma_input-2
must strictly exceed v2(Z). In particular sigma_input>=20 suffices
for the Z-parameter-17 case. No safe infinite repetition is assumed.

### 4.1 A contracting signed quantity, with an explicit limitation

Define delta=X-2^17 v. On RETURN,

    delta_new=delta/4+3(k+7);
    v_new=v+delta_new/2^16.                       (DELTA)

These identities use the inherited v and are not merely low-bit
congruences. When both successive R21 entry parameters are >=18,
delta and delta_new have valuation exactly 17.

If delta_new<0, then |delta_new|<|delta|/4. Negative-delta repetitions
therefore cannot persist indefinitely for a fixed integer initial
state. Once delta becomes nonnegative, it remains positive on this
subbranch. However v then increases, so v is not a decreasing rank.

For a separately justified finite prefix with all these Q<=g and
earlier C1, put M=3((g-1)^2/2+7). Then 0<3(k+7)<=M, and

    |delta_t|<=4^(-t)|delta_0|+(4/3)M(1-4^(-t)).

After at most ceil(log_4(max(1,|delta_0|/M))) repetitions, the absolute
value is <4M; this interval is invariant under the guarded recurrence.
Thus this particular repeated subbranch has a finite-height signed
coordinate after a logarithmic transient. It does not follow that the
subbranch terminates: there are still many possible positive deltas,
v can grow, Q depends on both, and k is the actual crossing-time function.
The ceiling g must come from a legitimate bootstrap, not an assumption
about an unproved infinite continuation.

## 5. Progress along the proposed order

Route A now has an arbitrary-height closure theorem for most odd-a
escapes from (5,17), and an exact reentry map for one resonant subbranch.
The full unresolved cases are:

* exceptional a outputs with parameter other than 17, or lacking a
  proved physical margin;
* the odd b/c source-output-1 collision;
* repeated guarded RETURN cycles within the positive-delta region.

The source examination in route B does not yet show consumed ancestry.
The same small source at 17 is reused, while the high-Q source may
change. It would be incorrect to infer a decreasing source pointer.
DELTA instead gives a limited contraction statement, not a global rank.

For route C, BAND is a concrete additional restriction from the actual
prefix, and DELTA gives a polynomial-height window under a valid g
bootstrap. The next useful test is to retain both when checking the
positive-delta transitions, including their inherited congruence lattice.
No claim is made that the resulting finite-height state space is small
enough, or has no cycles. Route D's all-scale classification is deferred
until a complete boundary transfer is established.

## 6. Verification

    python -B work_g2_escape_5_17/a_certificate.py
    python -B work_g2_escape_5_17/verify_pair.py

The latter runs the full pair map from 20 compatible local (5,17,Q)
prefixes with ten Q values up to 1021 and two different high bases.
Every path, exact duration, mass identity and safety margin agrees with
the certificate. These local prefixes are not asserted to occur on the
distinguished orbit. It also cross-checks the algebra of DELTA; those
checks do not assert actual occurrence of the resonant RETURN subbranch.
