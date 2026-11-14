# 对抗性审查：work_gc_t4_horizon（Theorem H-T4，EXT(<T4) 向机器层的迁移）

攻击员·R1（ZCode GLM），2026-11-10。对象：`work_gc_t4_horizon/NOTES.md`（Theorem H-T4、Lemma
EXT-T4、Lemma DATA-T4、Lemma HINQ、Lemma ORD、§6 验证）、`verify_t4_horizon.py`、
`t4_horizon_checks.json`、`extended_run_900s.log`、`agy_audit_prompt.md`。

## 一、方法

1. 逐节精读 NOTES 并对每条引用回到被引文件核对原文（行号逐一对照，见 §四）。
2. 运行验证脚本两次：默认预算 480 s（`PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/
   Python/Python312/python.exe -B work_gc_t4_horizon/verify_t4_horizon.py`，本轮 149.4 s，
   ALL PASS，exit 0，梯子 {20,22,24,26}）与同命令加参数 `900`（本轮 631.5 s，ALL PASS，
   exit 0，梯子 {20,22,24,26,28}；作者 extended_run_900s.log 记 420.4 s，机器负载差异）。
   两轮的全部计数与 NOTES §6 / t4_horizon_checks.json / extended_run_900s.log 逐项一致
   （含 H0=28 的 89,478,483/100,296,961/30,377,959/2,383,039/30,377,958/268,435,454/
   119,960,495/91,133,877/maxv 27）。
3. 独立复算（自写代码，不复制作者实现）：(i) 自实现 work_r1/work_r4 顶层映射，H0=16/18/20
   全量验证（无停机、sum law、singleton 结构、gap 只依赖 v、ℓ 表、off-by-one）；
   (ii) 用**仓库正确常数**（499997 系列）独立重推全部塔序（精确整数 slack 步骤）；
   (iii) HINQ 手推（恒等式、slack 多项式、基）。
4. 对抗性检查：常数一致性、off-by-one、循环性、范围夸大、与已反驳清单的冲突。

## 二、逐条发现

### F1 [MEDIUM] Lemma ORD 与脚本 part(b) 的 K 系列常数错误：验证对象与仓库定义不符，
###       NOTES §2 的界文字对真实常数是假命题

- **位置**：`verify_t4_horizon.py:156-173`（K/K′/K_clock 界用 Tw(2,449496)/Tw(2,449497)、
  Tw(3,449496/499497)、Tw(4,499495/499497)）；`NOTES.md §2`（行 84-86 的界文字）；
  对照 `verify_t4_horizon.py:14`（docstring 自写 `K=2^(2^499997-2)`）与仓库定义
  `CHECKPOINT_1RB1LA_0RC0RD.md:289`（K = 2^(2^499997−2)）、
  `work_global_clock_horizon/PROOF_CLOCK_HORIZON.md:8`（K′ = 2^(2^(2^499997−3)−2)）。
- **理由**：真实 log2 K = 2^499997−2，故 K ∈ (2^(2^499996), 2^(2^499497))，脚本却用
  (2^(2^499496), 2^(2^499497))；K′ 的真实 log2-log2 = 2^499997−3−δ **大于** 2^499497，
  所以脚本的「上界」 Tw(3,499497) 不是 K′ 的上界，K_clock 的「上界」 Tw(4,499497) 同样不是
  上界（真实 log2⁴ K_clock ≈ 499996.99 > 499497）。于是 checks `'K_prime < T3'`、
  `'K_clock < T4'`、`'K_prime <= K_clock'`（verify_t4_horizon.py:178-181）即使全部通过，
  也**不构成**对仓库常数系列的这些序关系的证明（"上界 < 下界 ⟹ 左 < 右"的推理要求上界
  真是上界）。docstring（499997）与 line 156 注释（499497）自相矛盾即其笔误根源（第二位
  9 误作 4，差 500）。NOTES §2 的界文字（"2^(2^499496) < K < 2^(2^499497)" 等）对真实
  K 系列逐条为假。
