# 复核报告（复核者-T）：SHIFT_TRANSPORT.md 与 FIRST_A_REDUCTION.md

日期：2026-10-23。复核对象：
`work_c3_drift/SHIFT_TRANSPORT.md`（140 行）与 `work_c3_drift/FIRST_A_REDUCTION.md`（168 行）。
被复核的审阅报告：`work_landing_symbolic/reviews/shift_transport.md`、`work_landing_symbolic/reviews/first_a.md`。
本报告不修改任何原文档，不改变 K_clock，不声称全局 EXT。所有临时脚本/JSON 只写在
`work_landing_symbolic/reviews/scratch/`。

**复核方式。** 不采信审阅报告中的数字；每一条都先打开原文对应行，再独立重推代数或重跑精确计算。
审查重点是：整数/有理 eta 与 source shift 的定义差别、HP 的真实前提（`x*≠0`、`j_0` 相等、
reference calls defined）、精度位/modulus 的使用、有限范围与 all-j 的混淆、以及把归约写成认证。
此外我检查了审阅者没有列出的地方（见 §4）。

**运行过的命令（全部在本会话中执行）：**

```
python -B work_landing_symbolic/reviews/scratch/checkT_transport.py        # 独立重算 SHIFT_TRANSPORT §5
python -B work_landing_symbolic/reviews/scratch/checkT_first_a.py          # 独立重算 FIRST_A §5–§6
python -B work_landing_symbolic/reviews/scratch/checkT_first_a_aux.py      # 336 源/常量/质量分解
python -B work_landing_symbolic/reviews/scratch/checkT_shift_algebra.py    # eta vs s、记录恒等式的精确代数
python -B work_landing_symbolic/reviews/scratch/checkT_extra.py            # source-shift 类、深层 λ 反例
python -B work_landing_symbolic/reviews/scratch/checkT_verify_shift_transport_copy.py
python -B work_landing_symbolic/reviews/scratch/checkT_verify_first_a_copy.py
```

后两条是把文档自带的两个 verifier 原样复制到 scratch 后运行（原版会把 json 写回
`work_c3_drift/`，任务禁止修改该目录）。复制版只改了两处路径：`ROOT=parents[3]`，
以及 `verify_first_a` 改为从 scratch 的复制文件 import `verify_shift_transport`。
两条均输出 `status=PASS`，数字与文档一致（见下）。

**结论一览。** 两篇文档的核心代数（SHIFT_TRANSPORT §2–§4 的精度归约、FIRST_A §1–§3 的
首次 a-步恒等式）经独立重算成立；审阅者列出的多数问题确实存在，但其中若干条是“文档没有做
它自己明确声明不做的事”，不能算作文档错误。审阅报告自身也有两处数字错误/不一致（§4.3、§4.4）。

---

## 1. SHIFT_TRANSPORT.md

### 1.1 独立重算的事实基线

`checkT_verify_shift_transport_copy.py`（复制版，PASS）与 `checkT_transport.py` 一致给出：

- `canonical_pairs`：4 对，全部 `p=5`、`precision=4`、ancestor_index=5；
  `P=14/87/158/231`，源下标 `6133 / 289086270696314883188925376 /
  136517131539405869694540270279944446662008190014 /
  6446839263191968112703081097646156153307841449936119739796858726807903`。
- `reference_status={end:260}`，`reference_tail_lengths={"1":260}`，`matched_states=260`。
- `synthetic_lift_reference_status={end:4940, ceiling:4}`；end 参考的长度分布为
  `{"1":4550,"2":375,"3":15}`（4 个 ceiling 也各贡献 1 个长度 1，故全状态分布是
  `{"1":4554,"2":375,"3":15}`，总和 4,944）；`synthetic_lift_matched_states=5345`
  （=4550+2·375+3·15）；非平凡（长度>1）参考 390 个。
- 4 个 forced controls：p=64,100,135,208；独立重算 `next_x=2^(p-1)` 全部成立，
  `eta` 位长 62/98/133/206。
- 祖先是 fire-shaped：4 对的 `(xc,tc)=(10,11)`，而 b-entry 应为 `(10,10)`
  （`fire_x=10`，`tau_p=tau_pm1=2`，`is_fire_shaped=true`，`is_b_entry_shaped=false`）。

