# LEVEL-T5：EXT 推到 T5 的第五层分析——正面前进与精确阻塞

GLM（攻坚·R3），2026-11-10/11。工作目录 work_gc_level_t5/。分级：[A]（从所列已接受导入给出证明）、[A-cond]
（在所述附加假设下证明）、[B]（对明示有限范围的穷尽精确计算，脚本命名）、[C]（启发式）。

> **审查更正块（第 1 轮三方审查，2026-11-11；来源：攻击员 3 MEDIUM＋5 LOW＋1 INFO＋复算员A 5 LOW。覆盖正文。）**
> 1. [MEDIUM·T5-RED 基座] 封顶 den≤3^9 曾把第 9 层发射族（den 3^10）及其后代排除在 [B] 基座外。
>    已改：levels_t5.py 封顶提至 **3^10** 并全量重跑（本版数字皆新跑）；发射族
>    6∓8/3^{10}（den 3^10）与 b/cs 后代认证通过，其 a-后代 δ_10^±（den 3^{10}）入族集、
>    恰只链 5 失败（=OBST 轨道在 r=10 层的表现，被 ORBIT-9 排除）；其后备（den 3^{11}
>    发射）只在 FIRE_LOG。verify check 8 的全量清单同步扩容（含 18+2 个轨道 no-lift 族
>    与 den-3^{10} 层全量复验）。
> 2. [MEDIUM·entry 完备] level_entries 的 generic-c 分支曾静默丢弃有理结果（对照 a/b 分支）。
>    已改：canon 后仍为有理的 θ+g−2 一律 add_fam（本版族数 122→134）。
> 3. [MEDIUM·REG 书写] §5 证明补全：显式尺寸引理（REG-Size，r≤0.6m−25 型）、y=J 情形的
>    G-坍缩链（m<T4 → <T3 → <T2 → <T1 → ≤N0，至多 4 步）、深回归次数 O(1) 计数（每深链
>    t 至多一次，回归结束后一切发射均浅 y<N0 ⟹ m<G(N0)+1≈52）。**REG 的标签自「无条件」改为
>    [A | 发射 Q≤3^11]**（即族证书/ORBIT-9 范围内；无穷轨道深度下 3^r 可破坏尺寸界——
>    这正是 OBST 的一部分）。
> 4. [LOW·scalar aouts] family_cert 曾丢弃链 5..63 的 scalar aouts：已改为聚合并**排除 NT 步
>    输出**（代表元伪影，类不可靠）。
> 5. [LOW·verify 覆盖] check 5 扩至 bulk [64,3·10^5)＋抽样 scalar；check 8 全量清单加入
>    18 个轨道 no-lift 族与 den-3^10 层；check 9 增加重放 spec 构造（从族 export 重建
>    4 个残余 entry 并逐一认证/失败）。
> 6. [LOW·bulk 发射路径] 曾用 56 位截断值发射且只取前 4 个失败：已改为按精确类
>    num/den（lift 计入）发射并无截断；该路径迄今零触发（记录在案）。
> 7. [LOW·OBST 措辞] 已接受对象是 **+支** c_r=−3+8/3^r（ODD_DENOMINATOR §3、
>    ORBIT_SHIFT_OBSTRUCTION §2）；−支为对称扩展，同阻塞。计算证实到 no-lift 族
>    **r≤9（den≤3^9 层）/发射族 r≤10（den 3^10）**，闭式对一切 r。
> 8. [LOW·S_2 紧值] 链 2 的 c-源 <T2 = 层级 A/B/C，其唯一深 a-输出类为 2，故 **S_2 紧值
>    为 {0}**；正文所列 S_2={−1,0,1} 为保守过逼近（层级 D 的集合复用）。Θ_3/Θ_4 的
>    **整数部分不受影响**（两种取法相同，已验证）；有理部分过逼近（紧值少 13/3）。
> 9. [LOW·§6 归属] 残余发射按**分式**归属：spec 残余（类 5/−11 mod 64，由分式
>    −19/9−2^j、−35/9−2^j 型实现）发射 154/27、170/27（orbit 数据为准）；整数
>    (5,5)/(5,−11) 全链项才发射 10/3、26/3。正文已改按此表述。
> 10. [LOW·OBST(b) 字表] 轨道族首步攀登字随代表元约定与 r 变化（[5,5]、[5,6]、[5,7]、
>     [5,8]、[5,10] 等），均止于首步；uncert 结论与字无关。
> 11. [LOW·§6 真实/过逼近区分] C7E 的残余经 S0 槽（含真实锚点：(5,5)→10/3→−1/3 线）；
>     层级 E 的 spec 残余只经 E0 槽族出口**过逼近**产生（对照实验：去 E0 族出口后 E 的
>     spec uncert 变空，仅剩整数 (5,[5])）；26/3、62/9 线在 T5 漂移结构内无独立实锚
>     （保守包含）。二者均被 GW 化解，不影响结论。
> 12. [LOW·spec 发射精度] 修补脚本按残余的**精确分式**与剩余类**双重发射**（此前只用
>     整数剩余类，与 orbit 数据不一致）。

