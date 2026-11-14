# Three-way review of work_gc_sigma (ZCode GLM subagent, R4: Σ_h uniform invariant, stage 1 — Σ_{<T4} and generator closure), 2026-11-11/12

Target: work_gc_sigma/NOTES.md (correction blocks rounds 1-2; P1–P6, Theorem CLO, Theorem
INV-FAIL, mechanism chain, §6 baseline precisification), sigma4.py, sigma4_20000000.json
(re-run after each patch round: 832.9 s round 1, 707.4 s round 2, headline numbers stable),
verify_sigma.py (patched, 29 checks), agy_audit_prompt.md. Route claim (R4, closesGap=false,
conclusion (b)): the candidate uniform-Σ invariant is exactly refuted in standard
hierarchical-closure semantics at h=4 — first precise violations 1/3, −5/3, 13/3 (den 3,
∉{4/3,−7/3}) and 28/9 (46/9-family shift, den 9 → 3-height 2); the non-integer part contains the
whole +branch 3-adic orbit δ_r = −3 + 8/3^r ≡ 5 (mod 16) for all r (closed form ⟹ unbounded den
3^r; 102 families certified r≤10, 12 distinct beyond-cap families continue); integer part
Σ_{<T4} = [−4,4] fails the ±1 candidate [−4,1]∪{3} both ways (h=3 possible-value reading already
violated by +2); mechanism = integer (5,5) entry, first possible at level E → GW fires the 10/3
family (m≤N0) → m=N0 boundary REG no-lift descendant −1/3 ≡ 5 (mod 16), chain 5 free → refires
the 46/9 family → the accepted R3 OBST orbit reproduced source-side; [B] baselines
Σ_{≤N0/<T1/<T2/<T3} reproduced field-by-field incl. the m=23 absence; [B] realization spectrum
of all 316,980 table c-crossings (cross-table {(1,−1):545,(1,0):37097,(3,0):278793,(5,0):545},
ω≥5 exactly {0}); [A-imp]+[B] Theorem CLO (⊇ walk-layer witnessed, crossing-layer honestly
downgraded open except {0}). Round-1 reviewers: adversary = ZCode GLM (attack); auditor 1 =
ZCode GLM-4.6, blind (aud1_scratch/); auditor 2 = agy gemini-3.8-flash-high, blind
(agy_scratch/). **All three attended round 1; none absent.** (Targeted re-review 1: adversary +
auditor 1; targeted re-review 2: adversary.)

## Round 1 (three-way, 2026-11-11)

- Adversary: `2. fixable gaps` (reviews/gc_sigma_adversary.md). 1 MEDIUM, 4 LOW, no HIGH.
  MEDIUM F1: FIRED_SHIFT_RANGE key-override defect — keying on (num,den) while iterating
  (num,den,lift) let each fired cs0 no-lift twin overwrite the lifted entry (17/85 dual-form
  keys, 0 lift-only), TOPFIRE/ORBITFIRE dead code; fired residues actually synthesised only for
  m∈[5,54), always liftless — scope "m<4096" false as stated; artifact iteration-order-dependent;
  verify V4 circular. No mathematical claim affected (out-of-table values are fired exact values;
  missed lifted residues all in the candidate table; legal sub-closure). LOW F2: beyond-cap log
  undeduplicated (18 lines = 12 distinct families). LOW F3: refutation-semantics qualifier.
  LOW F4: three dormant code paths undocumented. LOW F5: record inconsistencies (572 s vs 726.4;
  "25" vs 26 checks; §2 candidate omits 7/27; §3 core description; unannotated pseudo integer
  readings). Confirmed: verify re-run ALL PASS / 26 checks / 165 s; check_r0.py PASS (316,980);
  hand recomputation of every closed form; artifact forensics; DL(iv)/C7/DL5/DEEP-E/GW/REG/OBST
  citations verbatim; no EXT/horizon overreach.
