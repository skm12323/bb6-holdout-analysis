# Finite unsafe endpoints and an exponential loss budget

2026-10-17. New conditional proof work; not independently reviewed.
This continues `PROOF_CLOCK_WORDS.md`. It bounds which final parameters
can witness a first safety failure, including unbounded escape branches.
It also expresses a safe coefficient-loss budget in terms of the fire
parameter. It does not prove an epoch stops within that budget.

## 1. First-failure setting

Let a valid canonical epoch fire have parameter J, pointer rho, and
time s_0. Thus x_0=3s_0+4=2^J U with U positive odd, and J<rho.
Consider its first hypothetical unsafe A-output candidate. Write E
for the cumulative coefficient loss from the fire, t for elapsed F
time to the candidate, and q for its parameter. Its coefficient
valuation is rho-E, so a safety failure requires

    rho<=E+q=:M.

Earlier returns and replay sources are defined. The accepted safety
lemmas exclude a first failure inside replay or at a b/c copy, and
preserve S2; the remaining candidate is S1 at an A output. The mass
identity is available at this state before its unsafe update is
attempted (A-CONE, PROOF_LOCAL_REALIZATION section 1, which does not need
the output to be safe). It gives

    2^q<=x<=6(s_0+t)+5.                       (MASS)

C1 at the root gives s_0<=rho^2<=M^2. No completed-epoch assumption
is made. The source C1 hypotheses below concern only earlier calls.

## 2. A logarithmic endpoint bound for a fixed prefix

Fix the productive mixed-block prefix before the final candidate.
It determines E and t exactly from its earlier source table. Combining
MASS with C1 at the root,

    2^q<=6((E+q)^2+t)+5
        <=12E^2+12q^2+6t+5.

For every q>=12, 12q^2<2^(q-1). The inequality holds at 12 and
persists because ((q+1)/q)^2<2. Therefore, with C=12E^2+6t+5,

    q<=Q_fixed(E,t):=max(11,1+floor(log2 C)).    (FIXED)

The slightly loose integer endpoint avoids a special case when C is
a power of two. This is an all-q theorem, not a sampled cutoff.

Consequently a fixed prefix has only finitely many possible unsafe
final valuations. No source data at those final q values are needed:
the putative unsafe chain is not executed. The preceding block's
exact exit formula and the fire constraints suffice to test it.

This does not bound the possible SAFE outputs of the prefix, or the
source parameters that a later continuation of such an output may use.
Removing that distinction would turn a valid pruning rule into an
invalid termination argument.

## 3. A bound depending only on cumulative loss

Assume C1 also at every earlier call of this prefix. Every preceding
chain parameter is smaller than rho, hence smaller than or equal to
M. Each nonterminal top-level return costs at most M^2+1 F steps and
loses at least one coefficient unit. There are at most E such returns,
so

    t<=E(M^2+1).

MASS now gives

    2^q<=6(E+1)(E+q)^2+6E+5.                  (SIZE)

If q>=18 and q>=E, the right side is at most
24(q+1)q^2+6q+5, which is strictly less than 2^q for q>=18.
The base is direct; thereafter the positive polynomial increases
by at most ((q+1)/q)^3<2. This contradiction shows

    either q<=17, or q<E.

In the second case M<2E and SIZE is strictly smaller than

    24E^2(E+1)+6E+5<=60E^3, E>=1.

Thus every first-failure candidate satisfies

    q<=Q_loss(E):=max(17,floor(log2(60E^3))).   (LOSS)

This does not assume C2, NT, a return-count bound, or periodicity.
The implementation uses min(Q_fixed,Q_loss). Each bound is necessary
under its stated clock hypotheses.

## 4. Root-parameter safety budget using C1 alone

Since x_0=3s_0+4>=2^J and s_0<=M^2, a failure also requires

    2^J<=3(E+Q_loss(E))^2+4.                   (ROOT-SIZE)

Define, for J>=16,

    B_0(J)=2^(floor(J/2)-3).

