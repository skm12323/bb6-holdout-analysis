# A seven-productive-entry local witness using actual canonical sources

2026-10-17. New constructive result, not independently reviewed.
This disproves an unrestricted local extension of the seven-entry
finite-core exclusion. It does NOT show that the constructed outer
state occurs on the canonical orbit, and is not a counterexample to
global safety or non-halting. The displayed continuation itself ends.
Follow-up: `work_global_ancestry/PROOF_ANCESTRY.md` now excludes this
explicit fixed-clock state and its coefficient lifts canonically,
using the existing fire certificate. The same word at larger clocks
is a separate unresolved reachability question.

## 1. The finite search and the failed uniform conjecture

The accepted core certificate excludes seven consecutive productive
mixed-block entries when all parameters are <=1023. The streaming
search in `work_global_clock_words/probe_long_words.py` extends the
arithmetic check to <=4095, with all accumulated lattice constraints:

| Productive word length | Congruence-feasible words |
|---|---:|
| 2 | 1700416 |
| 3 | 399194 |
| 4 | 273115 |
| 5 | 99870 |
| 6 | 7987 |
| 7 | 0 |

There are 256 possible escape nodes at each of lengths 2 and 3, and
128 at length 4. None occurs at lengths 5 or 6. The 7987 six-entry
words force their next parameters to 1, 2, or 3, with counts 6670,
100, and 1217 respectively. These are terminal parameters.

This evidence might suggest a seven-entry exclusion independent of
the cap. The construction below shows that such an exclusion is
false on the same broad class of positive, physically safe local
states with the actual earlier source data. It explains why merely
enlarging that finite alphabet cannot establish a uniform seven-entry
stopping theorem without additional canonical reachability conditions.

The streaming search first matches the accepted cap-63 certificate.
Its initial-pair optimization discards a pair only when the positive
two-block identity has a unique least-valuation term and that valuation
is nonproductive. All other branches use the existing exact lattice
solver. The detailed scope remains finite; no escape is treated as
termination.

## 2. Four actual source records

Put P=122436 and R=367354. The canonical F prefix has odd type-a
crossings at the following indices, with exact half-times:

| Chain parameter j | Source index j-1 | k=tau(j-1)/2 |
|---|---|---:|
| 5 | 4 | 1 |
| 17 | 16 | 6 |
| P | 122435 | 54614 |
| R | 367353 | 163862 |

Their source heads are exactly (2^(j-1),6k+1), with epsilon=0.
`verify_long_witness.py` regenerates F up to the largest source with
`work_m/verify_m.py::Xdata`, checking each record rather than supplying
invented clock values. Xdata checks its chain safety assertions while
generating this prefix. All four calls also satisfy C1 numerically.
These sources are inside the V2 range n<=10^8 (PROOF_M section 4).
(The cap-4095 table is unreviewed finite evidence from probe_long_words.py
and is not used by the construction.)

The new resonance is identifiable algebraically. For a pure-A
substring 5,17,5,P,5, let Y_0 and Y_1 be the lambda chain values at
the entries 17 and P. Eliminating the low-parameter intermediate
values from the exact two-A identities gives the next lambda value

    Y_2=(5Y_1-Y_0)/4+3(3k_P-2).

The term Y_0/4 has valuation 15. The new source gives

    3(3k_P-2)=491520=15*2^15.

This is precisely the equal-valuation collision at which a large
next output becomes possible. The first positive k with
v2(3k-2)=15 is 54614; its actual canonical parameter is P. The
cap-4095 experiment does not include this source.

## 3. Explicit lambda and clock data

Define a local starting chain by

    x_0=3*2^R,
    Theta_0=9*2^(R-2)+5*2^(P+2)-1081554,
    s_0=(Theta_0-5)/3.

These are positive integers, including s_0: R and P are even, so
Theta_0=2 modulo 3. Its head/tail lambda components below are strictly
positive. This state is not asserted to be a canonical fire.

Apply the exact A maps x'=2Theta-x/2+6k and Theta'=Theta+6k+3
using the actual source records in section 2. Write

    x_i=3*2^R+b_i*2^P+c_i.

The resulting values are:

| i | b_i | c_i | v2(x_i) |
|---|---:|---:|---:|
| 0 | 0 | 0 | R |
| 1 | 40 | -1179936 | 5 |
| 2 | 20 | 393216 | 17 |
| 3 | 30 | -393312 | 5 |
| 4 | 25 | 0 | P |
| 5 | 55/2 | 131040 | 5 |
| 6 | 105/4 | 393216 | 17 |
| 7 | 215/8 | 262176 | 5 |
| 8 | 425/16 | 327744 | 6 |

