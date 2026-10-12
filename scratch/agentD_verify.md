# Agent D — independent verification report

Machine M = `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` (states A..F, symbols 0/1;
`---` = HALT). Tape infinite in both directions, all 0, head at cell 0, state A
(bbchallenge convention). All code written from scratch for this report:

* `D:\math_cc\scratch\agentD_a.py` — raw dict-tape TM, encoding, invariant, macro rules
* `D:\math_cc\scratch\agentD_b.py` — fast list-tape TM, macro iterator with step costs,
  closed-form top map, long runs
* `D:\math_cc\scratch\agentD_c.py` — symbolic affine executor (Lemma E)
* `D:\math_cc\scratch\agentD_d.py` — canonical-moment structural checks

Python 3.14, stdlib only. No other files in `D:\math_cc` were read or modified.

**Verdicts: A PASS · B PASS · C PASS · D: (ii) PASS, (i) FAIL in exactly one
w-independent family (the excursion's own start t=0, margin j−s′ = −2); for every
canonical odd-d moment with t ≥ 1 it holds with margin ≥ 3.**

Encoding used throughout: `(h; r1..rk)` = tape `0^∞ 1^h [0]_A 1^r1 0 1^r2 0 … 1^rk 0^∞`,
head on the bracketed cell, at a moment when A reads 0. Canonical form drops trailing
empty blocks (so rk ≥ 1; a double zero after block 1 encodes r2 = 0).

---

## Task A — raw simulation, claims (1) and (2): **PASS**

Blank-tape run, 500,000 TM steps, no halt, **4,586 A0-events** (event = configuration at
time t with state A reading 0; the t = 0 blank event has k = 0 and is outside the
encoding — the analysis proper starts at t = 5).

* First events (independently hand-derived anchors, all matched):
  `t=5 (0;3)`, `t=14 (1;1,0,1)`, `t=22 (0;0,0,1,2)`, `t=27 (0;4,2)`, `t=38 (1;4,1)`,
  `t=49 (2;4)`, `t=60 (3;2,0,1)`, `t=67 (4;0,0,2)`, `t=76 (0;9)`.
  **"blank tape reaches (0;3) at t=5": PASS.**
* **Invariant I** (k≥1, rk≥1, ri≥1 for i≥3, (r1≥2 or r2=0), k=1⇒r1≥2): held at **all
  4,584** in-orbit event configs. No encoding anomalies (no r_i = 0 for i ≥ 3 ever
  appears on the tape).
* **Macro rules R1–R5 + HALT row**: every one of the 4,584 consecutive event pairs
  matched **exactly one** row, the rule-predicted next config equalled the actual next
  event config, and the derived step costs matched every time delta:
  R1/R2/R3 cost `2·r1+3`, R4 cost `h+7`, R5 cost `h+5` (these costs are my own
  derivation from the transition dynamics; the HALT segment executes 8 transitions and
  halts on the 9th read).
  Rule histogram: R1 1262, R3 3145, R4 59, R5 69, R2 49.
* **Coverage/uniqueness beyond the orbit**: exhaustive box of **928** I-configs
  (h≤3, r1≤5, r2∈{0..3}, k≤4) and **400 random** I-configs (h≤12, entries ≤ 10, k≤6),
  each run on the raw TM: from every I-config the run reaches the next A0-event with the
  rule-predicted config, cost, and I-preserving output — **except** the HALT row
  (0; 1, 0, y+1, REST), which always halts. No I-config matched 0 or ≥ 2 rows.
* **Claim (1)**:
  * HALT happens iff F reads 0: PASS (the only undefined transition is F0 — definitional).
  * F is entered only from E0 (`1LF`): PASS (table fact) — every halt is launched by a
    leftward E→F step.
  * Every halt is preceded by a leftward E/F sweep: all 28 tested HALT-row configs
    (y = 0..6 × four REST shapes) halt after exactly **8 transitions** with state-read
    sequence `A,B,D,E,F,E,F,E,F`, the last four transitions being the left-moving
    `E,F,E,F` sweep. PASS.
  * Halting ⇔ an A0-config of the form (0; 1, 0, y+1, …): forward direction PASS (all
    such configs halt as above, independent of y and REST); backward direction holds on
    everything tested — from every other I-config the run reaches a further A0-event
    without halting (928 + 400 + 4,584 configs). No HALT-row config occurred in the
    500k-step orbit (consistent with no halt).
* **Caveats (wording, not substance)**: (a) R1's output can end in a trailing empty
  block (k=2, r2=0); the claim "outputs satisfy I" is true once the output is put in
  canonical form (drop the trailing empty block — same tape). This normalization is
  needed for R2 to fire next; it occurs in-orbit (e.g. (1;4,1) → (2;4,0) ≡ (2;4) at
  t=49). (b) The orbit is identical under the one-way vs two-way infinite tape
  convention (the tape support stays connected; parse hygiene checks passed).

## Task B — top map, three implementations cross-checked: **PASS**

Implementations: raw TM (fast list tape; self-tested step-by-step against the
independent dict-tape TM over 200k steps), macro-rule iterator (R1–R5 + costs,
canonicalization), closed-form T of claim (3) (missing entries = 0).

* **Formula vs macro**: **3,000 top steps** (L_0 … L_3000): lists identical, no halt.
  Macro times: t_0=5, t_1=27, t_2=76, t_3=169, t_4=230, t_5=432, …, **t_3000 =
  36,507,403,950**.
* **Raw vs macro** (lists **and** TM times): identical on **570 top steps**
  (L_0 … L_569), i.e. through TM time **248,738,232** (250,000,000 raw steps, 87 s).
  Raw simulation of all 3,000 top steps would need ≈ 3.7×10^10 steps (t_n grows ≈
  cubic), which is infeasible; the bridge is the per-event cost model, which the raw
  run re-verifies on every event in coverage (~2.3 M events), on top of Task A's
  per-event verification.
* **sum(L_n) = 3n+3 from L_0=(3)**: 0 violations over n = 0..3000 (macro lists) and
  over n = 0..65,536 (formula lists).
* **Halting criterion** "HALT ⇔ some top step has A odd and A+2b+3 = 2^k":
  * One-step form (T halts on L ⇔ A odd and A+2b+3 = 2^k): **270,900** synthetic lists
    (A odd ≤ 601, b ≤ 301, three tail shapes): PASS.
  * Over the whole n < 2^16 orbit the criterion never fires and T never halts
    (0 and 0).
  * Orbit-level constructive checks (macro-with-costs vs raw TM, **exact total step
    agreement**, both halt/non-halt): e.g. (0;15,1) halts after **16,220** steps at top
    config (0;1,0,1,4,8,16,31) (A+2b+3 = 4); (0;21,5) after 119,114; (0;15,1015) after
    733,711; one-step cases (0;7,11)→413, (0;9,506)→185,956, etc. The halting top
    config is always exactly the HALT-row shape. Non-halting spot checks ((0;9),
    (0;3), (0;33), (0;21)) agree (2 M steps each). PASS.
* **Excursion-entry formula**: singleton steps with n < 2^16: **29,293** found (22,255
  with n even; first ones 0,2,4,6,**9**,10,12,14,**17**,18,20,22 — odd-n singletons do
  occur, exactly when ell(v) is odd). **Every** one verified: n even ⇒ L_{n+1} =
  (3w+1, 3w, 6w, …, 3w·2^{v−2}, 3w·2^{v−1}−1) with n+2 = 2^v·w, w odd (v ≥ 1);
  (n odd ⇒ L_{n+1} = (3n+6), my extension — the claim only covers even n). PASS.

## Task C — symbolic executor, Lemma E(v): **PASS**

Entries are affine forms a·u+b (u ≥ 0, w = 2u+1). Parity decided only if a even;
halving only if both even; m ≥ 3 only if uniform (a = 0 both ways, or a > 0 ∧ b ≥ 3);
m = 1 only if uniform (a = 0, or uniformly even). Any non-uniform decision raises.

* v = 1..100, **all odd w simultaneously**: every excursion reached a singleton; **no
  HALT branch ever occurred**; **every decision was uniform** — counts: 7,805 parity,
  6,980 halvings, 1,937 “m ≥ 3”, 1,553 “m = 1”; 0 exceptions.
* ell(v) independent of w: concrete cross-check w ∈ {1, 3, 5, 7, 999, 123456789} gave
  identical ell(v) **and** identical full list sequences (symbolic forms evaluated at
  u = (w−1)/2 match the integer run step by step).
* ell(1..30) = 1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14, 15, 15, 16,
  16, 18, 18, 21, 20, 20, 22, 25, 25, 26. **ell(1..20) matches claim (4) exactly.**
* Bonus: concrete w = 1 for v = 101..2000 (full range of claim (4)): all reach a
  singleton, no halt. Max ell(v) for v ≤ 100 is 86.

## Task D — canonical-moment structural fact: **(ii) PASS; (i) FAIL at t = 0 only,
PASS with margin ≥ 3 for all t ≥ 1**

Interpretation used (stated because the claim's wording is compressed): moments = top
steps t = 0,1,2,… of the T-iteration starting at E(w,v); a moment is canonical if
entry 2 equals H = 3w·2^j exactly, entries 2..r+1 keep doubling (H, 2H, …, 2^{r−1}H),
d = entry1 − H; s′ = v2(d+3); "middle phase" = list length ≥ 5 (≥ 3 entries beyond the
first two). Checked v = 1..120 symbolically (all odd w at once) and concretely for
w ∈ {1,3,5,7}; the two agree everywhere; 0 non-uniform decisions; max excursion length
ell(120) = 106; 2,938 canonical moments recorded.

* **(ii) d = 3t+1: PASS** — at **all** 2,938 canonical moments, d is the *constant*
  affine form 3t+1 (slope 0, i.e. independent of w), with t the raw top-step index
  since excursion start. Note: "t counts canonical steps" cannot mean "counts only the
  canonical moments" — under that reading d = 3t+1 already fails at the 4th canonical
  moment (t = 4 has d = 13 ≠ 3·3+1).
* **(i) j > s′ during the middle phase at odd-d moments**: 2,094 odd-d middle-phase
  canonical moments checked. **Violations: exactly the excursion's first moment t = 0**
  — for **every v ≥ 4** (117 values), E(w,v) itself is canonical with H = 3w (j = 0),
  d = 1 (odd), s′ = v2(4) = 2, list length v+1 ≥ 5 ⇒ margin **j − s′ = −2**. This is
  w-independent (symbolic d = (0,1)) and occurs for concrete w = 1,3,5,7 as well.
  Under the alternative reading of "middle phase" (geometric run itself long, r ≥ 5)
  t = 0 still violates for v ≥ 6 — the conclusion is reading-independent.
* **Margins excluding t = 0**: minimum **3**, attained at t = 2 (j = 4, s′ = 1) and
  t = 4 (j = 7, s′ = 4); they grow roughly linearly in t. Min margin per t:
  t=2:3, t=4:3, t=8:9, t=10:12, t=12:13, t=16:19, t=18:22, t=20:20, t=26:30, t=28:31,
  t=32:37, t=34:40, t=36:40, t=40:46, … At the "critical" t where 3t+4 = 2^k (s′
  largest): t=4 → margin 3; t=20 → margin 20 (j=26, s′=6); t=84 → margin 91 (j=99,
  s′=8). j is nondecreasing along every excursion's canonical moments.
  Distinct margins observed: −2, 3, 9, 12, 13, 19, 20, 22, 30, 31, 37, 40, 46, 49, 50,
  56, 58, 59, …
* Example (v = 120, ell = 106), canonical (t, len, r, j, d, s′, margin):
  (0,121,119,0,1,2,−2), (1,119,117,2,4,0,2), (2,117,115,4,7,1,3), (4,114,112,7,13,4,3),
  (7,112,110,9,22,0,9), (8,110,108,11,25,2,9), (10,108,106,13,31,1,12),
  (12,105,103,16,37,3,13), …, (84,22,20,99,253,8,91), …, (103,4,2,117,310,0,117).
  (Even-d moments shown for completeness; (i) only constrains odd d, i.e. even t.)

### Bottom line for downstream use
Everything in claims (1)–(4) checks out (with the two harmless wording caveats in Task
A). The new structural fact needs one amendment: inside the orbit of E(w,v),
d = 3t+1 holds at every canonical moment, and j > s′ = v2(3t+4) holds at every
canonical odd-d moment **with t ≥ 1** (margin ≥ 3, growing ≈ linearly); the claim as
literally worded fails only at the excursion's initial moment t = 0, where j = 0 < 2 =
v2(1+3) for every v ≥ 4 and every odd w.
