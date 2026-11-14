# Three-way review of work_gc_freeb (ZCode GLM subagent, R2: FREE-B boundary-gate localisation), 2026-11-10

Target: work_gc_freeb/NOTES.md (FB-0..FB-5, Theorem FREE-B, §6/§7), fb.py, verify_freeb.py,
freeb_checks.json, agy_audit_prompt.md. Route claim: [A] FREE-B per CHECKPOINT:799 — every boundary
gate (determined but not record-safe, m′+1+ell>j_G) falls into one of three branches with decidable
membership tests: (I) first-landing escape c₁≥j−1 (accepted FREE ⟹ j≤3+log2(6gP(g))); (II) two-step
family with explicit sums S_a=k+3+3k_m+2k_{c₁} / U_b=12k+12k_{c₁}+9τ_m+20 / U_c=12(k+τ_m+k_{c₁}+2)−λ′
(non-zero-sum divisibility ⟹ j≤2+log2(3gP(g)+3) / 2+log2(21gP(g)+20) / 1+ε₁+log2(30gP(g)+29); zero
sum = exact cancellation, decidable; type-a u-parity knife: u even = determined m′=j−2, ΔR=1, u odd
= split at that step); (III) deep family (iterated calendar-sum 2^(j−ell)|u divisibility, decidable,
not excluded); plus FB-5: CL2 in the L′ environment at threshold B*(g)=2+log2(30gP(g)+29)+2⌈log2(3g²+4)⌉
holds ⟺ no gate with j>B*(g) has (α) post-gate tree split with escape branch reaching a true NT gate,
(β0) two-step zero-sum boundary, (γ) deep-family cancellation. [B]: census j<400 odd-a × m<5000
(357,821 pairs), sweep 906 starts/depth 3000 (3,072,713 leaves = the accepted sweep total), extended
scan j∈{24,42}×m<150,000, exact replays of counterexamples A (j=24, m=6,268,562, ΔR=1, S_a=2^23, u
even) and B/B2 (j=42/78, v2(U_b)=43/79, m′=j−1), 8 seeded/razor instances. Explicitly NOT claimed:
FREE-EXIT budget closure; G1/CL2/CL4 stay open (CL4 untouched). Reviewers: adversary = ZCode GLM
(attack; item-by-item adversarial hand derivation + own code, no fb.py reuse); auditor 1 = ZCode
GLM-4.6, blind (aud1_scratch/, 12 scripts; only accepted cyc.py/branch.py/calendar_oracle crossed;
fb.py/verify_freeb.py unread); auditor 2 = agy gemini-3.8-flash-high, blind (agy_scratch/, 10
scripts, blind rules 1–6 of agy_audit_prompt.md). **All three attended; none absent.**

## Round 1 (three-way, 2026-11-10)

