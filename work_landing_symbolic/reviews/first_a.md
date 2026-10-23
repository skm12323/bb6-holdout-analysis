# 审阅报告：work_c3_drift/FIRST_A_REDUCTION.md

- 审阅对象：`work_c3_drift/FIRST_A_REDUCTION.md`（2026-10-20，**UNREVIEWED**；本轮四份未审文档之一），全文 169 行。
- 审阅日期：2026-10-23。审阅人：子代理 `审阅者-first-a`。
- 背景已读：`CHECKPOINT_1RB1LA_0RC0RD.md` L614–681；`reviews/c3_drift_review_record.md` 全文；
  `work_r1r2/NOTES.md` §0–5（含 §6 数据与 §7 状态）；`work_claude_shifted/NOTES.md` §1–5（含 §6–8）；
  `work_global_ext/PROOF_EXT.md` §0–4（§2 为 walk 规则/HP/AB/RB）；`work_c3_drift/C5_EXTENSION.md` §1–4；
  `work_c3_drift/CONGRUENCE_TARGET_NOTE.md` §0–5；三份障碍 `ORBIT_SHIFT_OBSTRUCTION.md`、
  `STOP_CHECKPOINT_2026_10_21.md`、`OPTIMAL_PHASE_ENCODING.md`；另读 `work_c3_drift/SHIFT_TRANSPORT.md`、
  `work_c3_drift/TARGETED_PRECISION.md`、`work_ext_roots/PROOF_A_SOURCE_DESCENT.md` §1–2、
  `work_ext_roots/PROOF_EXT_ROOTS.md` §1、`work_global_calendar/calendar_oracle.py`、`work_c3_drift/verify_first_a.py`
  与 `work_c3_drift/first_a_checks.json`。

**总判断（先给结论）**：§1–§3 的首次 a-步归约在代数上是正确的，且确实不依赖 J、N0、2·10^7、窗口 [−12,15]、
T_h 或 log* J；它把 |η|≤8 的整数移位安全性精确化为一个"真实终链碰撞"余项。但该余项没有被关闭，
文档自己也如实说明（L6–7、L112–115）。因此本文是**尺度无关的条件归约**，不是尺度无关的着陆证明；
它也不声称全局 EXT。发现的问题均为 minor（未列假设与措辞），无 critical/major 代数错误。

---

## 1. 验证命令与输出

### 1.1 文档自带验证器（工作流已运行一次；本次**没有**重跑）

- 命令：`python -B work_c3_drift/verify_first_a.py`
- 工作流记录：`exit 0`；输出
  `{"status": "PASS", "review_status": "unreviewed", "source_P": [5, 256], "shifts": [-8, 8], "cases": 5712,`
  `"counts": {"valuation_mismatch_closes": 852, "collision_end": 492, "zero_shift": 336, "no_A": 4032},`
  `"collision_certificates": {"minimal_class_end": 488, "minimal_class_ceili...}, ...}`
- 我读取了该次运行写出的工件 `work_c3_drift/first_a_checks.json`（mtime 2026-10-23 00:42），其中：
  `counts` 同上；`collision_certificates = {"minimal_class_end": 488, "minimal_class_ceiling": 4}`；
  `max_extra_bits = 3`；`extra_precision_examples` 共 4 条（P=17/90/161/234，全部 η=−3，(j,δ)=(5,5)，
  K=8/7/9/7，x 残基=32/96/416/96，Θ 残基=37/101/421/101，词=5,6,1 / 5,5,1 / 5,7 / 5,5,1）。
- 说明：按任务要求未重跑同一脚本；下述"逐条"中引用的 [B] 计数均来自这次运行及其 json，而不是我本次的执行。

### 1.2 审阅者临时脚本（只写在 `work_landing_symbolic/reviews/scratch/`）