- Auditor 1 (blind, ZCode GLM-4.6): `2. with fixable gaps` (reviews/gc_sigma_auditor1.md). 2
  MEDIUM (A: "953 distinct minimal-representation values" miscounts — 953 records, 684 distinct
  values; B: Tier-2 count 4728 not reproducible from NOTES — 8 predicate variants 4687–4833,
  qualitatively robust >93% out), 2 LOW (C: "出表" two senses; D: (5,5) unc_spec vs R3 block 11
  accounting), 2 INFO (E: <T1 generic merge; F: tier1 m_range display value). Confirmed
  independently, author scripts unread: every closed form in exact fractions; Θ BFS; mechanism
  chain; baseline four-level spectra incl. m=23 absence; levels field-identical; P6 recomputed;
  E tight construction rebuilt (spec=170, single unc_spec (5,5) = the accepted T4 C7 uncert
  line); 102 families ⊆ independent mechanism closure; Tier-1 85/83 + den≤3 five-tuple; Tier-2
  partial. Family-walk half taken on the author's accepted certificates (declared).
- Auditor 2 (blind, agy gemini-3.8-flash-high): `1. all correct`
  (reviews/gc_sigma_auditor2_agy.md). No findings; one artifact-readability observation
  (bad_values detailed sample truncated at chain 30). Independent no-source re-derivations:
  baseline match + canonical classifier; GEN/CLO re-derivation; tight E construction; the full
  mechanism chain incl. the ∀r mod-16 freeness proof; two-tier INV-FAIL scan; realization
  spectrum recompute; §6 precisification legitimacy.
- Round-1 summarizer spot checks: verdict lines byte-confirmed (2/2/1); agy in attendance;
  artifact forensics reconciled auditor 1's 953-records/684-values with agy's 2148-entries/
  chains ≤30 as complementary reads of bad_values; scope string and seconds byte-confirmed; own
  full verify run ALL PASS / exit 0 / 26 checks / 175 s.
- Round-1 VERDICT: **ACCEPTED IN PART** + 11 patchItems (3 MEDIUM, 8 LOW). No verdict 3, no
  unfixable HIGH; straight-accept branch unavailable (2/2/1 with three unresolved MEDIUM);
  mathematics three-way confirmed. Route gap (closesGap=false) not closed.

## Patches (author) and targeted re-review 1 (2026-11-11)

- Patches (author, per the 11 round-1 patchItems): correction block (11 items) at the head of
  NOTES.md; F1 (MEDIUM): FIRED_SHIFT_RANGE keyed by (num,den,lift) with sorted() iteration;
  synthesis ranges honest — no-lift/deep m<54, lifted m<64 with the lift bit at the fired chain;
  [64,N0) claimed only via M_h.fired_range + family all-chain certificates (m≥65 fired classes
  all 4/3+2^m, in-table, so no Tier-2 residue lost); scope string rewritten; verify V4 split
  into V4a (all 102 families scalar-re-certified vs the artifact — circularity removed) / V4b
  (structure) / V4c (presence). F2: FIRE_SEEN dedup + RAW_FIRE_LOG. F3-F5: semantics sentence,
  dormant-path note, record fixes (832.9 s, 26→29 checks, candidate triple, core description,
  sigma_ints_note). Auditor-1 A/B/C/D/E + agy: bad_values_note semantics, Tier-2 predicate L
  made explicit ({(k,none): |k|≤16} ∪ {(4/3, m any)} ∪ {(−7/3, none)}, search domain e≤10,
  |v|≤64, m∈{none}∪[5,min(c,64)]), terminology, (5,5) accounting, <T1 aggregation, truncation
  note. Re-run (832.9 s; 59 chains 5..63): n_bad 4728→5379, bad_values 953→1600 keys/684
  distinct/2799 witnesses, canon 258→300, e≤1 no-representation 4049→4698 (e≤10 still 0),
  Tier-1 102 entries (85 distinct values) with 99 out (83 distinct), kinds {deep:85, top:1,
  orbit:16}, M_h[<T4>]=[5,63] + fired_range [5,N0]. All core results unchanged.
