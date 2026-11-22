# 攻击员审查：work_mixed_bridge（混合块桥定理与全局 strict-EXT 装配，PROOF.md + SMALL_BASE.md）

审查人：攻击员（ZCode GLM 5.3），2026-11-22。对象：work_mixed_bridge/PROOF.md、SMALL_BASE.md、verify_bridge.py、verify_source_prefix.py、audit_bridge.py。
方法：逐条手推全部关键代数（§1 块映射与界 (1)、§2 桥组合/同余/分离/Z_i/p_i/(5)、§3 常数、§4 网格不变量与四义务、§5 两种装配的全部不等式、SMALL_BASE 全部数值断言）；复跑作者全部可运行脚本；以自写代码（scratch/mb_review_adv/，不经 cyc.py 的原始对偶数据独立实现行表、标量走步、sym_exit、柱面枚举、提升重构）独立重放关键计算；主动构造对抗性反例搜索。

## 总评

**刻度 1（all correct）。** 在完整对抗审查下，PROOF.md §1–§5 与 SMALL_BASE.md 的全部数学论证**成立**：块映射 x′=−αx/2+2Θ+c、c=6d+6k−B/2、0≤c≤2t、t=3(d+1+2k)（我在 1300 个随机整数提升上逐块重放，含公式恒等、时间增量、清分母精确性 v₂(α)=−G）；界 (1) 的逐步推导（单步代价 1+ε≤4log₂q+4 由修正 C2-log、后继 ω≤2log₂q+3≤√q、几何级数 Σlog qᵢ≤2log₂M、4.4 因子、尾部≤3 证书）逐步核对无误；§2 桥组合更新（β→2−αβ/2∈[1,2]、γ→2t−αγ/2+c∈[0,2(t+u)]、逐块清分母之积 2^s）在 20,000 条随机多块链上通过且与显式轨迹逐点一致；端点整除 ⟹ (3) 同余；Z_i=b_ib_{i+1}t_i+b_ic_{i+1}−b_{i+1}c_i 为纯整数组合（不同桥各自 s_i 的混用合法，全程无除法），|Z_i|≤12T·2^(2S) 精确，(4)⟹Z_i=0⟹p_i=t_i+p_{i+1}、p_{i+1}≤p_i/2（由 p_i≤2t_i⟺t_i≥p_i/2）；r≤2+⌊log₂(2T)⌋ 与 (5) 的拉伸记账（含零/单高情形）重推成立（1+2F+r(F+1)≤(F+1)(4+⌊log₂(2T)⌋) 恰好）。§3 常数（S=201、T=42M³<2^66、4+66+402<1024、497≤√M）与 §4 网格不变量（e=20 等式、平方保持；四义务对**一切**整数 e≥20、r≥48e+64 成立——我用精确二次多项式系数+顶点/系数符号验证：间隙多项式分别为 576e²+3192e+3316、2304e²+5856e+3706、1440e²+4661e+3703、1968e²+5449e+3771，全部系数为正；且各间隙在 r≥48e+64 处对 r 单调增）核实无误。§5 计数（A−1 个连续生产性入口、n≤1+A+(A+1)g=(A+1)(g+1)、3l(2l+6)(2l+5)<2^(l−1)）与直接装配（j_t+Γ_t≤4l+4+(g+1)K_g+3g=18l²+61l+31≤32l²<2^(l−2)）逐步重推成立。SMALL_BASE 的 1023 前缀统计、二次时钟归纳（τ(n+1)−τ(n)≤4G²/3+1145，实测全部 n=0..1021 满足；4(2k+5)²+3435<3·2^(k+1) 对全部 k≥10 精确成立）、两档闭合（10l+37<2^(l−2) 自 l=10；l≥510 用 32l²）、downstream 与已接受 PROOF_EGX §5(b)/定理 U/E1–E4 的条款级一致性均核实。核心计算三方一致复现（原始格枚举 word_search.py 1023 7、作者柱面验证器、以及我的**第三套**独立枚举——无掩码精确柱面+原始对偶数据块表——均得 {1:325, 2:105625, 3:25438, 4:17378, 5:6271, 6:504}、最大生产性块损失 3、长度 7 为 0）；见证 661128→17→661128→857036 用我的独立标量走步重放得 (p₀,t₀,p₁)=(2654187,1769472,884715)、p₀=t₀+p₁，且我进一步在该真实整数提升上验证了 (3) 的两端同余 mod 2^1024、Θ₁=Θ₀+t₀（流逝时钟符号）、桥组合精确命中、Z₀=0（s₀=2 与 s₁=1 不同清分母混合）。四个指定攻击点 (i)–(iv) 全部裁决为**成立**（见下）。导入清单逐条核对为已接受且引用范围未越界。未发现任何 HIGH/MEDIUM 数学缺陷；以下 F1–F7 为 LOW/INFO 级工具与表述事项。

