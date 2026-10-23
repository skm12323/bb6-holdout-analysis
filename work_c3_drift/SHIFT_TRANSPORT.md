# Common-shift ancestry transport for interior c steps

**Review status (2026-10-23):** reviewed via the work_landing_symbolic three-way review (reviews/landing_symbolic_review_record.md, group 2). Status: §2–§4 accepted as an [A] conditional reduction (for integer eta, which is exactly the case needed since eta=theta−2 is an integer by construction), with added statements: j_D=j_C, reference calls inside X(0..J−1), the definition of eps_D, and the Lemma K(c) citation; x*≠0 is implicit in Safe (v2(0)=∞ violates the margin) and should be stated. §5 is thin [B] evidence; the terminal family is [C].

2026-10-20. **UNREVIEWED conditional lemma.** No new horizon and no
global EXT conclusion. This moves beyond enumerating individual deficits:
the transport applies to every later c source in an A-initial epoch,
including mixed histories, using the accepted A-SOURCE correspondence.

## 1. Keep the shifted safety obligation explicit

For a reached real chain C, let its scalar state be (x_C,Theta_C),
where x_C is its lambda numerator, Theta_C=3*s_C+5, and let sigma_C
be its physical coefficient valuation. Define Safe(C,eta) to mean:

    the scalar walk from (x_C,Theta_C+eta) terminates, and every
    parameter plus accumulated loss is strictly less than sigma_C.

Loss is measured from this chain, not from the beginning of its epoch.
This predicate is not assumed for every eta. In particular, real-chain
safety Safe(C,0) does NOT imply Safe(C,eta) for arbitrary eta.

## 2. Uniform common-shift lemma

Suppose actual source chains D,C satisfy

    v2(x_D-x_C), v2(Theta_D-Theta_C) >= sigma_C,
    sigma_D > sigma_C,

and the reference calls are defined. Then, for EVERY integer eta,

    Safe(C,eta) implies Safe(D,eta).

Proof: adding the same eta to both phases preserves the two initial
precision inequalities. HP at precision sigma_C transfers each step
of the strictly bounded reference walk. Its parameters, return types,
and accumulated losses are identical. Its records are <sigma_C<sigma_D,
so the D walk terminates with the required stronger physical margin.
Apply HP only up to the next step; strictness supplies its hypothesis
at each extension. No failed tie is crossed by assumption.

This is a general precision lemma. Its useful content here is that the
accepted A-SOURCE theorem supplies the hypotheses with genuine earlier
canonical chains, rather than freely selected matching residues.

## 3. Canonical ancestor and interior application

Take an odd c source D that is a later a-output of an A-initial epoch
(exclude its first A output, handled by NOTES.md). The accepted proof
PROOF_A_SOURCE_DESCENT sections 2--3 constructs an earlier chain C with

    sigma_C=p-1-e-Lambda_source,
    sigma_D-sigma_C=rho-p-1>0,

and both scalar differences divisible by 2^sigma_C. C is either an
earlier real fire (use its b crossing), or an earlier actual a-output
(use its c crossing). Its original source index is strictly smaller
than D's, and its epoch is already complete. The construction precedes
the old proof's choice eta=-1; it therefore supports all common shifts.

Now let an arbitrary outer symbolic chain T read D's c crossing n.
Write j=n+1, x_T=2^j*u, and choose an integer theta with

    Theta_T-x_T = theta (mod 2^j).

The outer c successor satisfies

    x_u = c_D*u+x_D,
    Theta_u = Theta_T+Theta_D-2,
    eta = theta-2.

Since v2(c_D)=sigma_D=n-epsilon_D<j, this successor agrees with
(x_D,Theta_D+eta) to precision sigma_D: the x error is c_D*u;
the phase error is Theta_T-theta, divisible by 2^j.
Combining with the canonical ancestor correspondence gives agreement
with (x_C,Theta_C+eta) to precision sigma_C.

Therefore Safe(C,theta-2) suffices to terminate the entire outer tail.
This preserves the incoming theta; it does NOT silently set theta=1.
The global record accounting is particularly simple:

    Gamma_u=Gamma_T+1+epsilon_D,
    Gamma_u+sigma_D=Gamma_T+j=R_T.

The transported tail has relative records <sigma_C<sigma_D, hence
global records <R_T. Even if R_T=J at the original root, all these
successor records are strictly below J. The result is independent of
the source deficit and of a fixed deep threshold or finite window.

## 4. Recursive normalization, and exactly where it stops

If C is again a later a-output in an A-initial epoch, apply the same
canonical ancestor construction to it. Each replacement has a strictly
smaller original source index, so this recursion is finite. The common
shift eta is unchanged, and each transport retains a strict margin.

The resulting terminal obligation is Safe(E,eta), where E is one of:

* a real fire, represented by its b crossing;
* the first A-output of an A-initial epoch;
* a c source in an epoch whose first odd return is b or c.

For the first A output the earlier c3 formula supplies an explicit
reference (z,z+2+eta), z=6k+2, with precision P-1 and q<P-1. This
reduces its safety if that reference's records stay below P-1;
it does not certify every eta automatically.

Thus all later A-initial c sources can be removed from an interior
shifted-safety proof obligation without an epsilon cutoff. The
remaining shifted fire and b/c-initial families are still unbounded.
This is a uniform reduction, not a proof of those residual families.

For eta=-1 this recovers the accepted least-counterexample A-SOURCE
argument: the earlier b/c crossing supplies a smaller strict EXT
instance. For eta=0 the earlier real chain's completed actual tail
is safe by S1. For other eta, neither ordinary EXT nor real S1 alone
provides Safe(E,eta). That distinction prevents a circular global proof.

## 5. Verification and an explicit negative control

Run python -B work_c3_drift/verify_shift_transport.py.

Four actual AA/earlier-b ancestor pairs, each tested at eta=-32..32:
260 transferred cases pass. All these small ancestors are terminal;
they do not exercise mixed-history transport or long continuations.

For nontrivial continuations, 76 canonical b-reference chains with
p<=256 are tested with eta=-32..32 and synthetic congruent lifts
at precision p-1. The 4,940 terminating references match their lifts
through 5,345 states. Those lifts are NOT claimed canonical sources.

Four additional deliberately chosen shifts make the next a-step
numerator equal 2^(p-1), reaching the precision ceiling. The verifier
retains them as unresolved, rather than asserting transport safety.
They show why a theorem asserting Safe(C,eta) for all integer eta
would be false even with a canonical C. They are not EXT counterexamples:
the forced shifts have not been shown reachable in S(J).

All general-history content depends on the accepted AB/HP ancestry
proof, not on extending these finite tests beyond their stated scope.
Further work must control the reachable shift eta for the terminal
families, including their first non-descent and subsequent record budget.
