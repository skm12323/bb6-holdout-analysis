# Clock sharpening of the finite EXT horizon

2026-10-18. **Accepted after three-way review** (reviews/global_clock_horizon_closure_review_record.md;
constant 32 -> 64 and Lemma MASS added during review). The imports below are accepted in the repository. No global non-halting claim is made.

## 1. Imports and scope

Write T = K' = 2^(2^(2^499997-3)-2). We use:

1. `work_global_clock/PROOF_CLOCK.md` sections 3-4: on every reached
   canonical crossing (including the final inspection),
   tau(n) <= n P(n), where
   g(n) = ceil(log2(6n^2+5)), P(n) = 2g(n)^2+1345.
   For n below 10^8 the accepted base tau(n)<=n implies the same bound.
   Acceptance is recorded in `reviews/global_astra11_review_record.md`;
   the older unreviewed label inside the clock note predates that review.
2. `work_global_ext/PROOF_EXT.md`: I-4 covers J<T; Theorem RA covers
   type-a entries unconditionally relative to F being defined through
   tau(J-1), inclusive. Theorem S covers type-b entries with omega<T
   and type-c entries whose copied epoch parameter J_W<T, **without
   EXT below J as an extra hypothesis**. It uses the accepted level-4
   certificate and bounds those exits by nine chains.
3. Lemma K there: an odd type-b crossing at n copies its fire at
   time tau(n), with omega(n)=v2(3tau(n)+4). An odd type-c crossing
   belongs to an epoch fired at time s_F<=tau(n), with
   J_W=v2(3s_F+4).
4. `work_global_egx/PROOF_EGX.md`, Theorem U(b), EGX and Corollary H,
   and `work_global_ext/PROOF_EXT.md`, Corollary H'': finite-prefix
   propagation from tie-free symbolic exits to F and to the real TM.

The old Corollary 4 used tau(n)<=n^2 to obtain J<2^(T/2-2).
Here only that clock-to-source-size estimate is replaced. The certified
source cutoff remains T, not a newly computed higher cutoff.

## 2. An exact per-index shallow-source criterion

**Proposition CSH (new).** Assume J>=T, F defined through tau(J-1)
inclusive, and put n=J-1. If

    3 n P(n) + 4 < 2^T,                         (CSH)

then S(J) is tie-free.

Proof. If X(n) is even, S(J) has no exit chains. If it is odd type a,
apply RA. If it is odd type b, then

    2^omega <= 3tau(n)+4 <= 3nP(n)+4 < 2^T,

so omega<T and Theorem S(c) applies. If it is odd type c, then

    2^J_W <= 3s_F+4 <= 3tau(n)+4 < 2^T,

so J_W<T and Theorem S(d) applies. These exhaust the crossing types.
The copied epoch parameter, rather than just its current chain
parameter, is bounded in the type-c case. No termination assertion for
an unknown deeper epoch is used. QED.

RA is deliberate: the stronger small-valuation condition in S(b) need
not follow from (CSH). Nor do we infer a uniform nine-chain bound for
the type-a case from this argument.

## 3. Explicit larger cutoff

For integers T>=64 define

    B(T) = floor(2^T / (64 T^2)).

(Constant 64, not 32: see Lemma MASS in section 3a; this was changed after review.)

For 0<=n<=B(T) we have n<=2^T, hence

    6n^2+5 <= 6*2^(2T)+5 < 2^(2T+3),
    g(n) <= 2T+3,
    P(n) <= 8T^2+24T+1363 <= 9T^2.

The last inequality is T^2-24T-1363>=0: its value at 64 is 1197,
and its forward difference is 2T-23>0. Therefore

    3nP(n)+4 <= (27/64)2^T+4 < 2^T.           (BOUND)

The final strict inequality follows from 4<(37/64)2^T for T>=64.
This proves the all-scale bound analytically; sampled integer checks
are not its proof.

Set

    K_clock = B(K') = floor(2^K' / (64 (K')^2)).

**Corollary EXT-CLOCK (new).** For every J<K_clock, if F is defined
through tau(J-1), S(J) is tie-free (with the usual small-J conventions).

Proof. J<T is the accepted base I-4. For T<=J<K_clock, n=J-1<B(T)
satisfies (BOUND), so CSH applies; Lemma MASS (section 3a) supplies the
range hypothesis that Theorem S's level-4 certificate needs. QED.

## 3a. Lemma MASS: later chains stay below K' (added after review)

Theorem S is stated for J>=K', but its level-4 certificate (states
R_1..R_3, Lemma M, rules S-a/S-c, tie emissions) only treats later chain
parameters j<K'. For J<K'' this followed automatically from the mass bound.
For J up to K_clock it must be checked.

**Lemma MASS.** Let T=K'>=64 and K'<=J<B(T)=floor(2^T/(64T^2)). In a
tie-free prefix of S(J), every chain t with 1<=t<=9 whose earlier chains
1..t-1 have parameters below T itself has j_t<T.

Proof. By Lemma T(2) (accepted, PROOF_EL; transferred to S(J) by EGX
Lemma TR), 2^{j_t}<=beta_t<=6d_t-1, with
d_t<=1+tau(J-1)+sum_{1<=t'<t}(1+tau(j_{t'}-1)).
By CLOCK, tau(J-1)<=(J-1)P(J-1)<=(9/64)2^T (section 3), and for
n<T, tau(n)<=nP(n)<=9T^3. Hence

    6d_t <= 6+(54/64)2^T+48(1+9T^3) < 2^T,