1. `python -B work_landing_symbolic/reviews/scratch/check_first_a_constants2.py`（输出 `check_first_a_constants2.json`）
   独立重建 336 个源（252 个 fire 源 + 84 个 c 源），求每个源的首个 a-步并检查 §2 的常数：
   ```
   min_state_time = 52        (Theta_A=3 s_A+5; s_A 的最小值)
   min_y = 248                (y=2Theta_A+3tau(m-1)-x_A/2)
   min_y_shifted = 232        (y+2eta, eta∈[-8,8]\{0})
   min_m = 5                  (首个 a-步链参数)
   min_slack_6sA5_minus_xA = 157
   collision_qdist = {"1":448, "2":4, "3":28, "4":12}   (合计 492)
   n_bad = 0
   base_odd_0_3 = [False, False, False, False]
   ```
   （第一版 `check_first_a_constants.py` 把 s_A 误取成"被读交叉 X(m−1) 的时刻"，因此报出 84 条 "const" 违规；
   那是审阅者的变量定义错误，不是文档错误。真实状态下 `Theta_A=3 s_A+5` 中的 s_A 是状态自身时刻；
   修正后 n_bad=0。）
2. `python -B work_landing_symbolic/reviews/scratch/check_lambda_nonneg.py`
   在 Calendar(512) 的 n∈[0,4000) 全部交叉上检查质量部分：`n_neg=0`（head_lambda、tail_lambda 均非负）；
   `n_time5=0`（没有 time=5 的奇交叉）。这支持 §2 使用的 λ_Y≥0，但只是有限范围。
3. `python -B work_landing_symbolic/reviews/scratch/check_q_min.py`
   - `cal.crossing(-1)` 抛 `KeyError -1`（即 j=0 的"交叉 X(−1)"在本模型中不存在）；
   - 84 个首 a-步的 `q=v2(y)` 最小值 = 1，q 取值集合 {1,2,3,4,5,6,7,9}；
   - 336 个真实 walk 中链参数最小值 = 1。
   这对应 §2 中"参数 ≤4 的返回为偶"应写成 1≤j≤4 的小问题。

---

## 2. 逐条结论表（行号为文件实际行号）

