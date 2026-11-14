# 盲审复算报告：work_gc_t4_horizon（Theorem H-T4：EXT(<T4) 视野向机器层的迁移）

**审查员**：Auditor 2（agy, Gemini 3.8 Flash High）  
**日期**：2026-11-10  
**审查对象**：`work_gc_t4_horizon/NOTES.md`，附核对数据 `t4_horizon_checks.json`、`extended_run_900s.log`  
**遵循规则**：严格遵守 `work_gc_t4_horizon/agy_audit_prompt.md` 规则 1–6。未阅读作者脚本源码 `verify_t4_horizon.py`；在 `work_gc_t4_horizon/agy_scratch/` 下编写并运行独立验证脚本，基于已接受材料独立重推导全部结论。

---

## 逐项复核清单与证明

### 1. Lemma HINQ（NOTES §1 末，第 59–66 行）
- **结论**：**成立**（附一处良性展开笔误说明）。
- **推导与复算**：
  - 定义 $L(H) := 3(H-1)^2 + 4 = 3H^2 - 6H + 7$。
  - 单步差分：
    $$L(H+1) - L(H) = (3H^2 + 4) - (3H^2 - 6H + 7) = 6H - 3.$$
    等式 $L(H+1) = L(H) + 6H - 3$ 恒等成立。
  - 单步增长率：$L(H+1) < 2L(H) \iff L(H) + 6H - 3 < 2L(H) \iff 6H - 3 < L(H)$。
    做差可得：
    $$L(H) - (6H - 3) = (3H^2 - 6H + 7) - (6H - 3) = 3H^2 - 12H + 10.$$
    *笔误指出*：NOTES §1 第 62 行写作 $3H^2 - 12H + 14 > 0$（可能因展开 $2L(H) = 6H^2 - 12H + 14$ 时未减去 $L(H+1)$ 中的常数 4，或 $7 - (-7)$ 的符号失误）。真实多项式为 $3H^2 - 12H + 10$。
    核对判别式与取值：$3H^2 - 12H + 10$ 的对称轴为 $H=2$（取值 $-2$），在 $H=1$ 时为 $1>0$，在 $H=3$ 时为 $27-36+10=1>0$。因此**对一切整数 $H \ge 3$，$3H^2 - 12H + 10 > 0$ 恒成立**！
  - 归纳基底：$H = 16$ 时，$L(16) = 3 \times 15^2 + 4 = 679 < 65536 = 2^{16}$ 显然成立。
    因归纳基底 $H = 16 \ge 3$，对一切整数 $H \ge 16$，均有 $L(H+1) < 2L(H) \le 2 \cdot 2^H = 2^{H+1}$。归纳严格成立。
  - 派生不等式：
    对一切 $H \ge 2$，$3(H-1)^2 + 4 - (3(H-2)^2 + 7) = (6H - 3) - 3 = 6H - 6 \ge 6 > 0$。
    故 $3(H-2)^2 + 7 < 3(H-1)^2 + 4 < 2^H$ 对一切 $H \ge 16$ 成立。
    对任意 $v \le H-1$，有 $v-1 \le H-2$，故：
    $$3((v-1)^2+1) + 4 = 3(v-1)^2 + 7 \le 3(H-2)^2 + 7 < 2^H,$$
    且 $3(v-1)^2 + 4 < 2^H \implies (v-1)^2 < (2^H-4)/3$。
  - 独立运行 `work_gc_t4_horizon/agy_scratch/check_hinq.py`，精确整数遍历 $H = 16..4096$，断言全部通过。

---

