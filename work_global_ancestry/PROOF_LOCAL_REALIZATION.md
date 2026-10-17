# Positivity and exact finite local realization from a fire-shaped state

2026-10-17. New conditional result, not independently reviewed.
This separates a finite word's local realizability from canonical
reachability. It does not prove global termination or a loss bound.

## 1. Positivity is forward invariant, even before valuation checks

Consider the cone

    Theta>=5, 0<x<=2Theta-5.                    (CONE)

At a productive A return with k>=1,

    x'=2Theta-x/2+6k, Theta'=Theta+6k+3.

Direct subtraction gives

    x'-(Theta'-1)=Theta-x/2-2>=1/2>0,
    (2Theta'-5)-x'=6k+1+x/2>0.

Thus its output lies strictly in

    Theta'-1<x'<2Theta'-5.                     (A-CONE)

At a B/C return, x'=r x+lambda, Theta'=Theta+3tau+3,
with 0<r<1 and 1<=lambda<=6tau+5. Therefore

    0<x'<2Theta+6tau<2Theta'-5.

CONE is preserved by every such map. These inequalities do not need
NT, C1, a parameter cap, or a periodic word. The upper bound on lambda
is the source mass bound; it must not be replaced by arbitrary constants.

At a mixed-block level the b/c corridor has x_c=alpha x+B,
Theta_c=Theta+3d, with 0<alpha<=1 and 0<=B<=6d. It preserves
CONE, and the final A gives A-CONE. This also proves positivity for
formal rational evaluations of block maps even if the chosen word
fails its integer valuation conditions. Such a rational evaluation
is only an inequality check, not a valid F itinerary.

## 2. Impose integer words and the exact fire identity

Let w=(q_0,...,q_n) be a fixed finite mixed-block entry word. Entries
before the last are productive and have actual earlier canonical
source kernels; the last is an output state whose next call need not
be executed. Let the exact fire projection of
`work_global_clock_words/PROOF_CLOCK_WORDS.md` be nonempty. It gives

    s_0=s_w modulo 2^K,
    Theta_0=3s_0+5, x_0=Theta_0-1,

and enforces every entry numerator's exact valuation. For every
nonnegative admissible s_0, the initial state satisfies CONE.
Section 1 then supplies strict positivity of both reconstructed
lambda components at every A-output entry:

    lambda_H=2Theta-x-5>0,
    lambda_D=x-Theta+1>0.

Thus checking positivity at more intermediate block entries does not
eliminate any additional clock lift of a fire-consistent finite word.
It is essential for a free local starting pair, but automatic once
this exact fire identity and the actual productive maps are imposed.

## 3. A complete criterion for finite SAFE LOCAL realization

Let G_* be total coefficient loss through the last entry, and Q the
largest entry parameter. Corridor parameters cannot exceed their
entry parameter. Choose an original pointer

    rho>G_*+Q,

and start the local pair map from

    H=(2^rho,3s_0+1), pending list empty, pointer rho.

This is a level-fire-shaped state: q_0>=1 makes s_0 even and the
head odd. It is not claimed to be the state of the canonical walk
at time s_0. Its mass identities hold, and its first chain numerator
has parameter q_0 by the fire projection.

At each intermediate chain, sigma=rho-G_t>=rho-G_*>Q. The strict
margin therefore holds. The accepted replay lemmas apply to the
known source kernels. B/C corridors have their prescribed copied
parameters and parities; each endpoint A produces the next entry
whose valuation is imposed by the clock projection. All integer
divisions are legitimate. Replay preserves positivity, and section
1 verifies it directly on the entry lambdas. Induction constructs
the entire specified finite word as a safe local continuation.

Consequently, under these fixed actual-source assumptions -- canonical
source kernels exist for every parameter <=Q, and the replay lemma
(PROOF_M Lemma 2.2) applies to the local fire-shaped state (empty pending
list, arbitrary rho) --

    nonempty exact fire-word projection
        iff existence of a safe LOCAL fire-shaped realization
            with some nonnegative clock and sufficient rho.

Necessity is the exact affine projection theorem; sufficiency is the
construction above. This upgrades that finite arithmetic test from
mere necessity to a complete local realizability criterion. It says
nothing about reaching the chosen starting pair from F's fixed initial
state. Increasing rho to guarantee margin does not supply that history.

## 4. What numerical clock bounds add, and what they do not

Each nonempty fire cylinder has arbitrarily large admissible s_0.
For a fixed word one can choose s_0 larger than G_*+Q and its fixed
duration, then take rho=s_0. This makes the initial numerical
constraints rho<=2s_0 and s_0<=rho^2 compatible with the construction.
Other fixed finite loss/deficit allowances can similarly be absorbed
by taking a larger member of the cylinder. This is an existence
statement for local starting states, not a claim that rho=s_0 is the
canonical fire pointer.

In contrast, at a first-failure candidate rho cannot be increased
freely: it must be <=G_*+q_n. The quadratic seed and finite endpoint
tests in `PROOF_CLOCK_WORDS.md` and `PROOF_FAILURE_BUDGET.md` remain
nontrivial precisely because they impose that upper bound. There is
no contradiction between local safe realizability and those tests.

The global missing information is the joint canonical origin of the
clock, pointer, and preceding epoch, or a uniform arithmetic bound
on the words that can accumulate loss. Positivity alone cannot turn
a nonempty rooted word cylinder into an impossibility proof. This
rules out a proposed shortcut; it does not show that a general rank
or stopping proof is impossible.

## 5. Checks

`positive_fire_lift` constructs a clock lift from the exact cylinder.
Its explicit affine positivity-threshold calculation agrees with
the universal sufficient threshold Theta_0>=5.

Run `python -B work_global_ancestry/verify_positive_lifts.py`.
It checks 8188 positive lifts of 4094 actual-source fire words,
including lifts with starting steps at least 2^8192; 4096 cone
updates in arbitrary formal block orders; and four independent
full pair-map microstep realizations starting at synthetic fires
with parameters 5,14,28,65. The latter execute 6,16,26,58 steps
respectively and check masses, positivity, margins, and the whole
mixed-block word. These starts are not asserted canonical.

The general local-realization theorem is proved in sections 1-3,
not extrapolated from those finite tests. The global goal and the
separate original-machine boundary/endgame obligation remain open.
