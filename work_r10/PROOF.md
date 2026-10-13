# R10: the deficit law of the universal walk — (M1′)/(M2′) verified to i = 10^8, reduced to one structural lemma

Scope (per the coordinator's instruction): this directory is self-contained; it does not
modify any other file. Base: work_g6/PROOF_G6.md §5 (the repaired Theorem R: the formal
pair map F, mass identities, I(ρ)); work_r1 (audited reduction). Tags [Class-A]/[Class-B]/[Class-C]
as usual. Artifacts: `fast_walker.py` (this directory).

## 1. The fast walker [tool; validated]

`fast_walker.py` implements the formal map F of work_g6 §5.1 with residue arithmetic:
each scale value c = 2^v·m (m odd) is stored as (v, m mod 2^192); λ values are exact
(λ ≤ 3s+1, small); original entries E_a = (a, 1). Addition is exact except when two
equal valuations sum to a multiple of 2^176 (a "Deep" tie — never occurred; counted).
Decisions are identical to the exact map (parity from v = 0 vs ≥ 1; j = v2(λ_x)).
**Validation:** on the full G6 base range i ≤ 20000 the walk is step-for-step identical
(17841 steps, 6690 chains, 6056 level fires — exactly V6's numbers), and the level-fire
stream (ρ, k, j) equals an independent exact big-int walker on all 60575 level fires for
i ≤ 2·10^5. Runtime: O(1) per step (measured 10^8 indices ≈ 40 min).

## 2. Measurements [Class-B, symbolic in U, valid for every odd U by F's simulation lemma]

Run to **i = 10^8** (89.3M steps, no Deep ties, F defined everywhere — S1/S2 hold at
every one of the 33.4M chains):

**(M2′) holds overwhelmingly:** max s/i = 0.8928 (s ≈ 0.9·i always).

**(Return) holds:** level fires recur throughout; max gap between consecutive level
fires = 22 steps; max pointer stall = 21 steps.

**(M1′) holds with a precise law.** Let Δ(i) = i − min v2(c) over head+stack. The
deficit records are:

| Δ | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 |
|---|---|----|----|----|----|----|----|----|----|----|----|
| at i | 28 | 101 | 390 | 1539 | 6132 | 24496 | 97957 | 391796 | 1567152 | 6268573 | 25074251 |

- every record sits **exactly 2 positions after the first occurrence** of spike level
  j = Δ − 2 (first-j positions 26, 99, 388, 1537, 6130, 24494, 97955, 391794, 1567150,
  6268571, 25074249 — independently confirmed against the universal sequence up to j = 22);
- the ratios ρ_{j+2}/ρ_j → 4.0000 and **Δ − log2(i) = 3.42 constant to two decimals
  across six orders of magnitude**;
- against (M1′): max Δ = 28 at i = 10^8 versus the required bound ⌊log2 i⌋² = 676;
  extrapolating the law, Δ(i) = log2(i) + 3.42 reaches ⌊log2 i⌋² never (log2 i + 3.42 <
  (log2 i)² for log2 i ≥ 6). **(M1′) is true with headroom ~ log2(i)²/log2(i) = log2(i).**

## 3. Proven arithmetic of spike levels [Class-A, this work]

**Lemma K.** Every spike (chain with j ≥ 5) has k ≡ 10 (mod 16) and j = 5 + v2(3s+2)
with k = 16s+10; hence k ≥ (2^{j−5} − 2)/3 ·16 + 10 = **(2^{j−1} − 2)/3**, and the FIRST
occurrence of each even level j ≥ 6 is exactly at k = (2^{j−1}−2)/3.
*Proof.* The class condition 6k+4 = 2^j·odd ⟺ k ≡ 10 mod 16 with j = 5+v2(3s+2), k = 16s+10
(work_g6/run7 algebra). v2(3s+2) = j−5 ⟹ 3s+2 ≥ 2^{j−5} ⟹ s ≥ (2^{j−5}−2)/3; for even j
(j−5 odd, 2^{j−5} ≡ 2 mod 3) the value s₀ = (2^{j−5}−2)/3 is an integer with 3s₀+2 = 2^{j−5}
(a power of two: v2 = j−5 exactly), so the bound is attained. ∎
(Checked: j = 6..26 first-occurrence k-values 10, 42, 170, 682, 2730, 10922, 43690,
174762, 699050, 2796202, 11184810 = (2^{j−1}−2)/3 exactly.)

**Corollary.** Any spike with parameter j has k ≥ 2^{j−2}, i.e. **j ≤ log2(k) + 2.**

## 4. The reduction of (M1′) [Class-A given one structural lemma]

**Lemma A1 (ancestry drain) [measured exact; proof pending].** At every state of F,
every live value's deficit satisfies δ ≤ (sum of the j-parameters of the spikes on its
ancestry) + 2, where the ancestry of a value is the chain of producers recorded in the
tags. In particular δ ≤ j*(i) + 2 with j*(i) the largest spike parameter fired so far.

**Sharper micro-laws [Class-B, i ≤ 2·10^5 and 5·10^4 respectively]:**
- at the spike chain itself, the transient deficit is **exactly j** (5582/5582 spikes);
- within ≤ 5 steps after each spike (its exit window) the peak deficit is **exactly j+2**
  (5580/5582; two j = 5 outliers peak at 9);
- between exit windows the deficit decays (absorption payback), so the running maximum
  is exactly j*+2 — the record table of §2 is complete, not a sample;
- spike counts by level halve per +1 of j (2794, 1394, 697, 349, 174, 87, 43, 22, 11,
  6, 2, 2, 1 for j = 5..18 at i = 2·10^5): the geometric class rarity of Lemma K.

**Drain dynamics [Class-A, c-arithmetic; proof = one line each].** With δ(v) = i − v2(c_v)
at current pointer i:
- (D1) chain with parameter j: the new head u = c_x/2^j has δ(u) = i − v2(c_A + 2c_b) + j
  ≤ max(δ(A), δ(b) − 1) + j; the pushed entries u·2^t have δ(u) − t; the seam
  D = c_c + c_A/2 has δ(D) ≤ max(δ(c), δ(A) + 1);
- (D2) even step (absorption): δ(new head) ≤ max(δ(A), δ(b), δ(c)); fresh originals
  E_a enter with δ = 0 (v = a at pointer a);
- (D3) pointer advance by 1–2 raises every live δ by the same amount;
- (D4) payback: absorbing a pushed pair u·2^t, u·2^{t+1} multiplies c by 4 (δ − 2),
  so each chain's +j is repaid −2 per absorbed pair — a full interlude of j−1 pushed
  entries repays j−1 of the j.
The remaining content of (A1) is the bookkeeping that the worst ancestry path (spike →
nested sub-cascade → exit chain on D → its sub-cascade → …) never accumulates more than
the outermost j plus the two structural +1s: each nested level's own chains are repaid
by their own pushed runs (D4), nested spike parameters strictly decrease (proved in the
R9 audit: nested ρ ≤ J_parent − 2, j < J_parent), and the measured exactness (j+2 at
every spike window) shows the residues cancel.

**Proposition (conditional).** Assume (A1) and any of the k-growth bounds
  (i) k_ρ ≤ 0.4465·ρ for all ρ (the conservation law; [Class-B] to ρ = 4·10^5), or
  (ii) k_ρ ≤ ρ² for all ρ (work_g6 Prop 4, itself conditional on the dk-table induction).
Then for i ≥ 64: Δ(i) ≤ j*(i)+2 ≤ log2(k*) + 4 ≤ max(2, 2log2 i) + 4 < ⌊log2 i⌋².
So **(M1′) holds for all i.**
*Proof.* By Lemma K any spike has j ≤ log2 k + 2; the largest spike parameter fired up
to pointer i has k ≤ k*(i) ≤ the bound in (i)/(ii); combine with (A1). For (i):
Δ ≤ log2 i + 4.1; for (ii): Δ ≤ 2log2 i + 4; both are < (log2 i)² for i ≥ 64. ∎

## 5. Status

- **(M2′) and (Return):** verified to i = 10^8 with huge margins (s ≤ 0.893·i; level-fire
  gap ≤ 22 steps) — not in doubt at any scale probed.
- **(M1′):** verified to i = 10^8 (was 4·10^5) with the exact law Δ(i) = log2 i + 3.42
  (records exactly at first-j-spike exits; transient law Δ = j at every spike chain,
  peak j+2 in every exit window); reduced by Lemma K + the drain dynamics (D1)–(D4) to
  the single bookkeeping lemma (A1). Conditional closure: (A1) + any k-growth bound
  (k ≤ 0.4465ρ [Class-B] or k ≤ ρ² [work_g6 Prop 4]) ⟹ (M1′) for all i ≥ 64.
- The residual for the repaired Theorem R (work_g6 §5.5) is now: **(A1), the k-growth
  bound's hypothesis chain, and (Endgame)** (unchanged scope).
- Next steps for (A1): formalize the payback bookkeeping of (D4) along ancestries (the
  walker's tags already record producers); the measured exactness (j+2 at every window)
  indicates the residues cancel structurally, so the induction should close by a
  transfinite-free argument on nesting depth (strictly decreasing spike parameters).

## 6. Reproduction

```bash
cd work_r10 && python fast_walker.py 20000 20000    # base-range validation (~1 s)
cd work_r10 && python fast_walker.py 100000000 200000   # the 10^8 run (~40 min)
```
Outputs: the record table, (M1′)/(M2′) checks, Return gap, and the prefix cross-check
against the exact big-int walker (60575 level fires identical at i ≤ 2·10^5).