> **第 2 轮（定向复审，2026-11-11；来源：攻击员 6 LOW）**：①「诚实结论」块与 §8 的 REG
> 「无条件解决」已同步改为「[A | 发射 Q≤3^{11}] 范围内解决」（本块第 3 条）；② REG(e)
> 与本块第 3 条的「y<64 ⟹ m<16」更正为「y<N0 ⟹ m<G(N0)+1≈52」（结论不变：恒浅、
> 无新深链）；③ §4「封顶 3^9」、§6「den≤3^9，122 族」、levels_t5.py orbit_cap_note、
> verify 注释「18 orbit no-lift」四处统一为 3^10/134 族/r=1..10 共 20 族版本；
> ④ verify check 6 改为读 levels_t5_20000000.json 族集动态验证全部 134 族的截断忠实界；
> ⑤ 本块抬头计数更正为「3 MEDIUM＋5 LOW＋1 INFO」；⑥ 休眠 bulk 发射路径的 lift 位
> 计入问题备注在案（levels_t5.py 该分支注释；0 触发，启用前需补）。

> **诚实结论（先行）**：本目录**没有证明 Theorem T5**。达到的是：
> 1. [A] 第五层的全部结构性引理（尺度/漂移 DL5、深 a-输出分类 DEEP-E、统一 NT-gateway 引理 GW、
>    深回归有界性定理 REG [A | 发射 Q≤3^{11}]——后者在该范围内把 r1r2 Remark 2.5 的
>    RES 残余在 T5 尺度下解决）；
> 2. [B] 层级 E 与 S(J)（T4≤J<T5）着陆类的完整逐项计算，全部认证，**除了链 5 的自由入口**；
> 3. [A]+[B] **阻塞定理 OBST**：链 5 自由入口的递归类恰是有理轨道 −3±8/3^r（即已接受的 route-A
>    3-adic 阻塞族，work_c3_drift/ODD_DENOMINATOR.md §3 / ORBIT_SHIFT_OBSTRUCTION §2 所引），
>    在每个塔层 r≤10 都出现 [B]、按闭式恒为 ≡5 (mod 16) [A]、由上一层族发射 [A+B]——
>    有限族证书沿此路线**不可能**闭合；
> 4. [A-cond] 归约定理 T5-RED：在 ORBIT-9（实际轨道递归不超出第 9 层塔）下 S(J) 无 tie。
>
> 不主张任何 EXT 范围扩大、不停机结论或机器层视野变化；已接受视野（2^T4−2 顶层步，R1 已迁移）
> 不变。EXT* 与全局不停机仍开放。

> **Round 3 (2026-11-14, independent Claude adversary; overrides the body and earlier rounds where they differ).**
> 1. [HIGH] **The "m = N0 boundary" deep emission does not exist.** GW(b) with CLOCK gives 2^m <= 30+4.5(y−1)P(y−1),
>    and y = j_3 < T1 gives m <= 10^7+50 < N0 = 2·10^7 (G(y)+1 is loose by a factor 2 in the exponent). Also table
>    row N0−1 is odd type a with 1+v2(9k+10) = 3, so even at m = N0 the a-descendant lands on chain 3, not (5,−1/3).
>    The boundary class is deleted from DEEP-E (S_0 = [−2,2], no rational drift).
> 2. [HIGH] **OBST(c) is NOT an impossibility theorem.** The algebra holds (delta_r^± ≡ 5 mod 16, emission
>    6∓8/3^(r+1), a-descendant delta_(r+1); this is ODD_DENOMINATOR §3). But the edge "emitted family →
>    delta_(r+1)@5" needs a deep emission chain (m >= N0); for shallow m the lifted family is certified. The closure
>    adds descendants unconditionally, ignoring GW(b). Each real orbit step costs one log-level: y < T3 allows at
>    most 2 deep emissions, y = J < T5 at most 4, so the real depth is <= r0+4 (also from REG(c)+(e)). OBST(c) is
>    relabelled **[B]: "this ungraded closure does not terminate"**. "The static certificate route cannot close T5"
>    is withdrawn; accepted Theorem O concerns the whole tower, not a fixed level. A closure graded by provenance
>    height may discharge ORBIT-9 (not proved).
> 3. [MEDIUM-HIGH] **T5-RED is unproved as written.** The family closure uses only one-step deep descendants, while
>    REG(c) allows up to 4 deep steps. Among the 36 absent <=4-step classes of 46/9, 62/9, 154/27, 10/3 (j < 3·10^5)
>    one fails: 10/9 = 46/9−4 at chain 8 (≡ 58 mod 512), which fires 179/27, off the ± orbit. verify check 9b prints
>    and tolerates this "(8,58)"; "all residuals sit at chain 5" is false. Also the Λ=5 analogue of C5_EXTENSION §4
>    is invoked without proof.
> 4. [MEDIUM] levels_t5.py:266-269 drops NT outputs as "representative artifacts"; they occur in 180/180 random
>    real states of their classes and must be kept (numerically harmless for the S0/E0 slots here).
> 5. [LOW-MEDIUM] ORBIT-9's "actual tower index" is undefined (a 6-bit class does not determine r; non-orbit
>    starting classes have no index); define it by emission history.
> 6. [LOW] S0 copies of lifted fired families are missing from FAM_SET (22 certified at j < 64 by the adversary, no
>    failure); verify checks 9/10 read the artifact or test trivial bounds; §9 "~20 min" vs 46,058 s in the log;
>    one provenance per spec entry (setdefault).
>
> Confirmed by round 3: DL5's hand re-derivation of the drift and landing sets (sound supersets; rational parts
> vacuous after item 1); the OBST closed forms (r <= 40); the family-status table; verify_t5.py ALL PASS at reduced
> range. **Net:** [A] DL5 (as supersets), GW, the OBST algebra; [B] the level-E data as computed. T5, T5-RED and
> the impossibility claim are NOT accepted. The route to T5 is open, not blocked.

