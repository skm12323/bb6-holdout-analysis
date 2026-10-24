# A source certificate pays for inherited denominator rank

**Review status (2026-10-24):** reviewed via the work_gateway_trains three-way review (reviews/gateway_trains_review_record.md, group 2). Accepted as a conditional result [A-cond]; not a global ranking function.

2026-10-21. **UNREVIEWED conditional composition lemma.** Applies to
b and c copies at arbitrary source deficit. It does not prove that
all earlier sources admit the needed low-height certificate.

## 1. Source and parent data

A parent chain has parameter j, accumulated loss Gamma, and phase
represented by a reduced denominator 3^r_p. It reads an odd b/c
crossing n=j-1. Let the copied real chain W have parameter omega,
physical coefficient valuation sigma=n-epsilon, and phase

    Phi=3*tau(n)+5-lambda'_W.

Its containing real epoch starts at original pointer rho with fire
parameter P<rho. If G_s is its loss from that fire, the accepted
coefficient ledger gives sigma=rho-G_s. For a b source G_s=0.

Assume the source phase has an extra-bit representation

    Phi=C_s/3^r_s+b_s*2^omega mod 2^(omega+1),

and a source certificate supplies

    G_s+omega+2*r_s <= P.                         (SOURCE-RESERVE)

Equality is allowed at a source fire (rank zero). Ordinary strict
EXT supplies the record bound but does not automatically supply
the additional rank allowance for a chosen rational representation.

## 2. Rank and extra-bit transfer

The exact b/c defect update is D'=D_p+Phi-2 modulo 2^(omega+1),
because the numerator-dependent error has valuation at least
omega+1 by real S1. The parent's extra bit at 2^j vanishes there;
the source bit b_s is retained.

The sum of two rationals whose denominators divide powers of 3 has
reduced denominator dividing their least common multiple. Therefore

    r_new <= max(r_p,r_s).

The source bit is an integer contribution and cannot increase this
rank. Reduction/cancellation can only decrease it. No bound on the
real numerator height is being inferred from this rank statement.

## 3. The inherited reserve is paid by the copy's record drop

The accepted copy ledger is

    Gamma_new=Gamma+1+epsilon,
    R_new=R_parent-(sigma-omega).

For V=Gamma+j+2r_p and V_new=Gamma_new+omega+2r_new,

    V-V_new
      =sigma-omega-2*(r_new-r_p)
      >=sigma-omega-2*r_s
      =rho-G_s-omega-2*r_s
      >=rho-P >=1.

Thus the copy preserves any strict outer potential ceiling and pays
for the inherited rank, with at least rho-P slack. This includes
arbitrarily high source deficits; HR5 is not needed for this budget
calculation. The next a step can still require separate height and
precision control.

## 4. Well-founded induction target, not an assumed theorem

For a parent in an exit of root parameter J, its read index n<j<=J
on a strict prefix. The copied epoch's root satisfies

    P<rho<=n< J.

Hence SOURCE-RESERVE is naturally an earlier-root obligation. One
can seek a strengthened exit certificate that records, at each chain,
its rational phase, retained precision, rank, and weighted record
bound relative to its own root P. If such certificates are established
inductively, this lemma handles their b/c inheritance automatically.
This is a proposed induction contract, not a proof of its closure.

Existing segment lemmas cover specified integer seeds, ordinary
strong descents, and large paired gateways. Missing clauses include
small gateways and control of phase height after arbitrary copies.
Those clauses cannot be supplied merely by assuming ordinary EXT
below J; the chosen low-height rational certificate is stronger.

There is always an exact integer representation of Phi with rank
zero. It makes the reserve easy when ordinary source EXT is known,
but Phi may have enormous height. This does not license the next
small-height descent argument. The height/rank tradeoff must remain
visible in any eventual certificate.

## 5. A necessary negative control

At the actual b crossing n=5, the source fire has P=1, G_s=0,
omega=1 and sigma=4. Its exact phase is 1. The rational 31/27
agrees with 1 modulo 4, so it is an adequate two-bit phase match,
but assigning source rank 3 gives source budget 1+6=7>P.

If that uncertified representation is inherited from a rank-zero
parent, the record drop is only sigma-omega=3 while the rank term
increases by 6; the potential increases by 3. Matching the source
bits alone is therefore insufficient. SOURCE-RESERVE is not a
cosmetic premise, and arbitrary inflation of denominators is forbidden.

## 6. Verification

    python -B work_c3_drift/verify_copy_budget.py

6,160 exact b-copy checks and 440 c-copy checks use real source
coefficients from a full-pair table, plus independently obtained
calendar epoch metadata. Both source and parent lift bits, two odd
parent bases, ranks through the source budget, and parent ranks 0..4
are exercised. All valid source-budget cases satisfy the claimed
slack; the uncertified-rank control is retained and fails as expected.

The phase representations are constructed tests, not assertions
that every source already has a proved low-height certificate.
No accepted horizon or global open status changes.
