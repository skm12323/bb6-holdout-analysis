# Descent of c sources whose epoch starts with an a return

2026-10-18. **Accepted after three-way review (reviews/ext_roots_review_record.md).** This strengthens the
low-deficit reductions. It does not prove global EXT.

## 1. The AA case has an actual earlier b source

Use the notation and accepted inputs of `PROOF_LOW_DEFICIT.md`.
Let a source epoch start at pointer rho, parameter P, numerator x0=2^P U,
and exact phase Theta0=x0+1. Assume its first two odd returns are AA.
Write k=tau(P-1)/2 and

    p=v2(6k+2)<P-1, l=tau(p-1)/2.

The first return parameter is p. The second a-output, shifted by -1
as required by the outer c-entry, is

    x=(5/4)x0+9k+6l+7,
    Theta=x0+6k+6l+6.                          (AA)

The crossing X(p-1) is an ACTUAL odd a fire. Its simultaneous b crossing
is X(p): at the P=∅ fire state, X(p−1) and X(p) are read in the same W-step
with the same head (PROOF_M Lemma 2.3), so X(p) is odd of type b and RB applies.
AB needs m=p−1>=4 and X(m) odd; if p<=4 or X(p−1) is even, both walks end
together by HP parity agreement. Therefore S(p+1) has a b-entry whose first chain is exactly

    y=6l+4, Theta_ref=y.

This supplies the missing real-source correlation; it is not an
arbitrary zero-defect state. The differences from (AA) are

    x-y=(5/4)x0+3(3k+1),
    Theta-y=x0+2(3k+1).

Since v2(3k+1)=p-1 and p<=P-2, their valuations are p-1 and p.
The reference b-entry coefficient valuation is p-1, as its actual
fire pointer is p-1. EXT(p+1) implies j_t+Lambda_t<p-1 for its entire
tail. HP at precision p-1 transfers that tail to (AA).

The outer source coefficient valuation is rho-2 (two a losses),
strictly larger than p-1, so the transferred tail is safe. Finally,
p+1<P<rho<J. Thus EXT(p+1) is available in a least-EXT-counterexample
induction. This closes the AA source class under that induction.

The source has deficit five: its crossing is at n=rho+3, and
epsilon=n-(rho-2)=5. With the earlier BA reduction, both possible
epsilon=5 histories are now covered, subject to review.

## 2. The same provenance extends past two returns

**Proposed theorem A-SOURCE.** Assume F is defined through the outer
odd c crossing X(J-1), and EXT holds at every smaller index. If the
epoch containing that source began with an odd a return, then S(J)
is tie-free and terminates, regardless of how many later returns that
source epoch has made.

In particular, this source-history class cannot occur in a least
strict EXT counterexample. The theorem does not assume a bounded
deficit or a bounded number of subsequent b/c returns.

### First source output

The source's first a-output has

    x1=(3/2)x0+6k+2, Theta1=x0+6k+4,
    p=v2(x1)=v2(6k+2)<P-1.

If the outer c source is this first output, theorem C3 in the earlier
note already reduces it to EXT(p), with p<J. Thus consider a later
a-output within the same source epoch.

### A reference copy with an actual earlier ancestor

Compare the source's first output (x1,Theta1) with the exact-phase-two
state R0=(x1,x1+2). Their x difference is zero and their Theta difference
is -x0/2, of valuation P-1>p. If R0 has an even return, the source
epoch ends and there is no later c source under consideration.

Otherwise apply accepted AB to R0. Let C0 be its real copied chain
from Lemma K at X(p-1), and put e=epsilon(p-1). Its coefficient
valuation is

    sigma_ref,0=p-1-e.

The real epoch E containing C0 starts at pointer at most p-1. It
has ended before the source epoch's fire at rho, since p<P<rho and
canonical epochs have disjoint increasing pointer intervals. Hence
AB's completed-epoch hypothesis is supplied by the existing prefix,
not by an assumption about the unresolved outer exit.

After R0's first return, AB identifies its entire tail with E from C0
on. At each corresponding real chain C_t, the scalar differences
between the phase-two reference and C_t have valuations at least

    sigma_ref,t=sigma_ref,0-Lambda_t,           (COPY-PREC)

