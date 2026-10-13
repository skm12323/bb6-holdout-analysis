# agentB2: the EXIT CLASS LEMMA — j_D <= J-2 at every spike exit

**Status: PROVED** ([Class-A] per shape, given one size input on the universal k-sequence
for the single tie shape; [Class-B] exhaustive agreement on every probe). No failing case.

Artifacts (this directory): `agentB2_lib.py` (traced Phi_m + shape extraction),
`agentB2_symbolic.py` (per-shape symbolic derivation with the class-pinning calculus),
`agentB2_verify.py` (V-A..V-D). Read-only inputs: `work_g6/PROOF_G6.md`, `work_g6/verify_g6.py`
(phi, kappa), `work_r10/PROOF.md`, `work_r10/fast_walker.py` (cross-check).

## 0. Statement

For every spike — a chain with parameter J >= 5 of class 6k_h+4 = 2^J·odd, with pushed run
(u, 2u, ..., 2^{J-2}u), seam D_h and tail T_e = 3·2^e·P behind it (the object Phi_J of
work_g6 §0; in the real walk P = 2^{rho-1}·U with rho the spike's universal position) —
**every exit fire reading the seam satisfies j <= J-2**: the D-fire (b = D_h) has
j_D <= J-2, and the possible second fire on the seam pushed by the D-fire has j_seam <= J-2.
(The exits where D_h is read as c by a chain, or swallowed by an even step, have no D-fire;
their j is also checked <= J-2 in V-A/V-C.)

## 1. Notation and the three Class-A lemmas

Write u = (9P+6k_h+4)/2^J = 9P/2^J + w with **w = (6k_h+4)/2^J odd and free** (k_h ranges
over the class), D_h = (15/2)P + 3k_h + 1 = (15/2)P + 2^{J-1}w − 1, T_e = 3·2^e P. By
Prop 2 (work_g6) the sub-cascade before queue index J−1 is the universal level process at
base u; its fires sit at universal sub-positions with universal k's. Let **rho*** = the last
pure sub-fire position (b = E_{rho*}, c = E_{rho*+1}, both run entries), **K** = its
universal k, **j_last** = 1+v2(3K+2) its class, **g** = J−2−rho* the gap
(work_g6's convention; the task's rho* = J−1−g), **K_exit** = s/2 where s = the number of
Phi_J-steps before the crossing at index J−1 (the first read of D_h).

**Lemma 1 (clean-crossing identity, script-free).** *If the first read of D_h is as b by a
chain (the D-fire), then x_D = (39/2)P + 9k_h + 6·K_exit + 8, with s = 2·K_exit even.*
Proof. Pushed entries enter the queue only at the front, so "D_h at the front" means
everything earlier (originals E_0..E_{J-2} and all pushes) is consumed. The sum lemma over
the state gives A + sum(live queue) = 2^{J-1}u + 1 + D_h + sum(T_e) + 3s; at the crossing
the live queue is exactly D_h + sum(T_e). Hence A = 2^{J-1}u + 3s+1, and
x_D = A + 2D_h + 3 = (9P+6k_h+4)/2 + 6K_exit + 4 + 15P + 6k_h + 2 + 3+... = (39/2)P + 9k_h
+ 6K_exit + 8. A is odd (chain), 2^{J-1}u even, so s is even. ∎
(This reproves and generalizes Prop 3's computation: no script details enter.)

**Lemma 2 (class reduction).** *9k_h = (3/2)(6k_h) = 3·2^{J-1}w − 6, so*
x_D = (39/2)P + 3·2^{J-1}w + 2·(3K_exit+1), *and, the P-part having valuation p−1 >> J:*
j_D = 1 + v2(3·K_exit + 1) *whenever v2(3K_exit+1) < J−1; if v2(3K_exit+1) >= J−1 then*
j_D >= J−1. *So the lemma is exactly the statement v2(3K_exit+1) <= J−3.*

**Lemma 3 (K_exit = K + delta).** *K_exit = K + delta with delta >= 1 an integer per
script: s = (steps before the fire at rho*) + 1 + (steps from that fire to the crossing) =
2K + 1 + e_cross by the same crossing identity at rho* (clean by rho*+1 <= J−2), and
e_cross = 2·delta − 1 is odd (s even).* For J = 5 there is no sub-fire (rho* would be < 4,
below the first universal position): K_exit = 1 directly.

## 2. The exit shapes [Class-B census, m = 5..3000; scripts are universal]

Every m = 5..3000 whose exit contains a D-fire (906 of them; the others read D_h as c
(954) or in an even step (1136)) falls into exactly one of 12 shapes (gap, j_last, delta).
**j_D = 1 + v2(3K + 3·delta + 1) with 3K+3·delta+1 = (3K+2) + (3·delta−1)**; the class of K
(v = j_last−1, m3 = (3K+2)/2^v odd) versus h = v2(3·delta−1), c' = (3·delta−1)/2^h:

- h < v: 3K+3d+1 = 2^h(c' + 2^{v-h}m3), bracket odd ⟹ **j_D = 1+h, CONSTANT**;
- h > v: 3K+3d+1 = 2^v(m3 + 2^{h-v}c'), bracket odd ⟹ **j_D = j_last, CONSTANT**;
- h = v: 3K+3d+1 = 2^v(m3+c'), odd+odd ⟹ j_D = j_last + v2(m3+c') — the only
  orbit-dependent case (a "tie" shape).

| shape (g, j_last, δ) | first m | count ≤3000 | j_D | min margin J−j_D | case |
|---|---|---|---|---|---|
| (no sub-fire, J=5) | 5 | 1 | **3 = J−2** | 2 | K_exit=1: j_D = 1+v2(4) |
| (2, 1, 1) | 8 | 325 | **1** | 7 | h=1>v=0: j_D = j_last |
| (3, 4, 2) | 12 | 84 | **1** | 11 | h=0<v=3: j_D = 1+h |
| (1, 2, 1) | 14 | 250 | 1+v2(3K+4) | 9 | **TIE h=v=1** (Prop 3) |
| (4, 3, 2) | 22 | 163 | **1** | 21 | h=0<v=2 |
| (4, 6, 3) | 32 | 21 | **4** | 28 | h=3<v=5 |
| (3, 5, 3) | 68 | 41 | **4** | 64 | h=3<v=4 |
| (5, 8, 4) | 106 | 6 | **1** | 105 | h=0<v=7 |
| (3, 7, 3) | 248 | 10 | **4** | 244 | h=3<v=6 |
| (4, 10, 5) | 394 | 2 | **2** | 392 | h=1<v=9 |
| (1, 9, 4) | 966 | 2 | **1** | 965 | h=0<v=8 |
| (5, 12, 6) | 1544 | 1 | **1** | 1543 | h=0<v=11 |

**11 of 12 shapes are closed by pure class arithmetic**: j_D in {1, 2, 4} (or 3 at J=5),
constant over the whole class, and <= 4 <= J−2 because any sub-fire shape needs
rho* = J−2−g >= 4, i.e. J >= 7 (J=5 handled separately; measured first occurrences are
J = 8, 12, 14, 22, ...). The constants were verified symbolically
(`agentB2_symbolic.py`): every decision of each script — parities and the j of every
intervening fire, including the nested sub-spike pushes (j_last in {5,...,12}) — is FORCED
for all P with v2(P) >= 2J+64, all odd w (all k_h in the class), all K with
3K+2 = 2^{j_last−1}·odd, by the pinning calculus (w = 1+2W', K = kap+2^{j_last}t:
parity always pinned; v2 pinned below digit v2(c_w)+1 and v2(c_K)+j_last). The replay
independently reconstructs x_D = (39/2)P + 3·2^{J-1}w + 6K + (6δ+2) in every shape.

**The single tie shape (1,2,1)** is exactly work_g6 Prop 3's case: j_D = 1+v2(3K+4) with
K ≡ 0 (mod 4) at rho* = J−3. Write K = 4n: j_D = 3 + v2(3n+1).

*Size closure of the tie case.* v2(3K+3δ+1) <= log2(3k(rho*)+3δ+1) with rho* <= J−3:
- with the conservation input k_p <= 0.4465·p (work_r10 [Class-B] to p = 4·10^5) and
  delta <= 2J: j_D <= 1 + log2(1.34(J−3)+6J+1) <= J−2 for **J >= 9**;
- with k_p <= p^2 (work_g6 Prop 4, conditional): j_D <= 1 + log2(3(J−3)^2+6J+1) <= J−2
  for **J >= 12**;
- J < 12: no tie shape exists — exhaustively, the D-fire m's with m <= 11 are {5, 8}
  (shapes (J=5) and (2,1,1)) — and structurally, rho* = J−3 <= 7 has universal
  k in {1, 2} (classes j = 1, 4; the first two fires 48U+10, 384U+16 of any level process),
  excluding j_last = 2. ∎

So: **EXIT CLASS LEMMA. j_D <= J−2 for every spike exit D-fire** — [Class-A] for the 11
constant shapes unconditionally; [Class-A given either k-growth input] for the tie shape
(1,2,1), with the finite residual J < 9/12 closed exhaustively. Note the constants make
the bound hugely slack in 11/12 of the cases (margins J−j_D = J−1, J−3 or J−4).

## 3. The second exit fire (the D-fire's own seam) [Class-A + Class-B]

When j_D >= 5 the D-fire pushes its own run and seam d = T_2 + (A_D+1)/2; the next fire on
d is the exit of the *sub-sub-cascade* at base u_D (the same lemma one level down; its
sub-positions are again universal). The clean-crossing identity at that level gives
(symbolically verified, both script variants):

  x_seam = (153/4)P + (15/2)k_h + 9·K_exit + 6·K' + 12,  j_seam = v2(9K_exit + 6K' + 7)
  (when < J−2),  K' in {1, 2} literal (no sub-sub fire, or the sub-sub fire at 4 with k=1).

For the only shape with seam fires, (1,2,1) (K_exit ≡ 1 mod 4): K'=1 gives
9K_exit+13 ≡ 2 (mod 4), so **j_seam = 1 constant** (44/47 cases); K'=2 (the j_D = 8
variant, first at m = 481) gives j_seam = 2 + v2(9K/4+7), size-bounded exactly as in §2
(j_seam <= J−2; needs j_D = 8, hence K ≡ 212 mod 256, hence J >= 478 under conservation).
Measured: 47 seam fires, all j_seam in {1, 4}, min margin J−j_seam = 13.

## 4. Verification [Class-B]

`python -B agentB2_symbolic.py` (per-shape table), `python -B agentB2_verify.py [N=3000]`
(42–64 s total; -B keeps work_g6 pristine — the library imports work_g6/verify_g6.py
read-only):
- **V-A** all m = 5..3000 (superset of the task's J = 5..300; 89 D-fires with m <= 300):
  for each of the 906 D-fires, x_D = (39/2)P + 9k_h + 6K_exit + 8 **exactly** (integer
  check against the traced value), j_D = 1+v2(3K_exit+1), j_D equals the shape constant
  (or Prop 3's formula), and **j_D <= m−2**; 47 seam fires with the x_seam form and
  j_seam <= m−2; 954 mixed fires (c = D_h): j <= m−2 (min margin 5), and for b = E_{J−2}
  the analogous identity x_mix = (27/4)P + (9/2)k_h + 6K_mix + 7 at the clean crossing
  at J−2 (j_mix = v2(6K_mix+4) when < J−2); 1136 exits swallow D_h in even steps.
- **V-B** 275 class-generic re-instantiations of the scripts (random k_h in the class
  mod 2^J, random K in the class, random p): every decision follows the script and j_D is
  the shape constant (Prop 3's formula for (1,2,1), truncated at the D-fire) — the
  constants are class-wide, not per-orbit.
- **V-C** the real walk (formal map F, exact big-int, level stream identical to
  `fast_walker.exact_walker` on all 60575 level fires to i = 2·10^5): 5582 spikes
  (chains j >= 5 at any nesting); **3171 exit D-fires, ALL with j <= J−2** (min margin 2
  at (J, j) = (5, 3); exit J-values seen: {5, 8, 12, 14} — the R10 J=17 event lies beyond
  2·10^5, and Phi_17's shape (2,1,1) gives j_D = 1, margin 16, matching R10's list);
  1582 seam-as-c reads (all j <= J−2); 829 seams swallowed by even steps. Accounting
  3171+1582+829 = 5582 is complete.
- **V-D** the tie thresholds of §2 (J >= 9 / J >= 12, monotone decreasing beyond).

## 5. Notes for the coordinator

- The task's proposed relation "K = k_h − dk(j_last)·(number of fires since)" does not
  hold as such: K is the universal k at the sub-position rho* of the sub-cascade and is
  **independent of k_h** (the sub-cascade replays the universal process at base u for
  every host in the class — work_g6 Prop 2). The correct relation is K_exit = K + delta
  with delta a per-script constant (Lemma 3); the class reduction that replaces it is
  9k_h = 3·2^{J-1}w − 6 (equivalently, with k_h = 16s+10 and 3s+2 = 2^{J-5}·odd,
  48s ≡ −32 mod 2^{J-2}, as the task suggests), which removes the k_h-dependence from
  x_D below level J−1.
- What remains orbit-dependent (both verified to the stated ranges): (i) the map
  J -> shape (which of the 12 scripts occurs), (ii) v2(3K+4) in the tie shape, (iii) the
  k-growth inputs. Everything else in "j_D <= J−2" is pure class arithmetic.
- The mixed exits (c = D_h) and even-step swallows never produce a D-fire; their j is
  covered by the same identity one position earlier and satisfies j <= J−2 with min
  margin 5 in all 954 cases (b = E_{J−2}: j_mix = v2(6K_mix+4), the same h-vs-v analysis).
- On-sequence spike levels {5,...,16, 18} to 2·10^5: the levels {6,7,9,10,11,13,15,16,18}
  have mixed/even exits (no D-fire) — the R10 statement "exit D-fires at every spike"
  refers to the spike events whose seam is read as b (all of which satisfy j_D <= J−2).
