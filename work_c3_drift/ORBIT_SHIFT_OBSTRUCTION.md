# Bounded real height does not give uniform shifted-source safety

2026-10-20. **UNREVIEWED proposed obstruction**, using a verified
canonical source. This rules out a stronger uniform safety target;
it does not disprove EXT or establish a halting trajectory.

## 1. Rational shifts and the actual source

The common-shift transport extends algebraically to rational eta with
odd denominator Q. Work over Z[1/Q]: scaling x and Theta by Q gives
integer recurrences with constants multiplied by Q. Since Q is a
2-adic unit, valuations and record losses are unchanged. The finite
HP argument still transfers a reference tail whose records are
strictly bounded. This does NOT assert that every rationally shifted
reference is safe; the counterexample below addresses that stronger
claim, not the earlier conditional transport lemma.

Calendar(512) verifies the actual fire

    P=49, k_fire=469124961184426,
    rho=sigma=1051689726214394,
    x0=5*2^49, Theta0=x0+1.

Its first return reads X(48), an odd-a crossing at time 40 (half-time
k=20, reached fire pointer 48). Its real a-output numerator is

    y=(3/2)*x0+122=4222124650659962=16*A+10,
    A=263882790666247=7 mod 8, A+1<2^48.

It has valuation 1, so this real epoch ends at its first a output.
All source time/pointer identities are exact canonical queries within
the calendar's permitted range.

## 2. The relevant infinite orbit shifts

The accepted rational orbit is c_r=-3+8/3^r. In the interior-source
transport, the corresponding shift is

    eta_r=c_r-2=-5+8/3^r, r>=0.

Its real absolute value is at most 5 and its 2-adic valuation is zero.
The shifted root's first output is exactly

    y_r=y+2*eta_r=16*(A+3^(-r))>0,
    v2(y_r)=4+v2(A*3^r+1).

The first a update costs one unit of physical precision. Therefore
strict shifted-source safety fails at that output whenever

    v2(A*3^r+1)>=sigma-5,

since the record is then at least (sigma-1)+1=sigma. This failure
is detected before any subsequent call is made; no undefined later
crossing is being assumed.

## 3. Such r exist, by an elementary group calculation

For every H>=3, the powers of 3 modulo 2^H are exactly the units
congruent to 1 or 3 modulo 8. Indeed their order is 2^(H-2): the
valuation identity v2(3^(2^t)-1)=t+2 follows by repeated squaring
from 3^2-1=8. The listed residues form a subgroup of that same size.

Since A=7 mod 8, the target -A^(-1) is 1 mod 8. Thus, for every
H>=3, there is an r in [0,2^(H-2)) satisfying

    3^r=-A^(-1) (mod 2^H).

Take H=sigma-5=1051689726214389. This proves existence of an
eta_r in the bounded-height orbit for which the strictly bounded
rational scalar tail is unsafe at its first output. The theorem
does not require computing or printing that r. It is NOT evidence
that this shift occurs jointly with this source along S(J).

More generally, if a real terminal output is y=16A+10 with A odd,
unbounded first-output valuation over this orbit is possible exactly
when A is 5 or 7 modulo 8. For A=1 or 3 modulo 8, the product
A*3^r+1 always has valuation 1 or 2, so the shifted output parameter
is always 5 or 6. If v2(y-10)!=4, no cancellation at that scale
occurs and the shifted output has parameter at most 4.
The dangerous terminal residues are therefore y=90 or 122 mod 128.
This is only a first-output classification, not a whole-tail theorem.

## 4. The obstruction needs enormous denominator depth

The bounded-height counterexample is not a contradiction of any
fixed-depth result in this directory. Since A+1<2^48 and 3^5<2^8,

    (A*3^r+1)^5 < 2^(240+8r).

If its valuation is at least sigma-5, then
5*(sigma-5)<240+8r, hence

    r > 5*(sigma-53)/8,
    r >= 657306078883964.

Thus the unsafe shifts here require at least that many denominator
generations. A valid proof may still exclude their joint reachability
using an ancestry/record budget. Such a budget has NOT been proved.
The common-shift theorem, finite window certificates, and ordinary
integer-shift results remain intact.

## 5. Verification and next target

    python -B work_c3_drift/verify_orbit_shift_obstruction.py

The script verifies the exact canonical source and lifts discrete
logs for H=3,4,5,8,16,32,64,128,256. For moderate r it also expands
3^r and checks the valuation directly. The full physical-precision
failure follows from section 3's all-H proof, not extrapolation from
these finite modular tests. The script does not simulate the full-H
shifted orbit or assert it is canonically reachable.

The resulting global obligation is sharper: one must relate the
actually reached denominator exponent r to the specific ancestor
precision sigma, or exclude the corresponding dangerous residue.
Proving Safe(C,eta_r) uniformly for every r at each real source C
is false, even with |eta_r|<=5. Continuing to enlarge a finite family
scan cannot establish that false target. EXT remains open and the
accepted horizon is unchanged.
