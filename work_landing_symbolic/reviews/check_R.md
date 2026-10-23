# 独立复核报告：`work_c3_drift/RATIONAL_MODE.md` 与 `work_c3_drift/ODD_DENOMINATOR.md`

复核者：独立复核者-R（workflow subagent）
日期：2026-10-23
范围：只读 `work_c3_drift/` 两篇原文及已接受背景；只写 `work_landing_symbolic/reviews/` 与
`work_landing_symbolic/reviews/scratch/`；未修改原文；未 git 提交；未声称全局 EXT、未改 K_clock。
本报告中的 `confirmed` 表示“审阅者指出的问题在原文/重算中成立”，即使审阅者的解释/修正需要更正；
`refuted` 表示按原文与重算不成立；`uncertain` 表示证据不足。逐条证据在下面。

## 0. 本次实际运行的命令与结果

```
python -B work_c3_drift/verify_rational_mode.py
  -> {"status":"PASS","review_status":"unreviewed","a_transition_checks":2360,
      "landing_scan_range":[5,128],"landing_status":{"end":3966,"ceiling":2}, ...}
  -> failures: (5,-17,37), (5,-1,21)   [exit 0]

python -B work_c3_drift/verify_odd_denominator.py
  -> {"status":"PASS","review_status":"unreviewed","a_transition_checks":11164,
      "gateway_emission_checks":256,"size_checks":33, ...}   [exit 0]

python -B work_landing_symbolic/reviews/scratch/check_R_rat.py
  -> 32 numerators; single representative per (j,C): end=3966, ceiling=2, total=3968;
     full (C,b,j) states = 7936; each lift: end=3966, ceiling=2;
     single-lift b-bit histogram: b=1 -> 1987, b=0 -> 1981;
     a_step_checks=2360; skipped (j,C) = (5,-17),(5,-1),(5,7),(5,23);
     resonance counterexample verified (see RAT E0); L3(N0)=10000002, SIZE3 true.

python -B work_landing_symbolic/reviews/scratch/check_R_odd.py
  -> BBBAA repeated-shift violation at t=8; random a-step 2845/2845;
     permitted-height 42066/42066; X(4) odd a, time 2, k=1;
     gateway all ok; r=1e7: d=15849626, NQ=63398512, first_j_size=25849628;
     O1: d=1041805486527146, NQ=4167221946108592, m=1051689726214393, m<NQ, ratio=3.9624;
     monotonicity: doc criterion min j = 6; correct ratio min j = 7;
     reviewer's ratio is >1 already at j=2.

python -B work_landing_symbolic/reviews/scratch/check_R_o1.py
  -> fire matches P=49, k=469124961184426, pointer=sigma=1051689726214394;
     X(48) odd a, time 40, k=20; y=16A+10, A=263882790666247=7 mod 8, v2(y)=1;
     d=1041805486527146, NQ=4167221946108592, m_lb=1051689726214393, ratio=3.9624;
     sharp size threshold with B is d+10^7+O(1) ~ 1.0418054965e15, far below m.
```

另外：文档的验证脚本从 `verify_shift_transport` 导入 `Calendar`（后者经 `work_ext_roots/verify_low_deficit`
从 `search_roots` 再导出），不是 `work_global_calendar/calendar_oracle.py`。我用后者的
`Calendar(256)` 对照 `n=0..255` 的 `kind/time/epsilon/odd`，**mismatches 0**；在扫描范围内
两者一致，故不构成问题。

---

# A. `RATIONAL_MODE.md`

## RAT E0（L47，critical）：“C!=0 mod 3 排除 exact resonance”为假 — **confirmed**

原文 L46–48：

> All preserve C!=0 mod 3. Therefore 9k+C is never zero, irrespective
> of the canonical k. This excludes exact resonance. It does NOT by
> itself bound v2(9k+C) or exclude a non-descent.

前半句（`9k+C` 永不为 0）为真：`9k+C ≡ C mod 3 ≠ 0`。但 “exact resonance” 在已接受的
work_deep Lemma 2.2/2.3 中定义为 `z_t = 3k+θ_t = 0`（`work_deep/NOTES.md:115,130`），
不是 `9k+C=0`。两者不同。

**反例（精确重算，j=5 的规范奇 a 交叉）**：`X(4)` 是 odd a、`τ(4)=2`、`k=1`（canonical
`Calendar(64).crossing(4)`；本次实际输出 `odd=True, kind='a', time=2`）。取
`θ = D = -3`（symmetric，`|θ|<16`），`C = 3D mod 2^{6} = -9 mod 64 = 55`，`b=0`。
则
- `3 ∤ 55`（55 mod 3 = 1），满足原文表示的前提；
- `9k+C = 9+55 = 64 ≠ 0`；
- 但 `z = 3k+θ = 3-3 = 0`，即精确共振；
- 类恒等式 `3D ≡ C+3b·2^j (mod 2^{j+1})` 成立（`3(-3)=-9 ≡ 55 mod 64`）；
- 实际 a 步：`x=32, Θ=29, x'=2Θ+6-16=48, Θ'=38, D'=-10`，`j'=v2(48)=4`；
  RA 的 `1+v2(9k+C)=1+v2(64)=7` 不适用（`7>j-2=3`），这正是 one-step resonance。

