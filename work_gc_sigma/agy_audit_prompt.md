# 盲审任务：work_gc_sigma（攻坚 R4：Σ_{<T4} 谱、生成元闭包、一致不变量判定）

你是外部盲审复算员（agy gemini-3.8-flash-high）。请独立复核 work_gc_sigma/NOTES.md 的全部数学声明。
**盲审规则**：独立重推导；**不得阅读 work_gc_sigma/sigma4.py、verify_sigma.py、probe1.py 的源码**（不得以它们
的输出代替你的复核）；可以读 NOTES.md 本身、它引用的已接受仓库文件、以及工件 work_gc_sigma/
sigma4_20000000.json（数据文件，非代码）。允许用 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/
python.exe 写你自己的复核脚本，**只放在 work_gc_sigma/agy_scratch/ 目录**；其余一切只读。numpy 可用
（该解释器实测有 numpy 2.5.2）。从 D:\math_cc 运行。

## 审查对象与逐项复核清单

对下列每项给出「独立重推导成立 / 有可修补缺口 / 结构性错误」之一并给证据：

1. **[B] 基线复现（NOTES §3 表、§5(i)）**。Σ_{≤N0}={0}；Σ_{<T1}={−1,0,1}；Σ_{<T2}={−2..1,3}∪{4/3+2^6}；
   Σ_{<T3}={−3..1,3}∪{4/3+2^m: 5≤m≤24, m=23 不出现}∪{−7/3}（见证读法）。复核方式建议：用
   work_claude_residual/rwalk.py 的 Table/certify/bulk（已接受机器）重算整数 bulk 的 a-输出聚合并按链分类
   剩余类（类−2 的对称代表；分类：v=num/3^e、|v|≤64、lift 位 2^m 于 m∈[5,链]，取 |分子| 最小的 den≤3 表示
   为规范读法）——检查 12@5=4/3+2^5、−20@6=4/3+2^6、83@7=−7/3 等。
2. **[A-imp] Lemma GEN 与 Theorem CLO（NOTES §4）**。逐步核对：入口一步生成（a:3−θ、b:θ−1、c:θ+D−2、
   D 取低层链类集）是否恰为已接受 DL(i)–(iv)/C5_EXTENSION §1/levels.py 层级规划的内容；⊆ 方向的覆盖论证
   （每个 a-输出或深层/着陆生成、或在已认证走步上、或经发射续走）是否只是已接受 T4/T5 机器的重述；
   ⊇ 的两层（walk 层 [B] / crossing 层缺口）是否如实标注。
3. **[B] 紧构造层级 E（NOTES §2 P3）**。D-源界 E0←ABCD、E1←ABC、E2←AB、E3←A 是否与 DL 源界
   （chain-t c-步复制源 <G(j_t)）一致；紧 unc_spec={(5,5)} 与 R3 审查更正块第 11 条对照实验的相容性；
   发射语义（整数入口按精确值、specific 入口按剩余类+e≤4 候选值）的上逼近合理性。
4. **[A-imp+B] 机制链（NOTES §0.3）**。(5,5) 整数入口首次在层级 E 可能（Θ^E_3∋−2 而 Θ^C_1={0,1,2}、
   Θ^D_2=[−1,3] ⟹ 3−θ≤4）；GW 发射 (15−5)/3=10/3；m≤N0（GW(b)：y=j_3<T1）；m=N0 边界的 REG 无 lift
   后代集 {3Q−C, C−Q, C±3sQ}/Q（Q=3）={−1/3, 7/3, 1/3, 10/3, 19/3}；−1/3≡5 (mod 16)（链 5 自由）；
   再发射 (15−(−1/3))/3=46/9；a-后代 3−46/9=−19/9=−3+8/9=δ_2；闭式 δ_r=−3+8/3^r≡5 (mod 16) 对一切 r
   （建议你独立验证 mod-16 同余与递推）。
