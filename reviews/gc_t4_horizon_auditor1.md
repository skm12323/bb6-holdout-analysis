# 盲审复算（auditor 1, R1）：work_gc_t4_horizon — Theorem H-T4（EXT(<T4) 视野的机器层迁移）

审查人：复算员A·R1（ZCode GLM-4.6 盲审复算员），2026-11-10。审查对象
`work_gc_t4_horizon/NOTES.md`（逐节）。未读 `verify_t4_horizon.py` 源码；全部复算用自写脚本
（`work_gc_t4_horizon/aud1_scratch/aud1_hinq.py`、`aud1_ord.py`、`aud1_machine.py`，
解释器 `C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B`，从 D:/math_cc
运行，全部整数运算、无浮点）。已接受文档只读引用（行号见下）。

## 0. 逐项复核结果

### (1) Lemma HINQ（NOTES §1 末，行 59-66）— 成立，证明含一处笔误

- 结论本身成立：`3(H−1)²+4 < 2^H` 对 H=16..4096 精确复算通过；步恒等式
  `L(H+1)=L(H)+6H−3` 通过；派生式 `3(H−2)²+7 < 2^H`、`3(H−2)²+4 < 2^H`、
  `(v−1)² < (2^H−4)/3 (v ≤ H−1)` 全部通过（aud1_hinq.py，输出 ALL PASS/exit 0）。
  底数 H=16：3·225+4=679 < 65536，手核一致。H=T4>2^64≥16 的使用合法（见 (2)）。
- **笔误（LOW，可修补）**：`6H−3 < L(H)` 等价于 `3H²−12H+10 > 0`（NOTES 写
  `3H²−12H+14 > 0`，差 4）。正确二次式判别式为 +24（根 2±√6/3），在 **H=2 处为负**
  （6·2−3=9 > L(2)=7），并非"disc −24 < 0、对一切整数成立"。对 H ≥ 16 无影响
  （H≥3 即成立），但 §6(a) "the slack 6H−3 < L(H) … checked for all integers H = 1..3999"
  的口径若直检 6H−3<L(H) 在 H=2 必失败——需把文本改为 `3H²−12H+10 > 0`（对 H≥3 与
  H≤−1 成立，仅 H=2 例外、与归纳无关）。
- 附带：STATE-CLOCK 支线需要的 `6ρ²+3ρ+4 < 2^ρ`（ρ>10^8 时 3s₀+4<2^ρ）在 ρ=23..4096
  精确成立且单调（我的脚本 H6 检查）。

### (2) Lemma ORD（NOTES §2）— 八个序关系全部为真；但 §2 印刷的 K 系列上界是错的

自实现纯塔比较器（`('i',n)/('p2',E)` 表示，int 对塔用 bit_length 精确判定，自测
全部组合对 0 失配，含相等边界），对每个中间步骤做精确整数断言。结果（aud1_ord.py，
ALL PASS/exit 0）：

**T1<K、T2<K′、K′<T3、T3<K_clock、K_clock<T4、K′<K_clock、T4>2^64 全部精确成立**，
与 residual 审查的确认（reviews/claude_residual_review_record.md:15）独立一致。我的界：
2^9999998<T1<2^9999999；2^(2^9999996)<T2<2^(2^9999998)；2^(2^(2^9999994))<T3<2^(2^(2^9999998))；
2^(2^(2^(2^9999990)))<T4<2^(2^(2^(2^9999998)))；2^(2^499996)<K<2^(2^499997)；
2^(2^(2^499996))<K′<2^(2^(2^499997))；K_clock 下界 >2^(2^(2^(2^499495)))（作者的印刷下界，
我验证为真）。

- **错误（MEDIUM，可修补）**：NOTES §2 行 84-86 印刷的三个上界
  `K < 2^(2^499497)`、`K′ < 2^(2^(2^499497))`、`K_clock < 2^(2^(2^(2^499497)))` 与定义
  矛盾：log2 K = 2^499997−2，而 2^499997−2 ≫ 2^499497（指数 499997 > 499497），
  三个上界全部为假（我的脚本对三个命题给出 False/False/False；三个印刷**下界**全部为真）。
  顶数应为 499,996/499,997 一档而非 499,496/499,497。用修正界
  （上界 2^(2^499997)、2^(2^(2^499997))、2^(2^(2^(2^499997)))）后全部序关系仍然成立
  （499,997 < 9,999,990 与 499,997 < 9,999,994 等比较我已精确验证），故 Lemma ORD
  本身不受影响；但 §2 声称"every intermediate step is an exact integer inequality"，
  所印的界却不能是其脚本实际断言的内容（否则 [b] 不可能 PASS）。需要更正 §2 的
  Bounds used 三行，并建议作者核对脚本内实际常数。

