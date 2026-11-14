# 攻击员审查：work_gc_level_t5（LEVEL-T5：EXT 推到 T5 的第五层分析）

攻击员（GLM，R3），2026-11-11。对象：work_gc_level_t5/（NOTES.md、rwalk_t5.py、levels_t5.py、
verify_t5.py、levels_t5_20000000.json、levels_t5_run.log、full_run_console.log、agy_audit_prompt.md）。
审查方式：逐条核对 [A]/[A-cond] 证明与代数恒等式；实际运行 verify_t5.py 与 levels_t5.py（smoke）；
对关键主张做独立数值对抗探测（新随机种子、全量范围补认证、entry 集完备性枚举）。

**总评刻度：2（fixable gaps）**。核心结构结果（GW 恒等式、DL5/DEEP-E 分类、OBST 闭式与轨道
数据、层级 E/C7-E 全量计算、T4 复现）全部复算通过、未发现致命漏洞；T5 未主张、诚实结论属实。
发现的问题集中在三处可修补的完备性/覆盖缺口（发现 1–3，均已被我在审查中用独立计算补验数值
成立，但按提交的文本/脚本不能核验），以及若干低危工程问题。

---

## 一、逐项发现

### F1 [MEDIUM] T5-RED 的 [B] 基座在闭环边界（den 3^10）不全量认证
位置：NOTES.md §7（T5-RED "≤9 层族已 [B] 认证"）、levels_t5.py:302-305（den 上限 3^9）、
verify_t5.py:242-285（check 8：den 3^10 发射族只在 smoke JHI=300003；b/cs 后代不在任何清单）。
理由：ORBIT-9 下第 9 层自由入口 δ_9（den 3^9）的 GW 化解需要其发射族（den 3^10, lift）及其
b/cs 后代在全部链 5..N0 认证；levels_t5.py 的 FAM_SET 封顶 den≤3^9 将它们排除（仅入 FIRE_LOG
——json 中 fire_beyond_cap 恰含 (354302,59049,True) 与其后代），verify check 8 的全量清单只有
den ≤ 27 的 8 族。故"≤9 层族已 [B] 认证"字面不成立。
攻击补验（我运行）：对 12 个 den-3^10 族做全量认证（scalar 5..63 ＋ bulk 64..2·10^7）：
2 个发射族 (354286/59049, lift)、(354302/59049, lift) 与 8 个 b/cs 后代全部 uncert=[]；
a-后代 −177139/59049、−177155/59049（=δ_10^±）恰只在链 5 失败——与 OBST 闭式一致
（δ_10 被 ORBIT-9 假设排除）。故缺口可修补且数值成立。
修补建议：verify check 8 的全量清单加入 den 3^10 的 2 个发射族＋10 个后代；NOTES 补一句该层
认证（或把 cap 提到 3^10 重跑）。

### F2 [MEDIUM] C7-E entry 集静默丢弃有理 θ 的 generic-c 着陆类（4 族未入闭包）
位置：levels_t5.py:355-358（level_entries：`for g in Gp` 循环中 canon 结果为有理时既不入
all_ints 也不 add_fam；对照 a/b 分支 levels_t5.py:349-354 有 add_fam）。
理由：S(J) 的有理漂移 θ（Θ_S 的 C/3 列）配 generic 源 g∈{0..4} 的 c-着陆类 θ+g−2 为有理数，
需要族认证；该分支被静默丢弃。完备性影响"[B] 残余恰为链 5 集"与 T5-RED 的着陆分类完备性。
攻击补验（我运行）：枚举全部所需类——19 个有理 θ+g−2，其中 15 个恰已在 122 族闭包内，
4 个缺失：−10/3、−8/3、14/3、16/3。对这 4 族做全量认证（5..2·10^7）：全部 uncert=[]——
数值良性，但提交物从未认证或列出它们。
修补建议：level_entries 的 generic-c 分支对有理结果调用 add_fam；重跑（或至少补认证）后
"残余恰为"的完备性才闭合。

