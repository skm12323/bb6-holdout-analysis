# Retaining the original variables through repeated parameter-5 rescues

2026-10-16. New argument, not independently reviewed. This establishes
uniform transfer and safety results for a specific repeated two-a
pattern. It does not prove a total exit-length bound or cover arbitrary
b/c interleavings.

## 1. A rational family beyond the first rooted resonance

The first rooted resonance in `work_global_root_phase` starts with
phase -2 and, after two a-returns through parameter 5, has phase 10/3.
More generally define

    delta_n=6-8/3^n, n>=0.

Suppose a safe parent chain of parameter p has

    x=2^p U, Theta=delta_n mod 2^p, U positive odd,

and its odd a-return has half-time k. Congruences with odd rational
denominators have their usual dyadic meaning. For p>=7 its next
parameter is 5 precisely when

    v2(3^(n+1)(k+2)-8)=4.

Equivalently, k=6 mod 32 for even n and k=22 mod 32 for odd n. This
condition also makes the first a-step descending. The actual small
table excludes such a parent p<17 (machine-checked for even n; for odd n,
k=22 mod 32 is impossible trivially since k<=8 there).

The following a-return at 5 has k5=1. Write
Theta=2^p z+delta_n, where z is dyadically integral but can be rational
with an odd denominator. Its output is

    x_new=2^p z+2^(p-2)U+C_n,
    C_n=delta_n+9k+12
       =[3^(n+2)(k+2)-8]/3^n.                  (ONE)

The high part has valuation exactly p-2. Put
a_n=v2(3^(n+2)(k+2)-8). Unless a_n=p-2, the output parameter is

    q=min(a_n,p-2)<=p-2,

and it is safe after the two coefficient losses. The exact joint
relation is

    3Theta_new-2x_new=delta_n+12 mod 2^(p-1).

Since q<=p-2, it implies

    Theta_new=delta_(n+1) mod 2^q.

Thus all noncolliding steps of this repeated-rescue family are
normalized by the same affine rule delta -> delta/3+4. This is an
all-n statement, not a list of finitely many phase constants.

## 2. Where the phase-only normalization loses information

Under earlier C1, k<=(p-1)^2/2. A convenient sufficient separation
condition is

    p>=2n+32.

It ensures

    0<3^(n+2)(k+2)-8<2^(p-2),

so a_n<p-2 and the strict parameter reduction follows. To check the
inequality for all n, first check n=0,p=32. Increasing n by one and
p by two multiplies the numerator bound by at most
3*((p+1)^2+4)/((p-1)^2+4)<4, while the right side is multiplied by four.
For fixed n the polynomial/exponential ratio decreases for p>=32.

This gives descent outside a core which grows with n. It does not
bound n: the precision required by the denominator 3^n also grows.

There is an explicit warning example. At n=1022,p=17,k17=6,

    v2(3^(n+1)(k17+2)-8)=4,
    v2(3^(n+2)(k17+2)-8)=15=p-2.

The local phase condition alone then permits arbitrary high output
parameters after 17->5. The script constructs compatible positive
local examples with outputs 41,101,201. These do not assert that 1022
such rescues actually occurred, and they do not preserve an entire
rooted history. They show why the phase-only normalization cannot be
used at its collision as if it still determined q.

The next section avoids that loss by retaining the original variables
and all intervening call times, rather than restarting from delta_n.

## 3. An exact ladder rooted at the original phase -2 parent

Start with

    x0=2^P U, Theta0=2^P z-2,
    U positive odd, z integer, sigma0>P.

Follow consecutive segments consisting of an odd a-return to parameter
5 and its odd a-return. Let p_i be the input parameter to segment i,
k_i=tau(p_i-1)/2 its first half-time. No b/c transition is permitted
between these segments; if another pattern occurs, this ladder stops.

After m segments the exact representation is

    x_m=2^(P-2m)[U+4(4^m-1)z/3]+b_m;
    Theta_m=2^P z+d_m;                             (ROOT)

where

    b0=0, d0=-2;
    b_(m+1)=b_m/4+d_m+9k_m+12;
    d_(m+1)=d_m+6k_m+12.                           (BD)