### (3) Lemma EXT-T4（NOTES §3）— 成立，无循环

- 三区间 2≤J<K′（I-4）、K′≤J<K_clock（EXT-CLOCK）、K_clock≤J<T4（Theorem T4）恰好覆盖，
  假设一致：三者都是"F 定义到 τ(J−1) 含该步"。引文核实：I-4 = PROOF_EGX §3:158-161；
  EXT-CLOCK 按 I-4 读基 = PROOF_CLOCK_HORIZON §3:89-92（"J<T is the accepted base I-4"）；
  T4 净表述 = work_claude_residual/NOTES.md:79-81（"for every J with K_clock ≤ J < T4 and F
  defined through tau(J−1), S(J) is tie-free"，相对已接受 EXT(<K_clock) 与导入）。
- **无循环性成立**：T4 证明内部对 source epoch 的 tie-free 需求由 DL(i)/(iv)
  （residual NOTES:162-163, 174-177）全部落 Q<T3；shallow crossing 的 Q<G(N0)<60、
  BBBA 家族 T1≤Q<T2 经 Theorem RA 吸收（RA 的唯一 F 假设是"F 定义到 τ(J−1) 含该步"，
  PROOF_CLOCK_HORIZON §1 第 2 条行 17-19、PROOF_EXT §2 Theorem RA 行 83-90 均核实）；
  C5_EXTENSION §4 的归纳在单个 S(J) 内部（≤4 deep 步）而非对 J。由 ORD 的 T3<K_clock，
  全部 source 落在区间 1-2（无条件逐 J 陈述），不需要对任何 J′∈[K_clock,J) 用 EXT。
  residual 审查更正块第 7 条与 reviews/claude_residual_review_record.md:29-31 的接受语
  与此一致。**未发现对 J′∈[K_clock,J) 的 EXT 使用。**
- 终止条款（偶返回、≤max(0,J−2) 链）= PROOF_EGX §5:206-208，引用正确。
- 小注（LOW）：陈述限定 J≥2，而 H-T4(i) 在 exit chain 处按 J 引用它；J=1 的 epoch 无
  exit chain（S(1) 在链 0 的 return 即偶返回：X(0)=起点 A=(1,1)，H=M_{u0}(A_X(0))=(1,1)
  偶；我的机器数据：H0=20/22 全部 42,569/170,274 个 J=1 fire 均 r=0）。正文宜补一句。

### (4) Lemma DATA-T4（NOTES §4）— 成立

(a) 恰为 PROOF_EGX §1:53-56（"X(m), m ≤ J−1 … chains at steps ≤ τ(J−1) inclusive，
b/c 首返回复制 F 在 τ(J−1) 那步的链"）+ §3:163-171 import audit（"None uses the pointer ρ
or any F step after τ(J−1)"）的内容，逐句核实一致。(b) C1 的"every reached crossing，
without an exit-length or C2 hypothesis"（PROOF_CLOCK §3，行 110-118）适用于已到达的
X(J−1)（F 定义到 τ(J−1) 含该步）。(c) 数值链 (J−1)² ≤ (T4−2)² 且 3(T4−2)²+4 < 2^T4
（HINQ 于 H=T4>2^64≥16）成立。该引理使 H-CLOCK 原来一笔带过的"replay source X(J−1) is
earlier and defined"的反循环记账显式化，定位正确。

### (5) Theorem H-T4 (i)（NOTES §5）— 成立

逐条对照 PROOF_EGX §5:215-226（Theorem U(b)）：
- 只有 level fire 与 exit chain 可能破坏 S1（PROOF_M Cor 3.5:113-115）；内部步是
  M_u-像（Lemma 2.1-2.3）——引用正确，替换 I-4→EXT-T4 后每个环节仍是已接受内容。
