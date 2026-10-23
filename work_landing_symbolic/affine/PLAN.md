# Affine-origin landing criterion — PLAN (planning round; no verification script written)

2026-10-23. Direction A (affine origin) of the landing-symbolic workflow.
Status of this file: **plan only**. No verifier was written or run in this round; every
statement below is a *draft* with its intended tag. Part of it is already proved in this
file (the algebraic lemmas); part is conditional on accepted imports; the computational
parts are specified but not executed. No global EXT claim; K_clock untouched; no other
directory modified; no git commit.

**Revision 2026-10-23 (post-implementation):** the statement is unchanged; four
interpretation points were clarified after running `verify_affine.py` (all PASS).
See §12. The headline clarification is that `J` is the *current record* at the chain
(re-anchoring: `J=j+Gamma`), not necessarily the source epoch's root parameter; this is
already allowed by the statement (it is an arbitrary affine origin), and it is the
reading the canonical verifier uses.

**中文摘要.** 本计划把来源的仿射表示 `x=A·U+beta, Theta=2^J·U+3d+1, v2(A)=J-Gamma`
做成一个**单步精确**的着陆/悬挂/碰撞三分法：a 步按 `r=v2(3k+theta)` 分为
`r<=j-3`（着陆，参数 `1+r<=j-2`，记录 `<=J-1`，类 `3-theta mod 2^{j'+1}`）、
`r=j-2`（碰撞，参数 `j+e`，`e=v2(A'U+beta')-(j-1)>=1`，记录恰为 `J+e`，需要 U 的
`e+1` 位）、`r>=j-1`（悬挂，参数 `j-1`，记录 `J`）；b/c 步**必然着陆**于 `omega(n)`，
类为 `theta+Phi-2 mod 2^{omega+1}`，记录 `<=J-1`。在深段（`j>=N0`, `|theta|<=B`）中
碰撞被已接受的 work_deep Lemma 2.2 排除，所以仿射游走**至多两条链**就成为 U-无关的；
唯一的记录上升机制是碰撞，代价是 `e`，安全判据是 `e<sigma-J`。这把 O2 的
`m>=8` gadget 精确识别为深度 `e=m-4` 的碰撞（记录 `m+1`），把 O1 的
`eta_r=-5+8/3^r` 识别为 `v2(3k+theta+s)=j-2` 的碰撞（`e>=sigma-J`），并把 O3 的
"局部相位类不够"精确化为"碰撞深度 e 需要实际来源的 e+1 位"。剩余未证条件被写成
来源/相位条件：无浅层碰撞或 `e<sigma-J`、落在已认证的类（窗口 [B] / 有理模式 N_Q /
DEEP）、以及 `sigma>J` 的松弛。未证明全局 EXT。

---

## 0. Exact statement draft (the target theorem)

Notation. `N0 = 2*10^7`, `B = 2^{10^7}`, `J < sigma`, `Gamma >= 0`, `j = J-Gamma`,
`A = 2^J*alpha`, `v2(alpha) = -Gamma` (so `v2(A)=j`), `U` odd, `beta in Z[1/6]`,
`d in Z[1/3]`, `x = A*U+beta`, `Theta = 2^J*U+3d+1`, `theta = 3d+1-beta in Z[1/6]`.
`theta mod 2^j = Theta-x mod 2^j` is the phase class. `record_t = j_t + Gamma_t`.
For the canonical/real origin of an actual epoch one has `alpha,beta in Z[1/2]`, `d in Z`,
`Gamma in Z`; the general `Z[1/3]` extension is only used for the source-shift deformation.

> **Theorem AFF (draft).**
> Let `O=(J,alpha,beta,d,Gamma,U)` satisfy `v2(beta) >= j+1` (tie-free affine origin) and
> put `theta = 3d+1-beta`.
> **(i) [A-imp + A; proof in §3.3, unreviewed.]** If `j >= N0+1` and `|theta| <= B-3`,
> then the affine run is U-free after at most two chains and every record is `<= J`;
> every non-root chain has record `<= J-1` except that an even crossing after a
> resonance can be the terminal chain with record `J`.
> **(ii) [A, algebra.]** At every j, an a-step is exactly one of:
> landing (`v2(3k+theta) <= j-3`: next parameter `1+v2(3k+theta)`, class `3-theta mod
> 2^{j'+1}`, record `<= J-1`), suspension (`v2 >= j-1`: next parameter `j-1`, record `J`),
> or tie (`v2 = j-2`: next parameter `j+e` with `e = v2((A'/2^{j-1})U + beta'/2^{j-1}) >= 1`,
> record exactly `J+e`, continuation needs `U mod 2^{e+1}`); a b/c-step always lands at
> `omega(n)`, class `theta+Phi-2 mod 2^{omega+1}`, record `<= J-1`.
> **(iii) [A-cond.]** If no tie occurs and the terminal class `(j_*,delta_*)` is certified
> (accepted minimal-information certificate; window `[B]` for integer classes with
> `5 <= j_* < 2*10^7` and `delta_* in [-12,15]` except `(5,5),(5,-11)`; rational-mode
> `N_Q` criterion for classes with denominator `3^r`; or DEEP), and `sigma > J`, then the
> whole walk has records `< sigma`. If a tie of depth `e<sigma-J` occurs, the tie's own
> record `J+e` is below `sigma`, but the continuation from the U-resolved state is a
> separate obligation (the gateway step); this draft does not certify it.

The criterion `C(O,sigma)` of A3 is the conjunction of the structural hypotheses, the
height bound, the no-tie-or-`e<sigma-J` condition and the certification clause (§3.4).
`C` depends on `(A,beta,d,sigma)` and the canonical table only — on `U` only through the
tie depth `e`, and on `J` not at all except through `j=J-Gamma` and the thresholds
`N0, 2*10^7`.

