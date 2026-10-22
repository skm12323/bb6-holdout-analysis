# Epsilon-three c steps preserve the small drift

Latest stopping/resume pointer: [phase-encoding checkpoint, 2026-10-21](STOP_CHECKPOINT_ENCODING_2026_10_21.md).
Paused at the user's request after completing that node; global EXT remains open.

**Review status (2026-10-23):** sections 1-4 of this note, C5_EXTENSION.md, UNBOUNDED_C_PARAMETER_IF_EXT.md
and the review note CONGRUENCE_TARGET_NOTE.md were ACCEPTED with corrections; see
reviews/c3_drift_review_record.md. All other files in this directory remain unreviewed.

2026-10-20. **UNREVIEWED.** Proposed symbolic lemma and conditional reduction,
plus exact finite canonical checks. No global EXT or non-halting claim.
The accepted horizon remains K_clock. This note does not supersede accepted
results until the repository's review process has examined it.

Continuation: [C5_EXTENSION.md](C5_EXTENSION.md) also handles epsilon=5
AA/BA drift and the BA bare tie, proposing the weaker residual H5/C7
(epsilon>=7) for J<T4. It too is unreviewed.

[SHIFT_TRANSPORT.md](SHIFT_TRANSPORT.md) gives a separate uniform
conditional reduction for arbitrary later A-initial c sources and
arbitrary common phase shifts, including interior outer chains.
It leaves the shifted safety of the earlier source explicit.

[FIRST_A_REDUCTION.md](FIRST_A_REDUCTION.md) reduces that shifted
safety obligation for eta in [-8,8] to an exact terminal-output
collision after the earlier real tail's first a return, without DH.

[TARGETED_PRECISION.md](TARGETED_PRECISION.md) constructs canonical-source
shifted tails (5,m,...) for every 5<=m<=256. These safely close by the
gateway family but require up to 258 bits in a strict HP-cylinder
certificate, ruling out a fixed three-extra-bit extrapolation.

[RATIONAL_MODE.md](RATIONAL_MODE.md) treats the large gateway output
as a low-height rational phase. Its corrected contraction includes the
denominator factor 3, proves the required size bound, and retains
HR5 and the uncertified landing classes as explicit open conditions.

[SECOND_GATEWAY.md](SECOND_GATEWAY.md) audits the next precision bit
and certifies the 46/9 and 62/9 emissions for 5<=m<16384. It closes
the stated a->5 branches from rational parents up to 2^8190, while
retaining the other predecessor and higher-scale obligations.

[ODD_DENOMINATOR.md](ODD_DENOMINATOR.md) gives a single contraction
and gateway formulation for all reduced odd denominators, with an
explicit denominator-dependent threshold. It retains the high-deficit
c condition, landing certification, and repeated-gateway budget as open.

[ORBIT_SHIFT_OBSTRUCTION.md](ORBIT_SHIFT_OBSTRUCTION.md) exhibits a
canonical source for which some bounded-height orbit shifts exhaust
the strict precision. It rules out safety uniform in all denominator
depths and identifies source/depth correlation as a necessary remaining
ingredient; it is not a joint-reachability or halting counterexample.

[BOUNDED_ORBIT.md](BOUNDED_ORBIT.md) is the user-requested stopping
checkpoint: every exponent 0<=r<=10^30 at that fixed parameter-49
source is covered by 198 disjoint HP certificates, replayed through
an independent full-pair implementation. Global obligations remain open.

Resumed after the user's explicit continuation.
[GATEWAY_TRAIN.md](GATEWAY_TRAIN.md) derives an exact three-catapult
clock condition, excludes three identical consecutive catapults at
all parameters, and bounds trains inside a suitable parameter band.
Its finite necessary-condition graph remains cyclic, so shared-clock
correlation and inter-scale transitions are not yet closed.

