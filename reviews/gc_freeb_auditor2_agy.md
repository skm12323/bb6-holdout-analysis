# 盲审复算报告：work_gc_freeb（FREE-B 边界 gate 局域化）

**审计员**：审计员 2（agy gemini-3.8-flash-high）  
**审查日期**：2026-11-10  
**审查对象**：`work_gc_freeb/NOTES.md` 及相关已接受背景文件  
**盲审规则合规声明**：
本审计员严格遵守盲审独立性原则：
1. **源码隔离**：未阅读 `work_gc_freeb/verify_freeb.py` 与 `work_gc_freeb/fb.py` 的任何源码。
2. **独立重推导**：所有数学引理（FB-0、FB-1、FB-2、FB-3、FB-4、Theorem FREE-B、Prop FB-5）均由手算和 2-adic 形式推导完全独立完成。
3. **独立验证脚本**：所有数值复算和符号遍历引擎均由本审计员自行编写，仅存放在 `work_gc_freeb/agy_scratch/` 目录下，并在 `D:/math_cc` 下使用 Python 3.12 独立执行。

---

## 审查结论总评

`work_gc_freeb/NOTES.md` 对 `work_claude_cycle` 遗留的 FREE-B 边界 gate 局域化缺口给出了完整、严谨且极为精准的处理。
- **数学定理 [A]**：FB-0、FB-1、FB-2、FB-3、FB-4、Theorem FREE-B、Prop FB-5 的推导全部正确，边界与相消判定、刀口奇偶对偶性、大小界以及 CL2 阈值不等式完全成立，逻辑自洽无缺口。
- **计算数据 [B]**：反例 A、B、B2 重放无误；自写全量遍历完全重现普查 357,821 对、1,474 个 determined gates、0 个边界实例以及 623 个首着陆逃逸（467 END + 156 SPLIT）；seeded 新实例与 razor 刀口实例在自建引擎下表现精确吻合。
- **范围与越级检查**：未做任何越级断言，明确声明不闭合 FREE-EXIT、G1、CL2 或 CL4，不涉及任何 EXT 新范围或非停机断言。

---

## 逐项复核详细报告

### 1. FB-0 / FB-1 重推导（后置柱体与三分分解）

#### 1.1 FB-0（后置 gate 状态分布）
在奇-a 链 $j$ 处发生 true NT gate 时，由 Lemma NT，$v_2(\Theta_{\mathrm{in}} + 3k_j) = j - 2$。故 $\Theta_{\mathrm{in}} + 3k_j = 2^{j-2} \cdot o$，其中 $o = 1 + 2X$ 为 2-adic 奇数，$X \in \mathbb{Z}_2$。
a-步状态更新：
$$\Theta_{\mathrm{after}} = \Theta_{\mathrm{in}} + 3 + 6k_j = 2^{j-2}(1 + 2X) + 3(k_j + 1) = 2^{j-2} + 3(k_j + 1) + 2^{j-1}X = c_\Theta + 2^{j-1}X$$
标量映射输出 $y$（输入 $x_{\mathrm{in}} = 2^j(1 + 2V_{\mathrm{prev}})$）：
$$y = 2\Theta_{\mathrm{in}} + 6k_j - \frac{x_{\mathrm{in}}}{2} = 2^{j-1}(1 + 2X) - 2^{j-1}(1 + 2V_{\mathrm{prev}}) = 2^j(X - V_{\mathrm{prev}})$$
条件化 $v_2(y) = m \ge j$ 等价于 $X - V_{\mathrm{prev}} = 2^{m-j} u'$（$u' \in 1 + 2\mathbb{Z}_2$ 为奇数）。令 $u' = 1 + 2V$（$V \in \mathbb{Z}_2$），则 $x_{\mathrm{after}} = 2^m(1 + 2V)$。由于映射 $(X, V_{\mathrm{prev}}) \mapsto (X, V)$ 在 $\mathbb{Z}_2^2$ 上是单模双射，故 $(X, V)$ 独立且满取 $\mathbb{Z}_2^2$。FB-0 成立。

