# REPORT — Direction C: R2 for c-landings (agent C)

Full detail: `D:\math_cc\work_r1r2\agent_C\NOTES.md` (unreviewed).  Scripts and JSON in the same
directory.  Nothing outside `work_r1r2/agent_C/` was written; caches in `D:\math_cc_astra\`.

## Verdict

**R2(c) is not provable with the present tools, but it is reduced to an explicit congruence on the
deep calendar and, in the exhaustive ranges, is bypassed by an exact two-step resolution.**  The
canonical data show no unresolved case; the residual is arithmetic, not structural.  EXT is not
claimed; K_clock unchanged.

## What is proved [A]

Standing hypotheses of C1: `F` through `tau(J-1)`; `T` is the last deep chain (`j_T >= N0`, and
`D_T ≡ theta_T mod 2^{j_T}`, which holds under the deep/R1 hypotheses via work_deep Lemma 2.2 +
Theorem SC); the step at `T` is type c; `X(n_T)` odd; `j_u := omega(n_T) < N0`;
`sigma := v2(c'_W(n_T)) = n_T - eps(n_T)`.

* **C1 (class formula).** `r_u <= r_T - 1`, and
  `delta := D_u mod 2^{j_u+1} = theta_T + Phi - 2 = theta_T - 1 - lambda_Y  (mod 2^{j_u+1})`.
  With `3 tau(n_T) + 4 + lambda_Y = 2^{j_u} q`, `q` odd:
  **`delta ≡ theta_T + 3 tau(n_T) + 3 - 2^{j_u}  (mod 2^{j_u+1})`.**
  Hence the class depends only on `(theta_T, tau(n_T) mod 2^{j_u+1}, j_u)` — **not** on the higher
  bits of `lambda_Y`.  Key structural fact: the c-landing class is a function of the deep calendar
  `tau` at the deep index, plus `theta_T`.  For `T = 0` it reproduces the accepted ENTRY defect
  `-lambda_Y`.
* **C2.** `R2(c) ⟺ certify(j_u, delta)`, i.e. a statement about `tau(n_T) mod 2^{j_u+1}`.
* **C3 (necessary congruence).** If `X(j_u-1)` is odd type a, `k = k_{j_u-1}`, and
  `delta ≡ 2^{j_u-2} - 3k (mod 2^{j_u-1})`, then `certify` fails with first record `>= j_u+1`.
  Equivalently **`certify` fails whenever
  `tau(n_T) ≡ tau_0(theta_T) := 3^{-1}(2^{j_u-2} - 3 k_{j_u-1} - theta_T - 3)  (mod 2^{j_u-1})`**.
* **C4.** `j_u <= 4` ⇒ the walk ends at chain `u`; R2(c) automatic (no calendar input).
* **C5 (drift).** Under R1, `theta_T = 1 - b` (even #a) or `2 + b` (odd #a); exact reachable set
  `{1-b: 0<=b<=Lambda-1} ∪ {2+b: 0<=b<=Lambda-2}`, `|theta_T| <= Lambda`.  So for `Lambda = 4`
  (`K_clock`): `theta_T ∈ {-2..4}` — only 7 values.  Lemma C5' (explicit example) shows the
  c-landing condition does *not* constrain `tau mod 2^{j_u+1}`.
* **C6 (two-step resolution, generalized gateway lemma).** If `X(j_u-1)` is odd type a and
  `Q := 2 theta_T + 6 + 6 k_{j_u-1} + 6 tau(n_T) - lambda'_W(n_T)/2` satisfies
  `Q ≢ 0 (mod 2^{sigma-1})`, then the two-chain block (c-step + a-step) has
  `j_2 := j_{u+1} = v2(Q) < sigma-1`, `r_{u+1} <= r_T - 1`, the class of chain `u+1` is known mod
  `2^{j_2+1}` as `theta_{u+1} = (theta_T + 6 + 3 tau(n_T) + 3 tau(j_u-1) - Q) mod 2^{j_2+1}`, and
  `certify(j_2, theta_{u+1})` ⇒ all records from `u` on are `<= r_T - 1 < J`.  The landing class is
  **bypassed**; `j_2 <= log2(2 Lambda + 10 + 3 tau(j_u-1) +
  9 tau(n_T))`.  At `j_u = 5` this is the accepted gateway lemma; C6 generalizes it to every odd-a
  `j_u` and makes `Q` explicit (only `D_T ≡ theta_T mod 2^{j_T}` is used).
* **Negative results.** (i) No reduction to the earlier EXT instance: the landing state differs from
  the source epoch's real chain by `delta Theta = Theta_T - 2` (small 2-adic valuation), so HP does
  not transfer; it would need the extra congruence `3 d_T ≡ 1 (mod 2^sigma)`.  (ii) A-SOURCE, C3,
  C5-BA, CA, MINUS/PLUS, D-ROOT, duration normalization **do not apply**: they treat the *entry*
  `V(C,-1)` with `eps ∈ {3,5}`, whereas this is an interior chain with unbounded `eps(n_T)` and a
  small-valuation phase shift.  (iii) No size argument: without an NT failure the class walk's
  records are non-increasing, so the certificate is irreducibly a class statement.

## The exact reduced congruence

For `18 <= j_u <= 27`, `X(j_u-1)` odd type a (exhaustive; work_deep Cor 3.3 and my recomputation):
`R2(c) ⟺ tau(n_T) ≢ 3^{-1}(2^{j_u-2} - 3 k_{j_u-1} - theta_T - 3) (mod 2^{j_u-1})`.
For other `j_u <= 27` the bad set is empty (`j_u = 17`: one extra `(5,5)`-preimage class).
Density `2^{-(j_u-1)}` per `theta_T` (one residue class of `tau`).  For `j_u >= 28` only the `⟹`
direction is [A].

## Data [B] — `table_100000000.pkl`, deep segment `[2*10^7, 10^8)`, run 7 s

1,267,918 odd type-c crossings:
* **`omega = j_u ∈ {1: 150569, 3: 1115171, 5: 2178}` — all odd, all `<= 5`.**  So every canonical
  deep c-landing is terminal (`j_u <= 4`) or at `j_u = 5`.
* `eps ∈ {3, 5}`, `sigma - j_u >= 20,000,032`; `tau ∈ [1.78e7, 8.92e7]`.
* Only `j_u = 5` has bad classes: `delta ≡ 5 (mod 16)` (the tie class, `k_4 = 1`).
* At all 2178 `omega = 5` crossings: `tau ≡ 31 (mod 64)`, `lambda_Y ≡ 8191 (mod 8192)`, `eps = 3`;
  hence `delta ≡ theta_T (mod 64)`, and the bad class is exactly `theta_T ≡ 5 (mod 16)`.
* Bad pairs by `theta` set: window `[-30,30]`: 8712 (4 per crossing); **drift `Lambda = 4`: 0**;
  drift `Lambda = 13`: 4356 (`theta_T = -11, 5`); `theta_T = 1`: 0.
* **Every one of the 8712 bad pairs is resolved by C6**: `j_2 = v2(Q) ∈ {5, 6, 12}`,
  `certify(j_2, theta_{u+1})` at the mod-`2^{j_2+1}` class passes 8712/8712,
  `r_{u+1} <= r_T - 1` 8712/8712, unresolved 0.  (Exact big-int checks of the two-step identity,
  both class lifts, the certificate and the record bound: 198/198 at `n = 6132`, `j_T` up to `2·10^5`.)
* Misc: `tau mod 256` has only 11 distinct values (families 55/119/183/247 dominate);
  `tau mod 2^16` 1167 values, `mod 2^20` 18,630.  Class formula exact check: 20,988 big-int
  one-step walks at crossings `< 20000` (0 mismatches) + 198 at cached crossings;
  `Bad_j` recomputed `5 <= j <= 24` matches work_deep.

## Failure mode

The only way R2(c) fails is the tie congruence `C3`; in the exhaustive ranges that is the *only*
failure class (`j_u = 17` also the `(5,5)`-preimage).  At a c-landing this is not an EXT obstruction:
C6 gives a strict record descent and an explicit small-parameter continuation.  What remains open is
the certificate of that continuation, `certify(j_2, theta_{u+1})`, and (for `j_u >= 28`) whether
failure classes are still only the tie class.

## Best next step

1. Prove `certify(j_2, theta_{u+1})` at the two-step image, i.e. the *short-modulus* congruence
   `theta_T + 6 + 3 tau(n_T) + 3 tau(j_u-1) ∉ Bad_{j_2}` with `j_2 = v2(Q)` explicit.  This is the
   shape the accepted MINUS/PLUS-type family reductions handle, and `j_2` is logarithmic (canonically
   `<= 12`).
2. Extend the exhaustive `Bad_j` (currently `j <= 27`) to the `j_2` values that can occur, and prove
   `Bad_j` = tie class for all `j` (needed for `j_u >= 28`).
3. The `omega <= 5` and `tau ≡ 31 (mod 64)` regularities are calendar facts of the computed range
   [C]; a structural reason would make R2(c) automatic for `j_u = 5` and is worth looking for in
   the fire/return structure of the c-family (`X(6132)`-type gateways).
