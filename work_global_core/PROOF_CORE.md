# A small parameter core for the global exit problem

2026-10-14. **New symbolic reformulation; three-way reviewed (no mathematical errors found).**
This is not a reduction in difficulty: CORE2 is equivalent, up to a factor
about 3 in the budget, to the old exit-length lemma. If every epoch has at
most b-1 exit chains then CORE2 holds; conversely CORE2 gives at most 3b+1
exit chains (section 4.2).
The core-visit bound below is unproved. No global non-halting result is claimed.
This note does not extend the finite horizon by another tower level.

## 1. Positive recurrence across two a-returns [exact]

At consecutive top-level chains write x_t=lambda_x, j_t=v2(x_t), and
Theta_t=3s_t+5. Suppose the first two returns are odd type a, and put
k=tau(j_t-1)/2, l=tau(j_(t+1)-1)/2. The exact return formulas give

    x_(t+1)=2Theta_t+6k-x_t/2,
    Theta_(t+1)=Theta_t+3+6k,
    x_(t+2)=2Theta_(t+1)+6l-x_(t+1)/2.

Eliminating Theta_t yields the positive identity

    x_(t+2)=(x_t+x_(t+1))/2+6(k+l+1).                    (POS)

Unlike a representative theta rule, POS is valid at a non-NT step as well.
It uses actual positive lambda values; no assumption that j decreases is made.

### Useful local consequences

For two odd a-returns, j_t,j_(t+1)>=5: crossings below index 4 are even.

* If k and l have the same parity, v2(6(k+l+1))=1, whereas the first
  two terms in POS are divisible by 16. Thus j_(t+2)=1 and the next return
  is even. In particular, an equal-parameter a-step j -> j is followed by 1.
* If j_t != j_(t+1), put p=min(j_t,j_(t+1))-1 and
  h=1+v2(k+l+1). If p!=h, then j_(t+2)=min(p,h). Only p=h leaves an
  unresolved valuation collision, in which case j_(t+2)>=min(j_t,j_(t+1)).
* If three odd a-returns are available and j_t=j_(t+2)=a, then the two
  intervening constants k+l+1 are equal. Eliminating x_(t+1) gives

      x_(t+3)=(3x_(t+2)-x_t)/2,  j_(t+3)>=a.             (REPEAT)

  The inequality follows because x_t/2^a and x_(t+2)/2^a are odd.
  Therefore a pattern a,b,a,b with a>b cannot occur through three a-returns.
  A nonconstant alternating period-two parameter pattern cannot continue
  for five chains with all four returns odd type a. A parameter-only graph that permits it has forgotten
  an actual arithmetic constraint.

These conclusions concern safe valid prefixes. They do not justify a
division at an outer chain whose margin has not yet been established.

## 2. No three consecutive large parameters [symbolic under C1]

Assume a defined prefix has j_t<=g, where g>=1, and the earlier crossing
times it uses satisfy (C1), tau(n)<=n^2. Define

    K(g)=ceil(log2(6g^2+6)).

Call j<=K(g) the core. If two successive chain parameters j,q exceed K(g),
their next chain, if any, belongs to the core; in fact its parameter is <K(g).

Proof. An odd b/c-return has next parameter bounded by

    j_next<=log2(6tau(j-1)+5)
           <=log2(6(g-1)^2+5)<K(g).

Thus the first return of two consecutive large chains must be type a.
If the next return is b/c the displayed bound finishes the proof; if even,
the epoch ends. If it is odd a, apply POS. Its positive constant satisfies

    0<6(k+l+1)<=6((g-1)^2+1)<6g^2+6<=2^K(g).

Since j,q>K(g), both x/2 terms are divisible by 2^K(g). Their sum with
this strictly smaller positive constant has valuation <K(g). QED.

Consequently, **at most two consecutive chains lie outside the core**.
For every finite prefix, if m counts its core chains, including the fire
when applicable (the initial fire counts as a core visit exactly when its
parameter J satisfies J<=K), and N counts all its chains, then

    N<=3m+2.                                             (COUNT)

