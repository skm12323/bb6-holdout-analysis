# 审阅报告：`work_c3_drift/RATIONAL_MODE.md`

审阅者：审阅者-rational-mode（本轮四份未审文档之一）
日期：2026-10-23
范围：全文 148 行逐行阅读；只读仓库其余部分；未修改 `work_c3_drift/`；未 git 提交；
不声称全局 EXT、不改变 K_clock。背景按任务要求读取：`CHECKPOINT_1RB1LA_0RC0RD.md`
L614–681、`reviews/c3_drift_review_record.md`、`work_r1r2/NOTES.md` §0–5、
`work_claude_shifted/NOTES.md` §1–5、`work_global_ext/PROOF_EXT.md` §2、
`work_c3_drift/C5_EXTENSION.md` §1–4、`work_c3_drift/CONGRUENCE_TARGET_NOTE.md` §4–5，
以及三份障碍 `ORBIT_SHIFT_OBSTRUCTION.md`、`STOP_CHECKPOINT_2026_10_21.md`、
`OPTIMAL_PHASE_ENCODING.md`。

## 0. 总评（先行）

`RATIONAL_MODE.md` 是一份**诚实的条件引理**：它给出分母恰为 3 的有理相位类在
高参数（`j>=N0`）上的收缩论证——在 HR5 与高度假设下，至多 `h3(q)` 条高参数链内离开
深段，且每步记录严格下降；着陆认证被明确留作未决。核心代数（RA、RC、四个许可映射、
`|C_t|<=C0+3t`、SIZE3、塔估计）逐条核对**正确**，常数 3、15<16、`N0/2+4`、
`2log2j+5` 均核实无误。

主要问题：

1. **L47“This excludes exact resonance”是错的**（critical）。`C!=0 mod 3` 只排除有理
   代表元 `3k+C/3=0`；精确共振（NT failure / one-step descent）是 k 的同余条件，
   完全可能发生（论证见错误 E1）。文中 L48 自己也说“不排除 non-descent”，与
   “排除共振”自相矛盾。
2. **归纳隐含假设“持续 c 步的 ε 只能是 3 或 5”，未声明**（critical，缺前提）。HR5 只
   覆盖 `ε>=7`，留下 `ε=4,6` 未处理；已接受的 weight grammar（`PROOF_ROOT_PHASE.md`
   §1：`ε=W+1`、W 恒偶；`PROOF_LOW_DEFICIT.md` §1：`ε=3` ⇔ A，`ε=5` ⇔ AA/BA）保证
   ε 为奇数，因此只需排除 3、5，但文中没有引用这一事实。
3. **只覆盖分母 3（r<=1），不是任务要求的一般 `s in Z[1/3]`**（major）。`D=C/3+b2^j`
   无法表示 `1/9` 或 O1 的 `eta_r=-5+8/3^r`（r>=2）。全文没有出现 r、祖先精度 sigma、
   也没有触碰 O1 的 r–sigma 耦合。标题“Low-height”中的 height 是 `|C|/3`，不是 O1 意义
   下的实高度；两者不能混同。
4. **着陆扫描范围/计数不足**（major）。脚本只扫 `j=5..128`、每对 (j,C) 只取一个 lift
   （`d=C*3^{-1} mod 2^{j+1}`）；而 §2 的收缩只保证着陆参数 `<N0=2*10^7`（B 主导时
   `<=10^7+2`，κ 主导时可逼近 `N0-1`），远大于 128。完整的 (C,b,j) 类为 7,936 个，不是 3,968 个。
   我的复核显示两个 lift 各 3,966 end / 2 ceiling，失败仍是同一对 (j,C)
   （(5,-17) 与 (5,-1)），所以**定性结论仍成立**，但计数和“覆盖全部类”的措辞要改。
5. **全文没有说明对 J 的依赖**（major，违反本轮硬性要求）。`h3(q)` 只写在起点参数 q 上；
   文中从未说明 q 与 J 的关系，也没有写出 `log* J`、N0、T_h 的依赖。§2 的界是
   `h3(q)`（对 q 的迭代对数），这是正确的尺度无关类型，但必须点明。

结论：本文件可作为**条件引理 [A|HR5+高度] + 有限数据 [B]（范围 5..128）**保留；
不能作为“着陆已认证”或“gateway 已闭合”的依据，更不能作为全局 EXT 的一部分。
其中 (RA)、(RC)、SIZE3、塔估计可以原样引用（在补齐 E1/E2 的措辞后）。

## 1. 验证命令与输出

### 1.1 工作流已运行的文档自带脚本（我未重跑）

命令：`python -B work_c3_drift/verify_rational_mode.py`

工作流输出（exit 0）：

```
{"status": "PASS", "review_status": "unreviewed", "a_transition_checks": 2360,
 "landing_scan_range": [5, 128], "landing_status": {"end": 3966, "ceiling": 2},
 "scope": "All-scale mode lemma is conditional. These are synthetic class tests,
  not claimed canonical shifted trajectories ..."}
```

