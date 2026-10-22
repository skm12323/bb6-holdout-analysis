# Epsilon-five steps and a weaker residual at epsilon >= 7

2026-10-20. **UNREVIEWED proposed proof.** Extends NOTES.md. All imported
defined-prefix, C1/CLOCK and window/gateway-certificate hypotheses remain.
No global EXT claim and no change to K_clock.

## 1. Extra-bit class identities for AA and BA

At a c source the landing defect satisfies

    delta' = theta - 1 - lambda_Y  (mod 2^(q+1)), q=omega(n).

The accepted weight grammar says epsilon=5 has exactly histories AA, BA.
Here P is the source epoch's root parameter, x0=2^P U, and rho its pointer.

**AA.** Put k=tau(P-1)/2, p=v2(6k+2)<P-1 and l=tau(p-1)/2.
The accepted AA formulas in PROOF_A_SOURCE_DESCENT section 1 give

    x_C = 5*x0/4+9k+6l+7,
    3*tau(n)+4 = x0+6k+6l+6,
    lambda_Y = x_C-(3*tau(n)+4) = x0/4+3k+1.

At the actual fire X(p-1), y=6l+4 has q=v2(y)<p-1 by its real S1
margin. The difference x_C-y has valuation p-1 (the two summands have
valuations P-2 and p-1, with P-2>=p). Thus omega(n)=q. Also
v2(lambda_Y)=p-1, so lambda_Y=0 mod 2^(q+1). Therefore

    AA: delta' = theta-1 (mod 2^(q+1)).

This uses the real source fire's S1, not EXT at an arbitrary new index.

**BA.** Put y=3*tau(P-1)+4=2^p V, p<P-2, and k=tau(p-1)/2.
The accepted BA formulas in PROOF_LOW_DEFICIT section 4 give

    x_C = 13*x0/8+3*y/2+6k,
    3*tau(n)+4 = x0+y+2+6k,
    lambda_Y = 5*x0/8+y/2-2.

Their SIZE/SMALL estimate gives q=v2(6k)<p-1, and omega(n)=q.
The error 5*x0/8+y/2 has valuation p-1, because P>=p+3.
It vanishes modulo 2^(q+1), so

    BA: delta' = theta+1 (mod 2^(q+1)).

Together with the c3 identity, the permitted c steps act on small drift
as 0, -1, +1. Each identity retains the extra bit needed at a landing.
When q>=N0, a bounded input gives the exact small symmetric output.

## 2. The one new bare-tie case

The four maps a:3-theta, b:theta-1, c3:theta,
cAA:theta-1, cBA:theta+1 preserve

    1-t <= theta_t <= t+1.

