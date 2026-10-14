# Finite fire-spectrum barriers and an obstruction to global strict descent

2026-10-14. **Reviewed 2026-10-14 (adversary: fixable gaps, patched; auditors: all correct ×2). ACCEPTED.**
The finite results below import the already accepted work_tie theorem; they
are not based on an assumed global non-halting theorem or assumed global DL.
The very large fire positions are specified by existence, not simulated.

## 0. Three different conclusions must be kept separate

1. **Finite-witness theorem (relative to the accepted imports):** an actual
   epoch in the certified finite range has parameter sequence

       p3, p2, p1, 17, 5, 6, 1,

   where p1=244875 and p2,p3 are defined below. It ends safely and has r=6.
   The step 5->6 contradicts global DL. This is an a-after-a, hence G1,
   obstruction; it does **not** unconditionally refute G2.
2. **Conditional G2 obstruction:** a sufficiently long actual b-copy
   ancestry produces a b->a non-descent 5->5. Existence of that longer
   ancestry is not proved from the present finite horizon. It follows if
   the global fire spectrum satisfies the gap condition stated below.
3. **Positive G2-family result:** the canonical last-parent states arising
   from b depths 1..123 into the known parameter-5 source close safely,
   including seven depths where strict G2 descent fails. This is a uniform
   local argument, not a claim that all these ancestries are realized.

This note does not prove global non-halting or halting of machine #1.

## 1. Accepted inputs and notation

Use `work_tie/PROOF_RESCUE.md` section 4, accepted in commit 85f7c92:

    B = 2^(2^499997-2).

Inside Theorem M's earlier-epoch induction, an epoch with fire parameter
J<B has at most six exit chains and strict affine coefficient separation.
In particular, its chain parameters are at most J (the exit margins
J-Gamma_t-j_t>=1 give this for t>=1). The induction provides
tau(n)<=n^2 at earlier crossings. The resulting finite F horizon is

    s < (2^B-4)/3.

We also use the audited small crossing table, the call/return decomposition
of PROOF_M, and the mass identities of PROOF_G6. The relevant gap bounds
below are consequences of these inputs; no global strict descent is used.

At a level fire the time is even, s=2k, and its parameter is

    L(k)=v2(6k+4)=1+v2(3k+2).

The first fire is k=1. Consecutive fires have increasing positive integer
k-values. Write d=k_next-k for their gap; this is not assumed to be a
function of J outside the small certified cases.

## 2. An exponentially weak gap bound from six exits

For a fire of parameter J<B, the duration to the next fire is at most

    sum_(t=0..r) [1+tau(j_t-1)] + 2.

There is one initiating step per chain, its replay call, one final even
return, and at most one further even level step. The last assertion follows
from the empty-stack mass lambda_A=3s+1: if the resulting time is odd,
one even step makes it even, so the next state fires. The c-head is even.
[Review patch] Spelled out: the final return leaves P=∅ with lambda_A=3s+1;
if s is even the head is odd and the state is the next level fire; if s is
odd, one even step (s->s+1) restores even s and the following state fires.
A c-type final return lands on an even head, covered by the same step.
The bounds r<=6 and j_t<=J are from PROOF_RESCUE section 4 (NEW HORIZON),
and tau(n)<=n^2 is the induction hypothesis of Theorem M (PROOF_M, C1).

Since r<=6, j_t<=J, and tau(j_t-1)<=(J-1)^2,

    d <= [7(J-1)^2+9]/2.

At J=16 the numerator is 1584<2^15, and

    2[7(J-1)^2+9]-[7J^2+9]=7J^2-28J+23>0

for J>=16. Thus the polynomial grows by less than a factor two per unit J,
and d<=2^(J-2) for every J>=16 in the certified range.

For J=1..15 the exact symbolic exit certificate gives the gaps (these depend on
PROOF_M Lemma 6.1 being tie-free, certified by V4 for J<10^6, so that the
whole exit and its parity are functions of J alone)

    1,1,2,2,3,3,3,4,4,5,5,6,6,8,7.

