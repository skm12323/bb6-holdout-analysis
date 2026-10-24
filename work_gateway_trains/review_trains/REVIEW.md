# REVIEW — adversarial + audit of the four Astra train documents (+ five budget docs)

Reviewer: ZCode adversary/auditor, 2026-10-24, `work_gateway_trains/review_trains/`.
Scope: `work_c3_drift/{GATEWAY_TRAIN, CLOCK_FILTERED_TRAIN, TRAIN_CLOCK_ORBIT,
CROSS_SCALE_TRAIN}.md` (full, claim by claim), secondary lighter review of
`{DEPTH_CLOCK_BUDGET, SEED_BUDGET, COPY_BUDGET, JOINT_HEIGHT_BUDGET,
STOP_CHECKPOINT_2026_10_21}.md`. Imports used: CONTEXT.md chain formalism,
work_landing_symbolic THEOREM.md (review-correction block), work_claude_shift NOTES,
CHECKPOINT work_c3_drift/work_claude_shift/work_landing_symbolic sections.

Independent artifacts in this directory (all rebuilt from scratch, no reliance on
Astra's verifier logic for any verdict):

- `review_checks.py` / `review_checks.json` — every quantitative claim re-derived
  (random exact-Fraction instances of each identity, my own graph rebuilds from
  `Calendar(256)` k-data, my own streaming lambda-walk to n<10^8, my own exact
  cross-scale replay both via Calendar and via an independent `lam_walk` table,
  my own exact walkers for the STOP family). Exit 0 = all pass.
- Reruns (patched copies, outputs here): all four train verifiers and all six
  budget verifiers PASS with the published counts.

Verdict summary: **no claim is refuted**. All four main documents are acceptable
with the labels given below; the only findings are presentation/justification gaps
(listed in "Error list"), none of which changes a theorem statement.

---

## 1. GATEWAY_TRAIN.md

| # | Claim (section) | Tag | Basis |
|---|---|---|---|
| GT-1 | §1 two-a recurrences `y_i=-x_i/2+2Θ_i+6`, `x_{i+1}=x_i/4+Θ_i+15+6k_i`, `Θ_{i+1}=Θ_i+12+6k_i` | [A] | Hand re-derivation (X(4) step with k=1, then X(m_i−1) step with half-time k_i; τ=2k ⟹ 3τ=6k) + 500 random exact Fraction instances. Check `GT.S1.recurrences`. |
| GT-2 | §1 `y_{i+1}-y_i/4 = Θ_i+21+9k_i` | [A] | Same (eliminate x_i). |
| GT-3 | §1 `4y_{i+2}-5y_{i+1}+y_i = 12(4-k_i+3k_{i+1})` | [A] | Difference of two GT-2 relations + Θ recurrence. |
| GT-4 | (TRAIN) `v2(4-k_i+3k_{i+1}) ≥ min(m_i-2, m_{i+1}-2, m_{i+2})`, v2(0)=∞ | [A] | Min-occurs-twice applied to the four-term zero sum `4y_{i+2}-5y_{i+1}+y_i-12Z_i=0` gives `2+v2(Z_i) ≥ min(m_i, m_{i+1}, m_{i+2}+2)` — exactly TRAIN after subtracting 2 from the first two terms only. The subscript asymmetry (m_{i+2} carries the +2 in the four-term form, no −2) is **correct**: the y_{i+2} term enters multiplied by 4. Verified unconditional on 400 random instances (`GT.TRAIN.min_twice`). |
| GT-5 | §1 scope: necessary for any exact trajectory, canonical or not; must not cross unresolved ties; a claimed train must supply its transitions | honest | Necessary-condition framework; no circularity: "valid segment" = word whose displayed returns are odd-a with the displayed parameters; TRAIN is then forced. Displayed numerators are nonzero by construction (parameters are their v2). |
| GT-6 | §2 `5≤m<8`: only odd-a label is m=5 (k=1), v2(6)=1<3 | [A]+[B] | Calendar: X(4) odd a τ=2 (accepted), X(5) odd b (accepted), X(6) **even** type c (verified Calendar + table_1000000). So labels 6,7 do not exist; label 5 excluded. |
| GT-7 | §2 `m≥8`: `0<4+2k_m ≤ (m-1)^2+4 < 2^{m-2}` ⟹ no `5,m,5,m,5,m` | [A] with C1 note | Quadratic: base m=8 (53<64) + successive ratio <2 (verified symbolically and 8..4096). The step `2k_m=τ(m-1) ≤ (m-1)^2` holds: τ≤n verified n<10^8 (my streaming walk), and all-scale τ(n)≤n·P(n)≤n² for n≥2697 (P(n)=2⌈log2(6n²+5)⌉²+1345≤n from n=2697). Doc attributes this to "C1" without the derivation — see Error list LOW-1. All 76 labels ≤256 checked: v2(4+2k)<m−2. |
| GT-8 | §2 "each complete return to five costs two loss units"; varying labels not excluded | [A]/honest | Two a-steps, Γ+1 each. |
| GT-9 | §3 (BAND): labels in [L,M], `4+2(M-1)^2<2^{L-2)` ⟹ Z_i=0 ⟹ `k_i=3k_{i+1}+4`, i.e. `k_i+2=3(k_{i+1}+2)`; hence `3^{s-1}≤k_0+2`, `s≤1+⌊log_3(k_0+2)⌋` | [A] | Algebra verified (300 instances `GT.S3.band_algebra`); k_{s−2}≥1 ⟹ k_{s−2}+2≥3. Same C1 note for |Z|≤4+2(M−1)². |
| GT-10 | §3 applies only where C1 estimate holds; inter-scale gap acknowledged | honest | — |
| GT-11 | §4 graph: 76 labels, 5776 vertices, 1433 edges, **cyclic** (no train-length bound certified) | [B] | Rebuilt independently from Calendar(256) odd-a k-data (my own code): 76/5776/1433 exact; cyclic. `GT.S4.graph_rebuild`. |
| GT-12 | §4 cycle (8,244,81,27): advance Σ(12+6k)=960, v2=6, max pair precision 81; exact repetition would need 2^81 \| 960 — false | [A]+[B] | k = 2,106,34,10 (Σk=152 ⟹ 48+912=960 ✓); e=max min(a−2,b)=min(242,81)=81 ✓; 2^81∤960 ✓. Pair clock constraints Θ_i≡−21−9k_i (mod 2^{min(a−2,b)}) around the cycle are mutually consistent (CRT verified) so a single traversal is not excluded — matches the doc. |
| GT-13 | §5 verifier contents (144 substitutions, 76 diagonal, quad 8..4096, saved cycle) | [B] | Rerun PASS in this directory, counts identical. |

**GATEWAY_TRAIN verdict: ACCEPT.** Core identities [A], graph facts [B], no misused
sufficiency, cycles honestly reported.

## 2. CLOCK_FILTERED_TRAIN.md

| # | Claim | Tag | Basis |
|---|---|---|---|
| CF-1 | §1 y≡0 (mod 32) ⟹ Θ≡5 (mod 16) at a five-chain (x=32u, u odd) | [A] | 2Θ+6−16u≡0 (mod 32) ⟹ Θ≡8u−3≡5 (mod 16); brute-forced over residues. |
| CF-2 | §1 two five-clocks differ by 12+6k_i ⟹ k_i≡6 (mod 8) | [A] | 12+6k≡0 (mod 16) ⟺ k≡6 (mod 8); brute-forced. |
| CF-3 | §1 only odd-a label <8 is m=5 (k=1) ⟹ internal m_i≥8 | [A]+[B] | X(5) odd b, X(6) even (see GT-6). |
| CF-4 | (ENTRY) pair relation modulus ≥16 (m_i≥8) + Θ≡5 (mod 16) ⟹ k_i≡6 (mod 16); applies to every label but the last | [A] | −21−9k≡5 (mod 16) ⟺ k≡6 (mod 16); brute-forced; layered mod-8 → mod-16 derivation is strict (both five-clocks ≡5 mod 16 give mod 8; the pair relation with e=min(m_i−2,m_{i+1})≥5≥4 upgrades to mod 16). |
| CF-5 | §1 audited base through index 15 ⟹ internal label ≥17 | [B] | Labels 5..16 odd-a with k: {5:1, 8:2, 12:4, 14:5} — none ≡6 (mod 16); smallest with k≡6 (mod 16) is 17 (k=6). Internal labels ≤256: {17,54,90,125,161,198,234} — matches verifier. |
| CF-6 | §1 internal label's source crossing has fire parameter 1+v2(3k+2)=3 | [A] | k=6+16t ⟹ 3k+2=4(5+12t), odd cofactor ⟹ v2=2 exactly. (Converse caution, not used by the doc: fire parameter 3 ⟺ k≡6 mod **8**.) Real-source provenance: odd-a crossings ↔ fires (each epoch's first crossing), pointer = fire pointer. |
| CF-7 | §2 among {m_i, m_{i+1}, m_{i+2}+2, 2+v2(Z_i)} the minimum occurs ≥ twice (omit last if Z_i=0) | [A] | This is exactly min-occurs-twice for the four-term zero sum of GT-3 — consistent with TRAIN (verified). |
| CF-8 | (DROP2) Z_i=0 ⟹ k_i>k_{i+1} ⟹ m_i>m_{i+1} (τ nondecreasing in index) ⟹ distinct valuations ⟹ m_{i+2}=m_{i+1}−2 | [A-imp]+[A] | Valuation step is unconditional algebra (verified on 400 forced Z=0 instances). τ nondecreasing: structural calendar fact (corrected in review: crossings of an epoch do NOT share the fire time; the reason is that s is nondecreasing inside an epoch and the epoch-final s equals the next fire time) + verified n<10^8 (streaming, `STREAM.big`). |
| CF-9 | §2 two internal labels m_{i+1}, m_{i+1}−2 would be two param-3 fires at pointer gap 2 — impossible ("kernel advances pointer by five") | [B]+structural | Calendar constants: a J=3 epoch occupies exactly kernels[3].advance=**5** pointers (epoch_crossings asserts offset==advance), so the next fire is at rho+5; together with the structural fact that odd type-a crossings are exactly fire pointers (mid-epoch 'a' rows occur only for odd s, where head lambda=3s+1 is even). (Corrected in review: weights[2]=10 is the aggregate step of 3 consecutive fires, not an alternative successor.) Verified empirically: their 899 gaps over n<16381 (rerun PASS) and my streaming walk over n<10^8 — **minimum observed gap 12** (5,488,724 param-3 odd-a crossings, none closer than 12). The doc's one-sentence justification is complete (see corrected MED-1). |
| CF-10 | §3 band version: four labels in [L,M] with (BAND) ⟹ Z_0=0 ⟹ DROP2 ⟹ param-3 gap 2 — contradiction ⟹ ≤3 catapult labels | [A] | Logic chain verified; size inputs as GT-7/GT-9. |
| CF-11 | §3 [5,16381] version: first three internal ≥17 ⟹ 2^15 \| Z_0; k_i≤8190 ⟹ \|Z_0\|≤32764<2^15 ⟹ Z_0=0 ⟹ same contradiction | [A]+[B] | Arithmetic verified; actual max half-time over odd-a crossings below 16381 is 7305 (so |Z_0|≤29224 in fact, ≤32764 with the doc's bound). The import "τ(n)≤n for n<10^8" is now **verified by me over the full range** (streaming walk to n=10^8 in 29 s: max τ(n)−n = 0, τ monotone, param-3 gaps ≥12; table_1000000 typ/tau/odd reproduced crossing-by-crossing). |
| CF-12 | §3 uniformity statement ("not an assertion that all other continuations end") | honest | — |
| CF-13 | §4 revised graph [5,256]: 532 vertices, 14 edges, acyclic, ≤3 catapult labels, longest (17,125,5), shared initial clock consistent (residue 32693, precision 15); (8,244,81,27) excluded by ENTRY (k_8=2) | [B] | Rebuilt independently with my own admissibility + TRAIN + repeated-min code: 532/14/acyclic/max 3/path (17,125,5) exact; initial-clock replay consistent, residue 32693 mod 2^15; 12+6·2=24≢0 (mod 16) excludes the old cycle. Direction of use is sound: necessary conditions cut the graph, so an acyclic necessary graph upper-bounds *actual* trains. |
| CF-14 | §4 checker contents (16381 linear clock bounds, 899 p3 gaps) | [B] | Rerun PASS. |
| CF-15 | §5 missing pieces (b/c interruptions, re-entry, no total-r bound) | honest | — |

**CLOCK_FILTERED verdict: ACCEPT.** ENTRY/DROP2/no-four are [A] (with the two
[B] calendar inputs now verified to 10^8), graph facts [B].

## 3. TRAIN_CLOCK_ORBIT.md

| # | Claim | Tag | Basis |
|---|---|---|---|
| TO-1 | §1 (CLOCK-ORBIT) internal labels ≥L≥17 ⟹ u_i=(k_i+2)/8 odd; Z=8(3u_{i+1}−u_i)≡0 (mod 2^{L−2}) ⟹ u_{i+1}=3^{−1}u_i (mod 2^{L−5}) | [A] | Algebra verified (200 instances). Note Z=8(3u'−u) ⟹ modulus drops 3 bits exactly as stated. |
| TO-2 | §1 boundary: L=17 conclusion covers u_0..u_{s−3} only; last two labels not automatic | honest+correct | Triples among internal labels give relations for i≤s−4 (conservative reading, actually i≤s−3 under "all labels ≥L"; the doc's caution is the safe direction). |
| TO-3 | §2 ord(3 mod 2^a)=2^{a−2} (a≥3) ⟹ forced-orbit period p_L=2^{L−7}; L=17: 1024 | [A] | Classical (LTE v2(3^{2^t}−1)=t+2, proof exists in ORBIT_SHIFT_OBSTRUCTION §); verified numerically a=3..26. |
| TO-4 | §2 same label twice in covered portion ⟹ distance multiple of p_L ⟹ ≥2·p_L loss units (2048 at L=17) | [A] | u_i determined by k_i, hence by the label. |
| TO-5 | §3 residues over a period = one coset of ⟨3⟩ = {1,3 mod 8} or {5,7 mod 8}; coset sums 4N(2N∓1), N=2^{a−3}, v2=a−1; higher lifts cannot change it; Δ=48Σu_i ⟹ (ADVANCE) v2(Δ)=L−2 | [A] | Coset membership and sizes verified; sums verified exactly a=3..22; lift invariance is rigorous: Σu_i = 2^{a−1}·odd + 2^a·M ⟹ v2 exactly a−1 (verified on random lifts); ADVANCE verified L=17..20 ×4 starts. |
| TO-6 | §4 one exact period cannot repeat as source pattern: pair constraints force 2^{e_i}\|Δ; some label >L (else all clocks identical, contradicting distinct residues, p_L>1) ⟹ some e_i≥L−1>v2(Δ)=L−2 | [A] | Logic verified: e_i=min(m_i−2,m_{i+1}) at the pair *starting* at the >L label is ≥L−1 and that pair exists within the repeated pattern. Odd multiples of the period also excluded (odd sum of terms each v2=L−2 keeps v2=L−2). Even multiples/nonperiodic/interrupted honestly left open. |
| TO-7 | §5 1,044,480 orbit points, L=17..24 ×4 starts; arithmetic controls only | [B] | Rerun PASS; count matches 4·Σ2^{L−7}. |
| TO-8 | §5 scope: no b/c interruption control; parameter-49 shift obstruction reachable via b/c ancestry outside the pattern; no arbitrary-ancestor denominator claim | honest | — |

**TRAIN_CLOCK_ORBIT verdict: ACCEPT.** All sections [A]/[B]; the ADVANCE
lift-invariance sentence is correct as stated.

## 4. CROSS_SCALE_TRAIN.md

| # | Claim | Tag | Basis |
|---|---|---|---|
| CS-1 | §1 fires: k_a=819270 @ pointer 1836654, k_b=229398 @ pointer 514272, both parameter 3 | [B] | `preceding_fire_by_time(2k)` on Calendar(256): k/pointer/J all match, J=3 (v2(3k+2)=2 exactly); crossing data confirmed a second way via lam_walk table (τ(a−1)=2k_a etc.). |
| CS-2 | §1 construction Y0=2^a, Y1=2^b+2^{a+10}, Θ0=Y1−Y0/4−21−9k_a, X0=4Θ0+12−2Y0; v2(X0)=5; solves the first two five-output equations | [A]+[B] | Equivalence to y_0=Y0, y_1=Y1 verified by hand; v2(X0)=5 verified exactly (X0/2 = 2^{b+1}+2^{a+11}−5·2^{a−2} − 144·(odd), the last term v2=4 dominates the valuation since b+1≫4). |
| CS-3 | §2 word 5,1836655,5,514273,5,17,5,17,19; X(18) even; losses 0..8; max record a+1=1836656; precision a+2 certifies the tail | [B] | Two independent replays by me: (i) my own exact Calendar walk (Fractions, own step code), (ii) my own a-step evaluator over an independently built lam_walk(a) table. Word, losses, records identical; X(18) even (Calendar + table). |
| CS-4 | §2 guiding clock identities 4−k_a+3k_b=−2^17; 4−k_b+3·6=−7·2^15 | [B] | Exact; these are exactly the TRAIN divisibilities at the triples (a,b,17) (v2=17 ≥ min(a−2,b−2,17)) and (b,17,17) (v2=15 ≥ min(b−2,15,17)) — verified. The fourth label 17 is the last catapult (no y_4), so no (17,17,19) triple exists; no TRAIN violation (19 is the X(16)-output chain, not a five-output). |
| CS-5 | §2 normalized residues mod 4096 = 9,3,1 matching the forced inverse-3 orbit; repeated 17 at the boundary not covered by the internal-orbit conclusion | [B]+[A] | u_a=102409≡9, u_b=28675≡3, u_17=1; 3^{−1}·9≡3, 3^{−1}·3≡1 (mod 4096). Boundary honesty correct: the (17,17) pair needs a following catapult for TRAIN/CLOCK-ORBIT; the walk ends instead. |
| CS-6 | §2 labels outside [5,16381]; contradicts only a hypothetical all-scale 3-catapult cap, respects the proved band/finite-interval statements | honest | Correct: CLOCK_FILTERED §3 is stated for [5,16381]; a=1836655 is far outside. |
| CS-7 | §3 v2(D+3)=3, (D+3)/8≡3 (mod 8); for every H≥6 ∃r≥0 with c_r=−3+8/3^r≡D (mod 2^H); at H=a+2 HP transfers the whole trace (max record H−1) | [A]+[B] | Unit ≡3 (mod 8) lies in ⟨3⟩ mod 2^{H−3} ⟹ exponent exists. Verified concretely: solved the 2-adic dlog mod 2^48 (witness r=50969618443259, 3^r=(unit)^{−1} mod 2^48 exactly), and replayed the walk from an integer representative (X0, X0+(D mod 2^{a+2})) — identical word, all records < a+2 (HP mechanics at the full 1.8M-bit precision). "Existence, not joint reachability" honesty preserved (no claim that the orbit history generates r together with X0). |
| CS-8 | §4 two replays, SHA-256 fingerprints, ~1.84M-bit integers | [B] | Rerun PASS; my independent replay agrees; x has 1836667 bits; fingerprints recomputed and match the saved json. |
| CS-9 | no K_clock change, no EXT claim | honest | — |

**CROSS_SCALE verdict: ACCEPT** as a *construction* witness (non-canonical initial
state, explicitly flagged). No overreach found: every "does not assert" sentence in
the document matches what the construction actually provides.

## 5. Secondary documents (lighter review)

### DEPTH_CLOCK_BUDGET.md — core [A-cond], instance data [B]
- Identity `D=51+27k+(11/4)y−3z`, E0=min(m−2,n): **[A]** — re-derived (z=Θ+21+9k+y/4 from the pair relation, x=4Θ+12−2y) and verified on 300 exact instances; v2((11/4)y)=m−2 decomposition verified.
- DEPTH-SOURCE `3^{r+3}u≡1 (mod 2^{E−3})`, k≡6 or 22 (mod 64): **[A]** — exact equivalence 8/3^r=8·27u (mod 2^E) ⟺ 3^{r+3}u≡1 (mod 2^{E−3}) verified symbolically (51+27k+3=27(k+2)=8·27u for k≡6 mod 16).
- Cross-scale instance (u=102409, E0=514273; 3^r=(27·102409)^{−1} mod 2^514270; 256-bit reduction fixes r mod 2^254 with least residue 12538...2907): **[B]** — I verified pow(3,claimed,2^256)=(27·102409)^{−1} mod 2^256 exactly and claimed<2^254. Next pairs E0=17,15 ✓.
- §3 paired-gateway budget (Z=Q(9k+12)+C≠0 by 3∤C; |Z|<2^{3j/4+1}<2^{j−4} for j≥N0; m=v2(Z)≤j−5; class denominator exactly 3Q; Potential drop ≥1): **[A-cond]** — algebra and arithmetic verified (potential drop 200 instances; size-chain inequality checked at sample j; hypotheses κ<2^{j/2}, B≤2^{j/2}, j≥4(d+2), N_Q imported from ODD_DENOMINATOR, which the checkpoint accepts as [A-cond] §1). Verifier rerun PASS (80 pair identities).
- §4 limits (starting potential a hypothesis; DEPTH-SOURCE necessary not sufficient): honest.

### SEED_BUDGET.md — core [A-cond], small cases [B]
- a-parent `m=v2(9k+θ+12)` (θ=−2/14) with y₂=(5/4)x+D+9k+12: **[A]** — identity verified on 300 exact instances (y₂ formula exact; m matches whenever v2(9k+θ+12)<j−1). Polynomial 4.5(j−1)²+26<2^{j−5} + ratio persistence verified; Γ_new+m+2<Γ+j arithmetic verified for both loss patterns.
- b-parent `x₂=(13/8)x+2D+9k+10`, m=v2(9k+2θ+10): **[B]** (their verifier, 114 canonical-call checks, rerun PASS). Note: this exact formula is equivalent to x₅=(3/4)x+6k+4; the derivation is not shown in the doc and I did not re-derive it independently — keep it [B]-tagged (Error list LOW-3).
- c-history reference z₂ forms (A: 9k+19/−13; AA: 9k+22/−10; BA: 9k+16/−16) from z₂=(3/2)z+2d+6: **[A]** — verified exactly; forced k minima (v2(6k+2)=5 ⟹ k≡5 mod 32 etc.) verified; positivity then holds (9·5−13=32>0 etc.). Small exception s=14 (A, k=5, m=6/5) present in verifier output.
- Source-margin table and assembly: conditional; §4 limits honest. Verifier rerun PASS (568 checks).

### COPY_BUDGET.md — core [A-cond], controls [B]
- Exact copy identity D'=D+Φ−2+(2^j−c'u) and class rule mod 2^{ω+1}: **[A]** — verified on canonical odd b/c crossings with real Calendar coefficients (my check).
- Rank transfer r_new≤max(r_p,r_s) (lcm of 3-power denominators): **[A]** elementary.
- (SOURCE-RESERVE) ⟹ V−V_new = σ−ω−2(r_new−r_p) ≥ ρ−P ≥ 1 (σ=ρ−G_s from the accepted coefficient ledger): **[A-cond]** — derivation re-verified step by step; composition arithmetic randomized.
- Negative control at n=5 (P=1, G_s=0, ω=1, σ=4, phase 1; 31/27≡1 mod 4; rank-3 budget 7>1; potential +3): **[A]+[B]** — verified (X(5) odd b, ω=1, Φ=1; congruence and arithmetic exact; verifier rerun PASS with the same failing control).
- §4 well-founded-induction contract: correctly framed as a target, not a theorem; height/rank tradeoff honesty ok. Verifier rerun PASS (6160 b + 440 c copies).

### JOINT_HEIGHT_BUDGET.md — core [A-cond]
- Height identities h(3−c)=h(c), h(cp+cs−2)≤h(cp)+h(cs)+1, h(4+c/3)≤⌈(h+8)/3⌉≤h+3: **[A]** — verified on full rational grids (c ∈ (1/9)·[−60,60] etc.).
- Copy composition W_new−W_parent ≤ −(ρ−P)+1 and drop ≥2 under ρ−P≥3: **[A-cond]** — composition arithmetic randomized; **ρ−P≥3 verified**: fires with ρ<16 are exactly {4,7,11,13} with gaps {3,3,9,12} (recomputed from Calendar), and for ρ≥16, 2^P≤3τ(ρ)+4≤3ρ²+4<2^{ρ−2} (base 772<2^14 at 16, ratio persists) forces P≤ρ−3. (Same C1 shorthand note on τ≤ρ² — valid via table+P(n)≤n for n≥2697.)
- §3 large paired gateways m≤j−8 (j≥N0>32) and W-drop ≤−1: arithmetic verified (3j/4+1<j−7 ⟺ j>32).
- §4 seeds: h(10/3)=2, h(26/3)=7, charge 9; ρ≥P+11 for P≥14 (base 3·24²+4=1732<2^14, ratio persists); two-step drops ≥13 (A) and ≥14 (AA/BA) — all arithmetic verified. Verifier reruns PASS (720 copies, 20 reflection/gateway, 216 paired).

### STOP_CHECKPOINT_2026_10_21.md — [A] obstruction family + [B] walks
- u=(2^{m−4}−1)/3 odd, x=32u, Θ=x+5 ⟹ x'=3x/2+16=2^m: **[A]** — verified exactly for m∈{6,8,...,64}.
- Entry W=8<9 (c=5, r=0, h=3) yet next record m+1≥9 for every even m≥8: **[A]** — the O2-type disproof of unconditional local sufficiency of the joint reserve. Correct and important.
- m=6 word (5,6,1), max record 7, intermediate normalized weighted value 11: **[B]** — my exact walk reproduces (5,6,1); W=11 under the lift-bit-separate bookkeeping (Γ=1, j=6, c=10/3, r=1 ⟹ 1+6+2+2). m=8 word (5,8,3), max record 9 (precision 10): **[B]** — reproduced.
- Honesty (constructed states, not S(J), no contradiction with conditional macro lemmas): ok. Verifier rerun PASS (126 cases).

## 6. Error list

**HIGH:** none.

**MEDIUM:** (none after review; MED-1 downgraded to LOW)

**LOW (formerly MED-1):**
1. (MED-1, CLOCK_FILTERED §2) The sentence justifying "two parameter-3 source fires
   cannot be separated by only two original positions" cites only the kernel-3
   advance (5). (Corrected in review: this is already complete — a J=3 epoch occupies exactly
   5 pointers and odd type-a crossings are exactly fire pointers; the earlier "2²-jump /
   weights[2]=10" branch was a misreading of an aggregate step.) Plus the empirical
   check (verified to n<10^8 by this review's streaming walk). Only the premise "odd
   type-a crossings are exactly fire pointers" should be stated explicitly in the doc.

**LOW:**
2. (LOW-1) "C1" is used as an unexplained shorthand in GATEWAY_TRAIN §2/§3 and
   JOINT_HEIGHT §2 for the accepted CLOCK bound τ(n)≤n·P(n). The specific derived
   inequalities τ(n)≤n² (and, in CLOCK_FILTERED §3, τ(n)≤n) are correct, but the
   doc should spell out the derivation: table τ≤n for n<10^8 (now verified by this
   review over the whole range) and n·P(n)≤n² for n≥2697. No statement changes.
3. (LOW-2) GATEWAY_TRAIN §1 "valid segment" should state explicitly that all
   displayed numerators are nonzero (implicit, since parameters are v2's).
4. (LOW-3) SEED_BUDGET §2's exact b-parent formula x₂=(13/8)x+2D+9k+10 (≡
   x₅=(3/4)x+6k+4) is presented as plain algebra but only exercised at canonical
   calls in the verifier; derivation not shown; keep the [B] tag visible.
5. (LOW-4) TRAIN_CLOCK_ORBIT §3's "higher lifts ... cannot change that valuation"
   is asserted without the one-line proof (Σ=2^{a−1}·odd+2^a·M ⟹ v2=a−1 exactly);
   the claim is correct and verified.

## 7. Hidden-assumption / honesty audit (all four main docs)

- TRAIN is applied only to segments that realize their displayed transitions
  (stated in GATEWAY_TRAIN §1). No circular use of "valid segment"; necessary
  conditions are never read as sufficient (graphs are labeled overapproximations;
  CLOCK_FILTERED's "upper bound valid for actual trains" is the sound direction:
  every actual train induces a graph walk, and acyclicity + longest path 1 of the
  necessary graph caps actual trains).
- CLOCK_FILTERED's [5,16381] theorem uses exactly two finite inputs, both now
  verified beyond their needed range (τ≤n and param-3 gaps).
- TRAIN_CLOCK_ORBIT is conservative at the boundary (u_0..u_{s−3}) and honest
  about non-applicability to the last two labels.
- CROSS_SCALE claims construction only; the c_r compatibility is existence-only
  and is explicitly separated from reachability/ancestry; the example contradicts
  only a cap that no accepted document asserts.
- No document claims global EXT or non-halting; K_clock unchanged everywhere.

## 8. CHECKPOINT status-line drafts

- **work_c3_drift group 3 (trains), 2026-10-24, reviewed (this review):**
  GATEWAY_TRAIN accepted: two-a recurrences and the (TRAIN) necessary congruence
  [A] (min-occurs-twice, index asymmetry m_{i+2}+2 correct); no three identical
  catapults [A] (size input: τ≤n [B] n<10^8, re-verified; nP(n)≤n² n≥2697);
  5776-vertex necessary graph cyclic [B]; cycle (8,244,81,27) not exactly
  repeatable [A] (advance 960, v2 6 < 81 required bits).
- **CLOCK_FILTERED_TRAIN accepted:** (ENTRY) k≡6 (mod 16) for internal labels
  [A], smallest internal label 17 [B]; (DROP2) m_{i+2}=m_{i+1}−2 [A] (τ
  monotonicity structural + [B] n<10^8); param-3 fire pointer gaps ≥5 [B n<10^8
  + structural: J=3 epoch length 5, odd a-crossings are fire pointers]; at most three consecutive
  catapult labels in [5,16381] [A + B]; revised graph 532 vertices/14 edges/acyclic
  [B]. (The original justification is complete; see corrected MED-1.)
- **TRAIN_CLOCK_ORBIT accepted:** (CLOCK-ORBIT) u_{i+1}=3^{−1}u_i (mod 2^{L−5})
  for internal labels ≥L≥17 [A]; period 2^{L−7} [A]; (ADVANCE) v2(Σ(12+6k_i))=L−2
  per period, lift-invariant [A]; exact period repetition (incl. odd multiples)
  impossible [A]. Scope: uninterrupted all-a segments only; b/c ancestry and
  parameter changes uncovered, as stated.
- **CROSS_SCALE_TRAIN accepted as construction:** four-catapult exact local trace
  5,1836655,5,514273,5,17,5,17,19 from a constructed (non-canonical) five-state,
  canonical calls (param-3 fires at pointers 1836654/514272) [B, replayed twice
  independently here]; c_r-compatibility existence (no joint reachability) [A];
  shows the small-interval cap cannot be promoted to all scales; no EXT/K_clock
  consequence.
- **Budget group (DEPTH_CLOCK/SEED/COPY/JOINT_HEIGHT/STOP_CHECKPOINT):** kept
  conditional/unreviewed-promoted-to-"reviewed, conditional": identities [A]
  (D=51+27k+(11/4)y−3z; SOURCE-RESERVE potential drop; height identities;
  ρ−P≥3 and ρ≥P+11 inductions; cross-scale 256-bit dlog residue [B] exact),
  O2-type family W=8<9 [A] — the joint reserve is *not* a local sufficient
  condition at small bare ties; none of these is a global ranking function (as the
  docs themselves state).

## 9. Reproduction

```
python -B work_gateway_trains/review_trains/review_checks.py   # exit 0
```
Final run: 19 checks, 0 failures (the 10^8 streaming walk caches itself in
`stream_cache.json`, 29.1 s uncached). Plus the ten patched verifier reruns in
this directory (all `status: PASS` with the published counts). The big-integer
SHA-256 fingerprints of the cross-scale construction recomputed here match
Astra's saved `cross_scale_train_checks.json` exactly.