There are m+1 gaps before, between, and after the m core chains, each of
length at most two. For an entire epoch with r exit chains this gives
r<=3m+1. It is valid without NT and without a bounded rational-phase window.

In Theorem M's intended induction g is about 2log2(rho), so the core has
only O(log log rho) parameter values. The core size is still unbounded;
this is not a fixed finite-state proof.

## 3. A core return is at most three transitions [exact representation]

Between successive core visits there are at most two noncore chains.
Every core first-return map therefore composes only one, two, or three
top-level transitions. On the state (Theta,x), each step is affine:

    a:   Theta'=Theta+3+6k,   x'=2Theta-x/2+6k;
    b/c: Theta'=Theta+3tau+3, x'=(c_X/2^j)x+lambda_X.

Here c_X and lambda_X are not the crossing head itself: they are the parts
of W's chain value at step tau(n), i.e. of (crossing head + 2*next entry + 3),
split into the x-dependent coefficient and the constant term.

Hence every core first-return branch has the form

    Theta'=Theta+d,
    x'=alpha*x+beta*Theta+gamma,

with dyadic rational coefficients and |alpha|<1, 0<=beta<=2. The coefficient
bound follows directly by composing at most three steps (and also holds
for longer such compositions): a sends beta to 2-beta/2, b/c scales it
by a number strictly between 0 and 1.

The joint relation ATheta-2^G x=C modulo 2^L from
`work_global_compression` can be transported through these branches with
its exact updates. Thus large jumps can be retained as short affine
branches of a core return system rather than expanded into long words.

**Important limit:** |alpha|<1 is not a termination proof. Theta changes,
the branch coefficients vary, and the choice of branch depends on correlated
high bits. Nor does a small set of j values bound the number of core visits.

## 4. An explicit sufficient core-visit bound for global F

Let rho be the fire pointer, N_B=10^8 the audited base, and

    g=2log2(rho)+4, b=floor(g^2), K=K(g).

Consider this unproved condition in the earlier-epoch induction:

**(CORE2)** For an epoch at rho>N_B, no prefix justified by the bootstrap
below reaches b+1 core visits (visits to j<=K, counting the initial fire
when J<=K, as in COUNT).

Informally: the epoch ends after at most b core visits. The prefix form
above is the definition; it is what makes the argument non-circular.

This is weaker than requiring a bound on every step separately, but it is
still a substantive stopping statement. It has not been established here.

**Conditional theorem.** The audited base and CORE2 imply that F is defined
forever and its universal walk never halts. They also give s<=i^2,
epsilon(n)<=max(7,n/4), and Delta<=9(log2 i)^3 beyond the large base.

### 4.1 Constants for the epoch bootstrap

Use the relaxed exit budget R=3g^2+2 and E=max(7,g/4). For rho>=10^8,

    R(1+E)+g < rho,                                      (I1)
    3+R(2+E) < rho/4,                                    (I2)
    (R+1)(1+g^2) < 2rho.                                 (I3)

To prove these, set x=log2 rho. On this range E=x/2+1 and g=2x+4.
The three inequalities are 2^x>P(x) for positive-coefficient polynomials
of degree at most four (divide the I3 polynomial by 2). Since xP'<=4P,
P/2^x decreases for x>=log2(10^8)>26. At rho=10^8 use x<27, hence
g<58, E<14.5 and R<10094. The upper bounds on the three P values are

    156515, 666216, 16984837.5,

all strictly below 10^8. This proves I1--I3 on the entire interval,
not merely on a numerical grid.

### 4.2 Induction and stopping

Proceed as in Theorem M, retaining (C1),(C2) at earlier crossings. For the
first 3b+3 potential top-level chains (indices 0..3b+2), the partial
bootstrap gives s_t<=rho^2+t(1+g^2)<2rho^2, hence j_t<=g. By the sigma
recursion and I1, sigma_t>=rho-t(1+E)>g, so each such chain is safe and
its replay uses only already reached indices j_t-1<rho. Its call lasts
at most g^2 steps. This justifies the finite prefix without assuming the
current epoch has already ended.

