# Affine-origin landing — RESULT (final)

2026-10-23. Direction A (affine origin). **Decisive gate: exit code 0, `status: PASS`,
0 failures** (`python -B work_landing_symbolic/affine/verify_affine.py`, 3.02 s in the
gate run; my own run also PASS, 6.6 s). JSON: `work_landing_symbolic/affine/checks.json`.
No global EXT claim; K_clock unchanged; only files under
`work_landing_symbolic/affine/` were written; no git commit.

**中文摘要.** 仿射来源 `x=A·U+beta, Theta=2^J·U+3d+1` 的 a 步被精确三分：着陆
（`v2(3k+theta)<=j-3`，参数 `1+r`，类 `3-theta mod 2^{j'+1}`，记录 `<=J-1`）、悬挂
（`v2>=j-1`，参数 `j-1`，记录 `J`）、碰撞（`v2=j-2`，参数 `j+e`，`e=v2(A'U+beta')-(j-1)>=1`，
记录恰为 `J+e`，需 `U mod 2^{e+1}`）；b/c 步必然着陆于 `omega(n)`，类
`theta+Phi-2 mod 2^{omega+1}`，记录 `<=J-1`。深段 `j>=N0+1, |theta|<=B-3` 无碰撞，
至多两条链成为 U-无关，记录 `<=J`。碰撞是记录超过 J 的唯一机制，安全判据为
`e<sigma-J`。规范 Calendar(512) 的 252 火 / 419 链 / 84 c 源 / 5712 移位全部通过；
判据 C 在 503 个实例上成立且 0 不安全；O1、O2 都被精确定位。未证明全局 EXT。

---

## 1. Precise theorem, hypotheses, tags

**Setting.** `N0=2*10^7`, `B=2^{10^7}`, `J<sigma`, `Gamma>=0`, `j=J-Gamma`,
`A=2^J*alpha`, `v2(alpha)=-Gamma`, so `v2(A)=j`; `U` odd; `beta in Z[1/6]`;
`d in Z[1/3]`; `x=A*U+beta`; `Theta=2^J*U+3d+1`; `theta=3d+1-beta in Z[1/3]`;
`record=j+Gamma`. Note `J` is the **current record**, i.e. `J=j+Gamma` at the chain
where the origin is anchored (re-anchoring is allowed: `alpha=2^{-Gamma}`,
`beta=x-2^j U`, `d=(Theta-2^J U-1)/3`). The source-root origin
(`alpha=1,beta=0,d=0,J=P`) is the special case with `d in Z`.

> **Theorem AFF.**
> **(A1) [A] One-step recursions.** `Theta-x ≡ theta (mod 2^j)`. An a-step with
> `tau(j-1)=2k` gives `alpha'=2-alpha/2`, `beta'=6d+2+6k-beta/2`, `d'=d+1+2k`,
> `Gamma'=Gamma+1`, `v2(alpha')=-Gamma-1` (five-input `beta'=6d+8-beta/2`); a b/c-step
> with `ratio=c'_W/2^j` gives `alpha'=ratio*alpha`, `beta'=ratio*beta+lambda'_W`,
> `d'=d+1+tau`, `Gamma'=Gamma+1+eps`, `v2(alpha')=-Gamma-1-eps`, `v2(beta')=omega`.
> **(A2) [A] a-step trichotomy and tie ledger.** With `r=v2(3k+theta)` and `ell'=j-1`:
> `r<=j-3` ⇒ landing, `v2(beta')=r+1`, `j'=r+1<=j-2`, record `<=J-1`, class
> `3-theta (mod 2^{j'+1})`; `r=j-2` ⇒ tie, `v2(beta')=ell'`, `j'=ell'+e` with
> `e=v2((A'/2^{ell'})U+beta'/2^{ell'})>=1`, record exactly `J+e`, continuation needing
> `U mod 2^{e+1}`; `r>=j-1` ⇒ suspension, `v2(beta')>=j`, `j'=j-1`, record `J`.
> **(A3) [A] b/c is always a landing.** `v2(beta')=omega(n)<v2(A')`, `j'=omega(n)`,
> class `theta+Phi-2 (mod 2^{omega+1})`, record `<=J-1`.
> **(A4) [A-imp + A] Deep two-chain U-freedom.** If `j>=N0+1` and `|theta|<=B-3`, no tie
> occurs; the affine run is U-free after at most two chains and every record is `<=J`
> (every non-root chain `<=J-1`, except an even crossing after a resonance, which is
> terminal with record `J`).
> **(A5) [A-cond; finite instances B] Criterion.** If no tie occurs, the terminal class
> is certified, and `sigma>J`, then the whole walk has records `<sigma`, uniformly in
> `U` and with no upper bound on `J`. If a tie of depth `e` occurs, the tie's own record
> is `J+e`, and `e<sigma-J` is the exact safety condition; the continuation is a
> separate obligation.

