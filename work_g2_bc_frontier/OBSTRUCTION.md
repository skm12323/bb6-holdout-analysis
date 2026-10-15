# An actual-source b/a resonance surviving the retained local constraints

2026-10-15. Research stopping-point evidence, not independently reviewed.
The constructed outer prefixes are compatible local F states. They are
not claimed to be reachable on the distinguished orbit, nonterminating,
or counterexamples to any accepted finite-horizon theorem.

## 1. Why the ordinary finite scan does not settle this branch

`scan.py 100000` streams the actual crossing table and checks both R21
and E affine families at every odd b/c entry q>=1024 in that range.
All 63094 tested families close: 31547 R and 31547 E, with at most four
chains. The scan retains all failures and found none in this range.

That result does not provide a general b/c theorem. A copied fire can
have a large parameter p only at a source time at least roughly 2^p;
scanning moderate parent indices therefore never sees many of the
large-p source types relevant to a global proof.

The following construction supplies a concrete example of that gap.

## 2. A verified earlier crossing, and a certified actual source fire

The exact canonical crossing table has

    p=24480;
    X(p-1) odd type a;
    tau(p-1)=21832, k_p=10916;
    40+6k_p=65536.                                (CLOCK)

`verify_resonant_source.py` verifies CLOCK directly on the full pair
walk, without loading a large table of giant coefficients.

The accepted finite-spectrum barrier in
`work_g2_obstruction/PROOF_SPECTRUM.md`, section 3, guarantees an actual
fire of this even parameter p at

    s_p=(2^p-4)/3, A=3s_p+4=2^p.

Indeed p+4<B for its accepted cutoff B, so that finite theorem applies.
Let rho_p be that fire's actual pointer, and Q=rho_p+2. By the crossing
type-b rule, X(Q-1) is the b crossing that copies this source fire.
S1 at the source gives Q>=p+3. C1 at the same actual earlier prefix
is inherited from the accepted finite result. Q is defined by this
real source; it is not freely assigned a convenient numerical value.

Thus the upcoming b and a crossing records can both be actual records,
even though the outer R21 state using them is not known reachable.

## 3. Exact resonant b/a output from R21

At a compatible R21 state with chain value X=2^Q w and old odd base v,
the b return copying the above fire gives

    x_p=3X/4+A, Theta_p=X/2+2^15 v+A+20.

Because Q>=p+3, v2(x_p)=p. Its known odd a-return from CLOCK gives

    Y=5X/8+65536(v+1)+3A/2.                     (BA)

The coefficient loss across these two returns is three. The resulting
joint state is

    Theta_Y-Y/2=3X/16+A/4+32751.                (NEW)

NEW retains the actual source mass A and the old X; replacing it by a
fresh free phase would lose information. Its low phase at a sufficiently
high output is 32751 mod 65536. (The comparison with "four previously
classified small-core escape phases" is not checked against the cited
dependencies; it is a research remark, not part of the obstruction.)

## 4. Arbitrarily high outputs survive the original local band

Fix the actual Q from section 2. For any odd integer R>=Q+8, let w be
the largest odd integer <=(9/10)*2^(R-Q), and define

    Y=2^R, X=2^Q w;
    v=(Y-5X/8-3A/2)/65536-1;
    u=X/16-4096v-3.                              (WIT)

Since Q>=p+3 and p=24480, v is an integer and odd: the numerator before
division by 65536 is divisible by 2^17. Also v>0. X has valuation Q.
Formula BA holds identically, so the b/a output has parameter R,
which can be arbitrarily large while the two referenced source records
remain fixed.

Importantly these states can retain the earlier local prefix (5,17).
Use its exact first-chain phase and lambda components

    Theta0=X/2+2^15 v-27;
    lambda_A0=196608v-X+37;
    lambda_b0=3X/2-163840v-68.

The choice of w gives (7/8)Y<X<=(9/10)Y. Substituting it into WIT,
using A<=2^(Q-3) and w=X/2^Q>=11 (automatic for R>=Q+8), gives the
convenient bounds

    (15/32)X <65536v<(17/32)X.                   (RATIO)

