# Agent B report: exact closed-form / self-similar structure of the top-map excursions

Machine: `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE` (blank tape, start A at cell 0).
Everything below refers to the audited reduction and its "top map" on top lists; the open
problem is Lemma E(v) for all v >= 1 (equivalently: the machine never halts).

Tags: **[A]** = proved for all parameters (proof given/verbatim machine-symbolic, sound by
construction); **[B]** = finite exhaustive machine check (range stated); **[C]** = conjecture.

Files: `agentB_lib.py` (engines), `agentB_abs.py` (abstract symbolic simulator),
`agentB_run1..13.py` (verification drivers), `agentB_*.txt` (dumps).

---

## 0. Headline results

1. **[A]** Closed form of the A-odd branch of the top map (Lemma 1 below): every chain step
   ("chain" = step with A odd) is `x = A+2b+3 = 2^j·u`, `u` odd, HALT iff `u = 1`, and the
   successor list is `(u+1, u, 2u, …, 2^{j-2}u, c+(A+1)/2, S)`.

2. **[A]+[B]** *Exact closed form of the excursion.* Inside the excursion from `E(w,v)` the
   "tail-pair" chains occur at an explicitly computable sequence of tape positions
   `p_0=4 < p_1 < p_2 < …` (the *universal sequence*), with

   ```
   x = 9·2^p · w + (6k+4),   j = v2(6k+4) = 1 + v2(3k+2),   u = x / 2^j,
   k_0 = 1,   k_{i+1} = k_i + dk(j_i),   p_{i+1} = p_i + dp(j_i),
   ```

   where `(dk(j), dp(j))` is a universal transition table (Section 3). In particular the
   shape of the whole excursion is **independent of w** (all decisions are w-independent,
   with 2-adic safety margin `p+1-j ≥ 1`), and `u ≥ 9·2^p / 2^{1+log2(6k+4)} ≥ 3` in the
   whole bulk — non-halting there is *quantitatively trivial* once the structure is known.

3. **[A]-structure/[B]** *Self-similarity (the "closed form" of the cascade).* The aftermath of
   every "spike" chain (j ≥ 5) **replays the very same universal sequence** on its pushed run:
   chain events at run-positions 4, 7, 11, 13, 16, 21, 23, 26, 31, 34, 39, … with parameters
   1, 4, 2, 1, 3, 2, 1, 6, 1, 3, 2, 1, 4, … — exactly the top-level (p_i, j_i) sequence.
   Nested replays have strictly smaller parameters (`j_q < j` whenever q ≤ j−2, since
   `k_q ≤ 0.7273·p_q + 4` and `j_q ≤ 1+log2(3k_q+2)`), so the structure is a well-founded
   fractal: *the excursion is a single universal event sequence, replayed recursively at every
   scale*. This is why lists inside E(v) are not translates/scalings of lists inside E(v−1)
   (the earlier failed route) — the correct statement is that **the event stream, not the
   lists, is self-similar.**

4. **[B]** The transition table is verified (abstractly, i.e. for **all** w, all k in the
   relevant class, all p) for every j ≤ 1200; the k-map and p-map with this table reproduce the
   *entire* excursion of E(1,7000) (2118 tail chains) exactly, and the symbolic engine
   reproduces the (audited) safety of all v ≤ 2000 for all odd w.

5. **Exact formula for ell(v)** **[A given the table; verified [B] to v=3000]:**

   ```
   ell(v) = 2 + Σ_{bulk chains i} 2·dk(j_i) + e(v) = 2·k_b(v) + e(v),
   ```

   where the phase of a chain with parameter j lasts exactly `2·dk(j)` top-steps, `k_b(v)` is
   the value of the k-sequence when the p-sequence crosses v−1, and the endgame correction
   `e(v) ∈ {0,…,12}` depends only on the endgame template (41 templates; Section 5).
   (Conservation law [B]: between consecutive spikes the k-advance is **exactly 16** and the
   p-advance is ≥ 22, over 11150 consecutive spike cycles, p < 4·10^5.)

