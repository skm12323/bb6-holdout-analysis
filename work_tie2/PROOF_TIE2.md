# TIE2: an exact extended-state automaton and one (conditionally two) further tower levels

Date: 2026-10-13. New research, **not independently audited**. Concerns the universal
formal walk F only; nothing here is a claim about the finite excursions or about machine #1
halting/not halting. No other file of the repository was modified.

Tags: **[A]** symbolic proof given here or imported with reference; **[B]** finite exact
computation (`verify_tie2.py`, output `certificate_tie2.json`, log `run_main.txt`);
**[C]** simulation/heuristic (used only in §7, labelled).

## 0. Results

1. **Extended automaton** (§2) [A]: state (j, Θ mod 2^M, λ_u mod 2^m, h) with exact a- and b/c-transition
   identities. It needs **no NT hypothesis**; it is exact through non-descending steps and records the
   *true* Θ-representative of every chain (so the PROOF_RESCUE §4 defect "rule gives 62, truth is 46"
   disappears: 46 is what is recorded and what copies use).
2. **Level generator** (§3) [A]: for an epoch of tower level l, a complete description of the chains that
   can occur, in terms of the a-outputs of lower-level epochs. Its level-2 instance reproduces COVER.
3. **Level-3 certificate** [B]: 7,000,101 entries, every one terminates; 13,943 genuine NT failures
   (13,940 from θ = −2 entries, 3 from θ = −1), all of the single tie class (5, Θ≡5 mod 32), resolved
   exactly by the extended automaton with **no branching** and margin h ≥ 1 throughout (from the minimal
   entry assumption h ≥ 1; the earlier stated 13,949 additionally counted six NT-safe extended inputs, §4).
4. **Theorem TIE2** (§5) [A+B]: inside Theorem M's epoch induction, every fire parameter
   J < K′ := 2^(K/2−2) has an exit with r ≤ 7 chains and h_t ≥ 1 at every chain. Hence

       F is defined and its universal walk is non-halting for s < (2^K′ − 4)/3,
       K′ = 2^(2^(2^499997−3) − 2).                                               (HORIZON-3)

5. **Level 4** (§6): 9,035,944 + 999,999 entries. Exactly one minimal-information entry fails, (j,θ)=(5,5)
   from the any-j family θ=5; its *only* source is an a-step out of a large-j state with θ=−2. A symbolic
   two-a macro (identity (AA) with the hidden crossing number k) replaces it by the new **2-adic rational
   family θ = 10/3** (any j < N), which is certified closed [B]. This gives a *conditional* next level
   J < K″ = 2^(K′/2−2), resting on one more imported margin bound (Lemma LM, §6.3). Status: proposed;
   conditional on Lemma LM; outside Theorem TIE2 (which uses levels ≤ 3 only).
6. **Trend** (§7): the entry set does **not** stabilize. Each level widens the any-j θ-window by 2 and adds
   a new non-integer (2-adic rational) family; at level 5 exact copies of tie chains of large-j origin
   appear, which the bit-level state cannot resolve. What breaks is described precisely.

## 1. Notation and tower ranges

As in PROOF_EL/PROOF_RESCUE: chain parameter j, Θ = 3s+5, θ = Θ mod 2^j, n = j−1, k_n = τ(n)/2 at odd
type-a crossings, λ_u = λ-part of the run base, σ = v2(c_x), h = J−Γ−j (PROOF_EL Thm B), ω(n) = j of
W's chain at τ(n). (C1): τ(n) ≤ n² at already reached crossings.

    T_1 = N = 10^6,  T_{i+1} = 2^(T_i/2 − 2):   T_2 = H = 2^499998,  T_3 = K,  T_4 = K′,  T_5 = K″.
    R_0 = [1, N),  R_i = [T_i, T_{i+1})  (i ≥ 1).

An epoch has **level l** if its fire parameter J ∈ R_l. Two size facts are used throughout [A]
(same derivation as PROOF_RESCUE §4 opening, using (C1)):

* (S-a) a chain with j ∈ R_i, i ≥ 1, and bounded representative −2 ≤ θ ≤ 10 is followed, at an odd
  type-a return, by an **NT** step (θ+3k ≥ 1 and θ+3k ≤ 10+1.5(j−1)² < 2^(j−2)) to
  j′ = 1+v2(θ+3k) ≤ log2(8+3(j−1)²) < T_i, with θ′ = 3−θ (PROOF_EL A2). (The lower end must be
  θ ≥ −2: θ = −3 with k = 1 would give θ+3k = 0. This is harmless at level 3, where every large-state
  window satisfies θ ≥ −1.)