- Targeted re-review 1 (adversary): `2. fixable gaps — 仅余 LOW 记录性残留，数学内容封闭`. All 11
  items verified closed (patched verify full re-run ALL PASS / exit 0 / 29 checks; own
  independent re-scan of all 5706 residues gives in-table 327 = 278 strict + 49 bare-4/3, out
  5379 — exact; code regions read; the "m≥65 loses nothing" argument independently checked).
  5 residual LOW: §3:178 body old count "18 条"; bad_values_note hard-coded "953" (now 1600
  keys); orbit [5,64] synthesis-cap-vs-GW(b)≈17 loosening unannotated; V4a vs [:4]-truncated
  family_unc latent; T1_BAD family field drops lift bit.
- Targeted re-review 1 (auditor 1): `2. with fixable gaps` (2 residual LOW). A–E all verified
  patched (1600/684/2799 re-parsed; predicate L re-implemented: 5706/5379/327=278+49 exact —
  Tier-2 now independently reproducible; C/D/E text-verified). Full regression pass (levels
  identical, P6, E construction, 102 families, FIRE_LOG 12+18, Tier-1, M_h, canon 300, 4698/0
  independently recomputed — the auditor's initial 2860 reading was the auditor's own
  negative-residue mod bug, located and fixed, not an author issue). Residual LOW: the
  bad_values_note "953"→1600 sync; §2 P3's specific (5,5) candidate selection rule still
  implicit (168 candidates per the auditor's a7b enumeration; only 3 symmetric-representative
  seeds fired — harmless for INV-FAIL, potential under-inclusion for CLO ⊆).
- Verification gate: PASSED — and re-run by the summarizer that round: ALL PASS / exit 0 / 29
  named checks / 173 s.
- Summarizer checks that round: correction block 1:1 with the 11 patchItems; patched code
  regions read (sigma4.py:456-486, :717-722, :281-301; verify_sigma.py:259-303); artifact
  forensics (832.9 s, 5379, 1600/684/2799, canon 300, kinds {deep:85,top:1,orbit:16}, 12+18
  note, M_h); residual "953" note and §3 "18 条" byte-confirmed; own verify run as above.
- Round-end status: ACCEPTED IN PART + 6 residual LOW patchItems; one author patch round +
  targeted re-review remained under the round cap 2.

## Patches (author) and targeted re-review 2 (final; round cap 2, 2026-11-12)

- Patches (author, per the 6 residual items): round-2 correction block (NOTES.md:49-64, 6
  items): §3 body synced to "12 个不同族（18 次原始追加）" (:154/:200-201); bad_values_note now
  dynamically generated from len(bad_values) (sigma4.py:638-644); orbit loosening annotated
  (GW(b) true bound m≲17 for chain-5 shallow-provenance free entries; [17,64) direction-safe —
  extra synthesised residues share values with deep twins) at :55 and §2/§3 (:154); family_unc
  stores the full unc list, no [:4] truncation (sigma4.py:735); T1_BAD family field now
  '%d/%d/%d' with the lift bit (sigma4.py:651); the specific (5,5) candidate selection rule
  disclosed (correction block item 6: per-e-layer symmetric representatives sym(cls·3^e mod 2^6)
  — 15/3=5, −19/9, 7/27, 21/81=7/27 after Fraction reduction → exactly {5, −19/9, 7/27};
  −49/3-type candidates unfired, calendar-open). Artifact re-run (707.4 s) — all headline
  numbers identical (59 chains 5..63, 5706 residues, n_bad 5379, 102 families, 12 beyond-cap +
  18 raw, Tier-1 99/83, 1600/684/2799).
