已通过三方审查 / accepted (reviews/deep_review_record.md) — work_deep: structure of the deep segment of S(J), and a sharper remainder for DEEP (ZCode, 2026-10-19)

## 中文摘要

本笔记研究 BB(6) holdout #1 的全局不停机证明中最后一个充分条件 **DEEP**（work_claude_shifted/NOTES.md §6）。
符号沿用 PROOF_EXT §2（walk rules）、PROOF_EL A1–A3（θ̃ 自动机）、PROOF_M Lemma 6.1、work_claude_shifted
（SC、HP、证书）。**没有证明 EXT，没有改变 K_clock，没有声称全局不停机。**

主要结果（每条标注 [A] 全参数证明 / [B] 有限精确计算 / [C] 猜想·数据）：

1. **深段三分法 [A]**。令 N₀=2·10⁷、B=2^{N₀/2}=2^{10⁷}、κ(j)=(3/2)(j−1)P(j−1)（P 来自 PROOF_CLOCK）。
   若链 t 的参数 j_t ≥ N₀ 且 |θ_t| ≤ B（θ_t 取 mod 2^{j_t} 的对称代表元），则 |3k_{n_t}+θ_t| ≤ κ(j_t)+B < 2^{j_t−2}，
   故 **无 NT 失败**；该步恰为：终止 / 共振 a（z=0，j′=j−1，θ′=3−θ，记录不变）/ 非共振 a
   （j′=1+v₂(z)≤1+⌊log₂|z|⌋≤1+⌊log₂(κ+B)⌋，θ′=3−θ，记录严格下降）/ b（θ′=θ−1，记录严格下降）/ c（θ′=θ+Φ−2，记录严格下降）。
2. **共振孤立 [A]**：共振步之后的一步必非共振（θ′=3+3k>0，且下一步的 z>0）。因此深段链数
   ≤ 2Λ(J)+1（Λ 为到 N₀ 的迭代对数深度），这补上了 Lemma 6.1 "log\* 计数" 未计共振的缺口。
3. **着陆亏损类已知 [A]**：沿深段每一步，精确亏损 D_t 已知模 2^{j_t+1}（共振时提升位为 3−θ−2^{j′}，
   由 x/2=2^{j−1}u、u 奇得到）。因此**着陆链（第一个参数 < N₀ 的链）的亏损类 mod 2^{j+1} 是显式确定的**：
   a: 3−θ；b: θ−1；c: θ+Φ−2。
4. **DEEP(i) 锐化 [A]**：a 步改变 |θ| ≤ 3、b 步 ≤ 1、c 步 ≤ 3τ+7；深段链数 ≤ 2Λ+1。故
   **在 6Λ+4 ≤ B 时，初始深段上的 DEEP(i)（|θ|≤B）只可能在一个"深→深 c 步"处失败，
   而"无深→深 c 步"蕴含初始深段上的 DEEP(i)**（ω(j_t−1) ≥ N₀，即 τ(j_t−1) ≥ (2^{N₀}−5)/6）。
   由 L(j) ≤ max(2log₂j+3, 10⁷+2)，6Λ+4 ≤ B 对 J < T_{⌊(B−4)/6⌋} 成立（T_h 见 Lemma 2.4，塔高约 2^{10⁷}/6）[A]；
   特别地 Λ(K_clock)=4，6Λ+4=28 ≪ B。在 R1（无深→深 c 步）下，深段亏损满足 |θ| ≤ 6Λ+4，
   且 a/b 着陆的亏损 δ 满足 |δ| ≤ 6Λ+7（显式小量，不再是 2^{10⁷}）。
5. **着陆判据的极限 [C]（备注，未证明）**：HP 的精度受 x 侧限制——真实状态与代表元之差
   δx₀=2^{j_u}(u−1) 的 v₂ = j_u+v₂(u−1) ≥ j_u+1（u 奇），而缺陷精度可以更大。因此不能直接用
   "参考走步记录 < p（p>j_u+1）"来弱化证书。"类内走步发散"与"证书是最强统一判据"未经证明；
   已知的例子是裸 tie (5,5)，其结果由高位决定（work_claude_shifted Cor 3.1 / SC）。
6. **DEEP(ii) 锐化 [B]**：穷举 j ≤ 24 的全部剩余类（j=25,26,27 另见补充）：在 18 ≤ j ≤ 27 中，
   证书失败集 Bad_j 仅在 odd-a 参数 j=22,24,27 非空，且**恰等于首链 tie 类**（各 4 个剩余类 mod 2^{j+1}）；
   其余（非 odd-a）j 的 Bad_j=∅。j=17 为 8 个（4 tie + 4 个 (5,5)-预像）；j=5,8,12,14 各 4 个。
   因此**仅在 18 ≤ j_u ≤ 27（穷举）**、且 X(j_u−1) 为奇 a 型时，DEEP(ii) 等价于**单个同余**
   `3k_{j_u−1}+δ ≢ 2^{j_u−2} (mod 2^{j_u−1})`（着陆链不 tie）；X(j_u−1) 非奇 a 时 DEEP(ii) 在此范围自动成立。
   对 28≤j≤80 的随机大亏损（≤2^{10⁷}）样本与 (5,5)-预像构造未发现反例 [C-support]（不是穷举）。
   对 j < 2·10⁷ 的窗口 δ∈[−12,15] 结果是"除裸 tie (5,5),(5,−11) 外全部证书通过"，不是一个同余。
