# A retained-root precision budget for arbitrary a/b/c return paths

2026-10-16. New conditional result, not independently reviewed. This
extends the special parameter-5 ladder to all return types. It proves
a uniform safe prefix, not that the prefix must reach an even return.

## 1. Root data and a coefficient invariant

Start at a compatible safe top-level chain

    x0=2^P U, Theta0=2^P z+delta,
    P>=1024, U positive odd, z integer,
    delta in {-2,-1,0,1,2,3,4}, sigma0>P.

Assume the earlier replay prefixes are defined, earlier C1 holds at
the source crossings used, and C2 holds at the first source index P-1.
The true canonical fire is included by taking delta=1 and z=U.

At every later top-level chain in a fixed valid return prefix retain

    x_t=2^(P-G_t)(a_t U+b_t z)+c_t;
    Theta_t=2^P z+d_t.                          (ROOT)

Initially (a,b,G,c,d)=(1,0,0,0,delta). At an odd a-return from j,
with tau=tau(j-1), the exact updates are

    a'=-a, b'=2^(G+2)-b, G'=G+1;
    c'=2d-c/2+3tau, d'=d+3tau+3.                (A)

At an odd b/c return put e=1+epsilon(j-1) and reduce its coefficient
ratio to c_X/2^j=N/2^e with N odd and positive. Then

    a'=Na, b'=Nb, G'=G+e;
    c'=(c_X/2^j)c+lambda_X, d'=d+3tau+3.       (BC)

Consequently a remains odd and b remains divisible by four. For odd
U the unknown root term in ROOT has valuation **exactly P-G**, even
when the a/b/c pattern and the signs of its coefficients change.
This does not replace U,z by new independent variables after a copy.

## 2. Positivity and height of the scalar intercept

At an odd b/c source, its odd head has lambda at least one and the
source mass bounds give

    0<lambda_X<=6tau+4, 0<c_X/2^j<1.

After the first nonterminal return, the scalar intercept satisfies

    0<c_t<=2d_t+2, d_t>=7.                     (INTERCEPT)

For the first a return, c1=2delta+3tau>=2, since its source is an odd
a crossing at j>=5 and tau>=2. For the first b/c return c1=lambda_X,
and d1=delta+3tau+3 gives 2d1+2>=6tau+4. Also P>=1024 ensures that
the first call time is at least two, giving d1>=7.

For later a returns, the upper bound on c gives
c'>=d-1+3tau>0; c'>0 and c'<=2d'+2 follow directly from (A).
For b/c use positivity, contraction and lambda_X<=6tau+4:
c'<=2d+2+6tau+4=2d'<=2d'+2.

The needed scalar divisions are integral as long as the root term
has valuation strictly above the current parameter. This follows
from ROOT and the known divisibility of the actual x_t. The next
section proves that strict separation inductively; it is not assumed
for the full future path.

If t_t is elapsed F time from the initial chain to the current chain,
then d_t=delta+3t_t, so c_t<=6t_t+10. A positive scalar intercept
cannot acquire arbitrary high valuation without first becoming large.

## 3. Uniform mixed-prefix theorem

Define

    K(P)=ceil(log2(12P^2)),
    M(P)=1+floor(P/(16K(P))).

**Theorem.** Under section 1's hypotheses, either the epoch ends
earlier or every top-level chain through return index M(P) is safe.
For 1<=t<=M(P),

    0<c_t<12P^2, j_t=v2(c_t)<K(P);
    G_t<=5P/16+1<P/2;
    elapsed time <=(17/16)P^2.                  (MIXED)

Within this prefix the entire return itinerary is independent of
the compatible choices of U,z. The equations for c,d and the actual
earlier crossing table determine it exactly. No NT assumption is used.

Proof. The first call costs <=P^2 by C1. Its loss is at most P/4+1
by C2 at P-1, including the a and b cases. Suppose the previous
nonterminal outputs have parameters <K. Each subsequent call costs
<=K^2, and its loss is <=j<=K using only epsilon(n)<=n.
For at most M-1 further transitions this gives

    t_elapsed<=P^2+(P/(16K))K^2<=(17/16)P^2;
    G<=P/4+1+P/16.

INTERCEPT now gives c<12P^2. For P>=1024,
12P^2<2^(P/2), so c<2^(P-G). ROOT forces j=v2(c)<K;
the actual coefficient valuation sigma0-G is greater than P-G
and hence greater than j. This justifies the next chain, including
its replay and scalar divisions, and closes the induction. An even
return instead ends the epoch. QED.

The elementary estimates K<=P/4 and 12P^2<2^(P/2) hold at the base and
persist by polynomial/exponential monotonicity. If the process ends
within this budget, a convenient bound including the final replay
and even step is 2P^2 F steps.

## 4. What the reduction isolates for a true epoch fire

(Scope note added after review: closing the induction with this section
also needs the accepted V4 tie-free certificate with r<=2 for fires with
J<1024, and recovers C2 at later indices from epsilon=O(P); C2 at P-1 is
an explicit hypothesis.)

For delta=1,z=U, the root is the actual fire data. The scalar process
starts with c=0,d=1 and first parameter P, then uses (A)/(BC) and
j=v2(c). It has no free high-bit choice within MIXED.

An explicit sufficient stopping target is:

    (INTERCEPT-STOP) At every reached fire with P>=1024, its actual
    earlier crossing table makes the delta=1 scalar process reach
    an even return by index M(P).

This target is **not proved**. It is stronger than necessary: failure
to terminate within this precision budget would not imply that the
actual epoch fails or that global non-halting is false.

If INTERCEPT-STOP were proved with the required earlier C1,C2 data,
MIXED would give r<=M(P) and G<=5P/16+1. Combined with the global-clock
argument and the audited small-P exits, this would close the epoch
induction. New crossing deficits would satisfy

    epsilon<=3+r+G=O(P)=O(log rho),

so C2 would propagate; the physical margin would remain positive.
This explains precisely how a stopping result for the scalar process
would supply the missing global budget. It is not a substitution of
that stopping result by the already proved safe-prefix theorem.

The immediate remaining task is a monotone measure, an exhaustive
all-scale word theorem, or another stopping argument for c,d using
their actual source records. Positivity and the bound c<=2d+2 alone
do not imply termination, because d increases with time.

## 5. Evidence and its limits

`verify_mixed_root.py` checks all 50176 affine root families with
P=1024,...,8191 and the seven delta values. All reach an even return
within the tested budget; there are 33337 nonterminal transitions,
and the maximum observed count of returns is three. The checks
retain the coefficient invariant and INTERCEPT at every transition.

These are actual source-table calculations and universal statements
over the root lifts for the stated P range. They are not an all-P
proof of INTERCEPT-STOP and do not enlarge the accepted unconditional
horizon.

The separate `probe_intercept.py` examines the first-rescue scalar
family c=64+288h,d=46+192h. At residue depth 20 it closes 20 cylinders
and leaves h=582542 mod 2^20 unresolved at the initial valuation.
That remaining cylinder allows a larger initial parameter; it is not
counted as a terminated tail. This probe reinforces the need to
handle unbounded source parameters rather than only split residues.

Reproduce:

    python -B work_global_mixed_precision/verify_mixed_root.py
    python -B work_global_mixed_precision/probe_intercept.py 20
