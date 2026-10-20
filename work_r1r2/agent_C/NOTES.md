未经审查 / unreviewed

# DIRECTION C — R2 for c-landings (agent C, 2026-10-20)

Target: the landing step at the last deep chain `T` of `S(J)` is type c with `omega(n_T) < N0`
(the R1-compatible case).  Determine the landing class, decide whether R2 can be proved,
reduced, or shown automatic outside an explicit congruence.

**Verdict (one line).** The landing class is an explicit function of the *deep calendar*
`tau(n_T) mod 2^(j_u+1)` and of `theta_T` alone (Theorem C1); R2(c) is *exactly*
`certify(j_u, delta)` (C2) and its failure contains, hence in the exhaustive ranges *equals*,
one explicit congruence on `tau(n_T)` (C3, [B]); R2(c) is proved automatic for `j_u <= 4` (C4),
and — the new point — a failure at an odd-a `j_u` is **repaired by one exact two-step
resolution** at the deep predecessor, which lands at the small parameter
`j_{u+1} = v2(Q)` (C6).  Canonically (`[2*10^7, 10^8)`, 1,267,918 deep c-crossings) every
landing is automatic or repaired; no unresolved case exists in that range.  R2(c) is **not
proved in general**: the residual is a congruence on the deep calendar.  EXT is not claimed;
K_clock is unchanged.

Tags: **[A]** proved for all parameters (hypotheses stated), **[B]** finite exact computation
(range stated), **[C]** conjecture/data.

---

## 中文摘要

结论先行：**c 型着陆的类完全由深部日历决定**，R2(c) 不能证明，但可以被精确归约，并且在
“首次链 tie”这一（穷举范围内唯一的）失败模式下被**一次两步精确化解**自动修复。

1. **定理 C1 [A]（着陆类公式）**。设 `T` 是最后一个深链（`j_T >= N0`，`D_T ≡ theta_T mod 2^{j_T}`），
   该步为 c 型，`j_u := omega(n_T) = v2(3 tau(n_T)+4+lambda_Y) < N0`，`sigma := n_T - eps(n_T) = v2(c'_W)`。
   则 `r_u <= r_T - 1`（着陆链本身永远安全），且
   `delta := D_u mod 2^{j_u+1} = theta_T + Phi - 2 = theta_T - 1 - lambda_Y (mod 2^{j_u+1})`。
   写 `3 tau + 4 + lambda_Y = 2^{j_u} q`（q 奇），则
   **`delta ≡ theta_T + 3 tau(n_T) + 3 - 2^{j_u} (mod 2^{j_u+1})`**。
   所以类只依赖 `(theta_T, tau(n_T) mod 2^{j_u+1}, j_u)`，与 `lambda_Y` 的高位无关：
   这是本方向的结构性关键（c 型着陆的类是深部日历 `tau` 加 `theta_T` 的函数）。
   `T = 0` 时退化为已接受的 ENTRY 公式 `-lambda_Y`（一致性检验）。
2. **定理 C2/C3 [A]（归约与显式同余）**。R2(c) ⟺ `certify(j_u, delta)`。若 `X(j_u-1)` 为奇 a 型，
   `k := k_{j_u-1}`，则首链 tie 类 `delta ≡ 2^{j_u-2} - 3k (mod 2^{j_u-1})` **必然**使证书失败
   （记录 `>= j_u+1 > j_u`）。换成日历变量：
   **`tau(n_T) ≡ tau_0(theta_T) := 3^{-1}(2^{j_u-2} - 3k_{j_u-1} - theta_T - 3) (mod 2^{j_u-1})`**。
   在穷举范围 `5 <= j_u <= 27` 内反之亦真（`Bad_j` 恰为首链 tie 类；`j = 17` 另加 (5,5)-原像；
   `X(j_u-1)` 非奇 a 时 `Bad_j = empty`）。**一个同余不是证明。**
3. **定理 C4 [A]**：`j_u <= 4` 时走步在链 u 结束，R2 自动成立。
   **定理 C5 [A]**（漂移可达集）：R1 下 `theta_T = 1-b`（a 步数为偶）或 `2+b`（a 步数为奇），
   `b` = 深段 b 步数，`T <= Lambda-1`；故可达 `theta_T` 只有 `<= 2Lambda` 个值，`|theta_T| <= Lambda`。
   所以坏类 `mod 16` 至多命中可达集中的一个元素（可达集有 `< 16` 个值）；规范数据中该类恒为
   `5 mod 16`，与 `{-2..4}` 完全不相交（0 命中）。
4. **定理 C6 [A]（两步化解；广义 gateway 引理）**。若 `X(j_u-1)` 为奇 a 型且
   `Q := 2 theta_T + 6 + 6 k_{j_u-1} + 6 tau(n_T) - lambda'_W/2` 满足 `Q ≢ 0 (mod 2^{sigma-1})`，则两步块
   （c 步 + a 步）给出 `j_{u+1} = v2(Q) < sigma-1`、`r_{u+1} <= r_T - 1`、
   `theta_{u+1} ≡ theta_T + 6 + 3 tau(n_T) + 3 tau(j_u-1) (mod 2^{j_{u+1}})`；若再 `certify(j_{u+1}, theta_{u+1})`
   （`theta_{u+1}` 取 mod `2^{j_2+1}` 的精细类，而非仅 mod `2^{j_2}`）则链 u 及之后所有记录
   `<= max(r_u, r_{u+1}) <= r_T - 1 < J`（整个着陆类被绕过）。这把 `j_u` 处的（大模数、坏集只到 27 已知的）同余换成了 `j_{u+1} = v2(Q)`
   处的（小参数、坏集穷举已知的）证书。`j_u = 5` 时它就是已接受的 gateway 引理（含 (5,5)/(5,-11) 裸 tie）。