## 逐条发现

### F1 [LOW] audit_bridge.py 在本环境不可运行（z3 缺失），其"universal checks"实际从未以发布形态执行
- 位置：work_mixed_bridge/audit_bridge.py:7（`import z3`）；PROOF.md:265-268。
- 理由：本机未装 z3-solver 且禁止安装；`python -B work_mixed_bridge/audit_bridge.py` 立即 ModuleNotFoundError。PROOF.md 邀请审阅者运行它做"universal checks of the local polynomial obligations"。
- 我的替代核查（scratch/mb_review_adv/indep_ineq.py）：(a) 任意走廊类型的组合界（200,000 随机情形 + 手推）；(b) determinant = P×整数见证 的多项式恒等（手工展开逐单项式比对）；(c) 归一化 |Z|≤12（区间上确界 + 网格）；(d) 非零整数倍模幂 ⟹ |k|≥1、|v|·mod<mod ⟹ v∈(−1,1)；(e) 支付符号与减半；(f) 网格四义务对全部 e≥20（见总评的多项式）；(g) 前缀计数 n≤(g+1)(g+2)、代价倍增、边际 4l+4+(g+1)K+3g≤32l² 对全部 l≥64 精确、32l²<2^(l−2) 精确至 l=3999、3l(2l+6)(2l+5)<2^(l−1) 精确至 l=2000。全部通过。故数学上无损失，但脚本发布形态不可复现。
- 修补：附一个无 z3 的精确整数版本（把我上述检查并入仓库脚本）。

### F2 [LOW] verify_bridge.py scale_checks 仅采样 7 个网格指数（20,21,40,80,160,320,640），全尺度主张依赖未被机器执行的 invariant 论证
- 位置：verify_bridge.py:119-128。
- 理由：`for e in (20,21,40,80,160,320,640)` 为采样；audit_bridge.py 有符号版但不可运行（F1）。全尺度正确性我已用精确多项式补全（总评）；建议在 verify_bridge 内直接嵌入四个间隙多项式的系数断言（对任意 e≥20 免采样成立）。
- 附带核对：e=21（奇 e，上取整平方根）虽在网格之外，脚本用 isqrt 上取整处理，结论不受影响。

### F3 [INFO] §3 的 N≤7(4+67)=497 用了宽松的 67；紧值为 66（N≤490）
- 位置：PROOF.md:141。
- 理由：2T=84·2^60=21·2^62，⌊log₂(2T)⌋=66，(5) 给 7·70=490；文中以 67 为上界得 497。两者均 ≤√M=1024，结论不变；表述为上界无错。

### F4 [INFO] SMALL_BASE 的"至多 22 次小输入重放"实为 ≤21 的宽松上界
- 位置：SMALL_BASE.md:47-49。
- 理由：参数从 ≤63 每步至少降 3 且 ≥5，b/c 步至多 20 次（63,60,…,6），加可能 a 端点 1 次 = 21；取 22、每次 ≤52（实测 max_{n≤62}τ=51 ⟹ 1+τ≤52 ✓）、加 1 个终步得 1145=22·52+1 ✓，方向安全。