What is genuinely new relative to accepted work_deep (which already has Lemma 2.2
"no NT failure at deep chains", Lemma 2.5 "the landing class is known", Theorem 3.1
"certificate at the landing chain"):
1. the exact **one-step affine recursions** for `(alpha,beta,d)` including the
   five-input `beta' = 6d+8-beta/2` and the coefficient valuation `J-Gamma-1`
   (the checkpoint's requested form);
2. the **record trichotomy and tie ledger** `record = J+e`, `e` = tie depth, at *every* j
   (not only deep), which is the quantity the W budget does not see;
3. the explicit **class formulas in affine coordinates** and the statement that the
   landing class depends on `(beta,d,j,k)` only, while a tie needs the lift
   (high bits of `beta` and `U`) — the O3 separation;
4. the **shift `s in Z[1/3]`** realized as `beta -> beta-s` or `d -> d+s/3`, with the
   exact landing classes and the conclusion that the denominator `3^r` is invisible to
   every valuation statement.

---

## 1. A1: exact one-step recursions

### 1.1 The state

An **affine state** is a tuple `O = (J, alpha, beta, d, Gamma, U)` with

    J >= 1,  alpha in Z[1/2]\{0},  Gamma := -v2(alpha) >= 0,
    beta in Z[1/6],  d in Z[1/3],  U an odd integer,
    x := alpha*2^J*U + beta,      Theta := 2^J*U + 3d + 1,
    j := J - Gamma,               theta := 3d+1-beta in Z[1/6].

`A := alpha*2^J` has `v2(A)=j`. **`J` is the record level of the affine representation:**
`j+Gamma = J` identically, so `J` is the record at the chain where the representation is
fixed (for a fire root, `J=P`). "Records `<= J`" means "no chain exceeds the record of the
origin". Two warnings that are the source of repeated errors in the literature and in the
reviews:

* **The coefficient of `U` in `Theta` is `2^J`, the ROOT exponent, and it is never updated.**
  `J` is not the current parameter; `j=J-Gamma` is. (This is exactly
  `affine_origin.py:39` `x=alpha*X0+beta, Theta=X0+theta`, `X0=2^J*U`, and the checkpoint's
  `Theta=2^J U+3d+1`, `STOP_CHECKPOINT_2026_10_21.md:66-68`.) A naive `2^{J'}U` with
  `J'=J+1` at each a-step is wrong by `2^{J+1}U`; I verified this trap algebraically.
* `v2(beta) >= j+1` is the **tie-free hypothesis**; `v2(beta) < j` is an immediate landing
  at `j_0=v2(beta)` (clause C1 of §3.4); `v2(beta) = j` is a tie of the origin itself and
  never occurs for a canonical
  origin because the root has `beta=0` and every landing resets `beta` to a dominated
  value.

### 1.2 Lemma A1 (recursions) [A]

At a step from a chain with parameter `j` and `u = x/2^j`:

**(a) type-a step, `tau(j-1)=2k` (`k>=1`).**

    alpha' = 2 - alpha/2,      beta' = 6d + 2 + 6k - beta/2,
    d'     = d + 1 + 2k,       Gamma' = Gamma + 1,
    v2(alpha') = -Gamma-1.

At the five-input a-step (`j=5`, `X(4)` odd a, `tau(4)=2`, `k=1`):

    beta' = 6d + 8 - beta/2,      v2(A') = J-Gamma-1 = 4.        (A1-five)

This is exactly `STOP_CHECKPOINT_2026_10_21.md:70-73` (`beta'=6d+8-beta/2`,
coefficient valuation `J-Gamma-1`) and `affine_origin.py:47-50`
(`alpha=2-alpha/2`, `beta=2*theta+6k-beta/2`, `theta=theta+6k+3`, where
`theta` there is our `3d+1`).

*Proof.* `x' = 2Theta+6k-x/2`
`= (2*2^J - alpha*2^J/2)U + (6d+2+6k-beta/2)`, and
`Theta' = Theta+3+6k = 2^J U + 3(d+2k+1)+1`. `v2(2-alpha/2) = v2(alpha/2) = -Gamma-1`
because `v2(2)=1 > -Gamma-1`. ∎

**(b) type-b/c step, reading `X(n)`, `n=j-1`, with W-chain `(c'_W,lambda'_W)`,
`v2(c'_W)=n-eps=j-1-eps`, `omega(n)=v2(lambda'_W)`, `Phi=3tau(n)+5-lambda'_W`.**

    alpha' = c'_W*alpha/2^j,       beta' = c'_W*beta/2^j + lambda'_W,
    d'     = d + 1 + tau(n),       Gamma' = Gamma + 1 + eps,
    v2(alpha') = -Gamma-1-eps,     v2(beta') = omega(n).

*Proof.* `u = x/2^j = alpha*2^J*U/2^j + beta/2^j = alpha*2^Gamma*U + beta/2^j`; the first
term is odd (`alpha*2^Gamma` is a 2-adic unit, `U` odd), and `beta/2^j` is even by the
tie-free hypothesis, so `u` is odd. Then
`x' = c'_W u + lambda'_W = (c'_W alpha 2^Gamma)U + (c'_W beta/2^j + lambda'_W)` and
`c'_W alpha 2^Gamma = c'_W alpha/2^j` since `2^j = 2^J/2^Gamma`.
`v2(alpha') = v2(c'_W)+v2(alpha)-j = (j-1-eps)-Gamma-j = -Gamma-1-eps`.
`v2(c'_W beta/2^j) = (j-1-eps)+v2(beta)-j >= j-eps >= omega+2` (using
`v2(beta)>=j+1` and `omega <= j-2-eps` from S1), so `v2(beta')=omega`. ∎

**(c) Theta is always `2^J U+3d'+1`** in both cases, because
`Theta'-Theta = 3+6k` (a) or `3+3tau(n)` (b/c) and `d` absorbs it. This is the reason `d`
is the correct bookkeeping variable and why the "root J" convention is forced.

### 1.3 The phase identities

With `D := Theta - x` (the exact defect) and `theta = 3d+1-beta`:

    a :  D' = 3 - D - x/2,        D' == 3-theta-beta/2  (mod 2^{j-1}),
         theta' = 3d'+1-beta' = 3-theta-beta/2      (exact),
    b/c: theta' = theta + Phi - 2 + beta(1-c'_W/2^j)   (exact),
         theta' == theta + Phi - 2  (mod 2^{omega+1}),
    and in both cases  theta == D  (mod 2^j).

Proof: substitute; for b/c use `v2(1-c'_W/2^j)=j-1-eps` and `v2(beta)>=j+1`, so the error
term has valuation `>= j-eps >= omega+2`. For a, `v2(beta/2)>=j` and the class modulus is
`2^{j-1}=2^{j'}`. ∎

These are the `Phi`/`s` identities of `work_claude_shift/NOTES.md:60-97` (Theorem S),
`C5_EXTENSION.md:7-46` (AA/BA), `work_c3_drift/NOTES.md:158-196` (C3), and
`BBBAA_COPY_CERTIFICATE.md:34-52` (Phi=10/3 at m).

### 1.4 The five-input specialization

`X(4)` is odd type a with `tau(4)=2`, `k=1` (`Calendar(64).crossing(4)`; reviewed in
`work_landing_symbolic/reviews/odd_denominator.md` §1.2 item 2 and `check_R.md` ODD E6).
So *every* chain at parameter five executes (A1-five) with `k=1`; there is no b/c
alternative at j=5. This is the only place where a "five-input" formula is used.

---

## 2. A2: the input phase `theta+s`, `s in Z[1/3]`

### 2.1 What the shift is, and what it is not

In the drift calculus the source shift of a c-step is

    s(n) = Phi(n) - 2 = -1 - lambda_Y(n)   (mod 2^{omega(n)+1}),

see `CONGRUENCE_TARGET_NOTE.md:252-258`, `work_claude_shift/NOTES.md:9-21,85-97`.
The *exact* quantity `Phi = 3tau+5-lambda'_W` is an integer; the *reduced automaton value*
`Phi_red in Z[1/3]` satisfies `Phi == Phi_red (mod 2^H)` with `H >= omega+1`
(Theorem S, `work_claude_shift/NOTES.md:85-97`). The height `h(s+2)` is the height of the
reduced representative (`JOINT_HEIGHT_BUDGET.md:9-16`), not of the exact integer.