- **为何不是 HIGH**：八个序关系对正确常数系列**全部仍然成立**——我已独立重推（见 §四.2，
  每一步都是精确整数 slack 断言，无浮点），关键 slack（499997 < 9999990、499497 < 9999996、
  499496 < 9999998）依然巨大。Theorem H-T4 实际只使用 T3 < K_clock < T4、K′ ≤ K_clock、
  T4 > 2^64，结论不受影响。脚本其余部分（(a)、(c)）不涉及这些常数。
- **修补**：把 part(b) 与 NOTES §2 的界常数改为 499996/499997/499995 系列
  （K ∈ (Tw(2,499996), Tw(2,499497))、K′ ∈ (Tw(3,499996), Tw(3,499497))、
  K_clock ∈ (Tw(4,499996), Tw(4,499497))，各步 slack 论证逐字相同地成立），重跑。修改量
  约五行。

### F2 [LOW] HINQ 的 slack 等价多项式写错（"i.e." 不真）

- **位置**：`NOTES.md:61-63`（"L(H+1) = L(H)+6H−3 < 2·L(H) whenever 6H−3 < L(H), i.e.
  3H²−12H+14 > 0, which holds for every integer H"）；脚本 `verify_t4_horizon.py:64-67`。
- **理由**：6H−3 < 3(H−1)²+4 等价于 **3H²−12H+10 > 0**（仅对 H≥3 成立，判别式 24，H=2
  反例：9 > 7）。14 版本处处成立（最小值 2 在 H=2）但它**不蕴含** slack（H=2 即是
  14>0 而 slack 失败的实例）。NOTES 用 14 版本论证"the step is valid at *every* H"方向
  错了。实际无损：HINQ 只需 H≥16；slack 对一切 H≥3 解析成立，且脚本 line 71 在
  H=16..4096 直接断言了 slack 本身（不依赖该蕴涵）。
- **修补**：NOTES 措辞改为"a sufficient condition is 3H²−12H+10 > 0, which holds for
  every integer H ≥ 3（判别式 24，两根 ≈1.18/2.82）；HINQ 从 H=16 起步，故步进恒有效"。

### F3 [LOW] H = T4 是无理数，HINQ/H-CLOCK 的整数表述应用于 T4 缺一句实数延伸

- **位置**：`NOTES.md:65-66`（"The same inequality at H = T4 is what the proof below
  uses; it does not depend on any finite range"）；§4(c)、§5(ii) 在 H=T4 处使用
  3(H−2)²+7 < 2^H 等。
- **理由**：HINQ 与其派生式是对**整数** H 证明/验证的；T4 = 2^((T3−3)/2) 无理
  （NOTES §0 自己声明了这一点并给出 reading 约定）。从整数版本到实数 T4 不是自动的
  （步进 +1 与 2^{frac} 因子）。但实数版一步可证：log2 T4 = (T3−3)/2 ⟹ 3T4² =
  3·2^(T3−3) < 2^(T3+2) < 2^T4（比较 T3+2 < 2^((T3−3)/2)，T3 ≥ 16 显然），故
  3(T4−1)²+4 < 3T4² < 2^T4，且 (T4−2)² 等派生式同理由巨大 slack 得出。
- **修补**：在 §1 HINQ 段末补一句上述实数论证（或引用 T4 > 2^64 的 slack 直接比较）。

### F4 [LOW] §3 对 BBBA family 处理的转述与 residual 审查更正块的净论证措辞不齐

- **位置**：`NOTES.md:111-113`（"the one uncertified landing family (BBBA, §5.4) has
  T1 ≤ Q < T2 and is absorbed by Theorem RA"）。
- **理由**：residual 更正块第 1 条（work_claude_residual/NOTES.md:10-33）明确**撤回**了
  §5.4 的 AB′/copy-principle 吸收论证；净论证是：(5,5) 的唯一可能来源是 X(J−1) 为
  type a（此时 RA **整体**给出 EXT(J)，其内部的 AB 使用自洽，因为被复制的 epoch 在
  τ(J−1) 前结束）；而 X(J−1) 为 type b/c 时 (5,5) 不可达（route c：j₁ = ω(J−1) < T2
  与 DL(i) 给出的 j₁−1 > T2 矛盾；route b：θ₁ = 0 ≠ 2），C5_EXTENSION §4 照原样适用。
  "absorbed by Theorem RA" 字面上更接近被撤回的 §5.4 旧表述。**无循环性结论不受影响**
  （gc_t4_horizon 对 RA 的 F-假设的引用——PROOF_CLOCK_HORIZON §1 item 2——是准确的），
  但审查追溯性上应与更正块对齐，避免读者沿错误措辞重建论证。