### F3 [MEDIUM] REG（[A]，"无条件解决 RES 残余"）的书写证明覆盖不全
位置：NOTES.md §5。
理由：(i) 尺寸不等式 3Q·(m−1)P(m−1)/2+|C|<2^{m−2}（Q=3^r）隐含假设 r ≲ 0.63m，未声明；
在无界塔深（记录预算允许 r 至 ~J/(3log2J)，远超 0.63·T4 ≥ 0.63m）时字面失效。
(ii) y=J 情形发射 m∈[N0,T4)（§5 括号自己承认存在）未写出处理："≤3 步回浅区"只对 m<T2
证明；m∈[T2,T4) 需 log*-型坍缩链（每 a 步 m→≈log2 m+1.6r，~5-6 步离深区）。
(iii) 使 (i) 实际无害的关键计数论证——深火塔层数 O(1)（浅链 <64 不能深发射：m<G(64)+1≈15；
深链单步输出 ≈log2 m；故 r 在深链处 ≤~10 « 0.63·N0）——完全未写出。
判断：结论本身应为真（我核过坍缩算术：首次深发射的类 den≤9——bare tie 5/−11 与 spec 自由
类 −1/3/−17/3；此后的火全部 <64 由表格族覆盖；中段分支火每层坍缩链规模），但按提交文本
无法核验，[A]＋"无条件"标签超前。
修补建议：补写 (ii)(iii)（约半页），并把 (i) 写成显式引理（r ≤ 0.6m 于一切深火链，由
坍缩计数供给）。在补写前把 REG 降格为依赖"深火塔深 O(1)"的引理。

### F4 [LOW] family_cert 丢弃族在链 5..63 的 scalar aouts
位置：levels_t5.py:253-268（family_cert 只保留 bulk B['aout']，scalar 部分 c['aouts'] 丢弃；
对照已接受 T4 机制 levels.py:43-50 对整数族聚合 scalar＋bulk 两部分）。
理由：小火（发射链 m<64，如 SECOND_GATEWAY 的 (7,46/9)）真实存在，其 walk 的 a-输出是潜在
source export；被丢弃则 consumer spec entry 集可能不全。
攻击补验（我运行）：122 族在 [5,64) 的全部 scalar aouts 与 bulk aouts（smoke 64..3·10^5）
比对：仅 1 个新键 (chain 7, res 206=−50)，且它是 NT 步的代表元伪影（该族 δ_7^− 在链 5 的
NT 发射之代表元输出；真实发射类 mod 2^8 应为 14=fired 族类，已覆盖——这正是 GW m>j 情形
类形式需要两步来源、代表元类不可靠的体现）；由 (7,−50) 生成的全部 consumer entry（θ∈
Θ_E∪Θ_S 全表）我逐一认证通过。数值无害。
修补建议：聚合 scalar aouts 但排除 NT 步输出（代表元类不可靠）；或注明覆盖论证。

### F5 [LOW] verify_t5.py 的独立性与覆盖弱于 NOTES 宣称
位置：verify_t5.py:287-295（check 9 只读 json 断言残余，非独立重算 entry 集）；
verify_t5.py:271-284（check 8 全量清单不含 18 个轨道 no-lift 族——全量结论只能由
levels_t5.py 运行日志反推：ORBIT 键全在链 5、family_status 无 bulk 失败）；NOTES §6 宣称
"bulk 与 scalar certify 在 64≤j<3·10^5 交叉一致"而 check 5 只做 [64,3000)。
攻击补验（我运行）：bulk==scalar 于 [64,3·10^5) 对 3 族（10/3+lift、46/9+lift、7/3）复核
0 失配——NOTES 宣称范围成立，但 verify 未覆盖到。
修补建议：check 9 改为至少重放若干 spec entry 的构造；check 8 全量清单扩容；check 5 扩到
3·10^5 或改 NOTES 措辞。

### F6 [LOW] certify_families 的 bulk 失败发射路径不可靠（当前空转）
位置：levels_t5.py:333-339：`for j in d['unc_b'][:4]` 把 56 位截断值当精确 δ 发射（真实发射
类需 δ mod 2^{m+1}），且只发射前 4 个失败。实际运行 122 族 bulk 失败为 0（我核过
family_status 全空），路径空转。若未来有 bulk 失败需先修此逻辑。

