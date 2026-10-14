# Completed-tail shadowing and a candidate global induction

2026-10-14. New symbolic arguments, **not independently audited**.
No global non-halting theorem is claimed. This work changes no accepted proof.

## 1. What is new

Rather than certify another finite tower level, this note proves a local
transfer principle for a whole already completed epoch suffix. A sufficiently
precise copy follows that suffix through **all** its a/b/c returns, including
non-NT transitions. Individual hidden-k formulas are unnecessary for these
copies. A second lemma localizes low-precision shifted-copy failures to an
explicit valuation collision. The same transfer principle has a finite-tail
version relevant to the excursion endgame.

The global proposal is an induction on the original fire pointer rho,
charging completed copied suffixes to strictly earlier epochs. The missing
part is a bound on the prefix before an epoch closes or enters a sufficiently
precise copy. An additional boundary-entry condition is still needed for the
original Turing machine, rather than just F.

Dependencies: the exact pair map and positivity/mass lemmas in
`work_g6/PROOF_G6.md` section 5; replay, crossing types, and sigma recursion in
`work_m/PROOF_M.md` sections 2--3; the exact (not NT-restricted) a-return formula
in `work_el/PROOF_EL.md` Theorem A. No r10 endgame closure is imported.

## 2. State variables that retain the lost information

At a top-level chain write

    x = lambda_A + 2 lambda_b + 3 = 2^j u,
    Theta = 3s+5,
    sigma = v2(c_x).

Here u is the lambda component of the run base, not the entire integer value.
For an odd a-return, n=j-1 and k=tau(n)/2. The exact next-chain identity is

    x_next = 2 Theta + 6k - x/2,
    Theta_next = Theta + 3 + 6k,
    sigma_next = sigma-1.                                  (A)

For an odd b/c-return, let (c_X,lambda_X) be the x-pair of W's chain at
the crossing X(n). Then

    x_next = c_X * x/2^j + lambda_X,
    Theta_next = Theta + 3*tau(n)+3,
    sigma_next = sigma-1-epsilon(n),
    v2(c_X)=n-epsilon(n).                                  (BC)

None of these identities assumes that the new j is smaller than the old j.
Even returns end the epoch. Their parity is determined by X(j-1) and is
independent of the particular positive odd run base (the replay parity lemma).

## 3. Exact error transport [symbolic]

Compare a reference epoch suffix with another compatible top-level run.
Until a first disagreement in j, both use the same crossing indices and
return types. Define

    D = Theta_outer - Theta_reference,
    E_t = x_outer,t - x_reference,t.

The time increments in (A)/(BC) are the same, so **D is constant**. Their
differences give the exact error recurrences

    a:    E_next = 2D - E/2,
    b/c:  E_next = (c_X/2^j) E.                            (ERR)

In the b/c formula the quotient need not itself be an integer, but E is
divisible by 2^j whenever the two chains have the same j, so the product is
an integer. Its valuation decreases by exactly 1+epsilon(n), unless E=0.
Use v2(0)=infinity for the comparisons below.

This replaces an accumulating list of high-bit residues by a constant shift
D and a single transported error E. It does not assume an NT theta update.

## 4. Completed-tail shadowing theorem [symbolic]

Suppose the reference suffix is a finite, safe top-level suffix ending in an
even return. Let its initial coefficient valuation be sigma_0. Assume:

1. Both compatible starting chains have the same j; their coefficient
   valuations differ by a fixed C>=0: sigma_outer,0=sigma_0+C.
2. v2(E_0)>=sigma_0.
3. v2(D)>=sigma_0-2.
4. The earlier W prefixes needed by the reference calls are defined, so
   the standard replay lemmas apply to those calls in both runs.

Then the outer run has the same entire top-level parameter sequence, crossing
types, call lengths, and ending even return. Its coefficient valuation is
sigma_outer,t=sigma_reference,t+C. It is safe at every chain, including
any non-descending chains of the reference suffix.

