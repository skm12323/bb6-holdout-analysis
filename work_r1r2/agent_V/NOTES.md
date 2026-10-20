未经审查 / unreviewed
# agent_V 对抗性复核：BB(6) #1 深段 R1/R2（Theorem A）

机器 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`。本文件只复核"深段 R1 ∧ R2 ⇒ EXT"这一步，
**没有**证明 EXT，没有改变 K_clock，没有声称 #1 不停机。所有代码在本目录，缓存表只读。

## 中文摘要

我独立重写了 pair map F、交叉表访问、精确 walk、θ̃-walk 和证书（`vlib.py`），
不听信被审代码的证书逻辑；只用缓存表作为数据，并在 4096 个交叉上用自己的 pair map
逐项核对表（0 不一致）。结论：

**主要缺陷（按重要性）**

1. **GAP（最重要）：A5→A6 的桥缺少 `m < 2·10^7`。** A5 只给出 `m = j_{u+1} ≤ j_T−3`
   （b 型 `≤ j_T−4`），而 A6 的有限证书只覆盖 `5 ≤ m < 2·10^7`（我独立验证到 `10^8`）。
   在 `Λ(J) ≤ 13` 的范围内，最后深链可以是 `T=1` 且 `j_T = j_1 ≤ L(J) ≈ log2 J`；
   对 `J < T_13` 这是高度约 11 的塔，远大于 `2·10^7`。于是
   `m = v2(θ_T+12+9k)`（a）或 `v2(2θ_T+10+9k)`（b）可以达到 `≈ log2(9k) ≈ log2 j_T`，
   **超过 `2·10^7`**。此时 `u+1` 链又是深链（`j ≥ N0`，θ=−2 或 14），A6/查表不适用；
   而且重入深段的漂移窗口整体偏移，之后 a/b 着陆的 `δ=3−θ` 可低到 `1−3l`
   （`l ≤ 2Λ+1`），θ=14 时更低，**不再落在 [−12,15]**，A4 的窗口论证也不覆盖。
   因此"裸 tie 情形由 A5+A6 闭合"只在额外假设 `m < 2·10^7` 下成立，而该假设未证。
   `gap_m.py` 给出非空性证据：取 θ_T=−2 时，`k ≡ −10/9 (mod 2^{2e7+1})` 与
   `k ≡ 6 (mod 32)` 相容（`k mod 32 = 6`, `v2(3k−2)=4`），故 a 型裸 tie (5,5) 与
   `m ≥ 2e7+1` 可同时满足（这是代数配置，不断言它由某个 S(J) 实现）。

2. **ERROR（A2/A3 的陈述范围）：** 简报中 `2(B−4)/6+1 < 3.34·10^6` 是**假的**：
   `(B−4)/6` 在这里有 3,010,300 位十进制数字。由漂移 `|θ_t| ≤ t+1 ≤ Λ`，无共振
   `3k+θ_t ≠ 0` 只在 `Λ ≤ 14,999,997`（精确漂移）或 `Λ ≤ 7,499,998`（粗界 `2Λ+1`）时成立；
   仅 `6Λ+4 ≤ B` 不够。A3 的 `T ≤ Λ−1` 同样只在这个范围内成立。最终的 `Λ ≤ 13`
   不受影响（`2Λ+1 = 27 ≪ 3k ≥ 15,000,000`）。协调者已确认此更正。

3. **ERROR（A3，T=0）：** `R_T ≤ J−1` 在 `T=0` 时是假的：`R_0 = J`。结论仍成立
   （A5 给 `R_{u+1} ≤ R_T−1 = J−1`；窗口证书给 `R_u < J`），但该句需要 `T ≥ 1`。

4. **ERROR（A5 措辞）：** "着陆同余 `v2(3k+θ_T)=4`" 只对 **a 型**着陆成立；b 型着陆是
   `j_u = ω(n_T) = 5`，即 `v2(6k+4)=5`。b 型公式本身正确。另外
   `θ_T ∈ {−2,6}` / `{14,−10}` **不是**仅由着陆类推出的：着陆类只定 `θ_T mod 64`，
   是漂移界 `|θ_T| ≤ Λ ≤ 13` 把它钉到这些小值。没有漂移界时一般类是
   `3D_{u+1} ≡ (θ_T+12)−2^m`（a）或 `(16−θ_T)−2^m`（b）`(mod 2^{m+1})`；
   例如 `θ_T=62`（仍 ≡−2 mod 64）给出不同类，我按代数验证了它不属于 A6 声称的
   `(10−2^m)/3`。在 `Λ≤13` 下可能的裸 tie 只有 a-(5,5)、b-(5,5)、b-(5,−11)；
   a-(5,−11)（θ=14）被 `|θ|≤13` 排除。

5. **SCOPE（A1）：** 漂移集 `θ_t = 2i−t+1` 只对**初始深段**的链成立（R1 下）。
   若着陆后参数经浅段 tie 反弹回 `≥N0`，重入链不满足该递推（见缺陷 1）。

6. **未明说的边界（都无害）：** `j_u ≤ 4` 时链 u 终止（无需证书）；`X(n_T)` 偶时
   在深段终止；`T=0`；c 型着陆不在 A4–A6 范围内（R2 对 c 仍开放，与 work_deep 一致）。

**已确认的主要结论**

- A1 递推/漂移集 [A]：a: `i' = t−i+1`，b: `i' = i`；穷举所有 ≤16 步 a/b 序列（131,071 条）
  和 1,841 个真实 `j≥1000` 的 θ̃-walk 步，0 失败。
- A2 在 `Λ≤13` 正确：`3k ≥ 15,000,000` 来自 `τ(n) ≥ (n−1)/2`（在 10^8 表全部
  62,160,928 个奇交叉上验证，0 反例；深界 `n=19,999,999` 处 `3k=26,764,062`）。
- A3 在修正范围内：`T ≤ Λ−1`；`L(j)<j`、`L` 单调、`L≤G`、`Λ(K_clock)=4`。
- A4 [A+B]：`Λ≤13 ⇒ T≤12 ⇒ δ_a∈[−10,14], δ_b∈[−12,12] ⊂ [−12,15]`。我独立**全扫**
  窗口证书 `5≤j<2·10^7, δ∈[−12,15]`：559,999,860 个证书，**恰有 2 个失败**
  `(5,5),(5,−11)`；不是抽样，是完整重算。
- A5 代数 [A]：在真实交叉 `X(16)`（a,k=6）、`X(53)`（a,k=22）、`X(64)`（b,ω=5,
  c′=3·2^63）和 `X(4)`（a,k=1）上，对任意奇数 `u_T` 精确验证两步恒等式；另 208 个
  符号代数例。一般类恒等式在所有非退化情况成立；唯一失败是 `mval=0` 的退化
  （θ_T=−66,k=6，超出漂移窗口）。全部 1,239 个 n<4096 的奇 b 交叉满足
  `c′=3·2^{n−1}`, `λ′=3τ+4`, `ω=v2(λ′)`。
- A6 [B]：独立全扫 **0 失败**：`5≤m<2·10^7`（40,000,000 个证书）和
  `5≤m<10^8`（200,000,000 个证书），两类 `(10−2^m)/3`, `(26−2^m)/3`。字面慢证书
  在 `m≤2500` 上 4,992 例全部通过；证书实现与 `deep_lib.certify`（即 work_deep/verify_deep.py 中同名实现抽出的库版本）
  和 `shiftlib` 在随机 (j,δ) 上 0 不一致（含 800 个 resolved-class 实例）。
- 数据 [B]：10^8 表上 `τ ≥ (n−1)/2`、CLOCK `τ ≤ nP(n)`、`λ_Y ≤ 3τ+1`、
  `ω < v2(c′)` 全部成立（0 反例）；`B+κ < 2^{n−3}`（n=N0 处余量 9,999,996 位）；
  β-walk 对全部 19,999,995 个 `J<2·10^7`：无 tie、`r_1<J`、记录不增（max 3 链）。

**Bottom line.** A1、A4、A5（代数）、A6 验证通过；A2/A3 在 `Λ≤13` 正确但简报的
范围陈述错误。最终蕴含**不完整**：裸 tie 的补救需要未证的 `m<2·10^7`；补上该假设
（且 c 型着陆另行处理）后蕴含成立。R2 本身在裸 tie 处按定义是失败的（A4 的
"except possibly"），A5+A6 是更强的闭合论证，不是 R2。

---

## 0. Verdict table

| claim | verdict | exact defect / scope |
|---|---|---|
| A1 drift | **VERIFIED [A]**, scope corrected | under R1; initial deep segment only; resonant a-step OK (θ→3−θ, j→j−1); re-entry excluded |
| A2 no resonance | **ERROR as stated; VERIFIED for Λ≤13** | brief's `2(B−4)/6+1<3.34e6` false; valid Λ ≤ 7,499,998 (crude) / 14,999,997 (sharp) |
| A3 count | **ERROR (T=0) + same range caveat; otherwise VERIFIED** | `R_T≤J−1` fails at T=0; T≤Λ−1 only under no resonance |
| A4 window | **VERIFIED [A+B] for Λ≤13** | full 5.6·10^8 certificate scan; exactly (5,5),(5,−11) fail |
| A5 gateway | **ALGEBRA VERIFIED [A]; GAP m<2e7; wording errors** | b-congruence is v2(6k+4)=5; θ_T values need drift; m not bounded by 2e7 |
| A6 classes | **VERIFIED [B] to 10^8** | 0 failures; range stronger than claimed |
| final implication | **GAP** | needs m<2e7; re-entry window shift; c landings outside scope |
| data | **VERIFIED [B]** | τ lower/CLOCK/λ/ω/size; β-walk all J<2e7 |

---

## 1. Setting and independent implementation

`vlib.py` contains:
- `my_small_full(NS)`: my own implementation of the formal pair map F from
  work_g6/PROOF_G6.md §5.1 (even step / chain, S1/S2, M_u images, D / push order). It matches
  the accepted `fdata.small_full` on all 4,096 crossings and the cached table's
  typ/tau/eps/odd/lY/lA on the same prefix (0 mismatches).
- `Tab`: loader for the accepted cached tables (data input only), with `info(n)`:
  even / a,k / b,c(ω,Φ,ε); `lam = lA+2lY+3`.
- `theta_walk`: PROOF_EL A1–A3 θ̃-walk (a: z=3k+d, ND iff v2(z)=j−2, one-step descent if
  v2(z)≥j−1, else j′=1+v2(z), d′=3−d; b: d′=d−1; c: d′=d+Φ−2).
- `exact_walk`: exact integer walk from (x,Θ) with ceiling; my own.
- `certify_slow`: literal representative (2^j, 2^j+δ), precision j+1.
- `certify_fast`: one symbolic step then exact tail with precision j−loss (the accepted
  minimal-information certificate; used as a cross-check, not trusted for A6).
- `beta_walk`: Lemma BR β-walk of S(J), my own.

Cross-checks (0 mismatches unless stated): θ-walk 30,000 random; exact walk 3,000;
certificate vs shiftlib 20,000; vs deep_lib.certify (same code as verify_deep.py's certify)
20,000; β-walk 2,000 J;
resolved-class certificates vs deep_lib 800. `certify_fast` vs literal `certify_slow`
agrees except for 6 cases where the slow walk needs c′ beyond the small table NS
(`nodata`, not a logic difference).

## 2. A1 — drift

Rules on the initial deep segment (R1: no c-step at a deep chain keeps the walk deep):
every step is a or b, and θ changes by `3−θ` or `θ−1` as the exact symmetric representative
(the exactness needs `|3−θ| < 2^{j′−1}`; for deep→deep `j′ ≥ N0`, and `|θ| ≤ t+4 ≤ 1.5·10^7`).
Induction: `θ_0=1`; a-step `i′ = t−i+1`; b-step `i′=i`. Hence `1−t ≤ θ_t ≤ t+1`.
The resonant a-step also has `θ′=3−θ`, `j′=j−1` (Lemma 1.3), so it does not break the drift.
Verified: exhaustive over all 131,071 a/b step sequences of length ≤16; 1,841 real θ-walk
steps with `j≥1000` (3000 walks). Caveat: "for every deep chain" must be read as "for every
chain of the initial deep segment"; a re-deep chain after a shallow tie is not covered.

## 3. A2/A3 — resonance and count

Resonance at a deep a-step means `3k+θ_t=0`. On the initial deep segment, by A1 and the count,
`|θ_t| ≤ t+1 ≤ Λ`. At the deep boundary `n=j_t−1 ≥ N0−1 = 19,999,999`,
`τ(n) ≥ (n−1)/2` [A, verified], and τ is even at odd type-a crossings (verified), so
`τ ≥ 10,000,000`, `k ≥ 5,000,000`, `3k ≥ 15,000,000`. Contradiction if `Λ < 15,000,000`.
With the crude `2Λ+1`, the condition is `Λ ≤ 7,499,998`.
**The brief's claimed range is wrong**: `2(B−4)/6+1` is ~10^{3,010,300}, not < 3.34·10^6;
`6Λ+4≤B` alone does not give no-resonance. For the final `Λ≤13` it is fine.

Count: at non-resonant deep steps `j′ ≤ L(j)` (a: `1+⌊log2|z|⌋ ≤ 1+⌊log2(κ+B)⌋`;
b/c: `ω ≤ ⌊log2(6(j−1)P(j−1)+5)⌋`), so `j_T ≤ L^{(T)}(J)`; if chain T is deep,
`T < Λ(J)`, i.e. `T ≤ Λ−1`. Records: non-resonant a and b/c steps strictly decrease `j+Γ`;
resonant a keeps it. With no resonance, `R_T ≤ J−T` for T≥1; **T=0 gives R_0=J**.
Verified: `L(j)<j` for j≥N0 (exact at N0: L=10,000,001<j), `L` monotone, `L≤G` with
`G(j)=max(2log2j+3,10^7+2)`; `κ(j)<2^{j−4}` and `P(n)≤n` at samples up to 10^{100};
`Λ(K_clock)=4` (exponent comparison: `2^499997 ≫ 10^7`, plus `L^{(3)}(K_clock) ≥ 2^{499997}−3 > N0`).

## 4. A4 — window

`Λ≤13 ⇒ T≤12`; drift gives `θ_T∈[−11,13]`, hence
`δ_a=3−θ_T ∈ [−10,14]`, `δ_b=θ_T−1 ∈ [−12,12]`, both inside `[−12,15]`. For
`j_u ≥ 5` (if `j_u≤4` the walk terminates at u) Lemma 2.5 gives the exact class mod
`2^{j_u+1}`, and the symmetric representative is the displayed δ (since `|δ|≤14<2^{j_u−1}`).
Two hidden cases are excluded by the deep size bound: (i) a *one-step descent* at the last deep
chain (v2(3k+θ_T) ≥ j_T−1) would need |z| ≥ 2^{j_T−1}, contradicting
|z| ≤ κ(j_T)+|θ_T| < 2^{j_T−3}, unless z=0, which A2 excludes; hence j_u ≤ j_T−3 and
D_u ≡ 3−θ_T (mod 2^{j_u+1}) with no lift bit; (ii) the b-landing term u_T(2^{j_T}−c′) has
v2 = j_T−2 > j_u+1, so D_u ≡ θ_T−1 (mod 2^{j_u+1}). Without these, Lemma 2.5's resonant lift
would change the class by 2^{j_u}, far outside the window.
The accepted window certificate [B] then certifies except (5,5),(5,−11).

**Independent full recomputation** of the window claim (`full_window.py`):
for every `5≤j<2·10^7`, every `δ∈[−12,15]`, run `certify` (literal slow for j<64, the
one-step certificate for j≥64): **559,999,860 certificates, nfail=2**, exactly
`(5,-11)` (status ceiling, word 5,5) and `(5,5)` (ceiling, word 5,6). This reproduces the
[B] claim over its entire stated range, not just a sample. (A sampled run
`check_window.py` gives the same plus targeted NT-failure subsamples.)

## 5. A5 — bare-tie gateway

Derivation (mine, all exact):
- a-landing: `x_{u+1} = 5·2^{j_T−2}u_T + (D_T+12+9k)`,
  `D_{u+1} = −2^{j_T−2}u_T − 3k`; `m = v2(θ_T+12+9k) = j_{u+1} ≤ j_T−3`.
- b-landing: with `c′_W = 3·2^{j_T−2}`, `λ′_W = 3τ+4 = 6k+4`,
  `x_{u+1} = 13·2^{j_T−3}u_T + 2D_T+10+9k`,
  `D_{u+1} = −5·2^{j_T−3}u_T − D_T + 2 − 3k`; `m = v2(2θ_T+10+9k) ≤ j_T−4`.
- class: `3D_{u+1} ≡ (θ_T+12)−2^m` (a), `(16−θ_T)−2^m` (b) mod `2^{m+1}`. For exact
  in-window θ_T this is `(10−2^m)/3` (θ_T=−2 a, 6 b) or `(26−2^m)/3` (θ_T=14 a, −10 b).
- records: `R_{u+1} = m+Γ_T+2` (a) / `m+Γ_T+3` (b) `≤ R_T−1`.

Real instances checked exactly with my own c′ data:
`X(16)` (odd a, τ=12, k=6; θ_T=−2 → (5,5), m=6, class −18 mod 128),
`X(53)` (odd a, τ=44, k=22; θ_T=14 → (5,−11), m=5, class −2 mod 64),
`X(64)` (odd b, τ=52, λ′=160, c′=3·2^63; θ_T=6 → (5,5), m=8, class −82 mod 512;
θ_T=−10 → (5,−11), m=5, class −2 mod 64), for several odd u_T including 2^{70}+7.
`X(4)` is odd type a with τ=2 (k=1). All identities and record inequalities pass.

Symbolic: 208 cases with j_T=200, arbitrary k, u_T, and θ_T including lifts ±64 and huge
adds. The general class identity holds in all non-degenerate cases; the 4 failures are the
degenerate `9k+θ_T+12 = 0` (e.g. θ_T=−66,k=6 ⇒ mval=0, j_{u+1}=j_T−2), which is outside the
drift window (|θ_T| would exceed Λ).

**Defects found:** (i) the brief's "landing congruence v2(3k+θ_T)=4" is only for a-landings;
for b it is v2(6k+4)=5. (ii) `θ_T ∈ {−2,6}/{14,−10}` relies on `|θ_T|≤Λ`, not just the class
mod 64; a lift like θ_T=62 gives a different resolved class (e.g. (74−2^m)/3). (iii) **the
m<2e7 bridge is missing** (see §7). (iv) a-(5,−11) is impossible for Λ≤13 (θ=14>13).

## 6. A6 — resolved classes

My scan (`scan_A6.py`) computes the class `(D−2^m)/3 mod 2^{m+1}` for D=10,26 by the closed
form `3^{-1} mod 2^K` (no big-int inverse), handles m<64/≤K+1 exactly, and for m≥64:
- even n=m−1: certified (terminal chain 0, record m);
- a: `j1 = v2(2δ+6k) = 1+v2(10+9k)` (D=10) resp. `1+v2(26+9k)` (D=26). `j1≤4` ⇒ terminal;
  `j1≥6` ⇒ the θ̃-walk from `(j1, −1/3)` resp. `(j1,−17/3)` is NT-good for every j1 (checked
  6..129), so Theorem SC bounds relative records by j1 < m; `j1=5` is a bare tie at (5,−11)
  resp. (5,5), resolved by a 192-bit truncated exact walk;
- b/c: `θ1 = 3τ+3+δ`, the exact walk from `(λ′, θ1 mod 2^192)` runs with ceiling `m−1−ε`
  (HP precision available from x); all walks end with records ≤ 26.
Results:
- `5≤m<2·10^7`: 39,999,990 certificates, **0 failures**.
- `5≤m<10^8`: 199,999,990 certificates, **0 failures**
  (counts: even 75,678,090; a_term 55,000,150; a_sc 2,787,922; a_tie5 2,787,922;
  bc 63,745,788; small 118; max bc record 26; min bc precision 62).
Validation: the literal slow certificate for all m≤2500 (4,992 cases) passes; j1/d1 formulas
and the tie5 truncated resolution agree with the slow results; 87 random bigger slow
certificates (a/even) pass; 800 resolved-class certificates agree with `deep_lib.certify`.
Caveat: A6 is a finite statement; nothing here extends it to m≥10^8.

## 7. Final implication — bookkeeping and missing cases

For `Λ≤13` and an a/b landing:
- `T≤12`, δ∈[−12,15], `j_u<2·10^7`, `j_u≥5`; A4 + [B] gives R2 except (5,5),(5,−11);
- for those, A5 gives `m≤j_T−3/4`, the class mod `2^{m+1}`, and `R_{u+1}≤R_T−1≤J−1`
  (T=0 also covered: `R_{u+1}≤J−1`); HP at precision `m+1` needs exactly
  `j_T−2≥m+1` (a) / `j_T−3≥m+1` (b), which A5's bounds give; x-side precision
  `v2(x_{u+1}−2^m)≥m+1` holds because the base is odd.
- **Missing: `m<2·10^7`.** A6 applies only there. Derivation: T can be 1 with
  `j_T=j_1≤L(J)`; for `J<T_13`, `L(J)≈log2 J` is a tower far above 2·10^7. The bare-tie
  congruences do not bound m: `gap_m.py` shows `k≡−10/9 (mod 2^{2e7+1})`, `k≡6 (mod 32)`
  is solvable, giving the a-(5,5) landing with `m≥2e7+1`. Then `u+1` is deep again, and the
  re-entered drift window is shifted (`θ_{u+1}=−2` or 14; after l deep steps `|θ|≤2+3l`,
  so a later a/b landing has δ down to `1−3l ∉ [−12,15]` for l≥5). Neither A6 nor A4 covers
  this. This is the central gap.
- Scope: c-landings are not covered by A4–A6 at all (R1 allows a c-step that lands);
  R2 for c remains open as in work_deep. `j_u≤4` and even `X(n_T)` are harmless but unstated.
- The logical structure "A2 uses A1 and A3, A3 uses A2" is resolved by the minimal
  first-resonance argument; there is no circularity, only the range error in §3.

## 8. Data checks [B]

`check_data.py` on `table_20000000.pkl` and `table_100000000.pkl`:
- all odd crossings (12,432,185 / 62,160,928): `τ≥(n−1)/2` and CLOCK `τ≤nP(n)`; 0 violations.
- τ is even at every odd type-a and type-b crossing of the 10^8 table (30,288,015 each, 0 odd);
  so `k=τ/2` is an integer and `3k ≥ 15,000,000` at the deep boundary.
- odd type-c: `λ_Y≤3τ+1`; odd type-b: `c′=3·2^{n−1}`, `λ′=3τ+4`; `ω<n−ε`; 0 violations.
- deep range `[N0,1e8)`: 24,230,413 odd-a crossings; min `3k=26,764,062` at
  `n=19,999,999` (τ=17,842,708); max bitlen(3k)=27; min `j−2−bitlen(3k)=19,999,973`.
- `B+κ(j)<2^{j−3}`: bit-length margin 9,999,996 at j=N0; all sample j up to 10^{12} pass.
- Full β-walk for all J<2·10^7: no tie, `r_1<J`, records non-increasing, at most 3 chains.
- Full pair map vs cached table/fdata on n<4096: 0 mismatches (typ/tau/eps/odd/lY/lA,
  c′/λ′ at odd b/c).

## 9. Reproduce (Windows, `python -B`, files in this directory)

```
python -B check_table.py 4096          # own pair map vs cached table + full-table identities, 5 s
python -B check_cert.py                # library cross-checks vs shiftlib/deep_lib, 1 s
python -B check_cprime.py              # c'=3*2^(n-1), lambda'=3tau+4, X(4) data, <1 s
python -B check_A5.py                  # gateway algebra on real crossings + symbolic, <1 s
python -B check_A6_logic.py            # slow-cert validation m<=2500, d1 formulas, tie5, 3 s
python -B scan_A6.py 20000000          # A6 full scan 5<=m<2e7, 34 s
python -B scan_A6.py 100000000         # A6 full scan 5<=m<1e8, 135 s (2.8 GB table)
python -B check_window.py              # sampled window scan + targeted ND, 3 s
python -B full_window.py 20000000      # full window scan 5<=j<2e7, 331 s
python -B check_data.py "D:\math_cc_astra\deep1\table_20000000.pkl"      # 10 s
python -B check_data.py "D:\math_cc_astra\deep1\table_100000000.pkl"     # 160 s
python -B check_beta.py                # beta-walk all J<2e7 + drift data, 20 s
python -B check_logic.py               # inequalities/range bookkeeping, 1 s
python -B check_resolved_certs.py      # resolved classes vs deep_lib, 0.4 s
python -B gap_m.py                     # m>=2e7 congruence non-vacuity, <1 s
```

JSON outputs beside each script: `check_table.json`, `check_cert.json`, `check_cprime.json`,
`check_A5.json`, `check_A6_logic.json`, `scan_A6_20000000.json`,
`scan_A6_100000000.json`, `check_window.json`, `full_window.json`,
`check_data_table_100000000.json`, `check_data_table_20000000.json`, `check_beta.json`,
`check_logic.json`, `check_resolved_certs.json`, `gap_m.json`.

## 10. Tags / scope

Tags: [A] all parameters (hypotheses stated), [B] finite exact computation (range stated),
[C] conjecture/data. This note proves no new global theorem; it does not prove EXT, DEEP,
R1 or R2, does not change K_clock, and does not assert non-halting of #1. The cached tables
are accepted corpus data; my independence is in the walk/certificate logic and the pair-map
validation on the prefix, not in rebuilding the 10^8 crossing table.