一般地，在高参数 `k<2^{j-3}` 下 `9k<2^{j+1}`，取 `C=2^{j+1}-9k∈(0,2^{j+1})` 有
`C ≡ 2^{j+1} ≡ ±1 (mod 3)`，故 `3∤C`，且 `9k+C=2^{j+1}≠0`，而 `z=0`。所以
“C 非 3 的倍数 ⇒ 无 exact resonance” 是假的。
审阅者的同余形式 `9k+C ≡ -3b·2^j (mod 2^{j+1})` 也正确（b=0 时 `9k+C≡0 mod 2^{j+1}`；
b=1 时 `v2(9k+C)=j`）。

原文 §2 不依赖 L47（SIZE3 用 `|9k+C|<2^{j-2}` 另行排除共振：b=0 要求 `v2≥j+1`，b=1 要求
`v2=j`，均与 `<2^{j-2}` 矛盾），所以这是 §1 的一条假 [A] 陈述，不是 §2 的致命漏洞；但作为
[A] 陈述确为假，审阅者的判定成立。L48 的“不排除 non-descent”并不能挽救 L47。

## RAT E1（L38–44，L62–63，critical）：“持续 c 步 ε∈{3,5}”未声明 — **confirmed**

原文 L38–44 只列了 `a: C->9-C`、`b or cAA: C->C-3`、`c3: C->C`、`cBA: C->C+3`，
即只覆盖 `ε=3`（c3）、`ε=5`（AA/BA）和 b（Φ=1）；L62–63 的 HR5 只覆盖 `ε>=7`。若存在
`ε=4` 或 `6` 的 c 步，`C'=C+3Φ-6` 的 `Φ` 不在 `{1,2,3}`，`|C_t|<=C0+3t` 立刻失效，
SIZE3 与收缩都不成立。

已接受的 weight grammar 确实排除 ε=4,6：
- `work_global_root_phase/PROOF_ROOT_PHASE.md:22`：`epsilon(i)=W+1`；
- 同文件 L33–34：“W is always even and every type-c deficit is odd and at least 3”；
- `work_ext_roots/PROOF_LOW_DEFICIT.md:3,15–16`：`epsilon=3` forces A；`epsilon=5`
  permits exactly AA or BA（该文开头声明 weight identity 已接受，acceptance 记录在
  `reviews/global_astra11_review_record.md`）。

所以结论在已接受语料内是成立的，但原文没有引用这条已接受事实，作为自包含的 [A] 证明前提
不完整。审阅者的“critical（缺前提）”在“缺前提”意义上成立；更准确的严重度是 major
（结论可由已接受定理补全，不是数学错误）。

## RAT E2（L10–20，L58，major）：只覆盖分母 3，不覆盖一般 `s∈Z[1/3]` — **confirmed**

原文 L12 的表示是 `D = C/3 + b·2^j (mod 2^(j+1))`，`C` 整数、`3∤C`。这只覆盖分母整除 3
的相位（r≤1）：`1/9`、`eta_r=-5+8/3^r`（r≥2）都不能写成 `C/3`（C 整数）。全文没有出现
`r`、`sigma`、`eta`（`grep -n "eta\|sigma\|3^r\|denominator\|Q"` 只命中 L10/L17/L27/L80/L86/L137
等一般性词），L58 只从 `C0=10` 或 `26` 出发。标题的 “height” 是 `|C|/3`，与 O1 的实高度
`|eta_r|≤5` 不是同一个量。任务要求一般 `s∈Z[1/3]`、分母 `3^r`；本文没有覆盖，也没有
触及 O1 的 r–σ 耦合。审阅者的 scope 判断成立。

## RAT E3（L127–131，major）：着陆扫描范围/lift/计数 — **confirmed（有两处需更正）**

**实际重算**（`check_R_rat.py`）：
- 分子闭包（`C0=10,26`，5 层映射）共 **32** 个分子；
- 文档脚本对每个 `(j,C)` 只取 `d=C·3^{-1} mod 2^{j+1}` 一个代表，`j=5..128`，共 **3,968**
  个状态；`end=3966, ceiling=2`；
- 完整 `(C,b,j)` 状态数 = `32×124×2 = 7,936`，不是 3,968；两个 lift 各 `end=3966,
  ceiling=2`，失败仍是同一对 `(j,C)=(5,-17),(5,-1)`；