[CLOCK_FILTERED_TRAIN.md](CLOCK_FILTERED_TRAIN.md) adds the mandatory
five-entry clock residue and exact valuation cancellation. It proves
that four consecutive all-a catapults cannot all lie in [5,16381],
and gives the analogous general-band result. Interruptions and
inter-scale re-entry remain open.

[TRAIN_CLOCK_ORBIT.md](TRAIN_CLOCK_ORBIT.md) derives the forced
source-clock orbit modulo 2^(L-5), its period 2^(L-7), and the exact
next-bit change after a full period. It excludes short source revisits
and certain periodic trains, while leaving interruptions and escape open.

[CROSS_SCALE_TRAIN.md](CROSS_SCALE_TRAIN.md) gives an exact four-catapult
local trace using canonical calls, replayed independently. It proves
that the small-interval cap cannot be promoted to all scales; the
constructed initial state is not claimed reachable in the original orbit.

[DEPTH_CLOCK_BUDGET.md](DEPTH_CLOCK_BUDGET.md) couples the c_r depth
to its canonical source clock at the correct per-pair precision,
and proves a conditional record-plus-denominator budget decrease for
large paired a->5 gateways. Initial and inherited budgets remain open.

[SEED_BUDGET.md](SEED_BUDGET.md) supplies the initial denominator
reserve for the specified large integer a/b and epsilon-3/5 c
bare-tie seeds. It connects those entries to the paired-gateway
potential; inherited and other-entry budgets remain unresolved.

[COPY_BUDGET.md](COPY_BUDGET.md) shows how a certified earlier-source
reserve pays for inherited rank through any b/c copy, including high
deficits. Establishing suitable earlier certificates and phase-height
control remains part of the unclosed induction.

[JOINT_HEIGHT_BUDGET.md](JOINT_HEIGHT_BUDGET.md) adds a nonnegative
integer phase-height charge to the rank/record reserve. Certified
copies and large paired gateways decrease the combined quantity;
the specified integer seeds initialize it. Small gateways and full
induction closure are still open.

[STOP_CHECKPOINT_2026_10_21.md](STOP_CHECKPOINT_2026_10_21.md) is the
latest requested stopping node. Its small-gateway negative controls
show why the joint reserve alone cannot close the local rule; the
resume task is to retain and constrain the actual affine origin.

Resumed on the user's explicit instruction.
[AFFINE_REACHABLE_CATAPULTS.md](AFFINE_REACHABLE_CATAPULTS.md) retains
sparse affine origins, replays the accepted non-descent witness, and
uses the accepted finite-spectrum construction to propose actual
canonical five-to-m occurrences for every 5<=m<=18. Global beta
control remains open; the new reachability assembly is unreviewed.

[UNBOUNDED_C_PARAMETER_IF_EXT.md](UNBOUNDED_C_PARAMETER_IF_EXT.md)
proves conditionally that global strict EXT would force every m>=5
as a canonical c parameter already at deficit eleven. It rules out
a fixed all-scale CAL-C cap as a simultaneous route to global EXT,
without refuting phase-sensitive conditions or the non-halting goal.

[BBBAA_COPY_CERTIFICATE.md](BBBAA_COPY_CERTIFICATE.md) gives that
unbounded-parameter source family a rank-one, bounded-height phase
and a proved joint source budget. Its c-copy transition is controlled
without a parameter cap; other histories and subsequent tails remain open.

[B_PREFIX_SOURCE_ENCODING.md](B_PREFIX_SOURCE_ENCODING.md) gives a
joint source certificate for arbitrary reached B^tAA prefixes with
an intermediate five and root P>=512, including resonant small parts.
Its generic encoding can have a large denominator; mixed histories
and the subsequent tail remain unresolved.

[EARLY_MIXED_SOURCE_CERTIFICATES.md](EARLY_MIXED_SOURCE_CERTIFICATES.md)
removes the pure-b restriction for a bounded number of early a outputs,
using smaller-root EXT and the accepted C2-log bound. It supplies joint
source certificates through that prefix, not a bound on all later returns.