### 2. Lemma ORD（NOTES §2，第 68–87 行）
- **结论**：**成立**。
- **独立推导（无浮点、纯整数剥层比较）**：
  常数定义：$N_0 = 2 \cdot 10^7 = 20,000,000$，$T_1 = 2^{(N_0-3)/2} = 2^{9999998.5}$，$T_{h+1} = 2^{(T_h-3)/2}$；$K = 2^{2^{499997}-2}$，$K' = 2^{K/2-2} = 2^{2^{2^{499997}-3}-2}$，$K_{clock} = \lfloor 2^{K'} / (64(K')^2) \rfloor$。
  各塔纯整阶界：
  - $T_1$：$2^{9999998} < T_1 < 2^{9999999}$。
  - $T_2$：指数 $(T_1-3)/2$ 落在 $(2^{9999996}, 2^{9999998})$ 内，故 $2^{2^{9999996}} < T_2 < 2^{2^{9999998}}$。
  - $T_3$：同理 $2^{2^{2^{9999994}}} < T_3 < 2^{2^{2^{9999998}}}$。
  - $T_4$：同理 $2^{2^{2^{2^{9999990}}}} < T_4 < 2^{2^{2^{2^{9999998}}}}$。
  - $K$：$2^{2^{499996}} < K < 2^{2^{499997}}$（2 层塔）。
  - $K'$：$2^{2^{2^{499997}-4}} < K' < 2^{2^{2^{499997}-3}}$（3 层塔）。
  - $K_{clock}$：因 $K' > 2^{64}$，$64(K')^2 < 2^{K'/2}$，故 $2^{K'/2} < K_{clock} < 2^{K'}$，即 $K_{clock}$ 为 4 层塔，其指数介于 $2^{2^{2^{499997}-5}}$ 与 $2^{2^{2^{499997}-3}}$ 之间。
  
  八项偏序核对：
  1. $T_1 < K$：指数比较 $9999999 < 2^{24} < 2^{499997}-2$。成立。
  2. $T_2 < K'$：二层指数比较 $9999998 < 2^{24} < 2^{499997}-4$。成立。
  3. **$K' < T_3$ 专项核对**：
     $K'$ 与 $T_3$ 均为三层 2-塔。
     - $K'$ 的三层形式：$2^{2^{2^{499997}-3}-2}$，剥去两层 2 后，顶层指数是 $499997$（而非有人误读的 $2^{499997}-3$）。
     - $T_3$ 的三层形式：$2^{2^{2^{9999997.5}-2.5}-1.5}$，剥去两层 2 后，顶层指数是 $9999997.5 > 9999994$。
     - 比较顶层整常数：$499997 < 9999994$。因此 $K' < T_3$ 确定成立，方向无可动摇。
  4. $T_3 < K_{clock}$：$T_3$ 是三层塔（$< 2^{2^{2^{9999998}}}$），而 $K_{clock}$ 是四层塔（$> 2^{2^{2^{2^{499997}-5}}}}$）。四层塔大于三层塔，显然成立。
  5. **$K_{clock} < T_4$ 专项核对**：
     两者同为四层 2-塔。
     - $K_{clock}$ 的四层上界顶层指数为 $499997-3 = 499994$。
     - $T_4$ 的四层下界顶层指数为 $9999990$。
     - 比较顶层常数：$499994 < 9999990$。因此 $K_{clock} < T_4$ 确定成立。
  6. $K' \le K_{clock}$：由 $K' < T_3 < K_{clock}$ 严格成立。
  7. $T_4 > 2^{64}$：四层塔显然大于 $2^{64} \ge 16$。
  - 独立运行 `work_gc_t4_horizon/agy_scratch/check_ord.py`，8 项断言全部无浮点通过。

---

### 3. Lemma EXT-T4（NOTES §3，第 88–120 行）
- **结论**：**成立**。
- **逐项核对**：
  - **三分区间覆盖**：$[2, K') \cup [K', K_{clock}) \cup [K_{clock}, T_4) = [2, T_4)$。由 Lemma ORD 中 $K' < K_{clock} < T_4$ 保证各区间非空且恰好无缝衔接。
  - **假设一致性**：三个区间引用的前置假设严格均为「$F$ 定义到 $\tau(J-1)$ 含该步」：
    1. $J < K'$：已接受导入 I-4（`PROOF_EGX.md` §3 第 158–161 行，及第 163–171 行 import audit）；
    2. $K' \le J < K_{clock}$：已接受 EXT-CLOCK（`PROOF_CLOCK_HORIZON.md` §3 第 89–94 行）；
    3. $K_{clock} \le J < T_4$：已接受 Theorem T4（`work_claude_residual/NOTES.md` 第 79–81 行、更正块第 1, 2, 7 条；`reviews/claude_residual_review_record.md` 第 25–28 行）。
  - **重点核对——无循环性**：
    - 检查 `work_claude_residual/NOTES.md` 的 DL(i)（第 162–163 行）：指标 $n$ 处的 crossing 其 source epoch 标号 $Q < G(n)$。
    - DL(iv)（第 174–177 行）：在 $S(J)$（$J < T_4$）中，deep chains $t \in \{0,1,2,3\}$ 处的 $c$-步其 source $Q < G(j_t)$，依次有 $Q < T_3, T_2, T_1, N_0$。
    - shallow crossings（$n < N_0$）的 source $Q < G(N_0) < 60$。
    - BBBA 家族（更正块第 1 条）：仅在 $Q \ge T_1$ 且 $j_1-1 > T_2$ 出现，且排除 route c，route b 给 $\theta_1 = 0$，故 $X(J-1)$ 必为 a-型。而 a-型由已接受的 Theorem RA 直接吸收。核对 `PROOF_CLOCK_HORIZON.md` §1 第 2 条，Theorem RA 的假设**仅有**「$F$ 定义到 $\tau(J-1)$ 含该步」，完全不要求任何子级 EXT 假设。
    - `C5_EXTENSION` §4 的归纳仅在单个 $S(J)$ 内部（$\le 4$ 个 deep steps）进行，并非对 $J$ 的归纳。
    - **无循环核心**：由 Lemma ORD，$T_3 < K_{clock}$，因此证明中调用的所有 source epoch $S(Q)$ 的标号 $Q < T_3 < K_{clock}$ 全部严格落在第 1 与第 2 区间内，已由已有成果无条件确立！不存在任何对 $J' \in [K_{clock}, J)$ 的 EXT 使用。
  - 终止条款（even return, $\le \max(0, J-2)$ exit chains）由 `PROOF_EGX.md` §5 第 206–208 行标准成立。

---

### 4. Lemma DATA-T4（NOTES §4，第 121–145 行）
- **结论**：**成立**。
- **逐项核对**：
  - **(a) 数据局部性**：核对 `PROOF_EGX.md` §1（第 53–56 行）原文：
    `it needs F's crossing data X(m), m <= J-1, and F's own chains at steps <= tau(J-1) inclusive`；
    以及 §3 import audit（第 163–171 行）：
    `The F-facts they use are: crossing data X(m), m <= J-1; the copied W-chains at tau(m), m <= J-1 (at or before tau(J-1)) ... None uses the pointer rho or any F step after tau(J-1)`。
    完全逐字一致。
  - **(b) C1 适用条件**：核对 `PROOF_CLOCK.md` §3 第 114–118 行：
    `C1 for every reached crossing, without an exit-length or C2 hypothesis. If the current crossing step is the first undefined step, the induction stops there ... Its own time is already bounded by the preceding induction.`
    因 $X(J-1)$ 位于步 $\tau(J-1)$，且假设 $F$ 在该步有定义，故 $X(J-1)$ 属于 reached crossing，C1 无条件给出 $\tau(J-1) \le (J-1)^2$。
  - **(c) 数值链**：若 $J < T_4$（$J \le T_4-1$ 为整数），则 $(J-1)^2 \le (T_4-2)^2$。由 Lemma HINQ 在 $H = T_4 > 2^{64} \ge 16$ 时给出：
    $$3(T_4-2)^2 + 4 < 2^{T_4} \implies (T_4-2)^2 < \frac{2^{T_4}-4}{3}.$$
    数值链严格闭合。

---

### 5. Theorem H-T4 (i)（NOTES §5，第 148–177 行）
- **结论**：**成立**。
- **对照 `PROOF_EGX.md` §5 Theorem U(b)（第 215–226 行）逐条核对**：
  - 将 I-4 替换为 Lemma EXT-T4 后，归纳假设为：步 $< t$ 均有定义且 $3t+4 < 2^{T_4}$。
  - 步分类（`PROOF_M.md` Corollary 3.5）：仅 level fires 与 exit chains 可能违背 S1；S2 永不违背；内部步由 replay Lemma 2.1–2.3 保持定义；偶数步有定义。
  - **Level fire at step $t$**：指针 $\rho$，$s_0 = \tau(\rho) = t$，$J = v_2(3s_0+4) < T_4$。
    S1 即 $J < \rho$：
    - $\rho \le 10^8$：已有 V2 审计基底（`PROOF_EGX.md` §5 第 217–218 行）；
    - $\rho > 10^8$：`PROOF_CLOCK.md` §4 第 133 行 STATE-CLOCK 无条件给出 $s_0 \le \rho P(\rho) < \rho(2\rho+1)$，故 $2^J \le 3s_0+4 < 2^\rho$，即 $J < \rho$。
  - **Exit chain $t' \ge 1$ 与严格性 $\tau(J-1) < \tau(\rho) = t$ 的独立验证**：
    - 检查 `work_m/verify_m.py`（第 208–216 行）关于同时刻 crossing 的生成结构：
      在步 $s$ 处，仅当 $k = \mathrm{len}(P) = 0$（即 $P = \emptyset$）时，才会同时记录两个 crossing $X(i)$ 与 $X(i+1)$。其中 $X(i)$ 必为 a-型（$\epsilon=0$），$X(i+1)$ 必为 b-型（$\epsilon=1$）。当 $k=1$ 时仅记录一个 c-型 crossing，当 $k \ge 2$ 时无 crossing。
      因此，**仓库模型中同时刻出现的 crossing 对只有且必然是 $(X(m)\text{ a-型}, X(m+1)\text{ b-型})$**。
    - 现考虑在指针 $\rho$ 处的 level fire：其发生于 $P = \emptyset$，对应 crossing 为 $X(\rho)$，类型必为 a-型。
    - 若假设 $\tau(\rho-1) = \tau(\rho)$，则二者必须构成同时刻配对，由上可知 $X(\rho)$ 必须为 b-型。这与 $X(\rho)$ 是 a-型矛盾！
    - 因此必有 $\tau(\rho-1) \ne \tau(\rho)$。由于 $\tau$ 随指标非减，严格得出：
      $$\tau(\rho-1) < \tau(\rho) = s_0 = t.$$
    - 由 $J < \rho$（$J \le \rho$ 为整数，故 $J-1 \le \rho-1$），得出：
      $$\tau(J-1) \le \tau(\rho-1) < \tau(\rho) = t.$$
    - 因此步 $\tau(J-1)$ 严格位于步 $< t$ 的已定义前缀内，$F$ 在其上有定义。Lemma EXT-T4 适用，$S(J)$ 为 tie-free。
  - **系数裕度**：
    由 `PROOF_M.md` Lemma 6.1 与 Lemma 3.2，$\sigma_{t'} - j_{t'} = (\rho - J) + h_{t'}$。由于 $\rho - J \ge 1$ 且 $h_{t'} \ge 1$，差值 $\ge 2 > 0$，S1 在所有 exit chains 处成立。
  - **终止**：$S(J)$ 在至多 $\max(0, J-2)$ 步内偶数返回，$P = \emptyset$，指针前移 $\ge 2$。步 $t$ 有定义，归纳顺利推进至所有满足 $3t+4 < 2^{T_4}$ 的步。

---

### 6. Theorem H-T4 (ii)（NOTES §5，第 179–222 行）
- **结论**：**成立**。
- **对照 `PROOF_EGX.md` §3 Corollary H（第 173–179 行）逐条核对**：
  - 单步归纳基于单态时间（singleton times）：基底 $L_0 = (3)$ 位于 $n=0$，$0+2 = 2 < 2^{T_4}$。
  - 在单态 $n$ 处（$n+2 < 2^{T_4}$）：
    - S2 判据（`work_r4/PROOF.md`:18–19）：$A+2b+3 = 3(n+2)$ 能被 3 整除，绝非 2 的幂，不在此停机。
    - $n$ 奇数：下一单态为 $n+1$（S1）。
    - $n$ 偶数：设 $v := v_2(n+2) < T_4$，$w := (n+2)/2^v$ 奇数。进入 $E(w,v)$。
      - $v \le 2000$：Lemma E(v)（Class-A）涵盖，不停机且到达 $n+1+\ell(v)$。
      - $v \ge 3$：
        - 检验 I-3 reached-crossing 论证：
          步 $(v-1)^2$ 与 $(v-1)^2+1$ 均满足 $3s+4 \le 3((T_4-2)^2+1)+4 < 2^{T_4}$（Lemma HINQ），均落在定理第 (i) 部分确立的 $F$ 已定义前缀内。
          在步 $(v-1)^2+1$ 处，$s = (v-1)^2+1 > (v-1)^2$。由 `PROOF_CLOCK.md` §4，定义前缀内每个状态均满足 $s \le i^2$，故 $i^2 \ge s > (v-1)^2 \implies i > v-1$。
          由于原始指针 $i > v-1$，crossing $X(v-1)$ 必然已被触及（reached）！
          由 C1（`PROOF_CLOCK.md` §3），$\tau(v-1) \le (v-1)^2 < (2^{T_4}-4)/3$，$F$ 在步 $\tau(v-1)$ 有定义。
        - 由 Lemma EXT-T4，$S(v)$ tie-free 并以偶数返回终止。
        - 由 D5（队列确定性）与 Theorem EGX，endgame 与 $S(v)$ 逐对一致，对任意奇数 $w$ 安全到达单态 $(2^v, 3\ell(v))$。
        - 由 E1–E4（`work_global_endgame/LEMMAS_E.md`），真实轨道与 pair 映像完全吻合，全程不停机。
  - **覆盖论证（Coverage）**：任意 $n^* < 2^{T_4}-2$ 若非单态时间，则落在相邻单态 $n < n'$ 之间，满足 $n+2 \le n^*+2 < 2^{T_4}$，全程被 excursion 覆盖。
  - **Off-by-one 检查表**：
    - 视野不等式：$3(H-1)^2+4 < 2^H \implies (v-1)^2 < (2^H-4)/3$（$v \le H-1$），与 precedent 一致；
    - 首个使 $v_2(n+2) \ge T_4$ 的单态恰为 $n = 2^{T_4}-2$，集合 $\{n : n+2 < 2^{T_4}\}$ 恰为前 $2^{T_4}-2$ 个顶层步，完全遵循 Corollary H'' 与 Corollary H-CLOCK 惯例；
    - 其它各项（fire 界、通过 $\tau(J-1)$、excursion 记账）均与前例精准吻合。

---

### 7. [B] 声明的诚实性与独立复算（NOTES §6）
- **结论**：**成立**。
- **声称核实**：
  - NOTES §6(c) 所报默认预算数据：$H_0 \in \{20,22,24,26\}$；$H_0=26$ 对应 $F$ 前缀 $s^* = 22,369,619$ 步，指针 $25,074,248$，$7,594,491$ fires，$595,760$ exit chains，$7,594,490$ closed epochs；顶层步 $67,108,862$，$29,990,130$ singletons，最大 $v = 25 = H_0-1$；最小 fire 裕度 $\rho - J = 3$。
  - 核对 `t4_horizon_checks.json` 与 `extended_run_900s.log`，上述数字全部逐字完全吻合。
  - 声明边界明确：明确声明属于模式验证（pattern validation），非数学证明，且解析证明不依赖于有限范围 $H_0$。
- **独立代码复算（Auditor 2 独立代码，无外部依赖）**：
  - 编写脚本 `work_gc_t4_horizon/agy_scratch/independent_verify.py`，采用仓库 Class-A 规则：
    1. 顶层映射按 `work_r1/RULES.md` / `work_r4/PROOF.md` 执行，核对停机判据与和不变式；
    2. pair map $F$ 记录 $X(n)$ 的状态与 $\tau(n)$；
    3. 符号退出 $S(J)$ 按 `work_m/verify_m.py` 逻辑计算；
    4. pair endgame 自 $X(v-1)$ 出发，单态判定按队列 $P$ 清空（`len(P) == 0`，即列表仅余单项 $A$）执行。
  - 在 $H_0 = 18$ 尺度（$262,142$ 顶层步，耗时约 5 秒）进行独立复算，输出如下：
    - (i) 顶层映射前 $262,142$ 步无停机，每步和不变式 $\sum L_n = 3n+3$ 均严格成立；
    - (ii) 共出现 $117,155$ 个单态，每个偶单态的 $v = v_2(n+2) \le 17 < H_0$，且同一 $v$ 在所有不同出现位点上的步数差 $\mathrm{gap} = n' - n - 1$ **绝对唯一**，与出现次序完全无关；
    - (iii) 对 $v = 3..8$：从 $X(v-1)$ 出发的 pair endgame 产生的 exit chains $j$-序列与 $S(v)$ 逐项完全相同；且 $\mathrm{gap} = \tau(v-1) + \text{endgame length}$ 恒等成立（具体如 $v=5$ 时 $\tau(4)=2$，endgame 长度 3，和为 5，吻合顶层 $\mathrm{gap}=5$；$v=6$ 时 $2+2=4$；$v=7$ 时 $3+1=4$；$v=8$ 时 $4+2=6$）；
    - (iv) 观测到的步长表 $\ell(1..17)$ 与 `work_r4/PROOF.md` 第 40 行的 Class-A 表完全一致：
      $$\ell(1..17) = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14].$$
  - 复算结论完全再现，数据真实可靠。

---

### 8. 越级检查（Overclaiming Check）
- **结论**：**成立**。
- **核对要点**：
  - NOTES §0 与 §7 均明确声明：**无超出 $J < T_4$ 的主张**，不声称 $T_5$、全局 $\mathrm{EXT}^*$ 或全局不停机；
  - 声明未触动 G1（FREE-B / CL2 / CL4）；
  - 明确承认在三方审查通过前，仓库公认视野维持 $2^{K_{clock}}-2$；通过后才推进至 $2^{T_4}-2$；
  - 与已有的死路清单（如 level method 在 $T_4$ 之后无法稳定等）完全一致，无任何冲突。

---

## 盲审最终结论

`work_gc_t4_horizon/NOTES.md` 的所有声明在给定的导入前提下均推导严密、逻辑闭合，无循环论证；中间涉及的一处展开代数常数笔误（$3H^2-12H+14$ 应为 $3H^2-12H+10$）完全不影响归纳单步增长性质（因 $H \ge 3$ 恒正，而归纳基底为 $H=16$）；塔序引理 Lemma ORD 与迁移记账引理 Lemma EXT-T4、Lemma DATA-T4 全部成立；机理与数值验证完全真实。

VERDICT: 1
