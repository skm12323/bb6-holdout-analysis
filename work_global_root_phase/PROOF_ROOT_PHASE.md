# Root-anchored return weight and the first resonant layer

2026-10-16. New research proof, not independently reviewed. This adds
canonical reachability restrictions and a uniform first-resonance
rescue; it does not prove SQRT-EXIT or a total coefficient-loss bound.

## 1. An exact weight stored by the coefficients

Start at an actual canonical epoch fire of pointer rho. At a later
top-level chain let

    G=sum of completed return losses (1+epsilon),
    a=number of completed odd a-returns,
    W=G+a.

The initial fire has W=0. An odd a-return adds 2 to W; an odd b-return
adds 2; an odd c-return adds 1+epsilon_source.

At an odd type-c crossing, i.e. a chain which is itself an a-output,
the accepted bookkeeping formulas give the exact identity

    epsilon(i)=W+1.                              (WEIGHT)

Indeed sigma=rho-G is both the chain coefficient valuation and the
head coefficient valuation at this a-output. Its pointer is
i=rho+1+a. Their difference is 1+G+a.

If a c-return copies such a source, write W_source for the source's
weight. Its cost is therefore 2+W_source. The copied source is an
a-output, by the accepted crossing-location lemma.

These identities do not require NT. Induction over earlier source
crossings shows that W is always even and every type-c deficit is
odd and at least 3. Its source weight is strictly below the final
outer weight reached by that c-copy.

Thus a freely selected physical margin does not encode a canonical
history: the exact head deficit records restrictions on that history.

## 2. A phase grammar rooted at the true fire

At the fire the representative phase is theta=1. Whenever the return
is NT, the exact exit identities give the following operations:

    A: theta -> 3-theta,             weight cost 2;
    B: theta -> theta-1,             weight cost 2;
    C: theta -> theta+theta_source-2,
       weight cost 2+W_source, source history ending in A.

Each representative means Theta=theta mod 2^j at the current parameter,
not equality of the actual clock. The c rule retains the source's
canonical phase; it is not an independently chosen offset.

For weights through 8, this grammar gives the overapproximation

| W | Allowed representative set |
|---|---|
| 0 | {1} |
| 2 | {0,2} |
| 4 | {-1,1,3} |
| 6 | {-2,0,2,4} |
| 8 | {-3,-1,1,3,5} |

The finite combinatorial expansion is saved by `verify_root_phase.py`.
Every actual canonical state of these weights lies in the table; no
claim is made that every abstract word or value is actually reachable.

### Why using NT here is not circular

To reach weight <=8 via A, its input weight is <=6, whose phase lies
in [-2,4]. The accepted NT criterion applies under earlier C1, with
the small cases checked directly. A copied source has smaller weight,
so its phase statement is available in this induction. No a-step at
weight 8 is executed in order to justify the weight-8 table.

More explicitly, for j>=10 and theta in [-3,5], the earlier clock
bound and pointer-speed bound give

    0<theta+3k<2^(j-2), k=tau(j-1)/2.

The upper bound follows from 5+(3/2)(j-1)^2<2^(j-2); the lower bound
uses k>=(j-3)/4. Both are valid from j=10 onward. Among j=5,...,9,
the actual odd a cases are checked from the small table. The sole NT
failure for theta in [-3,5] is (j,theta)=(5,5).

Earlier C1 is explicit in these phase/safety statements. The new
`work_global_clock` argument would make it available on the maximal
canonical prefix without an exit-length hypothesis, but that separate
new argument has not yet been independently reviewed.

## 3. A global restriction on the old local obstruction's coefficients

Under earlier C1 at the source crossings used in section 2, suppose
the canonical walk contains a consecutive a-return segment

    17 -> 5 -> 17.

Let epsilon_mid be the head deficit at the middle parameter-5 crossing.
Then necessarily

    epsilon_mid>=11.                            (REACH)

Proof. If epsilon_mid<=9, WEIGHT gives W_mid<=8 and the preceding
parameter-17 state has W<=6. Its representative lies in [-2,4]. The
odd a-return at 17 uses k17=6. Among these representatives, the only
one which can produce parameter 5 is theta=-2. For theta=-2 mod 2^17,
the accepted exact rescue forces

    17,5,6,1,

