# Uncertified / residual sources (gap G2, H5_res, C7) — preliminary exploration

Claude, 2026-11-02. **Reviewed (three-way, 2026-11-02); the review-correction block below overrides the body.** Tags: [A] proved here (proof given) from the listed accepted imports [A-imp];
[A-cond] proved under the stated extra hypothesis; [B] exhaustive exact computation over a stated finite range
(script named); [C] heuristic. No global EXT claim. The accepted horizon K_clock is unchanged by this note; §6
states a *candidate* horizon improvement that needs the repository's three-way review.


> **Review corrections (2026-11-02, reviews/claude_residual_review_record.md; they override the body below).**
> 1. [MEDIUM] **Absorption of the BBBA family via AB′ is withdrawn; Theorem RA suffices.** Lemma AB needs phase
>    exactly 2 (route a). AB′ as stated has an incomplete record condition (it must include the offset
>    Gamma* = 1+eps(m)+DeltaGamma_E, not "records < Q") and needs "F defined through the end of E", which does not
>    follow for type-b/c J. AB′ and the "copy principle" of §5.4 are **unreviewed remarks**, not used. Replacement
>    argument [A]:
>    - (re-review) The uncertified entry (5,5) needs theta_t + D − 2 ≡ 5 (mod 64), where D is a chain-5 class of a
>      source admissible at deep chain t. Using the §4 chain-5 sets:
>      - t=0: theta=1 and classes {−1,0,1,2,3,5,14}; D=6 would be needed. None.
>      - t=1: theta ∈ {0,1,2} and classes {0,1,2,3,5}; only theta=2, D=5. Class 5 at that position occurs only in
>        level C, so Q >= T1, and DL(i) gives j_1−1 > T2.
>      - t=2 (theta ∈ [−1,3], classes {1,2,3}) and t=3 (theta ∈ [−2,4], class {2}): none.
>
>      (The (5,5) in levels D/OUT comes from delta=−2 entries and is not reachable at these positions.)
>    - Route c is excluded. Here j_1 = omega(J−1) is the chain of an a-output of a source Q′ < G(J−1) < T3. A shallow
>      output has j_1 < N0. A deep one sits at chain 1 (< G(Q′) < T2) or chain 2 (< T1). Either way j_1 < T2.
>    - Route b gives theta_1 = 0.
>    - Hence X(J−1) is of type a, and the accepted Theorem RA (no hypothesis) gives EXT(J).
>    - For X(J−1) of type b/c, C7 has no uncertified entry below T4 by the enumeration above. levels.py records only
>      one provenance per entry (setdefault), so its printout alone does not show this. C5_EXTENSION §4 therefore
>      applies as it stands. The a/b-landing (5,5) at theta_3 = −2 is not a C7 entry; the accepted r1r2/C5_EXTENSION
>      gateway handles it.
>
>    §6 is proved by this case split: X(J−1) even → trivial (r = 0); type a → RA; type b/c → C5_EXTENSION §4 with H5
>    by §5.1 and C7 by §4.
> 2. [MEDIUM] The BBBA landing is **not** a G2 instance. The source walk from (m0,−1) is certified with precision
>    m0+1, and the real defect at m0 is −1 modulo far more than that. By HP the real chain-5 state agrees with the
>    representative mod 2^(m0−3) (>= 244,872 bits). "Precision 16" is the automaton's information, not the real
>    information. c7_family.py (c) varies bits that are not free: 12 random lifts for each of four m0 give one word
>    (m0,17,5,6,1) and one D_5 mod 2^60. C7 fails in its literal mod-2^(j+1) form at the constructed J [A-cond]; the tail is certified via HP.
>    "Genuine G2 instance" (§0 item 5, §5.4, §8) is withdrawn.
> 3. [MEDIUM] **Zero margin.** Widening every drift range by 1 creates an uncertified level-D entry 5 and the
>    chain-5 class 6 (the case-(iii) target). The stated ranges are correct and the true sets are tighter:
>    - level D, deep chain 2: theta_2 ∈ {−1,1,3} (deep chain 2 needs j_1 >= T1, so route a or b);
>    - level C, deep chain 1: theta_1 ∈ {0,2};
>    - S(J): theta_1 ∈ {0,1,2}, theta_2 ∈ [−1,3], theta_3 ∈ [−2,4].
>
>    These exact sets, with their one-line reasons, are the load-bearing part of DL(iii)–(iv).
> 4. [LOW] §3(ii): work_deep's L(j) contains a B-term (≈ 10^7+1) and its G is max(2log2 j+3, 10^7+2), so
>    "L(j_t) < G(j_t)" with G = 2log2 j+3 is false as written for N0 <= j < 2^(5·10^6). Use the direct small-theta
>    bounds instead: a-step j' <= 1+log2(1.5n²+5), b/c step omega <= log2(6tau+5), both < 2log2 j+3. The conclusion
>    is unchanged.
> 5. [LOW] The spectra Sigma_h hold at chains omega >= 5 only (landings at omega <= 4 end; level A has classes
>    −1, 1, 3 at chains 1–4). m = 23 does not occur in the gateway family 4/3+2^m.
> 6. [LOW] §5.4: log2^(4) J ≈ m0 needs CLOCK (with C1 alone, only >= m0/2 − O(1)). The construction is
>    [A-cond] and is not used by the theorem.
> 7. [LOW] Theorem T4 can be stated relative to the accepted EXT(<K_clock): every source used has Q < T3 < K_clock,
>    so it is a statement about K_clock <= J < T4. The machine-level horizon (no halt in the first 2^T4−2 top steps)
>    is *expected* to follow by the Corollary H-CLOCK pattern with H = T4; this is not separately verified.
>    §5.2 (i)–(v) is a consistency remark once §5.1 holds. R0(c)'s "source epoch = latest odd-a pointer" is [B],
>    with Lemma K(c) as the [A] basis.
>
> 8. [LOW] Reproducibility:
>    - the scratch cross-checks are now in this directory: `xcheck_bulk_vs_certify.py` (bulk = certify) and
>      `xcheck_symbeta.py` (rwalk vs route_c sym_beta, 5 <= Q < 10^6);
>    - rwalk.py resolves ROOT as its parent's parent (the repo);
>    - levels.py writes levels_<JMAX>.json into its own directory.
>
> Confirmed by the review:
> - DL's case split, re-derived by hand: deep a-outputs below T3 are exactly (1,2), (2,1), (2,3); S(J), J < T4, has
>   at most 4 deep chains; strict boundaries G(T_{h+1}) = T_h; H5 holds.
> - The certificate equals Prop 3.2/HP.
> - An independent vectorised bulk certificate (ALL MATCH, delta ∈ [−8,10], j <= 2·10^7) and an independent level
>   closure (B 54, C 83, D 148, C7 89 classes, single uncertified (5,5)).
> - Lemma R0, rechecked on the 2·10^7 and 10^8 tables.
> - Real data on the 10^8 table (62,160,927 odd entries): no DL(i) violation, nothing outside the A/B sets, no ties.
> - The 68 m0 values; T3 < K_clock < T4.
>
> Levels C and D rest on the hand case split; no real data exists there.
>
> **Net result: Theorem T4 [A+B]**, relative to the accepted EXT(<K_clock) and the accepted imports (C5_EXTENSION §4,
> CLOCK/C1, gateway and window certificates): for every J with K_clock <= J < T4 and F defined through tau(J−1),
> S(J) is tie-free.