Accepted values: `eps=3: s=0`; `AA: s=-1`; `BA: s=+1`; `BBBAA: s=+4/3`
(`work_claude_shift/NOTES.md:18`, `C5_EXTENSION.md:28,43`, `CHECKPOINT...:665-668`).
The denominator of `Phi_red` divides `3^(#non-descents)`
(`work_claude_shift/NOTES.md:9-16,111-127`).

**Two different deformations must not be conflated** (this is the `eta` vs `s` confusion
isolated by `check_T.md` §1.2 E0):

* `beta -> beta - s`: `x` shifts by `-s`, `Theta` fixed, phase `theta -> theta+s`.
  This is a *lift-level* deformation; it preserves `A` and `j` only if `v2(beta-s) >= j`.
* `d -> d + s/3`: `Theta` shifts by `s`, `x` fixed, phase `theta -> theta+s`.
  This is the deformation used by `FIRST_A_REDUCTION.md:33-42` (`y_eta=y+2eta`,
  `T_eta=T+eta`) and by the O1 obstruction (`ORBIT_SHIFT_OBSTRUCTION.md:34-47`).
  Here `d in Z[1/3]` in general.

**The input phase class does not determine the state.** Two states with the same
`(j, theta+s)` differ by a multiple of `2^j` in `beta`; their future walks can differ after
a tie. The affine origin supplies the actual lift `beta` (or `d`), which is why the
criterion must be stated on `(A,beta,d)` and not on the class alone. This is the precise
content of O3 (`OPTIMAL_PHASE_ENCODING.md:61-96`) and of work_deep Remark 3.2.

### 2.2 Landing classes in affine coordinates

Let the input phase be `theta_s = theta+s` and let `j=J-Gamma`.

| step | landing parameter `j_*` | landing class `delta_*` | depends on |
|---|---|---|---|
| a | `1+v2(3k+theta_s)` if `<= j-2` | `3-theta_s mod 2^{j_*+1}` | `j, beta, d, k`; **not** `U`, not the high bits of `beta` |
| b | `omega(n)` | `theta_s-1 mod 2^{omega+1}` | `j,beta,d,lambda'_W` |
| c | `omega(n)` | `theta_s+Phi-2 mod 2^{omega+1}` | `j,beta,d,Phi` |
| tie | `j+e` (`e>=1`) | needs `U mod 2^{e+1}` and `beta mod 2^{e+1+j}` | the **lift** |

**Which of `(beta,d,A,sigma)` the class uses.** `beta` and `d` enter only through
`theta_s=3d+1-beta+s`; `beta` enters the tie test only through `beta mod 2^{j-1}`
(and through `beta` itself in the depth `e`); `A` enters only through `j=v2(A)` and the
tie comparison `v2(beta') vs v2(A')`; `sigma` enters only in the ceiling comparison
`j_*+Gamma_* < sigma` (and through the certification range `j_* < 2*10^7`). The high bits
of `beta` above `j` do not affect the landing class, only a tie.

The class error terms are: for a, `beta/2` has valuation `>= j > j_*+1`; for b/c,
`beta(1-c'_W/2^j)` has valuation `>= j-eps >= omega+2`. Hence the displayed classes are
**exact mod 2^{j_*+1}**, not approximate (the extra bit is retained, as in C3-ID,
`work_c3_drift/NOTES.md:173-185`).

### 2.3 Denominator `3^r` is invisible

All recursions of Lemma A1 are identities over `Z[1/6]`. Multiplying `x,Theta` by `3^r`
(a 2-adic unit) preserves `v2`, hence every parameter, record and class. Consequently:

* no step of the criterion involves `r` except through the actual value of `s` and its
  height `h(s+2)`; the only other place `r` re-enters is the rational-mode threshold
  `N_Q = max(N0,4(ceil(log2 3^r)+2))` of clause C5, which is source-adaptive;
* "bounded height with unbounded denominator" is a real phenomenon (§3.6, O1), but it
  enters only through the congruence `v2(3k+theta_s)=j-2`, never through a size estimate
  on `s`.

This is the exact sense in which the criterion is scale-free in `r`; it is not a claim that
large `r` is harmless.

---

## 3. A3: trichotomy, tie ledger, and the criterion `C`

### 3.1 Lemma A2 (a-step trichotomy) [A]

Let `v := v2(beta) >= j+1`, `beta' = 2(3k+theta) + (3/2)beta` (check:
`2theta+1.5beta = 6k+6d+2-0.5beta`), and `ell' := v2(A') = j-1 = J-Gamma-1`.

| `r := v2(3k+theta)` | `v2(beta')` | next parameter | record | name |
|---|---|---|---|---|
| `r <= j-3` | `r+1 <= ell'-1` | `j'=r+1 <= j-2` | `j'+Gamma' = r+Gamma+2 <= J-1` | **landing** |
| `r = j-2` | `ell'` | `j' = ell'+e`, `e>=1` | `J+e >= J+1` | **tie** |
| `r >= j-1` | `>= ell'+1 = j` | `j' = j-1` | `J` | **suspension** |

(Comparisons, with `v2(2(3k+theta))=1+r` and `v2((3/2)beta)=v-1>=j=ell'+1`:
if `1+r <= ell'-1` the minimum `1+r` is exact because the other term is `>=ell'+1`;
if `1+r=ell'` the other term is `>=ell'+1`, so `v2(beta')=ell'` exactly, with no
cancellation; if `1+r>=ell'+1` both terms are `>=ell'+1`, so `v2(beta')>=ell'+1`
(possibly higher by cancellation), while the parameter is `v2(A')=ell'` and the record is
`J`. This proves the table in all cases.)
At a tie `x' = A'U+beta' = 2^{ell'}(aU+b)` with `a=A'/2^{ell'}`, `b=beta'/2^{ell'}` both
odd, so `aU+b` is even and `e := v2(aU+b) >= 1`, `j' = ell'+e`, `record = J+e`. ∎

This trichotomy is the affine form of work_deep Lemma 2.2/2.3 (`work_deep/NOTES.md:99-120`)
and of `work_claude_shifted/NOTES.md:97-108` (Theorem SC). The **new** content is the exact
record values and the tie depth `e`.

### 3.2 Lemma A3 (b/c is always a landing) [A]

For every b/c step with the hypotheses of Lemma A1(b):
`v2(beta')=omega(n) < j-1-eps = v2(A')`, so `j'=omega(n)`, the class is
`theta+Phi-2 mod 2^{omega+1}`, and `record = omega+Gamma+1+eps <= J-1` (S1:
`omega <= j-2-eps`). ∎

### 3.3 Proposition A4 (two-chain U-freedom in the deep regime) [A + accepted imports]

**Definition (U-free).** A state is U-free if its residues
`(x mod 2^{j+1}, Theta mod 2^{j+1})` are determined by `(A,beta,d,j)` and do not depend on
`U`. By HP with precision `j+1` (Prop 3.2 of `work_claude_shifted`) the subsequent walk is
then determined by that class **for as long as the reference walk stays inside the
certificate**; if the class itself is uncertified (a bare tie, or a class outside the
window), a later step may again depend on `U`. "U-free" is therefore a statement about the
state, not a blanket termination claim.

