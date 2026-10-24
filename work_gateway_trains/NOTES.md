# NOTES — work_gateway_trains：gateway 链与爬升的控制（(B)+(C)+记录预算）

**三方审查结论（2026-10-24，见 reviews/gateway_trains_review_record.md）**：B1、B2/B4/B6、C1/C3/C5、r=1 退化到 Lemma CB、
Ledger 恒等式成立；RECORD_BUDGET 的“塔下降/T≤Λ(y_1)+O(1)/失效模式穷尽/对 J 统一”被更正（只对首门；补 F4–F6）；
B5 的“移动残基”为坐标表象；B1 推论降为 [B]；C6 限 r=1；Astra 文档处置结论保留，但 MED-1/CF-8/CS-1 的理由已改正。
各文件文首有审查更正块，优先于正文。


2026-10-24。作者：coordinator（ZCode 会话）。本目录只写 `work_gateway_trains/`；
未修改其他目录；未 git 提交。**不证明全局 EXT，不声称不停机，K_clock 不变。**
标签纪律：[A]（从列出的导入证明，假设列全）/ [A-imp] / [A-cond] / [B]（有限精确
计算，范围写明）/ [C] / [REFUTED]（附反例）。合成状态一律标 non-canonical。
被 REFUTED 的六条陈述（THEOREM.md 审查更正）未使用。

## 0. 一页结论

1. **(B) 连续 gateway 块数不能由纯类层约束界定**（B_RANK §2 推论 [A]：两个奇偶
   的可行内部 label 各有无穷多），但得到了比 Astra ENTRY 更强的结构：tie 类在
   {5,21} (mod 32) 间**强制交替**、内部 label 的 k ≡ 22/6 (mod 32) 与奇偶配对
   （B1 [A]，两分支数值验证）；内部 B-return 在 [7,10^6) **不存在**（B2/B3）。
   真实可达统计 [B]：规范 kernel（J≤512）无 tie/gateway；36 坏类代表元+witness
   全终止，最大严格 train = 2，最大 m = 18。**秩盲性**（B5 [A]）：NT 门的本质是
   类命中**移动单残基** C ≡ −3^{r+1}k (mod 2^{j−2})（危险集 = 单轨道，密度
   2^{−v2(3k)−2}，r 唯一 mod 2^{j−4−v2(3k)}）；(SC) 是它的大小型充分条件。
   (S2*) 在全部测试走法的 25 条非门 a-链上通过；DEPTH 捷径在门后链系统性失效
   （lift 位高度，比值仅 1.006–1.15）。
2. **(C) Lemma CB 推广到一般入口**（C_CLIMB）：经任意长度 run 进入裸 tie 的
   catapult 输出满足 x'' = A''·u_y + Z_run（C1 [A]），Z_run = S·D_y + Cst 且
   **S ≠ 0 恒成立**（C3 [A]：不存在恒等相消 run）；爬升界
   **m < G(y) + log2(3/2)·s + 2log2(r+1) − 10**（y ≥ N0、|D_y| ≤ 5；C4，富余
   ≥ 10.95）；**爬升超界 = 单残基**（C5 [A]：{D_y : v2(Z_run) ≥ L} 为空或
   mod 2^{L−w} 单残基，w ≤ 1）；C 字母入口在最小反例归纳内由
   σ_y ≥ y−4log2(y)−5 认证（C6 [A-cond]）。r=1 精确退化为 Lemma CB（4,396
   恒等式）。规范刚性 [B]：tie 进入在 j₁=17 恰 2^−5、j₁∈[18,19] 全枚举为 0；
   9 个 y 至 2·10^7 的规范 run 全部 m ≤ 7。
3. **记录预算定理**（RECORD_BUDGET §2/§5）：Ledger [A]——非 NT 步记录至少降 1
   （一步下降降 0），NT 门至多升 j'−j+1（tie 步 m−4），**records ≤ R_0 ⟺ 每个
   门 globally-paid**（j'_t ≤ R_0−Γ_t−1），maxrec 在段首或门后取到；run-paid
   （j' ≤ y−toll−1）⟹ 门输出严格下降（T ≤ j_0）且与 C4 组合给出塔下降。合并
   定理 RB：在 (ii) 非退化（C5 残基与 O2 边界排除——来源/相位条件）、
   (iii) toll/ε 控制（归纳内自动）、(iv) 小 y 端局 [B] 认证下，S(J) 的记录 ≤ J
   对 J 统一。失效模式穷尽为 (F1) 小 y / (F2) 高 toll（一步下降链，秩买通
   j ≤ 1.585r+O(log j)——与 O1 精确耦合）/ (F3) 残基与精度耗尽。