- **修补**：§3 该句改为更正块第 1 条的表述："(5,5) 只能经 X(J−1) type a 出现，此时
  Theorem RA 直接给出 EXT(J)；X(J−1) type b/c 时 (5,5) 不可达（route c 被 j₁ < T2 与
  DL(i) 排除，route b 给 θ₁=0），故 C5_EXTENSION §4 无需任何吸收假设"。

### F5 [LOW] EXT-T4 的陈述下界 J ≥ 2 与使用处 fire 的 J = 1 差一个值

- **位置**：`NOTES.md §3`（"For every integer J ≥ 2 with J < T4"；第 1 段写成
  "2 ≤ J < K′: import I-4"）与 §5(i)（fire 的 J = v2(3s₀+4) 可为 1；实测 H0=26 有
  2,724,369 个 J=1 的 fire，t4_horizon_checks.json fire_Js）。
- **理由**：Theorem H-T4(i) 对每个 fire 的 epoch 使用 EXT-T4，而 J=1 的 fire 大量存在。
  已接受的 I-4 原文是 "every J < K′"（PROOF_EGX §3:158，其首段 "J < 10^6 by V4 of
  PROOF_M (Class B, all J)" 含 J=1），U(b) 即在此之上运行；gc_t4_horizon 的三段覆盖
  [2, T4) 在下端少列了 J=1。缺口可一行补上（把第 1 段写成 1 ≤ J < K′，或注明 J=1 的
  epoch 由 I-4 的 all-J 基覆盖；机器层数据亦确认 S(1) 闭合、r=0）。
- **修补**：改范围下界并加半句说明。

## 三、核对通过的部分（未发现问题）

1. **Lemma EXT-T4 的三段组合与无循环性**（NOTES §3）：三段恰好覆盖且假设一致（均为
   "F 定义到 τ(J−1) 含该步"）；I-4 段按 PROOF_EGX §3:158-161；EXT-CLOCK 段按
   PROOF_CLOCK_HORIZON §3:89-94（CSH+Theorem S+Lemma MASS，Theorem S 无 EXT 假设，其
   证明内部 "copies read epochs of level ≤ 3, tie-free by I-4"，PROOF_EXT:139）；T4 段
   按 residual NOTES:79-81 的净表述。**无循环性**：T4 证明内部对 source 的 tie-free
   使用全部带 Q < T3 界——DL(i)（residual:162-163，我重推了其证明：2^Q | 3s+4 ⟹
   s ≥ (2^Q−4)/3，C1 给 ρ ≥ √s ≥ 2^((Q−2)/2)（Q≥4，等价 2^Q ≥ 16 核对无误）⟹
   2log2 n+3 ≥ Q+2）；DL(iv)（residual:175-177，deep chain t=0..3 的 source 界
   T3/T2/T1/N0 与 G 的严格边界 G(T_{h+1})=T_h 一致）；shallow crossing n<N0 ⟹
   Q < G(N0) < 60 < N0；BBBA 的 T1 ≤ Q < T2 < T3。全部 Q < T3 < K_clock 落入段 1-2
   （对 J 无条件成立）。假设传递正确：Q−1 < J−1 且 τ 非降 ⟹ F 定义到 τ(J−1) 给出
   F 定义到 τ(Q−1)。C5_EXTENSION §4 的归纳确在单个 S(J) 的 ≤4 个 deep steps 上
   （"simultaneously induct on the first at most Lambda deep steps"），非对 J 归纳。
   终止子句引自 PROOF_EGX §5:206-208，逐字一致。
