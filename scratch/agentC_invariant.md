# Agent C — list-level invariant for "1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE"

Tags: **[A]** = proved for all parameters (proof given/indicated here), **[B]** = mechanically
verified finite check (script named), **[C]** = conjecture.
All scripts are in `D:\math_cc\scratch\` (`agentC_*.py`, Python 3 stdlib only).

---

## 0. Executive summary

I did **not** find a single-line closed invariant, but I found something stronger than expected:
a complete **structural theory of the orbit** in which every fire (odd step) belongs to an explicit
finite-by-depth family, and **every family satisfies one uniform, provably-halting-excluding law**:

> **MASTER LAW.** At every fire inside every excursion, `x = α·w + γ` with `α > 0`, `γ > 0`,
> `v2(γ) < v2(α)`, where `w` (odd ≥ 1) is the excursion parameter. By the Affine Exclusion Lemma
> (Lemma 6, [A]) this makes `x ≠ 2^K` for **every** odd `w` and every `K`, i.e. q ≥ 3 (in fact
> q ≥ 3·2^{v2(α)−v2(γ)} ≥ 6 whenever γ ≥ 2^{...}; always q ≥ 3 — see Lemma 5/6).

The master law was verified on **374,114 distinct fire families** (all excursions `E(w,v)` with
`v ≤ 1500`), on the orbit for **4·10^6 steps** (1.5M fires, min q = 19), for all odd `w ≤ 61` with
`v ≤ 500`, 3000 random odd `w ≤ 10^15` with `v ≤ 64`, and against the **raw Turing machine**
(6·10^7 TM steps). What is *missing* for a complete proof is one induktive step: proving that the
annotated-grammar transitions (§4) preserve the master law for all `v` — a finite, fully tabulated
case analysis whose every rule I state and whose algebraic core is proved below (§5–§8). The only
rule families not hand-proved are the k ≥ 5 "interlude" landings (§8.3), which are tabulated and
verified but not yet written out as proofs.

---

## 1. Independent re-verification of the audited reduction [A][B]

Script: `agentC_verify.py`, library `agentC_lib.py`.

* I re-parsed the machine (note: `E0 → 1LF` moves **Left** — with the opposite convention the
  machine halts in 12 steps) and simulated it directly (dict tape) for 6·10^7 steps.
* **Alignment rule discovered:** the top-map list `(A, b, c, …)` equals the TM moment encoding
  `(h; r1..rk) = (0, A, b, c, …)` — i.e. the moments where state A reads 0, the head sits at the
  **left edge** (`h = 0`), and the right side has **no interior 0-runs** (`ri ≥ 1`).
* All 351 such "clean" moments produced by 6·10^7 TM steps match the top-map orbit
  `L_0=(3), L_1=(4,2), …` **exactly**, and no halt occurred. The top map is the return map on
  clean moments. [B]

The top map on lists (missing entries = 0), for `L = (A,b,c,S)`:

```
A even:  T(L) = (A+b+c+3, S)
A odd:   m := b+(A-3)/2; stack := (c+(A+1)/2, S);
         while m odd and m>=3: stack = (m+3)/2 :: stack; m := (m-3)/2
         m=1 -> HALT;  else T(L) = (m+4, stack)
