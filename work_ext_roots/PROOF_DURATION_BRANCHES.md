# Uniform branches of the duration references

2026-10-19. **Accepted after three-way review (reviews/ext_roots_duration_review_record.md).** This fills some branches of the
duration-reference obligation. It does not close all branches or EXT.
Accepted inputs are C1, Lemma K, HP and exact-phase-two absorption AB.
The predecessor/duration normalization is the preceding unreviewed note.

## 1. PLUS with an initial b return is closed

(Scope, added after review: sections 1-2 use only that X(q-1) is fixed
and that the ceiling C exceeds q. They therefore apply directly to the
original PLUS(m)/MINUS(m) states with C=m-1, not only to D-ROOT; the
original and D-ROOT have the same q and take the same first branch. The
normalization is needed only for the remaining branches: Z(q), PLUS c,
MINUS a/c, and MINUS b with copied parameter outside {5,8}. The AB
reference record is in fact <=p-1, from first-step loss 1+epsilon plus
S1 against sigma_C<=m-epsilon; the stated bound <=p suffices.)

Consider any scalar state x=2^q U, Theta=x+3, U positive odd, with
coefficient ceiling C>q and the canonical table defined through X(q-1).
Suppose X(q-1) is odd type b. It copies the real fire at pointer q-2:

    y=3tau(q-1)+4=2^p V, p<q-2,
    x1=(3/4)x+y, Theta1=x+y+2.

The initial B costs two coefficient units. Compare (x1,Theta1) with
the exact-phase-two state (x1,x1+2). The numerator difference is zero
and the clock difference is x/4, of valuation q-2>p.

If X(p-1) is even (in particular whenever p<=4, since X(0..3) are even),
both tails stop. Otherwise (m=p-1>=4, X(m) odd) AB makes the reference
copy a real epoch beginning at pointer at most p-1. That epoch has
ended before the already reached fire at q-2, so the completed-source
hypothesis is available. Its entire reference tail has

    j_t+Lambda_t<=p<q-2.

HP at precision q-2 transfers the word and termination to the actual
tail. Including the initial B loss, every later record is <q; the
initial record is q<C. Thus the whole PLUS b branch is safe and ends.

This proof works for arbitrary positive odd U and arbitrary outer
ceiling C>q. It therefore applies to D_PLUS(H) whenever its first
return is b, with C=H, without any further duration-specific estimate.
It is not merely a bound for the numerically observed cases.

## 2. Two uniform MINUS b subbranches

For Theta=x-1, the same B copy gives

    x1=(3/4)x+y, Theta1=x+y-2.

If the copied fire parameter p is 5 or 8, its next return is A,
with half-time k=1 or 2 respectively. Direct substitution yields

    x2=(13/8)x+(3/2)y+6k-4.

For p=5, write y=32V: x2=(13/8)x+48V+2 has valuation one.
For p=8, y=256V: x2=(13/8)x+384V+8 has valuation three.
Here V is odd and q>=p+3, so the high x term cannot change these
valuations. The words are exactly

    q,5,1  or  q,8,3.

The cumulative losses are 0,2,3. All records j+Lambda are <=q,
so every record satisfies j+Lambda<C for any ceiling C>q and the next return is even. More generally any
MINUS b input whose copied parameter has an even return stops after
the first B, again with record below q. Other MINUS b cases are not
covered by this argument.

## 3. PLUS a reduces to a specific zero-defect family

Suppose instead X(q-1) is odd type a, with k=tau(q-1)/2. The PLUS
return is

    x1=(3/2)x+6k+6, Theta1=x+6k+6.

Put z=6k+6. C1 gives v2(z)<q-1 for q>=10; the only smaller odd-a
cases q=5,8 satisfy this directly. The state after the return agrees
to precision q-1 with

    Z(q): x=z, Theta=z, z=6k_q+6.             (ZERO)

Indeed the differences are 3x/2 and x, of valuations q-1 and q.
If ZERO terminates with j+Lambda<q-1, HP and the initial A loss
close the original PLUS a branch. If ZERO's initial return is even,
that condition is already immediate; otherwise the full ZERO property
is still unproved.

ZERO must not be identified with an actual b-EXT entry merely because
both have defect zero. An actual b entry has x=3tau+4, whereas ZERO
has x=6k_q+6 and retains a different source correlation. Applying EXT
to it without supplying an actual earlier source would be unjustified.
PLUS c and the remaining MINUS branches remain open as well.

## 4. Genuine S(H) durations can give three chain parameters

The <=8192 duration scan had longest recorded word (5,2). That does
not justify a universal two-parameter bound. The new exact beta
kernel evaluator finds the following genuine S(H) durations (the S(H)
kernels are actual; the corresponding MINUS/PLUS entries are hypothetical,
not reached inside any verified range):

| family | H | Delta_H | duration-reference word |
|---|---:|---:|---|
| MINUS | 13784707579437011870 | 6148914691236517205 | 65,5,1 |
| PLUS | 41354122738311035613 | 18446744073709551617 | 65,5,1 |

For MINUS, Delta_H=(2^64-1)/3, so 6Delta_H+2=2^65.
For PLUS, Delta_H=2^64+1, so 6Delta_H-6=3*2^65.
The kernel evaluator computes S(H) directly from canonical crossing
data, verifies every strict margin, and obtains those exact durations.
It avoids materializing 2^H by using beta coordinates. The source
queries remain inside the accepted cutoff-8208 calendar.

At parameter 65, X(64) is the actual b copy of the parameter-5 fire
at pointer 63. Sections 1-2 therefore supply analytic proofs of these
three-parameter tails, uniformly in their odd numerator base. Their
loss-plus-parameter record is 65, far below the displayed H values.
These are not safety counterexamples or new horizon records; they
refute only the tempting universal two-parameter shortcut.

## 5. Verification and remaining work

`verify_duration_branches.py` checks three odd lifts at every relevant
q<=8192: 7437 PLUS b cases, 387 MINUS b cases copying parameter 5/8,
and 7437 finite PLUS a-to-Z cases. The first two branches have analytic
proofs above. The last set checks ZERO only finitely and does not
prove its all-scale condition.

The huge-index beta kernel evaluator is cross-checked against
the existing kernel implementation at every H=5..512 (508 cases; both
read the same calendar.crossing oracle, so this is a cross-check of the
beta evaluator, not an independent source check),
then verifies the two explicit large duration witnesses. All checks
pass. No bound on arbitrary remaining tails or on global EXT follows.

    python -B work_ext_roots/verify_duration_branches.py
