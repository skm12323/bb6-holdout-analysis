# 盲审复算任务：work_gc_t4_horizon（Theorem H-T4：EXT(<T4) 视野向机器层的迁移）

你是仓库 D:/math_cc 的盲审复算员（auditor 2，agy gemini-3.8-flash-high）。机器 #1
`1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`（BB(6) holdout #1）。本目录的产物声称：在已接受
导入之上证明了 **Theorem H-T4**（F 对一切满足 3s+4<2^T4 的步有定义，且 #1 在前 2^T4−2 个
顶层步内不停机），附两个新记账引理（EXT-T4 全局化、DATA-T4 数据局部性）与塔序引理 ORD。
**第 1 轮审查更正（2026-11-10）已应用**：NOTES 头部更正块列出了六处修补（K 系列上界常数
499497→499997；HINQ slack 二次式 3H²−12H+14→+10（H≥3 成立）；H=T4 的实数延伸论证；(5,5)
着陆措辞改为更正块第 1 条净论证；EXT-T4/DATA-T4 下界改 J≥1；时效数字与 fire_Js 语义）。
复审时请特别核对这些修补本身（而不只是原文）。

## 盲审规则（必须遵守）

1. **独立重推导**：你必须自己重新推导/复算每一条主张，不得把作者的论证当作已知。
2. **不得阅读作者的脚本源码**：`work_gc_t4_horizon/verify_t4_horizon.py` 禁止读。
   你可以读 `work_gc_t4_horizon/t4_horizon_checks.json` 与 `extended_run_900s.log`
   （作为作者运行结果的**数据**，用于核对声明范围是否与之一致），但不得据此代替复算。
3. **审查对象**：`work_gc_t4_horizon/NOTES.md`（逐节、逐主张）。
4. 允许只读的仓库文件（已接受材料）：
   - `CHECKPOINT_1RB1LA_0RC0RD.md`（相关节：work_global_egx、work_global_ext、
     work_global_clock_horizon、work_claude_residual、work_claude_cycle）
   - `work_claude_residual/NOTES.md`（头部更正块**覆盖正文**；Theorem T4 的净表述在其头
     部第 79–81 行与更正块第 7 条）
   - `work_global_clock_horizon/PROOF_CLOCK_HORIZON.md`（CSH、EXT-CLOCK、Lemma MASS、
     Corollary H-CLOCK 及其 §4 依赖清单）
   - `work_global_egx/PROOF_EGX.md`（§1 S(J) 定义与数据需求、§3 I-1..I-4 与 import
     audit、Corollary H、§5 Theorem U(b)）
   - `work_global_ext/PROOF_EXT.md`（§4 Theorem S、Corollary 4、Corollary H″）
   - `work_global_clock/PROOF_CLOCK.md`（§3–4：C1、CLOCK、STATE-CLOCK、s ≤ i²）
   - `work_tie2/PROOF_TIE2.md`（HORIZON-3 的表述，第 26–27、177–178 行）
   - `work_r4/PROOF.md`（§1 singletons S1–S3、§2 Lemma E(v)、ℓ 表第 40 行）
   - `work_r1/RULES.md`（top map 与停机判据）
   - `work_m/PROOF_M.md`（Lemma 2.1–2.3、3.2、3.5、6.1、Theorem 4.1）
   - `work_global_endgame/LEMMAS_E.md`（E1–E4）
   - `reviews/claude_residual_review_record.md`
   - `work_m/verify_m.py`（已接受的引擎，可读，供交叉核对 sym_exit/Xdata 的约定）
5. 其余文件只读；你**不得修改**仓库任何已有文件。
6. 允许写自己的复核脚本，只放在 `work_gc_t4_horizon/agy_scratch/`（可新建）。运行环境：
   从 D:/math_cc 运行 `PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B <你的脚本>`
   （该解释器带 numpy；输出用 ASCII）。

## 逐项复核清单

对每一项给出「成立 / 有可修补缺口 / 不成立」与理由（引用你读到的行号或你运行的命令与输出）：

1. **Lemma HINQ**（NOTES §1 末）：3(H−1)²+4<2^H 对一切整数 H≥16，及派生
   3(H−2)²+7<2^H、(v−1)²<(2^H−4)/3（v≤H−1）。请手推底数与单步常数
   （L(H+1)=L(H)+6H−3<2L(H) ⟺ 3H²−12H+14>0 对一切整数成立）。
2. **Lemma ORD**（§2）：用你自己的方法（不依赖作者脚本）重证
   T1<K、T2<K′、K′<T3、T3<K_clock、K_clock<T4、K′≤K_clock、T4>2^64。注意塔常数：
   N0=2·10^7，T_{h+1}=2^((T_h−3)/2)，K=2^(2^499997−2)，K′=2^(K/2−2)，
   K_clock=⌊2^K′/(64K′²)⌋（K 系列是 499,997，不是 499,497——第 1 轮审查更正块第 1 条）。
   特别核对 K′<T3（两个同为三层的塔，顶层指数 9999996.5 与 2^499997−3 的比较方向）与
   K_clock<T4（同高四层，10^7 > 499997）。不许用浮点。
