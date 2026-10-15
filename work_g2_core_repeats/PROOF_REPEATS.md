# Restrictions on repeated visits to the block core

2026-10-15. New continuation; not independently reviewed. No global
bound on core visits is proved.

## 1. A block is determined by its entry parameter up to its a output

Use the mixed-block representation of `work_g2_mixed_blocks`.
Starting at a safe entry parameter q, the b/c corridor is determined
by the earlier crossing table: each next b/c parameter and return
parity is independent of the outer odd base. The corridor either ends
at an even return, or reaches a first odd a-return. In the latter case
call q productive and denote its data by

    alpha_q, B_q, d_q, G_q, k_q;
    T_q=d_q+1+2k_q.

T_q is the exact F-step duration from this block entry to its a-output
chain. The output parameter can depend on high bits; the block data
preceding that output do not. As before, the entries considered here
are outputs of preceding odd a-returns, so the STATE relation applies.

## 2. Repeating the same entry forces an exact smaller output

Suppose two consecutive safe productive block entries have the same
parameter q, with chain values X0,X1. Their block data coincide. The
two-block identity reduces to

    X2=(alpha_q/2)X0+(1-alpha_q/2)X1+6T_q
      =X1+(alpha_q/2)(X0-X1)+6T_q.                (REPEAT)

Because X0 and X1 have valuation q, their difference is divisible by
2^(q+1). Since v2(alpha_q)=-G_q, the first two terms in the second
expression are both divisible by 2^(q-G_q). Put

    r_q=1+v2(T_q).

Whenever r_q<q-G_q, equation REPEAT proves

    v2(X2)=r_q<q.

It also proves safety of X2: the second block's output coefficient
valuation is sigma1-G_q-1>=q-G_q>r_q. No prior safety assumption for
X2 is needed.

**All-parameter conditional theorem.** Under earlier C1,C2 and the
audited small table, r_q<q-G_q for every productive q. Consequently
three consecutive identical productive block-entry parameters cannot
occur, and the output after two identical entries strictly decreases.

Proof for q>=1024: the preceding mixed-block estimates give
G_q<=3q/4 and d_q<2q^2, while 2k_q<q^2. Hence

    T_q<3q^2+1,
    r_q<=log2(2T_q)<log2(6q^2+2)<q/4<=q-G_q.

The strict exponential/polynomial inequality holds at 1024 and
persists because the logarithmic derivative of (6q^2+2)/2^(q/4)
is at most 2/q-log(2)/4<0. For q<1024, `probe.py` checks every
productive block against the exact crossing table. Parameters <=4
are terminal and do not give productive blocks. QED, relative to the
small finite certificate and earlier hypotheses.

The saved certificate additionally covers q through 4095. All 1304
productive parameters in this range have r_q in {1,2,4}:

| r_q | Productive q count |
|---|---:|
| 1 | 1239 |
| 2 | 8 |
| 4 | 57 |

Thus two identical entries in this finite range force a terminal next
chain, not merely a smaller parameter. The exact remaining duration
from the first of the two entries is

    2T_q + [1+tau(r_q-1)] + 1 <=2T_q+3.

The finite output classification is not extrapolated to every q.

## 3. Alternating entries: an exact finite exclusion

There is a stronger finite statement for the small core:

**Certificate theorem.** For distinct q,r in [5,255], no safe
continuation has five consecutive mixed-block entry parameters

    q,r,q,r,q.

If either parameter is nonproductive it cannot repeat in such a word.
There are 79 productive parameters in this interval, hence 6162
ordered distinct pairs to test. The proof uses the exact two-block
recurrence as a necessary arithmetic condition, retaining two
independent positive odd initial bases. It does not substitute sample
high-bit values or assume phase representatives.

Write X0=2^q U, X1=2^r V, with U,V odd. For the proposed alternating
word, propagate each subsequent X_i as an affine rational function
of U,V using POS from `work_g2_mixed_blocks`. To require v2(X_i)=j,
clear its power-of-two denominator D and impose

    D X_i = D*2^j (mod D*2^(j+1)).                (VAL)

These are exact linear congruences in U,V. They are necessary even if
one discards positivity, time compatibility and some source conditions.
Therefore proving them inconsistent excludes the actual word.

`period_two.py` maintains the full integer solution lattice, initially
(U,V)=(1,1)+2Z^2. For a new congruence, it substitutes the current affine
lattice, obtains c1*t1+c2*t2=b mod 2^a, and divides by the greatest
common power of two of c1,c2,2^a. A nondivisible right side proves
inconsistency. Otherwise an odd pivot is inverted modulo the remaining
power of two and the lattice is parametrized exactly. No branches are
discarded or sampled.

The first impossible word lengths are:

| Length | Ordered pairs |
|---|---:|
| 3 | 6146 |
| 4 | 8 |
| 5 | 8 |

Every pair is excluded by length five. The only pairs surviving length
three have smaller parameter 5 and larger parameter in
{17,54,90,125,161,198,234}, or the pair {8,139}. Starting at the larger
parameter fails at length four; starting at the smaller fails at five.

The full pair list and rejection lengths are saved in
`period_two_certificate.json`. The lattice update is separately
cross-checked 99 times against exhaustive solution sets modulo 16.
This checks the solver implementation; universal odd-base coverage of
each finite parameter pair comes from the lattice argument itself.

## 4. Implications and limitations

This adds actual restrictions on small-core repetition, where the
previous large-parameter return theorem alone was silent:

* identical adjacent block entries force a strict decrease at the next
  output under C1,C2, and terminate in the certified small range;
* a two-value alternating pattern cannot persist for five entries in
  the certified range, even with arbitrary odd high-bit bases.

These restrictions do not bound the number of visits to the core.
Longer-period words and nonperiodic words involving three or more
parameters have not been excluded. The finite alternating result also
does not cover unbounded core parameter values. A graph on parameters
alone can lose the lattice constraints accumulated along a path;
discarding those constraints would not preserve this proof.

A concrete next step is to use the same exact lattice propagation on
longer core words, retaining the constraints across visits, and seek a
structural bound on feasible word length. The present calculations
do not supply such a bound or a global termination theorem.

## 5. Reproduction

    python -B work_g2_core_repeats/probe.py
    python -B work_g2_core_repeats/period_two.py

The former supplies the small base for section 2. The latter proves the
finite exclusion in section 3 from necessary congruences. Neither
asserts actual orbit reachability of any tested entry word.
