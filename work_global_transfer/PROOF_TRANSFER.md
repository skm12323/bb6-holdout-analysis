# Transport of a parameter-5 rescue across a/b/c origins

2026-10-16. Conditional research work, not independently reviewed.
Imports: exact exit maps and copy safety from `work_el/PROOF_EL.md`,
root weight bookkeeping from `work_global_root_phase`, and the
phase/safety result through weight 16 from `work_global_weight16`.
Earlier sources are defined and satisfy C1 wherever a time bound is
used. No future termination or all-weight bound is assumed.

The new general result identifies the precise valuation collision
which prevents a uniform rescue formula. Its first application closes
all departures from weight 16, giving safety and phase inclusion
through weight 18. Its limitation is substantive: copying an already
rescued source requires a more general joint certificate.

## 1. A uniform normalizer with a precise collision condition

Use x,Theta,j,sigma as in the weight-16 note. All rational constants
below have odd denominators. Suppose an actual odd return produces
parameter 5 with representative eta, and perform the following odd
A return at 5 (half-time 1). There are three cases.

### A origin

Let the preceding parent have parameter p>=7, phase alpha, and
half-time k. Write

    x=2^p U, Theta=2^p z+alpha, U odd.

Since its output is 5<p, this first A satisfies NT, so eta=3-alpha
is an available representative. Two A returns give

    x_out=2^p z+2^(p-2)U+K_A,
    K_A=alpha+9k+12,
    3Theta_out-2x_out=15-eta modulo 2^(p-1).

The nonconstant part of x_out has valuation exactly L=p-2. If
v2(K_A)!=L, with v2(0)=infinity, then

    q=v2(x_out)=min(v2(K_A),L)<=L.

The input margin sigma>p loses two units, so sigma_out>=p-1>q.
The joint congruence implies the output phase

    f(eta)=5-eta/3.                                      (F)

### B origin

Let the B parent have parameter Q and phase beta; it copies a fire
with parameter 5 and lambda numerator A=32v, v odd and positive.
Then eta=beta-1. Writing the parent as x=2^Q u,
Theta=2^Q z+beta, the B and following A give

    x_out=2^(Q-3)(16z-3u)+K_B,
    K_B=(3/2)A+2beta+4,
    3Theta_out-2x_out=15-eta modulo 2^(Q-2).

Here the high part has exact valuation L=Q-3. If v2(K_B)!=L,
then q=min(v2(K_B),L)<=L. The two returns lose three coefficient
units, so sigma_out>=Q-2>q, and (F) follows again.

### C origin with a normal source A

The copied source is itself an A output with parameter 5. Suppose
its preceding parameter is p>=7, its phase is alpha, its half-time
is k, and its coefficient valuation before that source A is
sigma_pre>p. Write that source parent as

    x=2^p U, Theta=2^p z+alpha.

Let Q and beta be the outer C parent's parameter and phase. At the
source output its chain coefficient c_s has valuation

    S=sigma_pre-1>=p.

If its crossing deficit is epsilon_s, then Q=S+epsilon_s+1>S.
The exact copy has time shift

    D=Theta_outer-2=2^Q w+beta-2.

Writing the source output as x_s,Theta_s and the outer odd base as u_o,
the copied state is x_s+c_s u_o, Theta_s+D. Its phase representative
is eta=beta+1-alpha. After the parameter-5 A,

    x_out=2^p z+2^(p-2)U+2^(Q+1)w-c_s u_o/2+K_C,
    K_C=alpha+2beta+9k+8,
    3Theta_out-2x_out=15-eta modulo 2^(p-1).

The high part again has exact valuation L=p-2: all but the term
2^(p-2)U are divisible by 2^(p-1), using S>=p. Thus if
v2(K_C)!=L, q=min(v2(K_C),L)<=L. The outer C loss is
1+epsilon_s=Q-S. Including the following A,

    sigma_out=sigma_outer-(Q-S)-1>=S>=p>q.

This proves safety and (F), regardless of the source weight and of
how many earlier returns preceded its normal A.

### Scope of the rule