| # | 行号 | 结论（一句话） | 标签 | 判定 | 说明 |
|---|---|---|---|---|---|
| 1 | L11–L22 | §1 输入设定：真实链 C 的真实尾由 S1 给出 j_t+G_t<σ（严格），移位态 (x,Θ+η) 取同一精度 σ，η∈{−8,…,8}；覆盖 θ∈[−2,4] 的 η=θ−2。 | [A]（条件：真实尾输入） | 正确 | G 从 C 起算，等价于 S1 的 j_t+Γ_t<σ_C；η=θ−2∈[−4,2]⊂[−8,8]。 |
| 2 | L24–L31 | 首个奇 a 返回之前，b/c 步不读 Θ（x′=c′_W u+λ′_W），移位链与真实链的 x、参数、类型、损失逐链相同且相位差恒为 η；若无 a 步则两链同时终止。 | [A] | 正确 | 天花板判据 j+loss 也相同；无精度近似。 |
| 3 | L33–L42 | 首次 a 步输出恒等式 y_η=y+2η、T_η=T+η；剩余精度 σ−G−1；移位安全性 ⇔ 该显式余项终止且所有相对记录 <σ−G−1。 | [A] | 正确 | 需 y_η≠0；正性由 §2 提供。 |
| 4 | L46–L53 | 正性与常数：x_A≥32、s_A≥5、s′=s_A+1+τ(m−1)≥8、y=3s′+4+λ_Y≥28、y+2η≥12>0。 | [A]（需 λ_Y≥0） | 基本正确，依据需补 | 见错误 E1：L49 提到 "nonnegative lambda mass"，但 L52 把它用于**新**交叉的 λ_Y 时未明说、该非负性也未证明；再者由 L49 自己的 x_A≤6s_A+5 只能得 y≥25、y+2η≥9>0，仍足以保证正性。 |
| 5 | L55–L62 | 估值二分：若 q≠h（h=v2(2η)∈{1,2,3,4}）则 v2(y_η)=min(q,h)≤4，移位链在下一链终止，记录 ≤q+G+1<σ。 | [A] | 正确 | 需 q≥1、参数≥1（见 E2）。 |
| 6 | L64–L66 | 该论证不替换物理 ceiling、不需 DH/DH_out、不对 m 的大小作假设；唯一剩余情形是等估值。 | [A] | 正确 | 与 work_claude_ext_next §6 OB 的 DH_out 相比确实省掉。 |
| 7 | L68–L76 | 等估值 q=h≤4 ⇒ 真实尾在该 a 输出终止；剩余任务精确为 (y+2η,T+η) 在 ceiling σ−G−1 的余项，记 TERMINAL-COLLISION。 | [A] | 正确 | q≤4 ⇒ X(q−1) 为偶（规范小基 X(0..3) 偶）。 |
| 8 | L78–L81 | 该余项带真实终链来源与原始物理精度，强于任意 G_δ/H_δ 状态。 | [A] | 正确 | 来源条件确实是"到达的真实终链"，不是任意相位类。 |
| 9 | L83–L90 | 碰撞表：η 奇 → q=1；η=±2,±6 → q=2；η=±4 → q=3；η=±8 → q=4。 | [A] | 正确 | v2(2η) 分别为 1,2,3,4。 |
| 10 | L92–L95 | 真实 S1 对终止后的移位后缀没有任何信息；这是真实的剩余义务。 | [A] | 正确 | 与接受框架一致。 |
| 11 | L99–L104 | §4：SHIFT_TRANSPORT 把 A-初始 c 源归约到更早的真实链且 η 不变；漂移∈[−2,4] 时终端义务可用 EXACT 分析。 | [C]（依赖未审的 SHIFT_TRANSPORT） | 条件成立，措辞需限定 | 见 E5：SHIFT_TRANSPORT 自身未审，且其第一 A 输出族在原文用 (z,z+2+η) 参考表述。 |
| 12 | L106–L110 | η=−1 复现已接受的 outer-b 停止二分；其余 |η|≤8 得到类似二分；避免 DH_out；保留精确余项和物理 ceiling 是必要的。 | [A] | 正确 | 与 OB 的步骤 1–4 对照一致（OB 的残余步 4 仍开，本文只做二分）。 |
| 13 | L112–L115 | 剩余工作：TERMINAL-COLLISION 的统一记录界、范围外移位、更高尺度条件；K_clock 与全局开放状态不变。 | [C] 范围声明 | 如实、正确 | 没有把未证分支写成已证。 |
| 14 | L119–L123 | 验证器用 Calendar(512)，对 5≤P≤256 的规范 fire 及其 epoch 的全部奇 c 交叉取源：336 个真实源链、5712 个源/移位对。 | [B] | 正确 | 我独立重建：252 fires + 84 c 源 = 336；5712=336×17。 |
| 15 | L125–L135 | [B] 计数：336 零移位、4032 无 a 步、852 估值不匹配在下一链终止、492 碰撞在剩余精度内终止；明确 492 个成功不外推到所有碰撞；移位相位是反事实的。 | [B] | 正确 | 与 `first_a_checks.json` 一致；我另验了 84 个首 a-步的估值二分（n_bad=0）。 |
| 16 | L137–L143 | [B] 最小类证书：492 个中 488 个从 (2^j,2^j+δ) 在精度 j+1 下终止且记录≤j；4 个失败且全为 (j,δ)=(5,5)。 | [B] | 正确 | json: minimal_class_end=488, minimal_class_ceiling=4。 |
| 17 | L144–L150 | 对每个实际终止后缀取 K=R+1（R 为最大相对记录），则 (x mod 2^K, Θ mod 2^K) 由 HP 证明整条同余柱体；验证器用带符号整数重演且 K≤可用精度。 | [A] 论证 + [B] 检查 | 正确 | HP 需 x*≠0 且记录<K；K=R+1 满足；实际 K≤σ−G−1 先验成立。 |
| 18 | L152–L159 | 四个例外：(P,η,K,x,Θ,词)=(17,−3,8,32,37,5,6,1)、(90,−3,7,96,101,5,5,1)、(161,−3,9,416,421,5,7)、(234,−3,7,96,101,5,5,1)。 | [B] | 正确 | 与 json 完全一致。 |
| 19 | L161–L168 | "1–3 个额外位"只是有限观察，不是普适界；TARGETED_PRECISION 有 252 额外位的构造并由 gateway 族安全关闭；保留完整残基。 | [B]+[C] | 基本正确 | 见 E4；另注意 TARGETED_PRECISION.md 自身也是未审文件，这里只是交叉引用，不是本文的证明成分。 |
| 20 | L3–L7 | 本文不证明残余分支、不证明全局 EXT、不改变 K_clock。 | [C] 范围声明 | 正确 | 与 L112–115 一致。 |

