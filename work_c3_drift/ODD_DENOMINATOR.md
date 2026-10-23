# A uniform rational-mode lemma for odd denominators

**Review status (2026-10-23):** reviewed via the work_landing_symbolic three-way review (reviews/landing_symbolic_review_record.md, group 2). Status: accepted as an [A-cond] local tool. §1 is [A] only for Phi∈{1,2,3} (a, b, c3, AA, BA steps): with a rational shift (e.g. BBBAA, Phi−2=4/3) the claims Q'=Q and 'preserves coprimality' fail (Q=3,C=2 collapses; Q=5,C=1 gives 23/15); the height recursion also fails (first violation t=8). §2 [A | fixed Q, eps∈{3,5}, eps>=7 c steps leave the window, A+h_Q<=B, R_0<=J]; the conclusion is only descent below N_Q (coarse threshold 4(d+2); r=1e7 gives N_Q=63,398,512 vs exact ~25,849,627). §3 [A] given X(4) odd a with k=1. §4 only for j>=N_Q.

2026-10-20. **UNREVIEWED proposed lemma.** This replaces separate
denominator-3 and denominator-9 descent calculations with one
parameterized argument. It does not close the landing problem or HR5.

## 1. Exact representation and recurrence

Let Q>1 be odd, gcd(C,Q)=1, and represent a chain's defect by

    D = C/Q+b*2^j (mod 2^(j+1)), b in {0,1}.

The size used below is the real height |C|/Q, not the size of the
symmetric integer residue. At an odd a return with half-time k,
if p=1+v2(3Qk+C)<=j-2, the exact successor is

    j'=p, C'=3Q-C, Q'=Q, b'=0.

The proof is the same direct substitution as RATIONAL_MODE, now
using the integer numerator 3Qk+C. It cannot be zero because
gcd(C,Q)=1 and Q>1. At a strict b/c step,

    C'=C+Q*(Phi-2), Q'=Q, b'=0.

Both preserve coprimality with Q. In particular b/cAA subtract Q,
cBA adds Q, and c3 leaves C unchanged. Reflection C->3Q-C
preserves |C/Q-3/2|, so after t permitted steps

    |C_t|/Q <= A+t,
    A=max(|C_0/Q|, |3-C_0/Q|).

These statements concern a fixed denominator between gateways.
No claim that the denominator remains fixed across a bare tie is made.

## 2. Denominator-dependent threshold, proved analytically

Keep N0=20,000,000 and B=2^(N0/2). Put

    d=ceil(log2 Q), N_Q=max(N0,4*(d+2)).

The accepted bound P_clock(j-1)<=j-1 gives
kappa(j)<=(3/2)*(j-1)^2<2^(j/2) for j>=N0. For the last inequality,
the squared polynomial comparison holds at N0 and persists because
2*j^4/(j+1)^4>1 for j>=6. Also B<=2^(j/2).
For every j>=N_Q,

    Q*(kappa(j)+B) < 2^(d+j/2+1)
                         <=2^(3*j/4-1)<2^(j-2).

Thus, whenever |C|/Q<=B, the a numerator is nonzero and below
2^(j-2) in absolute value. There is a strong descent by at least
two and the next precision bit is known. This proof works for
arbitrarily large Q; it does not hold j's threshold fixed while Q grows.

Define the nondecreasing contracting bound

    L_Q(j)=max(1+floor(log2(Q*(kappa(j)+B))),
                floor(log2(6*(j-1)*P_clock(j-1)+5))),
    h_Q(q)=min{t: L_Q^t(q)<N_Q}.

It satisfies L_Q(j)<j for j>=N_Q. If A+h_Q(q)<=B, and every c step
with epsilon>=7 in this rational-mode prefix exits below N_Q,
then a walk starting at q>=N_Q ends or lands below N_Q within
h_Q(q) high-parameter chains. All those transitions strictly lower
the record. Induct the height bound and contraction simultaneously,
as in RATIONAL_MODE. The high-deficit c condition is still an OPEN
condition on the actual rational trajectory; it is not implied merely
by replacing the old cutoff N0 with N_Q.

## 3. The gateway map also has a uniform denominator formula

At parameter five suppose QD=C mod 2^H and the exact next numerator
y has m=v2(y)<H. The identity 3D'=15-D-y gives

    D'=(15Q-C)/(3Q)+2^m (mod 2^(m+1)).

After reducing the rational fraction, its denominator is either Q
or 3Q: gcd(15Q-C,Q)=1, and only a factor 3 can cancel. It remains
an odd denominator >1. For Q=3^r and gcd(C,Q)=1, it always triples.
The real height obeys

    |(15Q-C)/(3Q)| <= 5+|C/Q|/3.

Thus a gateway need not cause unbounded real-height growth, but it
does increase denominator complexity. The output precision bit is
1; a subsequent strong descent resets it to 0. The hypothesis m<H
is essential and is not supplied by the minimal six-bit landing class.

Following an a descent after that emission gives the rational map

    c -> (c-6)/3.

For c_0=5 it yields c_r=-3+8/3^r, exactly the already accepted
3-adic obstruction orbit. This calculation is a consistency check
with that result, not a claim to have removed the obstruction.

## 4. What the lemma does and does not remove

The same analytic argument now handles the large-parameter part of
every odd-denominator mode. There is no need to prove a fresh size
lemma for denominators 27, 81, and so on. All-scale descent in that
part still depends on the explicit height and high-deficit c conditions.

Crucially, a fixed finite landing certificate is still insufficient:
N_Q increases with log2 Q. Even while N_Q=N0, infinitely many distinct
rational residues arise. Bare ties require actual precision provenance,
and the record budget must survive repeated gateways. The new lemma
does not prove any of those three missing facts. It therefore does
not contradict the accepted finite-generator obstruction theorem.

## 5. Verification

    python -B work_c3_drift/verify_odd_denominator.py

11,164 exact a-step checks exercise both input precision bits at
odd denominators including 3,5,7,9,27,81,243 and 3^20. Another 256
gateway checks verify the reduced denominator and output bit.
33 exact size checks include denominator bit lengths around five
million, where N_Q actually increases beyond N0. All pass.
The checks are algebraic controls, not assertions of canonical
reachability or global landing certification. The all-j size statement
rests on section 2's analytic inequalities, not extrapolation from them.
