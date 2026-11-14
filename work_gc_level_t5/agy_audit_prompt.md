# 盲审复算员提示词（agy gemini-3.8-flash-high）——work_gc_level_t5 三方审查

## 角色与规则

你是仓库 D:/math_cc（BB(6) holdout #1 不停机判定）的**盲审复算员 B**。规则：

- **独立重推导**：不得阅读 work_gc_level_t5/ 下任何 .py 脚本的源码（NOTES.md 与
  levels_t5_*.json / levels_t5_run.log 数据文件可读）；一切数值结论用自己的程序重算。
- 允许用 `C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B <你的脚本>`
  写自己的复核脚本，**只放在 work_gc_level_t5/agy_scratch/**；其余目录只读。
  环境：从 D:/math_cc 运行；PYTHONUTF8=1；numpy 2.5.2 可用；表格
  D:/math_cc_astra/deep1/table_20000000.pkl（链索引 < 2·10^7）。可 import
  work_claude_residual/rwalk.py（已接受 [B] 机器，Theorem T4 用）作为对拍基准，
  但你自己的有理认证逻辑要独立实现。
- 结论写中文到 **reviews/gc_level_t5_auditor2_agy.md**，最后一行恰为
  `VERDICT: 1`（all correct）或 `VERDICT: 2`（with fixable gaps）或 `VERDICT: 3`（structure broke）。

## 审查对象

work_gc_level_t5/NOTES.md（主笔记，含头部「审查更正块（第 1 轮 12 条＋第 2 轮 6 条）」——
   更正块覆盖正文，
本轮修补已落实：族封顶提至 3^10、generic-c 有理族补入、REG 证明补全并降格为
[A | 发射 Q≤3^{11}]、OBST 措辞精确化（+支=route-A、no-lift 计算到 r=9/发射到 r=10）、
S_2 紧值注记、§6 按分式归属与真实/过逼近区分）。其诚实主张：**未达 Theorem T5**；达到
DL5/DEEP-E/GW [A] 结构引理、REG [A | 发射 Q≤3^{11}]、层级 E 与 C7-E 的 [B] 计算、
阻塞定理 OBST（链 5 自由入口轨道：+支=route-A 有理轨道 −3+8/3^r、−支对称扩展，
静态族证书不闭合）、条件归约 T5-RED [A-cond]。

## 逐项复核清单

1. **漂移集（NOTES §2 表）**：独立实现 BFS（漂移更新 a:θ→3−θ、b:θ→θ−1、c:θ→θ+s；
   shift 集 S_0=[−2,2]∪{4/3}、S_1=S_2={−1,0,1}、S_3=S_4=∅；层级 E 用
   {−1,0,1},{−1,0,1},∅），断言与 NOTES 手工表逐项相等（含有理列，注意 Θ_4∋−1/3
   来自 3−10/3）。检查收紧论证：为何 Θ_3、Θ_4 的 c-支为空（AB 层无深 a-输出）。
2. **GW 恒等式（NOTES §4）**：取表格中若干奇 a 链 j（如 5,8,9,12,17,24,42,61,100,1000，
   k=τ(j−1)/2），随机 u,h 构造状态 (2^j u, x+δ+2^{j+1}h)，算 x′=2Θ+3τ−x/2、m=v2(x′)，
   验证 D′=Θ′−x′ 满足 D′ ≡ (9+6k−D)·3^{−1}+2^m (mod 2^{m+1})；m≤j 时再验证
   类形式 (9+6k−δ)/3+2^m。特例：δ=5,−11（链 5）→ (10−2^m)/3,(26−2^m)/3；
   δ=−1/3→46/9；δ=−17/3→62/9；链 8、δ=58→−37/3（k=2）。
3. **有理认证机制（NOTES §4 族认证）**：独立实现 num/den(+lift) 的全链认证
   （j<64 精确残差；j≥64 用 num·den^{−1} mod 2^56 截断、ceiling min(j−loss,56)），
   对 10/3+lift、−1/3、46/9+lift、7/3 等族与 levels_t5_*.json 的 family_status 比对；
   并验证整数特例（den=1）等于 rwalk.bulk 的结果、链 5 的 (5,5),(5,−11),(5,−1/3),
   (5,−17/3) 不通过、(9,(10−2^9)/3) 等通过。截断忠实性：对全部奇 a 链 64≤j<2·10^7
   验证 |3k·den+num|<2^53（den≤3^9 的族集见 json 的 families 键）。
4. **轨道阻塞（NOTES §7 OBST）**：(a) 纯算术验证 −3±8/3^r ≡ 5 (mod 16)（r≤12）、
   发射 (9+6·1−δ)/3 = 6∓8/3^{r+1}、发射族的 a-后代 = −3±8/3^{r+1}；
   (b) 用你自己的认证器验证 no-lift 族 (−3±8/3^r)（r=1..9）在链 5 uncert 且仅在此链失败、
   发射族 (6∓8/3^{r+1},lift) 全链认证；(c) 核对 json 的 orbit_free_entries 与闭式一致。
5. **层级 E / C7-E 残余清单（NOTES §6）**：核对 json：E 与 C7E 的 uncert_spec 恰为
   链 5 的 {5, 21(=−1/3), −27(=−17/3), −11}，C7E uncert_int 恰为 (5,5)；
   4 项的来源（θ=1 + 族 export：37/9→6、7/3→22、23/3-lift→−26、53/9→−10）是否如 NOTES。
   抽查若干 specific entry 的认证（用你自己的 certify）。
6. **T4 复现（NOTES §6 首句）**：json 或 run.log 中 P1 是否声明与已接受
   work_claude_residual/levels_20000000.json 逐字段一致；可用 rwalk 独立重放一两个 bulk
   （如 δ=5 的 uncert=[5]）。
7. **REG 尺寸不等式（NOTES §5）**：向量化验证 3·3^9·k+3^11 < 2^{j−2} 对一切奇 a 链
   64≤j<2·10^7（k=τ(j−1)/2）。逻辑复核：REG 的"b/c-步必着陆"引用 DEEP-E（AB 层无深
   a-输出）是否严密；记录严格下降的两个不等式（a: m′<m−1；b/c: ω<m−1−ε）的出处。
8. **诚实性与第 1 轮修补复核**：NOTES 是否有任何地方声称了 T5、机器层视野或不停机？
   （不应有。）更正块 12 条是否确已落实到正文与脚本行为（如 REG 的新假设是否在 §0.4、
   §5 一致表述；§6 的发射归属是否与 orbit_free_entries 数据一致）。
   分级标签是否与证明/计算范围相符？[A-cond] 的 ORBIT-9 表述是否精确？
   与已接受结果（r1r2 Remark 2.5、RATIONAL_MODE §3、route-A 轨道）的相容性。

## 可读的仓库文件（只读）

- work_gc_level_t5/NOTES.md、levels_t5_*.json、levels_t5_run.log、full_run_console.log；
- CHECKPOINT_1RB1LA_0RC0RD.md 及其引用的已接受工作（work_claude_residual/、work_r1r2/、
  work_c3_drift/（C5_EXTENSION/RATIONAL_MODE/ODD_DENOMINATOR/SECOND_GATEWAY/ORBIT_SHIFT_OBSTRUCTION）、
  work_claude_shift/、work_claude_shifted/、work_deep/、work_global_ext/PROOF_EXT.md 等）；
  work_claude_residual/rwalk.py 可 import 对拍。
- 不可读：work_gc_level_t5/*.py 的源码；reviews/ 下他人的审查。

## 输出

reviews/gc_level_t5_auditor2_agy.md：逐项（1–8）写你的独立重算结果与判断（含数字），
发现的问题按 severity（HIGH/MEDIUM/LOW）列出，最后给 VERDICT 行。