2. **Lemma DATA-T4**（NOTES §4）：(a) 恰为 PROOF_EGX §1:54-56 + §3:163-171 的内容
   （我逐字对照）；(b) C1 的适用面按 PROOF_CLOCK §3:114（"for every reached crossing,
   without an exit-length or C2 hypothesis"，归纳在每个已达 crossing 上）；
   (c) 的数值链 (J−1)² ≤ (T4−2)²、3(T4−2)²+7 < 2^T4 无误（除 F3 的实数延伸一句）。
3. **Theorem H-T4(i)**（NOTES §5）：与 U(b)（PROOF_EGX §5:215-226）逐环节对照——
   Cor 3.5/replay 的使用、fire 的 J<ρ（ρ ≤ 10^8 审计基 V2 = U(b):217-218 原文；ρ > 10^8
   的 STATE-CLOCK = PROOF_CLOCK §4:133，P(ρ) < 2ρ+1 即该文 §3 的 (INC)，原文如此）、
   exit chain 的系数裕度 σ−j = (ρ−J)+h（与 U(b):220-223 相同，ρ−J ≥ 1 由 fire S1、
   h ≥ 1 由 tie-free）、termination（U(b):224-226）。**τ(J−1) < τ(ρ) 的严格性补强**
   独立验证：Lemma K（PROOF_EXT:60-66）给出同一步记录的 crossings 恰为相邻指针的
   (a,b) 对（"A state with P = ∅ reads E_i, E_{i+1} (types a, b at the same step)"），
   X(ρ) 是 a 型 ⟹ (ρ−1, ρ) 非同时刻对 ⟹ τ(ρ−1) < τ(ρ)；这修复了 U(b)/H-CLOCK 原文
   "J−1 < ρ gives τ(J−1) < τ(ρ)" 的隐含跳跃（τ 只是非降），是本笔记对先例的实质补强。
4. **Theorem H-T4(ii)**（NOTES §5）：与 Corollary H（PROOF_EGX §3:173-179）逐情形对照
   ——S2（3(n+2) 非 2 的幂）、S1（奇→n+1）、S3（n 偶→E(w,v)）、v ≤ 2000 用 Lemma E(v)
   （work_r4 §2, Class-A）、v ≥ 3 的五步（前缀内性 = HINQ、I-3 reached-crossing 实例化
   与 PROOF_EGX §3:156-158 的原文论证一致（"the state at step m²+1 ... i² ≥ s > m²,
   so i > m"）、EXT-T4、D5+EGX（对一切奇 w）、E1-E4）——全部对应已接受内容；
   覆盖论证（每个 n* < 2^T4−2 是 singleton 或严格介于两个相继 singleton 之间）与
   Corollary H''（PROOF_EXT:149-153）的模式逐条一致；off-by-one 表（§5 末）与
   H''/H-CLOCK 的 reading {n : n+2 < 2^H} 一致，且 "首个 v2(n+2) ≥ H 的 n 恰为 2^H−2"
   是平凡数论（v2(m) ≥ H ⟺ 2^H | m），脚本第 5 项做了精确断言。
5. **脚本 part(a)**：恒等式 L(H+1) = L(H)+6H−3 代数核对无误（3H²+4 = 3(H−1)²+4+6H−3）；
   H=16..4096 直接断言主不等式、派生式与 slack 本身；无溢出（Python 大整数）；无浮点。
6. **脚本 part(c) 的检验真实性**：lam_walkB 覆盖 s = 0..(2^H0−5)//3（s ≤ s*−1 ⟹
   3s+4 ≤ 3s*+1 ≤ 2^H0−4，即恰好"3s+4 < 2^H0"的全部步）；top_map_run 覆盖
   n = 0..2^H0−3（恰为 {n : n+2 < 2^H0}）；每个 fire 断言 J = v2(3s+4)、3s+4 < 2^H0、
   J < ρ、τ(J−1) ≤ (J−1)²、CLOCK s ≤ i·P(i)（P 的 bit_length ≥ ⌈log2⌉，方向保守）；
   每个 exit chain 断言 margin；每个 closed epoch 断言 j-序列 == S(J) 且 r ≤ max(0,J−2)
   （Lemma 6.1/3.2 的机器层全量复演，H0=26 达 7,594,490 个 epoch）；每个 even singleton
   断言 v < H0 且 gap == ℓ(v)（每次出现，H0=26 达 22,783,474 次）；引擎一致性
   （lambda-only vs full-pair，n < 64 的 τ/ε）与 verify_m.sym_exit 只读交叉核对
   （J = 1..32，json 记录实际执行而非 skipped）；s ≤ i² 对 i ≥ 16 每步断言；C1 对
   n < 4096 的记录 crossing 断言。预算自适应诚实（本轮 H0=28 预测 468 s > 288 s 被跳过）。
