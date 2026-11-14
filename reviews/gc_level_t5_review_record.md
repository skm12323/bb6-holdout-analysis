# Three-way review of work_gc_level_t5 (ZCode GLM subagent, R3: level 5 — EXT toward T5), 2026-11-11

Target: work_gc_level_t5/NOTES.md (Lemma DL5, Lemma DEEP-E, Lemma GW, Theorem REG, Theorem OBST,
[A-cond] Theorem T5-RED), rwalk_t5.py, levels_t5.py, verify_t5.py, levels_t5_20000000.json,
levels_t5_run.log, full_run_console.log, agy_audit_prompt.md (+ aud1_scratch/, agy_scratch/).
Route claim (per the R3 brief): prove Theorem T5 — for every T4<=J<T5 with F defined through
tau(J−1), S(J) is tie-free, relative to the accepted EXT(<T4) — via (1) full-chain rational bulk
certification, (2) level E zero-uncertainty (or explicit absorbed residual families), (3) the
C5_EXTENSION induction re-proved at Lambda=5 incl. BBBAA/RES-type deep regressions. **The author
honestly did NOT claim T5**: the static family-certificate route is blocked by Theorem OBST (the
chain-5 free-entry recursion is exactly the accepted route-A rational orbit −3±8/3^r, infinite
3-adic path, closed-family closure impossible). What was claimed: [A] DL5/DEEP-E/GW/REG
(REG resolving the r1r2 Remark 2.5 RES residual at T5 scale), [B] the level-E and C7-E full
computations with residuals exactly the chain-5 free-entry set {5, 21(≡−1/3), −27(≡−17/3),
−11}∪{(5,5)} all GW-resolved, plus the rational-family certification (orbit no-lift families
fail exactly at chain 5, the rest pass full range), [A+B] OBST, [A-cond] T5-RED (ORBIT-9 ⟹
S(J) tie-free). Not claimed: T5, any EXT range increase, machine-level horizon change.
Reviewers: adversary = ZCode GLM (attack; algebra re-derivation, own randomised cross-checks,
full-range supplemental certifications, entry-set completeness enumeration, source-level audit;
also the targeted re-reviewer in rounds 1 and 2); auditor 1 = ZCode GLM, blind (aud1_scratch/:
a1_algebra.py, mywalk.py, a2_validate.py, closure.py, closure_noefam.py; scripts/JSON only);
auditor 2 = agy gemini-3.8-flash-high, blind (agy_scratch/: 16 scripts, rules 1–6 of
agy_audit_prompt.md). **All three attended; none absent.**

## Round 1 (three-way, 2026-11-11)