- 但**“只扫 b=0”这一句不对**：单代表 `d` 的 b 位分布是 `b=1: 1987, b=0: 1981`（因为
  `d` 可以 ≥`2^j`）。文档列出的失败 `(5,-17,37)` 的 `37>>5=1`（b=1），`(5,-1,21)` 的
  `21>>5=0`（b=0），并非统一 b=0。另一 lift 的失败是 `(5,-17,5)` 和 `(5,-1,53)`；
  `5 mod 64=5`、`53 mod 64=-11`，正是已接受窗口证书的裸 tie `(5,5),(5,-11)`。
  审阅者说“b=0 的 3,966/2 … b=1 同样是 …”在状态计数上对，但“lift 0 = b=0”的标签不对。
- 范围：§2 的 `j'<N0=2·10^7`；`L3(N0)=10,000,002`（精确重算，`κ(N0)=405,179,979,741/2`,
  `P(N0-1)=6753`），远大于 128；`L3(j)` 的下界对一切 `j≥N0` 都是 `1+floor(log2(3B))=
  10,000,002`，而上端可逼近 `N0-1`（例如 `log2 j≈19,999,948` 时 `L3≈20,000,000`，
  `log2 j≈19,999,945` 时 `L3≈19,999,997`）。所以 128 远不足以覆盖真实着陆参数。
  文档的“3,968 classes”应理解为“3,968 个代表状态”，不是全部 `(C,b,j)` 类；审阅者的
  7,936 计数成立。文档自己说 landing certification is separate，所以这不是“错误的定理”，
  而是计数/范围表述问题；审阅者的 major 判定在“数据不足以构成着陆认证”上成立。

## RAT E4（L117–118，L143–148，major）：全文没有 J 依赖 — **confirmed**

`grep -n "J\|T_h\|log\*\|K_clock" work_c3_drift/RATIONAL_MODE.md` 返回空：全文没有出现
`J`、`T_h`、`log*`、`K_clock`。`h3(q)` 只是对起点参数 `q` 的迭代对数；没有说明 `q` 与
祖先 `J` 的关系，也没有 `h3(q)≤log* J`、`N0/B/T_h` 各自如何进入。`N0` 与 `B` 实际是通过
`L3` 的常数和 SIZE3 的 `B≤2^{j-6}` 进入；`T_h` 未使用。任务要求“说明每一部分对 J 的依赖”，
本文没有做到。审阅者的修正方向正确（把 `q` 的起点、`h3(q)≤log* q`、`J<K_clock ⇒ h3≤4`
写明）；其修正中“q=m 与祖先 J 无关”一语略强：`q` 是本段起点参数，满足 `q≤J`，所以
`h3(q)≤h3(J)`，这也是 `h3(J)≤4` 论证的来源；说“与 J 无关”不如说“只通过 q≤J 依赖 J”。

## RAT E5（L4–6，L122–125，major）：开头“continue a gateway”与内容不匹配 — **confirmed（措辞级）**

原文 L4–6：“This addresses how to continue a gateway whose output parameter is above the
existing finite certificate cutoff.” §2 只给出高参数段的收缩（`j'≤j-2`、记录下降），L118
明说 “Landing certification is still separate”，§3 的数据只到 `j=128`。所以本文没有
“关闭 gateway”，只把网关的高参数段化为一个着陆参数 `<N0` 的显式类。审阅者建议改成
“reduce the high-parameter part …, leaving the landing certificate open”是准确的。
需要指出：文档开头已自标 “UNREVIEWED conditional lemma, not a global certificate”，
L118 也明确保留着陆；因此这不是隐藏的过度声明，而是标题/摘要的 scope 措辞问题，严重度
可降为 minor/major 之间。

## RAT E6（L77–84，minor）：`|3k+C/3|≤κ+B` 静默使用高度界与 CLOCK — **confirmed**

L78 的 `|3k+C/3| ≤ κ(j)+B` 需要两件事：
1. `|C|/3 ≤ B`：由 L60 的 `(C0+3h3(q))/3≤B` 与 L72 的 `|C_t|≤C0+3t`（`t≤h3(q)`）得到；
2. `3k ≤ κ(j)`：由已接受 CLOCK `3k=3τ/2 ≤ 3(j-1)P(j-1)/2=κ(j)` 得到。
原文 L78 没有在同一句引用这两条，读者可能误以为它是深段条件的直接推论。审阅者的补充
推导正确。

## RAT E7（L97，minor）：`L3 is nondecreasing` 未证明 — **confirmed（陈述为真，缺一行证明）**