5. **反面结果 [A]**：(i) 不能把 R2(c) 归约到更早的 EXT 实例：着陆链与源 epoch 的实链之差
   `delta Theta = Theta_T - 2` 的 2-adic 赋值很小，HP 不成立（除非 `Theta_T ≡ 2 mod 2^sigma`，即
   `3 d_T ≡ 1 mod 2^sigma` 这一对时长的额外同余，未被接受结果蕴含）；(ii) 已接受的低亏损 c-source
   归约（A-SOURCE、C3、C5-BA、CA、MINUS/PLUS、D-ROOT、时长归一化）**不适用**：它们处理的是
   `S(J)` 的**入口**（链 1 是 `V(C,-1)`，`epsilon ∈ {3,5}`），而这里 c 交叉是内部链，亏损 `eps(n_T)`
   一般无界。
6. **数据 [B]**（`table_100000000.pkl`，深段 `[2e7, 1e8)`，1,267,918 个奇 c 交叉，7 s）：
   `omega = j_u ∈ {1, 3, 5}`（全为奇数，全部 <= 5！）；`eps ∈ {3,5}`；`sigma - j_u >= 2*10^7 + 32`。
   唯一非空 `Bad_j` 是 `j_u = 5`：4 个类 `mod 64`，即 `delta ≡ 5 (mod 16)`（首链 tie 类，`k_4 = 1`）。
   在全部 2178 个 `omega = 5` 交叉上 **`tau ≡ 31 (mod 64)`、`lambda_Y ≡ 8191 (mod 8192)`**，
   故 `delta ≡ theta_T (mod 64)`，坏类恰为 `theta_T ≡ 5 (mod 16)`。
   窗口 `theta_T ∈ [-30,30]`：8712 个坏对（每个交叉 4 个）；漂移集 `Lambda = 4`（扫描用超集
   `{-3..4}`，精确可达集 `{-2..4}`）：**0**；`Lambda = 13`（扫描用超集 `[-12,14]`，精确可达集
   `[-11,13]`）：4356 个（`theta_T = -11, 5`，两值都在精确集内）。
   **全部 8712 个坏对都被 C6 化解**：`j_2 = v2(Q) ∈ {5,6,12}`，`certify(j_2, theta_2)` 全部通过，
   `r_{u+1} <= r_T - 1` 全部成立，未化解 0。同余密度：`Lambda = 4` 时为 0；`Lambda = 13` 时 7.7%
   （理论上限 `|Bad_j|/2^{j+1} = 4/64 = 6.25%` 每个 theta）。
7. **没有证明**：R2(c)（一般情形）、`omega <= 5` 的结构性、同余回避、EXT。也没有改变 K_clock。

---

## 1. Notation and standing hypotheses

Machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`.  Standing imports (accepted, used as black
boxes): PROOF_EXT §2 walk rules and Lemmas K/HP/AB, PROP RB; PROOF_EL A1–A3, Lemma 1, Lemma T;
work_claude_shifted Theorem SC, Prop 3.2, §4 window certificate, §5 gateway lemma; work_deep
Lemmas 2.1–2.6, Cor. 2.7, Thm 3.1, Thm 3.4; work_ext_roots ENTRY and Lemma K(c).

* `F` defined through `tau(J-1)`; `S(J)` has chains `t = 0..r`, parameters `j_t`, loss
  `Gamma_t` (`Gamma_0 = 0`, `Gamma_{t+1} = Gamma_t + 1 + eps(n_t)`), record `r_t = j_t + Gamma_t`,
  `j_0 = J`, `n_t = j_t - 1`.  The step at chain `t` reads `X(n_t)`:
  * `X(n_t)` even: the exit ends at chain `t`;
  * type a, `tau = 2k`: `x' = 2 Theta + 6k - x/2`, `Theta' = Theta + 3 + 2k*3`; `eps = 0`;
  * type b/c: `x' = c'_W u + lambda'_W`, `j' = omega(n_t) = v2(lambda'_W)`, `Theta' = Theta + 3 + 3 tau`;
    `eps = n - v2(c'_W) >= 1`.  `v2(c'_W) > omega` (S1).
* Defect `D = Theta - x`; `theta_t` = `theta`-automaton value ([A], PROOF_EL A3):
  `theta_0 = 1`, a: `3 - theta`, b: `theta - 1`, c: `theta + Phi - 2` with
  `Phi = 3 tau + 5 - lambda'_W` (= 1 for b, = 1 - lambda_Y for c).  `D_t ≡ theta_t (mod 2^{j_t})`
  until the first NT failure (Theorem SC); at deep chains there is none (work_deep Lemma 2.2).
* `N0 = 2*10^7`, `B = 2^(10^7)`.  Deep: `j_t >= N0` and `|theta_t| <= B`.  `T` = last deep chain,
  `u = T+1` the landing chain.  `6 Lambda(J) + 4 <= B` (so `Lambda` is small; `Lambda(K_clock) = 4`).
* `R1`: no c-step at a deep chain keeps the walk deep.  `R2`: `certify(j_u, delta)`, where
  `certify(j, d)` = the exact walk from the representative `(2^j, 2^j + d)` ends with all records
  `<= j` (Prop 3.2 / work_deep Thm 3.1).
* `Bad_j := {d mod 2^{j+1} : certify(j, d) = false}`.
* Table (canonical, `fdata.lam_walk`): `typ`, `tau`, `eps`, `odd`, `lY = lambda_Y`, `lA`.
  Mass identity `lambda_A + lambda_Y = 3 tau + 1`, hence
  **`lambda'_W = lA + 2 lY + 3 = 3 tau + 4 + lambda_Y`** (ENTRY).
* Imported [A] facts of the coordinator (used): under R1, at every deep chain `theta_t` equals the
  integer a/b drift value, `|theta_t| <= Lambda(J)`, no resonance (`3k + theta != 0`), and
  `T <= Lambda(J) - 1`.

---

## 2. Theorem C1 — the landing class of a c-landing  [A]

**Hypotheses.** (H1) `F` is defined through `tau(J-1)` and `S(J)` has chains `0..u`.
(H2) chain `T = u-1` is deep and `D_T ≡ theta_T (mod 2^{j_T})` (holds under the standing deep
hypotheses: work_deep Lemma 2.2 + Theorem SC; also implied by the imported R1 drift facts).
(H3) `X(n_T)` is odd of type c, `j_u := j_{T+1} = omega(n_T) < N0`.  Write `x_T = 2^{j_T} u_T`
(`u_T` odd) and `sigma := v2(c'_W(n_T)) = n_T - eps(n_T)`.

**Theorem C1.**
1. `j_u < sigma <= j_T - 1`.
2. `r_u <= r_T - 1` (so the landing chain itself is never an EXT-tie).
3. Exact identity `D_u = D_T + u_T (2^{j_T} - c'_W) + 3 + 3 tau(n_T) - lambda'_W(n_T)`; consequently
   `delta := D_u mod 2^{j_u+1} = theta_T + Phi(n_T) - 2 = theta_T - 1 - lambda_Y(n_T)  (mod 2^{j_u+1})`.
4. Write `2^{j_u} q = 3 tau(n_T) + 4 + lambda_Y(n_T)` (so `q` is **odd**, by definition of `j_u`).
   Then `lambda_Y = -3 tau - 4 + 2^{j_u} q`, and since `q` is odd
   `2^{j_u} q ≡ 2^{j_u} (mod 2^{j_u+1})`; hence
   **`delta ≡ theta_T + 3 tau(n_T) + 3 - 2^{j_u}  (mod 2^{j_u+1})`**.
5. In particular `delta` is a function of `(theta_T mod 2^{j_u+1}, tau(n_T) mod 2^{j_u+1}, j_u)`
   only; it does not depend on `q`, i.e. on the higher bits of `lambda_Y`.

*Proof.* (1) is S1 (`omega < v2 c'`) plus `sigma = n_T - eps_T <= j_T - 1 - eps_T`.
(2) `Gamma_u = Gamma_T + 1 + eps_T` and `j_u <= sigma - 1 = n_T - eps_T - 1`, so
`r_u = j_u + Gamma_u <= n_T + Gamma_T = r_T - 1`.
(3) `x_u = c'_W u_T + lambda'_W`, `Theta_u = Theta_T + 3 + 3 tau`, and `Theta_T = x_T + D_T`, so
`D_u = Theta_u - x_u = D_T + u_T(2^{j_T} - c'_W) + 3 + 3 tau - lambda'_W`.  Here
`v2(2^{j_T} - c'_W) = v2(c'_W) = sigma` (as `sigma < j_T`), and `sigma >= j_u + 1` by (1); and
`D_T ≡ theta_T (mod 2^{j_T})` with `j_u + 1 <= j_T - 1`.  Reducing mod `2^{j_u+1}` kills
`u_T(2^{j_T}-c'_W)` and replaces `D_T` by `theta_T`; then use `lambda'_W = 3 tau + 4 + lambda_Y`
and `Phi = 1 - lambda_Y`.
(4) Algebra, as displayed.  (5) Immediate from (4).  ∎

*Consistency with accepted ENTRY.*  For `T = 0` (the fire chain itself is deep) `theta_0 = 1`, so
(3) reads `delta ≡ 1 - 1 - lambda_Y = -lambda_Y`, i.e. the accepted ENTRY defect of a c-source;
and (4) reads `-lambda_Y ≡ 3 tau + 4 - 2^{j_u} (mod 2^{j_u+1})`, which is the same statement.
The new content is `T >= 1`, where the outer argument `u_T` is not `1` and the shift relative to
the source chain is `Theta_T - 2` (see §6.1).

*Exact check [B].*  `check_small.py` V1 verifies (contiguously with big integers, not mod a
precomputed residue) at all 318 odd type-c crossings `n < 20000` and for `theta ∈ {1,0,-1,2,-2,3,-3,
5,-11,17,-17}`, `u ∈ {1,3,5,7,12345,2^40+1}` — 20,988 one-step walks, 0 mismatches of
`D' = theta + 3 tau + 3 - 2^{j'}` and 0 mismatches of `j' = omega`.  `scan_deep_c.py` repeats the
check on 198 further crossings from the cached table (0 failures).  At deep indices `c'_W` is not
stored; the formula uses it only through `v2(c'_W) >= j_u + 1`, which is exactly the table's
`sigma = n - eps > omega` (checked at every deep crossing, see §8).

---

## 3. Corollary C2 — reduction of R2(c); Theorem C3 — the congruence  [A]

**Corollary C2 [A].** At a c-landing, hypotheses of C1,
`R2(c)` ⟺ `certify(j_u, delta)` with `delta = theta_T + 3 tau(n_T) + 3 - 2^{j_u} mod 2^{j_u+1}`.
So R2(c) is a statement about the *deep calendar*: the residue of `tau(n_T)` mod `2^{j_u+1}`, plus
`theta_T` and `j_u`.

**Theorem C3 (first-chain tie fails the certificate) [A].** Let `X(j-1)` be odd of type a, `k = k_{j-1}`,
and let `delta ≡ 2^{j-2} - 3k (mod 2^{j-1})`.  Then `certify(j, delta) = false`, indeed the
representative's first record is `>= j+1`.

*Proof.* `n = j-1`.  The a-step ([PROOF_EL A2]) has
`j_1 = 1 + v2(Theta_0 + 3k - 2^{n-1} lambda_u) = 1 + v2(2^{n-1} lambda_u + z)`, `z = 3k + delta`.
The hypothesis says `z = 2^{n-1} z'` with `z'` odd, so `2^{n-1}(lambda_u + z')` with
`lambda_u + z'` even: the valuation is `>= n`, hence `j_1 >= 1 + n = j` and
`r_1 = j_1 + 1 >= j+1 > j`.  ∎

(`delta ≡ -3k mod 2^{j-1}`, the one-step-descent class `v2(z) >= j-1`, is different: then
`j_1 = j-1`, `r_1 = j`, and the certificate may survive; see work_claude_shifted Lemma 1.3.)

**Corollary C3' (the reduced congruence) [A].** At a c-landing with `X(j_u-1)` odd type a,
`certify(j_u, delta)` fails whenever

  `theta_T + 3 tau(n_T) + 3 ≡ 2^{j_u-2} - 3 k_{j_u-1}  (mod 2^{j_u-1})`

i.e. (multiplying by `3^{-1}`, which exists mod `2^{j_u-1}`)

  **`tau(n_T) ≡ tau_0(theta_T) := 3^{-1} (2^{j_u-2} - 3 k_{j_u-1} - theta_T - 3)  (mod 2^{j_u-1})`.**

Because `delta` is affine in `tau`, this is one residue class of `tau` modulo `2^{j_u-1}`:
`2^{-(j_u-1)}` of all `tau`, equivalently `4` classes of `delta` mod `2^{j_u+1}`.

*Remark C3'' [B].* In the exhaustive range the converse holds and `Bad_j` is *exactly* this class:
`Bad_j = 4` classes for `j ∈ {5,8,12,14,22,24}`, `8` for `j = 17` (the tie class plus the
`(5,5)`-preimage class), `empty` for every other `5 <= j <= 24` (my recomputation, `check_small.py`
V2/V3, 77 s at `JMAX = 24`; agrees with work_deep V1 and its `j = 25,26 (empty) / 27 (tie)` run).
So for `5 <= j_u <= 27`:
* `X(j_u-1)` not odd-a: R2(c) holds automatically;
* `X(j_u-1)` odd-a: R2(c) ⟺ `tau(n_T) ≢ tau_0(theta_T) (mod 2^{j_u-1})`, except `j_u = 17` where one
  extra class must also be avoided.

For `j_u >= 28` only the `⟹` direction is [A]; the converse is [C] (work_deep V8 samples support it
for `j <= 80`).

---

## 4. Corollary C4 — terminal landings  [A]

If `j_u <= 4`, then `j_u - 1 <= 3` and `X(0..3)` are even-headed (PROOF_EL Lemma 1); the walk ends at
chain `u`, and `certify(j_u, delta)` holds trivially (the representative ends with record `j_u`).
So **R2(c) is automatic for `j_u <= 4`** — no congruence, no calendar input.

Canonically this covers *everything except* `j_u = 5` (§8: `omega ∈ {1,3,5}`).

---

## 5. Theorem C5 (drift reachable set) and Theorem C6 (two-step resolution)

### C5 — `theta_T` is small and explicitly enumerable [A]

**Theorem C5.** Under R1 (no deep-to-deep c-step) and the standing deep hypotheses, let
`b` = number of b-steps and `a` = number of a-steps among the steps at chains `0..T-1` (`a+b = T`).
Then

  `theta_T = 1 - b` if `a` is even,   `theta_T = 2 + b` if `a` is odd.

With `a+b = T <= Lambda-1` the exact reachable set is
`{1-b : 0 <= b <= Lambda-1} ∪ {2+b : 0 <= b <= Lambda-2}` (at most `2 Lambda - 1` elements, all of
modulus `<= Lambda`, matching the imported bound).  For `Lambda = 4` (`K_clock`):
`theta_T ∈ {-2,-1,0,1,2,3,4}`.  For `Lambda = 13`: `[-11,13]`.  (The scan of §8 uses the one-larger
supersets `{1-b : 0 <= b <= Lambda} ∪ {2+b : 0 <= b <= Lambda-1}`, i.e. `{-3..4}` and `[-12,14]`, so
its zero-hit finding is a fortiori valid for the exact sets; the two `Lambda = 13` hit values
`theta_T = -11, 5` lie in the exact set.)

*Proof.* With `phi = theta - 3/2`, an a-step is `phi -> -phi` and a b-step is `phi -> phi - 1`.
So `phi_T = (-1)^a (phi_0 - b) = (-1)^a (-1/2 - b)`, giving `theta_T = 3/2 ± (-1/2 - b)`.  The
integer representative is `3 - theta` resp. `theta - 1` at a/b steps because `|theta| <= Lambda << 2^{j_t-1}`
(one-step descents included, work_claude_shifted Lemma 1.3).  ∎

**Lemma C5' (no interaction) [A].** The c-landing condition does not constrain `tau mod 2^{j_u+1}`:
for `j_u = 5`, `theta_T = 2`, `tau = 16` we have `lambda_Y = 44`, `3 tau + 4 + lambda_Y = 96 = 2^5·3`
(so `q = 3` odd, `0 <= lambda_Y <= 3 tau + 1`), and the class is `delta = 21 mod 64 ∈ Bad_5`.  So a bad
c-landing is arithmetically consistent with every constraint; only the calendar can exclude it.
(It is not claimed that such a crossing exists canonically.)

### C6 — exact resolution of the two-chain block [A]

**Theorem C6.** Hypotheses of C1, and in addition `X(j_u-1)` is odd of type a; put
`k = k_{j_u-1}`, `tau_2 = tau(j_u-1)`, and

  `Q := 2 theta_T + 6 + 6k + 6 tau(n_T) - lambda'_W(n_T)/2`.

Assume `Q ≢ 0 (mod 2^{sigma-1})`; put `j_2 := v2(Q)` (then `j_2 < sigma - 1`).  Then:
1. `x_{u+1} = Q' + u_T (2^{j_T+1} - c'_W/2)` with `Q' ≡ Q (mod 2^{j_T+1})`, `v2(c'_W/2) = sigma - 1`;
   hence `j_{u+1} = j_2` (the tie is resolved without any information about `u_T`);
2. the class of chain `u+1` is known modulo `2^{j_2+1}`:
   `theta_{u+1} := (theta_T + 6 + 3 tau(n_T) + 3 tau_2 - Q) mod 2^{j_2+1}`
   (modulo `2^{j_2}` this is just `theta_T + 6 + 3 tau(n_T) + 3 tau_2`, since `Q ≡ 0 mod 2^{j_2}`);
3. `r_{u+1} = j_2 + Gamma_T + 2 + eps_T <= r_T - 1`;
4. if `certify(j_2, theta_{u+1})` holds (`theta_{u+1}` the class mod `2^{j_2+1}` of item 2), then
   every record of `S(J)` at and after chain `u` is
   `<= max(r_u, r_{u+1}) <= r_T - 1 < J` (chain `u` itself is safe by C1(2)).

*Proof.* 1. `x_u = c'_W u_T + lambda'_W`, `Theta_u = Theta_T + 3 + 3 tau(n_T)`, and the a-step gives
`x_{u+1} = 2 Theta_u + 6k - x_u/2 = Q' + u_T(2^{j_T+1} - c'_W/2)` with
`Q' = 2D_T + 6 + 6k + 6 tau - lambda'_W/2`.  `Q' - Q = 2(D_T - theta_T) ≡ 0 (mod 2^{j_T+1})`, and
`sigma - 1 <= j_T - 2 < j_T + 1`, so `Q' ≡ Q (mod 2^{sigma-1})`; the `u_T` term has valuation
`sigma - 1` because `sigma - 1 < j_T + 1`.  So `v2(x_{u+1}) = v2(Q)`.
2. `Theta_{u+1} = Theta_u + 3 + 3 tau_2 = Theta_T + 6 + 3 tau(n_T) + 3 tau_2 ≡ theta_T + 6 + 3 tau
+ 3 tau_2 (mod 2^{sigma-1})` (`sigma - 1 < j_T` and `Theta_T ≡ theta_T mod 2^{j_T}`), and
`x_{u+1} ≡ Q (mod 2^{sigma-1})` by item 1; so `D_{u+1} = Theta_{u+1} - x_{u+1}` is known mod
`2^{sigma-1}`, hence mod `2^{j_2+1}` because `j_2 + 1 <= sigma - 1`.  (The certificate needs the
class mod `2^{j_2+1}`, not only mod `2^{j_2}`: this is the lift-bit issue of
work_claude_shifted §4, and it is resolved here because the extra precision `sigma - 1` is
available.)
3. `Gamma_{u+1} = Gamma_T + 2 + eps_T` (the second step is type a, `eps = 0`) and
`j_2 <= sigma - 2`; `sigma = j_T - 1 - eps_T`.
4. Apply work_deep Thm 3.1 (HP at precision `j_2+1`) at chain `u+1`: all later records satisfy
`r_w <= j_2 + Gamma_{u+1} = r_{u+1} <= r_T - 1 < J`.  ∎

*Size of `Q`.*  `|Q| <= 2 Lambda + 10 + 3 tau(j_u-1) + 9 tau(n_T)`, so
`j_2 <= log2(2 Lambda + 10 + 3 tau(j_u-1) + 9 tau(n_T))` — a *logarithmic* bound, and canonically
`j_2 <= 12` (§8 S6).  The hypothesis `Q ≢ 0 (mod 2^{sigma-1})` fails only if this explicit integer is
`0 mod 2^{sigma-1}`, with `sigma - 1 >= j_T - 2 - eps_T` (canonically `>= 2*10^7 + 32`); it did not
occur in any canonical case (§8).

**Consequence (the repair).** C6 applies to *any* c-landing with odd-a landing parameter, whether or
not `certify(j_u, delta)` holds, and it *bypasses* the landing class: the two-step block is exact and
its output is the explicit small-parameter state `(j_2, theta_{u+1})`.  So in the exhaustive ranges
(where the only failure classes are the tie class and, for `j_u = 17`, the `(5,5)`-preimage) R2(c) can
always be replaced by `certify(j_2, theta_{u+1})`.  For `j_u = 5` this is precisely the accepted
gateway lemma (work_claude_shifted §5: the cases `delta ≡ 5 (mod 16)` = the bare ties `(5,5)`,
`(5,-11)` and their two other lifts); C6 is its generalization to every odd-a `j_u`, and it makes the
arithmetic of `Q` explicit (the accepted lemma writes it with `D_p`; here `D_T ≡ theta_T mod 2^{j_T}`
suffices, because `Q' ≡ Q mod 2^{j_T+1}` and `sigma - 1 < j_T + 1`).

**What is still needed.** `certify(j_2, theta_{u+1})` is a *new* congruence, of modulus
`2^{j_2+1}` with `j_2 = v2(Q) <= log2(2 Lambda + 10 + 3 tau(j_u-1) + 9 tau(n_T))` (canonically
`<= 12`, §8).  It is
decidable by the exhaustive tables whenever `j_2 <= 27`.  C6 therefore turns a congruence at the
*landing* parameter (large modulus, bad set known only up to `j <= 27`) into a congruence at a
*small* parameter (small modulus, bad set known).  It is a reduction, not a proof.

---

## 6. Negative results — what does not work  [A]

### 6.1 No reduction to the earlier EXT instance

By Lemma K(c), `tau(n_T)` is an a-return time of the source epoch `E` and W's chain at `tau(n_T)` is a
**real chain** `C_{t+1}` of `E`, with parameter `j_u` and precision
`sigma_{t+1} = v2(alpha) = J_W - Gamma^E_{t+1} = sigma`.  At a least strict-EXT counterexample the
source epochs of the deep segment have fire parameter `J_W < J` and are tie-free by minimality
(imported hypothesis, work_deep §4); by Lemma T, `E`'s records relative to `C_{t+1}` are `< sigma`.  The landing chain of `S(J)` is the `M_{u_T}`-image of `C_{t+1}`, and its defect is
`delta ≡ D^E_{t+1} + theta_T - 2 (mod 2^{j_u+1})`, where `D^E_{t+1} = Phi(n_T) = theta^W` is the
exact defect of the real chain.

The two walks (landing vs `E` from `C_{t+1}`) read the same table and have

  `delta x_0 = c'_W (u_T - u_W)` (valuation `>= sigma`),   `delta Theta_0 = Theta_T - 2` (valuation `v2(Theta_T - 2)`).

HP needs `min(v2 delta Theta_0, v2 delta x_0) >= P`; since `Theta_T = 3 d_T + 1` is the `beta`-walk's
`Theta` at the deep chain (`d_T` = its duration), the transfer would require the extra congruence
`3 d_T ≡ 1 (mod 2^{sigma})`.  Nothing accepted implies it, and it is not a class statement.  The
divergence is immediate: after one a-step the difference becomes
`delta x' = 2 delta Theta - delta x/2`, of valuation `v2(Theta_T - 2)`.  So **`EXT(J_W)` does not
transfer to the landing**; the class certificate is the sharp `lambda_u`-uniform criterion
(cf. work_deep Remark 3.2).

### 6.2 The accepted low-deficit c-source reductions do not apply

C3, C5-BA, A-SOURCE, CA, MINUS/PLUS, D-ROOT and duration normalization analyze an **entry**: `S(J)`
whose chain 1 is `V(C,-1)` at a c-source `X(J-1)` with deficit `eps(J-1) ∈ {3,5}` (or the `eps = 7`
word grammar).  They need (i) the entry structure `V(C,-1)` (phase shift exactly `-1` at chain 1);
(ii) the source's own numerator `x_0 = 2^P U` to produce a high-valuation `Theta` difference
(`delta Theta = x_0`, `v2 = P-1`); (iii) a *bounded* deficit so that the source's weight word is one of
finitely many.  At an interior c-landing (T >= 1) all three fail: the phase shift is `Theta_T - 2`
(small valuation), the "numerator" is `c' u_T` whose leading bits are `u_T`-dependent, and
`eps(n_T) = n_T - sigma` is not a priori bounded.  What does apply at an interior c-landing:
Lemma K(c) (identifies the source epoch), Theorem SC / Prop 3.2 (the class certificate), the gateway
lemma (§5) and C1/C6 above.  (Boundary remark: for `T = 0` the c-landing *is* the entry case and the
accepted Theorem S(d) / Theorem W / C3 apply; C1 reduces to ENTRY there.)

### 6.3 Why no size argument closes R2(c)

The certificate asks for records `<= j_u`.  Without an NT failure the class walk's records are
non-increasing (a one-step descent keeps them, everything else lowers them), so the certificate is a
*class* statement and cannot be weakened by size.  A failure at chain `i >= 1` (a later tie) leaves
the parameter small (`<= j_u`), where the two-step resolution of C6 has no deep predecessor and the
higher bits needed are `u_T`-dependent.  So there is no size regime in which R2(c) becomes automatic;
the remaining freedom is exactly the congruence of C3/C3''.

---

## 7. The bare ties `(5,5)` / `(5,-11)`

At `j_u = 5`, `X(4)` is odd-a with `k_4 = 1`; `Bad_5 = {5,21,-11,-27} mod 64` = `delta ≡ 5 (mod 16)`
(`check_small.py` V2, and work_claude_shifted §4).  In `tau` form the condition is
`tau ≡ 6 + 5 theta_T (mod 16)`, which forces `theta_T` odd whenever `tau` is odd; canonically `tau` is
odd at 99.83 % of the deep c-crossings (the only exceptions are the `omega = 1`, `eps = 5` family of
2,178, where `lambda_Y` is even).

* With `Lambda = 4` (the `K_clock` scale) and `theta_T ∈ {-3..4}` (a superset of the exact drift set
  `{-2..4}`), the four lifts `{-27,-11,5,21}` of the class `5 mod 16` in the window `[-30,30]` contain
  **no** value of the drift set; correspondingly the canonical scan finds **0** bad pairs at
  `Lambda = 4`.
* With `Lambda = 13` the drift set (superset `[-12,14]` used in the scan; exact `[-11,13]`) contains
  `-11` and `5`; both are hit (4356 bad pairs = 2178 crossings x 2).
* In every hit C6 resolves the tie: `j_2 = v2(Q) ∈ {5,6,12}` and `certify(j_2, theta_{u+1})` holds
  (8712/8712).  So the bare tie is a real, computable configuration for `Lambda >= 13`, but it is not
  an obstruction to EXT at a c-landing.

---

## 8. Canonical data  [B]

Table `D:\math_cc_astra\deep1\table_100000000.pkl` (built by work_deep with `fdata.lam_walk`,
read-only), deep segment `[N0, N) = [2*10^7, 10^8)`.

**S1. Population.** 1,267,918 odd type-c crossings.  `sigma - omega >= 20,000,032`;
`tau ∈ [17,842,743, 89,213,529]`, `lambda'_W <= 401,460,878`.

**S2. Landing parameter.** `omega = j_u ∈ {1 : 150569, 3 : 1115171, 5 : 2178}` — **all odd, all <= 5**.
`eps ∈ {3 : 1265740, 5 : 2178}`.  `tau` is odd except for 2178 crossings (`omega = 1`, `eps = 5`,
`lambda_Y` even).  So every canonical deep c-landing in this range has `j_u <= 5`:
`j_u <= 4` (automatic, C4) or `j_u = 5`.

**S3. Bad sets.** `Bad_1 = Bad_3 = empty`; `Bad_5` = the 4 tie classes `delta ≡ 5 (mod 16)`.

**S4. `omega = 5` structure (2178 crossings).** All satisfy
`tau ≡ 31 (mod 64)`, `lambda_Y ≡ 8191 (mod 8192)`, `lambda'_W ≡ 32 (mod 64)`, `eps = 3`.  Hence
`delta ≡ theta_T (mod 64)`, and the bad class is `theta_T ≡ 5 (mod 16)` (a single class for the whole
range: `bad_theta_class_counts = {'5': [[5, 2178]]}`).

**S5. Bad-class counts over `theta_T`** (window `[-30,30]`, the drift set of C5 for `Lambda = 4` and
`Lambda = 13`, and `theta_T = 1`):

| theta set | pairs | bad pairs | density |
|---|---|---|---|
| window `[-30,30]` (61 values) | 132,858 | 8,712 | 6.56 % |
| drift `Lambda = 4` (superset `{-3..4}`) | 17,424 | **0** | 0 |
| drift `Lambda = 13` (superset `[-12,14]`) | 56,628 | 4,356 | 7.69 % |
| `theta_T = 1` | 2,178 | **0** | 0 |

The 8712 window hits are exactly `4` per `omega = 5` crossing (the four lifts of `5 mod 16` in
`[-30,30]`); the theoretical density `|Bad_5|/2^6 = 1/16 = 6.25 %` per `theta`.

**S6. Two-step resolution (C6) of every bad pair.** 8,712/8,712 resolved:
`Q ≢ 0 (mod 2^{sigma-1})` in all cases, `j_2 = v2(Q) ∈ {5 : 4356, 6 : 2178, 12 : 2178}`,
`certify(j_2, theta_{u+1})` **passes in all 8,712** (`theta_{u+1}` = the `mod 2^{j_2+1}` class
`(theta_T + 6 + 3 tau(n_T) + 3 tau_2 - Q)`), and `r_{u+1} <= r_T - 1` in all 8,712.
Unresolved: 0.  So in `[2*10^7, 10^8)` every canonical deep c-landing (for every `|theta_T| <= 30`) is
either directly certified or repaired.

**S7. `tau` mod small powers.** Among the 1,267,918 crossings: `tau mod 256` takes only 11 distinct
values (top: 55, 119, 183, 247, each ~278,792; 89: 139,397; 95: 2,178 = the `omega = 5` family;
98: 2,178 = the even-`tau` family).  `tau mod 2^16`: 1,167 distinct values (max multiplicity 1,090);
`tau mod 2^20`: 18,630 distinct (max multiplicity 69).  So the deep calendar is *very* far from
uniform: the crossings come in a handful of arithmetic-progression families.

**S8. Exact spot checks.** Class formula: 198/198 at crossings `< 2048` (plus 20,988 at crossings
`< 20000` in S1 of §2).  `certify` vs `Bad` membership: 10/10.  Bad_j recomputation `5 <= j <= 24`:
matches work_deep exactly (4 classes at `j ∈ {5,8,12,14,22,24}`, 8 at `j = 17`, else empty).

**Interpretation.** In the whole canonical deep range the answer to "does R2(c) fail?" is: only at
`j_u = 5`, only for `theta_T ≡ 5 (mod 16)`, and never for `|theta_T| <= 4`; and every such failure is
repaired by C6.  This is *evidence*, not a proof: it is a finite range, and both `omega <= 5` and
`tau ≡ 31 (mod 64)` at `omega = 5` are calendar facts of this range, not theorems.

---

## 9. Reproduce

All commands run from `D:\math_cc\work_r1r2\agent_C` with `python -B` (CPython 3.14, standard library
only); read-only on the repository, caches in `D:\math_cc_astra\`.

```
python -B check_small.py 20000 24        # 52-78 s; writes check_small.json
python -B check_gateway.py 8000 8 6      # 0.2 s; writes check_gateway.json
python -B scan_deep_c.py                 # 7 s after the 2.4 s pickle load (100M table, 2.8 GB)
                                         # writes scan_deep_c.json
python -B scan_deep_c.py "D:\math_cc_astra\deep1\table_20000000.pkl" 1000000 2048 "<out>.json"
                                         # 15 s; small-range cross-check (omega in {1,3,5} as well)
```

Measured (two full re-runs, 2026-10-20): `check_small.py 20000 24` 52.2 s and 77.6 s (dominated by
the exhaustive `Bad_j`, `sum_{j<=24} 2^{j+1}` walks; the spread is OS caching of the 28 MB table);
`check_small.py 20000 22` 24.7 s; `check_gateway.py` 0.2 s (table load + 198 exact two-step cases at
`n = 6132`, `j_T ∈ {61, 1000, 200003}`, 6 arguments, both class lifts and the certificate);
`scan_deep_c.py` 7.0 s wall clock on the 100M table including the 2.4 s pickle load (a first version
spent 312 s constructing `2^{sigma-1}` as a big integer; the committed version compares bit lengths).  The 20M-table cross-check with
`N0 = 10^6` (301,130 crossings) took 15 s and reproduces `omega ∈ {1,3,5}`.

Logs: `check_small.json`, `check_gateway.json`, `scan_deep_c.json`, `scan_deep_c_run.log`.

---

## 10. Scope

**Proved [A] (hypotheses stated):** Theorem C1 (class formula; items 1–5), Corollary C2, Theorem C3
(first-chain tie fails the certificate), Corollary C3' (the congruence), Corollary C4 (`j_u <= 4`
automatic), Theorem C5 (drift reachable set), Lemma C5' (no interaction, by explicit example),
Theorem C6 (two-step resolution), §6.1 (the HP obstruction to using the source epoch), §6.2 (why the
low-deficit machinery does not transfer), §6.3 (no size argument).

**Proved [B]:** the exhaustive `Bad_j` for `5 <= j <= 24` (and the cited `j = 25,26,27` from work_deep);
the equivalence `Bad_j` = first-chain tie classes for `5 <= j <= 27` (with the `j = 17` exception);
S1–S8 of §8 (range `[2*10^7, 10^8)`).

**Conjecture / data [C]:** `omega` odd and `<= 5` at deep c-crossings, and `tau ≡ 31 (mod 64)` /
`lambda_Y ≡ -1 (mod 8192)` at `omega = 5`, beyond the computed range; the converse direction of
Corollary C3'' for `j_u >= 28`.

**Not proved:** R2(c) in general; in particular the avoidance of the congruence
`tau(n_T) ≡ tau_0 (mod 2^{j_u-1})` for odd-a `j_u`, and the certification of the two-step image
`(j_2, theta_{u+1})` at astronomical indices.  R1 is untouched.  EXT is not claimed, no horizon change,
no statement about whether the machine halts.

**Best next step.** At a least EXT counterexample, R2(c) can now be assumed to hold *or* to be
repaired by C6 (in the exhaustive ranges), so the c-frontier is: prove that the two-step image
`(j_2, theta_{u+1})` is certified, i.e. that
`theta_T + 6 + 3 tau(n_T) + 3 tau(j_u-1) ≢` the bad classes mod `2^{j_2+1}`.  Equivalently, since
`j_2 = v2(Q)` with the explicit `Q`, this is a *short-modulus* calendar statement — much more
tractable than the original `2^{j_u-1}` congruence, and it is exactly the class of statement that
the accepted `MINUS/PLUS`-type family reductions were built for.