### F7 [LOW] OBST 轨道标识与 r 范围的措辞精度
(a) "恰为已接受 route-A 有理轨道 −3±8/3^r"：已接受的 route-A 轨道是 +支 c_r=−3+8/3^r
（ODD_DENOMINATOR.md:95、ORBIT_SHIFT_OBSTRUCTION.md:36 均只此式）；−支是对称扩展
（计算证实同样阻塞），把 ± 都说成"已接受对象"略过头（§7(c) 用单支表述正确）。
(b) "r≤10 逐层计算证实"：no-lift 族只计算到 r=9（den≤3^9 上限）；r=10 的 no-lift 链 5 失败
未直接计算（我已补：δ_10^± 全量范围恰只链 5 失败，见 F1），由闭式推出。建议措辞
"r≤9 计算证实＋闭式对一切 r"。

### F8 [INFO] 审查附带影响（披露）
我的 smoke 复现运行 `levels_t5.py 300003`（exit 0，12.7 s）覆盖写了 levels_t5_run.log 与
levels_t5_300003.json。已用 full_run_console.log 恢复 run.log（原 1505 字节 vs 恢复 1553
字节，行内容相同、疑行尾差异）；smoke JSON 因计算确定性内容等价（残余、122 族、轨道键与
提交的全量产物一致）。git status 中 work_claude_residual/r0_checks.json 的修改在我开始前
已存在，非本次审查所为。

---

## 二、我独立复核/复算过的内容

1. **verify_t5.py 全套**：`PYTHONUTF8=1 C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -B work_gc_level_t5/verify_t5.py`（自 D:/math_cc）——10 项全 ok、ALL PASS、exit 0，103.6 s。
2. **GW 恒等式**：(i) 代数手推：由 D′=3−D−x/2 与 x′=3·2^{j−1}u+2D+6k 消去 x 得精确恒等式
   3D′=9−D−x′+6k；mod 2^{m+1}（x′=2^m·奇 ⟹ −x′/3≡2^m）得 D′≡(9+6k−D)·3^{−1}+2^m。类形式
   (m≤j) 由 D≡δ mod 2^{j+1} 即够；m>j 需两步来源（r1r2 Lemma 2.3 的替换 9k+θ+12≡2^m 正是
   使 D 的未知高位消去——与 work_r1r2/NOTES.md:180-260 逐式核对一致）。
   (ii) 独立随机对拍（新种子 987654321，12 链×9 类×200 试，含 h∈[−1000,1000) 扰动）：
   1400 个 m≥j−1 状态（491 个 m>j）精确-缺陷形式零失败。
   (iii) 锚点：k_5=τ(4)/2=1、k_8=τ(7)/2=2（表格直读）；(15−5)/3=10/3、(15+11)/3=26/3、
   (15+1/3)/3=46/9、(15+17/3)/3=62/9、(21−58)/3=−37/3 手算与 SECOND_GATEWAY 一致。
3. **漂移集**：手推 Θ_S 全表（Θ_1=[−1,3]∪{7/3}；Θ_2=[−2,4]∪{2/3,4/3,7/3,10/3}；
   Θ_3=[−3,5]∪{−1/3,1/3,2/3,4/3,5/3,7/3,10/3,13/3}；Θ_4=[−4,6]∪10 项——含 Θ_4∋−4/3 来自
   3−13/3、−1/3 来自 3−10/3）与 Θ^E 全表，和 BFS/手工表逐项相等；shift 集的尺度论证核对
   （t=0 源<T4 用 DE=[0,4]∪{10/3}；t=1 源<T3、t=2 源<T1(层级A, GA=∅)、t=3/4 空——与
   T4 DL(iii)-(iv) 及 levels.py 的 GB/GC/GD 一致）。