`L3(j)=max(1+floor(log2(3(κ(j)+B))), floor(log2(6(j-1)P_clock(j-1)+5)))`；
`κ(j)=(3/2)(j-1)P(j-1)`，`P(n)=2⌈log2(6n²+5)⌉²+1345` 非降（`6n²+5` 增，ceil log 非降），
故 `(j-1)P(j-1)` 与 `6(j-1)P(j-1)+5` 均非降，两个 max 项非降，`L3` 非降。我抽查
`P(N0-1..N0+19998)` 全部非降（`P_nondecreasing_sample=True`）。原文只断言未证；作为
[A] 命题应补这一行。审阅者的判定成立。

## RAT E8（L90，minor）：“SIZE3 … no extra hypothesis”易误读 — **confirmed**

SIZE3 本身确实无条件：`κ(j)<2^{j-4}`（work_deep Lemma 2.1）、`B≤2^{j-6}`（`j≥N0`），
故 `3(κ+B)<15·2^{j-6}<16·2^{j-6}=2^{j-2}`。我的精确整数核对：`3(κ(N0)+B)` 的
`floor(log2)` 为 10,000,001 < `N0-2=19,999,998`。但把它用于 `j'≤j-2`、RA 适用时，
需要 `|9k+C|≤3(κ+B)`，即需要 `|C|/3≤B` 的高度界（L60）；原文的强调句“no extra
hypothesis is needed”容易被读成整个 §2 无条件。审阅者的修正（把 SIZE3 本身与它的应用
分开）正确。

## RAT E9（L38，L52，L143，全文，minor）：措辞/标签 — **confirmed**

- L38 “the proposed low-deficit identities”过时：`CHECKPOINT_1RB1LA_0RC0RD.md` 的
  work_c3_drift 节明确 “Accepted: work_c3_drift/NOTES.md §1–4, C5_EXTENSION.md, …”；
  应改为 “accepted (C5_EXTENSION §1)”。
- L52 “the accepted split estimate”应为 “size estimate”：work_deep 的引理名是
  Lemma 2.1 (size)（`work_deep/NOTES.md:88`），不是 “split”。
- L143 “testing both incoming precision bits”对 a 步的 2,360 次比较成立（脚本对每个
  `(j,c)` 检查 `lift∈{0,1}`），但着陆扫描只取一个代表；应把两者分开表述。
- 全文没有 [A]/[B]/[C] 标签（grep 无命中）；按本轮约定应给每条实质结论加标签。
审阅者的四条均成立。

---

# B. `ODD_DENOMINATOR.md`

## ODD E0（L28–31，major）：`permitted` 未定义；ε≥7 的 c 步破坏高度递推 — **confirmed**

`grep -n "permitted"` 只在 L27 命中一次，全文没有定义。“after t permitted steps
`|C_t|/Q≤A+t`”只在每步 `|Φ−2|≤1` 时成立：a 步是反射（不增），b 与 c3/AA/BA 分别给
`−1,0,−1,+1`。对 ε=11 的 BBBAA，来源移位是 `+4/3`（`CHECKPOINT…` work_c3_drift 节：
“ε=11 (BBBAA) … shift +4/3”），一步就把 `X=|C/Q−3/2|` 增加 4/3，`A+t` 的归纳步骤失效。

我的重算：取 `Q=3, C_0=1`（`c_0=1/3`，`A=8/3`），连续 BBBAA：
`c_t=1/3+(4/3)t`；`|c_t|>A+t` 首次在 `t=8`（`c=11 > A+8=32/3`）。若从极值 `|c_0|=A`
出发，一步就违反。对 `Φ∈{1,2,3}` 的许可步，我的 42,066/42,066 步全部满足 `A+t`
（`height_recurrence_permitted`），与“只有 |Φ−2|≤1 才行”一致。审阅者的修正定义
`permitted={a,b,Φ∈{1,2,3} 的 c}` 正确。

## ODD E1（L61–68，major）：主引理假设清单不完整 — **confirmed（其中 (i) 已在 §1 披露且自动成立）**

逐项：
1. **固定 Q/无参数五 gateway**：原文 L32–33 已写 “These statements concern a fixed
   denominator between gateways.”；且 gateway 在参数五（j=5），而主引理的前缀 `j≥N_Q≥N0≫5`，
   j 严格下降（a: `j'≤j-2`；b/c: `j'≤j-2-ε`），所以在高参数前缀内不可能遇到参数五。
   这一条不是隐藏的缺失，主引理只是没有复述 §1 的 scope。审阅者把它列为“未写”略强。
2. **续走 c 步只有 ε∈{3,5}**：确实缺；需引用已接受的 PROOF_ROOT_PHASE §1 与
   PROOF_LOW_DEFICIT §1（见 RAT E1 的引用）。审阅者成立。
3. **F 定义到所读 τ(n)**：原文没有出现 `F`/defined prefix；这是 PROOF_EXT §2 的 standing
   hypothesis（`work_global_ext/PROOF_EXT.md:15,28,83`），主引理没有写。成立。