## 0. Summary

1. **Lemma R0 (what an uncertified shift is) [A].** For every odd c crossing X(n) with ω = ω(n),
   s(n) := −1−λ_Y(n) = D_src − 2 *exactly* (D_src = real defect Θ−x of the copied source chain), and
   s(n) ≡ 3τ(n) + 3 + 2^ω (mod 2^(ω+1)), with τ(n) = τ(ρ) + d (ρ the source fire pointer, d the clock sum of the
   source word). "Uncertified" only means that the automaton value Φ−2 no longer equals this clock residue; the shift
   is still the real class of a real chain of the source epoch. MASS/CONE/clock *inequalities* give no restriction on
   it mod 2^(ω+1) (§2) [A]. [B] all 316,980 c crossings n < 2·10^7 (`check_r0.py`).
2. **Scale lemma DL [A].** For a source epoch S(Q) with Q < T_h only chains 0..h−1 can be ≥ N0 ("deep"), and their
   classes are explicit small integers; a c crossing at index n has source parameter Q < G(n). So below T4 every
   object needed by H5/C7 lives in finitely many explicit *levels* (sources Q ≤ N0, (N0,T1), [T1,T2), [T2,T3)),
   each fed only by lower levels (§3).
3. **Level computation [B]** (`levels.py`, 83 s, exhaustive over all chains < N0 = 2·10^7 with over-approximated
   entry sets): every shallow entry of every S(Q), Q < T3, is certified. The a-output classes, hence the full
   **shift spectrum Σ_h of all c crossings with source Q < T_h, is finite and explicit**: Σ_{≤N0} = {0};
   Σ_{<T1} = {−1,0,1}; Σ_{<T2} = {−2,…,1, 3} ∪ {4/3+2^m at m=6}; Σ_{<T3} = {−3,…,1, 3} ∪ {4/3+2^m, 5≤m≤24} ∪ {−7/3}
   (heights ≤ 3, 3-rank ≤ 1, lift bit only on the gateway family). §4.
