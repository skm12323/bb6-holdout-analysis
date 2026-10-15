# A positive identity across two pure-b return blocks

2026-10-15. New continuation, not independently reviewed.
This proves a conditional return to a parameter core, not a bound on
the number of core visits or a global non-halting theorem.

## 1. Setting and exact elimination

Use the state class and block notation of
`work_g2_return_block/PROOF_BLOCK.md`. A block consists of m odd b
returns ending at parameter 5, followed by its odd a-return. Write

    alpha=(3/4)^m, A=sum a_i, B=sum (3/4)^i a_i,
    C_block=18+2A-2m-B/2.

For input x=X and Theta=X/2+8v+6, its output and new odd base are

    Y=(1-alpha/2)X+16v+C_block;
    32v_new=alpha X+B.

Consider two consecutive such blocks, with depths m,n and respective
source triples (alpha,A,B), (beta,D,E), beta=(3/4)^n. Let their entry
chain values be X0,X1 and the second output X2. The first block has
already returned safely to the class; the second block's b prefix is
safe by replay. The second output's safety is not assumed.

Substitute the first block's new base into the second output formula:

    X2=(alpha/2)X0+(1-beta/2)X1+C,                 (POS-BLOCK)
    C=B/2+18+2D-2n-E/2.

The old unknown base v has disappeared. Both coefficients are strictly
positive. For genuine sources, 0<E<=D and each source fire value is at
least 32, so

    C>=B/2+18+(3/2)D-2n>0.

The constant is integral. This identity is valid through resonant
returns and does not require parameter descent or an NT assumption.

For nonterminal blocks within this class, m,n are 9 mod 16. The identity
also holds formally for other depths; those depths instead terminate
the actual class trajectory at the first block.

## 2. Control of the constant by actual earlier sources

Let q0=v2(X0), q1=v2(X1), Q=max(q0,q1). For each block retain its actual
ancestor sequence p0=5,...,pm=q. Assume earlier C1 at the source fires
and all called crossings. As in the preceding note, p1>=65 and
p_(i+1)>2p_i for i>=1.

The source masses satisfy

    a_i=3s_i+4<=3(p_(i+1)-2)^2+4<3p_(i+1)^2.

(This bound comes from M2' (s<=i^2) at pointer rho_i, not from C1, which
would give (p_(i+1)-1)^2; the conclusion A<4q^2 is unaffected.)

Summing over the geometrically increasing parents gives the sharper
bound

    A<4q0^2, B<=A; D<4q1^2, E<=D.

Consequently

    0<C<2q0^2+8q1^2+18<=10Q^2+18.                (SIZE)

This uses the actual sources and C1, rather than replacing their masses
by independent arbitrary integers. It is exactly the extra information
missing from the preceding formal rebound examples.

## 3. Two sufficiently large entries force a safe core output

Define

    K(Q)=ceil(log2(10Q^2+18));
    S0=q0-2m-1, S1=q1-2n-1.

The first two summands of POS-BLOCK have valuations exactly S0,S1:
3^m and 2^(2n+1)-3^n are odd. Thus, if

    min(S0,S1)>=K(Q),                              (SEP)

the positive constant C is strictly below 2^K. It cannot cancel against
either high-valuation summand. We obtain

    q2=v2(X2)=v2(C)<K(Q).                          (CORE)

Moreover the physical coefficient valuation after the second block is

    sigma2=sigma1-(2n+1)>=q1+1-(2n+1)=S1+1.

Hence q2<sigma2, proving the second output safe without presuming its
safety. Its replay uses an earlier index: q2<sigma2<=the outer pointer.

Hypotheses of this section, stated explicitly: X0 and X1 are safe; C1, C2
and M2' hold at all source, corridor and endpoint crossings used; the
entries are of the class treated here with q>=65.

**Convenient sufficient condition.** For q>=65, the earlier C1 bound
m<=1+log2(q/65) implies 2m+1<=q/2. Check the inequality at 65 and note
that q/2-3-2log2(q/65) is increasing thereon. Therefore

    min(q0,q1)>=2K(Q)                              (LARGE)

implies SEP. Two entries both above this logarithmic threshold cannot
produce a third entry above it. Equal large parameters, and more
generally comparable large parameters satisfying LARGE, are excluded
from continuing as a third large block entry.

This is not an unconditional exclusion of two nonterminal blocks.
If one entry is small relative to log Q, SEP may fail. Such a large
scale disparity is one remaining possibility; repeated visits to the
small parameter core are another.

## 4. Costs and a fixed-ceiling counting consequence

The two blocks together cost exactly

    sum_(first parents) [1+tau(p_i-1)]
      +sum_(second parents) [1+tau(r_i-1)]+6

F steps, up to the new chain X2, and lose exactly 2(m+n)+2 coefficient
bits. The geometric source estimate and C1 bound this duration by

    (4/3)(q0^2+q1^2)+m+n+6.

Now consider a safe run of consecutive blocks with all their entry
parameters bounded by a fixed g. Put K_g=ceil(log2(10g^2+18)) and call
q<2K_g a core entry. If two successive entries are outside this core,
the theorem forces the next entry into it. Therefore no three
consecutive block entries lie outside the core. A finite string with
b core entries has at most 3b+2 entries in total.

This is a counting reduction, not the missing core-visit bound. It also
applies only to strings of the specified blocks; intervening a/c routes
must be handled separately for a global theorem.

## 5. What changed and what did not

The earlier single-block formula allowed an unbounded old base to
control the next valuation. Across two blocks that base is eliminated,
and real source bounds give a positive polynomially bounded constant.
This supplies a new safety and logarithmic-return theorem for consecutive
resonant blocks, without guessing their high bits.

The argument does **not** prove that the next block has a smaller source
pointer in every case, or that an epoch can enter the core only a bounded
number of times. It does not yet supply the global C1,C2 propagation or
cover arbitrary interleavings of return types. The remaining targeted
problem is the behavior following a core entry, retaining its source
record, rather than unrestricted consecutive large block entries.

## 6. Checks

    python -B work_g2_two_blocks/verify_two.py

The script checks 96 exact two-block identities using rational
arithmetic and 4037 instances of the elementary bound constants. The
identity inputs are synthetic algebra arrays, not orbit records or
C1-certified histories; the all-parameter C1 argument is in sections
2--3. No actual two-nonterminal-block orbit witness is asserted.