---

## 3. 错误清单（行号 + 严重度 + 修正）

| # | 行号 | 严重度 | 问题 | 修正 |
|---|---|---|---|---|
| E1 | L52 | minor | `y=3*s'+4+lambda_Y>=28` 需要 λ_Y≥0（新状态所在交叉的质量部分非负）。L49 的 "nonnegative lambda mass" 是在 x_A 的不等式里提到的，L52 未说明它对**新交叉**同样适用，该非负性本身也没有证明/引用；只按 L49 的 x_A≤6s_A+5 推不出 28（可得 y≥3s_A+7.5+τ≥25，进而 y+2η≥9>0）。结论"正性"仍成立，但所写常数 28/12 缺一步依据。 | 明确写出并引用：规范交叉质量分解 λ_A+λ_Y=3s+1 的两部分非负（[A-imp] 或 [B]；本次在 n<4000 内 0 反例），故新交叉亦有 y≥3s′+4≥28；或把常数改为 y≥25、y+2η≥9。 |
| E2 | L59 | minor | "All parameters <=4 have even returns" 中 j=0 未定义：本模型没有 X(−1)，`Calendar.crossing(-1)` 在本次复算中抛 `KeyError`。该句要成立须有 q≥1（即到达链的参数≥1）。 | 改为 "1≤j≤4"，并补一句：到达链的参数≥1（故 q=v2(y)≥1；本次 84 个首 a-步 min q=1）。 |
| E3 | L102–L103 | minor | "The only positive-output obstruction" 与 §2 已证的正性矛盾——移位输出恒有 y+2η≥12>0；真正的剩余障碍是**高估值**（等估值 q=h 后的碰撞）。 | 改为 "the only remaining obstruction is the equal-valuation (terminal-collision) branch"。 |
| E4 | L166–L168 | minor | "these four states … their different continuations" 不准确：P=90 与 P=234 的 (K,x mod 2^K,Θ mod 2^K,词) 完全相同（7,96,101,(5,5,1)）；四个状态只有 3 个不同残基类/3 个不同词。"保留完整残基"无法区分这两个源，区分它们需要 K 以上的实际状态。 | 改为："三种不同后续，其中两个源共享一种；完整 K-残基只区分到 3 类"。 |
| E5 | L99–L101 | minor | "SHIFT_TRANSPORT reduces later A-initial c sources to earlier real chains" 依赖未审的 `SHIFT_TRANSPORT.md`；其 §4 把"第一 A 输出"族用 (z,z+2+η) 参考（精度 P−1）表述，而该族是否就是本文意义下的真实链、其真实尾是否可用，文中没有逐族说明。 | 逐族注明终端对象是真实链（真实 fire / 真实 a-输出 / 真实 c 源），并把该应用句明确标为依赖未审文件的 [C] 条件陈述；若第一 A 输出族按 SHIFT_TRANSPORT 的参考表述处理，则 §1 的"真实尾"假设不适用，需另写。 |
| E6 | 全文 | minor | 没有任何 [A]/[B]/[C] 标注（项目标准要求每条实质结论带标签，且未证内容不得写成 [A]）。 | 按上表补标签；§5–§6 的有限检查标 [B]，§4 的应用句标 [C]，§1–§3 标 [A]（条件列全）。 |
| E7 | L4–L5 | minor | "the shift range needed by the current Lambda<=4 drift argument"：Λ≤4 漂移中 ε∈{3,5} 的 c 步只产生整数移位 {0,±1}（ε=3/AA/BA），a 步为 θ↦3−θ、b 步为 θ↦θ−1；本文覆盖 [−8,8] 的整数，但不覆盖 BBBAA 的 +4/3（有理移位），也不覆盖 O1 的 η_r。文中 L112 只笼统写 "outside this bounded range"。 | 明确说明：Λ≤4 漂移所需是整数移位；有理移位（O1、BBBAA）不在本引理范围，需 RATIONAL_MODE/ODD_DENOMINATOR 型处理。 |