脚本实际行为（`work_c3_drift/verify_rational_mode.py` L7–L45）：

* `Calendar(256)`；分子闭包由 `C0 in {10,26}` 出发、5 层映射 `{9-c,c-3,c,c+3}` 生成
  （L8–L15），共 32 个分子；
* 着陆扫描 L17–L25：`d=(c*pow(3,-1,1<<(j+1)))%(1<<(j+1))`，`bounded_walk(cal,1<<j,
  (1<<j)+d,j+1,signed=True)`，`j=5..128`。**只取了一个 lift**（`d` 本身，即文中的 b=0；
  另一个 lift `d+2^j` 未扫）。
* a 步检查 L26–L37：仅当 `q=1+v2(9k+c)<=j-2` 时，对 `lift in (0,1)` 两 lift 都检查
  `val(xn)==q` 与 `3*(tn-xn) ≡ 9-c (mod 2^{q+1})`。

### 1.2 我另跑的 scratch 脚本（本次会话实际执行）

目录：`work_landing_symbolic/reviews/scratch/`（只写此处）。

**(a) `python -B work_landing_symbolic/reviews/scratch/scan_both_lifts.py`**

输出（约 0.35 s）：

```
numerators: 32
lift 0: {'end': 3966, 'ceiling': 2} nfail=2 hist={5: 2}
    {'j': 5, 'C': -17, 'lift': 0, 'delta': '37', 'status': 'ceiling', 'chains': 1}
    {'j': 5, 'C': -1,  'lift': 0, 'delta': '21', 'status': 'ceiling', 'chains': 1}
lift 1: {'end': 3966, 'ceiling': 2} nfail=2 hist={5: 2}
    {'j': 5, 'C': -17, 'lift': 1, 'delta': '5',  'status': 'ceiling', 'chains': 1}
    {'j': 5, 'C': -1,  'lift': 1, 'delta': '53', 'status': 'ceiling', 'chains': 1}
gateway C=10: {'end': 124} fails=[]
gateway C=26: {'end': 124} fails=[]
json: work_landing_symbolic/reviews/scratch/scan_both_lifts.json
```

要点：
* b=0 的 3,966/2 与文档一致；b=1 同样是 3,966/2，失败是**同一对 (j,C)**；
  lift 1 的 δ=5 与 δ=53 正是已接受窗口证书中的裸 tie (5,5)、(5,-11)
  （mod 64），lift 0 的 37、21 是它们的另一 lift。文档只列出了另一 lift。
* 实际网关类 `(10-2^j)/3`、`(26-2^j)/3`（文档 L19–L20 指出其 (C,b)=(10,1),(26,1)）
  在 `j=5..128` 全部 certify（各 124/124）。这与 r1r2 的 `5<=m<2*10^7` 证书相容，
  但注意：文档 §3 的扫描用的是 b=0，**不是**这两个网关类本身；我补扫的 b=1 才是网关类。
* 两个失败分子 `-1`、`-17` 恰好是网关分子 `10`、`26` 在 a 映射 `C->9-C` 下的像；
  因此这两类并非纯“合成”无关对象：类层面它们是网关的第一次 a 步着陆像（是否在
  规范日历中实现为 j=5 取决于 `1+v2(9k+10)=5` 的同余，未证）。

**(b) `python -B work_landing_symbolic/reviews/scratch/check_constants.py`**

输出（节选）：

```
a_checks_reproduced: 2360        a_skipped_pairs: 8
j_N0: kappa=202589989870, bitlen(3kappa)=40, j_minus_2=19999998,
      SIZE3_exact=true, bitlen(3(kappa+B))=10000002
L3 rows (j, term1, term2, L3, claimed_bound, ok):
  20000000   10000002 39  10000002 10000004.0 true
  20000001   10000002 39  10000002 10000004.0 true
  100000000  10000002 42  10000002 10000004.0 true
  1e20       10000002 84  10000002 10000004.0 true
  2^100      10000002 118 10000002 10000004.0 true
h3: q=N0 -> [1, 10000002]; q=1e8 -> [1, 10000002]; height_ok both true
json: work_landing_symbolic/reviews/scratch/check_constants.json
```

要点：`a_transition_checks=2360` 被独立复算（32 个分子 × 2 lift，跳过 8 个 j=5 的
弱下降对：C=-17,-1,7,23 各两 lift，因为 `1+v2(9+C)>3`）；`j=N0` 时
`3(κ+B)` 的精确位长 10,000,002 < j-2=19,999,998，SIZE3 严格成立；
`L3(j)<=max(2log2j+5,N0/2+4)` 在 5 个采样点成立；`h3(N0)=h3(1e8)=1`，
故 §2 的高度假设在网关处是 `(10+3)/3=13/3 <= B`，平凡满足。