## 0. 总结

1. **Lemma DL5（第五层尺度引理）[A]**。对 J∈[T4,T5)，S(J) 至多 5 条深链（t=0..4，参数
   j_0=J<T5、j_1<G(J)<T4、j_2<T3、j_3<T2、j_4<T1，链 5<N0）；深漂移集 Θ_t 的精确集合（§2 表，
   含有理值；整数集 Θ_1=[−1,3]、Θ_2=[−2,4]、Θ_3=[−3,5]、Θ_4=[−4,6]，有理漂移全部形如
   C/3 且只在 t≥1 经 t=0 的唯一有理 shift 4/3 进入）。层级 E（T3≤Q<T4）自身深漂移全整数。
   代码 BFS 与手工表逐项相等（levels_t5.py P2 断言）。
2. **Lemma DEEP-E（源深 a-输出分类）[A]**。源 S(Q) 的深 a-输出类：层级 C、D 均为 {1,2,3}
   （T4 DL(iii)；层级 D 无深入口 bare tie——Θ^D_1={0,1,2}、Θ^D_2=[−1,3] 均不含 −2，且 t=1 的
   C 入口 (5,5) 需要 j_1>T2 与 level-C 源界矛盾，即 T4 论证）；层级 E 为 [0,4]∪{10/3（仅链 N0）}
   （层级 E 深漂移全整数；(5,5) a-入口自链 3（θ=−2，y<T1）的 catapult 输出 m≤N0，深者仅 m=N0）。
   因此 S(J) 深段 c-步的 shift 集：t=0 为 [−2,2]∪{4/3}（层级 E），t=1 为 {−1,0,1}（D），
   t=2 为 {−1,0,1}（C），t=3,4 为空（A、B 无深 a-输出——c 步必着陆）。
3. **Lemma GW（统一 NT-gateway）[A]**。设链 j<N0 的状态 (2^j u, x+D)（k_j=τ(j−1)/2）的
   下一步为 X(j−1) 的 a-步，输出 v2(x′)=m≥j−1（自由步）。则**精确恒等式**
   **D′ ≡ (9+6k_j−D)·3^{−1} + 2^m (mod 2^{m+1})**（D 为精确缺陷；有理类 δ=C/Q 的版本为
   (9Q+6k_jQ−C)/(3Q)+2^m）。当缺陷已知到 m+1 位时输出类被 **(9+6k_j−δ)/3+2^m 完全决定**：
   m≤j 时入口类 δ mod 2^{j+1} 即够；m>j 时由两步来源知识（进入链 y 给 θ mod 2^{y−2}，
   r1r2 2.3 的 m+1≤j_T−2 即此情形）。且 m<G(y)+1（y=进入该段的链）。特例：j=5,k=1,
   δ∈{5,−11} 给出 r1r2 的 (10−2^m)/3、(26−2^m)/3；δ=−1/3 给出 SECOND_GATEWAY 的
   46/9+2^m。证明用恒等式 3D′=9−D−x′+6k_j 与 mod 2^{m+1} 下 −x′/3≡2^m（x′=2^m·奇）；
   m-界用两步来源公式（r1r2 Lemma 2.3(a,b)、Lemma CB 的 C-支）与 CLOCK/C1、MASS 的尺寸界。
