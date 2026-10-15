# Resonance, ancestry, and safe first rebounds

2026-10-15. New results; **not independently reviewed**. No global
non-halting theorem, global G2 descent, or larger unconditional horizon is
claimed. This directory leaves the accepted proofs unchanged.

## 1. Scope and imports

The accepted `work_g2_obstruction/PROOF_SPECTRUM.md` refutes global DL by
an actual safe epoch. Thus the objective here is safe rebound and eventual
exit, not restoration of DL. We use the exact pair map, replay and crossing
lemmas of `work_m/PROOF_M.md`, and the exact exit identities of
`work_el/PROOF_EL.md`. A local family need not be realized on the orbit.

At a compatible top-level chain put x=lambda_A+2lambda_b+3=2^j u,
Theta=3s+5, sigma=v2(c_x), with u positive odd and sigma>j. An odd return
at n=j-1 has the exact updates

    a:   x' = 2Theta-x/2+3tau(n),  sigma'=sigma-1;
    b/c: x' = c_X x/2^j+lambda_X, sigma'=sigma-1-epsilon(n);
    both: Theta'=Theta+3tau(n)+3.

An even return terminates the epoch. These formulas require no NT
assumption. For b/c, j'<=j-2-epsilon(n), epsilon(n)>=1; the source is an
earlier crossing. The necessary earlier prefixes and replay hypotheses
are assumed throughout. In sections 4--5 we explicitly use the earlier
induction hypotheses C1: tau(n)<=n^2 and, where stated, C2:
epsilon(n)<=max(7,n/4). These are not assumed conclusions for the current
epoch. We use v2(0)=infinity.

## 2. An infinite-depth family with complete safe exit

Fix the known parameter-5 source fire at s=52, rho=63, with 3s+4=160.
Its b-parent parameter is 65. After m-1 initial pure b copies, m>=1,
the compatible parameter-65 state has

    x=2^65 u, Theta=2^65 z+2-m, sigma>=66.

The accepted calculation, followed by the odd a-return at parameter 5,
gives

    x1=3*2^63 u+160, Theta1=2^65 z+161-m;
    x2=2^62(16z-3u)+2(124-m);
    Theta2=2^65 z+170-m;
    Theta2-x2/2=46+3*2^61 u.                 (1)

Both returns are safe when q=v2(x2)<=62: coefficient valuations are
sigma, sigma-2, sigma-3. Because 16z-3u is odd,

    v2(124-m)<61  => q=1+v2(124-m);
    v2(124-m)>61  => q=62.

Consequently the sole excluded depth progression is

    m = 124+2^61 (mod 2^62).                (2)

**Theorem 1 (finite symbolic certificate).** Every compatible state above
outside (2) ends its epoch safely in at most 112 F steps, counted from the
parameter-65 chain, uniformly over all positive odd u and all compatible
z. In particular m=124 is covered. This bounds the tail, not the preceding
m-1 copies.

Proof. By positivity and (1), after the first two returns the state belongs
to one of the 62 families

    x=2^q U, Theta=x/2+46+3*2^61 V,
    1<=q<=62, U,V positive odd, sigma>=63.  (3)

Allowing U,V to be independent enlarges the family. Substitute
U=1+2a,V=1+2b with a,b nonnegative integers and propagate affine triples
(constant, coefficient of a, coefficient of b) by the exact updates.
`verify_uniform.py` checks at each continued chain that the valuation of
the constant is strictly below both coefficient valuations. This proves
one exact next parameter for every a,b, with no residue sampling or
branch truncation. It also checks sigma>j at every chain and terminates
only on the audited table's even-return condition.

The complete affine records are in `uniform_certificate.json`. To make
the finite certificate readily inspectable, the resulting suffixes are:

| Starting q | Subsequent parameters before the even return |
|---|---|
| 1,2,3,4,7,10,11,16,19,20,21,26,29,30,31,34,37,38,39,44,47,48,53,56,57,58 | none |
| 5,6,14,15,24,25,32,33,42,43,50,51,52,59,60,61,62 | 1 |
| 12,13,22,23,40,41,49 | 2 |
| 8,18,27,36,45,55 | 3 |
| 9,35,46 | 4 |
| 17 | 7 |
| 28 | 6,1 |
| 54 | 5,8,3 |

The minimum coefficient margin is 1. Count 1+tau(j-1) per chain and one
final even-return step. The first two chains cost 56 steps, and the maximum
whole tail cost is 112 (q=54). The path 54,5,8,3 explicitly uses a
non-descending step; no NT phase update is substituted. QED, subject to
the reproducible finite certificate and imported crossing table.