The bracket multiplying 2^(P-2m) is an odd integer. ROOT follows by
composition of the exact two-a map
x'=Theta+x/4+9k+12, Theta'=Theta+6k+12. It does not depend on whether
a phase-only valuation comparison at an intermediate state is tied.

The actual time cost of m segments is sum_i(2k_i+4), and the physical
coefficient valuation is sigma0-2m.

## 4. Uniform safety for a linear root-precision budget

**Theorem.** Assume P>=64, the initial state is compatible and safe,
the earlier replay prefixes are available, and C1 holds at the source
indices used. For any consecutive ladder prefix of at most
floor(P/4) segments, every resulting chain is safe and

    0<b_m<6mP^2<2^(P-2m),
    p_m=v2(b_m)<P-2m, m>=1.                       (SAFE)

This is a finite-prefix statement: it certifies each segment if its
first return has parameter 5, rather than assuming the entire future
ladder exists. It does not certify that all those segments occur.

Proof. Induct on m. At the start p0=P. If the preceding outputs are
safe and below P, the next source half-time is <=(P-1)^2/2. The
intermediate parameter 5 is safe because sigma0-2m-1 is still large
throughout this budget. ROOT's high term is divisible by at least
2^(P-2m), so the divisibility of the actual input x_m by 32 makes
b_m/4 integral whenever another segment is about to occur. Initially
b0/4=0.

From BD one has b_m<=2d_m+4, with strict inequality for m>=1. Indeed
the difference in the induction step is at least d_m/2+3k_m+15>0,
using d_m>=-2. Since 6k_m+12<=3P^2,

    d_m<=3mP^2-2, b_m<6mP^2.

For m<=P/4,

    6mP^2 <=(3/2)P^3 <2^(P/2)<=2^(P-2m).

The strict middle inequality holds at 64 and persists because the
logarithmic derivative 3/P-ln(2)/2 is negative. The high term in ROOT
cannot cancel against b_m. Thus p_m=v2(b_m)<P-2m, while the physical
valuation is sigma0-2m>=P+1-2m. This proves the next output safe with
margin at least two and closes the induction. QED.

This theorem handles local collisions such as the one in section 2
as long as the original root precision remains within this budget.
They no longer allow a completely free high rebound: the output is
determined by the retained intercept b_m.

## 5. A fixed logarithmic core and an explicit cost bound

For P>=1024, SAFE can be sharpened throughout the same m<=P/4 prefix:

    b_m<8P^2, p_m<2log2(P)+3;
    total F time <=(5/4)P^2;
    coefficient loss=2m<=P/2.                    (CORE)

Proof. The coarse estimate already gives
p_i<log2((3/2)P^3)<3log2 P+1 for i>=1. Let
h=ceil(3log2 P+1); then h<=sqrt(P) for P>=1024, since
3log2 P+2<=sqrt(P) from that point onward. All calls after the first
therefore have 6k_i+12<=3h^2<=3P. It follows that

    d_m<3P^2+3mP, b_m<6P^2+6mP<8P^2.

The first segment costs <=P^2 and every subsequent segment <=h^2<=P,
giving the stated time bound. QED.

The core in CORE is independent of U,z and of m within the root budget.
The root variables have not been forgotten on each reentry.

## 6. What this does not yet close

The ladder covers consecutive two-a rescues through parameter 5, not
arbitrary mixed paths. Even within that pattern, safety of P/4
segments is not a proof that an even return occurs before the budget
is exhausted. The logarithmic core can be unbounded as P grows, so
the fixed-cap word certificate cannot simply be applied at every P.

For fixed P with that core within a certified range, the existing word
exclusion can be combined with CORE and the appropriate physical
margin. A uniform proof for all core sizes, or a way to refresh root
precision with a strictly decreasing ancestry budget, is still needed.

Thus this supplies an infinite-family transfer rule and a retained-root
safety theorem through later collisions. It does not prove SQRT-EXIT,
bound the total canonical weight, or establish global non-halting.

## 7. Verification

    python -B work_global_rescue_ladder/verify_ladder.py

The script checks 880 exact rooted identities through formal depth 512,
256 rational-phase instances, sufficient-bound bases, and the three
phase-only collision examples. The long identity tests deliberately
use synthetic k=6 at later parameters; these are algebra tests, not
canonical F itineraries. All-scale scope comes from the displayed
identities and induction, not those samples.