[OPTIMAL_PHASE_ENCODING.md](OPTIMAL_PHASE_ENCODING.md) provides an
exact minimum-cost local phase encoder and proves that reserve m
cannot encode every m-bit phase class in the joint-budget format.
It preserves the explicit lift bit but does not recover higher precision
or replace actual-origin constraints.

## 1. Inputs and notation

Use work_r1r2/NOTES.md for N0, B, L, Lambda, theta, the landing defect
delta modulo 2^(j+1), and the accepted window certificate. Use
work_ext_roots/PROOF_LOW_DEFICIT.md sections 1--3 for the weight grammar
and epsilon-three source formulas. In particular epsilon=3 means that
the source epoch has history A: its first odd return is type a.

Write P for that source epoch's fire parameter, rho for its pointer,
x0=2^P U for its lambda numerator (U positive odd), and
k=tau(P-1)/2. The source crossing is n=rho+2. Put z=6k+2.
The accepted SIZE/SMALL estimate gives q=v2(z)<P-1 at such a source.
This estimate is used on the reached canonical prefix, with the same
definedness/C1 hypotheses as the imported low-deficit argument.

## 2. Identity c3 (proposed all-parameter lemma)

At the epsilon-three crossing,

    lambda_Y = x0/2 - 1,
    lambda'_W = 3*x0/2 + z,
    omega(n) = q < P-1.

Proof: the initial real fire has head lambda 6*s0/2+1=x0-3.
The pending D created by its first odd update has lambda
(head_lambda+1)/2=x0/2-1. Its a-return leaves exactly D pending,
so this is lambda_Y at X(rho+2). The second identity is the accepted
low-deficit source formula; its summands have valuations P-1 and q,
which are different. This proves omega=q.

The generic c-step landing formula is

    delta' = theta - 1 - lambda_Y (mod 2^(q+1)).

Consequently

    delta' = theta - x0/2 = theta (mod 2^(q+1)),             (C3-ID)

because P-1 >= q+1. **The extra precision bit is retained.** This is
stronger than an identity merely modulo 2^q and is exactly the class
needed for the landing certificate. It applies to an interior c step
with arbitrary incoming small theta, not only to S(n+1)'s first step.

If q>=N0 and |theta| is in the small drift range used below, the
symmetric representative after the step is exactly theta. Thus this
c step may remain deep without disturbing drift. If q<N0, its class
is represented by the same integer theta. The accepted c-step ledger
still gives R_next <= R_current-1 and j_next<=L(j_current).

This does NOT prove CAL-C. It proves that forbidding all such c steps is unnecessary
for drift control. (Added in review: CAL-C at threshold N0 is in fact false, relative to
accepted EXT(<K_clock) only, by an epsilon-three source of this kind; and R1 fails at some
J in [K_clock,T4). See CONGRUENCE_TARGET_NOTE.md sections 1-2.)

## 3. Weaker conditional target below T4

Define H3(J): every odd c step reached in the initial deep segment
whose source deficit is not 3 has next parameter <N0. Thus all c steps
that remain above the threshold are required to have epsilon=3.
This is an explicit sufficient condition; it avoids the conflicting
uses of the name R1 in older notes (parameter threshold vs deepness).

(Review correction: H3 is NOT true for all J<T4. An epsilon-five BA source with omega>=N0 makes
H3(J) fail at some J in [K_clock,T4); see CONGRUENCE_TARGET_NOTE.md section 3. The theorem
below is a valid implication but not a viable route; it is superseded by C5_EXTENSION.md
section 4, whose hypothesis H5 is not affected by that construction.)

Define C_rest(J): if the landing is a c step with epsilon!=3, its
actual class is certified. For a stopped deep walk this condition is
vacuous. Neither H3 nor C_rest has been proved globally.

**Proposed reduction, using the accepted finite window/gateway certificates:**

    J<T4 and H3(J) and C_rest(J) imply EXT(J).