since 54+432T^3<(10/64)2^T for T>=64 (at T=64: about 1.1e8 versus
2.9e18; the right side doubles per increment while the left grows by
less than a factor two). So j_t<T. QED.

(The 48(1+9T^3) term already allows the t-1<=8 earlier chains; the same
estimate holds for any t<=2^T/(64T^4).) By induction over t this places
every chain of a prefix of at most nine chains below T, including the
ninth chain whose return the certificate must read, which is exactly the range in which Theorem S's
certificate operates and yields at most nine chains. The constant 32 of
the first draft would give 6tau(J-1) up to (54/32)2^T and does not
suffice.

**Strict improvement.** For integer T>=64,

    B(T) > 2^(T/2-2).

One can avoid fractional exponents: write m=ceil(T/2). At T=64 and
65, 2^(T-m)>=32T^2; within each parity class the left side doubles
when T increases by two, whereas T^2 increases by a factor below two.
Thus 2^T/(64T^2)>=2^(m-1). Its floor is at least that integer, which
is strictly greater than 2^(T/2-2). In particular it improves the old
K'' at T=K' (which is even). For the illustrative T=64, the old cutoff
is 2^30 while B(T)=2^46. This illustration is not a tower certificate
at T=64.

## 4. Finite-prefix propagation to the original machine

**Corollary H-CLOCK (new, importing the accepted assembly).** With
H=K_clock, F is defined for s<(2^H-4)/3 and the original machine does
not halt during the first 2^H-2 top-level steps, in the same horizon
convention as Corollary H''.

Here are the dependencies in that transfer, to avoid silently assuming
F already exists throughout the new range:

* Induct over reached level fires before s<(2^H-4)/3. Their parameters
  satisfy 2^J<=3s+4<2^H, hence J<H. The accepted level-fire safety
  argument gives J<rho, where rho is the fire pointer. Its replay
  source X(J-1) is earlier and defined, so EXT-CLOCK applies. Theorem
  U(b)'s coefficient-margin argument then keeps every exit safe and
  terminates the epoch. Internal calls use the accepted replay lemma;
  the finite base and even steps are handled as in U(b).
* For a singleton n_real=2^v w-2<2^H-2 (w positive odd), v<H.
  The required crossing time is <=(v-1)^2< (2^H-4)/3. The final
  inequality follows already from 3(H-1)^2+4<2^H for integer H>=16:
  the base is direct and the left side grows by less than a factor
  two per increment. The accepted next-original/progress lemma gives
  that crossing inside the F prefix just established.
* EXT-CLOCK at v and EGX make each such endgame safe; the accepted
  boundary and replay arguments exclude halts between singletons.

Thus this is exactly the finite-horizon transfer used in H'', with a
larger cutoff satisfying the same per-J implication. It does not
replace a finite bound with a universal assertion.

## 5. What remains open and why this cannot be iterated for free

Global EXT* and global non-halting remain open. The remaining difficult
cases can now be restricted, subject to review of this note, to J at
least K_clock and to deep type-b/c entries as before. More precisely,
every remaining candidate must violate (CSH); one may use its monotone
integer inverse as a somewhat sharper cutoff than B(T).

Knowing EXT below K_clock does NOT establish a level-5 shallow-source
certificate with source cutoff K_clock. Theorem S still requires
omega<K' or J_W<K'. Replacing K' by K_clock in that theorem would be an
unsupported iteration. The level-5 failure ('pair',5,5) is untouched.

This advance is a stronger finite horizon obtained from accepted
ingredients, not a solution of the deep-copy mechanism. It requires
independent review before the repository's accepted-result summaries
are changed.

## 6. Verification

Run `python -B work_global_clock_horizon/verify_clock_horizon.py`.
The script uses integer arithmetic to check constants, endpoints and
the strict improvement, and cross-checks the b/c source formulas on
actual finite crossings against a full pair implementation. It writes
`checks.json` beside itself. The checks do not compute K', simulate the
new horizon, or replace the analytic proof and its imported lemmas.
