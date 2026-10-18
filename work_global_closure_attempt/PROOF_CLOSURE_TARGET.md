# A smaller first-counterexample alphabet and a global word-bound target

2026-10-18. **Conditional argument, accepted after three-way review
(reviews/global_clock_horizon_closure_review_record.md). Global closure is NOT obtained.** This note records both a sufficient all-scale theorem
that is still missing and a concrete obstruction to a tempting stronger
local assertion.

## 1. Inputs and the proposed missing theorem

Use the accepted CLOCK bound, PROOF_EGX Lemma T(2) and Theorem L's
by-product (with EXT below J, supplied by the strong induction; it uses C2-log), and the mixed-block identity in
`work_g2_mixed_blocks/PROOF_MIXED.md`. These concern valid prefixes and
already defined earlier source data; no future epoch termination is
assumed. Here EXT means strict tie-freeness, a sufficient condition for
global non-halting by Theorem U. We do not extend the beta-only formulas
through over-ties.

For integer Q>=64 consider the following **unproved** statement W(Q):

> Using the canonical source records at indices below Q, every
> congruence-feasible consecutive productive mixed-block word whose
> entries lie in [5,Q] has length at most 2^ceil(Q/2).

"Productive" means the b/c corridor reaches an odd a return. A word
retains the same initial integer variables and all intermediate exact
valuation constraints, as in `work_global_clock_words/clock_words.py`.
It is not a collection of independently chosen pairwise congruences.
This is a deliberately strong local statement: positivity, canonical
outer ancestry and the true-fire constraint are not imposed. A version
restricted to actually occurring symbolic-exit prefixes would also
suffice below, but is a different and weaker conjecture.

W(Q) is conditional on the source records being available. It does not
assume F exists at all indices: in its proposed application they are
strictly earlier than a putative minimal counterexample's source limit.

## 2. Logarithmic parameter cap from the near-linear clock

Fix J with F defined through X(J-1), let l=ceil(log2 J)>=64, and put

    b=ceil(log2 l), g=l+2b+7.

Then g+1<=2l. At l=64 this is immediate; the inequality persists on
each dyadic interval, and at the next power of two the jump of b by
one is dominated by the increase in l (the first endpoint is 65).

**Lemma CAP (new).** Every chain 1..t, t<=J, in a tie-free symbolic
exit prefix has parameter <=g. The same estimate holds for the next
candidate when the preceding chains are valid and the usual positive
beta mass bound is available at that candidate.

Proof. Write d_t for elapsed pair-walk time, excluding chain 0.
CLOCK and J<=2^l give, as in the clock-horizon note,

    tau(J-1)<=9 J l^2, d_1<=1+9 J l^2.

Induct over chains. If all preceding j's are <=g, their source times
are <=g^2 by C1, hence for t<=J,

    d_t <= 1+9Jl^2+(t-1)(1+g^2)
        <= 1+9Jl^2+J(1+4l^2) <=16Jl^2.

The mass bound 1<=beta_x<=6d_t-1 gives

    2^j <= beta_x <96 J l^2
         <=96*2^(l+2b) <2^(l+2b+7)=2^g.

In fact j<g; the weaker <=g suffices for the induction. The first
chain uses the same mass argument with d_1. All later source indices
are below g<J, so this uses no unavailable later table. QED.

This replaces the former first-prefix cap approximately 2log2 J by
log2 J+2log2log2 J+O(1). It is a finite-prefix bound, not a bound on an
arbitrarily long unproved continuation.

## 3. W(Q) at every scale would close EXT

**Conditional theorem (new).** If W(Q) holds for every Q>=64 with
available canonical source records, then EXT holds globally and the
machine never halts, using the accepted finite base and Theorem U.

Proof by strong induction on J. The accepted base covers J<K'. For
J>=K', assume the defining antecedent F through X(J-1), and EXT below
J. Put l,g as above, and L=floor(J/(3l)). The accepted Theorem L
by-product guarantees that the first L+1 exit chains, if they exist,
are tie-free: our use of ceil(log2 J) makes this budget no larger than
the accepted one using log2 J. Also L+1<=J, so CAP bounds their entire
parameter alphabet by g.

