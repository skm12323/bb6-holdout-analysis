# Height ledger — step 1: canonical statistics

Claude, 2026-10-27. **[B] data only; unreviewed; no proof.** EXT open; K_clock unchanged.

Script: `python -B work_claude_heights/hl_stats.py N [sample]` (uses the cached table
`D:/math_cc_astra/deep1/table_N.pkl` built by `work_global_ext/route_c/fdata.lam_walk`). Output: `hl_stats_N.json`.
Run at N=10^6 (1 s) and N=10^8 (102 s, 1,000,000 sampled start chains).

## Results (n < 10^8)

1. **Whole S(J), J <= 10^8** (existing `work_global_ext/route_c/stats_100000000.json`). At most 3 chains after
   the fire; every chain after chain 1 is <= 6. The classes met are only −1, 0, 1, 2, 3; max Gamma is 6. No height
   accumulates anywhere in this range.
2. **S1 shift spectrum.**
   - 30,288,015 odd b crossings (shift −1) and 1,584,898 odd c crossings.
   - Every c crossing has eps ∈ {3,5} (1,582,175 and 2,723). The observed residual shifts are only 0 (eps=3) and −1
     (all 2,723 eps=5 cases are AA). No BA occurs below 10^8. There is no c crossing with omega >= 8; c crossings
     have omega ∈ {1,3,5}. (Corrected in review.)
3. **S2 pure b/c trains** (j → omega(j−1) while X(j−1) is odd b/c). The longest train has length 2 (791,085 cases).
   Below 10^8 these are (corrected in review):

   | tail | count |
   |---|---|
   | j→6→1 | 696,981 |
   | j→9→4 | 87,122 |
   | j→13→2 | 5,445 |
   | j→15→1 | 1,361 |
   | j→18→3 | 170 |
   | j→23→2 | 5 |
   | j→25→1 | 1 |
4. **S3 class walks.** 12,239,772 walks: start chain 19 <= j < 10^8 (sampled), start class in
   {−3..4, ±2/3, 4/3, 10/3, 26/3}.
   - At most 3 steps (worst: 6131 → 14 → 5 → 1).
   - Heights do grow inside walks: 3,738,283 walks increase |theta| (by up to +4) and 2,204,237 increase A (by up
     to +2). The reported "max height" 26/3 was only the global maximum, attained at a start (corrected in review).
   - No NT gate at any chain >= 19. This is implied a priori by Lemma ND/LC, so it is not new evidence. All 42,454 NT
     gates and 43,038 catapults occur at (j,k)=(5,1).
   - The S3 catapult rule (3−theta, lift dropped) is faithful on the landing chain. By construction it preserves
     height and rank, so S3 cannot test HL2.

   (The rank-4 count of 240 is an artefact of choosing least-height shift representatives for small omega; it
   is not a real rank.)

## Conclusion for the plan

Up to 10^8 the canonical calendar contains **no deep c structure at all**: no large-omega c copies, no trains
longer than 2, and every class walk collapses to chains <= 6 within 3 steps. The regime where heights could
accumulate (large-omega c copies, as in the congruence-target constructions) begins only at astronomically large
n, beyond any table. Two consequences:

- Statistics over a full table cannot test the height ledger. Evidence must come from **constructed canonical
  instances**: Calendar(512) fires at congruence targets, as in CONGRUENCE_TARGET_NOTE and BBBAA, which realise
  large-omega c sources with known histories.
- The ledger itself must be **analytic**. The ingredients are already accepted:
  - Theorem S: a certified shift is Phi(w)−2 with |s| <= W/2 (from the accepted |Phi−3/2| <= W/2−1/2) for catapult-free histories;
  - catapult classes (9+6k−d)/3 with k <= 6 on small chains;
  - Lemma LC: exponential DEPTH margins.

  Step 2 is to state and prove the ledger lemma and the "DEPTH automatic above j*" lemma; step 3 is to probe
  constructed large-omega sources with the calendar.

---

# Step 2: the ledger lemmas, localisation of non-descents, and the real target for S(J)