* (S-c) any b/c return from a chain with j < T_{i+1} copies a W-epoch with
  J_W ≤ log2(3(j−1)²+4) < T_i, i.e. of level ≤ i−1; the first return of a level-l fire has
  j_1 ≤ log2(6(J−1)²+5) < T_l. (log2(6 T_{i+1}²) = T_i − 1.415.)

## 2. The extended automaton [A]

State (j, T, M, u, m, h): Θ ≡ T (mod 2^M), λ_u ≡ u (mod 2^m), h a lower bound for the margin.
Transitions at n = j−1 (parity/type from the real crossing table X(n), n < N, E1 of PROOF_EL):

* **even** return: the epoch ends.
* **a-step**, k = k_n. Exactly (PROOF_EL A2 before reduction; PROOF_RESCUE (AA)):

      λ_x′ = x := 2(Θ+3k) − 2^n λ_u,   j′ = v2(x),   λ_u′ = x/2^j′,   Θ′ = Θ+3+6k,   h′ = h+j−j′−1.

  x is known mod 2^B, B = min(M+1, n+m). If x ≢ 0 (mod 2^B), j′, Θ′ mod 2^M and λ_u′ mod 2^(B−j′)
  are determined. Otherwise the next unknown bit (of Θ if M+1 ≤ n+m, else of λ_u) is **branched**
  into both values — an exhaustive case split. NT is never assumed; a step with j′ ≥ j is marked "A".
* **b/c-step** (PROOF_EL A1, PROOF_M Lemma 3.2): chain t+1 = M_{u_t}(W-chain at w = τ(n)), with
  M_u(c′,λ′) = (c_u c′, λ_u c′+λ′). Hence j′ = ω(n), Θ′ = Θ + 3w + 3 **exactly**, and
  λ_u′ = λ_uW + c_uW·λ_u ≡ λ_uW + 2^v (mod 2^(v+1)), v = v2(c_uW) = σ_W − j_W (PROOF_M 3.2),
  because λ_u is odd. For n < N, w, λ_uW, σ_W are real-walk data; `sigma_walk` asserts j < σ and
  cross-checks only j against `verify_el.real_walk` (all 326,639 top-level chains) — the value σ_W
  itself is not independently recomputed and rests on the PROOF_M 3.2/3.3 identities.
  h′ ≥ h+1 (PROOF_EL Thm B: j′ ≤ j−2−ε).

**Soundness.** Every rule is an identity of F (or a congruence derived from one); branching covers all
values of unknown bits; forgetting bits (caps at 4096 bits) only loses information. Hence any terminal
run of the automaton from a state *compatible with* the true chain is the true continuation. When all
steps are NT it should coincide with the (j,θ) automaton of PROOF_EL; the script does not check this,
but the reviewer's sample check found agreement on non-tie inputs.

**Entry knowledge.** "Minimal" entry (j,θ): Θ ≡ θ (mod 2^j), λ_u odd, h ≥ 1. "Extended" entry
(record X): a copy of a chain that was itself produced by an extended run, carrying
Θ ≡ T_W + δ (mod 2^min(M_W, cap)) and λ_u ≡ u_W (mod 2^min(m_W, h_W)) — the copier's term c_uW·λ_u
vanishes mod 2^v and v = σ_W − j_W ≥ h_W. δ = −1 for a first-return copy (Θ_fire ≡ 1 mod 2^J) and
δ = θ−2 for a copy made from a large-j state (j ≥ N, Θ ≡ θ mod 2^j).

## 3. The level generator and coverage [A]

Write AO_l for the set of **a-outputs** (chains created by a type-a return) of level-l epochs, in three
forms: any-j pairs (range i, θ), specific pairs (j, θ mod 2^j), extended records X.
By the location lemma (PROOF_RESCUE §4, valid at every crossing index) a c-return copies an
a-output; a b-return copies a W-fire (θ_W = 1).

For a level-l epoch:
* **chain 1** (j_1 ∈ R_i, i ≤ l−1 by S-c): route a gives (i, 2); route b gives (i, 0); route c gives
  (j_W, θ_W − 1) for every a-output of AO_{lw}, lw ≤ l−1 (extended records with δ = −1).
* **large state** (j ∈ R_i, i ≥ 1, bounded θ): by S-a/S-c the next chain is (i′, 3−θ) or (i′, θ−1),
  any i′ < i, or (j_W, θ+θ_W−2) for an a-output of AO_{lw}, lw < i (records with δ = θ−2).
  Margins: a-step change j−j′−1 ≥ 0, b/c ≥ 1.
