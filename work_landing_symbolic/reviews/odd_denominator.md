# 审阅报告 — work_c3_drift/ODD_DENOMINATOR.md

审阅者：审阅者-odd-denominator（workflow subagent）
日期：2026-10-23
目标：`work_c3_drift/ODD_DENOMINATOR.md`（全文 122 行）
范围约束：只读其他目录；只在本文件与 `work_landing_symbolic/reviews/scratch/` 下写文件；未运行 `verify_odd_denominator.py`（工作流已运行一次，按指示不重跑）；未修改任何被审文档；未声称全局 EXT。

---

## 0. 读过的背景（按任务要求）

| 文件 | 读的范围 |
|---|---|
| `CHECKPOINT_1RB1LA_0RC0RD.md` | L614–681（work_claude_ext_next / work_claude_shifted / work_deep / work_r1r2 / work_c3_drift 三节） |
| `reviews/c3_drift_review_record.md` | 全文 33 行 |
| `work_r1r2/NOTES.md` | L1–430（§0–§5，含 κ/P/L/Λ 定义、Lemma 2.3、Cor 2.6、Lemma 5.1/5.3） |
| `work_claude_shifted/NOTES.md` | 全文 264 行（Theorem SC、Prop 3.2、§4 窗口证书、§5 gateway-tie） |
| `work_global_ext/PROOF_EXT.md` | L1–120（§2 走法、Lemma K/HP/AB/RB） |
| `work_c3_drift/C5_EXTENSION.md` | 全文 174 行（§1 AA/BA 类恒等式、§2–3 BA 裸 tie、§4 H5/C7） |
| `work_c3_drift/CONGRUENCE_TARGET_NOTE.md` | L130–273（§2 CAL-C 失败、§3 H3 失败、§4–5 剩余） |
| `work_c3_drift/ORBIT_SHIFT_OBSTRUCTION.md` | 全文 119 行（O1） |
| `work_c3_drift/STOP_CHECKPOINT_2026_10_21.md` | 全文 84 行（O2） |
| `work_c3_drift/OPTIMAL_PHASE_ENCODING.md` | 全文 96 行（O3） |
| `work_deep/NOTES.md` | L80–160（Lemma 2.1–2.5、L/Λ 的 tower、P(j−1)≤j−1） |
| `work_global_clock/PROOF_CLOCK.md` | L25–135（P(n)=2g(n)²+1345、CLOCK、P(n)<2n+1） |
| `work_c3_drift/RATIONAL_MODE.md` | L1–120（分母 3 版本及 tower 估计） |

另读：`work_c3_drift/verify_odd_denominator.py`（未运行）、`work_c3_drift/odd_denominator_checks.json`、`work_ext_roots/verify_low_deficit.py` / `search_roots.py`（Calendar API）、`work_c3_drift/JOINT_HEIGHT_BUDGET.md` 与 `DEPTH_CLOCK_BUDGET.md`（下游引用 N_Q 的上下文）。

---

## 1. 验证命令与输出

### 1.1 文档自带验证脚本（由工作流运行，本审阅未重跑）

命令（任务给定）：

    python -B work_c3_drift/verify_odd_denominator.py

输出（任务给定）：

    exit 0; {"status": "PASS", "review_status": "unreviewed", "a_transition_checks": 11164,
             "gateway_emission_checks": 256, "size_checks": 33,
             "scope": "Finite exact algebra and adaptive-threshold checks, not landing certification or canonical reachability."}

我核对了落盘 JSON `work_c3_drift/odd_denominator_checks.json`：字段一致，`size_samples` 共 33 条，末三条为
`denominator_bits=5000003, threshold=20000020, j=20000020,20000021,20000147`，`LQ=15000003<j`。
这些检查覆盖：a 步恒等式（两种输入精度位）、gateway 的分母/输出位、33 个 size 样本；不覆盖高度递推、L_Q/h_Q 迭代、c 轨道。

