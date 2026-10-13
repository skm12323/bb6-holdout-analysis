# ADVERSARY-3 review — the coordinator layer (fast_walker, Lemma K, INV-L/PD measurements, PROOF.md §7) and the ASSEMBLY logic

Reviewer: ADVERSARY-3 (2026-10-13). Scope per instruction: coordinator's own artifacts +
final assembly; agentA/B2/C10/D contents cited only as one-line claims from ASSEMBLY.md.
Scripts (all in work_r10/, stdlib only, footprint << 30 MB): `revC_cadd.py`,
`revC_walk_xcheck.py`, `revC_scope.py`, `revC_lemmaK.py`, `revC_cases.py`, `revC_pd.py`.
Read-only inputs: work_r10/{fast_walker.py, check_invariants.py, residue_inv.py, PROOF.md,
ASSEMBLY.md}, work_g6/{PROOF_G6.md, verify_g6.py}, work_r1/RULES.md.

Verdicts per audit item: CONFIRMED / GAP / REFUTED. Summary verdict at the end.

---

## 1. fast_walker soundness

### 1(a) residue arithmetic of `cadd` — CONFIRMED (with one precise qualification)

Re-derived from scratch and fuzz-tested (300,000 random pairs, operands up to 320 bits —
wider than B = 192 — plus adversarial cases; `revC_cadd.py`):

- **Unequal valuations, delta = |v1−v2| < B**: exact in BOTH components. The odd part of
  the sum is m_small + 2^delta·m_big (odd + even = odd), so the new valuation is exactly
  min(v1,v2), and its residue mod 2^B is (r_small + (r_big << delta)) mod 2^B — because
  2^delta·m_big mod 2^B = 2^delta·(m_big mod 2^{B−delta}) and (r_big << delta) mod 2^B
  reproduces exactly that. 0 failures in 3·10^5 fuzz cases.
- **delta >= B**: the code returns (v_small, r_small) — exact, since 2^delta·m_big ≡ 0
  (mod 2^B). 0 failures in 2·10^4 cases.
- **Equal valuations (tie)**: the returned VALUATION v1+t is exact whenever t < B (the
  residues determine m1+m2 mod 2^B, hence v2(m1+m2) for any value < B); the code raises
  `Deep` when the residue-visible t >= B−16 — conservative and consistent. BUT the
  returned RESIDUE is exact only **mod 2^(B−t)**: the top t bits can be wrong
  (m1+m2 = s + 2^B·q ⟹ (m1+m2)>>t = (s>>t) + 2^{B−t}·q). Concrete demonstration:
  m1 = 3·2^192+3, m2 = 5, v=7: code returns (10, 1); true odd part mod 2^192 =
  2353913150…3312942337. They agree mod 2^189 = 2^(B−t), not mod 2^192.
  So PROOF.md §1's soundness statement — "Addition is exact except when … Deep" — is
  **not the correct justification** (tie residues are not exact mod 2^B in general).

### 1(b) silent precision-loss path — RESOLVED, in the coordinator's favor (and stronger than claimed)

The only way the top-bit tie loss could corrupt a decision is a later tie whose true
depth t' >= the running correctness width (parities and j = v2(λ) only ever read LOW
bits; λ is exact big-int throughout). The Deep guard alone does not exclude this.
Instrumented run (`revC_scope.py`) tracking exactness/width per value:

- To i = 2·10^6 AND to i = 10^8: **all 111,516,950 ties had exactly-known operands;
  zero ties with inexact operands; no live value was ever inexact.** The walker's
  arithmetic is bit-exact on the entire measured range.
- Structural reason (which the coordinator never stated and which closes the question
  generally): the mass identity Σc = 2^i gives every live odd part m = c/2^{v2(c)} ≤ 2^Δ
  and all live valuations lie in [i−Δ, i], so |v1−v2| ≤ Δ; whenever **Δ ≤ 95**, every
  operand and every result fits in 192 bits, the arithmetic is bit-exact, and Deep
  (t ≥ 176) is unreachable. The walker tracks Δ itself (maxdef = 28 at i = 10^8), so
  every run is self-certifying. The measured law Δ ≈ log2 i + 3.42 stays ≤ 95 until
  i ~ 2^91.
- Cross-check upgraded beyond the coordinator's: lockstep exact-vs-fast to **i = 3·10^5
  (they did 2·10^5, level-fires only)** comparing EVERY step's decision, i, s, chain j,
  and EVERY live v2(c): identical; mass identities (Σc = 2^i, Σλ = 3s+1) and positivity
  asserted at all 267,645 states (`revC_walk_xcheck.py`).