* **small entry** (j < N): run the extended automaton; its a-outputs go to AO_l.
* AO_l = {(i,2): i < l} ∪ {large a-outputs (i′,3−θ)} ∪ {a-outputs of the small runs}.

`verify_tie2.py` implements exactly this recursion (AO_0 = a-outputs of all fires (J,1), J < N).
Level 1 gives θ ∈ {0,2} and the 26 A0−1 entries (EL level 1); level 2 gives θ ∈ {−1,…,3} plus
64 specific entries — the COVER family of PROOF_RESCUE §3 (5,000,059 entries after deduplication
mod 2^j; same distribution, same 3 ties) [B].

## 4. Level-3 certificate [B]

Generator output (level 3): large states θ ∈ {0,2} on R_2 and {−1,0,1,2,3} on R_1; minimal small
families θ ∈ {−2,−1,0,1,2,3,4} × 1 ≤ j < N; 102 specific pairs; 6 extended records (copies of the
level-2 rescued chains (5, Θ≡37) and (6, Θ≡46 mod 2^17) — the true values).

| further chains after entry | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| entries | 2,648,803 | 4,065,716 | 273,657 | 11,922 | 3 |

Total 7,000,101. NT failures (audited count): 13,943 — 13,940 from θ = −2 entries, 3 from θ = −1 —
every one at a state (5, Θ ≡ 5 mod 32) (the n = 4, k = 1 tie). The earlier stated 13,949 additionally
counted six extended inputs that are NT-safe: three project to (5,4), three to (6,45), each terminating
after one further chain. All 13,943 genuine failures are resolved by the extended automaton: 0 failures,
0 branches; margins stay ≥ 1 from the baseline h = 1, and the independent audit gives global min h = 1
and min h = 10 immediately after a non-descending step; every non-NT output satisfies 3Θ ≡ 10 (mod 2^j′)
(j′ ∈ {5,…,19}). The resolution is the two-a identity (PROOF_RESCUE §1 with l = 1), applied with the side conditions
**j_e ≥ 12** and **|θ_e| ≤ 10** of its two-step descent lemma — both are met by every actual tie entry:
landing on (5,5) forces k_{j_e−1} ≡ 6 (mod 32) (auditor's argument: v2(x1) = 5 together with
Θ_1 ≡ 5 (mod 32) forces the congruence), hence n = j_e−1 ≥ 11 and j_e ≥ 12; and the bounded
representatives in play satisfy |θ_e| ≤ 10 (S-a's range). An entry (j_e, θ_e) whose a-step lands on
(5,5) continues to j_2 = v2(θ_e+12+9k_{j_e−1}) ≤ j_e−3 with Θ_2 ≡ (θ_e+12)/3 (mod 2^j_2).
Corollary (auditor): 10/3 ≡ 14 ≢ −2 (mod 32), so no post-tie chain re-enters (5,5): one tie per run.
Level-3 a-outputs: 99 specific pairs and 35,801 extended records.

## 5. Theorem TIE2 (one further tower level) [A + B]

**Theorem.** Inside Theorem M's epoch induction (with (C1), (C2) at earlier crossings, the audited
base for ρ ≤ 10^8, EL Theorem D for J < H and PROOF_RESCUE §4 for J < K), every fire parameter
J < K′ has a tie-free exit (symbolic coefficient separation, h_t ≥ 1 at every chain) with r ≤ 7.

*Proof.* Only K ≤ J < K′ is new.

1. *Bounds.* j_1 ≤ log2(6(J−1)²+5) < log2 6 + 2(K/2−2) < K; every copied W-epoch at the first
   return has J_W ≤ log2(3(J−1)²+4) < K − 2.4. From j ∈ R_2: j′ < H and J_W < H; from j ∈ R_1:
   j′ < N and J_W < N (S-a, S-c). So copies at the first return read W-epochs of level ≤ 2, later
   copies from large states read levels ≤ 1, ≤ 0 respectively. All are earlier in time.
2. *Coverage.* By §3, every chain of the epoch is chain 1, a large state of the generator, or lies on
   a run from a level-3 small entry. The a-outputs of level ≤ 2 epochs are AO_0 ∪ AO_1 ∪ AO_2 as
   computed: this uses Theorem D/PROOF_RESCUE for those epochs, and the extended automaton supplies
   the **true** representatives of the rescued level-2 chains (46, not 62). This closes the gap
   named in PROOF_RESCUE §4 "After the non-NT step".