4. **DEEP-E**：层级 D 深链仅 0,1,2（j_3<N0），深 a-输出={2}∪{3−θ:θ∈{0,1,2}}={1,2,3}；
   层级 E 深链 0..3，深 a-输出 [0,4]（链 2 的 3−[−1,3]）＋链 3 (θ=−2) 弹射 m<G(j_3)+1≤N0
   故深者仅 m=N0 类 10/3+lift——逐条核对塔界 j_t<T_{5−t}。
5. **OBST 闭式**：δ_r^±≡5 (mod 16)（r≤24 独立算术验证）；发射 (15−δ_r^±)/3=6∓8/3^{r+1}；
   a-后代 (3Q−C)/Q=δ_{r+1}^±；与 json orbit_free_entries（'5,3^2'..'5,3^10' 各 2 条，
   如 −59041/19683→354286=6·3^10−8）一致；与 ODD_DENOMINATOR §3 的 c→(c−6)/3 自 c_0=5
   轨道核对一致。
6. **残余清单与溯源**：json E/C7E uncert_spec 恰 {(5,5),(5,21),(5,−27),(5,−11)}＋int (5,5)；
   θ=1+D−2 溯源（D=6←37/9 族、22←7/3 族、−26←23/3-lift 族、−10←53/9 族）算术核对；
   21≡−1/3、−27≡−17/3 (mod 2^6) 核对；GW 化解四族 10/3、26/3、46/9、62/9（lift）全量认证
   （check 8；我另独立复跑）。
7. **截断忠实界**：对**全部 122 族**（不止 check 6 的 32 族）在全部奇 a 链 64≤j<2·10^7 验证
   max|3k·den+num| = 526797150452 < 2^53（最坏族 177155/19683）。
8. **family_status**：122 族无 bulk uncert、无非链 5 的 scalar uncert；18 个轨道 no-lift 族
   （r=1..9 两支）在列。
9. **smoke 复现**：`levels_t5.py 300003` 重跑 exit 0（12.7 s），残余 spec/int、122 族、
   轨道键与全量产物完全一致（specific 计数随范围缩小如预期 1433/1604）。
10. **bulk==scalar** 于 [64,3·10^5)（3 族 0 失配）——NOTES §6 宣称范围的独立复核。
11. **F1/F2 补验**：den-3^10 层 12 族与 4 个缺失 generic-c 族的全量认证（结果见上）。
12. **F4 探测**：122 族 scalar aouts vs bulk aouts（smoke），唯一新键 (7,−50) 的后代 entry
    （Θ_E∪Θ_S 全表 × (−50)）逐一认证通过；并核实该键为代表元 NT 伪影（真实类 14）。
13. **诚实性**：NOTES 无任何 T5、机器层视野、不停机主张；"未主张"清单与实际相符；
    未使用已反驳对象（AB′/copy、C7 字面、DL-下降）——§1/§8 声明与正文用法抽查一致。
14. **导入核对**：r1r2 Theorem 2.4（5≤m<10^8 证书）与 Remark 2.5（m≥10^8 残余 [C]）存在于
    work_r1r2/NOTES.md:254-280；route-A 轨道引述存在于 work_c3_drift/ODD_DENOMINATOR.md:95、
    ORBIT_SHIFT_OBSTRUCTION.md:36；T4 层级 json 与 levels.py 机制（levels_t5.py P1 逐字段
    断言＋全量运行通过；verify check 7 锚点＋δ=5 全量复跑）。

## 三、总评

诚实框架（T5 未达、OBST 阻塞、T5-RED 条件归约）与主要计算经得起对抗复算：GW 恒等式、
漂移集、OBST 闭式、层级 E/C7-E 残余、T4 复现全部独立确认。三个 MEDIUM（F1 闭环边界
[B] 基座、F2 entry 集有理 generic-c 丢弃、F3 REG 证明覆盖）都是可修补的完备性缺口——
F1/F2 的数值部分我已用全量认证补验成立，F3 需补写约半页坍缩计数论证。无致命漏洞。
刻度：**2（fixable gaps）**。

---

# 第 1 轮定向复审（2026-11-11，攻击员）

