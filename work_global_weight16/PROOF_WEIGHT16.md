# Rooted phase inclusion and safe returns through weight 16

2026-10-16. New conditional research result; not independently reviewed.
This extends `work_global_root_phase/PROOF_ROOT_PHASE.md`. It supplies
no bound on total epoch weight and does not prove global non-halting.

## 1. Statement and imports

Use the canonical formal walk, the exact exit maps of
`work_el/PROOF_EL.md`, and the root bookkeeping of
`work_global_root_phase/PROOF_ROOT_PHASE.md`. For a chain in an epoch,
let G be accumulated coefficient loss, a the number of preceding odd
a-returns, and W=G+a. Write x for the chain's lambda numerator,
j=v2(x), sigma for its coefficient valuation, and Theta=3s+5.
A representative theta means Theta=theta modulo 2^j; odd denominators
are interpreted in dyadic congruences.

Assume safe root fires and defined earlier replay sources satisfying
C1: tau(n)<=n^2. These are prefix hypotheses, not assumptions of future
termination. The separate new clock note proposes to supply C1 on the
maximal defined canonical prefix. Its argument is not independently
reviewed either.

**Claim.** Every reached chain of root weight W<=16 has a representative
in the sets below. Every continued return whose resulting weight is
at most 16 preserves sigma>j. In particular, under the stated source
hypotheses, a first safety failure cannot have resulting weight <=16.

This is a weighted statement, not a guarantee for the first 16 returns:
a c-copy can jump over several weights. No departure from weight 16
is covered merely by this claim.

The normal rules are

    A: theta -> 3-theta, cost 2;
    B: theta -> theta-1, cost 2;
    C: (theta,theta_s) -> theta+theta_s-2, cost 2+W_s.

The C source is an earlier a-output of weight W_s, and its exact head
deficit is W_s+1. All weights are even. Normal A means the NT condition
holds; normal B and C are automatically safe by the accepted copy lemma.

## 2. Phase sets and the exceptional inputs

Starting with S_0={1}, use the normal rules, retaining even the normal
A output of an exceptional branch as an overapproximation. Additionally
include 10/3 as an A output at weights 10 and 14, and 46/9 at weight 14.
Sections 3-5 justify precisely these extra outputs.

| W | S_W |
|---|---|
| 0 | {1} |
| 2 | {0,2} |
| 4 | {-1,1,3} |
| 6 | {-2,0,2,4} |
| 8 | {-3,-1,1,3,5} |
| 10 | {-4,-2,0,2,10/3,4,6} |
| 12 | {-5,-3,-1,-1/3,1,7/3,3,5,7} |
| 14 | {-6,-4,-2,-4/3,0,2/3,4/3,2,10/3,4,46/9,6,8} |
| 16 | {-7,-5,-3,-7/3,-19/9,-1,-1/3,1/3,1,5/3,7/3,3,37/9,13/3,5,7,9} |

When forming C outputs only source representatives arising as A outputs
are admitted. This restriction is essential; an arbitrary member of
S_W is not necessarily an eligible source at that weight.

The complete NT exceptions for input weights <=14 are

    W=8:  (j,theta)=(5,5);
    W=12: (j,theta)=(5,5) or (5,-1/3).

For 5<=j<64 this is a finite check against the exact canonical crossing
table. For j>=64 write theta=N/D in lowest terms, D odd and positive.
Through weight 14, D<=9, |N|<=46, and theta>=-6. The pointer-speed bound
gives k=tau(j-1)/2 >=(j-3)/4, so theta+3k>0. C1 and

    92+27(j-1)^2 < 2 * 2^(j-2)

give, writing theta=N/D (D odd), 0<N+3kD<2^(j-2), hence v2(N+3kD)<j-2.
This excludes the NT congruence theta+3k=2^(j-2) modulo 2^(j-1)
(the bound theta+3k<2^(j-2) alone would not suffice when D>1). The inequality holds at 64 and
persists: its positive quadratic left side grows by a factor less
than two at each next integer. Parameters <=4 terminate.

