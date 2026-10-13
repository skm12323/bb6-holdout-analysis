# Allowing a controlled non-descent: a local rescue and one further tower level

Date: 2026-10-13. New research, **not independently audited**.
Existing documents are unchanged. This note concerns the universal formal walk F;
it does **not** prove that the original finite excursions, or machine #1, never halt.

## Status and dependencies

Results obtained here:

1. An exact two-a-transition identity, giving descent over a pair of transitions
   without requiring NT at the second transition.
2. A safe terminal macro for the known obstruction:
   `(17,-2) -> (5,5) -> j=6 -> j=1 -> even return`.
   This is a symbolic argument for every compatible reached state, not a claim
   that these states occur in the actual F orbit.
3. A finite certificate for a complete set of second-level entry families:
   5,000,063 entries; exactly three old NT failures, all resolved by this macro.
4. A proposed extension of the audited finite F horizon by one tower level,
   with proof below. It uses the existing audited base as a black box and the
   new, unaudited finite certificate. No claim of global closure is made.

Dependencies: `work_g6/PROOF_G6.md` section 5; `work_m/PROOF_M.md` sections 2--6;
`work_el/PROOF_EL.md` Theorems A/B/D and the corrected A3 qualification.
In particular, (C1) means tau(n) <= n^2 at already reached crossings.
No EL/PIN conclusion from work_r10, and no claim about its endgame, is used.

Notation: at a top-level chain, j is its parameter, u is the **lambda part**
of its run base, Theta=3s+5, and sigma=v2(c_x). An integer theta represents
Theta modulo 2^j. An a-transition uses n=j-1 and k=tau(n)/2.

## 1. A two-a identity [symbolic]

Suppose a top-level chain of parameter j is followed by two odd type-a returns.
Write q for the intermediate parameter, k=tau(j-1)/2, and l=tau(q-1)/2.
The exact identities from Theorem A, before taking any residues, give

    x1_lambda = 2 Theta + 6k - 2^(j-1) u,
    u1 = x1_lambda / 2^q,
    Theta1 = Theta + 3 + 6k,
    x2_lambda = 2 Theta1 + 6l - 2^(q-1) u1
              = Theta + 6 + 9k + 6l + 2^(j-2) u.             (AA)

The cancellation of q in the final expression is exact. It remains valid
when the second transition violates NT.

**Two-step descent lemma.** Suppose j>=12, |theta|<=10, the earlier crossings
used here satisfy (C1), and both returns are odd type a. Then the first
transition is NT, and the parameter j2 at the second return satisfies

    j2 = v2(theta + 6 + 9k + 6l) <= j-3.

Proof. Since k<= (j-1)^2/2,

    |theta+3k| <= 10 + 1.5(j-1)^2 < 2^(j-2),

so the first transition is NT and q<j. Both k and l are positive integers
because odd type-a crossings have indices at least four. Thus

    0 < 11 <= B := theta+6+9k+6l
      <= 16+7.5(j-1)^2 < 2^(j-2).

The upper bound uses l<= (q-1)^2/2 <= (j-1)^2/2. At j=12 the last
polynomial is 923.5 < 1024. The inequality propagates since
2 P(j)-P(j+1)=7.5j^2-30j+31 > 0 for j>=12, where
P(j)=16+7.5(j-1)^2. The first, smaller polynomial is covered as well.
By (AA), x2_lambda is congruent to B modulo 2^(j-2), proving the claim.

**Safety and no circularity.** If the initial chain has sigma>j, the first
return is safe because sigma1=sigma-1 >= j > q. This justifies its replay.
The second return has sigma2=sigma-2 >= j-1 > j2, so it too is safe.
On the symbolic affine recursion, the margin h=J-Gamma-j changes by
j-q-1 >=0 at the first transition and by j-j2-2 >=1 over both transitions.
Thus a possible second-transition increase spends only some of the margin
earned by the first transition.