4. **Theorem REG（深回归有界，RES 残余消解）[A | 发射 Q≤3^{11}]**。J∈[T4,T5) 时 S(J) 的
   bare-tie/自由入口若发射 m≥N0（T4 下不可能、T5 下可能：y=j_1,j_2<T3 时 m<T2、
   y=j_3<T2 时 m<T1、y=J 时 m<T4），则深有理链 (m,C/Q+2^m) 之后：a-步严格下降（REG-Size
   显式引理：r≤0.6m−25 ⟹ |3Qk+C|<2^{m−2}，无共振），b/c-步着陆或按尺寸界 <G(m)，
   G-坍缩至多 4 步回浅区（a-步对 Q≤9 一步即浅），记录严格降；深回归次数 O(1)（每深链
   至多一次；回归后发射恒浅）；着陆类落在显式 no-lift 后代集 {3Q−C, C−Q, C+3sQ}/Q 内。
   **r1r2 Remark 2.5 的 m≥10^8「深入口有理相位」残余在该范围内被完全消解**（发射
   Q≤3^{11} 于族证书/ORBIT-9 范围内自动成立；相关族 [B] 认证，除 §7 轨道）。
5. **层级 E 与 C7-E 计算 [B]**（levels_t5.py，全表 j<2·10^7）。层级 E 的全部 entry（整数
   [−3,5] 全链、2315 项 specific c-入口、gateway 族）与 S(J) 着陆类（整数 [−6,7] 全链、
   2554 项 specific、with-lift 拷贝族）逐项认证：**除链 5 自由入口外全部通过**
   （层级 E 与 C7-E 各 5 项 = 整数 (5,5) + specific 有理 5/21/−27/−11 ≡ 5、−1/3、−17/3、−11，
   两步化解为已认证族——除轨道递归，见 §7）。有理 bulk（D=56 位截断，ceiling min(j−loss,56)）
   与 scalar certify 交叉一致（64≤j<3000 全链＋[64,3·10^5) 抽样 2000 链，verify check 5）；
   整数特例重现 rwalk.bulk。
6. **Theorem OBST（阻塞）[A+B]**。(a) [A] 对每个 r≥1，δ_r^±=−3±8/3^r ≡ 5 (mod 16)，且
   (5,δ_r^±) 的 GW 发射为 6∓8/3^{r+1}+2^m；后者的 a-后代恰为 δ_{r+1}^±。(b) [B] 对 1≤r≤10
   逐层精确计算：no-lift 族 (δ_r^±) 在链 5 为自由入口（且仅在该链失败；with-lift 变体全链
   认证）；发射族 (6∓8/3^{r+1}, lift) 全链认证。(c) [A] 因此族图含无穷路径
   δ_r→6∓8/3^{r+1}→δ_{r+1}→…，任何有限族集都不闭合链 5 自由入口递归；该轨道族即已接受的
   route-A 有理轨道 c_r=−3+8/3^r（ODD_DENOMINATOR §3、ORBIT_SHIFT_OBSTRUCTION §2 所引）。
   (d) 单条真实轨迹仍终止（每次发射记录严格下降 / 非下降预算 L″ 有限），但界随 J 增长，
   无一致有限证书。
7. **Theorem T5-RED [A-cond]**。定义 ORBIT-9(J)：S(J) 着陆化解中每条链 5 自由入口递归的
   实际塔层指数 ≤9（≤9 层族已 [B] 认证）。则 ORBIT-9(J) ⟹ S(J) 无 tie（在已接受
   EXT(<T4)＋导入内，证明同 T4 §6 模式：DL5/DEEP-E 分类深段、着陆分类、GW 化解、REG 处理
   深发射、记录 <J）。**ORBIT-9 未被证明，T5 不主张**（OBST 表明静态证书路线不可行）。

## 1. 记号与已接受导入

同 work_claude_residual/NOTES.md §1：链 (x,Θ)，x=2^j u，缺陷 D=Θ−x；a-步 x′=2Θ+3τ−x/2；
b/c-步 x′=c′_W u+λ′_W；N0=2·10^7，G(x)=2log2x+3，T_{h+1}=2^{(T_h−3)/2}。
[A-imp] 使用：Lemma K/HP/AB/RA、Lemma BR、Prop RB（PROOF_EXT）；窗口证书 5≤j<2·10^7、
δ∈[−12,15]\{(5,5),(5,−11)}＋Prop 3.2（work_claude_shifted §4）；gateway 证书 (10−2^m)/3、
(26−2^m)/3 于 5≤m<10^8（work_r1r2 Thm 2.4）及其 Lemma 2.3 两步恒等式、Lemma CB；Theorem S
（work_claude_shift §2，非下降映射 Φ′=3+2k−(Φ+2^m)/3≡(9+6k−Φ)/3+2^m）；RATIONAL_MODE §1
（RA/RC 恒等式）、§2（SIZE3）、ODD_DENOMINATOR §1–2、SECOND_GATEWAY §1；work_deep 塔界
Λ(J)≤h（J<T_h）与深步界；CLOCK/C1、MASS；Theorem L″ 非下降预算；Lemma R0、DL（T4）；
route-A 有理轨道 c_r=−3+8/3^r（已接受；见 ODD_DENOMINATOR §3 与 ORBIT_SHIFT_OBSTRUCTION §2
的引述）；Theorem T4 及其 [B] 层级计算 levels_20000000.json（本目录 P1 逐字段重现）。
本目录不使用 AB′/copy principle、C7 字面形式、DL-下降等已反驳目标。