All three cases are all-parameter algebraic implications. They do not
assert that an arbitrary phase assignment occurs canonically. When
K=N/D with odd D, the convenient sufficient test

    0<|N|<2^L                                        (SEP)

excludes the sole collision v2(K)=L. The case K=0 is also safe, since
then q=L. At the collision no valuation or safety conclusion follows
from this lemma alone; the retained high coefficient can matter.

For C, the condition p>=7 is essential. A source A from parameter 5
can itself be a non-NT rescue. Section 4 treats that distinction.

## 2. Exhaustive application at the weight-16 boundary

The phase sets already proved through weight 16 have |numerator|<=46,
denominator<=9, and minimum representative -7. The same analytic
estimate as in the weight-16 proof excludes NT failures at j>=64:

    0<theta+3k<2^(j-2).

More precisely, with theta=N/D (D odd) the same inequality gives
0<N+3kD<2^(j-2), hence v2(N+3kD)<j-2, which is what excludes the NT
congruence when D>1.

The exact small table leaves only parameter 5 with

    eta in {5,-1/3,-19/9}.

The full source-sensitive grammar has 20 origins of these exceptions:
3 A origins, 2 B origins, and 15 C origins. They compress as follows.

| Origin | eta | Parent/source phases |
|---|---|---|
| A | 5, -1/3, -19/9 | alpha=-2, 10/3, 46/9 respectively |
| B | 5, -1/3 | beta=6, 2/3 respectively |
| C | 5 | alpha is an integer in [-4,2], beta=alpha+4 |
| C | -1/3 | (alpha,beta)=(1,-1/3),(10/3,2),(7/3,1) |
| C | -19/9 | none |

The C rows include different source/outer weight decompositions. They
are all retained explicitly in `checks.json`. In particular none uses
the exceptional source representative 10/3 or 46/9: each source phase
here really arises from the normal rule 3-alpha, rather than silently
substituting that rule for a rescued source.

Finite low-parameter exclusions using the actual source table show:

- A origins require p>=17.
- C origins with integer alpha require p>=14.
- C origins with nonintegral alpha require p>=17.
- B copies of a parameter-5 fire require Q>=65.

These are exclusions only up to the stated thresholds, not assumed
formulas for the infinite source clock. In particular, no eligible C
source has preceding parameter 5 or 6 here.

For A, the constants K_A have numerators 9k+10, 27k+46, 81k+154
over denominators 1,3,9. C1 and p>=17 give the uniform bound

    0<N <=(81/2)(p-1)^2+154 <2^(p-2).

For C with eta=5, K_C=9k+3alpha+16 has positive numerator at most
9k+22; its bound is valid already at p=14. For the three eta=-1/3
cases the numerators are, respectively,

    27k+25, 27k+46, 27k+37.

The first is bounded by (27/2)(p-1)^2+25<2^(p-2) at p>=14;
the others are covered by the p>=17 estimate above.

For B, A=3tau(Q-2)+4<=3(Q-2)^2+4. After multiplying K_B by its
odd denominator, both cases have positive numerator bounded by

    (27/2)(Q-2)^2+66 <2^(Q-3), Q>=65.

Every displayed inequality holds at its lower endpoint. Dividing its
positive quadratic left side at p+1 (or Q+1) by its value at p (or Q)
gives a factor less than two thereafter, whereas the right side
doubles. Thus these are analytic infinite-range bounds.

SEP holds for all 20 origins, so their output phases are

    10/3, 46/9, 154/27.

## 3. Resulting conditional theorem

Under the root and earlier-source hypotheses of the weight-16 note,
all continued returns with resulting weight at most 18 are safe.
The weight-18 representative set is

    {-8,-6,-4,-10/3,-28/9,-2,-4/3,-10/9,-2/3,0,
      2/3,4/3,2,8/3,28/9,10/3,4,46/9,16/3,154/27,6,8,10}.

Proof: A inputs have weight <=16. Ordinary NT cases preserve margin;
section 2 handles all remaining ones. B/C outputs are safe by copying
earlier safe sources and use the already known phase sets. Their
source weights are lower than the resulting weight, so the weighted
induction is not circular. This proves neither termination before
weight 18 nor safety at arbitrary later weights.

## 4. The more general joint transport needed beyond this lemma