- Adversary: `2. fixable gaps` (reviews/gc_freeb_adversary.md). 2 MEDIUM, 5 LOW, no HIGH.
  MEDIUM F1: verify_freeb.py:267 `chk('P1b_nondet', res['status'] != 'GATE' or True, ...)` tautology —
  the 2,832 non-determined pairs carried no assertion; split-direction engine agreement never
  machine-tested. MEDIUM F2: :576-577 `P8_free_classified` constructive tautology (pairs_long never
  incremented) — PART 8's "exhaustive" print unsupported. MEDIUM F3: NOTES.md:336-337 "for j = 24 …
  the type-b class at m ≈ 1.1·10^12" data error — 1.1e12 is counterexample B's m (j=42); the
  adversary exhausted the j=24 type-b congruence class to 1.89e12 with zero instances. LOW F4:
  NOTES:267-268 razor-exhaustive claim vacuous for m=j (E odd ⟹ c₁=1) and m=j+1. LOW F5: decidability
  note (NOTES:216-219) lacked the termination argument; caps 400/200 below the a priori bound; §7 vs
  PART 2b inconsistency. LOW F6: four precision items (FB-2 V-argument; FB-4(b) determinedness
  implicit; §0.4 u-parity rider; FB-0 "unimodular"). LOW F7: fb.py ZERO-leaf vs SPLIT naming.
  Confirmed: all [A] propositions by item-by-item adversarial hand derivation (FB-0 cylinder; FB-1
  v2(A)=j−ell+L_bc+1 induction incl. off-by-one, v2(B)=m+1−ell, v2(β2^m)=m−ell; FB-2 ⟺ branch.py
  vc<vs; FB-3 ΔR∈[1,1+L_bc] + boundary ⟺ 2^(j−ell)|C_final; FB-4 three closed forms + u-parity knife
  + size bounds 3mP+3/21mP+20/30mP+29 + trichotomy; FB-5 iff both directions + B*(g) chain 0
  violations g∈[2,2000]∪{1e4..1e30}); imports accepted; full script re-run ALL PASS/exit 0/187,309
  checks/0 fail (499.5 s); counterexamples A/B/B2 + seeded + razor independently replayed with own
  code; FB-4 closed forms 173 pairs own arithmetic; sweep 3,072,713 leaves == accepted
  sweep_3000_3000.json; escapes 467∈{5,8,12}, 623=467+156; j=24 type-a first occurrence 6,268,562;
  no overreach.
- Auditor 1 (blind, ZCode GLM-4.6): `2. with fixable gaps` (reviews/gc_freeb_auditor1.md). 6 LOW, all
  [B]-layer §6/§2 wording/count descriptions — "mathematics and computation all correct": 15,525
  population (15,435 stated-population count; 90 first-step-b super-escape surplus); "razor-edge
  parities … at m∈{j,j+1} occurring in the range" false; 1.1e12 attribution; type-c U_c "verified on
  every type-c pair in census range" vacuous (0 in box; auditor built 8 real ones, all pass);
  "(2948 checks)" granularity (2,948=2×1,474 walks vs 381,148 steps, which the auditor fully
  checked); FB-0 "unimodular" wording. Confirmed: complete independent re-derivation of FB-0..FB-5 +
  Theorem FREE-B with a fully independent engine (aud1_scratch/, 12 scripts); every [B] number
  reproduced (census 575,644/357,821/356,191/156/1,474, 0 boundary; extscan 186,442/4,181; sweep
  replay 286 s via accepted branch.py, 6,958 determined word-identical; A 4-lift big-integer + B/B2
  mod-2^200; seeded j=61/97/78; razor two-parity outputs j−1 vs ≥j; j=24 type-a first occurrence
  124 s full scan; B*(g) 2,027 g values; citations genuine; no overreach).
- Auditor 2 (blind, agy gemini-3.8-flash-high): `1. all correct` (reviews/gc_freeb_auditor2_agy.md).
  Independent no-float 2-adic re-derivations of FB-0..FB-5 + Theorem FREE-B; own agy_scratch/ 10
  scripts — A/B/B2 replayed exactly (Sa=2^23 u=2; v2(Ub)=43, dR=3 sharp; v2(Ub)=79); sampled
  FB-1/2/3 on 1,240 pairs; full census independently (357,821/356,191/156/0/1,474/0 boundary;
  escapes 623 ∈ {5,8,12}, 467+156); seeded + razor + intermediate dR=2 reproduced; CL2 chain
  exhaustive g∈[5,10000]+samples to 1e12, 0 failures; congruence explanation of the census
  zero-boundary (first realisation of the j=24 type-a congruence is exactly A's m=6,268,562); scope
  check passed. No findings.
- Round-1 summarizer spot checks (own reads): verify_freeb.py:267 `or True`; :576-577 constructive
  identity; NOTES:336-337/267-268/216-219 as cited; VERDICT lines confirmed in all three review
  files; agy in attendance with agy_scratch/ present.
- Round-1 VERDICT: ACCEPTED IN PART + 10 patchItems (3 MEDIUM, 7 LOW); route R2's gap (FREE-B,
  closesGap=true) not closed; patch round + targeted re-review next.