3. *Termination.* By §4 every small entry ends with ≤ 4 further chains; at most chains 1–2 are large,
   so r ≤ 2+1+4 = 7.
4. *Margins.* h_1 ≥ 1 (PROOF_EL Thm B, both routes); large steps keep h (≥ 0 or ≥ 1 changes); the
   certificate tracks h along every run from the baseline 1 and finds min h = 1. With
   v2(α_{x_t}) = J−Γ_t (Lemma T) and h_t ≥ 1 one gets v2(β) = j_t < v2(α): the strict comparison of
   PROOF_M Lemma 6.1 — no symbolic tie, including at the non-NT steps. σ_t − j_t = ρ − J + h_t ≥ h_t
   (ρ > J: S1 at the fire, where j_0 = J and σ_0 = ρ), so every replay is safe.
5. *No circularity.* A rescued (non-NT) chain of a level-3 epoch comes from a W-epoch with J_W ≥ K; a
   copy of it would be a b/c-step of the copying epoch, so (S-c) gives J_W ≤ log2(3(J−1)²+4), and
   J_W ≥ K gives 3J² ≥ 2^K − 4, i.e. J ≥ 2^(K/2−0.8) > K′. Large-state copies of a level-3 W need the
   copying state in R_4 or higher (a large state on R_i copies W-levels lw < i): outside the horizon,
   where every chain of a covered epoch has j < J < K′. Level-3 epochs copy only levels ≤ 2 (step 1).
6. *Deficit.* For J ≥ K, 3s+4 ≥ 2^J and s ≤ i² (M2′) give log2 i ≥ J/2 − 0.8, hence ⌊log2 i⌋ ≥ J/2 − 2. PROOF_M Lemma 3.3 gives
   Δ ≤ 2+t+a_t+Σ_{t′<t} ε(n_t′)+j with t, a_t ≤ 7 and ε(n) ≤ 7 + n/4 ((C2), as used in PROOF_RESCUE
   §4), so Δ ≤ 16 + 7·7 + (J + 3 log2(6J²))/4 + J < 1.3J + 100 < (J/2−2)² ≤ ⌊log2 i⌋². ∎

**Imports (inherited, not re-proved here):** the PROOF_RESCUE location lemma (used in §3 and step 2 above;
valid at every crossing index) and PROOF_RESCUE §4; (C1) (τ(n) ≤ n² at reached crossings) and (C2); the
audited base certificate for ρ ≤ 10^8; and the PROOF_EL/PROOF_M lemmas cited inline (A1/A2, Theorems B
and D, Lemma T; Lemmas 3.2, 3.3, 6.1).

**Horizon** (HORIZON-3): a fire before time s has 3s+4 < 2^K′, so J < K′; hence F is defined and
non-halting for s < (2^K′ − 4)/3. This is a bound on F steps, not on original machine steps.

## 6. Level 4 [B + A, conditional]

### 6.1 Certificate [B]
Large states: R_3 {0,2}; R_2 {−1,…,3}; R_1 {−2,…,4}. Small any-j θ ∈ {−3,…,5}; 140 specific pairs;
35,813 extended records. Entries 9,035,944; old-automaton ties 49,789; resolved 49,788 (0 branches);
non-NT outputs again all ≡ 10/3 mod 2^j′. **One failure**: the minimal entry (5,5) of the any-j
family θ = 5 (here Θ ≡ 5 mod 32 and λ_u odd are all that is known, and j′ = 4+v2((Θ+3)/8 − λ_u) is
genuinely undetermined; branching to depth 24 never closes). The real-u refinement of §2 is needed:
without it (first run) 29 further entries (j,5) failed after a c-step into (5,5).
The generator records the sources of each family: θ = 5 at level 4 has the **single source**
"a-step from a large state on R_1 with θ = −2" (3 − (−2) = 5).

### 6.2 The large-state macro [A]
Let a chain have j_b ∈ R_1, Θ ≡ −2 (mod 2^j_b), take an a-step with unknown k (k ≤ (j_b−1)²/2) to
j′ = 5 (so −2+3k = 16·odd) and then the a-step at X(4) (k′ = 1). By (AA),

    x_2 = Θ + 6 + 9k + 6 + 2^(j_b−2) λ_u,   j_2 = v2(10 + 9k) ≤ log2(10 + 4.5 (j_b−1)²) < N,