4. **H5 holds for every J < T4 [A+B].** Every deep→deep c step of S(J), J < T4, copies a deep a-output of a source
   with Q < T3, and those are only (chain 1, class 2) [history A] and (chain 2, class 1 or 3) [AA, BA]; so ε ∈ {3,5}.
   All five residual types (i)–(v) of work_claude_shift are **vacuous below T4**. In particular the [C] "2-layer
   case-(iii) shape" is an **artifact**: it needs a nested crossing with ω=5 and shift ≡ 4 or −12 (mod 64), i.e.
   class 6 or −10 at a chain-5 a-output, and no S(Q) with Q < T3 has one (chain-5 classes ⊂ {−1,0,1,2,3,5,14}). §5.
5. **C7 below T4 [A+B]:** every c landing of S(J), J < T4, has a certified class **except one family**: the bare tie
   (5,5) entered by a C letter at deep chain 1 with θ_1 = 2, copying the chain-5 a-output of a source with word
   Q →b j1 →b m0 →b 17 →a 5 (ε = 9, T1 ≤ Q < T2, m0 ∈ {244875, 538715, …}, 68 values). Its source chain is a genuine
   G2 instance (automaton precision 16, but the bare tie needs more bits), so **C7 as literally stated is not
   provable**; and [A-cond] it is realised at some J in (K_clock, T4). But θ_1 = 2 makes the state phase-2, so the
   accepted absorption lemma AB (and Theorem RA when θ_1 = 2 comes from route a) copies the real source epoch to its
   end: the landing is **safe**. §5.4.
6. **Candidate theorem [A+B, pending review]:** inside the least strict-EXT counterexample induction, EXT(J) holds
   for every J < T4 (accepted C5_EXTENSION §4 with C7 replaced by "certified or AB-absorbed"). Since T3 < K_clock < T4,
   this would move the EXT horizon from K_clock to T4. §6.
7. **G2 vs G1.** G2 is not an independent obstacle: by the copy principle (§5.4) a C letter landing with drift θ
   continues as the source epoch's tail shifted by θ−2. θ = 2 hands the post-gate problem to the source epoch
   (closed by induction); θ ≠ 2 makes it a post-gate problem (G1) for a shifted reference. Below T4 no shifted copy
   ever needs uncertified bits. Beyond T4 the level sets grow (drift +1 per level, new rational families, gateway
   climbs back to deep chains from T4 on), so this is a level-by-level method, not yet a uniform argument (§7–8).

## 1. Setting and imports

