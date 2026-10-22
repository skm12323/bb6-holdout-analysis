# A uniform copy certificate for the large-parameter BBBAA source family

2026-10-21. **UNREVIEWED proposed source-certificate theorem.** This
handles the family used in UNBOUNDED_C_PARAMETER_IF_EXT without
imposing any fixed upper bound on its output parameter m. It does
not certify every deficit-eleven source or the whole copied tail.

## 1. Hypotheses concern a reached source prefix

Let an actual source epoch start at pointer rho and fire parameter P.
Suppose its first returns are BBBAA, with parameter sequence

    P,q2,q1,p,5,m.

The three b steps give q2>=q1+3, q1>=p+3 and P>=p+9. Let k be
the half-time of the canonical odd-a call X(p-1). The formulas below
apply whenever this source prefix is reached; no global EXT or
termination of the source's later tail is assumed.

The first a-output is five precisely when v2(6k-4)=5, since all
other affine terms have higher valuations. C1 supplies the required
separation at p>=10, and the small odd-a cases p=5,8 are direct.
The canonical base then shows p>=17. The following small numerator is

    Z=9k+10, m=v2(Z)>=5.

For p>=17, C1 yields

    0<Z<=4.5*(p-1)^2+10<2^(p-3), so m<=p-4.

The polynomial bound holds at 17 and persists by its growth factor
below two. Thus the second a step also has strict affine separation.

## 2. Full affine phase, including the root contribution

Let X0 be the root numerator of valuation P and let L2,L1,L0 have
valuations q2,q1,p. After the displayed five returns, loss is 8 and

    x=(283/256)*X0+(73/64)*L2+(19/16)*L1+(5/4)*L0+9k+10,
    Theta=X0+L2+L1+L0+6k+10.

Therefore

    Phi=Theta-x
        =-(27/256)*X0-(9/64)*L2-(3/16)*L1-L0/4-3k.

Every term except -3k has valuation at least p-2>=m+2. It follows
that the real source phase has the extra-bit representation

    Phi=(10-2^m)/3=10/3+2^m mod 2^(m+1).

The term containing X0 is retained in this calculation; it is not
discarded merely because an analogous beta-only formula exists.

## 3. The source budget closes without a size cutoff on m

There are two a outputs. The latter is a c crossing at n=rho+3,
with coefficient valuation rho-8. Thus epsilon=11 and omega=m.
Its certificate has source loss G_s=8, rank r_s=1, and
height h(10/3)=2. Its joint budget is

    G_s+omega+2*r_s+h = m+12 <=p+8 <P.

This is exactly the earlier-source contract required by
JOINT_HEIGHT_BUDGET. It is proved directly from the reached prefix,
without assuming that contract for the remainder of this epoch.

## 4. Arbitrary parent phase and the copied class

Let an outer chain with rational representative c_p copy this source.
The generic c rule and the source's retained bit give

    c_new=c_p+4/3, output lift bit 1,
    r_new<=max(r_p,1), h(c_new)<=h(c_p)+2.

The exact output parameter is m by source S1. The source contract
proved above and the copy-budget calculation ensure a strict drop
of the outer joint reserve; in particular the bound from that lemma
is at least rho-P (and rho-P>=3 under the canonical clock estimate).
The copied parameter may be arbitrarily large; neither CAL-C nor
HR5 is used for this particular transition.

For an integer incoming theta in [-2,4], the low rational numerators
are -2,1,4,7,10,13,16 over denominator three, each with the same
lift bit. Their later continuation still needs appropriate descent
or landing certificates. This note proves the copy's phase and
budget, not unconditional termination of all those rational tails.

## 5. Relation to the unbounded-parameter obstruction

The preceding conditional all-m construction produces exactly this
history. Hence its large c parameters are not a reason to exclude
the family: it has a bounded-height phase and a proved source reserve.
This supplies a phase-sensitive alternative to the impossible fixed
cap identified in UNBOUNDED_C_PARAMETER_IF_EXT.

Other histories at epsilon=11, sources with more preceding b/c steps,
and later outputs of the same epoch are not automatically covered.
They require their own provenance calculation or a uniform extension.
The source-contract induction and global EXT remain open.

## 6. Verification

    python -B work_c3_drift/verify_bbbaa_copy_certificate.py

57 canonical odd-a calls p<=4096 satisfy the first-five condition.
Sparse affine checks include the root coefficient, all source terms,
valuation separation and the exact extra phase bit. Another 1,767
parent-phase copies check the height/rank update and budget inequality.
The large ancestors are specified through the earlier spectrum
construction, not directly simulated. The all-p claim rests on the
analytic formulas and inequalities and is pending independent review.
Accepted horizon claims are unchanged.
