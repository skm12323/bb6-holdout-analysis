# Canonical predecessor and duration normalization for MINUS/PLUS

2026-10-19. **Accepted after three-way review (reviews/ext_roots_duration_review_record.md).** Earlier ext_roots reductions were
accepted in commit 5119184; see reviews/ext_roots_review_record.md.
The reduction here does not establish global EXT or family closure.

## 1. A nontrivial entry immediately follows a large epoch

An odd a crossing X(m-1) is a canonical fire at pointer m-1 and
time 2k. The correlated families are

    MINUS: x=6k+6, Theta=x-1;
    PLUS: x=6k-2, Theta=x+3.

Their initial q=v2(x)<m-1 is already known. If q<=4 they end
immediately, because the crossings X(0..3) are all even. If q>=5, MINUS requires k=15 mod16 and PLUS k=11 mod16.
Neither is the initial fire k=1, so an immediately preceding fire
k0 exists. Write H for its parameter and Delta=k-k0.

The accepted small kernels give Delta_1=1, Delta_2=1, Delta_3=2,
Delta_4=2. For each residue r=k0 mod16 other than 10, the parameter
1+v2(3r+2) lies in 1..4. The complete 15-residue transition table
r -> r+Delta_(1+v2(3r+2)) never lands at 11 or 15. Therefore

    H>=5, k0=10 mod16;
    Delta=5 mod16 (MINUS), Delta=1 mod16 (PLUS).

This is an all-clock statement from an exact finite residue table,
not extrapolation from a sampled trajectory. The relevant large epoch
is the immediate predecessor; intervening small epochs cannot produce
the landing in question.

## 2. Exact removal of the large absolute clock

Inside a least strict EXT-counterexample argument at outer index J,
the family input m is smaller than J. The predecessor parameter obeys
H<rho0<m-1, where rho0 is its fire pointer. Thus EXT(H) is available.
The accepted uniform kernel construction gives the actual predecessor
half-duration Delta_H independently of its odd fire base.

Put X0=6k0+4=2^H U. Since k=k0+Delta_H, the family states are

    MINUS: x=X0+6Delta_H+2, Theta=X0+6Delta_H+1;
    PLUS: x=X0+6Delta_H-6, Theta=X0+6Delta_H-3.

Define smaller duration references

    D_MINUS(H): z=6Delta_H+2, Theta_ref=z-1;
    D_PLUS(H): z=6Delta_H-6, Theta_ref=z+3.     (D-ROOT)

Both differences equal X0, so the original and reference states
agree to exactly H bits. Delta_H must remain the actual kernel
duration, not a freely chosen integer with the same residue class.

## 3. The reduced initial parameter is below H

EXT(H) bounds the number of exit chains by H-2. Including the fire,
there are at most H-1 calls, each costing <=1+(H-1)^2 by C1. The
final even step gives

    L_H <= (H-1)(1+(H-1)^2)+1,
    Delta_H=ceil(L_H/2)<=H^3.

For H>=16, 6H^3+2<2^H, checked at 16 and propagated because the
positive cubic grows by a factor below two per increment. The actual
small kernels verify 0<6Delta_H-6<6Delta_H+2<2^H for H=5..15.
For larger H, Delta_H>1 also follows from the pointer-speed lower
bound on tau(H-1). Hence in both cases

    0<z<2^H, q=v2(z)<H.

The original initial valuation is the same q. In particular it is
at most floor(log2(6H^3+2)), rather than depending on the size of
the predecessor's absolute clock.

## 4. The exact remaining sufficient condition

If the applicable duration reference terminates and every entry on
its tail satisfies

    j_t+Lambda_t<H,

where Lambda is loss relative to D-ROOT, accepted HP at precision H
transfers its whole word to the original MINUS/PLUS state. (HP needs
x* != 0 along the walk: D_MINUS (Theta=z-1, z>=8) and D_PLUS (Theta=z+3,
Delta>=17) lie in the positive cone Theta>=5, 0<x<=2Theta-5, so x*!=0.) Its
required ceiling m-1 is strictly larger than H, so termination and
the original family margin follow.

Only Delta_H=5 mod16 for MINUS, and Delta_H=1 mod16 for PLUS, need
this condition; all other nontrivial landings were excluded above.

The condition is NOT proved for arbitrary H. D-ROOT is not S(H).
Knowing EXT(H) supplies the duration but does not automatically supply
the new reference tail's margin. The reduction decreases the parameter
controlling the input size while changing the initial-state family.
Ignoring that change would create a circular proof. Higher c deficits
and outer b entries also remain outside this reduction.

## 5. Verification and limits

`verify_duration_reduction.py` checks all 15 small-kernel residue
transitions. Consecutive actual fires through original index 999999
give 653 nontrivial MINUS predecessor/shadow checks. Further canonical
fires of parameters 5..256 and their successors give 14 cases per
family. Some cases may overlap. Each check matches actual duration,
pointer advance, H-bit differences, and complete terminating words.

Examples: H=10, Delta=5 gives D_MINUS z=32 and word (5,2);
H=38, Delta=17 gives D_PLUS z=96 and the same word.

For H=5..8192, the verifier checks the initial size bound and tests
every relevant duration class: 458 D_MINUS and 461 D_PLUS cases.
All terminate within the H ceiling. This is finite evidence only;
the source data stay within an accepted cutoff-8208 calendar.
No horizon extension or global theorem is claimed.

    python -B work_ext_roots/verify_duration_reduction.py