7. **数据 [B]**：规范表到 10⁸。随机深步（j∈[N₀,10⁸)，a/b/c 三类，|d|≤2^{10⁷}）：**证书失败数 = 首链 tie 数**
   （a: 11/4800, b: 17/4800, c: 0/4800；无其他失败）；深段大小不等式在全部 24,230,413 个 odd-a 交叉上成立；
   400 个强制共振的下一步均非共振型 a 步，112 个着陆全部证书通过；精确大整数走步验证 Lemma 2.5 的公式（36 例）；
   构造的"tie 着陆"（m=5,8,14,17）证明 DEEP(ii) 确实可能失败（是真实同余，不是自动成立）。
8. **剩余 [A] 归约**：对每个满足 6Λ(J)+4 ≤ B 的 J（[A] 范围：J < T_{⌊(B−4)/6⌋}，含 J=K_clock 附近，见 Lemma 2.4），
   EXT(J) ⟸ **R1**（无深→深 c 步）∧ **R2**（着陆类满足证书）。在此范围之上 DEEP(i) **没有被归约**，仍是假设
   （最小反例只知 J ≥ K_clock，无上界）。R2 在 18 ≤ j_u ≤ 27 且 X(j_u−1) 奇 a 时等于上面的单个同余（非奇 a 时自动成立）；
   j_u ≤ 17 时是显式的 ≤8 个类之一；更大 j_u 只有抽样/窗口支持。R1/R2 都是深部日历算术，**没有证明**。
   另注意：本文的归约只是充分条件——未认证类中的结果可能依赖 λ_u（类外高位，见 Remark 3.2 [C]），
   故证书失败不等于 EXT-tie；更正确的目标仍是"记录 < 精度"。

Tags: [A] all parameters (hypotheses stated), [B] finite exact computation (range stated), [C-support] sampled
(non-exhaustive) evidence, [C] conjecture/data/unproved remark.

---

# 1. Setting and the exact statements

Notation as in PROOF_EXT §2 and work_claude_shifted §1–§3. For J ≥ 2 the symbolic exit S(J) has chains
t = 0,1,…,r (chain 0 = the fire), parameters j_t, loss Γ_t, record r_t := j_t+Γ_t, j₀ = J, Γ₀ = 0,
defect automaton value θ_t (θ₀ = 1). Chain t reads X(n_t), n_t = j_t−1. The step is:

* X(n_t) even: S(J) ends at chain t;
* type a, τ(n_t)=2k: z_t := 3k+θ_t. If v₂(z_t) = j_t−2, a **non-descent** (NT failure; j_{t+1} ≥ j_t−1,
  and ≥ j_t when the odd part forbids j_t−1); if v₂(z_t) ≥ j_t−1, a one-step descent j_{t+1} = j_t−1
  (z_t = 0 in the deep regime); otherwise j_{t+1} = 1+v₂(z_t). In all cases θ_{t+1} ≡ 3−θ_t
  (mod 2^{j_{t+1}}), and D_{t+1} ≡ 3−θ_t−2^{j_{t+1}} (mod 2^{j_{t+1}+1}) at a one-step descent;
* type b: j_{t+1} = ω(n_t), θ_{t+1} = θ_t−1, ε = 1;
* type c: j_{t+1} = ω(n_t), θ_{t+1} = θ_t+Φ(n_t)−2, Φ = 3τ+5−λ′_W = 1−λ_Y, ε = ε(n_t) ≥ 1;
* Γ_{t+1} = Γ_t+1+ε(n_t), ε = 0 for type a, ε(n) = n−v₂(c′_W(n)) for b/c (so v₂(c′_W) = n−ε).

An **EXT-tie** at chain t ≥ 1 is r_t ≥ J (the HP comparison v₂(β_{x_t}) ≥ v₂(α_{x_t}) = J−Γ_t is not
strict). EXT(J) = no EXT-tie. A non-descent is not an EXT-tie; it is the only step that can raise a record.

**DEEP (work_claude_shifted §6)**: (i) every chain with parameter ≥ N₀ := 2·10⁷ has |θ̃| ≤ 2^{10⁷};
(ii) the first chain with parameter < N₀ has its exact defect mod 2^{j+1} certified. DEEP ⇒ EXT(J) was
proved there from Theorem SC + Prop 3.2. Below, for J with 6Λ(J)+4 ≤ B, (i) is reduced to one forbidden
event, and (ii) to one congruence for 18 ≤ j_u ≤ 27 at odd-a X(j_u−1) (exhaustive), with sampled support beyond.

**Standing imports [A, accepted].** (CLOCK) τ(n) ≤ nP(n), P(n) = 2⌈log₂(6n²+5)⌉²+1345, at every reached
canonical crossing (PROOF_CLOCK §3–4; base τ(n) ≤ n for n ≤ 10⁸). (S1/S2) the walk rules of
PROOF_EXT §2. λ-mass: λ_Y ≤ 3τ+1 at every type-c crossing (used in PROOF_EXT §3; checked on the table
in V0). The λ-only table of work_global_ext/route_c/fdata.py is the canonical crossing data.
On the table to 2·10⁷: λ_Y ≤ 3τ+1 holds at every odd type-c crossing (0 violations, equality attained),
and ω < v₂(c′_W) = n−ε holds at every odd b/c crossing with n < 1024.

# 2. The deep segment [A]