3. **Lemma EXT-T4**（§3）：三分区间（J<K′ 用 I-4；K′≤J<K_clock 用 EXT-CLOCK；
   K_clock≤J<T4 用 Theorem T4）是否恰好覆盖且假设一致（都是「F 定义到 τ(J−1) 含该步」）。
   重点——**无循环性**：核对 work_claude_residual/NOTES.md 的 DL(i)/(iv)（§3，行
   162–177）与 §5、更正块第 1–2 条：T4 证明内部对 source epoch 的 tie-free 要求是否
   全部落在 Q<T3；Theorem RA 的假设是否只有 F 定义到 τ(J−1)（见
   PROOF_CLOCK_HORIZON §1 第 2 条）；C5_EXTENSION §4 的归纳是否只在单个 S(J) 内部
   （≤4 个 deep 步）而非对 J 归纳。若发现任何对 J′∈[K_clock,J) 的 EXT 使用，判 3。
4. **Lemma DATA-T4**（§4）：(a) 是否恰为 PROOF_EGX §1（行 53–56）与 §3 import audit
   （行 163–171）的内容；(b) C1 的适用条件（"every reached crossing"）在此是否满足；
   (c) 数值链 (J−1)² ≤ (T4−2)² < (2^T4−4)/3。
5. **Theorem H-T4 (i)**（§5）：对照 PROOF_EGX §5 Theorem U(b)（行 215–226）逐条核对
   「I-4 被 Lemma EXT-T4 替换」后每个环节仍是已接受的：PROOF_M Cor 3.5 与 replay
   引理；层级 fire 的 J<ρ（ρ≤10^8 审计基；ρ>10^8 用 STATE-CLOCK，核对 PROOF_CLOCK §4
   的原文）；exit chain 的系数裕度 σ−j=(ρ−J)+h；**严格性 τ(J−1)<τ(ρ)=s₀** 的论证
   （同时刻交叉对只可能是 (X(m) a 型, X(m+1) b 型)，X(ρ) 是 a 型）——请独立验证这一
   论证（可读 work_m/verify_m.py 的 Xdata 循环核对同时刻配对结构）。
6. **Theorem H-T4 (ii)**（§5）：对照 PROOF_EGX §3 Corollary H（行 173–179）核对
   singleton 归纳的每一情形（S1/S2/S3、v≤2000 用 Lemma E(v)、v≥3 用 D5+EGX+E1–E4）；
   覆盖论证（每个 n*<2^T4−2 都落在某段已处理区间内）；**I-3 reached-crossing 论证的
   实例化**（步 (v−1)² 与 (v−1)²+1 都在已定义前缀内；s≤i² ⟹ i>v−1 ⟹ τ(v−1)≤(v−1)²）；
   off-by-one 表（2^H−2、(2^H−4)/3、含 τ(J−1) 该步）是否与 H″/H-CLOCK 的惯例一致。
7. **[B] 声明的诚实性**：NOTES §6(c) 所报范围（默认预算下 H₀=20,22,24,26；时长随机器
   负载 98-150 s，各项计数确定性不变；H₀=26 的各项计数）是否与 t4_horizon_checks.json
   （由最后一次默认预算运行写入，见其 c_total_s）/ extended_run_900s.log 一致；声明是否
   明确「模式验证、非证明、不依赖 H₀」。你应当**用自己的代码**独立复算一个
   较小尺度（建议 H₀=16..20）：至少验证 (i) top map 前 2^H₀−2 步无停机且 sum law；
   (ii) 每个 even singleton 的 v<H₀ 且 gap（到下一 singleton 的步数−1）只依赖 v、与
   出现次序无关；(iii) 对 v=3..8：pair endgame（从 F 的状态 X(v−1) 出发）与符号退出
   S(v) 的 j-序列逐项相同，且 gap==τ(v−1)+endgame 长度；(iv) ℓ(1..20) 与
   work_r4/PROOF.md:40 的表一致。
8. **越级检查**：NOTES 是否声称了 T5、J≥T4、全局不停机，或改动已接受视野（应只说
   「接受后」才改）；是否与死路清单冲突。
9. 结论格式：中文写审查到 `reviews/gc_t4_horizon_auditor2_agy.md`，含逐项清单与证据，
   最后一行**恰为** `VERDICT: 1`（all correct）/ `VERDICT: 2`（with fixable gaps）/
   `VERDICT: 3`（structure broke）。