At Lambda<=4 the last deep chain has T<=3 and theta_T in [-2,4].
The small c landings have classes in [-3,5]. The only exceptional
window class possible is (q,delta')=(5,5), and it must be a BA
landing with theta_T=4. Reaching theta=4 needs T>=3.

We now resolve that case rather than adding a new open hypothesis.
At the outer deep chain j=n+1, write its exact phase as
Theta_outer=x_outer+theta+E, where E is divisible by 2^j.
The c update has x_u=c'_W*u_outer+x_C and
Theta_u=Theta_outer+3+3*tau(n). At a BA source, sigma=v2(c'_W)=rho-3,
P<rho and p<=P-3. At theta=4 these formulas give

    x_u = 6k                 (mod 2^(p-1)),
    Theta_u = 6k+5           (mod 2^(p-1)).

Indeed the x error is c'_W*u_outer+13*x0/8+3*y/2, all divisible
by 2^(p-1). The phase error is x_outer+E+x0+y, all divisible by
2^p. This establishes the comparison for an arbitrary interior
outer chain, not merely for the first chain of S(n+1).

Since q=5, k=16v with v odd. The next call is X(4), whose k is 1.
The reference (6k,6k+5) takes one exact a step to

    x2=9k+16, Theta2=6k+14, m=v2(9k+16)>=5.

We need m<p-2 to preserve the extra bit after this step. For p>=15,
C1 gives k<= (p-1)^2/2 and

    9k+16 <= (9/2)*(p-1)^2+16 < 2^(p-2).

The inequality holds at p=15 and persists since the quadratic's
successive ratio is below 2. The odd-a cases 5<=p<15 are
(p,k)=(5,1),(8,2),(12,4),(14,5), none with v2(6k)=5.
Thus m<p-2 in every BA bare-tie case. The first-step x error has
valuation at least p-2, so the actual next parameter is m and the
next defect is known modulo 2^(m+1). Its class is

    3*(Theta2-x2) = -9k-6 = 10-(9k+16),
    delta2 = (10-2^m)/3 (mod 2^(m+1)).

This is exactly the first accepted gateway family of work_r1r2.
There is no free higher-bit choice: m<p-2 supplies the needed bit.

The records also remain safe. The first c step drops the record by
sigma-q. The next a step changes it by m-q+1, so the two-step record
is R_T-sigma+m+1<R_T, since sigma=rho-3>p-2>m.

## 3. Why its certificate is in range when Lambda<=4

The drift bound forces T>=3 for theta_T=4. Every preceding deep step
contracts by L, so Lambda(J)<=4 implies Lambda(j_T)<=1 and
L(j_T)<N0. The BA source root numerator x0=3*s0+4 obeys
s0<=tau(n), n=j_T-1. Hence

    P <= floor(log2(x0))
      <= floor(log2(6*tau(n)+5)) <= L(j_T) < N0.

In particular p<P<N0=20,000,000. C1 now gives

    9k+16 <= (9/2)*(p-1)^2+16 < 2^51.

Thus 5<=m<=50, well within the accepted gateway certificate range
5<=m<10^8. The actual next defect class is certified, and its entry
record is below J. This closes the BA bare tie under the stated
Lambda bound without assuming a new infinite certificate.

## 4. Conditional reduction with epsilon>=7 residual

Define H5(J): every odd c step of the initial deep segment with
epsilon>=7 has next parameter <N0. Define C7(J): if the landing is
a c step with epsilon>=7, its actual class is certified. Conditions
on a landing are vacuous if the walk ends in the deep segment.

(Review note: the shallow epsilon-three and epsilon-five constructions of
CONGRUENCE_TARGET_NOTE.md refute R1 and H3 at some J in [K_clock,T4) but do not touch H5,
and the BBBAA construction lands at n+1>=T4. It is conjectured [C], not proved, that
epsilon>=7 and omega(n)>=N0 force n>=T4-1; this would make H5 automatic for J<T4, leaving C7.)

**Proposed theorem:** for J<T4,

    H5(J) and C7(J) imply EXT(J).

Proof: simultaneously induct on the first at most Lambda deep steps.
All c steps remaining deep have epsilon 3 or 5 by H5, so section 1
and the a/b maps give 1-t<=theta_t<=t+1. The large positive 3k at
a deep a step prevents resonance for t<=4. Every continuing deep
step therefore contracts by L, which forces an endpoint or landing
within Lambda<=4 deep chains. This establishes the count without
using R1. Records strictly decrease at all these transitions.

For the landing: an even return ends; c3 and cAA have certified
window classes; cBA has a certified class except the case resolved
in sections 2--3; c with epsilon>=7 uses C7. For a/b landings use
the old gateway proof as in NOTES.md section 3. Its drift bounds
and T>=3 implication remain valid with the new maps; it does not
require alternating T-parity. That covers all cases.

Compared with NOTES.md, this removes epsilon=5 as well as epsilon=3
from the two residual conditions. It does not prove H5 or C7. It
does not address J>=T4, and hence is not a global non-halting proof.
The accepted general-source defect calculus explains why continuing
deficit-by-deficit is not itself a global strategy: larger histories
introduce unbounded phase shifts. The new low-deficit cases establish
how the history's phase, rather than the copied parameter's size,
can be used in a uniform future argument.

## 5. Checks and review scope

python -B work_c3_drift/verify_c5.py

Calendar(512), first chosen fires for P<=256: four AA and four BA
sources; 488 exact class identities. Separately, 6,000 algebraic
gateway/precision checks (explicitly noncanonical test states),
the small odd-a cases, and drift states through T=3 pass.
These verify identities, not H5/C7 and not all canonical histories.

Review must check: the real-fire S1 use in AA; the phase comparison
at an interior BA outer step; extra-bit survival through the gateway;
the p<N0 implication at T>=3; and the defined-prefix scope of C1.