```

**Lemma 1 (halting criterion) [A].** Let a *fire* be a step whose list has odd head `a`
(writing `b` = second entry, `x = a + 2b + 3`, `x = 2^k·q`, `q` odd). HALT occurs iff some fire
has `x = 2^K` with `K ≥ 3`.
*Proof.* Put `z = x/2 = m+3` at an odd step. The while-loop replaces `z ← z/2` while `z` is even
and `z ≥ 6`; it returns "HALT" iff `z` ever equals 4, i.e. iff `z` is a power of two ≥ 4. ∎
(Empirically `a ≥ 3` at all fires, so `x ≥ 6`; `x=4` would need `a=1,b=0`, never observed.)

**Lemma 2 (checksum) [A].** `sum(T(L)) = sum(L)+3` in both branches; hence `sum(L_n) = 3n+3`.
Verified at every step of every run in this note. [B]

---

## 2. Singletons are safe; every excursion is `E(w,v)` [A]

**Lemma 3 [A].** If `L_n = (3n+3)` with `n` even (singleton fire; `n` odd gives an even head and a
plain even step to the next singleton), then `x = 3(n+2) = 2^v·3w` with `w` odd ≥ 1, `q = 3w ≥ 3`
(no halt), and

```
L_{n+1} = E(w,v) := (3w+1, 3w, 6w, …, 3w·2^{v−2}, 3w·2^{v−1} − 1).
```

*Proof.* Direct substitution in the odd branch; the seam `c+(a+1)/2 = (3n+4)/2 = 3·2^{v−1}w − 1`
is exactly twice the last chain entry minus 1. ∎  (This reproduces the context's `E(w,v)` and
Lemma E; matches all data.)

So: **non-halting ⟺ no excursion `E(w,v)` (w odd ≥ 1, v ≥ 1) ever contains a fire with `q = 1`.**
All heavy verification below is done on excursions directly (`agentC_excursion.py`,
`agentC_master.py`, `agentC_family*.py`), which is exponentially cheaper than orbit simulation.

---

## 3. The grammar: annotated lists [B, preservation trivial]

Scripts: `agentC_annot.py`, `agentC_annot2.py`. Every entry of every list the orbit visits is of
one of three *roles* (assigned at construction time):

* `('R', β, i)` — a **run** entry with value `β·2^i`, `β` odd (chain entries of a fire with
  quotient `q` get `β = q`; the excursion's own entries get `β = 3w`);
* `('T', ρ)` — a **tail**: value `2ρ−1` (always the last entry of the excursion's E-block);
* `('S',)` — a **seam**: the value `c + (a+1)/2` pushed by a fire (a seam whose value happens to
  equal `2·(last chain entry)−1` is tagged T; this happens exactly for singleton-parent fires).

Runs of equal `β` always appear with *consecutive* indices `i` (verified: 0 anomalies in 4·10^6
steps and in all excursion runs) — i.e. the list is a stack of **geometric blocks** separated by
seams, each E-block ending in a tail. Grammar preservation under T is trivial: even steps only
*consume* entries from the front; odd steps *create* a fresh geometric chain (base q) plus one
seam. The only non-trivial content is the **head-offset dynamics** (§5).

**Position data at a step.** Let `e1` = first entry, and

```
σ := e1        (role R or S)
σ := e1 + 1    (role T;  e1 = σ − 1)
i := v2(σ),    D := head − σ.
```

Empirical facts (all of §3–§8 verified on the full universes in §9):

* At **every** R- or T-step: `D = 3t+1` with `t ≥ 0` (i.e. `D ≡ 1 (mod 3)`), and
  `3t + 4 < 2^i` whenever `t ≥ 2` ("room"). 0 violations in 4·10^6 orbit steps + all excursions.
* Fires occur exactly when the head is odd, which at R/T positions means `t` even ≥ 2 (σ even).

---

## 4. Fire algebra and the Safety Lemma [A]

**Lemma 4 (x-law) [A].** At any fire, with `(σ, D)` as above:
`role R or S:  x = 3σ + (D+3)`;  `role T:  x = 3σ + (D+1)`.
*Proof.* `x = head + 2·e1 + 3` and `head = σ + D` (with `e1 = σ` or `σ−1`). ∎
[0 violations in > 10^6 recorded fires.]

**Lemma 5 (valuation-gap safety) [A].** If at a fire `x = 3σ + R` with `R > 0` and
`v2(R) < v2(σ) = i`, then `k := v2(x) = v2(R)` and

```
q = x / 2^k  =  3·β·2^{i−v2(R)}  +  R/2^{v2(R)}   ≥  3·2^{i−v2(R)}  ≥ 6 ,
```

so the fire is safe. *Proof.* `v2(3σ) = i > v2(R)` ⇒ `v2(3σ+R) = v2(R)`; divide. ∎

This is the *only* safety mechanism needed at R/T fires, and it is exactly the required
"coupling of 2-adic valuation with size": the condition `v2(R) < i` with `R ≤ 3t+4` follows from
the room inequality `3t+4 < 2^i`, i.e. from `i ≥ t+2` (since `3t+4 < 2^{t+2}` for `t ≥ 2`). So:

**Corollary 5.1 [A].** Every fire at an R/T position with `t ≥ 2` and `i ≥ t+2` is safe
(indeed `q ≥ 3·2^{i−v2(3t+4)}` resp. `3·2^{i−v2(3t+2)}`).

Observed fire table (orbit, 4·10^6 steps — the complete set of R/T fire *types* is the same for
all excursions, see §7):

| role | D | t | i | k=v2(R) | q (β = block base, odd ≥ 3) | count |
|------|-----|---|----|---------|------------------------------|--------|
| R | 7 | 2 | 4 | v2(10)=1 | 24β+5 | 62499 |
| T | 7 | 2 | 4 | v2(8)=3 | 6β+1 | 62500 |
| R | 13 | 4 | 7 | v2(16)=4 | 24β+1 | 7812 |
| T | 13 | 4 | 7 | v2(14)=1 | 192β+7 | 7812 |
| R | 25 | 8 | 11 | v2(28)=2 | 1536β+7 | 488 |
| T | 25 | 8 | 11 | v2(22)=1 | 3072β+11 | 488 |
| R | 31 | 10 | 13 | v2(34)=1 | 12288β+17 | 122 |
| T | 31 | 10 | 13 | v2(32)=5 | 768β+1 | 122 |
| R | 37 | 12 | 16 | v2(40)=3 | 24576β+5 | 15 |
| T | 37 | 12 | 16 | v2(34)=1 | 98304β+19 | 15 |
| … | … | … | … | … | q = 3·2^{i−k}β + R/2^k | … |

The sequence of `(t, i)` pairs continues `(2,4), (4,7), (8,11), (10,13), (12,16), (16,21),
(18,23), (20,26), (26,31), (28,34), (32,39), …` with `i − t ≥ 2` always (min 2 at the start;
`i−t = 133` at `t = 1064` inside `E(1,1200)`), see §8.

---

## 5. The affine-in-w master law

**Lemma 6 (Affine Exclusion) [A].** Let `α > 0`, `γ > 0` with `v2(γ) < v2(α)`. Then for every odd
`w ≥ 1` and every `K ≥ 1`: `α·w + γ ≠ 2^K`. *Proof.* Write `γ = 2^v γ'`, `α = 2^v α'` with
`v = v2(γ)`, `γ'` odd, `α'` even. If `αw + γ = 2^K`, divide by `2^v`: `α'w + γ' = 2^{K−v}`. The
left side is `even + odd = odd`, so `K = v` and `α'w + γ' = 1`; but `α'w ≥ 2` and `γ' ≥ 1`.
Contradiction. ∎

**Lemma 7 (w-independence of valuations) [A].** If `v2(γ) < v2(α)` then `v2(αw + γ) = v2(γ)` for
**every** odd `w`. *Proof.* `αw + γ = 2^{v2 γ}(α'w + γ')` with the bracket odd. ∎
This is why the entire dynamics (fire types, k-values, dive positions) is *independent of w* —
the sole w-dependence anywhere is the explicit value of seam-relative offsets at S-fires
(e.g. `D = 24576w + 7`), and even those have x affine with the valuation gap.

**Master Law (empirical) [B].** For every `v ≥ 1` and every fire of the excursion `E(w,v)`:

```
x = α_{v,s} · w + γ_{v,s},      α > 0,  γ > 0,  v2(γ) < v2(α).
```

Verified: all `v ≤ 1500` (374,114 families; α, γ fitted from `w ∈ {1,3}`, affinity re-checked at
`w ∈ {5,7,9,11,21,101}`, `v ≤ 250`, plus the random-`w` sweep below). Moreover `q = (αw+γ)/2^{v2γ}`
is then odd and `≥ 3` for all odd `w ≥ 1` — non-halting for **all** w at once, per family.

*Why the master law is preserved (mechanism, provable per transition):* quantities evolve
affinely in `w`. The two nontrivial productions are (i) the fire value `x = 3σ + R`:
`(α_x, γ_x) = (3α_σ, 3γ_σ + R)`, and `v2(γ_x) = min(v2(γ_σ), v2(R)) < v2(α_σ) = v2(α_x)` exactly
when `v2(R) < v2(σ) = v2(γ_σ)` (Lemma 7) — i.e. the master law at fires *is* Lemma 5's condition;
(ii) the new chain base `q = x/2^k`: `(α_q, γ_q) = (α_x, γ_x)/2^{v2(γ_x)}`, which again satisfies
`v2(γ_q) = 0 < v2(α_q)`. Heads merge entries (sum of affines), seams are `c + (a+1)/2` (affine).
So the induction is: *all* tracked quantities stay affine with the gap condition — this is
Lemma 7 making every valuation w-independent, so the dive (§8) is a single deterministic object.

---

## 6. The S-fires (b = seam) — the only fires off the R/T pattern

Three subfamilies occur (all inside excursions; all satisfy the master law):

1. **In-chain S-fire `(S, D=7, i=4)`, k=1.** After a fire with `k ≥ 6` (chain of ≥ 5 entries), the
   chain block itself fires at its position `i = 4` (the `(R,7,4)` algebra with σ = `16q'`):
   `x = 3s + 10`, `k = v2(10) = 1 < 4 = v2(3s)`: safe by Lemma 5. [A given the position]
