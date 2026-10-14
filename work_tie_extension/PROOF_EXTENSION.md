# Copy-aware residue certificates: extending the finite F horizon once more

**Status: Supplementary to the audited work_tie2 Theorem TIE2 (same horizon K′);
contribution = exact b/c margin gain + bigint kernel checks + information-loss construction.**
Adversary review (2026-10-14): "with fixable gaps", no structural defect; fixes applied below.

2026-10-13. New derivation and computational certificate.
Scope: the universal formal walk F. This is not a global non-halting proof,
and it does not close the finite-excursion endgame.

## 1. Results and dependencies

Write

    T0 = 1,000,000,
    T_(d+1) = 2^(T_d/2 - 2).

Thus T1=2^499998 and T2=2^(2^499997-2) are the earlier thresholds.
The new certificate supports the following extension, with the proof below:

> Inside the epoch induction of Theorem M, every fire parameter J<T3 has
> an exit with at most seven exit chains, with strict affine coefficient
> separation throughout. Consequently F is defined and non-halting for
> s < (2^T3-4)/3.

The result uses the audited base and symbolic identities from
`work_g6/PROOF_G6.md`, `work_m/PROOF_M.md`, `work_el/PROOF_EL.md`, and the
previous two-level analysis in `work_tie/PROOF_RESCUE.md`, and
`work_tie2/PROOF_TIE2.md` (its copy rule, its coverage induction, and its
corrected deficit inequality floor(log2 i) >= J/2-2). The new computational
obligation is the complete third-layer certificate in `certificate_layers.json`.
It does not use the purported all-v endgame closure or the EL/PIN proof tree.
We assert Theorem M's quadratic time and cubic-logarithmic deficit conclusions
on the new finite range, not an independently rederived quadratic-log bound.

The verification program was adapted from `work_tie2/verify_tie2.py`
(committed in d38aa62), read as a reference, without modifying that directory.
The snapshot hash in the program header (DA278BF3...) is stale: the current
committed file hashes to 67bd2b9f..., because verify_tie2.py was edited after
the snapshot was taken. The adversary review compared the two and found the
make_ext core unchanged apart from the edits listed here. Changes here include the exact
b/c margin increment, rejecting nonpositive margins, limiting unresolved
searches, exporting complete output families, and stopping at an incomplete
layer. This is not an independent implementation of that reference algorithm.
The separate kernel checks use full bigint crossing coefficients as an oracle
only for b/c steps. For a-steps the oracle uses the same symbolic formula as
the engine, x = 2*theta+3*tau-u*2^(j-1); it is tied to bigint data only through
the head identity lambda_head+lambda_Y = 3*tau+1 (lambda = 3*tau+1), checked for n < 2048.

## 2. Why copied states need additional information

At a chain write j for its parameter, u for its lambda run base,
Theta=3s+5, and sigma=v2(c_x). For an epoch with initial fire parameter J,
let Gamma be the accumulated coefficient valuation loss and put

    h = J-Gamma-j.

The physical margin is sigma-j = rho-Gamma-j >= h, since rho>J at the fire.
The known rescue contains a non-NT transition 5 -> 6. At the new j=6 state,
the true Theta is 46 modulo 64, whereas continuing the old reflection rule
would give 62 modulo 64. Thus one cannot feed the old theta representatives
through another round of c-copying without correcting this information.

Use a residue record

    (j, T, M, U, m; h0)

meaning Theta=T mod 2^M, u=U mod 2^m, and h>=h0>0.
U is odd and m>=1. This denotes an overapproximation of compatible states;
it is not an assertion that every member occurs in F. Forgetting bits enlarges
the set. A successful certificate must close every retained possibility.

## 3. Exact transfer rules and soundness

### 3.1 a-return

Put n=j-1, k=tau(n)/2. The exact formulas are

    x_new = 2(Theta+3k)-2^n u,
    j_new = v2(x_new), u_new=x_new/2^j_new,
    Theta_new=Theta+3+6k,
    h_new=h+j-j_new-1.

From the residue record, x_new is known modulo 2^B, where
B=min(M+1,n+m). If its residue is nonzero, its valuation and the low
B-j_new bits of u_new are fixed. Retaining fewer bits is safe.