Put N₀ = 2·10⁷, B = 2^{N₀/2} = 2^{10⁷}, κ(j) = (3/2)(j−1)P(j−1). Chain t is **deep** if j_t ≥ N₀ and
|θ_t| ≤ B (θ_t the symmetric representative mod 2^{j_t}).

**Lemma 2.1 (size) [A].** For every integer j ≥ N₀: B + κ(j) < 2^{j−3}.

*Proof.* B = 2^{10⁷} = 2^{N₀/2} ≤ 2^{N₀−4} ≤ 2^{j−4}. For κ: by
g(n) = ⌈log₂(6n²+5)⌉ ≤ 2log₂n+4 (PROOF_CLOCK; the constant +3 is false, e.g. n ≈ 1.155·2^m),
P(n) ≤ 2(2log₂n+4)²+1345, so κ(j) ≤ (3/2)j(2(2log₂j+4)²+1345) = 12j(log₂j+2)²+2017.5j
≤ 15j(log₂j)²+2018j for j ≥ 2^{20} (as (x+2)² ≤ 1.21x² for x ≥ 20).
At j = N₀ (log₂N₀ ≈ 24.25) the right side is ≈ 2.2·10¹¹ < 2^{40} < 2^{N₀−4}; and the ratio
2^{j−4}/(15j(log₂j)²+2018j) has logarithmic derivative ≥ ln2 − 1/j − 2/(j ln j) > 0 for j ≥ 8, so
κ(j) < 2^{j−4} for all j ≥ N₀. Hence B+κ(j) < 2^{j−3}. ∎ (V0/V6-D check the numerical form at every odd-a crossing in [N₀,10⁸): the worst
bit length of 3k is 27, the minimum slack j−2−bitlen(3k) is 19,999,973.)

**Lemma 2.2 (deep trichotomy; no non-descent) [A].** Let chain t be deep. Then |3k_{n_t}+θ_t| ≤ κ(j_t)+B < 2^{j_t−2},
and:
1. X(n_t) even ⇒ S(J) ends at chain t;
2. type a: v₂(z_t) ≠ j_t−2. If z_t = 0 then j_{t+1} = j_t−1, θ_{t+1} = 3−θ_t, r_{t+1} = r_t. If z_t ≠ 0 then
   j_{t+1} = 1+v₂(z_t) ≤ j_t−2, θ_{t+1} = 3−θ_t, r_{t+1} ≤ r_t−1;
3. type b/c: j_{t+1} = ω(n_t) ≤ log₂(6τ(n_t)+5) < j_t−2, θ_{t+1} = θ_t−1 (b) or θ_t+Φ−2 (c), and
   r_{t+1} ≤ r_t−1.

*Proof.* 3k_{n_t} = 3τ(n_t)/2 ≤ 3n_tP(n_t)/2 = κ(j_t) by CLOCK; Lemma 2.1 gives |z_t| < 2^{j_t−2}. If
v₂(z_t) = j_t−2 then j_t−2 ≤ log₂|z_t| < j_t−2, a contradiction, so no non-descent. z_t ≠ 0 ⇒
j_{t+1} = 1+v₂(z_t) ≤ 1+log₂|z_t| ≤ j_t−2, and j_{t+1}+Γ_{t+1} = j_{t+1}+Γ_t+1 ≤ j_t−2+Γ_t+1 = r_t−1.
For b/c: λ′_W = 3τ+4 (b) or 3τ+4+λ_Y ≤ 6τ+5 (c), so ω = v₂(λ′_W) ≤ log₂(6τ+5) ≤ log₂(6(j_t−1)P(j_t−1)+5) < j_t−2
(the last step is the same estimate as Lemma 2.1). S1 of W's chain gives ω < v₂(c′_W) = n−ε, hence
j_{t+1} = ω ≤ j_t−2−ε and r_{t+1} ≤ j_t−2−ε+Γ_t+1+ε = r_t−1. z_t = 0 is PROOF_EL A2 / Lemma 1.3 of
work_claude_shifted. ∎

**Lemma 2.3 (resonance isolation) [A].** If chain t is deep and z_t = 0, then θ_{t+1} = 3−θ_t = 3+3k_{n_t} ≥ 6,
and if chain t+1 is deep then its step either ends, is b/c, or is an a-step with z_{t+1} > 0. Hence two
consecutive deep one-step descents are impossible.

*Proof.* k_{n_t} = τ(n_t)/2 ≥ 1 (n_t ≥ N₀−1 and an odd-a crossing has τ ≥ 2). For an a-step at chain t+1:
z_{t+1} = 3k_{n_{t+1}}+θ_{t+1} ≥ 3+6 > 0. ∎

**Lemma 2.4 (deep chain count) [A].** Let L(j) := max(1+⌊log₂(κ(j)+B)⌋, ⌊log₂(6(j−1)P(j−1)+5)⌋).
L is non-decreasing and L(j) < j for j ≥ N₀. Every deep chain, or every pair of consecutive deep chains
whose first is a one-step descent, has its parameter drop to ≤ L of the parameter at the start of the pair.
Hence the number of deep chains is at most 2Λ(J)+1 with Λ(J) := min{h : L^{(h)}(J) < N₀}.

