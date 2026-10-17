# Endgame lemmas E1–E5 (revised after three-way review)

2026-10-17. Revised statement of Lemmas E1–E5 from `work_r10/agentC10_report.md` §1. That report claimed them as Class-A but they were never individually reviewed. This file restates them in the form that survived a three-way review (§7) and is meant to be cited instead of the original. The original report is unchanged.

Background (accepted): `work_r1/RULES.md` (top map; missing entries read as 0), `work_r4/PROOF.md` (excursions), `work_g6/PROOF_G6.md` §5 (pair map F, §5.2 simulation, D5), `work_m/PROOF_M.md` (crossing types, deficit ε).

## 0. Setting and conventions

Fix v ≥ 1 and odd U = 3w. The excursion is E(w,v) = (U+1; U, 2U, …, 2^{v−2}U, 2^{v−1}U − 1). Run the pair map of G6 §5.1, where a pair (c,λ) stands for cU+λ, with the following suffix:
- originals E_a = (2^a, 0) for a ≤ v−2;
- the **defect** pair (2^{v−1}, −1) at index v−1;
- after the defect, no further originals. When the queue holds exactly one entry and a second entry must be read, the **zero pair** (0,0) is used (RULES §5: missing entries read as 0).

The steps up to the first read of index v−1 coincide with F (D5, queue determinism). The state just before that read is F's crossing X(v−1). The **endgame** is the part from that state on.

Write s for the step count from the excursion start (the same s as in F), and n := v−1. For a pair with c > 0 define the **deficit** d := n − v₂(c). The zero pair has d = −∞. Deficits may become negative after the defect is read (e.g. d = −1 at c = 2^v); this is harmless.

Define **D_cross** := the maximum deficit over the head, the pending list, and the unread entries at X(n). By the PROOF_M type analysis of X(n) (types a, b, c), D_cross = ε(n) = n − v₂(c_A).

A **defined prefix** is a prefix of steps at whose chains S1 (v₂(λ_x) < v₂(c_x)) and S2 (c_A even) hold.

## 1. E1 — boundary simulation [A]

**Lemma E1.** Fix v and odd U. If S1 and S2 hold at every chain of steps 0..s−1 of the pair run, then for every odd U the real top-map orbit of E(w,v) agrees through step s with the image of the pair run under (c,λ) ↦ cU+λ.

*Proof.* Induction on steps, as in G6 §5.2:
- parity of cU+λ is (c+λ) mod 2 for odd U;
- even steps are the same linear update;
- at a chain, S1 gives v₂(c_x U + λ_x) = v₂(λ_x) = j for every odd U; the sign of λ_x does not matter modulo powers of 2; the successor is the audited closed form;
- the defect evaluates to 2^{v−1}U − 1, and the zero pair to 0.

The zero pair occurs only as the second read entry c. Then D = (c_A/2, (λ_A+1)/2), which matches the real "missing = 0" rule. The defect is only ever read as b or as c, never as the head.

For v = 1, 2 the endgame starts at the start state, and its single step is even (resulting heads (2,3) and (4,3)). So the only state with c_A odd is the start state, which is not a chain; elsewhere S2 is a hypothesis of the defined prefix (and is supplied by E5 in the endgame). ∎

## 2. E2 — signs [A]

**Lemma E2.** Along a defined prefix:
- c_A ≥ 1, and every stored entry has c > 0 (only the read-in zero fill has c = 0);
- every λ is ≥ 0, except the unread defect (−1);
- the head has λ_A ≥ 0, and λ_A is odd at chains;
- at every chain λ_x = λ_A + 2λ_b + 3 ≥ 2, in particular λ_x > 0;
- the run base has λ_u = λ_x/2^j odd and ≥ 1; the pushed entries u·2^t (0 ≤ t ≤ j−2) have λ = λ_u·2^t ≥ 1 (odd only for t = 0);
- every D has λ_D = λ_c + (λ_A+1)/2 ≥ 0, and λ_D = 0 is reachable.

*Proof.* Induction over steps. The F prefix has all λ ≥ 0 and all c > 0. The only negative input ever read is the defect:
- as b: λ_x ≥ 1 − 2 + 3 = 2;
- as c: λ_D ≥ −1 + (1+1)/2 = 0.

Every other combination adds a non-negative amount (at least 3 at chains and even steps) or halves a positive odd number. Positivity of c follows because updates add or halve positive c-parts, and zero pairs contribute 0 only alongside a positive head. Oddness of λ_A at chains is the chain condition combined with S2 (c_A even). ∎

## 3. E3 — no halt [A]

**Lemma E3.** At an endgame chain satisfying S1, with E2's invariants: c_u = c_x/2^j is even and ≥ 2, and λ_u is odd and ≥ 1. Hence u = c_u U + λ_u ≥ 2U + 1 ≥ 3 for every odd U ≥ 1, and **the chain does not halt**.

*Proof.* By S1, v₂(c_x) ≥ j+1, so c_u is even. Since c_x > 0 (E2, from c_A ≥ 1 and stored c > 0), c_u ≥ 2. λ_u is as in E2. A halt requires u = 1. ∎

## 4. E4 — mass [A]

**Lemma E4.** Along a defined prefix, with i the number of originals consumed (counting the defect):
- c_A + Σ_P c = 2^i (equal to 2^v once the defect is consumed);
- λ_A + Σ_P λ = 3s + 1 − [defect consumed].

