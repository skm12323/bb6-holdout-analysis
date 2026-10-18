# Direct EXT entry constraints and finite source bounds for a first tie

2026-10-18. **Accepted after three-way review.** This studies S(J) itself. EXT remains
unproved; no finite search is extrapolated to arbitrary indices.

## 1. The correct root for type b is not a real fire root

Assume F is defined through X(J-1), and X(J-1) is odd type b or c.
Put n=J-1 and s=tau(n). Let Y be the pending entry at that crossing;
for type b its lambda part is zero. The accepted RB identity says
chain 1 of S(J) is V(C,-1), where C is the real source chain at s.
Consequently its beta walk has

    Theta_1 = 3s+4,
    x_1 = lambda_A+2lambda_Y+3 = 3s+4+lambda_Y,
    c_1 := Theta_1-x_1 = -lambda_Y.             (ENTRY)

Here the second equality uses the canonical crossing mass identity
lambda_A+lambda_Y=3s+1. Thus:

* type b: c_1=0 exactly, and x_1=Theta_1=3s+4;
* type c: c_1=-lambda_Y, retaining the actual source tail;
* a real fire instead has c=1. Filtering for c=1 is NOT the b-EXT test.

The accepted RA handles a-type outer entries separately. Its chain-1
defect is 2. These are exact integer equalities, not just low-bit phases.

## 2. Source-conditioned clock cylinders

For any proposed productive mixed-block word starting at chain 1,
the accepted general solver yields

    Theta_1=t mod 2^H,
    x_1=p Theta_1+r mod 2^K, p even, K>=H.

Substituting ENTRY gives two necessary conditions on the ACTUAL source:

    3tau(n)+4 = t mod 2^H,
    (1-p)(3tau(n)+4)+lambda_Y = r mod 2^K.     (SOURCE)

For type b, lambda_Y=0 and 1-p is odd, so the candidate word fixes
one class for Theta_1 modulo 2^K. It must be even (s is an even fire
time). If this residue is even, it equivalently fixes one half-time
class k=s/2 modulo 2^(K-1): divide Theta_1-4 by two and invert 3.
An odd residue excludes that b-entry outright.

For type c the tail is correlated with tau(n); it must not be replaced
by a newly chosen free integer at each block. SOURCE is necessary and
sufficient for the word's affine valuation constraints at the given
integer source data. Physical margin and prefix availability remain
separate checks. It does not certify a source's canonical reachability
if tau or lambda_Y was invented rather than read from canonical F.

## 3. Fixed-defect search with one shared variable

For a fixed initial defect c, set x_0=Theta_0-c and retain

    2^E x_i=N Theta_0+C, N odd,
    Theta_i=Theta_0+3d.

Initially E=d=0,N=1,C=-c. A productive mixed block has
alpha=a/2^G, a positive odd, constant z=6d_block+6k-B/2,
duration T, and map x'=-(alpha/2)x+2Theta+z. Thus

    E'=E+G+1,
    N'=-aN+2^(E'+1),
    C'=-aC+(6d+z)2^E', d'=d+T.               (ROOT)

Requiring valuation q fixes a single class

    Theta_0=N^(-1)(2^(E+q)-C) mod 2^(E+q+1).

Intersect this with the retained root class. No independent choices
are made for later clocks, odd bases, or copied tails. ROOT applies
to b/c corridors and their a endpoint, not just pure-a words.

If the current root is r mod 2^h, the next numerator is known modulo
2^h because N is odd. If v2(Nr+C)<h, the next valuation is uniquely
v2(Nr+C)-E. Otherwise all valuations >=h-E are arithmetically possible
and the search records an unbounded branch rather than calling it
termination. Missing source parameters are likewise recorded as escapes.

(Scope, added after review: the root search does not check coefficient margins, so "length <=2 at defect zero" bounds continuation, not safety; and at any least counterexample J>=K_clock the first parameter ω(J−1) lies far above this selection, so it covers no relevant start. Only 170 projector cross-checks are run, a spot check. For EXT* use the starred C2-log bound 2J_W+1; Γ_1<=J/2 still holds at J>=128.)

`search_roots.py` builds all actual kernels for q<=8191 and for 35
additional parameters in five-point windows around selected resonances.
Its source records come from the accepted finite calendar (B=64).
There are 2621 productive kernels. The exact results are:

