# work_r10/review_advD.md — ADVERSARY-2 review of agentD's H1-dk closure

Reviewer: ADVERSARY-2 (independent re-derivation, code-level). Date 2026-10-13.
Object under review: `agentD_report.md` (final), `agentD_proof.py`, `agentD_measure.py`,
`agentD_table_cpt.json`, `agentD_table5100.json`, `agentD_data.json`, and the H1-dk
claims propagated into `ASSEMBLY.md`. Read-only inputs respected; all outputs in
work_r10 only. Review scripts: `revD_1_identities.py`, `revD_2_window.py`,
`revD_3_spinedec.py`, `revD_4_phiprofile.py`, `revD_5_step.py`, `revD_6_scope.py`,
`revD_7_basetable.py`, `revD_7b_fast.py`, `revD_gap5200.py`. Total footprint < 1 MB.

**Method disclosure.** My Phi_J tracer was written from PROOF_G6 §0's definition
(queue [u·2^0..2^{J−2}, D_h, T_2..], A = u+1, per-step pair read, j-chain pushes
j−1 run entries + 1 seam) with its own labeling and its own K-extraction; it is
structurally different from agentB2_lib.phi_traced (which I had already seen, being
on the allowed read list, before coding — the identities were nonetheless re-derived
by hand from the queue-consumption argument first). Engine agreement is bit-level:
my V1 census equals agentD's V1 census digit-for-digit (max S_win = 21 at J = 1539
with ρ* = 1534, K = kat[1534] = 681; window b-kind histogram {R: 2597, D: 603,
d: 201, M: 211} identical), and my tracer reproduces all 3280 certified table
entries exactly (attack 7).

## VERDICT SUMMARY

