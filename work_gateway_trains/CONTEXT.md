# CONTEXT — shared background for work_gateway_trains (gateway trains & climb control)

Session: 2026-10-24. Machine: BB(6) holdout #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`.
This directory attacks (B) gateway-chain / denominator-rank growth control (obstacle O1, condition (SC))
and (C) the climb bound (S3): generalizing work_claude_shift Lemma CB from canonical bare-tie
entries to general entries, then merging both into a "record budget".

**Hard rules for every contributor (human or agent):**
- Write files ONLY under `D:\math_cc\work_gateway_trains\` (your own subdirectory). Never modify any
  other directory, never git commit.
- If you must run an existing verifier that writes a json in its own directory, COPY the script into
  your subdirectory first and patch the output path. Import-only usage is fine (all repo verify
  scripts have `if __name__=='__main__'` guards).
- Honesty: no global EXT claim, no non-halting claim, K_clock unchanged. Tag every statement
  [A] (proved here from listed imports, all hypotheses stated), [A-imp] (accepted import),
  [A-cond] (explicit conditional), [B] (finite exact computation, range stated),
  [C] (conjecture/heuristic), [REFUTED] (with explicit counterexample). Synthetic states must be
  marked non-canonical. Do not reuse any REFUTED claim (list below).
- Every quantitative claim needs a recomputable script + json artifact in this directory.

## 1. Chain formalism (accepted; see work_global_ext/PROOF_EXT.md §2, work_r1r2 §1)

Chain state `(x, Θ)`, `x = 2^j u` (u odd), `n = j−1`, reads canonical crossing `X(n)`:
- **a step** (X(n) odd type a, `τ(n)=2k`): `x' = 2Θ + 6k − x/2`, `Θ' = Θ + 3 + 6k`, `Γ' = Γ + 1`.
- **b/c step** (X(n) odd type b or c): `x' = c'_W(n)·u + λ'_W(n)`, `j' = ω := v2(λ'_W(n))`,
  `Θ' = Θ + 3 + 3τ(n)`, `Γ' = Γ + 1 + ε(n)`, `ε = n − v2(c'_W) ≥ 1`, and S1: `ω < σ := v2(c'_W)`.
- Record `R = j + Γ`. a step has ε = 0. Even X(n): epoch ends.
- Defect `D := Θ − x`; class θ = D mod 2^{j+1} (symmetric rep). Rules (class determined):
  a: `θ' ≡ 3 − θ (mod 2^{j'+1})` for descents; b: `θ' ≡ θ − 1`; c: `θ' ≡ θ + s`,
  `s = Φ − 2 = −1 − λ_Y ∈ Z[1/3]` (source shift; work_claude_shift Theorem S gives it for every
  history via the reduced automaton with precision H).
- Rational normal form: `D ≡ C·Q^{-1} + b·2^j (mod 2^{j+1})`, `Q = 3^r`, gcd(C,Q)=1, b∈{0,1};
  height ht = |C|/Q (symmetric rep), rank r. a-step trichotomy with
  `p := 1 + v2(3Qk + C)`: p ≤ j−2 strong descent (j'=p, C'=3Q−C); p = j−1 NT gate (j' and class
  NOT class-determined; x'=0 possible); p ≥ j one-step descent/catapult (j'=j−1,
  C'=(9+6k)Q−C−bQ·2^j, Q'=3Q, b'=1, rank r'≤r+1). (work_landing_symbolic THEOREM.md §2.1.)
- Affine normal form: `x = A·U + β`, `Θ = 2^J·U + 3d + 1`, `v2(A) = J − Γ =: j`, β ∈ Z[1/6],
  `θ = 3d+1−β`. a step: `β' = 6d + 2 + 6k − β/2`, `α' = 2 − α/2`, `d' = d+1+2k`.
  b/c step: `β' = ratio·β + λ'_W`, ratio = c'_W/2^j. (THEOREM.md §2.6; STOP_CHECKPOINT note:
  at a five-input a step `β' = 6d + 8 − β/2`.)

## 2. Gateway / tie definitions (THEOREM.md §3)

- **tie**: chain at parameter 5 with class θ ≡ 5 (mod 16); Bad_5 = {5,21,−11,−27} mod 64.
  X(4) is odd type a with τ(4)=2, k=1 — the parameter-5 step is always the k=1 a step.
