# A period-clock divisibility obstruction at every parameter scale

2026-10-16. New conditional proof work; not independently reviewed.
This controls repeated mixed-block words. It does not bound arbitrary
aperiodic itineraries, total epoch weight, or global non-halting.

## 1. Exact data attached to a productive block

Use the mixed blocks of `work_g2_mixed_blocks/PROOF_MIXED.md` and
`work_g2_core_repeats/PROOF_REPEATS.md`. A productive entry parameter
q has a deterministic b/c corridor ending at an odd A return. The
earlier canonical crossing table fixes

    alpha_q, B_q, d_q, G_q, k_q,
    T_q=d_q+1+2k_q > 0,

where G is corridor coefficient loss, d is corridor time, k is the
endpoint half-time, and v2(alpha_q)=-G_q. The exact block map is

    x' = -(alpha_q/2)x + 2Theta + c_q,
    Theta' = Theta+3T_q,
    c_q=6d_q+6k_q-B_q/2.                       (BLOCK)

This follows directly by composing the corridor x_end=alpha_q x+B_q,
Theta_end=Theta+3d_q with its A endpoint. It is valid at a resonance.
The next entry parameter need not be determined by q alone.

The first result below needs only these exact maps and defined earlier
sources. C1/C2 enter only when bounding the block times and losses.
It is a necessary condition on a valid repeated word; freely choosing
a word or affine variables does not assert canonical reachability.

## 2. Eliminate the unknown clock and affine constant over a period

Fix a productive word w=(q_0,...,q_(m-1)), m>=1, and define

    T=sum_i T_(q_i), E=sum_i(G_(q_i)+1).

Composing BLOCK over w gives rational a,b,c such that

    x_m=a x_0+b Theta_0+c,
    Theta_m=Theta_0+3T,
    v2(a)=-E,
    v2(b)=G_(q_0)+2-E.                        (MONO)

For the last valuation, b is a sum of terms

    2 product_(i=t+1)^(m-1) (-alpha_(q_i)/2), 0<=t<m.

Their valuations are strictly increasing with t, since each omitted
factor has valuation -(G_(q_i)+1)<=-1. The first summand therefore
has unique minimum valuation 1-sum_(i=1)^(m-1)(G_(q_i)+1), exactly
the value in MONO. No real-size estimate is used.

Suppose the word is traversed twice and the three boundary entries
have the same parameter q_0. Set

    Delta_0=x_m-x_0, Delta_1=x_(2m)-x_m.

Their differences are divisible by 2^(q_0+1), since each x at these
entries is 2^q_0 times an odd integer. Subtracting the two affine
period equations cancels c and the unknown starting clock:

    Delta_1=a Delta_0+3bT.                     (DIFF)

The first two quantities in DIFF have valuations at least q_0+1
and q_0+1-E respectively. Hence

    v2(3bT)>=q_0+1-E,
    v2(T)>=q_0-G_(q_0)-1.                     (DIV)

The case of a zero difference is included by v2(0)=infinity. This
does not assume nonzero drift or approximate contraction.

**Period-clock theorem.** If a valid productive entry word contains
three consecutive copies www, then

    v2(T)>=Z(w),
    Z(w)=max_i [q_i-G_(q_i)-1].                (PERIOD)

Indeed apply DIV at each cyclic starting position i in the first
copy. Its three matching entries occur at i,i+m,i+2m, all within
www, and the two intervening block maps have the same cyclic word
and the same T. All necessary transitions end before the final
entry. Thus the argument does not require a fourth copy.

This is an all-word, all-parameter necessary condition. It retains
the shared clock and initial state throughout the repetition.

## 3. Exponential minimum period at large parameter

Now assume earlier C1, C2 and M2' (the hypothesis list of PROOF_MIXED
section 4) and that every entry is safe; safety is what makes the corridor
data depend only on q (PROOF_MIXED section 2). For productive q>=1024,

    G_q<=3q/4, T_q<3q^2+1.