（其余小问题写入 §5–§6 的备注：如 L38–L42 的 "equivalent" 只在真实段安全假设下成立；L11–L13 的 S1 形式是相对 epoch 的、对内部链 C 应写成 j_t+(Γ_t−Γ_C)<σ_C。这两点在文中语义上已隐含，不算错误。）

---

## 4. 范围与尺度依赖（按行号）

**文中出现依赖的位置：**

- **L4–L5**：`current Lambda<=4 drift argument` —— 依赖 work_deep/work_r1r2 的 T₄（Λ≤4）区间与 K_clock⊂[K_clock,T₄) 的已接受归约；本文的"适用性"说法以此为前提。
- **L17**：`eta in {-8,...,8}` —— 显式参数范围；也是本文对有理移位（Z[1/3]）的门槛。
- **L115**：`The accepted K_clock horizon and global open status are unchanged` —— 提到 K_clock（未改变）。
- **L119–L123、L133**：[B] 的有限范围 P∈[5,256]、Calendar(512)；不是尺度统一结论，文中已写 "finite selection"。
- **L163–L165**：TARGETED_PRECISION 的 252 额外位（m≤256）与 gateway 族（5≤m<10^8，[B]）；这里出现一个参数上界 10^8，但它是被引用的已接受证书范围，**没有**被用来声称统一结论。

**文中不出现（这点是优点）：** N0=2·10^7、2·10^7、j<2·10^7、窗口 [−12,15]、T_h、log* J、T_4 的具体数值。
§1–§3 的符号论证对 J 完全一致，不依赖任何有限窗口。

**需要注意的隐含范围：**

- L46–L53 的 §2 用 "canonical small base"（X(0..3) 偶）与质量部分非负；前者是固定机器基的 [B] 事实，后者是规范质量分解的结构事实（本次 n<4000 内 0 反例）。
- L99–L104 的 Λ≤4 适用性还需要"incoming theta 有界"与"真实尾输入"；文档 L19–L22 已声明这两点是未来证明的义务，但 §4 的措辞比 L19–L22 更肯定。

---

## 5. 与三份障碍及本轮目标的关系

- **O1（ORBIT_SHIFT_OBSTRUCTION）**：O1 的 η_r=−5+8/3^r 是**有理**移位，v2(η_r)=0、实数高度 ≤5；本文只处理整数 |η|≤8，明确指出 "control incoming shifts outside this bounded range" 是剩余（L112–113）。因此本文**没有**重复 "所有有界高度位移都安全" 这个已被 O1 否定的目标；它恰好在等估值分支里保留了"移位输出记录可能达到 σ"的现象。O1 要求的"实际分母深度 r 与祖先精度 σ 关联，或排除危险剩余类"本文完全没触及。
- **O2（STOP_CHECKPOINT_2026_10_21）**：O2 要求保留实际仿射来源 x=A·U+β、Θ=2^J U+3d+1 与 v2(β′)<J−Γ−1 判据；本文保留的是显式整数余项 (y+2η,T+η) 与物理 ceiling，而不是仿射 β 判据。两者精神一致（都不把来源简化为局部相位类），但本文没有把 TERMINAL-COLLISION 写成 β 判据，也没有处理任意小 gateway 的局部闭合。
- **O3（OPTIMAL_PHASE_ENCODING）**：O3 说明"局部相位类 + 预留 S 位"不能覆盖所有类；本文不枚举相位类，直接保留完整状态/残基，因此与 O3 的教训一致。§6 的 K-柱体正是"用实际来源的额外位"而不是扩大有限类表。
- **本轮目标**：目标是"c/a/b 着陆的尺度无关符号论证：着陆类可认证，或经有限步 gateway 化解且每步记录严格下降，界不依赖 J；若做不到，精确写出所需附加条件，必须是来源/相位条件，不能是参数上界"。本文给出的是一条尺度无关的**归约**（[A]），并把剩余写成 "reachable TERMINAL-COLLISION states 的统一记录界"（L112–113）——这是一个**来源/相位条件**（真实终链、q=h≤4、实际 y 的高位），不是参数上界。就此而言它符合"做不到时精确写出附加条件"的格式；但该条件尚未被证明可统一成立，相当于把问题缩小到 q∈{1,2,3,4} 的真实终链，而不是解决它。本文没有、也不声称完成本轮目标。

