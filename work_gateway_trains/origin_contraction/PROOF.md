# Origin contraction and a uniform bound for the next NT gate

2026-10-27. **New proposed proof; not independently reviewed.**
No global EXT/non-halting claim. The accepted K_clock is unchanged.
This note does not modify or replace an accepted review verdict.

**Review corrections (2026-10-27, three-way review: reviews/origin_contraction_review_record.md; override the body).**
1. [LOW] tau(n)>=(n-1)/2 is PROOF_EXT §4 (pointer speed), not PROOF_CLOCK.
2. [LOW] "arbitrary-length run": under |D|<=y/4 the first landing satisfies j_1<=2L+2 (a step) or omega<=log2(6tau+5)<=2L+3
   (b/c step), so r<=L+1 holds automatically and mu>=y-1-(L+1)E follows directly. No run-length cap is needed because
   one is automatic.
3. [MEDIUM] Relation to accepted results (replaces the §6 summary where they differ):
   (a) For S(J) itself, the beta walk is the reference walk with y=J, D=1, Q=1. Its first gate is already covered by the
       accepted Theorem L' (which also allows one-step descents). The new content is payment *relative to an anchor*,
       which is useful at the anchors of C_CLIMB/RECORD_BUDGET and in source epochs. It is not a new closure of S(J).
   (b) work_claude_uniform's NZ is discharged only for arrivals from y>=65536 with no catapult between y and the first
       region gate, rank<=4 (Q<=81) and height<=2048<=y/4. NZ remains a hypothesis for y in [500,65536) and for the
       2nd/3rd non-descent in a region walk.
   (c) Newly closed: D2 of C4 (on all canonical sources); for the first gate with y>=65536, |D|<=y/4 and loss<=E, the
       obligations D4, the O2 boundary and the C5 residue (previously y>=2·10^7, |D|<=5); the first F5 gate after a
       nonempty strict run.
   (d) Not closed: F1 (later gate outputs satisfy m<h+3L+3, so they necessarily fall below 65536); one-step descents
       (F2); D>y/4 (F4; canonical runs pin D to one class mod 2^{j_1}, compatible only for j_1≲log y); F6; F3 at later
       gates.
4. [LOW] The (10-2^m)/3 remark needs m>=65536. Since gate outputs satisfy m<3L+5, iterating y->m blocks drops below the
   threshold after O(log*) blocks. These classes come only from j=5 tie gates (Theorem E) and do not cover F5 gates.
5. [LOW] §5 wording: read "delta_1>=y; HP with P=y from chain 1 on".
6. [LOW-MED] The verifier's huge-y gate examples are all r=1, type 'aa'. The reviewer's tests cover runs with b/c steps and r=2
   (89,280 + further walks, 542 gates, all SAFE-GATE). check_uniform_arithmetic's hmax assertion is constructed from QB
   (tautological).

Tags: [A-imp] accepted imported result; [A-new] argument proved here, pending
independent review; [A-cond] explicit conditional corollary; [B] finite checks.
All constructed verification starts are non-canonical: canonical *call data*
does not make an ancestor state reachable in S(J).

## 1. Contribution and exact scope

The reviewed C_CLIMB section 6 uses the loose bounds R<=3/2 and
|lambda'_W|<=9 tau+9. It consequently pays (3/2)^s for s b/c steps,
and leaves nonzero/precision condition D4 as a hypothesis.

The canonical mass identities give the stronger facts

    b: R=3/4;       c: 1/2<R<1;
    0<lambda'_W<=6 tau+5.                                  (MASS)

Thus D2 is an accepted-import consequence, not an additional empirical
assumption, and b/c steps do not expand the affine origin in ordinary
absolute value. We obtain a cone invariant with no factor exponential
in the number of b/c steps, and a **conditional, uniform next-gate
theorem** for arbitrary-length strong-descent/b/c runs.

The theorem covers any following a-step, including NT gates at j>=6.
It is not restricted to a return through parameter 5. It permits an
odd-denominator reference phase and all integer lifts agreeing modulo
2^y, provided the denominator and height budgets below hold together.

It does NOT yet control one-step a descents in the intervening run,
empty runs, arbitrary small starting parameters, or the availability
of an inexpensive reference phase after every subsequent gate/source
copy. In particular it does not prove RH, H5_res, C7, or EXT.