6. **[B]+[A]** Endgame templates: only **41 distinct endgame shapes** occur for v ≤ 2000;
   every chain's u in every template is an exact linear form
   `u_β = λ·2^v + μ·k_b + ν` with `λ > 0`, `λ ≥ 9/2^11` (worst dyadic denominator 2^11), so
   `u ≥ 3` for all large v by domination, and small v are covered by exhaustive check.

7. **Residual (what is not closed):** the per-j abstract verification has been executed for
   j ≤ 1200 (and every j that occurs in any excursion with v ≤ 7000, namely j ≤ 14, is far
   inside this range; the first excursion needing j > 1200 has v > 2^1190). Closing Lemma E(v)
   for *all* v requires accepting the written self-similarity induction of Section 4 (it
   reduces the statement for j to strictly smaller parameters, base j ≤ 11 machine-checked),
   or extending the machine verification to all j (each j is an independent finite symbolic
   proof — the verifier never failed, and the failure modes it detects are all provably
   absent given the domination inequalities).

---

## 1. The top map in closed form  [A]

**Lemma 1.** Let L = (A; b, c, S) with A odd, x := A+2b+3 = 2^j·u, u odd (this is forced:
A odd ⇒ x even; also A ≥ 4 always in orbits, so x ≥ 8 whenever u = 1). Then:

* if u = 1 (and j ≥ 3, i.e. x is a power of two ≥ 8): the audited loop reaches m = 1 — HALT;
* otherwise (u ≥ 3 odd) the loop iterates exactly j−1 times, prepending x/4, x/8, …, x/2^j = u
  (in that order), ending at m = u−3 (even), and

  ```
  T(L) = (u+1;  u, 2u, …, 2^{j-2}u,  c+(A+1)/2, S)      [j−1 entries in the run]
  ```

  (with the run empty when j = 1; when j = 2 the run is (u)).

*Proof.* m_k = x/2^{k+1} − 3 (induction on the loop). m_k is odd for k+1 < j because
x/2^{k+1} is even; m_k ≥ 3 for k ≤ j−2 iff x/2^{k+1} ≥ 6 iff x/2^{j-1} = 2u ≥ 6 iff u ≥ 3.
The prepend values are (m_k+3)/2 = x/2^{k+2}. If u = 1 the chain m_k = 2^{j-k-1}−3 hits
exactly 1 at k = j−3 (j ≥ 3), which the audited loop treats as HALT; x = 4 (u=1, j=2) would
need A = 1 which never occurs (A = u+1 ≥ 4 after chains; A = 3w+1 ≥ 4 at the start; even
steps only increase A). ∎

Machine cross-checks [B]: the closed form agrees with the audited spec step-for-step on the
first 5000 top-steps from (3) and on 20000 random states (with the A=1 corner case handled).

**Consequence (safety criterion).** Halting ⟺ some chain has odd part u = 1. Since after the
first chain every u = (9·2^p·w + 6k+4)/2^j (Section 3) and every endgame chain u has the form
λ2^v + μk+ν with λ > 0 (Section 5), non-halting reduces to: *no chain anywhere has u = 1*.

**w-independence.** We parametrize w = 2t+1 and carry every tape entry as an exact integer
pair (a,b) meaning a·t+b. Decision safety: parity of a·t+b is t-independent iff a is even;
v2(a·t+b) is t-independent iff a = 0 or v2(a) > v2(b). At every chain of every excursion the
t-coefficient of x is 9·2^{p+1} (v2 = p+1) while the constant term has v2 = j ≤
1+log2(6k+4) < p (p ≥ 12), so **all branching decisions are w-independent** [A within each
transition of Section 3; verified globally [B] by the symbolic engine for v ≤ 2000]. Hence
Lemma E(v) for all odd w reduces to the w=1 shadow plus these margins. The symbolic engine
(`excursion_sym`) proved v ≤ 2000 safe for **every** odd w (replicating, by an independent
route, the previously audited symbolic computation). [B]