2. **Endgame S-fire, `D = 24576w + 7`, `i = 4`, `k = 1`** (occurs e.g. in `E(w,14)`, `E(w,30)`-type
   endings; 122 instances in 4·10^6 orbit steps at `n = 16396 + 32768j` for w=1). Here the head
   `= 16q'+7` faces the *seam* `s` with `v2(s) = 4` and `x = 3s + (D+3)`, `v2(D+3) = 1 < 4`:
   safe by Lemma 5 again, and `q = (3s + D+3)/2 ≥ (3·12304 − …)/2`, explicitly
   `x = 61498 + 122880j` for w=1. [A given the position; position verified in family runs]
3. **Landing-below-seam S-fires, `D < 0` huge, `i ∈ {0,1}`, `k ∈ {1,3}`** (end of deep dives,
   `v ≡ 1,2 (mod 4)`-type endings, e.g. in `E(1,65)`, `E(1,66)`). The head `= 4^j q' + 3j + 1`
   (`j = (k_parent−1)/2 ≥ 2`) sits *below* the seam: `x = 4^j q' + 2s + 3j + 4 > 2s ≥ 190`.
   Mechanism: `x = 2s + H` with `H = 4^j q' + 3j + 4`, `v2(H) = v2(3j+4)` (since `3j+4 < 4^j`);
   observed `k ∈ {1,2,3,4}` only, giving `q ≥ x/16 ≥ 2s/16 ≥ 23`. The *complete* exclusion for
   this family is via the master law (affine, gap) — no deep-tie case ever occurs in 374k
   families. [B]