Proof by induction on the reference suffix. Suppose v2(E_t)>=sigma_t.
Since its chain is safe, j_t<sigma_t, and addition of E_t cannot change its
valuation: the outer chain has the same j_t. Its physical margin is at least
the reference margin. Replay therefore gives the same return type and duration.

If the return is odd a, (ERR) yields

    v2(E_next) >= min(v2(D)+1, v2(E_t)-1)
               >= sigma_t-1 = sigma_next,

because sigma_t<=sigma_0 and v2(D)>=sigma_0-2. If it is odd b/c,

    v2(E_next) >= sigma_t + (j_t-1-epsilon(n))-j_t
                = sigma_t-1-epsilon(n) = sigma_next.

The two sigma recurrences have the same decrement, preserving C. Thus the
induction continues regardless of whether j_next descends. At an even return
both runs end their epoch. Inner calls are safe by the replay lemma applied
to the already defined W prefixes. This proves the statement without
assuming future safety of the outer run. QED.

### 4.1 Corollary: an actual theta=2 b/c-copy closes the whole tail

Suppose a safe parent chain of parameter j_p makes a b/c return, and

    Theta_parent = 2 (mod 2^j_p).

The newly copied W-chain at X(n), n=j_p-1, has initial sigma_0=n-epsilon(n).
The exact image relation gives

    E_0 = c_xW * u_parent,
    D = Theta_parent-2,
    C = v2(c_u,parent) >= 1.

Hence v2(E_0)=sigma_0, and v2(D)>=j_p>sigma_0-2. The theorem applies to
the **whole remaining suffix of that W-epoch**, not just its b/c segment.
The same conclusion holds under the weaker, directly checkable condition

    v2(Theta_parent-2) >= sigma_0-2.                        (SHADOW)

This covers a nested exact copy of the previously troublesome hidden-k
a-output at j=5: if the source later uses k to resolve 5 -> q, the outer
copy follows the same q by error separation. The copier need not reconstruct k.
It does not cover arbitrary nonzero small offsets that fail (SHADOW).

### 4.2 Why the source suffix is earlier, not circular

Let rho be the current epoch's fire pointer. Its safe parent satisfies
j_p<sigma_parent<=rho, so n=j_p-1<rho. The crossing X(n) belongs to an
epoch starting at rho_W<=n<rho. Since the current fire has empty pending
stack, that earlier epoch has already ended. Its entire suffix is historical
data of F, not a future object assumed to exist. This is an induction on rho;
it requires no conjecture that every fire parameter occurs.

## 5. First-collision lemma for shifted copies [symbolic]

An actual b/c copy always starts with E_0=c_xW*u_parent. Before the first
a-return, only b/c transitions occur, so E_t=c_xW,t*u_parent and
v2(E_t)=sigma_t. D remains constant, without any assumption about its size.
Thus the outer copy follows that b/c prefix even when (SHADOW) fails.

Consider its first odd a-return. Let r be the reference's next parameter,
and d=v2(D)<infinity. If

    sigma_t-1 > d+1,

then (ERR) implies v2(E_next)=d+1. Therefore:

* if r != d+1, the outer next parameter is min(r,d+1);
* if r = d+1, the low valuations cancel; higher correlated information is
  needed. No bounded continuation is claimed for this collision.

If sigma_t-1<=d+1, the completed-tail theorem can instead be restarted
at this point, since d>=sigma_t-2 and the error still has valuation sigma_t.

**Odd-shift corollary.** If D is odd, a safe odd a-return in the reference
has sigma_t-1>r>=1, hence sigma_t>=3 and v2(E_next)=1. If r>=2, the outer
next parameter is exactly 1 and its next return is even: it terminates.
Only **r=1** is a collision. If no odd a-return is encountered, both runs
reach the same earlier even return instead.

This localizes the difficulty for odd shifts. It does not prove that the
r=1 collision is harmless or rarely repeated on the distinguished orbit.

### 5.1 Controlled rational shifts: a whole block descends [symbolic]

There is a useful way to resolve even the valuation collision without
guessing higher bits. Let the original copying parent have parameter n+1,
and write its shift as

    D = delta (mod 2^(n+1)),  delta=P/Q, Q>0 odd.