If the residue vanishes, the implementation splits the next unknown bit of
Theta or u into both values, refining the component that limits B. This is
an exhaustive split of the residue set, not an arbitrary choice of a lift.
At a search cap, missing crossing data, or h_new<=0, it reports an incomplete
certificate. It does not interpret that outcome as a counterexample orbit.
In the successful third-layer run **no bit splitting was needed**.

### 3.2 b/c-return using a finite crossing

Let the chain of W at tau(n) have parameter j_W, lambda run base u_W,
and sigma_W=v2(c_xW). Replay gives

    j_new=j_W,
    u_new=c_uW*u+u_W,
    Theta_new=Theta+3*tau(n)+3,
    h_new=h+n-epsilon(n)-j_W=h+v,
    v=sigma_W-j_W>=1.

Here sigma_W=n-epsilon(n): in type b this follows from the original pair
coefficients, and in type c from c_A+c_Y=2^n and c_x=2^(n+1)-c_A.
Verification status of this identity: it is checked against full bigint pair
coefficients only for n < 2048 (`verify_kernel.py`). For 2048 <= n < 10^6 the
certificate relies on PROOF_M Lemma 3.2 together with the internal consistency
of the walk; the adversary review additionally checked it on all 318,728 odd
b/c crossings with n < 10^6 against the walk's own recursion.
Since c_uW/2^v and u are odd,

    u_new = u_W+2^v (mod 2^(v+1)).

The program keeps at most 4096 bits. The increment **v**, rather than merely
the lower bound 1, is used in the margin accounting. The full-pair oracle
checks the coefficient identity and the recorded chain data at the 651 odd
b/c crossings with n < 2048.

### 3.3 Copying a previously certified a-output

An odd type-c crossing of W is an a-return chain: its pending list is the
single entry D, as in PROOF_M Lemmas 2.3 and 3.3. Therefore only the a-output
families of earlier W-epochs need to be exported for c-copying.

Suppose a source output has residue data (j,T,M,U,m) and a certified lower
margin h0. Its physical c_uW is divisible by 2^h0. Thus after any copy,

    u_copy = U (mod 2^min(m,h0)).

Also Theta_copy=Theta_W+Theta_outer-2. A first return after a fire shifts
T by -1, because Theta_outer=1 modulo 2^J. A return from a large chain with
known representative theta shifts T by theta-2, retaining precision at most
the available outer precision. Here every large chain has j>=T0, while
exported records have M<=4096, so all exported Theta bits can be retained.

For the new band T2<=J<T3, the first-fire precision also exceeds 4096.
Lower bands were already certified, so no assumption of this much precision
at a tiny fire is made.

The six extended a-output records of layer 2 are explicitly present in
`certificate_layers.json`. Three have j=5 and T=655397,1441829,2228261;
three have j=6 and T=655406,1441838,2228270. Their low residues are 37
modulo 64 at j=5 and 46 modulo 64 at j=6. The first c-copy shifts them to
36 and 45 respectively, not to residues obtained from the invalid reflection.

### 3.4 Coefficient separation

Ordinary NT steps preserve h>0: an a-step has j_new<=j-1; a b/c-step
increases h by at least one. At an extended step, the computed exact valuation
and the checked inequality h_new>0 give

    v2(alpha_x)=J-Gamma > j_new=v2(lambda_x).

Hence v2(beta_x)=j_new for lambda_x=alpha_x*lambda_initial+beta_x.
This is the same strict comparison required by the affine exit recursion.
It validates the next division and replay, without presupposing NT there.
Every tested extended run starts from the conservative bound h0=1 and
keeps its minimum at least 1.

## 4. Coverage of the third layer

Use bands R0={1,...,T0-1} and R_i=[T_(i-1),T_i) for i>=1.
Thus R1=[T0,T1), R2=[T1,T2). In a new epoch with T2<=J<T3,
its first exit parameter and any first copied W-fire parameter are <T2.
This follows from (C1) and

    j_next <= log2(6(j-1)^2+5),
    J_W <= log2(3(j-1)^2+4),
    6*T_(d+1)^2 < 2^T_d.