There are also 376 checks using the full bigint pair map, including large
depths beyond 2^120. These cross-checks support the implementation; the
universal coverage comes from the affine certificate, not these samples.

## 3. Why the exceptional progression is real local ambiguity

At m=124+2^61 the formula is

    x2=2^62(16z-3u-1).

For every t>=1, set N=2^(t+1), z=3N, and choose the odd residue
r=-(1+2^t)*3^(-1) mod N, 0<=r<N. Put u=z+r. Then
v2(16z-3u-1)=t, so q=62+t. The initial time is integral because
2z-m=0 mod 3. The pair construction used by `concrete` has positive
lambda components and becomes arbitrarily large as required. Taking
sigma=q+4 supplies sufficient margin for this prefix.

Thus the local phase and oddness data alone permit arbitrarily large q.
The full pair checks realize q=63,64,65,72,128,256 as *local states*.
They are not a claim of reachability by actual m-deep ancestry. With only
sigma=66, the same lambda cancellation would instead fail S1. An actual
ancestry imposes extra correlations, which the next section retains.

## 4. Pure-b ancestry resolves the first rebound at every depth

Consider an actual initial pure b^m prefix ending at parameter 5.
Index its retained source ancestors upward:

    p0=5, p_(i+1)=rho_i+2,
    a_i=3s_i+4=2^p_i U_i, U_i positive odd.

Here (s_i,rho_i) is the actual earlier fire copied by the b-transition
p_(i+1)->p_i. The first parameter-5 fire has rho=63 (the accepted small
table), hence p1>=65. Source S1 gives p_(i+1)>=p_i+3, and therefore
p_ell>=3ell+62 for ell>=1. These sources are earlier than the current
epoch; C1 below applies only at their crossing indices.

Retain the lowest ell ancestors, 1<=ell<=m. The phase at their parent is

    x=2^P v, Theta=2^P Z+ell+1-m, P=p_ell,

because each preceding pure b copy reduces the phase representative by
one. A b return copying source i has the exact update

    x'=(3/4)x+a_i, Theta'=Theta+a_i-1.

Define

    S_ell=P-2ell-1;
    c_i=2^(2i+2)-3^i;
    M_ell=4+sum_(i=0)^(ell-1) c_i*2^(p_i-2i-2)*U_i.

All powers in the center are nonnegative integral powers. Composition of
ell b returns and then the a-return at 5 (tau(4)=2) gives

    x_a=2^S_ell (2^(2ell+2)Z-3^ell v)+2(M_ell-m);  (4)
    Theta_a=2^P Z+10-m+sum_(i=0)^(ell-1) a_i.      (5)

The leading bracket in (4) is odd. The coefficient valuation after these
returns is sigma_parent-2ell-1>=S_ell+1. Consequently only
v2(M_ell-m)=S_ell-1 is unresolved by valuation comparison at this level.
For ell=1 at the known source, M_1=124 and S_1=62, recovering (2).

Increasing ell changes the center by a term of valuation S_ell-1, while
S_(ell+1)>=S_ell+1. Thus the exceptional class at level ell+1 is contained
in the exceptional class at level ell. Formula (4), rather than a fixed
offset window, records the information needed to refine a collision.

**Theorem 2 (conditional ancestry resolution).** Under C1 at the earlier
source crossings, select the least ell with P=p_ell>=m. Then

    0<2(M_ell-m)<2^S_ell,
    j_a=1+v2(M_ell-m)<1+3log2(P)<S_ell.

In particular the first a-rebound is safe, with margin at least 2,
independently of the unknown outer Z,v. Such an ell always exists and
requires at most 1+ceil(log2(max(1,m/65))) source ancestors.

Hypotheses (stated explicitly after review): S1 at the sources
(p_(i+1)>=p_i+3), the accepted first parameter-5 fire at rho=63, and C1
at the indices rho_i (valid since tau(rho+1)=tau(rho), e.g. tau(64)=tau(63)=52).

Proof. Since p_m>=3m+62, the selected ell exists. C1 and the pointer-speed
bound rho<=2s+2 (PROOF_M) give, for each retained source,

    a_i<=3(p_(i+1)-2)^2+4<=3(P-2)^2+4;
    a_(ell-1)>=3P/2-2, still M_ell>P.

The weight of a_i in M_ell is 1-(3/4)^i/4, lying in [3/4,1).
Hence M_ell>P>=m, and

    M_ell<4+ell*(3(P-2)^2+4)<P^3.

The last inequality follows from ell<=(P-62)/3 and P>=65. Also
S_ell>=(P+121)/3 and

    2P^3<2^((P+121)/3), P>=65.

