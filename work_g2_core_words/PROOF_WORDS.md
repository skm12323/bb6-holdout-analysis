# Exhaustive short-word closure inside a fixed block core

2026-10-15. New computational certificate, not independently reviewed.
This proves finite-core statements for arbitrary odd high bits; it is
not a global bound on core visits separated by large excursions.

## 1. What is being enumerated

Use mixed-block entries immediately after odd a-returns, as in
`work_g2_mixed_blocks`. A parameter is productive if its deterministic
b/c corridor reaches another odd a-return rather than an even return.
There are 325 productive parameters in [1,1023]. All other parameters
in this interval end the epoch after their b/c corridor and even return.

For consecutive entries X0,X1 the necessary recurrence is

    X2=(alpha/2)X0+(1-beta/2)X1+C,
    C=B/2+6+6k1+6k2+6f-E/2.

The two block types fix these coefficients from the known crossing
table. Start every ordered pair of productive parameters q,r with

    X0=2^q U, X1=2^r V, U,V odd.

Positivity, initial time compatibility and some source restrictions are
discarded, giving an overapproximation of actual trajectories. The
integer lattice of all allowed U,V is retained along the entire word.
No later step resets the bases to fresh independent symbols.

## 2. Exact branching and exhaustion

Every later X is affine rational in U,V with a power-of-two denominator.
After clearing denominator D and substituting the current solution
lattice, write its numerator as c+a*s+b*t. Put

    v=v2(c), z=min(v2(a),v2(b)).

If v<z, its valuation is fixed at v; the output parameter is v-v2(D).
Otherwise the numerator ranges through every multiple of 2^z, so every
finite valuation at least z is allowed by this affine constraint.

For each productive output parameter j<=1023 that remains possible,
the algorithm adds the exact congruence

    D X = D*2^j (mod D*2^(j+1))

to the full two-dimensional integer lattice. Its update divides by the
common power of two and inverts an odd pivot, as described in
`work_g2_core_repeats`. This preserves all solutions, not just selected
residue representatives. Any possibility of j>1023 is explicitly
recorded as an escape and not treated as a terminating branch.

`word_search.py 1023 16` exhausts the frontier at length seven:

| Productive word length | Congruence-feasible words |
|---|---:|
| 2 | 105625 |
| 3 | 25438 |
| 4 | 17378 |
| 5 | 6271 |
| 6 | 504 |
| 7 | 0 |

All 155216 processed nodes are checked. To keep the artifact small,
`words_1023.json` records detailed edges only for the 7099 nodes with
productive children or an escape; the 148117 verified terminal leaves
are represented by counts and can be regenerated. The search stops
because the frontier is empty, not because its requested depth limit
of 16 is reached.

**Finite-core theorem.** No valid continuation has seven consecutive
productive mixed-block entries all at most 1023. This excludes all
words of that length, including aperiodic ones, not just short cycles.

The candidate-valuation pruning is cross-checked against unpruned
congruence solving at 128 nodes in this run. A separate full run with
cap 63 checks it at all 486 processed nodes and also exhausts at length
seven. The underlying lattice solver was previously cross-checked
against exhaustive modular solutions; these checks support the
implementation, while the lattice argument supplies odd-base coverage.

## 3. Tracking escapes strengthens the stopping statement

The cap-1023 certificate has exactly 165 nodes allowing an output above
the cap, distributed as follows:

| Length of already matched productive prefix | Escape nodes |
|---|---:|
| 2 | 66 |
| 3 | 66 |
| 4 | 33 |
| 5 | 0 |
| 6 | 0 |

These are arithmetic possibilities, not asserted reachable escapes.
There may also be an escape directly after the first entry, before the
two-entry initialization; the table makes no claim about that case.

**Five-entry closure.** If a safe valid continuation has already reached
five consecutive productive block entries with parameters <=1023, then
the next output cannot exceed 1023. If it is productive, there are six
matched entries; the following output again cannot exceed 1023 and
cannot be productive, because the length-seven frontier is empty.
Thus, provided these last outputs have sufficient physical margin,
the epoch ends after at most two more productive blocks and one
terminal corridor, counted from the fifth entry.

This conclusion does not assume that all future outputs remain below
the cap: the absence of escapes at depths five and six proves that
fact for the remaining continuation.

## 4. Explicit safety and time budget

The same exact crossing table gives, for parameters <=1023:

    productive block: duration <=909, coefficient loss <=3;
    terminal corridor: duration <=912, coefficient loss <=4.

Durations for productive blocks stop at their output chain. A terminal
corridor's duration includes its final even-return step. All b/c
parameters within a corridor decrease, so no intermediate parameter
exceeds its entry parameter.

Suppose the fifth entry in section 3 has coefficient valuation

    sigma5>=1034=1023+1+2*3+4.

At every remaining prospective chain the valuation is then at least
1024, strictly larger than its parameter. The absence of escaping
outputs and the exhausted frontier justify the continuation without
assuming its safety in advance. Replay uses earlier crossing data as
usual. Therefore the epoch ends within

    2*909+912=2730 F steps

of the fifth entry. The remaining coefficient loss is at most 10.
The necessary earlier-prefix and compatibility hypotheses remain in
force; arbitrary formal words need not correspond to physical states.

A related confined-suffix bound is at most

    6*909+912=6366 F steps,

with loss at most 22, from the first entry, whenever no earlier escape
occurs. Initial sigma>=1046 is a sufficient margin for that confined
argument. This latter statement explicitly needs the no-early-escape
condition; it does not follow for every starting core state.

## 5. Scope of the progress

The previous result only ruled out equal-parameter persistence and
two-parameter alternation. The present certificate bounds *all*
consecutive productive words in this fixed core and proves an actual
safe stopping rule once five consecutive core entries have occurred
with enough margin.

It does not bound the total number of core visits separated by larger
entries. A possible unresolved path could repeatedly escape within
its first few core entries, later return, and escape again. The earlier
two-large-block theorem limits certain large excursions but does not
exclude this repeated pattern. Parameters in the global logarithmic
core can also exceed 1023 for sufficiently large outer scales.

Thus the remaining problem is now more explicit: control escape and
reentry while preserving the lattice/source correlations, and extend
the fixed-core bound uniformly with the outer scale. Merely restarting
the current certificate with fresh U,V on each reentry loses precisely
the information that could bound the number of repetitions.

## 6. Reproduction

    python -B work_g2_core_words/word_search.py 1023 16
    python -B work_g2_core_words/word_search.py 63 16

An earlier cap-255 run is also saved; it exhausts at length seven.
No independent review was initiated in this work.