- θ≡5 (mod 16) ⟹ 3+D ≡ 8 (mod 16) ⟹ p = 4 = j−1: the tie step IS the NT gate; output
  `x' = 2^m u'` (m ≥ 5), record rises m−4 (from R = 5+Γ to m+Γ+1). Class map (THEOREM §2.5):
  `D' ≡ (15Q − C − 32bQ)/(3Q) + 2^m (mod 2^{m+1})`, i.e. C' = 15Q−C−32bQ, Q'=3Q, b'=1;
  rank r' = r+1 for r ≥ 1 (and r=0 unless 3 | C+2b).
- **A-type entry**: a-step from j_p ≥ 7 landing at 5, `v2(3k_p + D_p) = 4`; entry congruences
  `3Q_p k_p + C_p ≡ 16 (mod 32)`, `C_p ≡ 14Q_p (mod 16)` i.e. `k_{j_p−1} ≡ 6 (mod 16)`.
  **B-type entry**: b/c step with ω = 5 landing at class ≡ 5 (mod 16).
- Block = entry step + parameter-5 step. Block record: ρ_2 ≤ ρ_pred − 1 (THEOREM §3.3, under the
  valuation hypotheses C2 of §3.2). The tie step itself raises the record by m−4 (obstacle O2).
- 36 bad classes [B]: full-residue scan 5 ≤ j ≤ 18 gives 24 exceptions (j=5,8,12,14 have 4 each,
  j=17 has 8); j=22,24,27 have 4 each from the gateway direction (spot-checked). Representative
  exact walks all terminate, max parameter 29, max record 30, successor graph 36 vertices/4 edges/
  acyclic. NOT true that record ≤ entry record (refuted).
- REFUTED claims that must NOT be reused: tie→tie record law rho(t+1) ≥ rho(t)+(m−4)
  (counterexample walk from (j_p,D_p)=(73515,98094): records [73515,6,19,8,21,22,7]); Z[1/3]
  extension of A4; strong a preserving ht; universal catapult height constant (32b/3 is j=5 only);
  "record ≤ entry record" on the 36 representatives; rational (A4) "Q>1 ⇒ x'≠0".

## 3. The two open targets of this directory

- **(B) rank growth / gateway-train control.** NT gates in real walks (j ≥ 19) can only come from
  rational classes with large denominator rank r (DEPTH failure: `Q(κ(j)+h) < 2^{j−2}` with
  `κ(j) = (3/2)(j−1)P(j−1)`, `P(n) = 2⌈log2(6n²+5)⌉²+1345`), and r gains +1 per gateway block.
  Target forms: (S2*) `3Q_t k_t + C_t ≢ 0 (mod 2^{j_t−2})` on every a-chain of the walk;
  (SC) `r_0 + T < 5(σ−53)/8`; or a direct bound on consecutive gateway blocks. NOTE: 3^r is
  2-adically a unit, so the *congruence* content of (S2*) is rank-blind; rank enters only through
  (i) which residue is dangerous (C ≡ −3^r k mod 2^{j−2}) and (ii) failure of the DEPTH size
  shortcut. Astra's train identities (GATEWAY_TRAIN/CLOCK_FILTERED_TRAIN/TRAIN_CLOCK_ORBIT) give
  necessary congruences linking consecutive catapult labels' canonical half-times
  k_i = τ(m_i−1)/2: TRAIN `v2(4−k_i+3k_{i+1}) ≥ min(m_i−2, m_{i+1}−2, m_{i+2})`, ENTRY
  `k_i ≡ 6 (mod 16)` for internal labels, orbit `u_{i+1} = 3^{−1}u_i mod 2^{L−5}` on
  `u_i = (k_i+2)/8`, period 2^{L−7}, ADVANCE v2(Σ(12+6k_i)) = L−2 per period. These are
  UNREVIEWED until the review task finishes; verify before relying on them.
