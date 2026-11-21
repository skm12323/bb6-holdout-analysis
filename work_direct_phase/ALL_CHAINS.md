# Every fixed-chain direct train is finite on the canonical calendar

Research draft, pending independent review. Machine #1. A return counted
here starts at a true gate on chain j, reads an odd a row at its output m,
and returns directly to a true gate on the same j. A run consists of N
consecutive such returns at one j. The last successor need not itself
return. Only completed returns with finite outputs are counted.

**Theorem.** For every j ≥ 5, every integer cap M on the outputs of a
nonempty canonical run, and every integer initial gate state in NF,

    N ≤ b(D₀) + M⁴,     b(d) = min{t ≥ 0 : 4ᵗ ≥ |d|+1}.

There is no fixed upper limit on M. In particular, an infinite direct
run from any one finite integer state is impossible, even if its outputs
are allowed to grow. Within a tie-free prefix of S(J) a single run has
O(log J · (log log J)²) returns, uniformly in j.

## Identities and the finite base

Use NF/JT from work_claude_trains/NOTES.md §5. To check its entry
condition m ≥ j+2, first observe from the two clock increments alone
that 6u is the difference of two odd gate coordinates o. Hence 3u is
integral, and u is integral since its denominator is a power of two.
At m=j the numerator 2k_j+1 is odd, which is impossible. At m=j+1
there is no consecutive odd-a pair for j<32 (verified below), and for
j≥32 the CLOCK estimate below already makes 0<u<1 at m=j+1.
Thus NF applies. For each returning index
i, let u_i=(k_j+1+k_{m_i})/2^(j−2), a positive odd integer, and let
o_i=(Θ_i+3k_j)/2^(j−2), z_i=o_i−x_i/2^j. Then

    v₂(z_i) = m_i−j+1,                  o_{i+1} = o_i+6u_i,
    4z_{i+1} = z_i+2(o_i+9u_i),        D_i = 3z_i−2o_i,
    4D_{i+1} = D_i+6u_i.

Write U=max u_i. Accepted CLOCK bounds U by (T(M)+1)/2^(j−2)
since j ≤ m_i ≤ M and 2k_q ≤ T(q). Here T(q)=(q−1) times
2 ceil(log₂(6(q−1)²+5))²+1345, with the whole sum as the multiplier.
For M ≥ 256, T(M) ≤ M³, as proved in PROOF.md (use the bound on the
whole multiplier). In particular U ≤ M³.

First take M ≤ 2^4000. For odd-a chains 5 ≤ j < 32, enumerate the odd-a
outputs j ≤ m ≤ j+4091 for which u is integral and odd. At j=5 there
are 114 (minimum 17), at j=8 there are 14 (minimum 139), and at every
other eligible j there are none. For 32 ≤ j ≤ 4096 there are none
because T(8192)+1 < 2^30 ≤ 2^(j−2). For j > 4096 use
T(j+4091)+1 ≤ (2j)³+1 < 2^(j−2). The last inequality holds at 4096
and the polynomial grows by a factor less than two per increment.

Thus m_i ≥ j+12 for every returning output. JT gives
3u_{i+1} ≡ u_i mod 4096 for 0 ≤ i ≤ N−3. At each j reduce its enumerated
labels modulo 4096. On the odd-residue orbits of this recurrence the
maximum number of consecutive vertices without two adjacent misses is
7 at j=5, 6 at j=8, and 1 for the empty label sets. These are exact
finite checks in verify_all_chains.py.

Apply the cut argument of PROOF.md to the first N−1 labels. Two adjacent
misses have m > j+4091, hence both z values are divisible by 2^4093.
Successive cut starts a,b have b−a ≤ 7 and

    6 Σ_{a≤i<b} u_i + 9(u_b−u_a) ≡ 0 mod 2^4092.

Its absolute value is at most 51U, and 64U < 2^4092 even using the
common bound (T(2^4000)+1)/8. Consequently u_b ≤ u_a/3.
The same bound gives U < 3^2540, so N ≤ 7(2+2539)+1 < 18000.
Every nonempty run has M ≥ 17 and 18000 < 17⁴. This proves the induction
base, independently of the size or sign of the starting clock.