**未运行/不可运行的部分**：§2 的 `j>=N0=2*10^7` 高参数收缩无法用 `Calendar(B)`（B<=1024）
做机器验证；它只能是解析论证。我的检查只覆盖其常数前提。`Calendar(256)` 也不足以验证
`j>256` 的着陆类；文档的 j<=128 扫描正好落在其范围内，但这也说明它离真实着陆范围很远。

## 2. 逐条结论表

标签说明：`[A]` 对全部参数证明（假设列全）；`[B]` 有限精确计算（范围写明）；
`[C]` 猜想/数据。文档本身未使用这套标签（见 minor 错误 E10）。

| # | 行号 | 结论（一句话） | 标签 | 是否正确 |
|---|---|---|---|---|
| 1 | L10–L13 | 用 `D=C/3+b*2^j (mod 2^{j+1})`、`C` 整数且 `3∤C`、`b in {0,1}` 表示精确亏损类。 | A（表示约定） | **正确**，但仅覆盖分母 3（r<=1）；不是一般 `Z[1/3]`。 |
| 2 | L15–L20 | 小的 `\|C/3\|` 不蕴含旧的 `\|theta\|<=B` 深条件；网关类 `(10-2^j)/3`、`(26-2^j)/3` 的 `(C,b)=(10,1),(26,1)`。 | A | **正确**。我核对 `10/3+2^j ≡ (10-2^j)/3 (mod 2^{j+1})`（因 `4*2^j/3 ≡ 0`），26 同理。 |
| 3 | L22–L24 | (RA) 若 `1+v2(9k+C)<=j-2`，则精确地 `j'=1+v2(9k+C)`、`C'=9-C`、`b'=0`。 | A | **正确**。两 lift 均成立；脚本 2,360 项与独立复算一致。 |
| 4 | L26–L30 | RA 的证明：`3k+D ≡ (9k+C)/3 (mod 2^j)`，`3x/2` 的 valuation 为 `j-1>j'`，`D'=3-D-x/2` 的误差项在 `2^{j'+1}` 消失；由此得 `b'=0`。 | A | **正确**，但证明没写出 `b*2^j` 项在乘 2 后是 `2^{j+1}`、在 `mod 2^{j'+1}` 下为零（需要 `j>=j'+1`，由 `j'<=j-2` 保证）。 |
| 5 | L32–L36 | (RC) b/c 步 `D'≡D+Phi-2 (mod 2^{j'+1})`（S1 给出误差 valuation `>=j'+1`）；严格降参数时 `C'=C+3*Phi-6`、`b'=0`。 | A | **正确**。`j'<=j-3` 保证 `b*2^j` 项消失；`C'≡C mod 3`。 |
| 6 | L38–L44 | 许可映射：`a:C->9-C`；`b` 或 `cAA:C->C-3`；`c3:C->C`；`cBA:C->C+3`。 | A（用已接受的 ε=3/5 恒等式） | **正确**（`Φ-2` 分别为 −1、−1、0、+1，与 C5_EXTENSION §1 一致），但 “proposed” 措辞过时（C5_EXTENSION 已被接受），且未声明“持续 c 步的 ε 只能是 3 或 5”。 |
| 7 | L46–L47 | 四个映射保持 `C!=0 mod 3`；因此 `9k+C` 永不为零。 | A | **正确**（`C'≡C mod 3`；`9k+C≡C mod 3`）。 |
| 8 | L47 | “This excludes exact resonance.” | — | **错误**。见 E1：它只排除有理代表元 `3k+C/3=0`；精确共振（无论用 exact defect 还是 work_deep 的 symmetric representative）都是 k 的同余条件，不被 `C≢0 mod 3` 排除。L48 的“不排除 non-descent”与这句自相矛盾。 |
| 9 | L54–L57 | 定义 `L3(j)=max(1+⌊log2(3(κ+B))⌋, ⌊log2(6(j-1)P_clock+5)⌋)`、`h3(q)=min{t:L3^t(q)<N0}`。 | A（定义） | **正确**。 |
| 10 | L58–L65 | 起点 `q>=N0`、`C0 in {10,26}`；高度假设 `(C0+3*h3(q))/3<=B`；HR5：每个 `ε>=7` 的 c 步都退出到 `<N0`；并声明旧 R1/H5 不自动蕴含 HR5。 | 假设（非定理） | **正确且诚实**。HR5 是来源/轨迹条件而非参数上界，符合本轮“附加条件必须是来源/相位条件”的要求；但 HR5 本身未证。 |
| 11 | L67–L70 | 在 HR5+高度假设下，至多 `h3(q)` 条高参数链内到达偶端点或 `<N0` 参数；每步记录严格下降。 | A|条件 | **正确**。a 步 `j'<=j-2,Γ+=1`；b/c 步 `j'<=j-2-ε,Γ+=1+ε`，两者记录都至少降 1。 |
| 12 | L72–L76 | 任何异常 c 着陆之前，`\|C_t\|<=C0+3t`；理由：`C->9-C` 保持 `\|C-9/2\|`，其余映射改变至多 3。 | A | **正确**（`\|C\|<=\|C-9/2\|+9/2<=C0+3t`，C0=10,26）。 |
| 13 | L77–L84 | 每个 `j>=N0` 的 a 步：`\|3k+C/3\|<=κ(j)+B<2^{j-3}`，`\|9k+C\|<=3(κ+B)`，故 `j'<=1+⌊log2(3(κ+B))⌋`。 | A|条件（高度+C锁） | **正确**，但 L78 没有写明用了 L60/L72 的高度界；`3k<=κ(j)` 来自已接受的 CLOCK（τ(n)<=nP(n)）。 |
| 14 | L86–L88 | 因子 3 不能去掉；“奇分母有理数可能有大于其绝对值对数的 2-adic valuation”，所以 L3/h3 取代旧 L/Λ。 | A | **结论正确**（`\|9k+C\|=3\|3k+C/3\|` 正是因子 3 的来源）；解释性句子不够精确（真正原因是分母 3 使分子放大约 1.585 bit），但不影响常数。 |
| 15 | L90–L96 | (SIZE3) 对每个 `j>=N0`：`3(κ(j)+B)<(12+3)*2^{j-6}<16*2^{j-6}=2^{j-2}`。 | A | **正确**。用 `κ<2^{j-4}`（work_deep Lemma 2.1 [A]）与 `B<=2^{j-6}`；我在 j=N0 用精确整数核对：3(κ+B) 位长 10,000,002 < 19,999,998。 |
| 16 | L97–L102 | 因此 `j'<=j-2`、`L3(j)<j`、L3 非降；对至多 h3(q) 步归纳同时得高度界与收缩；HR5 处理其余 c 步；不使用大整数对称相位假设。 | A|条件 | **正确**（“L3 is nondecreasing” 未证，但为真：κ、P_clock 非降；第二项 `<j` 的证明在 L104–L106 才给出）。 |
| 17 | L104–L115 | 塔估计：`L3(j)<=max(2log2j+5,N0/2+4)`；`U_1=2^{(N0-5)/2}`，`U_{r+1}=2^{(U_r-5)/2}`；`N0<=q<U_r ⇒ h3(q)<=r`；`C0+3r<=3B` 时高度条件成立。 | A | **正确**。我核对了 `3(κ+B)<=6max(1.5j²,B)`、`1+log2(9)<5`、`1+log2(6)<4`，以及 5 个采样点的 L3 上界；`h3(N0)=h3(1e8)=1`。 |
| 18 | L117–L118 | 剩余假设 = reached-prefix inputs、HR5、高度范围；着陆认证仍然分离。 | A（声明） | **诚实**，但 “reached-prefix inputs” 未精确定义（应写明：实际 S(J) 到达参数 q、类为 `(10-2^q)/3` 或 `(26-2^q)/3`、记录 `<J`，来自 r1r2 网关引理）。 |
| 19 | L122–L125 | 强 a/b/低亏损 c 着陆的类为 `C'/3 mod 2^{j'+1}`、`b'=0`；高亏损 c 着陆有精确的一般类但需另控；`C!=0 mod 3` 不自动认证。 | A | **正确**（RC 对高亏损 c 步也给 `b'=0` 和 `C'=C+3Φ-6`，只是该类未认证；文档说“needs separate control”是对的）。 |
| 20 | L127–L131 | 测试枚举从 10/26 出发至多 4 个映射的分子集，检查 `j=5..128`；3,968 类中 3,966 认证、2 个失败：`(5,-17,37)`、`(5,-1,21)`。 | B（范围 j=5..128，32 分子） | **实质正确但计数/范围有误**：只扫了一个 lift，完整 (C,b,j) 类为 7,936 个；两 lift 各 3,966/2，失败为同一对 (j,C)；且 128 远低于 §2 可达的着陆参数上界 `<N0=2*10^7`。 |
| 21 | L133–L137 | 两个失败是“rational-mode bare-tie obstruction”；合成检查、非断言可达；`C=-1` 是已接受 route-A 3-adic 轨道值 `-1/3`，不可丢弃；无限分母障碍仍适用。 | A-imp / C | **基本正确**：`-1` 即 `c_1=-3+8/3=-1/3`（PROOF_EXT §4 Theorem O 列出 10/3, −1/3, 46/9, …）；但“that theorem 的 infinite-denominator obstruction”具体来自 `ORBIT_SHIFT_OBSTRUCTION.md`（未审），不是已接受的 Theorem O 的直接陈述，最好分别引用。 |
| 22 | L141–L148 | 2,360 次强 a 步比较（两输入精度位）、RA 及额外位成立；有限分子界与着陆扫描通过，两个失败保留为数据；验证的是代数，不是 HR5 或着陆安全。 | B | **正确**（我复算 2,360；脚本 PASS）。 |

