# RECORD BUDGET — 合并 (B)(C) 的记录预算定理

**审查更正（2026-10-24，三方审查 reviews/gateway_trains_review_record.md；优先于正文）**
1. [HIGH] “塔下降 m_{t+1} ≤ G(m_t)+…< m_t−1”与“T ≤ Λ(y_1)+O(1)”只对**首门**成立。C4 要求 y≥N0 且 |D_y|≤5；
   后续门的 y_t=m_{t−1}≪N0，门后祖先缺陷为 (10−2^m)/3 型（|D|≈2^m/3），且 |D_y|≤5 本身来自 Theorem L（仅 n+1<T4）。
   后续门归入 (iv) 小 y 端局——但 (iv) 的 [B] 认证集只覆盖窗口类、36 坏类与 r1r2 族（m<10^8），不在其中的后续门仍开放；(ii)–(iv) 需显式加入 D5：|D_y|≤B_D。
2. [HIGH] 失效模式 F1/F2/F3 **不穷尽**；补 (F4) 祖先缺陷过大，(F5) j≥6 的非 tie NT 门（C1–C5 只处理以 j=5、k=1 结尾的 run，
   “一般 NT 门同型”未证），(F6) 空 run 门（门在段首：toll=0、j'≥y，永不 run-paid；budget_ledger 的 46 门只有 1 个 run-paid）。
   因此“train 长度由 (e) 界定”（B_RANK §2 推论、§8）只在 run-paid 时成立，不是一般结论。
3. [MED] “非 NT 步记录至少降 1”应为“非增；除一步下降（R 不变）外严格降”；F2 中一步下降对 toll 计 +1（drop 为 0）。
4. [MED] (RB-toll) 的富余应按平均法：drop ≥ max(n, y−5−n·c)，富余约 0.415·y/(4log2 y+5)（y=N0 时约 8·10^4，
   不是 2·10^7）；前提是段内无一步下降。“记录 ≤J，等号仅在锚”不对（j'=y−toll−1 可取等，一步下降保持 R）。
5. 定理 RB 的“对 J 统一”只能作为附条件表述（首门 + (ii)–(iv) + D5）；不证明全局 EXT，K_clock 不变。
6. 正文与 NOTES §0 中残留的“失效模式穷尽”“至少降 1”“富余 2·10^7”“≥10.95”“B1 推论 [A]”均以本更正块为准。


2026-10-24。作者：coordinator（本会话）。复算 gate：
`python -B work_gateway_trains/budget_ledger.py`（status PASS，45 走法 / 46 门 / 0 失败），
`python -B work_gateway_trains/B_rank/train_checks.py`（PASS），`python -B
work_gateway_trains/C_climb/climb_checks.py`（PASS，115,121 检查 / 0 失败）。
不证明全局 EXT，不声称不停机，K_clock 不变。标签：[A]（本文件或所列 work_gateway_trains
子文件从列出的导入证明）、[A-imp]（已接受导入）、[A-cond]（显式条件）、[B]（有限精确
计算，范围写明）、[C]。(B) 由 coordinator 完成（子 agent 两次启动失败）；(C) 由外部
agent 完成；两者的文件分别是 B_rank/B_RANK.md 与 C_climb/C_CLIMB.md。

---

## §1 记账设定（与 CONTEXT.md §1 一致）

链状态 (j, x, Θ, Γ)，x = 2^j u（u 奇），记录 R = j + Γ。精确走法（每步 x' ≠ 0；
零门单独处理）。步型按输出参数分类（THEOREM §2.1/§2.3，已接受）：