复审对象：修补后的 work_gc_level_t5（NOTES.md 2026-11-11 16:52 含 12 条审查更正块；
levels_t5.py 03:47；verify_t5.py 16:47；全量重跑产物 16:35——run.log 显示新全跑
46074 s、P1 T4 复现断言通过）。

## 修补逐条核验（对照我方 F1–F7）

* **F1（MEDIUM，闭环边界）——已修，实测确认。** add_fam 封顶提至 3^10
  （levels_t5.py:314 `if den > 3 ** 10`）；新全量重跑：族集 122→**134**，轨道 no-lift
  族 r=1..10 共 20 个入集（我从 json 独立核对 20/20），orbit_free_entries 新增
  '5,3^11' 键（δ_10 的发射，den 3^11 入 FIRE_LOG=36 条——阻塞数据，与 OBST 一致）；
  verify check 8 全量清单扩至 **38 族**（含 18+2 轨道 no-lift、den-3^10 发射对＋
  10 后代）。**verify_t5.py 实跑**：`PYTHONUTF8=1 …Python312/python.exe -B
  work_gc_level_t5/verify_t5.py` 自 D:/math_cc——11 行检查全 ok、ALL PASS、exit 0、
  328 s（NOTES §9 写 ~280 s，量级相符）；check 8 报 "38 families at FULL range
  incl. den-3^10 layer"。ORBIT-9 所需的 den≤3^10 层现已有全量 [B] 认证。
* **F2（MEDIUM，generic-c 有理丢弃）——已修；且我方原探测需自我更正。** 代码已加
  add_fam（levels_t5.py:368-372）。重跑后族数 122+12（12=den-3^10 层）——generic-c
  分支未新增族。我用**正确的按 t 源层级结构**（t=1: GABCD={0..4}；t=2: GABC={1,2,3}；
  t=3: GAB={2}；t=4: GA=∅——出自 T4 DL(ii) 尺度论证，与 levels_t5.py PLAN_S 一致）
  重算可达有理 generic-c 类：恰 8 个，**全部在新 134 族集中（缺失=∅）**。我第 1 轮
  探测对一切 t 用 g∈{0..4} 是过逼近——所flag的 4 类（−10/3、−8/3、14/3、16/3）在
  正确结构下**不可达**（如 16/3 需 θ=10/3 配 g=4，但 g=4 只在 t∈{0,1} 而 10/3∈Θ_2..Θ_3）。
  结论：原代码的丢弃是潜在脆弱性而非实际漏洞；修补正确且现以构造保证完备。
* **F3（MEDIUM，REG 书写）——实质已修，余两处文字残留。** §5 重写为 REG-Size
  显式引理（r≤0.6m−25；我在边界数值复核：m=780,r=443 时 log2(LHS)=723.5<778、
  m=1000,r=575 时 933.1<998、m=N0,r=11 时 55≪2·10^7——0.6m−25 形式在边界成立）、
  G-坍缩链（≤4 步，覆盖 y=J 的 m∈[N0,T4)）、m≥T2 的 c-步尺寸界、深回归次数 O(1)
  计数；标签改 **[A | 发射 Q≤3^{11}]**（§0.4、§5）。**残留（见 R1/R2）**：
  顶部"诚实结论"块与 §8 仍写"无条件解决"，与更正块/§0.4/§5 矛盾；REG(e) 的
  "此后自由入口的 provenance y<64，发射 m<16"应为 y<N0（链可落在 [64,N0)）——结论
  不变（m<G(y)+1≤G(N0)+1≈52 仍浅），但字面错误。
* **F4（LOW，scalar aouts）——已修。** family_cert 现聚合链 5..63 的 scalar aouts
  并排除 NT/攀登输出（levels_t5.py:261-269 `if c2 in ntout or c2 >= j+1: continue`）。
  副作用检查：E/C7E specific 计数 2133→2315、2372→2554（新出口进入），残余清单不变
  （json 核对：链 5 的 {5,21,−27,−11}＋int (5,5)）。注：`c2 in ntout` 可能误删与
  NT 输出同链号的合法 aout（过删方向安全），实测无影响。
