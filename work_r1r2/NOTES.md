已通过三方审查 / accepted (reviews/r1r2_review_record.md) — work_r1r2: R2 for a/b landings is automatic under R1, and sharp reductions of R1 and of the c-landing R2 (ZCode agent, 2026-10-20)

## 中文摘要

本笔记推进 BB(6) holdout #1（`1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`）全局不停机证明中，
已接受归约 **EXT(J) ⟸ R1 ∧ R2**（work_deep Theorem 3.4，对 6Λ(J)+4 ≤ B 的 J）之后剩下的缺口。
**未证明 EXT，未改变 K_clock，未声称机器不停机。**

主要结果（[A] 一般参数证明，[B] 有限精确计算并注明范围，[C] 猜想/数据）：

1. **精确漂移 [A]。** 设 N₀=2·10⁷，B=2^{10⁷}。在 R1 下，初始深段的每条链 t 的 θ_t 恰为
   a/b 两步映射（a: θ↦3−θ，b: θ↦θ−1）的整数值；因而 θ_t = 2i−t+1（0≤i≤t），
   |θ_t| ≤ t+1，且 θ_t 的奇偶性随时间交替（θ_t ≡ t+1 mod 2）。此结论不需要无共振假设（但需要 R1）。
2. **无共振与更锐的链数 [A]。** 在 R1 下，若 2Λ+1 < 3(N₀−2)/4（等价于 Λ ≤ 7 499 998；特别 Λ≤13 成立），
   则深链的 a 步 z=3k+θ 恒不为 0；于是每个深→深步都满足 j_{t+1} ≤ L(j_t)，
   故深链数 ≤ Λ(J)（改进 work_deep 的 2Λ+1），且末深链 T ≤ Λ−1。（没有 R1 时，深→深 c 步可能制造共振，
   只剩 work_deep 的 2Λ+1 计数。）注意 B=2^{10⁷} 是天文数字，
   Λ ≤ (B−4)/6 远不足以推出无共振；本笔记只用 Λ ≤ 13 的范围。
3. **R2 对 a/b 着陆自动成立（在 Λ≤13 范围内）[A+B]。** 若着陆步是 a 型，δ=3−θ_T ∈ [3−Λ, Λ+1]；
   b 型 δ=θ_T−1 ∈ [1−Λ, Λ−1]。Λ ≤ 13 时两者都落在已接受的证书窗口 [−12,15]（[B]，
   work_claude_shifted §4）。因此 R2 对 a/b 着陆自动成立，**唯一例外是裸 tie 类 (5,5)、(5,−11)**。
4. **裸 tie 的两步网关归约 [A]。** 若 a/b 着陆的类恰为 (5,5) 或 (5,−11)，则 θ_T∈{−2,6} 或 {14,−10}，
   且着陆同余 v₂(3k+θ_T)=4。设 k=k_{j_T−1}、u_T 为奇数底、D_T 为精确亏损，则两条精确恒等式
   （PROOF_RESCUE §1 的 (AA)）给出：解出链 u+1 的参数 m=v₂(θ_T+12+9k)（a 型）或 v₂(2θ_T+10+9k)（b 型），
   记录严格下降 R_{u+1} ≤ R_T−1 ≤ J−1，且 u+1 的亏损类**只依赖 (θ_T,m)**：
   δ_{u+1} ≡ (10−2^m)/3（(5,5)）或 (26−2^m)/3（(5,−11)）(mod 2^{m+1})。
   这把裸 tie 化为一个更小尺度的显式类，而不是"自动通过"。
5. **[B] 大规模规范检验。** certify(m, (10−2^m)/3) 与 certify(m, (26−2^m)/3) 对**全部**
   5 ≤ m < 2·10⁷ 成立（19 999 995 个 m，0 失败，53 秒；用带精度的精确游走 + 缓存交叉表）；
   独立复核（agent V，自写代码）把它推进到 **全部 5 ≤ m < 10⁸**（两族共约 2 亿个证书，0 失败）。
   （修正版 verify_r1r2_big.py 的 b/c 步精度为 min(curP, j)−1−ε；对抗审查者用修正版重跑全部
   5 ≤ m < 2·10⁷（1350 万个 b/c 步）：0 失败。）
   因此对 j_T < 2^{10⁸}/(4.5 P) 的范围，裸 tie 归约完全闭合。若 m ≥ 10⁸（需要
   τ(j_T−1) ≥ 2^{10⁸}/10 的极端同余，密度 2^{−10⁸}），解出的链 u+1 重新变深，成为一个显式的
   "深部大相位入口"（相位 Θ·3 ≡ 10 或 26），与 R1 同类，本笔记明确留作残余。
6. **结论 [A+B]。** 对 J < T₄（Λ(J) ≤ 4，含 K_clock）：**EXT(J) ⟸ R1 ∧ R2_c**；
   对 T₄ ≤ J < T₁₃（Λ(J) ≤ 13）：**EXT(J) ⟸ R1 ∧ R2_c ∧ RES**，RES := 不存在 m ≥ 10⁸ 的
   a/b 裸 tie 着陆。理由 [A]（Cor 2.6）：裸 tie 需 θ_T ∈ {−2,6,14,−10}，由 1−T ≤ θ_T ≤ T+1 得 T ≥ 3；
   m ≥ 10⁸ 需 j_T ≳ 2^{10⁸}/(4.5P) ≫ 2^{N₀}，故 Λ(j_T) ≥ 2；又 j_T ≤ L^{(T)}(J)，故 Λ(J) ≥ T+Λ(j_T) ≥ 5。
   即 R2 从"着陆类证书"退化为"c 着陆的一条显式同余"（Λ ≥ 5 时另加残余 RES）。
7. **R1 的更锐刻画 [A]。** R1 ⟸ (CAL-C)：不存在 n ≥ N₀−1 使 X(n) 为奇 c 型且
   2^{N₀} | (3τ(n)+4+λ_Y(n))。（对单个 J 只有 R1(J) ⟸ CAL-C；反方向取 J=n+1（可能 ≥ T₁₃），
   且新亏损约 2^{N₀−1} ≫ B 时链 1 因 |θ|≤B 条款离开深段，故逆命题只在 Lemma 4.2 的漂移条件下成立。）
   ¬R1 时 τ(n_T) ≥ (2^{N₀}−5)/6，
   新亏损 θ_{T+1} ≡ θ_T+3τ+3 (mod 2^{j_{T+1}}) **完全由 τ 决定**，记录严格下降；
   而 |θ_{T+1}| > B **不被强制**（精确条件见 Lemma 4.2）。更进一步，源恒等式
   λ′_W(n) = (6τ(n)+4−3τ(n′)) − 2^{n′}λ_u 给出充分条件 R1 ⟸ (CAL-C′) ∧ (NC)（逆向不成立：
   NC 可因抵消而失败但 n′ ≤ ω < N₀；CAL-C′ 可失败而 CAL-C 成立）：(CAL-C′) 是纯 τ 同余，
   (NC) 是"无抵消"v₂(6τ+4−3τ(n′)) < n′。二者都未被证明；必要形式：¬R1 ⟹ SIZE ∨ CANCEL。
   R1 失败本身不是 tie，而是"漂移界失效 + 强同余"。
