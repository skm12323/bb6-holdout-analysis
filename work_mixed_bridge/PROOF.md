# A proposed global non-halting proof for BB(6) holdout #1

Machine `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`.
Research draft, pending independent mathematical review. The claim is
relative to the repository's accepted reduction and source estimates.
It uses strict EXT throughout. The intervening fixed-chain and all-a
drafts in work_direct_phase are not dependencies.
The alternative assembly in [SMALL_BASE.md](SMALL_BASE.md) starts the
outer proof at J=1024 using the same source rows as the mixed-word base.

**Claim.** At the strict least-counterexample induction step, every finite
congruent word of productive mixed-block entries with indices in [5,Q]
has length at most Q for Q ≥ 64, using the available earlier source rows.
This implies strict EXT and, by the accepted Theorem U, non-halting on
the blank tape. The new argument is in §§2–4. In particular, it includes
reentries after excursions above the finite base and changes of b/c type.

## 1. Coordinates, source scope and one block

Fix J in the strict EXT induction. Assume F defined through τ(J−1)
and EXT below J as in PROOF_EGX §§5–6. Only use available canonical
source rows below the root in the word bounds. A *productive entry* is
an a-output x with q=v₂(x) whose deterministic (possibly empty) odd b/c
corridor reaches an odd a-step. A block executes that corridor and its
final a-step. It goes from this entry to the next a-output. The word
lists productive **inputs**; its final output need not be productive.
A contiguous subword inherits a single clock and all its realized
valuation conditions. We need only integer lifts of the whole word.

Write Θ for the repository's phase. In one block, the corridor sends
x to αx+B, increases Θ by 3d, and incurs coefficient loss G. By MASS
and the scalar rules, 0<α≤1, 0≤B≤6d, and multiplying α and B by
2^G clears their denominators. Indeed each row has a dyadic multiplier
of valuation −(1+ε) and integral offset. If the terminal a-row has
half-clock k, the entire block has loss l=G+1 and phase increment
t=3(d+1+2k) ≥ 3. Its map is

    x' = −αx/2 + 2Θ + c,     Θ' = Θ+t,
    c = 6d+6k−B/2,           0 ≤ c ≤ 2t.

This is the scalar productive block of work_g2_mixed_blocks/PROOF_MIXED.md
and work_global_clock_words/clock_words.py, on the actual available
source prefix. In particular 2^l clears all coefficients and constants.

For cap M ≥ 1024 every such block satisfies

    t ≤ 6M³,          l ≤ 9 log₂ M + 3.                       (1)

For the time bound the b/c input indices strictly decrease, at most M
rows including the endpoint are read, and CLOCK's quadratic bound C1
gives 1+τ(q−1) ≤ 1+M². For the loss bound, at q≥1024 an individual
b/c step costs at most 4 log₂ q+4 and its successor is at most
log₂(6(q−1)²+5) ≤ 2 log₂ q+3 ≤ √q. The first bound for c is the
corrected strict C2-log of PROOF_EGX §4: its containing epoch has
parameter J_W ≤ log₂(3(q−1)²+4) < J and is available by the outer
induction (cf. work_ext_roots/PROOF_EXT_ROOTS.md §4); for b the cost
is 2. The successor bound uses MASS and C1. The square-root inequality
holds at 1024 and its margin increases thereafter. Hence the sum of the
logarithms of the high b/c inputs is at most 2 log₂ M, including a
possibly truncated last term. Their total cost is at most
4.4 · 2 log₂ M, since log₂ q ≥ 10. Either one further a-step costs 1,
or a productive tail starting at q ≤ 1023 costs at most 3 in total
by the finite certificate below. This proves (1). No bound here is
obtained by assuming EXT at J.

## 2. A bridge between two high entries

Suppose low words with all entries ≤ h have length at most F. Call an
entry high if q>h. Between successive high entries there is a bridge
of at most F+1 blocks, starting at the first high and omitting the
second. Suppose every such bridge has total coefficient loss s ≤ S
and total phase increment t ≤ T. Composition gives

    x_end = a x_start + β Θ_start + γ,        Θ_end = Θ_start+t,
    1 ≤ β ≤ 2,       0 ≤ γ ≤ 2t,
    2^s a,  2^s β,  2^s γ  are integers.                       (2)

For the first block use §1. To append a block with multiplier −α/2,
increment u and constant c, update β to 2−αβ/2, and γ to
2t−αγ/2+c. The new γ is between 0 and 2(t+u). Multiplication by
the product of the two clearing denominators clears the new map.
This proves (2), regardless of corridor shapes and intervening clocks.

Put b_i=2^s β and c_i=2^s γ for bridge i (using its own s).
At both endpoints x is divisible by 2^(h+1). In the cleared map
this implies

    b_i Θ_i + c_i ≡ 0 mod 2^(h+1).                             (3)

There is no division modulo a power of two. For the next bridge use
Θ_{i+1}=Θ_i+t_i. Subtract b_{i+1} times the first congruence
from b_i times the second. The integer

    Z_i = b_i b_{i+1} t_i + b_i c_{i+1} − b_{i+1} c_i