- level fire 的 J<ρ：ρ≤10^8 用审计基 V2（PROOF_EGX:217-218；verify_m V2 到 i=10^8，
  89,213,562 步，PROOF_M §4）；ρ>10^8 用 STATE-CLOCK（PROOF_CLOCK §4:133 τ(n)≤nP(n) +
  INC P(n)<2n+1 ⟹ s₀<ρ(2ρ+1)，再 6ρ²+3ρ+4<2^ρ ⟹ 2^J ≤ 3s₀+4 < 2^ρ）——与 U(b):217-219
  逐字同型，且 6ρ²+3ρ+4<2^ρ 我已精确验证（H6）。
- exit chain 裕度 σ_{t′}−j_{t′} = (ρ−J)+h_{t′}，其中 j_{t′}=v2(β)、v2(α)=J−Γ_{t′}
  （Lemma T(1)，经 TR 迁移）、σ_{t′}=ρ−Γ_{t′}（PROOF_M Lemma 3.2）——代数核对无误，
  ρ−J≥1 与 h≥1 给出裕度 ≥2。
- **严格性 τ(J−1) < τ(ρ)=s₀ 的论证：我独立重推导并机器验证。**从 G6 §5.1 的状态结构
  （每步恰读 (A,b,c) 三项；list = [A]+P+[E_i,…]）：E_m 与 E_{m+1} 同步首读 ⟺ 该步
  P=∅ 且 i=m（b=E_m、c=E_{m+1}），此时从 X(m) 看是 a 型、从 X(m+1) 看是 b 型——同时刻
  配对只能是 (a,b)。X(ρ) 是 a 型（level fire，Lemma K(a)：PROOF_EXT:60-66 "type a ⇔ a
  level fire at pointer n"），故 τ(ρ−1)<τ(ρ)，J−1≤ρ−1 给 τ(J−1)≤τ(ρ−1)<s₀。
  机器验证：full pair walk 10^5 步的 44,688 个同时刻对**全部**是 (X(n−1) a, X(n) b)，
  0 例外；τ 严格非降 ✓。
- 终止（偶返回、指针前移 ≥2、epoch 间只有 P=∅ 偶步）= U(b):224-226，引用正确。
- 机器级佐证（我的 λ-walker，见 (7)）：H0=20/22 全前缀每条顶层链 j<σ 断言通过；
  每个闭合 epoch 的 (j_t) 序列与 S(J) 逐项相等（Lemma 6.1 的机器形态）、σ_t=ρ−Γ_t。

### (6) Theorem H-T4 (ii)（NOTES §5）— 成立

对照 PROOF_EGX §3:173-179（Corollary H）逐情形核对：S1/S2/S3（work_r4:18-26）、
A 奇 singleton 不停机（3(n+2) 被 3 整除非 2 的幂，work_r4:11-12 停机判据）、v≤2000 用
Lemma E(v)（Class-A，含 v=1,2）、v≥3 用 D5（PROOF_EGX:34-35）+EGX（§2，对一切奇 w）+
E1–E4（LEMMAS_E）——全部引用正确。I-3 reached-crossing 实例化：(v−1)² 与 (v−1)²+1 均在
前缀 (i) 内（3((T4−2)²+1)+4 < 3(T4−1)²+4 < 2^T4，HINQ），s≤i²（PROOF_CLOCK §4:136）
⟹ i>v−1 ⟹ X(v−1) 已达、τ(v−1)≤(v−1)²<(2^T4−4)/3（HINQ 派生式）——成立。
覆盖论证（每个 n*<2^T4−2 或为 singleton 或落在相邻 singleton 之间、由 excursion 覆盖；
每情形都产生下一 singleton）与 R4 §3 的分解一致。off-by-one 表：horizon 集合读法
{n : n+2 < 2^H} 与 H''（PROOF_EXT:149-153）/H-CLOCK（PROOF_CLOCK_HORIZON:141-145）
一致；首个 v2(n+2)≥H₀ 的 n 恰为 2^H₀−2（纯算术 + 数据 max v=H₀−1，我已验证）。

### (7) [B] 声明的诚实性与独立复算（NOTES §6）— 全部数值精确一致