- Targeted re-review 2 (adversary): `2. fixable gaps — 仅余披露层面 LOW 残留，数学内容封闭`. All 5
  round-2 items (N1-N5) verified closed three ways — code lines, re-run artifact, own full
  verify re-run against the round-2 artifact (ALL PASS / exit 0, 163 s; the reviewer's command
  captured only the output tail, honestly noted — ALL PASS prints only when the failure list is
  empty, so all 29 checks passed); patches introduced no mathematical problem and disturbed no
  headline number. The selection-rule disclosure verified as stated. 2 new LOW residuals:
  N6 — the quoted candidate count "168 个" (correction block item 6 / §3:151, sourced from
  auditor 1's round-1 enumeration) is not reproducible: the reviewer's two natural conventions
  give 162 (global reduced-by-value dedup: 2 int + 4 den3 + 12 den9 + 36 den27 + 108 den81) and
  242 (stratified (num,e) pairs); the payload fact (only 3 symmetric-representative seeds fired
  ≪ the full candidate set) holds under either; N7 — §4's Theorem CLO statement defines
  Fire(𝓔_{h+1}) without back-referencing the seed convention: at theorem level the ⊆ direction
  should mean the full candidate firing closure (all ≡5 mod 64 candidate values), while the
  artifact certifies a symmetric-representative-seeded sub-closure — disclosed in the correction
  block but not referenced where the theorem is stated. Strengthening observation (reviewer's
  own analysis): the spec free entry (5,5)'s unique D-source is the bulk a-output
  ('bulk',−1,244875), an integer walk's a-output whose true value the accepted window forces to
  exactly 5 (−59 out of window) — so θ+D−2=5 exactly and the true-value seed 5 is already in
  the firing set; the under-inclusion concern of correction block item 6 does not bite on this
  data.
- Verification gate: PASSED (re-reviewer's 163 s run) — and re-run by the summarizer this round:
  `PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B
  work_gc_sigma/verify_sigma.py` from D:/math_cc — **ALL PASS, exit 0** (tail captured: V7a
  cross-table, V7b ω≥5={0}, V8a/V8b/V8c all ok; ~169 s; ALL PASS prints only on an empty
  failure list, so all 29 checks passed; the summarizer's earlier full-output runs this review
  confirm the check list). sigma4.py's 707.4 s full-table run not repeated by the summarizer
  (the re-reviewer verified the shipped artifact; headline numbers byte-checked below).
- Summarizer checks this round (own reads + own runs): round-2 correction block read
  (:49-64, 6 items mapping to the 6 residual patchItems — the disclosure item resolved in
  substance); §3 sync byte-confirmed (:154/:200 "12 个不同族", :201 raw-append annotation; the
  old :178 "18 条" gone); orbit annotation at :55/:154 ("真界 ≲17，[17,64) 方向安全");
  bad_values_note now reads "(1600 keys, 684 distinct values in this run)" (dynamic); family_unc
  102 entries with unc_s lengths ∈ {0,1} (17 families with unc — no truncation); T1_BAD family
  fields carry the lift bit ('-177139/59049/0' etc.); E.unc_spec provenance byte-confirmed
  (['E1','c',2,5,5,['bulk',−1,244875]] — the input to the reviewer's window-bound
  strengthening); §4:215-221 Theorem CLO read — Fire(𝓔) defined with no back-reference to the
  seed convention (N7 confirmed); "168" present at :61/:151 (N6 target). Own candidate
  enumeration (Python312 one-off): convention A (reduced distinct values, e≤4, |v|≤64,
  v≡5 mod 64) = **162** with per-layer 2/4/12/36/108; convention B (stratified (num,e) pairs) =
  **242**; variants (|v|<64 → 162) — **168 not reproduced under any convention tried**,
  matching the re-reviewer exactly; the disclosed symmetric-representative rule's arithmetic
  checked (15/3=5, −19/9, 7/27, 21/81=7/27 → {5,−19/9,7/27}). Own verify gate run as above.
- FINAL VERDICT: **ACCEPTED IN PART (terminal — round cap 2 reached, no further re-review
  rounds)**. Round 1's 11 patchItems and round 2's 6 patchItems are all resolved and verified;
  targeted re-review 1 `2` (LOW-only), targeted re-review 2 `2` (LOW-only, disclosure-level;
  "数学内容封闭"). The straight-accept branch stayed unavailable at every round gate (final
  re-review at 2), so acceptance-in-part is the terminal decision; the 2 remaining LOW items
  (N6 count disclosure, N7 theorem-statement back-reference) are recorded below for a future
  touch — they gate nothing: no mathematical claim depends on the 162/242-vs-168 count (the
  fired-seed set {5,−19/9,7/27} is what was certified, under either convention a strict
  subset), and the CLO ⊆ sub-closure vs full-closure distinction is exactly the reviewer's
  window-bound observation (the true seed 5 is in the firing set on this data). Route R4's gap
  (closesGap=false by route definition) not closed; gapClosed=false.

What stands (terminal, three-way confirmed + two re-review rounds): [A+B] **Theorem INV-FAIL**
in standard hierarchical-closure semantics — integer part [−4,4] vs the ±1 candidate [−4,1]∪{3}
both ways (h=3 possible-value reading already violated by +2); first exact non-integer
violations 1/3, −5/3, 13/3, 28/9; the +branch 3-adic orbit δ_r≡5 (mod 16) ∀r with GW fire
6−8/3^{r+1} and a-descendant δ_{r+1} makes the 3-height unbounded (witness reading at h≤4
itself stays zero-out-of-table — violations are closure/fired-reading statements; r≥2 orbit
values depend on the m=N0 deep-fire calendar-open branch). [A-imp] the mechanism chain ((5,5)
first possible at level E → 10/3 family → m=N0 boundary −1/3 ≡ 5 mod 16 → chain-5 free → 46/9
family; R3's OBST orbit reproduced source-side; round-2 strengthening: the (5,5) spec entry's
D-source is an integer bulk a-output window-forced to exactly 5). [A-imp]+[B] Theorem CLO with
the honest crossing-layer downgrade (⊇ at ω≥5 witnessed only by {0}; rest calendar-open) — with
the standing qualification that the artifact's Fire term certifies the
symmetric-representative-seeded sub-closure {5,−19/9,7/27} ⊂ full candidate closure (162
reduced / 242 stratified candidates; −49/3→94/9-type branches unfired, calendar-open; N7's
back-reference pending). [B] baselines field-by-field (incl. the m=23 absence, BASE_OK 5/5);
[B] the tight level-E construction (spec=170, unc_spec={(5,5)} = the accepted T4 C7 uncert
line, families 102 with R3 overlap 60/42/74); [B] the realization spectrum (316,980; four
cells; ω≥5={0}); [B] the patched Σ_{<T4} assembly — 59 chains (5..63) 5706 residues, 300
canonical families, Tier-2 5379 out of the explicit candidate list L (in-table 327 = 278
strict + 49 bare-4/3; independently reproduced by both re-reviewers), e≤1 no-representation
4698 / e≤10 zero, Tier-1 102 entries (85 distinct fired values) with 99 out (83 distinct),
beyond-cap 12 distinct families (den 3^11). Route conclusion (b) stands: the candidate
uniform-Σ invariant shape is refuted; successors must be orbit-aware or J-dependent/
trajectory-level (G1/tower ladder). Remaining for a future touch (LOW, non-blocking; round cap
2 reached): the N6 count disclosure (168 → state the convention or use 162/242) and the N7 §4
Fire-term back-reference to the seed convention ("full candidate firing closure at theorem
level; artifact certifies the symmetric-representative sub-closure").

## Round 3 addendum (2026-11-14): independent Claude adversary (coordinating session)
Rounds 1–2 above used a GLM adversary and a GLM auditor (same family as the author) plus one agy auditor. The
coordinating Claude session re-ran the verifier and added an independent Claude adversary.
- Claude adversary: `2. fixable gaps` with withdrawals. HIGH: all den-3 violations and the orbit enter through the
  non-existent (N0, 10/3+2^N0) chain; the values 1/3, −5/3, 13/3 are not a-outputs; "unbounded 3-height" false.
  Survives: 14 residues 46/9+2^c (shift 28/9+2^c), 3-height 2, fired-range reading only.
- Patch: Round-3 block in NOTES.md. No recomputation done.

REVISED VERDICT: ACCEPTED in part. [B] baselines Sigma_{<=N0}..Sigma_{<T3}; [B] the weak INV-FAIL at h=4 (28/9+2^c).
Withdrawn: the den-3 violations, unbounded height, the (5,5)→10/3@N0 mechanism.
