# R7: the odd part of x at odd steps. Status: NOT CLOSED (non-halting for all n remains open)

TM `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Base: work_r1/RULES.md (accepted) top map T; halt <=>
some step with A odd and x:=A+2b+3 a power of 2. Write x = 2^k q, q odd. Halting <=> q = 1 at an odd step.
Imports (unaudited, used only where stated): R4 (S3 excursion entry, Lemma E(v) v<=2000), R5 (canonical
states, Lemma R). Tags: [Class-A] proved for all stated parameters (by hand, or exact symbolic run
uniform in all symbols); [Class-B] finite exhaustive check (none of them is a proof for all n);
[Class-C] empirical / conjecture. Simulation evidence is always [Class-C] here.

## 1. Exact formulas for q at each kind of odd step

**P1 (singleton, n even) [Class-A].** L=(3n+3): x = 3n+6 = 3(n+2) = 3w 2^v (n+2=2^v w, w odd),
so k=v, q=3w >= 3. Never halts (= RULES Corollary). The near-halts q=3 of R6 §2 are exactly w=1.

**P2 (Lemma R step) [Class-A, by hand, given R5's canonical form].** Gamma=(H+d,H,2H,...,Y), d odd,
s'=v2(d+3), j=v2(H)>s'. Then x = 3H+d+3, k = s', and q = o' = (3H+d+3)/2^{s'} = 3H/2^{s'} + (d+3)/2^{s'}.
Since 3H/2^{s'} is even and >= 6 and (d+3)/2^{s'} is odd >= 1, q >= 7; with R5's observed form
H=3w 2^j (j>=1), q >= 9*2 + 1 = 19. The 3H term dominates: q = 3*(H/2^{s'}) + odd.
(If j <= s' the 2-adic insulation fails and k may exceed s'; this is R4's "margin 0" case.)

**P3 (R-even step)** has A even: no x. [Class-A]

**P4 (all odd steps inside one excursion, uniformly in w) [Class-A for v<=1000, verify_r7.py check1].**
Put w=2u+1 (u>=0 symbol) and run T symbolically from E(w,v) exactly as R4 does, additionally halving
x=A+2b+3 while its parity is uniformly even. In every run (v=1..1000) every halving decision is
uniform in u, so at each odd step k=kappa is independent of w and q = alpha*u + beta with alpha>=0
even and beta odd; hence **min over all odd w of q is attained at w=1 and equals beta**, and
beta >= 19 always (min 19, first at v=5). Consequence: within E(w,v), v<=1000, q >= 19 at every odd
step. (This re-proves R4's no-halt for v<=1000 with an explicit margin; it is not new for v<=2000.)

## 2. Is there an inductive invariant "q >= 3" (or >= 9) off the singletons?

**No closed congruence form [Class-C, n<3e5].** For every odd modulus M tested (3..257, incl. 3,7,
31,63,127,257) the residues of x at non-singleton odd steps meet the powers of 2 mod M; with R6's
2-adic refutation, no predicate depending on x mod M alone excludes q=1. In particular q is not
forced divisible by 3 (x mod 3 takes both values 1 and 2, ~50/50), and q mod 8 takes all of 1,3,5,7.
So the bound on q is a **size/valuation** fact, not a residue fact.

**Size/valuation form [Class-C, n<3e5, check2].** Off singletons: min q = 19, q >= 1.54 sqrt(x),
equivalently k <= log2(x)/2 - 0.62 at every odd step. Conjecture C7: k <= (1/2)log2 x at every
non-singleton odd step (which implies q >= sqrt(x) >= 3).

**Why q>=3 alone is not inductive [Class-A remark].** q at step n+1 is not a function of q (or of
(k,q)) at step n: the next odd step's x is built from list entries that the halving chain
creates (pushes (m+3)/2) and from deeper stack entries, so any invariant closed under T must
constrain the whole list. The natural list-level invariant is R5's canonical shape, under which
P2 gives q=3H/2^{s'}+odd with the explicit margin j-s'. Closing it requires:
(i) j > s' (resp. j >= p(s')) at every middle step -- R5 gap G1; and
(ii) a bound for the odd steps of the nested process Phi_{s'} and of the end phase, where the
perturbed odd entry 2^r H-1+K is read as b -- R5 gap G2. P4 handles these for v<=1000 by
exhaustion over the step sequence, not by an invariant.
A weaker invariant that would suffice -- "at every odd step x = 2^k(3G + e) with G>=2 even and e odd>=1,
where 3G is (3x) a pushed/run entry" -- holds at P1, P2 and empirically everywhere, but proving its
preservation through the end phase again needs the case analysis of G2 (the entry read as b there
is 2^r H - 1 + K, whose low bits are not those of a run element). Not done.

## 3. Result and exact residual
**Theorem (unchanged, [Class-A] conditional on RULES.md and R4's Lemma E(v), v<=2000):** no halt
for top steps n < 2^2001 - 2. R7 adds: within each E(w,v), v<=1000, every odd step has q>=19,
and the minimum over w is the w=1 orbit (P4) [Class-A for those v].
**Residual (open):** prove for all v that every odd step of the orbit of E(w,v) has q >= 3.
By P1/P2 this reduces exactly to the odd steps that are not Lemma-R steps with j>s' -- i.e. the
steps inside nested Phi_{s'} processes and the end phase -- equivalently R5's G1+G2. Conjecture C7
(k <= (1/2)log2 x) is the cleanest candidate invariant, but it is [Class-C]; no proof found.
