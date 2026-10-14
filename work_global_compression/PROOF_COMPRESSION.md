# Eliminating the source clock without discarding its correlation

2026-10-14. **New, not independently audited. No global non-halting claim.**
This continues `work_global_shadow`. It supplies exact algebraic tools for
the missing ancestry invariant, not another finite-horizon extension.

## 1. Results

* An exact source-clock elimination formula produces an odd-denominator
  representative for a shifted-copy output, without keeping its enormous
  source starting time explicitly.
* A stronger joint relation between Theta and x propagates through every
  a/b/c transition, including non-NT steps, without losing modulus bits.
* For a fire followed only by b/c returns and then its first a-return,
  the compressed arithmetic height has a conditional polylogarithmic bound
  in the source fire parameter, under earlier-epoch Theorem M estimates.
* A fixed bounded rational phase still permits an arbitrarily large
  17 -> 5 -> q jump among synthetic mass-compatible states. This rules out
  forgetting the joint relation in favor of the phase alone.

Dependencies are the exact return identities and mass/replay lemmas already
used in `work_global_shadow/PROOF_SHADOW.md`. Source prefixes must be defined;
where a bound imports earlier Theorem M conclusions, this is explicit.

## 2. Affine dependence on the source starting time [symbolic]

Let Theta0=3s0+5 at a reference level fire. Its initial lambda chain value is
x0=3s0+4=Theta0-1. Along any fixed, valid top-level prefix, write

    x = (A Theta0+B)/2^G,  Theta=Theta0+d.                  (F)

Initially (A,B,G,d)=(1,-1,0,0). All four quantities are obtained from the
observed crossing sequence, not from a guess about high bits. A stays odd
and positive; 0<A/2^G<2. The pattern need not be independent of Theta0:
(F) is asserted for a fixed valid pattern, not for all hypothetical fires.

At an a-return, put k=tau(j-1)/2. Then

    A' = 2^(G+2)-A,
    B' = -B + (2d+6k)2^(G+1),
    G' = G+1,
    d' = d+3+6k.                                         (FA)

For b/c, put e=1+epsilon(j-1), and write the crossing coefficient as
c_X/2^j=a/2^e, with a odd and 1/2<=a/2^e<1. Then

    A'=aA,
    B'=aB+lambda_X*2^(G+e),
    G'=G+e,
    d'=d+3*tau(j-1)+3.                                   (FBC)

These follow by substitution in x'=2Theta+6k-x/2 and
x'=(c_X/2^j)x+lambda_X. Oddness of A and its range are preserved.
The same G is the cumulative coefficient valuation loss from the fire.
Thus the source's physical coefficient valuation is rho_source-G.

## 3. Source-clock elimination at a shifted a-return [symbolic]

At the first a-return of a shifted copy, use the notation of the shadowing
note: D is its constant time-quantity difference, E is the pre-return x
error, and the source output has representation (F). Suppose

    D=delta (mod 2^M),  delta=P/Q with Q positive odd,
    q=v2(x_outer),
    v2(2(D-delta)-E/2)>q,  M>q.                           (SEP)

The stronger dominance bounds in the shadowing note are one way of proving
SEP. This section does not assume SEP for an arbitrary collision.
Then x_outer=x_source+2delta modulo 2^(q+1). Multiplying by 2^G gives

    A Theta0+B+2^(G+1)delta = 0 (mod 2^(q+G)).

Since A is odd, division by A is valid in this congruence. Consequently

    Theta_outer = theta_comp (mod 2^q),
    theta_comp = [Ad-B+(A-2^(G+1))delta]/A.                (COMP)

The huge Theta0 has disappeared. The result involves only a source-prefix
record and the inherited shift. Its odd denominator divides A Q.
The congruence is what is proved: theta_comp need not equal Theta_outer as
real numbers, and the higher bits of u must not be inferred from it alone.

Example: the symbolic source fire J=65 has prefix b,a through parameters
65,5. The records after the a-return are A=13, G=3, B=1955, d=168.
At delta=-1, COMP gives theta_comp=232/13. This example's shifted parameter
is 2, where this rational can also be replaced by the integer representative
0. The denominator 13 is a feature of this exact representation, **not a
proof that powers of 3 cannot suffice after some other normalization**.

## 4. A joint relation that can actually be propagated [symbolic]

The congruence theta_comp alone throws away information. Retain instead

    A Theta - 2^G x = C (mod 2^L),  A odd.                (LINE)

For a reference epoch this is an exact equality, starting with
(A,G,C)=(1,0,1), and C=Ad-B in section 2. For copied states it can be a
congruence. Both forms use the following updates.