7. **[B] 声明的诚实性**：NOTES §6 的全部数字与我两轮运行及 json/log 完全一致
   （H0=26：22,369,619/25,074,248/7,594,491/595,760/7,594,490/67,108,862/29,990,130/
   22,783,474/maxv 25/min margin 3；900 s 轮另达 H0=28：268,435,454 top 步、89,478,483
   F 步、30,377,959 fires、119,960,495 singletons、91,133,877 gap checks，且明确注明
   per-fire CLOCK 断言是 H0=28 运行之后加入、由默认预算轮行使）；§6 的范围声明
   （"模式验证、非证明、分析定理不依赖 H0"）与吞吐限制如实写明。
8. **越级检查**：NOTES §0/§7 未声称 T5、J ≥ T4、全局不停机；明确"接受前已接受视野仍为
   2^K_clock−2"；未触碰 K_clock 算术、Theorem S 截断、G1/CL4；与死路清单无冲突
   （未使用 DL 严格下降/NT/CAL-C/C7 字面/AB′/copy principle 作为前提——AB′ 的撤回在
   residual 更正块，gc_t4_horizon 的论证路径不依赖它，见 F4 的措辞问题）。
9. **agy_audit_prompt.md**：盲审规则完备（禁读作者脚本、独立重推、允许文件清单、复核
   清单覆盖我发现的全部敏感点、VERDICT 格式与输出路径明确）。

## 四、独立复核/复算清单（本人在本轮执行）

1. **脚本重跑**：`PYTHONUTF8=1 <Python312> -B work_gc_t4_horizon/verify_t4_horizon.py`
   （默认 480 s：ALL PASS，exit 0，本轮 149.4 s，梯子 {20,22,24,26}）与同命令加参数 `900`
   （ALL PASS，exit 0，本轮 631.5 s，梯子 {20,22,24,26,28}）；两轮输出计数与
   t4_horizon_checks.json、extended_run_900s.log、NOTES §6 逐项一致。
2. **塔序（正确常数）独立重推**：自写精确整数 slack 断言脚本（无浮点，仅小整数比较
   2^24 > 10^7 级），按仓库定义 K = 2^(2^499497−2)、K′ = 2^(2^(2^499497−3)−2)、
   K_clock = ⌊2^K′/(64K′²)⌋ 重推 T1<K、T2<K′、K′<T3、T3<K_clock、K_clock<T4、
   K′≤K_clock、T4>2^64：全部成立（输出 "ALL OK"）——确认 F1 不推翻 Lemma ORD 的结论。
3. **独立 top map**：自实现 work_r1 宏规则（work_r4 形式），H0=16/18/20 全量：
   无停机、sum law 3n+3 每步、max v = H0−1、每个 v 的 gap 集合为单点（gap 只依赖 v）、
   ℓ(1..19) 与 work_r4/PROOF.md:40 的表逐项一致、v2(2^H0) = H0 且 v2(2^H0−1) < H0。
4. **HINQ 手推**：恒等式与基（H=16：679 < 65536）核对；slack 等价多项式为
   3H²−12H+10 > 0（H≥3 成立；NOTES 的 14 版本系充分不必要，见 F2）。
