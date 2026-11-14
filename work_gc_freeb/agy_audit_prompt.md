# 盲审复算任务：work_gc_freeb（FREE-B 边界 gate 局域化）— 审计员 2（agy gemini-3.8-flash-high）

## 角色与盲审规则
你是独立的盲审复算员。规则：
- **独立重推导**：所有数学断言你必须自己重新推导（手算或用你自己写的脚本），**不得阅读
  work_gc_freeb/verify_freeb.py 与 work_gc_freeb/fb.py 的源码**（它们是被审对象的一部分）。
  你可以读 work_gc_freeb/NOTES.md（被审正文）。
- 你可以用 `C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe` 写自己的复核脚本，
  **只放在 work_gc_freeb/agy_scratch/ 目录内**；其余文件一律只读。
- 从 D:/math_cc 运行：`PYTHONUTF8=1 <解释器> -B <你的脚本>`。
- 可读的已接受仓库文件（只读）：work_claude_cycle/{NOTES.md, cyc.py, branch.py, postgate.py,
  sweep.py, verify_laws.py, seeded.py}（NOTES 头部更正块覆盖正文）、reviews/claude_cycle_review_record.md、
  work_global_ext/PROOF_EXT.md、work_gateway_trains/origin_contraction/PROOF.md、
  work_global_calendar/calendar_oracle.py、CHECKPOINT_1RB1LA_0RC0RD.md 末六节。
  依赖：`sys.path.insert(0, 'work_claude_cycle')` 后 `from cyc import Cal, walk, v2` 可用
  （Cal() 为 Calendar(512) 交叉数据包装）。

## 审查对象
work_gc_freeb/NOTES.md（若其头部更正块与正文冲突，以更正块为准）。核心主张分级：
- **[A] Lemma FB-1（三分分解）**：后置 gate 状态 Θ = 2^(j−2)+3(k+1)+2^(j−1)X、x = 2^m(1+2V)
  （X,V 取遍 Z₂²），沿任意路径 x = C + A·X + B·V 满足 v2(A) = j−ell+L_bc+1（首个 a-步前 A=0，
  该步 A=2^j 精确）、v2(B) = m+1−ell、C = u + β·2^m 且 v2(β2^m) = m−ell。
- **[A] Lemma FB-2（可判定性判据）**：一步的链对所有 (X,V) 固定 ⟺ v2(C) < min(v2(A), v2(B))，
  且等于 v2(C)；否则分裂。
- **[A] Lemma FB-3（边界＝输出相消）**：determined 的 G′ 满足 m′ = v2(C_final) <
  min(j−ell+L_bc+1, m+1−ell)，ΔR = m′+1+ell−j ≤ 1+L_bc（DR′），且
  **边界 ⟺ 2^(j−ell) | C_final**，ΔR ∈ {1,…,1+L_bc}。
- **[A] Theorem FREE-B（三分支穷尽）**：每个边界 gate 恰属 (I) 首着陆逃逸 c₁ ≥ j−1（已接受 FREE
  局域化 j ≤ 3+log2(6mP(m))）；(II) 两步族（显式和 S_a/U_b/U_c 的整除；非零和 + CLOCK/MASS 给出
  j ≤ 2+log2(3mP(m)+3) / 2+log2(21mP(m)+20) / 1+ε₁+log2(30mP(m)+29)；零和＝精确相消）；(III) 深族
  （迭代日历和的整除，可判定，不排除）。成员测试可判定。
- **[A] Lemma FB-4（两步族显式公式）**：(a) C_final = 3S_a + 2^(j−2) + 2^(m−2)，
  S_a = k+3+3k_m+2k_{c₁}；(b) C_final = 2^(j−1) − 3·2^(m−3) + U_b/2，U_b = 12k+12k_{c₁}+9τ_m+20；
  (c) 2C_final = 2^j + U_c − R_c·2^m，U_c = 12(k+τ_m+k_{c₁}+2) − λ′_c；边界等价于相应整除
  （(a) 2^(j−2)|S_a；(b) 2^(j−2)|U_b；(c) 2^(j−1−ε₁)|U_c）；(a) 的奇偶刀口（u = S_a/2^(j−2)
  偶＝determined 且 m′=j−2、ΔR=1；u 奇＝该步分裂）。
- **[A] Prop FB-5（CL2 归结）**：在 L′ 环境中（gate 输出 ≤ g、b/c 交叉 ε < 2⌈log2(3g²+4)⌉），
  阈值 B*(g) = 2+log2(30gP(g)+29)+2⌈log2(3g²+4)⌉ 的 CL2 成立 ⟺ 无 j > B*(g) 的 gate 具有
  (α) 后置树分裂且逃逸分支到达真 NT gate、(β0) 两步零和边界、(γ) 深族边界。
- **[B] 数据**（NOTES §6 所列精确范围）：反例 A/B/B2 的精确核验、seeded 新实例、普查零边界实例
  等范围性陈述。