---

## 7. Excursion anatomy and the dive [B + algebraic rules [A]]

Script: `agentC_excursion.py`, `agentC_dive.py`, `agentC_dive3.py`, `agentC_probe.py`.

An excursion `E(w,v)` (w odd) evolves as a single **dive** down its own geometric block, punctuated
by fires; each fire pushes a fresh chain (a *nested block* of length `k−1`) which is consumed
within `≈ k/2` steps, after which the dive continues **in the same E-block** at a deeper position
(`i → i + 2` or `i + 3`), with the offset parameter advancing `t → t + Δt(k)`. Chains with
`k ≥ 6` host one in-chain fire at their own `i = 4` (family 6.1). When the runs run out the
endgame produces a T-fire or an S-fire (families 6.2/6.3) and the excursion returns to a
singleton. Example (`E(1,30)` states as (role, D, i)):

```
(R,1,0) (R,4,2) (R,7,4)FIRE  (S,−46,·) (R,13,7)FIRE  (R,1,0) (S,4,2)
(R,22,9) (R,25,11)FIRE  (S,1,0) (R,31,13)FIRE  (S,−24574,4) (R,37,16)FIRE
(R,1,0) (S,−196603,0) (R,46,19) (R,49,21)FIRE  (S,1,0) (R,55,23)FIRE
(S,−25165822,2) (R,61,26)FIRE  (R,1,0) (R,4,2) (S,7,4)FIRE  (S,−352321549,0) (S,77,0)FIRE → singleton
```

Verified for all odd `w ≤ 61` (and spot `w ≤ 101`, `w = 10^6+1`, `w = 10^{30}+1`, random
`w ≤ 10^{15}`) and all `v ≤ 500/1500`: **every excursion ends in a singleton; no fire has q < 3**;
the fire sequence of `E(w,v)` is independent of `w` except the S-fire constants (affine in w). [B]

---

