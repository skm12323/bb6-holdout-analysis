# Exact clock cylinders for arbitrary return words

2026-10-16. New research result, not independently reviewed. This applies
to aperiodic as well as periodic words. It gives exact necessary affine
constraints and a first-failure filter, not an all-word stopping theorem.

Imports are the canonical crossing/replay and safety bookkeeping of
`work_m`, the exact mixed-block maps of `work_g2_mixed_blocks`, and
their composed valuation identities proved in `work_global_period`.
The crossing clock C1 is assumed where used. The separate new
`work_global_clock` note proposes to supply it on the maximal defined
prefix without assuming epoch termination.

## 1. What can be decided without knowing the high coefficients

Consider a fixed entry word w=(q_0,...,q_n). Every entry before the
last is productive: its known b/c corridor ends at an odd A return.
The last entry may be terminal or a prospective unsafe chain. Write

    x_(i+1)=-(alpha_i/2)x_i+2Theta_i+c_i,
    Theta_(i+1)=Theta_i+3T_i,
    c_i=6d_i+6k_i-B_i/2,
    e_i=G_i+1, v2(alpha_i)=-G_i.

These exact maps hold up to the candidate output, without assuming
that the next chain update is safe. All source data used to obtain
them must be earlier defined data; arbitrary invented source clocks
are not covered by the canonical interpretation.

Let E_i=sum_(t<i)e_t. Multiplying the composed map by 2^E_i gives

    2^E_i x_i=A_i x_0+B_i Theta_0+C_i, A_i odd,

with integer coefficients. Exact valuation q_i is equivalent to

    x_0=p_i Theta_0+r_i modulo 2^K_i,
    K_i=E_i+q_i+1,                              (ROOT-CONG)

where the odd A_i is inverted modulo 2^K_i. Initially p_0=0,
r_0=2^q_0 and K_0=q_0+1. Every p_i is even, since the clock
coefficient in each block map is 2.

**Clock projection theorem.** Either the word is inconsistent, or
all integer solutions to its affine valuation constraints have the
exact parametrization

    Theta_0=r_theta modulo 2^H,
    x_0=p Theta_0+r_x modulo 2^K,
    K=max_i K_i.                               (CYLINDER)

These are all solutions of those constraints, including arbitrary
high bits. Positivity, coefficient margins, and actual reachability
are separate conditions. A surviving cylinder is not a trajectory
certificate.

Proof and algorithm. Retain the ROOT-CONG with largest modulus as
the anchor. To add another, compare it with the anchor modulo the
smaller modulus. The compatibility condition is one linear congruence
in Theta_0. Divide by the common power of two of its coefficient and
modulus. A nondivisible right side means no solutions; otherwise an
odd inverse yields one residue class for Theta_0. Intersect this with
the existing clock class. If the new ROOT-CONG has larger modulus,
make it the new anchor.

Because all moduli are powers of two, agreement with the largest
anchor implies agreement with all smaller anchors already processed,
under the accumulated clock condition. This proves necessity and
sufficiency by induction. It also proves the representation does not
discard the shared starting variables between successive returns.

`clock_words.py` implements this with exact integers and fractions.
It uses one clock class and one root congruence instead of repeatedly
parametrizing a two-dimensional lattice. Bit lengths still grow with
cumulative loss; no constant-cost or all-scale runtime claim is made.

## 2. Clock precision and nonperiodic recurrence spacing

For i<j write E_(i,j)=sum_(i<=t<j)e_t. The subword map has

    x_j=a x_i+b Theta_i+c,
    v2(a)=-E_(i,j), v2(b)=G_i+2-E_(i,j).

Since x_i=2^q_i modulo 2^(q_i+1), and likewise for x_j, this fixes
Theta_i to a residue modulo 2^H_(i,j), where

    H_(i,j)=min(q_i-G_i-1,
                 q_j+E_(i,j)-G_i-1).           (PREC)

If the resulting right side is not dyadically integral, the word is
inconsistent. Translate by the known time from entry 0 to i to obtain
the same-precision congruence for Theta_0. The pairwise compatibility
conditions of ROOT-CONG are exactly these subword conditions. Thus,
for a consistent word of length at least two,

    H=max_(i<j) H_(i,j).

For a one-entry word H=0. The implementation also handles that case.

As Theta_0=3s_0+5 and 3 is odd, a feasible word fixes a unique time
residue s_w modulo 2^H. Therefore any two occurrences of the same
word in the canonical walk, both starting at fire or A-output states
(where STATE holds), with starting times s<t, satisfy

    t-s is a positive multiple of 2^H.          (SPACING)

The intervening sequence can be arbitrary and aperiodic. Within an
integer time interval of width S, this word occurs at most
1+floor(S/2^H) times. This counts one fixed word; it does not bound
the number of different words or their combined occurrences.

For example the word (17,5,17) gives

    Theta_0=32702 modulo 65536,
    s_0=10899 modulo 65536.

Repeated appearances of this three-entry word must therefore be
separated by at least 65536 F steps, even if the intervening words
are all different. No periodicity assumption is used.

## 3. Exact entry-height filtering without enumerating time values

At an entry immediately after an odd A return, the reconstructed
head/tail lambda values are 2Theta_0-x_0-5 and x_0-Theta_0+1.
Their nonnegativity requires

    Theta_0-1<=x_0<=2Theta_0-5.                 (MASS)

This condition alone neither establishes a valid coefficient state
nor guarantees all later margins. It is a necessary local filter.

