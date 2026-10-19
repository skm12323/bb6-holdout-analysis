# 已通过三方审查 / accepted (reviews/claude_shifted_review_record.md) — shifted chains are θ̃-walks: DH → NT, the WITNESS, a window certificate, and the deep residue (Claude, 2026-10-19)

## 中文摘要

- claude_ext_next 的低位相差 d=Θ−x 与 PROOF_EL 的 θ̃（Θ mod 2^j）是同一个量（x≡0 mod 2^j）。其"下降假设" DH
  (v2(6k+2d)<j−1) 严格强于 PROOF_EL 的 NT (3k+d≢2^{j−2} mod 2^{j−1})：两者之差恰是"一步下降" j'=j−1
  （含共振 6k+2d=0），它保持记录 j+Λ 不变且自动机仍正确（mod 2^{j'}）。所以 DH 可以全部换成 NT（DR 末字母与 OB 的 DH_out 除外），审查中提到的
  "需要 k_j>|d|/3 的下界"并不需要。[A]
- **题目所要求的 "所有尺度 DH" 与 "移位参考状态（H_5 族，副本结束后的 a 输出）中不出现第一个非下降" 都是假的**：已接受的 PROOF_SPECTRUM §4 WITNESS
  实际 epoch (p3,p2,p1,17,5,6,1) 中，H_5(17) 这个移位参考状态实际出现并在 j=5 处非下降 (5→6)；位于其 a 返回处的
  c 交叉具有历史 BBBAA（亏损 11），其最后一个 A 字母 DH 与 NT 都失败，DR 归约失效（正是旧扫描中 m=5, δ=−3 的
  "失败"）。但其记录仍严格低于精度。因此正确目标只能是"记录低于精度"，不能是"不下降"。[A，依赖已接受结果]
- 定理 SC：任何移位链（任意整状态）在第一次 NT 失败之前就是 θ̃-游走，记录不增；G_δ(p)/H_e(m) 在第一次 NT 失败之前
  （以及对被证书覆盖的 (v2(z),δ) 全程）只依赖 (v2(z), δ)，与 p 无关；对未覆盖的裸 tie (5,5)、(5,−11)，结果由 z 的高位决定。[A] 再加 HP：若代表元 (2^j, 2^j+δ) 的精确游走以记录 ≤ j 结束，则所有该类状态都闭合。[A]
- 有限证书 [B]：对 6≤j<2·10^7、δ∈[−12,15] 的全部 (j,δ)（其中约 111.6 万个 NT 失败对）都被证书覆盖（记录 ≤ j）；
  唯一未覆盖的是 j=5、δ≡5 (mod 16) 的"裸 tie"。j≤18 时对全部剩余类 mod 2^{j+1} 也算了：未覆盖类只在奇 a 参数
  j∈{5,8,12,14,17} 出现，每个 ≤8 个。
- 推论 [A+B]：G_δ/H_e（含 MINUS、PLUS、Z=H_0、H_3、G_4 等）凡 δ∈[−12,15]、6≤v2(z)<min(p−1,2·10^7) 的成员全部闭合；
  定理 W：任意 J，若 X(J−1) 为奇 c 型、ω(J−1)<2·10^7 且 −λ_Y mod 2^{ω+1} 落在证书集内，则 S(J) 无 tie
  （不需 J_W<K′，不需 EXT 下界，不需 DH）。
- 剩余（充分条件 DEEP）：在 |θ̃|≤2^{10^7} 且 θ̃≠−3k_j 的条件下，S(J) 中参数 ≥2·10^7 的链只有开头的至多
  h(J)≈log* J 条；DEEP（深段 θ̃ 有界、第一次进入表内时的精确亏损 mod 2^{j+1} 落在证书集里）蕴含 EXT（是充分条件，
  不声称是精确的剩余部分）。深段读取的是天文数字下标处的交叉数据，WITNESS 型的 fire 塔
  显示这种落点（含 tie）确实会发生，所以任何证明都必须处理 tie 的消解（本文给出门口 tie 消解引理）。
- 没有证明 EXT，没有改变视界 K_clock。

Tags: [A] proved for all parameters (hypotheses stated), [B] finite exact computation (range stated), [C] conjecture/data.
Script: `verify_shifted.py` (writes `shifted_checks.json`), library `shiftlib.py`.
Notation as in PROOF_EXT §2 (walk rules), PROOF_EL A1–A3 (θ̃), claude_ext_next NOTES (G_δ, H_e, automaton).
A state is (j, Θ, x), x = 2^j u, u odd; n = j−1; k = k_n = τ(n)/2 at odd type-a crossings; Φ(n) := 3τ(n)+5−λ'_W(n)
is the exact defect of W's chain at τ(n) (= θ̃^W of PROOF_EL A3; for type b Φ = 1, for type c Φ = 1−λ_Y).
The record of chain t is j_t + Λ_t (Λ = accumulated 1+ε); "closes at precision P" means: ends at an even return with
every record < P (HP).

## 1. Dictionary and the replacement DH → NT [A]

**1.1 (identity).** For any state, Θ − x ≡ Θ (mod 2^j). So the defect d of claude_ext_next, read mod 2^j, is the θ
of PROOF_EL A1–A3, and the automaton (fire 1, A: 3−d, B: d−1, C(w): d+Φ(w)−2) is PROOF_EL's θ̃-automaton (A3).

**1.2 (DH vs NT).** At an a-step at parameter j: DH ⇔ v2(3k+d) < j−2. NT (PROOF_EL A2) ⇔ v2(3k+d) ≠ j−2
(read mod 2^{j−1}). Hence DH ⇔ NT ∧ ¬(v2(3k+d) ≥ j−1).

**Lemma 1.3 (one-step descents are harmless).** Let the exact defect D = Θ−x satisfy D ≡ d (mod 2^j) and let
v2(3k+d) ≥ j−1 (this includes the resonance 6k+2d = 0). Then j' = j−1 exactly, the record j+Λ is unchanged, and
D' ≡ 3−d (mod 2^{j'}).
*Proof.* x' = 2Θ+6k−x/2 = (6k+2D) + 3x/2. 6k+2D ≡ 6k+2d (mod 2^{j+1}) has valuation ≥ j, and 3x/2 has valuation
exactly j−1, so v2(x') = j−1. D' = Θ+3+6k−x' = 3−D−x/2, and x/2 ≡ 0 (mod 2^{j−1}). Λ increases by 1. ∎

**Corollary 1.4.** In LOW and P2, and in DR/OB except at the places listed below, DH can be replaced by NT, with
LOW's congruence read mod 2^{j} (PROOF_EL A3) instead of mod 2^{j+1}, and LOW's descent statement "a: by ≥ 2"
weakened to "a: by ≥ 1" (b/c: by ≥ 3 unchanged). **Lift bit:** after a one-step descent, D' ≡ 3−d (mod 2^{j'}) but
D' ≡ 3−d+2^{j'} (mod 2^{j'+1}) (from D' = 3−D−x/2 with x/2 ≡ 2^{j−1} mod 2^j). Hence:
* **P2** after a one-step descent: D_i ≡ 2+2^{j_i} (mod 2^{j_i+1}), so the comparison with R0 = (x_{D_i}, x_{D_i}+2)
  has precision π_i = j_i exactly, not ≥ j_i+1. The conclusion survives: δx_0 = 0 (same x), so after the first step
  δx' = 2δΘ (a) or 0 (b/c), with δΘ unchanged and v2 δΘ ≥ j_i; thus v2 δx_1 ≥ j_i+1 at an a-step (resp. δx_1 = 0)
  while j_1 < j_i, and from chain 1 on the usual HP applies with precision j_i + 1 − loss ≥ j_1 + 1. (HP variant: if
  δx_0 = 0, chain 0 needs only v2 δΘ_0 ≥ P − 1.)
* **Exceptions (NT does not suffice):** (i) DR's requirement v2(z) < p−1 on the *final* letter; (ii) OB's DH_out:
  if v2(3k+d−1) ≥ m−1 then j_out = m−1 equals the precision, so OB step 4 gives no margin.
In case (i): when the final letter is a one-step descent (or an NT failure) the outer chain has
parameter ≥ p−1 and the reference G_δ(p) is useless — this is exactly the m=5, δ=−3 "failure" of the old scans, and it
is realized (§2). Such sources must be treated by Theorem SC/W directly (§3–4), not by DR. The review's request for a
lower bound k_j > |d|/3 (to exclude 6k+2d = 0) is unnecessary: that resonance is a one-step descent.

## 2. The target as posed is false at actually arising letters [A, relative to accepted PROOF_SPECTRUM §4]

PROOF_SPECTRUM §4 (accepted, g2_obstruction review) constructs an actual epoch with exit parameters
(p3, p2, p1, 17, 5, 6, 1) (returns b, b, b, a, a, b, even), p1 = 244875, all inside the certified horizon.

* Its chain at 17 has θ̃ = −2 (three b-copies drift 1→0→−1→−2). The a-step gives the state (5, θ̃ = 5): this is the
  shifted reference H_5(17) = (6k_17+6−10, 6k_17+6−5) = (32, 37) of claude_ext_next (a-output of a defect −2 state).
  At (5,5): 3k_5+5 = 8 = 2^{j−2}: **NT fails, DH fails** (v2(6k+2d) = 4 = j−1), and the next parameter is 6 > 5 —
  a first non-descent in a shifted reference state. (Precisely: by PROOF_EL Remark S the b-copy ends at the a-return
  from 17, so (5,5) is the a-output after the copy ends, i.e. a member of the H_5 family, not a state inside the
  copy itself.) The rescue macro (PROOF_RESCUE §2) resolves it: 17→5→6→1, records
  below precision.
* Exact indices. Let ρ be the pointer of the WITNESS fire (parameter p3). The fire reads E_ρ, E_{ρ+1} (X(ρ) type a,
  X(ρ+1) type b). By PROOF_M Lemma 3.3 a chain t′ ≥ 1 reads a new original iff the return of chain t′−1 is type a,
  and the pointer after the a-return following chain t is ρ+2+a_t. Chain 3 (j=17) returns a (reads X(16)), so chain 4
  (j=5) reads E_{ρ+2}: X(ρ+2) is an odd type-c crossing (history BBBA, ε = 3+0+6 = 9). Chain 4 returns a (reads X(4),
  type a), so chain 5 (j=6) reads E_{ρ+3}: **X(ρ+3) is an odd type-c crossing** (odd because chain 5 fires), whose
  W-chain at τ(ρ+3) is chain 5 itself (Lemma K(c)), ω(ρ+3) = 6, history **BBBAA**, deficit ε = 3+a_4+Γ_4 = 3+1+7 = 11
  = W+1. (Chain 5 then reads X(5), type b; that is the return of chain 5, not a source.) So X(ρ+3) is an actual c
  crossing whose source chain D_t is the 6-chain and whose source history is BBBAA — the "source" in the sense of
  claude_ext_next §3 (the letters of its own epoch up to its a-return), not a pending entry Y. Its final A letter is the
  (5,5) step: DH fails at an actually arising A letter, and DR's reduction to G_{−3}(5) (z = 16, v2 = 4 = p−1)
  has no margin. The old scan "failure" (m=5, δ=−3) is therefore a realized configuration, not a virtual one. It is harmless:
  that c crossing has index far below K″ (p3 < 2^(2^244879)), so S(J) for it is tie-free by PROOF_EXT Corollary 4;
  only the DR route fails there. Explicitly: the outer chain 1 of S(ρ+4) is V(D_t,−1) with j = 6, whereas DR's
  reference G_{−3}(5) has v2(z) = 4.

Consequently "DH holds at all scales at actually arising A letters" and "no first non-descent in a shifted
reference state (family H_5)" are **false** (inside the accepted horizon; the same fire-tower construction is available at any level where fires of
all parameters exist). What can be true is the weaker statement that records stay below precision, which the
WITNESS satisfies. Every route to EXT must resolve ties of the class (5, θ̃ ≡ 5 mod 16) rather than exclude them.