## Patches (author) and targeted re-review 1 (2026-11-10)

- Patches (author, per the 10 round-1 patchItems): F1 — P1b rewritten as a three-way exhaustive
  cross-check against the accepted branch.explore at verify_freeb.py:262-284 (P1b_oneleaf
  GATE/END/CUT_BITS leaf mix; P1b_det+word for GATE; P1b_end for END; P1b_split + P1b_splitprefix
  for CUT_BITS, checking the determined-prefix word on the split side); sweep side hardened by
  per-pair P6_splitprefix (355,910 pairs). F2 — PART 6 decomposition pairs_free = nogen + worddiff
  with worddiff/LIMIT hard failures; PART 8 rewritten as four substantive assertions. F3 — the data
  error upgraded to a theorem-grade argument: the j=24 type-b class 9τ ≡ −140 mod 2^22 fixes τ mod
  2^8, hence ω(m−1)=v2(3τ+4)=7 for every class member, and X(6) is even ⟹ the II-b two-step family
  is empty for j=24 at every m; first class realisation m=1,044,747; PART 7c checks 200/200 labels
  all ω=7. F4 — FB-4 unreachability note for m=j; new checked claim: the 120 pairs at m=j+1 are all
  type-b and all END. F5 — termination argument (ell≥m−3 ⟹ v2(B)≤4 ⟹ END, so ≤m+3 steps) in NOTES
  and fb.py:173-183 (default max_steps=m+3, a priori complete; LIMIT hard-failed; all 9 call sites).
  F6 — FB-2 fixed-V argument (NOTES:200-203), FB-4(b) DETERMINED rider (NOTES:314-316), §0.4
  u-parity clause (NOTES:104-107), FB-0 bijection restated. F7 — fb.py:179-181 ZERO folded into
  SPLIT with an unreachability note. Auditor-1 items — 15,525 population description; type-c
  vacuity remedied by PART 7b (m=6133 × 8 gates closed-form check, census type-c count 0 declared);
  2948-checks granularity; P2_srep/P6_srep identified.
- Targeted re-review 1 (adversary): `2. fixable gaps` — all 10 round-1 items verified closed (F3
  independently strengthened: t₀=932,052, v2(3t₀+4)=7 exact, every member ω=7, X(6) even ⟹ j=24
  II-b globally empty; first realisation m=1,044,747 reproduced i=0/1/2; m=j+1 claim independently
  verified 120/120 type-b; type-c remedy 8/8; 15,525=15,435+90 reproduced; full re-run ALL PASS,
  exit 0, 546,301 checks, 0 fails, 373.8 s, census numbers undisturbed). 4 residual LOW: P8_
  splitprefix_count still a constructive tautology; FB-0 measure parenthesis wrong in
  exponent/direction (source cylinder 2^−(m−j+1), target 1/2, magnification 2^(m−j)); "every class
  label" overstates the 200-label machine check; PART 7c print hard-codes 1044747.
- Round-2 VERDICT: ACCEPTED IN PART (after targeted re-review 1) + 4 residual LOW patchItems; one
  targeted re-review round remained under the round cap 2. Summarizer checks: patch locations
  byte-verified; own QUICK-mode run ALL PASS, exit 0, 28,500 checks, 0 fails, 8.1 s (smoke scope,
  not the full run).

## Patches (author) and targeted re-review 2 (final; round cap 2)