### F5 [INFO] 相邻桥对（Z 恒等式）的非平凡实测覆盖只有见证中的一对；我构造第二对的对抗搜索全部落空——且落空方式恰为定理所预测
- 位置：PROOF.md:269-274（three_high_replay）；verify_bridge.py:132-152。
- 理由：见证词 (m,17,m,n)（h=1023）恰含 2 座桥（s₀=2, s₁=1，t 不同）⟹ 一对相邻 Z。我用自写柱面可行性代码测试 4 高词 (m,17,m,17,m)、(m,17,m,17,n)、(n,17,m,17,m)、(m,17,n,17,m)：全部 2-adic **不可行**——对重复桥词这正是定理的必然推论（两桥相同 ⟹ Z=b²t>0 与 2^(h+1)|Z 矛盾 ⟹ 词不存在），构成对 (4)–Z 机制的独立阳性证据。9 项词 (5,367354,5,17,5,122436,5,17,5)（closure_attempt 的最长词）经我的可行性检查确认为可行（与已接受结果一致），但其整数提升重构（含 2 座多块桥的 Z 验证）未在预算内完成；逐对代数与已测对完全相同。不构成缺陷；若作者能补一个含非空走廊低块的第二对实测，覆盖更完整。

### F6 [INFO] 逃逸处理、确定性走廊输入无关性、行公式交叉验证均通过
- 理由：(a) 两个枚举器中超出上限的输出均记录为 escape（word_search 165 个 escape 节点，深度 2–4 分布 66/66/33 复现）而不计为终止，我的独立枚举同口径；(b) v₂(x)=q 的任意整数提升走同一确定性走廊（由 ω≤q−2−ε<q−(1+ε) 保证），我在每块 4 个提升（含随机大 Θ）上验证；(c) 全部 1023 行的日历↔原始对偶接口（R=(c_H+2c_Y)/2^(n+1)、λ=λ_H+2λ_Y+3、ω=v₂(λ)、τ=(λ_H+λ_Y−1)/3、odd=Σhead mod 2）由 verify_source_prefix 断言，我的独立行表计算再次通过；(d) 全部 odd b/c 行 v₂(R)=−(1+ε) 精确（R 分子奇）、ω≤n−ε−1 无违例；(e) cap 8191 实测：2611 个生产性入口、最大块损失 5≤9·13+3、最大 t=21921≤6M³、后继/代价界无违例、最小下落 5。

### F7 [INFO] 若干处推导压缩过紧（均补全后成立）
- (a) §1 的 t≤6M³ 需要 d≤M(1+M²) 与 6k=3τ≤3M²（终 a 行指标≤走廊首输入），文中只给"C1 gives 1+τ(q−1)≤1+M²"；(b) §2 的 γ 不变量证明需要区分"已累积相位 t"与新块相位 u（γ′=2t−αγ/2+c，下界 t′≥t−t=0 用 αγ/2≤t），文中一句带过；(c) §4 的 (4) 蕴含链（12<2^4、T≤h⁷=2^(7e)、2S+7e+4<h+1）未显式写出 12<2^4。均建议各补一行。

## 四个指定攻击点的裁决