## 3. Theorem SC: shifted chains are θ̃-walks; references depend only on (v2(z), δ) [A]

**θ̃-walk** on pairs (j, d mod 2^j) (PROOF_EL A1–A3 with Lemma 1.3): stop if j ≤ 4 (X(0..3) even) or X(j−1) even;
type a: z = 3k+d; v2(z) = j−2 → **NT failure** (stop, "ND"); v2(z) ≥ j−1 → j' = j−1; else j' = 1+v2(z); d' = 3−d.
type b/c: j' = ω(n), d' = d + Φ(n) − 2.

**Theorem SC.** Let (j0, Θ0, x0) be any integer state (no hypothesis on its origin) and d0 = (Θ0−x0) mod 2^{j0}.
Until the first NT failure of the θ̃-walk from (j0, d0), the exact walk has the same parameters and types, its exact
defect is ≡ the θ̃-value mod 2^j at every chain, and its records are non-increasing (strictly decreasing at b/c steps
and at descents by ≥ 2). If the θ̃-walk ends without NT failure, every record of the exact walk is ≤ j0.
*Proof.* Induction over chains. a-step: PROOF_EL A2 (two-step descent and NT) and Lemma 1.3 (one-step descent).
b/c-step: x' = c'_W(n)u + λ'_W(n), j' = ω(n) since v2 c' = n−ε > ω (W's S1); exact
D' = D + Φ(n) − 2 + u(2^j − c'), and v2(2^j − c') = n−1 (b, c' = 3·2^{n−1}) resp. n−ε (c, 2^j − c' = c_A), both
≥ ω+1. Records: b/c: j' ≤ j−2−ε and Λ grows by 1+ε; a: j' ≤ j−1, Λ grows by 1. ∎

**Corollary 3.1 (references).** For G_δ(p) (z = 6k_p+4−2δ, Θ = z+δ) and H_e(m) (z = 6k_m+6−2e, Θ = z+e), with z ≠ 0
and j0 := v2(z) < precision: the walk until its first NT failure is the θ̃-walk from (j0, δ) — independent of p
(resp. m) except through j0. If it has no NT failure the reference closes with records ≤ j0. So, up to the first NT
failure — and for the whole walk when (j0, δ) is certified (Prop. 3.2) — a family member's fate is a property of the
pair (j0, δ) only. For the uncertified bare ties (5, 5), (5, −11) the outcome depends on higher bits of z (hence on p). (HP needs x* ≠ 0, not x* > 0:
the positive-cone condition z > 0 of claude_ext_next can be dropped.)

**Proposition 3.2 (minimal-information certificate).** Call (j, δ) *certified* if the exact walk from the
representative (2^j, 2^j+δ) never has x = 0, ends, and has every record ≤ j. Then every state with x ≡ 2^j and
Θ−x ≡ δ (mod 2^{j+1}) — in particular every actual state of parameter j whose defect is known mod 2^{j+1} and
whose precision exceeds j — follows the same parameters and types, ends, and has records ≤ j.
For j ≥ 64 the equivalent one-step form is used (this threshold is the one in `certify`; the separate threshold
3000 in the V4 NT-failure scan only decides where the θ̃-walk is memoized): after the first step every true successor agrees with the small
representative (6k+2δ, 6k+δ+3) (type a) resp. (λ'_W(n), 3τ(n)+3+δ) (b/c) modulo 2^{j−loss}, and HP is applied
with that precision.
*Proof.* HP (PROOF_EXT §2) with P = j+1: δx_0 = x−2^j and δΘ_0 = δx_0 + (D−δ) have valuation ≥ j+1. For the
one-step form: x' − (6k+2δ) = 2(D−δ) + 3x/2 has valuation ≥ j−1 = j−loss; x' − λ' = c'u has valuation n−ε = j−loss;
Θ' agrees mod 2^j. ∎

The certificate covers NT failures too: the exact walk resolves a tie whenever the available bits suffice.

## 4. Window certificate, Theorem W, family closures [B, A+B]

**[B] Certificate (`verify_shifted.py` V4, V5; tables from the certified λ-walk to index N = 2·10^7).**
For every 5 ≤ j < 2·10^7 and δ ∈ [−12, 15] the θ̃-walk was run (j < 3000 directly; j ≥ 3000: one exact step to a
parameter < 30, then the memoized table). NT failures occur only for δ ∈ {−11, −10, −2, −1, 5, 6, 14}
(1,116,397 pairs; δ = −1 only at 68 parameters, the b-crossings copying a parameter-17 fire: 244875, 538715, …;
δ = −2 at the odd-a j with v2(3k_j−2) = 4: 17, 90, 161, …).
Every NT-failure path in the window passes through (5, θ̃ ≡ 5 mod 16); the gateways are exactly:
δ = −2 / 14: a-step to (5, 5) / (5, −11); δ = 6 / −10: b-step (Φ = 1 exactly, ω = 5) to (5,5) / (5,−11); δ = 5 / −11 (545 each):
c-step (Φ ≡ 2 mod 64, ω = 5; the exact Φ = 1−λ_Y is negative, e.g. X(6132) (the gateway at j = 6133): λ_Y = 8191, Φ = −8190); δ = −1: b-step (ω = 17) to (17, −2), then the a-gateway (all 68 b-crossings with ω = 17 below
2·10^7, and only those); δ = 5 also at 68 odd-a j whose a-step lands on (17, −2). **All 1,116,395 NT-failing pairs with
j ≥ 6 are certified** (Prop. 3.2); the only uncertified window pairs are (5, 5) and (5, −11) (bare ties: at j = 5
with only j+1 known bits the tie outcome needs more bits). NT-good pairs are certified by Theorem SC; the direct
certificate of all 5 ≤ j < 3000, δ ∈ window confirms this.
For 5 ≤ j ≤ 18, **all** residues δ mod 2^{j+1} were certified except: j = 5: {5, 21, −11, −27}; j = 8: {58, 186, −70,
−198}; j = 12: {1012, 3060, −1036, −3084}; j = 14: 4 residues; j = 17: 8 residues (the tie class
3k_j+δ ≡ 2^{j−2} mod 2^{j−1}, 4 lifts; plus at j = 17 four a-step-to-(5,5) classes whose (AA) resolution needs more bits).
Direct certificate of all 5 ≤ j < 3000, δ ∈ window: 83,858 certified, 2 not ((5,5), (5,−11)).
Non-odd-a parameters (6, 7, 9, 10, 11, 13, 15, 16, 18) have no uncertified residue.

**Theorem W [A+B].** Let F be defined through τ(J−1), X(J−1) odd of type c, j_1 := ω(J−1), and r the symmetric
residue of −λ_Y mod 2^{j_1+1} (λ_Y the λ-part of the pending entry at X(J−1)). If either
(i) 6 ≤ j_1 < 2·10^7 and r ∈ [−12, 15], or (ii) j_1 = 5 and r ∈ [−12, 15] \ {5, −11}, or (iii) j_1 ≤ 18 and r is not
one of the listed uncertified residues, then S(J) is tie-free.
*Proof.* Chain 1 of S(J) is V(C, −1) (Prop RB) with exact defect Θ_1 − x_1 = −λ_Y (ENTRY, PROOF_EXT_ROOTS §1),
parameter j_1 and record j_1 + Γ_1 < J (RB). In the β-walk (Lemma BR, exact while tie-free) the defect is an exact
integer, so Prop. 3.2 applies with the [B] certificate: records after chain 1 are ≤ j_1 + Γ_1 < J. ∎
No hypothesis on J_W, on EXT below J, on DH or on NT in the source is used. (Type b: chain 1 is (ω, 0); certified for
ω < 2·10^7 — already contained in Theorem S(c).)

**Corollary 4.1 (families) [A+B].** Every G_δ(p) and H_e(m) with δ (resp. e) ∈ [−12, 15], z ≠ 0 and
6 ≤ v2(z) < min(precision, 2·10^7) closes with records ≤ v2(z); for v2(z) = 5 the same holds unless δ ≡ 5 (mod 16).
This includes MINUS = G_{−1} (whose 68 NT-failing parameters are certified), PLUS = G_3, G_4 (BBBA), G_{−2}
(BBAA), H_3 (outer b at t=0), H_0 = Z(q), and every open δ produced by deficits ε ≤ 27
(−(ε−3)/2 ≤ δ ≤ (ε−1)/2, claude_ext_next §4). [B, V3] All 56 families for odd-a m < 10^6 agree with this
(exact reference walk = θ̃-walk until NT failure; every certified member closes).

**Consequence at a least counterexample.** With Theorem S(d) (J_W < K′) and Theorem W, a least strict-EXT
counterexample of type c needs J_W ≥ K′ **and** one of: ω(J−1) ≥ 2·10^7; or −λ_Y mod 2^{ω+1} outside the certified
set; or the bare tie (5, ≡5 mod 16). Under NT in the source epoch, −λ_Y ≡ Φ(w)−1 holds only **mod 2^ω**
(|Φ(w)−3/2| ≤ (ε−2)/2); mod 2^{ω+1} it is Φ(w)−1 or Φ(w)−1+2^ω, the latter when the final source letter is a
one-step descent. This lift bit does not matter: for NT-good classes Theorem SC uses only the class mod 2^j, and
[B] for all 166 NT-failing certified window pairs with 5 ≤ j < 3000, (j, δ+2^j) is also certified (re-checked).
So for ω < 3000 an out-of-certificate entry needs Φ(w)−1 outside [−12,15] mod 2^ω, i.e. deficit ε(J−1) ≥ 29,
or a source tie; for 3000 ≤ ω < 2·10^7 the same holds under the additional hypothesis "no one-step descent at the
final source letter" (the lift δ+2^ω was not scanned there).

## 5. Gateway ties resolve with a net descent [A; thresholds A+B / conditional, see end]

Every NT failure in the window enters j = 5 from a predecessor ("gateway"). If the predecessor has parameter j_p,
defect D_p ≡ θ_p (mod 2^{j_p}) and precision > j_p, the tie is resolved without further information:

* **a-gateway** (a-return from j_p to 5, then the tie a-return at 5, l = k_5 = 1): by the exact identity (AA) of
  PROOF_RESCUE §1, x_2 = D_p + 12 + 9k + 5·2^{j_p−2}u_p. So j_2 = v2(θ_p+12+9k) whenever this is < j_p−2, and
  θ_2 ≡ θ_p + 12 + 6k (mod 2^{j_2}).
* **b/c-gateway** (b/c-return from n = j_p−1 with ω(n) = 5): x_5 = c'u_p + λ', Θ_5 = Θ_p+3+3τ(n), so
  x_2 = 2Θ_5+6−x_5/2 = Q + u_p(2^{j_p+1} − c'/2), Q := 2D_p + 12 + 6τ(n) − λ'(n)/2, v2(c'/2) = j_p−2−ε.
  So j_2 = v2(Q) whenever this is < j_p−2−ε, and θ_2 ≡ θ_p + 12 + 3τ(n) (mod 2^{j_2}).

In both cases the record after the pair is j_2 + Λ_p + 2 + ε_gate < j_p + Λ_p: the pair is a net descent.
Sizes: take |θ_p| ≤ (j_p−2)/2. Then Q ≠ 0 (b: Q = 2D_p+10+4.5τ(n); c: Q = 2D_p+10+4.5τ(n)−λ_Y/2 with
λ_Y ≤ 3τ(n)+1; and τ(n) ≥ (n−1)/2), likewise θ_p+12+9k ≥ 12 + 9(j_p−2)/4 − (j_p−2)/2 > 0, and
|Q|, |θ_p+12+9k| ≤ 14τ(n) + j_p + 12. Thresholds: [A+B] with V2's τ ≤ n and ε ≤ 7 (n ≤ 10^8) the
valuation condition holds for j_p ≥ 20 (the bounds already work from j_p ≥ 16). In general: a- and b-gateways need
only CLOCK (τ ≤ nP(n); ε ∈ {0,1}); c-gateways also need C2-log for ε(n), which requires S(J_W) tie-free for the
copied epoch — true at a least counterexample (J_W < J) or for J_W < K″ — and under that hypothesis j_p ≥ 60
suffices (the bounds already work from j_p ≥ 44). This generalizes PROOF_RESCUE's two-step lemma (a-gateway, |θ| ≤ 10) to b/c gateways
(PROOF_SPECTRUM §6's parent-65 computation is the instance n = 64). The new state (j_2, θ_2) is generally *not* in a
small window: after a resolved tie the defect is a residue determined by k or τ(n).

## 6. What remains: a single deep statement

**Lemma 6.1 (deep segment) [A].** At a chain with parameter j ≥ N_0 := 2·10^7 and |θ̃| ≤ 2^{N_0/2}:
|3k_j+θ̃| < 2^{j−2} (CLOCK: 3k_j ≤ 1.5 jP(j)), so NT holds and the record does not increase (Theorem SC). If moreover
θ̃ ≠ −3k_j (automatic when |θ̃| < 3(j−2)/4, since k_j ≥ (j−2)/4 by τ(n) ≥ (n−1)/2), then
j' ≤ L(j) := log2(6jP(j) + 2|θ̃| + 5) (b/c: ω(n) ≤ log2 λ'_W(n) ≤ log2(6τ(n)+5), using λ_Y ≤ 3τ+1; a: 0 < 3k+θ̃).
Hence, while these size conditions hold, the chains of S(J) with parameter ≥ N_0 form an initial segment of
length ≤ h(J) := min{h : L^{(h)}(J) < N_0} (an iterated-logarithm count, growing like log* J).

**Reduction [A+B].** EXT(J) holds whenever
(DEEP) the chains of S(J) with parameter ≥ 2·10^7 satisfy |θ̃| ≤ 2^{10^7}, and the first chain with parameter
< 2·10^7 has (j, exact defect mod 2^{j+1}) certified (window minus the bare 5-tie, or any non-listed residue for j ≤ 18).
Proof: on the deep segment NT holds (first sentence of Lemma 6.1), so records are non-increasing by Theorem SC —
including at a resonant one-step descent θ̃ = −3k_j, where j′ = j−1 and the record is unchanged (Lemma 1.3); chain 1
is tie-free by RA/RB; then Prop. 3.2 with the certificate from the first table chain on. ∎
The reduction does not use the segment-length bound. The count "at most h(J) ≈ log* J deep chains" (second part of
Lemma 6.1) holds only under the additional hypothesis θ̃ ≠ −3k_j at the deep a-steps; resonant one-step descents
(j′ = j−1, still deep) are not counted by it and are not bounded here.
For type b at a counterexample (ω ≥ K′) and type c with deep or out-of-window entry, DEEP is a statement about at
most h(J) chains (under θ̃ ≠ −3k_j; resonant one-step descents are not counted) reading crossing data at astronomically large indices: the θ̃-drift there (−1 per b-copy, Φ−2 per
c-copy, reflection at a) and the landing residue. It is a sufficient condition (not claimed to be the exact remainder) for "S1 for shifted copies"; Lemma 6.1's
segment count additionally assumes |θ̃| ≤ 2^{10^7} and θ̃ ≠ −3k_j on the deep segment.

**Why DEEP is not provable by the present tools [C, with an [A] example].** The WITNESS mechanism (fires of every
parameter exist, PROOF_SPECTRUM §3; a fire at pointer ρ makes X(ρ+1) odd b with ω = its parameter) builds, at any
tower height where fires of the needed parameters exist, deep b-chains p_{i+1} = ρ(p_i)+2 that drift θ̃ by −1 per
level and land at chosen gateways. Three levels reach the tie (WITNESS); deeper towers can reach θ̃ = −3, −4, … at
parameter 17 or 65 (four b-levels give θ̃ = −3 at 17, which is harmless: 3·6−3 = 15, j' = 1; twelve give −10 at 65,
the G2 tail 65,5,5,1 of PROOF_SPECTRUM §5, conditional there). Landings are congruence conditions on F's k-values at astronomically large indices; resolved
ties produce residues set by those k-values. Hence any proof of DEEP needs arithmetic control of the deep calendar
(which fires occur at pointers ρ with prescribed parameters), not a defect potential: the θ̃-window genuinely widens
by about 2 per tower level (PROOF_TIE2 §7), and Π = j + 2|θ̃−3/2| is only non-increasing *before* the first tie.

**Assessment [C].** The defect calculus adds no leverage beyond PROOF_EL/TIE2: G_δ/H_e are θ̃-starts, their
closure is p-independent and is settled by finite tables wherever the first parameter is < 2·10^7 and the defect is
small (§4). The open core is unchanged — the deep segment of S(J) — and it contains realized ties, so the target must
be "records below precision" with tie resolution. The most promising route I see: (1) prove a uniform gateway-tie
lemma for deep predecessors (§5 does the one-tie case) and show that after a resolved tie the walk drops below
2·10^7 with a residue avoiding the listed uncertified classes U_j (measure ≈ 8/2^{j+1} at odd-a j); (2) combine with
a calendar-arithmetic statement bounding the number of consecutive deep b/c copies (fire towers) that can feed a
gateway. Data cannot test (2): all canonical data have r ≤ 4.

## 7. Data [B]

`python -B verify_shifted.py 20000000 1000000 20000000` (see `shifted_checks.json`):
* V1: 200,000 random exact states (j0 ∈ [5,60], 80-bit bases, defects ∈ [−40,40], random high Θ bits): the exact
  walk equals the θ̃-walk until the first NT failure (445 failures; at each the exact next parameter is ≥ j), records
  non-increasing in all 199,555 NT-good walks.
* V2: S(J) for all 12,432,184 indices 5 ≤ J < 2·10^7 with X(J−1) odd: β-walk (Lemma BR) = θ̃-walk from (J,1);
  **0 DH failures, 0 NT failures**; θ̃ at a-steps only ∈ {0, 1, 2}.
* V3: 56 families G_δ, H_e (δ ∈ [−12,15]) at all 302,878 odd-a m < 10^6: exact reference walk = θ̃-walk until NT
  failure; 16,905,426 NT-good members (records ≤ v2(z), all close); 55,730 NT-failing members (G_5, G_{−11}, H_5,
  H_{−11}, 4 of G_{−2}, 3 of H_{−2}) — all close; 987,964 certified members, all close; 6 members with
  v2(z) ≥ m−1 (m = 5, no DR margin) and 6 with z = 0. No member fails.
* V4/V5: as in §4. V6: the WITNESS tail (17,−2) → (5,5) [NT and DH fail] → certified word 17,5,6,1.

## 8. What is proved / not proved

Proved [A] (unreviewed): Lemma 1.3 and the DH→NT replacement; Theorem SC; Prop. 3.2; gateway-tie lemma (§5);
Lemma 6.1 and the DEEP reduction. [A, relative to accepted PROOF_SPECTRUM §4]: DH and "no first non-descent in a shifted reference state (H_5 family)" fail at actually arising letters, so the posed target is false as stated. [A+B]: Theorem W,
Corollary 4.1 (family closures for window defects and first parameter < 2·10^7).
Not proved: EXT; DEEP; any statement for first parameters ≥ 2·10^7 or defects outside the window. K_clock unchanged.