With CYLINDER, write s=s_w+2^H t, t>=0, and Theta=3s+5. For fixed
Theta, write x=pTheta+r_x+2^K u. The exact number of integers u
satisfying MASS is

    floor(((2-p)Theta-5-r_x)/2^K)
      -floor(((1-p)Theta-2-r_x)/2^K).           (COUNT)

Since s>=0 gives Theta>=5, the real interval is nonnegative in
width, so this difference never counts a negative number of lifts.
Summing over a bounded time interval reduces to two sums of floors
of linear functions. `count_entry_lifts` evaluates them by Euclidean
division, without iterating over every admissible time.

For the fixed words below the first time at which this affine and
initial-mass filter admits a lift is:

| Word | Earliest admitted F step |
|---|---:|
| 5,17 | 29136 |
| 17,5,17 | 207507 |
| 5,17,5,17 | 731792 |

These are exact minima for the stated local filter, not claims that
the canonical walk reaches these words then. For example (17,5,17)
has a time residue 10899 but its early residue representatives fail
MASS. This illustrates why a residue class by itself should not be
mistaken for a positive compatible starting state.

## 4. Impose the true fire instead of a free entry

For a word starting at an epoch fire the stronger exact identity is

    x_0=Theta_0-1=3s_0+4.

Substitution in the anchor gives

    (1-p)Theta_0=r_x+1 modulo 2^K.

Since p is even, 1-p is odd. Therefore the word either contradicts
its clock class or prescribes one time residue

    s_0=s_*(w) modulo 2^K, 0<=s_*(w)<2^K.      (FIRE)

`fire_projection` computes this and checks compatibility with the
whole clock cylinder. Its modulus grows with the full accumulated
coefficient loss, rather than only with the largest parameter.
This is an exact projection of the fire-rooted affine constraints;
it still does not prove that this time is a canonical fire time.

The three nontrivial examples in section 3 are all impossible as
words starting immediately at a fire. They can be considered only
as later-entry words. This distinction is enforced computationally.

## 5. A quadratic-seed necessary condition for the first failure

Suppose a canonical epoch at pointer rho has a first safety failure
at the final candidate entry q_n of a finite mixed-block word. Its
earlier entries and replay sources are valid; odd b/c copies are safe,
so the candidate failure must be an A output (PROOF_M Lemma 3.2 / Cor. 3.5:
S2 is preserved and odd b/c returns are copies). The fire time is the
crossing time of original rho, s_0=tau(rho). Let

    E=sum_(i<n)(G_i+1), M=E+q_n,
    P=max_(i<n)(E_i+q_i).

The coefficient valuation at entry i is rho-E_i. Earlier safety and
the final failure give

    rho>=P+1, rho<=M.

In particular the last E_i+q_i must be a strict new record. Also
K=max_i(E_i+q_i+1)>=M+1. Assume C1 at the root fire:

    s_0=tau(rho)<=rho^2<=M^2.

For M>=5, M^2<2^(M+1)<=2^K. FIRE now forces the exact equality

    s_0=s_*(w), and s_*(w)<=M^2.               (SEED)

There is at most one possible starting time, rather than an infinite
residue class, for this word to witness a first failure. The root
pointer must lie in the finite necessary interval

    max(P+1,E+1,ceil(sqrt(s_*(w))),5)<=rho<=M.  (INTERVAL)

The positive coefficient-valuation condition E+1 is a harmless
additional necessary lower bound. Actual A-output margins before a
failure generally yield a stronger one. Cases below the audited base
are already safe and do not need this asymptotic filter.

`failure_pointer_interval` returns an empty result when the affine
word, fire identity, quadratic seed bound, or interval is impossible.
A nonempty result is only a candidate: it does not certify a fire
at that time/pointer, available sources, or a failure on the orbit.

This supplies a concrete global proof target. To exclude first
failures, it suffices to exclude every remaining word with a strict
new record M, a quadratically small seed s_*(w), and a nonempty
INTERVAL, under the canonical earlier-source hypotheses. We have
not proved that exclusion. In particular, no general lower bound on
s_*(w) growing faster than M^2 has been established.

## 6. Checks and limits of this advance

Run `python -B work_global_clock_words/verify_clock_words.py`.
The new projection is compared with the existing independent
two-dimensional lattice solver on 9072 words/attempted extensions
over the productive alphabet below 64. The feasibility counts and
the entire projected clock residue and modulus agree; 1458 explicit
integer lifts also satisfy every retained valuation constraint.
The finite frontier again exhausts at length seven.

Additional checks cover 540 signed floor sums, four bounded-time
counts against direct enumeration, and 144 fire-rooted formal lifts.
No word in this finite experiment survives the first-failure filter.
This small comparison validates the new representation; it is not
an extension of the accepted large non-halting horizon.

The filter's nonempty branch is also checked on deliberately invented
source data: changing the actual k(7)=2 to k(7)=21 makes the word
(8,9) admit seed 84 and pointer interval [10,10]. The invented clock
still obeys 2k<=7^2, but it is not the canonical clock. This test
illustrates that C1 by itself cannot replace the exact source data
in a proof excluding every surviving candidate.

The advance is that arbitrary return histories can now be filtered
by exact clock, entry height, and true fire data without resetting
their shared variables. The missing global argument is the uniform
exclusion or loss control for the residual unbounded word family.
The separate original-machine boundary/endgame obligation is also
unchanged. Global G2/non-halting remains open.

2026-10-17 continuation: `PROOF_FAILURE_BUDGET.md` proves a finite
all-parameter bound for the unsafe final extensions of a fixed prefix
and derives larger conditional loss budgets. The verifier now also
checks all unsafe-last possibilities for 504 finite-base prefixes;
safe large-output continuations remain outside that last-step check.