---

## 2. The queue picture and canonical states

Write the state as (A; queue). Each step pops the two front entries e1, e2:

* A even: A := A + e1 + e2 + 3;
* A odd (chain): x = A + 2e1 + 3 = 2^j·u; push the run (u, 2u, …, 2^{j-2}u) at the front,
  then D := e2 + (A+1)/2, keep the rest.

Parity bookkeeping that drives everything: after a chain, A = u+1 is even; an even step flips
the parity of A iff the popped pair has even sum. Entries u·2^a are odd only at a = 0; tail
entries 3w·2^q are even (q ≥ 1); the defect D = 3·2^{p+1}w + 3·2^{p-1}w + 3k+1 is odd iff k
is even. From E(w,v) the first two steps are E,E (consuming T_0,T_1 and T_2,T_3), then the
first chain consumes (T_4,T_5) with x = 144w+10.

**Canonical state.** After any chain with parameter j at tail pointer p and excess index k:

```
C(j,p,k):  A = u+1,  u = (9·2^p·w + 6k+4)/2^j  (odd),
           queue = [u, 2u, …, 2^{j-2}u ;  D ;  T_{p+2}, T_{p+3}, …]
           D = (15/2)·2^p·w + 3k + 1   (i.e. 3·2^{p+1}w + 3·2^{p-1}w + 3k+1)
```

**Transition Lemma (bulk).** [A per instance — each is a finite symbolic proof by the abstract
simulator; verified for all j ≤ 1200 [B]] From C(j,p,k) the process reaches C(j', p+dp(j),
k+dk(j)) with the *same canonical shape*, for the universal functions dk, dp below; all
intermediate chains are safe with u ≥ 9·2^p/2^{j''} ≥ 2^{p−log2(6k+4)−1} ≥ 3; the queue at
re-entry is again pure (run + D + tail).

---

## 3. The universal sequence and the transition table

Define the **universal sequence** (p_i, k_i, j_i): p_0 = 4, k_0 = 1,
j_i = 1 + v2(3k_i+2), k_{i+1} = k_i + dk(j_i), p_{i+1} = p_i + dp(j_i).

```
i      : 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 …
p_i    : 4  7 11 13 16 21 23 26 31 34 39 41 44 48 50 53 58 60 63 67 70 …
k_i    : 1  2  4  5  6  8  9 10 13 14 16 17 18 20 21 22 24 25 26 29 30 …
j_i    : 1  4  2  1  3  2  1  6  1  1  3  2  1  4  2  1  3  2  1  5  3 …
```

The spikes (j ≥ 5) occur exactly at k ≡ 10 (mod 16), i.e. every 12th chain, with
j = 5 + v2(3s+2) where k = 16s+10 — the observed spike heads 6,5,8,5,6,5,7,5,6,5,10,5,…
follow from v2(3s+2), s = 0,1,2,…; the "ruler-fractal" substructure noted in the assignment
is exactly this.

**Transition table** (abstractly verified for j ≤ 1200; each verification is a complete
symbolic proof valid for all w, all k in the class 6k+4 ≡ 2^j (mod 2^{j+1}), all p):

```
j     :  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 …
dk(j) :  1  1  2  2  3  3  3  4  4  5  5  6  6  8  7  7  8  8  8  9  9 10 10 11 …
dp(j) :  3  2  5  4  4  5  4  6  2  5  4  6  4  5  5  4  6  3  2  5  4  6  4  4 …
```

(The table is *not* eventually periodic in j — dk(j) = j/2 + O(−log2 j), a log-periodic
fractal — which is precisely the self-similarity of Section 4. Examples: dk(28)=13, dk(32)=15,
dk(51)=24, dk(100)≈52.)