These are uniform small-parameter patterns, not samples of one odd base.
They imply the same bound except for J=1. Altogether:

    d <= M(J),  M(1)=1, M(J)=2^(J-2) for J>=2.           (GAP)

The verifier regenerates the symbolic patterns for all J=1..64. This also
records the small descent readout needed when a base fire has J<55, without
rerunning the full 10^8 base computation.

## 3. A no-overshoot lemma for fire times [elementary arithmetic]

Define target k-values

    T_1=1, T_2=8,
    T_J=(2^(J-1)-2)/3                 for even J>=4,
    T_J=(5*2^(J-1)-2)/3               for odd J>=3.

Each is an integer and L(T_J)=J. For every integer 1<=k<T_J,

    M(L(k)) <= T_J-k.                                  (BARRIER)

Proof for even J>=4. Put P=2^(J-1), a=T_J-k. Then 0<a<P and
3k+2=P-3a, so v2(3k+2)=v2(a). If a is odd the allowed gap is 1<=a;
otherwise it is 2^(v2(a)-1)<=a.

For odd J>=3, 3k+2=5P-3a and 0<a<2P. Unless a=P, the same valuation
argument applies. At the sole exception a=P, L(k)=J+1 and
M(J+1)=2^(J-1)=a. For J=2, check k=1..7 directly: the allowed gaps are
1,4,1,1,1,2,1, bounded respectively by 7,6,5,4,3,2,1. J=1 is the start.
QED.

Therefore an increasing fire-time sequence satisfying GAP cannot jump
over T_J. It must hit T_J once it has enough defined continuation to leave
the finite set {1,...,T_J-1}.

### Finite-range application, without assuming global progress

If J+4<B, then before T_J every fire label is at most J+2<B:
3k+2<3T_J+2<=5*2^(J-1). The accepted per-epoch result therefore supplies
the next fire and GAP at every such reached fire. BARRIER keeps the next
k-value at most T_J. Induction over this finite set forces a visit to T_J.
[Review patch] Precisely: fire k-values are strictly increasing integers,
so k_i>=i; while k_i<T_J, BARRIER gives k_(i+1)<=T_J. Hence some k_i equals
T_J, at the latest i=T_J. Only the accepted horizon theorem is used to
supply each next fire; the conclusion is not used in its own proof.

This does not cross the certified time horizon: for J>=3,
2T_J<(5/3)2^J<(2^B-4)/3 under the stated slack. Each completed transition
in the induction ends by 2T_J, by BARRIER. No existence statement at time
beyond the certified horizon is being invoked. The small targets are in
the audited base.

Hence **every J with J+4<B occurs as an actual fire parameter in that
finite range**, at the explicitly specified time 2T_J. Its tape pointer
need not be known numerically.

## 4. Three reachable b copies force the known non-descent macro

Take the parameter-17 fire at k=T_17=109226, s=218452. The finite walk
readout gives its pointer rho0=244873, so define

    p0=17, p1=rho0+2=244875.

By section 3, choose the actual fire of parameter p1 at time 2T_(p1),
and let its pointer be rho1. Define p2=rho1+2. Likewise choose the actual
fire of parameter p2 at 2T_(p2), let its pointer be rho2, and put p3=rho2+2.
Finally choose the actual fire of parameter p3 at 2T_(p3).

All three applications lie within the finite range. The pointer increases
by at most two per F step, so for J>=3 the chosen fire satisfies

    rho(J)+2 <=4T_J+2 < 2^(J+3).

Consequently

    p2 < 2^244878,
    p3 < 2^(2^244879) << B=2^(2^499997-2).

The slack is much more than the four units required in section 3. To avoid
depending on the exact numeric pointer readout, one could instead use
p1<=4T_17+2=436906, giving p3<2^(2^436910), still far below B.

At a fire of pointer rho_i, the crossing at rho_i+1 is type b and copies
that fire's parameter p_i.
[Review patch] Proof: a level fire at pointer rho reads the pair
(E_rho, E_(rho+1)) and its chain has parameter p_i with c_A=2^(p_i-1) at
n=rho+1, which is exactly type b of the crossing table (PROOF_M §5.4, P1:
type b means W fired at n-1). The crossing X(rho+1) is recorded at that
fire time and is read unchanged by the later epoch (call/return R1).
Checked on all 72,690 actual fires of the finite walk readout. Therefore the p3 epoch must begin

    p3 --b--> p2 --b--> p1 --b--> 17.