Every fraction is absorbed by the factor 2^P. At rows with nonzero
c_i, both high terms have valuation at least P-4, so the displayed
small valuation is exactly v2(c_i). At row 4 the coefficient 25 is
odd and R>P. No numerical approximation of the huge integers is used.

At parameter 6 the actual b source has copied chain (48,10), hence
x_next=(3/4)x_8+10 has valuation 1. The parameter-1 call has an even
return and ends the epoch. Thus the local chain sequence is

    R,5,17,5,P,5,17,5,6,1.

The crucial seven productive mixed-block entries are

    5,17,5,P,5,17,5.

The first of these is an actual A output of the preceding local R
chain, not merely a freely declared block entry. All subsequent six
entries are also A outputs. This avoids assuming the very entry
condition required by the finite-core theorem.

## 4. Positive physical coefficients and replay safety

Choose any integer sigma>=R+16 and let e=2R+1. At the starting state
take one pending tail, original pointer i=sigma+e, and pairs

    H=((2^e-1)2^sigma, 2Theta_0-x_0-5),
    D=(2^sigma, x_0-Theta_0+1).

The two mass identities are exact:

    c_H+c_D=2^i,
    lambda_H+lambda_D=3s_0+1.

All four pair components are positive; the head is odd and its
coefficient is even. The chain coefficient H_c+2D_c has valuation
sigma>R, and the initial parameter is below the original pointer.

For each A return of parameter j and source half-time k, the exact
replay/image return map is

    u_c=(H_c+2D_c)/2^j, u_l=(H_l+2D_l+3)/2^j,
    D_new=(2^i+H_c/2,(H_l+1)/2),
    H_new=(2^(j-1)u_c,2^(j-1)u_l+6k+1),
    i_new=i+1, s_new=s+1+2k.

The verifier checks these pair maps independently of the scalar
recurrence for all eight A returns, including mass, positivity,
parameters, and margins. The coefficient valuation drops by one
per A. The following b copy loses two more units and is safe. With
the explicitly materialized sigma=R+16, the minimum checked A-input
margin is 16. Replay uses the actually computed earlier source
prefixes and is justified by the accepted replay lemmas; a new
full microstep simulation of the very long copied calls is not claimed.

This proves a defined, positive, safe local continuation. It is
stronger than consistency of a valuation lattice alone.

## 5. What additional bounds can and cannot exclude this family

Increasing sigma multiplies every coefficient by the same power of
two and shifts the unread-original pointer by the same increment.
The pair recurrence is homogeneous in these coefficients, including
the original term 2^i. Lambda values, source parameters, and clocks
are unchanged; margins only improve. Thus the construction applies
to every sigma>=R+16, not only the materialized example.

For instance one may symbolically choose sigma=s_0. No integer
2^s_0 needs to be stored to state or verify this scaling implication.
At this lift, the original pointer is s_0+e and the local continuation
is compatible with the numerical bounds

    i<=2s_0, s_0<=i^2,
    4(e+32)<=i, e+32<=(floor(log2 i))^3.

The remaining displayed tail lasts fewer than e steps, so the
stronger local clock inequality s<i is also available throughout it.
The extra allowance 32 covers its pointer increments and coefficient
loss. These estimates show that elementary clock/deficit size bounds
alone are not a reason to discard every coefficient lift of the
example. They do not prove that any such lift lies on the canonical
orbit or has a canonical preceding epoch history.

In particular the initial R chain cannot be interpreted as a fire:
at a true fire with parameter R, phase 1 and k_R=163862 force its
first A output to have parameter 1, rather than 5. The exact fire
projection of this eight-entry word is empty, as the script checks.
The construction may only be used as a local continuation example.
The ancestry follow-up additionally excludes its displayed fixed clock
at every canonical position. It does not exclude every larger-clock
realization of the same parameter word.

## 6. Consequence for the global proof strategy

The fixed-core seven-entry exclusion remains valid in its certified
range. Its unrestricted version on arbitrary safe compatible local
entries is false, even with actual canonical source data. Therefore
one cannot close the global loss budget merely by removing the cap
from that local certificate.

This leaves two substantive possibilities: use the exact rooted
fire/ancestry constraints to exclude such long local families from
the canonical walk, or prove a scale-dependent bound which charges
new resonances to their source sizes. The present example neither
proves unbounded local lengths nor decides either route. It also
does not show a safety failure: its continuation terminates safely.

Reproduce with `python -B work_global_long_witness/verify_long_witness.py`.
The compact record stores the explicit construction, source values,
path, margins, and hashes of the large clock integers. Accepted notes
are unchanged. This result and the cap-4095 search are new and have
not undergone independent review.