4. **任务 1（Astra 文档审查）**：四篇主文档**全部 ACCEPT，无一条被否定**（详见
   §2）。两处日历事实被审查员复算加强到 n<10^8：τ(n) ≤ n（max τ−n = 0）、
   param-3 源火指针间距 ≥ 12（文档只需 ≥5）。

## 1. 产物与复算（详见 MANIFEST.md）

| 产物 | 内容 | gate |
|---|---|---|
| CONTEXT.md | 共享背景/形式体系/基础设施/诚实性规则 | — |
| B_rank/B_RANK.md | (B) 全部结论（B1–B8 + 剩余条件） | `python -B work_gateway_trains/B_rank/train_checks.py` → PASS（T1–T9，0 失败） |
| C_climb/C_CLIMB.md | (C) 全部结论（C1–C6 + 退化 + 刚性 + 缺口） | `python -B work_gateway_trains/C_climb/climb_checks.py` → PASS（115,121 检查，0 失败） |
| budget_ledger.py | Ledger 恒等式 L1–L4（45 走法/46 门） | → PASS |
| RECORD_BUDGET.md | §2 Ledger [A]；§3 (C) 注入；§4 失效模式；§5 定理 RB | 上述三个 gate |
| review_trains/REVIEW.md 等 | 任务 1：四主文档逐条判定 + 五次级文档 + 状态行 | `python -B work_gateway_trains/review_trains/review_checks.py` → PASS（exit 0） |

## 2. 对 Astra 文档的处置（任务 1 结论；逐条判定见 review_trains/REVIEW.md）

- **GATEWAY_TRAIN.md — ACCEPT**。二 a 步递推与 (TRAIN) 必要同余 [A]（四项零和
  最小值出现两次原理；m_{i+2}+2 的下标不对称是对的）；无三连相同 catapult [A]；
  5776 顶点必要条件图有环 [B]（如实报告，未冒充无环）；圈 (8,244,81,27) 不可
  精确重复 [A]。
- **CLOCK_FILTERED_TRAIN.md — ACCEPT**。(ENTRY) k ≡ 6 (mod 16) [A]、最小内部
  label 17 [B]；(DROP2) [A]；param-3 间距 ≥5 [结构性+复算到 10^8]；[5,16381]
  至多 3 个连续 catapult [A+B]；532/14 图无环 [B]。原论证已完整（J=3 epoch 长 5 且奇 a
  交叉即 fire 指针）；审查中关于 2²-jump 的说法已撤回。
- **TRAIN_CLOCK_ORBIT.md — ACCEPT**。(CLOCK-ORBIT) [A]；周期 2^{L−7} [A]；
  (ADVANCE) v2(Σ)=L−2（lift 不变性严格）[A]；周期不可精确重复（含奇倍）[A]。
- **CROSS_SCALE_TRAIN.md — ACCEPT（作为构造）**。四 catapult 局部见证被独立
  重放（词、损失、记录、SHA-256 全对）；c_r 相容性为存在性 [A]（审查员用
  mod 2^48 的 2-adic dlog 见证验证）；只否定无人主张的"全尺度三 catapult 上限"。
- **次级五篇（DEPTH_CLOCK_BUDGET / SEED_BUDGET / COPY_BUDGET /
  JOINT_HEIGHT_BUDGET / STOP_CHECKPOINT）**：[A-cond]/[A]+[B] 标签概览见
  REVIEW.md §5；恒等式逐步复验（含 256-bit dlog 大数逐位核对、ρ−P≥3 与
  ρ≥P+11 归纳、O2 族 W=8<9 反例重放）；十份 verifier 复跑全 PASS。共同点：
  均为条件/分段结果，不是全局排名函数（文档自己如此声明，审查确认）。
- 可直接写入 CHECKPOINT 的状态行：REVIEW.md §8 的五条草案。

## 3. 与已接受结果的衔接

- B1 与 work_claude_shift Theorem S / THEOREM §3.1 的 A 型入口同余一致（是其
  mod 32 精化 + 交替结构）；与 CLOCK_FILTERED 的 ENTRY 一致（22 ≡ 6 mod 16）。
