# A joint record, denominator, and phase-height reserve

2026-10-21. **UNREVIEWED proposed composition invariant.** It closes
the bookkeeping of specified copies and large gateways, not all exits.

## 1. Integer height and the candidate invariant

For a real rational phase c=C/3^r in reduced form define

    h(c)=ceil(max(0,1-c,c-2)),
    W=Gamma+j+2r+h(c).

The lift bit b*2^j is tracked separately and is not included in c's
height. This is a height of the chosen rational description, not of
the potentially enormous symmetric integer residue. A fire has
c=1,r=0,h=0 and W=J.

Elementary interval bounds give

    h(3-c)=h(c),
    h(c_p+c_s-2)<=h(c_p)+h(c_s)+1,
    h(4+c/3)<=ceil((h(c)+8)/3)<=h(c)+3.

For example c lies in [1-h,2+h]; adding two such intervals and
subtracting 2 proves the copy bound. Reflection proves the first
identity. Applying 4+c/3 to that interval proves the last bound.

## 2. Copies pay both inherited quantities

Strengthen the earlier source contract to

    G_s+omega+2*r_s+h(c_s)<=P.

Use COPY_BUDGET's source notation sigma=rho-G_s, parent record drop
sigma-omega, and r_new<=max(r_p,r_s). The output rational phase is
c_new=c_p+c_s-2, with the source lift bit retained. Hence

    W_new-W_parent
      <=-(sigma-omega)+2*r_s+h(c_s)+1
      <=-(rho-P)+1.

On the reached canonical prefix, rho-P>=3. For rho>=16, C1 and
2^P<=3*tau(rho)+4<=3*rho^2+4<2^(rho-2) prove P<=rho-3.
The quadratic inequality holds at 16 and persists by its growth
ratio below two. The finitely many odd-a fires rho<16 have gaps
3,3,9,12, checked directly. Therefore W drops by at least two
through every source-certified b/c copy, regardless of deficit.

Choosing an exact integer source phase gives rank zero but can have
huge height; it need not satisfy this stronger source contract.
Matching bits alone still does not prove the contract. At n=5,
the rank-zero phase 9 matches the actual source phase 1 modulo 4,
but its height 7 causes the resulting W to increase by 3. The
source budget fails, as it should.

## 3. Large paired gateways pay the height change as well

Take the hypotheses of DEPTH_CLOCK_BUDGET for an a->5->m pair,
with Q=3^r, |c|<=B and parent j>=N_Q. Its integer numerator Z obeys

    0<|Z|<2^(3*j/4+1)<2^(j-7),

because j>=N0>32. Thus m<=j-8 (strengthening the earlier j-5 bound).
The output phase is 4+c/3 with one extra lift bit, rank r+1, and
loss increment two. Consequently

    W_new-W_parent
      <=(m-j)+2+2+3 <=-1.

The intermediate five record is also below the parent budget. This
is a macro-boundary decrease, not a claim of pointwise decrease at
the second step relative to the intervening small state.

Ordinary strong a descents preserve h and r and lower the record,
so they lower W directly. Copies preserve the stronger reserve when
their earlier sources have corresponding certificates.

## 4. The specified integer seeds can initialize W

The emitted seed phases 10/3 and 26/3 have heights 2 and 7, so
their rank-plus-height charge is at most 9. For the large integer
a/b parents of SEED_BUDGET, the same polynomial estimate at j>=N0
can be strengthened to m<=j-14. Their two-step losses are at most
three, leaving record drop at least 11, which pays that charge.

For c histories A, AA, BA in that note, all eligible source roots
have P>=14. C1 gives rho>=P+11: otherwise
2^P<=3*rho^2+4<=3*(P+10)^2+4<2^P. The last strict inequality holds
at P=14 and persists by the same quadratic growth argument.
This supplies ten more source-pointer units than the weaker P<rho
bound used in SEED_BUDGET. With its existing m<=s-4 and source
parameter relations, the two-step record drop is at least 13 (A)
or 14 (AA/BA). Thus these specified seeds also pay the charge 9
without a separate starting-height allowance.

## 5. What has not been proved

The earlier-source contract itself is an induction target, not an
assumption that can be imported from ordinary EXT. The represented
height at a copy is now budgeted, but it need not be below the B
required by the next large-gateway lemma. Adaptive thresholds,
small-parent gateways, unpaired ties, and any remaining return
patterns still require certified rules or a counterexample.

It is not valid to claim that W decreases at every state of every
exit. In particular a small bare tie can raise W before a later
rescue. No full induction closure or global non-halting theorem is
claimed, and the accepted K_clock horizon is unchanged.

## 6. Verification

    python -B work_c3_drift/verify_height_budget.py
    python -B work_c3_drift/verify_gateway_budget.py

720 exact copies check both rank and height against actual small
source coefficients and eligible synthetic phase descriptions.
Twenty reflection/gateway height checks and 216 paired-gateway
updates pass. The uncertified source-height control remains a
deliberate failure. The small fire gaps and polynomial boundary
checks support the analytic arguments; they do not replace them.