Suppose a source at parameter 5 carries a joint certificate

    a Theta_s - b x_s = L modulo 2^R,

where a is odd, b is even, and its coefficient valuation satisfies
S+v2(b)>=R (S>=R is a convenient stronger sufficient condition).
Copy it with coefficient c_s and time shift D. The copied variables
are y=x_s+c_s u and T=Theta_s+D, so

    aT-by=L+aD modulo 2^R.

For the following A at parameter 5, y'=2T-y/2+6 and T'=T+9.
Substitution, with no NT assumption, gives the exact transfer

    (a-4b)T'+2b y'=L+aD+9a-24b modulo 2^R.       (JOINT)

This formula remains valid after a source resonance. The new odd
coefficient a-4b need not be a power of 3. If the output valuation
q<R is separately established, it gives a phase by division by
a-4b. It does not itself prove q<R or supply a size bound on D.

For example, starting with 3Theta_s-2x_s=10, the copied A yields

    5T'-4y'=11-3D modulo 2^R.

If D=5/3 modulo 2^R, the new phase is 6/5 when q<R. This differs
from the naive f(5)=10/3 by 32/15, so they cease to be interchangeable
once the output parameter exceeds 5.

The verifier constructs an integer local witness with actual source
half-time k(233)=102 and source parent p=234, phase -2. Its two-A
source output is parameter 5, carrying joint constant 10. Copying it
with D=5/3 modulo 2^Q and then applying A produces parameter 6 with
phase 6/5, and fails the proposed phase 10/3 modulo 64. All checks
use exact integers/rationals; the clock value comes from the canonical
finite source table.

The outer copy is a local algebraic lift. Its canonical reachability,
and a complete canonical history for the phase -2 parent, are NOT
asserted. This is not a counterexample to the global conjecture or
to section 1, whose normal-source hypothesis is absent. It shows that
source clock data and a post-rescue phase alone do not justify blindly
reusing (F) for every later copy. To exclude such lifts canonically,
one would need an additional reachability theorem.

### An all-depth coefficient invariant

JOINT is not restricted to powers of 3 or to a finite catalogue of
phases. Starting from (a_0,b_0)=(3,2), negate the displayed output
relation to keep b positive. Repeating a copy followed by A gives

    a_(r+1)=4b_r-a_r, b_(r+1)=2b_r,
    b_r=2^(r+1), a_r=(2^(r+3)+(-1)^r)/3.

In particular a_r is always positive odd. For a general A half-time
k_r, the constant update, derived from the same exact exit map, is

    L_(r+1)=(12k_r+12)b_r-(6k_r+3)a_r-L_r-a_r D_r.

The modulus 2^R is unchanged by the A substitution; it is not divided
by two. A copy's error is -b_r c_s u, which vanishes modulo 2^R
provided only

    S+r+1>=R.                                      (PREC)

Thus a decreasing source coefficient valuation does not by itself
force this joint certificate to lose a bit per A: the growing power
of two in b_r compensates. This is an exact all-depth algebraic
invariant for any compatible sequence of such transports, not a
claim that every formal sequence is a canonical itinerary.

It sharpens the next proof target. Even with R fixed and PREC true,
concluding a phase still requires output q<R, and neither this
invariant nor positivity of a_r bounds the accumulated constant L_r
or time shifts D_r. In particular it is not an all-depth safety proof.

## 5. Verification and remaining proof target

Run `python -B work_global_transfer/verify_transfer.py`.
The script checks 459 exact transport identities, 128 iterated joint
identities at the limiting precision S=R-r-1, all 20 boundary
origins, bounded low-parameter exclusions, inequality bases and a
finite sample of their monotone tails, the weight-18 phase set, and
the rescued-source witness. Formal identity samples are not counted
as canonical paths.

The all-weight problem is now more specific: propagate a joint
certificate together with its precision R, and bound either the
frequency of valuation collisions or the cumulative loss of R.
Equation JOINT provides a closed algebraic update, but does not
establish that its precision outlasts the epoch. A uniform stopping
or loss argument remains missing. The new finite extension and the
general transfer rule therefore leave global G2/non-halting open.