### 1.2 本审阅额外做的独立计算（全部在 scratch，非规范可达性声明）

1. `python -B work_landing_symbolic/reviews/scratch/check_calendar_small.py`
   - 输出：`n=4 j=5 odd=True kind='a' time=2 epsilon=0 omega=1`；`X(4)` 为奇 a 型、`k_5=tau(4)/2=1`；`3D'=15-D-y` 在 24 个精确状态上成立。
   - 作用：确认 §3 的恒等式前提（参数五的链只能走 k=1 的 a 步）。

2. `python -B work_landing_symbolic/reviews/scratch/check_odd_denominator_claims.py`
   - `a_step_random_checks: 2894`（随机 Q,C,j,k,b；`v2(y)==p` 且 `Q(t-y)-(3Q-C)≡0 mod 2^{p+1}`）；
   - `bc_step_random_checks: 2777`（`C'=C+Q s`、类模 `2^{j'+1}`、`gcd(C',Q)=1`）；
   - `height_recurrence_states: 2000`，`height_recurrence_max_slack: 0`（即所有测试序列都满足 `|C_t|/Q ≤ A+t`，且等号可达）；
   - `gateway: denominator_choices_ok=2187`（`g∈{1,3}`，约分后分母 ∈{Q,3Q}），`map_ok=True`；
   - `poly_vs_exp_violations: [5..17]`（`1.5(j-1)^2<2^{j/2}` 在 j=18 起成立），`ratio_criterion_first_valid_j: 6`；
   - `c_orbit`：13 项与 `-3+8/3^r` 逐项相等。

3. `python -B work_landing_symbolic/reviews/scratch/check_odd_denominator_thresholds.py`
   - `gateway_random: checks=2874, reduced_denominator_ok=2874`（`D'=(15Q-C)/(3Q)+2^m mod 2^{m+1}`，独立于文档脚本）；
   - `height_map_limit ≈ 7.5`（`h→5+h/3` 的迭代极限），`height_map_below_8: True`；
   - `threshold_table`：见 §4。

4. `python -B work_landing_symbolic/reviews/scratch/check_threshold_numbers.py`
   - r=10^7：`d=15849626, NQ=63398512, exact_first_j=25849628`（即 `Q(κ+B)<2^{j-2}` 只在 j≥25,849,628 成立）；
   - O1：`r=657306078883964, d=1041805486527146, NQ=4167221946108592, m_lower_bound=1051689726214393, m_below_NQ=True, NQ_over_m≈3.96`。

5. `python -B work_landing_symbolic/reviews/scratch/check_o1_digits.py`
   - 用 80 位小数 `log2 3` 复算 O1 的 `d=ceil(r log2 3)`：`r log2 3 = 1041805486527145.1332...`，故 `d=1041805486527146`，与浮点结果一致（delta=0）。

所有 scratch 是合成的、非规范的；它们验证代数与阈值算术，不声称 canonical reachability。

---

## 2. 逐条结论表

标注说明：[A] 对所有参数证明（假设列全）；[B] 有限精确计算（范围写明）；[C] 猜想/数据/论证不足。
“正确？”一栏中的“条件”表示：在文中（或可补出的）假设下正确，但假设未写全。