including the next parameter 6 rather than 17. This is a contradiction.
Since type-c deficits are odd, the next possible value is at least 11.

For the weaker conclusion epsilon_mid!=3, no NT or C1 assumption is
needed. WEIGHT=2 means the middle state is the first a-output of a
fire. Its preceding parameter would be the fire parameter 17. But a
fire of parameter 17 has x=2^17 U, Theta=x+1, and its a-output is
3*2^16 U+38, of valuation 1, not 5.

The coefficient assignment in the accepted local frontier construction
has head 3*2^sigma, tail 5*2^sigma and pointer sigma+3 at that middle
parameter-5 state. It therefore has epsilon_mid=3 and cannot be a
canonical occurrence, regardless of the initial fire parameter J.
This strengthens a reachability restriction on that particular local
coefficient assignment; it does not invalidate its local algebra or
show that its lambda pattern is impossible with different coefficients
and a longer actual history. No accepted file is modified here.

## 4. The first non-NT layer is a uniform, safely resolved family

Within weight 8 the phase 5 can arise only from the outer return word

    B B B A.

This follows directly from the grammar: the minimal phase -2 at weight
6 comes only from BBB, and A reflects it to 5. C and B cannot produce
the maximal phase 5 at weight 8.

Let p be the parameter before that last A. Its phase is -2 mod 2^p.
For its output to be 5, its earlier half-time k must satisfy

    p>=17, k=6 mod 32.

The p<17 cases are excluded by the actual small table. For larger p,
the NT identity gives v2(3k-2)=4, which is exactly the displayed
congruence. Write the pre-return state as

    x0=2^p U, Theta0=2^p z-2, U odd.

Follow its a-return and the next a-return at parameter 5. Exact algebra
gives

    x2=2^p z+2^(p-2)U+9k+10;
    Theta2=2^p z+6k+10.                          (RESCUE)

Earlier C1 implies

    0<9k+10<=(9/2)(p-1)^2+10<2^(p-2), p>=17.

The final inequality holds at 17 and persists by polynomial/exponential
monotonicity. Consequently the rebound parameter is exactly

    q=v2(9k+10), 5<=q<p-2.                      (DROP)

It may exceed the intervening parameter 5, but strictly decreases from
the parameter p preceding this two-a segment. If the input coefficient
valuation exceeds p, then after two a losses it is at least p-1>q;
the non-NT rebound is therefore safe, uniformly in U,z.

Moreover the full joint information satisfies

    3Theta2-2x2=10 mod 2^(p-1),
    Theta2=10/3 mod 2^q.                         (JOINT)

The division by 3 is legitimate in the dyadic congruence. JOINT is
stronger than replacing the resulting phase by a free offset. It is
the correct information to carry into the next weighted layer.

This result resolves the first possible NT failure at weight 8 for
arbitrary p, not just p=17. For p=17, k=6 it recovers q=6. It does
not assert that the subsequent tail from arbitrary q always ends.

## 5. Relation to the still-open exit budget

The root weight gives exact history information; it is not a decreasing
rank. It increases at every return. The preceding argument excludes
low-weight canonical versions of a troublesome local pattern and
closes the first resonant layer with a strict two-step drop from p.

The unresolved task is to extend this rooted grammar through JOINT and
later c-copies without losing the accumulated precision or generating
an uncontrolled number of new rational phase relations. In particular,
nothing here bounds the total weight by sqrt(rho), or proves that the
finite-precision rooted grammar becomes terminal at every higher weight.

Thus SQRT-EXIT and the global safety theorem remain open. The present
result supplies a genuine reachability constraint missing from the
free-base local constructions, rather than substituting a new assumed
exit bound for the one to be proved.

## 6. Checks

    python -B work_global_root_phase/verify_root_phase.py

The script enumerates the complete weighted grammar through 8,
verifies the sole small NT failure, checks 57 applicable actual
half-time records through parameter 4095, and checks the exact rescue
and joint identities on compatible local lifts. The all-p statements
use the analytic inequalities above, not extrapolation from this table.