**Hypotheses (each checked against "is it a parameter bound?").**

1. *Reached affine origin* (`x=A U+beta`, `Theta=2^J U+3d+1`, `U` odd, `v2(A)=J-Gamma`,
   `beta in Z[1/6]`, `d in Z[1/3]`; source-root `d in Z`). Source/provenance condition —
   **not** a parameter bound.
2. *Tie-free lift* `v2(beta)>=j+1` (or `v2(beta)<j`: immediate landing). Structural —
   **not** a parameter bound.
3. *Phase height* `|theta+s|<=H` and `h(s+2)<=h` for `s in Z[1/3]`; `H,h` are statement
   parameters. Phase condition — **not** a bound on `J`.
4. *Deep regime* `j>=N0+1`, `|theta|<=B-3` (only for A4). A **lower** bound on the chain
   parameter (CLOCK's size regime) — **not** a cap; `j<N0` is a separate finite/window
   dispatch.
5. *No tie* at shallow a-steps, `v2(3k+theta)!=j-2`; if a tie, `e<sigma-J` and the
   resolved lift with re-certified continuation. A congruence/source condition — **not**
   a parameter bound; it fails at any scale (O1, O2).
6. *Terminal-class certificate*: integer `5<=j_*<2*10^7`, `delta_* in [-12,15]` except
   `(5,5),(5,-11)`; or rational `Q=3^r`, `N_Q=max(N0,4(ceil(log2 Q)+2))<=j_*`; or DEEP.
   The window branch **is** a finite range [B]; the rational branch is source-adaptive;
   DEEP is an open source condition.
7. *Ceiling* `sigma>J` (and `sigma>J+e` at ties). A relation between source quantities
   (precision slack) — **not** a global parameter bound.
8. *Tie continuation* is a separate gateway obligation; A5 does not claim it.

Tag summary: **A1-A3 [A]** (proved in `PLAN.md` §1.2, §3.1, §3.2; re-checked on 60,000
synthetic cases and 167 canonical steps); **A4 [A-imp + A]** (proof `PLAN.md` §3.3,
using accepted work_deep Lemma 2.2/2.3; **not** tested in [B]); **A5 [A-cond]** with
finite instances **[B]**; the imported window, `N_Q`, `certify` and DEEP are
**[A-imp]**, not reproved.

---

## 2. Proof / proof skeleton and the key identities

All identities are over `Z[1/6]`; every valuation decision is 2-adic, and 3 is a 2-adic
unit, so the denominator `3^r` of a source shift is invisible to every valuation and
record statement.

**A1.** Substitute `x=alpha 2^J U+beta`, `Theta=2^J U+3d+1`:
`x' = 2Theta+6k-x/2 = (2^{J+1}-A/2)U + (6d+2+6k-beta/2)`, and
`Theta' = Theta+3+6k = 2^J U+3(d+1+2k)+1`. For b/c with `u=x/2^j`:
`x'=c'_W u+lambda'_W = (ratio*alpha)2^J U + (ratio*beta+lambda'_W)`, because
`ratio=c'_W/2^j` and `c'_W alpha 2^Gamma = ratio alpha 2^J`. Valuations:
`v2(alpha')=-Gamma-1` (a), `-Gamma-1-eps` (b/c); `v2(beta')=omega` because
`v2(ratio beta)=omega+(j+1)+(-1-eps)-j >= omega+2` while `v2(lambda'_W)=omega`.

**A2.** `beta' = 2(3k+theta)+(3/2)beta` (check: `2theta+1.5beta=6k+6d+2-0.5beta`).
`v2(2(3k+theta))=1+r`, `v2((3/2)beta)=v2(beta)-1>=j=ell'+1`. Hence: if `1+r<=ell'-1`,
`v2(beta')=1+r`; if `1+r=ell'`, `v2(beta')=ell'` with no cancellation; if
`1+r>=ell'+1`, `v2(beta')>=ell'+1` (possibly higher), so the parameter is `ell'`.
At a tie, `x'=A'U+beta'=2^{ell'}(aU+b)` with `a,b` odd; `aU+b` is even, so
`e=v2(aU+b)>=1`, `j'=ell'+e`, `record=J+e`.

**A3.** `v2(beta')=omega(n)` and `omega<=j-2-eps` (W's S1), so `j'=omega` and
`record=omega+Gamma+1+eps<=J-1`. The class is `theta+Phi-2 (mod 2^{omega+1})` because
the error `beta(1-ratio)` has valuation `>=j-eps>=omega+2`.

**A4.** At a deep chain work_deep Lemma 2.2 gives `|3k+theta|<2^{j-2}`, hence no tie and
either a landing (`r<=j-3`) or the exact resonance `3k+theta=0`. In the resonance case
`j_1=j-1`, `theta_1=3-theta`, and Lemma 2.3 gives `3k_1+theta_1=3(k_1+k+1)>0`, which
Lemma 2.2 bounds by `<2^{j_1-2}`, so chain 1 is a landing/end/b/c. Records are `J` on
the resonance chain and `<=J-1` on the terminal one.

**A5.** The landing/end chain is U-free: `x'≡beta' (mod 2^{j'+1})` because
`v2(A')>=j'+1`, and `Theta'≡3d'+1 (mod 2^{j'+1})` because `2^J U` is divisible by
`2^{j'+1}`. HP at precision `j'+1` (Prop 3.2) then gives the tail with relative records
`<=j'`, hence global records `<=j'+Gamma'<=J-1<sigma`. At a tie the exact record is
`J+e` and the next state needs `U mod 2^{e+1}`.

**O1 and O2** (the two obstructions) are special cases of A2:
* O2 `u=(2^{m-4}-1)/3`, `x=32u`, `Theta=x+5`, `j=5`, `k=1`, `theta=5`:
  `3k+theta=8`, `r=3=j-2` ⇒ tie; `e=v2(3u+1)=m-4`, record `m+1`; `W=8` is blind to
  `e`; `e<9-5` holds only for `m=6`.
* O1 P=49, `theta=1`, `k=20`, `eta_r=-5+8/3^r`: `3k+theta+eta_r=8(7+3^{-r})`,
  `v2(...)=3+v2(7*3^r+1)`; the tie is `v2(7*3^r+1)=44`. The output is
  `y_r=16(A_1+3^{-r})` with `A_1=15*2^44+7`, `v2(y_r)=48+e`, `record=49+e`; the
  dangerous residue `A_1*3^r=-1 (mod 2^{sigma-5})` forces `e>=sigma-49=sigma-J`.

---

## 3. Gap to the target form and the exact J-dependence

Target: for input phase `theta+s`, `s in Z[1/3]`, height `<=h`, either certify the
landing class, or resolve it by a finite-step gateway with **strictly decreasing
records**, with a bound independent of `J`.

**What matches.**

* `s in Z[1/3]`: realized as `beta->beta-s` (x-shift) or `d->d+s/3` (Theta-shift); the
  class is `theta+s`; the height enters hypothesis 3. A genuine AA/BA/BBBAA shift has
  `s=0,-1,+1,+4/3` (`work_claude_shift/NOTES.md:9-21`, `C5_EXTENSION.md:7-46`).
* Landing/record descent: the a-landing and every b/c landing are `<=2` chains, with
  records `<=J-1`; suspensions keep `J`; ties are the **only** record increases.
* No `J`-dependence in A1-A3, in the trichotomy/ledger, or in the landing step A4-A5;
  `J` enters only as `j=J-Gamma` and as the ceiling comparison `sigma>J`.

**What does not match.**

* The target allows "finite-step gateway with strict records". Our ties are **not**
  certified: C rejects every tie (including the five exact-safe canonical shift-ties
  and O2 `m=6`). The affine ledger gives the tie depth `e` and the record `J+e`, but not
  the continuation; the gateway step is missing.
* The tail certificate is not `J`-free in the deep/rational regime: it uses the finite
  window `j_*<2*10^7` (a genuine range bound, [B]), or `N_Q=max(N0,4(ceil(log2 3^r)+2))`
  (source-adaptive), or DEEP (which costs `log* J` chains and `T_h`).
* The canonical `[B]` corpus is shallow (`j<=256`); the deep clause A4 has no `[B]`
  evidence because `Calendar(B)` would need `B>=N0`.

**Dependence table.**

| item | J | N0 / B | 2*10^7 | T_h / log* J | T4 / K_clock |
|---|---|---|---|---|---|
| A1-A3 (recursions, trichotomy, classes) | only `j=J-Gamma` | no | no | no | no |
| A4 (two-chain, deep) | lower bound `j>=N0+1` | yes (`N0`, `B`) | yes | no | no |
| C1-C4, C6 | `j=J-Gamma`, `sigma>J` | C3 threshold | no | no | no |
| C5 integer window | — | — | `5<=j_*<2*10^7` [B] | no | no |
| C5 rational | — | `N0` floor | — | `[N0,N_Q)` band open | no |
| C5 DEEP | — | — | — | `2*Lambda(J)+1`, `T_h` | no |
| O1 r | no J bound | no | no | no | no |

`K_clock` and `T4` are not used; `T_h` only through the accepted deep-chain count. The
`O1` denominator exponent `r` enters only through `e`; the accepted Theorem S/Lemma ND
(`work_claude_shift/NOTES.md:60-140`) bounds `r` by the number of nested non-descents,
which is a layer count, not a `J` bound.

---

## 4. Additional conditions (source/phase, checkable)

If the criterion is not unconditional, these are the exact hypotheses; each is a
statement about the reached source/phase, not a cap on `J`.

* **(AC1) No shallow tie.** At every a-step of the affine run before the first
  landing/end, `v2(3k+theta) != j-2`, equivalently `v2(beta') != v2(A')`.
  Checkable from `(beta,d,j,k)` alone; `U`-free.
* **(AC2) Tie budget and resolution.** If a tie occurs, `e := v2((A'/2^{j-1})U +
  beta'/2^{j-1})` satisfies `e<sigma-J`, and the actual `U mod 2^{e+1}` is supplied by
  the source, with the continuation re-certified. `e` is the exact record excess
  `record-J`; it is the quantity `W` lacks.
* **(AC3) Terminal class in the certified set.** For the landing class `(j_*,delta_*)`:
  either `5<=j_*<2*10^7`, `delta_* in [-12,15]`, `delta_* not in {(5,5),(5,-11)}`
  (accepted [B]); or `Q=3^r`, `N_Q=max(N0,4(ceil(log2 Q)+2))<=j_*` with the
  ODD_DENOMINATOR condition; or DEEP.
* **(AC4) Ceiling slack.** `sigma>J` (and `sigma>J+e` at ties); for a fire source this
  is the accepted `rho-P>=3` slack.
* **(AC5) O1-specific.** For the reached shift with denominator `3^r`, the dangerous
  residue `A_1*3^r = -1 (mod 2^{sigma-5})` (`A_1=15*2^44+7` in the P=49 instance) is
  excluded, equivalently `v2(7*3^r+1)<44` or `e<sigma-J`. Bounded real height alone
  does **not** imply this (O1).

Each of AC1-AC5 is refutable at any scale; none is "`J` below a constant".

---

## 5. Unresolved points and next steps

1. **Tie continuation / gateway.** C rejects every tie. Five canonical counterfactual
   shifts are exact-safe ties at `(5,5)` (`e=1,2,3,4`); O2 `m=6` is a safe tie. A
   uniform gateway lemma must pair the tie depth `e` with a following descent and
   produce a certified class. Next: use the affine ledger to state the gateway as
   `J_new = J+e` and apply C at the resolved state; the missing input is `U mod 2^{e+1}`.
2. **Deep `[B]` and the two-chain clause.** A4 is analytic [A-imp]; no `B<=1024`
   calendar can reach `j>=2*10^7`. Next: independent review of the A4 constants at
   `j=N0+1`, and a written proof of the `Z[1/3]` extension of work_deep Lemma 2.2/2.3.
3. **Rational `N_Q>j_*` band** (`[N0,N_Q)`), ODD_DENOMINATOR reviewer E2/E3. Next:
   use the actual `Q=3^r` from Theorem S and the layer count to bound `r`, not a cap on
   `J`.
4. **O1's actual `r`** and the dangerous residue. Next: combine Lemma ND (a non-descent
   at `j` needs `2^{j-1} <= 3^r(3(j-1)P(j-1)+2|d|)`) with the layer/record budget to
   exclude the residue at reached sources.
5. **`(5,5),(5,-11)`** beyond the accepted gateway families; the five `(5,5)` shift-ties
   are safe but uncertified.
6. **`H` calibration** and a non-`H` formulation; the 503 canonical instances all have
   `|theta|<=64`.
7. **F1** (a direct [B] falsification of A4) is impossible under `B<=1024`; recorded as
   not run, not as passed.

---

## 6. Reproduction and JSON

    python -B work_landing_symbolic/affine/verify_affine.py
    # exit 0, status PASS, 0 failures; writes checks.json

Gate output (decisive): `status: PASS`, `failures: 0`, 3.02 s;
canonical `fires=252, chains=419, c_sources=84, step_checks=167,
shift_cases=5712, criterion_holds=503, criterion_hold_unsafe=0,
anchor_failures=0, shift_tie_safe=5`; synthetic `a_cases=30000, bc_cases=30000,
trichotomy_cases=30000, bc_landing_cases=30000, class_cases=59962,
record_cases=60000, tie_cases=27, alpha_valuation_checks=60000,
phase_identity_checks=60000`; O2 `cases=126, tie_cases=252, threshold_ok=126`;
O1 `cases=504, identity_cases=504, dangerous_H=5, dangerous_ok=5`.

JSON: `work_landing_symbolic/affine/checks.json` with `status`, `scope`,
`canonical_tests` (including `shift_ties` and `criterion_fail_examples`),
`synthetic_tests` (including 40 per-case `canonical: false` samples), `obstructions`
(O1/O2), `falsification`, `counts` (per-conclusion counts) and `failures` (empty).
Script: `verify_affine.py`; plan: `PLAN.md` (statement, proofs, §12 post-run
revision); this file: `RESULT.md`.

**No global EXT; the accepted horizon is unchanged.**
