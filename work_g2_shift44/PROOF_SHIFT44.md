# Closing shifted b/c copies and pure-b reset prefixes

2026-10-15. New continuation; no independent review initiated.
This is a collection of conditional local termination theorems, not a
global non-halting theorem or an enlarged unconditional horizon.

## 1. Reset family and the relevant shift

Retain the state from `work_g2_resonance` and `work_g2_after_reset`:

    x=2^q u, Theta=x/2+46+3*2^61 V, q>=63,

where u,V are positive odd. Assume the chain is safe and the earlier
crossing prefixes needed by replay are defined. For comparison with an
earlier source epoch we additionally require that epoch's suffix to have
completed safely; in an induction on the outer fire pointer this is
earlier historical data, as in the proof of Theorem B in `work_g2/PROOF_G2.md`.

Suppose the return at q is odd type b/c. The newly copied source chain
has x_ref=lambda_X, c_ref=c_X and coefficient valuation sigma_ref.
The outer-minus-reference errors are

    E=c_ref*u, D=Theta_parent-2
     =2^(q-1)u+44+3*2^61 V.

Thus v2(D)=2, independently of all high bits. Along a matched b/c prefix,
D is constant and E=c_ref,current*u. The outer coefficient margin over
the reference is the fixed positive integer C=sigma_parent-q>=1.

We use the exact error updates of the accepted copy lemma (`work_g2/PROOF_G2.md` section B):

    b/c: E'=(c_X/2^j)E;
    a: E'=2D-E/2.

That copy lemma says a safe completed suffix is
copied to its end when v2(E)>=sigma_ref and
v2(D)>=sigma_ref-2. This includes non-NT returns.

## 2. A complete-tail shortcut for b/c returns

Follow the source's b/c prefix from the copied chain.

* If it reaches an even return before an odd a-return, the outer run
  follows the same parameter sequence and terminates there.
* If its coefficient valuation becomes at most 4, the accepted copy lemma
  (work_g2/PROOF_G2.md section B, condition v2(D)>=sigma^R-2) applies,
  re-applied from step t where sigma_ref<=4 (2>=sigma_ref-2), so the whole
  outer suffix follows the completed source suffix and terminates.
  (The earlier citation of the unaudited work_global_shadow is replaced by
  this accepted lemma.)
* Otherwise let sigma_ref>=5 at its first odd a-return, and let r be the
  parameter of the source's next chain. If r!=3, the outer next parameter
  is exactly min(r,3), hence at most 3, and its next return is even.

Proof of the last assertion: at the first odd a-return,

    v2(E')=v2(2D-E/2)=3,

since v2(E/2)=sigma_ref-1>=4. If r!=3 the two valuations differ, so
v2(x_ref,next+E')=min(r,3). Physical safety follows because the new outer
coefficient valuation is sigma_ref-1+C>=5. The newly created chain has
parameter at most 3 and therefore terminates after its replay and even
return. This uses no assumed safety of an unexamined outer continuation.

This is a whole-tail statement with no bound on q. Its only untreated
source behavior is a first odd a-return producing **r=3** while the
reference coefficient valuation is at least 5. An r=3 source chain is
itself terminal, but the outer copy may rebound; source termination alone
does not settle that collision.

If there are h matched source b/c transitions after the initial outer
return, the shortcut uses h+3 chains counted from q, or fewer if it ends
earlier. No uniform bound on h, and therefore no new global exit budget,
is asserted here.

## 3. Pure-b prefixes ending at 5: fifteen of sixteen depths close

There is a direct way to resolve many of these collisions without
reconstructing the completed source suffix.

**Theorem.** Start at the reset state above. Suppose its initial top-level
continuation consists of m>=1 odd b returns ending at parameter 5, with
no intervening a/c return. If m is not 9 modulo 16, the a-return at 5
produces

    j_next=1+v2(9-m)<=4,

and the epoch ends safely. From the parameter-5 chain at most six F steps
remain. There is no bound on m or on the initial q in this theorem.

Proof. At a b-return copying a source fire of parameter p, put
a_source=3s_source+4=2^p U_source. The exact phase update is

    Theta_next=Theta+a_source-1.

B parameters strictly descend. Since the prefix ends at 5, each copied
source parameter is at least 5. Every a_source is therefore divisible
by 32. The initial reset phase is 46 modulo 32, so at parameter 5

    Theta=46-m (mod 32), x=32v, v odd.

The known odd a-return at 5 has tau(4)=2. Consequently

    x_next=2Theta-x/2+6
          =2(9-m) (mod 32).                         (P)

When m!=9 mod 16 the valuation is determined by (P) and lies in 1..4.
Every preceding b copy is safe by replay. At parameter 5 the coefficient
valuation is at least 6; after its a-return it is at least 5. Thus the new
j<=4 is safe and its return is even. The chain at 5 costs 1+tau(4)=3
steps; a terminal j<=4 costs at most two replay/chain steps plus one
final even-return step, giving six. QED.

This proves a conditional statement for any such actual prefix. It does
not assert the existence of pure-b prefixes of every depth.

**Direct-parent corollary.** If the initial b return copies any source
fire of parameter 5, then m=1 and the entire parameter path is

    q,5,4.

It closes in tau(q-1)+7 F steps. The source need not be the earliest
parameter-5 fire. In particular this resolves the entire direct-parent
family of r=3 source collisions, not only the known q=65 example.

For m=9 mod 16, (P) only gives divisibility by 32. It provides no safe
valuation bound or termination claim for that remaining class. Reducing
the depth condition further requires the retained source information.

## 4. Verification and finite classification

`verify_depth.py` records the 15 affine residue certificates. Write
m=r+16h, Theta=46-m+32z, x=32(1+2a). The output coefficients are

    x_next=(82-2r)-32h+64z-32a.

For every r other than 9 the constant has valuation <=4, below all
variable slopes. There are also 816 exact integer checks, including
depths above 2^100. These formal choices test the algebra, not reachability.

`explore.py` uses the exact crossing table to classify all initial odd
b/c returns with q=63,...,4095:

| Source continuation | Count |
|---|---:|
| even return before first odd a | 1220 |
| first odd a output r!=3 | 8 |
| first odd a output r=3 | 57 |

All 57 collision cases in this finite range are direct copies of a
parameter-5 fire, so the direct-parent corollary closes them. The script
checks the source crossing is type b, the copied chain is its level fire,
and the source a-output has the predicted value. This gives a structural
explanation of the previously computed b/c closure over this range.
It does not assume that the same classification exhausts larger q.

Reproduce:

    python -B work_g2_shift44/explore.py
    python -B work_g2_shift44/verify_depth.py

## 5. Remaining obstruction

The high b/c problem is narrowed to shifted copies whose first source
a-output is 3, except for the pure-b-to-5 prefixes already closed above.
For that pure-b subclass only m=9 mod 16 remains. Other source prefixes
may contain c transitions or reach a first a at a different parameter;
they are not covered by the depth congruence theorem.

Together with the previous arbitrary-q odd-a certificate, these results
give several whole-tail closure rules. They do not yet form a closed
state family or establish the global duration and coefficient-loss
bounds required by Theorem M.
