# Affine origins force selected catapults in actual canonical epochs

2026-10-21. **UNREVIEWED proposed extension relative to accepted imports.**
The construction supplies actual reachability by finite-spectrum
existence, not by simulating the enormous lifted fires. It does not
enlarge the non-halting horizon or prove global EXT.

## 1. Preserve the affine origin

Use x=alpha*X0+beta and Theta=X0+theta_beta, X0=2^J*U.
The accepted rules give, for a b copy with real source numerator L,

    alpha'=(3/4)*alpha, beta'=(3/4)*beta+L,
    theta_beta'=theta_beta+L-1, loss increment 2;

and for an a call of half-time k,

    alpha'=2-alpha/2,
    beta'=2*theta_beta+6k-beta/2,
    theta_beta'=theta_beta+6k+3, loss increment 1.

affine_origin.py retains sparse dyadic coefficients and separate
source symbols. It certifies a valuation only when one exact term
has strictly lower valuation than every other term's lower bound.
Equal minima or an inexact leading valuation remain unresolved.
It never treats absent cancellation evidence as a proof.

The replay of the accepted p3,p2,p1,17,5,6,1 witness gives

    beta_5=(55/32)*L2+(13/8)*L1+983072,
    beta_6=(73/64)*L2+(19/16)*L1+819264.

The constant 819264 has valuation exactly 6; all other terms and
the root coefficient have strictly larger valuations. Thus this
actual five state is forced to 6. The arbitrary large jumps allowed
by the minimal (5,5) class are not allowed at this particular origin.

## 2. Canonical sources for m=5..18

For each m in this range, the targeted calendar search finds a real
fire of half-time k with v2(9k+10)=m. Let its pointer be p-1.
Then X(p-1) is actual odd a with half-time k. The selected pairs are
recorded in reachable_catapults_checks.json and satisfy

    m+4<=p<=359137<400000.

These are the same genuine call sources used in TARGETED_PRECISION.
That note used a counterfactual shift of a real root. Here we supply
the shift through three actual b copies.

## 3. Three actual b ancestors inside the accepted horizon

The accepted PROOF_SPECTRUM section 3 proves occurrence of every
fire parameter P with P+4<B. Its extension to P+4<K' is explicitly
stated in work_global_egx/PROOF_EGX.md after Lemma TR, using the
accepted TIE2 bound of at most seven exits below K'. For completeness,
the corresponding half-time gap is at most 4*(P-1)^2+5, bounded
by 2^(P-2) for P>=16; the audited small gaps handle P<=15. The
same no-overshoot barrier reaches T_P within the certified horizon.

Start with p0=p. Choose an actual fire of parameter p0 at its
spectrum time T_(p0), let its pointer be rho0, and set p1=rho0+2.
Repeat to obtain p2=rho1+2, p3=rho2+2, then choose the actual
parameter-p3 fire. The crossing X(p_(i+1)-1) is the b crossing
at the preceding parameter-p_i fire. Therefore the p3 exit begins

    p3 -> p2 -> p1 -> p,

with three b returns. The source parameters are strictly earlier:
p_(i+1)>=p_i+3, by S1 and the pointer definition. This is the same
canonical ancestry construction as the accepted WITNESS proof.

All applications are inside the finite spectrum range. The accepted
pointer bound p_(i+1)<2^(p_i+3) gives, conservatively,

    p3+4 < 2^(2^(2^(p+6))) < K',
    K'=2^(2^(2^499997-3)-2),

since p<=400000. The smaller ancestors satisfy the same slack.
No extrapolation of fire existence beyond the accepted horizon is used.

## 4. Forced gateway and strict margins

Let L0,L1,L2 denote the actual fire numerators at p,p1,p2, respectively.
Their valuations are p,p1,p2. After the three b copies,

    beta_p=(9/16)*L2+(3/4)*L1+L0,
    theta_beta_p=L2+L1+L0-2, Gamma=6.

The next two a calls (half-times k and 1) yield

    beta_5=(55/32)*L2+(13/8)*L1+(3/2)*L0+6k-4,
    beta_m=(73/64)*L2+(19/16)*L1+(5/4)*L0+9k+10.

From v2(9k+10)=m>=5, one gets v2(6k-4)=5. Since p>=m+4,
p1>=p+3, and p2>=p1+3, all source-symbol terms lie strictly above
the required valuations. Thus the next two parameters are exactly
5 and m for every actual odd root base, without choosing its high bits.

At the m chain, 3D=-9k mod 2^(m+1), so its class is
(10-2^m)/3. The accepted finite gateway certificate covers m<=18;
the checker also executes these small representative tails directly.

The first three records are p2+2, p1+4, p+6, all below p3. At the
five state the loss is 7, and at m it is 8. The whole remaining
tail has record at most m+8<p+9<=p3. Hence no uniform-coefficient
margin is crossed in this derivation.

Consequently, relative to the accepted imports, actual canonical
epochs contain the indicated five-to-m gateways for every 5<=m<=18.
For example m=18 has terminal portion p=65298,5,18,3. The formerly
known m=6 case is recovered at p=17. These are safe non-descents,
not halting witnesses or a global termination proof.

## 5. Checks and remaining global question

    python -B work_c3_drift/verify_affine_origin.py
    python -B work_c3_drift/verify_reachable_catapults.py

The first performs sparse-origin replay, 54 exact Fraction substitution
checks, and a deliberately ambiguous valuation control. The second
checks all 14 canonical call sources, the affine valuation separation,
the emitted precision bit and finite suffix certificates. The huge
ancestor pointers and fires are specified by the proof, not generated
numerically.

This establishes useful genuine-origin fixtures for further filtering.
The missing all-scale step is still to bound the next beta valuation
for arbitrary reachable prefixes, including mixed b/c ancestry and
repeated small gateways. The new code is a checker of supplied affine
origins, not a solver for that universal condition. Independent proof
review is pending; accepted checkpoints remain unchanged.