Notation as in work_claude_shift §1: chain (x, Θ), x = 2^j u, defect D = Θ−x; a-step x' = 2Θ+3τ−x/2; b/c-step
x' = c'_W u + λ'_W, Θ' = Θ+3+3τ. N0 = 2·10^7, G(x) = 2log2 x + 3, T1 = 2^((N0−3)/2), T_{h+1} = 2^((T_h−3)/2), so
G(J) < T_h ⇔ J < T_{h+1} and G(J) < N0 ⇔ J < T1. "Deep" = chain ≥ N0 (all deep classes below are tiny, |θ| ≤ 5 ≪ B).
An **entry** (j, δ) is a chain j < N0 whose class δ = D mod 2^(j+1) is known; it is **certified** if the exact walk
from its representative ends with all records below the trusted precision (work_claude_shifted Prop 3.2; one-step form
for j ≥ 64). A certified entry fixes, for every real state in its class, all later parameters and types, records
≤ j, and (HP) the class mod 2^(j_t+1) at every later chain t.

[A-imp] used: Lemma K, HP, AB, Theorem RA, Prop RB, Lemma BR (work_global_ext/PROOF_EXT.md); ENTRY
(work_ext_roots); MASS (origin_contraction); C1/CLOCK; work_deep Lemma 2.4 (deep step ≤ L(j) ≤ G(j) for small θ);
C5_EXTENSION §4 (J < T4: H5 ∧ C7 ⟹ EXT), c3/AA/BA identities; r1r2 a/b-landing gateway; window certificate
(work_claude_shifted §4); PROOF_SPECTRUM (first fire of every label; X(ρ+1) is the b copy of the fire at ρ);
Theorem CT (congruence targets) and DEF relative to EXT(<K_clock) (CONGRUENCE_TARGET_NOTE §1).

## 2. Lemma R0 and the meaning of "uncertified" [A]

**Lemma R0.** Let X(n) be odd of type c, ω = ω(n), C its source chain (Lemma K(c): W's chain at τ(n) is chain t+1 of
the current real epoch E, with real data x_C = λ'_W(n), Θ_C = 3τ(n)+5). Then
(a) s(n) := −1−λ_Y(n) = D_C − 2 exactly, D_C := Θ_C − x_C;
(b) s(n) ≡ 3τ(n) + 3 + 2^ω (mod 2^(ω+1));
(c) if E's fire has pointer ρ, label Q, and E's word up to C has clock sum d (Lemma BR), then τ(n) = τ(ρ)+d and
    D_C ≡ 3d+1−β_C ≡ (3d+1) − 2^ω (mod 2^(ω+1)) while E is tie-free.
*Proof.* (a) λ'_W = λ_A+2λ_Y+3 and λ_A+λ_Y = 3τ+1 (mass identity) give λ'_W = 3τ+4+λ_Y, so
D_C = 3τ+5−λ'_W = 1−λ_Y. (b) v2(λ'_W) = ω gives λ'_W ≡ 2^ω (mod 2^(ω+1)). (c) EGX/TR: the real chain is the β-walk
chain plus a U-part of valuation Q−Γ_C > j_C (tie-free margin); Θ_real = 6k+4+(3d+1). ∎
[B] `check_r0.py`: (b) for all 6,057,602 b and 316,980 c odd crossings n < 2·10^7; (c) for all 316,980 c crossings:
the source epoch is the latest odd-a pointer, the kernel S(Q) (exact β-walk) has an a-output at chain ω with class
s+2 and clock sum τ(n)−τ(ρ). 0 failures (`r0_checks.json`).