## Induction across clock intervals

Fix j and use strong induction on the integer M. For M > 2^4000 put
e=ceil(log₂ M), h=j+16e, P=2^(16e), and B=M³. Since
2^(j−2) ≤ T(M)+1 ≤ M⁴, h ≤ 21e. In particular h⁴ ≤ M² and h<M:
(21e)² ≤ 2^(e−1) < M for e ≥ 4001, by induction on e.

1. From the D recurrence, |D_i| ≤ 4^(−i)|D₀|+2U. Drop at most
   b(D₀) initial returns. In the remaining suffix |D_i| ≤ 3B,
   and the integer clock w_i=2o_i increases by 12u_i per return,
   between 12 and 12B inclusive.
2. Call an output high if m_i>h. At such an index 3z_i is a multiple
   of P, and w_i=3z_i−D_i. Thus the high index lies within 3B of
   the center 3z_i on the clock line. Any contiguous low stretch in
   this suffix is itself a run with cap h, so its length is at most
   h⁴+b(D_start) ≤ 2M² by induction. Here b(D_start) ≤ 2e since
   4^(2e) ≥ M⁴ ≥ 3B+1. The low stretch is counted even when its final
   gate is the starting gate of a high return.
3. For two consecutive high indices (consecutive among the highs) at
   different centers the clock distance is at least P−6B. Their index
   distance is at most 2M²+1 by step 2. This is impossible because
   P ≥ M^16 and M^16−6B > 12B(2M²+1). Thus all high indices in the
   suffix share one center. The clock distance from the first to the
   last high is at most 6B. Their inclusive span contains at most B+1
   returns, using the lower increment 12. This also covers a single high.
4. The initial and terminal low stretches each have at most 2M²
   returns. With no high there is only one low stretch. In both cases
   the suffix length is at most 4M²+B+1 ≤ M⁴. Restoring the discarded
   returns closes the induction.

**Sharper count.** In that final induction step the center radius can
be taken to be 2U+1 once b(D₀) returns have been dropped. Thus the
span in step 3 has length at most 1+(4U+2)/12. Each exterior low
stretch has length at most (21e)⁴+2e by the already proved theorem.
This gives N ≤ b(D₀)+O(T(M)+(log M)⁴), with absolute constants. The
finite base is absorbed by a constant. Since T(M)=O(M(log M)²), this
is b(D₀)+O(M(log M)²) asymptotically.

## Two consequences and the remaining count

* **No infinite direct run.** Fix o₀,D₀ and apply the theorem to each
  nonempty prefix with its actual maximum M. Bounded M bounds the
  prefix length N. For unbounded M consider a prefix reaching M ≥ 256.
  At a maximizing index, |z_i| ≥ 2^(M−j+1) while
  3|z_i| ≤ 2|o₀|+12NM³+|D₀|+2M³. For the fixed j the former grows
  exponentially, the latter at most polynomially after substituting
  N ≤ b(D₀)+M⁴. Hence M cannot be unbounded either.
* **Within S(J).** The import g=floor(log₂(12J²)) bounds the outputs
  of a tie-free prefix. At a starting gate Θ ≤ 6J²+1 and |x| ≤ 4Θ
  (work_claude_sgexit/NOTES.md §5, the scalar mass estimate).
  Since D=o−3x/2^j and k_j ≤ T(g)/2, b(D)=O(log J). Substitution
  into the sharper count gives O(log J · (log log J)²) per run.
* **Total budget.** For B_J disjoint maximal runs the completed direct
  returns covered here cost O(B_J log J · (log log J)²) gates at their
  returning chain. The small-gate budget is of order J/log J. Thus
  B_J=o(J/((log J)²(log log J)²)) would make this contribution lower
  order. The number of interruptions, gates outside these runs, and the
  terminal transition that could first tie still need separate control.
  This theorem does not establish EXT or change the machine horizon.

Run `python -B work_direct_phase/verify_all_chains.py` from the repo root.
The executable checks the finite base and selected boundary arithmetic.
The induction and unbounded-output conclusion are symbolic arguments.