## 8. The dive map and the room invariant

**8.1 In-block step [A].** At an R-position with `2` more entries in the block:
`head' = head + σ + 2σ + 3`, `σ' = 4σ` ⟹ `D' = D + 3`, `i' = i + 2`. (Same arithmetic when the
pair `(run, tail)` is consumed, relative to `σ' = 4σ` where the tail is `4σ − 1`.)

**8.2 Landing after a mid-block fire (c = next run) [A for k ≤ 4].** Fire at `(t, i)`, `k = v2(3t+4)`:

```
k odd :  land before run i+3 with  D_land = (R + 3t + 3k + 7)/2  = 3t + (3k+11)/2
k even:  land before run i+2 with  D_land = (R + 3t + 3k + 4)/2  = 3t + (3k+8)/2
```

and if `D_land` is even (no fire) one more in-block step gives `(D_land+3, i_land+2)`.
*Proof (k odd; the even case is the same computation with the last chain entry paired with the
seam and landing before run i+2):* before the fire the list is `(σ+3t+1, σ, 2σ, 4σ, …)` with
`x = 3σ+R`, `R = 3t+4`, `q = x/2^k`. After `(k−1)/2` in-block steps the head is
`q·2^{k−1} + (3k−1)/2 = x/2 + (3k−1)/2`, sitting before the seam `s = c + (a+1)/2 =
2σ + (σ+3t+2)/2 = (5σ+3t+2)/2` (here `c = 2σ` = run i+1). The next even step consumes
`(head, s, run i+2 = 4σ)` and lands before run `i+3 = 8σ`, so

```
D_land = x/2 + (3k−1)/2 + s + 4σ + 3 − 8σ
       = (3σ+R)/2 + (3k−1)/2 + (5σ+3t+2)/2 − 4σ + 3 = (R + 3t + 3k + 7)/2,
```

all σ-terms cancelling (this cancellation is *why* the dive is w- and β-independent).
Verified numerically: k ∈ {1,2,3,4}: 52,668 checks, 0 mismatches (`agentC_landing2.py`). [A][B]

**8.3 Interludes, k ≥ 5 [B].** k = 5: the chain (4 entries) is consumed in 2 steps, the head
`16q'+7` fires at the **seam** (family 6.3), net `(Δt, Δi) = (6,4)`. k ≥ 6: an in-chain fire at
chain-position 4 (family 6.1) intervenes, net `(Δt, Δi)` per the table below. These rules are
tabulated from `E(1,1200)` (362 E-block fires) and hold for every excursion tested; the algebra
is the same σ-cancellation but I did not write out the proofs.

**Dive map table** (`Δt, Δi` as functions of `k = v2(3t+4)`; from `E(1,1200)`, counts shown):

```
k :   1     2     3     4     5     6     7     8     9    10
Δt:   2     2     4     4     6     6     6     8     8    10
Δi:   3     2     5     4     4     5     4     6     2     5
Δ(i−t): +1    0    +1    0    −2    −1    −2    −2    −6    −5
count:130    99    65    34    16     9     4     2     1     1     (in E(1,1200))
```

**8.4 Room invariant [B + drift argument].** `i − t ≥ 2` at every dive fire of every excursion
tested (min = 2, only at `(t,i) = (2,4)`; `i − t = 133` at `t = 1064`). Mechanism: `k = 1` fires
(`t ≡ 2 (mod 4)`, exactly) and `k = 3` fires gain `+1`; `k ∈ {2,4}` are neutral; `k ≥ 5` fires
occur only when `32 | 3t+4` (`t ≡ 20 (mod 32)`, at most one dive visit per 32 of t, by the
Δ-pattern), and their losses (1–6, with the worst `−6` only when `512·… | 3t+4`, i.e. once per
4096 of t) are dominated by the ≈ +4 gain per 32 of t. Since `3t+4 < 2^{t+2} ≤ 2^i` for `t ≥ 2`,
room ⟹ `v2(3t+4) < i` ⟹ safe by Corollary 5.1. A fully rigorous proof is a finite 2-adic periodic
induction on `t mod 2^m` (m ≤ 11) of this one-dimensional map — elementary, not yet written. [C→B]

---

## 9. Verification tallies [B]