The sources are strictly earlier: S1 at a fire gives p_i<rho_i, so
p_(i+1)=rho_i+2>p_i and the later source fires have increasing pointers.
There is no circular ancestry choice.
[Review patch] Time order: T_J is not monotone in J (T_(J+1)<T_J for odd J),
so order is argued directly: p_(i+1)=rho_i+2>=p_i+3 (rho_i>p_i by S1, and
rho_i>=p_i+1), so T_(p_(i+1))>=(2^(p_i+2)-2)/3>T_(p_i). Each source fire
strictly precedes the fire that copies it.
Scope: p1=244875<10^6 lies inside the tie-free V4
range; by (C1) 2^(p1/2-1)<=p2<2^244878, so p2 lies in [10^6,H) where PROOF_RESCUE's strictly descending pattern
holds; p3>=2^(p2/2-1) by (C1), so p3 lies in [H,K). This is consistent with
Theorem D and with rescues occurring only for J>=H. The rescue premise
sigma>17 holds trivially: at the 17-chain sigma=rho_3-6.

At a fire Theta=1 modulo 2^J. Every b-copy adds the copied fire phase 1
and subtracts 2; because b returns strictly decrease the parameter, the
representative propagates from 1 to 0 to -1 to -2. Thus the reached
parameter-17 chain has Theta=-2 modulo 2^17.

As a consistency check, the two intermediate actual source epochs have
patterns (p1,17,2) and (p2,p1,17,1). Their phases at 17 are respectively
0 and -1, giving the next parameters 2 and 1 directly from X(16).
Thus the construction agrees with the older r<=2 and r<=4 layers; it does
not force a non-descent inside their established NT ranges.

The accepted rescue macro in work_tie section 2 then forces

    17 --a--> 5 --a--> 6 --b--> 1 --even--> end.

Combining these, the **actual** epoch has the exact parameter sequence

    (p3,p2,p1,17,5,6,1),  r=6.                           (WITNESS)

It is safely defined by the finite theorem and completes. Its fire parameter
exceeds 244875, whereas a base fire at rho<=10^8 has
2^J<=3rho^2+4<2^55. Hence this is outside the small base, where DL was
proposed. The a-after-a step 5->6 violates DL in precisely that domain.

This is an existence construction using certified dynamics and barriers,
not a numerical simulation to p2 or p3. It makes the accepted r<=6 bound
sharp on an actual epoch if the present derivation passes review.
It strengthens the older conditional fire-spectrum obstruction in
`reviews/astra_NT_research.md` by supplying the needed finite fire occurrences.

There is also a concrete consequence for the proposed offset invariant in
work_g2. At the reached parameter-6 chain, the rescue formula gives
Theta=46 modulo 64. Its next return is b, with

    delta=Theta-2=44 (mod 64), i.e. signed representative -20.

(delta is the copy offset as defined in work_g2/PROOF_G2.md, Lemma C1.)

Thus the suggested invariant that **every** real b/c copy has offset in
{0,1,-1,-2} fails as stated for this copy. This does not invalidate
the already proved short-prefix table. Nor does it exclude a larger set or
an invariant restricted to copies that actually encounter an odd a-return:
this particular b-copy goes directly to parameter 1 and then ends, so it
needs no small-offset hypothesis at all.

**It does not refute G2 by itself:** 5->6 follows an a return, so this is G1.
It does refute the proposed global strict-descent target DL, relative to
the accepted imports. None of this suggests a halt; WITNESS ends safely.

## 5. A G2 non-descent with a longer ancestry [conditional reachability]

There is a parameter-5 fire at pointer 63, time 52; X(64) is type b with
chain pair (3*2^63,160). By p=rho+2 (P1), its parent parameter is 65.

