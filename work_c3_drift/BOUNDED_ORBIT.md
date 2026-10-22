# Complete finite exponent cover for the parameter-49 source

2026-10-20. **UNREVIEWED mathematical assembly; independently implemented
certificate replay passes.** This is a finite family result at one
canonical source, not an all-source or global EXT theorem.

## 1. Fixed source and a bounded-depth question

Use the actual source of ORBIT_SHIFT_OBSTRUCTION.md:

    x0=5*2^49, sigma=1051689726214394,
    y=4222124650659962, T=x0+124,
    eta_r=-5+8/3^r.

After its first a return, the shifted residual is

    x_r=y-10+16/3^r, Theta_r=T-5+8/3^r,

with physical precision sigma-1. The full-unbounded-r safety property
is false by the earlier group argument. We now prove the finite statement:

    Every integer 0<=r<=10^30 gives a terminating residual with
    all records strictly below sigma-1.

The shifted root's initial parameter 49 is also below sigma, so these
entire shifted tails are safe. Joint reachability of the shifts with
this source in S(J) is not asserted.

## 2. A certified binary residue class of exponents

Fix b>=1 and r=a mod 2^b. Repeated squaring gives

    3^r=3^a (mod 2^(b+2)).

Therefore x_r=x_a mod 2^(b+6) and Theta_r=Theta_a mod 2^(b+5).
Their common known precision is K=b+5. Execute the exact finite
representative (x_a mod 2^K,Theta_a mod 2^K), allowing signed integer
representatives but rejecting zero. If it terminates with every
relative record <K, HP certifies the whole exponent residue class.
Here each retained K is smaller than sigma-1, so its physical margin
is sufficient. Rational inputs are covered by the odd-unit scaling
argument of ORBIT_SHIFT_OBSTRUCTION, not by treating them as integers.

The search starts with the two parity classes. A failed certificate
is split into a mod 2^(b+1) and a+2^b mod 2^(b+1). Classes whose least
nonnegative member exceeds R are pruned. Time/depth limits produce
explicit unresolved nodes and cannot produce PASS.

## 3. Coverage and independent replay

For R=10^30, the completed tree has 396 visited nodes and 198 certified
leaves; no unresolved node remains. A leaf (a,b) covers exactly
floor((R-a)/2^b)+1 integers in the target interval. A separate checker
verifies every pair of leaves is disjoint modulo 2^min(b1,b2), and
their counts sum to exactly R+1. Thus this is exhaustive coverage,
not random or sparse sampling of exponents.

The generator uses Calendar for representative tails. The replay
uses shiftlib.Tables and its independent full-pair source reconstruction,
then exact_tail for each leaf. All 198 words and strict record bounds
match. Only canonical table indices through 107 are needed. An
additional 594 period checks match the class residues. This is an
independent implementation check, not independent proof review.

Reproduction:

    python -B work_c3_drift/verify_bounded_orbit.py 1000000000000000000000000000000
    python -B work_c3_drift/check_bounded_orbit_certificate.py

The corresponding bounded_orbit_*.json and bounded_orbit_replay_*.json
files retain all leaves and replay totals. The smaller R=10^6 run is
also saved (78 visited nodes, complete coverage).

## 4. Exact first-output bound on the interval

For A=(y-10)/16 and H>=3, let r_H be the least nonnegative discrete
log solving 3^r=-A^(-1) mod 2^H. All such exponents are
r_H mod 2^(H-2). Hence an exponent in [0,R] has
v2(A*3^r+1)>=H if and only if r_H<=R.

For R=10^30 the first excluded lift is

    H=102, r_H=1042434400033284774852912479058 > R.

At H=101 the least lift is 408609099919170074104560876370<=R.
It has exact valuation 101, so the maximum first residual parameter
on the full interval is exactly 4+101=105. This bound alone would
not prove suffix termination; the complete leaf certificates above do.

## 5. Stopping point and remaining global work

Stopped at the user's requested next node after certificate replay.
No new branch was started after saving this result. All work in
work_c3_drift remains unreviewed and uncommitted; accepted documents
and K_clock are unchanged.

On resumption, the central missing fact is still a uniform relation
between actually reached denominator depths, the selected ancestor
source, and its physical precision. This finite cover settles one
source up to a large explicit depth, not arbitrary sources or depths.
Other unresolved obligations include high-deficit c control, generic
landing certification, and total record budgets across repeated gateways.
The full non-halting objective has not been achieved.