---

## 6. 总评

1. **代数正确性**：§1–§3 的核心恒等式（y_η=y+2η、T_η=T+η、剩余精度 σ−G−1、q≠h⇒min(q,h)≤4、q=h⇒真实尾终止）逐条可验，且与 first_a_checks.json 的分类计数一致；我的独立复算在 336 个源/84 个首 a-步上没有发现代数反例。§6 的 K-柱体论证符合 HP 的精度形式（K=R+1，x≡2^j mod 2^{j+1} 的方式正确）。
   **精度位核对**：最小类用 δ=(T_η−y_η) mod 2^{j+1} 与代表元 (2^j,2^j+δ)（精度 j+1）匹配，x≡2^j mod 2^{j+1} 成立（v2(y_η)=j），未见 mod 2^j/2^{j+1} 混用；K-柱体要求 x、Θ 各 K 位，正是 HP 的 min(v2 δΘ,v2 δx)≥K，且 K=R+1 保证记录 <K。lifting bit（claude_shifted Cor 1.4 的 δ+2^j 情形）在四例 (5,5) 上由取 K>j+1 的实际残基规避；这与已接受窗口 (5,5) 为裸 tie 的事实一致，不是错误。
2. **未列假设**：λ_Y≥0（质量部分非负）与 q≥1/参数≥1 是两处应写而未写的结构性前提；它们不改变结论（正性仍成立、数据无 q=0），但按本项目的标准应补。
3. **范围**：整数 |η|≤8，真实链、完整真实尾；不含有理移位（O1/BBBAA）、不含 SHIFT_TRANSPORT 的完整终端族论证、不含 Λ≤4 漂移的 incoming-θ 证明。§4 的 "SHIFT_TRANSPORT reduces … to earlier real chains" 依赖未审文件，应以 [C] 记载。
4. **与已接受结论的关系**：本文不引用 CAL-C/R1/H3（它们已被否定为统一目标），也不引用窗口 [−12,15] 作为关闭手段；§6 只用实际残基 + HP。这一点符合"不能用参数上界型条件当统一目标"的要求。
5. **判定**：作为**条件归约**接受为 [A]（列出上述假设后）；作为**着陆证明**不成立——TERMINAL-COLLISION 分支仍开，文中已如实说明。没有全局 EXT 声明，没有改变 K_clock。

---

## 7. 复现

```
# 文档自带验证器（本次未重跑；工作流已运行一次，exit 0, PASS）
python -B work_c3_drift/verify_first_a.py

# 审阅者临时检查（只写 work_landing_symbolic/）
python -B work_landing_symbolic/reviews/scratch/check_first_a_constants2.py
python -B work_landing_symbolic/reviews/scratch/check_lambda_nonneg.py
python -B work_landing_symbolic/reviews/scratch/check_q_min.py
```

输出 json：`work_landing_symbolic/reviews/scratch/check_first_a_constants2.json`（修正版）、
`check_first_a_constants.json`（第一版，含审阅者变量定义错误，保留以备核对）。
未修改 `work_c3_drift/` 或其他目录的任何文件；未 git 提交；未声称全局 EXT。