- **(i) 分离条件 (4) 的两处分母损失与混合 clearing 因子：成立。** 每座桥用自身 s_i 得整数 b_i=2^(s_i)β_i、c_i=2^(s_i)γ_i（逐块清分母之积的归纳，我验证 2^(lᵢ)(−αᵢ/2)、2^(lᵢ)cᵢ 整数且组合后 2^s 清 a,β,γ）；(3) 由 2^(s_i)x_end=(2^(s_i)a)x_start+b_iΘ_i+c_i 两端各 ≡0 mod 2^(s_i+h+1) ⟹ mod 2^(h+1)。b_{i+1}×(3)_i − b_i×(3)_{i+1} 是**整数**线性组合减法，全程无除法，混用不同 s 完全合法；Z_i≡0 mod 2^(h+1) 为定理而非假设。实测：见证上 b₀Θ₀+c₀≡b₁Θ₁+c₁≡0 mod 2^1024 且 Z₀=0（s₀=2≠s₁=1）。
- **(ii) 流逝时钟符号与 γ/β 实数界：成立。** Θ_{i+1}=Θ_i+t_i（t_i 为桥 i 相位增量，正整数，块级 t=3(d+1+2k)≥3）；p_i=c_i/b_i=γ_i/β_i 良定义（β≥1>0），0≤p_i≤2t_i（γ≤2t、β≥1），p_{i+1}=p_i−t_i≤p_i/2 由 t_i≥p_i/2（⟺p_i≤2t_i）严格成立；p_{i+1}≥0 由 γ≥0 单独给出。衰减链 p_0≥2^(r−2)p_{r−2}≥2^(r−2) 与 p_0≤2T 给 r≤2+⌊log₂(2T)⌋。实测见证 Θ₁=Θ₀+t₀ 精确成立。
- **(iii) 严格 EXT below J 下对更早源用 C2-log 的合法性：成立，无循环。** C2-log（PROOF_EGX §4，已接受修正版 ε≤max(3,2J_W−1)）的前提是 S(J_W) 前 t 链 tie-free；在最小反例归纳中 J_W≤log₂(3(q−1)²+4)<J（各应用点逐验：§5 走廊 q≤g=2l+4 ⟹ J_W≤log₂(3g²+4)<16+2log₂l≪J；塔内 cap≤最小网格 cap≥g ⟹ J_W≤4e+2<J，且 J>2^(2^(e−1)−3)≫4e+2；SMALL_BASE q≤J ⟹ J_W<log₂(3J²)<J 于 J≥1024 平凡），故由强归纳 EXT(J_W) 可用；F 经 τ(J−1) 定义且 τ 单调 ⟹ τ(J_W−1)≤τ(J−1) 使 S(J_W) 有定义。C1 在极大定义前缀上无条件（PROOF_CLOCK §3–4，已接受；SMALL_BASE 自带从 1023 前缀的二次时钟自举）。§5 所引"前缀估计"确为 PROOF_EGX §6 的 unconditional by-product（"the induction did not use LIN-EXIT until its last sentence"原文核实），且 l=⌈log₂J⌉ 使 L 只短不长；直接装配不引 Theorem L。work_ext_roots/PROOF_EXT_ROOTS.md §4 的 J_W≤⌊log₂(3(J−1)²+4)⌋<J 引用与原文一致（该文件已接受）。
- **(iv) 走廊内前缀截断的生产性输入计数：成立。** 相继 a 转变之间的 A−1 个 a-输出为连续生产性入口（每块的走廊+终 a 步都在已实现前缀内；最后一座 a 转变的输出不计为入口，其未完成走廊不读下一行——在计数版中该尾部按参数严格降 ≤g 步计账，在直接装配版中其损失按 S1 伸缩 ≤g 计账，均不需读下一行）；入口必 ≥5（否则行偶、走步止，不生产性）；全部入口 ≤g（质量界 j_t≤log₂(12J²)<g 逐链归纳）。n≤1+A+(A+1)g=(A+1)(g+1) 重推无误；A≤g+1（g>1023 档，§4 全 Q 界）或 A≤7（g≤1023 档，cap-1023 证书 F=6 ⟹ A−1≤6）。

## 导入清单核对（对照 CHECKPOINT_1RB1LA_0RC0RD.md 第 700–865 行接受记录）

