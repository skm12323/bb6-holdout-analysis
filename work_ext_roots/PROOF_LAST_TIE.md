# Complete last-step filtering for a fixed EXT prefix

2026-10-18 continuation. **Accepted after three-way review; EXT remains open.**
This removes the unbounded final-valuation branch for one fixed prefix.
It does not bound the set of possible prefixes.

## 1. Setting and the previous outer-index endpoint

Suppose J>=128 is a least strict EXT counterexample, with F defined
through X(J-1) and EXT at every smaller index. The first exit chain
is type b/c; type a is covered by accepted RA. The first tie can only
be the output of an odd a return, since b/c copies preserve safety.

Fix the productive mixed-block prefix before that output. Let

    E=sum (G_i+1) >=1, T=sum T_i,

be its total coefficient loss and elapsed call/return time. Denote
the candidate final valuation by q and put M=E+q. Earlier entries
are strictly safe. `PROOF_EXT_ROOTS.md` derives

    J<=M+2 for type b, J<=2M for type c.

In the b case with J>=128, M>=126 so M+2<=2M. Thus J<=2M holds in
both cases. Its c-case input C2-log uses EXT below J; this is not an
unconditional estimate for arbitrary invented source tables.

## 2. All possible last valuations after a fixed prefix

The elapsed symbolic time at the candidate is d=1+tau(J-1)+T.
The positive beta mass bound (available at the first candidate before
executing it) gives

    2^q <= beta_x <=6d-1
        <=24(E+q)^2+6T+5
        <=48E^2+48q^2+6T+5.                    (FIXED-SIZE)

Only C1 at the reached outer source and the preceding J<=2M were
used. For every integer q>=15,

    48q^2 < 2^(q-1).

This holds at 15 and persists because ((q+1)/q)^2<2. Subtracting this
term in FIXED-SIZE yields 2^(q-1)<48E^2+6T+5. A convenient slightly
loose integer endpoint is therefore

    q <= Q_fixed(E,T)
      := max(14, bit_length(48E^2+6T+5)).       (FIXED)

No source data at the final parameter q are needed to obtain this
bound or evaluate that output: the putatively unsafe chain is not
executed.

## 3. A last-valuation bound depending only on loss