4. **进入记录 R_0≤J**：原文 L65 只说 “All those transitions strictly lower the record”，
   没有 `J`、`R_0` 或 `R_0≤J`；若用于 S(J) 这条是必需的。成立。
5. **A 是来源属性而非相位类 (j,θ) 的函数**：`A=max(|C_0/Q|,|3-C_0/Q|)` 取决于所选有理
   代表元 `C_0/Q`；给定 `(j,θ)`（对称整数余数）不能唯一确定 `C_0/Q` 的绝对高度。成立。
审阅者五条中四条（2–5）是真实缺口；第 1 条已由 §1 披露且在高参数前缀自动成立，应在
修正中说明，而不是当作缺失。

## ODD E2（L61–62，L99–102，major）：只降到 N_Q，`[N0,N_Q)` 带未覆盖 — **confirmed**

`N_Q=max(N0,4(d+2))`，`d=ceil(log2 Q)`。`Q>2^{N0/4-2}` 时 `N_Q>N0`。精确重算（r=10^7，
Q=3^{10^7}）：
- `d=15,849,626`，`N_Q=63,398,512`；
- `Q(κ+B)<2^{j-2}` 实际首次成立在 `j=25,849,628`（用 90 位 `log2 3` 精确核对；
  `log2(Q(κ+B))+2=25,849,627.0072...`）；
- 因此 `[20,000,000, 25,849,628)`（宽 5,849,628）是连精确 size 不等式都不成立的带；
  文档的 `N_Q` 阈值更大，实际留下的带是 `[20,000,000, 63,398,512)`。
窗口证书只覆盖 `j<2·10^7`（且是整数 δ；有理着陆类根本不在其中），所以这段确实没有
本文论证。文档的 §2 结论本来就是“降到 N_Q”，不是 N0；审阅者要求把 `[N0,N_Q)` 明确为
open 带，并收窄 §4 的 “every odd-denominator mode”，是准确的。注意：文档的结论没有
声称降到 N0，所以这是 scope gap/措辞，不是结论错误。

## ODD E3（L61–68，L99–102，major）：没有 J 依赖分析 — **confirmed（但“记录预算不出现”不准确）**

`grep -n "J" work_c3_drift/ODD_DENOMINATOR.md` 无命中；没有 `log*`、`T_h`、`K_clock`、
`窗口`；`h_Q(q)` 只是抽象定义，没有与 q（≤J）的关系，也没有 tower。RATIONAL_MODE 的
`U_1=2^{(N0-5)/2}, U_{r+1}=2^{(U_r-5)/2}` 在本文没有对应物；没有 `N_Q≤J` 与
`h_Q(q)≤J-R_0` 的检查。审阅者要求补平行 tower 与两条预算不等式，或明确写“本引理只给
逐段结论”，是准确的。

更正：原文 L107 确实写了 “the record budget must survive repeated gateways”，所以
“全文不出现记录预算”过强；出现的是定性说法，缺的是定量的 `R_0≤J`/`h_Q≤J-R_0`。

## ODD E4（L37–48，L50，major）：用 B 而非实际高度，O1 上为空 — **confirmed（结论成立，但审阅者的机制错误）**

我独立重算 O1：
- 规范源 P=49，`k_fire=469124961184426`，`Calendar(512).preceding_fire_by_time(2k)` 返回
  `pointer=1,051,689,726,214,394=σ`，与 O1 文一致；
- `X(48)` 是 odd a、time 40、k=20；`x0=5·2^49`，`y=2Θ0+120-x0/2=4,222,124,650,659,962=
  16A+10`，`A=263,882,790,666,247≡7 mod 8`，`v2(y)=1`；
- `r=657,306,078,883,964`，`d=ceil(r log2 3)=1,041,805,486,527,146`，
  `N_Q=4(d+2)=4,167,221,946,108,592`；
- `m≥σ-1=1,051,689,726,214,393`，`m<N_Q`，比值 `3.9624`；源参数 j=49 也远小于 N_Q。
  所以 §2 的引理在 O1 的源与输出上都不适用。审阅者的这一结论成立。

**但“B 把 N_Q 放大约 N0/2 位”是错的。** `N_Q=max(N0,4(d+2))` 完全不含 B；它来自
`d+2≤j/4` 的粗放指数拆分，是 B 无关的。若用精确 size 不等式（即使仍用 B），
`log2(Q(κ+B))≈d+10^7+1`，其阈值 `≈1.0418054965e15`，远低于
`m=1.0516897262e15`（差 `m-d≈9.884e12` 位）。用实际 h≤5 时阈值约 `d+65`，同样远低于 m。
所以让引理在 O1 上为空的不是 B vs h，而是 `4(d+2)` 这个过粗的充分阈值；即使保留 B，改用
`log2 Q+log2(κ+B)+2` 也能覆盖 m。审阅者的修正“按一般高度 h 陈述”方向可用，但仅替换
B→h 而不改 `4(d+2)` 阈值仍不能解决 O1；应把这条机制更正为“粗阈值”。