| 导入 | 接受记录 | 裁决 |
|---|---|---|
| MASS/CONE（0<α≤1、0≤B≤6d、λ′≤6τ+5） | reviews/origin_contraction_review_record.md（2026-10-27 ACCEPTED；CHECKPOINT:748-759） | 已接受，§1 用法在范围内（B≤Σ6(τ+1)−步数=6d−h ⟹ 0≤B≤6d ✓） |
| core_words 枚举（word_search 1023、长度分布、逃逸 165 节点、损失/时长表） | reviews/g2_rest_review_record.md（2026-10-16 ACCEPTED，"WORDS: no defects"，auditor 2 复算计数） | 已接受；我三方复现（含原始枚举重跑） |
| mixed_blocks 局部公式（PROOF_MIXED (BC)/(BLOCK)/POS） | reviews/g2_frontier_review_record.md（ACCEPTED） | 已接受；§1 的块映射即其 (BLOCK) 的标量化，我用原始数据独立验证 |
| CLOCK/C1（τ≤n² 于极大定义前缀、next-original 引理、HALF j′≤j/2、E4 j≤log₂(6s+5)） | reviews/global_astra11_review_record.md（2026-10-17 ACCEPTED，CHECKPOINT:392-406） | 已接受；SMALL_BASE 的时钟自举（4G²/3+1145）为其常数改良+自有 1023 基，全部不等式我精确复核 |
| C2-log（修正版） | reviews/claude_egx_adversary.md 流程，PROOF_EGX §9 VERDICT: ACCEPTED | 已接受，修正版 max(3,2J_W−1) 引用正确 |
| 定理 U / PROOF_EGX §§4–6（TR、EGX、H、L 及其 by-product、E1–E4） | PROOF_EGX §9 VERDICT: ACCEPTED（CHECKPOINT 未单列，属 work_global_egx 接受记录） | 已接受；§5 引用的"prefix estimate precedes LIN-EXIT"与 §6 末"unconditional by-product"原文一致；SMALL_BASE downstream 对 §5(b) 逐条对应（level fire J<ρ 由 3ρ²+4<2^ρ 于 ρ≥32 成立、小 ρ 由 raw 前缀覆盖、exit chain 由 EXT(J)+ρ>J、v≥3 由 EGX+E1–E4、v≤2 由 E1、blank-tape singleton reduction 由 R4/I-1）——均为已接受条款的同构复用，未发现越界 |
| work_ext_roots §4 | ext_roots 接受记录（文件头"Accepted after three-way review"） | 已接受，J_W 界引用与原文一致 |
| W(Q)≤2^ceil(Q/2) | reviews/global_clock_horizon_closure_review_record.md（closure_attempt 作为条件结果接受，W(Q) 为其未证目标） | 引用方向正确：§4 证明的是 W(Q) 的充分条件的成立（词长≤Q≤2^ceil(Q/2)），与条件定理相容 |
| work_direct_phase 非依赖声明 | —（PROOF.md:6-7"not dependencies"） | 核实：两份草稿全文无任何对 work_direct_phase 的引用；work_direct_phase/PROOF.md 自身为 chain-5 直接返回的独立结果，与本文无依赖关系，声明一致 |
| sym_exit/Xdata（work_m/verify_m.py） | work_m 接受记录（reviews/astra_work_m_review.md；calendar 亦接受） | 已接受；我以自写 sym_exit 实现（按 PROOF_EGX §1 规则重写）与自写标量走步对 J=1..1023 逐链核对一致 |
| cyc.py Calendar(512)（>1022 行的来源） | work_claude_cycle ACCEPTED in part（[A] 部分与 calendar 已接受） | 用于见证重放与大 cap 行；≤1022 行与原始数据逐行核对一致 |

## 运行的命令与关键输出

作者脚本（仓库根，python -B）：
- `python -B work_mixed_bridge/verify_bridge.py` → mixed-word counts [(1,325),(2,105625),(3,25438),(4,17378),(5,6271),(6,504)] maximum block loss: 3；separation and scale constants: PASS；three-high scalar replay: PASS (2654187, 1769472, 884715)。
- `python -B work_mixed_bridge/verify_source_prefix.py` → lengths {0:389,1:586,2:48}；maximum exit loss: 4; maximum small clock: 51; tau(1022): 910。
- `python -B work_mixed_bridge/audit_bridge.py` → ModuleNotFoundError: No module named 'z3'（记录，见 F1；以自写精确检查替代）。
- `python -B work_g2_core_words/word_search.py 1023 7` → counts 2..7 = 105625/25438/17378/6271/504/0，escape_nodes 165（66/66/33），max_block_loss 3。

