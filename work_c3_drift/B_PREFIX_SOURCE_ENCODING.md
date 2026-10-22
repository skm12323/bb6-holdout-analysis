# A source certificate for arbitrary pure-b prefixes before AA

2026-10-21. **UNREVIEWED proposed all-parameter lemma.** Extends the
fixed BBBAA certificate to a reached B^tAA prefix of arbitrary length.
It proves the joint source budget, not termination of the later tail.

## 1. Every phase class has an explicit bounded-height encoding

Given an integer source phase Phi at parameter m>=1, set

    Q=3^m, C=Q+((Phi*Q-Q) mod 2^m).

Then Q<=C<Q+2^m<=2Q, so c=C/Q lies in [1,2] and h(c)=0.
After reducing the fraction its rank r is at most m. Since
C=Phi*Q mod 2^m, there is a uniquely determined bit b in {0,1}
such that

    Phi=c+b*2^m mod 2^(m+1).

Thus a source whose accumulated loss G satisfies G+3m<P always
has a certificate G+m+2r+h(c)<P. The bit must be retained. This
encoding is not claimed optimal in rank and does not automatically
make the next state large relative to its denominator threshold.

## 2. Reached B^tAA sources, with t>=1

Suppose a real source epoch of root parameter P>=512 reaches

    P --B^t--> p --A--> 5 --A--> m.

All b parameters drop by at least three. Hence t<P/3 and p<=P.
Let L_i, i=0,...,t-1, denote the source fire numerators, indexed
backwards: L_0 has parameter p and L_i has parameter at least p+3i.
Every read source index is below P. C1 therefore gives

    0<L_i<=3*(P-1)^2+4.

The sparse affine recurrence sums explicitly. After the two a steps,

    alpha=1+(3/4)^t/4,
    beta=sum_i[1+(3/4)^i/4]*L_i + 9k+13-t,
    theta_beta=sum_i L_i+6k+13-t,
    G=2t+2, k=tau(p-1)/2.

The physical numerator is alpha*X0+beta, with coefficient valuation
P-G. No cancellation test on 9k+13-t is needed below, including when
it is exactly zero. All these dyadic expressions are integral on the
specified source hierarchy.

## 3. A uniform small-part bound pays for the encoding

The largest source satisfies L_(t-1)>=2^(p+3(t-1))>t, with p>=5.
Every coefficient in beta's sum is at least one, so beta>0.
Every such coefficient is at most 5/4, k<=(P-1)^2/2, and t<P/3.
Therefore

    beta < (5/4)*P^3+(9/2)*P^2+(5/3)*P+13 <2P^3.

The latter inequality holds for P>=16: divide by P^3 and check
at 16, after which all nonconstant terms decrease.

Put m0=v2(beta). For 2^e<=P<2^(e+1), e>=9, the preceding bound
gives the convenient conservative estimate m0<=3e+4. Hence

    G+3m0 < (2/3)*P+9e+14 <P,

because 3*(9e+14)<2^e for every e>=9 (true at 9 and preserved
when the exponential doubles). In particular m0<P-G, so the root
coefficient cannot alter the output parameter: m=m0, uniformly in
the actual odd root base. Also P-G>m+1, giving the extra phase bit.

The real phase Phi is congruent to theta_beta-beta modulo 2^(m+1):
its remaining root coefficient has valuation P-G. Apply section 1
to this exact class. It yields the strict source contract

    G+m+2r+h(c) <=G+3m<P.

No all-scale EXT assumption is used to justify the later tail. The
hypothesis is only that the stated canonical source prefix is reached,
with the imported source/C1 identities on that prefix.

## 4. Copy consequence and limits

The source is an odd c crossing at n=rho+3, with
epsilon=n-(rho-G)=2t+5. Thus the result covers unbounded deficits
inside this pure-b-prefix family. Its actual phase certificate can
be inserted in JOINT_HEIGHT_BUDGET, so a b/c parent copying it pays
both inherited rank and height from its record drop.

This general encoding trades precision for denominator size. Taking
Q=3^m may put the emitted parameter m below the adaptive threshold
N_Q even when m is numerically large. Therefore the result does NOT
license the next large-parameter contraction rule automatically.
For BBBAA, the explicit low-rank 10/3 description remains preferable;
the generic encoding is a valid fallback for the source budget.

Mixed b/c prefixes, different a-return patterns, roots below 512,
and arbitrary continuation after copying are not proved here. In
particular this does not close the strengthened induction or change
the accepted horizon.

## 5. Verification

    python -B work_c3_drift/verify_b_prefix_encoding.py

All 16,380 phase classes for m=1..12 are encoded with the correct
extra bit, reduced rank bound and zero height. Twenty-two algebraic
prefix tests, including five exact-zero values of 9k+13-t, verify
the affine size/budget calculations. Their call half-times come from
the canonical table, but their outer source lifts are not asserted
to be actual B ancestries. The all-parameter assertion is proved by
the inequalities above and is pending independent review.