This is not a global ranking function: it assumes a bounded representative
at entry and two a-returns. A b/c transition or a large representative still
requires analysis. After the pair one may take theta2=-3k modulo 2^j2;
there is no resulting uniform bound on this new integer representative.

## 2. Resolving the actual finite-certificate obstruction [symbolic]

Assume a safe reached top-level chain satisfies

    j=17, Theta == -2 (mod 2^17), sigma>17.

The inequality sigma>17 is derived, not assumed: section 4 shows
sigma>=18 at every real invocation of this macro.

Write Theta=2^17 z-2, with integer z, and let u be the odd lambda run base.
The audited small crossing data are

| n | type | head pair | tau(n) | epsilon(n) |
|---|---|---|---|---|
| 16 | a | (65536,37) | 12 | 0 |
| 4 | a | (16,7) | 2 | 0 |
| 5 | b | (16,7), partner (16,0) | 2 | 1 |
| 0 | a | (1,1) | 0 | 0 |

For the first a-return, k=6 and

    x1_lambda = 32 [1+2048(4z-u)],
    j1=5, u1=1+2048(4z-u), Theta1=2^17 z+37.

Theta1 == 5 (mod 32). This is exactly the state where the NT-only automaton
reports a tie. Keep the higher bits instead. At the next a-return k=1:

    x2_lambda = 2(Theta1+3-8u1)
              = 64 [1+512(4z+u)],
    j2=6, and Theta2 = Theta1+9 = 2^17 z + 46.

Both brackets are odd; no unspecified high bit affects these valuations.
The next return uses X(5), a b-return copying the parameter-1 fire at step 2,
so j3=1. X(0) gives an even return and the epoch closes.

The successive (j,sigma) are

    (17,sigma), (5,sigma-1), (6,sigma-2), (1,sigma-4).

Every margin is strictly positive already when sigma=18. Replay safety
inside the calls follows from the earlier crossing prefix (indices <=16).
The four call durations, including their initiating chain steps, are
13,3,3,1; the final even step adds one. The macro takes exactly 21 F steps.

In the affine symbolic exit proof, the successive h changes are +11,-2,+3.
In particular a positive h at j=17 remains positive throughout. This proves
symbolic coefficient separation too: the non-descent tie is **not** an
equality of the affine alpha/beta valuations.

`verify_rescue.py` independently evolves the full bigint pair map for 1,004
synthetic, mass-compatible states, including z>2^100 and the tight
sigma=18 case. All produce these top-level parameters and close in 21 steps.
These constructed states are explicitly not asserted to be actual orbit states.

## 3. Complete finite entry certificate [finite computation]

Put N=10^6. Let A0 be all pairs (j,theta) produced by an a-transition in
the exits starting from (J,1), 2<=J<N. Let A1 be all such output pairs in
the finite runs starting from

    (j,0), (j,2), 1<=j<N; and (j,theta-1), (j,theta) in A0.

These are the same level-0 and level-1 objects used in the audited EL proof.
The regenerated sizes are |A0|=27, |A1|=46. A1 records outputs of
a-transitions, not all intermediate states.

The complete new family checked here is

    (j,theta), 1<=j<N, theta in {-1,0,1,2,3};
    (j,theta-1) for (j,theta) in A0 union A1;
    (j,theta-2) and (j,theta) for (j,theta) in A0.          (COVER)

The last two lines contain 68 distinct specific entries. We retain them
even when an entry is also in an any-j family, so counts include overlap.
In particular, route-c entries A1-1 are included explicitly; the old
informational E6 entry set is not assumed to prove this coverage.

Results (`certificate.json`):

| Further chains after the entry | Number of entries |
|---|---:|
| 0 | 1,892,003 |
| 1 | 2,917,464 |
| 2 | 190,537 |
| 3 | 56 |
| 4 | 3 |

Total: 5,000,063. The only NT failures are the entries
(244875,-1), (538715,-1), (832554,-1). Each follows

    entry -> (17,-2) -> (5,5).