- Patches (author, per the 4 residual items): R2a — P8_splitprefix_count deleted (grep: the key
  occurs nowhere in verify_freeb.py or freeb_checks.json); PART 8 keeps its four substantive
  assertions with a comment stating that the per-pair P6_splitprefix condition carries the content
  and no aggregate count identity is asserted (verify_freeb.py:691-693). R2b — FB-0 measure wording
  corrected (NOTES:181-192): the conditional cylinder {v2(y)=m} has Haar measure 2^−(m−j+1) in the
  incoming class, the event has Haar probability 2^−(m−j+1), the map is a bijection onto Z₂×Z₂^×
  with the target cylinder of measure 1/2 and magnification factor 2^(m−j); "only the qualitative
  bijection is used in this note". R2c — §6 item 1 (NOTES:433-437) now separates the machine check
  ("at each of the first 200 class labels — first at m = 1,044,747") from the theorem statement
  ("ω(m−1) = 7, which the class fixes for ALL its members"), with the adversary's independent
  1.89·10^12 search cited. R2d — PART 7c's first m is now measured by the search loop itself
  (verify_freeb.py:661-676) and pinned by a new assertion chk('P7c24_first_realized',
  first_m == 1044747) (:677).
- Targeted re-review 2 (adversary; appended at reviews/gc_freeb_adversary.md:110): `1. closed in
  all states`, no findings. R2a verified by full-text scan (the only remaining constant-condition
  chks are the intentional hard-failure branches P6_worddiff_none/P6_limit_none, not vacuous
  checks); R2b verified by independent arithmetic (P(v2(X−V_prev)=m−j)=2^−(m−j+1) and
  (1/2)·2^(m−j+1)=2^(m−j) self-consistent); R2c wording accurate; R2d verified (the value
  1,044,747 was independently confirmed by the re-reviewer in round 1). Full re-run by the
  re-reviewer: ALL PASS, exit 0, 546,301 checks, 0 fails (435.9 s), matching the author's round-2
  record (−P8_splitprefix_count +P7c24_first_realized net out exactly); every substantive number
  unchanged across all three rounds (357,821 pairs / 1,474 gates / 0 boundary / 0 LIMIT; 15,525 =
  15,435+90; sweep 3,072,713 leaves / 362,868 pairs / 6,958 determined / 355,910 split-reached /
  0 worddiff / 0 LIMIT; type-c census empty + m=6133×8 gates; PART 7c 200/200 all ω=7). New-issue
  scan: none — the [A] layer was never touched by either patch round and matches the round-1
  item-by-item hand derivation. No open items.