## ODD E5（L41–44，minor）：单调性理由的比值/常数 — **refuted**

原文 L41–44：
> `kappa(j)<=(3/2)*(j-1)^2<2^(j/2)` for `j>=N0`. For the last inequality, the squared
> polynomial comparison holds at N0 and persists because `2*j^4/(j+1)^4>1 for j>=6`.

令 `f(j)=2^{j/2}/((3/2)(j-1)^2)`。则
`f(j+1)/f(j)=√2·((j-1)/j)^2`；`>1 ⇔ 2(j-1)^4>j^4 ⇔ j≥7`。原文的
`2j^4/(j+1)^4>1` 是同一条件把 `j` 换成 `j+1`（即步骤 `j+1→j+2`）：
`j=6` 时 `2·6^4/7^4=1.0795>1`，`j=5` 时 `2·5^4/6^4=0.9645<1`。因为 `N0≫7`，
base case 在 N0 成立、之后所有步骤的比值都 >1，故持久性成立。`3/2` 常数在比值中消掉，
只在 base case 进入，已经被处理。原文的论证（虽然索引写得粗）是有效的。

审阅者写的“正确的逐步比值是 `√2·(j/(j-1))^2>1 ⇔ j≥7`”本身是错的：
`√2·(j/(j-1))^2>1` 对一切 `j≥2` 都成立（j=2: 5.657；j=5: 2.210；j=6: 2.036），
并不给出 j≥7。审阅者的“3/2 常数未在理由中处理”也不对：常数在比值中抵消。
结论（`(3/2)(j-1)^2<2^{j/2}` 持久）是对的，但原文并没有这里所称的错误。**refuted。**

## ODD E6（L72–75，minor）：`3D'=15-D-y` 只对 k=1 — **confirmed（minor；b/c 替代情形不可能）**

一般 a 步：`3D'=9+6k-D-y`（`y=x'`）。我的精确检查对 k=1,2,3,20 都验证了
`3(t-y)=9+6k-D-y`；k=1 时正是 `15-D-y`。`X(4)` 由 canonical calendar 固定为
`odd=True, kind='a', time=2`，所以参数五的链必然走 `k=1` 的 a 步；原文
“At parameter five” 已经隐含这一点，但没有明说。审阅者建议写明
“X(4) 为奇 a 型、τ(4)=2、k=1”是合理的；其“若参数五的链会走 b/c，公式不成立”
的反事实不可能发生（X(4) 是固定日历数据，不会走 b/c）。所以这是缺一句显式前提的
minor 问题，不是潜在错误。

## ODD E7（L89–95，minor）：`c` 未定义；复合/边界 — **confirmed（minor）**

- `c` 只在 L91 `c -> (c-6)/3` 首次出现，全文没有定义（应为 `c=C/Q`）。
- 复合确实是两步：gateway `c->5-c/3`，再反射 `c->3-c`，合起来
  `3-(5-c/3)=c/3-2=(c-6)/3`；我的 Fraction 检查：`c0=5 -> 10/3 -> -1/3`，与
  `(5-6)/3=-1/3` 一致。不是单步 “a descent”。
- `c_0=5` 对应 `Q=1`：若 `c=5` 且 `Q>1, gcd(C,Q)=1`，则 `C=5Q`，`gcd(C,Q)=Q>1`，
  矛盾；所以唯一表示是 `Q=1`，确实在 §1 的 `Q>1` 之外。文档把它作为一致性检查使用，
  但没说边界。
- “For `Q=3^r` and `gcd(C,Q)=1`, it always triples”在 r=0 不普遍：`Q=1,C=3` 给
  `(15-3)/3=4`（分母 1），`Q=1,C=15` 给 0（分母 1）；`C=5` 给 10/3（分母 3，恰好翻三倍）。
  r≥1 时确实翻三倍（`Q=3,C=5 -> 9`；`Q=9,C=5 -> 27`）。文档 §1 假定 Q>1，所以 r≥1
  的陈述在其域内成立；`c_0=5` 的例子在域外。审阅者的 minor 判断成立。

## ODD E8（L104–106，minor）：“Even while N_Q=N0, infinitely many distinct rational residues”为假 — **confirmed**

若 `N_Q=N0`，则 `4(d+2)≤N0`，即 `d≤N0/4-2=4,999,998`，故 `Q<2^d≤2^{4,999,998}`。
又 §2 的高度假设 `|C/Q|≤B=2^{10^7}`，故 `|C|≤BQ<2^{10^7+4,999,998}=2^{14,999,998}`。
既约分数 `C/Q` 只有有限多个（Q 有限、每个 Q 的 C 有限）。所以按字面这句话是假的。
审阅者的修正（“Q 本身无界，故来源/分母空间无限”，或“对无界的 j，类 mod 2^j 有无穷多”）
正确。注意：若 Q 无界，`N_Q>N0`，则不再是 “while N_Q=N0”；原句把两种情况混在一起。