| # | 行号 | 结论（一句话） | 标注 | 正确？ | 说明 |
|---|---|---|---|---|---|
| 1 | L9–11 | 缺陷表示 `D=C/Q+b·2^j (mod 2^{j+1})`，Q>1 奇，gcd(C,Q)=1 | [A] | 是 | 定义；C/Q 指 `C·Q^{-1} mod 2^{j+1}`；表示的是 2-adic 类，而 |C|/Q 是实高度（两种“大小”独立） |
| 2 | L13–14 | 用的尺寸是实高度 |C|/Q，不是对称整数余数的大小 | [A] | 是 | 与 RATIONAL_MODE 一致；但该高度不是相位的函数，须由来源确定（见 E2/E5） |
| 3 | L15–18 | 奇 a 返回，`p=1+v2(3Qk+C)≤j−2` 时 `j'=p, C'=3Q−C, Q'=Q, b'=0` | [A] | 是 | 精确代入；`x'=3·2^{j−1}u+2D+6k`，`x/2` 项和提升位在模 `2^{j'+1}` 下消失；scratch 2894 例 + 文档 11164 例 |
| 4 | L19–21 | a 分子 `3Qk+C≠0`（gcd=1, Q>1） | [A] | 是 | 否则 Q|C |
| 5 | L22–23 | 严格 b/c 步 `C'=C+Q(Φ−2), Q'=Q, b'=0` | [A] | 是 | 用 W 的 S1（`ω<v2(c'_W)=j−1−ε`）；误差项 `u(2^j−c'_W)` 的 valuation ≥j'+1；scratch 2777 例 |
| 6 | L25–26 | 两步都保持与 Q 互素；AA 减 Q、BA 加 Q、c3 不变 | [A] | 是 | `C'≡C mod Q` / `3Q−C≡−C`；Φ∈{1,2,3} 分别对应 |
| 7 | L28–31 | 反射 `C→3Q−C` 保持 `|C/Q−3/2|`；经 t 个“permitted”步 `|C_t|/Q≤A+t` | [A] 条件 | 条件 | “permitted”未定义；只有当每步 `|Φ−2|≤1` 时才对（c3/AA/BA/a/b）；ε≥7 的 c 步（如 BBBAA 的 +4/3）破坏它。scratch：2000 条合成序列 slack 0（每一步都取 |Φ−2|≤1） |
| 8 | L32–33 | 只在 fixed denominator 的段内成立；跨“bare tie”不保持分母 | [A] | 是（措辞） | 真正改分母的是参数五的 gateway；bare tie (5,5) 恰是 gateway 的特例，但 j=8/12/14/17 的裸类不是 gateway——用词混同 |
| 9 | L37–39 | `N0=2·10^7, B=2^{N0/2}, d=ceil(log2 Q), N_Q=max(N0,4(d+2))` | [A] | 是 | 定义；与 work_deep/work_r1r2 的 N0,B 一致 |
| 10 | L41–44 | `κ(j)≤(3/2)(j−1)²<2^{j/2}`（j≥N0） | [A] | 是 | κ=(3/2)(j−1)P_clock(j−1)；P(j−1)≤j−1 由 work_deep“Size of Λ”[A]；最后的单调性理由有偏移（见 E6） |
| 11 | L45–48 | `Q(κ+B)<2^{d+j/2+1}≤2^{3j/4−1}<2^{j−2}`（j≥N_Q） | [A] | 是 | 逐项：Q<2^d；κ+B<2^{j/2+1}；d+2≤j/4；j>4。文档脚本 33 个 size 样本 PASS |
| 12 | L50–53 | a 分子非零且 |·|<2^{j−2}；至少两层强下降；下一位已知 | [A] | 是 | p≤j−2，b'=0；任意大 Q 成立（阈值随 Q 动） |
| 13 | L55–59 | `L_Q(j)`、`h_Q(q)` 定义；非减 | [A] | 是 | κ、P_clock 未在本文定义（从 work_r1r2/work_deep 引入） |
| 14 | L61 | `L_Q(j)<j`（j≥N_Q） | [A] | 是 | 第一项 ≤d+j/2+2≤3j/4；第二项 ≤2log2 j+3<j；证明省略 |
| 15 | L61–68 | 主条件引理：若 `A+h_Q(q)≤B` 且 ε≥7 的 c 步都在前缀中降到 N_Q 以下，则从 q≥N_Q 出发的走法在 h_Q(q) 条高参数链内结束或降到 N_Q 以下；所有转移严格降记录 | [A] 条件 | 条件 | 结论本身按“降到 N_Q”是对的；但假设列不全：固定 Q（无 gateway）、续走 c 步只有 ε∈{3,5}（即 |Φ−2|≤1）、F 的 defined-prefix、进入记录的预算、以及 A 是来源属性而非相位函数。见 E1–E4 |
| 16 | L72–75 | gateway 恒等式 `3D'=15−D−y`，故 `D'=(15Q−C)/(3Q)+2^m (mod 2^{m+1})`，m=v2(y)<H | [A] | 是 | 仅对参数五的 k=1 a 步；已确认 X(4) 奇 a、τ(4)=2。scratch 2874 随机例 + 文档 256 例 |
| 17 | L77–79 | 约分后分母 ∈{Q,3Q}，仍为奇 >1；Q=3^r（r≥1）必翻三倍 | [A] | 是 | gcd(15Q−C,Q)=1；公因子只能是 3；Q=3^r 时 3∤(15Q−C) |
| 18 | L80–82 | `|(15Q−C)/(3Q)|≤5+|C/Q|/3` | [A] | 是 | 三角不等式；迭代极限 7.5（scratch） |
| 19 | L84–87 | gateway 不导致高度无界增长；输出精度位是 1；之后强下降把它清 0；m<H 本质且六位着陆类不提供 | [A] | 是 | `+2^m` 是提升位；b'=0 需 p≤m−2；六位类只给 m+1≤6，故 m=5 之外不可判 |
| 20 | L89–95 | gateway+a 给出 `c→(c−6)/3`；c_0=5 给 `c_r=−3+8/3^r`；与已接受 3-adic 轨道一致；只是 consistency check | [A] | 是（变量未定义） | 复合是 gateway `5−c/3` 再反射 `3−·`；c 未定义；c_0=5 对应 Q=1，在 §1 的 Q>1 之外；scratch 13 项精确相等 |
| 21 | L99–102 | “同一解析论证现在覆盖每个奇分母模式的大参数部分”；不需要为 27/81 重证 size 引理；全尺度下降仍依赖高度与高亏损 c 条件 | [A] 条件 / 范围 | 部分 | “大参数部分”=j≥N_Q；对 Q≤2^{N0/4−2}（含 27,81）N_Q=N0，成立；对更深的分母，N_Q>N0，只降到 N_Q，残留带 [N0,N_Q) 无人处理（E3/E5） |
| 22 | L104–109 | 固定有限着陆证书仍不够；N_Q 随 log2 Q 增；N_Q=N0 时也有无穷多有理剩余；裸 tie 需精度出处；记录预算需跨 gateway；本引理不证这三件事；故不与有限生成元障碍矛盾 | [C] | 部分（“无穷多”为假） | 有限证书不够的真原因是 δ 可出窗口/出处（O3），不是 N_Q；`|C/Q|≤B` 且 N_Q=N0 时只有有限多既约分数；“三个缺失事实”指代不明。最后一句正确 |
| 23 | L115–119 | 11,164 a 步检查、256 gateway 检查、33 size 检查全 PASS | [B] | 是 | 工作流输出与 JSON 一致；检查范围是代数控制，j≤64 的 a 检查远低于 N_Q |
| 24 | L120–122 | 检查不是 canonical reachability/着陆证书；全 j 的 size 结论靠 §2 的解析不等式而非外推 | [A] | 是 | 与 §2 的范围一致（但 §2 的“全 j”是 j≥N_Q） |