#### 1.2 FB-1（三分分解递推与赋值）
设从 $G$ 输出后的路径累计损失为 $\ell$。写状态为 $x = C + AX + BV$ 与 $\Theta = \theta + 2^{j-1}X$。
初始状态（$\ell = 0$）：$C_0 = 2^m$，$A_0 = 0$，$B_0 = 2^{m+1}$，$\theta_0 = c_\Theta$。
步进规则递推：
- **a-步**（损失 1）：
  $$\Theta' = \Theta + 3 + 6k_q \implies \theta' = \theta + 3 + 6k_q, \quad X\text{ 系数保持 } 2^{j-1}$$
  $$x' = 2\Theta + 6k_q - \frac{x}{2} = \left[2\theta + 6k_q - \frac{C}{2}\right] + \left[2 \cdot 2^{j-1} - \frac{A}{2}\right]X + \left[-\frac{B}{2}\right]V$$
  即 $C' = 2\theta + 6k_q - \frac{C}{2}$，$A' = 2^j - \frac{A}{2}$，$B' = -\frac{B}{2}$。
- **b/c-步**（损失 $1 + \varepsilon_q$，$v_2(R_q) = -1 - \varepsilon_q$）：
  $$\Theta' = \Theta + 3 + 3\tau \implies \theta' = \theta + 3 + 3\tau, \quad X\text{ 系数保持 } 2^{j-1}$$
  $$x' = R_q x + \lambda'_q = \left[R_q C + \lambda'_q\right] + [R_q A]X + [R_q B]V$$
  即 $C' = R_q C + \lambda'_q$，$A' = R_q A$，$B' = R_q B$。

赋值追踪：
1. **$B$ 的赋值**：每步 $v_2(B)$ 严格减少该步损失（a-步减 1，b/c-步减 $1+\varepsilon$）。从 $v_2(B_0) = m+1$ 开始，在累计损失 $\ell$ 后：
   $$v_2(B) = m + 1 - \ell$$
2. **$A$ 的赋值**：
   - 在首次 a-步之前，经历 $L_{\mathrm{bc}}$ 损失的连续 b/c-步（若首步为 a 则 $L_{\mathrm{bc}} = 0$），期间 $A' = R_q A = 0$，故 $A = 0$。
   - 在首个 a-步处，$A' = 2^j - \frac{A}{2} = 2^j - 0 = 2^j$，精确达到 $v_2(A) = j$。此时累计损失为 $L_{\mathrm{bc}} + 1$。
   - 首个 a-步之后，后续 a-步有 $v_2(A) \le j$，因而在 $2^j - A/2$ 中，$v_2(2^j) = j > v_2(A/2) = v_2(A) - 1$，由超度量不等式严格取等号：$v_2(A') = v_2(A) - 1$；后续 b/c-步使得 $v_2(A') = v_2(A) - (1 + \varepsilon)$。因此后续每步精确减少该步损失。
   - 故在路径末尾总损失 $\ell$ 处：
     $$v_2(A) = j - (\ell - (L_{\mathrm{bc}} + 1)) = j - \ell + L_{\mathrm{bc}} + 1$$
3. **$C = u + \beta \cdot 2^m$**：
   $\beta$ 满足与 $B / 2^{m+1}$ 完全相同的线性递推（初始 $\beta_0 = 1$），故 $v_2(\beta) = -\ell$，即 $v_2(\beta \cdot 2^m) = m - \ell$。FB-1 证毕。

---

### 2. FB-2 重推导（可判定性判据）

设当前步输入形式为 $x = C + AX + BV$，$(X, V) \in \mathbb{Z}_2^2$。设 $s := \min(\{v_2(A) : A \ne 0\} \cup \{v_2(B) : B \ne 0\})$。
- **充分性（$v_2(C) < s$）**：
  设 $t = v_2(C) < s$。提取 $2^t$：
  $$x = 2^t \left( \frac{C}{2^t} + \frac{A}{2^t}X + \frac{B}{2^t}V \right)$$
  因 $t = v_2(C)$，$C/2^t \in \mathbb{Z}_2^\times$（模 2 为 1）。因 $t < s \le v_2(A), v_2(B)$，系数 $A/2^t \equiv 0 \pmod 2$ 且 $B/2^t \equiv 0 \pmod 2$。
  因此括号内对于**所有** $(X, V) \in \mathbb{Z}_2^2$ 均有：
  $$\frac{C}{2^t} + \frac{A}{2^t}X + \frac{B}{2^t}V \equiv 1 + 0 + 0 \equiv 1 \pmod{2\mathbb{Z}_2}$$
  故对任意 $(X, V)$ 恒有 $v_2(x) = t = v_2(C)$。步输出赋值恒定，完全由日历常数项 $C$ 决定。
- **必要性与分裂显式选择（$v_2(C) \ge s$）**：
  若 $s = v_2(A)$（若 $s = v_2(B)$ 对偶选择 $V$），提取 $2^s$：
  $$\frac{x}{2^s} = \frac{C}{2^s} + aX + bV, \quad a = \frac{A}{2^s} \in \mathbb{Z}_2^\times, \quad \frac{C}{2^s} \in \mathbb{Z}_2$$
  取 $V = 0$：
  - 当 $X = 0$ 时，$\frac{x}{2^s} \equiv \frac{C}{2^s} \pmod 2$；
  - 当 $X = 1$ 时，$\frac{x}{2^s} \equiv \frac{C}{2^s} + 1 \pmod 2$。
  $X \in \{0, 1\}$ 的两相必有一者模 2 为奇数（赋值恰为 $s$），另一者模 2 为偶数（赋值 $\ge s+1$）。因此 $v_2(x)$ 在柱体内部必然分裂。
  若 $C = 0$ 且存在变量，取 $(0, 0)$ 输出 $\infty$，取基向量输出 $s$，同样分裂。

与 `work_claude_cycle/branch.py` 第 65-67 行对照：
```python
vc, vs, var = fval(xn)
if vc < vs:
    jn = vc  # determined, no split
```
规则完全一致，FB-2 证毕。

---

### 3. FB-3 重推导（边界判定与 DR′ 上界）

设 $G'$ 为 $G$ 确定的 gate。由 FB-2，从 $G$ 输出到 $G'$ 输出的每一步均处于 determined 状态。在 $G'$ 输出处：
$$m' = v_2(C_{\mathrm{final}}) < \min(v_2(A_{\mathrm{final}}), v_2(B_{\mathrm{final}})) = \min(j - \ell + L_{\mathrm{bc}} + 1, m + 1 - \ell)$$
因此必有整值不等式：
$$m' \le j - \ell + L_{\mathrm{bc}} \implies \Delta R := m' + 1 + \ell - j \le 1 + L_{\mathrm{bc}}$$
这直接重现了审查更正后的 sharp DR′ 结论。

边界 gate 定义为 determined 且非 record-safe（即 $m' \ge j - \ell$）：
1. **边界等价性**：$m' = v_2(C_{\mathrm{final}}) \ge j - \ell \iff 2^{j-\ell} \mid C_{\mathrm{final}}$。
2. **$\Delta R$ 范围**：$m' \in [j - \ell, j - \ell + L_{\mathrm{bc}}] \iff \Delta R \in \{1, \dots, 1 + L_{\mathrm{bc}}\}$。
3. **$V$-项不阻碍**：由于 $G$ 是 gate，其输出 $m \ge j$，故：
   $$v_2(B_{\mathrm{final}}) = m + 1 - \ell \ge j + 1 - \ell > j - \ell$$
   因此 $v_2(C_{\mathrm{final}}) \ge j - \ell$ 时，$C_{\mathrm{final}}$ 的赋值绝不会被 $B_{\mathrm{final}}$ 的赋值阻挡，能否成为 gate 仅受 $A_{\mathrm{final}}$ 约束。FB-3 证毕。

---

### 4. FB-4 重推导（两步显式闭式与奇偶刀口）

考虑首着陆 $c_1 \le j - 2$ 且在 $c_1$ 处发生 a-步（参数 $k_{c_1}$）。此时 $G'$ 即为该 a-步。
输入状态：$c_\Theta = 2^{j-2} + 3(k_j + 1)$，$C_0 = 2^m$。

#### 4.1 公式独立重推导
- **(a) 首步为 a-步（$L_{\mathrm{bc}} = 0, \ell = 2$）**：
  $$C_1 = 2c_\Theta + 6k_m - 2^{m-1}, \quad \theta_1 = c_\Theta + 3 + 6k_m$$
  $$C_{\mathrm{final}} = 2\theta_1 + 6k_{c_1} - \frac{C_1}{2} = c_\Theta + 9k_m + 6k_{c_1} + 6 + 2^{m-2}$$
  代入 $c_\Theta = 2^{j-2} + 3(k_j + 1)$：
  $$C_{\mathrm{final}} = 2^{j-2} + 2^{m-2} + 3(k_j + 3k_m + 2k_{c_1} + 3) = 3S_a + 2^{j-2} + 2^{m-2}$$
  其中 $S_a = k_j + 3 + 3k_m + 2k_{c_1}$。公式 (a) 精确吻合。
- **(b) 首步为 b-步（$L_{\mathrm{bc}} = 2, \ell = 3$）**：
  $$R_b = \frac{3}{4}, \quad \lambda'_b = 3\tau_m + 4 \implies C_1 = 3 \cdot 2^{m-2} + 3\tau_m + 4, \quad \theta_1 = c_\Theta + 3 + 3\tau_m$$
  $$C_{\mathrm{final}} = 2(c_\Theta + 3 + 3\tau_m) + 6k_{c_1} - \frac{3 \cdot 2^{m-2} + 3\tau_m + 4}{2}$$
  $$2C_{\mathrm{final}} = 2^j - 3 \cdot 2^{m-2} + (12k_j + 12k_{c_1} + 9\tau_m + 20) = 2^j - 3 \cdot 2^{m-2} + U_b$$
  $$C_{\mathrm{final}} = 2^{j-1} - 3 \cdot 2^{m-3} + \frac{U_b}{2}$$
  其中 $U_b = 12k_j + 12k_{c_1} + 9\tau_m + 20$。公式 (b) 精确吻合。
- **(c) 首步为 c-步（$L_{\mathrm{bc}} = 1 + \varepsilon_1, \ell = 2 + \varepsilon_1$）**：
  $$C_1 = R_c \cdot 2^m + \lambda'_c, \quad \theta_1 = c_\Theta + 3 + 3\tau_m$$
  $$C_{\mathrm{final}} = 2(c_\Theta + 3 + 3\tau_m) + 6k_{c_1} - \frac{\lambda'_c}{2} - R_c \cdot 2^{m-1} = 2^{j-1} + 6(k_j + \tau_m + k_{c_1} + 2) - \frac{\lambda'_c}{2} - R_c \cdot 2^{m-1}$$
  $$2C_{\mathrm{final}} = 2^j + U_c - R_c \cdot 2^m, \quad U_c = 12(k_j + \tau_m + k_{c_1} + 2) - \lambda'_c$$
  公式 (c) 精确吻合。

#### 4.2 边界整除与奇偶刀口分析
- 对于 (a)：$v_2(A_{\mathrm{final}}) = j - 1$。边界条件为 $v_2(C_{\mathrm{final}}) \ge j - 2$。
  因 $m \ge j$，$2^{m-2} \equiv 0 \pmod{2^{j-2}}$。故 $2^{j-2} \mid C_{\mathrm{final}} \iff 2^{j-2} \mid S_a$。
  设 $u = S_a / 2^{j-2}$。则：
  $$\frac{C_{\mathrm{final}}}{2^{j-2}} = 3u + 1 + 2^{m-j}$$
  - **当 $m > j$ 时**：$2^{m-j}$ 为偶数，故 $\frac{C_{\mathrm{final}}}{2^{j-2}} \equiv 3u + 1 \pmod 2$。
    - 若 $u$ 为偶数：$3u + 1$ 为奇数 $\implies v_2(C_{\mathrm{final}}) = j - 2 < v_2(A_{\mathrm{final}}) = j - 1$。由 FB-2，步为 determined，且 $m' = j - 2$，$\Delta R = 1$。
    - 若 $u$ 为奇数：$3u + 1$ 为偶数 $\implies v_2(C_{\mathrm{final}}) \ge j - 1 = v_2(A_{\mathrm{final}})$。由 FB-2，步发生分裂（SPLIT）！
  - **当 $m = j$ 时**：$2^{m-j} = 1$，故 $\frac{C_{\mathrm{final}}}{2^{j-2}} \equiv 3u + 2 \equiv 3u \pmod 2$。奇偶性恰好反转：
    - $u$ 奇数 $\implies$ determined 且 $m' = j - 2$；
    - $u$ 偶数 $\implies$ 分裂。
- 对于 (b)：$v_2(A_{\mathrm{final}}) = j$。因 $m \ge j$，$2^j - 3 \cdot 2^{m-2} \equiv 0 \pmod{2^{j-2}}$。故 $v_2(2C_{\mathrm{final}}) \ge j - 2 \iff 2^{j-2} \mid U_b$。
  极端情况 $m' = j - 1$（即 $\Delta R = 3$）需要 $v_2(2C_{\mathrm{final}}) = j$，此时 $3 \cdot 2^{m-2}$ 必须模 $2^j$ 为 0，故必须 $m - 2 \ge j \implies m \ge j + 2$。
- 对于 (c)：$v_2(R_c \cdot 2^m) = m - 1 - \varepsilon_1 \ge j - 1 - \varepsilon_1$，且 $j > j - 1 - \varepsilon_1$。故 $2^{j-1-\varepsilon_1} \mid U_c$。

#### 4.3 大小界推导
利用 CLOCK 界 $k_n \le \tau(n)/2 \le \frac{1}{2} n P(n)$ 及 MASS 界 $\lambda'_c \le 6\tau_m + 5$（$n \le m$ 时 $P(n) \le P(m)$）：
- $|S_a| \le \frac{1}{2}m P(m) + \frac{3}{2}m P(m) + m P(m) + 3 = 3m P(m) + 3$。非零整除给出 $2^{j-2} \le |S_a| \implies j \le 2 + \log_2(3m P(m) + 3)$。
- $|U_b| \le 6m P(m) + 6m P(m) + 9m P(m) + 20 = 21m P(m) + 20$。非零整除给出 $j \le 2 + \log_2(21m P(m) + 20)$。
- $|U_c| \le 6m P(m) + 12m P(m) + 6m P(m) + 6m P(m) + 24 + 5 = 30m P(m) + 29$。非零整除给出 $j \le 1 + \varepsilon_1 + \log_2(30m P(m) + 29)$。
FB-4 推导全部成立。

---

### 5. 独立计算复核（自写脚本与关键输出）

本审计员在 `work_gc_freeb/agy_scratch/` 目录下编写并运行了以下独立验证脚本：

#### 5a. 反例 A 与 B、B2 的重放
- **脚本**：`work_gc_freeb/agy_scratch/test_counterexample_a.py`、`test_counterexample_b.py`、`test_counterexample_b2.py`、`test_walker_exact.py`。
- **反例 A 重放输出**（`j=24, m=6268562`）：
  ```
  j=24: k=9
  m=6268562: kind=a, odd=True, tau=5592396, km=2796198
  c_Th = 4194334
  v2(2*c_Th + 6*km) = 5 -> c1=5 (kind=a, kc1=1)
  Sa = 8388608, v2(Sa) = 23
  u = Sa / 2^22 = 2 (even)
  3*Sa + 2^22 = 29360128, v2 = 22
  Exact Fraction Walker:
    Status: GATE, Steps: [(6268562, 'a', 5, 1), (5, 'a', 22, 2)]
    m': 22, dR: 1, is_boundary: True, ell: 2, L_bc: 0
    v2(C_final): 22, v2(A): 23, v2(B): 6268561
  ```
- **反例 B 重放输出**（`j=42, m=1095510131453`）：
  ```
  j=42: k=17
  m=1095510131453: kind=b, tau=977343669108, omega=5 -> c1=5 (kc1=1)
  Ub = 8796093022208, v2(Ub) = 43
  j - 2 = 40, Is 2^(j-2) | Ub? True
  v2(2^j + Ub) = 42 -> m' = 41, dR = 3 = 1 + L_bc (sharp!)
  ```
- **反例 B2 重放输出**（`j=78, m=526980180956824005813092`）：
  ```
  j=78: k=33, m=526980180956824005813092: kind=b, omega=5
  Ub = 4231240368651202111471616, v2(Ub) = 79 >= 76
  v2(2^j + Ub) = 78 -> m' = 77, dR = 3
  ```
结论：反例 A、B、B2 的所有链、步类型、中间日历值、整除性及 sharp DR′ 边界完全重现。

#### 5b. 抽样验证 FB-1 / FB-2 / FB-3
- **脚本**：`work_gc_freeb/agy_scratch/sample_census.py`（对 $j < 40$ 奇 a、$m \in [j, j+200)$ 抽样 1,240 个奇数对）。
- **关键输出**：
  ```
  Odd-a chains j < 40: [5, 8, 12, 14, 17, 22, 24, 27, 32, 35]
  FB1_B_checks: 1328 (100% pass)
  FB1_A_checks: 672 (100% pass)
  FB1_A_zero_checks: 656 (100% pass)
  FB2_det_steps: 1321 (100% pass)
  GATE_found: 2
  FB3_DRp_checks: 2 (100% pass)
  FB3_boundary_iff_div_checks: 2 (100% pass)
  Total boundary gates: 0
  ```
结论：FB-1 的 $v_2(A), v_2(B)$ 递推、FB-2 的可判定性及 FB-3 的 $\Delta R \le 1 + L_{\mathrm{bc}}$ 和边界等价性在所有抽样步中全部成立。

#### 5c. Seeded 新实例与 Razor 刀口分裂实例
- **脚本**：`work_gc_freeb/agy_scratch/test_seeded_razor.py`。
- **关键输出**：
  ```
  --- Testing seeded a-instance j=61 ---
    j: 61, m: 2584632671144439708, c1: 5
    Sa: 3458764513820540928, vSa: 60 >= 59 (div=True), u: 6 (even)
    val_Cfinal: 59 < v2(A)=60 -> is_det: True, m_prime: 59, dR: 1

  --- Testing razor instance j=24 ---
    j: 24, m: 15671400, km: 6990502, c1: 5
    Sa: 20971520, vSa: 22 = j-2 exactly (div=True), u: 5 (odd)
    val_Cfinal: 26 >= v2(A)=23 -> is_det: False, m_prime: SPLIT

  --- Testing seeded b-instance j=78 (intermediate dR=2) ---
    j: 78, m: 18820720748458000207560, c1: 5
    Ub: 151115727451828646838272, v2(Ub): 77 >= 76 (div=True)
    v2(2^j + Ub): 77 -> m': 76, dR: 2 (intermediate case)
  ```
结论：$u$ 偶数时 determined（$m' = j - 2, \Delta R = 1$），$u$ 奇数时由于 $v_2(C_{\mathrm{final}}) \ge v_2(A)$ 精确发生分裂，FB-4(a) 刀口论断获得确凿证实；中间态 $\Delta R = 2$ 实例也被独立重现。

#### 5d. 全量普查复核（$j < 400$ 奇 a，$j \le m < 5000$）
- **脚本**：`work_gc_freeb/agy_scratch/full_census.py`、`test_escape_outcomes.py`。
- **关键输出**：
  ```
  Full census completed in 7.5s
  Pairs tested: 357821
  Det END: 356191
  Splits: 156
  Limits: 0
  Gates found: 1474
  Boundary gates found: 0
  DRp checks: 1474 (100% pass)
  Boundary iff div checks: 1474 (100% pass)
  Escape landings (c1 >= j-1): 623
  Escape j set: [5, 8, 12]
  Escape free congruence pass: 623 (100% pass)
  Escape outcomes: Counter({'END': 467, 'SPLIT': 156})
  ```
结论：
1. 357,821 个奇数起始对中，完全无 LIMIT；
2. 恰有 1,474 个 determined next gates，每一个均满足 $\Delta R \le 1 + L_{\mathrm{bc}}$，且无一为边界实例（$\Delta R \le 0$）；
3. 首着陆逃逸（$c_1 \ge j - 1$）仅出现在 $j \in \{5, 8, 12\}$，共 623 例，FREE 同余全部通过；且其后继结果恰为 467 END 与 156 SPLIT（正是普查中全部的 156 次 split，无一到达 gate）。与 NOTES §6 完全一致。

---

### 6. CL2 归结核对（Prop FB-5 阈值不等式链）

- **脚本**：`work_gc_freeb/agy_scratch/test_cl2_bounds.py`。
- **定义**：
  $$P(g) = 2\lceil\log_2(6g^2 + 5)\rceil^2 + 1345$$
  $$B^*(g) = 2 + \log_2(30g P(g) + 29) + 2\lceil\log_2(3g^2 + 4)\rceil$$
- **不等式链分析**：
  在 $L'$ 环境下，门输出 $\le g$，且 $\varepsilon_1 < 2\lceil\log_2(3g^2 + 4)\rceil \implies \varepsilon_1 \le 2\lceil\log_2(3g^2 + 4)\rceil - 1$。
  1. 分支 (I) 界：$3 + \log_2(6g P(g)) = 2 + \log_2(12g P(g)) < 2 + \log_2(30g P(g) + 29) < B^*(g)$。
  2. 分支 (II-a) 界：$2 + \log_2(3g P(g) + 3) < 2 + \log_2(30g P(g) + 29) < B^*(g)$。
  3. 分支 (II-b) 界：$2 + \log_2(21g P(g) + 20) < 2 + \log_2(30g P(g) + 29) < B^*(g)$。
  4. 分支 (II-c) 界：
     $$1 + \varepsilon_1 + \log_2(30g P(g) + 29) \le 1 + (2\lceil\log_2(3g^2 + 4)\rceil - 1) + \log_2(30g P(g) + 29) = B^*(g) - 2 < B^*(g)$$
- **数值与全域扫描输出**：
  对 $g \in [5, 10000]$ 进行遍历，以及对 $g \in \{10^5, 10^6, 10^8, 10^{12}\}$ 抽样检查：
  ```
  Exhaustive check g in [5, 10000]: 0 failures.
  g=5: B*=33.75, diff_I=15.32, diff_IIb=14.51, diff_IIc=2.00
  g=1000: B*=72.10, diff_I=45.32, diff_IIb=44.51, diff_IIc=2.00
  g=10^12: B*=224.65, diff_I=165.32, diff_IIb=164.51, diff_IIc=2.00
  ```
所有不等式均严格成立（其中 diff_IIc 恒等于 2.00，其余富余量 $> 14$）。因此在 $j > B^*(g)$ 处，分支 (I) 和所有非零和分支 (II) 被彻底排除，仅剩 $(\alpha)$ 分裂后逃逸、$(\beta_0)$ 零和边界、$(\gamma)$ 深族边界。FB-5 的双向等价成立。

---

### 7. 范围核查与同余类分析

1. **与 `freeb_checks.json` 的范围对照**：
   - 普查范围：$j < 400$ 奇 a，$j \le m < 5000$。与 `freeb_checks.json` 中 `"JMAX": 400`, `"MMAX": 5000` 一致。
   - sweep 范围：starts $j < 3000$，深度 3000。与 `"SWJ": 3000`, `"SWB": 3000` 一致。
   - 步上限 400：所有确定的后置行走均在远小于 400 步内结束（零 LIMIT）。
2. **普查“零边界实例”的数论同余解释**：
   - **脚本**：`work_gc_freeb/agy_scratch/test_congruence.py`。
   - 对 $j = 24$，要使两步族 (a) 出现边界 gate，必须 $2^{22} \mid S_a$，即 $3k_m \equiv -(9 + 5) = -14 \pmod{2^{22}}$。
   - 最小正解为 $k_m = 2,796,198$。这要求 $\tau(m-1) = 2k_m \ge 5,592,396$。
   - 但在 $m < 5000$ 范围内，实测 $\max_{m < 5000} \tau(m-1) = 4,456 \ll 5,592,396$。
   - 最小实现该 $k_m$ 的实际 $m$ 正是反例 A 的 $m = 6,268,562$！
   - 对于更大的 $j$（如 $j=42$），模数 $2^{j-2} = 2^{40} \approx 1.1 \times 10^{12}$，更不可能在 $m < 5000$ 内实现。
因此普查范围内零边界实例是数论同余方程的直接必然结果。

---

### 8. 越级检查

对 `work_gc_freeb/NOTES.md` 全文进行了细致检索，确认：
1. **未声称 FREE-EXIT 闭合**：§0.7 及 §7 明确指出 $(\alpha), (\beta_0), (\gamma)$ 三类相消未被排除，其频率先验无界，FREE-EXIT 依然开放；
2. **未声称 G1 闭合**：§7 明确将 G1、CL2、CL4 列为开放问题；
3. **未声称 EXT 新范围**：§0 及 §7 明确声明接受的地平线（$2^{T_4}-2$）保持不变；
4. **未声称非停机**：无任何越级声称。

---

VERDICT: 1