If the fire spectrum is closed under twelve repetitions of
"take a fire of the desired parameter, then its pointer plus two",
an outer epoch begins with twelve b returns ending in parameter 5. Its
penultimate parameter is 65, with phase Theta=-10 modulo 2^65; the
parameter-5 phase is -11 modulo 32. This forces an a non-descent.

Indeed, for a safe parameter-65 parent write Theta=2^65 z-10 and let u be
its positive odd lambda run base. The last b return and the next a return
give

    x1=3*2^63*u+160,       Theta1=2^65*z+149,
    x2=2^62*(16z-3u)+224,  j2=5.

So the parameters are 65,5,5. One more a-return gives

    x3=2^61*(16z+3u)+210,  j3=1,

and the next return is even. The tail is exactly 65,5,5,1 and takes 61 F
steps. From initial sigma>65, the successive coefficient valuations are
sigma,sigma-2,sigma-3,sigma-4, so every chain is safe.

This conditional path violates G2's **strict** descent, but safely exits.
The present finite horizon is not claimed to cover twelve such ancestors.
[Review note] In fact it cannot: twelve b-returns before the tail would give
r=14>6, contradicting the accepted r<=6 bound for J<B. Such an ancestry can
only be realized beyond B. (The first three repetitions are supplied by §3.)
Therefore no unconditional actual-orbit G2 counterexample is claimed here.

If F were globally defined and satisfied GAP globally, section 3 would
give all fire parameters and hence this G2 counterexample. Thus a proof of
full G2 would have to be incompatible with at least one of those additional
global properties. Global DL itself would imply GAP: with strict descent,

    d <= [J + sum_(a=0..J-1) a^2 + 2]/2
       = (2J^3-3J^2+7J+12)/12 <=2^(J-2)  for J>=9,

and small J are covered by the exact table. This provides a second,
global-assumption reductio, but section 4 already excludes DL using only
the accepted finite range.

## 6. Positive local result: pure-b depths 1..123 safely close

More generally, after m-1 preceding b copies, the parameter-65 parent
phase is Theta=2^65 z+2-m. The known last b-copy gives

    x1=3*2^63*u+160,       Theta1=2^65*z+161-m.

At its a-return,

    x2=2^62*(16z-3u)+2(124-m).

For 1<=m<=123 the nonzero constant has valuation at most 7<62. Hence

    q=j2=1+v2(124-m)<=7.

If q<=4 the next return is even. If q=5, the equal-parameter a-step 5->5
is followed by 1 (or derive it directly from the two-a positive identity).
If q=6, X(5) copies parameter 1; if q=7, X(6) is even. Every such tail
therefore ends in at most 61 F steps, with positive margins.

Within this family strict G2 fails at

    m=12,28,44,60,76,92,108,

yet all seven cases are safe. The family is proved for compatible entries;
realization of a particular large b-depth is a separate ancestry question.
At m=124 the constant vanishes and the next parameter is 62, so the above
small-q argument is not asserted beyond its stated range.

## 7. Verification and research consequence

The scripts record:

* symbolic exit and descent patterns for J=1..64, including the needed
  small fire gaps;
* 203867 integer barrier checks for target labels 1..18, supplementing
  the all-label arithmetic proof;
* the actual parameter-17 anchor at (k,s,rho)=(109226,218452,244873);
* exact exponent comparisons keeping p2,p3 within the accepted cutoff,
  without constructing their enormous positions;
* 126 full bigint instances of the 65,5,5,1 macro, all ending in 61 steps;
* 123 full bigint instances of the extended b-depth family, all safe.

The barrier and macro proofs do the unbounded work; finite tests alone do
not establish the existential actual WITNESS. That dependency chain is the
priority item for independent review.

If confirmed, pursuing global DL as the route to non-halting should stop.
G2 can still be useful as a classification of safe collisions and short
exit tails. The appropriate global targets remain exit-length bounds,
correlated core-visit bounds, and the separate finite-excursion endgame.

    python -B work_g2_obstruction/verify_obstruction.py
    python -B work_g2_obstruction/verify_finite_witness.py
    python -B work_g2_obstruction/verify_short_b_family.py

All new outputs stay in this directory. Existing accepted files are unchanged.