---

## 3. 错误清单（行号 + 严重度 + 修正）

### E1 [major] L28–L31：`permitted` 未定义，高度界缺关键假设

- 问题：`after t permitted steps |C_t|/Q <= A+t` 中的 “permitted” 在全文没有定义。该不等式只在每一步的 b/c 增量 `Φ−2` 满足 `|Φ−2|≤1` 时成立（a 步为反射，不增；c3/AA/BA 分别给 0/−1/+1；b 步给 −1）。对 ε≥7 的 c 步（例如 BBBAA 的来源移位 +4/3），每步可增加 4/3，`A+t` 失效。
- 修正：明确写 `permitted = {a 步, b 步, Φ∈{1,2,3} 的 c 步}`（等价于 `|Φ−2|≤1`），并说明 ε≥7 的 c 步不在高度递推内、只能由 §2 的“降到 N_Q 以下”条件处理（或显式保留 `A+Σ|Φ_s−2|` 的高度账）。

### E2 [major] L61–L68：主引理的假设清单不完整

- 问题：引理的结论是在若干未写出的前提下才成立：
  1. **固定 Q、无 gateway**：前缀内不得发生参数五的 gateway（否则 Q 变、`N_Q` 变、`A` 重置）；
  2. **续走的 c 步只有 ε∈{3,5}**：这依赖已接受的 weight grammar（ε 为奇数 ≥3；AA/BA 是仅有的 ε=5），文档未引用；
  3. **defined prefix**：需要 F 定义到所读的每个 `τ(n)`（PROOF_EXT 的 standing hypothesis）；文档未提；
  4. **记录预算**：若结论要用于 S(J)，进入时的记录 `R_0` 必须 ≤ J（并且 gateway 会把记录抬高 `m−4`），文档未写；
  5. **A 的来源性**：`A=max(|C_0/Q|,|3−C_0/Q|)` 是所选有理解释的性质，不是相位类 `(j,θ)` 的函数；需要从实际 affine 来源/上游 gateway 提供。
