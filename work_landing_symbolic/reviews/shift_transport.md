# 审阅报告：work_c3_drift/SHIFT_TRANSPORT.md

审阅日期：2026-10-23。审阅对象：`work_c3_drift/SHIFT_TRANSPORT.md`（140 行，2026-10-20，
作者自标 **UNREVIEWED conditional lemma**）。本报告只评价该文档自身的论证与有限证据；不修改原文，
不声称全局 EXT，不改变 K_clock。

**结论先行。** §2 的 common-shift precision lemma 在补齐若干假设后是正确的 [A]；§3 引用的
A-SOURCE 祖先公式（`sigma_C=p-1-e-Lambda_source`、`sigma_D-sigma_C=rho-p-1>0`）与
`work_ext_roots/PROOF_A_SOURCE_DESCENT.md` §2 的已接受证明一致；§3 的 c-step 代数与记录恒等式
`Gamma_u+sigma_D=R_T` 正确。但该文的 `eta` 是 **outer defect shift**（`eta=theta_T-2`），不是本轮
所问的 c-step **source shift s**（`s=theta_D-2`，取 0、±1、4/3 等），所以它没有给出 source-shift
分类，也没有认证 landing 类；§4 的 “remove” 只是把 later A-initial c source 归约到更早的
`Safe(E,eta)`，real fire 与 b/c-initial c source 两个 terminal families 仍无界（first A-output 只归约到
C3 reference）。有限证据 [B] 的数字与 JSON 一致，但比文字弱得多：
4 个 AA pair 的 ancestor 全是 p=5、全是单状态；4,940 个 synthetic reference 中只有 390 个长度 >1。
该文没有处理 O1（有界高度有理位移）、O2（仿射 gateway）、O3（编码限制）；它没有证明全局 EXT，
也没有这样声称。总评：作为条件归约可用，需补假设与改正表述；不能作为本轮 landing 目标或全局 EXT 的证据。

---

## 1. 验证命令与输出

### 1.1 文档自带 verifier（工作流已运行一次，本审阅未重复运行）

工作流报告：`python -B work_c3_drift/verify_shift_transport.py`，exit 0；
`work_c3_drift/transport_checks.json` 的 `status=PASS`、`review_status=unreviewed`。

JSON 关键内容（`work_c3_drift/transport_checks.json:1-74`）：

- `canonical_pairs` 4 对：`P=14/87/158/231`，全部 `p=5`、`ancestor_index=5`、`precision=4`；
  源下标分别为 `6133`、`289086270696314883188925376`、
  `136517131539405869694540270279944446662008190014`、
  `6446839263191968112703081097646156153307841449936119739796858726807903`。
- `reference_status: {end: 260}`，`matched_states: 260`。
- `synthetic_lift_reference_status: {end: 4940, ceiling: 4}`，`synthetic_lift_matched_states: 5345`。
- `unresolved_controls` 4 条，`p=64,100,135,208`，`status=ceiling`，`kind=canonical reference`。

### 1.2 本审阅额外运行的 scratch 脚本（全部写入 `work_landing_symbolic/reviews/scratch/`）

1. `python -B work_landing_symbolic/reviews/scratch/review_shift_transport_checks.py`
   → `PASS`。独立重算并与自带 JSON 对数：

   - `ancestor_p_values=[5]`，`ancestor_precisions=[4]`；
   - `integer_eta_cases=260`，`reference_tail_lengths={"1":260}`，`matched_states=260`；
   - `fire_references=76`，`synthetic_status={"end":4940,"ceiling":4}`，
     `synthetic_reference_tail_lengths={"1":4554,"2":375,"3":15}`，`synthetic_matched_states=5345`；
   - 4 个 forced controls 的 `next_x_is_2sc=true`（p=64,100,135,208）；
   - 24 个 rational-eta 诊断探针全部 same/precision（**仅诊断**；文档只声称整数 eta）。

2. `python -B work_landing_symbolic/reviews/scratch/rational_eta_lift_checks.py`
   → `PASS`。在 synthetic lifts 上对 8 个有理 eta（含 `-7/3`、`-5+8/3`、`-5+8/9`、`1/3`、`-1/27`）
   检查 608 个 case：560 个 reference 长度 1、48 个长度 2，全部 same word 且 precision ok。
   **这只是 2-adic shadowing 的诊断，不是对 Z[1/3] 的证明；文档没有作此声称。**