自写脚本（scratch/mb_review_adv/，均 python -B 自仓库根）：
- `indep_walk.py`：仅由原始对偶数据（Xdata）构建行表/走步/块表 → productive 325、max loss 3、max t 2727（=3·909，与 PROOF_WORDS §4 的 duration≤909 换算一致）、1300 次随机整数提升块映射重放全过、ω≤n−ε−1 无违例、v₂(R)=−(1+ε) 精确。
- `indep_words.py`：第三套无掩码柱面枚举 → 计数与作者/原始枚举逐位一致。
- `indep_witness.py`：独立见证重放 + 桥代数（组合恒等、Θ₁=Θ₀+t₀、端点同余 mod 2^1024、Z₀=0、s₀=2/t₀=1769472/p₀=2654187、s₁=1/t₁=1769433/p₁=884715）。
- `indep_ineq.py`：z3 全替代（组合界 200,000 例、行列式恒等、|Z|≤12、支付减半、网格四义务全 e≥20 精确、前缀计数/预算、SMALL_BASE 全部端点、§3 首次放大）全部 PASS。
- `indep_prefix.py`：τ(n)≤n 全前缀、τ(1022)=910、max τ(n≤62)=51、时钟间隙 ≤4G²/3+1145（n=0..1021 全查）、G=23 且 <2n+1、自写 sym_exit ≡ 自写标量走步（J=1..1023 逐链、逐型、逐损失）、split {0:389,1:586,2:48}、max loss 4、每链严格安全 q+Γ<J。
- `indep_blocks_large.py`：cap 8191 实测（1）与逐步/后继/下落界。
- `indep_composition.py`：20,000 条随机多块链组合不变式 + Z 整除代数。
- `indep_randomwalk.py`、`indep_lift.py`、`find_lifts.py`、`debug_lift.py`：随机大入口走步（多为短词，符合预期）与 4 高词构造尝试（见 F5：全部不可行，重复桥情形与定理预测一致）；9 项词 2-adic 可行性确认。

## 结论

核心主张链条——严格最小反例归纳下输入链 ∈[5,Q]（Q≥64）的生产性混合块词长 ≤Q（cap 1023 有限证书 → §3 首次放大 497 → §4 网格归纳 F(M)=√M）⟹ §5/直接装配排除首次 tie ⟹ strict EXT（PROOF.md 主线自 K′、SMALL_BASE 自 1024）⟹ 已接受定理 U ⟹ #1 空白带不停机——在本次全面对抗审查（手推代数+三方计算复现+反例搜索）下**未发现任何数学断点**。四个攻击点与导入清单均裁决成立。建议按 F1/F2 补一个无 z3 的全尺度精确审计脚本、按 F7 补三处一行推导；F3–F6 为信息性备注。

攻击员：ZCode GLM 5.3，2026-11-22

## 定向复审（patch round, 2026-11-22）

对象：git diff HEAD（4d80eab 之后）中 work_mixed_bridge/ 四文件的 P1–P5 修补。方法：逐行读新 audit_bridge.py 并独立攻击其每个论证（scratch/mb_review_adv/recheck_audit.py：四个间隙多项式与我的独立闭式及真实差值在 10 个 e 值逐一相等；400 个随机 (e,r≥48e+64) 直接验证四义务；导数正性/单调性/顶点位置数值核验；12 元行列式恒等 300 个随机整点；20 万个盒内部点落在角点界内；persist/三个 margin 的闭式核验；shifted() 变换自检）；变异测试（故意删去 (b) 义务的 6r 项、翻转 (a) 的 c0 符号）确认脚本断言有牙；复跑两个脚本；文本修补逐句与既有论证比对。

- **P1（audit_bridge.py 无 z3 重写）：闭合。** 八项 EXACT 覆盖旧 z3 版全部名目：composition（新证的代入 γ=2t·ĝ、c=2u·ĉ 精确，系数 t/u 分离后 coef_t=2−αĝ 双线性、coef_u=2ĉ 线性、β′=2−αβ/2 双线性 ⟹ [0,1] 盒角点即极值，16 角点完备枚举，物理范围 ⊆ 所查盒）、determinant（12 元多项式环恒等 n_sub=={}，零采样；我 300 随机整点独立复核）、normalized bound（z 多线性 ⟹ 32 角点，精确极值 (−4,8) 钉死，强于旧 [−12,12]）、separation、payment、grid invariant（(48e+64)²−(96e+64)=2304e²+6048e+4032 全非负系数，平方保持精确）+ 四义务（我独立重推四个间隙多项式 576e²+3192e+3316 / 2304e²+5856e+3706 / 1440e²+4661e+3702 / 1968e²+5449e+3771 与导数下界 60e+116 / 96e+122 / 78e+122 / 89e+123，与脚本逐系数一致；c1/c0 三元组**无缺项**——历史漏 6r 的 (b) 义务现 c1={0:6}、c0={0:6} 双全；顶点 r*=c1/2<48e+64 由 deriv>0 保证，D 在不变量右方递增的论证成立；非负系数+正常数 ⟹ 对一切 e≥0 严格成立，无采样）、prefix corridor（二元环恒等 (g+1)(g+2)−(1+a+(a+1)g)=(g+1)(g+1−a)）、prefix budget（persist=2cost(l)−cost(l+1) 平移至 64 后 12m³+2334m²+151218m+3257448 全正，精确；三个 margin 平移全正，闭式核验）。**变异测试**：删 6r 项后间隙多项式本身仍"通过"非负断言（r²−6 系数照旧非负），但 e=20 多项式↔直接数值对照（1048570≠1042426）把它抓住；(a) c0 变号同样被对照抓住——即脚本对 D2 类转写错误的防线是 e=20 对照，有效。
  - R1 [INFO] 两处微型循环（整数 |k|≥1 的 range(−5,6)、序保持的 9 个分数例、payment 的 6 点、2l+6<2(2l+4) 的 range(100)）是**公理级平凡性的例示**而非穷举证明（非零整数绝对值≥1、正数乘保序、nxt≤t⟹2nxt≤t+nxt 均为有序域/ℤ 公理推论，旧 z3 版同样是从公理派发）。实质断言全部精确无采样，无强度损失；建议加注释标明"illustrative"以免未来审阅者误读。
  - R2 [INFO] e=20 单点对照可被"多项协同转写错误"绕过（单系数错误必被抓住，因差 δ·20^k≠0）。数学命题本身为真（我的独立闭式+400 随机点直接验证），非阻塞；建议对照扩到 2–3 个 e 值（如 20、21、40）加固。
