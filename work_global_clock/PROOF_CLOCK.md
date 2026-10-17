# A global clock bound before any possible safety failure

2026-10-16. New argument; not independently reviewed. This concerns
the canonical formal pair walk F, not arbitrary locally compatible
states. It does not prove that F has no first safety failure.

## 1. Objective and accepted imports

The accepted Theorem M uses an exit-length hypothesis to propagate
both crossing-time C1 and deficit C2. Here we separate the clock from
the exit-length problem. Let the maximal canonical walk consist of all
defined F steps, together with its last state if the next step is
undefined. We prove clock bounds throughout this maximal prefix,
without assuming that an epoch terminates or has few exits.

Imports from `work_m/PROOF_M.md` and `work_el/PROOF_EL.md`:

* crossings occur at top-level states; their types are a,b,c;
* replay from a safe chain reaches its return after 1+tau(j-1) steps;
* odd b/c returns copy an earlier chain and are automatically safe;
  their next parameter is <=j-2-epsilon(j-1)<=j-3;
* the coefficient recursion is sigma_next=sigma-1-epsilon(j-1),
  with 0<=epsilon(n)<=n;
* S2 is preserved, so a first failure after the base can only be S1;
* lambda mass gives j<=log2(6s+5) at a chain candidate;
* the audited base through N_B=10^8 has tau(n)<=n, and is safe.

We use no unreviewed shadowing or source-compression theorem.

At a possible first-failure endpoint, the head/list state and the
original entries it would inspect are already defined, even though
the attempted chain update is not. We extend the term "crossing time"
to this final inspection only when bounding that state's clock. We
never use such a terminal attempted step as a valid replay source,
and never infer another crossing beyond it. At all earlier crossings
this convention agrees with the usual tau of the defined walk.

Write

    g(n)=ceil(log2(6n^2+5)),
    P(n)=2g(n)^2+1345.                             (P)

## 2. The next-original lemma

Suppose the current crossing X(n) exists and its step is defined.
Then the next unread original is inspected after a finite sequence
consisting of an initial chain and an odd b/c corridor, possibly one
final even step. Reaching this inspection does not require the next
odd a-output chain to satisfy S1.

More explicitly:

1. At type a, the current step reads both E_n and E_(n+1), so their
   crossing times coincide.
2. At type b or c with an even head, the next crossing is one step later.
3. At type b or c with an odd head, start its safe chain of parameter j.
   Each replay contributes 1+tau(j-1). A type-a return already reads
   the next original, whether its next head is odd or even. A b/c even
   return empties the pending list and the following step reads the
   next original. An odd b/c return continues with a parameter smaller
   by at least three.

The corridor cannot continue indefinitely: its positive integer
parameters strictly decrease. Its interior calls and b/c chains are
safe by the earlier-prefix replay lemmas. The endpoint can be the state
of the first failed a-output, but no failed step is executed to reach it.

This proof does not assume the current epoch has ended. It handles a
type-c crossing, and therefore repeated odd a-returns within an epoch,
in exactly the same way as a level crossing.

## 3. Quadratic crossing times by induction on the original index

Assume crossing bounds tau(m)<=m^2 at the earlier indices needed,
and tau(n)<=n^2. At a nontrivial crossing in section 2, its initial
parameter j is <=g(n). All indices used by the corridor are <n,
because S1 gives j<sigma<=the current pointer<=n.

For a b/c input j>=64, the source lambda mass and the already known
clock bound imply

    j_next<=log2(6tau(j-1)+5)
           <=log2(6(j-1)^2+5)<=j/2.              (HALF)

The last inequality holds at 64; its left-minus-right comparison
improves thereafter, since the logarithmic derivative is at most
2/((j-1)ln 2)<1/2. Thus large input parameters have square sum at
most (4/3)j_initial^2. Their individual replay/chain costs satisfy
1+tau(j-1)<=1+(j-1)^2<=j^2.

Below 64 there are at most 21 chains with j<64 in total, because each continuing
b/c step drops the parameter by at least three; each costs at most j<=63. The actual audited
small table has tau(j-1)<=j-1, so each such cost is <=64. Including
the possible final even step yields

    tau(n+1)-tau(n)
       <=(4/3)g(n)^2+1345<=P(n).                (GAP)

The same loose bound covers the zero- and one-step cases.

For n>=N_B put x=log2 n. Since g(n)<=2x+4,

    P(n)<=8x^2+32x+1377<2n+1.                  (INC)

For clarity, at n=N_B use x<27 to bound the polynomial by 8073,
far below 2N_B+1. Its ratio to 2^x decreases for x>=log2 N_B:
the positive-coefficient polynomial has logarithmic derivative at
most 2/x<ln 2. Thus INC is an all-scale inequality.

Consequently, whenever the next crossing is reached,

    tau(n+1)<=n^2+P(n)<(n+1)^2.

Together with the audited base this proves C1 for every reached
crossing, without an exit-length or C2 hypothesis. If the current
crossing step is the first undefined step, the induction stops there;
it does not assert a nonexistent next crossing. Its own time is
already bounded by the preceding induction.

## 4. Near-linear clock throughout the maximal prefix

P is nondecreasing. Summing GAP from the audited base, whose crossing
time is <=N_B, gives, for every reached n>=N_B,

    tau(n)<=N_B+(n-N_B)P(n)<=nP(n).              (CLOCK)

Every defined intermediate state with current original pointer i lies
before the next inspection of E_i. Section 2 and replay reach that
inspection in finite time, unless the current state is already the
first failed crossing. Inner-call and b/c failures are excluded by
the accepted replay lemmas. Thus in both cases

    s<=iP(i)=O(i(log i)^2), i>=N_B.              (STATE-CLOCK)