* **F5（LOW，verify 覆盖）——已修。** check 5 扩为 [64,3000) 全量＋[3·10^3,3·10^5)
  抽样 2000 链（诚实标注"sampled"）；check 8 全量扩容（见 F1）；新增 **check 9b 重放**：
  从 14 个族的出口重建 t=0 spec entry（θ=1）280 项逐项认证，失败集恰为链 5 的
  mod-16=5 类 {5,21,37,53}（=−27/−11 的 mod 64 像）＋已知 (8,58)——实跑通过。仍非
  全独立重算（14 族、θ=1、smoke 出口），但已是实质性重放。
* **F6（LOW，bulk 发射路径）——已修（休眠路径）。** 现按精确类 Frac(num,den) 发射
  无截断（levels_t5.py:346-351），注释标明 provisional/dormant；本次运行 bulk 失败
  仍为 0（family_status 全空，我核对）。小注：lift 族的发射未计入 2^j 位——休眠中
  无碍，若启用需补。
* **F7（LOW，OBST 措辞）——已修。** §7(a) 明确"+支＝已接受 route-A；−支对称扩展"；
  §7(b) 改为"no-lift r=1..9（den≤3^9）、发射 r=1..10（den≤3^10）、闭式对一切 r"。

## 复审新发现（第 1 轮）

* **R1 [LOW] 顶部诚实结论与 §8 的"无条件"残留**：NOTES.md:47（"REG——后者把 r1r2
  Remark 2.5 的 RES 残余在 T5 尺度下无条件解决"）与 NOTES.md:278（§8"无条件解决"）
  未随更正块第 3 条同步改为"[A | 发射 Q≤3^{11}]"。更正块声明覆盖正文，形式上无碍，
  但诚实结论块是最常被引用的位置（本轮任务摘要即引用了"无条件解决"字样）——应同步。
* **R2 [LOW] REG(e) 的 y<64 字面错误**：应为 y<N0（回归结束后链可落在 [64,N0)）；
  "m<16"应为"m<G(N0)+1≈52"。结论（恒浅、无新深链）不变。
* **R3 [LOW] 过时的封顶/计数字符串**：§4（NOTES.md:181"封顶 den≤3^9"）、§6 首段
  （NOTES.md:226"den≤3^9，122 族"——与下文 134 族矛盾）、levels_t5.py 的
  orbit_cap_note（仍写 "beyond den=3^9"）、verify_t5.py:288 注释（"18 orbit no-lift
  (r=1..9)"——代码实际追加全部 20 个）。
* **R4 [LOW] check 6 的 32 族清单未含 den-3^10 层**：我已对全部 134 族独立验证
  max|3k·den+num| = 1580391451340（最坏族 531449/59049）< 2^53——成立；建议清单
  扩容或改为读 json 族集。
* **R5 [INFO] 更正块抬头"攻击员 4 MEDIUM"** 实为 3 MEDIUM＋5 LOW＋1 INFO（我方第 1
  轮文件）；无实质影响。
* **R6 [INFO] 一致性核验**：修补版 smoke（levels_t5_300003.json，03:47 同版代码）与
  新全量跑族集完全相同（134/134）、残余相同、orbit 键相同（至 3^11）、family_status
  无异常；run.log 与 full_run_console.log 仅差末行 WROTE（写序所致）。更正块第 11 条
  的消融实验（去 E0 族出口）我未重跑，按作者记录采信。

## 第 1 轮复审裁定

四项 MEDIUM（F1–F3＋我方 F2 的自我更正）全部落实并经我方实跑/独立计算确认；修补未
引入数学性问题（新出口、新族层、双发射均为防御性扩展且全量认证）。剩余问题 R1–R4
均为文字/清单层面的残留（其中 R1 因位置显眼建议务必同步）。刻度维持 **2（fixable
gaps）**——距 1 只差上述编辑性收尾；无新的数学缺口。

---

# 第 2 轮定向复审（2026-11-11，攻击员）

复审对象：第 2 轮修补（NOTES.md 17:43 新增第 2 轮更正块；levels_t5.py 17:23；
verify_t5.py 17:38；计算产物未重跑——16:35/03:47 版本仍有效，因本轮仅文字/验证脚本改动）。