## ODD E9（L104–105，minor）：有限着陆证书不够的理由与 N_Q — **refuted（审阅者的“真原因”不成立）**

原文：“a fixed finite landing certificate is still insufficient: N_Q increases with
log2 Q.” 这个理由是**有效**的：§2 的着陆参数是 `j'<N_Q`，Q 增大时 N_Q 增大，固定的
有限 j-范围证书（例如已接受的 `j<2·10^7` 窗口）不能覆盖 `[2·10^7,N_Q)`。所以
“N_Q 增长不是着陆证书不足的原因”是错的；它是**一个**真实原因。原文紧接着还写了
“Bare ties require actual precision provenance, and the record budget must survive
repeated gateways”，即出处/记录预算这一独立原因已经列出，不存在审阅者所说的“混淆”。

审阅者的“真原因是把 δ 移出固定窗口 [−12,15]（如 +4/3 的 BBBAA）”也不准确：
`4/3=1.333` **在** `[-12,15]` 之内（我的检查 `E9_shift_4_3_inside_window=True`）；
真正的问题是 `4/3` 不是整数，而已接受窗口证书枚举的是整数 δ，并且有理类的提升位/出处
不由类单独决定。`+4/3` 的例子支持“非整数/出处”问题，不支持“移出窗口的数值范围”。
另外，累计 12 步 BBBAA 才到 16>15；单步 4/3 并没有移出窗口。因此该条作为“错误”不成立；
审阅者的出处（O3）观察可以保留，但不能用 +4/3 作为“移出窗口”的证据。**refuted。**

---

# C. 额外发现（审阅者漏掉或需要更正的）

1. **RAT E3 的 b=0 标签错误（更正审阅者，不是原文新增错误）**：单代表 `d` 的 b 位分布是
   `b=1:1987, b=0:1981`；文档的两个失败是 `(5,-17,37)`（b=1）与 `(5,-1,21)`（b=0）。
   不能说“文档只扫 b=0”。审阅者的 7,936/3,968 计数结论仍成立。

2. **ODD E4 的 O1 机制错误（更正审阅者）**：`N_Q=4(d+2)` 与 B 无关；即使保留
   B=2^{10^7}，精确 size 阈值 `d+10^7+O(1)≈1.0418054965e15` 也远低于
   `m≈1.0516897262e15`。让引理在 O1 上为空的是过粗的 `4(d+2)` 阈值，不是 B vs h。
   审阅者的结论（引理在 O1 上为空）成立，但修正建议“换成 h”本身不够。

3. **ODD E3 的“记录预算不出现”不准确**：L107 有 “the record budget must survive
   repeated gateways”；缺的是定量 `R_0≤J`/`h_Q≤J-R_0`，不是完全没有提到。

4. **RATIONAL_MODE L136–137 的引用归属**：`C=-1` 是已接受的 3-adic 轨道值 `c_1=-1/3`
   （O1 §2 明确 “The accepted rational orbit is c_r=-3+8/3^r”；PROOF_EXT Theorem O 也列出
   10/3, −1/3, 46/9, …）。但具体的“无限分母障碍”（P=49、`eta_r=-5+8/3^r`、
   `r≥657306078883964` 的首个输出严格安全失败）来自 `ORBIT_SHIFT_OBSTRUCTION.md`
   （未审），不是 Theorem O 的直接陈述。L137 “The infinite-denominator obstruction of
   that theorem still applies”把两者混在一起；应分别引用并注明 ORBIT_SHIFT 的未审状态。
   这是引用/归属问题，不是数学错误。

5. **RATIONAL_MODE L67 的 “even endpoint” 未定义**：全文只出现这一次；应说明是
   “even crossing（X(n) even）的终止”。

6. **ODD L61 的 `L_Q(j)<j` 未证**：它由与 §2 相同的 `d+2≤j/4` 与 `2log2j+3<j` 得到，
   原文只断言；作为 [A] 命题应补一行（与 RAT E7 同类）。

7. **ODD L32–33 的 “bare tie” 与 “gateway” 用词**：真正改变分母的是参数五的 gateway；
   `(5,5)` 是 gateway 的特例，但审阅者的结论表第 8 行提到另有一些裸类（该表列了
   `j=8/12/14/17`）不是 gateway——这些具体 j 我未独立复核，但 `(5,5)` 之外存在非
   gateway 裸类这一点与该表一致。原文 “across a bare tie” 与 “between gateways” 的
   混用会让读者误以为所有裸 tie 都改分母；建议一并修正。