is divisible by 2^(h+1). By (2), |Z_i| ≤ 12 T 2^(2S). Consequently
under the explicit separation condition

    12 T 2^(2S) < 2^(h+1),                                    (4)

Z_i vanishes as an ordinary integer. Put p_i=c_i/b_i=γ/β.
Then 0≤p_i≤2t_i and p_{i+1}=p_i−t_i≤p_i/2. This is one equality
for each pair of adjacent bridges along the **same** word. It charges
every intervening low block, including any b/c restart, to the change
in p. No common type, slope or denominator at different bridges is needed.

With r bridges, if r≥2 then p_{r−2}≥t_{r−2}≥1 (indexing from zero),
while p_0≤2T. Thus r≤2+floor(log₂(2T)). There are r+1 high entries,
and at most F lows in each intervening or exterior low stretch. Including
the zero- and one-high cases, any word under this separation has length

    N ≤ (F+1)(4+floor(log₂(2T))).                              (5)

The argument applies to every finite word, without assuming termination
of the surrounding epoch or imposing any bound on its entry phase.

## 3. Base certificate and first enlargement

For h=1023 take F=6. The finite-core computation in
work_g2_core_words/PROOF_WORDS.md enumerates a superset of all allowed
words at that cap. There are 325 productive inputs. For lengths 2 through
7 the counts are 105625, 25438, 17378, 6271, 504, 0. Maximum productive
block loss is 3. Both the original lattice enumerator and the forward
cylinder verifier in this directory reproduce these numbers. The latter
builds the blocks from the calendar oracle and replays each on two
integer lifts using the scalar map.

Specifically, the new verifier stores Θ=t+2^b v and x=r+p v+2^a u
over the 2-adic integers. Imposing x≡2^q mod 2^(q+1) restricts v
on the overlap of the two moduli; for each permitted v the remaining
modulus for x is the stronger one. The block updates this cylinder
directly. Its odd multiplier on the free column is a 2-adic unit.
This overcovers all integer entry states and uses a different recurrence
from the original enumeration of consecutive x pairs. An escape above
the cap is handled in §2, not counted as an actual termination.

Take M=2^20. A bridge has at most one initial block of loss ≤183 by
(1) and at most six low blocks of loss ≤3. Thus S=201 suffices and
T=42 M³ < 2^66 suffices. Inequality (4) follows from
4+66+402 < 1024. By (5) the word length is at most 7(4+67)=497,
in particular at most √M=1024.

## 4. The infinite sequence of scales

For e=20·2^n, h=2^e, inductively suppose F=√h bounds all words under
cap h. Take M=h²=2^(2e). Each bridge contains at most one high block
and F low blocks. By (1) one may take

    S = 18e+3 + (9e+3)√h,        T = 6(√h+1)h⁶.

Put r=√h. On the entire grid r≥48e+64: equality holds initially,
and squaring r gives at least 48(2e)+64. This elementary invariant
gives 4S≤h, 6(r+1)≤h and 2S+7e+4<h+1. These imply T≤h⁷
and (4). From (5)

    N ≤ (√h+1)(7e+5) ≤ h = √M.

The last inequality follows from the same invariant. The polynomial
implications for arbitrary e,r satisfying it are checked in audit_bridge.py.
This closes the induction. The bounds are uniform over partial source tables:
apply them to words using only rows already available. Rounding the
cap upwards does not require querying rows between the actual maximum
and the rounded cap. The base rows are already available at the outer
induction step J≥K′.

For every integer Q≥64 the word length is at most Q. Up to 1023 use 6;
from 1024 to 2^20 use 497. For larger Q choose the least cap in the
sequence ≥Q. Its square root is the previous cap, strictly below Q.
In particular the reviewed sufficient bound W(Q), namely 2^ceil(Q/2),
holds in the strict outer induction in which it is needed.

## 5. Return to the original machine

Use the accepted finite base below K′ and fix a putative induction step
J≥K′ with F defined through τ(J−1). Write l=ceil(log₂ J),
g=2l+4 and L=floor(J/(3l)). Use just the prefix estimate inside the
accepted proof of Theorem L (PROOF_EGX §6): through chain L+1, whenever
it exists, previous safety implies d_t≤2J², j_t≤log₂(12J²)<g and
excludes a first tie there. This estimate precedes the use of LIN-EXIT
in that proof. Rounding log₂ J up only shortens the prefix inspected.
Here l≥64, g<J. At a c row q−1 the containing fire occurred earlier
at pointer ρ_W<q−1, has J_W≤log₂(3(q−1)²+4)<J, and its required source
prefix through τ(J_W−1) is already present (PROOF_EGX §§4–6,
including the finite base for small J_W). Thus §1 can be used on this
prefix before proving EXT(J). Rounding the inner cap never enlarges the
set of source rows actually read.