- C1–C6 与 Lemma CB（r=1 精确退化）、STOP_CHECKPOINT 的 β 判据
  （v2(β') < J−Γ−1 ⟺ v2(Z_run) < μ）一致；C5 的单残基与 O1 的 (SC)
  （3^r ≢ −A^{−1}）同一机制、与 B5 的移动单残基互补（不同链上的不同事件）。
- Ledger §2(e)（run-paid ⟹ m 严格下降）**不是**被 REFUTED 的 tie→tie 记录律
  (R)（那是 ρ(t+1) ≥ ρ(t)+(m−4) 的错误方向）；反例走法 (73515,98094) 在
  budget_ledger 中作为样本逐门核账。
- 规范统计与 CHECKPOINT work_global_ext [B]（J ≤ 10^8 无 tie）一致。

## 4. 未解决点（诚实账；全部为来源/相位型或 [B] 范围，非参数上界）

1. **移动单残基不命中**（B5/RECORD_BUDGET §4(F3)）：对一般来源/提升未证；
   C5 的祖先残基 S·D_y ≡ −Cst (mod 2^L) 同型（合成频率 2^{−E} 几何衰减，
   无结构回避证明）。
2. **O2 边界**（v2(Z_run) = μ 的 u 依赖爬升）：已刻画（单 (D_y,u_y)-类/级），
   未排除。
3. **归纳外 toll/ε 控制**（(F2)）：H5/H5_res 残余源 (i)–(v) 未清。
4. **小 y 端局的 [B] 范围**：窗口 5 ≤ j < 2·10^7、24/36 坏类、r1r2 族
   m < 10^8；j₁ ≥ 2·10^7 的表外刚性未扫（本轮 C 扫到 12000，B 扫到 10^6）。
5. **类层 train 无界**：长度 ≥ 3 的规范 run 未找到（刚性），其公式覆盖仅合成
   数据（non-canonical）+ [A] 恒等式。
6. **零门**（x' = 0）：5/36 代表元走法在 catapult 处 x'' = 0（负残基代表）；
   (S2*) 排除 NT 分支时一并排除，独立义务。

## 5. 下一步建议

1. 把 (F3) 统一成一个"移动残基联合回避"陈述：B5（a-链残基）× C5（tie 入口
   祖先残基）× ENTRY 交替配对——在同一规范日历上联合统计命中率 [B]，寻找
   结构性互斥（如交替奇偶是否使两级残基不相容）。
2. j₁ ≥ 2·10^7 的规范刚性扫描（Calendar 查询可行；C 的 TIE_REACH 方法直接
   推广）；顺带把 B3 的内部 label 扫描推到 10^7。
3. (F2) 的归纳外情形：把 work_claude_shift 的 H5_res 残余源 (i)–(v) 与本目录
   的 toll 预算对接（哪类残余源能产生违反 (RB-toll) 的高 toll run）。
4. REVIEW.md §8 的五条状态行提交 CHECKPOINT（用户决定）。

## 6. 协作与审查记录

- (B)：两次尝试启动子 agent 均因并发上限失败，由 coordinator 完成。
- (C)：外部 agent 完成（C_CLIMB.md + climb_checks.py，115,121/0）。
- 任务 1（Astra 审查）：外部 agent 完成（REVIEW.md + review_checks.py，19 项
  独立检查 + 10 份 verifier 复跑 + n<10^8 流式复算）。
- **独立挑错**（内部）：外部 agent 对 B/C/Ledger/RECORD_BUDGET 做对抗审查
  （1,000+ 项独立复算，全部 [A] 声明独立重推）。结论：无实质数学错误；
  修补项已全部落实——
  - RECORD_BUDGET 定理 RB(ii)：补"段内无一步下降"假设 + 扩展引理（恒等式与
    尺寸界对任意非 NT 段成立，m = μ 情形仍在预算内）[MED]；
  - B_RANK §5 "⟺ NT 门"措辞（改为 p ≥ j−1 事件）、§7 tie 拆分（7+2）、
    work_global_ext 引用精确化 [LOW]；
  - C_climb：X(6132) 重复添加去重（169→168 池、2,028→2,016 实例、总数
    115,289→115,121）、§7 频率公式改为诚实表述、residue 检查改为全 run/级
    累积、§9 "[7..16] 全枚举"措辞 [LOW×4]；
  - budget_ledger：L1–L3 检查性质说明（自洽性 vs L4 实检）[LOW]。
  修补后三个 gate 重跑全 PASS。