- 修正：把这五条全部写进引理；第 2 条引 accepted grammar，第 3 条引 PROOF_EXT，第 4/5 条明确标为 open（记录预算、来源高度）。

### E3 [major] L61–L62、L99–L102：只降到 `N_Q`，残留带 [N0, N_Q) 未处理

- 问题：`h_Q(q)` 的目标是 `N_Q=max(N0,4(d+2))`，不是 N0。当 `Q>2^{N0/4−2}` 时 `N_Q>N0`：走法只被证明降到 `j<N_Q`，可以停在 `[N0,N_Q)` 内；这一段既不在已接受窗口证书（只覆盖 `j<2·10^7=N0`）内，也没有本文的其他论证。`§4` 的 “handles the large-parameter part of every odd-denominator mode” 会被读成覆盖所有大 j，实际只覆盖 `j≥N_Q`。
- 定量证据（scratch 3，精确整数）：`r=10^7`（Q=3^{10^7}）时 `d=15,849,626`、`N_Q=63,398,512`，而 `Q(κ+B)<2^{j−2}` 实际只在 `j≥25,849,628` 成立；因此 `[20,000,000, 25,849,628)` 是真正的未覆盖带（宽 5,849,628）。`r=7·10^6` 起已有非空带。
- 修正：把结论写成“降到 `N_Q`，且 `[N0,N_Q)` 是 open 带”；或把阈值改进到 `≈log2 Q + log2(κ+h) + 2`（h 为实际高度，见 E5），并仍为 `[N0, threshold)` 单独给引理。

### E4 [major] L61–L68、L99–L102：没有 J 依赖分析（log*、T_h、记录预算）

- 问题：全文不出现 J、log*、T_h、窗口、记录预算。`h_Q(q)` 只是抽象定义，没有给出 `h_Q(q)` 与 q（≤J）的关系；`RATIONAL_MODE.md` 对分母 3 给出了显式 tower（`U_1=2^{(N0−5)/2}, U_{r+1}=2^{(U_r−5)/2}, h_3(q)≤r for q<U_r`），本文没有对应物。也没有 `N_Q≤J` 与 `h_Q≤J−R_0` 的检查。
- 修正：补一条与 RATIONAL_MODE §2 平行的 tower 估计（把 Q 通过 d=ceil(log2 Q) 进入常数），并写出用于 S(J) 时的两条预算不等式：`N_Q≤J`、`h_Q(q)≤J−R_0`；若做不到，明确写“本引理只给出逐段结论，J 依赖留给记录/来源预算”。

