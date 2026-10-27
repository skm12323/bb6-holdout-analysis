# Scope and proof checks performed by the author

2026-10-27. This is **self-review**, not an independent audit or an
accepted repository review record.

1. **Normalization attack.** Checked R against full pair coefficients,
   not just a normalized source odd part. The divisor is 2^(n+1),
   since j=n+1. This gives b=3/4 and c in (1/2,1). Dividing by 2^n
   would invalidate the contraction argument.
2. **Wrong positivity import.** Only canonical W lambdas are taken
   nonnegative. The translated beta can have either sign; CONE is
   proved for its zero-defect constant b, with beta=qD+b.
3. **Rational valuation attack.** The size-to-valuation estimate is
   applied to QZ, a dyadic rational. The factor Q and budget QB are
   essential and were retained in both proof and exact tests.
4. **Circular strictness attack.** Strictness is assumed only for the
   incoming run. Its coefficient loss gives a margin lower bound
   independent of the next output. Positivity and size of Z are
   then proved without assuming v2(Z)<mu; only afterwards is the
   gate valuation determined. Intermediate uniformity in odd U is
   justified by the same strict-run coefficient gap.
5. **Lift-bit attack.** At the initial chain j=y, the usual strict HP
   inequality with P=y does not apply. The proof handles the first
   step explicitly (same numerator; phase difference divisible by
   2^y) before invoking the difference induction. Actual integer
   lifts include gate examples, not solely already-terminal paths.
6. **Vacuity attack.** Added rational gate starts at y=146935 and a
   non-bare NT gate 2424159 -> 17 -> 18. Integer lift checks contain
   12 gate events. These are constructed local states, not claimed
   canonical S(J) entries.
7. **Known obstruction.** Replayed 126 small-start O2 examples. They
   keep v2(Z)=mu and arbitrary even output valuation. The new theorem
   explicitly requires a large anchor and a nonempty strict run;
   it does not contradict or dispose of this obstruction.
8. **Global overclaim attack.** Source availability and the loss bound
   are explicit assumptions. Neither inexpensive phase descriptions
   after arbitrary histories nor closure of the post-gate tail is
   proved. No accepted file or horizon has been changed.

Suggested independent review targets: applicability of the imported
per-source loss bound inside the least strict-EXT induction; the
rational HP extension through the first step; and whether the local
conditions can be maintained by a useful actual-source grammar.