(For clarity, the band convention is R_i=[T_(i-1),T_i) for i>=1;
R0 is the finite table. The code indexes large bands 1 and 2 accordingly.)

The entry-family construction is a descending-band induction:

1. First a/b returns produce representative 2/0 in any lower band.
   First c returns copy any a-output family of a lower-layer epoch, shifted
   by -1, with the extended transfer rule when needed.
2. In each large band, an a-return reflects theta to 3-theta; a b-return
   subtracts one; a c-return adds theta_W-2. The target is in a strictly
   lower band. Every relevant representative is bounded, so the large
   a-steps satisfy NT by the size argument.
3. At R0, exhaust every j<T0 for each any-j representative, every specific
   pair, and every extended residue record. Collect all a-output records
   for possible future copying, retaining their proved precision.

In code, these sets are `big`, `small_any`, `small_spec`, `small_x`, and
the output triples `AO[layer]`. Every c case uses all smaller admissible
source layers, including their any-j, specific, and extended outputs.
Duplicate entries are allowed; no class is removed merely because it looks
unreachable. Counts therefore describe certificate entries, not orbit states.

The generated large-band representatives in layer 3 are

    R2: {0,2},
    R1: {-1,0,1,2,3}.

They are in the bounded window needed for the large-index NT size bound.
The finite families are:

    7 any-j families, theta in {-2,-1,0,1,2,3,4};
    102 specific pairs;
    6 copied extended residue records.

All finite continuations resolve. At most three exit chains occur up to
and including entry into R0, and at most four further chains occur after
that entry. Hence r<=7. Paths that terminate earlier only improve the bound.

## 5. Certificate results

The finite F table is regenerated to i=10^6, taking 892137 steps and
recording 326639 top-level chains. The existing 10^8 base certificate is
used as an audited dependency, not rerun here.

| Layer | Certificate entries | Extended entries/runs | Unresolved | Max further chains |
|---|---:|---:|---:|---:|
| 1 | 2,000,024 | 0 | 0 | 3 |
| 2 | 5,000,059 | 3 | 0 | 4 |
| 3 | 7,000,101 | 13,949 (= 13,943 + 6) | 0 | 4 |

Of the 13,949 layer-3 extended runs, 13,943 are genuine NT ties (specific
'pair' entries); the remaining 6 are the copied 'X' entries, which are NT-safe
extended inputs run with the extended engine for their retained precision,
not ties.

The different counts from work_tie are due to canonicalizing theta modulo
2^j and deduplicating specific pairs, not reducing the admissible residue set.

Layer-3 continuation counts:

| Further chains | Count |
|---|---:|
| 0 | 2,648,803 |
| 1 | 4,065,716 |
| 2 | 273,657 |
| 3 | 11,922 |
| 4 | 3 |

Every extended run has one terminal leaf, no bit splitting, and positive
minimum h starting from h=1. This is stronger than merely observing a
successful numerical representative: the arithmetic decisions are uniform
over the full retained residue set.

New safe tails go beyond the old 17->5->6->1 macro. Examples include

    (90,-2) -> (5,5) -> (5,14) -> (1,1),
    ... -> (5,5) -> (8,174 mod 256) -> (3,5),
    ... -> (5,5) -> (17,43694 mod 2^17) -> (7,85),

followed by an even return. The largest observed parameter immediately
after these non-NT steps is 19. This is a statement about the certified
families, not a universal upper bound on such steps.

The kernel check samples 3,012 concrete lifts (1,004 sampled starting parameters — 4 hand-picked tuples plus 1,000 random (j,T) draws, seed 20261013 — x 3
lifts). Of these, 152 are skipped (count obtained as 3,012 − 2,860; the script has no explicit skip counter) (x <= 0 or a needed crossing beyond the
n < 2048 data), and the remaining 2,860 are compared against the residue
predictions and exact margin increments, including 12 non-descending
transitions. In these comparisons b/c steps use full bigint crossing
coefficients; a-steps use the symbolic formula of section 3.1 (see section 1).
It also checks the 651 odd b/c crossings with n < 2048.
These tests supplement the symbolic transfer proof; they are not an
independent review of the full induction.

## 6. Finite-horizon theorem

