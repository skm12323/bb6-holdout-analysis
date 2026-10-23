# 方向 R（有理模式）最终结果

日期：2026-10-23。状态：**实现 + 有限精确检验完成；条件定理成立；全局 EXT 未证明，K_clock 未改。**
决定性 gate：`python -B work_landing_symbolic/rational/verify_rational.py`，**exit code 0，修复轮数 0**，
stdout 末尾 `{"status": "PASS", "total_checks": 1337300, "total_fail": 0,
"canonical": 581524, "synthetic": 755776, "elapsed_s": 6.12}`，stderr 为空。
本方向就是本轮期间被接受的 `work_claude_shift`（CHECKPOINT 末尾）所说的 **Part B**
（"rational/uncertified class at a small chain"）。

---

## 1. 精确定理

### 1.1 约定（全部来自已接受文档）

链状态 `(j, x, Theta)`，`x = 2^j u`（u 奇），`n = j-1`，读规范交叉 `X(n)`
（`work_global_ext/PROOF_EXT.md` §2 的走法：`x' = 2Theta+3tau-x/2`（a 型，`tau = 2k`）；
b/c 型 `x' = c'_W u + lambda'_W`，`j' = omega(n) = v2(lambda'_W)`，`Theta' = Theta+3+3tau`；
记录 `R = j + Gamma`，a 步 `Gamma += 1`，b/c 步 `Gamma += 1+eps`）。
缺陷 `D := Theta - x`。**有理证书**：

    Q = 3^r,  gcd(C,Q) = 1,  b in {0,1},   D ≡ C*Q^{-1} + b*2^j  (mod 2^{j+1}).

记 `c := C/Q`、实高度 `ht := |C|/Q`、中心高度 `A := |c - 3/2|`、`h_t := A_t + 3/2`、
秩 `r`（`Q = 3^r`）、`kappa(j) := (3/2)(j-1)P(j-1)`，`P(n) := 2*ceil(log2(6n^2+5))^2 + 1345`
（`PROOF_CLOCK` 的已接受界 `3k <= kappa(j)`；`work_deep/NOTES.md` L122–L141）。
输入相位形式 `theta + s`（`s = a/3^d in Z[1/3]`, `gcd(a,3)=1`, `|s| <= h`）是它的特例：
`Q = 3^d`、`C = theta*3^d + a`、`b = 0`、`ht <= |theta| + h`。

### 1.2 Theorem RAT-0（a 步三分类）[A]

设 a 步读 `X(j-1)`，`k = tau(j-1)/2`，`p := 1 + v2(3Qk + C) = 1 + v2(3k + C/Q)`
（后式为 Z_2 估值；`3Qk+C = 0` 时约定 `p = +inf`，只有 Q=1 可能）。则

* **(A1) 强下降**：`p <= j-2` ⟹ `j' = p`，`C' = 3Q-C`，`Q' = Q`，`b' = 0`，
  且 `D' ≡ (3Q-C)Q^{-1} (mod 2^{j'+1})`。
* **(A2) 一步下降**：`p >= j` ⟹ `j' = j-1`，`D' ≡ 3 - D - 2^{j-1} (mod 2^j)`，`b' = 0`
  （类仍确定；低高度描述改用 catapult：`C' = (9+6k)Q - C - bQ*2^j`，`Q' = 3Q`，`b' = 1`，
  秩 +1；见 1.6）。
* **(A3) NT 门**：`p = j-1` ⟹ `v2(x') >= j`，故 `j' >= j`；`j'` 与输出类**不由类决定**，
  只由底数 u 的高位决定。
* **(A4) 无零**：`Q > 1` 时任何情形 `x' != 0`；`Q = 1` 时 `x' = 0` 可能（虚拟共振）。

**[A] 依据**：脚本 `a_step_*` 计数（canonical 21,952 强 / 544 一步 / 544 NT；synthetic
234,976 强 / 2,176 一步 / 1,888 NT），0 失败；`a_step_*_nozero` 20,480 + 212,480 次，0 失败；
`a_step_nt_u_dependence`：540 个 NT 门类**全部**显示 u 依赖；
`a_step_Q1_resonance_zero`：3 个显式 `x'=0` 实例。

### 1.3 Theorem RAT-1（b/c 步与有理位移）[A]