Let B=2^ceil(g/2). In a finite prefix with a odd a returns, the entries
after its first a return and before each subsequent one form a
consecutive productive mixed-block word of length a-1. W(g) implies
a<=B+1. This also covers a=0. Between a returns, b/c transitions
strictly lower the positive parameter by at least three; the looser
bound g transitions per corridor is enough. Counting a possible final
chain and final unfinished corridor, the total number of chains is at
most

    C=(B+2)(g+1)+2.                             (COUNT)

This applies to finite prefixes, without assuming they terminate. The
same bound accommodates prefixes cut inside a corridor.

For all integer l>=64,

    B <=32l*2^ceil(l/2), g+1<=2l,
    C <=128l^2*2^ceil(l/2),
    768l^3 < 2^floor(l/2).

The last inequality holds at 64 and 65 and persists separately in
each parity class: its right side doubles per increment of two,
while the cubic's factor ((l+2)/l)^3 is below two. The other bounds
follow from 2^b<2l (or <=2l) and the displayed definitions. Thus

    3l C <2^(l-1)<J,

where the final inequality is strict also when J is a power of two,
since l=ceil(log2 J). As C is an integer, C<=L. Existence of chain
L+1 contradicts COUNT. A first tie within those first L+1 chains is
already excluded by the by-product. Therefore the exit ends safely
and EXT(J) holds. The accepted Theorem U gives global non-halting.
QED, conditional on W.

The quantitative target is loose: a square-root-exponential bound in
the *small alphabet cutoff* Q would suffice. A polynomial bound would
be stronger than necessary. This is not a proof of W, and an observed
short maximum in any finite alphabet does not establish it.

## 4. Exact search and a longer local continuation

`probe_words.py` recomputes canonical source clocks up to index 999999
with S1 assertions, cross-checks the small selected sources against
a full pair walker, and checks every selected source against the
independent compressed canonical calendar with cutoff 64. It searches
all words in the selected pure-A
alphabet

    {5,8,14,17,27,48979,122436,367354}.

Shared integer lattices are retained at every extension. Lengths
2..9 have respectively 64,66,49,27,21,12,2,1 feasible words. None
continues within this selected alphabet to length 10. Branches outside
the alphabet remain open; this is NOT a finite-core certificate even
for all q<=367354. A broader initial search was abandoned for cost;
no result from it is used.

The longest word found is

    5,367354,5,17,5,122436,5,17,5.

Its source half-times are k(4)=1, k(16)=6, k(122435)=54614 and
k(367353)=163862. Its exact projection has 122439 clock bits and
367356 root bits. The script selects a positive integer lift in the
mass cone and executes nine independent pair macro returns, checking
mass, positivity, exact parameters and positive coefficient margins.
The minimum margin is 12 (for the chosen initial coefficient valuation sigma0=K+11; in general the margin is sigma0-max_i(i+q_i), positive for every sigma0>=K+1). The next parameter is 6.

The first entry is a local chain state. The remaining eight entries
are actual a-outputs of this local continuation, so there are eight
consecutive productive a-output entries. This rules out a uniform
seven-entry upper bound for arbitrary safe local states with these
actual sources. It does not refute the much larger W(Q) bound.

The exact true-fire projection of the nine-entry word is **empty**.
It cannot occur beginning at a fire. This does not decide whether a
word of this shape can occur later in a canonical epoch; the positive
local construction supplies no canonical ancestry. It is not a
non-halting counterexample and no safety failure was found.

## 5. Remaining gap

Neither the search nor CAP proves W(Q). Existing finite-core
certificates, local two-block descent, and period exclusions do not
control arbitrary words that leave and re-enter increasingly large
cores. The local nine-entry witness makes a constant-length shortcut
less plausible, while leaving scale-dependent bounds open.

A genuine closure still requires either an all-Q bound such as W,
or a bound restricted to canonically rooted symbolic exits. No such
bound has been supplied here. The new horizon from the previous turn
(work_global_clock_horizon) has since been accepted; this note does not enlarge it or close level 5.

## 6. Reproduce

    python -B work_global_closure_attempt/probe_words.py
    python -B work_global_closure_attempt/verify_cap.py

Outputs are `word_probe.json` and `cap_checks.json`. Algebra and
all-scale inequalities are proved above; finite computations support
the implementation and supply the explicit local example only.