For the latter, check P=65 and note that the derivative of the logarithm
of the right/left ratio is log(2)/3-3/P>0. These estimates prove strict
separation in (4) and the claimed valuation and margin bounds.

For the ancestor count, C1 gives 2^p_i<=3(p_(i+1)-2)^2+4. For p_i>=65,
2^p_i>3(2p_i-2)^2+4, so p_(i+1)>2p_i. The inequality holds at 65 and
persists as the exponential/polynomial ratio increases. Therefore
p_ell>=65*2^(ell-1), yielding the stated bound. QED.

`verify_ancestry.py` checks 150 formal coefficient identities and 300
bound instances. Its synthetic chains test algebra only: they are not
asserted to satisfy C1 or to occur on the orbit. The analytic arguments
above, not those finite checks, justify all-depth coverage.

## 5. First-a safety after a general initial b/c prefix

There is also a useful broader result which needs C1 and C2. Start at a
fire of parameter J with x=2^J U, Theta=2^J U+1. Follow its initial b/c
prefix until it ends or reaches an odd a-return at q>=5. After m copies
write

    x=alpha*2^J U+b, Theta=2^J U+1+3D;
    D=sum(tau(j_i-1)+1), G=sum(1+epsilon(j_i-1)).

The b/c formulas and source mass bounds imply

    0<alpha<=1, v2(alpha)=-G,
    0<=b<=sum(6tau(j_i-1)+5)=6D-m.

Indeed c_X<=2^j for the source x-pair and lambda_X<=6tau+5; each update
therefore contracts the preceding nonnegative constant by at most one.
The b/c descent also implies G<=J-q-m, so all these copies are safe.
(Changelog: an earlier draft had G<=J-q-2m; corrected, see
work_g2_mixed_blocks/PROOF_MIXED.md. Each b/c step drops j by 2+epsilon.)
At the first odd a-return put k=tau(q-1)/2. Its output is

    x'=(2-alpha/2)2^J U+beta,
    beta=2+6D+6k-b/2>0.                    (6)

The coefficient in (6) has valuation J-G-1 (the two summands have
distinct valuations). Since m<=(J-5)/3 and every preceding parameter is
at most J, C1 gives beta<3J^3. The constants are integers, because b is
divisible by 2^q.

For J>=1024, each b/c successor satisfies
j'<=log2(6(j-1)^2+5)<=j/2 whenever j>=64. Thus the sum of the large
parameters is at most 2J and their number is at most log2 J. C2 bounds
their epsilon by j/4. Below 64 there are at most 21 further b/c steps,
each with 1+epsilon<=8 by the audited small table. Consequently

    G<=J/2+log2 J+168<=3J/4;
    beta<3J^3<2^(J/4-1)<=2^(J-G-1).

Both numerical inequalities hold at 1024 and persist by monotonicity
(for the last exponential comparison use logarithmic derivative
log(2)/4-3/J>0). Therefore (6) separates strictly and

    j'=v2(beta)<3log2 J+2, j'<J-G-1.

(This analytic bound is proved for J>=1024; smaller J are covered only by
the J<4096 certificate.)

Initial physical sigma>=J+1 gives output sigma>=J-G, so this establishes
S1 as well as a bound relative to the original J. It need not give a
decrease relative to the immediately preceding q.

For 1<=J<1024, `verify_first_a.py` certifies the same positivity and
strict valuation separation with affine integer coefficients in U. It
checks every b/c transition until an even end or the first a, without
sampling U. The saved certificate additionally checks J through 4095:
1304 first-a cases, 2791 even ends, minimum symbolic margin 1. The
observed maximum of two b/c copies in this finite range is **not** used
as an all-J bound.

Thus the first odd a-transition after any initial b/c prefix is safe
under the earlier C1,C2 hypotheses. This includes an empty prefix.
The proof does not control the whole suffix after that transition.

## 6. Remaining gap and a concrete continuation target

Theorem 1 closes an infinite family of complete tails. Theorems 2 and
section 5 remove first-rebound safety as an obstruction, even when local
phase data exhibit resonance. They do not show that all later a/b/c
returns terminate, or that their total loss and duration preserve C1,C2.

A possible next step is to propagate the joint state (4),(5) through
later returns, and prove entry into either a finite certified suffix or
a sufficiently precise completed-tail copy. An ancestor count alone is
not a global decreasing measure: after a rebound the new tail has not
been shown to belong to the same pure-b ancestry class. No such closure
is assumed here.

Reproduce from the repository root:

    python -B work_g2_resonance/verify_uniform.py
    python -B work_g2_resonance/verify_first_a.py
    python -B work_g2_resonance/verify_ancestry.py
