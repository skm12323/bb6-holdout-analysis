# Starting the global induction at J = 1024

This is a second assembly of the mixed-bridge proof from a single small
source prefix. It proves strict safety for every J beginning at 1. It
replaces the finite tower horizon in the outer induction and the large
numerical starting range in the quadratic crossing-clock bound. It
retains the repository's structural pair-map, crossing, replay, mass
and endgame lemmas. The new proof is pending independent review.

## One chronological finite input

Generate the original-pair crossings X(0),...,X(1022) using
`work_m/verify_m.py:Xdata`, which checks both S1 and S2 before
each chain division in the raw walk. As each row appears, store only
the prefix reached so far. For J=n+1:

* Check the full symbolic recursion `sym_exit` on that prefix,
  beginning with u=(1,0), D=(2^(J−1),−1). It compares the two
  valuations before division. Compare every chain, return type, and
  total loss with the scalar walk starting at (J,1,0); also check
  q+Γ<J before continuing the scalar walk.
* Compare every source field used by the bridge-base enumerator against
  the raw pairs. For example at odd b/c sources the multiplier is
  (c_H+2c_Y)/2^(n+1), the offset is λ_H+2λ_Y+3, and its valuation
  gives the next input. At every row the time is
  (λ_H+λ_Y−1)/3 with λ_Y=0 when no tail is present.

The 1023 exits split as 389 with zero chains after the root, 586 with
one, and 48 with two. All terminate with an even head. The maximum
loss is 4. The same rows support the 325 productive blocks and
the exclusion of seven consecutive low entries in PROOF.md §3.
On the raw prefix τ(n)≤n, τ(1022)=910, and max τ(n) for 0≤n≤62
is 51. Reproduce with `python -B work_mixed_bridge/verify_source_prefix.py`
and `python -B work_mixed_bridge/verify_bridge.py` from the repo root.
The J=1 exit is the directly even special case.

## Quadratic clock on the maximal defined prefix

Use the structural next-original lemma and the per-corridor replay
calculation of work_global_clock/PROOF_CLOCK.md §§2–3. Suppose C1,
τ(m)≤m², holds through the reached crossing n. If the next crossing
is reached, put G=ceil(log₂(6n²+5)). The first corridor parameter is
at most G. At each large input j≥64 the next b/c parameter is at most
j/2, and a replay costs 1+τ(j−1)≤j² by the earlier clock bound. The
sum of large costs is at most 4G²/3. At small inputs j≤63 a replay
costs at most 52 by the raw table. Continuing b/c steps lower the
positive parameter by at least three. At most 21 such small-input
replays (20 b/c steps 63,60,…,6 plus a possible a endpoint), plus one
final step, suffice; charging 22 of them gives the rounder 22·52+1=1145
used below. These are upper bounds for the same corridor in the
next-original lemma, including prefixes whose next inspection is the
first undefined step. Therefore

    τ(n+1)−τ(n) ≤ 4G²/3+1145.

At n=1022,1023 we have G≤23, and this bound is <2n+1. For n≥1024,
take k=floor(log₂ n)≥10. Then G≤2k+5 and

    4(2k+5)² + 3435 < 3·2^(k+1).

At k=10 this is 5935<6144. The left side grows by less than a factor
of two per increment of k, which proves the inequality at every
larger k. Thus the clock increment is <2n+1 and C1 propagates to
every reached crossing. No exit-length hypothesis or extent of future
definedness entered this induction.

## Closing the interval from 1024 onwards

Take J≥1024, assume F defined through τ(J−1) inclusive and all earlier
strict exits safe whenever their defining prefixes exist. The required
earlier conditional exits include the small cases verified above. At a
type-c crossing q−1 with q≥1024 the parameter J_W of its earlier fire
is at most log₂(3(q−1)²+4)<J for q≤J. The needed earlier source rows
are present by the crossing/replay rules. Thus strict C2-log and the
block estimates of PROOF.md §§1–4 apply. In particular their finite
base uses rows only through X(1022), even when J=1024.

Use the direct first-tie proof in PROOF.md §5 with l=ceil(log₂ J),
g=2l+4. The clock bootstrap 1+g²≤J holds for J=1024 directly.
For l≥11, 1+(2l+4)²≤2^(l−1)<J (at 11 the left side is 677, and
it grows by a factor less than two). Hence the prospective q≤g
bound is available with all earlier chains safe.

* **When g≤1023**, the already-safe inputs contain at most seven odd
  a transitions: between A of them are A−1 consecutive productive
  entries under cap 1023, and only six are possible. Each completed
  corridor costs at most 3. The unfinished b/c tail costs at most g;
  the transition into the candidate costs at most g. Including root
  loss ≤4l+4 and the candidate q≤g gives

      q+Γ ≤ 4l+4 + 7·3 + 3g = 10l+37 < 2^(l−2) < J/2.

  The exponential inequality holds at l=10 and persists by doubling.
* **When g>1023**, l≥510, so the all-scale estimate of the direct
  first-tie proof gives q+Γ≤32l²<J/2.

This discharges the strict comparison before the candidate division in
both ranges. Positive loss bounds the number of chains for each fixed
J. Strong induction now proves strict safety for every J for which the
required prefix exists. In particular it supplies the EXT hypothesis
of the accepted Theorem U.

## Downstream use of the finite data

In the continued-definedness argument of PROOF_EGX §5(b), a large
level fire at pointer ρ has s=τ(ρ)≤ρ² by C1. For ρ≥1023,
3ρ²+4<2^ρ, hence J=v₂(3s+4)<ρ and the fire is safe. The inequality
already holds at 32 and persists by doubling. Smaller fire pointers
are covered by the raw defined prefix. At a later exit chain, repeat
Theorem U(b) with strict safety at its own J: the real coefficient
valuation is ρ−Γ, and the chain index is <J−Γ. Earlier calls are
defined by replay, S2 is structural, and the epoch ends. The canonical
pointer advances without bound. For v≥3, EGX identifies the endgame
with the just-proved S(v); E1–E4 then give safe singleton-to-singleton
excursions. The v=1,2 excursions are directly even as in E1. The
accepted blank-tape singleton reduction concludes non-halting.

This changes the finite base required by this chain of implications.
It does not constitute a fresh independent review of the structural
lemmas that identify the pair process with the original machine.
