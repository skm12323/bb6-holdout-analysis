# Cycles through NT gates: post-gate memorylessness, free gates, and train data

Claude, 2026-11-02. **Preliminary exploration; reviewed (three-way, 2026-11-02), see the corrections block below.** No EXT / non-halting claim; K_clock unchanged.
Tags: [A] proved here (proof given, from the exact pair-map rules only unless an import is named),
[A-cond] proved under stated hypotheses, [B] exact computation over a stated finite range (script named),
[C] heuristic / conjecture. **Every multi-gate instance in this note is SYNTHETIC**: a free 2-adic start
cylinder run on canonical Calendar(512) crossing data. None is canonical-reachable (S(J) itself has no
non-descent for any J tested, §4.0).


> **Review corrections (2026-11-02, reviews/claude_cycle_review_record.md; they override the body below).**
> 1. [HIGH] **Lemma DR is FALSE.** At the gate output, x has no X term. X first enters at the first a-step after the
>    output, with coefficient 2^j (through 2Theta). After that it drops by 1 per a-step and by 1+eps per b/c step. So
>    at G′'s output the X-valuation is j−ell+L_bc+1, not j−ell, where L_bc is the loss of the b/c run right after the
>    output. Correct form **DR′ [A]**: if G′ is determined by G, then m′ <= j−ell+L_bc, i.e.
>    R_after(G′) <= R_in(G)+1+L_bc. Here ell is the loss from G's output to G′'s output, and L_bc is the
>    loss of the maximal b/c run right after the output (0 if X(m−1) is type a). For a type-c first step the bound
>    reads R_in+2+eps+(later b/c loss). The bound is attained for L_bc ∈ {0, 2}; whether it is reached after a
>    type-c first step is open.
>    - Counterexample A (exact replay with random high bits): j=24 (k=9), m=6,268,562 (type a). The walk is
>      24 → m → 5, gates at 5 with output 22 = j−2, then 2. R goes from 24 to 25, and verify_laws.check_walk itself
>      returns DETREC_FAIL.
>    - Counterexample B (exact mod 2^P / symbolic): j=42, m ≈ 1.1·10^12, X(m−1) of type b. The walk is m → 5, gates
>      at 5 with output 41, R_after = R_in+3. The congruence is solvable for j = 42, 78, 113, … and (239, omega=8);
>      instances are exhibited for j = 42 and 78.
>    - NEXT needs the case v2(N) > j−2: then m′ = j−2 (determined), and v2(N) = j−2 splits.
>
>    The [B] DETREC check (m < 5000) cannot see these. "Determined cascades cost nothing" (§0.3, §3, CL1, CL5) is
>    withdrawn.
> 2. [HIGH] **§3 as stated depends on the false DR.** Determined gates that are not record-safe can each add up to
>    1+L_bc, and nothing bounds their number. Corrected statement: call a gate **record-safe** if it is determined and
>    m′ < j−ell, and count every other gate as free. With this definition §3 holds [A], with the DR bullet
>    replaced by: "a record-safe gate has R_after = m′+Gamma_0+1+ell <= j+Gamma_0 = R_in(G) <= M by definition; a
>    non-record-safe gate G′ raises M by at most m′+1−j_{G′} <= g−4, since R_in(G′) <= M". With this definition
>    determinism plays no role: the reduction is bookkeeping, and any gain over ND-EXIT rests entirely on FREE
>    (first landing), FREE-B and CL2. The chain-count
>    replacement t < J is confirmed. But FREE then has to be extended to the boundary gates (determined, not
>    record-safe). That extension, FREE-B, is open: a CLOCK/MASS argument seems to work for the two-step families; the
>    general case belongs to CL2.
> 3. [MEDIUM] §0.1 memorylessness:
>    - The determined region reaches R_in+1+L_bc.
>    - The walk depends on k_j and on the crossing data at m to the precision given by DR′ (for example
>      tau(m−1) mod 2^(j+1) in counterexample B), not on "data mod 2^(j−1)".
>    - This agrees with the height-ledger review: post-gate classes remain uncertified. PG/LAND remove the pre-gate
>      class, rank and height from the low bits only; they do not certify the high bits.
> 4. [MEDIUM] Localisation (FREE) is proved only for **first-landing** escapes. §0.7 and §7 overstate it.
> 5. [MEDIUM] [B] scope. The CUT leaves are exactly the walks with m ≳ j+BITS. So "<= 3 gates", "splits at the first
>    step", "free only after 5/8", "DETREC strict" and "24 bits for any j >= 9" hold only in the sampled ranges
>    (postgate: j < 400, m < 5000; sweep: j < 3000, depth 3000; the 24-bit claim: 9 <= j < 400), not for large m.
> 6. [LOW] §4.5/§7.2: label residue 3 occurs (k = 174,771), and residue 15 occurs 262 times among 121,150 labels
>    below 178,425. "Labels avoid 3, 7, 11, 12 mod 16" and the recommended step 2 built on it are unsupported.
> 7. [LOW] NEXT for type c needs min(j−2, m−1−eps) >= c−1. The cut mass 0.0 in sweep_3000 is a float underflow. The
>    "nondescents" counter also counts catapults. "CLOCK-ORBIT at every j" is a sketch, not a proof.
>
> Confirmed:
> - PG; LAND (types a and b/c; type c via lambda' = 3tau+4+lambda_Y);
> - FREE for first landings, with its CLOCK/MASS constants and m <= g;
> - CG; 2G/3G/JT (JT re-derived by hand); SELF; NEXT for v2(N) < j−2;
> - the §6 counterexamples;
> - the synthetic starts are genuine gate states;
> - re-runs by the adversary (verify_engine, verify_laws, verify_3g, postgate subset, sweep 1000; DR scans j<120, m<1500
>   and j<60, m<2·10^5); blind auditor 1's own engine and j<300 scan.
>
> **Net result:** [A] PG, LAND, DR′, FREE (first landing), NEXT (for type c under the precision hypothesis of
> item 7), SELF, CG, 2G/3G/JT. [A] FREE-EXIT ⇒ EXT holds with "free" meaning "not record-safe"; it is bookkeeping,
> and its value depends on FREE-B and CL2. Open: FREE-B for boundary gates, later escapes (CL2), and trains (CL4). G1 is
> not closed.

## 0. Summary

1. **Post-gate memorylessness [A] (Lemmas PG, LAND, DR, §2).** After a true NT gate at an odd-a chain j
   (k = k_j) with output m, in *every* exact walk:
   - the phase is Theta = 2^(j-2) + 3(k+1) (mod 2^(j-1)), whatever the history;
   - at the first landing c after m, the defect is D_c = delta + 2^(j-2) (mod 2^min(j-1, m-1-eps)), with the
     *integer* class delta = -3k (X(m-1) type a), 3k+2 (type b), 3k+2-lambda_Y(m-1) (type c);
   - while the walk stays below the gate's input record, it is a function of (j, the crossing data at m mod 2^(j-1))
     alone, and any gate it meets has output record <= R_in(gate) (Lemma DR).

   So below level j-1 the pre-gate class, its 3-adic rank and its height are invisible. The rational class
   (9+6k-d)/3 + 2^m of Theorem S is, mod 2^(j-1), the integer 3(k+1)+2^(j-2). The G1 residue 3d'+1-2^m matters
   only through the bits of o = (Theta_in+3k)/2^(j-2) above position 0, i.e. only if the walk climbs back to the
   gate's input record.
2. **Free gates and localization [A] (Lemma FREE, §2.3).** If the first step after the output is *not* a
   determined landing below j-1, then
   - v2(k_j+1+k_m) >= j-2 (type a), or
   - omega(m-1) >= j-1 (type b/c).

   Both force j <= 3 + log2(6 m P(m)) (CLOCK, MASS). With m <= g = log2(12J^2) inside a tie-free S(J) prefix,
   such escapes happen only after gates at j <= log2 g + 2log2 log2 g + O(1).
3. **FREE-EXIT ⇒ EXT [A, modulo review of the L' transfer] (§3).** Only *free* gates can raise the running
   maximum record; a gate determined by its predecessor cannot (Lemma DR). Hence Theorem L' holds with
   "non-descents" replaced by "free gates" (gates not determined by the previous gate, plus the first gate).
   This is a genuine but modest weakening of ND-EXIT: in a long train every gate is free.
4. **Exact gate-to-gate laws [A] (§2.4–2.6).**
   - NEXT: at a first landing c <= j-3 the step is a gate iff v2(delta+3k_c) = c-2. Then (type a) its output
     is v2(k_j+3+3k_m+2k_c) when that is < j-2.
   - SELF: an a-type landing back at c = j is always another gate at j.
   - CG: consecutive gates at g, g' have clock increment E = (sum of 1+tau) + k_g' - k_g with
     v2(E) >= min(g,g')-2 (equality iff g != g'), so E >= 2^(min(g,g')-2).
   - JT: the TRAIN/CLOCK-ORBIT recurrence holds for direct-return all-a trains at every j:
     4y_{i+2} - 5y_{i+1} + y_i = 12(2+2k_j-k_{m_i}+3k_{m_{i+1}}).
   - 3G: a general three-gate identity for arbitrary intervening paths.
5. **Data [B].**
   - Over all 575,644 post-gate pairs (j odd-a < 400, j <= m < 5000), 574,014 end deterministically with no
     further gate.
   - Every continuing pair's next gate is either at chain 5 or 8, or (after j ∈ {5,8}) at the output chain m
     itself (a staircase).
   - The Haar cost of a second gate after a first one is 14.0 bits at j=5, 24 bits at best for any j >= 9,
     and 133 bits at j=8.
   - Exhaustive branching from every forced-gate start G(j), j odd-a < 3000 (906 starts), to cylinder depth 3000:
     **every resolved walk has at most 3 true NT gates**. Only j=5 and j=8 reach 3, always by the pattern
     (j,m),(j,m),(m,m').
6. **Refuted (§6).**
   - "The next gate after any gate is at chain 5 or 8 (or at the output chain itself)". Explicit counterexamples: (j,m) = (9194, 45901) gives a
     determined gate at 14 with output 16, and (27560, 64268) gives (14, 15).
   - "Gate outputs decrease along consecutive gates". Staircases (j,m) -> (m,m'>m) exist. Decrease does hold for
     determined pairs.
7. **Assessment.** The direction converts G1 into a sharply localized problem: free gates at chains
   j <= log2 g + O(log log g), followed by small-chain trains with explicit recurrences. It does not close G1. The
   missing piece is a bound on consecutive *free* gates (trains) for labels up to g. JT only gives contraction
   (K=0) or "exponentially spread labels" (K != 0), and the CLOCK-ORBIT period argument works only for
   g <~ 2^150 (§5, CL4).

## 1. Setting, engine, verification

Scalar pair map (PROOF_EXT §2 / Lemma BR), on canonical data. At chain j, n = j-1:
- a-step (tau = 2k): x' = 2Theta + 6k - x/2, Theta' = Theta + 3 + 6k, Gamma += 1;
- b/c-step: x' = R x + lambda' with R = c'_W/2^j, Theta' = Theta + 3 + 3tau, Gamma += 1+eps.

Then j' = v2(x'). S(J) is the walk from (J, Theta=1, x=0) (Theta = 3d+1, x = beta_x); a tie means j' >= J-Gamma'.
Record R = j + Gamma. Lemma NT: with v = v2(Theta+3k) at an a-chain j:
- v <= j-3: descent to 1+v;
- v = j-2: **true NT gate** (j' >= j);
- v >= j-1: catapult (j' = j-1).

Gate notation: Theta_in + 3k = 2^(j-2) o with o odd; x_in = 2^j b; output y = 2^(j-1)(o-b), m = v2 y.

- `cyc.py`: exact walk on `Calendar(512)` rows (kind, tau, eps, odd, R, lambda', lambda_Y).
  **[B] verify_engine.json PASS**:
  - S(J) word, types and status equal `Calendar.projected_epoch` for 5 <= J <= 30000 and 3000 random J < 2^500
    (32,996 J);
  - exact beta_x equals `route_b/core.symexit` (independent full pair walk) for 5 <= J < 600;
  - 11,050 a-step classifications checked;
  - 0 non-descents occur in all these S(J).
- `branch.py`: exact 2-adic branching walk on affine forms in free Haar variables. At a FREE step the free part
  is first made one variable by a unimodular (measure-preserving) substitution, then split. Leaves are
  concretized (`lift`) and replayed with the exact integer walk. Every replay in the JSON files passes.

## 2. Structure lemmas [A]

### 2.1 Lemma PG (post-gate phase)
Theta_after = Theta_in + 3 + 6k = (Theta_in + 3k) + 3(k+1) = 2^(j-2) o + 3(k+1).

*Proof:* the a-rule. ∎ Hence Theta_after ≡ 2^(j-2) + 3(k+1) (mod 2^(j-1)), independent of the history.
Along any later path Theta only gains exact calendar increments.

### 2.2 Lemma LAND (first landing class)
Let x' = y = 2^m u' and consider the step from m.

*(a) X(m-1) odd a, K = k_m, E = k+1+K.*
- x'' = 2^(j-1) o + 6E - 2^(m-1) u'.
- If 1 + v2(2^(j-2)o + 3E) < m-1, the landing is c = 1 + v2(2^(j-2)o + 3E).
- In particular c = 1+v2(E) when v2(E) < j-2, and c = j-1 when v2(E) > j-2 and m > j.
- Exactly, D'' = Theta'' - x'' = 3 - Theta' + x'/2 = -3k - 2^(j-2) o + 2^(m-1) u'.

*(b/c) X(m-1) odd b/c.*
- c = omega(m-1). Exactly, D'' = 2^(j-2) o + 3(k+1) + 3 + 3tau - lambda' - R 2^m u', with v2(R 2^m u') = m-1-eps.
- MASS (Lemma K / origin_contraction §2) gives lambda' = 3tau+4 (b) and 3tau+4+lambda_Y (c).
- So D'' = delta + 2^(j-2) o + O(2^(m-1-eps)) with delta = 3k+2 or 3k+2-lambda_Y.

In all cases D_c ≡ delta + 2^(j-2) (mod 2^min(j-1, m-1-eps)), o being odd. ∎

[B] verify_laws.json: 82,469 landing-class checks and 55,321 landing-chain checks, all PASS.

*Remark (rank).* At precision 2^(j-1), the class after a gate is an integer of height <= 3k_j+2+lambda_Y.
HL2's "each cycle raises the rank by one" concerns the representation through the pre-gate class Phi, as already
flagged in the heights review. It does not concern the real low-order state.

### 2.3 Lemma DET/DR and Lemma FREE
Write the generic post-gate state as Theta = 2^(j-2)(1+2X) + 3(k+1), x = 2^m(1+2V) (X, V free). By the a/b/c
rules, the X-coefficient of x has valuation exactly j - ell after loss ell from the gate's output:
- it starts at 2^j inside y;
- an a-step maps c to 2^j - c/2, so the valuation drops by exactly 1 once below j;
- a b/c step multiplies by R, so it drops by exactly 1+eps.

The V-coefficient has valuation m+1-ell > j-ell. Call the next gate G' **determined by G** if every step from
G's output through G''s output has its valuation fixed by the X,V-free part (the branch of the generic tree has no
split).

**DR [A].** If G' is determined by G, then m' < j - ell. With Gamma_0 the loss before G,
- R_after(G') = m' + Gamma_0 + 1 + ell <= j + Gamma_0 = R_in(G).

[B] DETREC: 1,512 determined pairs, all with strict inequality.

**FREE [A].** If the first landing is not a determined descent below j-1, then
- type a: v2(E) >= j-2, so 2^(j-2) <= k+1+k_m;
- type b/c: omega(m-1) >= j-1, and by MASS 2^(j-1) <= lambda' <= 6tau(m-1)+5.

With CLOCK tau(n) <= nP(n) (P(n) = 2ceil(log2(6n^2+5))^2+1345), both give j <= 3 + log2(6mP(m)).

[B] 49,772 (a) and 1,036 (b/c) escapes checked.

FREE covers only *first-landing* escapes. A later escape inside a determined continuation needs the X-free part
to reach valuation j-ell. Bounding that part by poly(m) (cone-type bound) gives j <= ell + O(log m) *unless the
part vanishes* (an NZ-type cancellation). This later-escape case is not proved here. In all data (§4) every free
gate follows a gate at j ∈ {5, 8} (verify_laws: 34,946 free pairs, all after j=5 or 8), and in postgate every
split happens at the first step after the output.

### 2.4 Lemma NEXT and Lemma SELF
- *NEXT.* If c <= j-3, then mod 2^(c+1) the class is delta, and the a-step at c is a gate iff
  v2(delta+3k_c) = c-2 (Lemma NT).
- *Output (type a).* y_c = 2Theta_c + 6k_c - x_c/2 = 2^(j-2) o + 3(k+3+3k_m+2k_c) + 2^(m-2) u'. So
  m' = v2(k+3+3k_m+2k_c) whenever that is < j-2 (and < m-2).
- *Examples.* c=5 (type a) needs k_j ≡ 9 (mod 16): j = 24, 61, 97, ...; type b needs k_j ≡ 1 (mod 16):
  j = 42, 78, .... c=8 (type a) needs k_j ≡ 66 (mod 128): j = 152.
- *SELF.* An a-type landing at c = j has v2(o+3E/2^(j-2)) = 1, and the class at j is -3k - 2^(j-2)o + 2^(m-1)u'.
  So v2(D+3k) = j-2: a gate. ∎

[B] 2,363 criterion checks, 758 output checks, 24,692 SELF checks, all PASS.

### 2.5 Lemma CG (clock between consecutive gates)
For consecutive true gates at g, g' with phases Theta_g, Theta_g':
- 3E := (Theta_g'+3k_g') - (Theta_g+3k_g) = 2^(g'-2)o' - 2^(g-2)o;
- E = (sum over steps from g to g' of (1+tau)) + k_g' - k_g > 0 (the first term is >= 1+2k_g).

Hence v2(E) >= min(g,g')-2, with equality iff g != g', and E >= 2^(min(g,g')-2). In beta-walk terms this reads
v2(d_g' - d_g + k_g' - k_g) >= min(g,g')-2. ∎

[B] 36,458 pairs PASS.

### 2.6 Identities 2G/3G and JT (generalized TRAIN)
For gate i (chain g_i, input phase Theta_i, output y_i) let the path to the next gate input be
x = alpha_i y_i + beta_i Theta_i + gamma_i and Theta_{i+1} = Theta_i + delta_i (exact affine composition). Put
a_i = 2 - beta_i/2 and c_i = 2delta_i + 6k_{i+1} - gamma_i/2. Then:
- (2G) y_{i+1} + (alpha_i/2) y_i = a_i Theta_i + c_i;
- eliminating Theta_i, (3G) a_i y_{i+2} + (a_i alpha_{i+1}/2 - a_{i+1}) y_{i+1} - (a_{i+1} alpha_i/2) y_i = K_i,
  where K_i = a_i a_{i+1} delta_i + a_i c_{i+1} - a_{i+1} c_i is a pure calendar number.

For a direct-return all-a j-train, (alpha, beta) = (-1/2, 2) and
- (JT) 4y_{i+2} - 5y_{i+1} + y_i = 12(2 + 2k_j - k_{m_i} + 3k_{m_{i+1}}) (j=5 is GATEWAY_TRAIN's TRAIN);
- so v2(2+2k_j-k_{m_i}+3k_{m_{i+1}}) >= min(m_{i+2}, m_{i+1}-2, m_i-2);
- with the free-label congruence k_m ≡ 2^(j-2)-k_j-1 (mod 2^(j-1)) this is the CLOCK-ORBIT law at every j.

[B] verify_3g.json: 25,436 path/2G checks, 5,192 3G checks (5,065 have K=0 exactly), 134 JT checks, all PASS.

## 3. FREE-EXIT ⇒ EXT [A, transfer of L' to be reviewed]

Count as **free** the first gate of S(J) and every gate not determined by its predecessor. Let M_t be the
running maximum record.
- By DR, a determined gate's output record is <= R_in(predecessor) <= M.
- Descents and catapults never raise R.
- A free gate raises M by at most g-4 (output <= g, input chain >= 5).

So R_t <= R_1 + N_free(t)(g-4). L''s proof then goes through verbatim with "non-descents" replaced by "free gates".
Its chain/clock bound (d <= 2J^2, so j <= g) follows from tie-freeness alone: t <= Gamma_t < J and tau <= (g-1)^2.

Hence:

**(FREE-EXIT)** "at most floor(J/(3log2 J)) free gates in every tie-free prefix of S(J), J >= K_clock" ⇒ EXT.

Gain over ND-EXIT: determined cascades (big gate -> determined small gate) cost nothing. No gain for trains.

## 4. Data [B]

0. *Canonical.* No non-descent in S(J) for the 32,996 J of §1, consistent with route_c (J <= 10^8). All
   instances below are synthetic starts.
1. **Continuation sets** (`postgate.py 400 5000 20` -> postgate_400_5000.json, 30 s).
   - Scope: generic post-gate starts for every odd-a j < 400 and j <= m < 5000.
   - 574,014 pairs are determined END with no further gate; 1,474 have a determined next gate; 156 are split.
     Continuing pairs number 1,630.
   - Every next gate occurs at the first step after m. Its chain is the landing (5: 4,099 GATE leaves; 8: 339)
     or m itself (8 leaves, all (5,17) -> gate at 17 within 20 bits; a gate at m costs about m-j bits). So
     "next gate at 5 or 8, or a staircase gate at m" holds in this range.
     - j=5: m with k_m ≡ 6 (mod 16) (139 values: 17, 54, 90, ...), next-gate probability ≈ 1/2.
     - j=8: k_m ≡ 61 (mod 128) (17 values: 139, 425, ...).
     - The NEXT families k_j ≡ 9 (mod 16) (X(m-1) type a) and k_j ≡ 1 (mod 16) (type b) land
       deterministically at 5. j=152 (a) and j=239 (b) land at 8.
   - Haar cost -log2 P(next gate | gate at j), weighting m by 2^-(m-j+1): 14.0 (j=5), 133 (8), 24 (42, 113,
     186, ...), 56–67 (other continuing j), 438 (239), 563 (152). Every other j < 400 has no continuation with
     m < 5000.
2. **Gate-count sweep** (`sweep.py 3000 3000`, 231 s; also `sweep.py 1000 1000`).
   - Scope: every forced-gate start G(j), j odd-a < 3000 (906 starts), cylinder depth 3000.
   - Leaves: 2,781,386 END with 1 gate, 217,551 with 2, 72,635 with 3, none with more. 1,141 CUT leaves of total
     mass <= 1141·2^-3000.
   - Maximum 3, reached only from j=5 and j=8, always as (j,m),(j,m),(m,m'). For example 5→17→5→17→17→1 and
     8→139→8→139→139→1.
   - Haar mass from G(5): P(>=2 gates) = 6.1e-5 = 2^-14.0, P(3) = 7.5e-9. Each further gate costs about 13 bits.
3. **Free-label model** (`residue_cont.py`, files residue_cont_30_300.json and residue_cont_120_70.json).
   - The output label K = k_m is a free residue, with m -> infinity, which over-approximates all real a-type
     outputs.
   - At most 3 further gates after j=5 or j=8 (depth 300); at most 2 after j ∈ {24, 42, 61, 97}; at most 1 for
     the other j < 120 (depth 70).
4. **Deep seeds** (`seeded.py` -> seeded.json, replay PASS).
   - The two §6 counterexamples.
   - Big gates j ∈ {24, 61, 97, 132, 168} with outputs m ≈ 10^5–5·10^5, chosen by solving the NEXT congruences
     so that the determined landing is the 5-gate with output 17 ∈ C_5.
   - The continuation stays determined by the big gate, with 2–3 gates in total: e.g. 61→293820→5→17→5→5.
     The would-be free 5-train is resolved by the big gate's precision.
5. **Label structure** (observation, not used in proofs). Odd-a labels k_j avoid k ≡ 3, 7, 11, 12 (mod 16):
   15 occurs 26 times among 121,151 labels < 178,425, and about 68% of the residues are present mod 2^r.
   - So the a-type free condition k_m ≡ 2^(j-2)-k_j-1 (mod 2^(j-1)) is unsatisfiable whenever
     -(k_j+1) mod 16 ∈ {3, 7, 11, 12}, e.g. j = 12 (k=4) and j = 22 (k=8).
   - The c=12 NEXT landing is likewise impossible, since it needs k_m ≡ 1019 ≡ 11 (mod 16).

## 5. Candidate lemmas and proof status

- **CL1 (memorylessness) — PROVED [A]** (PG, LAND, DR). Statement in §0.1.
- **CL2 (free localization) — first-landing case PROVED [A]; general case OPEN.** Every free gate follows a gate
  at j <= 3 + log2(6gP(g)). The general case fails exactly at a possible exact cancellation of the X-free part
  inside a determined continuation (an NZ analogue). Here the start is fully explicit, so this may be provable.
- **CL3 (free gates only after gates at 5 and 8) — [B]** in the ranges of §4.1–4.2; **[C] false in general**
  (expected). FREE allows any j with 2^(j-2) <= k_j+1+k_m that is compatible with the label residues.
- **CL4 (train bound) — [C], proof attempt fails.** "Every maximal run of consecutive free gates has length
  <= T(g) = O(log g)." Data: <= 3 in §4.2. Proof attempt for direct-return all-a j-trains:
  - by JT, each triple either has K=0, so k_{m_i} = 3k_{m_{i+1}}+2+2k_j and the labels contract by 3, or K != 0,
    which forces 2^min(m_{i+2}, m_{i+1}-2, m_i-2) <= |K| <~ 4 max k, i.e. some label in the triple is
    <= log2(2gP(g)) + 2 (about log2 g + 2 with the actual labels k ≈ 0.45 j);
  - contraction runs last <= log_3 g steps, so small labels recur every <= log_3 g + 3 steps;
  - CLOCK-ORBIT (accepted, L=17 for j=5) forbids a label from recurring within 1024 transitions.

  Together (sketch, not checked in detail) these bound direct-return 5-trains by about 1024 only while the
  small labels are too few: about (log2 g)/36 small labels in C_5 against the >= 1024/(log_3 g+3) appearances
  required, i.e. only for g up to about 2^150–2^200. The argument breaks at three points:
  1. for larger g there are enough distinct small labels;
  2. trains with b/c returns, landings c ∈ {j-1, j+1, ...} or staircase climbs (j,m) -> (m,m') are not covered
     by JT (3G covers them, but with path-dependent coefficients);
  3. mixed-scale triples (K != 0) are not excluded.
- **CL5 (FREE-EXIT) — the reduction is PROVED [A, §3]; FREE-EXIT itself is OPEN.** Since g = O(log J) and the
  budget is J/(3log J), any bound N_free <= 2^(g/2-3)/g on free gates per prefix would suffice. Heuristically
  [C]: if the small integer starts were equidistributed in the gate cylinders (cost >= 13–14 bits per gate), a
  start of height 2^O(g) would give N <= O(g)/13.

## 6. Refuted

1. *"After a true NT gate, the next one is at chain 5 or 8, or at the output chain itself"* ([B]-true for
   j < 400, m < 5000, and for the 3000-sweep). Counterexample [B, exact replay]:
   - j = 9194 (k = 4101) with output m = 45901 (k_m = 20474, X(m-1) odd a). The walk lands deterministically at
     14 and gates there with output 16 = v2(4101+3+61422+10) = v2(65536). A second example is
     (27560, 64268) -> (14, 15).
   - Mechanism: NEXT with c=14 needs v2(k_c-k_j) = 12 and v2(k_j+1+k_m) = 13.
2. *"Outputs decrease along consecutive gates"*. False: (8,139) -> (139,140) in §4.2 (the landing at m is
   itself a gate), and 5-trains 17 -> 54 occur. It holds for determined pairs (DR: m' < j - ell <= m).
3. *"Rank/height accumulate across NT gates at the precision that drives the walk"*. Not a refutation of an
   accepted statement (the review had already withdrawn HL2's cycle picture). LAND shows the low-order post-gate
   state is an integer class depending only on (k_j, type, lambda_Y).

## 7. Recommended next step

1. **Prove CL2 in general**: no exact cancellation of the X-free part inside a determined post-gate
   continuation. The start is explicit (Theta ≡ 2^(j-2)+3(k+1), x = 2^m·odd), and the small part is a calendar sum.
   This would make *every* free gate a first-landing escape after j <= log2 g + O(log log g).
2. **Turn the label-residue structure (§4.5) into a theorem**, an automatic-sequence description of fire
   half-times mod 2^r via PROOF_SPECTRUM gaps. It removes free continuations for whole classes of j (all j with
   k_j ≡ 4, 8 mod 16) and constrains train labels.
3. **Attack trains at chains j <= j_*(g) with 3G + CG**, in the FREE-EXIT form (only consecutive free gates
   matter). The first target is the mixed-scale K != 0 case of JT for g >= 2^150. A bound on train length that
   is polynomial in g, even a weak one, suffices.

Is this direction promising for G1? It localizes G1 well: uncertified residues act only at free gates, which
follow gates at doubly-logarithmic chains, and the problem becomes trains with exact recurrences. But it still
leaves a genuine train problem at small chains for astronomically large label ranges. That problem is the same
kind as the accepted TRAIN/CLOCK-ORBIT work, now posed for all j and arbitrary paths.

## 8. Files and reproduction (run from D:\math_cc with PYTHONUTF8=1, `python -B work_claude_cycle/<script>`)

| script | output | time | content |
|---|---|---|---|
| verify_engine.py | verify_engine.json | 160 s | engine vs projected_epoch / route_b core |
| postgate.py 400 5000 20 | postgate_400_5000.json | 30 s | continuation sets, Haar next-gate costs |
| verify_laws.py 400 800 | verify_laws.json | 8 s | PG, LAND, FREE, SELF, NEXT, DR, CG |
| verify_3g.py 800 | verify_3g.json | 5 s | 2G, 3G, JT |
| maxgates.py B (B=150,400,1000) | maxgates_B.json | <10 s | G(j) and anchor starts A(y,D) (anchors: 0 gates) |
| sweep.py 1000 1000 / 3000 3000 | sweep_*.json | 18 s / 231 s | all-start gate-count sweep |
| residue_cont.py 30 300 / 120 70 | residue_cont_*.json | 2 s | free-label model |
| seeded.py | seeded.json | <1 min | §6 counterexamples, deep seeds |

Libraries: cyc.py (exact walk, Calendar wrapper), branch.py (2-adic branching with unimodular splits, lift,
replay). Standard library only. Scratch logs: D:/math_cc_astra/cycle_scratch/.