| fixed c | one productive entry | two | three | escapes |
|---|---:|---:|---:|---:|
| 0 (b-EXT root) | 2621 | 128 | 0 | 0 |
| 1 (real fire) | 2621 | 130 | 0 | 0 |
| 2 | 2621 | 133 | 1 | 0 |
| -1 | 2621 | 1 | 0 | 0 |
| -2 | 2621 | 130 | 65 | 0 |

Examples of longest words are (8143,5) for c=0, (6131,14,5) for
c=2, and (8122,5,5) for c=-2. Counts are productive BLOCK entries,
not chain counts: b/c corridors may contain extra chains.

No escapes means these selected starting kernels at the specified
defect terminate after the listed productive blocks for every
congruence-compatible integer root lift for which the replay formulas
apply. It does not cover other initial q, arbitrary negative c, or
prove a physical margin for an arbitrary outer J. This is not a new
global bound and not an improvement on the accepted enormous horizon.

## 4. A finite outer-index bound for any fixed first-tie word

This section gives an all-scale necessary condition for a least strict
EXT counterexample. Assume EXT below J, F through X(J-1), and let a
proposed word run from chain 1 to its FIRST tie candidate. A candidate
here means j>=v2(alpha_x), including both exact and over-ties: this is
the strict EXT problem, before any starred continuation.

Only an a output can be the first tie; b/c copies are safe (PROOF_EXT Prop 2.1/L′: b/c steps give
j′=ω(n)<=n−ε(n)−1, so h increases by >=1). Group the preceding transitions into
productive mixed blocks. Let E_i be the cumulative block loss at
entry i (E_0=0), with last loss E and candidate valuation q. Initially

    Gamma_1=1+epsilon(J-1),
    v2(alpha_i)=J-Gamma_1-E_i.

Define M=E+q and R=max_(earlier entries)(E_i+q_i). Earlier strict
safety and final failure require

    Gamma_1+R < J <= Gamma_1+M.                 (RECORD)

In particular M>R is necessary, independently of the outer source.
The interior b/c corridor need not be reinterpreted as a free word:
its validity follows from its earlier safe input and known source.

**Type b.** epsilon(J-1)=1, so every candidate outer index lies in

    R+3 <= J <= M+2.                           (B-INTERVAL)

**Type c.** For J>=128, accepted C2-log and EXT below J give

    Gamma_1<=max(4,2J_W),
    J_W<=floor(log2(3(J-1)^2+4))<J,
    Gamma_1<=4log2 J+4<=J/2.

The epoch parameter J_W belongs to an earlier defined fire and EXT(J_W)
is available in the minimal-counterexample induction. CLOCK supplies
C1 without an independent exit-length assumption. The final analytic
inequality holds at 128; its right-minus-left derivative is
1/2-4/(J ln 2)>0 thereafter. RECORD therefore implies

    J <= 2M.                                  (C-ENDPOINT)

Cases J<128 are already inside the accepted finite base. Hence for a
FIXED word and its final valuation, only finitely many outer source
indices must be inspected: B-INTERVAL for b, or 128<=J<=2M for c,
followed by exact RECORD and SOURCE checks on each reached source.

This is a direct S(J) analogue of the earlier F first-failure word
filters. It is not a bound on the number of candidate words, their
lengths, or final valuations. Those remain unbounded, and the source
endpoint theorem by itself does not prove EXT.

## 5. Consequence for a global proof attempt

The search can now target the correct b root and the correlated c root,
instead of proving a stronger statement for arbitrary local states or
mistakenly substituting a real-fire root. Any proposed first-tie word
must create a new loss-plus-parameter record and satisfy a finite set
of canonical source constraints.

The unresolved theorem is exclusion of ALL such words at all scales.
Neither the finite root table nor the endpoint bound supplies it.
The accepted constant-64 K_clock horizon is unchanged, and uses of
Theorem S beyond its old range still require a MASS argument.

## 6. Reproduce

    python -B work_ext_roots/search_roots.py
    python -B work_ext_roots/verify_entries.py

The second script checks ENTRY on full pair crossings, the integer
C2-log endpoint inequality, and recorded root-search coverage. The
all-scale arguments are the displayed algebra and inequalities, not
an extrapolation from the computations. Independent review is pending.