### E5 [major] L37–L48、L50：高度上界取 B=2^{10^7}，而不是实际有理高度 h

- 问题：引理假设 `|C/Q|≤B`，并把 `Q(κ+B)` 作为 a 分子上界。但本文件 §3 自己给出 gateway 后的高度 `≤5+h/3`（极限 7.5）；O1 的轨道高度 |eta_r|≤5；BBBAA 的高度 2。任务关心的正是“高度≤h”的有界位移。用 B 代替 h 使阈值 `N_Q` 多出约 `N0/2` 位：O1 的 `r=6.573e14` 给 `N_Q=4.167e15`，而其首个输出的参数下界 `m≥1.052e15<N_Q`（比值 ≈3.96），所以引理在 O1 的参数上根本不适用；若用实际 h≤5，size 条件只是 `Q(κ+h)<2^{j−2}`，阈值约 `log2 Q+O(log N0)`，m 会落在覆盖范围内。
- 修正：把引理按一般高度 h 陈述（h 是参数，不是 B），并显式把 §3 的 `h→5+h/3` 与 §2 的 `A+h_Q≤B` 合并成一个跨 gateway 的归纳；至少注明“用 B 是保守的，O1 参数落在 N_Q 之外”。

### E6 [minor] L41–L44：单调性理由的比值/常数不对齐

- 问题：`2·j^4/(j+1)^4>1 for j>=6` 对应的是 `2^{j/2}` 与 `j²` 的比较；要延续 `(3/2)(j−1)²<2^{j/2}`，正确的逐步比值是 `√2·(j/(j−1))²>1 ⇔ j≥7`，且 3/2 的常数没有在理由中处理。
- 修正：写成“在 N0 处 `(3/2)(j−1)²<2^{j/2}` 成立；此后 `2^{j/2}/((3/2)(j−1)²)` 的比值为 `√2·(j/(j−1))²>1`（j≥7），故持续”。结论不变（N0≫7）。

### E7 [minor] L72–L75：gateway 恒等式只对参数五的 k=1 a 步成立，前提未写

- 问题：`3D'=15−D−y` 在一般 a 步是 `3D'=9+6k−D−y`；只有 k=1（参数五读 X(4)）才是 15。文档没有说 X(4) 是奇 a 型；若参数五的链会走 b/c，公式不成立。
- 修正：写明 “X(4) 为奇 a 型、τ(4)=2、k=1，故每条参数五的链都走此 a 步”，并把该映射称为 a-gateway。

### E8 [minor] L89–L95：`c` 未定义；c_0=5 是 Q=1 边界；映射是 gateway 后接反射

- 问题：`c` 第一次出现且无定义（应说明 `c=C/Q`）；`c→(c−6)/3` 的复合是 gateway `c→5−c/3` 再反射 `3−·`，不是单步 “a descent”；c_0=5 对应 Q=1（§1 要求 Q>1），且 “Q=3^r 必翻三倍” 在 r=0 不普遍成立（C=5 恰好成立）。
- 修正：定义 c；写出两步复合；注明 c_0=5 是 Q=1 的边界，结论只作一致性检查。

### E9 [minor] L104–L106：“Even while N_Q=N0, infinitely many distinct rational residues arise” 为假

- 问题：若 `N_Q=N0`，则 `d≤N0/4−2`，即 `Q<2^{N0/4−2}`；又 `|C/Q|≤B` 给 `|C|≤BQ`。因此既约分数 `C/Q` 只有有限多个（每个 Q 有限、Q 有限）。这句话按字面是假的。
- 修正：改成“Q 本身无界，故来源/分母空间无限”，或“对无界的 j，类 `mod 2^j` 有无穷多”，不要写 “while N_Q=N0”。

### E10 [minor] L104–L105：有限着陆证书不够的理由与 N_Q 是两件事