- Adversary: `2. fixable gaps` (reviews/gc_level_t5_adversary.md). 3 MEDIUM, 4 LOW, no HIGH.
  MEDIUM F1: T5-RED's [B] base was not full-range at the closure boundary — levels_t5.py capped
  FAM_SET at den<=3^9 (den-3^10 emissions only reached FIRE_LOG), and verify check 8's full-range
  list had only the 8 den<=27 key families, orbit families only at smoke JHI=300003 — so NOTES §7
  "≤9-layer families are [B]-certified" was literally unsupported. The adversary pre-verified the
  gap numerically: all 12 den-3^10 families certified full range (2 emission + 8 b/cs descendants
  uncert=[]; the a-descendants δ_10^± fail exactly at chain 5, consistent with OBST and excluded
  by ORBIT-9). MEDIUM F2: level_entries silently dropped rational generic-c landings (only
  canon-integer results registered; the a/b branch did call add_fam) — the adversary's
  enumeration flagged 4 uncertified classes (−10/3, −8/3, 14/3, 16/3) and certified all 4 full
  range (pass). [Re-classified in re-review 1: with the correct per-t source structure the 4
  flagged classes are unreachable — see the patch section; the original drop was a latent
  fragility, not an actual hole.] MEDIUM F3: REG's written proof did not cover its
  "unconditional" label — (i) the size inequality tacitly assumed r≲0.63m; (ii) the y=J case
  (emissions m∈[N0,T4)) was unwritten; (iii) the deep-fire tower-depth O(1) counting argument was
  absent. LOW F4: family_cert dropped scalar aouts on chains 5..63 vs the accepted T4 mechanism —
  probe found exactly one new key (7,−50), a representative NT artifact (true class 14, already
  fired-covered), consumers all certified. LOW F5: verify coverage weaker than NOTES claims
  (check 9 read the json rather than recomputing; check 8 full list lacked the orbit no-lift
  families; check 5 covered [64,3000) while NOTES claimed cross-consistency to 3·10^5). LOW F6:
  the bulk-failure fire path fired the 56-bit truncated value as if exact and only the first 4
  failures — dormant (0 bulk failures in the run). LOW F7: OBST wording — only the +branch
  c_r=−3+8/3^r is the accepted route-A object; no-lift families computed to r=9 only.
  INFO F8 (disclosure): the adversary's smoke re-run overwrote levels_t5_run.log/
  levels_t5_300003.json (restored from full_run_console.log, content equivalent).
  Confirmed (all independently): verify_t5.py 10/10 ALL PASS exit 0 in 103.6 s; GW identity
  (hand algebra + 1400 random states incl. 491 with m>j, zero failures + five anchors); drift
  sets Θ_S/Θ^E hand == BFS == tables (incl. Θ_4∋−1/3); DEEP-E classification; OBST closed form
  (δ_r^±≡5 mod 16 verified to r=24; json orbit_free_entries match; real anchor chain
  (5,5)→10/3→−1/3→46/9→…); E/C7E residuals exactly {(5,5),(5,21),(5,−27),(5,−11)}+int(5,5) with
  source tracing; T4 reproduction; truncation faithfulness on all 122 round-1 families
  (max|3k·den+num|=526797150452<2^53); family_status (no bulk uncert, no non-chain-5 scalar
  uncert, 18 orbit no-lift families); smoke re-run reproducible; imports all exist as cited;
  honesty framing accurate.
- Auditor 1 (blind): `2. with fixable gaps` (reviews/gc_level_t5_auditor1.md). 5 LOW, no
  MEDIUM/HIGH. F1: the tight value of S_2 is {0}; NOTES reused S_1={−1,0,1} at t=2 — reliable
  over-approximation (integer tables identical under both choices, both computed; rational Θ_3
  misses 13/3), but "exact drift sets (zero margin)" overstated t=3,4 rationals. F2: REG's size
  inequality needs r≲0.63m; holds with huge margin in the actual use range — should be noted or
  structurally sourced. F3: §6's four-residual resolution narrated by mod-64 class grouping —
  literal reading misattributes the two spec residuals' emissions (true fractions −19/9−2^j and
  −35/9−2^j emit 154/27, 170/27 per the author's own orbit_free_entries; only the integers
  (5,5)/(5,−11) emit 10/3, 26/3). F4: §7 OBST(b) climb-word list incomplete ([5,8]/[5,10] also
  occur, representative-convention dependent). F5 (clarification): level E's spec residuals
  arise only through the E0-slot family-exit over-approximation — control experiment
  (closure_noefam.py): removing E0 family exits empties E's spec uncert while C7E's residuals
  persist via S0; the 26/3 and 62/9 lines have no independent real anchor (conservative
  inclusion). Confirmed: GW identity + all special cases (7000 random pairs; r1r2/
  SECOND_GATEWAY/ODD_DENOMINATOR cross-checked); DL5 tower bounds and full drift tables
  (independent BFS == hand tables); DEEP-E re-derived; REG structure + inequality in range; OBST
  closed form + json data + fire_beyond_cap == closed form + REG descendant set; T4 reproduction
  byte-identical (independently recomputed in full, 2045 s); integer window uncert only (5,[5]);
  E/C7E residuals identical (spec counts 1834/1960 vs the author's — narrower source handling,
  residual sets equal); 122 families: exactly the 18 orbit no-lift families fail at chain 5
  only, the other 104 pass full range; truncation faithfulness and bulk==scalar; honesty and no
  overclaim.