If all 3b+3 chains could occur before termination, COUNT would force at
least b+1 core visits, contradicting CORE2. Thus the epoch ends with
r<=3b+1<R. I3 propagates the quadratic crossing-time bound to the next
epoch; I2 and the exact crossing-deficit formula propagate (C2).
Even level steps advance the pointer as usual. Every epoch now ends, so
F remains defined and makes progress forever.

For the stated deficit bound, the same bookkeeping gives

    Delta<=2+R(2+E)+g
           =6x^3+60x^2+171x+156 <=9x^3  (x>=26).

The last inequality holds at x=26 and its difference and derivative grow
thereafter. Since the actual pointer i>=rho, this gives the advertised
bound. The larger constant 9 matters: one must not silently reuse the
unit-coefficient cubic bound from the stronger original exit hypothesis.

This theorem concerns F. The actual finite-excursion boundary/endgame
obligation for machine #1 remains separate and unproved globally.

## 5. What the new target does and does not simplify

CORE2 is not easier than the old exit-length lemma; the two are equivalent
up to a factor about 3 in the budget (b-1 exit chains imply CORE2; CORE2
implies at most 3b+1). What changes is the form of the target: CORE2 asks for a polynomial bound in g on visits to a core of size
O(log g), rather than controlling every possible large-parameter jump.
The positive recurrence removes long excursions outside that core exactly,
including large jumps caused by non-NT collisions.

For example, at rho=2^1000000 the formal bootstrap uses g=2000004 and
K(g)=45. The claim is a structural statement under the induction hypotheses,
not a claim that we have simulated that epoch or proved it globally safe.

The unresolved part is the return system on the correlated state
(j,A,G,C,L,known residues,source provenance). The local constraints of
section 1 eliminate equal-j persistence and immediate alternating
parameter cycles, but do not exclude longer cycles or many revisits.
Proving a rank for these short affine return maps, or a sufficient bound
on their correlated lift information, would prove CORE2. Neither has been
done here. A graph on j alone is not sufficient.

## 6. Exact verification

`verify_core.py` uses full bigint F updates, with the existing work_m
crossing table as read-only input. It checks:

* 2479 actual small F epochs (7308 steps), plus 110 synthetic resonant epochs;
* 148 positive two-a identities, including 116 resonant cases and jumps to 4096;
* 298 exact affine core first-return maps, including returns of length 3;
* mass, local coefficient margins, COUNT, and the absence of three consecutive
  large parameters throughout these tested epochs.

Caveat on the real data. Across the 2479 real epochs (and an auditor's
302,878 real epochs) only about 3-30 chains exceed the cutoff, and no two
are adjacent. The two-consecutive-large checks are therefore vacuous on
real data; the two-in-a-row bound and most resonant checks come from the
110 synthetic epochs. The auditor found 28 real two-a cases, all with
equal parity, so the next j is 1; the maximum observed m is 3 and the
maximum m/g^2 is 0.0156 (Class-C, weak evidence since r<=2 in this range).

The upper bound of two consecutive high chains is nonvacuously attained
by the synthetic parameter sequence 17,5,17,17,1. With g=17 its cutoff is
K=11, so the middle core return 5->17->17->1 has length 3. This example
starts from a synthetic non-empty-list state, not from a level fire. It
shows the two-in-a-row bound is attained, but not that 3m+2 is tight
(here N=5, versus 8 for m=2).

The earlier unbounded-jump constructions were also run past their jump
to the end of the epoch for 109 choices of q. All tested cases end safely;
one is 17,5,4096,2, followed by an even return. These are not actual-orbit
reachability claims or a proof for every q. They illustrate why unbounded
parameter increases alone are not evidence of nontermination.

    python -B work_global_core/verify_core.py

This regenerates core_checks.json; the stored file is that regenerated
output. All outputs are written in this directory. Previous proofs are unchanged.