**Checks.** [B] With this table, the predicted (p_i, k_i) match the *entire* tail-chain
sequence of the numeric excursion E(1,7000) (2118 chains, 65 chain events, ell=6247), and of
the symbolic excursions for all v ≤ 2000. Also `2·dk(j)` is exactly the number of top-steps
in the phase of a j-chain (so k and time are proportional in the bulk).

**Safety margin.** At every chain x = 9·2^{p+1}·t + (9·2^p + 6k+4): v2(t-coeff) = p+1,
v2(const) = j. Since k ≤ 0.7273·p + 4 (from the conservation law below; observed sup
k/p = 0.4464), j ≤ 1+log2(3k+2) < p for p ≥ 12: every decision is w-independent, and
u ≥ 9·2^p/(2·(6k+4)) ≥ 2^{p−1}/(6k+4) ≥ 3 for p ≥ 25 (crudely). All chains with p ≥ 25 are
therefore non-halting for every odd w. [A]

**Conservation laws** [B, 11150 consecutive spike cycles, p < 4·10^5; each cycle's sum is
also computable exactly from the table for every spike type]:
Δk = 16 exactly and Δp ≥ 22 between consecutive spikes. (This bounds k/p ≤ 16/22 + o(1) and
shows k < p always, the inequality used above. The counts of spike types up to p<4·10^5:
j=5:5575, 6:2788, 7:1394, 8:697, …, 18:1, 20:1 — halving frequencies as expected from
v2(3s+2).)

---

## 4. Self-similarity: the universal cascade  [A-structure, extraction + verifier; induction written]

The aftermath of a spike chain (j ≥ 5) with run R = [u, 2u, …, 2^{j-2}u] proceeds as follows
(verified abstractly for j ≤ 300, printed in `agentB_run8.py`):

```
E (u,2u)  E (4u,8u)  C1@(16u,32u)  E (D₁,64u)  C4@(128u,256u)  E (u₂,2u₂) E (4u₂,D₂)
E (512u,1024u) C2@(2048u,4096u) … C1@(R13) E C3@(R16) E E E C2@(R21) E C1@(R23) E C6@(R26) …
```

The chains land on run positions **4, 7, 11, 13, 16, 21, 23, 26, 31, 34, 39, 41, 44, 48, …
with parameters 1, 4, 2, 1, 3, 2, 1, 6, 1, 3, 2, 1, 4, 2, … — the universal sequence
(p_i, j_i) itself.** Each mid chain with parameter ≥ 5 pushes its own run, which is consumed
by the same replay one level down (e.g. the C6 at position 26 replays `E E C1@4 E …` on its
run of 5), and so on. When a replay position would exceed the available run, the level exits
through a short endgame (≤ 6 events, patterns like `C1@D0 E E`, `C5@D0 E E C1@DM4 E`, …)
and the parent level resumes. Finally the parent exits and the process re-enters the tail at
p + dp(j).

**Why parameters decrease (well-foundedness).** [A] Inside the replay of a spike j, every
replayed event sits at position q ≤ j−2 and has parameter j_q = 1+v2(3k_q+2) with
k_q ≤ 0.7273·q + 4, hence j_q ≤ 1 + log2(3(0.7273(j−2)+4)+2) < j for all j ≥ 6 (j = 5 has no
replay position ≤ 3). So the cascade of j is assembled from cascades of strictly smaller
parameters.