Apply Theorem M's induction over epochs. For rho<=10^8 use its audited
base. At later epochs, retain (C1),(C2) at earlier crossings. The coverage
and coefficient-separation argument above give r<=7 whenever J<T3.
This is smaller than floor(log2 rho)^2, so the remaining time, margin,
and progress estimates of Theorem M apply unchanged; for the deficit bound
we use the corrected inequality of PROOF_TIE2 (step 6),
floor(log2 i) >= J/2-2 (from 3s+4 >= 2^J and s <= i^2), exactly as in
work_tie2 Theorem TIE2.

Before s=(2^T3-4)/3, every fire has

    2^J <= 3s+4 < 2^T3,

so J<T3. Thus the induction certifies F throughout that finite range.
This threshold is one more application of T -> 2^(T/2-2) beyond work_tie.
It is a count of F steps, not original Turing-machine steps. It does not
imply all finite excursions are safe after they read their boundary defect.

## 7. An obstruction to forgetting lift information [symbolic]

For every integer q>=7, there is a mass-compatible top-level pair state
with j=5 and Theta=5 mod 32 whose next top-level parameter is exactly q.
This is a family of synthetic states, not a reachability result for F.

Choose sigma=q+2, i=sigma+1, s=2^(q-2), and

    A = (2^sigma, 2^(q-1)-27),
    P = [(2^sigma, 2^(q-2)+28)].

Then the c-mass is 2^i, the lambda mass is 3s+1, all components are
positive, and

    lambda_x = 2^q+32 = 32(2^(q-5)+1),
    j=5, u=2^(q-5)+1,
    Theta=3*2^(q-2)+5 = 5 (mod 32).

The X(4) a-return has k=1. Its next chain satisfies

    lambda_x_new=2(Theta+3-8u)=2^q,
    j_new=q, sigma_new=sigma-1=q+1>q.

In the pair map, the chain at step 0 is odd with
c_x=3*2^sigma, j=5; the new pending list is [w,2w,4w,8w,D] with
w=(3*2^(sigma-5), 2^(q-5)+1), D=(2^(sigma+1)+2^(sigma-1), 2^(q-2)-13), and
A=(3*2^(sigma-5), 2^(q-5)+2). The two intermediate steps are even, since
sigma>=9 and q>=7 make both components of A even:

    step 1: A <- A+w+2w+(0,3) = (3*2^(sigma-3), 2^(q-3)+8),
    step 2: A <- A+4w+8w+(0,3) = (3*2^(sigma-1), 2^(q-1)+23).

Step 3 is odd, with b=D; using the odd-step rule x = A + 2b + (0,3) of the pair map (PROOF_M/PROOF_G6 §5): c_x=13*2^(sigma-1), lambda_x=2^q, as claimed.
These are polynomial identities in 2^q, so they hold for every q>=7.
Both chain margins are safe, yet the parameter jump is unbounded.
The exact full pair-map check additionally covers q=7..512 and q=4096,65536 (508 cases).
This does not contradict any actual-orbit bound: these states have not been
shown reachable, and are not claimed to satisfy all earlier-time hypotheses.
It proves that a bounded-j continuation theorem based only on (5,5),
positivity, mass, and local safety cannot work.

## 8. Remaining work and limits

The third-layer certificate exports 99 ordinary specific a-output pairs and
35801 extended a-output records, in addition to its any-j families. This
growth is a warning about the cost of naive repeated finite enumeration,
not a proof that the arithmetic class set is infinite or cannot be compressed.

A fourth-layer covering certificate has not been run in this directory.
More generally, there is no all-depth bound on the number of residue records,
the necessary precision, or exit length. Section 7 explains why a proof must
retain ancestry/lift restrictions, rather than universally close a small
(j,theta) state set. The separate finite-excursion endgame remains open.

Reproduce:

    python -B work_tie_extension/explore_layers.py 3
    python -B work_tie_extension/verify_kernel.py
    python -B work_tie_extension/verify_unbounded_lift.py

Only this directory receives output files. Existing proofs and work_tie2
are unchanged. No commit or remote operation was performed as part of this directory's work (the d38aa62 note above refers to work_tie2).