- Auditor 2 (agy, blind): `1. all correct` (reviews/gc_level_t5_auditor2_agy.md). No findings at
  any severity. Independently: BFS drift sets == NOTES tables item-by-item; the S_3=S_4=∅
  tightening argument; GW identity derived and validated by sampling on 8 chains; all special
  cases; own certifier (scalar walk + 56-bit vectorised bulk) reproducing family_status
  verbatim; truncation faithfulness on all families over all 6,057,585 odd a-chains
  (max ≈5.27·10^11 < 2^39 ≪ 2^53); OBST arithmetic (r=1..12) + independent certification of the
  18 no-lift families (fail exactly chain 5) and all emission families; orbit_free_entries ==
  closed form; E/C7E residual lists and provenance all verified; T4 reproduction (json
  byte-equal + rwalk.bulk replay of δ=5/−11: uncert exactly [5]); REG inequality vectorised over
  the whole table (min margin 41.29 bits) and the ≤3-step logic; honesty, grading labels, and
  historical compatibility all in order.
- Round-1 VERDICT: ACCEPTED in part + 11 patchItems (3 MEDIUM, 8 LOW). No HIGH findings from any
  reviewer; all three independently confirmed the core [A]/[B] content. Route R3's gap NOT
  closed: T5 was not proved and OBST shows the static family-certificate route cannot close it.
- Summarizer checks round 1: the three review files; code citations byte-checked; the round-1
  json via python -I (122 families, orbit keys 5,3^2..5,3^10, fire_beyond_cap 36, E/C7E
  n_specific 2133/2372, residuals exactly the chain-5 set); NOTES honesty header; own full run
  of the round-1 verification suite: 10/10 ALL PASS, exit 0, 107.9 s.

## Patches (author) and targeted re-review 1 (2026-11-11)

- Patches (author, per the 11 round-1 patchItems; recorded as a 12-item review-correction block
  at the head of NOTES.md, declared to override the body): cap raised to den<=3^10
  (levels_t5.py:314) + full re-run (run.log: 46,074 s; P1 T4-reproduction assertion passed;
  family set 122→134; orbit_free_entries now 10 tower keys 5,3^2..5,3^11 — the den-3^11
  emissions stay in FIRE_LOG, 36 entries); generic-c branch now add_fam's canon-rational
  results; §5 rewritten with the explicit REG-Size lemma (r<=0.6m−25), the G-collapse chain for
  the y=J case (<=4 steps), an m>=T2 c-step size bound, and the deep-regression O(1) counting,
  with the REG label downgraded "unconditional" → **[A | 发射 Q<=3^11]**; family_cert aggregates
  scalar aouts excluding NT/climb outputs (E/C7E specific counts 2133→2315, 2372→2554,
  residual lists unchanged); verify check 5 extended, check 8 full list expanded to 38 families
  incl. the den-3^10 layer, new check 9b replaying the t=0 spec construction (280 entries;
  failures = the chain-5 mod-16=5 set {5,21,37,53} + the known (8,58), which GW-fires −37/3);
  bulk-failure fire path now fires exact classes incl. lift (dormant, 0 triggers); OBST wording
  per ±branch and r<=9 no-lift / r<=10 emission; the five auditor-1 wording items applied.