Thus the small check is exhaustive in j, rather than a numerical
extrapolation. A normal A decreases j by at least one while costing
one unit of sigma, and therefore preserves the strict margin.

## 3. A-origin phase 5 and the rational second resonance

If phase 5 is created by A, its predecessor has phase -2. The existing
root-phase lemma applies: whenever that A produces parameter 5,
p>=17, k=6 modulo 32, and two A steps from its parent give

    x_out=2^p z+2^(p-2)U+9k+10,
    Theta_out=2^p z+6k+10,
    q=v2(9k+10)<p-2,
    3Theta_out-2x_out=10 modulo 2^(p-1).

The output is safe and has phase 10/3. This handles the weight-8
exception and every A-origin instance of phase 5 at weight 12.

For the weight-12 phase -1/3, its only possible last operation is A
from phase 10/3 at weight 10. A B origin would require 2/3 at weight
10, which is absent. The eligible C phase pairs also exclude -1/3.
Write the preceding state as

    x=2^p U, Theta=2^p z+10/3.

Here z may have denominator 3; all congruences remain dyadic. The small
table excludes p<17. The A output is 5 only if k=22 modulo 32.
After that A and the parameter-5 A (whose half-time is 1),

    x_out=2^p z+2^(p-2)U+(27k+46)/3,
    9Theta_out-6x_out=46 modulo 2^(p-1).

C1 gives

    0<27k+46 <= (27/2)(p-1)^2+46 < 2^(p-2), p>=17.

Therefore q=v2(27k+46)<p-2. The two returns lose two coefficient
units, so sigma_out>=p-1>q, and the new phase is 46/9. This uses
the joint relation, not an independent choice of high bits.

## 4. B-origin phase 5 at weight 12

Such a B originates at weight 10 with phase 6. Let its parameter be Q,
and write x=2^Q u, Theta=2^Q z+6. It copies a canonical fire with
parameter 5, whose lambda numerator is A=32v with v positive odd.
The finite source table excludes Q<65 (the first such b source has
Q=65). Its fire pointer is Q-2.

The exact B copy and following parameter-5 A are

    x_5=3*2^(Q-2)u+32v,
    Theta_5=2^Q z+32v+5,
    x_out=2^(Q-3)(16z-3u)+48v+16,
    Theta_out=2^Q z+32v+14.

The source fire numerator satisfies A=3tau(Q-2)+4. Thus C1 gives

    0<48v+16 <= (9/2)(Q-2)^2+22 < 2^(Q-3), Q>=65.

Consequently q=v2(48v+16)<Q-3, with q>=5. The B and A together
lose three coefficient units; from sigma>Q follows sigma_out>=Q-2>q.
Moreover

    3Theta_out-2x_out=10 modulo 2^(Q-2).

This branch therefore also has phase 10/3. No bound on the odd
source numerator v is assumed beyond its actual C1 clock bound.

## 5. C-origin phase 5 at weight 12

The eligible phase pairs are exactly, for m=0,1,2,3,4,

    W_outer=8-2m,  W_source=2m+2,
    theta_outer=5-m, theta_source=m+2.

The maximal source phase m+2 at these weights can only be the A
output of B^m: the minimum predecessor phase 1-m is attained only
by B^m. One verifies this inductively through weight 8; a C output
is strictly above the minimum. The added 10/3 at weight 10 is below
its maximum 6. Thus the source provenance is B^m A, not an arbitrary
history with the same residue.

Let p,k be the parameter and half-time of this source's final A.
Before it, write x=2^p U and Theta=2^p z+1-m. Its A output has
parameter 5. The actual small table excludes p<14. Let rho_s be
its root pointer, and sigma_pre=rho_s-2m>p its pre-A coefficient
valuation. Its first a-output crossing has pointer rho_s+2.
The outer chain that calls this crossing has parameter

    Q=rho_s+3.

Let c_s be the source output chain coefficient. Then

    v2(c_s)=sigma_pre-1=Q-2m-4.