Zero-pair reads add 0 and do not advance i. **If** a singleton is reached at step ℓ, it is the pair (2^v, 3ℓ), i.e. the value 2^v·U + 3ℓ. (Termination is **not** claimed.)

At every chain, λ_x ≤ 2(3s+1) + 3 = 6s + 5, so j ≤ log₂(6s+5). (The original report's bound 9s+6 is valid but looser.) ∎

## 5. E5 — deficit drain, prefix form [A]

**One-step inequalities.** Since v₂(x+y) ≥ min(v₂x, v₂y):
- even step: d(A′) ≤ max(d(A), d(b), d(c));
- chain: d(x) ≤ max(d(A), d(b) − 1); d(u) = d(x) + j; the t-th pushed entry has deficit d(u) − t; the new head u+(0,1) has deficit d(u);
- D: d(D) ≤ max(d(c), d(A) + 1).

**Lemma E5.** Let M_k be the maximum deficit over the head, the pending list and the unread entries just before the k-th endgame chain (k = 0, 1, …), and let j_k be that chain's parameter. Then M_0 ≤ D_cross and M_{k+1} ≤ M_k + j_k. Consequently, **if**

    n − D_cross > Σ_{i≤k} j_i,

then S1 and S2 hold at the k-th endgame chain. Applying this for every k makes the endgame prefix defined; with E1–E3, no chain in it halts.

*Proof.* By induction over steps:
- even steps do not increase the maximum deficit;
- at a chain, the new head and pushes have deficit ≤ M_k + j_k;
- D has deficit ≤ M_k + 1 ≤ M_k + j_k, since j_k ≥ 1. So the "+1" in D never accumulates beyond the j_k budget.

At chain k, v₂(c_x) ≥ n − d(x) ≥ n − M_k ≥ n − D_cross − Σ_{i<k} j_i > j_k, which gives S1. Also v₂(c_A) ≥ n − M_k ≥ 1, which gives S2. The S2 step uses only j_k ≥ 0 (λ_x ≥ 0 − 2 + 3 = 1 > 0 holds without S2), so there is no circularity; once S2 holds, j_k ≥ 1 absorbs D's "+1". M_0 ≤ D_cross because even steps before chain 0 do not raise the deficit, and the unread entry E_{v−2} is covered by the type-b case ε = 1. ∎

**Numerical check [B].** Adversary: for v = 3..1499, over 1021 endgame chains, max(d(x) − (ε + Σ_{previous} j)) = 0 and max(M − budget) = 0, so the bound holds and is tight. The original report's condition "(v−1) − D_cross > maxj + Σj + 1" over the whole run is stronger than needed; it can be negative while S1 holds (gemini: at v = 5, 9 it evaluates to −3, −2, with measured S1 margins 1, 3).

## 6. What is not claimed (corrections to the original report)

- The original says margins are "automatic for large v given D(n) ≤ log₂ n + c". This silently needs a bound on the endgame chain count (or on Σj), which is not proved, and it also uses s ≤ 0.9v + 16 [B]. It is only a **reduction** to a chain-length/Σj hypothesis; see `PROBLEM_ENDGAME.md` (EG-LEN).
- "Closure iff n − D_cross > J" is a Class-B probe. It is not what the proof gives, which is the Σj sufficient condition above.
- Termination of the endgame is not proved (E4 is conditional).

## 7. Review record (2026-10-17)

Reviewers: adversary = Claude subagent (scratch aud39); auditor 1 = agy gemini-3.8-flash-high (blind, aud37, agy_aud37.log); auditor 2 = cmdc deepseek-v4.1-flash (blind, aud38, cmdc_aud38.log).
- Adversary: `2. with fixable gaps`. Core arguments sound; all four propagation inequalities correct. Fixes:
  - prefix/S2 formulation of E1, E2;
  - vacuous c_A-odd case;
  - c_A ≥ 1 invariant for E3;
  - E4 termination overclaim;
  - E5 prefix form, an explicit D_cross, and demoting the two Class-A overclaims.
- Auditor 1 (gemini): `2. with simple errors`, with the same points. 1,780,141 lockstep steps (v ≤ 2000, U ∈ {3, 9, 15}) with 0 errors; min λ_x = 8, min λ_u = 1, min u = 7 (U=1) and 19 (U=3); terminal pairs exact. It raised the possible accumulation of D's "+1", which is resolved by the prefix form (§5).
- Auditor 2 (deepseek): `2. with simple errors`.
  - E2 wording: pushed entries u·2^t have odd λ only for t = 0 (fixed above).
  - E1 alone does not exclude a halt; that needs E2 + S1 (that is E3).
  - E4 "terminates" was an overclaim (fixed).
  - E5's original whole-run condition is loose (slack ≥ 2), false only at v = 1, 2, 5, 9, where S1 nevertheless holds; the prefix form is tight (slack 0).
  - Recomputed: 1.78M lockstep steps (v ≤ 2000), v ≤ 200 × 5 values of U; 44,882 endgame chains; min λ_x = 8, min λ_u = 1; terminal pairs exact.
- Coordinator patch: this file. PROBLEM_ENDGAME.md also corrected (steps vs chains, S2 in EG-SAFE, prefix-form reduction).
- Targeted re-reviews (adversary): round 1 `2. with fixable gaps` (E1 wording, E5 circularity note, PROBLEM_ENDGAME step count j−1, ε scope); after second patch `1. closed in all states`.

VERDICT: ACCEPTED (E1–E5 in the revised form above).