*Proof.* At a non-resonant a-step j_{t+1} = 1+v₂(z_t) ≤ 1+⌊log₂|z_t|⌋ ≤ 1+⌊log₂(κ+B)⌋ (note: not
≤ log₂(κ+B); z = 2^m is a counterexample to that); at b/c, j_{t+1} = ω ≤ ⌊log₂(6τ+5)⌋ ≤ ⌊log₂(6(j_t−1)P(j_t−1)+5)⌋.
So j_{t+1} ≤ L(j_t) at non-resonant steps; Lemma 2.3 gives j_{t+1} = j_t−1, j_{t+2} ≤ L(j_t−1) ≤ L(j_t)
after a resonance (L monotone since κ and P are). L(j) < j: 1+log₂(κ+B) < j−2 by Lemma 2.1, and
log₂(6(j−1)P(j−1)+5) < j−2. The count is the number of L-iterations to fall below N₀. ∎

**Size of Λ [A].** At n = N₀−1, g(n) = 52 and P(n) = 2·52²+1345 = 6753 < n; since P(n) = O(log²n),
P(n) ≤ 2(2log₂n+4)²+1345 ≤ n for n ≥ N₀−1, by the same log-derivative argument as in Lemma 2.1 (P itself is a step
function, so P(n)/n is not literally monotone), so P(j−1) ≤ j−1 for all j ≥ N₀. Hence κ(j) ≤ (3/2)(j−1)² and 6(j−1)P(j−1)+5 ≤ 6j²+5 ≤ 7j², so
⌊log₂(6(j−1)P(j−1)+5)⌋ ≤ 2log₂j+3; and 1+⌊log₂(κ+B)⌋ ≤ 2+max(log₂κ, 10⁷) ≤ max(2log₂j+3, 10⁷+2). Thus
  L(j) ≤ G(j) := max(2log₂j+3, 10⁷+2)   (j ≥ N₀),
with 10⁷+2 < N₀. Define reals T₁ := 2^{(N₀−3)/2} = 2^{10⁷−3/2}, T_{h+1} := 2^{(T_h−3)/2}, so that
2log₂J+3 < T_h ⇔ J < T_{h+1}. By induction on h, **Λ(J) ≤ h for all J < T_h**: for N₀ ≤ J < T₁, G(J) < N₀;
for N₀ ≤ J < T_{h+1}, L(J) ≤ G(J) < max(T_h, N₀), so Λ(J) ≤ 1+Λ(L(J)) ≤ h+1. Consequently
**6Λ(J)+4 ≤ B holds for every J < T_{h*}, h* := ⌊(B−4)/6⌋** (a tower of height ≈ 2^{10⁷}/6) [A].
Above that range Λ is not bounded here.
At J = K_clock = ⌊2^{K′}/(64K′²)⌋, K′ = 2^{2^{2^{499997}−3}−2}: log₂K_clock ≈ K′. One computes
T₃ = 2^{2^{2^{10⁷−5/2}−5/2}−3/2} and log₂T₄ = T₃/2−3/2. Comparing with log₂K_clock ≈ K′ at matching
heights (2^{10⁷−5/2} ≪ 2^{2^{499997}−3}, while 2^{10⁷−5/2} ≫ 2^{499997}) gives T₃ < K_clock < T₄, so
Λ(K_clock) ≤ 4. Conversely L(j) ≥ ⌊log₂(6(j−1)P(j−1)+5)⌋ ≥ log₂j, and three iterations of log₂ from
K_clock give ≥ 2^{499997}−O(1) ≥ N₀, so **Λ(K_clock) = 4** and 6Λ+4 = 28. Heuristically
J → ≈K′ → ≈2^{2^{499997}−3} → ≈2^{499997} → ≈499997 < N₀ (up to factors 2 from L ≈ 2log₂). (An earlier draft
quoted Λ ≈ 5·10⁵, confusing the exponent 499997 with a tower height.) Since a least counterexample is only
known to satisfy J ≥ K_clock, with no upper bound, the range J < T_{h*} does not cover all candidates.

**Lemma 2.5 (defect precision; the landing class is known) [A].** Along a deep segment, at every chain
the exact defect D_t is known modulo 2^{j_t+1}:
 * t = 0: D₀ = 1 (exactly);
 * non-resonant a-step: D_{t+1} ≡ 3−θ_t (mod 2^{j_{t+1}+1});
 * resonant a-step: D_{t+1} ≡ 3−θ_t−2^{j_{t+1}} (mod 2^{j_{t+1}+1});
 * b/c-step: D_{t+1} ≡ θ_t+Φ(n_t)−2 (mod 2^{j_{t+1}+1}).
In particular the landing chain u (first with j_u < N₀) has a fully determined class δ = D_u mod 2^{j_u+1}.

*Proof.* a-step: x′ = 2(D+3k)+3·2^{j−1}u with u odd (derivation in PROOF_EXT §2); so x′/2^{j−1} is odd and
D′ = 3−D−x/2 ≡ 3−D−2^{j−1} (mod 2^j). If j′ ≤ j−2 then j′+1 ≤ j−1 and D′ ≡ 3−D (mod 2^{j′+1}); if
j′ = j−1 then the modulus is 2^{j′+1} = 2^j and the lift bit is −2^{j−1} ≡ +2^{j−1} (mod 2^j). In both
cases D mod 2^{j′+1} is known by induction (only θ_t mod 2^{j_t} is used, and j′+1 ≤ j_t).
b/c-step: D′ = D+Φ−2+u(2^j−c′_W) and v₂(2^j−c′_W) = v₂(c′_W) = σ ≥ j′+1 by S1, so D′ ≡ θ_t+Φ−2 (mod 2^{j′+1}). ∎