### a-return

    A'=2^(G+2)-A,
    G'=G+1,
    C'=-C+A'(3+6k)-12k*2^G.                              (LA)

### b/c-return

Using a,e as in FBC and T=3*tau(j-1)+3,

    A'=aA,
    G'=G+e,
    C'=aC+aA*T-2^(G+e)*lambda_X.                         (LBC)

**The same modulus 2^L survives both updates.** For LA, solve
x=4Theta+12k-2x' and substitute in LINE, then use Theta'=Theta+3+6k.
The old equation is multiplied only by -1. For LBC multiply the old
equation by the odd integer a and substitute 2^e x'=a x+2^e lambda_X.
Thus neither update loses modulus bits. No step uses the NT reflection rule.

### Copy transfer

For an actual b/c copy of a source chain,

    Theta_outer=Theta_source+D,
    x_outer=x_source+c_x,source*u_parent.

Therefore the copied relation is

    A Theta_outer-2^G x_outer = C+A D
       (mod 2^min(L,G+sigma_source)).                    (LCOPY)

If D is known only as delta modulo 2^M, replace C+A D by C+A delta and
clip precision further to M. With an exact source-epoch relation,
G+sigma_source=rho_source, independent of the point copied. The source's
fire pointer therefore supplies an explicit precision budget that survives
division-related changes of j.

An exact theta=2 copy has D=0 modulo 2^j_parent and
rho_source<j_parent. Thus it inherits the same A,G,C modulo
2^rho_source, consistent with the completed-tail shadowing theorem.

**Limit.** LINE does not by itself determine the next valuation at every
collision. It must be retained with the available Theta/u residues and the
source/precision information. Constantly many fields for one path do not
prove that the number of admissible paths or coefficient records is bounded.
No claim is made that the prior 35,801 records have already been merged.

## 5. Height bounds for a first-a source prefix [symbolic + finite base]

First assume the source starts at its fire and takes only b/c transitions
until its first odd a-return. Before that last return 0<A/2^G<=1; after it

    3/2 <= A/2^G < 2.

The earlier (pre-a) intercept satisfies |B/2^G|<=2d+1. This follows from
the b/c contraction and lambda_X<=6*tau+5, with d increasing by
3*(tau+1). FA then gives |B/2^G|<=3d+1 at the a-output. Hence COMP has

    |theta_comp| <= 3d+1+|delta|/3.                       (SIZE)

The coefficient of delta is 1-2/(A/2^G), whose magnitude is at most 1/3.
This contraction does not remove the additive source term 3d+1.

Let h(delta)=ceil(log2(max(1,|P|,Q))) for delta=P/Q in lowest terms.
Before cancellation of common factors, the output numerator and denominator
are bounded by A*2^h(delta)*(3d+2). Thus

    h(theta_comp) <= h(delta)+G+1+ceil(log2(3d+2)).        (HEIGHT)

With (C1) at earlier crossings, the decreasing b/c parameters give the crude
bound d<=6J^3, where J is the source fire parameter. Independently of that
time bound, the stronger b/c descent j_next<=j-2-epsilon gives G<=J-4
at the first odd a-output.

### A better G bound under the earlier-epoch Theorem M estimates

Use Theorem M's already proved earlier-state bounds within an induction:
tau(n)<=n^2 and Delta<=(log2 i)^3 beyond its base; epsilon<=7 on the
10^8 base. At type c, epsilon(n) is the crossing deficit; at type b it is 1.
Consequently epsilon(j-1)<=max(7,(log2 j)^3).

For j>=1024, b/c transitions obey

    j_next<=log2(6(j-1)^2+5)<sqrt(j).

The last inequality holds at 1024 and its difference increases thereafter:
sqrt(j)-log2(6j^2) has positive derivative there and beyond. Thus the cubic
logarithms form a geometric sum with ratio at most 1/8 until j<1024.

The complete small b/c-prefix certificate for 1<=j<1024 gives cumulative
G gain at most 4, with witness 28->6->1. Add one for the final a-return.
Therefore, for J>=1024,

    G <= (3/2)(log2 J)^3 + 5.                             (GBOUND)

For J<1024 use G<=5. The coefficient 3/2 dominates
(1001/1000)*(8/7), bounding both the cubic sum and its per-step +1.

Together HEIGHT, GBOUND, and d<=6J^3 show additive arithmetic-height growth
O((log J)^3), rather than carrying the source starting time itself.
For a b-copy of an actual fire at crossing n, J<=log2(3n^2+4) under (C1),
so the added height is O((log log n)^3).