Section 2 replaces their unresolved tail by j=6,j=1 and an even return.
Every other entry terminates under the ordinary NT rules. Therefore every
compatible occurrence of a COVER entry terminates with at most four further
chains, under the margin hypotheses of section 4; the only exceptional
tail preserves those margins by section 2.

## 4. One further tower level [proof using the finite certificate]

Define

    H = 2^499998,
    K = 2^(H/2-2) = 2^(2^499997-2).

The audited EL Theorem D covers J<H. We claim that, inside the epoch
induction of Theorem M, every fire parameter J<K has a symbolically
tie-free exit with at most six exit chains. The word tie-free here means
affine coefficient separation, **not** NT at every transition.

Only H<=J<K is new. With (C1) at earlier crossings, the first exit parameter
and the parameter of any W-epoch copied at a c-return obey

    j1 <= log2(6(J-1)^2+5) < H,
    J_W <= log2(3(J-1)^2+4) < H.

The strict bounds follow from 6K^2 < 2^H and the stated definition of K.
All these W-epochs are earlier in time, not future uses of the conclusion.

There are three possibilities for the first return:

* **a:** entry (j1,2), j1<H.
* **b:** entry (j1,0), j1<H.
* **c:** entry (j_W,theta_W-1), where the copied chain is an a-transition
  output in a W-epoch with fire parameter <H (location lemma below).

**Lemma (location of odd type-c crossings).** If X(n) is a type-c crossing
of F whose step at tau(n) is odd, then tau(n) is the return step of a
type-(a) return of a top-level chain t: the crossing sits on an a-return
chain, the state is P=[D_t], and the step reads (D_t,E_n). The chain at
tau(n) (the exit chain that follows this return) is therefore an
a-transition output of the epoch containing chain t. The proof uses no
bound on n, so the statement covers every crossing index, not only n<10^6.

