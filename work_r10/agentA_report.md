# R10/A: the conservation law of the universal sequence — p_i − k_i ≥ 3 PROVED

**Status: PROVED with C = 3 (the measured optimum).** Unconditionally for every fire with
j ≤ 120, i.e. for every i with k_i ≤ 16·(2^116−2)/3 + 10 ≈ 2.6·10^35 (the entire range in
which every fire's parameter is covered by the machine-certified table); and for ALL i under
the single structural hypothesis (H1) dk(j) ≤ j, dp(j) ≥ 2 for every j — measured to
j = 20000 by the per-J verifier (prior runs; re-certified here to j = 120).

Artifacts: `agentA_proof.py` (all checks V0–V8, runs in 18 s), `agentA_run.log` (its output),
`agentA_data.json` (the certified table and walk tables). Nothing outside work_r10 was
modified; scratch/agentB_run7.py and work_r10/fast_walker.py were imported read-only.

## 0. Object

The universal sequence: p_0 = 4, k_0 = 1; at each fire j = 1 + v2(3k+2) and
k → k + dk(j), p → p + dp(j), with the (dk,dp) table (dk,dp) = (1,3)(2,1·2)... as quoted in
the task. Let Φ := p − k.

## 1. Certification of the inputs [V0, V4]

- **(V0)** For every j = 1..120, `scratch/agentB_run7.py`'s `verify(j)` returns a unique
  (dk, dp) with all class-split branches agreeing, canonical re-entry and u ≥ 3 — the
  table used below. The j = 1..20 values equal the table in the task context, digit for
  digit. Facts used later: **min dp = 2**; **dk(j) ≤ j for all j ≤ 120**.
- **(V4)** The table-driven (p, k, j) stream equals the level-fire stream of the formal map
  F (`work_r10/fast_walker.exact_walker`, = work_g6 §5) on all 60575 fires with i ≤ 2·10^5:
  the object analysed here IS the audited walk. (Table j≤120 ⟂ run7 ⟂ F: three independent
  engines agree.)

## 2. Structural lemmas [Class-A; V1, V2]

**(L1) Fire classes.** j ≥ 5 ⟺ v2(3k+2) ≥ 4 ⟺ k ≡ 10 (mod 16); writing k = 16s+10,
j = 5 + v2(3s+2). For k ≢ 10 (mod 16), j ∈ {1,2,3,4} depends only on k mod 16:
residues 0..15 (≠10) have j = 2,1,4,1,2,1,3,1,2,1,·,1,2,1,3,1. *Proof:* 3 is invertible
mod 16; v2(3k+2) ≤ 3 is decided by 3k+2 mod 16, and 3(16n+r)+2 ≡ 3r+2 (mod 16).

**(L2) Off-spike increments.** For j = 1,2,3,4 the table gives (dk,dp) = (1,3)(1,2)(2,5)(2,4),
so **every off-spike fire increases Φ by +2, +1, +3 or +2 > 0**. Hence Φ is strictly
increasing between spike fires, and minima of Φ over the whole sequence occur only at
i = 0 (Φ = 3) or **immediately after a spike fire**.

**(L3) The residue flow.** Off spikes the walk is r → r + dk(j(r)) with steps 1 or 2
(at r ≡ 2, 6, 14 only). The flow on Z/16 is 0→1→2→4→5→6→8→9→10, 3→4, 7→8, 11→12→13→14→0,
15→0: it reaches 10 from every start and never jumps over it (10 is entered only from 9,
by a +1 step). So **spikes are skipped only by the spike jump itself** (dk(J) ≥ 17,
first at J = 38).

**(L4) Walk tables.** From a fire at residue ρ = k mod 16 (ρ ≠ 10) the k-distance to the
next spike and the Φ-gain of the intermediate fires are fixed, s-independent (V2, verified
by absolute-position brute force over 40 blocks):

| ρ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|
| d | 10| 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0  | 15 | 14 | 13 | 12 | 11 |
| g | 14| 13| 11| 11| 9 | 8 | 6 | 5 | 3 | 2 | 0  | 22 | 20 | 19 | 17 | 16 |

with **g(ρ) ≥ d(ρ) + 1 for ρ ≠ 10** and d(10) = g(10) = 0 (direct landing, see §4).
The pre-spike-0 segment k = 1 → 10 fires j = 1,4,2,1,3,2,1 and lifts Φ from 3 to
**B₀ = 16**.

**(L5) Cycle dynamics.** Let the visited spikes fire at blocks 0 = s₀ < s₁ < …, and let
B_t := Φ just before spike s_t fires, V_t := Φ just after. With J = J_{s_t} and
ρ(J) := (10 + dk(J)) mod 16:

```
V_t     = B_t − drop(J),          drop(J) := dk(J) − dp(J)          (the only Φ-decreases)
B_{t+1} = V_t + g(ρ(J)) = B_t + net(J),  net(J) := dp(J) − dk(J) + g(ρ(J))
s_{t+1} = s_t + m(J),             m(J)  := (dk(J) + d(ρ(J)))/16      (integer, ≥ 1)
```

and the k-bookkeeping per cycle is exact: dk(J) + d(ρ(J)) = 16·m(J). *The conservation law
is exactly the statement* **B_t ≥ 3 + drop(J_{s_t}) for all t** (plus the initial segment,
whose minimum is 3 at i = 0).

## 3. The mined transducer [V6] and why it does not close finitely

For s ∈ [0, 2^14) the inter-spike (dk,dp)-sequence equals `[spike fire (J,dk,dp)] + walk
sequence of r₀ = 10+dk(J)` — a function of s **only through t := v2(3s+2)** (all 16384
instances machine-compared). The classes t = 0..14:

| t | J | dk | dp | r₀ | d | g | net | drop | m |
|---|---|----|----|----|---|---|-----|------|---|
| 0 | 5 | 3 | 4 | 13 | 13 | 19 | +20 | −1 | 1 |
| 1 | 6 | 3 | 5 | 13 | 13 | 19 | +21 | −2 | 1 |
| 2 | 7 | 3 | 4 | 13 | 13 | 19 | +20 | −1 | 1 |
| 3 | 8 | 4 | 6 | 14 | 12 | 17 | +19 | −2 | 1 |
| 4 | 9 | 4 | 2 | 14 | 12 | 17 | +15 | +2 | 1 |
| 5 | 10 | 5 | 5 | 15 | 11 | 16 | +16 | 0 | 1 |
| 6 | 11 | 5 | 4 | 15 | 11 | 16 | +15 | +1 | 1 |
| 7 | 12 | 6 | 6 | 16 | 10 | 14 | +14 | 0 | 1 |
| 8 | 13 | 6 | 4 | 16 | 10 | 14 | +12 | +2 | 1 |
| 9 | 14 | 8 | 5 | 18 | 8 | 11 | +8 | +3 | 1 |
| 10 | 15 | 7 | 5 | 17 | 9 | 13 | +11 | +2 | 1 |
| 11 | 16 | 7 | 4 | 17 | 9 | 13 | +10 | +3 | 1 |
| 12 | 17 | 8 | 6 | 18 | 8 | 11 | +9 | +2 | 1 |
| 13 | 18 | 8 | 3 | 18 | 8 | 11 | +6 | +5 | 1 |
| 14 | 19 | 8 | 2 | 18 | 8 | 11 | +5 | +6 | 1 |

(For s < 2^14 the occurring classes are t ≤ 13 and the deep members t = 15, …; on this
window the map is the pullback of s mod 2^15, with the single (dk,dp)-collision t ∈ {0,2}.)

**No finite modulus closes the transducer.** The deep class s ≡ c_m (mod 2^m) has
3s+2 = 2^m(3u + q_m), i.e. J = 5 + m + v2(3u + q_m): each refinement depth introduces a
**new affine constant** q_m — the depth-2 transducer is not self-similar. This is the same
leakage as the exit/D-entry cascade of work_g6 §4.2. Consequently the proof must go through
the per-J table plus amortization — which is what §5 does.

**The anticipated obstruction is real and first bites at J = 19**: drop = 6 > net = 5
(first occurrence at s = 27306, p ≈ 1.1·10^6 — inside our V3 run; the task's "net ≥ +6,
dp ≥ 22 per cycle" holds only for p < 4·10^5; the true per-cycle minima over the certified
table are net = 5 and dp_total = 21, both at J = 19). Depth-1 induction fails outright
from J = 23 on (all J ≥ 23 have 2·drop > g; net < 0 from J = 28; J = 35..37 have dk ≡ 0
mod 16 — **empty walks**, m = 1, net as low as −14; the first block-skippers are
J = 38..41 with m = 2; J = 120 already has drop 48, net −34, m = 4).

**Depth-2 closure of the non-skipping regime [V6b].** s odd ⟺ v2(3s+2) = 0 ⟺ J = 5.
For s < s₀ := 2863311530 (first block with J ≥ 38, = ((2^33−2)/3·3^{-1}) mod 2^33) every
visited spike has m = 1, so **every block fires** and spikes alternate (J ≥ 6, J = 5):
each 2-cycle nets ≥ 20 − 14 = **+6** while per-cycle drop ≤ **14**; with B₂ = 57 this
gives B_s ≥ 17 = 3 + 14 for all s < s₀ — the invariant holds throughout the regime where
per-cycle repair is possible. Beyond s₀ the walk skips blocks and per-cycle accounting
cannot close; the amortized bound of §5 takes over.

## 4. The global proof: amortized counting bound [V7]

Sum the identities of (L5) over the cycles that bring the walk from block 0 to a visited
spike at block s (C cycles in total): Σ(dk + d) = 16s exactly, hence

```
B(s) = B₀ + Σ_cycles (dp + g + d) − 16 s .
```

Now bound each cycle from below: dp(J) ≥ 2 (table fact); g(ρ) + d(ρ) ≥ 2·d(ρ) (since
g ≥ d+1 off ρ = 10, and g = d = 0 at ρ = 10); and C ≥ s − Σdk/16, because
m − 1 = (dk + d − 16)/16 ≤ dk/16 (d ≤ 15; and m − 1 = 0 when m = 1). Therefore

```
B(s) ≥ B₀ + 2C + 16 s − 2 Σ_{cycles} dk
     ≥ B₀ + 18 s − (17/8) Σ_{cycles} dk(J) .
```

The visited blocks are a subset of all blocks, and block n carries J_n = 5 + v2(3n+2):
the class {v2(3n+2) = t} is an arithmetic progression of difference 2^{t+1}, so it has at
most s/2^{t+1} + 1 members below s, whence

```
Σ_{cycles} dk ≤ Σ_{n<s} dk(5+v2(3n+2)) ≤ ε s + K ,
  ε = Σ_t dk(5+t)/2^{t+1} = 3.167277… ,  K = Σ_{t≤115} dk(5+t) = 3228   (table to j=120)
```

(exact AP sum verified ≤ εs + K at s = 10^3…10^7; bound verified ≤ simulated B on the
10^7-block trajectory). This gives the explicit linear lower bound

```
B(s) ≥ 16 + 11.2695·s − 6859.5 .
```

On the other side, the demand is logarithmic: drop(J_s) ≤ dk(J_s) ≤ J_s = 5 + v2(3s+2)
≤ 5 + log2(3s+2), so B(s) ≥ 3 + drop(J_s) follows from B(s) ≥ 8 + log2(3s+2). Comparing
on every slab of constant bit-length(3s+2) (the bound is linear increasing within a slab):
**the inequality holds for every s ≥ 682** (slab-checked exactly for all 116 slabs of the
certified range).

**Theorem (scope A, unconditional given the table).** For every fire of the universal
sequence with j ≤ 120 — i.e. every i with k_i ≤ 16·(2^116−2)/3 + 10 ≈ 2.6·10^35 —

```
p_i − k_i ≥ 3 .
```

*Proof.* Fires off spikes increase Φ (L2), so minima sit at i = 0 and just after spike
fires (L2–L5). For spike blocks s ≤ 681 the invariant B ≥ 3 + drop was verified cycle by
cycle (V5: exhaustive to s = 10^7; V3: fire-by-fire to p < 1.1·10^6 with the same
conclusion, Φ_min = 3 at i = 0). For s ≥ 682 the counting bound gives
B(s) ≥ 16 + 11.27 s − 6860 ≥ 8 + log2(3s+2) ≥ 3 + drop(J_s), since all blocks s < S₁ :=
(2^116−2)/3 have J_s ≤ 120 (V1) and the table supplies dk, dp ≤ certified values. ∎

**Theorem (conditional closure).** Assume (H1) dk(j) ≤ j and dp(j) ≥ 2 for all j ≥ 5
(measured to j = 20000 by the per-J verifier; dk ≤ j re-certified here to j = 120).
Then p_i − k_i ≥ 3 for **all** i. *Proof:* identical, with ε, K recomputed under dk(5+t) :=
5+t for t > 115: ε ≤ ε_table + 2^−115·(122/2) and K(s) = 3228 + Σ_{116≤t≤tmax(s)}(5+t):
the slab comparison holds for all s ≥ 682 (checked for every slab t < 2000, i.e.
s < 2^2000; beyond, the majorant B ≥ 16 + 5.25 s − (17/8)·(t_max+1)(t_max+10)/2 − …
is increasing in s and positive, since 18 − (17/8)·Σ(5+t)2^{−t−1} = 18 − 12.75 = 5.25 > 0
dominates the O(log² s) term). ∎

**Optimality.** Φ = 3 exactly at i = 0 (p, k) = (4, 1), so no larger constant holds;
C = 3 is the measured and proved optimum.

## 5. Verification log (all machine checks in agentA_proof.py / agentA_run.log)

- V0: run7.verify(j) OK for j = 1..120 (0.4 s); == task table for j ≤ 20; min dp = 2; dk ≤ j.
- V1: class arithmetic (spike ⟺ k ≡ 10 mod 16; j = 5+v2(3s+2); off-spike j by residue)
  brute-verified for k < 10^5; first-occurrence modular roots for t < 30.
- V2: d/g tables built and brute-verified; g ≥ d+1 off ρ = 10; B₀ = 16 via j-sequence
  1,4,2,1,3,2,1.
- V3: fire-level walk, 333167 fires to p < 1.1·10^6: Φ ≥ 3 everywhere, Φ_min = 3 at i = 0;
  30667 spike cycles, all m = 1, per-class (net, dp_total) match the class map;
  min net = 5, min dp_total = 21 (both J = 19, first at s = 27306).
- V4: 60575-fire agreement with the exact big-int walker (the formal map F), i ≤ 2·10^5.
- V5: cycle-level simulator to s = 10^7 blocks (k ≈ 1.6·10^8): B ≥ 3 + drop and V ≥ 3 at
  every cycle (worst V = 18 at the first spike; worst slack 15); Σ(dk+d) = 16s identity.
- V6/V6b: transducer mining s < 2^14 (exact class map); parity closure of the m = 1 regime.
- V7: counting bound constants; slab checks; AP-sum and on-trajectory soundness checks;
  thresholds s* = 682 (both scopes); S₁ = (2^116−2)/3; s₀ = 2863311530.
- Runtime 18 s, stdlib only, footprint < 1 MB.

## 6. Reproduction

```bash
cd work_r10 && python -B agentA_proof.py     # full check suite, ~18 s
```

## 7. Residual

None for the stated theorem. The only gap to a literally unconditional "all i" claim is
(H1) for j > 120 (dk(j) ≤ j, dp(j) ≥ 2) — a per-J table extension, mechanical via
agentB_run7 (0.4 s per 120 j's here; the recorded prior run reaches j = 20000/30000).
The structural content — minima only at spike exits, the amortized repair, and the
linear-vs-logarithmic margin — is proved, not measured.