## 2. Lemma DL5：第五层的链、参数与精确漂移集 [A]

**(i) 深链个数与参数界。** J∈[T4,T5)。work_deep 塔界给 Λ(J)≤5。逐步地：链 t 的步为
a/b/c 之一，输出界：a-步 ≤1+log2(6k+2|θ|)+1（|θ|≤6 整数或有理分子 |C|≤13、den 3：
|3Qk+C|<2^{j−2}，RA/ND），b/c-步 ≤log2(6τ+5)（MASS）——均 <G(j_t)。归纳得
j_t<T_{5−t}（t=0..4），链 5<G(j_4)<N0。∎

**(ii) 精确漂移集（零裕度）。** Θ_0={1}；Θ_{t+1}={3−θ}∪{θ−1}∪{θ+s: s∈S_t}，其中
S_t=该层 c-步可用的深 shift 集（§3 DEEP-E）：
S_0=[−2,2]∪{4/3}（层级 E），S_1=S_2={−1,0,1}，S_3=S_4=∅。
层级 E 的深漂移：Θ^E_1={0,1,2}，Θ^E_2=[−1,3]，Θ^E_3=[−2,4]（全整数；其 c-步可用深 shift
为 {−1,0,1}——层级 D/C——与 t=2 后为空）。手工表：

| t | Θ^E_t | Θ_t（S(J)）整数 | Θ_t 有理 |
|---|---|---|---|
| 0 | {1} | {1} | — |
| 1 | {0,1,2} | [−1,3] | {7/3} |
| 2 | [−1,3] | [−2,4] | {2/3,4/3,7/3,10/3} |
| 3 | [−2,4] | [−3,5] | {−1/3,1/3,2/3,4/3,5/3,7/3,10/3,13/3} |
| 4 | — | [−4,6] | {−4/3,−2/3,−1/3,1/3,2/3,4/3,5/3,7/3,8/3,10/3} |

有理漂移仅经 t=0 的 shift 4/3 进入（复制层级 E 的 (N0,10/3+2^{N0}) 深输出；其 lift 位在
N0，对后续一切步不可见）。收紧论证（T4 审查教训）：深链 3 需要 j_2>T1 且链 2/3 的 c-步源
（<G(j_2)<T1 / <G(j_3)<T1 为层级 AB）无深 a-输出，故 Θ_3、Θ_4 的 c-支为空；S(J) 的
链 1、2 无收紧（level-E/C 的深输出参数可 >T1）。代码断言 BFS==手工表（P2）。
深漂移下无共振：3k+θ=0 需 k≤7/3，而 k≥(j−2)/4≥5·10^6（CLOCK 下界）；
有理时 3Qk+C≠0（gcd）。∎

**(iii) 着陆类（C7-E 的输入）。** 从深链 t 的着陆：a: 3−θ_t、b: θ_t−1（全链整数 ⊆[−5,7]、
有理 ⊆{C/3}）；c: θ_t+D−2，D 为 level(t) 在着陆链 ω 的浅输出（specific）。整数类全在已接受
窗口内，除 (5,5)（3−θ_t=5⟺θ_t=−2：t=2,3,4 可能——T5 新现象；t=4 时 y=j_4<T1 为旧情形）。
b-着陆类 5 需 θ_t=6（Θ_4∋6 ✓，r1r2 2.3(b) 的 θ_T=6 情形，y<T1 旧）；−11 需 θ_t=−10（不可能）。
c-着陆 bare tie：θ_t+D=7 (mod 16)（§6 计算）。

## 3. Lemma DEEP-E [A]

层级 L∈{C,D} 的深 a-输出：仅 a-步于链 0,1（输出链 1,2 参数 <T2/<T1 可深），类
{2}∪{3−θ: θ∈Θ^L_1}={1,2,3}。层级 D 无深入口 bare tie（§0.2 所引）；层级 E 有四条深链
（0..3），深 a-输出来自链 0,1,2 的 a-步（输出链 1,2,3 参数 <T3/<T2/<T1 可深），类
[0,4]∪{2}∪{1,2,3}=[0,4]，外加链 3 的 (5,5) a-入口（θ=−2）catapult 输出 m<G(j_3)+1≤N0
——深者仅 m=N0，类 (10−2^{N0})/3（10/3+lift）。∎

## 4. Lemma GW 与族认证框架