These are conditional estimates in an earlier-epoch induction, **not**
unconditional global Theorem M conclusions. For a c-copy the source may
already have a-transitions before the copied point. LINE and COMP remain
valid with its recorded coefficients, but the special first-b/c-prefix
bound GBOUND must not be applied to that longer prefix without proof.

For an arbitrary valid prefix one still has |B/2^G|<=4d+1, by induction
using FA/FBC. At a final a-return A/2^G>1, giving the weaker bound
|theta_comp|<=5d+1+|delta|. This bound alone does not close the global induction.

## 6. Why bounded rational phases alone are insufficient [symbolic]

The two-a rescue update with second crossing k=1 produces the formal
rational recurrence theta_next=(theta+12)/3. Starting at -2 gives

    theta_m=6-8/3^m.

These representatives are real-bounded. No assertion is made that every m
is realized on F's actual ancestry. For even m,

    v2(theta_m+66)=v2(8(3^(m+2)-1))=5+v2(m+2).

The last identity follows from v2(3^r-1)=2+v2(r) for even r, proved by
factoring an odd power of 9 and then repeatedly squaring. Hence the rational
constant can have arbitrarily high valuation despite real boundedness.
It does not follow that the next actual chain parameter equals that value:
the omitted run-base term can have the same or lower valuation.

At m=1022, theta_m=32702 modulo 2^17. Fix this phase and current j=17.
For every q>=24, set

    u=2^(q-17)+11,
    Theta=2^q-66-2^15*u = 3*2^(q-2)-360514,
    s=(Theta-5)/3,
    sigma=q+3, i=sigma+1,
    A_pair=(2^sigma, 2Theta-2^17*u-5),
    P=[(2^sigma, 2^17*u-Theta+1)].

All components are positive, Theta=32702 mod 2^17, and the two mass
identities hold. The initial lambda_x=2^17*u has parameter 17.
At X(16), k=6 and

    x1=2Theta+36-2^16*u,  v2(x1)=5.

At X(4), k=1, the two-a identity gives

    x2=Theta+66+2^15*u=2^q.

The top-level parameters are therefore **17,5,q**. The successive scale
valuations are sigma,sigma-1,sigma-2, so all three local margins are safe.
This is an infinite synthetic family, with the same fixed rational phase,
and an unbounded two-step parameter increase.

The construction is not a counterexample to F or to a proved orbit invariant:
actual reachability, prior-epoch time bounds, and ancestry constraints have
not been established for these states. It refutes a universal descent claim
based only on this phase, mass, positivity, and local margins. Any attempted
global argument must use additional history, such as LINE with its genuine
coefficient/precision provenance.

## 7. Implications for the global route

The more promising state is now

    (j, A,G,C,L, available residues, source provenance),

not merely (j,theta). The intended proof strategy is:

1. Discharge precise completed copies by the shadowing theorem.
2. Eliminate large source clocks through COMP while retaining LINE.
3. Use the source-pointer decrease and HEIGHT to budget arithmetic complexity.
4. At equal-valuation collisions, prove that the correlated state spends
   only already earned precision, or reaches a certified closing state.

Items 1--2 have symbolic formulas. Item 3 has the restricted first-prefix
bound above. **Item 4 and a closed all-prefix version of item 3 are open.**
In particular, a small new j can be comparable to or smaller than the
arithmetic height; the old size criterion cannot simply be applied again.
This is still the obstruction to proving CC in the shadowing note.
The separate actual-boundary entry condition for the original machine also
remains open. There is no new global or finite-horizon theorem here.

## 8. Checks and reproduction

`verify_compression.py` examines J=2..4095: 1304 first-a records, maximum
observed G=3, and the exhaustive small b/c gain certificate G<=4. It checks
80 synthetic source epochs with the full bigint pair map, 720 source-clock
elimination congruences (including rational shifts), 84 joint-relation
updates, and 1476 copy-transfer congruences. All pass; no sampled case lies
outside the tested separation hypothesis. The moduli and source patterns
are checked explicitly, not inferred from floating-point approximations.

`verify_resonant_family.py` verifies the synthetic 17,5,q family by full
bigint evolution for q=24..128 and q=512,4096: 107 cases, all pass.
These checks support the algebra; neither is an independent audit or proof
of actual-orbit reachability for the constructed states.

    python -B work_global_compression/verify_compression.py
    python -B work_global_compression/verify_resonant_family.py

Only this directory is written. Prior documents and accepted results remain unchanged.