## 第 1 轮复审遗留（R1–R6）逐条核验

* **R1（"无条件"残留）——已修。** 诚实结论块（NOTES.md:55-57）改为"深回归有界性定理
  REG [A | 发射 Q≤3^{11}]——后者在该范围内把…RES 残余…解决"；§8（NOTES.md:289-291）
  改为"REG（[A | 发射 Q≤3^{11}]）是…上述范围内的解决（假设在族证书/ORBIT-9 范围内
  自动成立）"。grep 全文：仅更正块内描述性出现"无条件"（第 17/46/196/231 行，均为
  记录改动本身），无存活的无条件主张。
* **R2（y<64 字面错误）——已修。** REG(e)（NOTES.md:224-226）改"provenance y<N0
  （回归后链可落在 [64,N0)），发射 m<G(N0)+1≈52"；GW(b) 尾句（NOTES.md:185）同步
  "浅链段（y<N0）…m<G(N0)+1≈52"；更正块第 2 轮②亦记录。
* **R3（过时封顶/计数字符串）——主体已修，余 2 处纯装饰残留。** 已修：NOTES.md:191
  （"封顶 den≤3^{10}"）、NOTES.md:237（"P3 族闭包（den≤3^{10}，134 族"）、
  levels_t5.py:472（orbit_cap_note 字符串改 3^10）、verify_t5.py 注释（:19/:300/:304
  "ALL 20 orbit no-lift families (r=1..10)"）。**残留（新 R7，纯装饰）**：
  (a) levels_t5.py:325 certify_families docstring 仍写 "closure within den <= 3^9"；
  (b) 已发布产物 levels_t5_20000000.json 的 orbit_cap_note 字段仍是 "beyond den=3^9"
  （该 JSON 生成于 16:35，早于 17:23 的代码改动、未重跑）——两处均为非数学的描述
  字符串，无任何主张/计算依赖之；重跑或下次产数时自愈。
* **R4（check 6 清单缺 den-3^10 层）——已修且实测。** check 6 改为动态读取
  levels_t5_20000000.json 族集（异常时回退固定清单并在消息中标注来源）。**verify_t5.py
  实跑**（`PYTHONUTF8=1 …Python312/python.exe -B work_gc_level_t5/verify_t5.py` 自
  D:/math_cc）：11 行检查全 ok、ALL PASS、exit 0、324.8 s；check 6 报 "134 families
  from levels_t5_20000000.json (observed max 1580391451340 < 2^53)"——与我第 1 轮
  独立计算值 1580391451340 完全一致。
* **R5（更正块抬头计数）——已修。** NOTES.md:6 改"攻击员 3 MEDIUM＋5 LOW＋1 INFO＋
  复算员A 5 LOW"。
* **R6（休眠发射路径 lift 位）——已记录在案。** levels_t5.py:346-348 加 NOTE 注释
  （"if ever enabled, LIFT families must add the 2^j lift bit…rj already includes it
  via residue(lift)"）；该分支本轮仍 0 触发（round-1 已核 family_status 全空）。

## 新问题扫描

未发现新数学问题。check 6 的动态读取有安全回退且消息标注来源（verify_t5.py:229-238），
实测走 json 路径；其余改动均为文本/注释。计算产物（134 族、orbit 至 3^11、残余清单、
P1 T4 复现）沿用第 1 轮已核验的 16:35 全量重跑，未被本轮改动触及。

## 第 2 轮复审裁定

两轮三方审查的全部 MEDIUM/LOW 数学性发现（第 1 轮 F1–F7、复审 R1–R6）均已落实并经
我方实跑或独立计算确认；verify_t5.py 11 项检查在本轮代码上 ALL PASS（exit 0）。仅余
两处纯装饰性字符串残留（R7：一个函数 docstring、一个 JSON 描述字段，均把封顶误写为
3^9，无主张依赖、不影响任何计算或证书）。**刻度：1（closed in all states）**——数学
内容在我方可核验范围内全部闭合；R7 作为下次产数时的顺手清理项记录在案。