8. **c 着陆的 R2 的更锐归约 [A]。** 对 c 着陆（j_u=ω(n_T)<N₀），有
   δ ≡ θ_T+3τ+3−2^{j_u} (mod 2^{j_u+1})，**只依赖 (θ_T, τ mod 2^{j_u+1}, j_u)**（与 λ_Y 的高位无关）。
   故 R2(c) 等价于 τ(n_T) 避开一条显式同余（j_u≥18 的 odd-a 情形为 τ ≡ τ₀ mod 2^{j_u−1}）；
   这不是自动性质，需要深部日历算术。**新增 [A] 两步化解（广义 gateway 引理，Lemma 5.3）**：
   若 X(j_u−1) 为奇 a 型且 Q := 2θ_T+6+6k_{j_u−1}+6τ−λ′_W/2 ≢ 0 (mod 2^{σ−1})，则两步块给出
   j_{u+1}=v₂(Q)、r_{u+1} ≤ r_T−1 和显式的类 θ_{u+1} ≡ θ_T+6+3τ+3τ(j_u−1)−Q (mod 2^{j_{u+1}+1})；
   只要该小参数类可证书化，整个着陆类被绕过。规范数据中 ω ≤ 5，唯一坏类在 j_u=5
   （θ_T ≡ 5 mod 16），**全部 8,712 个坏对都被两步化解**（j₂∈{5,6,12}，8712/8712 通过）；
   Λ=4 的漂移集内坏对数为 0。范围说明：8,712 = [N₀,10⁸) 中 2,178 个 ω=5 交叉 × [−30,30] 中
   θ_T ≡ 5 mod 16 的 4 个值；其中只有 4,356 个在 Λ ≤ 13 漂移可达，Λ=4 时 0 个。真实的 J~K_clock
   深着陆发生在远超 10⁸ 的 n_T，所以这只是 Lemma 5.3 的 [B] 支持，不是 R2(c) 的证据。

9. **独立复核（agent V，自写代码）[B]。** 漂移可达集、无共振不等式、窗口证书（全范围
   5 ≤ j < 2·10⁷ 的 28 个 delta，恰 (5,5)、(5,−11) 失败）、网关恒等式（真实交叉 X(16), X(53), X(64)
   及符号验证）、以及 A6 类证书均被独立复现；唯一发现的范围错误（B=2^{10⁷} 使无共振不能从
   Λ ≤ (B−4)/6 推出）已在正文中修正为 Λ ≤ 7 499 998（本笔记只用 Λ ≤ 13）。

Tags: [A] all parameters (hypotheses stated), [B] finite exact computation (range stated),
[C-support] sampled, [C] conjecture/data. **Not proved: EXT, R1, the c-landing R2, the residual RES
(m ≥ 10⁸, relevant only for Λ(J) ≥ 5).** Cor 2.6 does not cover J ≥ T₁₃ (work_deep already reduces
DEEP up to T_{h*}). No global non-halting claim; K_clock unchanged.

---

# 0. Setting, notation, imports

Machine #1 of BB(6): `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Imports are the accepted results
of `work_global_ext/PROOF_EXT.md` §2 (walk rules, Lemma K, HP, AB, RB), `work_el/PROOF_EL.md` A1–A3
(the θ̃ automaton), `work_claude_shifted/NOTES.md` (Theorem SC, Prop 3.2 certificate, §4 window
certificate, §5 gateway-tie lemma), and `work_deep/NOTES.md` (deep segment; Lemmas 2.1–2.6,
Cor 2.7, Lemma 2.5 landing classes, Theorem 3.4). All are used read-only as black boxes.

**Chains.** For J ≥ 2 the symbolic exit S(J) has chains t = 0,1,…,r with parameters j_t, accumulated
loss Γ_t, record R_t := j_t+Γ_t, j₀ = J, Γ₀ = 0, defect-automaton value θ_t (θ₀ = 1), n_t = j_t−1;
chain t reads X(n_t). Rules (PROOF_EXT §2): X(n) even ⇒ S(J) ends at chain t; type a (τ(n)=2k):
Θ_{t+1} = Θ_t+3+6k, x' = 2Θ+6k−x/2, ε=0; type b/c (W's chain (c′_W, λ′_W) at τ(n)): x' = c′_W·u+λ′_W
with u = x/2^{j}, Θ' = Θ+3+3τ, ε = n−v₂(c′_W) ≥ 1 for b/c. Γ_{t+1} = Γ_t+1+ε. A **tie**
(EXT-tie) at chain t ≥ 1 is R_t ≥ J; EXT(J) = no tie.