8. **ODD 全文没有 [A]/[B]/[C] 标签**（审阅者 E11，未列入任务 E0–E9）：§2 的主引理只有
   “Induct … as in RATIONAL_MODE”；按本轮约定应给每条结论加标签，或明确标 [A-cond]。

9. **RATIONAL_MODE L117 的 “reached-prefix inputs” 不精确**：应写明实际 S(J) 到达参数 q、
   类 `(10-2^q)/3` 或 `(26-2^q)/3`、入口记录 <J（来自 r1r2 网关引理），否则“剩余假设”
   无法核对。

10. **验证脚本的 Calendar 来源**：文档脚本用 `work_ext_roots/verify_low_deficit.Calendar`，
    不是任务指定的 `work_global_calendar/calendar_oracle.Calendar`。我在 `n=0..255` 对照
    `kind/time/epsilon/odd` 全部一致（mismatches 0），所以在本轮扫描范围内不构成问题；
    但若以后把扫描推到更大 j，应显式使用规范 oracle 并重跑。

---

# D. 结论表（顺序与输入错误一致）

| 文档 | 输入编号 | 行号 | 判定 | 一句话 |
|---|---|---|---|---|
| RATIONAL_MODE | E0 | L47 | confirmed | C≢0 mod3 只排除 9k+C=0；反例 j=5,C=55,k=1 有 z=0 |
| RATIONAL_MODE | E1 | L38–44,L62–63 | confirmed | ε∈{3,5} 前提未引已接受 grammar（结论可由它补全） |
| RATIONAL_MODE | E2 | L10–20,L58 | confirmed | 只覆盖分母 3；无 r/σ/eta，无 O1 |
| RATIONAL_MODE | E3 | L127–131 | confirmed | 7,936 类非 3,968；j≤128 远不足；但“只扫 b=0”不准确 |
| RATIONAL_MODE | E4 | L117–118,L143–148 | confirmed | 全文无 J/T_h/log*；无 q–J 关系 |
| RATIONAL_MODE | E5 | L4–6,L122–125 | confirmed | 只给高参数收缩；着陆开放（doc 已披露，措辞级） |
| RATIONAL_MODE | E6 | L77–84 | confirmed | |3k+C/3|≤κ+B 静默用了高度界与 CLOCK |
| RATIONAL_MODE | E7 | L97 | confirmed | L3 非降为真但未证 |
| RATIONAL_MODE | E8 | L90 | confirmed | SIZE3 无条件，应用需高度界 |
| RATIONAL_MODE | E9 | L38,L52,L143,全文 | confirmed | proposed/split/lift 措辞；无 [A]/[B]/[C] |
| ODD_DENOMINATOR | E0 | L28–31 | confirmed | permitted 未定义；BBBAA +4/3 破坏 A+t |
| ODD_DENOMINATOR | E1 | L61–68 | confirmed | 假设清单缺 (ii)–(v)；(i) 已在 §1 且自动 |
| ODD_DENOMINATOR | E2 | L61–62,L99–102 | confirmed | N_Q=63,398,512；精确带 [2e7,25,849,628) |
| ODD_DENOMINATOR | E3 | L61–68,L99–102 | confirmed | 无 J/log*/T_h/tower；记录预算仅定性出现 |
| ODD_DENOMINATOR | E4 | L37–48,L50 | confirmed | O1 上为空；但“B 放大 N_Q”机制错误 |
| ODD_DENOMINATOR | E5 | L41–44 | **refuted** | 原文比值/常数正确；审阅者的 √2(j/(j−1))² 判据错误 |
| ODD_DENOMINATOR | E6 | L72–75 | confirmed | k=1 前提未写；X(4) 固定奇 a，b/c 情形不可能 |
| ODD_DENOMINATOR | E7 | L89–95 | confirmed | c 未定义；两步复合；c_0=5 是 Q=1；r=0 不普遍翻三倍 |
| ODD_DENOMINATOR | E8 | L104–106 | confirmed | N_Q=N0 时分数只有有限多 |
| ODD_DENOMINATOR | E9 | L104–105 | **refuted** | N_Q 增长是有效 j-范围原因；+4/3 在 [−12,15] 内 |

**复核者独立重算的脚本与 json**：
- `work_landing_symbolic/reviews/scratch/check_R_rat.py` / `check_R_rat.json`
- `work_landing_symbolic/reviews/scratch/check_R_odd.py` / `check_R_odd.json`
- `work_landing_symbolic/reviews/scratch/check_R_o1.py` / `check_R_o1.json`

**未做的事**：没有验证 §2 的 `j≥N0=2·10^7` 解析收缩（`Calendar` 只到 B≤1024，无法机器
验证该范围）；没有重跑 `verify_r1r2_big.py` 的 2·10^7 网关证书（只引用了已接受 checkpoint
的 [B] 陈述）；没有证明 O1/O2/O3 或全局 EXT。本报告只判定审阅者所列错误与原文对应行。