Write the source output as x_s,Theta_s. The outer phase 5-m gives
the time shift D=Theta_outer-2=2^Q w+3-m. If u_o is the outer odd
lambda base, the copied parameter-5 state is

    x_5=x_s+c_s u_o, Theta_5=Theta_s+D.

Apply its A. For comparison, the formal second A of the source has

    x_ref=2^p z+2^(p-2)U+9k+13-m.

This comparison is just an algebraic expression, and does not assume
that the source's subsequent epoch terminates. The outer result is

    x_out=x_ref+2D-c_s u_o/2.

Since v2(c_s/2)=sigma_pre-2>=p-1 and Q>p, this yields

    x_out=C modulo 2^(p-2),  C=9k+19-3m.

Here C>0 for k>=1 and 0<=m<=4. The first source A producing 5
implies v2(3k+1-m)=4, so C=3(3k+1-m)+16 is divisible by 32.
C1 gives

    C <= (9/2)(p-1)^2+19 < 2^(p-2), p>=14.

Hence 5<=q=v2(C)<p-2. The outer C and A together lose 2m+5
coefficient units. From its initial sigma>Q follows

    sigma_out>=Q-2m-4=sigma_pre-1>=p>q.

Finally the source formal comparison satisfies

    3Theta_ref-2x_ref=13-m modulo 2^(p-1).

Copying changes this joint expression by -D+c_s u_o, whose residue
is -(3-m). Therefore

    3Theta_out-2x_out=10 modulo 2^(p-1).

All five C provenances have safe output phase 10/3, uniformly in the
outer and source high coefficients.

## 6. A stronger restriction on the 17,5,17 obstruction

Under these hypotheses, a canonical consecutive A segment 17,5,17
must have middle head deficit at least 19. This strengthens the
earlier root-phase lower bound 11, without asserting that deficit 19
is sufficient or reachable.

Indeed a middle deficit <=17 means W_middle<=16, so the preceding
parameter-17 chain has W<=14. Its half-time is the actual k(16)=6.
Among the representatives in these sets, an A output of parameter 5
is possible only from theta=-2 or theta=46/9. For any such parent
write x=2^17 U, Theta=2^17 z+theta. Two A steps give

    x_out=2^17 z+2^15 U+theta+66.

For theta=-2 the constant is 64, giving rebound 6; for theta=46/9 it
is 640/9, giving rebound 7. Neither is 17, independently of the high
coefficients. Since the middle deficit is odd, it must be >=19.
The second case handles a specific departure from weight 16; it is
not a general solution of that layer.

## 7. Induction, checks, and the remaining boundary

Induct on resulting root weight. Each normal A/B has lower predecessor
weight, and each C has both lower outer weight and lower source weight.
Sources are also earlier in canonical time. The only departures from
NT before resulting weight 16 are the exceptions treated above.
Their precursor histories have lower weights and their explicit
two-step formulas preserve safety. This proves the claimed phase
inclusion and safety through weight 16 without assuming that epochs
end or that higher weights are unreachable.

`verify_weight16.py` builds the full finite phase overapproximation,
checks the eligible C origins and low-parameter exclusions, checks
the displayed affine identities with exact arithmetic, and checks
bases and finite samples of the analytic inequalities. The inequalities
extend to infinity by the doubling comparison described in section 2.
These checks are supporting evidence; they do not substitute for the
all-parameter arguments in sections 3-5.

The small-parameter diagnostics at input weight 16 identify phases
5, -1/3, and -19/9 at parameter 5 as the next NT exceptions. Their
departures have resulting weight 18 and are not covered here. In
particular, new B/C origins of rational phases require fresh provenance
analysis. The table does not establish those branches' safety.

The substantive advance is that the second phase-5 resonance is
closed for all three possible origins A/B/C; copying it does not
require discarding the source's coefficient precision. The unresolved
global problem is still an unbounded-weight argument: either a
uniform normalization with a decreasing measure, or a total loss/exit
bound. Merely enumerating more finite weights will not supply it.