设 `X(n)`（`j = n+1`）为奇 b/c，`sigma := v2(c'_W) = n-eps`，`omega := v2(lambda'_W) < sigma`（W 的 S1），
`Phi := 3tau+5-lambda'_W`。则精确地

    D' = D + Phi - 2 + (2^j - c'_W)u,    v2(2^j - c'_W) = sigma >= omega+1,
    j' = omega <= j-2-eps,     D' ≡ D + Phi-2   (mod 2^{omega+1}),

故类满足 `C' ≡ C + Q*s (mod 2^{j'+1}Q)`、`b' = 0`，其中 `s` 是 `Phi-2` 模 `2^{j'+1}` 的**所选代表**。
写 `s = a/3^d`（`gcd(a,3)=1`），未约分地 `Q2 = 3^{max(r,d)}`、
`C2 = C*3^{max(0,d-r)} + a*3^{max(0,r-d)}`；3-约分后

    r' <= max(r,d),   且 r' = max(r,d)  <=>  3 !| C2  或  max(r,d) = 0.

**代表的选择**由 O3 代价 `2r + ceil(max(0,1-c,c-2))` 最小化决定（或由来源直接给出）；
低亏损情形 `eps=3 -> s=0`、`eps=5 -> s=∓1`、b 步 `s=-1`、`BBBAA -> s=+4/3`。
注意整数 `Phi-2` 可以很大（规范 c 交叉 n=65：`Phi-2 = -80`，但 `omega=3`，
`-80 ≡ 0 (mod 16)`），所以必须模 `2^{j'+1}` 后取代表。

**[A] 依据**：`bc_omega_v2_lambda`/`bc_sigma_v2_cW`/`bc_S1_omega_lt_sigma` 各 1,273
（规范 n<4000 的全部奇 b/c）；`bc_class_recurrence` 488,832 次；
`bc_synthetic_shift_class` 4,032 次（含 `4/3, -2/3, 2/9, 1/3`）；全部 0 失败。
**实现阶段修正**：原计划写 `r' = max(r,d)` 为等式，被反例 `Q=9,C=55,s=2/9`（`57/9 -> 19/3`，
秩 2->1）与 `Q=9,C=1,s=-1`（`C2=0`，秩 2->0）推翻；现为不等式 + 等号判据
（`bc_synthetic_rank_bound`/`_rank_drop_rule` 与 `rank_rule_bc`/`_rank_rule_bc_dichotomy` 各 4,032/9,120，0 失败）。

### 1.4 Theorem RAT-2（高度、秩、记录）[A]

* **高度**：`A_{t+1} = A_t`（a 步，精确：`|3-c-3/2| = |c-3/2|`）；
  `A_{t+1} <= A_t + |s_t|`（b/c 步）；故 `ht_t <= A_t + 3/2 <= A_0 + sum_{b/c}|s_i| + 3/2`。
  与已接受 `JOINT_HEIGHT_BUDGET` 的接口：`h_pen(c) := max(0,1-c,c-2) = max(0, A - 1/2)`。
* **秩**：A1（反射）`r' = r`；A2/NT 门（catapult）`r' = r+1`（3-约分后 `<= r+1`）；
  b/c 如 1.3；gateway `r' = r+1`（`r>=1`；此时必有 `3 !| C'`），`r=0` 时 `r'=1` 除非
  `C+2b ≡ 0 (mod 3)`（则 `r'=0`）。
* **记录**：`R_{t+1} <= R_t - 1`（强下降、b/c 步）；`R_{t+1} = R_t`（一步下降）；
  `R_{t+1} >= R_t + 1`（NT 门）。**记录只在 NT 门处增加**。

**[A] 依据**：`height_A_preserved_a` 3,058、`height_ht_le_A_plus_3_2` 3,080、
`height_Lipschitz_bc` 9,120、`record_strong_descent` 3,058、`record_one_step_equal` 10、
`record_bc_descent` 9,120、`gateway_height_ladder` 40；0 失败。

### 1.5 Theorem RAT-3（无 NT 门 ⇒ 类证书）[A]

若走法在终止前没有任何 NT 门（A3），则每个链的转移都由类决定（A1/A2/1.3），
且它在 `<= j_0 - 4` 步内终止于偶交叉（每步 `j` 至少降 1；`X(0..3)` 全偶，`[B]` canonical 小基），
全部 `R_t <= j_0`；并且**任何与起点同类（mod `2^{j_0+1}`）的状态走同一参数/类型序列**
（Lemma HP，`PROOF_EXT.md` §2，取 `P = j_0+1`：`min(v2 deltaTheta, v2 delta x) >= j_0+1`）。

充分条件：每个 a 链 `(DEPTH)` `Q_t(kappa(j_t)+h_t) < 2^{j_t-2}`
（因 `|3Qk+C| <= Q(kappa+h)`，故 `v2(3Qk+C) <= j_t-3`，即 `p_t <= j_t-2`）。

**[A] 依据**：`certify_name_swap_same_class` / `_same_result` / `certify_high_lift_same_result`
各 60,264（`(C,b) <-> (C-2^jQ, 1-b)` 与 `delta -> delta+2^{j+1}` 不变）；`certify_propagation_same_word`
40 个已认证类 × 15 个状态（u ∈ {1,3,5,9,33}、lift ∈ {0,1,3}），全部同一词；
以及全部 A/B 类恒等式。0 失败。

### 1.6 Theorem RAT-4（j=5 的 gateway / catapult）[A]

`X(4)` 是奇 a 型、`tau(4) = 2`、`k = 1`（规范小基，`[B]`：`X4_odd_type_a_tau2`）。
故 j=5 的每条链都走 k=1 的 a 步，且 `3D' = 15 - D - x'`（一般 a 步为 `3D' = 9+6k-D-x'`）。
设输入类已知到 `2^H`，`m := v2(x')`。则对 `m < H`：

    D' ≡ (15Q - C - 32bQ)/(3Q) + 2^m   (mod 2^{m+1}),   即
    C' = 15Q - C - 32bQ,   Q' = 3Q,   b' = 1,
    ht' = |C'|/Q' <= 5 + ht/3 + 32b/3,
    r' = r+1 (r>=1),   R' = m + Gamma + 1.

高度迭代：b=0 的不动点 `15/2`；b=1 的不动点 `47/2`；`ht_t <= 47/2 + 3^{-t}(h_0-47/2)`。
`R' <= R` 当且仅当 `m <= 4`（此时走法在下一链终止，j'<=4 即偶交叉）。
`m` 不由类决定（`m >= H` 时同类不同 lift 给出不同 `m`）。

**[A] 依据**：`gateway_class` 33,220、`gateway_height_bound` 33,220、`gateway_rank_rule` 33,220、
`gateway_rank_zero_exception` 1,296、`gateway_height_ladder` 40，0 失败；
`gateway_m_ge_H_is_provenance`：184 个 `m>=H` 的同类不同输出实例（正面确认 `m<H` 条件的必要性）。

### 1.7 Theorem RAT-5（三条不可能性 / 障碍） [A]

* **(O2) 只依赖 h 的链长/记录界不存在**：对每个偶数 `m >= 6`，`u = (2^{m-4}-1)/3`、
  `x = 32u`、`Theta = x+5` 满足 `j=5`、`D=5`（`C=5,Q=1,b=0`，ht=5），
  且 `x' = 48u+16 = 2^m`，`D' ≡ (10-2^m)/3 (mod 2^{m+1})`，记录 `5 -> m+1`。
  故任何"记录 `<= N(h)`"的陈述对任意来源为假。
* **(O1) 高度 <= 5 不足以保证 (DEPTH)**：P=49 源 `x0 = 5*2^49`、`D0=1`、`k=20`、
  `sigma = 1051689726214394`；位移 `eta_r = -5+8/3^r` 给
  `(C,Q,b) = (-4*3^r+8, 3^r, 0)`、ht `<= 4`。首个 a 步
  `p_0 = 4 + v2(7*3^r+1)`，`v2(x') = 4 + v2(A*3^r+1)`，`A = 15*2^44+7`。
  危险 `r`（`v2(A3^r+1) >= sigma-5`）强制 `v2(7*3^r+1) = 44`，故 `p_0 = 48 = j-1`：
  **O1 恰好是 A3 的 NT 门**。(DEPTH) 在源处只对 `r <= 18` 成立
  （`3^r*(kappa(49)+4) < 2^47`，`kappa(49) = 125064`）；O1 的 `r >= 663,542,339,794,048`
  （比 O1 自己的 `5(sigma-53)/8 = 657,306,078,883,963.125` 强 0.95%），违反幅度约 `1.04e15` 位。
* **(O3) 按高度/秩枚举类不可能**：`sum_{r<=32}[(2(64-2r)+1)3^r+1] = 8,338,590,849,833,250 < 2^64`；
  在参数 j 处"低代价描述"至多 `(R+1)(2h+1)` 个，而类有 `2^{j+1}` 个
  （j=64,h=5,R=32：363 / 2^65）。

**[A] 依据**：`O2_family_exact` 254（m=6..512）、`O2_record_unbounded`；
`O1_*`（源指针、`y=16A+10`、`v2(y)=1`、`x0=5·2^49`、`p0` 结构、`(DEPTH)` 阈值 `r<=18`、
`r_min`）；`O3_count_below_2_64`/`_exact_value`/`_enumeration_hopeless`。0 失败。

### 1.8 Corollary RAT-C（秩 <= 1、h <= 31 的着陆化解）[A | S1] + [B]

设 `h <= 31`，类在每个链有秩 `<=1` 的低高度描述（`Q in {1,3}`, `|C|/Q <= 31`），
所有 b/c 位移的 3-adic 分母指数 `<=1`，且每个 a 链满足 (DEPTH)
（在 `Q=3` 时只需 `h_t <= 841`；`Q=1` 时 `h_t <= 88222`；阈值来自
`2^17/3 - kappa(19) = 841.67`、`2^17 - kappa(19) = 88223`，`kappa(19) = 42849`）。
则所有 `j>=19` 的步都是强下降（A1）或 b/c 步，记录严格下降；到达 `j<=18` 后由已接受
**全残基 [B]** 证书认证，除非残基落在 24 个例外（见 1.9）。故除这些例外外全部记录 `<= j_0`、
走法终止。秩 0 的类只需 `j>=18`（`2^16/(kappa(18)+31) = 1.618 > 1`）。

**[B] 依据（实测，m ∈ [19,1000]）**：`(10-2^m)/3`：968 次偶交叉终止 + 14 次 j=5 gateway；
`(26-2^m)/3`：969 + 13；`BBBAA C/3`（`C ∈ {-2,1,4,7,10,13,16}`，ht `<= 16/3`）：981 + 1。
三族共 2,946 条 walk：**0 次 NT 门、0 次记录上升、(DEPTH) 在 `j>=19` 上 0 次失败**；
步数 `<= 2`（首步把 j 从 m 降到 `O(log m)`）；`max A_t <= 95/6`。
`RAT_C_family_walk_ok`/`RAT_C_depth_implies_no_nt`/`RAT_C_depth_at_j19plus` 各 2,946，0 失败。

### 1.9 [B] / [C] 清单

**[B]（有限精确计算，范围写明）**
* 小 j 全残基证书：`5 <= j <= 18` 的**全部** `2^{j+1}` 个残基逐类跑精确 walk（约 1.05M 次；耗时随机器/负载而异，2.7–5.7 s）。
  例外数分别为 `4,4,4,4,8`（j=5,8,12,14,17），对称残基为
  `{5,21,-27,-11}` / `{58,186,-198,-70}` / `{1012,3060,-3084,-1036}` /
  `{4081,12273,-12303,-4111}` / `{32702,32750,98238,98286,-98370,-98322,-32834,-32786}`。
  前三个与 `work_claude_shifted/NOTES.md` §4 列出的逐项一致（`{5,21,-11,-27}`、`{58,186,-70,-198}`、
  `{1012,3060,-1036,-3084}`）；j=14,17 的计数（4,8）一致。
* O1 的 `r_min` 由 60 位十进制对数判定（小数部分 0.7665，远离整数边界），非精确整数运算。
* RAT-C 三族的 `m <= 1000` 实测（1.8）。
* 规范的 b/c 数据（`n < 4000` 的 1,273 个奇 b/c）与 canonical 小基。

**[C]（猜想/数据，未证）**
* RAT-C 对**所有** m 成立（本轮只测到 1000；`m <= 1e8` 的 `(10-2^m)/3`、`(26-2^m)/3` 有已接受 [B]，
  但那是逐族扫描，不是定理）。
* 1.10 的 S1–S4 对**所有**来源成立。
* gateway 在 `m >= 1e8` 处的统一处理（RES）。
* `j >= 2e7` 的任何陈述。

### 1.10 需要的附加条件（全部是来源/相位条件，可检验）

* **(S1) 深度—秩关系**（(DEPTH)，对每个 a 链）：
  `Q_t*(kappa(j_t)+h_t) < 2^{j_t-2}`
  `<=> log2 Q_t + log2(kappa(j_t)+h_t) < j_t - 2`
  `<=> r_t <= floor((j_t-2-log2(kappa(j_t)+h_t))/log2 3)`。
  可检验（沿 walk 逐步算）；[A] 充分。**性质：这是秩上界**，不是 CAL-C/R1/H3 型参数上界。
* **(S2) NT 门的同余回避**（S1 的等价替代，纯同余）：
  对每个 a 链，`3Q_t k_t + C_t not≡ 2^{j_t-2} (mod 2^{j_t-1})`，
  等价地 `k_t not≡ 3^{-1}(2^{j_t-2} - C_t/Q_t) (mod 2^{j_t-1})`，
  日历形式 `tau(j_t-1) not≡ (3Q_t)^{-1}(2^{j_t-1}-2C_t) (mod 2^{j_t})`。
  [A] 与"无 NT 门"等价。这是同余，不是界。
* **(S3) gateway 的 provenance**：在每个 j=5 链上，若 `m >= 5`，则必须
  `m + 1 <= sigma_t`（`sigma_t` 为该 gateway 前的系数精度），等价于
  `v2(beta') < J - Gamma - 1`（`STOP_CHECKPOINT_2026_10_21.md` 的 affine 形式：
  `x = A*U + beta`、`Theta = 2^J U + 3d + 1`、`v2(A) = J - Gamma`）；
  或输出族 `{(15Q-C-32bQ)/(3Q) + 2^m}` 已被证书覆盖。
  对**规范裸 tie 入口**，已接受 `work_claude_shift` Lemma CB 给 `m < G(y)+1`
  （`y >= N0`，`G` 为该文的位长界），故跳幅 `O(log y)`。
* **(S4) 着陆类的类证书**：着陆残基 `delta' = C'Q'^{-1} + b'2^{j'} mod 2^{j'+1}` 必须落在
  已认证集合内：`5 <= j' < 2e7` 且 `delta' in [-12,15]`（除 `(5,5),(5,-11)`），
  或 `5 <= j' <= 18` 且不在 1.9 的 24 个例外，或者对该类单独跑精确 walk。
* **(S5) 秩预算**（S1 的另一种写法）：每个链的类有描述使
  `r_t <= (j_t-2-log2(kappa(j_t)+h_t))/log2 3`。

这五条里，S1/S5 是上界型（必须按关系陈述，不能当全局 cap）；S2 是纯同余；S3/S4 是
provenance/类条件。**没有一条是"某个 crossing 参数 < N"的形式**。

---

## 2. 证明骨架（关键恒等式给行内公式）

**(a)** 由 `Theta = x + D`、`x' = 2Theta + 6k - x/2` 得
`x' = 3*2^{j-1}u + 2D + 6k`，`D' = 3 - D - x/2`；于是 `3D' = 9 + 6k - D - x'`。
代入 `D ≡ C Q^{-1} + b 2^j (mod 2^{j+1})`：`2D ≡ 2CQ^{-1} + b2^{j+1} + 2^{j+2}m`，故
`Q*y = 2(C+3kQ) + 3*2^{j-1}uQ`（`y := x' - b2^{j+1} - 2^{j+2}m`）。第一项 valuation `p`，
第二项 `j-1`；`p <= j-2` 给 `v2(x') = p`，且 `D' ≡ 3 - CQ^{-1} = (3Q-C)Q^{-1} (mod 2^{p+1})`
（`b2^j`、`2^{j+1}m`、`2^{j-1}u` 在模 `2^{j'+1}` 下全消失，因 `j-1 >= j'+1`）。
`p >= j` 给 `2^{j-1} | (3k + CQ^{-1})`，于是 `x' = 2^{j-1}(3u + 2z)`，`3u+2z` 奇，`j'=j-1`；
且 `D' = 3-D-2^{j-1}u ≡ 3-D-2^{j-1} (mod 2^j)`。`p = j-1` 给 `x' = 2^{j-1}(3u+w)`（`w` 奇），
`3u+w` 恒偶，故 `j' >= j`，再往下的位由 `u mod 4` 与 `w mod 4` 决定。
`x'=0` ⟹ `Qy = 0` ⟹ `2C = -3Q(2k+2^{j-1}u)` ⟹ `Q | C`，与 `gcd(C,Q)=1, Q>1` 矛盾。

**(b)** b/c：`x' = c'_W u + lambda'_W`、`Theta' = Theta + 3 + 3tau`，故
`D' = D + 3 + 3tau - lambda'_W + (2^j - c'_W)u = D + Phi - 2 + (2^j-c'_W)u`；
`v2(2^j - c'_W) = sigma`（因 `v2(c'_W) = sigma < j`），S1 给 `sigma >= omega+1`，
故模 `2^{omega+1}` 只剩 `D + Phi - 2`。

**(c)** gateway：`3D' = 15 - D - x'`（j=5,k=1）；`x' = 2^m u'`，`u'` 奇，`u'/3 ≡ 1 (mod 2)`，
故 `D' ≡ (15-D)/3 + 2^m (mod 2^{m+1})`；代入 `D ≡ CQ^{-1}+32b (mod 2^H)`，
得 `C' = 15Q-C-32bQ`、`Q'=3Q`、`b'=1`，误差 `2^H Q k/3` 在 `m+1 <= H` 时消失。
一般 a 步同理给 `C' = (9+6k)Q-C-bQ2^j`。

**(d)** 高度：`A' = |3-c-3/2| = |c-3/2| = A`（a）；`A' = |c+s-3/2| <= A + |s|`（b/c）。

**(e)** 记录：`R' - R = (j'-j) + (Gamma'-Gamma) = (j'-j)+1`（a）或 `(omega-j)+1+eps`（b/c）。
A1：`<= -1`；A2：`= 0`；A3：`>= +1`；b/c：`<= -1`（因 `omega <= j-2-eps`）。

**(f)** 传播：两个初始数据在精度 `P` 上一致（`min(v2 deltaTheta, v2 delta x) >= P`），
参考走法记录 `< P`、无 `x=0` ⇒ 参数/类型逐链一致（Lemma HP）。取 `P = j_0+1`
（类的一致精度），得 1.5。

**(g)** O1：`x0 = 5*2^49`、`D0 = 1`、`k=20`；`y = 3x0/2+122 = 16A+10`，`A = 15*2^44+7`；
位移 `eta_r = -5+8/3^r` 给 `D = -4+8/3^r`，故 `C = -4*3^r+8`、`Q = 3^r`；
`3Qx' = 3^r(3x0/2+112+16/3^r) = 16(A3^r+1)`，故 `v2(x') = 4+v2(A3^r+1)`；
`3Qk+C = 56*3^r+8 = 8(7*3^r+1)`，故 `p_0 = 4+v2(7*3^r+1)`。
`A3^r+1 = (7*3^r+1) + 2^44*15*3^r`；若 `v2(A3^r+1) > 44` 则必须 `v2(7*3^r+1) = 44`
（否则 `v2 = v2(7·3^r+1) <= 44`），于是 `p_0 = 48 = j-1`。

**(h)** O2：`u = (2^{m-4}-1)/3` ⟹ `3u+1 = 2^{m-4}`，`x' = 48u+16 = 16(3u+1) = 2^m`；
`3D' = 10 - x'` ⟹ `D' ≡ (10-2^m)/3 (mod 2^{m+1})`。

---

## 3. 与目标形式的差距

**目标**：输入相位 `theta + s`（`s in Z[1/3]`，高度 `<= h`）；着陆类可认证，或经有限步 gateway
化解且**每步记录严格下降**；**界不依赖 J**。

**(3.1) 输入形式**：`theta+s` 是证书的特例（`Q=3^d`、`C=theta*3^d+a`、`b=0`、`ht<=|theta|+h`），
所以 1.2–1.6 直接覆盖该输入。**无差距**。

**(3.2) "认证或有限步 gateway + 严格记录下降"**：
* 无 NT 门时：认证成立（1.5），每步记录**严格下降**（1.4），gateway 不出现。**达标**。
* 出现 NT 门时：若在 j=5，就是 gateway（1.6），它的记录是 `R' = m + Gamma + 1`，
  **只在 `m <= 4` 时严格下降**；`m >= 5` 时记录上升 `m-4`（O2 族证明这对任意 `m` 都能发生）。
  所以"gateway 每步记录严格下降"**不能无条件成立**；只有 S3 成立时成立。
  这就是与目标形式的**实质差距**。
* 若 NT 门在 `j >= 6`：它需要 `p = j-1`，即 `2^{j-1} | (3Qk+C)`；结局由 u 决定，
  S1/S2 是排除它的条件。本轮数据里（2,946 条 walk）从未在 `j>=6` 出现 NT 门。

**(3.3) 对 J 的依赖（逐项）**：

| 项 | 是否依赖 J | 说明 |
|---|---|---|
| A1/A2/A3/B 的类转移公式 | **无** | 纯代数；阈值只依赖 `j_t, k_t, Q_t, C_t`。 |
| `p_t`、`(DEPTH)` 阈值 | **无 J**，依赖当前 `j_t` | `Q(kappa(j_t)+h_t) < 2^{j_t-2}`。 |
| 高度 `A_t/ht_t` | **无** | `h_0 + sum|s| + 3/2`；gateway 后 `<= 47/2`。 |
| 秩 `r_t` | **无**（递推） | 初值来自来源。 |
| 单步记录增量 | **无** | `-1 / 0 / >=+1`。 |
| **链数** | **依赖 J** | `<= min(j_0-4, R_0)`，`R_0 = j_0 + Gamma_0 <= J`。这是唯一的 J 依赖。 |
| **gateway 的记录** | **依赖精度（<=J 的量）** | `R' = m + Gamma + 1`，`m` 由 provenance 决定；`m+1 <= sigma_t <= J` 是 S3。 |
| `N0 = 2e7` | **不出现**（本方向定理内） | 只作为已接受 [B] 窗口证书的**范围**（`5 <= j < 2e7`）出现；定理自己的阈值是 `j >= 18/19`（h<=31、秩<=1），与 N0 无关。 |
| `B = 2^{10^7}` | **不出现** | 被 `h` 替代（相对 RATIONAL_MODE/ODD_DENOMINATOR 的实质改进）。 |
| `T_h` | **不出现** | 未使用。 |
| `log* J`（`Lambda`） | **不出现** | 未使用。只有在把 drift 预算从已接受 deep 段（`drift <= 6Lambda+4`）搬运时才会出现；本方向的 (DEPTH) 是沿 walk 逐步检查，不用 log*。 |
| `2*10^7` | 同上（仅 [B] 范围） | |

所以：**除"链数上界"和"gateway 的记录"两项外，所有量都不依赖 J**；这两项里，
链数的 J 依赖是 `R_0 <= J`，gateway 的 J 依赖通过精度 `sigma_t`（S3）进入。
**不存在只依赖 h 的链长/记录界**（O2，[A]）。

---

## 4. 需要的附加条件

若做不到无条件（本轮确实做不到），所需条件就是 1.10 的 S1–S5。写成可检验的数学陈述：

* **(S1)** 对每个 a 链 t（`j_t >= 5`）：
  `Q_t * (kappa(j_t) + h_t) < 2^{j_t - 2}`，其中 `h_t = |C_t/Q_t - 3/2| + 3/2`。
  （等价 `r_t <= (j_t-2-log2(kappa(j_t)+h_t))/log2 3`；上界型，**必须按关系陈述**。）
* **(S2)** 对每个 a 链 t：
  `3 Q_t k_t + C_t not≡ 2^{j_t-2} (mod 2^{j_t-1})`
  `<=> tau(j_t-1) not≡ (3Q_t)^{-1}(2^{j_t-1} - 2C_t) (mod 2^{j_t})`。
  （纯同余；与无 NT 门等价。）
* **(S3)** 对每个 j=5 链：若 `m := v2(x') >= 5`，则
  `m + 1 <= sigma_t`（等价 `v2(beta') < J - Gamma - 1`），其中 `sigma_t` 是 gateway 前的
  系数精度；或 `(15Q-C-32bQ)/(3Q) + 2^m` 已在认证集合内。
  （来源/provenance 条件；规范裸 tie 入口由 Lemma CB 的 `m < G(y)+1` 给出。）
* **(S4)** 每个着陆残基 `delta'` 落在已认证集合（1.9 的窗口/全残基，除去 24 例外），
  或对该类单独跑精确 walk（类层面可判定）。
* **(S5)** 每个链的类有描述使秩 `r_t` 满足 S1。

**必要性**：S1 的否定就是 O1 的源（bounded height、巨大 rank、首个 a 步即 NT 门，
记录达到 `sigma`）；S3 的否定就是 O2 的族（bounded height、记录 `5 -> m+1`）。
所以这些条件不是装饰：它们是**必要**的（O1 否定 S1 的必要性、O2 否定"无 S3 的记录安全"）。

---

## 5. 未解决点与下一步

1. **gateway 的 `m >= 1e8`（RES）**：`(10-2^m)/3`、`(26-2^m)/3` 的 [B] 只到 `m < 1e8`；
   本轮只在 `m <= 1000` 实测。下一步：对 `m <= 1e8` 用已接受 [B]，`m >= 1e8` 用 Lemma CB 的
   `m < G(y)+1` 与 S3。
2. **24 个小 j 例外**（j=5,8,12,14,17）：需实际精确位或 Lemma CB 逐类化解；本轮没有统一化解。
3. **(DEPTH) 在 `19 <= j < N0` 带内不是自动的**：它依赖 drift 预算；实测三族步数 `<= 2`，
   故成立，但一般来源未证。下一步：把 (NC) 同余检查加进 `rat_walk`，作为 (DEPTH) 的替代。
4. **链长是否被 h 界住**：既未证也未反证（O2 只否定记录界，不否定链长界）。
5. **affine 统一**：S3 的 `beta` 形式来自 STOP_CHECKPOINT；本方向只保留 `(C,Q,b)`，
   没有从 affine 坐标导出 `m` 的界，这是 O2 方向的缺口。
6. **`j >= 2e7`**：任何陈述都没有覆盖；[B] 不得外推。
7. **认证是类层面的事实**（`certify_Q ≡ certify(j,delta)`）：有理描述不产生新证书。
   若需要"有理证书 = 更强认证"，必须引入实际 affine 来源；本轮结论是否定的。
8. 未证明全局 EXT / 机器不停机；K_clock 未改。

---

## 6. 复算

```
python -B work_landing_symbolic/rational/verify_rational.py
```

* 输出（决定性 gate）：exit 0，修复轮数 0，
  `{"status": "PASS", "total_checks": 1337300, "total_fail": 0,
    "canonical": 581524, "synthetic": 755776, "elapsed_s": 6.12}`，stderr 空。
* json：`work_landing_symbolic/rational/checks.json`
  （`status`、`scope`、`canonical_tests`、`synthetic_tests`、`conclusions`（每条结论的计数与
  `[A]/[B]` 标签）、`failures`（空）、`failures_truncated`（空）、`data`、`counts`）。
  说明：`counts.elapsed_seconds` 是 wall-clock，随运行而异（决定性 gate 6.12 s，本地最后一次
  10.22 s）；**检查计数与失败数在所有运行中相同：1,337,300 / 0**。json 由最后一次运行覆盖写入。
* 规范实例：`work_global_calendar/calendar_oracle.Calendar(256)` 与 `Calendar(512)`
  （b/c 交叉用 `c'_W = (head_ratio+2*tail_ratio)*2^n`、`lambda'_W = head_lambda+2*tail_lambda+3`）；
  O1 的 P=49 源用 `work_ext_roots/verify_low_deficit.first_fire(cal512,49)`
  （k=469124961184426，pointer=1051689726214394）。
* 合成状态逐条 `canonical:false`（json 的 `scope` 与测试名 `*_synthetic_*`）。
* 规划/推导：`work_landing_symbolic/rational/PLAN.md`（§13 记录实现阶段发现并修正的陈述）。