Assume `j >= N0+1`, `|theta| <= B-3`. Then the affine run reaches a U-free state in at most
two chains and every record is `<= J`.

*Proof.* Chain 0 is deep. work_deep Lemma 2.2 (`work_deep/NOTES.md:99-114`) gives
`|3k+theta| < 2^{j-2}`, hence `r != j-2` (no tie) and either `r <= j-3` (landing at chain
1) or `3k+theta=0` (suspension). In the suspension case `j_1=j-1 >= N0`,
`theta_1 = 3-theta` with `|theta_1| <= B`, and Lemma 2.3 gives
`3k_1+theta_1 = 3(k_1+k+1) > 0`; Lemma 2.2 applied to chain 1 gives
`|3k_1+theta_1| < 2^{j_1-2}`, so `r_1 <= j_1-3` (landing) or the step is even/b/c. Either
way chain 1 is U-free. Records: `J` at chain 0 (root or resonance), `<=J-1` at chain 1
(Lemma A2/A3). ∎

**Rational extension.** work_deep Lemma 2.2/2.3 are stated for integer states; their
proofs use only the walk rules, `|theta|<=B`, CLOCK and S1, all of which make sense over
`Z[1/3]` (3 is a 2-adic unit, so no valuation or size estimate changes). The extension to
`theta in Z[1/3]` with the same `B` is therefore verbatim, and is required here for the
source shifts of §2. This is an extension of the accepted statement, not a reproof; it
must be flagged as such in the final write-up.

**Note.** The "no-tie" hypothesis is *automatic* in the deep regime; it is a genuine
hypothesis only for `j < N0`. This is the strongest part of the plan and it does not need
any new arithmetic.

### 3.4 Definition of the criterion `C(O,sigma)`

`C(O,sigma)` holds iff:

* **(C0) structure** `O` is an affine state as in §1.1 with `beta in Z[1/6]`,
  `d in Z[1/3]`, `U` odd, `v2(A)=j`, and (for a canonical source) `d in Z`,
  `beta in Z[1/2]`, `Gamma in Z`.
* **(C1) lift** either `v2(beta) >= j+1` (tie-free) or `v2(beta) < j` (immediate landing at
  `j_0 = v2(beta)` with class `theta mod 2^{j_0+1}`).
* **(C2) height** `|theta_s| <= H` for the input phase `theta_s=theta+s`; for a suspension
  also `|3-theta_s| <= B` (automatic when `H <= B-3`). `H` is a parameter of the statement;
  `h(s+2) <= h` bounds the reduced source shift.
* **(C3) regime** either `j >= N0+1` (deep; the size lemmas apply), or `j < N0` and the
  explicit finite dispatch of §5 is used.
* **(C4) no hidden tie** at every shallow a-step of the run:
  `v2(3k_t+theta_t) != j_t-2`; equivalently `v2(beta'_t) != v2(A'_t)`. If a tie is present,
  it is allowed only with `e_t < sigma-J` and with the resolved lift `U mod 2^{e_t+1}`;
  the continuation from the resolved state is then **not** covered by C5 and must be
  re-certified (this is the gateway obligation, §9).
* **(C5) certificate** the terminal class `(j_*,delta_*)` is in the accepted certified set:
  integer class with `5 <= j_* < 2*10^7`, `delta_* in [-12,15]`,
  `delta_* not in {(5,5),(5,-11)}` (`work_claude_shifted/NOTES.md:136-151`,
  `work_deep/NOTES.md:236-252`); or a rational class with `Q=3^r`,
  `N_Q = max(N0,4(ceil(log2 Q)+2)) <= j_*` meeting the `ODD_DENOMINATOR` condition
  (`work_c3_drift/ODD_DENOMINATOR.md:37-68`, reviewer E2/E3); or the DEEP hypothesis.
* **(C6) ceiling** `sigma > J` (and `sigma > J+e_t` at ties).

**Claim (to be proved next round, currently [A-cond]).** `C(O,sigma)` implies that the walk
terminates with every record `< sigma`.

### 3.5 Clause audit: which are source/phase conditions and which are bounds

| clause | type | parameter upper bound? |
|---|---|---|
| C0 structure | source/provenance (canonical `d in Z`, `beta in Z[1/2]`) | no |
| C1 lift | structural valuation condition on the origin | no |
| C2 height `H` | phase condition; `H` is a free parameter of the theorem | no (it bounds the phase, not the problem scale) |
| C3 `j >= N0+1` | **lower** bound on the chain parameter, the deep regime where CLOCK's size estimate is available | it is a parameter threshold, not a cap. The complementary range `j < N0` is a fixed finite check, labeled [B] |
| C4 no tie | congruence/source condition on the actual `k,beta,d`; refutable at any scale (O1, O2) | no |
| C5 certificate | accepted finite window [B] (`j_*<2*10^7` is a *range*, explicitly labeled [B]), or rational-mode `N_Q` (source-adaptive), or DEEP (source condition) | the window branch **is** a finite range; it is not offered as a uniform target and cannot be used to close the deep/rational cases |
| C6 `sigma>J` | relation between source precision and root parameter (the slack `rho-P`) | no |

Conclusion: the *uniform* part of `C` is `C0-C2 + C4 + C6`; the certification `C5` is
either an accepted [B] window (explicitly finite), the rational-mode `N_Q` condition
(source-adaptive), or DEEP (open source condition). No clause is a disguised cap on `J`.

### 3.6 The obstructions O1/O2/O3 in affine coordinates

**O2 (`STOP_CHECKPOINT_2026_10_21.md:9-47`).** The constructed state is
`u=(2^{m-4}-1)/3`, `x=32u`, `Theta=x+5`, `j=5`, `k=1`, phase `theta=5`.
It admits two affine representations:

* `A=32, beta=0, d=4/3, U=u, J=5` (so `d not in Z`);
* `A=32, beta=-64, d=-20, U=u+2, J=5` (so `d in Z`, `v2(beta)=6=j+1`), obtained by the
  family `U=u+2w`, `d=(4-64w)/3` with `w=1 mod 3` (`w` is an offset, not the a-step
  half-time `k=1`).

In both, `r=v2(3k+theta)=v2(8)=3=j-2`: **a tie**, not a landing. The tie depth is
`e = v2(3U-5) = v2(3u+1) = m-4`, hence `j'=m` and `record = J+e = m+1`.
This reproduces `STOP_CHECKPOINT` exactly (`x'=3x/2+16=2^m`; record `m+1`; the ceiling 9
is crossed at `m>=8`; the normalized intermediate value 11 at m=6 is the W bookkeeping, not
the affine record). `W=Gamma+j+2r+h(c)=0+5+0+3=8` is independent of `e`, which is precisely
why the W budget cannot close this gateway. **The affine criterion does:** it detects the
tie from `(beta,d,j,k)` (no `U` needed) and the ledger gives the record `J+e`; the ceiling
condition `e<sigma-J = 9-5 = 4` gives `m<8`, the exact STOP_CHECKPOINT threshold.
Numerically checked inline (no artifact): `m=6,8,10,12,18` give `e=2,4,6,8,14` and
records `7,9,11,13,19`.