## 3. 错误清单（行号 + 严重度 + 修正）

### E1（critical）L47：`C!=0 mod 3` 不能排除 exact resonance

* **问题**：`9k+C` 永不为零只说明有理代表元 `3k+C/3` 不为零（`9k+C=3(3k+C/3)`）。
  但 RA 的下降失败（NT failure / one-step descent / 共振）是 **k 的同余条件**，不是
  `9k+C=0` 这个方程：
  * 用 RA 的 exact defect `D`：`D ≡ C/3+b*2^j (mod 2^{j+1})`，于是
    `3(3k+D) = 9k+3D ≡ 9k+C+3b*2^j (mod 2^{j+1})`；若 `3k+D=0`（exact 形式的共振），
    则 `9k+C ≡ -3b*2^j (mod 2^{j+1})`，而 9 在 `2^{j+1}` 下可逆，该同余对每个 j
    都有解 `k ≡ -(C+3b*2^j)*9^{-1}`。
  * 用 work_deep 的 symmetric representative `theta_t`（`z=3k+theta_t=0`）：
    `D = theta_t + 2^j*m`，故 `3k+D=2^j*m`，只给出 `9k+C+3b*2^j ≡ 3*2^j*m
    (mod 2^{j+1})`，仍是 k 的同余（模 `2^j`），同样不被 `C≢0 mod 3` 排除。
  换言之，“`9k+C` 永不等于 0”与“共振被排除”是两件不同的事；是否真的在规范链上
  发生取决于日历的 k（这正是文档没有证明的），但 L47 的逻辑蕴含
  “C 非 3 倍数 ⇒ 无共振”是**假的**。若作者把 “exact resonance” 定义为有理代表元
  `3k+C/3=0`，则该句为真，但那不是 work_deep 的 resonance，也不能替代后者
  （以及 one-step descent）的排除。