- **P2（verify_bridge 全尺度+490）：闭合。** `from audit_bridge import gap_polynomials` 调用即触发其内部全部精确断言，`len==4` 钉住个数；`⌊log₂(2T)⌋=66`（2T=21·2^62）与 `7·70=490` 为精确断言；采样循环保留且诚实标注 "Numeric spot checks"。import 无副作用（模块仅定义+R0），无新问题。
- **P3（PROOF.md 三处补行）：闭合，无矛盾。** §1：d≤M(1+M²)、终 a 行 2k=τ≤M²（其指标≤走廊首输入）、t≤3(M(1+M²)+1+M²)≤6M³ 于 M≥2（M³≥M²+M+1 在 M=2 即 8≥7）——与我 round-1 推导一致。§2：以 t 为累计相位，−αγ/2≥−γ/2≥−t ⟹ γ′≥t+c≥0，αγ/2≥0 与 c≤2u ⟹ γ′≤2(t+u)——正确（round-1 已同法验证）。§4：12<2^4 ⟹ 12T<2^(7e+4)，配 2S+7e+4≤h ⟹ 12T·2^(2S)<2^(h+1)——链条完整（≤h 与 <h+1 整数等价，与 §4 义务表述一致）。
- **P4（见证注释）：闭合。** s₀=2、β₀=1（穿 17 复合桥）、s₁=1、β₁=2（单块）四个常数与我 round-1 独立重放全部吻合。措辞小疵 [INFO]：称桥 1 为 "escape block" 略松——857036 是词的入口（高项），"escape above the cap"（§3 义）指越过上限的**输出**；数据无误，不影响闭合。
- **P5（490 与 21）：闭合。** 两处 497→490 一致；SMALL_BASE "至多 21（20 个 b/c 步 63,60,…,6 加可能 a 端点），按 22·52+1=1145 计费"——算术核对 ((63−6)/3+1=20)，与未改动的 1145 界自洽，诚实标注取整；grep 确认无 497/22 残留、无 z3 字样残留。
- **未引入新问题**：改动仅限四文件（CHECKPOINT 的 diff 系 patch 前已存在）；verify_source_prefix.py 未动且复跑通过；verify_bridge.py 与 audit_bridge.py 新版均 PASS，字数/计数/见证输出与 round-1 逐字一致。

**定向复审总评：刻度 1（P1–P5 全部闭合，无新问题）。** 新 audit_bridge.py 的实质断言（多项式恒等、多线性角点、平移非负、导数单调）全部为无采样精确证明，四义务 c1/c0 无缺项（D2 类错误已由 e=20 对照设防并经我变异测试验证有效），仅余 R1/R2 两条 INFO 级加固建议与 P4 一处措辞小疵。

攻击员：ZCode GLM 5.3，2026-11-22
