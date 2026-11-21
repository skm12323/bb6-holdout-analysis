# Length of arbitrary all-a stretches on machine #1

Research draft, pending independent review. The canonical row data and the
scalar rules are those of PROOF_EXT §2 and BR. All assertions use only
rows already available in the prefix under consideration. In particular a
least-counterexample argument need not assume an infinite canonical calendar.

**Theorem.** Take N consecutive executed a-steps whose input chain
indices q are between 5 and M. The indices can change at every step.
Write d₀=3x₀/4−Θ₀ and b(d)=ceil(log₂(1+|d|)). There is an absolute
constant C, independent of the initial state, with

    N ≤ b(d₀) + C log₂(2+M).

An output at which the block ends need not satisfy the input cap. No
fixed-chain, prescribed word, gate, or return condition is imposed.
In particular the bound covers any number of switches between direct
trains without an intervening b/c step. This proof is independent of the
fixed-chain theorem in ALL_CHAINS.md.

## One-dimensional deviation with an advancing clock

The a-rule is x'=2Θ+6k−x/2, Θ'=Θ+3+6k, k=τ(q−1)/2.
Since 2^q exactly divides x, the integer d=3x/4−Θ satisfies

    d'=−(d+3k+6)/2,          v₂(Θ+d)=q−2.

A next a-input again has integral d. Let K be the maximum k in a
stretch. Iteration gives |d_i| ≤ 2^(−i)|d₀|+3(K+2). Thus, after
discarding at most b(d₀) steps, |d| ≤ 3(K+2)+1. The phase Θ strictly
increases by at least 3 each step. CLOCK gives 2K ≤ T(M), with the
same T as in ALL_CHAINS.md. In particular K ≤ M³ for M ≥ 256.
The canonical times τ(n) are nondecreasing in pointer order (the
time a pointer is read); hence among the odd-a inputs in a stretch
the largest input index attains the largest k. This also follows
from the first-read definition and queue order in PROOF_G6, lines 121ff.

## A finite computation for M ≤ 256

The oracle gives K ≤ 112 in this range. In the suffix just described,
use d exactly in [−343,343] and Θ mod 2^s. At a continuing input
Θ+d is divisible by 8. When its residue mod 2^s is nonzero, q is
determined. At residue zero allow every canonical odd-a q between
s+2 and 256. Advance Θ and d by the displayed rules. Count the present
step even if the next d is nonintegral or the next state cannot continue.
This directed graph contains every real path under the cap, since forgetting
higher phase bits adds choices. DFS checks every eligible vertex, rejects
a back edge, and computes the longest path in steps. The maximum is 7,
both at s=10 (87,936 vertices) and at s=12 (351,744 vertices).
An exact second enumeration keeps every chain q separately. At each
index impose Θ₀ ≡ 2^(q−2)−d_i−(Θ_i−Θ₀) mod 2^(q−1); all the moduli
are powers of two, so compatible cylinders intersect in the narrower one.
Integral x₀ is obtained by also imposing Θ₀ ≡ −d₀ mod 3. Enumerating
all 687 initial d values and compatible words gives an exact maximum
of **5** from within the bound, with the scalar witness 5,17,5,17,17.
This is a local integer state; reachability from S(J) is not needed.
Consequently N ≤ b(d₀)+5 for all such stretches. Reproduce with
`python -B work_direct_phase/verify_all_a.py`. Both precisions use the
same oracle and transition rules.

## A polynomial bound enabling induction

For dyadic L ≥ 256 prove N ≤ b(d₀)+L⁴ when M ≤ L. The finite result
starts the induction. For L ≥ 512 take h=L/2. After the initial b(d₀)
steps, the remaining suffix has |d| ≤ 4L³ and every clock increment
is between 3 and 9L³. At a high input q>h the integer center Θ+d is a
multiple of P=2^(h−1). The corresponding clock is within 4L³ of its
center. Any stretch of low inputs has length ≤ h⁴+L by induction,
since its initial |d| ≤ 4L³ and b(d) ≤ L.