* **修正**：删除 “This excludes exact resonance”，改为：
  “`C!=0 mod 3` 只排除 `3k+C/3=0`（有理代表元消失）。精确共振是 k 的同余条件
  （exact-defect 形式：`9k+C ≡ -3b*2^j (mod 2^{j+1})`；symmetric 形式给出同类同余），
  本段不排除；在高参数前缀上它由 §2 的 SIZE3（`1+v2(9k+C)<=j-2`）连同
  one-step descent 一起排除，前提是高度界 `|C|/3<=B`。”
  （L48 的“不排除 non-descent”保留，但与上一句要一致。）

### E2（critical）L38–L44 + L62–L63：缺少“持续 c 步 ε∈{3,5}”的前提

* **问题**：§2 的分子归纳只对四个映射成立，即只对 `ε=3`（c3）、`ε=5`（AA/BA）和 b（Φ=1）
  成立。HR5 只排除了 `ε>=7`，`ε=4` 和 `ε=6` 未被覆盖。若存在 ε=4 或 6 的持续 c 步，
  `C'=C+3Φ-6` 的 Φ 不是 −1/0/+1，`|C_t|<=C0+3t` 立刻失效，SIZE3 与收缩都不成立。
  已接受文献实际上保证了 ε 为奇数：`PROOF_ROOT_PHASE.md` §1（`ε=W+1`，W 恒偶，
  “every type-c deficit is odd and at least 3”），`PROOF_LOW_DEFICIT.md` §1
  （`ε=3` ⇔ A；`ε=5` ⇔ AA/BA）。但本文没有引用，因此作为 [A] 命题前提不完整。
* **修正**：在 L38 或 L62 前加一句：“由已接受的 weight grammar（`PROOF_ROOT_PHASE.md` §1、
  `PROOF_LOW_DEFICIT.md` §1），c 亏损 ε 恒为奇数且 >=3；故除 HR5 的 ε>=7 外，
  只剩 ε=3（c3）与 ε=5（AA/BA），其 Φ 分别为 2、1、3。”并把 “the proposed low-deficit
  identities” 改为 “the accepted low-deficit identities（C5_EXTENSION §1）”。

### E3（major）L10–L20、L58：只覆盖分母 3，不是一般 `s in Z[1/3]`，且不触及 O1

* **问题**：`D=C/3+b*2^j` 且 `3∤C` 只能表示分母整除 3 的相位（r<=1）。`1/9` 或
  O1 的 `eta_r=-5+8/3^r`（r>=2）无法写成 `C/3`（整数 C）。因此：
  * 任务要求的“一般 `s in Z[1/3]`、分母 `3^r`、高度 h”没有被覆盖；
  * O1 的核心——“实际分母深度 r 与祖先精度 sigma 关联，或排除危险剩余类”——
    全文没有任何处理；L137 只有一句“无限分母障碍仍适用”；
  * 标题 “Low-height rational phases” 中的 height 是 `|C|/3`，与 O1 的实高度
    `|eta_r|<=5` 不是同一个量。O1 的反例正是“实高度<=5 但 r 巨大”的位移，
    本文的分母 3 表示根本触及不到。
