# R6: trying to prove Lemma E(v) for all v. Status: NOT CLOSED

Tags: [Class-A] proved for all parameters; [Class-B] finite exhaustive check; [Class-C] empirical/conjecture.
All statements refer to the top map T of work_r1/RULES.md §5 (accepted):
A even → (A+b+c+3, S); A odd → m=b+(A−3)/2, st=(c+(A+1)/2, S); while m odd ≥3: push (m+3)/2, m←(m−3)/2;
m=1 HALT; m even → (m+4, st). Halt ⇔ some step with A odd and x:=A+2b+3 a power of 2.

## 1. Approach (c): a 2-adic invariant on the halting quantity — refuted
Q: is there k with x ≢ 0 (mod 2^k) at every odd step? **No** [Class-B, `verify_r6.py`, n<3·10^5]:
for every k ≤ 8 the residue 0 mod 2^k is hit (residues hit: 2/4, 4/8, 8/16, 15/32, 27/64, 49/128, 93/256).
So no predicate of the form "x mod 2^k avoids 0" is invariant; any invariant P must couple the
2-adic valuation of x with its size (x = 2^k·q with q>1). A purely congruential P on (A,b) alone
cannot work.

## 2. Where the near-halts are [Class-B, n < 3·10^5]
Listing odd steps with x = 2^k·q, q odd ≤ 7, k ≥ 6: they occur only at n = 2^k − 2 with x = 3·2^k.
These are exactly the singleton steps L=(3n+3) (RULES §5 Corollary: A+3 ≡ 0 mod 3, never a power
of 2) [Class-A]. Off the singletons, every odd step has q ≥ 9 when k ≥ 6 [Class-B, n<3·10^5].
This is consistent with the R4 picture: the orbit is a sequence of excursions from singleton
(3·2^v − 3) at n = 2^v − 2 back to the next singleton at n = 2^{v+1} − 2.

## 3. Why (a) and (b) were not completed
(a) Uniform-in-v symbolic execution: R4/R5 showed the excursion E(v) has Θ(2^v) top steps, and its
internal structure is a nested cascade whose depth (p(s) in R5) grows with log v; a block-level
description therefore needs an unbounded number of phase types, unless the R5 recursion on s
(F(s) ⇒ F(s′), s′ ≪ s) is closed. That closure is exactly R5's residual (G1 margin bound, G2 end
phase with perturbed odd entry 2^r·H−1+K, G3 initial phase). No new idea for G2 was found here.
(b) A closed form of L_n in terms of the binary expansion of n+2 was not identified: the excursion
is not self-similar at the list level (lists inside E(v) are not translates/scalings of lists in E(v−1)
— checked informally, not formalized), so an induction on bits of n has no evident hypothesis.

## 4. What is proved / known (unchanged)
- [Class-A] RULES.md reduction; singleton steps never halt.
- R4 Theorem (unaudited, not re-checked here): no halt for n < 2^2001 − 2 (relies on E(v), v ≤ 2000).
- [Class-B] verify_r6.py: no halt for n < 3·10^5 directly; ΣL_n = 3n+3 checked each step.

## 5. Exact residual
Lemma E(v) for all v > 2000: starting from the singleton (3·2^v − 3) the top map reaches the
singleton (3·2^{v+1} − 3) with no odd step having x a power of 2. Equivalently (R5) F(s) for all
s > 1000 with margin bound G1 and end-phase lemma G2. This is a genuinely open statement as far as
this work goes: it is a Collatz-like claim (the halving chain m ← (m−3)/2 interacts with carries),
and no structural invariant was found; it is not a matter of missing computation.