5. **依赖引用逐条对照**（行号级）：PROOF_EGX §1:54-56、§3:152-161、§3:163-171、
   §3:173-179、§5:206-208、§5:215-226；PROOF_CLOCK_HORIZON §1:17-22、§3:89-94、
   §3a、§4:141-168；PROOF_EXT Lemma K:60-66、Theorem RA:83-90、Theorem S:134-144、
   Corollary H'':149-153；PROOF_CLOCK §3:72-118（C1）、§4:120-136（CLOCK/STATE-CLOCK/
   s≤i²）；work_r4 §1:16-26（S1-S3）、§2:28-40（Lemma E(v)、ℓ 表）；work_claude_residual
   NOTES:79-81（T4 净表述）、更正块:9-77（第 1、7 条）、DL:160-177、§5-6；
   C5_EXTENSION.md §1-4。全部与 gc_t4_horizon 的引用相符（F4 的措辞差异除外）。
6. **严格性补强的独立验证**：由 Lemma K 原文重建 τ(J−1) ≤ τ(ρ−1) < τ(ρ) 论证
   （同时刻对仅 (a,b)、X(ρ) 为 a 型、τ 非降）。
7. **fire 参数分布**：从 t4_horizon_checks.json 读出 fire_Js（J=1 的 fire 存在且量大，
   支撑 F5）。

## 五、总评

Theorem H-T4 的证明主体（EXT-T4 的无循环三段组合、DATA-T4、(i)/(ii) 对 U(b)/Corollary H/
H''/H-CLOCK 的逐条重放、τ 严格性补强）经我逐环节对照已接受文献后**成立**；机器层验证真实、
全量、与我两轮重跑及独立实现一致；范围声明诚实，无越级。实质缺口一处（F1：Lemma ORD 的
[B] 验证用错了 K 系列常数——docstring/NOTES 声称的对象是 499997 系列、实际断言的是
499497 系列，三个 check 的"上界"对真实常数不成立，验证不覆盖其声称对象）；我已用正确
常数独立重推全部序关系确认结论侥幸不受影响，修复约五行。其余为措辞/一句话可补的 LOW
（slack 多项式引用、T4 无理数的实数延伸、BBBA 转述对齐、J=1 下界）。

**总评刻度：2. fixable gaps**（F1 修复 + F2-F5 措辞修补后可复核接受；核心定理链条经
对抗审查未发现结构性漏洞）。

---

# 定向复审（第 1 轮修补核查，2026-11-10，攻击员·R1）

对象：修补后的 `NOTES.md`（头部新增更正块 2026-11-10，行 11-49）、
`verify_t4_horizon.py`（part(a)/(b) 改动）、更新的 `t4_horizon_checks.json` 与
`extended_run_900s.log`。核查方法：字节级常数提取（regex `499[0-9]97`——渲染文本中
499497/499997 无法肉眼可靠区分，第 1 轮错误即此类笔误）、19 个精确整数链接的独立判定、
修订脚本重跑、part(c) 特征行比对。

## 1. 修补落实情况（7/7 落实）

1. **F1 [MEDIUM] ORD 常数** ✓ 已修且正确。脚本三个上界 `Tw(2,499997)`（:175）、
   `Tw(3,499997)`（:179）、`Tw(4,499997)`（:190）经字节级提取确认全部为 499**9**97 系；
   注释块（:173-190）与 NOTES §2（行 131-132）三个上界同步（`2^(2^499997)`、
   `2^(2^(2^499997))`、`2^(2^(2^(2^499997)))`）；下界 499996/499496/499495 保持不变
   （为真界，见下）。我用 19 个精确整数链接（每个塔比较归约到 ≤2^9999998 的可计算整数
   比较，无浮点、不构造双层幂）独立判定：修订后的每条界对仓库常数（K = 2^(2^499497−2)、
   K′ = 2^(2^(2^499997−3)−2)、K_clock = ⌊2^K′/(64K′²)⌋）**全部为真界**（含 K 上界
   2^499497−2 < 2^499497、K′ 上界 2^499497−3 < 2^499497、K_clock 的 log2⁴ < 499997
   链），8 个序关系的「上界<下界」推理链全部有效（ALL 19 LINKS OK）。两种预算重跑：
   作者 900 s（extended_run_900s.log：ALL PASS，600.2 s，梯子 {20,22,24,26,28}，per-rung
   计数与第 1 轮逐项一致）；本人默认 480 s（ALL PASS，exit 0，151.9 s，梯子
   {20,22,24,26}，计数一致）。