* **修正**：在 §1 开头显式写“本节只处理分母 Q=3（r<=1）的相位；一般奇数分母见
  ODD_DENOMINATOR.md（同样未审）”。在 §2 末尾或 §3 加一段：本引理不覆盖
  `ORBIT_SHIFT_OBSTRUCTION.md` 的 `eta_r`（r>=657306078883964），也不声称
  “所有有界高度位移安全”；该障碍需要的 r–sigma 耦合或危险剩余类排除仍未证明。
  标题建议改为 “Rational phases of denominator 3 after a large gateway”。

### E4（major）L127–L131：着陆扫描的范围、lift 与计数

* **问题**：
  1. **范围**：§2 的收缩给出着陆参数 `j'=1+v2(9k+C)`，其绝对上界是
     对最后一次深链 `j_t`，`j'=1+v2(9k+C)<=1+⌊log2(3(κ(j_t)+B))⌋`；B 主导时约
     `10^7+2`，κ 主导时可逼近 `N0-1`。总之 `j'<N0=2*10^7`，不是 128。
     扫描只到 `j=128`，无法认证 `j'∈[129,N0)` 的着陆类。
  2. **lift**：文档的表示含 `b∈{0,1}`，但脚本只取 `d=C*3^{-1} mod 2^{j+1}`（b=0）。
     完整 (C,b,j) 类是 32×124×2=7,936，不是 3,968。
  3. **计数**：我的补扫显示 b=1 也有 2 个失败，且是同一对 (j,C)（(5,−17) 的 δ=5、
     (5,−1) 的 δ=53，即已接受的裸 tie (5,5)、(5,−11)）；b=0 的 3,966/2 因此
     不因补扫而改变。**定性结论正确，计数与“所有类”的措辞错误。**
  4. 两个失败分子 `−1`、`−17` 恰是网关分子 `10`、`26` 的 a 像；类层面它们是网关的
     第一次 a 步着陆像，不只是“任意合成类”。是否在规范日历中实现为 j=5 取决于
     `1+v2(9k+10)=5`（即 `k≡22 mod 32`）等未证同余；文档的谨慎措辞（“not asserted
     reachable”）是恰当的，但“synthetic”不应被读成“与网关无关”。
* **修正**：把 §3 改为：“在 32 个分子 × 两个 lift × `5<=j<=128` 上，3,966+3,966 个
  类认证，两个 (j,C) 对（各两个 lift）在 j=5 失败，即 (5,5)、(5,-11) 两个已接受裸 tie。
  该 [B] 数据不覆盖 `j>128`，而 §2 的着陆参数可达 `N0-1≈2*10^7`；因此它不构成着陆认证。”
  若要覆盖 `j<N0`，需要另写扫描（`Calendar` 需 B>=N0，超出本题允许的 B<=1024）；
  这也说明该 [B] 数据只能是 gadget 级证据。

### E5（major）L117–L118、L143–L148：没有说明对 J 的依赖

* **问题**：本轮硬性要求“必须说明每一部分对 J 的依赖（含 log* J、N0、2*10^7、T_h）”。
  全文没有出现 J，也没有说明起点参数 q 与 J 的关系；`h3(q)` 只是对 q 的迭代对数。
  读者无法判断：给定 S(J)，q 是多少？`h3(q)` 与 `log* J` 是什么关系？`N0=2*10^7`
  和 `B=2^{10^7}` 在哪里进入？`U_r` 与 work_deep 的 `T_h` 谁大？
* **修正**：在 §2 开头写明：“q 是本段起点的链参数；若起点来自 r1r2 网关，q=m 是
  网关输出参数，与祖先 J 无关（m 由 `v2(9k+16)` 等决定）。`h3(q)<=log* q`；
  对 `J<K_clock`，q 至多与 J 同阶，且 `U_4>K_clock`，故 `h3(q)<=4`。N0、B 只通过
  L3 的常数 `N0/2+4` 与 SIZE3 进入；本文不使用 T_h；与 work_deep 的 T_h 相比，
  `U_r` 因因子 3 而更小（L115）。” 并给出 `h3(q)` 对 q 的单调性/上界。

### E6（major）L4–L6、L122–L125：gateway 的“continuation”并未闭合

* **问题**：开头说“This addresses how to continue a gateway whose output parameter is
  above the existing finite certificate cutoff”，但 §2 只给出高参数段的收缩，
  §3 明确说着陆认证分离。对 r1r2 的 RES（m>=10^8 的裸 tie 网关），本文能证明的只是
  “一步离开深段、记录下降”，**没有证明着陆地类认证**；而 E4 显示 §3 的数据只到
  j=128，远不足以覆盖 `j'` 可达的 `N0-1≈2*10^7`。因此“continue a gateway”应改为
  “reduce the high-parameter part of a gateway to a landing class, leaving the landing
  certificate open”。