where Lambda_t is loss since C0. This is the precision assertion in
AB's proof, propagated by HP and the real epoch's S1 margins.

The phase-two reference also satisfies j+loss<=p relative to R0.
HP with initial precision P-1 therefore matches the actual source
epoch to that reference through termination. At C_t, its differences
from the phase-two reference have valuations at least

    P-1-(1+e)-Lambda_t
      =P-2-e-Lambda_t > sigma_ref,t.

Combining this with COPY-PREC shows that the actual source chain D_t
and the real earlier chain C_t agree in both x and Theta to precision
at least sigma_ref,t. Their physical coefficient valuations obey

    sigma_D,t=rho-2-e-Lambda_t,
    sigma_D,t-sigma_ref,t=rho-p-1>0.           (MARGIN)

### The earlier outer index and the final shifted comparison

Our outer source is an a-output D_t. There are two possibilities:

* At the first embedding step, the return from R0 was a. Then C_t=C0
  is a real fire at pointer p-1. Choose its b crossing, giving the
  earlier outer index J'=p+1.
* At a later embedding step, the matched preceding return was a.
  Therefore C_t is a real a-output, at an odd c crossing n'. Choose
  J'=n'+1.

In the second case C_t lies in E, completed before the fire at rho,
so n'<rho and J'<=rho<J. The first case also has J'<rho<J. Both are
actual canonical source crossings; no free virtual b source is used.

RB gives the first chain of S(J') as V(C_t,-1), with coefficient
valuation sigma_ref,t. By EXT(J'), its whole tail terminates and
satisfies j_i+Gamma_i<sigma_ref,t, with Gamma measured from this entry.
The outer S(J) starts at V(D_t,-1). Subtracting one from both clocks
does not change their agreement to precision sigma_ref,t. Apply HP
once more, now to these two shifted tails. The outer follows S(J')
to termination; MARGIN gives strictly more coefficient room throughout.
This proves the theorem.

All reference calls are already defined. Each HP comparison is made
up to the next candidate and then the strict margin extends the
prefix; no first tie is crossed as an assumed valid update. No
Theorem S range extrapolation or new finite certificate is used.

## 3. Proposed remaining frontier

(The induction throughout is on **strict** EXT. Under EXT*, an over-tie in
S(J′) violates HP's strict hypothesis, so the argument does not transfer to
an EXT* induction.)

Combining A-SOURCE, C3, the AA calculation and C5-BA:

* all c sources of deficit three are excluded at a least counterexample;
* both AA and BA deficit-five source histories are excluded;
* more generally, ANY c source whose epoch begins with a is excluded,
  including arbitrarily high deficit and intervening mixed returns.

Thus a remaining c-type least counterexample must have deficit at
least seven and belong to an epoch whose FIRST odd return was b or c.
Type-b outer entries remain open. These are proposed reductions, not
new accepted conclusions until independent review.

Why not simply repeat the argument for a b/c-first source epoch?
After its first b/c copy, the comparison clock has a -1 offset rather
than high-precision agreement with a phase-two absorbed real epoch.
The later outer -1 shift compounds that discrepancy. The initial
COPY-PREC hypothesis used above is then unavailable. Assuming it
would discard precisely the shifted-copy difficulty of EXT.

## 4. Checks and what they do not cover

The extended `verify_low_deficit.py` checks four canonical AA sources
in the P<=256 calendar selection. It verifies both AA difference
identities, the earlier b source, its smaller outer index, the matched
shifted tail, and the two coefficient margins. Those are also four
instances of the A-SOURCE ancestry comparison. Other earlier checks
(76 A and four BA sources, plus 18 explicitly algebraic outer lifts)
remain in place and pass.

Only four AA instances are exercised; the verifier's mixed-history branch
(i>0) was not implemented correctly and is now explicitly disabled (it was
never reached). An independent reviewer sweep (P<300) met only the histories
a, aa, ab. This finite selection does not exercise every possible mixed history.
The arbitrary-history claim rests on the accepted AB/HP precision
statements and the provenance proof above, not extrapolation from four
AA examples. This dependency is particularly important for review.

    python -B work_ext_roots/verify_low_deficit.py