**O1 (`ORBIT_SHIFT_OBSTRUCTION.md:16-98`).** At the canonical `P=49` source:
`x0=5*2^49`, `Theta=x0+1`, `j=49`, `theta=1`, `X(48)` odd a with `k=20`, and the shift
`eta_r=-5+8/3^r` (`d -> d+eta_r/3`, `d in Z[1/3]`). Then

    3k+theta+eta_r = 56+8/3^r = 8(7+3^{-r}),
    v2 = 3 + v2(7*3^r+1),     tie <=> v2(7*3^r+1)=44 (=j-2-3).

At such an `r` the output `y_r = y+2eta_r = 16(A_1+3^{-r})`, `A_1=15*2^44+7=263882790666247`,
has `v2(y_r) = 4+v2(A_1*3^r+1) = 48+e`, so the tie depth is
`e = v2(15+b)` and `record = 49+e = v2(y_r)+1`. O1's dangerous residue
`A_1*3^r = -1 (mod 2^{sigma-5})` forces `v2(7*3^r+1)=44`, i.e. the tie, and
`record >= sigma` exactly when `e >= sigma-49 = sigma-J`. Thus:

* O1 is **positively localized**: it is the tie `v2(3k+theta+s)=j-2` with depth
  `e >= sigma-J`, and the affine criterion detects it from `(beta,d,j,k)` **without**
  knowing `U`; the required additional condition is the source/phase condition
  `e < sigma-J`, equivalently the exclusion of the dangerous residue
  `3^r = -A_1^{-1} (mod 2^{sigma-5})`, or the relation between the actual `r` and `sigma`.
* This is exactly the "relate `r` to `sigma` or exclude the dangerous residue" obligation
  stated in O1 §5; the affine ledger makes it an explicit inequality. It is **not**
  removed: `|eta_r|<=5` does not imply `e<sigma-J`.

**O3 (`OPTIMAL_PHASE_ENCODING.md:61-96`).** A landing class of parameter `j_*` is a point
of `Z/2^{j_*+1}`; a tie needs the lift (`U mod 2^{e+1}` and `beta mod 2^{e+1+j}`). The
affine origin supplies that lift for free *while it is valid*, and the class alone cannot:
this is the counting obstruction of O3. In the criterion, O3 shows up exactly as clause C4
(tie depth) and C5 (rational class denominator); no finite reserve `S` is used anywhere.

### 3.7 Relation to the accepted R1/H5 frontier

The criterion is a *per-prefix* condition, not a parameter cap. It does not re-open CAL-C,
R1 or H3 (refuted as uniform targets, `CONGRUENCE_TARGET_NOTE.md:118-230`); it is
compatible with them failing: a failing R1 is exactly a deep→deep c-step, i.e. a b/c
landing with `omega >= N0`, which is a C5 failure (rational/deep class), not a C0-C4
failure. A failing CAL-C is a c source with `2^{N0}|lambda'_W`; at the affine level it only
means `omega` is large, and the class is handled by C5.

---

## 4. Relation to the existing literature (what is imported, what is new)

| source | used for | relation |
|---|---|---|
| `work_global_ext/PROOF_EXT.md:53-96` | walk rules, Lemma HP, Lemma AB, Prop RB | the affine recursions must agree with these; HP is what makes the landing class sufficient (certificate) |
| `work_deep/NOTES.md:88-135` (Lemmas 2.1-2.4) | deep size, deep trichotomy, resonance isolation, log* count | Prop A4 is a corollary of Lemmas 2.2/2.3; this plan adds the affine bookkeeping and record values |
| `work_deep/NOTES.md:152-171` (Lemma 2.5) | the deep landing class `3-theta` / `theta+Phi-2` | identical formulas; the affine version exhibits them as exact rational identities including `beta` |
| `work_deep/NOTES.md:199-264` (Theorem 3.1/3.4) | `certify` + DEEP′ | the landing certificate used in C5; the plan does not reprove it |
| `work_claude_shifted/NOTES.md:97-151` | Theorem SC, Prop 3.2, window scan `5<=j<2*10^7`, `delta in [-12,15]` | C5's integer branch |
| `work_claude_shifted/NOTES.md:180-201` | gateway-tie lemma (net descent at a resolved tie) | the template for the tie continuation; the affine ledger gives the tie depth it needs |
| `work_claude_shift/NOTES.md:9-21,60-130` | Theorem S: shift `s` in `Z[1/3]`, denominator divides `3^(#non-descents)`, Lemma ND | the source-shift values and the `r`–`d`–`j` inequality; used in §3.6/O1 |
| `work_c3_drift/C5_EXTENSION.md:7-46` | AA: `delta'=theta-1`, BA: `theta+1` | the `s=-1,+1` instances of A3 |
| `work_c3_drift/NOTES.md:158-196` | C3-ID, extra bit | the `s=0` instance |
| `work_c3_drift/BBBAA_COPY_CERTIFICATE.md:34-52` | BBBAA `Phi=10/3` and the full phase incl. root term | the `s=4/3` instance; the plan's form `theta+Phi-2+beta(1-c'/2^j)` is the same identity |
| `work_c3_drift/SHIFT_TRANSPORT.md:21-86` | outer-phase transport, `Safe`, record identity | complementary: SHIFT_TRANSPORT shifts the outer `Theta`; this plan shifts the source's own `beta`/`d`; only the latter sees the tie depth |
| `work_c3_drift/FIRST_A_REDUCTION.md:33-80` | `y_eta=y+2eta`, `T_eta=T+eta`, terminal collision `q=h` | the `d`-shift specialization; `q=h` is a *cancellation in `x`*, which in the affine picture is a tie exactly when the coefficient valuation is reached |
| `work_c3_drift/ORBIT_SHIFT_OBSTRUCTION.md` | O1 | re-derived in §3.6 |
| `work_c3_drift/OPTIMAL_PHASE_ENCODING.md` | O3 | the class/lift separation of §2.1 |
| `work_c3_drift/JOINT_HEIGHT_BUDGET.md:9-77` | `W`, `h(c)`, copy/gateway budget | the comparison object for A5; the plan does not use `W` |
| `work_c3_drift/STOP_CHECKPOINT_2026_10_21.md:62-77` | the affine form + `beta'=6d+8-beta/2` + `v2(beta')<J-Gamma-1` | the exact task; this plan makes the inequality strict/equal/greater trichotomy |
| `work_c3_drift/AFFINE_REACHABLE_CATAPULTS.md:10-113` | sparse `alpha,beta`, canonical p=5..18 gateways | the special cases the general criterion must reproduce |
| `reviews/rational_mode.md`, `reviews/odd_denominator.md`, `reviews/check_R.md` | status of the rational-phase work; O1 `N_Q` numbers | C5's rational branch; the plan adopts their corrected scope (fixed denominator, `N_Q`, no false "all heights safe") |
| `reviews/shift_transport.md`, `reviews/first_a.md`, `reviews/check_T.md` | `eta` vs `s`; `Safe` needs `x!=0`; terminal collision | §2.1 and the tie ledger |

What the plan does **not** claim: global EXT; that every reached origin satisfies C;
that `W` is repaired; that deep c-steps (R1) are resolved; that O1's dangerous `r` never
occurs in a reached source.

---

## 5. A4: test plan (to be executed next round; no script written this round)

### 5.1 Canonical fixtures (Calendar(512), `B=512`)

The canonical oracle is `work_global_calendar/calendar_oracle.py` `Calendar(512)` (the
task's specified oracle; `B<=1024`). As a gate, compare its `kind/time/epsilon/odd` with
the legacy `work_ext_roots.search_roots.Calendar` over the queried range (the accepted
review `check_R.md` §0 reports 0 mismatches for `n=0..255`); if any queried `n` lies outside
the certified range, STOP rather than extrapolate. `D:/math_cc_astra/deep1/table_1000000.pkl`
may be used only as an auxiliary cross-check for `lambda` data with `n<10^6`, and any row
depending on it must be marked `"aux_table": true`.

Selector, exactly as the accepted scripts: for `P=5..256`, `fire = first_fire(cal,P)`
(`work_ext_roots/verify_low_deficit.py:30-38`; the calendar checks `fire['k']==k`), then
`rows = cal.epoch_crossings(fire)` and the source list
`[(rho, 6k+4, 6k+5, rho,'fire')] + [(n, 3t+4+lambda_Y, 3t+5, n-eps,'c') for odd c rows]`
(`work_c3_drift/verify_first_a.py:10-15`). The script must reproduce the accepted counts
**336 sources = 252 fires + 84 c sources** as a gate, and, in the shift sub-suite using the
same 17 shifts `eta in [-8,8]`, the **5,712 source/shift pairs**; otherwise STOP and report
(do not silently proceed).

For each source, build the affine origin and replay the epoch:

    J = P, alpha = 1, beta = 0, d = 0, Gamma = 0, x0 = 6k_fire+4 = 2^P U, U = x0/2^P.

At each chain read `cal.crossing(j-1)`; for b/c use
`c'_W = (head_ratio + 2*tail_ratio)/2`, `lambda'_W = head_lambda + 2*tail_lambda + 3`
(the identity used in `work_ext_roots/verify_low_deficit.py:19-21`). Assert at every chain:

1. `x = alpha*2^J*U + beta` equals the exact numerator (Fraction, exact);
2. `Theta = 2^J*U+3d+1` equals the exact `3s+5` (`s`=calendar time);
3. `v2(alpha) = -Gamma` and `v2(2^J*alpha) = J-Gamma = j = v2(x)`;
4. `theta = 3d+1-beta` and `theta == Theta-x (mod 2^j)`;
5. Lemma A1's predicted `(alpha',beta',d',Gamma')` equals the exact next state;
6. Lemma A2/A3's predicted `j'`, class, and record equal the exact walk's;
7. every landing is recorded with `(j_*,delta_*)` and compared with `certify(j_*,delta_*)`.