since 0 < 10+9k < 2^(j_b−2); Θ_2 = Θ+12+6k and 9k ≡ −10 (mod 2^j_2) give Θ_2 ≡ 10/3 (mod 2^j_2).
(10+9k = 16(1+3·odd), so j_2 ≥ 5.) Margin over the pair: j_b − j_2 − 2 ≥ 1. λ_u2 is only known odd.
So the failing entry is replaced by the minimal entries (j, 10/3 mod 2^j), 1 ≤ j < N (superset).

**Certificate** [B]: that family (999,999 entries) terminates with ≤ 4 further chains; 13,939 ties at
(5, Θ ≡ 5 or 21 mod 32), all resolved, 0 failures, min h = 1.

### 6.3 Margin lemma LM and the conditional theorem
Some resolved level-4 runs (copies into (5,5) followed by a non-NT step) dip to h = −1 relative to
the baseline 1, so the baseline is not enough. **Lemma LM** [A, imports (C2)]: in an epoch with
J ≥ H, every chain t ≤ 9 with j_t < N has h_t ≥ J − Γ_t − j_t ≥ 3J/4 − 10^7 > 10^6, because
Γ_t = Σ(1+ε(n_t′)) with ε(n) ≤ 7 for n < N (V2) and ε(n) ≤ 7+n/4 for the ≤ 4 large indices
(n_0 = J−1 and j_1,j_2,j_3 ≤ log2(6J²)). All drops in the certified runs are < 25, so h stays positive.

**Conditional Theorem TIE2′.** With Lemma LM, §6.1 and §6.2, every J < K″ = 2^(K′/2−2) has a tie-free
exit with r ≤ 9 (chains on R_3, R_2, R_1, the macro pair, then ≤ 4). The proof is §5 with T_4 → T_5,
coverage including the source check, and no circularity (level-4 epochs copy levels ≤ 3).
Status: proposed and conditional on Lemma LM; it adds the source-tracking claim, Lemma LM and the macro
to the audit surface. Level 4 is not used by Theorem TIE2 or HORIZON-3.

## 7. Trend and the precise obstruction

| level | any-j θ window | large-state θ sets | specific / extended | ties (all n=4) | failures |
|---|---|---|---|---:|---:|
| 1 | {0,2} | — | 26 / 0 | 0 | 0 |
| 2 | [−1,3] | R_1 {0,2} | 64 / 0 | 3 | 0 |
| 3 | [−2,4] | R_1 [−1,3], R_2 {0,2} | 102 / 6 | 13,943 | 0 |
| 4 | [−3,5] (+ 10/3) | R_1 [−2,4], R_2 [−1,3], R_3 {0,2} | 140 / 35,813 | 49,789 (+13,939) | 1 → macro |

**Not stabilizing** [B for the table; reading of the trend C]. The windows grow by 2 per level; the
extended records grow (6 → 35,801 → 60,068 a-outputs); every level since 2 adds new 1/3-adic
values (j, 10/3 mod 2^j), e.g. (14,10926), (19,174766), and level 4 adds a j-parametrized
rational family. What breaks next (level 5), precisely:
* AO_4 contains the any-j a-output (j, 5) of large-state origin. An **exact copy** (δ = 0, made from a
  large state with θ = 2) of that chain at j = 5 is again a (5, Θ ≡ 5) tie, now with no λ_u/Θ bits
  beyond the minimal ones, and the generator's bit-level knowledge cannot resolve it.
* It *is* resolvable in principle: the copied chain satisfies Θ = 5 + 2^5 w, λ_u = w + O(2^v) with w =
  (−2+3k)/16 for a hidden k ≤ n²/2, and the copier replays W's macro (j_2 = v2(10+9k)). The needed
  extension is a **symbolic hidden-k state** (affine in w with a size bound), not more bits.
* Rational θ (denominators 3^a) will reach large states (from R_2 at level 5). NT there still follows
  from size (θ = p/q: tie needs v2(p+3qk) = n−1 with 0 < |p+3qk| < 2^(n−1)) — but copies, shifts and
  macros must then be carried in this rational/hidden-k form, and nested exact copies compose.
No closure of this process under unlimited nesting is proved; global non-halting of F is **open**.

## 8. Reproduction

    python -B work_tie2/verify_tie2.py 4 16     # ~75 s with 16 workers; writes certificate_tie2.json

Imports `work_el/verify_el.py` (real walk, automaton) read-only; writes a temporary cache
`work_tie2/_walkcache.pkl` (deleted at exit). Run log: `work_tie2/run_main.txt`.
Not re-verified here: the 10^8 base certificate, PROOF_M/EL/RESCUE symbolic lemmas (imported).