- Targeted re-review 1 (adversary): `2. fixable gaps` — "距离 1 只差编辑性收尾，无新数学缺口".
  All patches verified, including by independent computation: own run of the patched
  verify_t5.py (11 checks ALL PASS, exit 0, 328 s); the 134-family set from the json (orbit
  no-lift r=1..10 = 20 families, 20/20 cross-checked); F2 **self-corrected**: with the correct
  per-t source structure (t=1: g∈{0..4}, t=2: {1,2,3}, t=3: {2}, t=4: ∅) exactly 8 rational
  generic-c classes are reachable and all are in the 134-family set — the round-1 flagging of 4
  classes was itself an over-approximation (unreachable); the original silent drop was a latent
  fragility, not an actual hole, and the patch is correct; F3 verified (REG-Size boundary
  numerics: m=780, r=443 → 723.5 < 778; m=1000, r=575 → 933.1 < 998; m=N0, r=11 → 55 ≪ m−2);
  134-family truncation faithfulness independently verified (max = 1,580,391,451,340 < 2^53,
  worst family 531449/59049); patched smoke vs the full re-run identical in family set,
  residuals, orbit keys. Remaining findings — all editorial: R1 the honesty block (NOTES.md:47)
  and §8 (:278) still said REG "无条件解决"; R2 REG(e) (:216) "y<64 … m<G(64)+1=16" literally
  wrong (should be y<N0, m<G(N0)+1≈52; conclusion unchanged); R3 stale cap/count strings
  (NOTES:181/:226, levels_t5.py orbit_cap_note, verify_t5.py:288 comment); R4 check 6's fixed
  32-family list lacked the den-3^10 layer; R5 the correction-block header miscounted the
  adversary's round-1 file ("4 MEDIUM"); R6 the dormant bulk-fire path does not add the 2^j
  lift bit for lift families (0 triggers). Verification gate after patches: ALL PASS.
- Summarizer checks this round: every remaining-finding citation byte-verified (incl. the same
  "y<64 ⟹ m<16" claim also inside correction-block item 3 at NOTES.md:17, flagged by the
  summarizer for the R2 fix); patch code spots verified (levels_t5.py:314 cap, :367-372
  generic-c add_fam, :260-272 scalar aggregation, :344-354 exact-class fire); patched json via
  python -I (134 families, orbit keys 5,3^2..5,3^11, fire_beyond_cap 36, E/C7E 2315/2554 with
  residuals unchanged, exactly 20 families failing exactly [5]); run.log tail (46,074 s, P1
  pass, ORBIT to 3^11); own full run of the patched verification suite: 11 checks ALL PASS,
  exit 0, 279 s; REG-Size boundary numerics reproduced exactly by me (723.5<778; 933.1<998;
  55≪m−2). NOT repeated by me: the 46,074 s full re-run itself (log and products verified).

## Patches (author) and targeted re-review 2 (final; round cap 2)