- 数据一致性：`t4_horizon_checks.json` 与 `extended_run_900s.log` 中 H0=26 的全部计数
  （F 前缀 22,369,619=(2^26−5)//3、ptr 25,074,248、fires 7,594,491、chains 595,760、
  epochs 7,594,490、top 67,108,862=2^26−2、singletons 29,990,130、gap 22,783,474、
  max v 25=H0−1、min margin 3）与 NOTES §6(c) 逐项一致；扩展 H0=28 的计数
  （268,435,454 top / 89,478,483 prefix / ptr 100,296,961 / 30,377,959 fires /
  119,960,495 singletons / 91,133,877 gaps / 420.4 s）与 log 一致。
- **我的独立复算（aud1_machine.py，ALL PASS/exit 0；top map 按 R1 §5、pair map 按
  G6 §5.1、S(J) 按 PROOF_M L6.1+EGX §1、endgame 按 LEMMAS_E §0 全部自实现）**：
  - top map H₀=20 与 H₀=22：前 2^H₀−2 步**无停机**（每步查 A 奇 ⇒ A+2b+3 非 2 的幂 +
    显式 m==1 分支双保险）、sum law 3n+3 每步、singleton 结构、每个 even singleton
    v<H₀ 且 gap==ℓ(v)。H₀=20：singletons=468,602、gap_checks=355,996（even singleton
    共 355,997，最后一个的 gap 越界不检——与作者口径 355,996 吻合）、max v=19；
    H₀=22：singletons=1,874,390、gap_checks=1,423,972、max v=21。**与作者 JSON 完全一致**。
  - ℓ(1..20) = R4 表（work_r4/PROOF.md:40）；ℓ 与终值 3w·2^v+3ℓ 对
    w∈{1,3,5,7,101,2^61−1} 无关。
  - full pair walk 10^5 步（33,948 fires/epochs_closed、2,664 exit chains）：质量
    恒等式 c 和=2^i、λ 和=3s+1 每状态；S1/S2 每链；σ-递归 v2(c_x)=ρ−Γ_t 每个 fire 与
    exit chain（Lemma 3.2 机器级）；ε 公式（a 型 0、b 型 1、c 型 i−σ_t+1）每个交叉；
    τ 严格非降、同时刻对只 (a,b)（44,688 对）；s≤i²；τ(n)≤n² (n<4096)；首链
    x=48U+10、j=1<4 与 G6 §5.1 的例证一致。
  - λ-walker 至 s*=(2^H₀−5)//3：H₀=20 fires=118,665、epochs=118,664、chains=9,309、
    ptr=391,793、min margin=3，逐 J fire 直方图与 v 直方图**逐项等于**作者 JSON；
    H₀=22 fires=474,657、epochs=474,656、chains=37,235、ptr=1,567,149、min margin=3
    同样精确一致；CLOCK s≤i·P(i) 在每个 fire 成立；τ(J−1)≤(J−1)² 每个 fire 成立；
    j<σ 在每条顶层链成立（Theorem 4.1 证书的全前缀形态）。
  - **全部 118,664（H₀=20）与 474,656（H₀=22）个闭合 epoch 的 (j_t) 序列 == S(J)**
    （含 σ_t=ρ−Γ_t），即 PROOF_M Lemma 6.1/3.2 的机器级验证（作者 §6(c) 检查 3 的
    独立重现）。
  - S(J) J=1..32：tie-free、r≤max(0,J−2)、h_t=J−Γ_t−j_t≥1、v2(α_{x_t})=J−Γ_t
    （Lemma T(1) 恒等式）全部通过。
  - endgame E(1,v) v=1..32：D5 状态与 F 逐状态一致（τ(v−1) 相等、v∈{5,10,20,32} 的
    前缀状态全同）；endgame 链与 S(v) **逐链相等**（j 序列与链数）；ℓ(v)=τ(v−1)+
    endgame 步数；终 singleton 对恰为 (2^v, 3ℓ(v))。
  - off-by-one：数据 max v=H₀−1；首个 v2(n+2)≥H₀ 的 n 恰为 2^H₀−2（精确算术检查）。
  - 说明：作者 §6(c) 检查 3 的"own walker == work_m.sym_exit"一项我未做（不读其源码），
    代之以机器级 endgame==S(v) 与 R4 ℓ 表两个独立锚点（强度等价或更强）。
- 范围声明诚实：默认 20-26、扩展 28、明示"模式验证非证明、不依赖 H₀"、full-pair 引擎
  的 ~2·10^6 步限制——均如实。小瑕疵（INFO）：NOTES 称默认预算"total 98-145 s"，随附
  JSON 实为 149.4 s（另一次运行）；"throughput ~1.0·10^6 steps/s" 与 JSON H0=26 实测
  ~6.5·10^5（λ）/8.1·10^5（top）同数量级但偏高。均非承重。

