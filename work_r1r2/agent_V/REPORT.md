未经审查 / unreviewed — agent_V, 2026-10-20

# Adversarial verification report: Theorem A (R1 ∧ R2 on the deep segment)

## Errors and gaps (most important first)

1. **GAP (main): the A5 → A6 bridge does not establish `m < 2·10^7`.**
   A5 proves only `m = j_{u+1} ≤ j_T−3` (resp. `j_T−4`). A6 is a finite certificate for
   `5 ≤ m < 2·10^7` (I re-verified it independently to 10^8). Nothing in A1–A5 bounds `m` by
   2·10^7. Within the claimed range `Λ(J) ≤ 13` the last deep chain can have `T = 1` and
   `j_T = j_1 ≤ L(J)`; for `J < T_13` this is `≈ log2 J` (a tower of height ~11, astronomically
   > 2·10^7), and `m = v2(θ_T+12+9k)` can be as large as `≈ log2(9k) ≈ log2 j_T`, far beyond
   2·10^7. Then chain `u+1` is *deep again* (`j_{u+1} ≥ N0`, θ = −2 or 14), A6/table do not apply,
   and the re-entered drift window is shifted: a later a/b landing has `δ = 3−θ` down to
   `≈ 3−14−6Λ`, outside `[−12,15]`, so A4 does not cover it either. The bare-tie case is
   therefore closed only under the extra hypothesis `m < 2·10^7`, which is not proved (and is
   not implied by the size bound `|mval| < 2^{j_T−3}`).
2. **ERROR (stated range of A2/A3).** The line `2(B−4)/6+1 < 3.34·10^6` is false: `(B−4)/6`
   has 3,010,300 decimal digits here. No-resonance (`3k+θ_t ≠ 0`) follows from the drift bound
   only if `2Λ+1 < 14,999,998`, i.e. `Λ ≤ 7,499,998` (crude), or `Λ ≤ 14,999,997` with the sharp
   `|θ_t| ≤ t+1 ≤ Λ`. Hence A3's `T ≤ Λ−1` also holds only in that range, not for all
   `6Λ+4 ≤ B`. The final use `Λ ≤ 13` is unaffected (`2Λ+1 = 27 ≪ 3k ≥ 15,000,000`).
   (Confirmed as an error of the brief by the coordinator; reported here as required.)
3. **ERROR (A3, T=0).** `R_T ≤ J−1` is false when `T = 0`: `R_0 = J`. The final conclusion
   still holds (A5 gives `R_{u+1} ≤ R_T−1 = J−1`; the window certificate gives `R_u < J`), but
   the statement as written needs `T ≥ 1`.
4. **ERROR (A5 wording).** "The landing congruence is `v2(3k+θ_T) = 4`" is true only for
   **a-landings**; a b-landing has `j_u = ω(n_T) = 5`, i.e. `v2(6k+4) = 5`. The b-landing
   formulas themselves are correct. Also `θ_T ∈ {−2,6}` / `{14,−10}` is not a consequence of the
   landing class alone: the class fixes `θ_T mod 64`, and `|θ_T| ≤ Λ ≤ 13` is what pins it to
   the exact small value. Without the drift bound the resolved class is the general
   `3D_{u+1} ≡ (θ_T+12)−2^m` (a) or `(16−θ_T)−2^m` (b) mod `2^{m+1}`; e.g. the lift `θ_T = 62`
   (≡ −2 mod 64) gives a different class, which I verified algebraically. In the actual range
   `Λ ≤ 13`, the possible bare ties are only a-(5,5), b-(5,5), b-(5,−11); a-(5,−11) needs
   `θ_T = 14 > 13`.
5. **SCOPE (A1).** The drift set `θ_t = 2i−t+1` is proved for the **initial** deep segment only
   (under R1). A deep chain reached again after a shallow excursion is not covered by the
   recurrence; see gap 1.
6. **Minor/unstated cases.** `j_u ≤ 4` (chain u is terminal; no certificate needed),
   `X(n_T)` even (walk ends on the deep segment), and `T = 0` are harmless but not stated.
   Type-c landings are outside A4–A6 (R2 for c remains open), as in work_deep.

## Confirmed (independently re-derived / recomputed)

- **A1 [A, R1]** drift recurrence and set preservation (a: i′ = t−i+1, b: i′ = i); checked on
  all 131,071 a/b sequences of length ≤ 16 and on 1,841 real θ-walk steps at j ≥ 1000.
- **A2 [A, Λ ≤ 7,499,998 / 14,999,997]** no resonance; 3k ≥ 15,000,000 from
  τ(n) ≥ (n−1)/2 (verified at all 62,160,928 odd crossings of the 10^8 table; at the deep
  boundary n = 19,999,999, 3k = 26,764,062). For Λ ≤ 13 the claim is correct.
- **A3 [A, same range]** T ≤ Λ−1; L(j) < j, L monotone, L ≤ G, Λ(K_clock) = 4.
- **A4 [A+B]** T ≤ 12 ⇒ δ_a ∈ [−10,14], δ_b ∈ [−12,12] ⊂ [−12,15]. Independent full scan
  of the window certificate (5 ≤ j < 2·10^7, all 28 δ): 559,999,860 certificates, exactly the
  two failures (5,5), (5,−11). The [B] claim is reproduced exactly, not just sampled.
- **A5 algebra [A]** exact two-step identities verified on real crossings X(16) (a, k=6),
  X(53) (a, k=22), X(64) (b, ω=5, c′=3·2^63), and X(4) (a, k=1), for arbitrary odd u_T, plus
  208 symbolic cases; general class identities hold in every non-degenerate case. Only
  `mval = 0` (θ_T = −66, k = 6) degenerates, outside the drift window.
  b-crossing data c′ = 3·2^{n−1}, λ′ = 3τ+4 verified for all 1,239 odd b crossings < 4096.
- **A6 [B]** independent scans: 0 failures for all 5 ≤ m < 2·10^7 (40M certificates) and all
  5 ≤ m < 10^8 (200M certificates); literal slow certificate checked for m ≤ 2500 (4,992 cases)
  and random larger m; certificate implementation agrees with shiftlib/deep_lib (0 mismatches
  on random (j,δ); 0 on 800 resolved-class instances).
- **Data** τ ≥ (n−1)/2, CLOCK τ ≤ nP(n), λ bounds, ω < v2(c′), B+κ < 2^{n−3} (margin
  9,999,996 bits at n = N0); β-walk for all 19,999,995 J < 2·10^7: no tie, r_1 < J, records
  non-increasing. Full pair-map implementation matches the cached table and fdata on 4096
  crossings (0 mismatches).

**Bottom line.** A1, A4, A5 (algebra) and A6 are verified; A2/A3 are correct for Λ ≤ 13 but the
brief's range statement is wrong. The final implication is NOT complete: the bare-tie rescue
needs the unproved bound `m < 2·10^7` (gap 1). With that extra hypothesis added (and with
c-landings still open), the implication follows.