`checkT_shift_algebra.py`（精确整数/有理数，P=14，n=6133，σ_D=6128）对 θ_T∈{0,1,2,5,−3} 验证：

- `v2(c_D)=6128=σ_D`；
- `v2(x_u−x_D)=6128`，`v2(Θ_u−(Θ_D+eta))=6134=j`；
- 与祖先 C=(10,11) 的一致：`v2(x_u−x_C)=4=σ_C`，`v2(Θ_u−(Θ_C+eta))=5≥σ_C`；
- `Θ_u−x_u ≡ θ_T + s (mod 2^{σ_D})`，其中 `s=−1−λ_Y`（本例 s=−4113，λ_Y=4112，
  即 AA 类 `s≡−1 mod 2^{ω+1}`，ω=1）；`eta=θ_T−2`。
- 记录恒等式：`Γ_u=1+ε_D=6`，`Γ_u+σ_D=6+6128=6134=R_T=j+Γ_T`（Γ_T=0）。

### 1.2 逐条复核

| 项 | 行号 | 审阅者主张 | 判定 | 复核证据 |
|---|---|---|---|---|
| E0 | L21–L30, L57, L86 | 只对整数 eta 证明；eta=θ_T−2 是 outer defect shift，不是 source shift s=θ_D−2；Z[1/3]/O1 不在范围；无 r–σ_C 关联 | **confirmed**（作为范围缺口） | 原文 L28 明写 “for EVERY integer eta”；L60–68 定义 `theta≡Θ_T−x_T (mod 2^j)`，`eta=theta−2`，故 eta 是外层缺陷减 2。已接受的 source shift 是 `s(n):=−1−λ_Y(n) mod 2^{ω+1}`（`work_c3_drift/CONGRUENCE_TARGET_NOTE.md:253`），等价于 c 步缺陷增量；我从 calendar 复算：76 个 A(ε=3) 源 `s≡0`，4 个 BA `s≡1`，4 个 AA `s≡3≡−1`（`checkT_extra.json`）。精确代数给出 `Θ_u−x_u≡θ_T+s (mod 2^{σ_D})` 而运输参数是 `eta=θ_T−2`，二者是不同的量（只有 θ_T=2+s 时相等）。原文没有出现 r、3^r、denominator、height 或 O1 的任何记号（grep 无命中），也没有把 r 与 σ_C 关联或排除危险剩余类。补充：该证明是纯 2-adic 的，对分母为奇数的有理 eta 逐字成立（O1 §1 也这样断言），所以“整数限定”本身是保守的表述；真正的缺口是 source-shift 分类与 O1 的 r–σ_C 关联。 |
| E1 | L95–L109, L139–L140 | “removed” 只是归约；terminal families 仍无界；无 landing 证书/gateway/记录下降；O2/O3 未处理 | **refuted（作为“文档错误/过度声称”）** | 这些事实本身都对（real fire 与 b/c-initial c 源确实仍无界；first A-output 确实只归约到 C3 reference；O2 的 affine/beta 与 O3 的编码确实未处理），但原文 L106–109 自己就写：“The remaining shifted fire and b/c-initial families are still unbounded. This is a uniform reduction, not a proof of those residual families.” L103–104 也写 “it does not certify every eta automatically.” L3–4 声明 “No new horizon and no global EXT conclusion”。因此审阅者要求把 “removed” 改写成 “reduced to Safe(E,eta)” 的修正，其内容原文已经具备；不构成文档的过度声称。真正成立的是：本文没有完成本轮的 landing 目标——但这是范围陈述，不是错误。 |
| E2 | L14–L16, L32–L38 | Safe 未要求每步 x≠0；HP 需要 reference walk 的 x*≠0 | **confirmed（major）** | `work_global_ext/PROOF_EXT.md:68` 的 Lemma HP 明确要求 “equal j_0” 与 “x*_i ≠ 0”，并在 L73 注明 “The hypothesis x* ≠ 0 is needed: a virtual ‘resonance’ x* = 0 exists”。原文 Safe 只要求 terminates 与 `j+loss<σ_C`，没有排除 x=0；`verify_shift_transport.py:12-13` 也把 `x==0` 单列为 `zero`。我实际复现了共鸣：`bounded_walk(32, 5, precision=10)` 返回 `('zero', [(j=5,loss=0)])`（`checkT_first_a.json` 的 `resonance_x32_theta5_P10`）。若 reference 在中间到 0，j 无定义、HP 不适用；因此 Safe 必须显式加 “x_i≠0”。（原文没有说明 termination 指 even return 而非 x=0。） |
| E3 | L32–L38, L59–L74 | HP 需两条 walk 初始 j_0 相等；未写 j_C<σ_C ⇒ j_D=j_C；theta 只按 mod 2^j 选代表，未说明 Safe 对 eta→eta+2^j 的不变性 | **confirmed（minor）** | HP（`PROOF_EXT.md:68`）要求 equal j_0。由 Safe 的首项 `j_C+0<σ_C` 与假设 `v2(x_D−x_C)≥σ_C` 得 `v2(x_D)=j_C`，即 `j_D=j_C`，但原文没有写出。theta 只在 L61–62 按 `mod 2^j` 选取；`j=n+1>σ_D>σ_C`，所以 `eta` 与 `eta+2^j` 的两个参考 walk 初相差 `2^j`、valuation `j>σ_C`，由 HP（P=σ_C）可知 Safe 不变——但原文没有这一步，也没有固定 exact defect 代表元。两点都是可补的（依赖 E2 的 x≠0）。 |
| E4 | L23–L30, L59–L74 | “reference calls are defined” 在 §3 应用时未验证；需 σ_C<σ_D<j_T≤J | **confirmed（minor）** | §2 L27 把它列为假设，§3 没有再验证。实际成立：A-SOURCE 的 `sigma_D-σ_C=rho-p-1>0`（`PROOF_A_SOURCE_DESCENT.md:113`），`σ_D=n−ε_D≤n=j−1<j`；对 S(J) 中的链，记录 `R_T=j+Γ_T≤J`（原文 L81/L85 也用到 `R_T=J` 的可能），所以 `j_t<σ_C<σ_D<j≤J`，reference 调用 `X(j_t−1)` 落在 `X(0..J−1)` 内。事实成立，但原文没有写出这条链。 |
| E5 | L70–L71, L80–L82 | ε_D 未定义；`v2(c_D)=σ_D=n−ε_D` 是 Lemma K(c)；记录恒等式依赖 ε_D=n−σ_D | **confirmed（minor）** | ε_D 在全文只出现在 L70，未定义；恒等式是 `PROOF_EXT.md:57,60–66` 的 K(c)（`v2 c′_n=n−ε(n)`）。记录恒等式本身正确：`Γ_u=Γ_T+1+ε_D`，`σ_D=n−ε_D` ⇒ `Γ_u+σ_D=Γ_T+n+1=Γ_T+j=R_T`（我用 P=14 的精确数复算为 6134=6134）。原文缺定义/引用。 |
| E6 | L125 | “76 canonical b-reference chains” 名不符实：是 fire-shaped (x,x+1)，不是 b-entry (y,y) | **confirmed（minor）** | `verify_shift_transport.py:57–60` 取 `a=cal.crossing(p−1)`（odd、type a），构造 `xc=3*a['time']+4`、`tc=xc+1`。这正是 pointer p−1 的 canonical fire `(x,x+1)`；b-entry 应为 `V(fire,−1)=(y,y)`（`PROOF_A_SOURCE_DESCENT.md:27`：`y=6l+4, Theta_ref=y`）。我的重算：p=5 时 `xc=10, tc=11, fire_x=10, b_entry_y=10`，`is_fire_shaped=true, is_b_entry_shaped=false`；全部 4 对 loop-1 祖先也都是 `(10,11)` 而非 `(10,10)`。76 个计数本身正确。 |
| E7 | L121–L128 | [B] 证据弱：4 对全 p=5/precision 4；260 参考全单状态；4,940 中只有 390 长度>1（4,550 长度 1） | **confirmed（minor）** | 独立重算（`checkT_transport.json`）：`ancestor_p_values=[5]`，`precision=[4]`；`reference_tail_lengths={"1":260}`；end 参考长度 `{"1":4550,"2":375,"3":15}`，非平凡 390，matched 5,345。原文 L125 把 “For nontrivial continuations” 直接接到 4,940，确实把 4,550 个单状态 case 算进了“非平凡”证据。补充：审阅报告 §1.2 的 `{"1":4554,...}` 是全状态分布（含 4 个 ceiling），不是 end-only；E7 里的 4,550 才是对的（见 §4.4）。 |
| E8 | L90–L93, L106–L109 | “strict margin” 是 precision margin，不是 record 下降；只证了 outer c step 的 successor records <R_T，没证递归到 ancestor C 时其 source record <R_T | **confirmed（minor，措辞）** | 原文 L35–36 的 “strict margin” 是 `records<σ_C<σ_D`，即 `σ_D−σ_C>0`（A-SOURCE MARGIN 的 `rho−p−1`）；L83–85 才给出 outer 后继记录 `<R_T`。§4 L93 的 “each transport retains a strict margin” 指同一 precision margin。递归本身是证明义务（按原 source index 下降，L91–92），不是 walk 的一步，因此不需要 `R_{T'}<R_T`；但原文没有说明这一点，“strict margin” 容易被读成记录下降。 |
| E9 | L3–L6, L137–L138 | “including mixed histories” 依赖 accepted A-SOURCE 的 written proof；§4 说 mixed-history verifier 分支被禁用；本文有限测试没有 mixed histories | **refuted（作为错误）** | 事实都对：`PROOF_A_SOURCE_DESCENT.md:179–185` 说 mixed-history 分支 “was not implemented correctly and is now explicitly disabled”，本文 §5 的有限测试也不含 mixed histories。但本文自己已写明：L122–123 “All these small ancestors are terminal; they do not exercise mixed-history transport”，L137–138 “All general-history content depends on the accepted AB/HP ancestry proof, not on extending these finite tests”。A-SOURCE 是已接受定理（`CHECKPOINT_1RB1LA_0RC0RD.md:554–561`：“mixed histories are untested. The general mixed-history claim depends on the written AB/HP precision proof … `PROOF_A_SOURCE_DESCENT.md` (accepted)”）。因此 “including mixed histories” 由被引用的 accepted written proof 支持，本文没有把它冒充为有限证据；不构成错误。 |