2. **F2 [LOW] HINQ 二次式** ✓ NOTES §1（行 102-104）改为 3H²−12H+10（判别式 24、
   roots 2±√6/3、H≥3、min 1 at H=3、H=2 失败 9>7 注明）；脚本（:64-73）检查范围改
   range(3,4000)+最小值断言+H=2 反例 negative control。roots/判别式我复核无误。
3. **F3 [LOW] 实数延伸** ✓ NOTES §1 新增 *Real-H instance* 段（行 106-113）：
   3·T4² = 3·2^(T3−3) < 2^(T3+2) < 2^T4，末步 T3+2 < 2^((T3−3)/2) 精确实例化为
   (T3+2)² < 2^(T3−3)（T3=16: 324 < 8192；右翻倍、左乘 ((T3+3)/(T3+2))² < 2 的保持性；
   T3=16..4096 精确检查 + T3 > 2^64 由 ORD）。我手核：3·2^(T3−3) < 2^(T3+2) ⟺ 3 < 4
   平凡真；保持性条件 T3²+2T3−1 > 0（T3≥1）正确；派生 3(T4−1)²+4 < 3T4² ⟺ T4 > 7/6 ✓。
   脚本 :81-89 落实为两个断言族。
4. **F4 [LOW] BBBA 措辞** ✓ §3（行 160-168）改为 residual 更正块第 1 条净论证：
   (5,5) 仅经 X(J−1) type a 出现（RA outright，其 AB 内用自洽），type b/c 不可达
   （route c: j₁ = ω(J−1) < T2 与 DL(i) 所需 j₁−1 > T2 矛盾；route b: θ₁ = 0 ≠ 2）。
   与更正块原文对齐。
5. **F5 [LOW] J=1** ✓ EXT-T4 陈述改 J ≥ 1（行 137）；第 1 段改「1 ≤ J < K′」并补
   J=1 论证（S(1) 的数据 X(0) = 初始态 A = (1,1) 偶头 ⟹ 立即闭合 r = 0；§6(c) 每个
   J=1 epoch 零 exit chain 佐证——与 json fire_Js 的 J=1 计 2,724,369 一致）；DATA-T4
   同步 J ≥ 1 并注 τ(0) = 0 初始态。
6. **INFO-1 时效数字** ✓ §6(c) 吞吐改为 ~6-9·10^5 / ~7-12·10^5 steps/s（与本轮实测
   0.65/0.81·10^6 相符，较第 1 轮声明更保守）；时长 98-150 s 覆盖 json 的 148.5 s 与
   本人 149.4/151.9 s；900 s log 更新为修订脚本重跑记录。
7. **INFO-2 fire_Js 格式** ✓ 更正块第 6 条、§6（行 322-323）、§8（行 383-384）三处
   说明 `[J, [fire_count, min_margin_rho_minus_J]]`。

## 2. 新引入问题检查

- **part(c) 无实质改动**：特征行逐字比对（CAP=4096、walkA/sym_walk/endgame_run/
  lam_walkB/top_map_run 五引擎、ladder 与 0.6 预算比、s* 公式、main 默认 480、r4ell 表、
  fire 断言族）全部一致；part(c) 计数在修订脚本下与第 1 轮逐项相同（确定性），与
  「stable across every run」的声明一致。
- 更正块本身（行 11-49）对三方发现与修补的概括准确（含「lower tops … may stay」与
  lower tops 数值 499,996/499,996/499,495 同脚本），无失实表述。
- 残留 nit（**预先存在、非本轮引入、非承重**）：脚本 docstring 用法行
  `[total_budget_seconds=540]`（:5）与 main 默认 480（NOTES §6/§8 亦写 480）不一致
  ——第 1 轮版本 :4 同样写 540。预算仅控制自适应梯子的时间上限，不影响任何断言的
  真值；可留待下一次顺手修改，不构成发现。

## 3. 复审结论