Also cover the accepted `c` sources (84 of them), the four `AA` and four `BA` sources
(`C5_EXTENSION` §1; the script must count them), and the 76 `eps=3` sources
(`work_c3_drift/NOTES.md:284-288`). Special fixtures with known outcomes:

* `P=17`: WITNESS tail `17,5,6,1` (tie `(5,5)` at `j=5`, `X(4)` a-step);
* `P=49`: O1 source (§3.6); `r=1,2,3,5` directly, `r<10^4` by `v2(7*3^r+1)` via modular
  exponentiation, and the discrete-log existence at `H=3,...,256` exactly as in
  `work_c3_drift/verify_orbit_shift_obstruction.py` (no large integers needed);
* `P=90,161,234`: the first-a collision exceptions (`work_c3_drift/first_a_checks.json`,
  `FIRST_A_REDUCTION.md:152-159`);
* the `P=65,101,136,209` deep first-a steps with negative `lambda_in`
  (`check_T.md` §4.1) — these test that the affine recursion does not assume `lambda>=0`.

**Range check.** `cal.crossing(n)` is valid only inside the certified calendar; the script
must assert `n < cal.boundary_pointer` for every query and must reject out-of-range
queries instead of extrapolating (`calendar_oracle.py:62-64,130-139`).

### 5.2 Synthetic fixtures (explicitly **non-canonical**)

Random `(J, alpha, beta, d, Gamma, U)` with `J in [5,60]`, `Gamma in [0, min(8,J-5)]`,
`alpha` odd/`2^Gamma`, `beta = odd * 2^{j+1+delta}` (`delta in [0,4]`), `d in [-10^6,10^6]`,
`U` odd in `[1,2^30)`, and for b/c random `(c'_W,lambda'_W)` with
`v2(c'_W)=n-eps`, `omega < v2(c'_W)`; check all Lemma A1/A2/A3 identities exactly
(Fractions). These are *algebra controls*, not reachability claims; every JSON row must
carry `"canonical": false`.

### 5.3 Planned identities (numbered, all exact)

1. `x' = alpha'*2^J*U+beta'` and `Theta' = 2^J*U+3d'+1` (a and b/c).
2. `beta' = 6d+2+6k-beta/2`; five-input `=6d+8-beta/2` when `k=1`.
3. `v2(alpha') = -Gamma-1` (a) / `-Gamma-1-eps` (b/c).
4. `theta' = 3-theta-beta/2` (a), `theta' = theta+Phi-2+beta(1-c'/2^j)` (b/c).
5. `v2(beta') = r+1` for `r<=j-3`; `=j-1` for `r=j-2`; `>=j` for `r>=j-1`.
6. `j' = r+1` / `j-1` / `j+e` with `e=v2(A'/2^{j-1}U+beta'/2^{j-1})>=1`.
7. `record = J-1-... <=J-1` (landing), `J` (suspension), `J+e` (tie); b/c `<=J-1`.
8. `delta_* = 3-theta mod 2^{j'+1}` (a) / `theta+Phi-2 mod 2^{omega+1}` (b/c).
9. `v2(beta')=omega(n)` and `j'=omega(n)` for every b/c step.
10. `theta == D (mod 2^j)` at every chain.
11. Shift: `s=0,-1,+1,4/3` instances; `beta->beta-s` vs `d->d+s/3` give the same class
    but different lifts; for `v2(beta-s)<j` the `beta`-shift lands at `v2(beta-s)`.
12. O2: `e=m-4`, `record=m+1`, `W=8`, threshold `m>=8`.
13. O1: `v2(3k+theta+eta_r)=3+v2(7*3^r+1)`, tie at `44`, `e=v2(y_r)-48`,
    `record=v2(y_r)+1`.