Proof. Crossings occur only at top-level states (PROOF_M Lemma 3.3: no
original is read inside a call window, Lemma 2.2). Every epoch is a level
fire, its call and return, further exit chains with calls and returns,
and a final even step, and every step that is not top-level lies inside a
call window (PROOF_M section 3, Lemma 3.1). So an odd top-level step is
either a fire (state P=empty) or a return chain. A type-c state has P=[Y],
a single entry, so tau(n) cannot be a fire: it is the return step of some
top-level chain t. By Lemma 2.3 the list at that return is [D_t]++R,
[M_u(E_{n_t-1}),D_t]++R or [M_u(Y'),D_t]++R according to type (a), (b),
(c), where n_t=j_t-1 and R is the originals-only tail (Lemma 3.1); the
pending part is the single entry D_t in the type-(a) case (R is the originals-only tail, not a pending entry) and
the two entries M_u(...), D_t in the other two. Since X(n) has the single
entry Y, the return type is (a): Y=D_t, and the step reads (D_t,E_n), one
pending entry plus the first unread original, matching i=n. In the §4 c-case the step is odd automatically (a successor chain exists, so the head H is odd and, by Lemma 2.3's parity clause, so is W's head). As the step
is odd, it is the epoch's exit chain t+1, the chain produced by this
type-(a) return; a c-return with odd head continues
the epoch with exactly this chain (Lemma 3.1), so the copied W-chain is
an a-transition output, for every crossing index.

For the c case, the location lemma identifies the copied chain as an
a-transition output at every index; the audited level-1 construction then
describes every such a-output as either an arbitrary (j,2) with j<N (the
first a-return; its parameter obeys j<=log2(6(J_W-1)^2+5)<log2(6H^2)
=N-1.415<N), or a member of A0 union A1 (all the other a-outputs). When
the W-epoch is below N, the copied first a-return is itself a specific
(j,2) entry of A0, so its theta=1 entry is also a specific A0-1 entry.
Thus this case enters COVER at once, through theta=1 or one of its
shifted specific entries.

For the a/b cases, if j1<N we also enter COVER at once. Otherwise
N<=j1<H and theta is 0 or 2. At its next return:

* an a-transition is NT by the bounded representative criterion, and gives
  (j2,3-theta) with j2<N;
* a b-transition gives (j2,theta-1) with j2<N;
* a c-transition copies an a-output from a W-epoch of parameter <N, hence
  gives (j2,theta+theta_W-2) with (j2,theta_W) in A0.

Here j2<N and the copied fire parameter <N follow from j1<H=2^(N/2-2),
(C1), and the same logarithmic bounds as above. The a bound can be read
directly as j2<=log2(3(j1-1)^2+4). If a return is even, the exit ends earlier.
Thus every new exit reaches COVER after at most two exit chains.
Its remaining tail has at most four further chains: r<=6.

**Margins.** At the fire h=J-Gamma-j=0. The first a-return has j1<=J-2,
by the audited first-return size argument, so h1>=1. A first b/c-return
also gives h1>=1. Every subsequent ordinary NT transition preserves a
positive h by EL Theorem B, and the only non-NT transition is the
section-2 macro, whose h-changes +11,-2,+3 keep h positive as proved
there.

The macro's sigma-hypothesis is derived, not assumed. At every
invocation: at the (17,-2) chain h=J-Gamma-17>=1 gives J-Gamma>=18, and
sigma=rho-Gamma >= J-Gamma >= 18 > 17 (rho>=J at the fire; equivalently
Theorem M's sigma_t > g >= j_t). Thus sigma-1>=17>5, sigma-2>=16>6,
sigma-4>=14>1, and the macro's chains (5,sigma-1), (6,sigma-2),
(1,sigma-4) all keep sigma_t-j_t positive, as section 2 requires.

Tie-freeness here is proved by this h-induction together with the macro,
not by Lemma T's size margin: the d-bound of EL Theorem D, d4 <=
4+(J-1)^2+3*10^6 <= 2J^2, used tau(n)<=n at the later calls, which are
below 10^6 in Theorem D's range; for J<K the first exit index is bounded
only by log2(6(J-1)^2+5) < H, not by 10^6, so Theorem D's argument does not apply verbatim. (Re-review note: the size margin itself still clears — (C1) gives tau(n_1)<=n_1^2, keeping d_6<=2J^2, and 2log2 J+3.585 < 0.75J-62 for J>=10^6 — so this is a choice of route, not a failure of Lemma T.) What the h-induction gives instead: by Lemma T's coefficient
recurrence v2(alpha_{x_t}) = J-Gamma_t, while h_t>=1 says J-Gamma_t >=
j_t+1, so v2(beta_{x_t}) = j_t < v2(alpha_{x_t}) (since lambda_{x_t} =
alpha_{x_t} lambda_u + beta_{x_t} has valuation j_t). That is exactly
the strict comparison required by the recursion of PROOF_M Lemma 6.1: at
the next chain the coefficient valuation exceeds its just-computed j,
forcing the constant term's valuation to equal j. Hence there is no
unhandled symbolic tie.

**After the non-NT step.** The macro's second a-step, from (5,5) with
n=4 (5+3*1 == 8 == 2^3 (mod 16)), violates NT, and the theta rule
theta -> 3-theta of (A3) no longer gives the true representative: the
true value is Theta2=2^17 z+46 == 46 (mod 64), while the rule gives
3-5 == 62 (mod 64). The rule's derivation in (A2) needs j_{t+1}<=n (both
correction terms then vanish mod 2^{j_{t+1}}); here j2=6>4, so the
higher bits decide. The rescued chains (the substituted j=6 and j=1
chains and the closing even step) are therefore not described by any
automaton pair (j,theta); what the induction needs is that no epoch reads
one of them as a copied W-chain.

**Lemma (rescued chains are never copied by any epoch with J<K).** No
epoch with fire parameter J<K copies a rescued chain.

Proof. A b-step copies a W-fire (EL Remark S), and a fire is never a
rescued chain, so only c-copies matter. By the location lemma a c-copied
chain is an a-transition output of a W-epoch E' whose fire pointer obeys
rho'=n-2-a_{t'} <= j_t-3 <= J-4 (PROOF_M Lemma 3.3 at the a-return of
E'; every top-level chain of the copying epoch has j_t<=J-1, since
h_t>=1 before the tie and the rescued tail has j<=6). Hence E' has fire
parameter

    J_W <= log2(3(J-1)^2+4) < log2(3K^2) = H-2.415 < H

(the opening bound of this section). But a rescue occurs only in an epoch
with fire parameter >=H: for J<10^6 the V4 data contain no tie, and for
10^6<=J<H the EL Theorem D exit descends at every step, so no non-NT
step, and therefore no rescue, can occur there. Every copied W-epoch has
fire parameter <H, so no copy can land on a rescued chain.

Note this is the obstruction at the next tower level: the protecting
inequality J_W <= log2(3(J-1)^2+4) < H holds while the copying epochs'
fire parameters stay below sqrt((2^H-4)/3) ~ 0.577*2^{H/2}, true
throughout [H,K); further tower jumps pass this threshold, copies can
then land in [H,K) on rescued chains, and the wrong representative (46,
not the rule's 62) would enter the classification.

**Finite-horizon consequence.** Using the audited base for rho<=10^8,
Theorem M's epoch induction now applies to every epoch whose J<K:
the exit bound r<=6 is smaller than floor(log2 rho)^2. Consequently

    F is defined and its universal walk is non-halting for
    s < (2^K-4)/3,  K=2^(2^499997-2).                       (NEW HORIZON)

Indeed, before that time 3s+4<2^K, so a fire cannot have parameter >=K.
This is a bound on F steps, not on original machine transitions.
Theorem M also supplies s<=i^2 (M2'), and with r<=6 the deficit bound
recomputes into (M1'), Delta <= floor(log2 i)^2 for i>10^8. By Lemmas
3.3-3.4,

    Delta <= 2+t+a_t+sum_{t'<t} epsilon(n_{t'})+j <= 49+epsilon(J-1)+j,

the constant 49 replacing the 31 of Corollary E (t,a_t<=6, and at most
five further epsilon-terms, each <=7 at indices <N). Correction (re-review): the t'=1 term epsilon(j_1-1) may have index in [10^6,H) (case 2), where the bound 7 is not available; there epsilon(n_1)=3+a_{t'}+Gamma_{t'}<=12, because the W-epoch E' has fire parameter <N, so V4 gives r<=2 and V2 gives epsilon<=7 on its crossings. The constant is therefore 54, giving Delta <= 65.5+2.5*log2 i, which still satisfies the bound below; hence, with
epsilon(J-1)<=7+J/4, j<=2log2 i+4, J<=2log2 i+2,

    Delta <= 65.5+2.5*log2 i <= floor(log2 i)^2   for i>10^8

(x^2-2.5x-65.5 is positive at x=log2 i>=26.58 and increasing; for
i<=10^8 the audited V2 gives Delta<=28). No assertion about the
finite-excursion endgame follows merely from this horizon.

## 5. What remains open

The global problem is not solved. Beyond this additional tower level,
new copied representatives and non-descent patterns may occur. Neither
the bounded-entry assumption of section 1 nor a finite collection of safe
macros has been proved closed under arbitrary nesting.

The concrete next target is a ranking argument for blocks of transitions:
account for decreases over a pair or longer block, instead of requiring
NT at every individual a-step. Identity (AA) is an exact starting point,
but b/c copying and the unbounded representatives remain unresolved.
The finite-excursion endgame is a separate unresolved obligation.

## Reproduction and limits

    python -B work_tie/verify_rescue.py
    python -B work_tie/verify_two_a.py

The first command writes only `work_tie/certificate.json`. Both import existing verification
modules read-only. Regenerates the small crossing data and both finite
entry levels; does not re-audit the imported symbolic proofs or rerun the
10^8-step base certificate. Run output is also recorded in `run_main.txt`.
The additional two-a check evaluates the exact identity on 690 integer
instances with actual small crossing data, including 42 second-transition
non-descents; every combined descent and minimal-sigma margin passes.
No repository summary or previously accepted theorem has been edited.
