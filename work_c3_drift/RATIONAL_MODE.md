# Low-height rational phases after a large gateway

2026-10-20. **UNREVIEWED conditional lemma**, not a global certificate.
This addresses how to continue a gateway whose output parameter is
above the existing finite certificate cutoff. It does not assume the
ordinary small-symmetric-integer deep condition for that state.

## 1. Representation and the precision bit

Represent a state's exact defect D=Theta-x by

    D = C/3 + b*2^j (mod 2^(j+1)),
    C integer, 3 does not divide C, b in {0,1}.

Division by 3 means multiplication by its inverse modulo the stated
power of 2. The actual symmetric representative of D mod 2^j can
be of order 2^j; a small C does NOT imply the old |theta|<=B deep
condition. What is small is the rational representative's ordinary
absolute value |C/3|. Gateway classes (10-2^j)/3 and (26-2^j)/3
have (C,b)=(10,1),(26,1), respectively.

At an a step, tau(j-1)=2k. If 1+v2(9k+C)<=j-2, then exactly

    j'=1+v2(9k+C),   C'=9-C,   b'=0.                (RA)

Proof: 3k+D is congruent to (9k+C)/3 modulo 2^j. In
x'=2Theta+6k-x/2, the high numerator term has valuation j-1,
strictly above j'. For the output defect,
D'=3-D-x/2; both x/2 and the representation error vanish modulo
2^(j'+1). This also proves the extra-bit claim b'=0.

For a b/c step, the accepted exact defect relation is
D'=D+Phi-2 modulo 2^(j'+1), since the numerator-dependent error
has valuation at least j'+1 by real S1. At a strict parameter drop,

    C'=C+3*Phi-6,   b'=0.                          (RC)

In particular, using the proposed low-deficit identities of this
directory, the permitted maps are

    a: C -> 9-C;
    b or cAA: C -> C-3;
    c3: C -> C;
    cBA: C -> C+3.

All preserve C!=0 mod 3. Therefore 9k+C is never zero, irrespective
of the canonical k. This excludes exact resonance. It does NOT by
itself bound v2(9k+C) or exclude a non-descent.

## 2. Conditional contraction above N0

Use N0, B, kappa and P_clock from work_r1r2/NOTES.md. Define

    L3(j)=max(1+floor(log2(3*(kappa(j)+B))),
              floor(log2(6*(j-1)*P_clock(j-1)+5))),
    h3(q)=min{t : L3^t(q)<N0}.

Start at parameter q>=N0 with C0=10 or 26. Assume

    (C0+3*h3(q))/3 <= B.

On the high-parameter prefix, impose HR5: every c step with
epsilon>=7 exits to a parameter below N0. This is a condition on
the rational-mode trajectory itself; the old R1/H5 hypotheses on
small symmetric integer phases do not automatically imply it.

Then the walk reaches an even endpoint or a parameter below N0
within at most h3(q) high-parameter chains. Every such step strictly
decreases the record. Before an exceptional c landing, its rational
numerator obeys

    |C_t| <= C0+3t.

Proof: reflection C->9-C preserves |C-9/2|; the other permitted maps
change it by at most 3. Hence the displayed bound holds inductively.
At every a step with j>=N0,

    |3k+C/3| <= kappa(j)+B < 2^(j-3).

Although this is an odd-denominator rational, its nonzero numerator
satisfies |9k+C| <= 3*(kappa(j)+B). Therefore the safe integer-valued
contraction bound is

    j' <= 1+floor(log2(3*(kappa(j)+B))).

The factor 3 cannot be dropped: an odd-denominator rational may have
2-adic valuation larger than the logarithm of its real absolute value.
This is why L3 and h3 replace the old L and Lambda.

**SIZE3 holds for every j>=N0; no extra hypothesis is needed.** The
accepted split estimate gives kappa(j)<2^(j-4). Since
B=2^(N0/2) and j>=N0>=12, also B<=2^(j-6). Therefore

    3*(kappa(j)+B) < (12+3)*2^(j-6)
                   < 16*2^(j-6) = 2^(j-2).        (SIZE3)

Thus j'<=j-2, RA applies with its extra bit, and L3(j)<j. L3 is
nondecreasing. The b/c bound and record decrease are the accepted
S1 ledger. Induction for at most h3(q) steps establishes both the
height bound and the contraction: otherwise the h3-th continuing
parameter would be below N0 by definition. HR5 handles other c
steps by exit. No large-integer symmetric-phase assumption is used.

An explicit tower estimate is available. From the accepted
P_clock(j-1)<=j-1, kappa(j)<=(3/2)(j-1)^2 and
log2(6*(j-1)*P_clock+5)<=2*log2(j)+3, one gets

    L3(j) <= max(2*log2(j)+5, N0/2+4).

Indeed kappa+B<=2*max((3/2)*j^2,B); the a term is bounded by
max(2*log2(j)+1+log2(9),N0/2+1+log2(6)), with constants below
5 and 4 respectively. Put U1=2^((N0-5)/2) and
U_(r+1)=2^((U_r-5)/2). Since N0/2+4<N0, induction gives
h3(q)<=r for N0<=q<U_r. Hence the height condition follows whenever
C0+3*r<=3B. These are corrected constants, not the old T_r bounds.

The remaining hypotheses are the reached-prefix inputs, HR5, and
the stated height range. Landing certification is still separate.

## 3. Landing obligations remain

At a strong a/b/low-deficit-c landing, the actual class is
C'/3 mod 2^(j'+1), with b'=0. A high-deficit c landing still has
its exact generic class and needs separate control. Neither is
automatically certified solely by C!=0 mod 3.

The test enumerates the numerator sets reached by up to four of the
permitted maps from C0=10 or 26, then checks all j=5..128. Of 3,968
classes, 3,966 certify and two fail the minimal precision bound:

    (j,C,delta)=(5,-17,37), (5,-1,21).

These are rational-mode bare-tie obstructions. They are synthetic
class checks, not asserted reachable canonical trajectories. In
particular C=-1 is the known 3-adic orbit value -1/3 from the
accepted route-A obstruction theorem; it must not be discarded.
The infinite-denominator obstruction of that theorem still applies.

## 4. Verification

python -B work_c3_drift/verify_rational_mode.py

2,360 exact strong-a-step comparisons, testing both incoming precision
bits, match RA including the extra output bit. Finite numerator bounds
and the landing scan pass with the two failures retained as data.
This verifies the algebra, not HR5 or landing
safety. A full proof still needs the residual families and arbitrary
reachable histories; no horizon enlargement is claimed.
