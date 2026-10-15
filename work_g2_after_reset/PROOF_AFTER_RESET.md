# A uniform suffix theorem after a high a-return

2026-10-15. Continuation of `work_g2_resonance`, without starting an
independent review. New symbolic certificates, not a global theorem.

## 1. The joint state that survives the old exceptional depth class

The exact identity in `work_g2_resonance/PROOF_RESONANCE.md`, equation (1),
holds even when the depth m belongs to its excluded congruence class.
After the parameter-65 b-return and the parameter-5 a-return it gives

    x=2^q u, Theta=x/2+K, K=46+3*2^61 V,               (R)

where u,V are positive odd integers and q can exceed 62. Here V is the
odd run base at the earlier parameter-65 chain. Physical safety of this
new chain is a separate requirement. The ancestry theorem of that note
supplies sigma>=q+2 for a genuine initial pure-b ancestry under earlier
C1. For general local states we explicitly assume that margin.

We retain the exact exit identities and earlier-prefix/replay hypotheses
from `work_m` and `work_el`. This result does not require that all the
local states in (R) be reachable.

## 2. Main theorem: arbitrary high q, with two k classes unresolved

Suppose (R) is a compatible top-level state with q>=63 and sigma>=q+2.
Suppose its crossing X(q-1) is odd type a, and write k=tau(q-1)/2.
If

    k mod 2^60 is neither
        384307168202282310 nor 512409557603043094,      (E)

then its epoch ends safely. Following its first a-return, the entire
remaining suffix takes at most 56 F steps and contains at most five
chains. Including the initial q chain, the bound is

    1+tau(q-1)+56 F steps, at most six chains.

There is **no upper bound on q or k** in this theorem. An even return at
q terminates immediately by the existing replay theorem. Odd b/c returns
at q are not covered by this new theorem.

### Reduction to four affine coefficients

Since q>=63, write x=2^63 U with U any positive integer; for the original
state U=2^(q-63)u. Allowing every positive U only enlarges the family.
After the odd a-return the exact state is

    x1=2^62 U+92+3*2^62 V+6k;
    Theta1=2^62 U+49+3*2^61 V+6k;
    sigma1>=64.                                      (A)

For a residue cylinder k=r+2^L w, 0<=r<2^L, substitute
U=1+a, V=1+2b, with a,b,w nonnegative integers. Then (A) is affine in
three independent integer variables. `modular.follow(r,L)` propagates
the four coefficients (constant,a,b,w) by the exact return identities.

At each next chain it requires the constant's valuation to be strictly
less than all three variable-coefficient valuations. Thus the parameter
is proved for **every** a,b,w in the cylinder. It also checks j<sigma,
uses only available earlier crossing records, and declares completion
only at an even return. Collisions, missing table entries, insufficient
margin and step-budget exhaustion are explicit failure results, never
treated as success. The known table through 127 is sufficient for all
the certified branches.

### Exhaustive residue partition, without enumerating 2^60 residues

`refine.py` starts with the whole cylinder (r,L)=(0,0). Whenever a
cylinder is unresolved it replaces it by its disjoint children

    (r,L+1), (r+2^L,L+1).

A proved terminal cylinder is retained without further splitting. At
depth 60 the output has 114 proved cylinders and precisely the two
unresolved cylinders (E). There are 231 nodes in the whole tree. The
script checks the exact coverage identity

    sum_(closed cylinders) 2^(60-L) + 2 = 2^60.

The construction gives disjointness; the identity cross-checks coverage.
All affine states are saved in `refined_certificate.json`. Across the
closed cylinders, maximum suffix duration is 56, maximum chain count
is five, and minimum physical coefficient margin is four, computed with
the conservative starting sigma1=64. Hence every return is safe and all
replay calls are covered by the earlier-prefix hypotheses. This proves
the stated theorem relative to the finite certificate and imported table.

## 3. Exact meaning of the two exceptions

The first exceptional residue solves

    46+3k = 0 (mod 2^60).

Indeed its least representative is (2^60-46)/3. This is the collision
already visible in x1 in (A); it has not yet made a further suffix chain.

The second residue has a proved next parameter 5. Its a-return has
tau(4)=2, and a direct substitution gives

    x2=3x/4+K+12+9k
      =3x/4+58+3*2^61 V+9k.                          (B)

Its least representative is (4*2^60-58)/9, so it solves
58+9k=0 mod 2^60. This is the collision after the suffix's parameter 5.
At depth 60 the unresolved paths are respectively [] and [5].

These cylinders are **unresolved**, not examples of nontermination or
unsafe actual states. Nor is the fraction 2/2^60 a probability of orbit
failure: there is no distributional assumption about actual k values.

## 4. Conditional corollary using C1

If 63<=q<=2^29, the return at q is odd a, and earlier C1 holds at q-1,
then

    0<=k<= (q-1)^2/2 <2^57
       <384307168202282310.

Neither class in (E) can occur. Thus **every such a-return closes**,
with total duration at most (q-1)^2+57 from the q chain.

This does not enlarge an unconditional horizon: it applies to compatible
reset-family states with the stated margin, crossing type and earlier
C1. Combined with the preceding ancestry theorem it resolves the entire
post-reset suffix of those actual pure-b ancestries whose bottom copy is
the parameter-65 b-return of the s=52 fire (only then K=46+3*2^61 V holds), and whose exceptional
rebound q lies in this interval and whose crossing is odd a. It is not a
claim that all rebounds lie in this interval or have this crossing type.

## 5. Additional finite coverage of all crossing types

`probe.py` separately propagates the two independent odd-symbol family
(R) for every q=63,...,4095, with initial sigma=q+2. All 4033 families
close safely, including b/c returns, with at most four chains from q.
The checks are uniform over both odd symbols, not sample choices of the
large parts. Together with the prior 62 certificates, this proves safe
closure of (R) for every 1<=q<=4095 when

    sigma>=max(63,q+2).

The bound is sufficient rather than optimal. For q<=62 use the prior
certificate with sigma>=63; for q>=63 use this directory's certificate.
This finite coverage should not be extrapolated to all q.

`verify_pair.py` independently runs the full integer pair map on 396
compatible local states (q=63..255 and five larger values, each with two
choices of V). Every complete parameter path and exact step count agrees
with the affine calculation; all mass identities and chain margins pass.
The largest observed duration is 3651 steps, including the initial call.
These are cross-checks, not reachability witnesses or the universal proof.

## 6. What remains for the global route

The previous depth obstruction is now partially resolved after, rather
than merely up to, its first rebound. The remaining branches are:

* high q with odd b/c return outside the finite coverage;
* odd a-return with k in either of the two residual cylinders;
* reset states outside this particular fixed parameter-5-source family.

The natural next information to retain is the source relation determining
k (or the b/c source state), not just its low residue. Equations (A),(B)
locate exactly which additional correlation is needed. No all-tail
decreasing measure or global exit budget has yet been proved.

Reproduce:

    python -B work_g2_after_reset/probe.py
    python -B work_g2_after_reset/refine.py
    python -B work_g2_after_reset/verify_pair.py

For an optional coarser, exhaustive residue table:

    python -B work_g2_after_reset/modular.py 12

The coarse table proves 4094 of 4096 classes, leaving residues 1350 and
1814. It is a diagnostic counterpart of the compact depth-60 certificate.