> **Review corrections (2026-10-27, reviews/claude_heights_review_record.md; they override §1–§4 below).**
> 1. [HIGH] §2 is WRONG as stated. Theorem S's precision H is not J−Gamma (that is the valuation of the beta-walk
>    coefficient). Along descents the dropped term x/2 has valuation j−1, so at a band chain g, H_g is only about the
>    previous input chain minus 1. A true NT gate has output m up to about 2log2 J. Once m >= H_g, the output class
>    (9+6k−d)/3+lift is no longer certified: the real class 3d'+1−2^m is exact integer data but has no small-height
>    representative. Consequences:
>    - HL2, the HL1 a-descent bound and NL are valid only up to the **first** NT gate of S(J);
>    - after it, a budget-propagation problem does exist for S(J) too;
>    - "each cycle raises the rank by 1 and widens the band by 1.585" conflates the small-height automaton value
>      with the real integer data.
>
>    The cycle problem must be posed for real residues, without a height bound.
> 2. [HIGH] NL is [A-cond], not [A]. The first-step shift bound uses SB, hence Corollary S1, which needs the copied
>    source chain to be certified (H_t >= omega+1). Tie-freeness of the W-epoch (EXT below J) does not give that; an
>    uncertified source's shift is an arbitrary residue mod 2^(omega+1). The constant 19.5 additionally assumes the
>    source history's non-descents lie at chains <= 18. The claim "non-descents of S(J) occur only at double-log
>    scale" is withdrawn; NL localises only the first NT gate, under these premises.
> 3. [MEDIUM] SB's general induction is wrong: nested C letters add their constants. The provable bound is
>    A(Phi) <= W/2 − 1/2 + 2·Σ_nu k_nu, summed over all (recursive) non-descents, using A' <= A/3+2k+1. HL2's non-descent
>    rule omitted Theorem S's lift term −2^m/3. Dropping it is harmless only while later chains stay <= m+2. With
>    Theorem S's lift term, "rank unchanged at r=0" requires 3 | (C+2^m) (without the lift it is 3 | C). Rank depends on the chosen representative:
>    at a catapult, 3−d−2^(j−1) is a rank-preserving valid representative.
> 4. [MEDIUM] Only true NT gates (j' >= j) count as L' non-descents. A catapult has output j−1, which L' counts as a
>    descent at no cost. Read "non-descent" in §1–§2 as "NT gate" where ND-EXIT is meant; a resonance 3Qk+C=0 is
>    always a catapult.
> 5. [LOW] ent.py's sets are classes of the defect D=Theta−x; in the beta-walk D ≡ 3d+1−2^j (mod 2^(j+1)). The phrase
>    "theta=3d+1 hits the set" is off by 2^j.
> 6. [LOW] band.py iterates A_max only along b/c landings. With large A an a-descent can land near log2 A_max
>    (e.g. about 42 at log2 J = 10^12, not 19). The 4log2 y+4 loss bound needs y >= 128. The "+30 tail" is [B] (table
>    data, eps <= 5). These affect the table only at low order.
>
> Confirmed: HL1 (MASS ⇒ omega <= floor(log2(6tau+5))); the a-descent bound; HL2's A, B, C rules and the lift-free
> non-descent algebra; rank +1 exactly when r >= 1; the accepted |Phi−3/2| <= W/2−1/2 (complete histories ending in
> A, under DH), giving |s| <= W/2 for catapult-free histories; "L' reduces EXT to ND-EXIT"; and "localisation does not
> lower L''s per-non-descent cost". **Net result of step 2:** the ledger and localisation hold up to the first NT gate
> of S(J), under the certified-source premise. ND-EXIT and the post-gate problem remain open.

Claude, 2026-10-27. **Unreviewed.** [A] = short consequence of accepted results, proof given; [B] = finite check;
[C] = conjecture. EXT open; K_clock unchanged. Script: `python -B work_claude_heights/band.py 100000000`
(produces `band_checks.json`).

## 1. Ledger lemmas

Work with the class automaton of Theorem S (work_claude_shift), value d ∈ Z[1/3] with rank r (the exponent of 3
in the denominator), and put A(d) := |d − 3/2|.

**HL1 (landing bound) [A].** A b/c step from chain z lands at chain omega(z−1) = v2(lambda'_W). By MASS
(origin_contraction, accepted), 0 < lambda'_W <= 6tau+5, so

    omega <= floor(log2(6 tau(z−1) + 5)) <= floor(log2(6(z−1)P(z−1) + 5)).

A descending a-step at chain z lands at 1 + v2(3Qk_z + C) <= 1 + log2(3^r(3k_z + A + 3/2)).
[B] All 31,872,913 odd b/c crossings with n < 10^8 satisfy the bound; none attains lambda = 6tau+5.

**HL2 (ledger) [A].**
- a-descent: d -> 3−d, so A is unchanged.
- b step: A' <= A+1.
- c step: A' <= A+|s|, and r' <= max(r, r_s).
- Non-descent (Theorem S): d -> (9+6k−d)/3, so A' <= (A+6k+3)/3 <= max(A, 3k+3/2), and r' <= r+1. The rank
  goes up by exactly 1 unless r=0 and 3|C.

**SB (shift bound) [A].**
- For a certified source chain, s = Phi − 2.
- For a catapult-free history of weight W = eps−1, the accepted bound |Phi − 3/2| <= W/2 − 1/2 gives |s| <= W/2.
- In general, running HL2 along the history gives A(Phi) <= W/2 + 1/2 + (3k̂ + 3/2), where k̂ is the largest k at a
  non-descent inside the history (recursively). If all of those non-descents are at chains <= 18 (canonical
  k <= 6), then |s| <= (eps+1)/2 + 19.5.

**NL (localisation of non-descents) [A].** By Lemma ND, a non-descent at an a-chain j with automaton (r, A)
requires 3Qk_j + C = 0 or

    2^(j−2) <= 3^r(3k_j + A + 3/2).

Along S(J) the automaton starts at d=1 (A=1/2, r=0). Its height before the first non-descent is bounded by:
- the first-step shift, (eps(J−1)+1)/2 + c <= 2log2 J + O(1) inside the induction, plus
- the later shifts.

By HL1, every descent lands at polylog of the current chain, so the later shifts add only O(log log J).

[B] band.py tabulates a crude worst-case A_max(J) and the largest odd-a chain where a non-descent is
arithmetically possible:

| log2 J | A_max | band r=0 | r=1 | r=4 | r=8 |
|---|---|---|---|---|---|
| 10 | 104 | 8 | 8 | 14 | 17 |
| 10^3 | 2,095 | 12 | 14 | 17 | 24 |
| 10^5 | 2·10^5 | 17 | 17 | 24 | 32 |
| 10^6 | 2·10^6 | 22 | 24 | 27 | 35 |
| 10^12 | 2·10^12 | 42 | 42 | 49 | 54 |

So the first non-descent of S(J) lies in a band of width about log2 log2 J + 1.585·r. For J <= 2^(10^5) with copied
shifts of rank <= 1, it lies in the canonical small region j <= 17. There the classes that reach an NT gate are a
fixed finite list (work_claude_uniform `ent.py`): 4 classes mod 2^(j+1) at each of j=5,8,12,14, and 8,196 of 2^18 at
j=17.

## 2. Assessment: for S(J) the propagation problem is not the obstacle

While S(J) is tie-free, the accepted integer beta-walk (PROOF_EXT Lemma BR) is exact: the anchor is chain 0 with
D=1, Q=1, and Theorem S's precision H = J − Gamma stays >= j+1 exactly as long as there is no tie. So **for S(J)
itself there is no budget to propagate**. The "reference phase after later gates" difficulty of origin_contraction
and RECORD_BUDGET comes from their relative anchors.

The accepted reduction is Theorem L' (PROOF_EXT §3):

    EXT ⟸ ND-EXIT: every tie-free prefix of S(J) has <= floor(J/(3 log2 J)) non-descents.

The ledger adds the localisation above. The precise remaining problem for S(J) is therefore:

**Cycle problem.** Every non-descent starts a cycle: band chain g → NT gate or catapult → output m → descents →
band again. Each cycle raises the automaton rank by 1 (barring cancellation by copied rational shifts), which
widens the band by about 1.585 chains. A cycle can only start when the band class θ = 3d+1, d = Σ(1+τ), hits the
finite NT-reaching set mod 2^(j+1). That is a congruence on the accumulated clock sum: the "moving residue" of
B5/F3, now posed for S(J) directly with the explicit allowance J/(3log2 J).

Data: S(J) has 0 non-descents for every J <= 10^8 (route_c stats). In the class walks of step 1, gates
occur only at chains <= 18.

## 3. What step 2 does and does not give

- **Does:** HL1 (from MASS), HL2, SB and NL are short [A] consequences of accepted results, with the explicit
  band widths [B]. They show that the non-descents of S(J) occur only at double-log scale, and for moderate J
  inside the fixed canonical small region.
- **Does not:** NL does not by itself shorten Theorem L''s non-descent cost: a gate output is v2 of the exact
  integer B, which can be up to about 2log2 J, so the cost per non-descent stays O(log J), as in L'. No ND-EXIT
  bound is proved.
- **Caveats:**
  - SB's constant 19.5 assumes that non-descents inside copied source histories sit at chains <= 18; otherwise use
    3k̂ + 3/2.
  - The rank r_s of copied shifts is carried as a parameter.
  - A_max is a crude worst case.

## 4. Proposed next target [C]

Attack the cycle problem through the clock sum: give a structural law for d mod 2^k along a cycle (in the spirit of
the accepted TRAIN_CLOCK_ORBIT u_{i+1} ≡ 3^(−1)u_i), and show that consecutive cycles cannot keep hitting the
NT-reaching residues more than O(J/log J) times. Use the step-3 constructed canonical instances (Calendar(512)
congruence-target fires) as test cases.
