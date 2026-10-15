# Shared clocks close two-high-parameter a branches of the (5,17) escape

2026-10-15. New continuation, not independently reviewed. This note
does not close high b/c branches or establish a global non-halting
theorem. All actual-prefix and safety assumptions below are explicit.

## 1. Two correlated families

Write R for the previously obtained R21 family

    R: Theta=X/2+2^15 v+21, v positive odd, q=v2(X)>=18.

If its return is odd a, put k0=tau(q-1)/2. The output is

    Y=X/2+2^16 v+6(k0+7),
    Theta1=Y-2^15 v-18.                         (R->E)

The existing certificate closes the whole suffix unless
k0=32761 mod 65536. In that exceptional case the output parameter
p=v2(Y) is at least 17. For p>=18 define the resulting family

    E: Theta1=Y-2^15 v-18.

It retains the same v and, for an actual R->E transition, the equation
for Y and the actual k0. Proving a statement for arbitrary compatible
E states enlarges this set; when that enlargement leaves exceptions,
the retained R->E equation must be restored.

Neither the existence nor safety of a very high Y follows from these
equations alone. The two-high theorem below assumes this intermediate
entry is already safe, for example under an independently justified
finite-prefix bootstrap.

## 2. Uniform E a-return certificate and its two exceptions

At a safe E entry with p>=18, an odd a-return with k1=tau(p-1)/2 gives

    Z=3Y/2-2^16 v+6(k1-6),
    Theta2=Y-2^15 v-15+6k1.                     (E-A)

`verify_e.py` represents Y=2^18 U with U arbitrary positive, v positive
odd, and k1 in dyadic cylinders. It propagates signed affine slopes
with exact valuation separation and sigma>=18 after the return.
Compatible actual states are a subset of these formal affine inputs.

The exhaustive certificate has 26 closed cylinders covering all k1
mod 65536 except the following two:

| k1 residue | Unresolved stage |
|---|---|
| 32774 | Immediately after E-A; output parameter >=17 |
| 54614 | E-A has output 5; its following a-return is unresolved |

Every closed cylinder ends safely in at most 16 steps after E-A, with
at most three chains and minimum coefficient margin two. These are
uniform statements over all compatible high-bit values, not sampling.

The second exception is real in this overapproximation. One must not
claim that E has only the first exception or that R and E alone are
already a closed two-state termination system.

## 3. Restore the first source clock in both exceptional branches

Assume E came from R as in section 1, with actual half-time k0. Write
q=v2(X), p=v2(Y), and g=max(q,p).

### 3.1 k1=32774 mod 65536 returns to R

Put k1=6+2^15 t1, t1 positive odd. The endpoint identity yields

    Theta2=Z/2+2^15 v_new+21,
    v_new=Y/2^17+3t1, positive odd,
    v2(Z)>=17.

Thus it returns to R, or to its parameter-17 terminal special case.
Moreover the shared-clock positive identity is

    Z=(X+Y)/2+6(k0+k1+1).                       (POS-R)

The final constant, not an arbitrary new phase, determines the return
valuation whenever its size is below the two preceding binary scales.

### 3.2 k1=54614 mod 65536 gives a phase-minus-two family

E-A first produces parameter 5. Apply the known a-return there with
k5=1, and call its output W. Direct substitution retaining k0 gives

    W=X/4+3Y/4+3(k0+3k1+5);
    Theta_W=X/4+Y/2+3k0+6k1+15.                (POS-D)

Since k0=32761 mod 65536 and k1=54614 mod 65536, and q,p>=18,

    v2(W)>=16, Theta_W=32766 mod 65536.

Equivalently Theta_W=-2+2^15 V with V positive odd for compatible
positive-time states. Denote this phase family by D. It need not lie
in R or E. This extra family is handled below at the required small
parameters, without pretending it disappears.

## 4. Three finite small-parameter suffix certificates

The saved affine certificates prove safe closure of every compatible
state in these ranges, uniformly in the indicated odd variables:

| Family | Entry parameter | Sufficient initial sigma | Maximum F steps |
|---|---|---|---:|
| R | 17..1023 | q+1 | 912 |
| E | 18..1023 | q+1 | 914 |
| D: Theta=-2+2^15 V, V odd | 16..1023 | max(q+1,18) | 923 |

The R and E certificates contain 1007 and 1006 families. The D
certificate contains 1008. All reach an even return with positive
coefficient margin. For D at parameter 17 the exact path is

    17,5,6,1,

and takes 21 steps. The non-descending 5->6 step is explicitly included.
None of these finite ranges is extrapolated to all parameters.

## 5. Conditional closure of two successive high odd-a entries

**Theorem.** Suppose a compatible R entry at q>=1024 makes its
exceptional odd a-return, and its output Y is a safe entry with
p>=1024. Suppose the return at p is also odd a. Assume earlier C1
for the two high calls, and max(q,p)<=2^500. Then the whole remaining
tail ends safely from Y onward. If k1 is not exceptional, section 2
applies. If k1 is either exceptional residue, the following argument
establishes safety and closure of its subsequent outputs.

For the first exception, C_R=6(k0+k1+1) is positive and at most
6g^2+6. For the second, C_D=3(k0+3k1+5) is positive and at most
6g^2+15. With g<=2^500, both are strictly below 2^1003.

In POS-R the high terms are divisible by 2^1023. Hence

    17<=v2(Z)=v2(C_R)<=1002.

The coefficient valuation at Z is at least p, so Z is safe and the
small R certificate applies.

In POS-D the high terms are divisible by 2^1022. Hence

    16<=v2(W)=v2(C_D)<=1002.

The intermediate parameter 5 is safe, and the coefficient valuation
at W is at least p-1>=1023. Thus W is safe and the small D certificate
applies. This includes the certificate's slightly stronger sigma
requirement for parameter 16.

In the first exceptional branch the total cost from the initial R
chain is at most 2(k0+k1)+914. In the second it is at most
2(k0+k1)+928. These include the final even return. The case where
k1 is nonexceptional has bound 2(k0+k1)+18.

The theorem does not prove the initial transition R->E safe when Y
has arbitrary high valuation. Nor does it cover an odd b/c return at
p. The sufficient scale cap is part of the statement, not a newly
certified unconditional machine horizon.

## 6. Relation to the previous repetition budget

Starting at R, a nonexceptional odd a-return closes. An exceptional
output of parameter 17 is the guarded reentry pattern studied in
`work_g2_reentry_budget`. Outputs 18..1023 are closed by the small E
certificate. An output >=1024 with another odd a-return is now closed
under section 5's hypotheses. Even returns end directly.

Thus, within the corresponding guarded scale bounds, the remaining
structural obstruction is more concentrated on high odd b/c entries
and on establishing the safety of the first resonant high output.
The repetition budget and this theorem cannot be combined into a
global theorem by assuming those missing guards. Interleavings through
other return types can still leave and later reenter these families.

## 7. Reproduction and verification scope

    python -B work_g2_escape_two_phase/verify_e.py
    python -B work_g2_escape_two_phase/verify_shared_clock.py
    python -B work_g2_escape_two_phase/verify_small_r.py
    python -B work_g2_escape_two_phase/verify_small_e.py

The shared-clock script checks 64 exact identity instances and saves
the full D affine certificate. The other scripts save their complete
uniform affine traces. Source-clock identities are algebraic checks,
not witnesses of actual two-high escapes on the distinguished orbit.
The analytic size argument in section 5 supplies its all-parameter
conditional scope.