For q<1024 the canonical finite table gives T_q<=909. Thus if a
word has maximum parameter Q>=1024, every block in it satisfies
T_q<3Q^2+1, including its small entries. Consequently

    T<m(3Q^2+1), Z(w)>=Q/4-1.

PERIOD requires 2^Z(w)<=T, yielding

    m > 2^(Q/4-1)/(3Q^2+1).                  (LENGTH)

Thus a repeated pattern containing a large parameter must have an
exponentially long period in that parameter. This controls three
consecutive repetitions; it does not require an infinite cycle.

In particular, for Q>=1024,

    2*(3Q^2+1)<2^(Q/4-1),

so two-parameter alternation cannot persist for six entries if
either parameter is at least 1024. The inequality holds at 1024;
the logarithmic derivative of (3Q^2+1)/2^(Q/4-1) is at most
2/Q-log(2)/4<0 thereafter.

## 4. Closing the small base: no six-entry alternation at any scale

The verifier generates the exact productive block data for every
q<1024 directly from `work_m/verify_m.py`'s crossing construction.
There are 325 such parameters. For all 105625 ordered pairs,
including equal parameters, it verifies

    v2(T_q+T_r)<max(q-G_q-1,r-G_r-1).          (PAIR)

The minimum strict gap is three. Only the integers q,G_q,T_q are
needed; there is no search over selected high-bit values. PAIR
contradicts PERIOD for the word (q,r).

**Uniform alternation corollary.** Under the earlier-source bounds
specified in section 3, no valid productive block continuation has
six consecutive entry parameters

    q,r,q,r,q,r

for any positive integers q,r. Nonproductive parameters cannot occur
in such a continuing word. Small productive pairs are excluded by
PAIR; all remaining pairs are excluded by LENGTH.

This extends the earlier finite alternating-word restriction to
unbounded parameters, with a six-entry bound rather than the sharper
five-entry bound previously checked on the smaller finite range.
It makes no claim that a general six-entry word is impossible.

## 5. A wider short-period corollary and its limitation

A stronger numerical form of the same inequality is

    2^233 * (3Q^2+1)<2^(Q/4-1), Q>=1024.

At Q=1024 this is equivalent to 3*2^20+1<2^22; monotonicity then
proves the full range. Thus LENGTH excludes www at any such Q
whenever m<=2^233.

For Q<1024, import the accepted finite-core certificate
`work_g2_core_words/PROOF_WORDS.md`: seven consecutive productive
entries all below 1024 are impossible. This excludes www for m>=3.
For m=2 use PAIR. For m=1, PAIR with q=r implies
v2(T_q)<q-G_q-1, so DIV already excludes three identical entries.

**Conditional short-period corollary.** A valid productive block word
cannot contain www with 1<=|w|<=2^233, at any parameter scale, under
the preceding hypotheses and the cited finite-core certificate.

This large period threshold is a structural restriction, not a new
unconditional time horizon. It does not bound the length of an
itinerary which avoids such triple repetitions. In particular the
finite number of parameters under a bootstrap cap does not force
an arbitrary word to contain a short consecutive triple repetition.
No bound on total core visits follows from this corollary alone.

## 6. Verification and relation to the remaining global gap

Run `python -B work_global_period/verify_period.py`.
The script recomputes all 105625 small ordered-pair inequalities,
checks MONO and DIFF on 1676 affine words (3352 exact identity
instances, word lengths through 32), and checks bases and a finite
sample of the analytic inequalities. Sample words are algebra tests,
not asserted realizable itineraries. The all-word proof is section 2.
The seven-entry finite-core theorem is imported from its existing
accepted certificate, not re-proved by these new tests.

This work arose from trying to bound the joint-certificate constants.
For repeated words, subtraction eliminates those constants entirely
and yields the global period obstruction. For an aperiodic sequence,
the successive block maps differ and this cancellation does not give
DIV. A general stopping/loss proof still needs control of those
changing maps, or a reason canonical long itineraries must develop
a prohibited repetition. Neither has been established here.