* **修正**：改写 L4–L6 与 L117–L118：“本文把网关的高参数段在 <=h3(q) 步内化为一个
  显式着陆类（`C'/3 mod 2^{j'+1}`, `b'=0`），每步记录严格下降；着陆类的认证仍是
  开放问题，本文不声称 gateway 已闭合。” 明确写出剩余目标：对
  `C'∈{9-C0, C0±3, C0}`（a/b/c3）及高亏损 c 的 `C+3Φ-6`，在 `j'` 到 `N0` 的范围
  认证或走有限 gateway。

### E7（minor）L77–L84：高度假设的使用未写出

* **问题**：L78 的 `|3k+C/3|<=κ(j)+B` 需要 `|C|/3<=B`，来自 L60 的假设与 L72 的归纳；
  文中没有在同一句引用。`3k<=κ(j)` 也需要已接受的 CLOCK。读者若只看 L77–L84
  会以为这是深段条件的直接推论。
* **修正**：在 L78 前加“由 L60 的 `(C0+3h3(q))/3<=B` 与 L72 的 `|C_t|<=C0+3t`
  （t<=h3(q)），有 `|C|/3<=B`；再由 CLOCK `3k<=κ(j)`，得 ...”。

### E8（minor）L97：`L3 is nondecreasing` 未证明

* **问题**：该句没有证明。它其实为真（κ(j) 与 P_clock(j-1) 都非降），但作为 [A]
  命题应补一行；否则 h3 的迭代定义虽不依赖单调性，读者无法核对 `U_r` 归纳。
* **修正**：加“κ 与 P_clock 非降，故 L3 非降（P 是阶梯函数但单调）”。

### E9（minor）L90：“no extra hypothesis is needed” 易误读

* **问题**：SIZE3 本身确实无条件（κ、B 是 j 的函数），但它的**应用**（`j'<=j-2`、
  RA 适用）需要 L60 的高度假设。强调句容易被读成“整个 §2 无条件”。
* **修正**：改为 “SIZE3 holds for every j>=N0 with no extra hypothesis; its application
  to j' uses the height bound |C|/3<=B from L60.”

### E10（minor）L38、L52、L143：措辞/标签

* L38 “the proposed low-deficit identities” —— C5_EXTENSION 已在
  `CHECKPOINT_1RB1LA_0RC0RD.md` L670–673 的 work_c3_drift 节被接受，应改为
  “accepted”。
* L52 “the accepted split estimate” —— work_deep 的引理名是 “size”（Lemma 2.1）；
  “split” 是笔误。
* L143 “testing both incoming precision bits” 对 a 步成立，但对着陆扫描不成立
  （只扫一个 lift），建议分别措辞。
* 全文没有 [A]/[B]/[C] 标签；按项目约定（本轮任务）应给每条实质结论加标签。
  最低限度：§1–§2 标 [A|HR5+高度]，§3 标 [B, j=5..128, 32 分子]，§3 的
  “C=-1 是 route-A 轨道值” 标 [A-imp]，“无限分母障碍” 标 [A-imp/C]。

### 报告级（不进前 10 的错误）：L136–L137 的引用归属

* `PROOF_EXT.md` §0 row O / §4 Theorem O 是“route A 方法不能由有限证书闭合”的
  已接受陈述，列出了 `c_m=-3+8·3^{-m}`（10/3, −1/3, 46/9, …）；而具体的
  “`eta_r` 在首个输出就让严格安全失败、r>=657306078883964” 来自
  `ORBIT_SHIFT_OBSTRUCTION.md`（**未审**），不是 Theorem O 的直接推论。L137
  “The infinite-denominator obstruction of that theorem still applies” 把两者
  混在一起；应分别引用，并注明 ORBIT_SHIFT 的未审状态。

## 4. 范围依赖（N0、B、2*10^7、T_h、log*、有限扫描）

| 行号 | 依赖 | 说明 |
|---|---|---|
| L52–L56 | `N0=2*10^7`, `B=2^{N0/2}=2^{10^7}`, κ, P_clock | 从 work_r1r2 §0 导入；所有常数界都通过这些量。 |
| L57 | `h3(q)=min{t:L3^t(q)<N0}` | 阈值 N0=2*10^7 固定；h3 是对 q 的迭代对数（log* 型），不是对 J。 |
| L58 | `q>=N0` | 高参数段的下界；q 是本段起点参数，文档未说明它与 J 的关系（E5）。 |
| L60 | `(C0+3*h3(q))/3<=B` | 高度/相位条件；对网关 q=1e8 为 13/3<=B，平凡满足（我核对 h3=1）。 |
| L62–L63 | HR5 的阈值 N0 | “ε>=7 的 c 步退出到 <N0”；这是来源/轨迹条件，未证（与 C5 的 H5 同类但更强，因为它是 rational-mode 前缀而非初始深段）。 |
| L67–L70 | `h3(q)` 条高参数链 | 迭代对数上界；对 q=1e8，h3=1；对 q<K_clock，h3<=4（由 U_4>K_clock，文档未写）。 |
| L77–L78 | `j>=N0` | a 步大小界只在深参数段使用。 |
| L90–L96 | SIZE3：`B<=2^{j-6}`, `κ<2^{j-4}` | 需要 `j>=N0`；精确核对：3(κ+B) 位长 10,000,002 < j-2。 |
| L97 | `L3(j)<j` | 对 `j>=N0`；第二项的证明在 L104–L106。 |
| L104–L115 | 塔 `U_1=2^{(N0-5)/2}`, `U_{r+1}=2^{(U_r-5)/2}`, `N0/2+4<N0` | 这是本文的 log* 塔；L115 明确说“not the old T_r bounds”。文档没有写出 U_r 与 work_deep 的 `T_h` 的大小比较（U_r<T_r，因为因子 3 使常数从 +3 变为 +5、N0/2+2 变为 N0/2+4）。 |
| L127–L131 | 有限扫描 `j=5..128` | 与 N0 无关的固定有限范围；远低于 §2 的可达着陆上界 N0-1≈2*10^7（E4）。 |
| L141–L143 | 2,360 次检查，`j=5..128` | 覆盖 37 个 odd-a 参数，跳过 8 个 j=5 弱下降对（C=-17,-1,7,23 各两 lift）。 |
| 全文 | 无 T_h、无 K_clock、无 log* J | 文档未提 J，也未提 T_h/K_clock 的具体值；只有 L115 的 “old T_r bounds” 一句。 |