For the lower bound, Y-5X/8>=(35/72)X and the subtraction 3A/2+65536
is less than (5/288)X; for the upper bound use Y<(8/7)X. These estimates
are already more than sufficient for the present Q. RATIO proves both
lambda components positive and u>0. Thus the original BAND holds,
not just relaxed R21 positivity. The first chain has lambda_x=32u,
with u odd; its two a returns have parameters 17 and Q exactly.

The first parameter-5 entry can itself be made a genuine local odd
a-return, as required by the mixed-block model. Prepend a parameter-17
chain with

    X_prev=393216v-2X, Theta_prev=Theta0-39;
    lambda_Aprev=3X-327680v-137;
    lambda_bprev=360448v-5X/2+67.

RATIO makes both components positive, and v2(X_prev)=17. Its actual
small a record has k17=6 and yields the displayed parameter-5 state.
This supplies a valid local predecessor, not a proof of canonical
orbit reachability.

Since R is odd, Y=2 mod 3. WIT then implies Theta0=2 mod 3, so its
time s0=(Theta0-5)/3 is integral. These are compatible local states.

The following coefficient data are a **local assumption** of the
construction (asserted, not derived from an a-return coefficient update
in this note). Choose the parameter-5 coefficient scale sigma0=s0, with head
coefficient 3*2^sigma0, list coefficient 5*2^sigma0, and pointer
i0=sigma0+3. The prepended parameter-17 state has head and list
coefficients both 2^(sigma0+1), and pointer sigma0+2; its return
produces precisely these parameter-5 coefficients.
The coefficients need not be materialized computationally to define
the state. Their mass identity is exact, i0<=2s0, and the five total
coefficient bits lost along 5,17,Q,p leave sigma0-5>R. The known replay
prefixes are available from the accepted finite source records.
The elementary time bound s_final<sigma0^2 also holds. Hence the
arbitrary-height construction is not eliminated merely by adding these
local coefficient, pointer-speed and quadratic-time envelopes.

The full local parameter prefix is therefore

    17,5,17,Q,24480,R,

with return types a,a,a,b,a as derived above. This is a local replay
construction, not an actual canonical-orbit witness.

## 5. What this obstruction proves, and what it does not

**Scope (added after review).** By M2' at the source fire,
rho_p>=sqrt((2^24480-4)/3)>2^12239, so Q>2^12239 (far beyond Q>=p+3).
By the accepted PROOF_RESCUE section 4 (for H<=J<K an epoch reaches COVER
within two exit chains, later parameters <N) and Theorem D (strict
descent for J<H, which excludes 5->17), no epoch with J<B contains the
prefix 17,5,17,Q,24480,R. The obstruction therefore concerns only J>=B.
It shows that the listed local envelopes are insufficient; it does not
show that the tower-extended (j,theta)/COVER phase tracking fails, and
it conflicts with no accepted result.

It proves that actual earlier source data, the original retained v,
the (5,17) mass/positivity band, and elementary finite-height envelopes
do not by themselves bound the next rebound parameter in this branch.
The high b/c difficulty cannot be dismissed as a purely synthetic
source table or an artifact of resetting v to an unrelated variable.

It does not prove that these outer prefixes occur on the canonical
orbit, or that their tails fail to terminate. A stronger reachability
invariant could exclude them; alternatively, a larger correlated
boundary-return theorem could prove that even these states terminate.
Neither result has been established in the current research.

This is a substantive stopping point for the current autonomous route:
ordinary scan extension misses this source type, while another residue
split would introduce NEW without a proved decreasing quantity or a
closed state family. A new cross-boundary invariant or termination
mechanism is needed to claim further global closure.

## 6. Reproduction and finite-check scope

    python -B work_g2_bc_frontier/scan.py 100000
    python -B work_g2_bc_frontier/verify_resonant_source.py

The second script verifies CLOCK and nine formal WIT instances with
manageable Q values. Those numerical Q values are not asserted to be
the actual parent pointer or to satisfy all source-history conditions.
Their purpose is checking the algebra. Sections 2--4 specify the
actual-source symbolic construction and justify its scope separately.