Every preceding chain has parameter below J. Each call costs at most
1+J^2 by C1 together with the accepted finite base (tau(n)<=n for n<=10^8; CLOCK gives
tau(n)<=nP(n)<=n^2 above that), and each completed chain transition loses at least one
coefficient unit. Consequently T<=E(1+J^2)<=E(1+4M^2). (Chain 1's call is part of the first block's
T and is paid for by that block's loss G+1>=1, so it is already counted.) The preceding
mass inequality strengthens to

    2^q <=24(E+1)(E+q)^2+6E+5.                (LOSS-SIZE)

If q>=E and q>=20, its right side is at most

    96(q+1)q^2+6q+5 < 2^q,

a contradiction. The strict inequality holds at 20; the positive
cubic increases per increment by at most (q+2)(q+1)/q^2<2. Thus either
q<=19 or q<E. In the latter case M<2E and

    2^q <96(E+1)E^2+6E+5 <=203E^3, E>=1.

Hence

    q <= Q_loss(E):=max(19,floor(log2(203E^3))). (LOSS)

For a fixed prefix the implemented bound is min(Q_fixed,Q_loss).
This is analytic for all parameters, not a sampled truncation.

As a further consequence, for a fixed cumulative loss E, all possible
least-counterexample outer indices satisfy

    J<=2(E+Q_loss(E)).

The words with that loss are still not bounded independently of E.
Allowing E to grow leaves infinitely many cases; the implication is
not an induction proving that none of them occurs.

## 4. The complete finite last-step procedure

For each q from 1 to the proven bound:

1. Require a strict new loss-plus-parameter record M>R, where
   R=max(previous E_i+q_i). Otherwise it cannot be the first tie.
2. Compute the exact shared-variable cylinder of prefix+(q). Reject
   inconsistent words, without replacing joint variables by independent
   congruence representatives.
3. Inspect every J in the finite source range. A b source must satisfy
   R+3<=J<=M+2; c sources lie in 128<=J<=2M. At the actual source,
   Gamma=1+epsilon and Gamma+R<J<=Gamma+M are required.
4. Substitute the actual canonical values
   Theta=3tau(J-1)+4, x=Theta+lambda_Y into the complete word cylinder.
   If they satisfy it, independently replay the scalar block maps,
   checking earlier entry valuations/margins and final mass.

`last_tie_filter.py` implements this procedure. A missing canonical
source raises an error rather than being regarded as excluded. Passing
is reported as a necessary candidate; no certificate of the surrounding
canonical history is manufactured.

There is an optional diagnostic mode for J<128. It does NOT apply the
large-J final-valuation theorem to those cases. Instead it enlarges
the diagnostic endpoint using their separate C1 bound

    2^q<=6*127^2+6T+5,

and inspects every 2<=J<128. These small indices are already covered
by the accepted base; this mode tests the implementation, not progress
beyond the known horizon.

## 5. Finite canonical check and a noncanonical positive control

**Scope (added after review).** In the J>=128 mode no source index is reachable for this alphabet (max M=16, so 2M<=32<128): every large-J case is removed by the record test or the cylinder. All source/congruence rejections and the positive control below are J<128 diagnostics, a range already certified. The large-J source path is untested by data; `last_tie_filter.inspect` now raises on a missing canonical source unless called with noncanonical=True (used only by the positive control).

The verifier builds the 18 productive actual kernels with parameters
5..63. All congruence-feasible productive prefixes over this alphabet
exhaust at length six. Their counts by length 1..6 are

    18, 324, 80, 59, 21, 2  (504 total).

For each prefix the verifier tests ALL final valuations permitted by
the analytic bounds, including final q outside that productive alphabet
and without requiring the final q to be productive. The large-J bound
is at most 14 here; small-J diagnostics expand enumeration to 16.

There are 8064 final-parameter checks; 7920 fail the new-record test,
113 further words are inconsistent. The remaining checks inspect
3906 source indices, including 1209 odd b/c records; 48 satisfy the
margin interval, but none satisfies the complete canonical source
congruence. No candidate survives. This is a finite method check
inside already certified ranges, not a new horizon theorem.

To ensure that the implementation is not an always-reject filter,
replace ONLY the source X(9) by this invented local type-c record:

    time s=27, head H=(64,7), pending Y=(448,75),
    original index n=9, epsilon=3.

It obeys the local mass identities

    64+448=2^9, 7+75=3*27+1,

and the numerical C1 bound 27<=9^2. Its source chain is (960,160),
with coefficient valuation six and lambda valuation five: locally safe.
The first S(10) state has base (30,5) and defect tail (544,3).
The next call uses the ACTUAL X(4)=(16,7), with half-time k=1:

    image head=(480,87),
    next chain=(480+2*544,87+2*3+3)=(1568,96).

Both components have valuation five. This is an exact tie. The filter
correctly retains the candidate J=10, prefix (5), final q=5, E=1.

**This source is not X(9) on the canonical orbit.** It violates the
actual time/pointer/source correlation, despite satisfying those
local mass, parity, C1 and first-chain safety conditions. It is not
a counterexample to EXT, and no actual machine halt is asserted.
It demonstrates why replacing canonical sources by arbitrary records
obeying only loose local inequalities cannot close EXT.

## 6. Remaining gap

A fixed prefix now has finitely many possible final valuations AND
outer indices, with a complete exact filter for its last unsafe step.
Safe final outputs can start further prefixes with larger loss, and
their number and length are not controlled here. Therefore this does
not establish global termination, a global word-length bound, or EXT.

Reproduce:

    python -B work_ext_roots/verify_last_tie.py

The script also checks 18,156 instances supporting the analytic
inequalities and independently verifies the positive control by pair
replay. The symbolic arguments above establish the all-scale bounds.