### 5.4 Planned commands, JSON and PASS/FAIL

    python -B work_landing_symbolic/affine/verify_affine_algebra.py       # -> affine_algebra.json
    python -B work_landing_symbolic/affine/verify_affine_canonical.py     # -> affine_canonical.json
    python -B work_landing_symbolic/affine/verify_affine_synthetic.py     # -> affine_synthetic.json
    python -B work_landing_symbolic/affine/verify_affine_obstructions.py  # -> affine_obstructions.json
    python -B work_landing_symbolic/affine/verify_affine_falsify.py       # -> affine_falsify.json
    python -B work_landing_symbolic/affine/verify_affine_landing.py       # -> affine_landing.json

Each script prints `PASS`/`FAIL`, counts, and the failure list; each writes its JSON beside
itself; each must run in `<10` minutes. PASS requires zero mismatches **and** the count
gates (`336`, `5712`, `252`, `84`, `76`, `4`, `4`). JSON fields:

    { "status": "PASS"|"FAIL", "review_status": "unreviewed", "canonical": true|false,
      "calendar_B": 512, "counts": {...}, "failures": [ {...} ],
      "scope": "..." }

`affine_landing.json` additionally records, for every landing, `(source, j, theta, j_*,
delta_*, k_or_omega, record_relative, certificate_status)`.

### 5.5 What cannot be tested this way

* `j >= N0 = 2*10^7`: `Calendar(B)` needs `B >= j`; the plan uses the analytic size
  lemmas (Lemma 2.1/2.2) for that regime and marks the `<=2`-chain proposition [A-imp],
  not [B]. No finite computation will be claimed for it.
* The deep c-landing (R1) and the rational class with `Q=3^r`, `N_Q > j_*`: only the
  algebra and the O1 modular identity are checked; certification stays open.
* Canonical `U` inside a huge source is never materialized; only the source symbols and
  the affine coefficients are.

---

## 6. A5: why the W budget is insufficient, and what the affine criterion adds

`JOINT_HEIGHT_BUDGET.md:9-77` defines `W = Gamma+j+2r+h(c)` and proves composition and
decrease for copies and large paired gateways. The STOP_CHECKPOINT construction
(`STOP_CHECKPOINT_2026_10_21.md:9-47`) is a local state with `W=8<9` whose next record is
`m+1`. In affine coordinates (§3.6) it is a **tie of depth `e=m-4`** at `j=5`, and the
record is `J+e`. `W` is a function of `(Gamma,j,r,h(c))`; it does not contain `e`, and the
tie can have any depth while `r,h(c)` stay fixed. Hence:

* no rule that uses only `W` and the local phase class can bound the next record;
* the missing datum is the **tie depth** `e`, i.e. `v2(A'U+beta')`, which is a property
  of the actual origin (its `beta` and `U`), not of `(j,theta,r,h)`;
* the affine criterion supplies the tie detection (from `beta,d,j,k`, no `U`), the exact
  record `J+e`, and the threshold `e<sigma-J`.

This is the positive content relative to O2: O2 says "the joint budget cannot be closed
locally at an arbitrary small gateway"; the affine criterion explains *why* (the missing
`e`) and gives the exact extra condition.

---

## 7. Dependence on `J` (required table)

| item | dependence |
|---|---|
| Lemma A1 (recursions) | none |
| Lemma A2/A3 (trichotomy, classes, records) | none; `J` enters only as `j=J-Gamma` |
| Prop A4 (`<=2` chains, deep) | uses `N0=2*10^7` and `B=2^{10^7}` through Lemma 2.1/2.2; lower bound `j>=N0+1` |
| criterion C0-C2, C4, C6 | none |
| C5 integer window | finite range `5<=j_*<2*10^7` (the accepted [B]); not a uniform target |
| C5 rational mode | `N_Q=max(N0,4(ceil(log2 Q)+2))`, a **denominator-adaptive threshold**, not a cap on `J`; the residual band `[N0,N_Q)` is open (review of ODD_DENOMINATOR, E2/E3) |
| C5 DEEP | `log* J`: at most `2*Lambda(J)+1` deep chains, `Lambda(J)<=h` for `J<T_h` (Lemma 2.4); `T_h` enters only here; `K_clock` untouched |
| O1 dangerous residue | the actual `r` enters through `e`; the accepted Theorem S/Lemma ND relates `r` to `#non-descents` and `|d|`; no `J` bound is claimed |
| shadows | none of `T_4`/`K_clock` is used; the only ranges are `N0`, `B`, `2*10^7` |

---

## 8. Falsification tests (what would kill the statement)

The next round must actively search for these; each is a hard failure of the plan.

1. **F1 (two-chain).** An affine origin with `j>=N0+1`, `|theta|<=B-3`, no tie, whose
   affine run needs `>2` chains to become U-free, or has a record `>J`. *(Would kill
   Prop A4; note the deep lemma forbids ties here, so this is a test of the `<=2` claim,
   not of the no-tie hypothesis.)*
2. **F2 (trichotomy).** Any `(J,alpha,beta,d,Gamma,U,k)` with
   `v2(beta') != r+1 / j-1 / >=j` in the three cases, or a tie with
   `j'-ell' != v2(aU+b)`. *(Would kill Lemma A2.)*
3. **F3 (b/c).** Any b/c step with `v2(beta') != omega(n)` or `j' != omega(n)`. *(Would
   kill Lemma A3.)*
4. **F4 (O2 rejection).** The STOP_CHECKPOINT gadget `m=8..256` must be classified as a
   tie with `e=m-4`, record `m+1`, and must fail `C` at every `m>=8`; if it passes `C`
   or is classified as a landing, the criterion is too weak. *(PASS is required here;
   a pass at m>=8 would be a failure of the plan.)*
5. **F5 (O1 detection).** For every `r` with `v2(7*3^r+1)=44`, the P=49 shifted origin
   must be classified as a **tie** (not a landing); and for the O1 dangerous residue
   `3^r = -A_1^{-1} (mod 2^{sigma-5})` the depth must satisfy `e>=sigma-J` (record
   `>=sigma`). If any of these is certified safe, the ledger is wrong.
6. **F6 (landing class).** Any canonical source where the affine-predicted `(j_*,delta_*)`
   differs from the exact walk's landing class at the same chain.
7. **F7 (shift lift).** Any `s in Z[1/3]` where the `beta`-shift and the `d`-shift give
   different classes (they must not), or where `v2(beta-s)<j` but the `beta`-shift is
   treated as parameter-`j` (it must land at `v2(beta-s)`).
8. **F8 (W-only).** Any attempted closure that uses `W` without `e`: the O2 family is the
   counterexample; the script must include it as a **negative control** (expected FAIL of
   any `W`-only predicate).
9. **F9 (provenance).** A canonical source where `d not in Z` or `v2(beta)<j` at a step
   that is not a landing/tie/suspension. *(Would mean Lemma A1 cannot be maintained on
   the canonical prefix; it would kill the whole direction.)*

Falsification data must be kept verbatim in `affine_falsify.json`, including any failure
of the criterion itself. A failure of `C` is **not** a counterexample to the theorem — it
is an unmet source condition, to be reported as such, never silently relaxed.

---

## 9. Open obligations and promotion criteria

