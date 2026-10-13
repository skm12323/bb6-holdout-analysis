# NT: the θ-window of the exit automaton — sharp tie law, failure of window closure, exact residual

Machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Base (audited, black boxes): work_el/PROOF_EL.md
(Theorem A automaton, (A3) θ̃-rules, Remark S, Lemma C, Theorems B/D, §6 adversarial paths), work_m/PROOF_M.md
((C1) τ(n) ≤ n² inside Theorem M's induction). Checks: `verify_nt.py` (N1–N5, log `run_main.txt`), which imports
`work_el/verify_el.py` read-only. Tags: **[A]** proved for all parameters; **[B]** finite computation, range stated;
**[C]** data/heuristic.

**Verdict.** No θ-window closes under the automaton. NT is **not** closed for all J. The obstruction is real
inside the automaton: any window closed under the θ̃-rules must contain the drift θ̃ ↦ θ̃−1 of nested fire copies.
But the largest tie-free window is [−1,4] (N2), and −2 already ties. What this file proves: (i) a sharp one-step
tie law (Lemma C′), which replaces the window [−10,4] by two residue classes plus a size bound of 1012; (ii) the
exact drift bookkeeping (Prop. D); (iii) the reduction of NT to a residual (R) that concerns only chains with
j ∈ {5,8}, plus a size condition.

## 0. Results

| # | statement | tag |
|---|---|---|
| C′ | A tie at an a-step from chain t (n = j_t−1) occurs **iff** θ̃_t ≡ c_n (mod 2^n), where c_n := 2^{n−1}−3k_n is centred. Here c_4 = 5, c_7 = 58, and \|c_n\| ≥ 1012 for every other odd type-a n. | A (n ≥ 10^6) + B (n < 10^6) |
| W | Over all 1 ≤ j < 2·10^5 and \|θ̃\| ≤ 40, the largest tie-free window containing 1 for complete runs from (j,θ̃) is **[−1,4]**. θ̃ = −2 ties for 2788 values of j, and θ̃ = 5 for 7. Every one of these ties occurs at n = 4. | B |
| L | For j < 2·10^4 and \|θ̃\| ≤ 300, a run from (j,θ̃) ends at an n=4 tie only if θ̃ ≡ 6 (mod 8) or θ̃ ≡ 5 (mod 16). Ties at n = 7 need \|θ̃\| ≥ 55. No other tie level occurs. | B |
| D | Drift bookkeeping: inside a b/c-run, θ̃ = θ̃^{W} + δ with δ fixed. δ changes only at a-steps (θ̃ ↦ 3−θ̃) and at the start of a new copy. Growth bound \|θ̃_{t+1}\| ≤ \|θ̃_t\| + max(3, 2+\|θ̃^W\|). | A |
| P | Partial NT: under the hypotheses of Theorem B, NT_t holds whenever (j_t ≠ 5 or θ̃_t ≢ 5 mod 16), (j_t ≠ 8 or θ̃_t ≢ 58 mod 128), and \|θ̃_t\| < 1012. | A+B |
| R | Exact residual (sufficient for NT, hence for (EL) by EL Theorem B) — see §5. | open |

## 1. Lemma C′ (sharp one-step tie law) [A+B]

Let chain t be followed by an a-step at n = j_t−1, so X(n) is odd and of type a. Let k_n = τ(n)/2. Assume all
earlier a-steps of the epoch are NT, so that by EL (A3) θ̃_t ≡ Θ_t (mod 2^{j_t}).

*Claim.* By EL Theorem A, a tie is exactly θ_t + 3k_n ≡ 2^{n−1} (mod 2^n), i.e. θ̃_t ≡ c_n (mod 2^n).
- *n < 10^6 [B, N5]:* the odd type-a crossings, together with their k_n, come from the certified λ-walk.
  The smallest centred |c_n| are 5 (n=4), 58 (n=7), 1012 (n=11), 4081 (n=13), 32750 (n=16), 1048552 (n=21).
- *n ≥ 10^6 [A]:* by (C1), 3k_n ≤ 1.5n². So |c_n| ≥ 2^{n−1} − 1.5n², which is far above 1012 (EL E7).

Hence a tie requires θ̃_t ∈ (5+16ℤ) [n=4] ∪ (58+128ℤ) [n=7] ∪ {|θ̃| ≥ 1012}. Lemma C ([−10,4]) is the special
case that avoids 5+16ℤ around 0. ∎

Because X(4) and X(7) are odd and of type a, a chain with j_t = 5 is always followed by the n=4 a-step, and a
chain with j_t = 8 by the n=7 a-step. Proposition P follows from C′ directly.

## 2. Proposition W/L: why no window closes [B]

N2 runs the full automaton (Φ = certified data to i = 10^6) from every (j,θ̃) with 1 ≤ j < 2·10^5 and |θ̃| ≤ 40.
The result is that the tie-free values around 1 are exactly −1..4. The neighbour −2 ties for 2788 values of j,
the typical path being (17,−2) →a(n=16,k=6)→ (5,5) →tie at n=4. The neighbour 5 ties directly at j = 5.

Now combine this with the rules (EL A3 and Remark S):
- fire → 1;
- b-step after a fire → 1+1−2 = 0;
- a b-step from a chain of value θ̃ copies a W-fire (value 1), giving θ̃+1−2 = θ̃−1. Nested fire copies (EL §6) therefore give the chain 1 → 0 → −1 → −2.

So any window that contains the real values {0,1,2} and is closed under "copy a W-chain whose value lies in the
window" contains −2. That window is not tie-free. **An induction on epoch order with a θ-window as the invariant
therefore cannot close.** This holds for every window, not only [−10,4]. The brief's concern is confirmed: the
drift is real at the level of the automaton. What is unknown is whether F realises it, i.e. whether three nested
level fires have b-type first returns with the parameters required (EL §6).

L (N3) shows that, as far as computed, the multi-step tie set is a union of residue classes: 6 mod 8 or 5 mod 16
(ending at n=4), plus classes of size ≥ 55 (ending at n=7). The obstruction is therefore arithmetic (mod 16),
not a matter of size.

## 3. Proposition D (drift bookkeeping) [A]

Fix an epoch. Call chain t an *anchor* if it is the fire (θ̃=1) or the target of an a-step. Let t be an anchor,
and suppose steps t→t+1→…→t+m are all b/c. By Remark S these chains are the M_u-images of consecutive top-level
chains w, w+1, … of one W-epoch, so θ̃_{t+i} = θ̃^W_{w+i} + (θ̃_t − 2) for 1 ≤ i ≤ m.

The next a-step gives θ̃ ↦ 3−θ̃ and a new anchor. Hence
  |θ̃_{t+1}| ≤ |θ̃_t| + 3 (a-step),   |θ̃_{t+1}| ≤ |θ̃_t| + 2 + |θ̃^W| (b/c).

The W-epoch has fire parameter J_W ≤ log2(3n²+4) < J (by (C1)), so its θ̃-values obey the same rules at a
smaller J. Writing G(J) := max|θ̃| over the exit of J (finite while NT holds), this gives
G(J) ≤ 1 + r_J·(3 + G(⌊log2(3J²+4)⌋)). The base case is G(J) ≤ 3 for J < 10^6 (N4: exit values in [−1,3], r ≤ 2) [B].

This recursion is **multiplicative**: G can grow by a constant factor at each tower level. So the bound
|θ̃| < 1012 of Prop. P is automatic only for a bounded number of tower levels beyond T₁. It does not hold for all
J. Even where it holds, the residue part of (R) is not implied.

Logarithmic descent [A, from Theorem A and C′]: if n ≥ 11 and |θ̃_t| < 1012, an NT a-step gives
j_{t+1} ≤ 1+log2(1012+1.5n²), and a b/c-step gives j_{t+1} ≤ log2(6n²+5) (EL §7). So the chain reaches j ≤ 11
after O(log* J) steps and then has at most 6 further chains.

## 4. Real-walk census [C]

N1, real walk to i = 10^6: 302,879 fires; a-steps 1→2 (15,822) and 2→1 (28); b-steps 1→0 (7,910). There are no
c-steps at top level, no chain of value 0 ever continues, and every real θ̃ lies in {0,1,2}. The drift paths of
§2 are not seen in F's data. This is consistent with (R), but the J's involved are small (≤ ~40), so it carries
no weight at J ≥ T₁.

## 5. Exact residual (R) and what is proved

**(R)** In every epoch with J ≥ T₁, every chain t that is reached with all earlier a-steps NT satisfies:
- (R5) j_t = 5 ⇒ θ̃_t ≢ 5 (mod 16);
- (R8) j_t = 8 ⇒ θ̃_t ≢ 58 (mod 128);
- (Rs) |θ̃_t| < 1012 whenever chain t is followed by an a-step at some n ∉ {4,7}.

(R) implies (NT) by C′ and induction along the epoch, and (NT) implies (EL) inside Theorem M's induction (EL
Theorem B). (Rs) follows from Prop. D for J in the first few tower levels above T₁, but not in general. (R5)
fails in the automaton under adversarial W-data: the path (17,−2) → (5,5). Closing (R5) therefore needs
arithmetic about F at large levels. Specifically, one must exclude that three nested level fires all have b-type
first returns with the parameters needed to produce θ̃ ≡ −2 (mod 16) at a chain whose next crossing sends it to
j = 5. This is a congruence condition on k-values (via ω(n)) at levels ≥ 10^6−2.

Proved here, for all J [A] (inside Theorem M's induction): the tie law C′ for n ≥ 10^6, the bookkeeping D, and
the reduction P/(R). [B]: C′ for n < 10^6, W, L, and the base case G ≤ 3.

## 6. Reproduce

`python -B verify_nt.py 1000000 200000 40 20000 300` (N1–N5, roughly 20–40 min). No git operations were
performed, and nothing outside work_nt/ was written.
