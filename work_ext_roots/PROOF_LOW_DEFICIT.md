# Low-deficit c sources: two all-scale reductions

2026-10-18. **Accepted after three-way review (reviews/ext_roots_review_record.md).**
These eliminate two source-history classes in a least-counterexample
approach to strict EXT. They do not prove global EXT.

## 1. Accepted inputs and a shadowing criterion

Use the accepted weight identity epsilon=W+1, W=G+a, from
`work_global_root_phase/PROOF_ROOT_PHASE.md`; its acceptance is recorded
in `reviews/global_astra11_review_record.md`. Each odd a or b return
adds two to W, and a c return adds at least four. A type-c source
is an a-output. Therefore:

* epsilon=3 forces source history A: the first a-output after its fire;
* epsilon=5 permits exactly AA or BA. There is no c operation in such
  a history. The letters denote odd return types within the same epoch.

Also use accepted HP, AB, RB and Lemma K from
`work_global_ext/PROOF_EXT.md`, C1 from CLOCK, and the symbolic-to-real
fire transfer from PROOF_M Lemma 6.1 / EGX Lemma TR.

We compare integer scalar walks on (j,x,Theta), where j=v2(x). The
return rules are

    a: x'=2Theta+6k-x/2, Theta'=Theta+6k+3;
    b/c: x'=r_n x+lambda_n, Theta'=Theta+3tau(n)+3,
         r_n=c_n/2^j, n=j-1.

For a continued tail let Lambda be cumulative loss sum(1+epsilon),
starting at zero at the compared entry. HP implies the following
useful formulation: if two entry states have the same j and their
x and Theta differences have valuations at least H, and a terminating
reference tail satisfies j_t+Lambda_t<H at every entry, the other
tail has the same parameter/return word and terminates with it.
If the outer starting coefficient valuation sigma_0 also satisfies
sigma_0>j_t+Lambda_t for the reference word, every outer chain is
strictly safe. Apply HP and this margin inductively, so no step beyond
an unproved first tie is assumed.

Two references will be used:

**Reference F(q).** If EXT(q) holds, a scalar fire-shaped entry
x=2^q U, Theta=x+1 with U positive odd follows the symbolic S(q)
word, ending safely. It has j_0=q, and j_t+Lambda_t<q for later
chains. This is the uniform fire transfer; the reference clock need
not be the time of an actual canonical fire. It is not asserting
canonical reachability of that reference state.

**Reference A2(q).** An entry of exact phase Theta=x+2, v2(x)=q,
terminates by AB if the real epoch it copies is already completed.
Its initial j+Lambda is q, and every later value is <q. Indeed its
first copied chain has coefficient precision q-1-epsilon(q-1), while
the first loss is 1+epsilon(q-1); add these to obtain q. Subsequent
loss is exactly the copied real epoch's loss, so S1 gives strictness.
An even initial return terminates immediately and needs no copy.

## 2. A small common estimate

If X(p-1) is odd type a, p>=5 and k=tau(p-1)/2 is a positive integer.
For p>=10, C1 (with the accepted finite base tau(n)<=n for n<=10^8) implies

    6k+2 <=3(p-1)^2+2 <2^(p-1).               (SIZE)

The strict inequality holds at 10 and persists since the positive
quadratic grows by a factor below two. The only odd type-a cases
5<=p<10 in the canonical table are (p,k)=(5,1),(8,2); both satisfy

    v2(6k+2)<p-1 and v2(6k)<p-1.             (SMALL)

(Notation: in this section p−1 is the index of the type-a crossing X(p−1), so (p,k)=(5,1),(8,2) are X(4), X(7); from section 3 on, p denotes the root chain parameter. The numerical statements are unaffected.)

These estimates will keep the comparison parameter below the retained
precision. They are not bounds on a whole exit's length.

## 3. All epsilon=3 c entries reduce to smaller EXT

**Proposed theorem C3.** Assume F defined through X(J-1), that crossing
is odd type c with epsilon=3, and EXT(q) holds for the smaller parameter
q constructed below. Then S(J) terminates with no tie. In particular,
epsilon=3 cannot occur at a least strict EXT counterexample.

Proof. The source epoch history is A. Let its root pointer be rho,
root chain parameter P and numerator x_0=2^P U, U positive odd.
The real fire phase is Theta_0=x_0+1 and P<rho. Let
k=tau(P-1)/2, where X(P-1) is odd type a. Its first a-output is

    x_C=(3/2)x_0+6k+2,
    Theta_C=x_0+6k+4.

It occurs at original index n=rho+2, hence J=rho+3. By RB the first
S(J) chain is (x_C,Theta_C-1), with starting coefficient valuation

    sigma_0=J-4=rho-1>=P.

Put z=6k+2 and q=v2(z). SIZE/SMALL gives q<P-1, so v2(x_C)=q.
Use the reference F(q) starting at (z,z+1). The two differences are

    delta_x=(3/2)x_0, delta_Theta=x_0,
    min(v2 delta_x,v2 delta_Theta)=P-1.