Congruence with a rational of odd denominator is in the usual 2-adic sense.
Follow the copied W-chain through its b/c prefix to the first odd a-return.
Let x_* be the reference lambda_x at that return, and let c be its preceding
chain's coefficient c_x. Before this first a-return the error is c*u_parent.
Thus the exact outer lambda value is

    x_outer,* = x_* + 2D - c*u_parent/2.                   (SHIFT)

Put S=v2(c)-1 and B=Q*x_*+2P. Since v2(D-delta)>=n+1 and S<n+1,

    Q*x_outer,* = B + error of valuation S,

where the second term has valuation exactly S: u_parent and Q are odd,
and the contribution 2Q(D-delta) has strictly higher valuation.
Consequently, **0<|B|<2^S implies j_outer,*=v2(B)<S**. If B=0 the
parameter is S. Equality v2(B)=S is the case where this shortcut is
insufficient. This statement retains the actual source value x_*, rather
than replacing it by only its valuation r.

There is a clean sufficient bound using exactly the earlier-crossing
hypotheses (C1),(C2) of Theorem M. Suppose

    n>=64, |delta|<=n/4, Q<=2^(n/4).

Then at the first a-return, the reference pointer is n+1: the initial copied
crossing at n advances to n+1, intervening b/c chains read no originals, and
the first a-return is the next state with a single pending D. At that crossing,

    S = n+1-epsilon(n+1) >= 3(n+1)/4                      by (C2),
    x_* <= 6(n+1)^2+5                                    by (C1).

Also x_*=A+2D_ref+3 >= (A+D_ref)+3=3*tau(n+1)+4.
The pointer increases by at most two per F step, so tau(n+1)>=(n-1)/2.
It follows that x_*+2delta>0 and

    0 < B <= Q*8(n+1)^2,
    log2 B <= n/4+3+2log2(n+1) <= n/2+3 < 3(n+1)/4 <= S.

Here log2(n+1)<=n/8 for n>=64; on [2^m,2^(m+1)) use m+1<=2^m/8,
valid at m=6 and preserved as m increases. Thus the whole copied-prefix
plus first-a block is safe and strictly descends from n+1 to at most n/2+3.
For Q=1 the stronger logarithmic bound j_outer,*<=3+2log2(n+1) holds.
If the source instead reaches an even return before an odd a-return, the
outer run already ends with it.

In particular the integer shift delta=-1 of a fire copy is covered at
large n, including its r=1 valuation collisions. Since x_*>2, its B=x_*-2
cannot vanish. This is stronger than the odd-shift corollary alone.

**Unclosed invariant.** The output representative can be written
Theta_reference,*+delta, with the same odd denominator Q. Its real magnitude
may be O(n^2) while the new j is only O(log n). Therefore the assumptions
|delta|<=n/4 and Q<=2^(n/4) are **not automatically preserved** at the next
copy. One cannot iterate this block-descent lemma indefinitely without an
additional compression or ancestry invariant. This is a precise remaining
obstacle, rather than a completed global ranking function.

## 6. Finite-tail version for the endgame [symbolic, conditional entry]

After the boundary defect has been consumed, a finite excursion has

    sum c = 2^v,  sum lambda = 3s.

Use Theta_finite=3s+4, equivalently sum(lambda)+4. There are no unread
originals; a missing second partner has pair (0,0). At a top-level a-return
the list is [D] and the mass identity gives

    x_next = 2 Theta_finite + 6k - x/2,
    c_x,next = 2^(v+1) - c_x/2.

Since 0<c_x<2^(v+1), its sigma is at most v, so the last coefficient has
valuation sigma-1. The b/c formulas are unchanged. Thus (ERR) and the
completed-tail proof apply, with Theta_finite replacing 3s+5. An even return
now leaves a singleton, since there is no original tail.

