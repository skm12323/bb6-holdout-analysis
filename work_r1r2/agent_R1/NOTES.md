未经审查 / unreviewed

work_r1r2/agent_R1 (DIRECTION B: R1, the deep->deep c-step), 2026-10-20

# R1: the deep -> deep c-step — sharp equivalent forms, a structural reduction, and canonical data

Tags used throughout: **[A]** proved for all parameters (hypotheses stated); **[B]** finite exact
computation (range stated); **[C]** conjecture / data / unproved remark.
**Nothing here proves EXT; nothing here changes K_clock; no claim is made about the machine halting or
not halting.** R1 is *not* proved and *no counterexample* to it was found.

## 中文摘要

本笔记处理 work_deep Theorem 3.4 中的条件 **R1**（"任何深链上的 c 步都不会让游走保持深度"，等价地：
深链 T 处 X(n_T) 为奇 c 型时 ω(n_T) < N₀ = 2·10⁷）。主要结论：

1. **[A] 精确化与锐化。** (a) R1 失败于深链 T ⟺ X(n_T) 为奇 c 型且 2^{N₀} | λ'_W(n_T) = 3τ(n_T)+4+λ_Y(n_T)。
   (b) **R1 完全等价于一个纯规范日历陈述 (CAL-C)**：对所有 n ≥ N₀−1，若 X(n) 为奇 c 型则
   2^{N₀} ∤ (3τ(n)+4+λ_Y(n))。证明用"链 0 技巧"：取 J = n+1，链 0 参数为 J ≥ N₀、θ₀ = 1，必为深链。
   因此 R1 与 J、Γ、θ 无关，只是规范交叉表上的一条整除条件——这正是题目所要求的"深部日历上的单一同余"。
   (c) 修正了任务书中的 (ii)：R1 ⟹ τ < (2^{N₀}−5)/6 是**假的**；正确方向是 ¬R1-at-T ⟹ τ(n_T) ≥ (2^{N₀}−5)/6。
   R1 在 τ(n_T) < (2^{N₀}−5)/6 的交叉处自动成立。结合 CLOCK 得 n_T P(n_T) ≥ (2^{N₀}−5)/6，
   故 **R1 在 n < 2^{N₀−64} 的范围里自动成立 [A]**。
   (d) 深→深 c 步的账本 [A]：R_{T+1} = R_T − (v₂(c'_W) − ω) ≤ R_T − 1，损失 = 1+ε(n_T)，
   ε(n_T) < n_T − ω ≤ j_T − N₀ − 2。**深→深 c 步本身永不造成 EXT-tie**。
   (e) |θ_{T+1}| > B **不是必然的**：给出精确条件（θ_T+3τ+3 mod 2^ω 落在 [0,B] ∪ [2^ω−B,2^ω)），
   并构造满足全部已接受约束（含 Lemma S、质量恒等式、λ_Y ∈ [0,3τ+1]、S1、CLOCK）而 |θ_{T+1}| ≤ B 的
   **一致性模型**。故 R1 与"DEEP(i) 失败"**不等价**；精确的漂移假设是 R1*（c 步后链不深）或更强的
   预算型 R1-C（|θ_{T+1}| ≤ B−6Λ−3）。R1-C ⟹ 初始深段上的 DEEP(i) [A]。
2. **[A] 新结构恒等式（Lemma S）。** 对每个 c 型交叉 n，设 t' 是源链（那个其 a-返回就是第 τ(n) 步的链），
   n' = j_{t'}−1，λ_u 为其奇基。则**精确地**
   λ_A(n) = 2^{n'}λ_u + 3τ(n') + 1，  λ'_W(n) = A − 2^{n'}λ_u，  A := 6τ(n)+4−3τ(n')。
   由此得**二分法 [A]**：若 v₂(A) < n' 则 ω = v₂(A) ≤ log₂ A；否则 ω ≥ n'。
   推论 **[A]**：R1 在 n 处失败 ⟹ 或者 (SIZE) 2^{N₀} | A（从而 τ(n) ≥ (2^{N₀}−4)/6），
   或者 (CANCEL) 2^{n'} | A 且 λ_u ≡ A/2^{n'} (mod 2^{N₀−n'})。
   且永远有 n' ≤ log₂(6τ(n)+5)（G6 §5.3 的已接受推论）。
   于是**在数据中处处成立的"无消去"性质 v₂(A) < n' 之下，R1 ⟺ (CAL-C′)：
   对所有 n ≥ N₀−1，X(n) 奇 c 型时 2^{N₀} ∤ (6τ(n)+4−3τ(n'))** —— λ_u 被完全消去，只剩 τ 的同余。
3. **[B] 大规模规范数据（到 10⁸，含深段 [2·10⁷,10⁸)）。** 1,267,918 个深段奇 c 交叉（全表 1,584,898 个）：
   - ω ∈ {1,3,5}，最大值 **5**（不是 2 的任意幂次；b 型对照最大 26 且呈几何分布）。所以 ω ≥ 16,20,…,64 的个数全为 0。
   - λ_Y ≤ 3τ+1 零违反；深段 max(λ_Y−3τ) = −26,764,118（全表 −86）。深段 max λ_Y/(3τ+4) = 133820239/267640489 ≈ 0.50000。
   - Lemma S 的两条恒等式在**全部 1,584,898 个**奇 c 交叉上逐位验证成立（源链由仪表化游走独立给出）。
   - **2^{n'} | A 从不发生**（0/1,584,898；深段 0/1,267,918）；因此 ω = v₂(A) 处处成立，min(n'−v₂(A)) = 1。
   - 深段 type-c 着陆类（θ_T ∈ [−30,30]）：θ_T=1 时 certify **0 失败 / 1,267,918**；任意 θ 时仅 2,178 个失败，
     其失败 θ 恰为 θ_T ≡ 6 (mod 16)（ω=5 且 base ≡ 0 mod 64；Bad₅ = {5,21,37,53} mod 64 = 首链 tie 类，与 work_deep 一致）。
   - 深段 τ 最大 89,213,529（n=99,999,965），A 最大 535,281,166（29 位）——与 2^{N₀} = 2^{2·10⁷} 相差 2^{N₀−29} 倍。
4. **未能证明 R1。** 最小反例 + 质量恒等式/最小性只给出 ω < J_W ≤ log₂(3n_T P(n_T)+4)，与 ω ≥ N₀ 相容；
   c 步的"源塔"（逐层把源链参数当新的深链）不断下降，终止于 a/b 步，不产生矛盾。
   R1 仍是深部日历的 2-adic 算术（与 PROOF_EXT §5 的"嵌套移位副本"同一障碍）。

---

## 1. Setting, notation, imported facts

Machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. F is the universal formal walk
(PROOF_G6 §5, PROOF_M §§1–4); X(n) is the crossing state at index n, read at step τ(n);
τ(n) is the return duration of a chain of parameter j with n = j−1 (PROOF_M Lemma 2.3);
ε(n) = n − v₂(c_A) at X(n); λ_A is the λ-part of the head at X(n); λ_Y is the λ-part of the
pending entry Y at a type-c crossing (PROOF_M §1: type c ⇔ P=[Y], i=n;
fdata.lam_walk stores these as `lA[n]`, `lY[n]`).

**Imported [A].**
- Walk rules of PROOF_EXT §2 (Lemma TR): at chain (j, Θ, x), n = j−1;
  a-step (τ(n)=2k): z := 3k+θ, θ = Θ−x read mod 2^j; b/c-step: j' = ω(n) := v₂(λ'_W(n)) with
  λ'_W = 3τ+4 (type b) and λ'_W = 3τ+4+λ_Y (type c).
- A1/A2 of PROOF_EL: b/c step has j_{t+1} = ω(n_t), θ_{t+1} ≡ θ^W + θ_t − 2 (mod 2^{j_{t+1}});
  a-step has λ_H = 2^{n_t}λ_{u_t} + 3τ(n_t) + 1 and θ_{t+1} ≡ 3−θ_t.
- Lemma K of PROOF_EXT §2 (classification of crossings), mass identity λ_A + λ_Y = 3τ(n)+1 at a
  type-c crossing (PROOF_M §1; verified as `lA+lY = 3*tau+1` on every type-c crossing below).
- Lemma T(2) of PROOF_EL: 1 ≤ β_x ≤ 6d_t − 1 for t ≥ 1; Lemma T(1): v₂(α_{x_t}) = J−Γ_t.
- CLOCK (PROOF_CLOCK §3–4): τ(n) ≤ n P(n), P(n) = 2⌈log₂(6n²+5)⌉² + 1345, at every reached
  canonical crossing.
- G6 §5.3 corollary, as used in PROOF_M §5: every top-level chain has j_t ≤ log₂(6 s_t + 5),
  s_t its step.
- work_deep: Lemma 2.2 (at a deep chain with j ≥ N₀ and |θ| ≤ B = 2^{10⁷}, |3k+θ| < 2^{j−2},
  hence no NT failure, no non-descent, and j' ≤ L(j) < j with records strictly decreasing except
  at a resonance), Lemma 2.4 (deep chains ≤ 2Λ(J)+1), Corollary 2.7, Theorem 3.4 (EXT(J) ⟸ R1 ∧ R2
  for 6Λ(J)+4 ≤ B).
- N₀ := 2·10⁷, B := 2^{10⁷}. A chain is **deep** if j_t ≥ N₀ and |θ_t| ≤ B (θ_t the symmetric
  representative mod 2^{j_t}). R_t = j_t + Γ_t.

**Definitions used below.**
- **R1** (work_deep Thm 3.4) := for every J and every deep chain T of S(J) with X(n_T) odd of
  type c: ω(n_T) < N₀.
- **R1\*** := for every J and every deep chain T with X(n_T) odd of type c: chain T+1 is not deep,
  i.e. ω(n_T) < N₀ **or** |θ_{T+1}| > B. (This is what "no c-step at a deep chain keeps the walk
  deep" literally means; R1 ⟹ R1\*.)
- **R1-C** := for every deep c-step T: |θ_{T+1}| ≤ B − 6Λ(J) − 3 (when 6Λ(J)+4 ≤ B).
- (CAL-C) := for every n ≥ N₀−1 at which X(n) exists: X(n) odd type c ⟹ 2^{N₀} ∤ λ'_W(n).
- (CAL-C′) := the same with λ'_W replaced by A(n) := 6τ(n) + 4 − 3τ(n'), n' = the source parameter
  of Section 4.

---

## 2. The c-step at a deep chain: exact ledger

**Lemma 1 (c-step ledger) [A].** Let chain t of S(J) read X(n_t), odd, of type c.
Put σ := v₂(c'_W(n_t)) = n_t − ε(n_t) (this is S1 of W's chain; note ω < σ). Then
  j_{t+1} = ω(n_t),  Γ_{t+1} = Γ_t + 1 + ε(n_t),  and
  **R_{t+1} − R_t = ω + ε − n_t = −(σ − ω) ≤ −1.**
*Proof.* R_{t+1}−R_t = (j_{t+1}+Γ_{t+1}) − (j_t+Γ_t) = ω + (Γ_t+1+ε) − (n_t+1+Γ_t) = ω+ε−n_t = −(n_t−ε−ω)
= −(σ−ω). S1 gives ω < σ. ∎

Consequences (all [A]):
1. No b/c step, at a deep chain or not, ever raises a record; a deep→deep c-step is **not** an
   EXT-tie. (Same computation as work_deep Lemma 2.2(3), now without any depth hypothesis.)
2. The loss at the step is 1+ε(n_t) with ε = n_t − v₂(c'_W) < n_t − ω ≤ j_t − N₀ − 2 whenever
   ω ≥ N₀. So an R1-failing step is very cheap: Γ grows by at most j_t−N₀−1.
3. The parameter still drops: ω = v₂(λ'_W) ≤ log₂(6τ+5) ≤ L(j_t) < j_t − 2, whether or not
   ω ≥ N₀. **Lemma 2.4's chain count (≤ 2Λ+1 deep chains) therefore never uses R1.**

**Lemma 2 (the new defect; exact condition for staying deep) [A].**
At a type-c step at deep T with ω := ω(n_T), write λ'_W(n_T) = 2^ω q, q odd. Then
  λ_Y = 2^ω q − 3τ(n_T) − 4,  and  θ_{T+1} ≡ θ_T − 1 − λ_Y ≡ θ_T + 3τ(n_T) + 3 (mod 2^ω).
Let ρ_ω := (θ_T + 3τ(n_T) + 3) mod 2^ω ∈ [0, 2^ω) (least non-negative residue). Then
  θ_{T+1} = sym(ρ_ω), and
  **|θ_{T+1}| ≤ B ⟺ ρ_ω ≤ B or ρ_ω ≥ 2^ω − B.**
Hence: **chain T+1 is deep ⟺ ω ≥ N₀ and [ρ_ω ∈ [0,B] ∪ [2^ω−B, 2^ω)].**
Equivalently, as a congruence on λ_Y mod 2^{j_{T+1}} = 2^ω (which is automatic because
λ_Y ≡ −3τ−4 (mod 2^ω)): the step keeps |θ| ≤ B ⟺ the symmetric residue of θ_T−1−λ_Y modulo 2^ω
lies in [−B,B]. So the "mild" R1 failure is a *near-congruence* on λ_Y, not a congruence; the
"hard" R1 failure (|θ_{T+1}| > B) is the generic outcome of the residue condition failing.
*Proof.* A1 gives θ_{T+1} ≡ θ_T + Φ − 2 with Φ = 1−λ_Y, i.e. θ_{T+1} ≡ θ_T − 1 − λ_Y (mod 2^ω).
From λ'_W = 2^ω q we get λ_Y = 2^ω q−3τ−4 ≡ −3τ−4, so −1−λ_Y ≡ 3τ+3 (mod 2^ω) (as 2^ω q ≡ 0).
The symmetric representative of ρ_ω has modulus ≤ B exactly on the two end intervals. ∎
Note the condition is a *shift congruence on τ(n_T) mod 2^ω* — equivalently on λ_Y mod 2^ω, which is
determined by τ(n_T) mod 2^ω because λ_Y ≡ −3τ−4 (mod 2^ω) is automatic.

**Lemma 3 (|θ_{T+1}| > B is NOT forced) [A].** There is a datum satisfying *every* constraint used
above (mass identity λ_A+λ_Y = 3s+1, λ_Y ∈ [0,3τ+1], λ_A odd, λ'_W = 3τ+4+λ_Y, S1 ω < n−ε, CLOCK,
|θ_T| ≤ B, and the source identity of Lemma 9 below) with ω = N₀ and |θ_{T+1}| ≤ B.
Explicit (N₀ = 2·10⁷ even):
  n' = 4, τ(n') = 2, λ_u = 5, q = 2, ω = N₀, s = τ(n) = (2^{N₀+1}+82)/6 ∈ ℤ,
  λ_A = 87 = 2⁴·5 + 3·2 + 1, λ_Y = 2^{N₀}−45, λ'_W = 3s+4+λ_Y = 2^{N₀+1},
  n = 2^{2N₀}, ε = 1, and any θ_T with |θ_T| ≤ B−44.
Then λ_A+λ_Y = 2^{N₀}+42 = 3s+1, 0 ≤ λ_Y ≤ 3s+1, ω(n) = v₂(λ'_W) = N₀, chain T+1 has
j = N₀ ≥ N₀, and θ_{T+1} ≡ θ_T−1−λ_Y ≡ θ_T+44 (mod 2^{N₀}), so |θ_{T+1}| ≤ B.
(CLOCK holds because s ≈ 2^{N₀}/3 ≤ nP(n) for n = 2^{2N₀}; S1 because ω < n−1.)
**This is a consistency model only** — it is not claimed to be realized by F. Its content is:
no inequality of the accepted corpus forces the drift above B, so **R1 is not equivalent to
"DEEP(i) fails"**, and R1\* (or R1-C) is the correct sharp hypothesis.

**Proposition 4 (sharp drift hypothesis) [A].** Assume 6Λ(J)+4 ≤ B. If at every deep c-step T of
the *initial deep segment* of S(J) one has |θ_{T+1}| ≤ B − 6Λ(J) − 3 (then in particular ω < N₀ is
not needed), then DEEP(i) holds on the initial deep segment.
*Proof.* a-steps change |θ| by 3−θ (|Δ| ≤ 3 when |θ| ≤ B), b-steps by −1; c-steps reset |θ| to the
bound. Every chain of the initial deep segment has j ≥ N₀, so Lemma 2.2 applies at all of them and,
by Lemma 2.4, the initial deep segment has at most 2Λ(J)+1 chains regardless of c-steps. Hence at any
chain of it, |θ| ≤ max(1, B−6Λ−3) + 3(2Λ+1) ≤ B. ∎ (R1 ⟹ R1-C, since an R1-obeying c-step does not
land on the deep segment at all.)

**Remark 5 (intermediate regime) [A].** The deep trichotomy (Lemma 2.2 of work_deep) only needs
|3k+θ| < 2^{j−2}, i.e. |θ| < 2^{j−2} − κ(j). After an R1-failing c-step we have
|θ_{T+1}| ≤ 2^{ω−1}; so for ω ≥ N₀+2 the walk is still *controlled* (no NT failure, descending
parameters, records non-increasing) as long as |θ_{T+1}| ≤ 2^{ω−2} − κ(ω), even when |θ_{T+1}| > B.
Only the DEEP(i) bound (and with it the landing-window argument of work_deep Remark 2.8) is lost.

---

## 3. Equivalent forms of R1

**Lemma 6 [A].**
(i) For a deep chain T: R1 fails at T ⟺ X(n_T) is odd of type c **and** v₂(3τ(n_T)+4+λ_Y(n_T)) ≥ N₀.
(ii) **Pure-calendar form.** R1 (for all J) ⟺ (CAL-C): for every n ≥ N₀−1 with X(n) existing,
    X(n) odd of type c ⟹ 2^{N₀} ∤ λ'_W(n) = 3τ(n)+4+λ_Y(n).
(iii) If R1 fails at T then τ(n_T) ≥ (2^{N₀}−5)/6; equivalently R1 holds at every deep type-c
    crossing with τ(n_T) < (2^{N₀}−5)/6. With CLOCK, R1 is automatic for n < 2^{N₀−64}
    (see the arithmetic below).
*Proof.* (i) is the definition plus j_{T+1} = ω = v₂(λ'_W) (A1) and lY/lA data identity
λ'_W = 3τ+4+λ_Y.
(ii) (⟹) Let X(n) be odd c with n ≥ N₀−1 and 2^{N₀} | λ'_W(n). By Theorem RA/Lemma TR the exit S(J)
is defined for **every** integer J with F defined through τ(J−1); take J = n+1 (F is defined through
X(n) by hypothesis). Chain 0 has j₀ = J = n+1 ≥ N₀ and θ₀ = 1, so it is deep, it reads X(J−1) = X(n),
and j₁ = ω(n) ≥ N₀: R1 fails. (⟸) every deep chain has j_T ≥ N₀ hence n_T ≥ N₀−1, and
ω(n_T) = v₂(λ'_W(n_T)) ≥ N₀ contradicts (CAL-C). ∎
(iii) 2^{N₀} | λ'_W forces λ'_W ≥ 2^{N₀} (it is positive), and λ'_W = 3τ+4+λ_Y ≤ 6τ+5 by
λ_Y ≤ 3τ+1. So 6τ(n_T) ≥ 2^{N₀}−5.
*Automatic range:* if n < 2^{T} then τ(n) ≤ nP(n) < 2^T·(2(2T+4)²+1345), since
⌈log₂(6n²+5)⌉ ≤ 2T+4. For T = N₀−64 this is < 2^{N₀−64}·2^{56} = 2^{N₀−8} < (2^{N₀}−5)/6. ∎

**Remark 7 [A, about the task's item (ii)].** Note the direction: "R1 ⟹ τ(n_T) < (2^{N₀}−5)/6"
is **false** as literally stated (R1 can hold with arbitrarily large τ(n_T): the divisibility is what
matters, not the size). The true statements are Lemma 6(iii) and its contrapositive.

**Remark 8 [C].** (CAL-C) is a statement about the canonical crossing table only: no J, no Γ, no θ,
no certificate. It is exactly the "single congruence on the deep calendar" that the task asked to
identify. Equivalently: R1 ⟺ "no type-c crossing of F at index ≥ N₀−1 is followed by a chain of
parameter ≥ N₀". So R1 is a statement about F's own epoch structure, and every proof must control
the deep calendar — the same object as PROOF_EXT §5.

---

## 4. The source identity and the cancellation dichotomy (new)

For a type-c crossing n, Lemma K(c) says: τ(n) (the step at which X(n) is read) is the **a-return
of the source chain t'** of the epoch containing that step; the W-chain at τ(n) is chain t'+1 of that
epoch and has parameter ω(n). Write n' := j_{t'} − 1 (so chain t' has crossing index n'), s_{t'}
its step, and λ_u the odd base of chain t'.

**Lemma 9 (source identity) [A].** With s := τ(n) and A := 6τ(n) + 4 − 3τ(n'),
  λ_A(n) = 2^{n'} λ_u + 3τ(n') + 1   and   **λ'_W(n) = A − 2^{n'} λ_u.**
Moreover n' ≤ log₂(6τ(n)+5) and s_{t'} < s.
*Proof.* A2 applied to the source chain t' (whose crossing X(n') is odd of type a with τ(n') = 2k)
gives λ_H = 2^{n'}λ_u + 3τ(n') + 1 at its return. The crossing state of X(n) *is* that return state
(Lemma K(c)), so λ_A(n) = λ_H. The mass identity at X(n) gives λ_Y = 3s+1−λ_A, hence
λ'_W = 3s+4+λ_Y = 6s+5−λ_A = 6s+4−3τ(n')−2^{n'}λ_u. Finally the source chain has step s_{t'} = s−1−τ(n')
and s_{t'} < s, so j_{t'} ≤ log₂(6s_{t'}+5) < log₂(6s+5) (G6 §5.3 corollary). ∎

**Lemma 10 (dichotomy) [A].** With A, n' as above:
(a) if v₂(A) < n' then ω(n) = v₂(A) ≤ log₂ A;
(b) if v₂(A) ≥ n' then ω(n) ≥ n' and, when 2^{n'} | A, ω(n) = n' + v₂(A/2^{n'} − λ_u).
*Proof.* λ'_W = A − 2^{n'}λ_u and v₂(2^{n'}λ_u) = n'. If v₂(A) < n' the valuations differ, so
v₂(λ'_W) = v₂(A); otherwise v₂(λ'_W) ≥ n'. ∎

**Corollary 11 (R1 reduced to SIZE or CANCEL) [A].** If R1 fails at a type-c crossing n (so
2^{N₀} | λ'_W(n)) then, with A = 6τ(n)+4−3τ(n'):
  either **(SIZE)** 2^{N₀} | A — which forces τ(n) ≥ (2^{N₀}−4)/6,
  or **(CANCEL)** 2^{n'} | A and λ_u ≡ A/2^{n'} (mod 2^{N₀−n'});
and in both cases n' ≤ log₂(6τ(n)+5).
*Proof.* If n' ≥ N₀ then 2^{N₀} | 2^{n'}λ_u, so 2^{N₀} | λ'_W ⟹ 2^{N₀} | A. If n' < N₀: from
λ'_W = A − 2^{n'}λ_u ≡ A (mod 2^{n'}) we get 2^{n'} | A; divide by 2^{n'} to get
2^{N₀−n'} | (A/2^{n'} − λ_u). ∎

**Consequence [A].** Let "no-cancellation" (NC) be the property: at every type-c crossing,
v₂(A) < n' (equivalently 2^{n'} ∤ A). Under (NC), for every type-c crossing with n ≥ N₀−1,
  R1 fails at n's chain ⟺ 2^{N₀} | A(n) = 6τ(n)+4−3τ(n'),
i.e. **R1 ⟺ (CAL-C′)**, a congruence on (τ(n), τ(n')) alone. The λ-part has disappeared.
Moreover, under (NC) one has ω(n) = v₂(A(n)) ≤ log₂ A(n), so R1's failure needs a crossing duration
τ(n) ≥ (2^{N₀}−4)/6 — the *same* necessary size as Lemma 6(iii), but now with the explicit
correction term 3τ(n').

**Remark 12 [B/C].** (NC) holds at 100% of the 1,584,898 odd type-c crossings n < 10⁸, and in fact
v₂(A) = ω ∈ {1,3,5} there (Section 7). Whether (NC) is a theorem is open; it is itself a statement
about the deep calendar (it says that a certain crossing duration is never ≡ 3τ(n')·6^{-1} + ...
modulo 2^{n'}).

---

## 5. Attempts to prove R1 (honest gap analysis)

**5.1 Minimality / least counterexample [A, gives less than hoped].**
Let J be a least strict-EXT counterexample (so EXT(J') holds for every J' < J).
(a) Every crossing read by S(J) belongs to an epoch whose fire pointer ρ_W satisfies ρ_W ≤ n, hence
its fire parameter obeys J_W = v₂(3τ(ρ_W)+4) ≤ log₂(3ρ_W P(ρ_W)+4) ≤ log₂(3n_T P(n_T)+4) < n_T ≤ J−1.
So J_W < J and, by minimality, S(J_W) is tie-free.
(b) The W-chain copied by our c-step has parameter ω and record ω + Γ_W < J_W. Hence
  **ω < J_W ≤ log₂(3 n_T P(n_T) + 4).**
(c) So R1's failure requires ω ≥ N₀ and hence J_W > N₀: the source epoch is itself a "deep-parameter"
epoch, and it is tie-free by minimality. The conjunction {λ_Y ∈ [0,3τ+1], 2^{N₀} | 3τ+4+λ_Y,
ω < J_W ≤ log₂(3nP(n)+4)}, together with CLOCK, is *satisfiable* (Lemma 3 gives an explicit model;
(b) is satisfied there with J_W = ω+1). So minimality gives **no contradiction**.
(d) *Descent:* iterating (b) produces a tower of epochs J = J⁰ > J¹ > … > J^m (strictly decreasing
fire parameters), each with a chain of parameter ≥ N₀, plus at each level the source parameter
n'_i ≤ log₂(6τ(n_i)+5). The tower terminates (positive integers) at an epoch whose chain of
parameter ≥ N₀ is followed by a type-a or type-b step. This is a *structure*, not a contradiction;
it is exactly the "nested shifted copies" obstruction of PROOF_EXT §5 / work_claude_shifted §6.

**5.2 Best available bound on ω in terms of source data [A].** Three bounds are available and none
closes R1:
 (i) *Margin/S1 + minimality:* ω < σ_{t'+1} = v₂(c′_W) and the copied chain's record is
     ω+Γ_W < J_W, while J_W ≤ log₂(3n_T P(n_T)+4). So ω < min(n_T−ε(n_T), J_W−Γ_W).
 (ii) *Lemma T:* at the source epoch's chains, λ_x = α_xλ_u+β_x with v₂(α_x) = J_W−Γ and
     1 ≤ β_x ≤ 6d−1; this bounds the *small part*, but a valuation tie v₂(α_xλ_u) = v₂(β_x) can raise
     v₂(λ_x) arbitrarily, so it yields no upper bound on ω.
 (iii) *Lemma 9/10 (sharper):* ω = v₂(A−2^{n'}λ_u) with A ≤ 6τ(n)+4 and n' ≤ log₂(6τ(n)+5):
     ω = v₂(A) if v₂(A) < n', else ω ≥ n'. This is the only bound that constrains ω by *table data
     alone* in the case realized by all computed crossings.

**5.2b The mass identity gives λ_Y exactly, not just an inequality [A].** Lemma 9 determines
λ_Y = 3s − 3τ(n') − 2^{n'}λ_u exactly, and λ'_W = A − 2^{n'}λ_u. A lower bound for λ_Y *is* not
available from the mass identity beyond λ_Y ≥ 0 (λ_A ≤ 3s+1); in the data the ratio λ_Y/(3τ+4) stays below 1/2
(numerical maximum 133820239/267640489 at n = 99,999,929; the deep-range maximum is the same). The useful arithmetic is the exact identity,
not an inequality.

**5.3 What does *not* yield a proof.** (i) Size: λ'_W ≤ 6τ+5 and CLOCK allow τ(n) up to nP(n), so
nothing forbids 2^{N₀} | λ'_W for n ≈ 2^{N₀}/poly. (ii) Minimality: see 5.1(c),(d).
(iii) Automaton/margin arguments are λ_u-uniform and cannot decide a congruence at an astronomical
index (this is the standard limitation recorded in PROOF_EXT §5, work_deep §4).

---

## 6. If R1 fails: the continuation, and which accepted result covers which case

Let T be a deep chain with X(n_T) odd of type c, ω ≥ N₀, and write D := θ_{T+1} (Lemma 2).

(a) **Records.** By Lemma 1, R_{T+1} = R_T − (σ−ω) ≤ R_T−1 with Γ_{T+1} = Γ_T+1+ε(n_T). So the step
creates no EXT-tie; the EXT budget argument (PROOF_EXT Theorem L′) is untouched. What is lost is only
the drift bound |θ| ≤ 6Λ+4, i.e. DEEP(i), i.e. the size control that makes R2's certificate
(work_deep Theorem 3.1, work_claude_shifted Prop 3.2) applicable at the landing.

(b) **Case |D| > B** (DEEP(i) fails at T+1, R1\* fails). Accepted coverage: the generic walk rules
(PROOF_EXT §2) and Theorem SC of work_claude_shifted (the θ̃-walk is exact until the first NT
failure; records are non-increasing at descents) apply; Lemma 2.4's *count* still applies to chains
with |θ| ≤ B. What is unavailable is the deep trichotomy at T+1 (|3k+θ| < 2^{j−2} is not implied by
|θ| ≤ 2^{ω−1}). The only accepted tool controlling a walk that leaves the deep segment with a large
θ is the non-descent budget, Theorem L′ (ND-EXIT ⟹ EXT). Nothing in the accepted corpus reduces this
case to an earlier EXT instance: it is the open "shifted copies" core of PROOF_EXT §5 / §6.

(c) **Case |D| ≤ B** (the "mild" R1 failure, R1\* does not fail at T). Chain T+1 is deep, so
Lemma 2.2 (work_deep) applies at it: no NT failure, parameters descend by ≤ L, records decrease.
The drift budget must be re-established; Prop. 4 shows how much room is needed
(|D| ≤ B−6Λ−3 suffices for the whole initial deep segment). Lemma 2's exact condition says exactly
when this happens: ρ_ω ≤ B or ρ_ω ≥ 2^ω−B, i.e. **a near-congruence on λ_Y ≡ θ_T−1 (mod 2^ω)**.
So a proof of R1\* can be replaced by a proof that at every deep c-step this residue is far from 0 —
again a calendar statement, but on the *landing* class rather than on the parameter.

(d) **Why the accepted transfer lemmas do not close the case [C, with [A] content].** After an
R1-failing step the outer record is R_{T+1} = ω+Γ_T+1+ε(n_T) ≥ N₀+Γ_T+2, while the copied source
epoch has precision σ_{t'+1} = σ = n_T−ε(n_T) at the corresponding chain. The HP comparison
(PROOF_EXT §2) needs the outer records to stay below the copied precision; here it needs
ω+1+ε+Γ_T < n_T−ε, which is *not* excluded (ω < σ holds by S1), but the outer record is already
≥ N₀, so no λ_u-uniform smallness argument applies and the *certificate* route (Prop. 3.2 with a
reference representative of parameter ω) is unavailable: it would require the whole rest of the walk
to have records ≤ ω, which the data (all canonical records ≤ 4) never has at such a scale. So the
A-SOURCE / DR / OB / duration lemmas of work_ext_roots and work_claude_ext_next do not reduce this
case to an earlier EXT instance. I found no such reduction.

---

## 7. Canonical data [B]

All numbers are exact integer arithmetic on the cached canonical tables
`D:\math_cc_astra\deep1\table_100000000.pkl` (N = 10⁸, built by
`work_global_ext/route_c/fdata.py::lam_walk`) and on the instrumented walk of
`verify_R1_src.py` (same algorithm, plus the exact source chain of every type-c crossing;
both identities of Lemma 9 checked for every crossing).

**7.1 Type-c, all odd crossings n < 10⁸ (1,584,898) and the deep range [2·10⁷, 10⁸) (1,267,918).**

| quantity | all n<10⁸ | deep [N₀,10⁸) |
|---|---|---|
| odd type-c crossings | 1,584,898 | 1,267,918 |
| ω histogram | {1: 188211, 3: 1393964, 5: 2723} | {1: 150569, 3: 1115171, 5: 2178} |
| max ω | 5 (at n=6132) | 5 (at n=20,023,896) |
| #{ω ≥ 16,20,24,28,32,40,48,64} | all 0 | all 0 |
| max τ(n) | 89,213,529 (n=99,999,965) | 89,213,529 (n=99,999,965) |
| λ_Y ≤ 3τ+1 violations | 0 | 0 |
| max (λ_Y − 3τ) | −86 (n=65) | −26,764,118 (n=20,000,038) |
| max λ_Y/(3τ+4) | 133820239/267640489 ≈ 0.50000 (n=99,999,929) | same |
| 2^{N₀} divides λ'_W ever? | **no** (max ω = 5) | **no** (max ω = 5) |

**Control, type b** (ω = v₂(3τ+4)): 30,288,015 odd crossings (24,230,413 deep); ω ≤ 26, geometric
histogram {1: 10865207, 2: 8358321, 3: 5488724, 4: 2787839, 5: 1393962, …}; #(ω≥24) = 5, #(ω≥28) = 0.
So the type-c ω is *not* a generic geometric variable: it is bounded by 5 and takes only odd values.

**7.2 Lemma 9 / Lemma 10 on the table.** Source chain found for all 1,584,898 crossings; both
identities λ_A = 2^{n'}λ_u+3τ(n')+1 and λ'_W = A−2^{n'}λ_u hold at **all** of them (0 failures).
Source parameters n' (all / deep): {4: 1396684, 7: 174246, 11: 10891, 13: 2723, 16: 340, 21: 11,
23: 3} / {4: 1117347, 7: 139397, 11: 8713, 13: 2178, 16: 272, 21: 9, 23: 2}. Joint (n', ω):
(4,1): 2723, (4,3): 1393961, (7,1): 174246, (11,1): 10891, (13,5): 2723, (16,1): 340, (21,1): 11,
(23,3): 3 — the joint is rigid: n' = 4 gives ω ∈ {1,3}, n' = 13 gives ω = 5, n' = 7, 11, 16, 21 give
ω = 1, n' = 23 gives ω = 3, exactly as Lemma 10 predicts (ω = v₂(A) when v₂(A) < n').

**Cancellation statistics.** 2^{n'} | A: **0 / 1,584,898** (deep 0 / 1,267,918). v₂(A) = ω ∈ {1,3,5};
min(n' − v₂(A)) = 1; max A = 535,281,166 (29 bits), min A = 328 > 0. So (NC) holds throughout, and by
Corollary 11 R1's failure at any of these 1.27M deep type-c crossings is equivalent to
2^{N₀} | A — which is impossible there since A < 2²⁹ ≪ 2^{N₀}. **Every ω = 5 crossing has n' = 13 and
τ(n) ≡ 31 (mod 64)** (all 2,723 of them), a further indication of the arithmetic rigidity of the
crossing calendar.

**Every scanned crossing obeys R1** (ω ≤ 5 < N₀ = 2·10⁷ at all 1,267,918 deep odd type-c
crossings, and at every crossing of the whole table); the structural form of the statement is in 7.2.

**7.3 Landing classes (direction C data).** For every deep type-c crossing and θ_T ∈ [−30,30] the
would-be landing class is δ = θ_T + 3τ + 3 − 2^ω (mod 2^{ω+1}). certify(ω, δ) computed exactly:
- θ_T = 1: **0 failures** in 1,267,918;
- θ_T ∈ [−30,30]: 2,178 crossings have at least one failing θ (exactly the count of ω = 5 crossings);
  the exhaustive Bad sets are Bad₁ = Bad₃ = ∅, Bad₅ = {5, 21, 37, 53} (mod 64) = the first-chain tie
  classes of work_deep. All 2,178 ω = 5 crossings have base ≡ 0 (mod 64) (equivalently τ(n) ≡ 31 mod 64),
  so their failing θ in the window are exactly θ_T ≡ 6 (mod 16), i.e. {−26, −10, 6, 22}.

**7.4 Exact big-integer walks.** (i) From j = 100,065 at the c-crossings n = 100,064, 100,136, …
the exact walk (genuine c'_W from the full pair map) reproduces Lemma 1 and Lemma 2 exactly:
ω = 3, σ = 100,061, so R drops 100,065 → 7 (= ω+Γ'), and θ' equals (θ_T+3τ+3) mod 2^ω for
δ = 1 and δ = −1 (θ_pred = θ_act = 1 resp. 7). (ii) At the deep boundary j = 20,000,005,
20,000,008, 20,000,013 (odd-a crossings) the exact a-step obeys j' = 1+v₂(3k+δ) (v₂z = 3,0,0 → j' = 4,1,1).
(A deep c-step cannot be run with full integers — c'_W at index ≈ 2·10⁷ would need a pair walk of
2^{2·10⁷}-bit integers — so Lemma 1/2 at deep c-steps rest on [A] plus the table identities.)

---

## 8. What is proved / not proved

**Proved [A] (unreviewed; hypotheses stated in place).**
Lemma 1 (c-step ledger: record drop σ−ω, loss 1+ε, parameter drop). Lemma 2 (exact new defect and the
condition for staying deep). Lemma 3 (consistency model: no inequality forces |θ_{T+1}| > B).
Prop. 4 (R1-C ⟹ DEEP(i) on the initial deep segment). Remark 5 (intermediate controlled regime).
Lemma 6 ((i) definitional equivalence; (ii) R1 ⟺ (CAL-C); (iii) size consequence and the automatic
range n < 2^{N₀−64}). Lemma 9 (source identity: λ'_W = A−2^{n'}λ_u, n' ≤ log₂(6τ+5)). Lemma 10
(dichotomy). Corollary 11 (R1's failure is SIZE or CANCEL; under (NC), R1 ⟺ (CAL-C′)).
Section 5.1 (minimality gives ω < J_W, no contradiction). Section 6 (what R1 does and does not buy).

**Verified [B].** Section 7 (N = 10⁸, deep boundary 2·10⁷, exact integers; the ranges and counts as
stated; the identity checks are complete over those ranges, not sampled).

**Not proved.** R1; R1\*; R1-C; (CAL-C); (CAL-C′); (NC); DEEP(i) for J ≥ T_{h*}. No EXT claim, no
horizon change (K_clock unchanged), no statement about the machine. No counterexample or obstruction
to R1 was found: R1 holds with an enormous margin (ω ≤ 5 versus N₀ = 2·10⁷) everywhere the canonical
table reaches.

**The single most promising next step** (see REPORT.md): prove (NC), i.e. v₂(6τ(n)+4−3τ(n')) < n'
at every type-c crossing, which would reduce R1 to the pure τ-congruence (CAL-C′) and eliminate λ_u;
then attack (CAL-C′) with the calendar/clock machinery (numbers: A ≤ 6τ(n)+4, n' ≤ log₂(6τ(n)+5)).

---

## 9. Reproduce (measured runtimes, Windows, `python -B`)

```
# 1. instrumented canonical walk: exact source chain of every type-c crossing (Lemma 9), 70.8 s
python -B verify_R1_src.py 100000000 D:/math_cc_astra/r1r2/agent_R1/src_100000000.pkl
python -B verify_R1_src.py  20000000 D:/math_cc_astra/r1r2/agent_R1/src_20000000.pkl   # 13.1 s

# 2. omega / lambda_Y distributions, congruence structure, landing classes, exact walks, 51.8 s
python -B verify_R1.py D:/math_cc_astra/deep1/table_100000000.pkl 20000000
#    small sanity run on table_1000000.pkl (16.2 s): writes verify_R1_table_1000000.json

# 3. summarise the source maps (cancellation statistics), 1.5 s
python -B verify_R1_summary.py D:/math_cc_astra/r1r2/agent_R1/src_20000000.pkl \
                               D:/math_cc_astra/r1r2/agent_R1/src_100000000.pkl
```

Outputs beside the scripts: `verify_R1_table_100000000.json`, `verify_R1_table_1000000.json`,
`verify_R1_src_summary.json`. The 2.8 GB table and the source maps live in
`D:\math_cc_astra\r1r2\agent_R1\` and `D:\math_cc_astra\deep1\` (outside the repository).
Runtime total for the runs above: ≈ 2 min (the 10⁸ table loads in 3.7 s from the page cache).
No repository file outside `work_r1r2/agent_R1/` was written; no git operations were performed.