3. `python -B work_landing_symbolic/reviews/scratch/orbit_source_recheck.py`
   → `PASS`。只读复算 O1 的 canonical source 数据：P=49，`k_fire=469124961184426`，
   `sigma=1051689726214394`，`x0=5*2^49`，`y=4222124650659962=16A+10`，
   `A=263882790666247≡7 mod 8`，`r>=657306078883964`。这确认 O1 的源数据，不是对本文的验证。

（自带 verifier 未重复运行；上述 scratch 均为独立重算/诊断。）

---

## 2. 背景与依赖

- **A-SOURCE**：`work_ext_roots/PROOF_A_SOURCE_DESCENT.md` 已接受。本文 §3 引用的
  `sigma_C=p-1-e-Lambda_source`（§2 line 83/96）、`sigma_D-sigma_C=rho-p-1>0`（line 113）、
  两差至少 `2^sigma_C`（line 105-113）、`C_t` 是 earlier real fire 或 earlier a-output
  （line 116-128）均一致。A-SOURCE 的 **构造**（C 的存在与精度）不使用 EXT；只有最后
  “EXT(J') 转移 termination” 一步使用较小 EXT（line 130-137）。本文只用构造，不用该最后一步。
- **HP**：`work_global_ext/PROOF_EXT.md:68-74` 的 Lemma HP 明确要求两条 walk 的 `j_0` 相等，
  且 reference walk 的 `x*_i≠0`。本文 §2 的证明没有写出这两个前提（见错误 E3/E4）。
- **K(c)**：`work_global_ext/PROOF_EXT.md:60-66`：type c 的 W-chain 是 source chain，
  `sigma=n-epsilon(n)`；本文 §3 line 70 的 `v2(c_D)=sigma_D=n-epsilon_D` 即此恒等式，但文中未引用/定义。
- **本轮三条障碍**：
  - O1 `work_c3_drift/ORBIT_SHIFT_OBSTRUCTION.md:34-98`：`eta_r=-5+8/3^r`，`|eta_r|<=5`，
    在 `r>=657306078883964` 时 canonical P=49 源的首个输出即耗尽严格精度；所以“有界高度位移都安全”为假，
    必须把 r 与祖先精度关联或排除危险剩余类。本文完全没有提到 r、3^r 或该 eta_r。
  - O2 `work_c3_drift/STOP_CHECKPOINT_2026_10_21.md:62-77`：必须保留实际仿射来源
    `x=A*U+beta, Theta=2^J*U+3d+1, v2(A)=J-Gamma`，判据 `v2(beta')<J-Gamma-1`；
    本文只用 scalar `(x,Theta)` 与 phase shift，没有 affine origin/beta。
  - O3 `work_c3_drift/OPTIMAL_PHASE_ENCODING.md:61-96`：局部相位类+预留 S 位不能覆盖所有类
    （S=m=64 时上界 8,338,590,849,833,250 < 2^64），必须用实际来源/相位限制。本文使用 A-SOURCE
    的实际来源（这一点与 O3 的方向一致），但没有解决编码/预留问题，也没有把它作为结论。
- **本轮目标**：输入相位 `theta+s`（`s∈Z[1/3]`，高度 <=h）时认证 landing 类，或有限步 gateway
  且每步记录下降。本文的 `eta` 是 outer defect 的 shift（`eta=theta_T-2`），与本轮/checkpoint
  所说的 **source shift s**（`s=theta_D-2`）不是同一个量；本文没有 source-shift 分类 0,±1,4/3。
  参见 `CHECKPOINT_1RB1LA_0RC0RD.md:665-681` 的 “beyond T4 classify c steps by source shift”，
  以及 `work_c3_drift/RATIONAL_MODE.md:1-60` / `ODD_DENOMINATOR.md:1-50` 中对 source defect D 的约定。

---

## 3. 逐条结论表

| 行号 | 结论（一句话） | 标签 | 判定 | 说明/依据 |
|---|---|---|---|---|
| L10-L12 | 链的 scalar state 为 `(x_C,Theta_C)`，`Theta_C=3s_C+5`，`sigma_C` 为 physical coefficient valuation。 | 定义 | 正确 | 与 `PROOF_EXT` §2 的链约定一致。 |
| L14-L16 | `Safe(C,eta)`：从 `(x_C,Theta_C+eta)` 的 scalar walk terminates，且每个 `parameter+accumulated loss < sigma_C`。 | 定义 | **有缺口** | 未要求每步 `x_i≠0`；HP 需要（`PROOF_EXT:68-74`）。见 E3。 |
| L18-L19 | `Safe(C,0)` 不蕴含任意 `Safe(C,eta)`。 | [A]+[B] | 正确 | §5 的 canonical fire 反例支持；O1 的有理位移是更强的同类现象。 |
| L23-L30 | 若 `v2(x_D-x_C),v2(Theta_D-Theta_C)>=sigma_C`、`sigma_D>sigma_C` 且 reference calls defined，则对每个整数 eta，`Safe(C,eta)⇒Safe(D,eta)`。 | [A] | 正确（条件） | 需补 `x_i≠0`、`j_D=j_C`、`reference calls defined`；见 E3/E4/E5。 |
| L32-L38 | 证明：同一 table、初始精度 `sigma_C`、reference records `<sigma_C`，HP 逐步传递；参数/类型/损失相同。 | [A] | 正确（条件） | 与 HP 一致；未写出 `j_0` 相等与 `x*≠0`。 |
| L40-L42 | 这是 general precision lemma；A-SOURCE 提供 genuine earlier canonical chains。 | [A] | 正确 | A-SOURCE 是已接受的；构造不使用 EXT。 |
| L46-L57 | A-SOURCE ancestor：`sigma_C=p-1-e-Lambda_source`，`sigma_D-sigma_C=rho-p-1>0`，两差可被 `2^sigma_C` 整除；C 是 earlier real fire 或 earlier a-output；source index 更小；epoch 已完成。 | [A] | 正确 | 与 `PROOF_A_SOURCE_DESCENT.md:83,96,105-113,116-128` 一致。 |
| L59-L74 | outer c-step：`x_u=c_D u+x_D`，`Theta_u=Theta_T+Theta_D-2`，`eta=theta-2`；与 `(x_D,Theta_D+eta)` 的 x 差 valuation `sigma_D`，phase 差可被 `2^j` 整除；故与 `(x_C,Theta_C+eta)` 一致到 `sigma_C`。 | [A] | 正确 | 代数正确；`j>sigma_D>sigma_C`。需说明 eta 是 outer shift，不是 source shift s。 |
| L76-L86 | `Safe(C,theta-2)` 足够 terminate outer tail；`Gamma_u=Gamma_T+1+epsilon_D`，`Gamma_u+sigma_D=Gamma_T+j=R_T`；successor records `<sigma_C<sigma_D`，故 `<R_T`；结论不依赖 source deficit/N0/window。 | [A]（归约） | 正确 | 记录恒等式正确； “不依赖 N0/window” 只对 reduction 成立，不覆盖 terminal families。 |
| L90-L93 | 若 C 仍是 A-initial 的 later a-output，递归；original source index 严格下降 ⇒ 有限；eta 不变；每步保留 strict margin。 | [A] | 正确 | “strict margin” 是 `sigma_C<sigma_D`，不是 record 下降；见 E9。 |
| L95-L104 | Terminal E = real fire（用 b crossing）/ first A-output / b-or-c-initial c source；first A-output 用 `(z,z+2+eta)`，`z=6k+2`，precision `P-1`，`q<P-1`；不自动认证所有 eta。 | [A] 分类 + [C] 未解 | 正确（分类） | first A-output 的 real chain 对 `(z,z+2+eta)`；shifted chain 对 `(z,z+1+eta)`；需补与 C3/F(q)/A2(q) 的关系。见 E11。 |
| L106-L109 | 所有 later A-initial c source 可从 interior shifted-safety obligation “removed”，无 epsilon cutoff；余下 fire/b/c-initial 仍无界；这是 uniform reduction，不是 residual families 的证明。 | [A] 归约 + [C] 开放 | 正确（归约） | “removed” 应读作 reduced to `Safe(E,eta)`；不是 elimination。见 E2/E9。 |
| L111-L115 | eta=-1 回到 A-SOURCE 的较小 strict EXT；eta=0 由 real S1；其他 eta 两者都不直接给。 | [A] 相对已接受结果 | 正确 | eta=-1 对应 canonical outer defect theta=1；不是 source shift s 的 AA 值（巧合相同）。 |
| L121-L123 | 4 个 actual AA/earlier-b ancestor pairs，eta=-32..32，260 transferred cases pass；ancestors terminal，不测 mixed histories/long continuations。 | [B] | 数字正确，证据弱 | 4 对全部 p=5、precision 4；260 个 reference 长度全为 1（单状态）。见 E8。 |
| L125-L128 | 76 个 canonical “b-reference” chains，p<=256，eta=-32..32 + synthetic congruent lifts at precision p-1；4,940 terminating references，5,345 states；lifts 非 canonical。 | [B] | 数字正确，名不符实 | 实际是 fire-shaped references（`cal.crossing(p-1)` 的 a 型链，`(3τ+4,3τ+5)`），不是 b-entry；4,940 中只有 390 个长度>1。见 E7/E8。 |
| L130-L135 | 4 个 forced shifts 使 next a numerator = `2^(p-1)`，达到 precision ceiling；verifier 保留为 unresolved；说明 “Safe 对所有整数 eta” 假；不是 EXT 反例（reachability 未证）。 | [B]/[A] | 正确 | 本审阅独立确认 next_x=2^sc，p=64,100,135,208；eta 是巨大整数，不是 O1 的有界高度有理 shift。 |
| L137-L138 | 所有 general-history 内容依赖 accepted AB/HP ancestry proof，不依赖有限测试的外推。 | [A] 依赖 | 正确 | A-SOURCE 的 mixed-history verifier 分支在 `PROOF_A_SOURCE_DESCENT.md` §4 被禁用；mixed histories 只有 written proof 支持。见 E10。 |
| L139-L140 | 进一步工作：控制 terminal families 的 reachable shift eta，含 first non-descent 与后续 record budget。 | [C] 开放 | 正确 | 本轮 O1/O2/O3 仍未解决；该文没有给出这些控制。 |

---

## 4. 错误清单（行号 + 严重度 + 修正）

### E1（major，L21-L30、L57、L86）— 整数 eta / outer shift vs 本轮的 Z[1/3] / source shift s

- **问题**：定理只对 **整数** eta 证明；本轮要求 `s∈Z[1/3]`（O1 的 `eta_r=-5+8/3^r` 就是有理），
  而本文的 `eta=theta_T-2` 是 **outer defect shift**，不是 c-step 的 **source shift**
  `s=theta_D-2`（0、±1、4/3…）。文中没有把实际分母深度 r 与 `sigma_C` 关联，也没有排除危险剩余类。
  §3 line 57 “supports all common shifts” 与 §4 line 111 的 eta=-1/0 容易被误读为 source-shift 分类。
- **修正**：明确写 “integer eta only”；把 `eta` 与 `s` 的定义并列写出（`eta=theta_T-2`，`s=theta_D-2`），
  说明本文只做 outer-phase ancestry transport；补充 Z[1/3] 的 2-adic 版本（或引用 companion docs），
  并把 O1 的 `r`-`sigma_C` 关联/危险剩余类作为独立假设或结论。若只保留整数版本，则删去 “all common shifts”
  的宽泛表述，明确 O1 不在本文范围。

### E2（major，L95-L109、L139-L140）— “remove” 只是归约，terminal families 未解；O2/O3 未处理

- **问题**：`Safe(E,eta)` 仍是 real fire 与 b/c-initial c source 两个无界 families 的 obligation；
  first A-output 也只是归约到 `(z,z+2+eta)` 的 C3 reference（records <P-1），不是对所有 eta 的认证。
  本文没有给出 landing 类证书、没有有限 step gateway、也没有“每步记录严格下降”的 terminal 处理。
  对 O2 的 affine source/beta 判据（STOP_CHECKPOINT:62-77）和 O3 的编码限制
  （OPTIMAL_PHASE_ENCODING:61-96）没有任何正面处理。“all later A-initial c sources can be
  removed” 的 “removed” 不是 elimination。
- **修正**：改成 “reduced to `Safe(E,eta)` at an earlier terminal real chain”；把 terminal families
  明确列为残余；说明本轮目标需要与 FIRST_A_REDUCTION（|eta|<=8）、RATIONAL_MODE/ODD_DENOMINATOR
  （有理 source defect）组合，并写出各自未闭合的条件；不要把 reduction 写成 landing 认证。

### E3（major，L14-L16、L32-L38）— `Safe` 缺 `x_i≠0`；HP 的 reference 前提缺失

- **问题**：`PROOF_EXT.md:68-74` 的 Lemma HP 明确要求 reference walk 的 `x*_i≠0`（“The hypothesis
  x* ≠ 0 is needed: a virtual resonance x* = 0 exists”）。本文的 `Safe` 只写 “terminates” 和 record 界，
  没有排除 `x=0`；若 reference 在中间出现 `x=0`，`j` 未定义，HP 不适用。`bounded_walk` 也把 `x==0`
  单列为 `zero`（`verify_shift_transport.py:12-13`），说明这不是空洞的学究问题。
- **修正**：在 `Safe` 定义中加入 “`x_i≠0` at every step（no zero）”；在 §2 证明中引用 HP 的该条件，
  并说明 `Safe(C,eta)` 的 termination 是指到达 even return，不是 `x=0`。

### E4（minor，L32-L38、L59-L74）— 未写出 HP 的 `j_0` 相等与 eta 代表元不变性

- **问题**：HP 要求两条 walk 的初始 `j_0` 相等。证明只用了 `v2(x_D-x_C)>=sigma_C`；需要
  `Safe(C,eta)` 的首个 record `j_C<sigma_C` 才能推出 `j_D=j_C`。另外，`theta` 只按 `mod 2^j` 选代表，
  `Safe(C,theta-2)` 对 `eta→eta+2^j` 的不变性没有写；虽然 `j>sigma_C` 时由同一 precision lemma 可证，
  但文中没有这一步。
- **修正**：加一句 “`j_C+0<sigma_C` ⇒ `v2(x_D)=j_C`”；说明 `theta` 取 exact defect `Theta_T-x_T`，
  或证明 `j>sigma_C` 时 `Safe` 只依赖 `eta mod 2^{sigma_C}`（从而与代表元无关）。

### E5（minor，L23-L30、L59-L74）— “reference calls are defined” 在应用中未验证

- **问题**：§2 把 “the reference calls are defined” 列为假设；§3 应用时没有验证。参考 walk 的调用是
  `X(j_t-1)`，需要 `j_t<sigma_C`（由 Safe 给出）且 `sigma_C<J` 才能落在 `F defined through X(J-1)`
  的前缀内。本文有 `sigma_C<sigma_D<j_T<=J`（`j_T=n+1` 是 outer chain 的参数，`R_T<=J`），
  所以事实上成立，但没有写出。
- **修正**：在 §3 加 “`sigma_C<sigma_D<j_T<=J`，且 Safe 给 `j_t+loss_t<sigma_C`，故 `j_t-1<J-1`；
  所有 reference calls 已由 `F defined through X(J-1)` 定义”。

### E6（minor，L70-L71、L80-L82）— `epsilon_D` 未定义；未引用 Lemma K(c)

- **问题**：`v2(c_D)=sigma_D=n-epsilon_D` 是 c-step 的 `epsilon` 定义/恒等式（`PROOF_EXT:60-66`
  Lemma K(c)），文中既未定义 `epsilon_D`，也未引用 K(c)；`Gamma_u+sigma_D=R_T` 的推导依赖
  `epsilon_D=n-sigma_D`。
- **修正**：定义 `epsilon_D=n-sigma_D`，引用 Lemma K(c)，并写出
  `Gamma_u=Gamma_T+1+epsilon_D` ⇒ `Gamma_u+sigma_D=Gamma_T+n+1=Gamma_T+j`。

### E7（minor，L125）— “76 canonical b-reference chains” 名不符实

- **问题**：`verify_shift_transport.py:57-60` 取 `a=cal.crossing(p-1)` 的 **a 型** crossing，
  构造 `xc=3*a['time']+4`，`tc=xc+1`；这是 fire-shaped reference `(x,x+1)`（即 `F(q)`），
  不是 b-entry chain（b-entry 是 `V(fire,-1)=(y,y)`）。第一个 loop 的 C 也是 fire，不是 b-entry。
- **修正**：改为 “canonical fire-shaped references / fire chains at pointer p-1”，并说明它们与
  `F(q)`（`PROOF_LOW_DEFICIT.md:41-48`）的关系；若确实要测 b-reference，应取 `(y,y)` 并重跑。

### E8（minor，L121-L128）— [B] 证据比文字弱：全单状态、同一 ancestor、390/4940

- **问题**：4 个 AA pair 的 ancestor 全是 `p=5`、`precision=4`；260 个 reference 的 tail length
  全为 1（本审阅 `reference_tail_lengths={"1":260}`），即只比较了首状态，没有实际执行迭代 HP。
  Synthetic 部分：4,940 个 end case 中 4,550 个长度 1、375 个长度 2、15 个长度 3，只有 390 个
  真正有 continuation；“For nontrivial continuations, 76 ... 4,940” 把 4,550 个 trivial case
  也算进去了。
- **修正**：在 §5 写出分布与 “all four AA pairs share p=5/precision 4”；把 “4,940” 改为
  “4,940 个 reference 中 390 个长度>1（5,345 states）”；说明迭代 HP 只在 390 个 case 上被实际检验。

### E9（minor，L90-L93、L106-L109）— “strict margin” 是 sigma margin，不是 record 下降

- **问题**：§4 说 “each transport retains a strict margin”。这个 margin 是 `sigma_C<sigma_D`；
  本文只证明了 outer c step 的 successor records `<R_T`，没有证明递归到 ancestor C 时其自身 source
  record `R_{T'}` 也 `<R_T`（两者是不同的 source index/记录）。本轮要求的 “每步记录严格下降” 只在
  outer step 上明确。
- **修正**：明确 “strict margin” 指 precision `sigma_D-sigma_C>0`；若要声称记录下降，需给出
  `R_{T'}` 与 `R_T` 的比较，或说明递归是 proof obligation 而非 walk step，故不继承 `R_T` 的界。

### E10（minor，L3-L6、L137-L138）— “including mixed histories” 依赖未测的 A-SOURCE 分支

- **问题**：`PROOF_A_SOURCE_DESCENT.md` §4 明确说 mixed-history 的 verifier 分支 “was not implemented
  correctly and is now explicitly disabled”，checkpoint 也说 “mixed histories are untested”；本文 §5
  的有限测试没有 mixed histories。因此 “including mixed histories” 只有 accepted written proof 的支持，
  不是有限证据。
- **修正**：在 §5 明确 “mixed-history 部分只依赖 accepted A-SOURCE 的 written AB/HP proof，本文
  不独立验证”；若需要独立支持，应实现 mixed-history verifier。

### E11（minor，L95-L104）— first A-output 引用与 C3/F(q)/A2(q) 的关系未说明

- **问题**：`(z,z+2+eta)` 是 real first A-output 的 phase-two reference；C3 的 shifted chain 用
  `(z,z+1+eta)`；`eta=-1` 时是 `F(q)`（EXT(q)），`eta=0` 时是 phase-two `A2(q)`。文中只说
  “earlier c3 formula”，未写这三者的对应，读者可能把 `(z,z+2+eta)` 直接当成 C3 的 reference。
- **修正**：加一句对应关系：real chain ↔ `(z,z+2+eta)`，shifted chain ↔ `(z,z+1+eta)`；
  `eta=-1` ↔ `F(q)`（`PROOF_LOW_DEFICIT.md:41-48,97`），`eta=0` ↔ `A2(q)`（`PROOF_LOW_DEFICIT.md:50-56`）。

### E12（minor，L86）— “independent of ... finite window” 只对 reduction 成立

- **问题**：该句对 ancestry reduction 成立（不使用 N0/[-12,15]），但 terminal `Safe(E,eta)` 仍无界；
  O1 的有理 shift 需要 `r>=657306078883964` 的尺度，本文没有给出任何该类尺度控制。
- **修正**：改为 “this reduction uses no N0/window”；把 terminal obligations 的 unbounded 性和
  O1/O2/O3 列为未解，不要把 reduction 的 scale-free 说成整个 landing 问题的 scale-free。

---

## 5. 范围依赖（N0 / 窗口 / j<2e7 / T_h / log* J / 参数上界）

- **L86**：显式声称 “independent of the source deficit and of a fixed deep threshold or finite window”。
  这对 §2-§4 的归约成立；但 terminal `Safe(E,eta)` 没有尺度上界，且 O1 的有理 shift 的
  `r>=657306078883964` 完全不在文中。该行是“宣称不依赖”，不是“依赖”。
- **L121-L123**：有限验证范围 `P<=256`（实际 4 个 AA pair），`eta∈[-32,32]`；ancestor 全为 p=5；
  [B] 范围。
- **L125-L128**：有限验证范围 `p<=256`、`eta∈[-32,32]`、synthetic lifts at precision `p-1`；
  [B] 范围；4,940/5,345 的数字只在这些范围内。
- **L130-L135**：4 个 forced shifts 是巨大整数（p=64..208，eta 约 2^{p-2}），不是有界高度；
  reachability 未证，因此不能作为 O1 的有界高度反例。
- **文中没有出现** `N0=2·10^7`、`[-12,15]`、`j<2·10^7`、`T_h`、`log* J` 或其数值依赖；
  一般性证明通过 A-SOURCE 的 `p,rho,sigma_C`（无 N0 上界）进行。这是本文的优点，也是它不能
  直接处理 O1/O2 的原因：它没有把实际分母深度/仿射来源带入。
- **隐含的无界量**：`sigma_C=p-1-e-Lambda_source`、`rho`、`p` 都是无界的；terminal `Safe(E,eta)`
  的 `sigma_E` 也无界。文中没有给出这些量的上界，也没有把它们与 J/N0/T_h 比较。

---

## 6. 总评

1. **核心数学是正确的**：§2 的 precision lemma 是 HP 的直接应用；§3 的 A-SOURCE 祖先精度公式、
   c-step 代数、记录恒等式 `Gamma_u+sigma_D=R_T` 均与已接受证明一致；§4 的递归按 source index
   严格下降而终止。补齐 `x_i≠0`、`j_D=j_C`、reference calls defined 后，§2-§4 可作为 [A] 条件归约。
2. **但这不是本轮要的 landing 认证**：`eta=theta_T-2` 是 outer defect shift，不是 c-step 的
   source shift `s=theta_D-2`；本文没有 source-shift 分类 0、±1、4/3，也没有认证 landing 类。
   §4 的 real fire 与 b/c-initial c source 两个 terminal families 仍无界；first A-output 只归约到
   `(z,z+2+eta)` 的 C3 reference（records <P-1），并未对所有 eta 认证。O1 的有理 `eta_r`、
   O2 的 affine/beta、O3 的编码限制均未处理。
3. **有限证据 [B] 太薄**：4 个 AA pair 全部同一个 ancestor p=5、precision 4、全部单状态；
   4,940 个 synthetic reference 中只有 390 个长度>1； “b-reference” 名不符实。这些测试支持
   precision 不等式的首状态，不检验长 tail/mixed history。
4. **文档的自我限定是诚实的**：它明说 “UNREVIEWED conditional lemma”“No new horizon and no global
   EXT conclusion”“This is a uniform reduction, not a proof of those residual families”。这些限定
   应保留；不能把它当作本轮 landing 目标或全局 EXT 的证据。
5. **建议**：以 “条件归约” 接受 §2-§4（补 E3/E4/E5 的假设与 E6/E7/E8/E9 的表述）；
   §4 的 terminal families 和 O1/O2/O3 留给 companion docs（FIRST_A_REDUCTION、RATIONAL_MODE、
   ODD_DENOMINATOR）与后续工作。不能把本文的 “remove” 读成 “close”。

**判定**：`2. with fixable gaps`（条件归约正确，假设/表述需补；不是 landing 或 EXT 证明）。