第 1 轮全部 5 项发现（1 MEDIUM + 4 LOW）与 2 项 INFO 均已正确落实；修补集中在
part(b) 常数、part(a) 断言与文字，核心证明（EXT-T4/DATA-T4/H-T4 (i)(ii)）与 part(c)
引擎未被触碰；修订脚本两种预算重跑全过且计数确定。F1 的修复经字节级常数确认、19 链接
精确判定与重跑三重核实。未发现修补引入的新问题（唯一残留为预先存在的 docstring 540/480
笔误，非承重）。

**复审刻度：1. closed in all states**（第 1 轮发现全部关闭；对修补后文本无保留意见，
除上述非承重 nit 外无新发现）。

---

# 定向复审（第 2 轮修补核查，2026-11-10，攻击员·R1）

对象：Round 2 修补——`verify_t4_horizon.py` docstring 用法行 540→480（唯一未决项，已由
总结方记录为 non-blocking round-cap-2 项）与 NOTES.md 更正块新增 Round 2 条目（:51-57）。

## 1. 修补落实情况（1/1 落实）

- **docstring 540→480** ✓：verify_t4_horizon.py:4 现为 `[total_budget_seconds=480]`，
  与 `main` 默认（`else 480.0`）及 NOTES §6/§8 一致；字符串 '540' 已不在脚本任何位置
  出现（本人字节级检查）。文件大小与 Round-1 修订版完全相同（29,160 字节，等长替换），
  且 Round-1 复审的全部特征行（part(a) 的 H=3..3999 slack 检查与 H=2 反例、real-H 断言
  族 (T3+2)²<2^(T3−3)；part(b) 的三个上界元组 `K=(Tw(2,499996),Tw(2,499997))`、
  `Kp=(Tw(3,499996),Tw(3,499497))`、`Kc=(Tw(4,499495),Tw(4,499497))`；part(c) 的五引擎/
  ladder/0.6 预算比/s* 公式/fire 断言族/r4ell 表）逐字保持——即除用法行外**无任何其他
  改动**。
- **重跑**（本人，默认 480 s）：`PYTHONUTF8=1 <Python312> -B
  work_gc_t4_horizon/verify_t4_horizon.py` → ALL PASS，exit 0，150.6 s，梯子
  {20,22,24,26}，H0=26 全部计数与历轮逐项一致（22,369,619/25,074,248/7,594,491/
  595,760/7,594,490/67,108,862/29,990,130/maxv 25/22,783,474/min margin 3）。
- 更正块 Round 2 条目对 typo 的描述（预先存在、非承重、预算只封顶梯子墙钟）与事实
  相符。

## 2. 新引入问题检查

- **一个 nit 级时效不一致（Round 2 条目自引入，非承重）**：NOTES.md:57 写「the
  shipped t4_horizon_checks.json (final default-budget run, **150.7 s**, ladder
  {20,22,24,26})」，而 shipped json 在 NOTES 定稿（03:37）之后又被一次运行覆盖
  （03:40，c_total_s = **153.3**）；本人本轮重跑后该字段再次变化（150.6）。所有
  per-rung 计数确定性不变（历轮逐项一致），仅墙钟字段随每次运行刷新——这正说明
  更正块里写死具体秒数不稳健。建议：把 :57 的「150.7 s」删去或改为「see its
  c_total_s」（与第 6 条同式）。不影响任何断言真值，不阻挡接受。
- 除上述外无其他新问题：NOTES 正文（§0-§8）除更正块追加 8 行（:51-57）外未动
  （行号整体平移 8，各节首行与关键句抽查一致）；review_record 的 Round 2 记录与
  本人第 1 轮复审结论一致转述。

## 3. 复审结论

Round 2 的唯一修补（docstring 540→480）已正确落实，等长替换、无任何其他字符变化，
重跑全过且计数确定。第 1 轮的全部发现（1 MEDIUM + 4 LOW + 2 INFO）与第 2 轮的
docstring 项至此全部关闭。唯一新注意到的是更正块 Round 2 条目中 shipped json 墙钟
秒数（150.7）与实际（153.3/150.6）的时效性出入——nit 级、非承重、一句话可修。

**复审刻度：1. closed in all states**（全部修补落实；无承重保留意见）。