**Lemma 2.6 (drift) [A].** Along a deep segment the symmetric representatives satisfy |θ_{t+1}| ≤ |θ_t|+3
(a-step), |θ_t|+1 (b-step), and |θ_{t+1}| ≤ min(|θ_t|+3τ(j_t−1)+7, 2^{j_{t+1}−1}) (c-step). Hence
|θ_t| ≤ 1+3(#a)+(#b) ≤ 6Λ(J)+4 at every deep chain, provided no c-step occurs on the deep segment.

*Proof.* θ′ = 3−θ, θ−1, θ+Φ−2 with |Φ| ≤ 3τ+5, and the symmetric residue is taken mod 2^{j_{t+1}}.
Use Lemma 2.4 for the number of steps. ∎

**Corollary 2.7 (DEEP(i) on the initial deep segment can fail only at a deep→deep c-step) [A].** Suppose
6Λ(J)+4 ≤ B (e.g. J < T_{h*}, Lemma 2.4; in particular J near K_clock, where Λ = 4). Let the *initial deep
segment* be chains 0,…,t with j_0,…,j_t ≥ N₀, up to the landing chain u = t+1. Then:
 * if no c-step at a deep chain keeps the walk deep (i.e. every deep c-step has ω(j_t−1) < N₀), then
   |θ| ≤ B at every chain of the initial deep segment;
 * conversely, if |θ| > B at some chain of the initial deep segment, then some c-step at a deep chain has
   ω(j_t−1) ≥ N₀.
(DEEP(i) itself quantifies over all chains of S(J); after the landing a non-descent could lift the
parameter back to ≥ N₀, which this corollary does not control. Theorem 3.4 is unaffected: there R2 keeps
all later records, hence parameters, ≤ j_u < N₀.)

*Proof.* A/b steps change |θ| by ≤ 3 and there are ≤ 2Λ+1 deep steps, so their total displacement is
≤ 6Λ+4 ≤ B (Lemma 2.6); c-steps with j_{t+1} ≤ 10⁷+1 give |θ_{t+1}| ≤ 2^{j_{t+1}−1} ≤ B automatically; and
a violation |θ_{t+1}| > B at a chain with j_{t+1} ≥ N₀ can only be produced by a c-step, since the other
cases were just bounded. ∎

*(Consequently, if the whole deep segment consists of a/b steps (no c-step at all, in particular no
c-entry), then the landing defect is |δ| ≤ 6Λ+7, i.e. |δ| ≤ 31 at J = K_clock (Λ = 4). A
c-landing has δ = θ+Φ−2 with |Φ| ≤ 3τ(j_t−1)+5, which is not bounded by the deep structure.)*

*Remark 2.8 [C] (reviewer's unverified observation, not claimed by this note; future work only).* With Λ this
small, under R1 a resonance (z_t = 3k+θ_t = 0 with |θ_t| ≤ 28 and k = τ/2 large at deep crossings) appears
impossible, and a refined drift count would put a/b landings in the certified window δ ∈ [−12,15] of
work_claude_shifted §4, where everything certifies except the bare ties (5,5), (5,−11). This suggests
R2 may be automatic for a/b landings away from those ties. Neither the lower bound on k nor the refined
drift count is proved here (the crude bound above gives only |δ| ≤ 31).

# 3. The landing: what the class suffices for [A]

Let chain t be the last deep chain, chain u = t+1 the landing chain, Γ_u = Γ_t+1+ε_t, δ = D_u mod 2^{j_u+1},
p := the defect precision at u produced by Lemma 2.5 (p ≥ j_u+1). The deep segment is finite and the
parameter strictly decreases on it (Lemma 2.2), so if S(J) does not end on it, the landing chain exists.

**Lemma 3.1 (precision budget) [A]; assumes t ≥ 1.** If the last deep chain is t ≥ 1, then at the landing
chain u one has p ≤ j_t if the landing step is an a-step, and p ≤ σ_t ≤ j_t−1−ε_t if it is a b/c step. In
both cases p ≤ J−Γ_u. (For t = 0 it fails: r₀ = J, and a non-resonant landing has p = J > J−Γ_u. The lemma
is not used below.)

*Proof.* Chain t ≥ 1 is deep and hence tie-free (Lemma 2.2), so j_t+Γ_t ≤ J−1. For an a-step Γ_u = Γ_t+1 and
p ≤ j_t = J−Γ_u; for b/c, p ≤ σ_t and J−Γ_u = J−Γ_t−1−ε_t ≥ j_t−ε_t ≥ σ_t.∎

**Theorem 3.1 (landing criterion) [A].** If certify(j_u, δ) holds (the exact walk from the representative
(2^{j_u}, 2^{j_u}+δ) ends with all records ≤ j_u), then every chain of S(J) at and after u has record < J;
in particular S(J) has no EXT-tie there.

*Proof.* HP (PROOF_EXT §2) with precision P = j_u+1: δΘ₀ and δx₀ between the true state and the
representative have valuations ≥ j_u+1 (δx₀ = 2^{j_u}(u−1) with u odd, δΘ₀ = δx₀+(D_u−δ) with
D_u ≡ δ mod 2^{j_u+1}). While the reference records are ≤ j_u they are < P, so the walks agree and the
true records (in S(J)'s accounting) are ≤ j_u+Γ_u = r_u ≤ r₁ < J. ∎ (This is Prop 3.2 of work_claude_shifted in the landing language.)

**Remark 3.2 (the extra defect precision does not obviously help) [C].** It is tempting to use p > j_u+1 and
require only "reference records < p". HP as stated does not justify this: HP needs
min(v₂δΘ₀, v₂δx₀) ≥ P, but the true x-coordinate is known only through its parameter, i.e.
δx₀ = 2^{j_u}(u−1) has v₂ = j_u+v₂(u−1) ≥ j_u+1, and u is an arbitrary odd integer (it depends on the fire
base λ_u). So the guaranteed x-side precision is j_u+1. That class-mates with different u actually have
diverging walks after a tie, and that the certificate with threshold j_u is the strongest λ_u-uniform
criterion, are **not proved** here. The known instance is the bare (5,5) tie, whose outcome is decided by
higher bits of z (work_claude_shifted Theorem SC / Cor 3.1). (A different and genuinely
additional resource is the *predecessor* data: the gateway lemma of work_claude_shifted §5 resolves a tie
at j=5 by a two-step identity, with a net record descent. That handles some of the certificate failures,
it does not weaken the certificate itself.)

**Corollary 3.3 (what DEEP(ii) is, in the verified ranges) [A+B].**
1. If j_u ≥ 18 and j_u ≤ 27, Bad_{j_u} is *exactly* the four first-chain tie classes
   δ ≡ 2^{j_u−2}−3k_{j_u−1} (mod 2^{j_u−1}) when X(j_u−1) is odd of type a, and empty otherwise
   (j ∈ {22,24,27}: four each; j ∈ {18,19,20,21,23,25,26}: empty). Hence, for 18 ≤ j_u ≤ 27 with X(j_u−1)
   odd of type a, DEEP(ii) ⇔ the landing chain is not a first-chain tie, a **single congruence**; for the
   other j_u in this range DEEP(ii) holds automatically.
2. For 28 ≤ j ≤ 80, sampling 30,000 random (j,δ) with |δ| up to 2^{10⁷} found 35 non-descents, all at
   later chains, and **zero** certificate failures other than first-chain ties; all ten (5,5)-preimage
   classes at deep j ≤ 400 (k_{j−1} ≡ 6 mod 16) are non-descents and all certify. This is sampled support
   [C-support] for the equivalence of item 1 at 28 ≤ j ≤ 80, not an exhaustive check; it is a conjecture
   for larger j [C].
3. For 5 ≤ j < 2·10⁷ and δ ∈ {0,1,2,3}, certify holds (V3: 0 failures in 4·(2·10⁷−5) exact walks).
4. For 5 ≤ j < 2·10⁷ and δ ∈ [−12,15] the window certificate of work_claude_shifted §4 holds
   (1,116,395 NT-failing pairs) **except the bare ties (5,5),(5,−11)**. This is a certification statement
   for a window, not a congruence.
5. For j ≤ 17 the Bad sets are explicit and finite: Bad₅ = {5,21,−11,−27} mod 64; Bad₈ = {58,186,−198,−70}
   mod 512; Bad₁₂, Bad₁₄ four classes each; Bad₁₇ = the four tie classes ∪ four (5,5)-preimages
   (the classes δ ≡ δ_tie+16 mod 32, numerically δ_tie∓48 for j=17).

**Theorem 3.4 (DEEP′ ⇒ EXT) [A].** Let J satisfy 6Λ(J)+4 ≤ B — by Lemma 2.4 this holds for every
J < T_{h*}, h* = ⌊(B−4)/6⌋, in particular at J = K_clock (Λ = 4). Let DEEP′(J) be
 (R1) no c-step at a chain with parameter ≥ N₀ keeps the walk deep (Corollary 2.7), and
 (R2) the landing class (j_u, δ) satisfies certify(j_u, δ).
Then EXT(J) holds. **Scope:** a least counterexample is only known to satisfy J ≥ K_clock, with no upper
limit; for J ≥ T_{h*} (where 6Λ(J)+4 ≤ B is not established) DEEP(i) is **not** reduced by this note and
remains a hypothesis.

*Proof.* Corollary 2.7 gives |θ| ≤ B on the initial deep segment, which is tie-free with non-increasing
records ≤ r₁ < J (Lemma 2.2; r₁ < J as in work_claude_shifted §6). Lemma 2.5 gives δ, and Theorem 3.1
(with R2) gives records ≤ r_u < J from the landing on; in particular every later parameter is ≤ j_u < N₀,
so DEEP(i) holds on all of S(J).∎

**What changed relative to DEEP.** For J with 6Λ(J)+4 ≤ B, DEEP(i) on the initial deep segment was a
drift bound; it is now one forbidden event (a deep→deep c-step). DEEP(ii) was "the class is certified"; it
is now the same certificate but with the class *proved* to be known (Lemma 2.5). For 18 ≤ j_u ≤ 27 with
X(j_u−1) odd of type a (j_u ∈ {22,24,27}) it is exhaustively a single congruence at the landing chain
(automatic for the other j_u in 18..27); j_u = 17 has 8 bad classes (4 ties + 4 (5,5)-preimages), and
j_u = 5,8,12,14 have 4 each. For 28 ≤ j_u ≤ 80 the congruence form has sampled support only [C-support].
For j_u < 2·10⁷ the window result is "δ ∈ [−12,15] certifies except the bare ties (5,5),(5,−11)", not a
congruence. For an a/b entry whose deep segment contains no c-step at all, the landing defect is ≤ 6Λ+7.

# 4. What remains; why it is still deep arithmetic [C]

**R1.** A c-step at a deep chain with ω(j_t−1) ≥ N₀. By λ′_W = 3τ+4+λ_Y (type c; Lemma 2.2, ENTRY) this is
v₂(3τ+4+λ_Y) ≥ N₀, so 3τ+4+λ_Y ≥ 2^{N₀}; with λ_Y ≤ 3τ+1 this gives 6τ+5 ≥ 2^{N₀}, i.e.
τ(j_t−1) ≥ (2^{N₀}−5)/6. Since τ(n) ≤ nP(n), this needs j_t ≳ (2^{N₀}−5)/(6P(j_t)),
so R1 is vacuous for J < 2^{N₀}/poly but not at a least counterexample J ≥ K_clock = 2^{K′}/poly with
K′ = 2^{2^{2^{499997}−3}−2}.
No structure in the accepted corpus bounds λ_Y or v₂(3τ+4+λ_Y) from above; λ_Y is the pending entry's
λ-part at a deep type-c crossing, i.e. exactly the kind of deep calendar quantity that PROOF_EXT §5
identifies as the open core.

**R2.** The landing class must avoid the explicit congruence classes of Bad_{j_u}. For 18 ≤ j_u ≤ 27 with
X(j_u−1) odd of type a (exhaustive; sampled support up to 80) this is 3k_{j_u−1}+δ ≢ 2^{j_u−2} (mod 2^{j_u−1});
for non-odd-a X(j_u−1) in that range Bad_{j_u} = ∅. For an a-landing one can eliminate k: the landing
condition v₂(3k_{n_t}+θ_t) = j_u−1 gives 3k_{n_t} ≡ −θ_t (mod 2^{j_u−1}), so the tie is equivalent to
k_{n_t} ≡ 3⁻¹(2^{j_u−2}−3k_{j_u−1}−3) (mod 2^{j_u−1}). For each landing parameter m there is exactly one
residue class of the deep half-time k modulo 2^{m−1} that produces a tied landing; V6-E constructs such
classes at deep j for m = 5, 8, 14, 17 (certificate failures, no EXT-tie claim). Thus R2 is a non-vacuous
congruence, not an automatic property; and it is a statement about τ(j_t−1) at deep j.

**Why neither is provable here.** R1 and R2 are congruences on τ at indices n ≈ J and n ≈ N₀. The
θ̃-automaton, HP, the certificate and the finite tables are λ_u-uniform size statements; none can decide a
specific congruence of modulus 2^{m−1} at an astronomically deep index. PROOF_SPECTRUM §3–§4 shows such
landings (including tied ones) are realizable at any tower height where the required fires exist, so a
proof must control the deep calendar. At a least strict-EXT counterexample every source epoch of the deep
segment has fire parameter < J and is tie-free by minimality; R1/R2 therefore concern tie-free real
epochs — the same object as "S1 for shifted copies" (PROOF_EXT §5). Also note that R2 is only a
sufficient condition: an uncertified landing class need not produce an EXT-tie, because inside an
uncertified class the outcome can depend on λ_u (bits beyond the class; cf. the bare (5,5) tie, whose
outcome is decided by higher bits, work_claude_shifted Cor 3.1, and its resolution by the gateway lemma of
work_claude_shifted §5). (The WITNESS of PROOF_SPECTRUM §4 is a chain at (5,5) but not a deep-segment landing
of an S(J), so it is not used as evidence here.) The sharpest target remains "records < precision with ties
resolved"; the present note reduces DEEP to R1 ∧ R2 (for 6Λ(J)+4 ≤ B) but does not claim DEEP′ is necessary.

**Possible next steps (not done here).** (a) Extend "Bad_j = first-chain tie classes" from the verified
range to all j < 2·10⁷ (would need a structural argument for later ties not raising records above j; the samples
suggest it). (b) Generalize the gateway lemma from j=5 to the other odd-a parameters 8,12,14,17, which
would remove those small-j Bad classes from R2. (c) Prove R1 under a calendar lower bound such as
"every fire at a deep pointer has parameter < N₀" — not available.

# 5. Data [B]

All numbers are exact integer arithmetic. Tables are built with
`work_global_ext/route_c/fdata.py::lam_walk` (read-only import; no repository file is written). The
`certify` implementation agrees with `work_claude_shifted/shiftlib.py` on 2000 random (j,δ) pairs
(V5, 0 mismatches).

**V0/V6-D (size).** In [N₀,10⁸): 24,230,413 odd type-a, 24,230,413 odd type-b, 1,267,918 odd type-c
crossings. At every odd-a crossing, bitlen(3k) ≤ 27 and j−2−bitlen(3k) ≥ 19,999,973: Lemma 2.1's
inequality holds with enormous margin. (At j = 2·10⁷ the crossing X(19,999,999) is odd-a with
k = 8,921,354, τ = 17,842,708.)

**V1 (exhaustive certificate failures, j ≤ 24) [B].** For every δ mod 2^{j+1}:
Bad_j = 4 classes for j ∈ {5,8,12,14,22,24} (exactly the four first-chain tie classes);
Bad_j = 8 for j = 17 (the four ties plus four (5,5)-preimages δ ≡ δ_tie+16 mod 32);
Bad_j = ∅ for j ∈ {6,7,9,10,11,13,15,16,18,19,20,21,23}.
Supplementary run: j = 25,26: ∅; j = 27: 4 = ties. Total ≈ 6.7·10⁷ exact walks; V1+V2 together 107 s.

**V2 (tie sets, same ranges) [B].** T(j) = classes whose θ̃-walk has a non-descent:
T(17) = 8196 (≫ Bad₁₇ = 8), T(24) = 260, T(j) = 4 for j ∈ {5,8,12,14,22}, T(j) = ∅ for
j ∈ {6,7,9,10,11,13,15,16,18,19,20,21,23}. So later non-descents do not break certification in range;
for 18 ≤ j ≤ 24, Bad_j = the first-chain tie classes (not T(j): T(24) = 260 ≫ 4 = |Bad₂₄|).

**V3 (automatic landing defects) [B].** For every 5 ≤ j < 2·10⁷ and δ ∈ {0,1,2,3}: certify holds,
0 failures (4·(2·10⁷−5) exact walks; V3 ≈ 50 s). For 5 ≤ j ≤ 80 and δ ∈ {0,1,2,3} this is also part of V1/V2.

**V4/V6-A (random deep steps) [B].** Deep crossings of each type sampled uniformly in [N₀,10⁸), 1200
crossings × 4 defects of bit lengths {8,20,40,1000,10⁵,10⁷}:
type a: 4800 landings, 11 first-chain ties, 11 certificate failures, max landing parameter 12;
type b: 4800 landings, 17 ties, 17 failures, max 11;
type c: 4800 landings, 0 ties, 0 failures, max 5.
**In every case certificate failure ⇔ first-chain tie at the landing**; no other failure occurred.
The separate V4 run at j = 2·10⁷ with 4000 random defects: same (0 failures, max landing 11).

**V6-C (forced resonances) [B].** 400 deep odd-a crossings with d = −3k (|d| ≤ B): the next step was
never a resonant a-step (Lemma 2.3); 112 landings occurred, all certified (max landing parameter 9).

**V6-E (constructed tied landings) [B].** For m ∈ {5,8,12,14,17} (odd-a landing parameters) the unique
residue k ≡ 3⁻¹(2^{m−2}−3k_{m−1}−3) (mod 2^{m−1}) was searched among deep odd-a crossings; at
m = 5,8,14,17 such crossings exist (e.g. m = 5: j = 20,000,027, k = 8,921,366, d = −26,764,082,
|d| < B), and in every hit the landing chain is a first-chain tie and certify fails.
**This shows DEEP(ii) can fail at deep chains**; it does not construct an S(J).

**V6-F (large-m landings) [B].** Forced landings at m = 40 and 100 (d = 2^{m−1}−3k) certify and are not
tied; no compatible deep crossing was found for m = 10,20,30,60,1000,10⁴,10⁵ in the scanned window.

**V6-G (exact big-integer checks of Lemma 2.5) [B].** For j = 2·10⁷, 2·10⁷+5, 2·10⁷+8, 2·10⁷+13 (odd-a
crossings) and d ∈ {1, 12345, −3k}, the exact walk from x = 2^j, Θ = x+d was computed with full integers
(≈ 2·10⁷ bits): j′ and D′ mod 2^{j′+1} agree with Lemma 2.5 in all 36 cases (including the resonant
lift bit).

**V8 (supplementary sampling) [B as computation; C-support for any general claim].** For 18 ≤ j ≤ 80: every first-chain tie class fails certification
(0 exceptions); 30,000 random (j,δ) with |δ| < 2^{10⁷} gave 35 non-descents, all at later chains, and 0
certificate failures; ten (5,5)-preimage classes at j ≤ 400 have a non-descent and all certify.

# 6. Reproduce

```
python -B verify_deep.py 20000000 24            # V1–V5, 163 s, writes verify_deep_checks.json
python -B verify_deep_supp.py 20000000          # V8, 34 s, writes verify_deep_supp_checks.json
python -B verify_deep_100m.py 100000000         # V6 (needs a 2.8 GB cached table), 129 s after load
```

The heavy table cache lives in `D:\math_cc_astra\deep1` (outside the repository). The scripts import the
repository's `work_global_ext/route_c/fdata.py` read-only and never write inside the repository except
their own json beside themselves.

# 7. Scope

Proved here [A], unreviewed: Lemmas 2.1–2.6 (incl. the size-of-Λ bound, Λ(K_clock) = 4, and the range
J < T_{h*} for 6Λ+4 ≤ B), Corollary 2.7 (initial deep segment only), Lemma 3.1 (t ≥ 1; unused),
Theorem 3.1, Theorem 3.4 (only for J with 6Λ(J)+4 ≤ B). [B]: the exhaustive statements of Corollary 3.3
(j ≤ 27; congruence form for 18 ≤ j_u ≤ 27 at odd-a X(j_u−1)), the window result (except bare ties), and §5
with their ranges. [C-support]: the congruence form for 28 ≤ j ≤ 80 (sampled). [C]: Remark 3.2,
Remark 2.8, the congruence form for j > 80, R1 and R2 as a route to EXT. **Not proved: EXT, DEEP, DEEP′,
R1, R2; DEEP(i) for J ≥ T_{h*}.** No global non-halting claim, no change of K_clock. The WITNESS of
PROOF_SPECTRUM §4 is not used.