---

## 2. FIRST_A_REDUCTION.md

### 2.1 独立重算的事实基线

`checkT_verify_first_a_copy.py`（复制版，PASS）与 `checkT_first_a.py` 一致给出：

- 336 个真实源 = 252 fire + 84 个 odd c 源；5,712 个源/移位对；
  `counts={zero_shift:336, no_A:4032, valuation_mismatch_closes:852, collision_end:492}`；
- `minimal_class_end=488`，`minimal_class_ceiling=4`，`max_extra_bits=3`；
- 四个例外正是 (17,−3,8,32,37,[5,6,1])、(90,−3,7,96,101,[5,5,1])、
  (161,−3,9,416,421,[5,7])、(234,−3,7,96,101,[5,5,1])；
- 84 个首 a-步：min m=5，min s_A=52，min y=248，min(y+2η)=232，
  min(6s_A+5−x_A)=157，min q=1，q 分布（η=−3 时）
  `{1:56, 2:1, 3:14, 4:6, 5:4, 6:1, 7:1, 9:1}`；
- 碰撞表与原文完全一致：奇 η→q=1，±2,±6→2，±4→3，±8→4；
- 492 个碰撞的真实 walk 全部在首个 a-output 处结束（`real_len−i−1=1`）；
- `Calendar.crossing(-1)` 抛 `KeyError: -1`；`X(0..3)` 全偶（`odd=False`）；
- 4 个首 a-步输入链的 `λ_in=x_A−(3s_A+4)` 为负（见 §4.1）。