- **强下降 a 步**（p ≤ j−2）：j' = p ≤ j−2，Γ' = Γ+1 ⟹ R' = R − (j−j'−1) ≤ R−1；
- **一步下降 a 步**（p ≥ j）：j' = j−1，R' = R（降 0）；
- **b/c 步**：j' = ω ≤ j−2−ε，Γ' = Γ+1+ε ⟹ R' = R − (σ−ω) ≤ R−1（σ = j−1−ε > ω，S1）；
- **NT 门**（p = j−1，x' ≠ 0）：j' = v2(x') ≥ j，R' = R + (j'−j+1) ≥ R+1；
  j=5 tie：j' = m，攀升 m−4。**记录只在 NT 门上升**。
- **零门**（NT 且 x' = 0）：走法终止。

**run（段）**：相邻 NT 门之间的极大非 NT 段。第 t 个门的 **run 峰值** y_t = 段首参数
= 上一门输出 m_{t−1}（首段 j_0），**R_peak(t) = R_after(t−1)**（首段 R_0），
**toll_t = Γ(gate_t) − Γ(peak_t) = Σ(1+ε)**，段内 drop_t = (y_t − j_gate) − toll_t ≥ 0。

## §2 Ledger Theorem（账本恒等式）[A]

**定理（Ledger）。** 精确走法从 (j_0, Γ_0) 出发，R_0 = j_0+Γ_0，NT 门 g_1..g_T。则：
(a) 段内 R 非增，每步降幅 j−j'−1−ε（a 步 ε=0；一步下降 0）；
(b) 门处 R_after = j'+Γ+1，攀升 = j'−j+1（j=5：m−4）；
(c) **支付恒等式** R_after(t) − R_peak(t) = j'_t + 1 + toll_t − y_t；门 t **run-paid**
    ⟺ j'_t ≤ y_t − toll_t − 1；**globally-paid** ⟺ R_after(t) ≤ R_0；
(d) **max_t R_t = max(R_0, max_t R_after(t))**；R_t ≤ R_0 ∀t ⟺ 每个门 globally-paid；
    每个门 run-paid ⟹ R_t ≤ R_0；
(e) 每个门 run-paid ⟹ 门输出严格下降 m_t ≤ m_{t−1} − toll_t − 1 ≤ m_{t−1} − 1
    （相邻门 toll=0 亦降 ≥1）⟹ T ≤ j_0 且一切参数 ≤ j_0。

证明：步型公式代入与段归纳（budget_ledger.py 逐门验证；其中 L1–L3 的逐行检查由
步规则 R' = j'+Γ' 自身生成，属**代码自洽性检查**，实质检验是 L4/L4b——对真实
maxrec 断言"全部门 globally-paid ⟺ maxrec ≤ R_0"与"maxrec 在段首或门后取到"：
45 走法 / 46 门 / 0 失败。样本：witness (73515,98094) 首门 run-paid、余门由积累
slack globally-paid、maxrec = R_0；36 坏类代表元门攀升 ≤ 3（入口门）或 ≤ 14
（17→5 后）；O2 族单门攀升 m−4 任意大——精度耗尽，非 Ledger 反例）。

## §3 NT 输出界（(C) 注入：一般入口的爬升界）

以下来自 C_climb/C_CLIMB.md（标签照抄；常数与验证见该文件）：

- **Theorem C1 [A]**：经长度 r 的 run（y = j₀ > j₁ > … > j_r = 5，强下降 a 与 b/c）
  进入裸 tie 后的 catapult 输出满足 **x'' = A''·u_y + Z_run**，Z_run := 6d_r+8−β_r/2
  （锚 (A₀,β₀,d₀) = (2^y, 0, (D_y−1)/3) 沿 run 跑仿射递推），μ := v2(A'') =
  y−1−#a−Σ(1+ε) ≥ r+4；**v2(Z_run) < μ 时 m = v2(Z_run)（与 u_y 无关）**；
  v2 > μ 时 m = μ；v2 = μ 时 m ≥ μ+1 依赖 u_y（O2 机制）。
- **Lemma C3 [A]**：Z_run = S·D_y + Cst 且 **S ≠ 0 恒成立**（无"恒等相消 run"）；
  w := v2(S) ≤ 1。
- **Theorem C4 [A+常数B]**：y ≥ N0 = 2·10^7、|D_y| ≤ 5 时
  **m < G(y) + log2(3/2)·s + 2log2(r+1) − 10**（s = run 中 b/c 步数；网格最小富余
  10.98；m < G(y)+1 当 0.585s + 2log2(r+1) ≤ 11，如 r ≤ 30（s=0））。每 b/c 步代价
  log2(3/2) ≈ 0.585，每 a 步仅累计 2log2(r+1)。
- **Theorem C5 [A]**：{D_y : v2(Z_run) ≥ L} 为空（该 run 对一切祖先无条件安全，
  m = v2(Cst)）或 **mod 2^{L−w} 的单残基**（w ≤ 1）；排除爬升是祖先 (D_y；边界情形
  加 u_y) 的来源/相位条件。
- **Corollary C6 [A-cond]**：C 字母入口同样适用；最小严格反例归纳内
  σ_y ≥ y−4log2(y)−5 认证 m 且 m < G(y)+O(1)；归纳外为显式假设 (Hσ) σ_y ≥ m+1−w。
- 退化：r=1 精确退化为 Lemma CB（4,396 恒等式）。

**NT 门输出界（本文件记号）**：在 C1 的条件下（含 Z_run ≠ 0、v2(Z_run) ≠ μ、
|D_y| ≤ B_D），**j'_t ≤ G(y_t) + log2(3/2)·s_t + 2log2(r_t+1) − 10**（y_t ≥ N0），
或一般地 j'_t ≤ ⌊log2 B_run(y_t, r_t, s_t, B_D)⌋。一般 NT 门（j ≥ 6，非 tie）同型：
同一 catapult 机制（A2/C1），界同形式。

## §4 run-payment 的失效模式（(B) 注入）

run-paid ⟺ j' ≤ y − toll − 1。由 §3：y ≥ N0、|D_y| ≤ 5 时自动成立只要

    toll ≤ y − G(y) − 0.585·s − 2log2(r+1) − 9.                                (RB-toll)

失效模式（穷尽）：
- **(F1) 小 y**（y < ~2log2 y + 0.585s + 2log2(r+1) − 7）：[B] 认证——36 坏类代表元
  的门在其可用精度内被类递推复现（攀升 ≤ 3（入口门）、≤ 18 = y+1（17→5 后）；
  注意 m 本身不由 tie 类决定，B6）；窗口 5 ≤ j < 2·10^7 除 (5,5),(5,−11) 全
  certify。
- **(F2) 高 toll**（违反 (RB-toll)）：toll = Σ(1+ε)，一步下降贡献 0、ε 大的 b/c 贡献
  大。一步下降链受 Lemma ND 约束（需 2^{j−1} ≤ 3^r(3(j−1)P(j−1)+2|d|)，**秩 r 买通
  j ≤ 1.585r + O(log j)**）；高 ε 受最小反例归纳内 C2-log/PROOF_EXT_ROOTS 约束
  （1+ε ≤ 4log2 y + 4 ⟹ (RB-toll) 对 y ≥ N0 成立，富余 ~2·10^7）。归纳外 = H5 型
  条件。
- **(F3) 残基/精度**：C5 的单残基 S·D_y ≡ −Cst（爬升超界的祖先类）、边界
  v2(Z_run) = μ 的 u 依赖爬升（O2）、以及 m ≥ σ 的精度耗尽（O1：B_rank B5 的移动
  单残基 C ≡ −3^{r+1}k_j (mod 2^{j−2})，危险集是轨道，密度 2^{−v2(3k)−2}）。
  **这些是来源/相位条件，不是参数上界**；规范数据上 (S2*) 25/25 通过（B8）、
  tie 进入类在 j₁ = 17 恰 2^13/2^18 = 2^−5、j₁ ∈ [18,19] 全枚举为 0（C9 刚性）。

**gateway train（(B) 的结构性结论）**：严格全 a train 中 tie 类在 {5,21} (mod 32)
强制交替，内部 label 需 k ≡ 6 (mod 16)（mod 32 副本 22/6 与奇偶配对；最小 17；
[7,10^6) 内 27,879 个）；内部 B-return 在 [7,10^6) 不存在。**类层约束不单独界定
train 长度**；train 长度由记录预算（(e)：run-paid ⟹ m 每块至少降 1）或精确态时钟
同余（Astra TRAIN/ENTRY/CLOCK-ORBIT/ADVANCE——本轮已审查接受，见
review_trains/REVIEW.md：全 a train 在 [5,16381] 至多 3 个连续 catapult label
[A+B]，band 版同，周期不可精确重复 [A]，τ≤n 与 param-3 间距已复算到 n<10^8）
或 (S3) 控制。
秩律：r ↦ r+1（例外：tie 类 ∈ {21,−27} 时首块不开分母；裸 tie (5,−11) 必开）。

## §5 记录预算定理（合并陈述）

**定理 RB（记录预算）[A + A-cond + B]。** 设仿射锚走法（S(J)：R_0 = J = σ 锚精度；
一般来源：天花板 min(J, σ)）满足：
(i) 每个非 NT 步（无需条件）：R 至少降 1（一步下降降 0）——§2(a)；
(ii) 每个门的前导段（run）满足 C1 的 run 定义（强下降 a 与 b/c，**特别地无一步
    下降**——一步下降段需下述扩展），且门满足 C1 的非退化条件（Z_run ≠ 0、
    v2(Z_run) ≠ μ——排除 C5 残基与 O2 边界；来源/相位条件）。**扩展（挑错后补）**：
    恒等式 x'' = A''·u_y + Z_run、Z_run = S·D_y + Cst 与尺寸界 |Z_run| ≤ B_run 对
    任意非 NT 段（含一步下降）成立（纯三角不等式展开，不用 C2 的分层）；此时若
    v2(Z_run) > μ 则 m = μ < log2 B_run 自动在预算内，故一般段的结论只需替换
    "m = v2(Z_run)" 为 "m ≤ max(v2(Z_run), μ) ≤ ⌊log2 B_run⌋"（m = μ 情形记录
    攀升 j'−j+1 = μ−j+1，仍由 (RB-toll) 支付）；
(iii) 该门的 run 满足 (RB-toll)（y ≥ N0、|D_y| ≤ B_D 时由 C4 + toll 界保证；
    归纳内 toll 由 C2-log 自动，归纳外为 H5 型假设）；
(iv) 小 y 门（y < y_*）落在认证集（[B] 窗口 + 24/36 坏类；代表元走法全部终止）。

则：**每个门 run-paid（§3 界 + (RB-toll)）⟹ 一切记录 ≤ R_0**（§2(d)），且门输出
按塔下降 m_{t+1} ≤ G(m_t) + 0.585·s + 2log2(r+1) − 10 < m_t − 1（y_t = m_{t−1} ≥ ~30
时），故门数 T ≤ Λ(y_1) + O(1) 量级（塔迭代 G），总爬升 Σ(m_t−4) = O(log y_1·Λ) ≪
Σ 段付费 ≈ y_1 ≤ R_0。对 J 统一：**S(J) 的记录 ≤ J（等号仅在锚），且无 m ≥ σ 的
精度耗尽事件**——只要 (ii)–(iv) 对每个门成立。

**剩余缺口（诚实账；全部为来源/相位型，非参数上界）**：
1. (ii) 的 C5 残基排除（与 O1 的 (SC) 同型；合成频率 2^{−E} 几何衰减，规范刚性
   j₁=17 恰 2^−5，但无结构回避证明）；
2. (ii) 的边界 v2(Z_run) = μ（O2 机制；单 (D_y,u_y)-类刻画，未排除）；
3. (iii) 归纳外的 toll/ε 控制（H5/H5_res 残余源 (i)–(v)）；
4. (iv) 的 [B] 范围（5 ≤ j < 2·10^7 窗口、24/36 坏类、r1r2 族 m < 10^8）与
   j₁ ≥ 2·10^7 的表外刚性；
5. 零门（x' = 0）：5/36 代表元走法在 catapult 处 x'' = 0（负残基代表）——(S2*)
   排除 NT 分支时一并排除，独立处理。

**与 (SC) 的关系**：(SC) r_0+T < 5(σ−53)/8 是 O1 的大小型充分条件；B5 表明其实质
是"移动单残基不命中"，本定理用 C4+C5 把每个门的爬升压到 G(y)+0.585s+O(log r)，
再用 Ledger 的段付费支付——预算差额从 THEOREM §4.1 的 ">3 倍" 转化为 (ii)–(iv)
的逐门条件。

## §6 复算

- `python -B work_gateway_trains/budget_ledger.py` → budget_ledger.json（§2）
- `python -B work_gateway_trains/B_rank/train_checks.py` → train_checks.json（§4 B 部）
- `python -B work_gateway_trains/C_climb/climb_checks.py` → climb_checks.json（§3）
- review_trains/（任务 1）：Astra 文档审查与重放，见 REVIEW.md