- 问题：“a fixed finite landing certificate is still insufficient: N_Q increases with log2 Q” 把 size 阈值与着陆证书混在一起。着陆证书不够的真原因是：有界高度有理位移会把 δ 移出固定窗口 `[−12,15]`（例如 +4/3 的 BBBAA），且提升位/出处不由类单独决定（O3）；N_Q 增长只是导致着陆参数可能落在 `[N0,N_Q)`（即 E3 的带）。
- 修正：把两个理由分开写：窗口外的 δ/出处（O3）与带内着陆（N_Q）。

### E11 [minor] L3–L5、L15–L68：没有 [A]/[B]/[C] 标注与完整假设清单

- 问题：项目标准要求每条结论要么有完整假设清单与证明，要么标 [B] 并写范围，要么标 [C]。本文 122 行没有一处 [A]/[B]/[C]；§2 的主引理只有一句 “Induct ... as in RATIONAL_MODE”。
- 修正：给每条结论加标注；把 §2 的归纳（高度与收缩同时归纳、每步记录下降、高亏损 c 出口）写成完整证明或明确归入 [A-cond]。

---

## 4. 尺度/参数依赖（N0、窗口、T_h、log* J、参数上界）

| 行号 | 依赖 | 说明 |
|---|---|---|
| L37 | N0=20,000,000；B=2^{N0/2}=2^{10^7} | 深段常数；`2*10^7` 以 `20,000,000` 出现 |
| L39 | d=ceil(log2 Q)，N_Q=max(N0,4(d+2)) | 阈值随 Q 变；`Q>2^{N0/4−2}≈2^{5·10^6}` 时 N_Q>N0 |
| L41–44 | j≥N0；P_clock(j−1)≤j−1；κ<2^{j/2} | 全部依赖 N0 |
| L45–48 | j≥N_Q | 依赖 N0 与 d |
| L50–53 | |C|/Q≤B | 依赖 N0（B=2^{10^7}） |
| L55–59 | L_Q、h_Q、N_Q | 无 T_h、无 log* J、无窗口 |
| L61–68 | q≥N_Q；h_Q(q) | 抽象；没有 `N_Q≤J`、`h_Q≤J−R_0` |
| L84–87 | m<H | H 是祖先精度（precision provenance），未与 σ 关联 |
| L100–102 | “large-parameter part”=j≥N_Q | N_Q 随 log2 Q 增长；残留带 [N0,N_Q) |
| L118 | N0 | size 检查的阈值 |

明确未出现（本文件不依赖）：窗口 `[−12,15]`、`j<2·10^7` 的证书、`T_h`、`log* J`、`T_4/T_13`。这本身是发现：任务要求说明每部分对 J 的依赖，而文档完全没有 J 维度的分析（见 E4）。

**O1 的定量对接**（scratch 3，精确整数）：

- O1：`r≥657,306,078,883,964`，`σ=1,051,689,726,214,394`，`eta_r=-5+8/3^r`，|eta_r|≤5。
- `d=ceil(r log2 3)=1,041,805,486,527,146`；`N_Q=4,167,221,946,108,592`。
- 首个输出参数 `m=4+v2(y_r)≥σ−1=1,051,689,726,214,393`。
- 结论：`m<N_Q`（比值 ≈3.96），所以 §2 的引理对 O1 的源（P=49）和输出（m≈1.05e15）都不适用；O1 的失败发生在进入 m 的那一步（记录 ≥σ），而 §3 只是把该轨道重新算出来作为一致性检查，没有关联 r 与 σ，也没有排除危险剩余类。O1 未被正面处理（文档也明说“not a claim to have removed the obstruction”）。

---

## 5. 三份障碍的正面处理评估

