# A length bound for canonical direct returns at chain 5

Research result, pending review. This concerns a contiguous run of direct
all-a returns at one chain. It does not bound the number of separate runs.
The subsequent ALL_CHAINS.md uses the finite estimate here as a base and
removes the fixed output cap by induction, for every fixed chain.
The proof uses the NF and JT identities in `work_claude_trains/NOTES.md`
§5, the accepted CLOCK bound, and a finite canonical-calendar certificate.
It does not require the confinement or transient claims in work_claude_sgexit.

**Claim.** Let each of N successive gates at j=5 return directly by
5 → m_i → 5 to another gate at 5 (the last successor need not return).
If every m_i ≤ 2^4000, then N ≤ 17781, for any initial phase or outer J.
More precisely N ≤ 7(2 + floor(log₃ U)) + 1 with U = max u_i,
where u_i = (2+k_{m_i})/8. The N=0 case is immediate.
Even without an output cap, equal outputs among indices 0 through N−2
have index difference divisible by 1024.

## Phase progression

Use the NF variables o_i and z_i. The canonical k_5 is 1. Each returning
output has an odd-a row, u_i is an odd positive integer, and
v₂(z_i)=m_i−4. The calendar through 16 excludes all m_i <17.
Consequently every z_i is a multiple of 8192. JT reads

    4z_{i+2} − 5z_{i+1} + z_i = 6(3u_{i+1} − u_i).

For 0 ≤ i ≤ N−3 this gives 3u_{i+1} ≡ u_i mod 4096. The order of
3 modulo 4096 is 1024 (its 1024th power is 1 and its 512th is not).
Since u is odd and determined by m, the recurrence proves the repetition
claim. Dropping the last output avoids using a third z outside the run.

## The canonical certificate

Enumerate every odd-a row at m−1 for 5 ≤ m ≤ 4096 satisfying
k_m+2 ≡ 8 mod 16. Save (k_m+2)/8 modulo 4096 in a set R.
There are 114 outputs and 114 distinct residues. On either odd-residue
orbit of multiplication by 3⁻¹ modulo 4096, every block of eight
consecutive residues contains two adjacent entries outside R. The maximum
block without such a pair has length seven. The script checks all starting
residues, then independently checks the cyclic gaps using the reverse
permutation. Both checks use the same repository calendar oracle.

Put a cut on every edge (i,i+1) of the first N−1 labels for which both
residues are outside R. Both outputs of any cut exceed 4096. Removing
all cut edges leaves pieces of at most seven vertices. If there are A cuts,
N−1 ≤ 7(A+1), and successive cut starts are at distance at most seven
(the vertices strictly after the first start through the next start form
one such piece). The inequalities are immediate for N ≤ 2.

## Paying for successive cuts

At a cut starting at a, both z_a and z_{a+1} are divisible by 2^4093.
The NF identity 2(o_a+9u_a)=4z_{a+1}−z_a implies
o_a+9u_a ≡ 0 mod 2^4092. For successive cut starts a<b, subtract the
two congruences and use o_{i+1}−o_i=6u_i. Hence

    6 Σ_{i=a}^{b−1} u_i + 9(u_b−u_a) ≡ 0 mod 2^4092.

The absolute value is ≤ (6·7+9)U. For the stated output cap M=2^4000,
CLOCK bounds U by floor((2+floor(T(M)/2))/8), with
T(M)=(M−1)(2 ceil(log₂(6(M−1)²+5))²+1345). The verifier checks even
64 times this upper bound is below 2^4092. Thus the displayed integer
vanishes. In particular

    3u_b = 3u_a − 2 Σ_{i=a}^{b−1} u_i ≤ u_a.

All labels are positive. There can be at most 1+floor(log₃ U) cuts,
which gives the claim. The exact CLOCK upper bound has floor(log₃)=2538.
This argument has no burn-in interval and needs no bound on the initial o.

## An all-scale exclusion for periodic output words

Suppose a chain-5 direct train continues forever with an eventually
periodic output word of period p. Let M be its maximum output on the
periodic tail. Then **p > 2^(2^3999)**, regardless of the initial phase.
This concerns periodicity of the outputs alone; the clock itself advances.

Discard the preperiod. Define D_i=3z_i−2o_i. Substituting NF gives
4D_{i+1}=D_i+6u_i. Since u_{i+p}=u_i, the integer D_{i+p}−D_i is
divided by four at every step. Infinite integrality forces it to be zero
already at i=0, and therefore everywhere. Write S for the sum of the p
positive labels. Now o_{i+p}−o_i=6S gives z_{i+p}−z_i=4S. At an index
attaining M the two z's have the same exact valuation M−4, so their
difference is divisible by 2^(M−3). Thus pU ≥ S ≥ 2^(M−5).

By the length bound above the periodic tail requires M > 2^4000.
For M ≥ 256, CLOCK gives U ≤ M³: indeed
ceil(log₂(6(M−1)²+5)) ≤ 4+2 log₂ M ≤ M/4 and
2(M/4)²+1345 ≤ M². Also 5+3 log₂ M < M/2 for M ≥ 256
(true at 256 and the difference is increasing). Consequently
p ≥ 2^(M−5)/M³ > 2^(M/2) > 2^(2^3999).
An aperiodic train can evade this argument, as can a finite train
that repeats an output word before exiting.

## Scope for SG-EXIT

The order-1024 exclusion applies at all output sizes. The length estimate
also applies to any contiguous subrun satisfying the output cap, even if
its neighbours violate it. For unrestricted outputs the cut congruence
still holds, but its left side can be a nonzero multiple of 2^4092.
Thus neither a uniform length bound at unbounded scale nor a bound on
the total cost of interrupted, mixed, or changing-chain returns follows.
No machine horizon changes here.

Reproduce from the repository root with
`python -B work_direct_phase/verify_phase.py`. Only the finite label set,
orbit checks and integer constants are computational inputs.