Below the audited base use its already verified state bound. The same
reasoning also gives s<=i^2 at every state of the maximal prefix.

If the canonical walk is infinite and defined, its original pointer
tends to infinity: a bounded pointer would contradict the finite
next-original lemma. This is progress conditional only on continued
definedness, not on a separate epoch-length assumption.

These are global statements about all reached states. They do not
establish continued definedness. In particular, proving a time bound
at the state of a hypothetical first failure does not rule that
failure out.

## 5. A long safe prefix of every epoch, without C2

At an epoch fire pointer rho>N_B define

    H(rho)=ceil(log2(6(2rho+2)P(2rho+2)+5)),
    R(rho)=floor((rho-H(rho)-1)/H(rho)).          (BUDGET)

The top-level chain with index t has pointer at most rho+2+t, by the
accepted epoch bookkeeping; the initial fire has index zero. For
t<=rho this is <=2rho+2. STATE-CLOCK therefore bounds its candidate
parameter by H(rho), even if this were a first failed chain.

Each preceding odd-return coefficient loss is
1+epsilon(j-1)<=j<=H(rho). This uses only the trivial deficit bound
epsilon(n)<=n, not C2. Hence

    sigma_t>=rho-tH(rho).

For t<=R(rho), this is at least H(rho)+1, strictly exceeding the
candidate parameter. A first failure in this prefix is impossible.
Replays also have already available source indices <rho. Therefore
either the epoch ends earlier, or every chain through index R(rho)
is safe. This is a finite-prefix theorem; it does not assume the epoch
continues forever.

For example, at rho=10^8 the conservative constants are H=44 and
R=2272726. The actual audited behavior is much shorter; the point of
this example is the uniform safety budget, not an observed long epoch.

A hypothetical first failure in such an epoch must consume nearly all
its initial coefficient valuation: G>=rho-H(rho). The remaining
problem is to exclude that much accumulated loss, not to propagate
the quadratic clock.

## 6. A weaker sufficient global exit condition

The following is an **open** sufficient condition, not a new theorem
about the actual exit lengths:

    (SQRT-EXIT) No valid prefix of an epoch at rho>N_B contains
    floor(sqrt(rho))+1 exit chains before an even return.

**Conditional global theorem.** The accepted finite base and
SQRT-EXIT imply that F remains defined forever and its pointer tends
to infinity. No separate assumed C1 or C2 is required.

Proof. Let L=floor(sqrt(rho)). For rho>=N_B,

    (L+2)H(rho)<rho.                             (SAFE)

Thus section 5 safely constructs chains through index L+1 if the
epoch has not yet ended. If they all occur, they contradict
SQRT-EXIT. The epoch must end safely first. Induction over epochs
and the next-original lemma then prove the conclusion.

Here is an analytic check of SAFE. With x=log2 rho, n=2rho+2<=3rho
and log2 n<=x+2,

    P(n)<=8x^2+64x+1473.

The inequality 18(8x^2+64x+1473)+5/rho<rho holds at N_B (use x<27)
and persists by the same polynomial/exponential monotonicity. It
implies 6nP(n)+5<rho^2, so H(rho)<=2x+1. Finally
(sqrt(rho)+2)(2x+1)<rho at the base and thereafter: after division
by rho, both exponential-decay terms are decreasing on this range.

SQRT-EXIT is much weaker numerically than the original log-squared
exit budget. Its proof is still missing. The theorem concerns F;
the separately documented original-machine boundary/endgame obligation
is not silently discharged.

Under SQRT-EXIT one also recovers C2 as a consequence. At any new
type-c crossing the accepted bookkeeping formula gives

    epsilon<=3+t+G<=3+L(H+1)<rho/4.

Types a,b have epsilon 0,1. The last inequality holds at the base and
persists by the same exponential/polynomial comparison, using H<=2x+1.
Thus the induction can recover the earlier source-deficit hypothesis
without using it to establish the clock or the long safe prefix.

## 6.1 A stronger actual-source restriction

An actual level fire of parameter p has s>=(2^p-4)/3 (exit chains only satisfy 2^p<=6s+5). For p>=64 its pointer
cannot be in the audited range, by the already established quadratic
bound. If its pointer rho<=2^p, CLOCK and g(rho)<=2log2(rho)+4 give

    rho >= (2^p-4)/(3[2(2p+4)^2+1345]).

If rho>2^p the same lower bound is immediate. Hence all such actual
source pointers are at least 2^p/O(p^2), independently of an exit-length
hypothesis. This strengthens the old square-root-exponential estimate
from C1 alone, but does not by itself give an exit rank.

For the accepted frontier source p=24480 at s=(2^p-4)/3, substitution
shows rho>2^24445. Indeed at rho0=2^24445, rho0*P(rho0)<s, and rho*P(rho)
is increasing. Its actual b-parent Q=rho+2 obeys the same lower bound.
This excludes additional small-source interpretations of the local
obstruction; it does not establish or refute outer-state reachability.

## 7. Verification and intended next target

`verify_clock.py` checks the exact crossing-gap prediction on 8191
successive original indices using the full pair table. It tests all
four stopping cases, not just observed epoch lengths, and cross-checks
135 inequality instances. The all-scale argument is analytic above.

    python -B work_global_clock/verify_clock.py

This changes the global proof target: one may now seek an independent
upper bound on exit count or coefficient loss as weak as section 6's
budget. A local high rebound remains insufficient to refute or prove
that target. No bound on total core reentries has been derived here.