Consider successive high inputs with no intervening high. Their clock
distance is at most 9L³(h⁴+L+1). Distinct centers would give distance
at least P−8L³, which is larger: already 2^(L/2−1)>L⁹ for dyadic
L ≥ 512 (at 512 directly, then by doubling). Hence all high inputs
share one center. Their entire inclusive span has length ≤ 8L³/3+1
by strict clock increase. The initial and final low stretches add at
most 2(h⁴+L). This totals less than L⁴; the case with no high input
is a single low stretch. This completes the induction.

## Logarithmic bound

Define F(M) as the supremum of max(0,N−b(d₀)) over all such stretches
with cap M (zero for an empty collection). The dyadic result gives
F(M)=O((M+256)⁴). Now for all sufficiently large M put
h=16 ceil(log₂ M). Work after the first b(d₀) steps. The same center
argument applies: the clock gap between different high centers is at
least 2^(h−1)−8M³, while a bridge of low inputs costs at most

    9M³(1 + b(4M³) + F(h)).

The first quantity grows at least as M^16/2−8M³; the second is
O(M³(log M)⁴). Thus all q>h in this suffix have the **same center**.
If it is nonempty, this set has a single input index m, since the center
is 3x/4 and its exact valuation is q−2. In particular its common label
k_m bounds all labels in the suffix by monotonicity of the clock table.

Discard at most b(4M³)=O(log M) further steps: the contraction now
gives |d| ≤ 3(k_m+2)+1 throughout the rest. All high clocks still
lie near the same center, now in an interval of width ≤ 6k_m+14.
Each high step advances the clock by 3+6k_m, so the number of remaining
high inputs is at most 1+floor((6k_m+14)/(3+6k_m)) ≤ 5. In particular
there are at most six low stretches. Each begins with b(d)=O(log M)
and has length at most b(d)+F(h). If the original suffix had no high
input, a single low stretch suffices and the second discard is unnecessary.
We obtain, for an absolute A and all sufficiently large M,

    F(M) ≤ A log₂ M + 6F(16 ceil(log₂ M)).

Since 6 log₂(2+h) ≤ (log₂ M)/2 for all sufficiently large M, strong
induction gives F(M) ≤ C log₂(2+M): take C ≥ 2A and enlarge it over
the finite initial interval using the polynomial bound. This proves the
stated theorem. The proof gives an asymptotic constant, not an evaluated
small constant for practical J.

## Consequences for global EXT

* No infinite all-a path can start at a finite integer state, even with
  unbounded input chains. For a prefix with maximum M, N is bounded
  by the theorem; at an index attaining M,
  2^(M−2) ≤ |Θ+d| ≤ |Θ₀|+N(3+6K)+|d₀|+3(K+2).
  For fixed entry data the right side is polynomially bounded in M,
  so M is bounded, and hence so is N.
* In the unresolved b/c-root cases of S(J), every later chain in a
  tie-free prefix has q ≤ g=floor(log₂(12J²)), and Θ ≤ 6J²+1.
  The scalar bound |x| ≤ 4Θ follows by induction from the a-rule and
  b/c MASS (see work_claude_sgexit/NOTES.md §5).
  Therefore b(d₀)=O(log J) and each all-a block costs O(log J)
  steps, including all its non-descents.
* Let R_J count the maximal nonempty all-a blocks in such a prefix.
  Since b/c steps descend, the number of non-descents is at most
  O(R_J log J), up to one endpoint if the transition out of the prefix
  is counted. In particular a uniform R_J=o(J/(log J)²) across the
  prefixes at issue would meet the L′ budget for all sufficiently large
  J. Any smaller J not covered by that asymptotic assertion would still
  require coverage or an explicit threshold. Counting R_J requires
  controlling **b/c-to-a restarts**; switches between chains inside
  an all-a block no longer cost an additional block. A b/c step resets
  the deviation recurrence, so this argument does not yet count these
  restarts or prove that S(J) is tie-free.