### (8) 越级检查 — 干净

NOTES §0/§7 明示"no claim beyond J<T4、无 T5/全局 EXT*/不停机主张"；视野改动明确写成
"On acceptance … the accepted horizon becomes 2^T4−2"（接受前仍为 K_clock，与
reviews/claude_residual_review_record.md:29-31 一致）；与死路清单无冲突（未使用
AB′/copy principle、NT、CAL-C、DR、C7 字面形式等）。

## 1. 与作者数值的比对总表（我的复算 vs 作者 JSON）

| 量 | H₀=20（我 / 作者） | H₀=22（我 / 作者） |
|---|---|---|
| top steps | 1,048,574 / 1,048,574 | 4,194,302 / 4,194,302 |
| singletons | 468,602 / 468,602 | 1,874,390 / 1,874,390 |
| gap checks | 355,996 / 355,996 | 1,423,972 / 1,423,972 |
| max singleton v | 19 / 19 | 21 / 21 |
| v 直方图 | 全部 19 档一致 | — |
| fires | 118,665 / 118,665 | 474,657 / 474,657 |
| closed epochs | 118,664 / 118,664 | 474,656 / 474,656 |
| exit chains | 9,309 / 9,309 | 37,235 / 37,235 |
| final ptr | 391,793 / 391,793 | 1,567,149 / 1,567,149 |
| min fire margin ρ−J | 3 / 3 | 3 / 3 |
| fire_Js 直方图 | 全部 18 档一致 | — |

另：作者 H₀=26/28 的计数（我未重跑该规模）与其 JSON/log 内部自洽（fire_Js 计数和
=fires、直方图和=singletons−odd 等均核对）。

## 2. 差异及定位（全部为可修补，无结构断点）

1. **[MEDIUM] NOTES §2 行 84-86：K/K′/K_clock 的印刷上界为假命题**（2^499997−2 ≫
   2^499497 等），与"every intermediate step is an exact integer inequality"的自我声明
   矛盾。修补：改为 2^(2^499997)/2^(2^(2^499997))/2^(2^(2^(2^499997)))（下界 499,495/499,496
   可保留，我已验证为真），并核对脚本实际断言的常数。Lemma ORD 的八个序关系不受影响
   （已用修正界独立证明）。
2. **[LOW] NOTES §1 行 62-63：HINQ 步常数二次式应为 3H²−12H+10（非 +14），判别式 +24
   （非 −24），slack 在 H=2 不成立**；§6(a) "H=1..3999" 的直检口径相应修正（H≥3 即可）。
   引理结论（H≥16）不受影响。
3. **[LOW] EXT-T4 限定 J≥2 而正文未注记 J=1 情形**：J=1 epoch 无 exit chain
   （X(0)=(1,1) 偶返回；机器数据全部 J=1 fire r=0）。补一句即可。
4. **[INFO]** 默认预算时长文本（98-145 s）与随附 JSON（149.4 s）小幅不符；吞吐声明
   偏高约 1.5×。非承重。
5. **[INFO]** t4_horizon_checks.json 中 fire_Js 每档第二元素语义未在 NOTES 说明（非承重）。

## 3. 总评

Theorem H-T4 及其两个记账引理（EXT-T4、DATA-T4）的证明结构完好：三分区间无循环
（T4 的 source 全落 Q<T3<K_clock 的无条件区间）、数据局部性闭住记账循环风险、
(i) 是 U(b) 的逐环节替换（fire 的 J<ρ 两分支与 exit 链裕度均引用已接受内容，
严格性论证我独立重推并机器验证）、(ii) 是 Corollary H 的同型归纳（I-3 实例化成立）、
off-by-one 与 H″/H-CLOCK 惯例一致；[B] 部分的全部数值在我的独立实现下精确重现
（H₀=20/22 全表一致，含 593,320 个闭合 epoch 与 S(J) 的逐项相等）。所发现的问题
均为正文层面的可修补错误（§2 界的数字、§1 二次式、J=1 注记、时效性小出入），
不影响任何定理的真值或证明结构。

VERDICT: 2（with fixable gaps）
