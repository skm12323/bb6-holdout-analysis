# Canonical-source targets requiring much more than three extra bits

2026-10-20. **UNREVIEWED relative to the accepted imports.** These are
safe shifted tails, not EXT counterexamples. They refute extrapolating
the previous sample's 1--3 extra certificate bits to all shifted real
fires. No claim of an unbounded canonical family beyond the proved
finite horizon is made.

## 1. Exact parameterized construction

Choose a canonical fire at half-time k and pointer r with

    v2(9k+10)=m>=5,       P=r+1>=m+4.

Thus X(P-1) is an actual odd-a crossing with tau(P-1)=2k.
Since 3(3k+2)=(9k+10)-4, this source fire has parameter 3.
The source is established by exact Calendar navigation, not merely
by solving a local phase congruence.

The accepted finite-spectrum theorem in
work_g2_obstruction/PROOF_SPECTRUM.md section 3 says every
P+4<B=2^(2^499997-2) occurs as a real fire parameter, at its specified
target time 2*T_P. Its numerator x0 is 2^P when P is even and 5*2^P
when P is odd (P>=3). We use that actual fire, with the counterfactual
clock shift eta=-3. Its initial state is (x0,x0-2).

The first a return reads the canonical X(P-1), giving

    x1=3*x0/2+6k-4,     Theta1=x0+6k+1.

Since 3*(3k-2)=(9k+10)-16 and m>=5, v2(6k-4)=5.
Therefore j1=5, and D1=Theta1-x1=5-x0/2 is 5 mod 2^(P-1).
The next return reads X(4), whose half-time is 1, and gives

    x2=5*x0/4+9k+10,    Theta2=x0+6k+10.

The high term has valuation P-2>m, so j2=m exactly. Moreover,

    3*(Theta2-x2) = 10-x2-x0/2,
    D2 = (10-2^m)/3 mod 2^(m+1).

This is the accepted gateway family. P>=m+4 retains the extra bit.
For the tested 5<=m<=256, its certificate is within the accepted
5<=m<10^8 range and is also re-executed independently with Calendar.

The original unshifted root ends at its first a return: its output
is x1+6, of valuation 1, because k is even and 6k+2=2 mod 4.
These examples therefore belong exactly to TERMINAL-COLLISION,
not to an unrelated artificial phase family.

## 2. Required cylinder precision and safety

Measure loss from the j1=5 state. The next state j2=m costs one,
so its relative record is m+1. A strict HP-cylinder certificate
with precision K must have K>=m+2. The gateway certificate bounds
the whole remaining relative record by m+1, so K=m+2 suffices.

Modulo 2^K the input state has residues

    x1=6k-4, Theta1=6k+1 (mod 2^K), K=m+2.

These are re-executed in the verifier and have exactly the predicted
maximum record. Relative to the minimal j1+1=6 bits, the extra
requirement is m-4. This is a statement about strict record/HP
certificates; it is not a universal information-theoretic lower bound
on every conceivable symbolic proof.

Physical safety is not threatened. The accepted real root has pointer
rho_outer>P, so the shifted root starts with record P<rho_outer.
Its entire tail from x1 has record <=m+1; including the first a loss
gives <=m+2<P. It therefore terminates strictly within the physical
precision. The same calculation supplies a uniform suffix certificate
for the corresponding residue cylinder.

## 3. Finite canonical selection

For each m=5..256, search the first 64 nonnegative lifts of

    k = -10/9 mod 2^m,

retain exact valuation m, and ask Calendar(512) whether k is an
actual fire. All 252 targets are found; in fact lifts 0 or 1 suffice.
The matched pointer P-1 and time 2k are checked through crossing().
The outer root's existence is supplied by the accepted spectrum
theorem, NOT by running Calendar beyond its boundary. The verifier
checks the sufficient bound P+4<2^499997<B. It never materializes
2^P when P is huge. Eight moderate examples P<=10000 also receive
direct full-integer two-step checks.

The m=256 target has

    k=167255240009456726722935867234771422454723311183703036945883176900318965035462,
    P=374954718097621994772030709527852398293085871064349085864977075934615689685979.

Its shifted residual cylinder has word (5,256,2), strict precision
K=258, and therefore needs 252 bits beyond the minimal class encoding.
The root is a real canonical fire by the finite-spectrum theorem.
The eta=-3 perturbation is counterfactual; this note does not prove
that the shifted state itself is reached by an unshifted S(J).

Reproduce:

    python -B work_c3_drift/verify_targeted_precision.py

All canonical-source checks, cylinder executions, and gateway-class
checks pass. Full exact records are in targeted_precision_checks.json.

## 4. Consequence for the proof strategy

The earlier 1--3 extra bits were a property of a small source sample.
A fixed three-bit repair, or any cap below 252 extra bits, cannot
cover even this certified finite family. This does not prove that
no finite universal cap exists: that stronger statement would require
unbounded canonical reachability, which is not established here.

Parameter-dependent gateway identities already handle these examples
without enumerating all their high-bit lifts. The remaining global
task is to control such symbolic families and their physical record
budgets across arbitrary reachable histories, rather than to extrapolate
a bounded residue table from a short scan. No accepted horizon changes.