5. **[B] 不变量判定（NOTES §5，主结论）**。用你自己的分类器对工件 sigma4_20000000.json 的
   sigma['<T1'..'<T4'] 各链剩余类做 Tier-2 存在性测试。**精确判定（务必按此复现，勿用变体）**：剩余类
   (c,s) 通过 ⟺ 存在 (v,m) 使 v=num/3^e（e≤10，|v|≤64）、m∈{无}∪[5,min(c,64)]、
   v+2^m·[m≠无]≡s (mod 2^{c+1})，且 (v,m)∈L＝{(k,无)：k 整数，|k|≤16}∪{(4/3,m)：m 任意（含无）}∪
   {(−7/3,无)}。等价的整数判据（verify_sigma.py 的 in_list_fast，经全量等价核验）：|s|≤16；或
   s≡4·3^{−1} (mod 2^{c+1})（裸 4/3）；或 s≡−7·3^{−1}（−7/3 无 lift）；或存在 m∈[5,min(c,64)] 使
   (s−2^m)≡4·3^{−1} (mod 2^{c+1})。h≤3 应零失败；h=4 应有失败（以工件 rat_<T4 的 n_bad 为准；
   在表内者可按「裸 4/3 退化项 vs 严格候选」分解核对）；Tier-1（fired_shift_ranges 全部键的精确值）中
   den 3 的新值 {1/3, −5/3, 13/3} 与 den 9 的 28/9 是否在；整数并集 [−4,4]（exact_structural [−3,3] ∪
   witnessed_core {−4..1,3,4}）。注意发射剩余类的显式合成范围＝无 lift 族 m<54、带 lift 族 m<64；
   m∈[64,N0) 仅以族证书＋M_h.fired_range 表述（这些值全为 4/3+2^m 型、在候选表内）。
6. **[B] 实现谱（NOTES §7）**。用 rwalk Table 全表重算 odd c-crossing 的 (ω, (−1−λ_Y) mod 2^{ω+1}) 交叉表；
   应恰为 {(1,−1):545, (1,0):37097, (3,0):278793, (5,0):545}（总 316,980）。
7. **基线精确化（NOTES §6）**。可能值读法下 Σ_{<T3}∋2（a-着陆类 4=3−θ_2, θ_2=−1∈Θ^D_2；着陆链可为
   [5,N0)）——检查该论证与「a-着陆是 a-输出」的对应（check_r0(c) 惯例），以及这对接受声明是否公允
   （levels.py 的 sigma 字段不含入口本身）。
8. **一致性与诚实性**。NOTES 是否有任何越级主张（EXT 范围、不停机、视野变化）；[B] 范围标注是否与
   sigma4_20000000.json 的 scope 一致（规范表链 <2·10^7；有理族 56 位截断 bulk j≥64；发射剩余类合成
   m<4096、范围主张到 N0）。

## 可读文件
- 审查对象：work_gc_sigma/NOTES.md（头部含第 1、2 轮审查更正块，覆盖正文）；工件
  work_gc_sigma/sigma4_20000000.json（数据，第 2 轮修补后重跑版；第 2 轮改动＝工件自注动态化、
  family_unc 全量、T1_BAD 含 lift 位——数据内容与第 1 轮版一致）。
- 已接受仓库文件（按需）：CHECKPOINT_1RB1LA_0RC0RD.md 相关节；work_claude_residual/NOTES.md（含更正块）、
  levels.py、rwalk.py、levels_20000000.json、check_r0.py（可自行运行：PYTHONUTF8=1 <解释器> -B
  work_claude_residual/check_r0.py，约 5 s）；work_claude_shift/NOTES.md（Theorem S）；
  work_c3_drift/C5_EXTENSION.md、RATIONAL_MODE.md、SHIFT_TRANSPORT.md；work_gc_level_t5/NOTES.md（含
  更正块）、rwalk_t5.py、levels_t5_20000000.json；work_r1r2（gateway 证书）相关文件。
- 禁读：work_gc_sigma/sigma4.py、verify_sigma.py、probe1.py 源码。禁改：work_gc_sigma/ 与 reviews/ 之外
  一切文件；agy_scratch/ 之外不得写文件。

## 输出
用中文写审查报告到 **reviews/gc_sigma_auditor2_agy.md**：逐项清单结论＋证据（你的脚本输出片段/推导）；
指出任何错误（位置＋性质＋建议修补）。**最后一行恰为**：
VERDICT: 1 或 VERDICT: 2 或 VERDICT: 3
（1=all correct；2=with fixable gaps；3=structure broke）。