## 2. Accepted imports and normalization

* `work_g6/PROOF_G6.md` sections 5.1--5.3: positivity of the canonical
  pair components, and c mass 2^i / lambda mass 3s+1 on defined prefixes.
* `work_m/PROOF_M.md` sections 1 and 3: crossing types, S1 at canonical
  source calls, and coefficient loss 1+epsilon.
* `work_global_ext/PROOF_EXT.md` section 2: exact scalar a/b/c rules,
  and HP. These apply on the already-defined source prefix, not on
  assumed future canonical states.
* `work_global_clock/PROOF_CLOCK.md`: tau(n)<=n P(n),
  P(n)=2 ceil(log2(6n^2+5))^2+1345. The pointer-speed bound also gives
  tau(n)>=(n-1)/2.
* `work_ext_roots/PROOF_EXT_ROOTS.md` section 4: inside the least
  strict-EXT counterexample induction, the type-c loss bound
  1+epsilon(j-1)<=4 log2(j)+4 for j>=128. This is used only in the
  conditional application in section 6, not asserted unconditionally.

At input parameter j set n=j-1. For b/c define

    C=c_A+2c_Y, lambda=lambda_A+2lambda_Y+3, R=C/2^j.

For type b, Y is the original E_(n-1), c_A=c_Y=2^(n-1), so R=3/4.
For type c, c_A+c_Y=2^n with both strictly positive. Hence

    R=(2^(n+1)-c_A)/2^(n+1) in (1/2,1).

At either crossing, lambda_A+lambda_Y=3 tau+1 and both are
nonnegative. Therefore 0<lambda<=6 tau+5. This proves MASS [A-new
from A-imp]. In particular it discharges the data premise D2 in C4
on all existing canonical sources; it does not discharge C4's other
premises or validate its old global assembly claims.

**Normalization warning.** The denominator of R is 2^j, not 2^(j-1).
The nonnegative lambdas above are the canonical W components, not
arbitrarily translated affine small parts.

## 3. Affine cone for arbitrary prescribed words [A-new]

Anchor the local walk at

    x_0=2^y U, Theta_0=2^y U+D, D=a/Q, Q positive odd,
    x_i=A_i U+beta_i, Theta_i=2^y U+D+3t_i,
    beta_i=q_i D+b_i,
    A_0=2^y, beta_0=q_0=b_0=t_0=0.

All q_i,b_i,A_i are dyadic rationals. For each prescribed canonical
odd source (with time tau), update as follows:

| step | q' | b' | t' |
|---|---|---|---|
| a | 2-q/2 | 6t+3 tau-b/2 | t+1+tau |
| b/c | R q | R b+lambda | t+1+tau |

These equations are exact, even if the prescribed word is not a
realizable parameter itinerary. For an actual itinerary they are the
affine small parts of the exact scalar walk.

**Cone lemma.** At every prefix of any such word,

    0<=q<=2,       0<=b<=6t.                            (CONE)

Proof by induction. At an a step q' is in [1,2], while
3t+3tau<=b'<=6t+3tau<=6(t+1+tau). At a b/c step, MASS gives
0<=Rq<=2 and 0<=Rb+lambda<=6t+6tau+5<6(t+1+tau).
The initial triple (q,b,t)=(0,0,0) satisfies CONE. No step count,
source height, 3-adic rank, or non-descent cap was used. Q is fixed
for this exact anchor description, not reselected at each step.

Consider a subsequent a step whose source time is tau_g. Its output
small part and coefficient are

    Z=2D+6t+3tau_g-beta/2 = (2-q/2)D+6t+3tau_g-b/2,
    A_out=2^(y+1)-A/2.

Thus, with B=|D|,

    1<=2-q/2<=2,
    3t+3tau_g-2B <= Z <= 6t+3tau_g+2B.             (GATE-CONE)

This improves the real size estimate for the slope and constant of
C_CLIMB C3/C4, and handles any a-output without a special k=1 rule.
It does not assert that Z is nonzero for unrestricted D.

## 4. Uniform next-gate theorem [A-cond, new]

Let y>=65536 and L=ceil(log2 y), E=4L+128. Suppose:

1. All source calls X(j-1) used below exist and are defined canonical
   calls. Start with exact reference defect D=a/Q, Q positive odd,
   |D|<=y/4, and put h=ceil(log2 Q).