* [A] after next round's algebra script: Lemmas A1-A3 on all tested ranges; Prop A4 is
  [A-imp + A] with the proof written in §3.3 and the constants `j>=N0+1`, `|theta|<=B-3`,
  `N0=2*10^7`; it needs independent review and the exact-constant recheck at `j=N0+1`.
* [A-cond]: Theorem AFF(iii) with C5 as a hypothesis. The proof must chain
  Lemma A2/A3 + Prop 3.2 (HP) + the record accounting; it is short and should be written
  in full next round.
* [B]: the canonical replay (336 sources / 5,712 pairs), the synthetic algebra controls,
  the O1/O2 modular arithmetic, the falsification suite.
* [C]/open: (i) whether every reached origin satisfies C4 (no shallow tie) or has
  `e<sigma-J`; (ii) the rational class with `N_Q>j_*` (the `[N0,N_Q)` band); (iii) deep
  c-steps (`omega>=N0`, R1); (iv) the `(5,5),(5,-11)` bare ties beyond the accepted
  gateway families; (v) O1's actual `r` for a reached source.

Promotion rule: nothing above is to be labeled [A] until the corresponding proof is written
in full with its imports, and no `[C]`/`[C-support]` item may be quoted as proved.

---

## 10. Planned reproduction commands (next round; not run now)

    python -B work_landing_symbolic/affine/verify_affine_algebra.py
    python -B work_landing_symbolic/affine/verify_affine_canonical.py     # Calendar(512), P<=256
    python -B work_landing_symbolic/affine/verify_affine_synthetic.py
    python -B work_landing_symbolic/affine/verify_affine_obstructions.py  # O1/O2/O3
    python -B work_landing_symbolic/affine/verify_affine_landing.py
    python -B work_landing_symbolic/affine/verify_affine_falsify.py

An **inline** sanity check (no file written, not a deliverable [B]) was run during this
planning round: 20,000 random a-step origins and 20,000 random b/c origins, exact
Fractions, zero mismatches for all identities of §1.2-§1.3 and Lemma A2/A3; the O2 gadget
gave `(e,record)=(2,7),(4,9),(6,11),(8,13),(14,19)` for `m=6,8,10,12,18`; the O1 identity
`v2(y+2eta_r)=4+v2(A_1*3^r+1)` held for `r=1,2,3,5`. These are consistency observations
only and are not claimed as verified ranges.

---

## 11. One-paragraph summary for the coordinator

The affine origin turns landing into a one-step valuation trichotomy. In the deep regime
`j>=N0+1`, `|theta|<=B-3`, the accepted deep trichotomy (work_deep Lemma 2.2/2.3) already
forbids the tie, so the affine run is U-free within two chains with records `<=J`
unconditionally. Everywhere else the only way a record can exceed `J` is a tie
`v2(3k+theta)=j-2`, whose exact cost is `e = v2(A'U+beta')-(j-1)>=1`, giving record `J+e`
and requiring `U mod 2^{e+1}`. This single quantity `e` is exactly what the W budget lacks
(O2: `W=8`, `e=m-4`, record `m+1`), exactly what O1 makes large (`e>=sigma-J` for the
dangerous `r`), and exactly what O3 says a local phase class cannot supply. The landing
class itself is always a small-height class independent of `U`, computable from
`(beta,d,j,k)`, and certifiable by the accepted window/rational/DEEP machinery except in
the explicitly listed open cases. The remaining hypotheses are therefore source/phase
conditions (no shallow tie or `e<sigma-J`; certified landing class; `sigma>J`), not
parameter caps.


---

## 12. Revision after the first implementation run (2026-10-23)

Command run: `python -B work_landing_symbolic/affine/verify_affine.py` (exit 0, PASS,
4.1 s, 0 failures; JSON `work_landing_symbolic/affine/checks.json`). The theorem
statement of §0 is **not** changed. Four interpretation points are clarified, and one
test-plan item is corrected.

1. **`J` is the current record; re-anchor at every chain.** The canonical verifier builds,
   at each chain `(x,Theta)` with true accumulated loss `Gamma`, the balanced origin
   `J := j+Gamma = record`, `alpha := 2^{-Gamma}`, `beta := x - 2^j U`,
   `d := (Theta - 2^J U - 1)/3`. Then `v2(alpha)=-Gamma`, `v2(A)=j`, `v2(beta)>=j+1`, and
   `d in Z[1/3]` (not always `Z`). All 419 canonical chains admit this origin (0 anchor
   failures). The statement already covers it because `C0` allows `d in Z[1/3]`; the
   source-root representation (`alpha=1,beta=0,d=0`, `J=P`) is the special case used in
   the epoch replay. "Records `<=J`" is therefore the statement that the walk does not
   exceed the record at the re-anchoring chain -- the per-step monotonicity form.
2. **The c-source `sigma` is a precision, not a parameter.** For an odd c crossing `n`,
   the source chain is the epoch chain at state time `tau(n)`; its *parameter* is
   `v2(x)`, while `n-eps` is its *precision* `sigma_c`. All 84 c sources satisfy
   `x = 3*tau+4+lambda_Y` and are matched to the epoch chain by state time
   (0 mismatches). The `336 = 252+84` and `5712 = 336*17` gates reproduce exactly.
3. **`C` is conservative at ties.** The implementation returns `C` false at every tie,
   including ties with `e < sigma-J`, because clause C4 also requires the resolved
   continuation to be re-certified. Five counterfactual shifts of canonical sources
   produce ties (`(P,eta,e,j_next,record)` = `(5,fire,4,4,8,9)`,
   `(14,6132,3,2,6,8)`, `(87,...,3,1,5,7)`, `(158,...,3,3,7,9)`,
   `(231,...,3,1,5,7)`); every one is exact-safe (`records < sigma`) and every one is
   rejected by `C`. This is the expected sufficient-but-not-necessary behaviour and is
   kept verbatim in `checks.json` (`canonical_tests.shift_ties`). It is *not* a failure
   of the theorem; it is the gateway obligation of C4.
4. **F9 (provenance) is corrected.** The plan's F9 said "`d not in Z` kills the
   direction". After re-anchoring, `d` may be in `Z[1/3]`; the criterion's C0 explicitly
   allows that. The implemented F9 checks `d in Z[1/3]` and `v2(beta)>=j+1` (419/419
   pass) and separately the source-root representation has `d in Z` by construction.
   The correct provenance statement is: the *source-root* affine data have `d in Z`,
   `beta in Z[1/2]`, `Gamma in Z`; a re-anchored balanced representation may have
   `d in Z[1/3]`.
5. **Coverage actually achieved.** 252 fires, 419 chains, 84 c sources, 167 step and
   landing-class checks, 5,712 shift cases, `C` true 503/503 with 0 unsafe, 30,000
   a-step and 30,000 b/c synthetic cases, 126 O2 gadgets (252 tie representations),
   504 O1 identity cases and 5 dangerous-residue depths. F1 (deep `j>=N0` two-chain)
   was **not** run: `Calendar(B)` would need `B>=2*10^7`, above the `B<=1024` limit.
   The deep part of Theorem AFF(i) remains `[A-imp]`, not `[B]`.