- Verification gate: PASSED (post-patch full re-run ALL PASS).
- Summarizer checks this round (own reads + own full run): R2a — grep confirms no P8_splitprefix_
  count key in verify_freeb.py or freeb_checks.json, and PART 8's four assertions stand with the
  no-aggregate-identity comment at :691-693; R2b — NOTES:181-192 reads exactly the corrected
  measure/magnification wording ("Haar measure 2^−(m−j+1) … target cylinder of measure 1/2;
  magnification factor 2^(m−j) … Only the qualitative bijection is used"); R2c — NOTES:433-437
  reads "at each of the first 200 class labels — first at m = 1,044,747 — … which the class fixes
  for ALL its members"; R2d — verify_freeb.py:661-677 records first_m from the loop and asserts
  P7c24_first_realized == 1044747 (present as a passing count of 1 at freeb_checks.json:235); the
  round-2 re-review appendix present at reviews/gc_freeb_adversary.md:110. Own full re-run
  (`PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B
  work_gc_freeb/verify_freeb.py` from D:/math_cc): **ALL PASS, exit 0, 546,301 checks, 0 fails,
  435.0 s** — identical totals to the re-reviewer's 435.9 s run; PART 7c prints "first m=1044747"
  from the measured value.

VERDICT: ACCEPTED (round-1 acceptance-in-part discharged: all 10 round-1 patchItems and all 4
re-review-1 residuals applied and verified; targeted re-review 1 `2`, targeted re-review 2 `1.
closed in all states`, no open items, no new issues; verification gate ALL PASS, and the
summarizer's own full re-run ALL PASS, exit 0, 546,301 checks, 0 fails). **[A] Theorem FREE-B**
— every determined, non-record-safe post-gate output satisfies 2^(j−ell)|C_final and falls into
exactly one of three decidable branches: (I) first-landing escape (accepted FREE ⟹ j≤3+log2(6gP(g)));
(II) two-step family with the explicit closed forms S_a/U_b/U_c — non-zero-sum ⟹ j ≤ 2+log2(3gP(g)+3)
(type a, u even; u odd splits at that step) / 2+log2(21gP(g)+20) (type b) / 1+ε₁+log2(30gP(g)+29)
(type c), zero sum = explicit exact cancellation (decidable); (III) deep family (iterated
calendar-sum divisibility, decidable, not excluded) — with FB-0 (post-gate cylinder bijection),
FB-1 (v2(A)=j−ell+L_bc+1, v2(B)=m+1−ell, C=u+β·2^m), FB-2 (decidable criterion ⟺ branch.py's
accepted vc<vs rule, with the m+3 a-priori-complete termination argument), FB-3 (boundary ⟺
2^(j−ell)|C_final; ΔR∈[1,1+L_bc], both endpoints attained). **[A] FB-5 CL2 reduction** — CL2 in the
L′ environment holds at B*(g)=2+log2(30gP(g)+29)+2⌈log2(3g²+4)⌉ ⟺ no gate with j>B*(g) exhibits (α)
post-gate tree split with escape branch reaching a true NT gate, (β0) two-step zero-sum boundary,
(γ) deep-family cancellation; FREE-EXIT's budget consumers thereby reduce to explicit cancellation
families. **[B]** the census/sweep/extended-scan zero-boundary data (357,821 pairs; 3,072,713 sweep
leaves = the accepted total; 186,442 extended), counterexamples A (j=24, m=6,268,562, ΔR=1) / B
(j=42, ΔR=3 sharp) / B2 (j=78), the seeded j=61/97/78 and razor j=24/61/97 instances; plus the
round-2 strengthening: the j=24 type-b two-step family is empty at every m (class fixes ω=7, X(6)
even; first class realisation m=1,044,747, END); the 120 m=j+1 pairs all type-b, all END. **Route
R2's gap (FREE-B) is CLOSED** (closesGap=true; acceptance standard was the localisation lemma
itself — trichotomy exhaustive + decidable membership — all three-way confirmed). FREE-EXIT is NOT
closed by this acceptance and stays open, as do G1 and CL4 (untouched); the (α)/(β0)/(γ) exclusion
is a CL2/NZ-type problem; no EXT-scope or non-halting claims made or accepted.

## Round 3 addendum (2026-11-14): independent Claude adversary (coordinating session)
Rounds 1–2 above used a GLM adversary and a GLM auditor (same family as the author) plus one agy auditor. The
coordinating Claude session re-ran the verifier and added an independent Claude adversary.
- Claude adversary: `2. fixable gaps`. FB-0..FB-4, closed forms and j-bounds survive hand re-derivation and an
  independent engine (11.19M starts; 41,859 determined gates, all two-step, 0 boundary). MEDIUM: FB-5 (α) must be on
  the walk; zero-sum cases are vacuous (sums positive) so (β0) is empty and the bounds unconditional; "FREE-B gap
  closed" is an overclaim (branch (III) is a catch-all). LOW: zero-step case; FB-5 is [A-cond]; type-c data thin.
- Patch: Round-3 block in NOTES.md.

REVISED VERDICT: ACCEPTED in part. [A] FB-0..FB-4 and FREE-B for two-step boundary gates with unconditional j-bounds;
[A-cond] FB-5: CL2 at B*(g) ⟺ no (α), no (γ). Withdrawn: "closes the FREE-B gap"; the zero-sum branches. Deep boundary
gates (III) stay open as part of CL2. FREE-EXIT, G1, CL4 open.
