# The unresolved depth class as an exact return block

2026-10-15. New continuation, not independently reviewed. No global
termination claim. Earlier C1 is invoked only where explicitly stated.

## 1. A natural class that is preserved by the exceptional block

The exact odd a-return at parameter 5 has tau(4)=2. If its input is
x5=32v, v positive odd, then

    Y=2Theta5-x5/2+6, Theta_new=Theta5+9,
    Theta_new-Y/2=x5/4+6=8v+6.                  (1)

Thus define the compatible state class

    C: x=X=2^q u, Theta=X/2+8v+6,
       u,v positive odd, q>=5.                 (2)

Physical coefficient margin and the earlier replay hypotheses are
separate requirements. Merely belonging to C does not imply safety or
reachability. The reset family studied previously belongs to C, since
46+3*2^61 V=8(5+3*2^58 V)+6 with the parenthesized integer odd.

Every state in C has Theta=14 mod 16. Suppose it follows m initial odd b
returns to parameter 5 and then makes its odd a-return. The phase
calculation from `work_g2_shift44` remains valid modulo 16 even at q=5:

    Y=2(9-m) mod 32.

If m!=9 mod 16, its next parameter is <=4 and the epoch ends safely as
proved there. If m=9 mod 16, Y is divisible by 32. Provided this rebound
is safe, (1) says that the new state is in C again. This is a genuine
return to the same enlarged state class, not a decrease established by
the depth congruence alone. The original fixed reset family is a proper
restriction of C; no claim is made that it is itself preserved.

The empty b-prefix m=0 corresponds to starting at q=5 and terminates;
a nonterminal return block must contain at least nine b copies.

## 2. Exact block transformation

Let p0=5,p1,...,pm=q be the actual source ancestry for this block,
indexed from the bottom. The b-return p_(i+1)->p_i copies the source fire
at rho_i=p_(i+1)-2. Write

    a_i=3s_i+4=2^p_i U_i, U_i odd positive;
    A=sum_(i=0)^(m-1) a_i;
    B=sum_(i=0)^(m-1) (3/4)^i a_i;
    alpha=(3/4)^m.

The initial b transitions occur in the order i=m-1,...,0. Their exact
composition, followed by a at 5, is

    H=alpha X+B;                           (input x at parameter 5)
    Theta5=X/2+8v+6+A-m;
    Y=(1-alpha/2)X+16v+18+2A-2m-B/2;
    Theta_new=Theta5+9;
    v_new=H/32, Theta_new=Y/2+8v_new+6.      (3)

All divisions in an actual valid prefix are integral; H has valuation
exactly 5, so v_new is positive odd. Formula (3) gives a two-variable
return map, together with its source record (A,B,m). It applies also
when the next parameter increases. There is no NT assumption.

The exact step count up to the newly produced chain is

    T_block=sum_(i=1)^m [1+tau(p_i-1)] + 3,             (4)

and the coefficient valuation loss is exactly

    L_block=2m+1.                                      (5)

The new chain's own replay is not included in (4). Its safety requires
v2(Y)<sigma_input-L_block; (3)--(5) do not assume or prove this inequality
in the unresolved class. For the terminal class the previous theorem
already establishes it.

## 3. Individual block costs under earlier C1

For actual sources satisfying earlier C1, the first parameter-5 fire
occurs at rho=63, hence p1>=65. At a source of parameter p_i,

    2^p_i <=3s_i+4<=3(p_(i+1)-2)^2+4.

For p_i>=65, the elementary inequality
2^p_i>3(2p_i-2)^2+4 implies p_(i+1)>2p_i.
It holds at 65 and persists by exponential/polynomial monotonicity.
Therefore

    m<=1+log2(q/65),
    sum_(i=1)^m p_i^2 <(4/3)q^2.

Combining C1 with (4)--(5) gives

    T_block < (4/3)q^2+m+3;
    L_block <=3+2log2(q/65).                           (6)

For m=1 the geometric sum bound is also strict. These estimates use
only earlier source times and crossing times. They do not presume the
current epoch has ended.

In particular any nonterminal block of this form, m>=9, requires
q>=65*2^8=16640. This is a sufficient low-parameter exclusion, not a
claim that blocks at that threshold exist. The original exponential
source inequalities imply much larger necessary thresholds; the simple
bound is sufficient here. Thus under C1, a C-state with 65<=q<16640
whose initial pure-b prefix reaches 5 cannot make this nonterminal
return: it must terminate by the depth congruence theorem.

These are useful per-block bounds. Summing them requires a bound on
the number of blocks, as well as treatment of intervening a/c branches.
Neither is supplied by (6).

## 4. Why two tempting ranks do not follow from the affine formulas

Neither q nor v is automatically reduced by (3). This can be checked
without claiming a counterexample on the actual orbit.

Fix a *formal* nine-source array with p0=5 and p_i=62+3i, so q=89, and
choose a_i=2^p_i times 5 for odd p_i, or times 1 for even p_i. These
values have a_i=1 mod 3, and the b-algebra produces each intended source
parameter. These arrays are **not actual crossing records and do not
satisfy all earlier C1 inequalities**. They test only what follows from
the affine map and phase class after source restrictions are discarded.

For any sufficiently large odd r, put target=2^r and

    D0=18+2A-2m-B/2,
    v=[target-(1-alpha/2)X-D0]/16.

Choose X=2^89 u with u odd just below
(target-D0)/[(1-alpha/2)2^89]. Then v is positive odd, bounded by a fixed
multiple of 2^89 as r grows, while v_new=(alpha X+B)/32 grows with 2^r.
The compatible lambda components are

    lambda_A=2Theta-X-5=16v+7;
    lambda_b=X-Theta+1=X/2-8v-5,

both nonnegative for large r. Since target=2 mod 3 and B=1 mod 3,
the output equation forces Theta=2 mod 3, so the time is integral.
An arbitrarily large physical coefficient scale can be assigned to these
formal input lambda values, but that does not turn the source arrays
into actual crossing data.

`verify_block.py` exhibits formal rebounds 89->101, 89->201, 89->501,
with v_new>v in each case. This rules out deriving a q-only or v-only
decrease from the enlarged affine class *alone*. It does not refute a
rank exploiting actual ancestry, C1, or the stricter original reset
relation, and it does not exhibit an actual nonterminating orbit.

## 5. Progress toward the global induction, and the remaining target

The depth-9 obstruction is now an explicit return map with exact costs.
It explains why repeatedly subdividing the depth residue does not by
itself supply a stopping proof: the nonterminal branch returns to C.

A viable next lemma must retain more than (q,v) and the low phase. One
concrete target is a bound on how many safe nonterminal blocks (3) can
occur in a current epoch, using the actual source records and their
ordering. The per-block bounds (6) then make the accounting explicit.
Alternatively, one can seek a rank on this source-enriched return map,
while proving that intervening branches return to the same ranked domain
or terminate. No such rank or block-count bound has been proved here.

The new results therefore improve the formulation of the remaining
problem and give conditional termination of a further subclass. They do
not close the depth-9 branch at all parameters or the global induction.

## 6. Reproduction

    python -B work_g2_return_block/verify_block.py

The script checks 360 exact block identities using rational arithmetic,
the output residue and preserved joint relation, and the three formal
rebound constructions. These are algebra checks, not orbit simulation.
The certificate is `block_checks.json`.