| Check | Universe | Result | Script |
|---|---|---|---|
| TM ↔ top-map alignment | 6·10^7 TM steps (351 clean moments) | exact match, no halt | `agentC_verify.py` |
| Orbit fires: q ≥ 3, C7 (`q ≥ 2^k`) | 4·10^6 steps, 1.5·10^6 fires (142k non-singleton) | min q = 19 (at n=33); min q/2^k = 19/8 | `agentC_orbit.py` |
| Grammar (roles, contiguity, values) | 4·10^6 steps | 0 violations | `agentC_annot.py` |
| x-law (Lemma 4), D ≡ 1 mod 3, room | all excursion runs | 0 violations | `agentC_annot2.py`, `agentC_landing2.py` |
| Every excursion ends; no danger fire | odd w ≤ 61, v ≤ 500; w=1, v ≤ 1500 | all end; min q ≥ 3 everywhere | `agentC_master.py`, `agentC_dive.py` |
| Master affine law (374,114 families) | v ≤ 1500 (fit w=1,3; check w ∈ {5,…,101}) | `γ>0`, `v2(γ)<v2(α)`: 100% | `agentC_family.py`, `agentC_family2.py` |
| Landing formulas k ≤ 4 | 52,668 mid-block fires | 0 mismatches | `agentC_landing2.py` |
| Random w sweep | 3000 odd w ≤ 10^15, v ≤ 64 (28,444 fires) | no q < 3 | `agentC_final.py` |
| Long orbit | 2·10^7 steps (7.5·10^6 fires) | no halt; min q = 3 only at the initial singleton fire n=2; min non-singleton q = 19 | `agentC_final.py` |

Also confirmed the context's negative-result boundary: the safety condition is *not* a congruence
on x (x mod 3 ∈ {1,2}, q mod 8 varies), but the valuation-gap condition `v2(γ) < v2(α)`, which
couples valuation with size exactly as required.

---

## 10. Theorem status and what is still needed

**Theorem (proved, conditional) [A].** *If* the Master Law of §5 holds for all `v ≥ 1` (equivalently:
the grammar + dive rules of §4/§8 cover all reachable states), *then* the machine never halts.
Proof: Lemma 3 (singletons), Lemma 6 (excursion fires: `x = αw+γ ≠ 2^K` for all odd w, all K). ∎

**Unconditional pieces proved here [A]:** Lemmas 1–8 (halting criterion, sum, excursion form,
x-law, valuation-gap safety, affine exclusion, w-independence, in-block + k ≤ 4 landing algebra).

**Remaining gap (exactly this):**
1. Write the preservation induction for the annotated grammar: every reachable state is a stack
   of blocks with roles as in §3 and every fire is one of the families §4/§6. All transition
   rules are listed (§8.1–§8.3); the k ≥ 5 interlude landings need their σ-cancellation proofs
   written out (the k ≤ 4 template applies verbatim).
2. Prove the room invariant `i ≥ t+2` for the one-dimensional dive map of §8.4 (finite 2-adic
   periodic induction; mechanism verified, statement [C] pending that write-up).
With (1)+(2) the Master Law follows for all v and the non-halting proof is complete.

**Conjecture C-C7′ (strengthened C7) [C]:** at every non-singleton fire `q ≥ 3·2^{i−k}` where
`(t, i)` is the dive position and `k = v2(3t+4)`; empirically `q ≥ 19` throughout 2·10^7 steps.

---

## 11. Script inventory (all in D:\math_cc\scratch)

`agentC_lib.py` (TM + top map + v2), `agentC_verify.py` (TM↔orbit), `agentC_orbit.py` (4M-step
fire census), `agentC_probe.py` (orbit segments), `agentC_annot.py`/`agentC_annot2.py` (grammar
checks, fire taxonomy), `agentC_excursion.py` (E(1,v) v ≤ 40 + state dumps),
`agentC_dive.py` (w ≤ 15, v ≤ 160 safety + dive sequences), `agentC_master.py` (grand validation
w ≤ 61, v ≤ 500), `agentC_strace.py` (S-fire traces), `agentC_family.py`/`agentC_family2.py`
(374,114 affine families + exclusion), `agentC_landing.py`/`agentC_landing2.py` (landing laws),
`agentC_dive3.py` (dive map from E(1,1200)), `agentC_final.py` (random-w sweep + 20M orbit).
