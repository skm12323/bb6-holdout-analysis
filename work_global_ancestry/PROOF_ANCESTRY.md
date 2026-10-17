# A denominator-separation cost for canonical ancestry

2026-10-17. New conditional result, not independently reviewed.
This restores the exact fire relation to local lambda/clock states.
It gives a lower bound on prior coefficient loss, not an upper bound
on total loss or an all-epoch stopping proof.

## 1. Rooted affine data and a sharper intercept estimate

At an epoch fire write Theta_f=3s_f+5 and x_f=Theta_f-1. On any
fixed valid top-level return prefix retain

    x=h Theta_f+c, Theta=Theta_f+d,
    h=A/2^G, A positive odd, 0<h<2, d=3(s-s_f).

G is the actual cumulative coefficient loss. This is the exact
rooted record, as in the accepted PROOF_RESCUE section 1 / PROOF_EL
Theorem A and PROOF_MIXED section 1 (the updates are re-derived below; the
unaudited `work_global_compression/PROOF_COMPRESSION.md` stated them earlier).
Initially h=1,c=-1,d=0. Its exact updates are

    A return: h'=2-h/2, c'=2d-c/2+6k, d'=d+6k+3;
    B/C:      h'=r h, c'=r c+lambda, d'=d+3tau+3,

where 0<r<1, its reduced numerator is odd, and
1<=lambda<=6tau+5. G increases by one at A and by the denominator
exponent of r at B/C. These facts preserve the odd numerator of h
and its range. The record belongs to the same original fire at every
step; its variables are not reset at a copy or a resonance.

A sharpening of the earlier coarse intercept estimate is

    0<c<=2d+1 after every nonterminal return.       (INT)

For the first A, c=1/2+6k>0; for the first B/C, c=lambda-r>0.
Their upper bounds are immediate. For a later A, the previous bound
gives c'>=d-1/2+6k>0 and c'<=2d+6k<=2d'+1. For B/C,
c'>0 and c'<=2d+1+6tau+5=2d'<=2d'+1. This proves INT by
induction, without NT or a clock bound.

## 2. Separation from the rational slope 4/3

Let Delta=3x-4Theta. Then

    Delta=(3A-2^(G+2))Theta_f/2^G+3c-4d.

The integer 3A-2^(G+2) is odd and nonzero. Its absolute value is at
least one. INT gives |3c-4d|<=4d+3; this also holds at the initial
fire with c=-1,d=0. Consequently

    Theta_f<=2^G(|Delta|+4d+3),
    Theta<=2^G(|Delta|+4d+3)+d.                 (SEP)

A dyadic coefficient with denominator 2^G cannot equal 4/3. For a
large rooted clock to be very close to that slope, G or the elapsed-
time intercept must already be large. A freely chosen compatible
local state does not automatically carry such a history.

## 3. Eliminate the unknown elapsed time using earlier C1

Assume C1 at all source calls used on this rooted prefix and put

    H=floor(log2(2Theta-5)).

Every earlier chain numerator is at most 6s_t+5<=2Theta-5, so
every earlier parameter is <=H. At most G returns have completed,
each costing at most H^2+1 steps. Thus d<=3G(H^2+1), and SEP gives

    Theta<=2^G(|Delta|+12G(H^2+1)+3)
                +3G(H^2+1).                  (ANCESTRY)

The right side increases with G. Its least feasible nonnegative
integer G is a computable necessary ancestry loss. Passing the test
does not construct an ancestry or imply reachability.

For a closed bound, let H>=32 and set

    C=|Delta|+12H(H^2+1)+3, L=ceil(log2 C).

If G<=H, then d<=3H(H^2+1)<2^(H-2)<Theta/2. The strict
cubic/exponential inequality holds at 32 and persists because
((H+1)/H)^3<2. Hence Theta_f>2^(H-2), whereas SEP gives
Theta_f<=2^G C<=2^(G+L). This forces G+L>=H-1. If G>H,
the resulting lower bound is automatic. Therefore

    G>=max(0,H-1-ceil(log2 C)).                (COST)

