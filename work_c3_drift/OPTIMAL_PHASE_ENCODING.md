# Exact local encoding cost and a counting obstruction

2026-10-21. **UNREVIEWED encoding result.** This concerns finite phase
descriptions, not the safety or reachability of their continuations.

## 1. The quantity minimized

For a known defect Phi modulo 2^(m+1), seek

    Phi=c+b*2^m mod 2^(m+1), c=C/3^r reduced, b in {0,1},
    cost=2r+ceil(max(0,1-c,c-2)).

The freely recorded bit b means the cost depends only on Phi modulo
2^m. The bit itself is then determined and retained explicitly.
This is precisely the local charge used by JOINT_HEIGHT_BUDGET.

## 2. Finite exact minimization, with no denominator cutoff guess

The previous rank-m height-zero construction costs at most 2m.
Any reduced rank greater than m costs more, so it cannot improve
the minimum. Thus only r=0,...,m must be considered.

For fixed Q=3^r, allowable numerators form the lattice

    C=Phi*Q mod 2^m.

Height is the ceiling of distance from C/Q to [1,2]. Its minimum
on this lattice is attained at the two neighbors of Q (one below
and one at/above it). If the latter lies in [Q,2Q], it already has
height zero; otherwise those two neighbors minimize distance to
the interval. The implementation evaluates them and reduces each
fraction before charging its rank.

A more distant candidate at the same reduced rank cannot improve
height. If it has a smaller rank through cancellation, that reduced
description is considered in the earlier rank search. Therefore
the algorithm finds the global minimum over all power-of-three
denominators, not merely a minimum within an arbitrary search depth.

## 3. Exact finite checks

    python -B work_c3_drift/verify_optimal_phase_encoding.py

All 8,190 low phase classes for m=1..12 are optimized, with both
choices of the extra input bit checked. For m<=7, a separate full
numerator enumeration under cost 2m agrees on all 254 classes.

Examples of the largest minimum costs:

| m | maximum minimum cost | classes affordable with charge <=m |
| --- | --- | --- |
| 5 | 5 | 32 / 32 |
| 6 | 7 | 60 / 64 |
| 8 | 10 | 214 / 256 |
| 10 | 12 | 676 / 1024 |
| 12 | 15 | 2130 / 4096 |

These are all local classes, not asserted canonical source classes.
The JSON retains worst-case examples and their optimal descriptions.

## 4. A general obstruction to a uniform small reserve

With total local charge at most S, a rank r<=S/2 has height at
most S-2r. Its numerator must lie in

    [(1-(S-2r))*3^r, (2+(S-2r))*3^r].

Thus the number of low phase classes representable with that charge
is at most

    sum_(r=0..floor(S/2)) [(2*(S-2r)+1)*3^r+1].

This is an upper bound: it deliberately overcounts duplicates and
unreduced fractions. For m=S=64 it equals 8,338,590,849,833,250,
strictly below the 18,446,744,073,709,551,616 possible low classes.
So even reserve S=m cannot encode every class in this format.
No enumeration of the 64-bit classes is needed for that conclusion.

This does not imply any canonical source violates the proposed
contract. It proves only that such a contract must exploit actual
phase/origin restrictions or provide a larger reserve; it cannot
follow from a claim about all local residue classes with that budget.

## 5. How this can be used without overstating it

At a specific reached source, the encoder can check whether its
actual minimal phase class fits the available reserve P-Gamma-m.
It improves on the deliberately loose rank-m fallback when possible.

It does not increase the known precision beyond m+1. Replacing an
analytic rational family by a cheaper congruent description can
discard the higher bits needed by a later bare tie. Keep the
original affine/family provenance when those bits are required.
The encoder alone cannot close small gateways, prove later
termination, or establish the source contract at every scale.
The global objective and accepted horizon remain unchanged.