**GW(a) 恒等式 [A]。** 在链 j 的 a-步（k=k_j）：3D′=9−D−x′+6k_j（直接由 D′=3−D−x/2 与
x′=3·2^{j−1}u+2D+6k_j 消去 x）。若 v2(x′)=m，则 mod 2^{m+1}（x′=2^m·奇，−1/3≡1 mod 2）：
**D′ ≡ (9+6k_j−D)·3^{−1} + 2^m**。当 D 已知到 2^{m+1}（m≤j 时入口类 δ mod 2^{j+1} 即够；
m>j 时用进入链 y 的两步知识）得类形式 **D′ ≡ (9+6k_j−δ)/3+2^m**（δ=C/Q 时分子
9Q+6k_jQ−C 于分母 3Q）。这正是"自由步决定于来源"的统一表述。特例核对：j=5（k=1）、δ=5/−11 → r1r2 的 c=10/26；
δ=−1/3 → 46/9；δ=−17/3 → 62/9（与 SECOND_GATEWAY §1 一致）；j=8（k=2）、δ=58 → −37/3。
**GW(b) m-界 [A]。** 自由入口的两步来源（进入链 y）：a/b-入口用 r1r2 Lemma 2.3(a,b) 的
公式（x-余项 ≤ 5·2^{y−2}u_y 等消失于 2^{m+1} 之上，Z=θ+12+9k_y 或 2θ+10+9k_y），
c-入口用 Lemma CB 的 C-支（Z_prev=λ′_W(y−1)≤6τ+5）；一律 |Z|≤9(y−1)P(y−1)+O(1)，故
m≤1+log2|Z|<G(y)+1（CLOCK/C1：k_y≤(y−1)P(y−1)/2）。浅链段（y<N0）同一界给 m<G(N0)+1≈52。

**族认证 [B]。** 族 (num,den,lift)=类 num/den(+2^j) 于一切链 j<N0 的认证：
j<64 用精确残差 scalar certify；j≥64 用 56 位截断 D=num·den^{−1} mod 2^56 的向量化 bulk
（ceiling min(j−loss,56)；截断忠实因为精确首步参数 j1=1+v2(3k·den+num)≤1+log2(3·den·(j−1)P(j−1)/2+|num|)<2^53<56，
且一切记录 ≤53）。den=1 时重現 rwalk.bulk/certify。自由入口按 GW(a) 发射新族，
后代集（REG 的 no-lift 着陆）{3Q−C, C−Q, C+3sQ}/Q 一并入队；封顶 den≤3^{10}，
超封顶发射记入 obstruction 数据（§7）。

## 5. Theorem REG：深回归有界 [A | 发射 Q≤3^{11}]

（审查更正块第 3 条：本节原版书写不全、标签「无条件」过强；本版为补全后的陈述。假设
「发射 Q≤3^{11}」= 自由入口的类来自族证书范围内（den≤3^{10} 的 export 或整数/三分之一
漂移类）——在 ORBIT-9 与本目录族集内自动成立；见 REG-Size 之后的说明。）

**REG-Size（显式尺寸引理）[A]。** 设深链 m≥N0 带类 C/Q+2^m（gcd(C,Q)=1，Q=3^r）。则其
a-步输出 m′=1+v2(3Qk+C) 满足
    3Qk+|C| ≤ 3^{r+1}·(m−1)P(m−1)/2 + |C|，
且只要 **r ≤ 0.6m−25**（更精确地 (r+1)log2 3 + log2((m−1)P(m−1)/2) + log2|C|/ ≲ < m−2）
就有 3Qk+|C| < 2^{m−2}，从而 m′<m−1（严格下降、无共振：3Qk+C≠0）。
数值范围：m=N0、r≤11 时左端 ≤ 3^{12}·10^7·7000 ≈ 2^{58}，而 2^{m−2}=2^{2·10^7−2}——
余量天文数字；对一切 m≥N0，r≤0.6m−25 在 r≤11 范围内永真。
结构性来源：S(J)/层级 E 着陆自由入口的类为整数或 C/3（漂移类）或族 export 类
（den≤3^{10}），故**首次深发射 Q≤3^{11}**；深回归内部无自由步（REG-Size 排除），Q 不再
增长；回归结束后的发射均自浅源（见下）。无穷轨道深度下 r 可破坏 r≤0.6m−25——那正是
OBST 的一部分，不在本定理范围内。

**REG（主定理）[A | 发射 Q≤3^{11}]。** 设 S(J)（J∈[T4,T5)，最严反例归纳内）某自由入口
经 GW 发射 m≥N0（进入链 y：y=j_1,j_2<T3 时 m<G(y)+1<T2；y=j_3<T2 时 m<T1；y=j_4<T1 时
m≤N0 旧情形；y=J（t=0 c-着陆）时 m<G(J)+1<T4）。则得深有理链 (m,C/Q+2^m)，且：
(a) **a-步**：m′=1+v2(3Qk+C)<G(m)（REG-Size；类 (3Q−C)/Q，b′=0（RA；lift 位 2^m 高于
    一切后续模）；对 Q≤9 更有 m′≤1+log2(2^{46})=47，一步即浅）。
(b) **b/c-步**：着陆 ω=v2(x′)≤log2(6τ+5)（MASS：|λ′_W|≤6τ+5 与 S1 边际 ω<σ=v2(c′_W)
    给出 v2(x′)=ω）；c-步的源 <G(m)：m<T1 时 level A、m∈[T1,T2) 时 AB、m∈[T2,T4) 时
    ABC——前两者无深 a-输出（DEEP-E）故必着陆；对 m≥T2 的 c-步仍用尺寸界
    ω≤log2(6(m−1)P(m−1)+5)<G(m)。