2. There is a nonempty valid run of r transitions
   y=j_0>j_1>...>j_r=g>=5. Every transition is either a **strong a
   descent**, j_(i+1)<=j_i-2, or a b/c step with canonical S1. Let
   ell be their total coefficient loss. In particular the run has no
   one-step a descent and no preceding NT gate.
3. Every run step has loss 1+epsilon<=E. The next step at g is type a.
   It may be an NT gate; we do not presuppose its output valuation.
4. The rank/denominator budget holds:

       (E+1)(h+3L+3) < y+4E-1.                    (QB)

Then the following a output is nonzero, its parameter is determined
by the affine small part, and it lies strictly below the anchor's
precision budget:

    mu=v2(A_out)=y-ell-1,
    m=v2(Z)<h+3L+3<mu,
    m+ell+1<y.                                   (SAFE-GATE)

In particular an NT gate at the end of this run is globally paid
relative to this anchor, in the terminology of RECORD_BUDGET. This
does not mean that it is paid relative to an arbitrarily chosen
later anchor, or that all gates in the same walk satisfy the theorem.

**Proof.** The normalized coefficient alpha=A/2^y starts at 1, obeys
alpha'=2-alpha/2 at a steps and alpha'=R alpha at b/c steps. Thus
0<alpha<=2. Its valuation drops by exactly 1 at an a step (its
current valuation is <=0), and by 1+epsilon at a b/c step. This
establishes mu=y-ell-1 without estimating the size of A.

Each strong a descent drops the parameter by at least its loss plus
one. At b/c, S1 gives the same inequality:
j_(i+1)<=j_i-2-epsilon. Hence

    ell<=y-g-r,   r<=(y-5)/2,
    mu>=g+r-1>=r+4,     mu>=y-1-rE.

At each intermediate chain i>=1 the same calculation gives
v2(A_i)=y-ell_i>=j_i+i>j_i. Thus the run parameter is determined by
beta_i and is the same for every odd U once it is valid for one odd
U. This also justifies applying the affine calculation uniformly;
validity of a source itinerary was not silently inferred from CONE.

Taking the E:1 weighted average of these last two lower bounds gives

    mu>=max(r+4,y-1-rE)>=(y+4E-1)/(E+1)>h+3L+3.   (MARGIN)

For any source j<=y, CLOCK and monotonicity give tau(j-1)<=y P(y).
For y>=65536, P(y)<=y: indeed, for L>=16,

    P(y)<=2(2L+3)^2+1345 < 2^(L-1) < y.

The polynomial inequality holds at L=16 and propagates because its
left side grows by a factor strictly less than 2. Consequently every
tau in the run and tau_g is <=y^2, and t<=r(1+y^2).
The first call alone has 1+tau(y-1)>=y/2, so t>=y/2. Also tau_g>=2,
as every continuing odd canonical call has parameter >=5. GATE-CONE
therefore gives

    Z>=3y/2+6-y/2=y+6>0,
    Z<=6r(1+y^2)+3y^2+y/2<8y^3<=2^(3L+3).

The strict upper inequality follows immediately from r<=(y-5)/2.
Since QZ is a nonzero dyadic rational and Q is odd,

    v2(Z)=v2(QZ)<=log2|QZ|<h+3L+3.

Here v2(z)<=log2|z| holds for a nonzero *dyadic* rational z; it would
not hold for arbitrary rational z without multiplying by Q. Together
with MARGIN this gives unequal coefficient/small-part valuations.
For every odd U the actual output A_out U+Z has valuation m and is
nonzero. The record inequality follows by substituting mu. QED.

**Integer corollary.** If Q=1, (QB) is automatic for every y>=65536.
For L>=16,

    (3L+3)(4L+129)<2^(L-1)-1<y-1.

The left polynomial is 12L^2+399L+387. At L=16 it is 9843<32767;
twice its value minus its next value is 12L^2+375L-24>0. Thus the
inequality holds for every L, and implies QB. This is an all-scale
proof, not an extrapolation from the finite arithmetic checks.

## 5. Phase lifts and rational reference descriptions [A-new]

Suppose the true local integer state has the same x_0=2^y U but

    Theta_actual-x_0 = D (mod 2^y),