Count chain inputs j_1,...,j_n with n≤L+1, excluding chain 0. Only the
n−1 transitions **between** these inputs are counted. Let A be the
number of odd a transitions among them. Between successive a transitions
the output of the first starts a productive block ending at the output
of the second. This gives A−1 consecutive productive entries when A≥1.
Therefore A≤g+1 by §4, also if A=0. Each of the at most A+1 intervening
or exterior b/c corridors has at most g transitions since the positive
indices strictly decrease and start at most g. Hence

    n ≤ 1 + A + (A+1)g = (A+1)(g+1) ≤ (g+2)(g+1).

This handles a final unfinished corridor without reading the next row.
For integer l≥64, 3l(2l+6)(2l+5)<2^(l−1)<J: the first inequality
holds at 64 and the positive cubic grows by a factor less than two
on each increment. Thus n≤L. Taking n=L+1 if that chain exists gives
a contradiction. A first tie earlier is excluded by the prefix
estimate, so the exit ends safely. This argument does not require the
sharper CAP bound or an estimate on the yet-to-be-executed transition.

Strong induction proves strict EXT. The accepted PROOF_EGX §5,
Theorem U, implies that F is defined forever, its pointer tends to
infinity, and #1 never halts. No assertion of independent review
of the new bridge or its global assembly is made here.

### Direct first-tie bound and quantitative margin

There is also a direct assembly without invoking Theorem L or its
prefix budget. Keep the same outer induction and definitions of l,g.
At a candidate t≥1 assume only the preceding chains are safe. If
t≥2, then t−1≤Γ_{t−1}<J by the positive per-step loss and strict
safety; hence t≤J. The same bound is immediate at t=1. Starting
with d₁=1+τ(J−1), successively apply C1 and transported Lemma T(2)
as in PROOF_EGX §6: as long as the preceding indices are ≤g,

    d_i ≤ 1+(J−1)² + J(1+g²) ≤ 2J²,
    1 ≤ β_{x_i} ≤ 6d_i−1,    j_i ≤ log₂(12J²) < g.

Here 1+g²≤J for l≥64. The mass estimate is the one at the prospective
chain with previous divisions valid; the division at i is not used.
This inductively bounds all indices through t, including the candidate.

Write K_g=9 log₂(max(1024,g))+3. The root loss is at most 4l+4 by
C2-log on earlier epochs, also covering types a and b. For t≥2 count
only the transitions between the already safe inputs j₁,...,j_{t−1}.
As above their A odd a-steps satisfy A≤g+1. Partition these transitions
into A corridors ending in their respective a-steps and a possible
final b/c-only tail. The first corridor may start at j₁; estimate (1)
depends only on its source rows and also holds there. Each completed
corridor costs at most K_g. Along the tail, 1+ε≤q−q' at every b/c
step by S1, so the sum telescopes to at most g. Charge the single
transition into the candidate separately: at source q≤g its loss is
1+ε(q−1)≤q≤g. No productive word constraint was imposed on its
output. Finally j_t≤g. Thus, also at t=1 by the root-only estimate,

    j_t + Γ_t ≤ 4l+4 + (g+1)K_g + 3g ≤ 32l² < J/2.

Indeed g≤3l, log₂(max(1024,g))≤l, and 32l²<2^(l−2) for integers
l≥64 by doubling. The candidate has a strict margin even before its
division. This excludes a first tie; positive loss excludes infinite
continuation for fixed J. Keeping K_g in the displayed estimate gives
an all-scale O(log J · log log J) bound on the coefficient loss and
the number of exit chains of S(J). This separate assembly uses the
same bridge theorem, MASS, C1, strict C2-log, and Lemma T. Its margin
is relative to the coefficient valuation J−Γ_t of the symbolic exit.

## Reproduction and review points

The finite [core-word review](../reviews/g2_rest_review_record.md)
accepts the capped enumeration, including its allowance for escapes.
The [MASS review](../reviews/origin_contraction_review_record.md) accepts
the b/c multiplier and offset bounds used in §1. The [mixed-block
review](../reviews/g2_frontier_review_record.md) concerns the earlier
local formulas. None of these reviews assessed the new bridge induction.

Run `python -B work_mixed_bridge/verify_bridge.py` from the repository
root. The original base solver is `work_g2_core_words/word_search.py`
with arguments `1023 7`. The infinite induction is algebraic.
With z3-solver installed, run `python -B work_mixed_bridge/audit_bridge.py`
for universal checks of the local polynomial obligations, the squaring
invariant, and the outer prefix count. This script does not formalize
the repository's machine reduction or certify the source lemma imports.
Both enumerators were run for this draft. In addition, the new verifier
replays 661128 → 17 → 661128 → 857036 on the exact scalar map:
the two bridges give (p₀,t₀,p₁)=(2654187,1769472,884715) with p₀=t₀+p₁.
This tests the determinant sign on a non-vacuous pair of adjacent
bridges, with distinct lengths and phase coefficients. This lift is
local; the proof does not require its reachability from the blank tape.
For adversarial review, check (i) both denominator losses in (4),
(ii) the sign of the elapsed clock in (3) and the ordinary-real bounds
on γ/β, (iii) C2-log on earlier sources under *strict* EXT below J,
and (iv) the productive-input count in a prefix cut inside a corridor.