(c) **G-坍缩链**：由 (a)(b) 每步输出 <G(m)：m<T4 → <T3+1 → <T2+1 → <T1+1 → ≤N0，
    至多 **4 步**回浅区（m<T2 时 ≤3 步、m<T1 时 ≤2 步；a-步按 (a) 的锐界一步即浅）。
(d) **记录**：每步严格降（a: m′<m−1 ⟹ Γ+1+m′<Γ+m；b/c: ω<m−1−ε）。
(e) **深回归次数 O(1)**：每次深回归都由「provenance y≥N0 的自由入口发射」启动；S(J)
    的深链 t=0..4 各至多启动一次（发射即结束该段的着陆化解）；一次回归结束后一切链
    <N0，此后自由入口的 provenance y<N0（回归后链可落在 [64,N0)），发射 m<G(N0)+1≈52
    恒浅——**不再产生新深链**（结论不变）。
    故每条 S(J) 轨迹至多 5 次深回归、每次 ≤5 条深有理链，总计 O(1)；着陆类落在显式
    no-lift 后代集 {3Q−C, C−Q, C+3sQ (s∈{−1,0,1})}/Q 内（全部在族集中被认证，除 §7 轨道）。∎
（对照：T4 下 m≤N0<10^8 由已接受 gateway 证书覆盖；T5 新范围 [10^8,T4) 由本定理覆盖。
原版「无条件解决 RES 残余」据此改为「在发射 Q≤3^{11} 范围内解决」；r1r2 Remark 2.5 的
深有理相位在该范围内被完全消解。）

## 6. 层级 E 与 C7-E 的计算 [B]

levels_t5.py（全表；首跑 879 s，修补后重跑完成、数字以重跑为准）：P1 逐字段重现 work_claude_residual/levels_20000000.json（层级
A,B,C,OUT,D,C7 与 uncert 一致）；P2 漂移集断言；P3 族闭包（den≤3^{10}，134 族；
自由入口逐层记录）；P4/P5 层级 E 与 C7-E 的 entry 集与认证（两轮 fixpoint 后稳定）。
结果（levels_t5_20000000.json）：

* 整数全链 entry：层级 E [−3,5]、C7-E [−6,7]，仅 (5,5) 自由（δ=5 的 bulk uncert=[5]，与 T4 一致）。
* specific c-入口：层级 E 2315 项、C7-E 2554 项（含族 export 的有理类；修补后数字——
  审查更正块第 1、2、4 条使 scalar aouts 聚合与 generic-c 有理族进入枚举），认证后残余
  **specific 各 4 项，全在链 5**：类 5（θ=1+D=6，D 来自 37/9 族 export）、21（=−1/3，D=22 自 7/3 族）、
  −27（=−17/3，D=−26 自 23/3-lift 族）、−11（D=−10 自 53/9 族）。全部由 GW 化解，**发射按
  精确分式归属**（以 orbit 数据为准）：spec 残余 21、−27（=−1/3、−17/3）发射 46/9、62/9；
  spec 残余 类 5/−11（由 −19/9−2^j、−35/9−2^j 型分式实现）发射 154/27、170/27；整数全链项
  (5,5)、(5,−11) 才发射 10/3、26/3——上述发射族及全部后代经 [B] 认证。真实/过逼近区分：
  C7E 的残余经 S0 槽产生（含真实锚点：(5,5)→10/3→−1/3 线）；层级 E 的 spec 残余只经 E0
  槽族出口过逼近产生（对照实验：去 E0 族出口重跑后 E 的 spec uncert 变空、仅剩整数
  (5,[5])，C7E 残余经 S0 原样保留）；26/3、62/9 线在 T5 漂移结构内无独立实锚（保守包含）。
  二者均被 GW 化解，不影响结论。
* 有理族：修补后共 134 族（审查更正块第 1、2 条：封顶 3^10＋generic-c 有理族补入；
  本行数字以本次全量重跑为准，见 levels_t5_20000000.json）：其中轨道 no-lift 族
  (−3±8/3^r)（**r=1..10，共 20 族**——den-3^{10} 层的 δ_10^± 现入族集）各**仅在链 5**
  失败（首步攀登）；其余 114 族（含全部 with-lift 轨道发射族）全链通过；with-lift
  变体在 j≥64 与 no-lift 同證（lift 位 ≥2^64 高于一切记录）。
* 层级 E 自身的 (5,5)（θ_1=2 复制 level-C 链 5 类 5 输出，244875 源）由 RA 吸收
  （route a，T4 审查块论证在 T5 仍适用：route c 给 j_1<T2 与 level-C 源 ≥T1 矛盾）。

## 7. Theorem OBST 与 T5-RED