### 2.2 逐条复核

| 项 | 行号 | 审阅者主张 | 判定 | 复核证据 |
|---|---|---|---|---|
| E0 | L52 | `y=3s'+4+λ_Y≥28` 需要 λ_Y≥0；L49 的 nonnegative lambda mass 只在 x_A 的不等式里出现，L52 未说明它对新交叉适用，非负性也未证明/引用；只按 L49 可得 y≥25 | **confirmed（但审阅者的数值退路是错的）** | 缺口本身成立：L52 的 `y=3s'+4+λ_Y` 要得到 ≥28，需要新链的 λ_Y≥0；原文只把 “nonnegative lambda mass” 用在 L49 的 x_A≤6s_A+5 上。但审阅者的 “只按 L49 可得 y≥25” 不成立：由 `y=2Θ_A+6k−x_A/2`、`Θ_A=3s_A+5`、`x_A≤6s_A+5`、`s_A≥5`、`k=τ(m−1)/2≥1` 得 `y≥3s_A+7.5+6k≥28.5`，整数 ⇒ y≥29。另有恒等式 `λ_Y=y−(3s'+4)=3s_A+3−x_A/2≥1/2`，所以 y≥3s'+4 直接成立。数据：84/84 满足 `y≥3s'+4`，`min λ_Y=79`，`min y=248`；`lam_new_formula_bad=0`。结论：需要补一步恒等式/引用，但常数 28/12 是对的，不应改成 25/9。 |
| E1 | L59 | “All parameters <=4 have even returns” 中 j=0 未定义：本模型无 X(−1)，`Calendar.crossing(-1)` KeyError；需 q≥1 | **confirmed（minor，措辞）** | `cal.crossing(-1)` 抛 `KeyError: -1`；`X(0..3)` 全偶。原文自己的 §2 已给出 m≥5（odd a call 读 X(m−1)，m−1≥4），于是 `x_A=2^m u, m≥5` ⇒ `x_A/2` 被 16 整除，而 `2Θ_A+6k` 偶 ⇒ `y` 偶 ⇒ `q=v2(y)≥1`；又 h≥1，所以 `min(q,h)∈[1,4]`。数据 min q=1。因此实际用的参数范围是 1≤j≤4，原文写成 “<=4” 不精确，但结论不受影响。 |
| E2 | L102–L103 | “The only positive-output obstruction” 与 §2 的正性矛盾；真正剩余障碍是等估值碰撞 | **refuted（作为“矛盾”）** | §2 的确证明 `y+2η≥12>0`；“positive-output obstruction” 最自然的上下文是上一版 work_claude_ext_next 的 “nonpositive-output exception”（`work_claude_ext_next/NOTES.md:150–152`：z≤0 at m∈{5,8} for δ≥5），此处 “positive-output” 是与 “nonpositive-output” 相对的 case，而不是“输出为正的障碍”。原文 §3 的剩余分支确实是 `q=h`（等估值碰撞），审阅者建议的改写更清楚，但“与 §2 矛盾”不成立。 |
| E3 | L166–L168 | 四个状态只有 3 个不同残基类/3 个不同词；P=90 与 P=234 的 (K,x mod 2^K,Θ mod 2^K,词) 完全相同 (7,96,101,(5,5,1)) | **confirmed（minor）** | 独立重算四个例外：`exception_distinct=3`（按 (K,x,Θ,word)），`exception_distinct_words=3`；P=90 与 P=234 均为 K=7, x_res=96, Θ_res=101, word=[5,5,1]。两者的实际 (y_s,Θ_s) 在 K 位以上不同（bit 长 91 vs 235，高位不同），但其 K-残基和已认证的 suffix word 相同。因此 “their different continuations” 对这四个状态不准确；“保留完整 K-残基” 也不能区分 90 与 234，只有更高位（超出 K）能区分，而那不影响已认证的 continuation。 |
| E4 | L99–L101 | “SHIFT_TRANSPORT reduces … to earlier real chains” 依赖未审的 SHIFT_TRANSPORT；其 §4 用 (z,z+2+η) 参考表述第一 A 输出族，是否本文意义下的真实链未逐族说明 | **confirmed（依赖/措辞），但审阅者的一处怀疑不成立** | 该句确实依赖 `work_c3_drift/SHIFT_TRANSPORT.md`（自称 UNREVIEWED），且本文没有把该句标为 [C]。SHIFT_TRANSPORT §4 的 terminal E 列表里，“first A-output of an A-initial epoch” 本身是一个真实 a-output（真实链，真实尾存在），所以 §1 的真实尾假设可以直接对它用；但 SHIFT_TRANSPORT §4 又给出 `(z,z+2+eta)` 的 C3 参考（z=6k+2），那个参考不是真实链，若走那条路线 §1 不适用。原文没有逐族说明，审阅者的修正要求合理；但“该族是否就是真实链”的答案对 E 是肯定的（对 (z,z+2+eta) 参考是否定的）。 |
| E5 | 全文 | 没有任何 [A]/[B]/[C] 标注 | **confirmed** | 全文 grep `\[A\]\|\[B\]\|\[C\]` 无命中。§1–§3 的归约、§5–§6 的有限检查、§4 的跨文件应用句都没有标签，不符合项目标注要求。 |
| E6 | L4–L5 | “the shift range needed by the current Lambda<=4 drift argument” 未说明：Λ≤4 的 ε∈{3,5} c 步只产生整数移位 {0,±1}；本文不覆盖 BBBAA 的 +4/3 或 O1 的 η_r；L112 只笼统写 outside this bounded range | **confirmed（minor，范围表述）** | 我从 calendar 复算 source-shift 类：76 个 A(ε=3) 源 `s≡0 mod 2^{ω+1}`，4 个 BA(ε=5) `s≡1`，4 个 AA(ε=5) `s≡−1`（≡3）；与 accepted 的 c 步类恒等式一致。BBBAA 的 +4/3 与 O1 的 `η_r=−5+8/3^r` 都不是整数，本文只覆盖 `η∈{−8,…,8}` 整数，L112–113 的 “outside this bounded range” 没有区分“超出范围”与“非整数”。因此该句需要写明：Λ≤4 漂移所需的是整数移位；有理移位（O1/BBBAA）另需 RATIONAL_MODE/ODD_DENOMINATOR 型处理。 |

---

## 3. 对“障碍 O1/O2/O3”的处理检查

- **O1（有界高度有理位移不安全）**：SHIFT_TRANSPORT 完全没有提到 r、3^r、η_r 或危险剩余类；
  FIRST_A 只处理整数 |η|≤8。两者都没有给出 O1 要求的 r–σ 关联。审阅者的 E0（shift）与 E6
  （first_a）在这点上正确。需要强调：O1 §1 断言 common-shift 证明“在代数上可推广到奇分母有理
  eta”，该断言只做了 scaling 论证；即使接受，O1 §2–§4 的 η_r 仍表明 `Safe(C,η_r)` 会失败，
  所以“有界高度”不足以代替 r–σ_C/剩余类条件。
- **O2（affine 来源/β 判据）**：两文都只用 scalar (x,Θ) 与相位移位，没有保留
  `x=A*U+β, Θ=2^J U+3d+1, v2(A)=J−Γ`，也没有使用 `v2(β')<J−Γ−1`。这是事实，但两文都没有
  声称解决了 O2 所针对的 small-gateway 局部闭合；不能据此判为文档错误。
- **O3（编码上界）**：两文都不做局部相位类编码（FIRST_A 保留完整残基 + 实际来源），方向与
  O3 的教训一致；但都没有处理“预留 S 位不能覆盖所有类”的计数问题，也没有声称处理了。

---

## 4. 审阅者漏掉或说错的地方（复核者独立发现）

### 4.1 [新发现，minor/major 视解读] FIRST_A L49 的“nonnegative lambda mass”前提对 4 个规范首 a-步为假

原文 L49：`If its time is s_A, nonnegative lambda mass gives x_A<=6*s_A+5`。我把 84 个首 a-步的
输入链的 `λ_in=x_A−(3s_A+4)` 全部算出来，发现 **4 个规范 fire 源的首 a-步输入链 λ_in<0**：

| P | i | g | m | λ_in |
|---|---|---|---|---|
| 65 | 1 | 2 | 5 | −46116860184273879039 = 1−x0/4 |
| 101 | 1 | 2 | 8 | −3169126500570573503741758013439 = 1−x0/4 |
| 136 | 1 | 2 | 5 | −21778071482940061661655974875633165533183 = 1−x0/4 |
| 209 | 1 | 2 | 5 | −1028440348325753776346855739098344065614209916020987414592880639 = 1−x0/4 |

（x0=6k+4 是该 fire 的分子；`checkT_extra.json`。）这些链的 λ_in=1−x0/4<0，所以“nonnegative
lambda mass”作为链级前提为假。不过 `x_A≤6s_A+5` 在这 4 例仍然成立（slack ≥1.5×10^20），
`y≥3s'+4` 和 `y≥28` 也仍然成立（新链的 λ_out=3s_A+3−x_A/2≥1/2）。因此这不推翻 FIRST_A 的
结论，但说明：审阅者的 E0 只质疑“新交叉的 λ_Y≥0 未证明”，实际更严重的是**输入链的 mass
前提本身在规范数据上有反例**；正确的补法不是引用“两部分非负”，而是写出
`λ_out=3s_A+3−x_A/2` 并把 x_A 的界（或另证）用上。

### 4.2 [新发现，minor] SHIFT_TRANSPORT 也没有 [A]/[B]/[C] 标注

审阅者只对 FIRST_A 提了“无标注”（E5/E6）。SHIFT_TRANSPORT 全文同样没有 [A]/[B]/[C]；
它只有 “UNREVIEWED conditional lemma” 的标题。按本轮标准，§2–§4 的条件归约应标 [A]（假设列全后）、
§5 的有限测试标 [B]、§4 的 terminal 分类/开放项标 [C]。

### 4.3 [审阅报告自身的数字错误] first_a.md 的 E0 “只按 L49 可得 y≥25” 不成立

重算：`y=2Θ_A+6k−x_A/2 ≥ 6s_A+10+6k−(6s_A+5)/2 = 3s_A+7.5+6k ≥ 28.5`（s_A≥5, k≥1）。
又由 `λ_out=3s_A+3−x_A/2 ≥ 0.5` 得 `y≥3s'+4≥28`。所以审阅者建议的“把常数改为 y≥25、
y+2η≥9”既不必要，也会削弱正确常数。E0 的核心（L52 缺一步依据）仍成立，但数值退路应撤回。

### 4.4 [审阅报告自身的不一致] shift_transport.md §1.2 的 tail-length 分布

§1.2 记 `synthetic_reference_tail_lengths={"1":4554,"2":375,"3":15}`（总和 4,944）；这是
**包含 4 个 ceiling** 的全状态分布。end-only 分布是 `{"1":4550,"2":375,"3":15}`（总和 4,940，
=4,940 个 end 参考），也是 E7/E8 里 4,550/390 的来源。E7 的 4,550 正确；§1.2 的 4554 容易
被误读为 end 参考，应注明含 ceiling。

### 4.5 [审阅者未展开，但已核对] 4 个 forced controls 的“deliberately chosen”措辞

`verify_shift_transport.py` 对每个 `crossing(p−1)` 为 odd a 的 p 都计算 forced shift，但只有
4 个 p 的 `crossing(q−1)` 也是 odd a（q=val(xc)），所以恰好 4 个 forcing。原文 “Four additional
deliberately chosen shifts” 的数字正确，但它们是系统导出的，不是任意挑的；这一点不影响结论。

### 4.6 [审阅者未提，但已核对] FIRST_A §5 “336 real source chains” 的构成

独立重算：252 个 fire 源 + 84 个 odd c 源 = 336；5,712=336×17；336=252+84。5,712 的四个分类
（336/4032/852/492）也逐项复算一致。该句正确。

---

## 5. 范围与尺度依赖检查（是否隐藏参数上界/有限外推）

- SHIFT_TRANSPORT §2–§4：证明只依赖 A-SOURCE 的 `p,rho,σ_C` 与 HP，**不依赖** N0、2·10^7、
  j<2·10^7、[−12,15]、T_h、log* J；这是它的优点，也是它不能处理 O1（需要 r 与 σ_C 的关联）的原因。
  §5 的 `p≤256, η∈[−32,32]` 是 [B]，原文已写 “These are not EXT counterexamples” 等限定。
- FIRST_A §1–§3：符号论证不依赖 J；`η∈{−8,…,8}` 是显式输入范围；§4 的 “Λ≤4” 隐含 J<T_4
  （Λ(K_clock)=4, T_3<K_clock<T_4），原文没有写出 T_4。§5–§6 的 P≤256 是 [B]，原文已写
  “finite selection”。没有把有限范围写成 all-j。
- 两文都没有使用 CAL-C/R1/H3 型“参数上界当统一目标”的条件；FIRST_A 的 §1 真实尾输入来自
  real S1（completed epoch），不是参数上界。但 FIRST_A L4–L5 的 “Lambda<=4 drift argument”
  是范围依赖（J<T_4），不是参数上界；应像审阅者 E6 建议的那样写明。
- 未发现把 `mod 2^j` 与 `mod 2^{j+1}` 混用：FIRST_A §6 的最小类用 `j+1` 位、K-柱体用 K=R+1 位；
  SHIFT_TRANSPORT §2–§3 的精度是 σ_C/σ_D，代数上 `v2(c_D)=σ_D` 与 `j=n+1` 的关系正确。

---

## 6. 总评

1. **SHIFT_TRANSPORT**：§2 的 precision lemma、§3 的 A-SOURCE 祖先公式（`σ_C=p−1−e−Λ`、
   `σ_D−σ_C=ρ−p−1>0`）、c-step 代数与 `Γ_u+σ_D=R_T` 都经独立重算成立；作为条件归约可用。
   但 Safe 缺 `x≠0`（E2，major）、`j_D=j_C` 与 `+2^j` 不变性未写（E3）、reference calls 未验证
   （E4）、ε_D 未定义（E5）、[B] 证据被 “b-reference/4,940” 高估（E6/E7）、strict margin 措辞
   （E8）。E0 的 source-shift 区分成立但原文自限于整数 eta；E1 与 E9 所指责的“过度声称/未审依赖”
   在原文里都有明确声明，不能算文档错误。
2. **FIRST_A**：§1–§3 的首次 a-步恒等式 `y_η=y+2η`、`T_η=T+η`、`σ−G−1`、`q≠h⇒min(q,h)≤4`、
   `q=h` 的真实尾终止，以及 §6 的 K-柱体，都经独立重算成立；492/852/4,032/336 与 488/4 全部复现。
   主要问题是 L52 的 λ_Y≥0 缺一步依据（E0；但审阅者的 y≥25 是错的）、L49 的 mass 前提在 4 个
   规范深层首 a-步为假（4.1，新发现）、j=0 的措辞（E1）、P=90/234 的重复类（E3）、跨文件依赖
   （E4）、无标注（E5）、Λ≤4/有理移位范围（E6）。E2 的“正性矛盾”不成立。
3. **没有**把未证内容写成 [A] 的实质性越界；两文都声明 UNREVIEWED/条件性。但两文都缺
   [A]/[B]/[C] 标签，SHIFT_TRANSPORT 的标签缺失被审阅者漏掉。
4. 本报告没有修改任何原文档，没有 git 提交，没有声称全局 EXT。

---

## 7. 复现文件

- `scratch/checkT_transport.py` → `checkT_transport.json`
- `scratch/checkT_first_a.py` → `checkT_first_a.json`
- `scratch/checkT_first_a_aux.py` → `checkT_first_a_aux.json`
- `scratch/checkT_shift_algebra.py` → `checkT_shift_algebra.json`
- `scratch/checkT_extra.py` → `checkT_extra.json`
- `scratch/checkT_verify_shift_transport_copy.py` → `scratch/transport_checks.json`（PASS；
  这是复制版按原脚本的 `Path(__file__).with_name(...)` 写出的文件，未写 `work_c3_drift/`）
- `scratch/checkT_verify_first_a_copy.py` → `scratch/first_a_checks.json`（PASS；同上）

两个复制版 verifier 只用于“在不写 `work_c3_drift/` 的前提下重跑原脚本”；
路径改动已在 §1 开头说明。`work_c3_drift/transport_checks.json` 与
`work_c3_drift/first_a_checks.json` 的 mtime 保持 2026-10-23 00:42，未被本次复核改写
（`git status --short` 只显示 `work_landing_symbolic/` 为未跟踪，`work_c3_drift/` 无改动）。