- **(C) climb bound (S3).** Lemma CB (work_claude_shift §3, accepted): bare-tie entry from a chain
  y ≥ N0 (N0 = 2·10^7) with entry letter A or B ⟹ catapult output m = v2(Z),
  `Z = 2d_5 + 6 + (3/2)Z_prev`, Z_prev exact mod σ_y (σ_y = y−2 A-entry, y−3 B-entry,
  y−2−ε(y−1) C-entry), so `m < G(y)+1`, `G(x) = 2log2(x)+3`; classes (10−2^m)/3 or (26−2^m)/3.
  Inside least strict-EXT induction, C-entries get σ_y ≥ y − 4log2(y) − 5. Generalize to entries
  through small chains (runs of descents/b/c below N0 before the tie): use affine β leading term
  to get `m < G(y) + O(r)`; identify when the β leading term cancels exactly (Z_run = 0) and how
  to exclude it (source/phase/congruence conditions, not parameter caps).

## 4. Accepted imports you may use ([A-imp] with pointer)

- Window certificate: certify(j,δ) for 5 ≤ j < 2·10^7, δ ∈ [−12,15], except (5,5),(5,−11)
  (work_claude_shifted §4).
- Gateway certificate: classes (10−2^m)/3 and (26−2^m)/3 certified for 5 ≤ m < 10^8
  (work_r1r2 Theorem 2.4).
- CLOCK: τ(n) ≤ n·P(n); τ(n) ≥ (n−1)/2. C1 on defined prefixes.
- work_claude_shift: Theorem S (reduced defect automaton, precision H), Lemma ND, Lemma CB,
  Theorem L (simple crossing eps≥7 ∧ ω≥N0 ⟹ n+1 ≥ T4), H5_res residual sources (i)–(v).
- work_landing_symbolic THEOREM.md (review-correction block at head OVERRIDES the body):
  Theorems A/B/C/D/E/F/G(H)/I, O1/O2/O3, RAT-C, 24 exceptions, 36 bad classes.
- work_deep / work_r1r2: deep-segment trichotomy, R1/R2; CAL-C FALSE, R1 fails somewhere in
  [K_clock,T4) — do not use parameter caps (CAL-C, R1, H3, fixed windows) as uniform targets.
- C2-log (work_global_egx): ε(i) ≤ max(3, 2J_W−1) when the containing epoch is tie-free in S(J_W);
  PROOF_EXT_ROOTS type-c: 1+ε ≤ 4log2(J)+4 inside the least strict-EXT induction.

## 5. Infrastructure

- Canonical calendar: `sys.path.insert(0,'D:/math_cc'); from work_global_calendar.calendar_oracle import Calendar`
  — `Calendar(512)` builds in ~0.1 s. `cal.crossing(n)` → dict(kind 'a'/'b'/'c', odd bool, time=τ(n),
  epsilon, omega, head_ratio, head_lambda, tail_ratio, tail_lambda) for 4 ≤ n < boundary_pointer
  (astronomically large; queries at n ~ 10^7 fine, cache per epoch).
  b/c step data: `cW = (head_ratio + 2·tail_ratio)·2^n` (integer), `λ'_W = head_lambda +
  2·tail_lambda + 3` — see `read_cross` in work_landing_symbolic/verify_landing.py (lines ~169–183),
  which also has `step_exact`, `exact_walk(cal,x,T,P)` (record-ceiling P), `certify(cal,j,δ)`,
  `v2`, `sym`, `clsmod`, `kappa`, `P_clock`. Copy what you need into your own script; do not edit
  the original.
- Canonical type/τ table for n < 10^6: `D:/math_cc_astra/deep1/table_1000000.pkl` (dict: typ bytes,
  tau array, eps array, odd bytes, lY array, lA array). Read-only.
- Astra train verifiers (unreviewed): work_c3_drift/verify_{gateway_train,clock_filtered_train,
  train_clock_orbit,cross_scale_train}.py — import-safe; copy before running (they write json).
- Calendar identities: X(4) odd a τ=2; X(5) odd b ω=1; X(0..3) even; X(27) odd b ω=6; X(28),X(29) even.
- G(x) := 2log2(x)+3; T1 = 2^((N0−3)/2), T_{h+1} = 2^((T_h−3)/2); G(J)<T_h ⟺ J<T_{h+1}.

## 6. Directory layout

- review_trains/ — Task 1: review of the four Astra train docs (+ budget docs).
- B_rank/ — Task 2: gateway-train / rank-growth results.
- C_climb/ — Task 3: climb-bound generalization of Lemma CB.
- RECORD_BUDGET.md, NOTES.md, MANIFEST.md — coordinator (Tasks 4–5).