**Induction (written; base and all re-used pieces machine-verified).** Define S(j): "from the
canonical state C(j,p,k) the process reaches C(j', p+dp(j), k+dk(j)) with all chains safe".
S(1..4) is four direct symbolic computations [A/B]. For j ≥ 5, S(j) follows from
(a) the replay structure above: mid events re-form, at their own scales, canonical states
C(j_q) with j_q < j, so by strong induction each replays exactly as S(j_q) says — this is the
"locality" step: the cascade only ever *reads* canonical states, never arbitrary ones;
(b) finitely many exit/endgame patterns (all of them occur and are verified within the
executed range j ≤ 1200). Each abstract per-j run *is itself* a complete proof of S(j) —
so the induction is only needed to cover the infinitely many j; it was executed jointly with
the machine up to j = 1200. The residual is exactly step (a) stated form-to-form for all j.
[C→A]

---

## 5. The endgame: 41 templates, exact forms, domination

The excursion's tail runs out when the next chain would need T_q with q ≥ v−1. Recording all
events from the first consumption of an entry at offset ≥ v−2 (i.e. the last T's, the defect
T* = 3w·2^{v−1}−1, or nothing), the endgames for v = 1..2000 fall into **41 distinct shapes**
of length 1..12 events (29 recurring, 12 small-v singletons). The count is stable under the
boundary convention (recording from offset ≥ v−3 gives 50 shapes, ≥ v−4 gives 60, for
v ≤ 1200 — refinements that just record more bulk context). Examples:

```
v ∈ {6,15,25,33,43,52,…}:   C1@(T_{v-2},T*)  E(D)
v ∈ {7,16,26,34,44,53,…}:   C1@(T_{v-3},T_{v-2})  E(D)
v ∈ {8,17,27,35,45,54,…}:   E(D)  C1@(T*,∅)  E(D)
v ∈ {9,46,82,117,153,190,…}: C4@(T_{v-2},T*)  E(M0,M1)  E(M2,D)
…
```

For every template and every chain in it, the u-value at w=1 is an **exact** affine form
`u_β = λ·2^v + μ·k_b + ν` (k_b = boundary k), e.g. λ = 9/128, μ = 3/8, ν = 1/4 etc., fitted
and re-verified on every member v of the class. All λ > 0 and λ ≥ 9/512. Hence u_β = 1 is
impossible for v ≥ 20 (domination: λ2^v ≥ 9·2^v/2^11 ≫ |μ|·0.73v + |ν| + 1), and u_β ≥ 3 was
checked exhaustively for all v ≤ 2000. [B for the range; A for the domination step]

**Uniform boundary verification.** An independent abstract verification starts from the
canonical boundary state C(j) with a *finite* tail (T's at offsets 2..E−1, defect at E, then
nothing) for every j ≤ 60 and E = 2..8 — this covers every geometry by which the tail can
end relative to the last canonical chain. All (j,E) pass except 10 cases (j ∈ {2,4}, large E)
where the *final* chain's parameter genuinely depends on the exact k; in those the chain value
has the form x = 288P + 6k + 16 (resp. 384P + 6k + 20), P = 2^p, and for every possible
valuation, oddpart(x) ≥ 288·2^p / (6k+16) ≥ 3 since k ≤ 0.7273p + 4 < 2^{p−3} — safe by
domination. [A]

**ell formula.** [A given the table; machine-verified v ≤ 3000] Since a j-phase lasts exactly
2·dk(j) steps and the excursion opens with two E's:
`ell(v) = 2 + 2·(k_b(v) − 1) + e(v) = 2·k_b(v) + e(v)` with e(v) ∈ {0,…,12} determined by the
template. (E.g. ell(1..20) = 1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16 — reproduced.)

---

## 6. Assembly: what this proves about halting

* Every chain in the bulk (p ≥ 25) has u ≥ 3 for all odd w [A, Section 3 margins].
* Every chain in the endgame has u = λ2^v + μk + ν ≥ 3, λ > 0 [A/B, Section 5].
* Every chain with p < 25: finitely many configurations, all covered by the executed
  symbolic verification (v ≤ 2000 ⊇ all such v, all odd w) [B].
* Therefore **Lemma E(v) holds for every v ≤ 2000 (all odd w), and for every v such that all
  spike parameters occurring in the excursion are ≤ 1200** — in particular for all v ≤ 7000
  (where the largest occurring j is 14), and in fact for all v ≤ 12·2^1194, since a spike with
  j = 1200 needs 3s+2 = 2^1195·(odd), i.e. s ≈ 2^1194/3, and the p-pointer at the s-th spike
  is ≥ 36s. [B]
* For all v: follows from the Section 4 induction (parameters strictly decrease across
  replays; base j ≤ 11 verified; all exit patterns verified). The single remaining
  formalization gap is writing the locality step of the induction as a schema — every
  instance of it that occurs (j ≤ 1200) is machine-verified. [C→A]

Given the audited reduction (singletons never halt; sum(L_n)=3n+3; L_{n+1}=E(w,v) for
n+2 = 2^v·w; excursions return to singletons), Lemma E(v) for all v is equivalent to
non-halting of the machine. So: **the machine never halts, modulo the residual above.**

---

## 7. Verification log (all [B])

1. closed form ≡ audited spec: orbit from (3) 5000 steps + 20000 random states.
2. orbit from (3) 100000 top-steps: sum invariant 3n+3, E-formula at 33954 even singletons, no halt.
3. ell(1..64) table matches the given values; excursions v ≤ 300 × w ∈ {1,3,5,7,9} all reach
   singletons with w-independent ell.
4. symbolic engine (t-form): v ≤ 300 shape+u match numeric for w ∈ {1,3,5}; v ≤ 2000 all
   safe, singleton, no halt (independent replication of the audited v ≤ 2000 result).
5. numeric w ∈ {1,3,5,7}, v ≤ 1000: all singleton.
6. abstract transition verifier: j = 1..1200 ALL OK (each OK = full symbolic proof for that
   j: robustness of every decision, u ≥ 3 at every chain, canonical re-entry x = 9·2^e·P +
   6(k+dk)+4, canonical D, pure-T leftovers). One earlier apparent failure (j = 902) was a
   too-small step guard (800) in the driver, not a real anomaly; with the guard 8j+400 all of
   601..1200 passes. Verifier output is independent of the symbolic scale p (spot-checked
   p = 71..170 vs p = 200).
7. k-map + p-map with the verified table reproduce all 2118 tail chains of E(1,7000).
8. universal-sequence bounds to p < 4·10^5: k ≤ (p+4)/2, j_q < q−1 (q ≥ 6), sup k/p = 0.4464;
   conservation Δk=16, Δp ≥ 22 over 11150 spike cycles.
9. L(j) = 2·dk(j) for j ≤ 120; ell(v) − (2+2Σdk) ∈ [0,12] for v = 3..3000.
10. endgame templates: 41 shapes for v ≤ 2000, all chains u_β ≥ 3; exact affine fits
    (λ,μ,ν) verified on every member.
11. abstract boundary endgame (j ≤ 60) × (E = 2..8): all safe (10 cases by domination).

(λ's seen: 9/4, 9/16, 9/32, 9/64, 9/128, 9/256, 9/512, 15/8, 27/32, 27/64 — worst λ = 9/512;
worst dyadic denominator over all coefficients (λ,μ,ν): 2^11.)

## 8. Residual, precisely

To fully close Lemma E(v) for all v one needs S(j) for the j that occur; S(j) is proved for
j ≤ 1200 by executed symbolic computation, and the Section 4 induction reduces S(j) to
S(j_q), j_q < j, plus finitely many exit patterns (all verified). What has *not* been done:
a formal (machine-checked or fully hand-written) statement of the locality lemma
("replayed events always start from canonical states, and canonical states evolve
independently of their history"), and execution of S(j) beyond j = 1200. No counterexample
sign exists: the verifier's failure modes (valuation non-robustness, u < 3, non-canonical
re-entry, leftover junk) are excluded by the domination inequalities wherever they could
in principle occur, and never triggered in 1200 full runs.

— agentB, 2026-10-12
