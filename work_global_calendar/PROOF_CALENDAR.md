# An exact binary calendar for a certified canonical prefix

2026-10-17. New construction, not independently reviewed. This computes
canonical times and original pointers, rather than treating a compatible
local clock as reachable. Its domain ends at an explicit high-parameter
fire. It does not assume that any unresolved epoch beyond that point ends.

## 1. Finite kernel hypotheses

Fix B>=2. For each fire parameter 1<=J<=B, suppose the exact symbolic
exit recursion has certified a uniform finite exit for every odd fire
lift. Let its chain parameters and return types be j_t and type_t.
Define the epoch duration through its final even step by

    L_J=sum_t(1+tau(j_t-1))+1.

A fire starts at an even time. If L_J is odd, its empty-list endpoint
is at an odd time and one further even step produces the next fire.
Thus the fire-to-fire half-time and pointer increments are exactly

    delta_J=ceil(L_J/2),
    a_J=2+number of A return types+2*(L_J mod 2).     (KERNEL)

Here the A count includes a terminal even A return. The initial chain
reads two originals. Each A return leaves one pending entry, so its
next update reads one more original. B/C returns leave two entries and
consume no new original in that next update. The possible final empty
even step reads two originals. These facts prove the pointer formula.

The additional checked condition is

    1<=delta_J<=2^(J-1), 1<=J<=B.                    (NO-SKIP)

These are FINITE hypotheses, not assumed for arbitrary J. The
implementation computes the kernels with `work_m/verify_m.py::sym_exit`,
rejects unresolved/tied results, records the maximum coefficient loss
G_max and the maximum chain parameter, and checks NO-SKIP. For the
reported run B=4096, G_max=4 and all chain parameters are <=B.

The direct canonical base is generated through original index 2B+15.
It covers the small-pointer fire states. Beyond that base,
rho>B+G_max ensures sigma>=rho-G_max>B at every kernel chain, so
all these uniform kernels execute safely. Replay sources lie in the
already computed small base. This justifies using the kernels along
the actual orbit until its fire parameter first exceeds B, without
assuming any unproved global exit bound.

## 2. Canonical fire times cannot skip the next binary boundary

The first canonical fire is at time s=2, pointer rho=4, parameter 1.
Write k=s/2 at a fire. Its parameter is

    J(k)=1+v2(3k+2).

Let h_B be the residue in [0,2^B) satisfying 3h_B+2=0 modulo 2^B.
For B>=2 it exceeds one. It is the first possible k>=1 with J(k)>B:

    h_B=(2^(B+1)-2)/3 for B even,
    h_B=(2^B-2)/3     for B odd.

For a fire k<h_B put D=h_B-k. Since 3h_B+2 is divisible by 2^B
and 0<D<2^B,

    J(k)=1+v2(D).

Writing r=v2(D), NO-SKIP gives delta_(r+1)<=2^r<=D. Hence the
next fire cannot pass h_B. It moves strictly forward, so the
canonical sequence reaches h_B after finitely many such kernels.
No unknown kernel is executed to reach that boundary state.

Equivalently, its distance to the boundary evolves by

    D -> D-delta_(1+v2(D)).                       (DIST)

This removes the large absolute clock from the navigation problem.
It is an exact canonical recurrence on the certified prefix.

## 3. Binary blocks and their exact pointer weights

Start at a distance D with v2(D)=r. The first kernel subtracts
delta_(r+1). Until distance D-2^r is reached, all subsequent
distances have lower valuations and depend only on the residue
below 2^r. NO-SKIP prevents any of them passing that endpoint.

Let W_r be the total original-pointer advance, and N_r the number
of completed fire epochs, while subtracting this entire 2^r block.
Both are independent of the higher bits of D. Define weighted
binary sums F(z)=sum_(l: bit_l(z)=1) W_l and C(z) similarly with N_l.
Then

    W_r=a_(r+1)+F(2^r-delta_(r+1)),
    N_r=1+C(2^r-delta_(r+1)).                      (WEIGHT)

Only weights with l<r occur on the right. Using the complement of
delta_(r+1)-1 within r bits gives the implemented equivalent form

    W_r=a_(r+1)+sum_(l<r)W_l-F(delta_(r+1)-1),
    N_r=1+sum_(l<r)N_l-C(delta_(r+1)-1).

The weights are positive. A traversal from any distance D to zero
has total pointer advance F(D) and completes C(D) epochs: remove
the least significant set bit at a time and apply its block.

In particular the first boundary fire has exact pointer

    rho_B=4+F(h_B-1),

and its index among fires, counting the initial fire as index zero,
is C(h_B-1). These are exact integer formulas, not density estimates.

## 4. Inverting time and pointer inside the prefix

