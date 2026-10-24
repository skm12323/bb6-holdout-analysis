# Initializing the denominator reserve at low-deficit bare-tie gateways

**Review status (2026-10-24):** reviewed via the work_gateway_trains three-way review (reviews/gateway_trains_review_record.md, group 2). Accepted as a conditional result [A-cond]+[B] (b-parent formula [B]); not a global ranking function.

2026-10-21. **UNREVIEWED proposed lemma.** This removes the separate
initial-potential assumption for the specific entry branches below.
It does not establish that every trajectory enters through one of them.

## 1. Statement and entry cases

Let an integer-phase parent chain have parameter j>=N0, prior loss
Gamma, and D=theta mod 2^j. Suppose its next chain is parameter five
with bare class d=5 or -11, arising by one of the following routes:

* a return: theta=-2 or 14;
* b return: theta=6 or -10;
* c source of history A (epsilon=3): theta=5 or -11;
* c source of history AA (epsilon=5): theta=6 or -10;
* c source of history BA (epsilon=5): theta=4 or -12.

The subsequent a return at five has a well-determined parameter m
and class (15-d-2^m)/3 modulo 2^(m+1). Assign rank r=1 to that
denominator-three output. Then

    Gamma_new+m+2 < Gamma+j.

Thus the first two units of denominator reserve are paid out of the
original record margin. If Gamma+j is at most the overall ceiling,
the emitted potential is strictly below it; no separate seed reserve
is assumed for these cases. The intermediate five state is also
strictly below the parent's record, since j>=N0 and its loss is at
most six. The lemma applies on a reached prefix with the same C1,
mass, low-deficit source formulas and S1 inputs used in the prior notes.

## 2. Large a and b parents

For an a parent, the two-a formula gives

    m=v2(9k+theta+12), theta=-2 or 14.

For a b parent, y=6k+4 has parameter five and

    x2=(13/8)*x+2*D+9k+10,
    m=v2(9k+2*theta+10), theta=6 or -10.

All low numerators are positive at these canonical calls. C1 gives
an upper bound 4.5*(j-1)^2+26<2^(j-5) for j>=N0, so m<=j-6.
The high-parent contributions have valuations j-2 (a) or j-3 (b),
well above m+1. After the first step the defect equals d to
precision j-1 (a) or j-2 (b); hence the gateway's extra output bit
is known. Total losses are two and three respectively. Therefore

    m+2+2<j (a), m+3+2<j (b).

The polynomial inequality follows at N0 and persists by its
successive growth factor being below two; this is not a finite
range assertion inferred from the test at j<=4096.

## 3. The three low-deficit c histories

Use P for the real source epoch's root parameter and rho its pointer.
The accepted/source-derived comparisons give the following reference
states for the outer chain immediately after the c step:

| history | source call parameter s | reference x=z | reference Theta | initial comparison precision |
| --- | --- | --- | --- | --- |
| A | P | 6k+2 | z+theta | s-1 |
| AA | p=v2(6k_P+2) | 6k+4 | z+theta-1 | s-1 |
| BA | p=v2(6k_P+4) | 6k | z+theta+1 | s-1 |

Here k=tau(s-1)/2 and the canonical call at s-1 is odd a. In all
three rows, v2(z)=5 and the displayed defect is exactly d=5 or -11.
These are arbitrary-interior-parent comparisons: the omitted outer
numerator terms have valuations above the listed precision, as in
C5_EXTENSION and the accepted low-deficit source proofs.

The next reference numerator is z2=(3/2)*z+2d+6. Explicitly it is
9k+19 or 9k-13 (A), 9k+22 or 9k-10 (AA), and 9k+16 or 9k-16 (BA).
All are positive. The congruences v2(6k+2)=5, v2(6k+4)=5, and
v2(6k)=5 force k>=5,26,16 respectively. For s>=15,

    z2 <=4.5*(s-1)^2+22 <2^(s-3),
    m=v2(z2)<=s-4.

The only eligible s<15 is the A case s=14,k=5; its two outputs
have m=6 and 5 and satisfy the same inequality. Comparison precision
after the next a step is at least s-2>m+1, so the actual output has
the same m and extra-bit class. The exact gateway identity
3D2=15-d-z2 gives the stated emitted family.

Source provenance supplies the remaining budget:

| history | total two-step loss | parent/source inequality | resulting m bound |
| --- | --- | --- | --- |
| A | 5 | j=rho+3, P<rho, s=P | m<=j-8 |
| AA | 7 | j=rho+4, p<=P-2, P<rho | m<=j-11 |
| BA | 7 | j=rho+3, p<=P-3, P<rho | m<=j-11 |

Adding the reserve 2 still leaves strict slack in every row. The
actual physical/source margins also dominate the comparison precisions,
so the two-step argument does not pass an unproved tie.

## 4. Assembly and limitations

At these seeds the emitted low rational phases are 10/3 or 26/3,
and their record-plus-rank potential is automatically strictly below
the original ceiling. DEPTH_CLOCK_BUDGET then preserves that reserve
through the large paired rational gateways it covers. Ordinary strong
steps with fixed denominator also lower it.

This is a segment-level assembly, not a global ranking function.
Other source histories, inherited denominators, small-parent gateways,
and unproved rational landing classes remain outside the argument.
In particular it does not prove that high-deficit c steps or arbitrary
b/c interruptions enter with a valid reserve. K_clock is unchanged.

## 5. Verification

    python -B work_c3_drift/verify_seed_budget.py

568 finite checks cover all five entry types using canonical call
clocks. The A/AA/BA reference checks are not claims that every selected
clock is realized by that whole outer history. The only small source
exception is tested explicitly. Exact a/b parent updates verify the
extra-bit class and reserve inequality. The all-parameter conclusion
uses the source inequalities and analytic estimates above, and remains
pending independent review.