The reference has j_t+Lambda_t<=q<P-1. HP therefore makes the outer
tail follow it to termination, and sigma_0>=P>j_t+Lambda_t ensures
strict safety throughout. All reference call indices are <=q-1,
strictly below the already defined source indices. Also
q<P<rho<J, so EXT(q) is available in the least-counterexample induction.
QED.

No shallow-source certificate, MASS extension, or fixed cutoff on P
is used. The theorem is conditional on smaller EXT(q); it must not
be advertised as unconditional EXT for arbitrary epsilon=3 sources
without that hypothesis.

## 4. Epsilon=5 with history BA is absorbed

**Proposed theorem C5-BA.** Assume F defined through the outer c source
and its source history is exactly BA. Then S(J) terminates tie-free.
This uses completed earlier real epochs, not EXT at an arbitrary new
virtual zero-defect root. Among epsilon=5 sources it leaves AA open
(superseded: AA is handled in PROOF_A_SOURCE_DESCENT.md §1).

Proof. Let the source epoch's fire be (rho,P,x_0=2^P U,Theta_0=x_0+1).
Its first return is type b. Lemma K identifies X(P-1)'s chain as the
real fire at pointer P-2, with

    y=3tau(P-1)+4=2^p V, V positive odd,
    p<P-2.

Its chain coefficient is 3*2^(P-2), so the B map's coefficient ratio
is 3/4. The source epoch after B has

    x_B=(3/4)x_0+y, Theta_B=x_0+y.

The following A reads X(p-1), with half-time k. Its output and the
shifted outer phase are

    x=(13/8)x_0+(3/2)y+6k,
    Theta=Theta_C-1=x_0+y+2+6k.               (BA)

Since P>=p+3, the first two summands in x have valuations at least
p and exactly p-1. SIZE/SMALL gives q:=v2(6k)=1+v2(k)<p-1, so v2(x)=q.
Compare with the exact-phase-two reference (x,x+2). Their x difference
is zero, and

    delta_Theta=-(5/8)x_0-y/2,
    v2(delta_Theta)=p-1.                      (PRECISION)

The source has one A and one B, so n=rho+2, J=rho+3 and
sigma_0=J-6=rho-3>=P-2>=p+1.

The reference A2(q) may copy an epoch beginning at pointer at most
q-1. Since q<p<P<rho, that real epoch has ended before the source
epoch's fire at rho (canonical epochs have disjoint increasing pointer
intervals). Its source data and end are therefore already defined.
AB makes the reference terminate with j_t+Lambda_t<=q<p-1.
HP with precision p-1 transfers the word to (BA); sigma_0>=p+1
keeps the entire outer tail strictly safe. QED.

This argument deliberately uses an exact phase-two reference, which
has the accepted absorption theorem. It does not replace it by an
unproved claim that every constant-phase family terminates.

## 5. The remaining lowest-deficit case and the synthetic control

**Subsequent proposal:** `PROOF_A_SOURCE_DESCENT.md` supplies the missing
actual b-source comparison for AA, and extends it to all c sources
whose epoch begins with A. The earlier gap description below records
why phase zero alone was insufficient; it is superseded by that
stronger provenance argument (since accepted).

Assuming these proposals pass review, a least EXT counterexample
with a c-type first source must have either epsilon=5 and history AA,
or epsilon>=7 (superseded: with PROOF_A_SOURCE_DESCENT the AA case is
excluded and the c frontier is epsilon>=7 with a b/c-first source epoch). Type-b outer entries remain open. The existing finite
horizon and all previously accepted sufficient routes remain unchanged.

The AA history is not closed here. Its shifted phase is congruent to
zero at the current chain precision, but zero-defect tails are the
b-type problem itself. A congruence to phase zero does not supply an
actual earlier b-source or a complete tail theorem. Nor may one apply
the finite zero-defect search to arbitrarily large parameters.

The previous diagnostic fake c source (time 27, H=(64,7), Y=(448,75))
has epsilon=3, real Theta=86 and chain x=160 of parameter five. A
canonical first-A output necessarily has real Theta=2 mod 2^q,
by the formulas in section 3. But 86=22 mod 32, excluding that fake
source from this canonical history class. This explains its failure
of provenance algebraically, rather than merely checking its small
index against a stored table. Its local exact tie was never an EXT
counterexample.

## 6. Verification and limits

`verify_low_deficit.py` uses the accepted exact calendar with cutoff
512. For root parameters P=5..256 it selects canonical fires and
verifies 76 A-source and four BA-source c crossings, including
their exact deficit, source formulas, parameter words, shadow
precision and outer coefficient margins (86 compared tail states).
These include outer indices far beyond a direct finite-step simulation;
the calendar stays inside its certified boundary.

It also tests 18 algebraic BA outer lifts with nonterminal phase-two
references (36 compared states), using actual inner fires and actual
call data. The chosen outer P=p+3 in those additional tests is NOT
claimed to be the canonical b-parent pointer; these are explicitly
algebra checks, not further reachable-source examples. This exercises
absorption rather than only terminal small parameters.

The two small productive A cases and 4087 instances of SIZE pass.
The all-scale proofs are the algebra, accepted imports and induction
above, not these finite checks. Independent review is still required.

    python -B work_ext_roots/verify_low_deficit.py
