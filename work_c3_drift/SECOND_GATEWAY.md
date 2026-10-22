# Second rational gateway, with retained parent precision

2026-10-20. **UNREVIEWED.** Resolves a bounded-output branch of the
rational-mode landing obstruction. It is not a proof of HR5 or EXT.

## 1. Exact emission and the missing-bit condition

At a parameter-five state, write x=32u, D=Theta-x. X(4) is odd a
with half-time 1. Its exact next state is

    y=3*x/2+2D+6, T=x+D+9,
    3*(T-y)=15-D-y.

Suppose 3D=C mod 2^H, C=-1 or -17, and m=v2(y)<H. Then

    T-y = (45-C)/9 - 2^m/3 (mod 2^(m+1)).

The two emitted classes are thus

    E46(m)=46/9+2^m mod 2^(m+1),
    E62(m)=62/9+2^m mod 2^(m+1).

The plus 2^m is equivalent to -2^m/3 at this modulus. The condition
m<H is essential. Knowing only the minimal class at parameter five
supplies H=6, which need not suffice. For example x=32 with D=37
and D=165 gives the same input D mod 64=37 and the same next m=7,
but output defects 206 and 78 modulo 256, respectively. Only the
second lift has the higher precision of -17/3 needed for E62(7).

Hence the 3,966 successful minimal classes and two failed classes
from RATIONAL_MODE must not be interpreted as two unconditional
transitions to these emitted families.

## 2. A large a predecessor supplies the missing precision

Let a parent parameter j>=N0 carry C0/3 with C0=10 or 26 modulo
2^j (either extra-bit lift is allowed). Suppose its a return lands
at parameter five. Write k=tau(j-1)/2. With parent numerator x,
defect D and phase x+D, two consecutive a steps have exact output

    y2=5*x/4+D+9k+12.

Consequently

    m=v2(27k+C0+36),

provided the numerator's valuation is below j-2. This proviso
follows from the accepted C1 bound for every j>=N0:

    0 < 27k+C0+36 <= (27/2)*(j-1)^2+62 < 2^(j-2).

For the last inequality, its doubled integer form holds at N0
(the polynomial is below 2^54), and the positive quadratic grows
by a factor below two per unit j for j>=4. Thus m<j-2, with no
DH_out hypothesis. Terms containing the parent's x have valuation
j-2 and cannot alter m.

After the first a step, D1=3-D-x/2 agrees with (9-C0)/3 to
precision H=j-1. Therefore H>m, and section 1 applies to give
E46(m) for C0=10 and E62(m) for C0=26. The two-step record is
m+2<j, strictly below the parent's record after adding prior loss.

This argument is specific to an a predecessor with C0=10 or 26.
Other routes into the same minimal parameter-five class still need
their own precision provenance; the conditional emission alone
does not supply it.

## 3. Finite emitted-family certificates and a closed branch

For every 5<=m<16384, direct signed representative execution verifies
both E46(m) and E62(m) at precision m+1, with maximum record <=m.
There are 32,758 certificates and zero failures. This is finite
evidence, not an all-m theorem. For m<=4 the small canonical base
terminates immediately.

Combining with section 2 closes the entire tail whenever its m is
below 16384. A convenient sufficient parent range is

    N0 <= j <= 2^8190.

Indeed 27k+C0+36 <= 13.5*(j-1)^2+62 < 16*j^2 <= 2^16384,
so m<=16383. HP transfers the emitted-class certificate, and the
strict two-step record drop gives the full physical margin.

This closes that particular pair of large-parent a->5 branches
without assuming RES or certifying all rational landing classes.
It does not control parents above the range, other predecessor
types, high-deficit c transitions, or the infinite 3-adic family.

## 4. Verification and scope

    python -B work_c3_drift/verify_second_gateway.py

744 exact emission checks exercise m=5..128 with three higher-bit
lifts for each family. The two insufficient-precision controls are
retained. All 32,758 emitted-family representatives terminate with
their stated record bounds. Source crossing data come from the
certified calendar; the tested shifted states themselves are
synthetic and are not asserted to be canonical trajectories.

The 46/9 emission is already present in the accepted route-A orbit;
it is not claimed as a new discovery. The contribution here is its
explicit precision audit together with the 62/9 branch and the
stated finite closure range. No accepted horizon changes.
