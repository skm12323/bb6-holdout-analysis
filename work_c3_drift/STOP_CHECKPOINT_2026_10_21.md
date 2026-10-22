# Stop checkpoint: small-gateway limitation of the joint reserve

2026-10-21. Saved at the user's request to stop at the next node.
All work in this directory remains **unreviewed and uncommitted**.
Global EXT/non-halting is unproved; accepted K_clock is unchanged.

## Current node completed

The joint quantity W=Gamma+j+2r+h(c) composes under the hypotheses
of JOINT_HEIGHT_BUDGET. However, W below a ceiling is not by itself
a sufficient local hypothesis at an arbitrary small bare tie.

For any even m>=6, define

    u=(2^(m-4)-1)/3, x=32u, Theta=x+5.

These are positive integers, u is odd, and v2(x)=5. The integer
phase description has r=0, h(5)=3, and initial W=8. The actual
canonical call X(4), with half-time 1, gives

    x'=3x/2+16=2^m.

Thus for every even m>=8 the next record m+1 reaches or exceeds
ceiling 9, despite W=8<9 at entry. The positive cone x<2Theta also
holds. This disproves any unrestricted rule that would fill the
small-gateway gap using only the joint reserve and these local data.

These are constructed local states. They are NOT claimed to occur
in S(J), are not halting examples, and do not contradict any conditional
macro lemma. Their exact origin remains the missing information.

At m=6 the full word is (5,6,1), with maximum record 7; nevertheless
the normalized intermediate weighted value is 11, above initial 8.
So a pointwise weighted invariant can fail even when the whole tail
is safe. At m=8 the word is (5,8,3), maximum record 9, requiring
strict precision 10 rather than 9.

## Verification

    python -B work_c3_drift/verify_small_gateway_budget_limit.py

126 cases m=6,8,...,256 verify the exact jump. The ceiling-9 failure
is retained for m>=8. Each finite tail is separately checked to end
with precision m+2, so failure of the smaller proposed reserve is
not mislabeled as nontermination. Results are saved in
small_gateway_budget_limit_checks.json. The all-even-m obstruction
above is algebraic and does not rely on extrapolating these tests.

## Established work to preserve

* Conditional integer-seed, source-copy, large paired-gateway, and
  joint height/rank budget calculations are documented separately.
* Source/depth congruences retain their per-pair precision limits.
* The finite exponent cover through r=10^30 at one fixed canonical
  source was replayed with an independent full-pair implementation.
* The small-range all-a train bound, clock orbit restrictions, and
  explicit cross-scale local witness keep their stated scopes.

None of those results is a completed global induction or independent
proof review. Do not promote them to the accepted checkpoint yet.

## Concrete next task on resumption

Retain the actual affine origin at a small gateway, rather than only
its phase class and W. The accepted symbolic form is

    x=A*U+beta, Theta=2^J*U+3d+1, v2(A)=J-Gamma.

At a five-input a step its next small part is

    beta'=6d+8-beta/2,

while its coefficient valuation is J-Gamma-1. A strict inequality
v2(beta')<J-Gamma-1 determines the next parameter uniformly; failure
is exactly where an origin/precision argument is required. This is
the existing beta/affine mechanism, not a newly proved global bound.
Relevant implementations include work_claude_shifted/shiftlib.py
(`sym_beta`) and the accepted PROOF_EXT beta-walk discussion.

The next investigation should connect the actual reachable beta,d
prefixes to the source/depth and shared-clock constraints, and test
that criterion against actual symbolic exits. Merely expanding the
set of arbitrary local states or assuming W alone suffices will not
close the gap. Work stops here until the user resumes it.
