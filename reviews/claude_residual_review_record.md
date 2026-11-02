# Three-way review of work_claude_residual (Claude subagent, uncertified sources / G2), 2026-11-02
Target: work_claude_residual/NOTES.md, rwalk.py, levels.py, check_r0.py, c7_family.py (+json/log). Reviewers:
adversary = Claude subagent (D:/math_cc_astra/adv_residual; independent vectorised bulk certificate, independent level
closure, real-data check on the 10^8 table, lift tests); auditors 1, 2 = agy gemini-3.8-flash-high, blind (aud88 numerical,
aud89 logic). The author is a Claude subagent launched by the coordinating session.

- Adversary: `2. fixable gaps`. MEDIUM: the BBBA exception family was absorbed via the unreviewed AB′, whose record
  condition is incomplete and which needs "F defined through the end of E" (not implied for type-b/c J); the accepted
  Theorem RA suffices (the exception is reachable only through route a). MEDIUM: the BBBA landing is not a G2 instance
  (by HP the real source state is pinned to >= m0−3 bits; c7_family's lift test varied non-free bits). MEDIUM: zero margin
  in the drift ranges (widening by 1 creates chain-5 class 6); exact sets supplied. LOW: §3(ii) cited work_deep's L with
  its B-term; Sigma_h only at omega >= 5 and m=23 absent; log2^(4) J ≈ m0 needs CLOCK; theorem statable relative to
  EXT(<K_clock); scripts outside the repo. Confirmed: DL case split by hand; certificate = Prop 3.2/HP; independent
  bulk (ALL MATCH, delta∈[−8,10], j<=2·10^7) and level closure (B 54, C 83, D 148, C7 89, single uncertified (5,5));
  R0 on the 2·10^7 and 10^8 tables; 62,160,927 real odd entries J<=10^8 inside the A/B sets, no ties; T3<K_clock<T4.
- Auditor 1 (numerical): `1. all correct` (R0 on the 2·10^7 table: 6,057,602 b and 316,980 c crossings, 0 failures;
  level counts, chain-5 class sets, all 68 m0 reproduced).
- Auditor 2 (logic): `2. with simple errors` (AB′ unproved but not needed — route a only; size estimate drops a factor).
- Patches (coordinator): review-correction block at the head of NOTES.md (overrides the body). Targeted re-review 1:
  "(5,5) only in level C" was false (also in D/OUT from delta=−2) → replaced by an explicit t=0..3 enumeration; route-c
  exclusion spelled out; setdefault caveat; [A-cond] wording; net-result wording. Cross-check scripts moved into the
  directory (xcheck_*.py). Targeted re-review 2: `1. closed in all states` (two cosmetic
  suggestions applied: item order; even X(J−1) trivial).

VERDICT: ACCEPTED (with the correction block). **Theorem T4 [A+B]**, relative to the accepted EXT(<K_clock) and the
accepted imports (C5_EXTENSION §4, CLOCK/C1, gateway and window certificates): for every J with K_clock <= J < T4 and F
defined through tau(J−1), S(J) is tie-free. Also [A]: Lemma R0 (s = D_src−2; s ≡ 3tau+3+2^omega mod 2^(omega+1)), the
scale lemma DL with the exact drift sets, H5 for J<T4. [B]: the level computation (zero margin). Withdrawn: AB′ and the
copy principle as proved statements (unreviewed remarks); "genuine G2 instance". The machine-level horizon 2^T4−2 is
expected by the Corollary H-CLOCK pattern but NOT separately verified; the accepted horizon stays K_clock until that
transfer is reviewed. Beyond T4 the level method does not stabilise; global EXT open.