where D satisfies section 4. Then the same strict run and following
gate have the same parameters and the same record bound. In
particular an unrecorded multiple of 2^y in the phase is harmless
for this certified block. Both simultaneous height and QB conditions
are needed; choosing an arbitrarily large denominator to represent
an arbitrary residue does not establish them.

Proof of transfer: the initial parameters agree by construction.
On the first a step the numerator difference has valuation >=y+1;
on a first b/c step the numerator difference is zero. The phase
difference keeps valuation >=y. Every subsequent run record is
strictly below y, because every run step decreases the record by at
least one. HP's elementary difference induction therefore applies
after that first step with precision at least y minus its loss.
SAFE-GATE gives the strict inequality needed at the last output too.
The same induction works over rationals with odd denominator:
division by odd numbers preserves the 2-adic congruences. No claim
that those reference states themselves occur on the integer orbit
is needed. The gate need not terminate the walk; transfer is claimed
only through its output.

This addresses the lift-bit issue for this *whole block*: one must
first establish its strict record bound. It does not authorize
dropping lift bits before an uncertified arbitrary gateway.

## 6. Relation to the least-counterexample induction

The explicit loss hypothesis of section 4 is available inside the
accepted least strict-EXT induction whenever the imported source
bound applies at every queried crossing. For j>=128 it is
1+epsilon<=4log2 j+4<=4L+4. For j<128, the canonical coefficient
bound gives 1+epsilon<=j<=127 (and type a has loss 1). Both are
bounded by E=4L+128. No global claim about the canonical table is
being made beyond that induction.

Thus the new result removes the separate affine nonzero/dominance
obligation D4 for a nonempty strict run with a qualifying integer
phase description. For rational descriptions it replaces it by QB.
It removes the need to cap the run length or b/c count in this
setting, and includes non-bare NT gates at g>=6.

The global remaining work is substantial:

* prove that reachable anchors admit a reference D satisfying both
  |D|<=y/4 and QB, together with actual phase precision;
* cover one-step a descents, empty-run gates and starts y<65536;
* propagate a usable reference through gate outputs and nested c
  copies. CONE uses a fixed anchor; it does not bound the denominator
  of newly chosen reduced phase descriptions or certify a reset;
* combine the blocks into a global record bound or a well-founded
  induction. Individual paid blocks do not by themselves do this.

In particular, the two familiar emitted classes (10-2^m)/3 and
(26-2^m)/3 have low representatives 10/3 and 26/3 modulo 2^m.
For sufficiently large m they satisfy the height/denominator portion
of this theorem, including either lift bit. This only controls a
subsequent qualifying strict run and its next gate; it does not
certify the entire tail or replace the existing finite certificates.

## 7. Verification, counterexample discipline, and review status

Run from the repository root:

    python -B work_gateway_trains/origin_contraction/verify_origin_contraction.py

The script writes only local `checks.json`. Checks currently include:

* 200,000 canonical crossings for mass and lambda bounds; an
  independent full-pair implementation checks 325 b/c ratios;
* 75,000 exact rational word steps for CONE and GATE-CONE, with
  deliberately non-canonical synthetic source sequences;
* 40,805 integer comparisons for dyadic exponents 16..4096,
  including QB boundary values (supporting, not replacing, the proof);
* 21,856 constructed anchors using canonical call data, with 39
  first gates and 6,369 full-integer replays; huge direct-gate
  examples use source pointers with over 120 bits, without allocating
  2^pointer;
* 120 integer phase-lift replays, including 12 genuine gate events
  in these *constructed* walks. Examples:
  (y,D)=(146935,58/3) -> parameters (146935,5,8), and
  (2424159,-32747) -> (2424159,17,18). The latter checks the extension
  to a non-bare NT gate;
* 126 members of the known y=5 small-gateway counterexample family:
  D=5, x=32(2^(m-4)-1)/3 gives output 2^m for even m>=6. Here Z=16
  and mu=4 are tied. It is explicitly outside the large-anchor,
  nonempty-run hypotheses, and remains an obstruction to arbitrary
  unqualified extrapolation.

All checks pass. They are not an independent proof review. In
particular, the arbitrary-word cone tests and the constructed-anchor
replays are not evidence that the reference conditions hold on all
actual S(J). Accepted checkpoint and horizon remain unchanged.