- **O1（ORBIT_SHIFT_OBSTRUCTION）**：未处理。§3 仅复现 `c_r=-3+8/3^r` 并承认它；没有给出 `r` 与祖先精度 σ 的关系，也没有排除危险剩余类。定量上，O1 的 m 落在文档的 N_Q 之外（见上），所以 §2 的收缩引理对它无效。文档的诚实声明（L94–95）成立，但任务的“必须正面处理”未被满足。
- **O2（STOP_CHECKPOINT：affine 来源、`v2(beta')<J−Γ−1`）**：未处理/未提及。文档的 `A+h_Q(q)≤B` 是高度条件，不是 affine 来源判据；全文没有 `x=A·U+beta, Θ=2^J U+3d+1, v2(A)=J−Γ`。§4 的“record budget must survive repeated gateways”只是定性承认，没有 O2 的判据形式。所需附加条件应写成：在 gateway 处保留实际 affine 来源并检查 `v2(beta')<J−Γ−1`；文档没有这样做。
- **O3（OPTIMAL_PHASE_ENCODING：局部相位类不够）**：部分承认（L107 “Bare ties require actual precision provenance”），但没有给出实际的来源/相位限制；`A` 的来源性也没有说明。文档正确地没有声称用有限扫描解决，但没有把 O3 的条件写成可检验的形式。

---

## 6. 与任务目标的对齐

任务目标：给 c/a/b 着陆建立与尺度无关的符号论证；对输入相位 `θ+s`（`s∈Z[1/3]`，高度≤h），着陆类可认证，或经有限步 gateway 化解且每步记录严格下降，界不依赖 J。

文档的实际成果：

1. §1 给出奇分母有理解释的精确 a/b/c 递推（正确，已独立复核）——这是可复用的工具。
2. §2 给出 Q-自适应的 size/收缩引理：在 `j≥N_Q`、高度≤B、高亏损 c 出 N_Q 的条件下，降到 `N_Q` 且每条记录严格下降（正确，假设不完整）。
3. §3 给出参数五 a-gateway 的精确有理映射与高度压缩（正确，已独立复核），并把它与已接受的 3-adic 轨道对齐。
4. §4 诚实列出未证事项（有限证书、裸 tie 出处、记录预算），明确不声称解决着陆或全局 EXT。

**没有达到目标的部分**：没有着陆类的可认证判据；没有“有限步 gateway 化解且每步记录严格下降”的定理（gateway 本身会把记录抬高 `m−4`，文档也没有给出跨 gateway 的记账）；界仍依赖 Q（`N_Q`），且对深分母留下 `[N0,N_Q)` 带；没有 J 维度（log*/T_h/记录预算）的说明；O1/O2/O3 均未正面处理。因此文档是一个**正确但局部的中间引理**，不是本轮目标所要求的尺度无关符号论证。

---

## 7. 总评

`ODD_DENOMINATOR.md` 的核心代数是对的：§1 的 a 步与 b/c 步递推（含提升位与 `mod 2^{j+1}` 精度）、§2 的 size 链、§3 的参数五 a-gateway 恒等式与分母结论，都经我独立计算复核通过，且与 RATIONAL_MODE、C5_EXTENSION、ORBIT_SHIFT 的已接受结论一致。文档最可贵的是诚实：它明确说自己不解决着陆、不解决 HR5、不与有限生成元障碍矛盾。

但它没有完成本轮任务：`permitted` 未定义、主引理假设不全、结论停在 Q 依赖的 `N_Q`（深分母留下未覆盖带 `[N0,N_Q)`）、完全没有 J 依赖与记录预算/tower 分析，并且 O1/O2/O3 都只是被承认而非被处理。§4 的 “handles the large-parameter part of every odd-denominator mode” 与 “infinitely many distinct rational residues” 两句需要收窄/修正。建议按 E1–E5 重写引理假设与范围，并按 E9/E10 修正 §4 的两句；在此之前，本文的结论只能作为 [A-cond] 的局部工具使用，不能作为着陆或尺度无关下降的证据。

**未证明全局 EXT；未改变 K_clock；本审阅未做 canonical reachability 声明。**