### 1(c) parity fix `cpar` — CONFIRMED

v >= 1 ⟺ c even holds for every c = 2^v·(odd) with c > 0; c = 0 never occurs (positivity
+ mass identity asserted per state in the lockstep run; originals are 2^a, all operations
are positive combinations, u = c_x/2^j > 0, D = c_c + c_A/2 > 0). The stored residue is
odd in every branch (odd + shifted-even), so `r & 1` is exact whenever v = 0. Note the
code checks A[0] >= 1 before computing tD = cadd(…, (A[0]−1, …)) — no negative shift.

### 1(d) three-way walk at U = 3 — CONFIRMED

`revC_walk_xcheck.py` runs four independent walks to i = 20,000: (1) fast_walker,
(2) its exact_walker, (3) work_g6 `F_walk` (the G6 base verifier), (4) the REAL audited
top map of work_r1 §5 from (U+1; U, 2U, 4U, …) at U = 3. Result: 17,841 top steps,
6,690 chains, **no halt (all u ≥ 3)**; the real map agrees with the exact F-walk
state-by-state (parity, pointer, every chain j, level flags); all four level-fire
streams identical (6,056 fires — exactly V6's numbers, as PROOF §1 claims). §1's base
validation claim and the "60,575 level fires at i ≤ 2·10^5" claim both reproduce
exactly; §2's full record table (Δ = 8…28 at i = 28…25,074,251), max s/i = 0.8928,
max stall 21, max level gap 22 all reproduce exactly at 10^8 (my run: 79–97 s on this
machine — §1's "≈ 40 min" is environment-specific and harmless).

**Item-1 verdict: CONFIRMED.** The tool is sound on the entire measured range; the
documented justification ("exact except Deep") is flawed but replaceable by the Δ ≤ 95
bit-exactness certificate above. GAP-in-documentation only.

---

## 2. Lemma K — CONFIRMED (lower bound + class arithmetic PROVED-grade; first-occurrence is measured, as §9 says)

Re-derived independently (`revC_lemmaK.py`):

- j = 1 + v2(3k+2) (I(ρ), g6 §5.4) ⟹ j ≥ 5 ⟺ v2(3k+2) ≥ 4 ⟺ k ≡ 10 (mod 16)
  (14·3^{−1} = 154 ≡ 10 mod 16); k = 16s+10 ⟹ 3k+2 = 16(3s+2) ⟹ j = 5 + v2(3s+2).
  Verified exhaustively. Lower bound: v2(3s+2) = j−5 ⟹ s ≥ (2^{j−5}−2)/3 ⟹
  k ≥ (2^{j−1}−2)/3 (16·(2^{j−5}−2)/3 + 10 = (2^{j−1}−2)/3 exactly).
- Even j ≥ 6: j−5 odd ⟹ 2^{j−5} ≡ 2 (mod 3) ⟹ s0 = (2^{j−5}−2)/3 integral with
  3s0+2 = 2^{j−5} (v2 exactly j−5) ⟹ the bound is attained by the class, k0 = (2^{j−1}−2)/3.
  k0-list 10, 42, 170, 682, 2730, 10922, 43690, 174762, 699050, 2796202, 11184810 —
  matches PROOF §3 exactly. (Odd j: floor bound not attained, e.g. j=7 min class k = 106.)
- First occurrences verified against the **certified table's walk** (work_g6 phi classes):
  8.15M fires traversed (k to 1.2·10^7, p to 2.69·10^7); every spike has k ≡ 10 mod 16,
  j = 5+v2(3s+2), k ≥ (2^{j−1}−2)/3; first occurrence of EVERY even j = 6..26 is exactly
  k0; the table-walk (p,k,j) stream is identical to my independent walker to i = 4·10^5;
  first-j i-positions 26, 99, 388, 1537, 6130, 24494, 97955, 391794, 1567150, 6268571,
  25074249 match PROOF §2's list exactly (my walker, to 10^8).
- **The corollary "j ≤ log2 k + 2" is FALSE** — fails at every first occurrence
  (e.g. (k,j) = (10,6): log2 10 + 2 = 5.32 < 6). Correct form: j ≤ log2 k + 3
  (equivalently k ≥ 2^{j−3}). PROOF §9 already records this — **but ASSEMBLY.md (the
  FINAL version) still defines K as "k ≥ (2^{j−1}−2)/3 ⟹ j ≤ log₂k+2" and G3 uses
  "j* ≤ log₂k*+2 [K, PROVED]": an uncorrected FALSE constant in the assembly.**
  Non-fatal: with +3, G3's chain gives Δ ≤ log2 k* + 5 ≤ max(log2 i, 2 log2 i) + 5,
  still < ⌊log2 i⌋² for i ≥ 64 (verified numerically).
- Restriction to level fires: needed and confirmed — exit (D-fire) spikes with j = 5
  exist, first exactly at (i,s) = (6132, 5471) as §9 states. Note a small data error in
  §9's text: "exit chains also reach j ≥ 5, up to 15" — on the universal walk to i = 10^8
  the non-level chains reach only j = 5 (D-fires; 1,584,899 of them) and j = 4
  (M-readers); "15" presumably refers to per-class Φ_m replays (g6 V3 reports exit
  D-fire j up to 11 for m < 3000), not the universal walk. Immaterial to the tree.

**Item-2 verdict: CONFIRMED** (proved content: class arithmetic + lower bound; measured
content: first-occurrence exactness — correctly classified by §9, mis-constant in ASSEMBLY).

---

## 3. PROOF.md §7 case analysis (`revC_cases.py`, exact walk to i = 1.5·10^5)

- **(E) CONFIRMED.** v2(sum) ≥ min at all 83,637 even steps (ties at every one of them —
  they only SHRINK δ); δ_new ≤ max(δ inputs) with worst slack −2. Direction as used.
- **(P) CONFIRMED.** Definitional in F's read rule (g6 §5.1: originals read only after P
  is exhausted) and identically implemented in fast_walker / g6 F_walk / my walkers;
  when the pointer advances (len(P) ≤ 1) the survivors are exactly the fresh pushes.
- **(C) CONFIRMED as a pure-stretch identity — but structurally thin.** The identity
  head = c_u·4^{k−1} before absorbing pair #k of a stretch holds EXACTLY wherever
  claimed (stretches starting at t = 0, i.e. immediately after the producing chain).
  Measured: stretch lengths are ALWAYS ≤ 2 pairs {1: 14,767, 2: 4,186} — a chain
  interrupts after at most two pair absorptions (this is forced by λ-parity:
  λ_A = 4λ_u+4 then 16λ_u+7, odd) — and 13 mid-run "orphan" same-producer pairs at
  i ≤ 6·10^4 where the identity does NOT apply. So the "+O(1)" in δ_A = J_enc − t + O(1)
  accumulates across mandatory interruptions; that bookkeeping is exactly the unproved
  residue of A1 (§9 flags it; ASSEMBLY G4 claims it proved — see item 5/6).
- **(Ch) CONFIRMED as inequality.** v2(c_x) = min(v_A, v_b+1) exactly at 100% of 50,182
  chains (0 lifted ties); post-chain slack δ(u) − J(u) ≤ 0 (worst 0).
- **(D) GAP — now precisely located.** The census: at ALL 50,182 chains the D-construction
  falls in the sub-case **v_c > v_A − 1**; the tie sub-case v_c = v_A − 1 (the one §7(D)'s
  one-line proof addresses: odd+odd = even ⟹ v2(D) ≥ min+1) NEVER occurs, nor does
  v_c < v_A − 1. In the occurring sub-case v2(D) = v_A − 1 and the needed bound is
  δ_A + 1 ≤ J_D + 2, i.e. head slack ≤ +1 (INV-L alone gives ≤ +2). Measured worst
  δ_A − J_D = −1 (margin 2), worst slack(D) = −2: the invariant holds empirically with
  room, but the §7 one-liner proves the vacuous case. This sharpens §9's objection;
  ASSEMBLY G4's "[all steps PROVED]" is wrong for (D).
- **(L) CONFIRMED.** δ_x = 0 and δ(u) = j at 100% of level fires (45,431 at 1.5·10^5;
  90,863 at 3·10^5 in the lockstep with I(ρ) asserts: c_x = 3·2^ρ, λ_x = 3s+4, s even).
  Re-derivation from g6 §5.3/5.4 (mass identity ⟹ c_A = 2^ρ at a fire) checks out.

---

## 4. PD measurements — CONFIRMED, and convention-robust

- `check_invariants.py` re-run at N = 200,000 (66,910 chains) and N = 500,000 (167,274
  chains): all four checks pass — worst lineage slack 2 (at the start), 0 post-chain
  violations, 0 PD violations, 0 level fires with δ_x ≠ 0. (§7's "100,367 chains /
  300,000 indices" reproduces exactly.)
- **t-convention robustness**: the code's D-position convention (tDp = producer j for
  M-producers, ρ+2 for E, b5+2 for D — generous) vs the strictest natural convention
  (tD = j_prod − 1): PD (t ≥ j at every chain) has **0 violations under BOTH**, min
  margins: overall 3 (E chain); at D-fires, 62 (code) / **1 (strict)** — the strict worst
  case is exactly the EX-tight event (i=65, s=55, j_D = 3 = J−2, t_D = J−1). So the
  t ≥ j claim survives the worst convention; PROOF §7's specific constant "margin ≥ 2
  everywhere" is a statement under its own convention (true there), not
  convention-invariant — immaterial.
- Reconciled §7's spike census: 2,794 = 2,788 level spikes + 6 exit D-spikes (j=5)
  below 2·10^5; total 5,582 spikes matches "5582/5582".

**Item-4 verdict: CONFIRMED** (all Class-B, as labeled).

---

## 5. ASSEMBLY logic (tree G0–G8, hypotheses, scopes)

**(a) Theorem R's hypotheses — COMPLETE in the tree.** g6 §5.5 needs exactly: the
Class-B base i ≤ 20,000 (V6) + (M1') + (M2') for i > 20,000; (Return) is explicitly not
needed for non-halting; Progress is proved inside via (M2'). ASSEMBLY G2 lists all
three ✓. I re-verified the closure arithmetic: f(i) = i − log2(i)² − log2(6i²+5)
increasing (integers to 10^6 + grid to 10^18) with f(20000) ≈ 19,765 > 0, and
i − ⌊log2 i⌋² ≥ 1 for i > 20,000. Minor phrasing gap: the FINAL theorem block conditions
on "the audited base (work_r1)" — the g6 V6 base (i ≤ 20,000, Class-B) is a separate
artifact that the block should name; the tree itself carries it.

**(b) The (M2') node — logic sound, input weaker than CL, one constant mis-cited.**
Prop 1 (Class-A; its "everything consumed" hypothesis is automatic since a level fire
requires P = ∅) gives s = 2dk between fires and steps-before-fire = 2k_ρ, so
s ≤ 2k_b + e. For (M2') = s ≤ i² the k-input is much WEAKER than CL: any k_ρ ≤ i²/4
suffices; CL (p ≥ k+3, i.e. k/p ≤ 1 − 3/p) gives s ≤ 2i + C < i² for i ≥ 6 ✓ (my table
walk: p ≥ k+3 with 0 violations over 8.15M fires to p = 2.7·10^7). The 0.4465 constant
is needed only for the sharper s ≤ 0.893i (measured). Constant-provenance slip: the
node's "+16" is EG's excursion constant e(v) ≤ 16; the relevant walk quantity is the
level-fire gap, measured max **22** to 10^8 (I reproduce 22). Any fixed constant (or the
structural e-law cited from EG: e ≤ max_j + 1 ≤ log2(6s+5)+1, which closes
s ≤ 2c·i + O(log s) with no constant) suffices — non-fatal, but the citation mixes two
different "e"s and the gap bound as used is Class-B.

**(c) PIN is stated as a hypothesis — CONFIRMED.** The final section: "The single
non-self-contained leaf is EL (measured) or PIN (… verified to j = 30000 with
leaves = 1, structural spine recursion closing the rest)"; the THEOREM block conditions
on "EITHER (EL) … OR (PIN) …". So PIN is not claimed as proved. The slogan "on this
route NO measured constant remains" is narrowly true (no free numeric constant) but PIN
itself is a finitely-verified lemma — adequately disclosed, mildly promotional.

**(d) Missing edges — none of substance.**
- The walker computes everything directly: fast_walker.py contains no (dk,dp) table and
  no dependence on any external data (verified by construction and by the four-way
  agreement with the real top map).
- Table-scope question: which j occur below the CL Phi-profile's p = 10^6? My own runs:
  level j ∈ {1..20} (j=20 first at p = 391,794; j=21 first at p = 3,917,860); D-fires
  j ≤ 5; M-readers j ≤ 4 — and even at i = 10^8 the all-chain maximum is j = 26 (a level
  fire). All wildly inside the certified tables (120 / 3200 / 5200). Table totality is a
  non-issue at every scale used.
- No dependence on the R9-era "ell = 2k_b + e" formula survives (G6's formula comes from
  Prop 1). One STALE CITATION: the "Proposed closure (coordinator)" paragraph cites
  "nested replays restart the sequence, parameters strictly decrease — R9 audit, proved";
  R9 was downgraded (PROOF §9 calls the same citation void). Superseded by agentD's
  actual proof, but the stale line should be struck (PROOF §4's analogous line is
  already covered by §9's erratum).

---

## 6. Overstatement sweep (ASSEMBLY.md / PROOF.md)

1. **ASSEMBLY K-definition and G3**: "⟹ j ≤ log₂k+2" / "j* ≤ log₂k*+2 [K, PROVED]" —
   FALSE constant (correct: +3), refuted at (k,j) = (10,6); §9 recorded the correction;
   the final ASSEMBLY never applied it. ERROR (non-fatal; G3's conclusion survives, §5b).
2. **ASSEMBLY G4**: "INV-L ⟸ PD + the §7 case analysis [all steps PROVED: (E),(P),(C),
   (Ch),(D),(L) one-liners/identities]" — contradicts §9 and my measurements: (D)'s
   one-liner proves a sub-case that never occurs (the occurring sub-case needs head
   slack ≤ +1, measured only); (C)'s "+O(1)" is not derived and the pure stretches it
   covers are ≤ 2 pairs with mandatory interruptions; "A1 ⟺ position-dominance" is
   unproved. OVERSTATEMENT — the strongest one in the assembly.
3. **ASSEMBLY G3**: "architecture proved except PD" — under-states (also the (D)
   sub-case and (C)'s constants). Milder overstatement.
4. **ASSEMBLY G6**: "+16" (see 5b) and the node label "PROVED modulo CL" (also needs a
   gap/e bound — measured 22, or the structural e-law). Minor.
5. **ASSEMBLY G7**: "each chain's pushed material is consumed within 2j+O(1) steps …
   PROVED given F-defined" — the 2j+O(1) consumption mechanism is asserted nowhere-proved;
   the conclusion (i → ∞) is nevertheless proved via Theorem R's Progress using (M2').
   Overstated mechanism, sound conclusion.
6. **PROOF §1**: "Addition is exact except when … Deep" — wrong justification (1a);
   the true statement is stronger in-regime (bit-exactness for Δ ≤ 95, my certificate).
   Also "(same (i,s) trace)" — the shipped cross-check compares only the level-fire
   stream; the full-trace claim is true (my lockstep) but not by the shipped code.
7. **PROOF §3**: states the first-occurrence-exactness inside the Lemma (it is
   measured); §9 is the erratum; §3 text uncorrected. Same for the false corollary.
8. **§9's own record**: "exit chains … up to 15" not reproducible on the universal walk
   (max 5 at 10^8); minor data error in the review record, immaterial.
9. "The complete proof tree is now proved modulo ONE measured constant" — acceptable
   with its own trailing disclosure ("plus the tree's own documented inputs…"), since
   EL is indeed the only free numeric constant on that route; see 5(c) for the PIN-route
   phrasing.

Everything else I checked reproduces exactly: §1's base numbers (17,841/6,690/6,056;
60,575 at 2·10^5), §2's full record table and the Δ = log2 i + 3.42 law, max s/i 0.8928,
stall 21, gap 22, first-j positions to j = 26, §7's INV-L/PD counts (100,367 chains) and
the spike census (5,582 = 2,788 level + 6 exit; halving law exact for j ≥ 6).

---

## OVERALL VERDICT

**Coordinator artifact layer (fast_walker, Lemma K, INV-L/PD measurements, PROOF §7
data): SOUND.** Every number reproduces; the walker's arithmetic is bit-exact on the
entire measured range (proved via the Δ ≤ 95 certificate, verified op-by-op to 10^8);
Lemma K's proved content is correct; the §7 case identities hold wherever claimed.
One documentation gap (the "exact except Deep" justification) and one §9 data slip
("up to 15").

**ASSEMBLY layer: SOUND tree topology with GAPS and ERRORS in its prose** — no missing
edge found (Theorem R's hypotheses correctly instantiated; table scopes fine; walker
table-free), but:

- ERRORS: (i) K's "j ≤ log₂k+2" survives in the final ASSEMBLY (G3 and the K
  definition) although refuted — must read +3; (ii) G4's "all steps PROVED" contradicts
  §9 and measurement ((D) proves the vacuous sub-case; (C)'s O(1) un-derived; A1⟺PD
  unproved); (iii) G6's "+16" conflates the endgame constant with the level-gap
  constant (22 measured).
- GAPS: G3/G4's remaining unproved bookkeeping is larger than "except PD" (the (D)
  sub-case head-slack ≤ +1 and the interrupted-interlude accounting are measured-only);
  G7's consumption mechanism asserted; final theorem block should name the g6 Class-B
  base explicitly; stale "R9 audit, proved" citation.

None of these errors changes any theorem statement's truth conditions: the final
THEOREM block's conditions (audited base + EL or PIN + the tree's recorded inputs)
remain correctly stated, and each error is repairable by a constant edit or by
re-pointing G4 at §9's corrected architecture. The assembly's substance — the
dependency topology and the hypothesis accounting — survives audit.