Proof follows, with Lambda=Lambda(J)<=4. Delete the c3 letters from
the initial deep word. If h a/b letters have occurred, its drift
satisfies

    theta = 2*i-h+1, 0<=i<=h; hence 1-h<=theta<=h+1.

Induction uses a:theta->3-theta, b:theta->theta-1, and (C3-ID).
All still-deep steps have small symmetric representatives. At an
a step, 3k>=3*(N0-2)/4, so |theta|<=5 cannot give resonance.
Therefore every continuing deep step decreases j to at most L(j).
There cannot be more than Lambda deep chains: otherwise induction
through Lambda transitions would put a deep j below N0 by the
definition of Lambda. This argument bounds the count while establishing
drift and does not assume the old R1 deep-chain count.

At the last deep chain T<=Lambda-1, h<=T, so theta is in [-2,4].
If the landing is c3, (C3-ID) puts its defect in [-2,4], excluding
both exceptional window representatives 5 and -11. The accepted
window certificate handles 5<=q<N0; q<=4 terminates by the small base.
Its entry record is strictly below J by the c ledger. If the landing
is another c step, use C_rest. If it is a or b, the old window proof
and two-step gateway apply unchanged: the drift bounds used there
still hold with h<=T (parity in T is not needed).

For completeness, the possible a/b bare tie in this range requires
incoming theta=-2; the other candidates 6,14,-10 are outside [-2,4].
It therefore requires h>=3 and T>=3. A gateway output m>=10^8
would require Lambda(j_T)>=2, by the accepted Corollary 2.6 estimate.
Since every prior deep step obeys j_next<=L(j),
Lambda(J)>=T+Lambda(j_T)>=5, a contradiction. Smaller gateway outputs
are covered by the accepted finite gateway certificates. This closes
all landing cases under the two stated hypotheses.

The argument is restricted to J<T4. In particular it does not eliminate
RES at higher scales or resolve the all-scale drift problem. It removes
epsilon=3 sources from BOTH the deep-c obstruction and the c-landing
certificate obligation in the stated range. The remaining c sources
have epsilon>=5 by the accepted weight grammar. Treating their classes
uniformly, rather than imposing a universal small omega bound, is the
next arithmetic target.

## 4. Canonical evidence against extrapolating omega<=5

Using Calendar(512), choose the actual parameter-P=51 fire at

    k=1876499844737706, rho=4206758904857514.

(Notation, review: here k is the half-time of the parameter-51 fire itself, at pointer rho,
so x0=6k+4=5*2^51; it is NOT section 1's k=tau(P-1)/2.)

Its first a-output is a genuine epsilon-three c crossing at

    n=4206758904857516,
    tau(n)=3752999689475455,
    lambda_Y=5629499534213119,
    omega(n)=7.

These are exact integer values, not a locally compatible fabricated
source. The navigation and epoch reconstruction run inside the
calendar's certified boundary; its implementation rejects out-of-range
queries and verifies the kernel duration, pointer advance, and mass.
The instance refutes extrapolating omega<=5 from the n<10^8 table.
It is NOT a counterexample to EXT or to the N0-threshold CAL-C.

Reproduction: python -B work_c3_drift/verify_c3.py

For the first selected canonical fire at each eligible 5<=P<=256:
76 epsilon-three sources, 4,636 phase-class comparisons, zero failures.
Observed omega values are 1,3,4,5,6,7,9; hence oddness of omega also
does not generalize from the previous table. Reachable drift states for
a/b/c3 words through length 13 obey the stated bound and h-parity.
This finite check supports the algebra but is not its general proof.
checks.json contains the exact larger-omega witnesses and scope.

## 5. Review and next work

Required review points: the pending-D identity and its extra precision
bit; the simultaneous drift/count induction with neutral c3 letters;
the gateway proof's use of h<=T rather than T-parity; reached-prefix
scope of SIZE/SMALL. No accepted document has been rewritten to claim
this result is reviewed. Remaining obligations H3 and C_rest, and
J>=T4, prevent any global non-halting conclusion.