So G2's "an uncertified source's shift is an arbitrary residue mod 2^(ω+1)" is precisely: the clock residue
τ(n) mod 2^(ω+1) beyond the bits pinned by the source word. **No-go for local constraints [A]:** MASS gives
D_C ∈ [−3τ, 3τ+4] and CONE gives 0 ≤ b ≤ 6t for the small part; both are size bounds, while by (b) the residue of
D_C mod 2^(ω+1) is 3τ+5−2^ω, i.e. a function of τ mod 2^(ω+1) on which neither bound says anything (the interval
[−3τ, 3τ+4] has length ≥ 2^ω−1 because 2^ω ≤ λ'_W ≤ 6τ+5, and for τ ≥ 2^(ω+1) it contains every residue). Hence
MASS, CONE and the clock bounds alone cannot give a finite Σ; any
restriction must come from the actual calendar at the small chains plus the scale structure — which is what §3–4 do.

## 3. Scale lemma DL [A]

(i) **Source parameter.** If E (label Q, pointer ρ) is the source epoch of a crossing at index n ≥ ρ, then
Q < G(n). *Proof.* The fire time s satisfies 2^Q | 3s+4, so s ≥ (2^Q−4)/3; C1 gives ρ ≥ √s ≥ 2^((Q−2)/2) (Q ≥ 4). ∎
(ii) **Deep chains.** In S(Q), chain t+1 ≤ L(j_t) < G(j_t) while the class is small (work_deep Lemma 2.4, small-θ
branch; no deep non-descent by Lemma ND). Hence for Q < T_h at most chains 0..h−1 are deep, chain t < T_{h−t}.
(iii) **Deep a-outputs below T3 (inductive form).** Assume (as verified in §4 [B]) that every shallow entry of every
S(Q), Q < T3, is certified. Then no chain after the first shallow one is deep, and the deep a-outputs of S(Q), Q < T3,
are exactly: chain 1 via route a (class 2, history A); chain 2 via a from a deep chain 1 of class 2 (route a) or 0
(route b): classes 1 (AA) and 3 (BA). *Proof.* By (ii) only chains 1, 2 can be deep. A root C letter landing deep
copies a deep a-output of a source Q' < G(Q) < T2; by induction only (chain 1, class 2), so θ_1 = 1. A deep chain 2
needs chain 1 ≥ T1; a root C letter with ω ≥ T1 needs a source Q' with a route-a chain 1 ≥ T1, so Q' ≥ T2,
contradicting Q' < G(Q−1) < T2. C letters at deep chain 1 copy sources Q' < G(j_1) < T1, which have no deep a-output.
So deep chain 1 ∈ {(2: a), (0: b), (1: c)}, deep chain 2 ∈ {3−θ_1 (a), θ_1−1 (b)}, and an a-output at chain 2 needs
θ_1 ∈ {2, 0}. ∎ (CA with deep output would need Q ≥ T3: consistent with Theorem L.)
(iv) **Drift in S(J), J < T4.** Deep chains t ≤ 3 with θ_t ∈ [1−t, t+1] (C5_EXTENSION §2): a/b maps, and deep c steps
with shifts {0, −1, +1} only (by (iii) the copied deep a-outputs have classes 2, 1, 3). A c step at deep chain t has
source Q < G(j_t), i.e. Q < T3, T2, T1, N0 for t = 0, 1, 2, 3.

## 4. The level computation [B]

`levels.py` (uses `rwalk.py`; table D:/math_cc_astra/deep1/table_20000000.pkl = indices < 2·10^7 = N0, plus
fdata.small_full). Bulk runs certify the entry (j, δ) for **every** 5 ≤ j ≤ 2·10^7 and every integer δ ∈ [−8, 10]
(vectorised one-step form; cross-checked against scalar `certify` and against route_c `sym_beta` words and classes for
all 5 ≤ Q < 10^6). Specific (chain, residue) entries are certified one by one. Levels (sources by parameter):

| level | sources | shallow entry classes (over-approximated: any chain unless "w") |
|---|---|---|
| A | Q ≤ N0 | exact: (Q, 1) for every Q |
| B | N0 < Q < T1 | 2 (a), 0 (b), (w, D−1) for D ∈ A(w) (root c) |
| C | T1 ≤ Q < T2 | B's, plus after deep chain 1 ∈ {0,2}: 3−D1, D1−1, (w, D1+D−2), D ∈ A |
| D | T2 ≤ Q < T3 | (w, D−1) D ∈ ABC; (w, D1+D−2) D1 ∈ {0,1,2}, D ∈ AB; (w, D2+D−2) D2 ∈ {−1..3}, D ∈ A; ints [−2,4] |
| OUT | H5_res entries of a source P < T3 (≤ 2 large-phase letters) | same shape as D |
| C7 | c landings of S(J), J < T4 | (w, θ+D−2): θ=1, D ∈ ABCD; θ ∈ [0,2], ABC; [−1,3], AB; [−2,4], A |

Each level also exports "generic" a-output classes valid at any chain (route-a chain 1: 2; deep→shallow a-steps:
3−θ), which enter the next level as all-chain integer entries.

**Results** (`levels_20000000.json`, `levels_run.log`):
* Bulk: δ ∈ [−8,10] uncertified only at (5,5) — the known bare tie; NT-gate counts reproduce the accepted window
  certificate (δ=−1: 68 gates; δ=5: 614; δ=−2, 6: ≈2.8·10^5, all certified).
* Levels A, B, C, D, OUT: **0 uncertified entries.**
* C7: **1 uncertified entry**: (5,5) from θ_1 = 2 and D = 5 at chain 5, provenance level C entry (244875, −1).
* Chain-5 a-output classes: A {2}; B {1,2,3}; C {0,1,2,3,5}; D {−1,0,1,2,3,5,14}.
* Shift spectrum Σ (by chain, residues mod 2^(ω+1), classified as small rationals with lift): see §0 item 3.

## 5. Consequences for each residual type, H5 and C7

### 5.1 H5 below T4 [A+B]
By DL(iii)–(iv) and §4, every deep→deep c step of S(J), J < T4, copies a deep a-output of history A, AA or BA, so its
ε ∈ {3,5}: H5(J) holds (and is stronger than H5_res). Theorem L (simple sources) is consistent with this; the new input
is that **no residual source exists below T4**.

### 5.2 Residual types (i)–(v) below T4
A residual source needs a source epoch S(P), P < G(n) < T3, whose source chain (ω ≥ N0) comes after its first shallow
entry. All such entries are certified (levels A–D/OUT), so later records stay < N0: impossible. Per type:
* (i) out-of-window entry class: entries are A/B classes in [−2,4] or C-entries (w, d+D−2) with D in the level sets;
  the only non-integer/out-of-window ones come from Σ_{<T3}'s gateway family and are certified [B].
* (ii) rational entry: rational shifts exist (4/3+2^m, −7/3) but every resulting entry is certified [B].
* (iii) C-entered bare tie: needs D ≡ 7−d or −9−d (mod 64) at a chain-5 a-output, d the large-phase class. With
  L = 0, 1, 2 large-phase letters (L ≤ 2 since P < T3) the nested source is < T2, T1, N0 and d ∈ {1}, {0,1,2},
  {−1..3}; the chain-5 sets {0,1,2,3,5}, {1,2,3}, {2} contain no target. **Excluded below T4; the work_claude_shift
  §5 [C] shape is an artifact** (it ignored that shift 4 at ω=5 must itself be produced by a source epoch, and no
  source below T3 produces class 6 or −10 at chain 5; even E_D lacks them).
* (iv) gateway output ≥ 10^8: Lemma CB needs the bare tie entered by A/B *directly* from a deep chain y; after L ≤ 2
  letters d_y ∈ [−1,3], so the entry classes 3−d_y, d_y−1 ∈ [−2,4] are never ≡ 5 (mod 16). Bare ties inside
  shallow walks have outputs ≤ 26 (`bulk.nt`). Excluded.
* (v) nested residual: large-phase C letters copy deep a-outputs of sources < T2, i.e. history A (simple). Excluded.

### 5.3 C7 below T4 [A+B]
All c landings (any ε) of S(J), J < T4, are certified except the family of §5.4. (a/b landings: only the accepted
A-entered bare tie (5,5) at θ_3 = −2, handled by the r1r2/C5_EXTENSION gateway; reported in `C7_ab_landings_uncert`.)

### 5.4 The BBBA family: a real G2 instance, absorbed
`c7_family.py` [B]: the 68 chains m0 < 2·10^7 with X(m0−1) odd b, ω = 17 (244875, 538715, 832554, …; 34 below 10^7,
33 of them in (499997, 10^7)); each entry (m0, −1) walks m0 →b 17 →a 5 with a-output class 5 at chain 5 (certified,
then 5→6→1). In a source S(Q) with word Q →b j1 →b m0 →b 17 →a 5 (automaton 1,0,−1,−2,5; ε = 9) the source chain is
(5, 5): **certified for the 6 landing bits but with automaton precision only 16** (the descent 17→5 drops x/2), while
the bare tie needs the bits above; for lifts 5+2^16 e the gate output varies (5, 6, 8) [B]. So the real class above
bit 16 is the clock residue of S(Q) (Lemma R0) — exactly G2.

*Construction [A-cond].* Take the first label-m0 fire (pointer ρ1), j1 := ρ1+2 (X(j1−1) is its b copy, ω = m0); the
first label-j1 fire (pointer ρ2), Q := ρ2+2; the first label-Q fire: its epoch has the word above, and its chain-5
a-output gives a c crossing n_c (ω=5, s = 3). Let k be a fire half-time with v2(3k+1) = n_c exactly and J := its
pointer+1. Then S(J): J →a (n_c+1, θ=2) →c (5, 2+3) — a C-entered bare-tie landing, ε = 9: **C7(J) fails.**
log2^(4) J ≈ m0, so J < T4 for m0 ≲ 10^7 and J > K_clock for m0 ≳ 499997 (log2^(4) K_clock ≈ 499997). Extra hypothesis:
the half-time k (Theorem CT gives the least k with 2^M | 3k+1, which has v2 = M only for M even; odd n_c needs a CT
variant or another label-Q fire) and DEF through these times (all labels ≤ n_c+2 < K_clock, so relative to EXT(<K_clock)).

*Absorption [A].* Chain 1 has phase exactly 2 (route a: β = 6k+2, Θ = 6k+4). By AB (PROOF_EXT) the walk from chain 1
copies the source epoch E = S(Q) from C on to its end, with records < J (Theorem RA). More generally (**AB′**, HP with
precision p): a deep chain with D ≡ 2 (mod 2^p), p > records of the copied tail, is absorbed; the copied tail of a
real epoch of label Q < J has records < Q ≪ p. So every θ_T = 2 landing is safe whatever its certification.
**Copy principle [A].** For a C letter at deep chain j_T with drift θ the landing equals the source chain with Θ
shifted by θ−2, to precision ≥ min(prec θ, n−ε(n)). θ = 2: the source epoch's own tail (EXT(Q), induction).
θ ≠ 2: the shifted reference G_{θ−2}(C) — a post-gate (G1) problem for a shifted reference, settled below T4 by §4.

## 6. Candidate theorem: EXT below T4 [A+B, pending review]

**Theorem T4 (candidate).** Inside the least strict-EXT counterexample induction, EXT(J) holds for every J < T4.
*Proof sketch.* C5_EXTENSION §4 (accepted): for J < T4, H5(J) ∧ C7(J) ⟹ EXT(J); its proof uses C7 only to know the
tail after an ε ≥ 7 c landing is safe with records < J. H5(J): §5.1. For the landing: §5.3 certifies it, except the
θ = 2 family, which AB/AB′ makes a copy of a completed real epoch of label Q < J (safe, records < J). Source epochs
are tie-free by the induction (Q < G(n) < J). ∎ Consequence to be checked by review: with the accepted finite-prefix
EGX/U/H″ assembly, no halt during the first 2^{T4}−2 top steps (T3 < K_clock < T4).
**Review checklist.** (1) DL(iii): completeness of the deep-history case split; the G-bounds at each depth.
(2) Soundness of the entry over-approximation in each level (every real shallow entry of S(Q), Q < T3, is listed).
(3) `rwalk.certify`/`bulk` = shiftlib Prop 3.2 certificate; precision of C-entries (S1 copy error ≥ ω+1).
(4) That C5_EXTENSION §4 needs nothing about ε ≥ 7 landings beyond safety of the tail. (5) AB′ statement.

## 7. Candidate lemmas, status, and where attempts fail

| statement | status |
|---|---|
| R0: s = D_src−2 exactly; s ≡ 3τ+3+2^ω | [A] + [B] |
| local no-go: MASS/CONE/clock bounds give no finite Σ | [A] |
| DL(i)–(iv) scale lemma | [A] (iii) inductive on §4 |
| Σ_{<T3} finite explicit (heights ≤ 3, rank ≤ 1) | [B] |
| H5(J), all residual types vacuous, J < T4 | [A+B] |
| C7(J) except BBBA/θ=2 family, J < T4 | [A+B] |
| C7 literal fails at some J ∈ (K_clock, T4) | [A-cond] (CT parity / DEF) |
| AB′ and copy principle | [A] (from HP, AB) |
| EXT(J) for J < T4 | [A+B] candidate, pending review |
| finite Σ for all J (uniform) | open; no proof attempt succeeded |

Attempt beyond T4 (where it fails): for J ∈ [T4, T5) the deep segment has 5 chains, θ_3 = −2 gives an A-entered
bare tie directly from a deep chain j_3 < T2 whose gateway output can be ≥ N0 (BBBAA, RES): the walk returns to deep
chains with a rational class 10/3+lift, outside C5_EXTENSION's Λ ≤ 4 framework. Source levels Q ∈ [T3, T4) already
produce gateway a-outputs (m, (10−2^m)/3) at *every* shallow m, so the next level needs all-chain bulk certification
of rational entries (d+(4−2^m)/3 at chain m). Each level adds 1 to the drift range and new rational families, so the
level sets do not stabilise by inspection; a uniform invariant on Σ_h is the missing ingredient for all J.

## 8. Refuted / corrected
* work_claude_shift §5 [C] "H5 probably NOT automatic below T4": **false** — H5 holds below T4 [A+B] (§5.1–5.2).
* "An uncertified source's shift is an arbitrary residue mod 2^(ω+1)" (heights review, G2): correct as a *local*
  statement (§2), but the *reachable* spectrum below T3 is the finite Σ of §4, and the one uncertified copy below T4
  is absorbed (§5.4).
* C7 as a uniform hypothesis on (K_clock, T4): not true literally [A-cond] (§5.4); replace by "certified or θ_T = 2".

## 9. Recommended next step
1. Three-way review of §3, §4 and Theorem T4 (§6), including an independent re-implementation of `levels.py`.
2. Level E (sources T3 ≤ Q < T4) and S(J) for T4 ≤ J < T5: add generic rational a-outputs (10−2^m)/3, (26−2^m)/3
   and their descendants; extend `bulk` to rational δ via a K-bit (K≈50) representative with ceiling min(j−loss, K);
   re-prove C5_EXTENSION's induction for Λ = 5 with gateway climbs (RATIONAL_MODE for the deep rational segment).
3. Track |Σ_h| and the maximal height/rank per level to look for an inductive invariant (the only route to all J).

## 10. Files and reproduction
Python with numpy (used: C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe, PYTHONUTF8=1, -B):

    python -B work_claude_residual/check_r0.py      # Lemma R0 checks -> r0_checks.json (~5 s)
    python -B work_claude_residual/levels.py        # level sets, certification -> levels_20000000.json (~85 s)
    python -B work_claude_residual/c7_family.py     # BBBA family data -> c7_family.json (~5 s)

`rwalk.py`: table loader, exact certificate `certify` (representative walk; one-step form for j ≥ 64) and its
vectorised `bulk` version. Validation: bulk = scalar certify on 64 ≤ j < 3·10^5 for δ ∈ {1, −1, 2}; certify(Q,1) =
route_c `sym_beta` (words and classes mod 2^j) for 5 ≤ Q < 10^6 (xcheck_bulk_vs_certify.py, xcheck_symbeta.py).