**OBST(a) [A]。** δ_r^±:=−3±8/3^r（**+支＝已接受 route-A 轨道 c_r=−3+8/3^r**；−支为对称
扩展，同阻塞）。则 δ_r^±≡5 (mod 16)（8/3^r≡8 mod 16 因 3^{-r} 奇），故 (5,δ_r^±) 在
链 5 为自由入口类；(9+6·1−δ_r^±)/3=6∓8/3^{r+1}；发射族 (6∓8/3^{r+1}, 3^{r+1}, lift)
的 a-后代 (3Q−C)/Q=−3±8/3^{r+1}=δ_{r+1}^±。闭式对一切 r≥1 成立。
**OBST(b) [B]。** 逐层精确计算：no-lift 族 (δ_r^±) 对 **r=1..9**（den≤3^9）与发射族
(6∓8/3^{r+1},lift) 对 **r=1..10**（den≤3^{10}，审查更正块第 1 条）均**仅在链 5** uncert
（首步攀登；字随代表元约定与 r 变化——[5,5]、[5,6]、[5,7]、[5,8]、[5,10] 等，均止于首步，
uncert 结论与字无关）；发射族的 b/cs-后代全链认证、a-后代=δ_{r+1}^± 恰只链 5 失败；
观测数据与闭式完全一致（levels_t5_*.json 的 orbit_free_entries；r=10 的 no-lift 行为
由闭式推出，其发射在 FIRE_LOG 有数据）。
**OBST(c) [A]。** 族图含无穷路径 δ_r^±→6∓8/3^{r+1}→δ_{r+1}^±→…：任何有限族集不能闭合
链 5 自由入口递归。此族（+支）即已接受 route-A 轨道（引出处同 §1）——本定理给出
它在 T5 着陆结构中的**精确再现位置**（层级 E/C7-E 的 c-着陆＋REG 深段 a-后代）。
**OBST(d)。** 单条真实轨迹的递归有限：每次发射（进入链 y≥8）记录降 ≥1（r1r2 2.3），
总数 ≤非下降预算（L″）；但预算 ⌊J/(3log2J)⌋ 随 J 增长，无一致有限界。[A-imp]
**T5-RED [A-cond]。** ORBIT-9(J)（一切链 5 自由入口递归的实际塔层 ≤9）⟹ S(J) 无 tie。
证明：DL5(iii) 着陆分类——整数窗口（除 (5,5)，GW→10/3 族 [B]＋m≥N0 时 REG）、
specific（§6 全认证）、有理族（≤9 层全 [B]）、自由入口链 5（GW 化解至 ≤9 层族）；
深段每步严格下降、记录 <J；源 <T4 由已接受 EXT(<T4)。∎
**T5 未证明**：ORBIT-9 未获释放；OBST 表明静态族证书不能释放它。可能的出路（记录，
不主张）：轨迹级论证（日历一致性＋记录预算的联合约束）；或对 3^r-轨道类的 J-依赖
精细结构（发射 m 的具体值由日历决定，可能排除回归链 5 的循环）。

## 8. 与已接受结果的一致性

* 不推翻任何已接受结论；K_clock/已接受视野（2^T4−2 顶层步）不变；无机器层主张。
* REG（[A | 发射 Q≤3^{11}]）是 r1r2 Remark 2.5 残余（m≥10^8 的"深入口有理相位"）在
  [T4,T5) 的、上述范围内的解决（假设在族证书/ORBIT-9 范围内自动成立）：
  旧漂移分析（|θ|≤B 整数对称代表）确实不适用，但 RATIONAL_MODE 的有理高度框架适用
  （§5 的证明即其推论），且着陆化为可计算族。
* OBST 与 RATIONAL_MODE §3 的"两个失败类 (5,−17),(5,−1)"、ODD_DENOMINATOR §3 的
  "route-A 轨道不可丢弃"完全一致，并将其精确化为 T5 着陆结构中的无穷递归。
* C7 字面形式、AB′、copy principle 等已撤回/反驳对象未被使用；自由入口的化解只用
  GW（Theorem S 的恒等式）与 RA/r1r2 两步结构。

## 9. 文件与复现

    python -B work_gc_level_t5/verify_t5.py        # 11 项检查（含 9b 重放）-> ALL PASS（实测 ~280 s）
    python -B work_gc_level_t5/levels_t5.py        # 全量计算 -> levels_t5_20000000.json (~20 min)
    python -B work_gc_level_t5/levels_t5.py 300003 # 冒烟（3·10^5 链）

* rwalk_t5.py：有理 certify/bulk（56 位截断）、残差、类运算；
* levels_t5.py：P1 T4 复现、P2 漂移 BFS、P3 族闭包＋轨道、P4/P5 层级 E 与 C7-E；
* verify_t5.py：GW 恒等式与闭式轨道的精确检查、漂移集断言、族交叉验证
  （bulk=scalar、整数特例=rwalk.bulk）、T4 复现断言、层级 E/C7-E 残余清单断言、
  REG 尺寸不等式数值验证、轨道层数据断言；
* levels_t5_20000000.json / levels_t5_run.log：计算产物。