The all-history claim is conditional on the rooted prefix and earlier
C1 hypotheses. It does not depend on periodicity or a bounded phase
grammar.

## 4. Cost of the explicit seven-entry witness

For the state in `work_global_long_witness/PROOF_LONG_WITNESS.md`,
P=122436, R=367354, and

    x=3*2^R,
    Theta=9*2^(R-2)+5*2^(P+2)-1081554,

one has exactly

    H=R+2=367356, |Delta|=80*2^P-4326216.

COST gives G>=244912. The exact monotone inequality ANCESTRY gives

    G>=R-P-5=244913.                           (WITNESS-COST)

Its right side at G=244912 is strictly smaller than Theta, excluding
all smaller values too. At 244913 the necessary inequality holds;
that is not a witness to an actual history.

All prior source parameters would be <=H<10^8. The accepted finite
base also gives epsilon<=7 there, so each return loses at most eight
units. Such an ancestry would require at least 30615 prior returns.

## 5. The displayed fixed-clock state is excluded canonically

(Here "canonical position" means a top-level return state inside an epoch;
fire states have x=Theta-1, so the witness is not one. Since s~2^367354 lies
inside the unconditional PROOF_M horizon and H<10^8 inside V2's C1 range,
this exclusion is unconditional relative to accepted work. V4 likewise
excludes U-family members with Theta_U<2^(10^6).)

Any possible preceding fire has Theta_f<=Theta, and therefore

    J_f<=floor(log2(Theta-1))=R+1=367355<10^6.

The accepted V4 certificate in `work_m/PROOF_M.md`, section 6, is
uniform over all odd fire lifts for every J_f<10^6. It gives a
tie-free exit with at most two exit chains and total loss at most
six. This contradicts WITNESS-COST (and independently the length
of the proposed subsequent local continuation).

Thus the explicitly displayed lambda/clock state, including EVERY
coefficient lift that leaves its clock fixed, is not canonically
reachable. This sharpens the previous note's provisional statement
that reachability had not been established. The positive safe LOCAL
continuation remains valid. The exclusion imports an existing
certificate and does not extend the global non-halting horizon.

## 6. Unbounded clocks remain a separate question

The same local word persists for every positive odd U with

    x_U=3*2^R U,
    Theta_U=9*2^(R-2)U+5*2^(P+2)-1081554.

In the local-witness table this multiplies its common 3*2^R term
by U. The other terms, all displayed valuations, and positivity are
preserved. A fixed-clock exclusion is therefore not an exclusion of
the parameter word at all clocks.

For this family |Delta| is fixed while H grows with log2 U. For all
H>=R+2, each of |Delta| and 12H(H^2+1)+3 is smaller than
2^(H/2-1). The base inequalities are strict; the polynomial bound
persists since ((H+1)/H)^3<sqrt(2). Thus C<2^(H/2) and COST gives

    G>=floor(H/2)-1.

The exact inequality is stronger for the sampled U values: it gives
required losses 244913 at U=1, 245937 at U=2^1024+1, and 1244913
at U=2^1000000+1. These are necessary losses, not witnessed histories.
No general exclusion beyond the applicable fire-certificate ranges
is established by these numbers.

The global gap remains: proving that this much loss is required does
not show that a long epoch cannot accumulate it. A stopping theorem
or an upper bound on cumulative loss is still needed. This result
does show precisely why source-clock and current-state compatibility
cannot replace the true fire history in that argument.

## 7. Checks

Run `python -B work_global_ancestry/verify_ancestry.py`.
It checks 6830 rooted affine records with actual finite source data,
including INT and SEP, the exact/coarse witness costs, its fire-
parameter cap, and the U family with exact integers. Infinite-range
scope comes from sections 1-3, not from those samples. The V4 result
is imported with its J<10^6, all-odd-lifts scope, not rerun or enlarged.
The original-machine boundary/endgame obligation remains unchanged.