For a target original index n<rho_B, start from k=1,rho=4,D=h_B-1.
At r=v2(D), if rho+W_r<=n, skip the complete 2^r block. Otherwise
the target is inside it. Check its first epoch: if rho+a_(r+1)>n,
that epoch contains the target crossing; otherwise advance that
single epoch and continue in its smaller residual block.

Every partial descent lowers the binary block level. Between
descents at most B set bits can be removed. Thus at most O(B^2)
block/epoch decisions are needed, with exact integer arithmetic.
The analogous time query compares k+2^r and k+delta_(r+1) with
the target half-time and finds its immediately preceding fire.

Both operations retain the accumulated pointer and fire count.
Unlike arbitrary clock cylinders, they recover the canonical
time/pointer pairing and can reject a freely selected pointer.
They refuse targets at or beyond the unresolved boundary.

## 5. Exact crossing data without materializing 2^n

Once the containing fire (k,rho,J) is known, simulate only its short
top-level call/return sequence. Represent each physical coefficient
as 2^rho times an exact dyadic fraction, and keep the original-pointer
offset from rho. Originals then have normalized coefficients 2^offset.
All source calls in this kernel have parameters <=B, so their actual
head and pending-entry data come from the small table.

At each top-level original inspection record its type, exact time,
head/tail lambda values, normalized coefficients, deficit epsilon,
parity, and the copied chain parameter when the head is odd. The
normalization allows querying an index n of thousands of bits without
ever constructing the integer 2^n. Replay formulas, mass identities,
and KERNEL verify that these records cover exactly all originals
between the containing fire and the next fire.

The resulting `Calendar.crossing(n)` is an exact canonical-source
query on this prefix. A normalized fraction is not a rounding of
the coefficient; it specifies it exactly relative to 2^n.

## 6. Verification and concrete outputs

`verify_calendar.py` builds the B=4096 calendar and checks:

- all crossing fields against 8192 direct full-pair source records;
- times, pointers, and fire indices against 6789 ordinary kernel steps
  (consistency of navigation with kernel stepping, not independent of KERNEL);
- epoch_crossings, with its delta/advance/mass assertions, at one actual fire
  of every parameter J<=B;
- the previously directly computed sources at indices 122435 and
  367353, with times 109228 and 327724 respectively;
- pointer/time navigation consistency for indices 2^64+123,
  2^256+12345, 2^1024+54321, and 2^4094+98765.

The last query requires 4160758 binary navigation decisions, not
2^4094 individual F steps. Its source is type a, epsilon=0, with
odd head and copied parameter 1. Its exact time is a 4094-bit
integer; the check record stores its hash to keep the artifact small.

The calendar also identifies the earliest arithmetically possible
parameter-17 fire as an actual canonical fire:

    time=(5*2^17-4)/3=218452, pointer=244873.

Its b crossing is index 244874 and has copied parameter 17. This
provides exact clock/pointer provenance for this source, instead of
choosing a compatible b-parent independently.

For a small illustration of pointer correlation, time 84 is a real
parameter-8 fire, but its pointer is 99. A local fire-shaped state
with the same time and pointer 10 may satisfy numerical clock
bounds; it is not that canonical state. This distinction is what
the earlier interval-only filters could not decide by themselves.

## 7. Projecting isolated much larger root parameters

`projected_epoch(J)` can use these exact crossing queries for a root
parameter much larger than B, provided each source index requested
is still inside the calendar's certified prefix. It follows the
exact phase automaton (PROOF_RESCUE (A3) theta->3-theta, valid because
nxt<j is enforced, plus the exact B/C clock update; A-step safety follows
from nxt<j<sigma and copies are covered by PROOF_M section 7 P2) and
accepts only NT descents or safe copies.
An NT tie, an out-of-range source, or a work limit is not treated as
termination.

The routine agrees with all 256 small kernels cross-checked and
closes the isolated root parameters

    2^64+124, 2^256+12346, 2^1024+54322.

Their return-type words are aa, c, aa, with losses 1,0,1. The two
aa cases return to parameter 1. These are conditional exit maps for
any applicable fire with the stated J and earlier sources; they do
not assert that those huge-J fires have actually occurred. Nor do
isolated kernels fill the gaps in a larger calendar cutoff.

## 8. Scope and remaining global obstacle

This establishes exact canonical source information at exponentially
large indices using finitely certified small exit kernels. It is
new access to the already controlled prefix, not a new non-halting
horizon or a proof that all kernels satisfy NO-SKIP.

The unresolved task is still to control a general root parameter
whose exit may have resonances and depend on retained high bits.
The present calendar cannot assume that such an epoch has a fixed
finite duration. It does provide a way to test its earlier source
conditions with genuine canonical times and pointers, avoiding the
unreachable local clock assignments that obstructed earlier routes.

Run `python -B work_global_calendar/verify_calendar.py`. No independent
review was initiated; the separate original-machine boundary/endgame
obligation is unchanged.