- Patches (author, per the 6 round-1-re-review items): R1 — the honesty block (NOTES.md:55-57)
  and §8 (:289-291) now read "REG [A | 发射 Q≤3^{11}] … 在该范围内…解决"; grep confirms
  "无条件" survives only inside the correction block's descriptions of the change itself
  (:17/:46/:196/:231). R2 — REG(e) (NOTES.md:224-226) now "provenance y<N0（回归后链可落在
  [64,N0)），发射 m<G(N0)+1≈52", with the GW(b) tail (:185) synced and the correction-block
  copy (:17) fixed as well (the summarizer's add-on). R3 — cap/count strings unified
  (NOTES.md:191 "封顶 den≤3^{10}", :237 "134 族", verify_t5.py:19/:300/:304 "ALL 20 orbit
  no-lift (r=1..10)", levels_t5.py:472 orbit_cap_note string "beyond den=3^10"). R4 — check 6
  now reads the family set dynamically from levels_t5_20000000.json (with a safe fallback and
  provenance label) instead of a fixed 32-family list. R5 — correction-block header (NOTES.md:6)
  now "攻击员 3 MEDIUM＋5 LOW＋1 INFO＋复算员A 5 LOW". R6 — NOTE comment at levels_t5.py:348
  (if ever enabled, LIFT families must add the 2^j lift bit); branch still 0 triggers.
- Targeted re-review 2 (adversary): `1. closed in all states` — "两轮全部数学性发现已闭合".
  Verified with its own run of the round-2 verify_t5.py (11 checks ALL PASS, exit 0, 324.8 s;
  check 6 reports "134 families from levels_t5_20000000.json (observed max 1580391451340 <
  2^53)" — identical to its round-1 independent computation); no new mathematical problems; the
  computational products (134 families, orbit to 3^11, residual lists, P1 T4 reproduction) are
  the already-verified 16:35 full-run outputs, untouched by the round-2 edits. One remaining
  cosmetic item R7 [LOW·纯装饰]: two purely descriptive strings still say 3^9 — (a)
  levels_t5.py:325 certify_families docstring "closure within den <= 3^9"; (b) the published
  levels_t5_20000000.json orbit_cap_note field "beyond den=3^9" (the json was generated 16:35,
  before the 17:23 code change, and was not re-run) — no claim, calculation, or certificate
  depends on either; they self-heal on the next data-producing re-run (or manual sync).
- Summarizer checks this round (all run/read during this adjudication): every round-2 fix
  byte-verified by me — grep "无条件" (only correction-block descriptive hits at :17/:46/:196/:231);
  NOTES.md:55-57/:289-291 downgraded label; :224-226 y<N0 / G(N0)+1≈52 (and :185, :17);
  :191 "封顶 den≤3^{10}", :237 "134 族"; verify_t5.py:15 (dynamic json source), :19/:300/:304
  (20 orbit no-lift r=1..10); levels_t5.py:472 orbit_cap_note code string "beyond den=3^10";
  NOTES.md:6 corrected header; levels_t5.py:348 NOTE comment; both R7 residues confirmed by me
  (levels_t5.py:325 docstring; json orbit_cap_note via python -I; timestamps: json 16:35,
  levels_t5.py 17:23, verify_t5.py 17:38, NOTES.md 17:43 — consistent with the re-reviewer's
  diagnosis). My own full run of the final verification suite
  (`PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B
  D:/math_cc/work_gc_level_t5/verify_t5.py`): **11 check lines all ok, ALL PASS, exit 0,
  310.2 s** — check 6: "134 families from levels_t5_20000000.json (observed max 1580391451340
  < 2^53)", check 8: "38 families at FULL range incl. den-3^10 layer", check 9b: 280 rebuilt
  entries, failures {5,21,37,53}+(8,58) — matching the re-reviewer's runs at both rounds.

VERDICT: ACCEPTED (round-1 acceptance-in-part discharged: all 11 round-1 patchItems and all 6
round-1-re-review items applied and verified; targeted re-review 1 `2. fixable gaps` closed by
round 2; targeted re-review 2 `1. closed in all states`, no mathematical reservations;
verification gate ALL PASS on the summarizer's own final run. Round cap 2 reached; the one
remaining item R7 is purely decorative and non-blocking — see below.) **[A]** Lemma GW — the
unified NT-gateway identity: exact 3D′=9−D−x′+6k_j and D′≡(9+6k_j−D)·3^{−1}+2^m (mod 2^{m+1}),
rational class form (9+6k_j−δ)/3+2^m with m<G(y)+1, unifying r1r2 Thm 2.4, SECOND_GATEWAY and
(j=8, δ=58)→−37/3 (three independent confirmations). **[A]** Lemma DL5 — S(J) has <=5 deep
chains with j_t<T_{5−t}; integer drift sets Θ_1=[−1,3], Θ_2=[−2,4], Θ_3=[−3,5], Θ_4=[−4,6] with
rational C/3 columns entering only via the t=0 shift 4/3; S_2 tight value {0} and the t=3,4
rational columns conservative (integers exact). **[A]** Lemma DEEP-E — source deep a-outputs:
levels C/D {1,2,3}, level E [0,4]∪{10/3 at chain N0}; hence the S(J) deep c-shift sets t=0:
[−2,2]∪{4/3}, t=1,2: {−1,0,1}, t=3,4: ∅. **[A | 发射 Q<=3^11]** Theorem REG (label downgraded
from "unconditional" per correction block, now synced everywhere incl. the honesty block and
§8) — deep rational regressions with m>=N0 return to the shallow region in <=3 symbolic steps
with strictly decreasing records, landing in the explicit no-lift descendant set
{3Q−C, C−Q, C±3sQ}/Q; with the written REG-Size lemma (r<=0.6m−25), the y=J G-collapse chain
(<=4 steps) and the O(1) deep-regression counting, boundary numerics independently reproduced.
**[B]** the level computation (cap den<=3^10, full re-run 46,074 s) — T4 reproduction
byte-identical; integer window [−8,10]∪{−6,−5,−4,6,7} uncert only (5,[5]); level-E and C7-E
residuals exactly the chain-5 free-entry set {5, 21≡−1/3, −27≡−17/3, −11}∪{(5,5)}, the four
GW-resolved into fully certified families (fraction-true attribution); 134 rational families
under the 56-bit truncated bulk (ceiling min(j−loss,56); truncation-faithful on all 134
families and all odd a-chains, max|3k·den+num|=1.58·10^12<2^53, now machine-checked over the
full family set by check 6's dynamic json path): exactly the 20 orbit no-lift families (r=1..10,
both branches) fail, at chain 5 only; the remaining 114 (including all with-lift) pass
5<=j<2·10^7; the reachable rational generic-c classes number exactly 8 and all lie in the
family set. **[A+B]** Theorem OBST — δ_r^±=−3±8/3^r ≡5 (mod 16) for all r, chain-5 GW emission
6∓8/3^{r+1} with a-descendant δ_{r+1}^±; the +branch is the accepted route-A 3-adic obstruction
orbit (−branch a symmetric extension, same obstruction); the family graph contains an infinite
path anchored in the real structure ((5,5)→10/3→−1/3→46/9→−19/9→…), so the static
finite-family certificate route for T5 cannot close (no-lift computed r<=10 in the artifacts,
orbit data to 5,3^11; closed form for all r). **[A-cond]** Theorem T5-RED — ORBIT-9(J) ⟹ S(J)
tie-free, relative to the accepted EXT(<T4) and imports; its [B] base closed in-artifact at the
den<=3^10 closure boundary. NOT achieved and NOT claimed: Theorem T5 itself; any EXT range
beyond T4; any machine-level horizon change (the accepted horizon 2^T4−2 from R1 stands).
**Route R3's gap is NOT closed** (hence gapClosed=false despite the acceptance): T5 was not
proved and OBST shows the static family-certificate route cannot close it — future progress
needs trajectory-level or J-dependent mechanisms (NOTES §7 end records two untried routes).
Remaining for a future touch (non-blocking; round cap 2 reached, no further re-review round):
R7 — levels_t5.py:325 docstring and the published levels_t5_20000000.json orbit_cap_note field
still say "3^9"; purely descriptive, no claim depends on them; self-heals on the next
data-producing re-run or by manual string sync.

## Round 3 addendum (2026-11-14): independent Claude adversary (coordinating session)
Rounds 1–2 above used a GLM adversary and a GLM auditor (same family as the author) plus one agy auditor. The
coordinating Claude session re-ran the verifier and added an independent Claude adversary.
- Claude adversary: `2. fixable gaps` with withdrawals. HIGH: the m=N0 boundary emission does not exist (CLOCK gives
  m <= 10^7+50); OBST(c) is not an impossibility (ungraded closure; real depth <= r0+4). MEDIUM-HIGH: T5-RED unproved
  (multi-step deep descendants missing; failing class 10/9 at chain 8; no Λ=5 analogue of C5_EXTENSION §4). MEDIUM: NT
  outputs wrongly dropped. LOW: ORBIT-9 index undefined; FAM_SET bookkeeping; tautological checks.
- Patch: Round-3 block in NOTES.md. No recomputation done.

REVISED VERDICT: ACCEPTED in part. [A] DL5 (sound supersets), GW, the OBST algebra; [B] the level-E data as computed.
NOT accepted: T5-RED, OBST(c) as impossibility, "static route cannot close T5". The route to T5 is open.
