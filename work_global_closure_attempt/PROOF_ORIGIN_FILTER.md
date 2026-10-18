# Exact phase-origin filter and a larger finite word search

2026-10-18 continuation. **Accepted after three-way review (as local/conditional results). Global EXT and the all-Q
word bound W remain open.** The phase filter below is an all-word
algebraic implication; its applications to particular words are finite.

## 1. Project a word onto its initial phase defect

The accepted clock-cylinder construction, for any feasible productive
mixed-block word, gives all integer solutions in the form

    Theta = t mod 2^H,
    x = p Theta + r mod 2^K, K>=H, p even.

Here x and Theta are the SAME initial chain numerator and clock used
throughout the word. This is a projection of exact valuation constraints;
it does not impose positive components, physical coefficient margins,
or canonical ancestry.

Define the exact phase defect c=Theta-x. Then:

**Phase-origin lemma.** There is an integer lift with defect exactly c
if and only if

    c = (1-p)t-r mod 2^H.                       (ORIGIN)

Proof. Substituting x=Theta-c into the anchor gives
(1-p)Theta=r+c mod 2^K. Since p is even, 1-p is odd and invertible.
Thus a unique Theta class modulo 2^K exists for every c. It intersects
the prescribed clock class precisely when its reduction modulo 2^H
is t. Multiplying by the odd 1-p gives (ORIGIN). QED.

This is necessity and sufficiency for the integer congruences only.
For a fixed c, arbitrarily increasing Theta and x=Theta-c does NOT in
general put the state into the physical mass cone: positivity must
still be checked separately.

For an exact shifted real fire V(C,delta), the underlying real fire
has Theta_C-x_C=1. Hence its initial defect is c=1+delta. ORIGIN
implies the necessary offset restriction

    delta = (1-p)t-r-1 mod 2^H.                 (SHIFT)

Let R be its representative in [0,2^H). Every compatible offset has
absolute value at least min(R,2^H-R). This bound allows arbitrary
initial clocks and odd bases satisfying the word constraints; fixing
the actual fire numerator can only add restrictions. Sufficiency
for reaching an actual shifted canonical fire is NOT asserted.

The usual true-fire test is delta=0. Thus SHIFT retains strictly more
information than a yes/no rejection of the true-fire constraint.

## 2. The previous nine-entry word needs a huge offset

Let P=122436 and take the word

    (5,367354,5,17,5,P,5,17,5).

The existing exact solver and the new incremental solver agree on
H=122439, K=367356 and the anchor slope p=4. Substitution in ORIGIN
gives

    c = -2^122438 + 3244677 mod 2^122439.

Therefore any realization beginning at an exact shifted real fire
satisfies

    delta = -2^122438 + 3244676 mod 2^122439,
    |delta| >= 2^122438 - 3244676.              (OFFSET-9)

The negative displayed representative is nearest zero, since its
magnitude is strictly below half the modulus. In particular delta=0
and delta=-1 are impossible. This excludes the word starting directly
at a type-b exit entry V(fire,-1). Its first parameter is only 5, so
that entry is already shallow in the accepted theory; no new deep
case is silently claimed here.

This does not exclude the same word starting later in an epoch, after
previous a returns have changed both numerator and phase, or beginning
at a shifted non-fire chain of a type-c source.

## 3. Incremental exact solver for pure a returns

After i consecutive a returns, write

    2^i x_i = (-1)^i x_0 + B_i Theta_0 + C_i,
    Theta_i = Theta_0+3d_i.

Initially B=C=d=0. A return with half-time k gives

    B_(i+1) = -B_i + 2^(i+2),
    C_(i+1) = -C_i + (6d_i+6k)2^(i+1),
    d_(i+1) = d_i+1+2k.

The requested valuation q_i is exactly one affine congruence on x_0
modulo 2^(i+q_i+1); the root coefficient is always +/-1. Adding this
congruence to the largest previous anchor yields one clock congruence,
using the same intersection proof as the accepted clock solver.
`fast_a_words.py` implements these integer recurrences. It never
replaces the shared variables by fresh independent values.

Performance optimizations preserve exactness: modulo powers of two is
computed with bit masks; low-64-bit disagreement rejects a branch
before constructing a high-precision residue; surviving branches still
undergo the full-precision check. There is no probabilistic equality
check, precision truncation of surviving branches, or rounded arithmetic.

## 4. Exhaustion of two selected alphabets

The small run reproduces every feasible-length count of the previous
independent lattice search on eight sources, with 308 additional
comparisons against the general clock solver, including rejections,
full cylinder fields and fire projections. Its free maximum is nine;
its fire-compatible maximum is two.

The broad run selects the 37 odd a sources with parameters <=128,
plus the sources below 10^6 selected by v2(3k-2)>=15 or v2(k+7)>=15,
and parameter 367354: 64 sources total. This deliberately targets
known resonance classes, rather than sampling all sources uniformly.
Each source is checked by both the lambda walk and the independent
compressed canonical calendar (B=64).

The search tries 1,050,560 extensions. Free feasible counts are:

| length | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| count | 64 | 4096 | 3654 | 3013 | 2245 | 1947 | 1008 | 287 | 82 | 12 | 6 |

No feasible word has length 12 **within this alphabet**. The depth
limit 14 was not reached and the stack exhausted. With the exact
fire relation, only 64 one-entry and two two-entry words survive;
there is no three-entry pure-a word in this alphabet beginning at a
fire. This statement does not exclude an exit taking another parameter
or a b/c transition immediately afterward.

One longest free word is

    (5,17,5,17,661128,17,661128,857036,5,17,5).

The general clock solver independently confirms its exact cylinder.
A positive physical pair lift executes all eleven a-return macro
steps, with minimum coefficient margin eight (for the chosen sigma0=K+7; positive for every sigma0>=K+1); the next parameter is
six. The last ten entries are genuine a-outputs of that local path.
The construction retains positivity and both mass identities at every
step, using the independently checked canonical source records.
No canonical ancestry of the outer state is constructed.

Its fire projection is empty. Its minimum possible absolute offset
from an exact real fire, as constrained by SHIFT, has bit length
661126. The exact large value is reproducible; the JSON records its
hash rather than a hundreds-of-thousands-digit decimal expansion.

## 5. What this does and does not establish

The finite search strengthens the warning against a universal small
constant bound on arbitrary local words. The origin lemma supplies
an exact arithmetic reason these examples cannot begin at a small
shift of a real fire. It applies to mixed-word cylinders too, although
the enlarged enumeration here covers pure-a words only.

There is still no upper bound on the phase shifts generated by an
arbitrary canonical mixed history, and no proof of the all-Q word
bound W from the previous note. A bound for one selected alphabet
does not justify replacing Q by an arbitrary larger parameter.

The remaining useful direction is to relate SHIFT to a quantitative
bound on actual ancestry, rather than discarding that ancestry when
passing to arbitrary local states. OFFSET-9 is a necessary origin
cost, not an upper bound on total ancestry or a global stopping rank.

## 6. Reproduce and scope of checks

    python -B work_global_closure_attempt/search_a_cylinders.py small
    python -B work_global_closure_attempt/search_a_cylinders.py broad
    python -B work_global_closure_attempt/verify_origin_filter.py

The origin verifier compares 26,832 defect tests against direct
substitution into the complete anchor/clock system, rechecks both long
words with the general solver, verifies OFFSET-9 exactly, and checks
the two positive pair lifts. It does not simulate the entire copied
microstep trajectories; their replay justification is imported from
the accepted source-image lemmas. The conclusions were accepted in the 2026-10-18 three-way review.