## 逐项复核清单（每项独立做，注明你用了什么方法）
1. **FB-0/FB-1 重推导**：用 PROOF_EXT §2 的步规则（a: x′=2Θ+6k−x/2；b/c: x′=Rx+λ′, v2(R)=−1−ε）
   手推 v2(A)、v2(B) 的递推，验证首 a-步 A=2^j 精确、其后每 a-步降 1、b/c 降 1+ε。
2. **FB-2 重推导**：证明 v2(C) < min 系数赋值 ⟺ 输出赋值恒定；等赋值时给出 (X,V) 使其变化的显式
   选择。与 branch.py 的 `vc < vs` 分裂规则对照。
3. **FB-3 重推导**：由 FB-1/FB-2 推出 ΔR ≤ 1+L_bc 与 边界 ⟺ 2^(j−ell)|C_final。
4. **FB-4 重推导**：对三种首步类型各算两步，验证 C_final 的显式公式；再验刀口奇偶论断
   （含 m=j 情形）。
5. **独立计算复核（自写脚本）**：
   a. 用 cyc.Cal 自建一对 (Θ, x) 的精确走步器，重放 NOTES §6 的反例 A（j=24, m=6268562：走步
   24→m→5，5 处 gate 输出 22，ΔR=1，S_a=2^23）与 B（j=42, m=1095510131453：5 处 gate 输出 41，
   ΔR=3，U_b=8796093022208，v2=43）。B 的 m 巨大：用 mod-2^P（P≈200）重放（真 x = 2^m(1+2V) 取
   V=0，x ≡ 0 mod 2^P；每次读链须 < live−8）。
   b. 抽样验证 FB-1/FB-2/FB-3 于若干 (j,m)（如 j<40 奇 a、m<j+200 内全部 determined gate 对）。
   c. 验证 seeded 新实例之一（如 j=61: m=2584632671144439708, m′=59, ΔR=1）与 razor 实例
   （j=24, k_m=6990502, m=15671400：v2(S_a)=22=j−2 恰好、u 奇 ⟹ 该步应分裂）。
   d. 核对普查断言：j<400 奇 a、j≤m<5000、X(m−1) 奇 的对中 1,474 个 determined gate 全部
   ΔR ≤ 1+L_bc 且无一为边界实例；首着陆逃逸（c₁ ≥ j−1）只出现在 j∈{5,8,12} 且各处 FREE 同余成立。
   e. （第 1、2 轮修补后新增的可核验点）(i) j=24 的 type-b 两步族空性论证：U_b 类
   9τ ≡ −140 (mod 2^22) 固定 τ mod 2^8 ⟹ ω=v2(3τ+4) 在全类上恒为 7，且 X(6) 为偶 ⟹ 着陆 7 处
   无 a-步；前 200 个类标签 kk=466026+i·2^21 逐一实现（首例 m=1,044,747），全部 ω=7（空性论证
   不依赖 realization）。
   (ii) type-c 闭式在构造对 (m=6133, ω=5, ε=3) × j∈{24,42,61,97,152,186,239,275} 上成立
   （普查盒内 type-c 两步对数为 0，首例 m=6133>5000）。(iii) FB-2 分裂方向与已接受 branch.py
   引擎的一致性：对 j<60、m<300 的泛型后置起点，branch.explore(min_bits=0) 单叶状态
   （GATE/END/CUT_BITS）应与 det_walk 的 GATE/END/SPLIT 三向一一对应，且 GATE 词与 CUT 前确定
   前缀逐字一致。(iv) FB-0 测度表述：条件柱 {v2(y)=m} 的 Haar 测度为 2^−(m−j+1)，双射到
   Z₂×Z₂^×（下游只用定性双射）。
6. **CL2 归结核对**：检查 FB-5 证明中阈值不等式链（3+log2(6gP) ≤ B*、2+log2(21gP+20) ≤ B*、
   1+ε₁+log2(30gP+29) ≤ B* 在 ε₁ < 2⌈log2(3g²+4)⌉ 下）对 g ≥ 5 是否成立（可数值抽查大 g）。
7. **范围核查**：NOTES §6/§7 所报的范围（j<400、m<5000 普查；j<3000/深度 3000 sweep；400 步上限）
   与 freeb_checks.json（可读）是否一致；普查"零边界实例"是否与 FB-4 的同余类分析一致
   （j=24 的 a 类首个实现 m=6268562>5000 等）。
8. **越级检查**：NOTES 是否声称了 FREE-EXIT 闭合、G1 闭合、EXT 新范围或不停机（不应有）。

## 输出
用中文写审查报告到 `reviews/gc_freeb_auditor2_agy.md`：逐项列出你的独立推导/计算与结论
（给出你的脚本路径与关键输出行），指出任何错误或可修补缺口。最后一行恰为：
`VERDICT: 1`（全部正确）/ `VERDICT: 2`（有可修补缺口）/ `VERDICT: 3`（结构性破坏）。