## 5. 本轮目标对照（“与尺度无关的符号论证”）

本轮要求：输入相位 `theta+s`（`s in Z[1/3]`，高度<=h）时，着陆类可认证，或经有限步
gateway 化解且每步记录严格下降，界不依赖 J；否则写出必须是来源/相位条件的附加条件；
必须说明对 J 的依赖。

本文的覆盖情况：

* **有**：对分母 3、非整数相位（`3∤C`）、高参数 `j>=N0` 的类，给出有限步
  （`<=h3(q)`，log* 型）收缩与记录严格下降；附加条件是 HR5（来源/轨迹）和高度
  （相位），符合“不能是参数上界”的形式要求；不依赖祖先 J（但文档未说明，见 E5）。
* **没有**：
  1. 一般 `s in Z[1/3]`（分母 `3^r`, r>=2）——见 E3；O1 的 r–sigma 耦合完全未处理；
  2. 着陆类认证——§3 只有 j<=128 的 gadget 数据；实际着陆参数可达 N0-1≈2*10^7（E4/E6）；
  3. HR5 的证明——它本身是开放条件（C5 的 H5 类似；CONGRUENCE_TARGET_NOTE 的
     layer conjecture [C] 只针对初始深段）；
  4. O2 的仿射来源 `x=A U+beta`——本文只用相位类，不用 affine origin；O2 的
     “joint budget 不能在任意小二步 gateway 局部闭合”没有被反驳，只是本文的
     记录下降论证绕开了 W 预算（对高参数、有理相位、四映射成立的类）；
  5. O3 的相位编码——本文不涉及。

因此本文是通往目标的一块**正确的局部拼图**，但不是目标本身；不能据此声称
“所有有界高度位移安全”或“gateway 已闭合”。

## 6. 建议的下一步（供协调者）

1. 修 E1/E2 后，把 §1–§2 作为 [A|HR5+高度] 引理接受（像 C5_EXTENSION 那样附
   假设清单）；把 §3 明确降为 [B, j=5..128, 两个 lift]。
2. 把 §2 的“起点类”与 r1r2 网关引理显式对接：写出 q=m、类
   `(10-2^m)/3` 或 `(26-2^m)/3`、入口记录 `<J`，并把 `h3(m)<=4`（或 1）算出来。
3. 着陆认证的真正缺口是 `j'∈[129,N0)` 的类 `C'/3 mod 2^{j'+1}`。要么给出
   对所有 `j'` 的符号论证（例如利用 `C'` 小、`j'` 大时 a 步强下降，迭代到小参数），
   要么把它写成新的 [B] 扫描范围（需要 `Calendar` 到 N0，超出本轮 B<=1024 的许可），
   要么明确列为开放。
4. 若要接 O1，需要把表示从 `C/3` 换成 `C/3^r`，并把收缩阈值 `N_Q` 与祖先精度
   `sigma` 关联（`ODD_DENOMINATOR.md` 的 `N_Q=max(N0,4(d+2))` 是分母相关的阈值，
   不是 J 上界；但它仍是未审的，且没有解决 O1 的 r>=657306078883964 情形）。
5. 补一条对 J 依赖的明确陈述（E5）。

## 7. 复核用文件

* `work_landing_symbolic/reviews/scratch/scan_both_lifts.py`
* `work_landing_symbolic/reviews/scratch/scan_both_lifts.json`
* `work_landing_symbolic/reviews/scratch/check_constants.py`
* `work_landing_symbolic/reviews/scratch/check_constants.json`

两个脚本都可重跑（`python -B`，均 <1 s）；它们只读 `work_c3_drift/` 的库与日历，
不写 `work_c3_drift/`。