| # | Attack | Result |
|---|--------|--------|
| 1 | Identities I1–I4 | **CONFIRMED** (with writeup defect G1: I4's stated "⟺" is off by 4, conservative direction) |
| 2 | Window structure, ≤ 2 roots | **CONFIRMED** |
| 3 | Spine recursion + strict decrease | **CONFIRMED** numerically (with labeling defect G2: §2's "[Class-A]" hides PIN-content in the frontier branch) |
| 4 | Φ-profile ≥ 1664 on [3000, 10^6] | **CONFIRMED** (min = 1664 exactly at p = 3000) |
| 5 | Step arithmetic (EL / PIN routes) | **CONFIRMED** (slacks +496 / +60 reproduce; grid clean to 2^64) |
| 6 | Circularity audit | **CONFIRMED** (well-founded; every consumption < J) |
| 7 | Base table re-certification | **CONFIRMED** (3280/3280 full cross-check + 45 stratified run7 + j = 20000/30000) |
| 8 | Honesty of "PIN: no measured constant" | **CONFIRMED with flags** (PIN is disclosed as residual; phrasing flags G1/G2/F1–F5 below) |

**OVERALL: STANDS WITH GAPS** — every load-bearing claim survived independent
re-derivation and machine attack; the gaps found are documentation/labeling level
(G1, G2, F1–F5), not mathematical holes. No REFUTED item. The proof's conditional
inputs (EL or PIN) are disclosed, not hidden. If G1/G2 and the numeric errata are
fixed in the text, this reviewer would upgrade to PROOF STANDS (modulo the EL/PIN
disjunction itself, which is the project's declared residual, not a defect of
agentD's argument).

---

## A1. The identities I1–I4 — CONFIRMED (G1: the "⟺" in I4 is off by 4)

Hand re-derivation (queue accounting): every step consumes exactly 2 front entries;
a j-chain pushes exactly j entries (j−1 run + 1 seam) — both verified structurally
in my tracer at every chain. Consumed over the whole interlude = 2·(2dk) = 4dk =
run (J−1) + D_h (1) + T_2..T_{dp+1} (dp) + all pushes except the re-entry's ⟹ **I2**.
Pre-window (steps 0..2K−1, K = kat[ρ*]): consumes the run entries u·2^0..u·2^{ρ*−1}
(ρ* of them; the ρ*-fire at step index 2K consumes u·2^{ρ*}, u·2^{ρ*+1}) + all
pre-window pushes ⟹ Σ_pre = 4K − ρ*. Window (steps 2K..2dk−1, e of them): consumes
the fire pair (2) + run remainder (g−1) + D_h (1) + dp T's + window pushes (S_win)
⟹ **I3**: 2e = g+2+dp+S_win; and **I1**: dk = K + e/2.

From I2 with Σ_pre = 4K − ρ*:
**dk ≤ J ⟺ dp + S_win ≤ 3J − 4K + ρ*** (exact threshold — my form).
The report's stated equivalence, dp + S_win ≤ 4Φ(ρ*) + 3(J−ρ*) − 4 with Φ = ρ*−K,
equals 3J + ρ* − 4K − **4** — i.e. 4 tighter than the exact threshold. The report's
algebra line "4J − 4K − g − 2 − dp = 4Φ(ρ*) + 3(J−ρ*) − 4" is false as written
(LHS = 3J+ρ*−4K−dp−S_win, RHS = that − 4). **G1**: I4's "⟺" is incorrect; the
direction the induction uses (⇐, sufficiency) is valid, and the 4-unit shift is
conservative. Machine check (revD_1, J = 7..500): 0 failures of I1, I2, I3, of
"steps before the ρ*-fire = 2K", of K = kat[ρ*] (all 4451 pure sub-fires
machine-equal to the universal kat), of the directional equivalence with my
threshold, and of the report's tighter target being sufficient. Measured margin
min(threshold − (dp+S_win)) = 16, so the 4-unit distinction never bites in the
certified range. Spot values dk(14)=8, dk(19)=8, dk(20)=9 reproduce.

## A2. Window structure, ≤ 2 spawning roots — CONFIRMED

Operational definition (mine; the report never defines "root" explicitly): a window
chain whose b is NOT a pushed entry (b-kind 'R' host-run or 'D' = D_h). Structural
argument for ≤ 2: pushes prepend, so an original b has original c — run a pairs
with run a+1 (pure: excluded after ρ* by maximality, verified: 0 late pure fires)
or the last run entry pairs with D_h (the single possible mixed fire); D_h is one
entry consumed once (as b: the D-fire; as c: mixed fire or a pushed-b fire; or in
an even step). Census (revD_2, J = 7..2000, every window chain): root-count
histogram **{1 root: 788, 2 roots: 1206}**, max = 2, 0 failures; forest audit: every
window chain descends via push-tags from one of the roots. (b,c)-kind taxonomy:
('R','R') 1994 (= one per window: the ρ*-fire itself), ('D','T') 603 (D-fires),
('R','D') 603 (mixed fires), and pushed-b fires: ('M','M') 108, ('M','d') 103,
('d','R') 106, ('d','T') 63, ('d','D') 32. The 32 ('d','D') cases are D_h consumed
as c of a tree-1 chain — the window then has only ONE root; still consistent with
S_win = spine(j_last) + spine(j_e) (second term empty). Census matches the report:
max S_win = 21 at J = 1539 (with the j = 12 mixed fire present in the window:
window js = [1, 12, 1, 4, 3]), ≤ 5 window chains, max window param 12 (13 appears
only above J = 3000, confirmed in my 3000..3200 sweep), dp ∈ [2,6], g ≤ 6.
No third root exists anywhere. CONFIRMED.

## A3. Spine recursion + strict decrease — CONFIRMED numerically (G2: §2's [Class-A] label)

revD_3 (J = 7..500, all chains of every interlude): **0 violations** of strict
decrease along every forest edge (child j < pusher j) — a stronger statement than
the spine-level decrease; 0 window params ≥ J; every window tree sum ≤ spine(j_root)
(worst slack 8); μ(j) < j for all j in 7..399; my independently implemented spine
recursion (ΣU at last fire ≤ j−3, μ(j) = 1+⌊log2(3·kat(j−3)+6j+13)⌋, c_base = 4)
reproduces the reported table **{7:16, 8:41, 10:47, 16:56, 18:108, 26:122, 64:189,
96:256} exactly**; S_win(1539) = 21, S_win(3066) = 22 confirmed.

**G2 (labeling)**: the report's §2 carries the header "[Class-A]" and derives the
decrease from "EX (D-branch) + CL at sub-positions (sub-fire branch)". That covers
(a) replay sub-fires — exact, j = 1+v₂(3k+2), no margin needed — and (b) D-fires —
EX, proved. But the frontier branch (fires on the crossing leftover Y and on seams
d, the very branch μ(j) bounds) needs more: j = v₂(λ_x) at those mixed fires,
i.e. small-part domination / non-tie / λ_x ≠ 0 — margin-safety at the class sim,
which is PIN's content (run7 leaves = 1). The parenthetical "(δ ≤ 2j generously;
λ ≤ 6s+5 with s ≤ 2dk ≤ 3J+92 from I2 + CL)" bounds the SIZE of the small part but
does not justify j = v₂(small part). §4's route packaging is correct ("PIN ... from
which the structural window lemmas proved here give S_win ≤ 2·spine(...)"), so the
overall proof is unaffected on the PIN route; the §2 bullet should be labeled
[Class-A given PIN/margin-safety]. On the EL route the spine recursion is not used
at all.

## A4. Φ-profile — CONFIRMED

revD_4 (certified table 121..3200 + 5001..5200 + my tracer below 121; 302879 fires
to p = 10^6; max spike parameter encountered j = 20 ≤ 3200, so the profile is
unconditionally table-driven): Φ_min = 3 only at p = 4; min for p ≥ 26 is 16 (at
p = 26); **min on [3000, 10^6] = 1664, attained exactly at p = 3000** (the zone
threshold is the exact crossing position); min on [4958, 10^6] = 2750 (at p = 4958).
All four zone claims reproduce. Beyond 10^6 the counting bound takes over: with the
H1-majorant ε = 6 (harsher than the table's 3.1673) the post-spike bound is ≥ 2486
on every slab 2^9..2^1020, the t = 1019 seam is astronomically positive, and at the
block index s ≈ 2787..28000 corresponding to p ≈ 10^5..10^6 the bound is ≥ 24564,
so Φ ≥ 1664 for all positions > 10^6 as well (monotone in s, slope ≥ 5.25).

## A5. Step arithmetic — CONFIRMED

revD_5: case (a) target ≥ 6652 (6661 with ρ* ≤ J−3), case (b) target = 614
(4·3 + 3·202 − 4 at J = 3201, ρ* ≤ 2999); EL = 66 ≤ 611 ≤ 614 — passes. PIN route:
spine(16) = 56 at J = 3201 ⟹ S ≤ 112; with dp ≤ 6: 118 ≤ 614 (slack **+496**, as
reported); with the structural dp ≤ 2+g+2S+μ*: lhs = 2+200+336+16 = 554 vs target
3·200+14 = 614 (slack **+60 at J = 3201**, as reported); worst case-(a) structural
slack +5389 at J = 2^64; dense grid 3201..20000: 0 failures; sparse grid to 2^64:
0 failures. Case (a) also closes under the structural dp (the code only grid-checks
case (b); I checked (a) separately — it is trivial since the target's g-coefficient
3 dominates lhs's 1 and 4·1664−4 ≫ 3S+μ* for all J ≤ 2^64). Counting-bound slabs
recomputed and pass even at ε = 6 (worst post-spike bound 2486 at t = 9).
Errata: the report states the needed EL bound as "611" in the status/ASSEMBLY lines
but "614" in §4; 614 is correct for J > 3200, 611 is 3 conservative (F2, safe).

## A6. Circularity audit — CONFIRMED (the induction is well-founded)

Complete consumption list of the step at J > 3200, with my machine checks
(revD_6, grids 11..400 + sparse to 2^64):
- **Table**: only parameters ≤ 3200 < J. ✔
- **CL at positions ≤ ρ* ≤ J−3** (used for Φ(ρ*), kat ≤ ρ−3, agentA's counting
  bound, and EX's tie shape): agentA's CL consumes dk only at spike parameters
  ≤ 5+log₂(3q/16+2) with q ≤ J−3; checked < J−1 for all J ≥ 11, and each traversal
  drops the parameter by ≥ 2 (5+log₂(3q/16+2) ≤ q−2 for q ≥ 11). ✔
- **Sub-fire parameters**: j ≤ 1+log₂(3(J−6)+2) < J for J ≥ 12 (via kat ≤ ρ−3). ✔
- **Spine recursion**: ΣU and μ evaluate kat only at positions ≤ μ*(J)−3 and
  consume table entries only at parameters ≤ μ*(J); μ*(J) = 1+⌊log₂(18J+283)⌋ < J
  for all J ≥ 11; the μ-cascade bottoms at ≤ 6 (finite strictly-decreasing chain). ✔
- **j_e ≤ min(J−2, 1+log₂(3(K+δ)+1)) via EX**: EX is proved (agentB2); its one
  CL-dependent case (tie shape) sits at sub-positions ≤ J−3 — same scope as above;
  no H1 at ≥ J. ✔
- **dp(J) inside its own bound?** No: μ* is a primitive function of J. The
  λ-constant "s ≤ 2dk ≤ 3J+92" is derivable WITHOUT H1(J): from I2 + CL(<J) +
  the spine bound, 4dk ≤ J + 6 + 4(ρ*−3) + 2·spine(μ*) ≤ 5J + 2·spine(μ*), and
  spine(μ*) ≤ J/2 + 92 for all J ≥ 3201 (checked), so dk ≤ 1.25J + spine/2 ≤
  1.5J + 46 without circularity. ✔
- **Φ-profile walk to ρ***: max spike parameter on the way = 20 at p = 10^6
  (≪ J for any J > 3200). ✔
- For J ≤ 2.2·10^35 the CL calls sit inside agentA's unconditional scope A
  (table j ≤ 120 covers k ≤ 2.6·10^35): there the induction consumes no H1 at all
  — consistent with agentA's S₁ = (2^116−2)/3.
**The CL ⟺ H1-dk loop is one well-founded strong induction on J.** CONFIRMED.

## A7. Base table — CONFIRMED

- **Full independent cross-check** (revD_7b_fast, deque-based tracer): all
  **3280/3280** entries of agentD_table_cpt.json (j = 121..3200, contiguous) and
  agentD_table5100.json (5001..5200, contiguous) reproduce exactly (dk and dp),
  including dk(3200) = (1426, 6), dk(5100) = (2274, 4), dk(5200) = (2319, 3).
- **Margins**: min (j − dk) over the cpt table = **66, at j = 122**; dp ∈ [2,6]
  throughout; max dk/j = 0.4615 at j = 195 (see F5).
- **run7 stratified re-certification** (revD_7_basetable run7): 45 j values
  (every 100th of 121..3200 + boundaries 121/122/3199/3200 + 1539/3066 + small
  j 5..120): all match the table / dk ≤ j, **leaves = 1 on every branch** (no
  decision depends on the class member).
- **Far spot values**: run7 dk(20000) = 8922, dk(30000) = 13384 — both match the
  report, both with leaves = 1.
- Extra (revD_gap5200): the uncertified gap zone J = 3201..5000 censused with my
  tracer: dk ≤ J (min margin 1775), dp ≤ 6, g ≤ 6, max window param 11,
  max dp+S_win = 23; zones 3000..3200 and 5001..5200 similarly clean (max win
  param 13 resp. 8). No halt-like chains (u ≥ 3) anywhere.

## A8. Honesty of the PIN packaging — CONFIRMED with flags

The exact wording: Route PIN is introduced as "the class-sim margin/pinning law —
exactly the tree's own INV-L/PD family applied at the class-sim level (ASSEMBLY's
G4/G5; **empirically run7 leaves = 1 at every probed j ≤ 30000**)" (§ status);
§4's PIN paragraph states its reduction ("PD cases need only CL at sub-positions,
EX, trivial T-cases"), names its residual content ("the §9-review caveats on
sub-steps (C),(D) ... and agentC10's λ≠0-tail genericity lemma E5"), admits what
it is NOT ("not derivable from H1(<J) through the real walk"), and gives the
empirical basis ("leaves = 1 at every probed j ≤ 30000; agentB2's pinning calculus
closed all 12 first-exit shapes symbolically"). §6's residual statement is exact:
"for J > 3200 the proof consumes either PIN ... or EL". **PIN is a disclosed
residual hypothesis, not a hidden one.** My stratified leaves=1 re-checks (45 j +
20000/30000) support the empirical claim. Flags (phrasing-level, in the safe
direction but worth fixing):
1. "**No measured constant.** ∎" (§4) and "no measured exit constant at all" (§
   status) are scoped to exit constants; a fast reader may miss that the PIN route
   trades the EL constant for the PIN hypothesis, whose own support is measured to
   j = 30000. The adjacent sentences do say this; the "∎" placement invites
   over-quoting.
2. G2 (§2's "[Class-A]" on the Spines bullet) — the frontier branch of the
   decrease is PIN-conditional (see A3).
3. "Status: PROVED for all j" headline — correct only together with the paragraph's
   own input list (table + CL-profile + EL-or-PIN); §4's formal theorem statement
   does not restate the inputs (they live in the preamble/§6).

## Additional findings (errata, none load-bearing)

- **F1 = G1**: I4's "⟺" off by 4 (see A1). The used direction is valid; the false
  direction is never used; measured margins ≥ 16.
- **F2**: needed-EL quoted as both 611 and 614 (614 correct at J > 3200; 611
  conservative; the code's grid uses 614, its printed threshold 611).
- **F3**: "measured max 28 over J ≤ 5200" mis-attributes the quantity: my full
  sweep J = 7..5200 gives max(dp+S_win) = **25** (at J = 3066: dp = 3, S_win = 22);
  28 is the max of the window step count 2e = g+2+dp+S_win (attained at
  J ∈ {2690, 3066, 3838}); agentD_proof.py's docstring says 27. All ≪ 66 ≤ 611.
- **F4**: agentD_proof.py hygiene: the module docstring still describes the old
  5020/4958 architecture (code implements 3200/3000); load_table references
  agentD_table5000.json which does not exist (silently skipped — TAB = 5100 + cpt
  + phi() for j ≤ 63; harmless: nothing queries the missing 64..120 range except
  the ε fallback, which is then H1-conservative); V1 contains a dead
  `ok = (... or True)` expression immediately overwritten — harmless but alarming
  to read.
- **F5**: ASSEMBLY.md's intermediate paragraph claims "dk <= 0.4472 j throughout"
  for the 120→5200 extension — false pointwise (dk(195) = 90, ratio 0.4615). Only
  dk ≤ j (margin 66 at j = 122) is used by the proof; the paragraph is superseded
  by the final 3200-architecture section.
- **F6**: agentD's own suite re-runs all-green in ~10 s (V1–V5), and its V1 census
  output is bit-identical to my independent tracer's — two engines, same data.

## Bottom line

Every mathematical claim I attacked — the four identities (in their used
direction), the ≤ 2-root window decomposition, the strictly-decreasing parameter
cascade, the Φ-zone constants, both route closures at J = 3201 / 10^6 / 2^64, the
well-foundedness of the CL⟺H1 loop, and the certified base table — reproduced
under independent re-derivation with a separately written engine and with run7
re-certification. The two genuine writeup defects (G1: I4's equivalence off by 4;
G2: §2's [Class-A] label on a PIN-conditional decrease) and the numeric errata
(F2–F5) should be corrected in the text; none of them weakens the result. The
proof of H1-dk stands as: certified table (1..3200, +5001..5200) + CL-profile +
(EL measured constant **or** PIN), exactly as the report's §6 residual states.

**OVERALL: STANDS WITH GAPS (G1, G2, F1–F5 — all documentation-level; no
mathematical hole found; nothing REFUTED).**