Consequently, a compatible finite-tail entry that satisfies the shadowing
conditions relative to an earlier completed W suffix reaches a singleton
safely. This avoids fixed cylinder widths **for entries that satisfy those
conditions**. It does not establish that every actual boundary entry does.
In particular, the boundary's -1 perturbation is not automatically a
high-precision shift; one cannot silently apply section 4 to all endgames.

## 7. A concrete sufficient global route for F

Let N_B=10^8 be the audited base, L(rho)=floor(log2 rho)^2, and
g=2 log2 rho+4, as in Theorem M. Define the following open stopping property:

**(CC)** In every epoch with rho>N_B, by top-level chain index
t<=floor(log2 rho), either the epoch has ended, or it makes a b/c return
satisfying (SHADOW).

Under the earlier-epoch hypotheses of Theorem M, the first L(rho) potential
chains can be justified by its partial time/margin bootstrap until an exit
occurs. Thus (CC) is a property of a well-defined finite prefix; it need not
assume that the whole current epoch is already safe.

**Conditional theorem.** The audited base plus (CC) imply that F is defined
forever and its universal walk never halts.

Proof. Induct on rho with Theorem M's time/deficit hypotheses and exit bound.
Put b=floor(log2 rho). If the epoch ends by b there is nothing further to
show. Otherwise its shadow source starts at

    rho_W <= j_p-1 < g.

By the induction hypothesis, its total number of chains is at most
1+R(g), where R(g)=max(2,floor(log2 g)^2); the maximum 2 includes base epochs.
Section 4 closes the outer copied suffix. Its exit count is bounded by

    r <= b+1+R(g) <= b^2=L(rho).

For b>=26, g<2b+6 and log2(2b+6)<=b/2, giving
b+1+R(g)<=b+1+b^2/4<=b^2. The logarithmic bound holds already at integer
b=10 and propagates because the right-hand exponential grows faster than
2b+6. The remaining estimates and progress follow from Theorem M. QED.

CC remains unproved. It is a deliberately explicit sufficient target, not
a claim that the main hard problem has disappeared. Its advantage is that
arbitrarily nested precise copies are discharged by earlier epochs, so a
proof only has to control the prefix before a stopping event. The odd-shift
lemma suggests studying repeated collisions into reference parameter 1.
One may enlarge the stopping set by any rigorously proved short terminal
macro, with corresponding constants in the exit bound.

For the **original machine**, a further statement is needed: every actual
boundary endgame must reach a safe singleton, for example by the finite-tail
transfer criterion after a controlled prefix. This second entry condition
is also open. A global F theorem alone must not be reported as machine #1's
global non-halting proof.

## 8. Verification, scope, and next work

`verify_shadow.py` evolves full bigint pair states. It does not evolve the
NT automaton or the extended residue engine. Its crossing table is imported
from the existing full-pair implementation in work_m; this is not an
independent peer review of those base lemmas.

Results:

* 1304 actual small b/c crossing sources, plus 8 explicitly synthetic safe
  sources containing the 17 -> 5 -> 6 -> 1 rescue;
* 3936 full copied infinite-tail runs: identical step/chain decisions and
  durations, all mass and margin checks pass;
* 363 exact error-recurrence checks, including 24 copied non-NT transitions;
* 57 odd-shift first-a cases with reference r>1 terminate at outer j=1;
  8 other source cases have r=1 and are recorded as collision cases for
  the odd-shift lemma alone;
* 65 controlled delta=-1 block checks satisfy the exact B-dominance
  inequality and give j=v2(B), resolving all 8 of those r=1 source cases
  under this stronger shift condition;
* 1312 constructed finite-tail copies reach a singleton with the same
  decision sequence as the reference suffix. These constructed entries are
  not asserted to be the actual boundary states of all excursions.

The next mathematical targets are (i) a bound on consecutive non-closing
shift collisions, or an invariant that allows iteration of section 5.1
after its output representative grows, retaining ancestry correlations;
and (ii) an entry
classification for actual boundary defects using the same error variables.
Neither bound has been proved here. No higher finite horizon is claimed.

Reproduce:

    python -B work_global_shadow/verify_shadow.py

Outputs are confined to this directory. No existing proof or summary is edited.