**θ̃.** θ_t := Θ_t mod 2^{j_t} (symmetric representative). Exact rules (PROOF_EL A2, A3; Lemma 1.3 of
work_claude_shifted): NT holds at a deep a-step, i.e. v₂(3k+θ_t) ≠ j_t−2 (work_deep Lemma 2.2);
at a non-resonant a-step θ_{t+1} ≡ 3−θ_t (mod 2^{j_{t+1}}); at a b/c-step
θ_{t+1} = θ^W+θ_t−2 (mod 2^{j_{t+1}}), where θ^W = 1 for type b (Lemma K(b): W's chain is a fire), so
θ_{t+1} ≡ θ_t−1; for type c Φ(n) := 3τ+5−λ′_W = 1−λ_Y and θ_{t+1} ≡ θ_t+Φ−2 = θ_t−1−λ_Y.

**Deep segment.** N₀ := 2·10⁷, B := 2^{N₀/2} = 2^{10⁷}. A chain is **deep** if j_t ≥ N₀ and |θ_t| ≤ B.
The **landing chain** u is the first chain with j_u < N₀; T := u−1 is the last deep chain (the deep
chains are 0..T because parameters strictly decrease: work_deep Lemma 2.2). Put
P(n) := 2⌈log₂(6n²+5)⌉²+1345, κ(j) := (3/2)(j−1)P(j−1),
L(j) := max(1+⌊log₂(κ(j)+B)⌋, ⌊log₂(6(j−1)P(j−1)+5)⌋), Λ(J) := min{h : L^{(h)}(J) < N₀}.

**Standing imports [A, accepted].**
* (CLOCK) τ(n) ≤ nP(n) at every reached crossing (PROOF_CLOCK).
* τ(n) ≥ (n−1)/2 at every crossing (PROOF_EXT §4).
* Deep trichotomy (work_deep Lemma 2.2): at a deep chain |3k+θ_t| ≤ κ(j_t)+B < 2^{j_t−2}; no
  non-descent; type a: j_{t+1} = 1+v₂(3k+θ_t) ≤ j_t−2, or (resonance z=0) j_{t+1} = j_t−1;
  type b/c: j_{t+1} = ω(n_t) ≤ j_t−3.
* Λ(K_clock) = 4; for J < T_{h*}, h* = ⌊(B−4)/6⌋, T₁ = 2^{(N₀−3)/2}, T_{h+1} = 2^{(T_h−3)/2}, we
  have 6Λ(J)+4 ≤ B and Λ(J) ≤ ⌊log-density tower⌋ (work_deep Lemma 2.4: Λ(J) ≤ h for J < T_h).
* Theorem 3.4 of work_deep: for every J with 6Λ(J)+4 ≤ B, EXT(J) ⟸ R1 ∧ R2, where
  **R1** = "no c-step at a deep chain keeps the walk deep" and
  **R2** = "the landing class (j_u, δ) is certified", certify(j,δ) := the exact walk from the
  representative (2^j, 2^j+δ) ends with all records ≤ j (Prop 3.2 of work_claude_shifted).
* [B] Window certificate (work_claude_shifted §4): for every 5 ≤ j < 2·10⁷ and δ ∈ [−12,15],
  certify(j,δ) holds except (j,δ) = (5,5) and (5,−11).
* [B] Bad_j data (work_deep Cor 3.3): Bad_5 = {5,21,−11,−27} mod 64, Bad_8 = {58,186,−198,−70} mod
  512, Bad_{12}, Bad_{14} four classes each, Bad_{17} eight; for 18 ≤ j ≤ 27, Bad_j is exactly the
  four first-chain tie classes δ ≡ 2^{j−2}−3k_{j−1} (mod 2^{j−1}) when X(j−1) is odd of type a
  (j ∈ {22,24,27}), and empty otherwise.

**Real vs virtual references.** All walk identities used in [A] hold for every integer state
(PROOF_EL A1–A3, Theorem SC); the "virtual" use is confined to the certificate framework of
Prop 3.2 (a reference representative (2^j, 2^j+δ) that must not hit x = 0; the [B] checks reject
x ≤ 0), which is exactly the accepted shifted-copy device. No EXT statement is applied to a virtual
reference beyond the accepted consistent fire transfers (Theorem SC / Prop 3.2 / Lemma RB). The
canonical data used in [B] are real crossings of F (fdata.lam_walk).

**Remark on the size of B.** B = 2^{10⁷} has ten million bits; Λ ≤ (B−4)/6 is astronomical. The
inequality 2Λ+1 < 3(N₀−2)/4 needed below for "no resonance" is **not** a consequence of
6Λ+4 ≤ B; it is an extra hypothesis, equivalent to Λ ≤ 7 499 998, hence satisfied by Λ ≤ 13,
which is the range of Theorem 2.4.

---

# 1. The exact drift

**Lemma 1.1 (exact drift) [A].** Assume R1. Then at every chain t of the initial deep segment
(t ≤ T) the following hold as identities for the symmetric representatives:
* if the step at chain t is type a: θ_{t+1} = 3−θ_t;
* if type b: θ_{t+1} = θ_t−1;
* consequently θ_t = 2i_t−t+1 for some integer 0 ≤ i_t ≤ t; in particular 1−t ≤ θ_t ≤ t+1,
  θ_t ≡ t+1 (mod 2), and |θ_t−3/2| ≤ t+1/2.

*Proof.* Induction on t. At t=0, θ₀ = 1 = 2·0−0+1. Suppose θ_t = 2i−t+1 with 0 ≤ i ≤ t.
(a) A deep a-step: PROOF_EL A2 gives θ_{t+1} ≡ 3−θ_t (mod 2^{j_{t+1}}), and j_{t+1} ≥ 5 (a
continuing chain has j ≥ 5, PROOF_EL Lemma 1). We have |3−θ_t| = |t+2−2i| ≤ max(t+2, t−2) ≤ t+2.
For t ≤ 12 (which is all we use) this is ≤ 14 < 2^4 ≤ 2^{j_{t+1}−1}, so 3−θ_t is the symmetric
representative. In general, for deep chains j_{t+1} ≥ N₀ and the same conclusion is immediate;
at the landing chain the statement is read as a congruence (see Lemma 2.1). Since
3−θ_t = 3−(2i−t+1) = 2(t−i+1)−(t+1)+1, the index i′ = t−i+1 satisfies 1 ≤ i′ ≤ t+1.
(b) A b-step: θ^W = 1 by Lemma K(b), so θ_{t+1} ≡ θ_t−1 (mod 2^{j_{t+1}}) and |θ_t−1| ≤ t+1 <
2^{j_{t+1}−1}; θ_t−1 = 2i−(t+1)+1 with i ∈ [0,t] ⊂ [0,t+1]. ∎
(Note: this argument does not use the absence of resonance; a resonant a-step has j′ = j−1 and
θ′ = 3−θ as well, by the same congruence with |3−θ| < 2^{j′−1}. The set of reachable values is
exactly {2i−t+1 : 0 ≤ i ≤ t}: the a-image has i′ = 1..t+1 and the b-image i = 0..t, whose union
is i = 0..t+1.)

**Lemma 1.2 (no resonance; sharp chain count) [A].** Assume R1 and 2Λ(J)+1 < 3(N₀−2)/4. Then:
(i) at every deep a-step, z := 3k_{n_t}+θ_t ≠ 0 (no resonance);
(ii) every deep→deep step, of type a, b **or c**, satisfies j_{t+1} ≤ L(j_t);
(iii) the number of deep chains is at most Λ(J); hence T ≤ Λ(J)−1;
(iv) |θ_t| ≤ t+1 ≤ Λ(J) for every t ≤ T.
(R1 is genuinely used: the proof of (i) needs |θ_t| ≤ 2Λ+1, which comes from Lemma 1.1 and hence
from R1. Without R1 a deep→deep c-step can move θ to size up to B and create a resonance; then only
the 2Λ+1 count of work_deep Lemma 2.4 survives.)

*Proof.* By the accepted count of work_deep Lemma 2.4 the deep chains are 0..T with T+1 ≤ 2Λ+1, so
|θ_t| ≤ t+1 ≤ 2Λ+1 by Lemma 1.1 (which uses R1). At a deep a-step, n_t = j_t−1 ≥ N₀−1 and
3k_{n_t} = (3/2)τ(n_t) ≥ (3/2)(n_t−1)/2 = 3(N₀−2)/4 > 2Λ+1 ≥ |θ_t|,
so z ≠ 0. (If z = 0, then |θ_t| = 3k ≥ 3(N₀−2)/4, contradiction.)
(ii) A non-resonant deep a-step: |z| < 2^{j_t−2} (work_deep Lemma 2.2), so v₂(z) < j_t−2 and
j_{t+1} = 1+v₂(z) ≤ 1+⌊log₂|z|⌋ ≤ 1+⌊log₂(κ(j_t)+B)⌋ ≤ L(j_t). A b- or c-step: j_{t+1} = ω(n_t) ≤
⌊log₂(6τ(n_t)+5)⌋ ≤ ⌊log₂(6(j_t−1)P(j_t−1)+5)⌋ ≤ L(j_t).
(iii) By (ii), j_T ≤ L^{(T)}(J); since j_T ≥ N₀, L^{(T)}(J) ≥ N₀, so T < Λ(J) by the definition of
Λ, i.e. T+1 ≤ Λ. (iv) Under R1 every θ_t is obtained by a/b steps (Lemma 1.1), so |θ_t| ≤ t+1 ≤
T+1 ≤ Λ. ∎

Explicit threshold: 3(N₀−2)/4 = 14 999 998.5 and 2Λ+1 < 14 999 998.5 ⇔ Λ ≤ 7 499 998. Since
Λ(J) ≤ 13 is what we use, the hypothesis holds with an enormous margin (2·13+1 = 27).

**Lemma 1.3 (records before the landing) [A].** Under R1 and 2Λ+1 < 3(N₀−2)/4:
R₁ ≤ J−1, and R_t is strictly decreasing on the deep segment; in particular R_T ≤ J−1 for T ≥ 1
and R_T = J for T = 0.

*Proof.* At chain 0: if X(J−1) is type a, z = 3k+θ₀ = 3k+1 > 0 and |z| < 2^{J−2}, so
j₁ = 1+v₂(z) ≤ J−2 and R₁ = j₁+1 ≤ J−1; if type b/c, j₁ = ω ≤ J−3 and R₁ ≤ J−3+2 = J−1. On the
deep segment, a non-resonant a-step has j_{t+1} ≤ j_t−2 and Γ_{t+1} = Γ_t+1, so
R_{t+1} ≤ R_t−1; a b-step has j_{t+1} ≤ j_t−3 and Γ_{t+1} = Γ_t+2, so R_{t+1} ≤ R_t−1. ∎

---

# 2. R2 for a/b landings

**Lemma 2.1 (landing defect for a/b) [A].** Assume R1, 2Λ+1 < 3(N₀−2)/4, and let the landing step
at chain T be of type a or b.
* type a: δ := D_u mod 2^{j_u+1} = 3−θ_T; if |3−θ_T| < 2^{j_u}, then δ = 3−θ_T ∈ [2−T, T+2].
  (This holds e.g. when Λ ≤ 13: 2−T ≥ 3−Λ ≥ −10 and T+2 ≤ Λ+1 ≤ 14 < 32 ≤ 2^{j_u}.)
* type b: δ = θ_T−1 ∈ [−T, T] (again the symmetric representative when Λ ≤ 13).

*Proof.* Lemma 2.5 of work_deep (with the lift bit absent: by Lemma 1.2 there is no resonance, so the
landing a-step is non-resonant and j_u ≤ j_T−2). Lemma 1.1 gives the ranges. ∎

**Corollary 2.2 [A+B].** Assume R1, Λ(J) ≤ 13. Then for an a/b landing, δ ∈ [−10,14] (type a) or
δ ∈ [−12,12] (type b), hence δ ∈ [−12,15]. By the accepted [B] window certificate, R2 holds for
every a/b landing **except** possibly when (j_u, δ) ∈ {(5,5), (5,−11)}.

*Proof.* Lemma 1.2 gives T ≤ Λ−1 ≤ 12, so Lemma 2.1 gives the ranges (δ_a ∈ [2−12,12+2] = [−10,14],
δ_b ∈ [−12,12]). j_u < N₀ = 2·10⁷ and (if j_u ≥ 5) the window certificate applies; j_u ≤ 4 ends the
walk, and if X(n_T) is even S(J) ends on the deep segment (no R2 needed). The only uncertified
window pairs are (5,5) and (5,−11). ∎

**Lemma 2.3 (bare-tie two-step gateway reduction) [A].** Assume the landing step is type a or b,
(j_u, δ) = (5,5) or (5,−11) with δ the symmetric representative mod 2^{j_u+1}, and R1 with
|θ_T| ≤ 13 (so that δ = 3−θ_T resp. θ_T−1 pins θ_T exactly, no lift ambiguity). Then:
* type a: θ_T = −2 for (5,5) and θ_T = 14 for (5,−11); the landing congruence is
  v₂(3k+θ_T) = 4, where k := k_{j_T−1} = τ(j_T−1)/2.
* type b: θ_T = 6 for (5,5) and θ_T = −10 for (5,−11); v₂(3k+2) = 4 (equivalently
  v₂(6k+4) = 5, i.e. ω(n_T) = 5).

Write x_T = 2^{j_T}u_T (u_T odd), D_T := Θ_T−x_T (the exact defect), and k = k_{j_T−1}. Then the
following are exact identities:
* **a-landing** (two a-steps, the second at j = 5 with k₄ = 1):
  x_{u+1} = 5·2^{j_T−2}u_T + (D_T+12+9k), D_{u+1} = −2^{j_T−2}u_T − 3k,
  m := j_{u+1} = v₂(θ_T+12+9k) ≤ j_T−3 (**a**),
* **b-landing** (one b-step with λ′_W = 3τ+4 = 6k+4, then one a-step at j = 5):
  x_{u+1} = 13·2^{j_T−3}u_T + 2D_T+10+9k, D_{u+1} = −5·2^{j_T−3}u_T − D_T + 2 − 3k,
  m := j_{u+1} = v₂(2θ_T+10+9k) ≤ j_T−4 (**b**).
Moreover in both cases R_{u+1} = m+Γ_T+2 (a) resp. m+Γ_T+3 (b), so R_{u+1} ≤ R_T−1 ≤ J−1; and the
class of chain u+1 is determined by (θ_T, m) alone:
δ_{u+1} := D_{u+1} mod 2^{m+1} = (c−2^m)·3^{-1} mod 2^{m+1}, c = 10 for (5,5), c = 26 for (5,−11),
where 3^{-1} is the inverse of 3 modulo 2^{m+1}. Equivalently 3·δ_{u+1} ≡ c−2^m (mod 2^{m+1}).

*Proof.* (a) The a-step rule at chain T gives x_u = (3/2)x_T+2D_T+6k and Θ_u = Θ_T+3+6k; applying
the a-step rule again at chain u (k₄ = τ(4)/2 = 1; PROOF_EL Lemma C) gives
x_{u+1} = (5/4)x_T+D_T+12+9k = 5·2^{j_T−2}u_T+D_T+12+9k and
D_{u+1} = Θ_{u+1}−x_{u+1} = −2^{j_T−2}u_T−3k (PROOF_RESCUE §1 identity (AA), valid even when the
second step violates NT). Since D_T ≡ θ_T (mod 2^{j_T}) and
|θ_T+12+9k| ≤ 14+12+4.5(j_T−1)P(j_T−1) = 26+3κ(j_T) < 2^{j_T−2} (CLOCK: 9k = 4.5τ(j_T−1);
κ(j) ≤ (3/2)(j−1)² for j ≥ N₀ by work_deep, so 26+3κ ≪ 2^{j_T−2}) while the first term has valuation exactly
j_T−2, we get m = v₂(θ_T+12+9k) < j_T−2. The class is D_{u+1} mod 2^{m+1} = −3k mod 2^{m+1}
(because m+1 ≤ j_T−2). The definition m = v₂(9k+θ_T+12) means 9k+θ_T+12 ≡ 2^m (mod 2^{m+1}), i.e.
k is determined modulo 2^{m+1}; substituting 3k ≡ (2^m−θ_T−12)·3^{-1} gives
−3k ≡ (θ_T+12−2^m)·3^{-1} ≡ (c−2^m)·3^{-1}, which is c = 10 for θ_T = −2 and c = 26 for θ_T = 14.
The landing congruence is automatic: from 9k+10 ≡ 2^m (mod 2^{m+1}) with m ≥ 4 we get
9k+10 ≡ 0 (mod 16), hence 3(3k−2) ≡ −16 (mod 32), hence 3k−2 ≡ 16 (mod 32) and v₂(3k−2) = 4;
similarly for θ_T = 14 (9k+26 = 3(3k+14)−16).
(b) The b-step at chain T gives x_u = c′_Wu_T+λ′_W = 3·2^{j_T−2}u_T+6k+4 and Θ_u = Θ_T+3+6k, with
ω = v₂(6k+4) = 1+v₂(3k+2) = 5. The a-step at chain u (k₄=1) gives
x_{u+1} = 2Θ_u+6−x_u/2 = 13·2^{j_T−3}u_T+2D_T+10+9k and D_{u+1} = −5·2^{j_T−3}u_T−D_T+2−3k.
The valuation is m = v₂(2θ_T+10+9k) < j_T−3 (same size estimate: |2θ_T+10+9k| ≤ 30+3κ(j_T)), the class is
2−θ_T−3k mod 2^{m+1}, and the substitution 9k+2θ_T+10 ≡ 2^m (mod 2^{m+1}) gives
3·(2−θ_T−3k) ≡ 16−θ_T−2^m (mod 2^{m+1}), i.e. the same two constants c = 10 (θ_T=6) and c = 26
(θ_T=−10). Records: for (a), Γ_{u+1} = Γ_T+2 and j_{u+1} = m ≤ j_T−3, so
R_{u+1} = m+Γ_T+2 ≤ j_T−3+Γ_T+2 = R_T−1; for (b), Γ_{u+1} = Γ_T+3 and m ≤ j_T−4, so
R_{u+1} ≤ j_T−4+Γ_T+3 = R_T−1. ∎

**Theorem 2.4 (R2 for a/b landings) [A+B].** Assume R1 and Λ(J) ≤ 13. Then R2 holds for every a/b
landing **unless** the landing class is a bare tie (5,5) or (5,−11) **and** the parameter m produced
by the two-step resolution of Lemma 2.3 satisfies m ≥ 10⁸. Indeed, the only possible uncovered
case is that of Lemma 2.3, where the resolved class (c−2^m)/3 is certified by the [B] check below
for every 5 ≤ m < 10⁸.

*Proof.* Corollary 2.2: either the landing class is certified by the window [B], or it is one of the
bare ties, in which case Lemma 2.3 produces chain u+1 of parameter m with record < R_T ≤ J−1 and the
explicit class (c−2^m)/3. If m < N₀ = 2·10⁷ and the [B] certificate for that class holds (V6), Prop 3.2
with precision m+1 (D_{u+1} is known modulo 2^{j_T−2} ⊇ 2^{m+1}) gives all later records ≤ R_{u+1} < J.
If N₀ ≤ m < 10⁸, the same argument applies: Prop 3.2/HP needs only that D_{u+1} is known modulo
2^{m+1}, which holds since m+1 ≤ j_T−2; the certificate certify(m, (c−2^m)/3) for these m is agent V's
independent 10⁸ scan (`agent_V/scan_A6.py`, which runs the first b/c step with HP ceiling m−1−ε and
later b/c steps with the exact c′_W) [B]. ∎

**Remark 2.5 (the residual m ≥ 10⁸) [C].** When m ≥ 10⁸ (> N₀) the resolved chain u+1 has a deep
parameter (though |θ_{u+1}| ≈ 2^m/3 > B), with
the explicit class 3Θ ≡ c (mod 2^{m+1}), c = 10 or 26 (i.e. Θ ≡ c/3 mod 2^{m+1}). Since
m = v₂(9k+θ_T+12), this needs 2^{m} | (9k+θ_T+12) with m ≥ 10⁸, i.e. τ(j_T−1) ≡ (explicit) modulo
2^{10⁸}/9: an astronomically strong congruence on the deep calendar (density 2^{−10⁸}). The walk is
then a "deep entry with rational phase 10/3 or 26/3"; the drift analysis of §1 does not apply
(|θ| ≈ 2^m/3 > B), so this is an explicit residual of the same nature as R1, not covered here.
Numerically, for every m < 10⁸ the resolved walk ends with records ≤ 24 (V6), so the residual is
only the astronomically deep congruence. (The first step at chain u+1 has z = 3k+θ_{u+1} with
|z| < 2^{m−1}; a non-descent there needs z = ±2^{m−2}, again a deep-calendar congruence.) Note that
in this branch the drift window is **shifted** (the initial defect is c·3^{-1} mod 2^m ≈ ±2^m/3, not
1), so even a later a/b landing is not covered by Corollary 2.2: the branch needs its own analysis.
The residual is non-vacuous: agent V's `gap_m.py` exhibits algebraic configurations
(k ≡ −10/9 mod 2^{2·10⁷+1} and k ≡ 6 mod 32) that satisfy the a-(5,5) landing congruence with
m ≥ 2·10⁷+1 (a consistency model only, not claimed to arise from an actual S(J)).

**Corollary 2.6 (the new form of the reduction) [A+B].**
* For every J < T₄ (so Λ(J) ≤ 4; this includes K_clock):  EXT(J) ⟸ R1 ∧ R2_c.
* For every T₄ ≤ J < T₁₃ (so Λ(J) ≤ 13):  EXT(J) ⟸ R1 ∧ R2_c ∧ RES,
  RES := "no a/b landing is a bare tie (5,5)/(5,−11) whose resolved parameter m satisfies m ≥ 10⁸".
Here R2_c is the c-landing class condition of §5. Outside the residual, R2 for a/b landings is
automatic (Theorem 2.4). This is strictly sharper than work_deep Theorem 3.4, whose R2 quantified
over all landing classes.

*Proof that RES is vacuous for Λ(J) ≤ 4 [A].* Assume R1, Λ(J) ≤ 13, and a bare-tie a/b landing with
m ≥ 10⁸. (1) By Lemma 2.3, θ_T ∈ {−2, 14} (type a) or {6, −10} (type b); Lemma 1.1 gives
1−T ≤ θ_T ≤ T+1, so θ_T = −2 needs T ≥ 3, θ_T = 6 needs T ≥ 5, θ_T = −10 needs T ≥ 11, θ_T = 14 needs
T ≥ 13; in all cases T ≥ 3. (2) 2^m divides the nonzero integer θ_T+12+9k (type a) or 2θ_T+10+9k
(type b), k = τ(j_T−1)/2 ≤ (j_T−1)P(j_T−1)/2 by CLOCK, so 2^{10⁸} ≤ 2^m ≤ 30+4.5(j_T−1)P(j_T−1).
Hence 6(j_T−1)P(j_T−1)+5 > 2^{10⁸} > 2^{N₀}, and the second term of L gives L(j_T) ≥ N₀; with
j_T ≥ N₀ this means Λ(j_T) ≥ 2. (3) By Lemma 1.2(ii), j_T ≤ L^{(T)}(J), and L^{(t)}(J) ≥ j_t ≥ N₀ for
t ≤ T; since L is nondecreasing (work_deep §2), Λ(J) = T+Λ(L^{(T)}(J)) ≥ T+Λ(j_T) ≥ 3+2 = 5.
So for Λ(J) ≤ 4, in particular for J < T₄ ∋ K_clock (work_deep Lemma 2.4), RES holds automatically. ∎

---

# 3. The general-Λ range

For Λ > 7 499 998 the no-resonance inequality fails, so Lemma 1.2 is unavailable. What survives is
Lemma 1.1 (exact drift under R1; no no-resonance hypothesis needed) together with the accepted count T+1 ≤ 2Λ+1, giving
|θ_t| ≤ 2Λ+1 and
* δ_a ∈ [2−(2Λ), 2Λ+2], δ_b ∈ [−2Λ, 2Λ] (as symmetric representatives mod 2^{j_u+1}, provided
  |δ| < 2^{j_u}).
Hence R2(a/b) for general Λ reduces to the finite list of explicit classes
{(j_u, 2−t), (j_u, 3−(2i−t+1)), …} — one per reachable drift value — i.e. to certify(j_u, δ) with
δ in the displayed range. It is **not** automatic: the window [−12,15] covers only Λ ≤ 13, and
Bad_j is nonempty for infinitely many j (the first-chain tie classes at odd-a j). Since
K_clock < T₄ < T₁₃, the range of Corollary 2.6 covers the K_clock scale with an enormous margin;
Corollary 2.6 does not cover J ≥ T₁₃ (work_deep already reduces DEEP up to T_{h*}).

---

# 4. R1: the deep → deep c-step (characterisation and sharp reduction)

**Lemma 4.1 (c-step ledger) [A].** At a type-c step at chain T: j_{T+1} = ω(n_T), Γ_{T+1} =
Γ_T+1+ε(n_T), and j_{T+1} = ω ≤ n_T−ε−1 = j_T−2−ε, so
R_{T+1} = j_{T+1}+Γ_{T+1} ≤ j_T−2−ε+Γ_T+1+ε = R_T−1,
and j_{T+1} ≤ L(j_T). Hence a c-step is never an EXT-tie and satisfies the parameter bound of
Lemma 1.2(ii). The count bound T ≤ Λ−1 nevertheless **does** use R1: it needs no resonance, which
needs |θ_t| ≤ 2Λ+1 (Lemma 1.1, under R1); without R1 a deep→deep c-step can create a later resonance
and only the 2Λ+1 count of work_deep survives.

*Proof.* PROOF_EL A1 (j' = ω, loss 1+ε) and W's S1 (v₂ c′_W = n−ε > ω). ∎

**Lemma 4.2 (exact new defect) [A].** Let chain T be deep with X(n_T) odd of type c, and put
w := ω(n_T) = v₂(3τ+4+λ_Y). Then
  θ_{T+1} ≡ θ_T + Φ − 2 = θ_T − 1 − λ_Y ≡ θ_T + 3τ(n_T) + 3 (mod 2^w),
the last step because λ_Y ≡ −3τ−4 (mod 2^w). Hence the new defect is a function of τ(n_T) alone.
Writing ρ for the least residue of θ_T+3τ+3 mod 2^w, chain T+1 is deep iff w ≥ N₀ and
(ρ ≤ B or ρ ≥ 2^w−B). Consequently R1's failure does **not** force |θ_{T+1}| > B; the exact
sufficient condition for the drift is R1-C: |θ_{T+1}| ≤ B−6Λ−4 (so that the remaining at most 2Λ+1
a/b steps, each changing |θ| by at most 3, keep |θ| ≤ B).

*Proof.* Lemma 4.1 and the definition Φ = 1−λ_Y; the residue statement is immediate. ∎

**Lemma 4.3 (R1 is implied by a calendar statement) [A].** Let
  (CAL-C) no n ≥ N₀−1 with X(n) odd of type c has 2^{N₀} | (3τ(n)+4+λ_Y(n)).
Then CAL-C ⟹ R1(J) for every J (sufficiency). The converse holds only in a restricted form: if n
violates CAL-C and, at J := n+1, the drift condition of Lemma 4.2 holds for chain 1 (the least
residue of θ₀+3τ(n)+3 = 3τ(n)+4 modulo 2^ω lies within B of 0), then R1(n+1) fails. Note that
J = n+1 may be ≥ T₁₃, so for a single J only R1(J) ⟸ CAL-C is available.
*Proof.* (⟸) a c-step at a deep chain has n_T ≥ N₀−1 and j_{T+1} = ω = v₂(3τ+4+λ_Y) < N₀.
(Restricted converse) Given such an n, take J := n+1 ≥ N₀. Chain 0 of S(J) is the fire with
j₀ = J ≥ N₀ and θ₀ = 1, hence deep, and it reads X(J−1) = X(n); the step is type c with ω ≥ N₀.
Chain 1 has j₁ = ω ≥ N₀, but its defect θ₁ ≡ 3τ(n)+4 (mod 2^ω) (Lemma 4.2) is in general of size
≈ 2^{N₀−1} ≫ B (since τ(n) ≥ (2^{N₀}−5)/6), in which case chain 1 leaves the deep segment by the
|θ| ≤ B clause and R1 is **not** violated. Only under the drift condition is chain 1 deep, and
then R1(n+1) fails. ∎
Consequently ¬R1 at T implies (via ¬CAL-C) τ(n_T) ≥ (2^{N₀}−5)/6 (from λ_Y ≤ 3τ+1: 3τ+4+λ_Y ≤ 6τ+5 and
2^{N₀} | λ′_W), and R1 is automatic for n < 2^{N₀−64} (since 6τ(n)+5 ≤ 6nP(n)+5 < 2^{N₀} there).

**Lemma 4.4 (source identity and dichotomy) [A; verified on the table].** At a type-c crossing let
n′ = j_{t′}−1 be the source parameter (Lemma K(c): W's chain is chain t′+1 of the real epoch with
parameter n′+1) and λ_u the odd base of that chain. Then
  λ′_W(n) = A − 2^{n′}λ_u,   A := 6τ(n)+4−3τ(n′),   n′ ≤ ⌊log₂(6τ(n)+5)⌋.
Hence if v₂(A) < n′ then ω = v₂(A) ≤ log₂ A; otherwise ω ≥ n′. If 2^{n′} ∤ A then
CAL-C at n ⇔ 2^{N₀} ∤ A.
*Proof.* Let s := τ(n). Apply the a-step formula A2 to the source chain t′ at its own crossing
X(n′) (odd of type a, τ(n′) = 2k): λ_H = 2^{n′}λ_u+3τ(n′)+1. The crossing state of X(n) is exactly
that return state (Lemma K(c)), so λ_A(n) = λ_H. The mass identity at X(n) gives
λ_A+λ_Y = 3s+1, hence λ′_W = 3s+4+λ_Y = 6s+5−λ_A = 6s+4−3τ(n′)−2^{n′}λ_u = A−2^{n′}λ_u. Finally the
source chain has step s_{t′} = s−1−τ(n′) < s, and j_{t′} ≤ log₂(6s_{t′}+5), so n′ ≤ log₂(6s+5). ∎
**Dichotomy and SIZE/CANCEL [A].** (a) If v₂(A) < n′ then ω = v₂(λ′_W) = v₂(A) ≤ log₂ A.
(b) If v₂(A) ≥ n′ then ω ≥ n′; when 2^{n′} | A, ω = n′+v₂(A/2^{n′}−λ_u). Consequently, if R1 fails
at n (so 2^{N₀} | λ′_W), then either **SIZE** 2^{N₀} | A (forcing τ(n) ≥ (2^{N₀}−4)/6), or
**CANCEL**: 2^{n′} | A and λ_u ≡ A/2^{n′} (mod 2^{N₀−n′}). [A; the identities are verified exactly at
all 1,584,898 type-c crossings to 10⁸, where CANCEL never occurs.]

**Reduction of R1 [A].** R1 ⟸ (CAL-C) ⟸ (CAL-C′) ∧ (NC), where (CAL-C′) is the pure τ-congruence
"2^{N₀} ∤ (6τ(n)+4−3τ(n′)) at every type-c crossing n ≥ N₀−1" and (NC) is
"v₂(6τ(n)+4−3τ(n′)) < n′". (NC) removes λ_u and leaves a congruence in τ alone. Only ⟸ holds: NC
can fail by cancellation with n′ ≤ ω < N₀ without violating CAL-C, and CAL-C′ can fail while CAL-C
holds (when NC fails). The necessary form is the dichotomy above: ¬R1 ⟹ ¬CAL-C ⟹ SIZE ∨ CANCEL.
Neither (CAL-C′) nor (NC) is proved here; both are canonical-calendar statements of the same type
as CLOCK.

**Remark 4.5 (minimality does not close R1) [A].** At a least strict-EXT counterexample the source
epoch has J_W < J and is tie-free, which gives ω < J_W ≤ log₂(3n_T P(n_T)+4); this is compatible
with ω ≥ N₀ (the size bound only forces τ(n_T) ≥ (2^{N₀}−5)/6, i.e. j_T beyond a tower of height
about N₀). The descent tower of source epochs terminates without contradiction — the nested-copy
obstruction of PROOF_EXT §5. Data: at all deep type-c crossings to 10⁸ the relevant valuations are
≤ 5 (see §6), so R1 holds with margin 2^{2·10⁷−5} in the computed canonical data.

# 5. The c-landing R2: exact class, congruence, two-step resolution

**Lemma 5.1 (c-landing class) [A].** Suppose the landing step at the last deep chain T is type c
(so R1 holds at T: j_u = ω(n_T) < N₀), and put σ := v₂(c′_W(n_T)) = n_T−ε(n_T). Then
  r_u ≤ r_T−1 (the landing chain is never a tie),
  δ = D_u mod 2^{j_u+1} = θ_T + Φ(n_T) − 2 = θ_T − 1 − λ_Y,
and, since 3τ(n_T)+4+λ_Y = 2^{j_u}q with q odd,
  δ ≡ θ_T + 3τ(n_T) + 3 − 2^{j_u} (mod 2^{j_u+1}).
So the class depends only on (θ_T, τ(n_T) mod 2^{j_u+1}, j_u); it is **independent of the higher
bits of λ_Y** and of the base u_T. For T = 0 it reduces to the accepted ENTRY defect −λ_Y.

*Proof.* Lemma 2.5 of work_deep gives D_u ≡ θ_T+Φ−2 (mod 2^{j_u+1}); λ_Y = λ′_W−3τ−4 = 2^{j_u}q−3τ−4
with q odd; so δ ≡ θ_T−1−λ_Y ≡ θ_T+3τ+3−2^{j_u}q ≡ θ_T+3τ+3−2^{j_u} (mod 2^{j_u+1}) because q is
odd. And r_u = ω+Γ_T+1+ε = r_T−(n_T−ε−ω) = r_T−(σ−ω) ≤ r_T−1 because σ > ω (W's S1). ∎
(19/19 exact big-integer one-step checks at n = 6132 and the small crossings; agent C's
`check_small.py`, 20,988 checks.)

**Corollary 5.2 (R2(c) as one congruence) [A].** R2(c) ⟺ certify(j_u, δ). If X(j_u−1) is odd of
type a, k := k_{j_u−1}, then the first-chain tie class δ ≡ 2^{j_u−2}−3k (mod 2^{j_u−1})
necessarily fails certification (record ≥ j_u+1 > j_u); in calendar variables this is
  τ(n_T) ≡ 3^{-1}(2^{j_u−2}−3k_{j_u−1}−θ_T−3) (mod 2^{j_u−1}).
For 5 ≤ j_u ≤ 27 this is exactly Bad_{j_u} (work_deep Cor 3.3; j_u = 17 also has four (5,5)-preimage
classes); for j_u ≤ 4 R2(c) is automatic (the walk ends at chain u). A congruence is not a proof:
R2(c) is a genuine deep-calendar statement and is **not** automatic in general.

**Lemma 5.3 (two-step resolution; generalized gateway) [A].** Assume X(j_u−1) is odd of type a and
  Q := 2θ_T + 6 + 6k_{j_u−1} + 6τ(n_T) − λ′_W(n_T)/2,   with   Q ≢ 0 (mod 2^{σ−1}).
Then the two-chain block (the c-step at T and the a-step at u) satisfies
  j_{u+1} = v₂(Q) < σ−1,   r_{u+1} ≤ r_T−1,
  θ_{u+1} ≡ θ_T + 6 + 3τ(n_T) + 3τ(j_u−1) − Q (mod 2^{j_{u+1}+1}),
and the class at chain u+1 is known modulo 2^{j_{u+1}+1}. If moreover
certify(j_{u+1}, θ_{u+1}) holds, then every record of S(J) at and after the landing chain u is
≤ max(r_u, r_{u+1}) ≤ r_T−1 < J: **the landing class is bypassed entirely.**

*Proof.* x_u = c′_Wu_T+λ′_W, Θ_u = Θ_T+3+3τ; the a-step at chain u (k′ = k_{j_u−1}) gives
x_{u+1} = 2Θ_T+6+6τ+6k′−(c′_W/2)u_T−λ′_W/2 = Q−(c′_W/2)u_T+2^{j_T+1}u_T, and (c′_W/2)u_T has
valuation σ−1 > v₂(Q), while 2^{j_T+1}u_T has valuation j_T+1 > σ−1; hence j_{u+1} = v₂(Q).
D_{u+1} = Θ_{u+1}−x_{u+1} and Θ_{u+1} = Θ_T+6+3τ+6k′ give the displayed class residue. Records:
r_{u+1} = r_u+(j_{u+1}−ω)+1 ≤ r_u+(σ−2−ω)+1 = r_u+(r_T−r_u−1) = r_T−1, because
r_T−r_u = n_T−ε−ω = σ−ω and j_{u+1} ≤ σ−2. ∎
At j_u = 5 this is the accepted gateway-tie lemma of work_claude_shifted §5; Lemma 5.3 extends it
to every odd-a landing parameter and makes Q explicit.

**Negative results for R2(c) [A].** (i) R2(c) cannot be reduced to an earlier EXT instance: the
landing state differs from the source epoch's real chain by a phase of Θ_T−2, whose 2-adic
valuation is small, so HP does not transfer (it would need the additional congruence
3d_T ≡ 1 mod 2^σ). (ii) The accepted low-deficit c-source reductions (A-SOURCE, C3, C5-BA, CA,
MINUS/PLUS, D-ROOT, duration normalization) do not apply: they treat the entry chain 1 = V(C,−1)
with ε ∈ {3,5}, whereas here the c-crossing is an interior chain with generally unbounded ε(n_T).
(iii) There is no size argument: without an NT failure the class walk's records are non-increasing,
so the certificate is irreducibly a class statement.

**Data supporting Lemma 5.3 [B].** On the canonical table to 10⁸, deep type-c crossings
(1,267,918 in [N₀,10⁸)): ω = j_u ∈ {1: 150569, 3: 1115171, 5: 2178}; every canonical deep
c-landing is either terminal (j_u ≤ 4) or at j_u = 5. Only j_u = 5 has bad classes
(δ ≡ 5 mod 16); at all 2,178 such crossings τ ≡ 31 (mod 64) and λ_Y ≡ −1 (mod 8192), so δ ≡ θ_T
(mod 64) and the bad class is θ_T ≡ 5 (mod 16). Bad pairs: for θ_T in [−30,30] there are 8,712
(4 per crossing); for the Λ = 4 drift set there are **0**; for the Λ = 13 drift set there are 4,356
(θ_T = −11, 5). **All 8,712 bad pairs are resolved by Lemma 5.3**: j₂ = v₂(Q) ∈ {5,6,12}, the
class at u+1 certifies in 8,712/8,712 cases, r_{u+1} ≤ r_T−1 in all cases, 0 unresolved. Exact
big-integer two-step checks: 198/198 at n = 6132 and cached crossings, plus 77 independent checks
by the coordinator. The structural regularities ω ≤ 5 and τ ≡ 31 (mod 64) are [C] facts of the
computed range; no structural reason is proved.
**Scope.** The 8,712 count is 2,178 ω = 5 crossings in [N₀,10⁸) × the 4 values θ_T ≡ 5 (mod 16) in
[−30,30]; only 4,356 of them are drift-reachable at Λ ≤ 13, and 0 at Λ = 4. Real deep landings for
J ~ K_clock occur at n_T far beyond 10⁸. These data are therefore [B] support for the mechanism of
Lemma 5.3, **not** evidence for R2(c).

**What remains for R2(c).** (a) The certificate of the two-step image (j₂, θ₂), a short-modulus
(j₂ canonically ≤ 12) calendar statement; (b) the characterisation Bad_j = tie classes for j_u ≥ 28
(proved exhaustively only to j = 27, sampled to 80, [C-support]); (c) the case Q ≡ 0 mod 2^{σ−1},
not covered by Lemma 5.3 and not observed in the data.

# 6. Data [B]

All computations are exact integer arithmetic; the canonical table is the accepted lambda-walk data
(`work_global_ext/route_c/fdata.py`, cached in `D:\math_cc_astra\deep1`, outside the repository).
Subagent scripts and JSON live in `work_r1r2/agent_R1/`, `work_r1r2/agent_C/`, `work_r1r2/agent_V/`;
their own NOTES/REPORT files are the primary records for directions B and C.

**V1 reachable drift (verify_r1r2.py).** For all words of length <= 14 over {a,b}: the reachable set
at depth t is exactly {2i-t+1 : 0 <= i <= t} (0 mismatches) -- confirms Lemma 1.1.

**V2 inequalities.** 3(N0-2)/4 = 14 999 998.5, 3*(N0-2)//4 = 14 999 998; the no-resonance
inequality 2L+1 < 3(N0-2)/4 holds at L = 13 (27) and exactly up to L = 7 499 998 (2L+1 = 14 999 997);
it fails at 7 499 999. (Earlier text said 14 999 997 / 7 499 997: an arithmetic slip, conservative.) At j = N0 the size inequality
B+kappa(j) < 2^(j-3) holds (work_deep Lemma 2.1).

**V3 window certificate.** For every 5 <= j < 1000 and delta in [-12,15] (27 860 pairs) the only
failures are (5,5) and (5,-11); the full range 5 <= j < 2*10^7, all 28 delta, is re-verified
independently by agent V (`agent_V/check_window.py` + `full_window.py`; 18*(2*10^7-5) certificates,
exactly two failures). This is an independent reproduction of the accepted [B] window certificate.

**V4 gateway algebra.** 4000 random integer instances of the two-a-step identity
x_{u+1} = 5*2^(j-2)*u+D+12+9k, D_{u+1} = -2^(j-2)*u-3k (0 errors); the class formula (c-2^m)/3
verified for m <= 64 in all four scenarios, including the automatic landing congruence. Agent V
re-verified the gateway identities on the real crossings X(16), X(53) (a-landing) and X(64)
(b-landing), symbolically and by exact walk.

**V5 end-to-end on real crossings.** Real odd type-a crossings with k = 6 (mod 16) realize a
(5,5)/(5,-11) landing; constructed true states (x = 2^{j_T}u, Theta = x+theta_T) run through the
exact walk: 24 cases, all with landing parameter 5, m matching the formula, class matching
(10-2^m)/3 or (26-2^m)/3, and R_{u+1} <= R_T-1. Real odd type-b crossings with omega = 5 realize
the b-landing variant: 280 checks (theta_T = 6 and -10, u = 1,3,5,7,17), all formulas and the
record inequality verified, 0 errors. Example: j_T = 65, k = 26, theta_T = 6, u = 1, m = 8.

**V6 resolved-class certificate (verify_r1r2_big.py).** For every m with 5 <= m < 2*10^7 (19 999 995
values of m, both classes), certify(m, (c-2^m)/3 mod 2^(m+1)) holds: the exact walk from
(2^m, 2^m+cls) ends with all records <= m. **0 failures** (53 s). The walk is run with truncated
precision (1024 bits) so that the level-m representative is handled without 2*10^7-bit arithmetic;
the prefix is validated against the full exact walk for 64 <= m < 3000 (0 mismatches where the exact
walk has table data). The resolved walks are very short (1-4 chains from the first step on).
**Correction (review).** The original script undercounted the precision lost at b/c steps: it drops
the term c'_W*u (v2(c'_W) = j-1-eps) but kept precision curP-1-eps; the correct HP precision is
min(curP, j)-1-eps. The script is now fixed. The adversary reran a corrected version over all
5 <= m < 2*10^7 (13.5M b/c steps): 0 failures; the editor independently reran the fixed script (on a
copy outside the repository, table_20000000.pkl): 19 999 995 values of m, 0 failures, 68 s.
Agent V re-scanned the same statement independently with its own code and extended it to
**all 5 <= m < 10^8** (two classes, about 2*10^8 certificates, 0 failures) using
`table_100000000.pkl`.

**V7 c-landing data and two-step resolution (agent C).** Canonical table to 10^8, deep range
[2*10^7,10^8): 1,267,918 odd type-c crossings, omega = j_u in {1: 150569, 3: 1115171, 5: 2178} --
all deep c-landings are terminal (j_u <= 4) or at j_u = 5. At all 2,178 omega = 5 crossings
tau = 31 (mod 64) and lambda_Y = -1 (mod 8192), so delta = theta_T (mod 64) and the bad class is
theta_T = 5 (mod 16). Bad pairs: for theta_T in [-30,30] there are 8,712 (4 per crossing); for the
L = 4 drift set **0**; for the L = 13 drift set 4,356 (theta_T = -11, 5). All 8,712 bad pairs are
resolved by the two-step Lemma 5.3: j2 = v2(Q) in {5,6,12}, the class at u+1 certifies in
8,712/8,712 cases, r_{u+1} <= r_T-1 in all cases, 0 unresolved; 198/198 exact big-integer two-step
checks. The coordinator independently re-verified the Lemma 5.3 identities at X(6132) (77/77 cases,
a real omega = 5 c-crossing). Scope: 8,712 = 2,178 crossings x 4 values theta_T = 5 (mod 16) in
[-30,30]; only 4,356 are drift-reachable at L <= 13 and 0 at L = 4; real deep landings at J ~ K_clock
have n_T far beyond 10^8, so this is [B] support for Lemma 5.3, not evidence for R2(c).

**V8 R1 data (agent R1).** Canonical table to 10^8, deep range [2*10^7,10^8): 1,267,918 odd type-c
crossings with omega = v2(3tau+4+lambda_Y) in {1,3,5} (max **5**; type-b control: max omega = 26).
Hence R1 holds in all computed data with margin 2^(2*10^7-5). lambda_Y <= 3tau+1 with 0 violations
(deep max lambda_Y-3tau = -26,764,118). The source identity
lambda'_W(n) = (6tau(n)+4-3tau(n')) - 2^(n')*lambda_u is exact at all 1,584,898 type-c crossings;
2^(n') | A occurs **never**, so (NC) holds throughout, omega = v2(A) <= 29, min(n'-v2(A)) = 1.
All omega = 5 crossings have n' = 13 and tau = 31 (mod 64). For deep type-c landing classes with
theta_T in [-30,30], certify fails only at omega = 5 with theta_T = 5 (mod 16); theta_T = 1 never
fails (0/1,267,918).

**Independent verification verdict (agent V).** A1 (drift), A4 (window), A5 (gateway algebra, on
X(4), X(16), X(53), X(64) and symbolically) and A6 (to 10⁸) were verified with independent code;
A2/A3 are correct for Λ ≤ 13 but the originally briefed range (all Λ with 6Λ+4 ≤ B) was wrong and
is corrected here to Λ ≤ 7 499 998; the residual m-bound (m < 10⁸) is confirmed as an unproved gap
and is stated as such in Theorem 2.4 / Remark 2.5; the T = 0 record bound (R₀ = J) and the b/a
landing-congruence distinction are confirmed and are stated correctly here.

**Table facts re-checked (agent V).** On the 2*10^7 table: tau(n) >= (n-1)/2 at every crossing
(0 violations), CLOCK tau <= nP(n) (0 violations), lambda_Y <= 3tau+1 (0 violations), the deep size
inequality B+kappa(j) < 2^(j-3) (minimum slack 10,999,996), omega bounds. No repository file is
written.

---

# 7. What is proved / open

**Proved [A] here (unreviewed, integrated with the subagent reports).** Lemma 1.1 (exact drift on
the initial deep segment under R1, no no-resonance hypothesis); Lemma 1.2 (under R1 and
2L+1 < 3(N0-2)/4, i.e. L <= 7 499 998, in particular L <= 13: no resonance and chain count <= L;
R1 is needed); Lemma 1.3 (record
bounds); Lemma 2.1, Corollary 2.2, Lemma 2.3 (bare-tie two-step reduction with exact identities,
resolved class (c-2^m)/3, record descent), Theorem 2.4 (R2 automatic for a/b landings except the
residual m >= 10^8, conditional on the [B] class checks); Corollary 2.6 (EXT(J) <= R1 and R2_c for
J < T4, the residual RES being vacuous when L(J) <= 4); Lemma 4.1 (c-step ledger), Lemma 4.2 (exact
new defect and the precise condition for the next chain to be deep), Lemma 4.3 (R1 <= calendar
condition CAL-C; converse only under the drift condition), Lemma 4.4
(source identity and SIZE/CANCEL dichotomy); Lemma 5.1 (c-landing class), Corollary 5.2 (R2(c) as
one congruence), Lemma 5.3 (two-step resolution of any odd-a c-landing, generalizing the accepted
gateway lemma).

**Proved [B].** V1-V8 as in section 6, in particular: certify for the resolved bare-tie classes for
all 5 <= m < 2*10^7 (19 999 995 values, 0 failures) and, independently, all 5 <= m < 10^8; the
window certificate re-verified over the full range 5 <= j < 2*10^7; the gateway identities
end-to-end on real crossings; the c-landing two-step resolution of all 8,712 canonical bad pairs;
R1 data to 10^8 (omega <= 5, NC holds).

**Not proved.** EXT; R1 (sufficient conditions: the calendar congruence CAL-C, or CAL-C' and NC);
R2(c) in general (the certificate of the two-step image, and the characterisation of Bad_j for
j_u >= 28); the residual RES (m >= 10^8 of Remark 2.5; only relevant for L(J) >= 5, i.e. J >= T4);
the two-step resolution case Q = 0 (mod 2^(sigma-1)). Corollary 2.6 does not cover J >= T13
(work_deep already reduces DEEP up to T_{h*}). No global non-halting claim; K_clock unchanged.

**Status of the reduction.** For J < T4 (includes K_clock): EXT(J) <= R1 and R2_c. For
T4 <= J < T13: EXT(J) <= R1 and R2_c and RES. R2 for a/b landings is now automatic (Theorem 2.4)
except for the explicit congruence RES of Remark 2.5 (vacuous for L(J) <= 4), and R2 for c-landings is
reduced either to one explicit congruence (Corollary 5.2) or, via Lemma 5.3, to a short-parameter
certificate (verified on all canonical data). The whole remaining problem is therefore:
  (i) R1, implied by a deep-calendar congruence (CAL-C), itself implied by (CAL-C') and (NC);
  (ii) the short-parameter certificates produced by the two-step resolutions (a MINUS/PLUS-type
       family statement), and the Bad_j characterisation beyond j = 27;
  (iii) RES for T4 <= J < T13; and the range J >= T13, not covered by Corollary 2.6 (work_deep
       already reduces DEEP up to T_{h*}).
This is strictly sharper than work_deep Theorem 3.4 (whose R2 quantified over all landing classes),
but it does not close EXT.

---

# 8. Reproduce

```
python -B work_r1r2/verify_r1r2.py 1000 1000      # V1-V6 small, ~0.4 s, writes verify_r1r2_checks.json
python -B work_r1r2/verify_r1r2_big.py "D:\math_cc_astra\deep1\table_20000000.pkl" 20000000
                                                  # V6 full 5 <= m < 2e7, ~68 s (fixed version), writes verify_r1r2_big_checks.json
# subagents (own code; see their NOTES.md for full commands):
python -B work_r1r2/agent_R1/verify_R1.py        # V8 table data (table_100000000.pkl), ~20 s
python -B work_r1r2/agent_C/scan_deep_c.py       # V7 c-landing data, ~7 s
python -B work_r1r2/agent_C/check_gateway.py     # C6 resolution of all 8712 bad pairs, ~1 s
python -B work_r1r2/agent_V/check_window.py      # independent window certificate
python -B work_r1r2/agent_V/scan_A6.py 20000000  # independent A6 scan (and 100000000)
```
The scripts import `work_global_ext/route_c/fdata.py` read-only and need the cached canonical
tables (560 MB for N = 2*10^7, 2.8 GB for N = 10^8) in `D:\math_cc_astra\deep1`, built by
work_deep's `build_table.py`. No script writes inside the repository except its own JSON beside
itself. Measured: verify_r1r2.py 0.4 s; verify_r1r2_big.py 53 s original, 68 s fixed (N = 2*10^7; the in-repo verify_r1r2_big_checks.json is from the fixed run, 19,999,995 m, 0 failures); agent V's A6 scan
34 s (N = 2*10^7) and a few minutes (N = 10^8); agent R1's table scan 14 s + 12 s; agent C's scan
7 s.