For 1<=E<=B_0, monotonicity of Q_loss and a direct base check at
floor(J/2)=8 give

    Q_loss(E)<=max(17,3floor(J/2)-4)<=B_0.

The last inequality persists as floor(J/2) increases: its exponential
right side doubles, while the linear left side increases by three.
Consequently

    3(E+Q_loss(E))^2+4
      <=3*2^(2floor(J/2)-4)+4 <2^J,

contradicting ROOT-SIZE.

**C1-only loss-budget theorem.** Under the stated earlier C1 and
source-validity hypotheses, no first safety failure in a canonical
epoch with J>=16 can occur at cumulative coefficient loss
E<=B_0(J).

The budget counts coefficient loss, not returns. A single c-copy
may consume several units and jump past it. It does not imply that
the epoch actually lasts B_0 steps, that its parameters remain small,
or that it ends before the budget is exhausted.

## 5. Stronger budget using the new global-clock lemma

The separate `work_global_clock/PROOF_CLOCK.md` proves on the maximal
defined canonical prefix (including the candidate inspection)

    tau(n)<=n P(n),
    g(n)=ceil(log2(6n^2+5)), P(n)=2g(n)^2+1345.

That proof is new and not independently reviewed; the following
strengthening explicitly depends on it, in addition to section 3.

For J>=64, a first failure must have E>=18: otherwise the section-3
dichotomy (Q_loss(17)=18) gives
q<=17 and rho<=E+q<=34, contradicting rho>J. Thus q<E and rho<2E.
Applying the clock lemma at the root,

    2^J<=3s_0+4<=6E P(2E)+4.                 (CLOCK-SIZE)

Put

    B_1(J)=floor(2^J/(128J^2)), J>=64.

If E<=B_1, then 2E<=2^J and g(2E)<=2J+4. Therefore

    P(2E)<=8J^2+32J+1377<=9J^2, J>=64.

The last quadratic inequality holds at 64 and its difference increases.
It follows that

    6E P(2E)+4<=(54/128)2^J+4<2^J,

contradicting CLOCK-SIZE.

**Clock-based loss-budget theorem.** With that additional clock lemma,
no first safety failure occurs at E<=B_1(J) for a reached canonical
fire of parameter J>=64. No C2 or strict-descent hypothesis is used.

For J=64 this gives B_1=2^45, whereas B_0=2^29. These are safe-loss
thresholds conditional on the cited arguments, not newly verified
run lengths or an unconditional horizon extension. Unlike the earlier
retained-lambda-root theorem, this result does not say that the full
itinerary is independent of the root's high bits. It uses the actual
canonical clock/physical margin instead.

## 6. Complete unsafe-last-branch check and what remains

`all_last_failure_candidates` takes a fixed productive fire prefix,
computes the finite endpoint bound, and tests every q from 1 through
that bound with the exact fire projection and necessary root-pointer
interval from `PROOF_CLOCK_WORDS.md`. It also checks the exact candidate
mass bound 2^q<=6(s_*(w)+t)+5. Parameters above the bound are excluded
analytically, rather than left as unexplored unsafe escape branches.

The verifier applies this to all 504 nonempty congruence-feasible
productive prefixes in its alphabet below 64 (including one-entry
prefixes). The largest endpoint bound needed is 11; no necessary
failure candidate remains. This is a check of this proof-search method
against a known finite base, not a new global theorem. The existing
synthetic clock test still leaves its intended candidate q=9, showing
that the filter's nonempty branch is exercised too.

The additional `verify_failure_budget.py` checks 16274 inequality
instances and records examples of B_0 and B_1. The elementary
monotonicity arguments above, rather than these finite samples,
establish the infinite-range inequalities.

The outstanding global task is unchanged in substance but has a
larger available safety budget: control the total coefficient loss
or prove a stop before that budget is exceeded. The new bounds do
not control the number of different prefixes, and safe large outputs
still lead to unbounded source-parameter branches. In particular,
finite branching for the LAST unsafe step is not finite branching
or termination of the entire proof search. No global G2/non-halting
conclusion is asserted.
