# G2: a-returns after b/c returns (machine #1 `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`)

2026-10-14, Analysis Agent G2. **Not audited. No global non-halting claim.**
Writes only in `work_g2/`. Tags: [A] all parameters (proof below), [B] finite exact computation,
[C] data / conjecture / research.

Notation follows `work_claude_global/NOTES.md` §1 (accepted): at a top-level chain, Θ=3s+5, x=λ_x,
j=v2(x), n=j−1; x=2^j·(odd). Exit recurrence (NOTES §1, from PROOF_M Lemma 6.1; checked against
F on 18,171 epochs):

    a  (n odd-head, type a, k=τ(n)/2):  x' = 2Θ − x/2 + 6k,         Θ' = Θ+3+6k
    b/c (W's chain value at τ(n) is (c_X, λ_X)):  x' = c_X·x/2^j + λ_X,  Θ' = Θ+3τ(n)+3
    hpar[n]=0: even return, epoch ends.

The fire at s_0 (even) has x_0=3s_0+4=2^J u (u odd), Θ_0=x_0+1.
Facts used (all [B] in `verify_g2.py`, besides being in the accepted sources):
F0 τ(n) ≤ n for n<20000 (PROOF_M V2: up to 10^8); in the Theorem-M induction (C1) τ(n) ≤ n² is
available for all n<ρ. F1 a b-type odd-head crossing n sits at an epoch start s′=τ(n), even, ≥1, and
X(n)=(3·2^{n−1}, 3s′+4) (NOTES §2, PROOF_M P2). F2 crossings 0,1,2,3 have even head (hpar=0), so any
odd a-return has j ≥ 5. (S1) (PROOF_M Lemma 2.1/R1): every W-chain satisfies j < σ:=v2(c_x).

---------------------------------------------------------------------------------------------------

## A. First step b, second step a  [A, with a finite base [B]]

**Lemma A.** Fire with parameter J, odd u, crossing J−1 of type b with odd head, s′=τ(J−1)=2K.
1. x_1 = 3·2^{J−2}u + 6K + 4, Θ_1 = 2^J u + 6K + 4, hence Θ_1 − x_1 = 2^{J−2}u.
2. q := v2(6K+4) = J(s′) satisfies q ≤ J−3, and the sharper q ≤ J−4 for J ≥ 12 (from (C1); for J ≤ 11 the only b-type odd-head
   cases are J=6 (q=1) and J=9 (q=4), both checked), so j_1 = q.
3. If the next return is odd type a (crossing q−1, k=τ(q−1)/2):
   x_2 = 13·2^{J−3}u + 9K + 6 + 6k, and **j_2 = 1 + v2(k) ≤ q−2 < q.**

*Proof.* (1) b-update with x_0=2^J u, j=J, c_X=3·2^{J−2}, λ_X=3s′+4=6K+4 (F1):
x_1=3·2^{J−2}u+6K+4. Θ_1=Θ_0+3s′+3=2^J u+1+6K+3. Subtract.
(2) 6K+4=3s′+4 ≤ 3(J−1)²+4 < 2^{J−3} for J ≥ 12, so q ≤ J−4 < J−2 = v2(3·2^{J−2}u); thus v2(x_1)=q.
J ≤ 11: only J=6,9 occur (b-type odd head at index J−1 ∈ {5,8}); q=1,4 ≤ J−3. [B]
(3) x_2 = 2Θ_1 − x_1/2 + 6k = 2^{J+1}u + 12K + 8 − 3·2^{J−3}u − 3K − 2 + 6k = 13·2^{J−3}u + 9K+6+6k.
The odd-head crossing q−1 is at an epoch start s″=τ(q−1)=2k ≥ 1 (F1/F2), so k ≥ 1. Valuations:
v2(13·2^{J−3}u)=J−3; v2(9K+6)=v2(3(3K+2))=q−1 (since 6K+4=2(3K+2)); v2(6k)=1+v2(k).
Need v2(k) ≤ q−3; it suffices (not equivalent) that k < 2^{q−2}, i.e. τ(q−1) < 2^{q−1}: true by (C1) when q−1 ≥ 5 ((q−1)² < 2^{q−1});
for q ≤ 5 an odd a-return needs q−1=4 (F2), τ(4)=2 < 16 [B]. Then 1+v2(k) < q−1 ≤ J−4, so the
minimum is attained uniquely: j_2 = 1+v2(k) ≤ q−2. ∎

**Hypotheses, all explicit:** J ≥ 3 with crossing J−1 b-type odd head; (C1) at indices J−1 and q−1
(or F0 below 10^8); next return odd a. No tie assumption — ties are excluded by the proof.
(C1) is available at J−1 and q−1: both are < ρ, since J = j_0 < σ_0 = ρ by (S1) (PROOF_M R2) and
q−1 < q ≤ J−3. F1/F2 are used for all n, as proved in NOTES §3 and PROOF_M P2; `verify_g2.py`
re-checks them only for n < 20000.

**Reconciliation with NOTES §6 (38/317).** The NOTES §3 formula j_2=min(J(τ(m)), m), m=j_1−1, was
derived for an **a** first step (it uses Θ_1=2^Jλ_u+4+6K with 3K+1=2^m·odd). After a b first step
the state is different (Θ_1−x_1=2^{J−2}u, x_1 ≡ 6K+4); the true value is v2(9K+6+6k), whose 9K+6 term
has valuation q−1=m. So the old formula reads min(v2(3s″+4), m) where the truth is v2(3s″)=1+v2(k).
They agree only by coincidence. `verify_g2.py` reproduces the auditor's population exactly
(smallest λ, 12 ≤ J < 20000): 317 cases, old formula fails 38, Lemma A fails 0. The old formula was
not wrong; it was applied outside its hypothesis. Additional checks: x_1, Θ_1, q for 24,220 (J,u)
pairs; x_2 and j_2 for 1,268 b→a pairs, all whole tails strictly descending [B].

**Interpretation (A′, [A]).** With D := Θ_1 − (3s′+5) = 2^J u − 1 and E_1 := x_1 − (3s′+4) = 3·2^{J−2}u,
the outer state is a copy of the earlier fire epoch at s′ shifted by D ≡ −1 (mod 2^J). Lemma A is
the resolution of the one valuation collision of Lemma C1 below at t=0 (reference return r=1).

---------------------------------------------------------------------------------------------------

## B. a-returns after an exact θ=2 copy  [A, conditional on the induction hypothesis]

**Copy lemma (self-contained version of PROOF_SHADOW §4 inside the recurrence).** Outer parent chain
p (Θ_p, x_p=2^{j_p}w, w odd) makes an odd b/c return at n=j_p−1. Reference R = W's chain at step τ(n),
(Θ^R_0, x^R_0)=(3τ(n)+5, λ_X), and its remaining suffix in its own (earlier) epoch, with coefficient
valuations σ^R_t (σ^R_0 = v2(c_X) = n−ε(n)). Put D := Θ_p − 2, E_t := x^O_t − x^R_t. If
**v2(D) ≥ σ^R_0 − 2** (in particular if Θ_p ≡ 2 mod 2^{j_p}, "exact θ=2"), the outer suffix has the
same j-sequence, types and even ending as R's suffix.

*Proof.* Θ^O_0 − Θ^R_0 = Θ_p+3τ+3−3τ−5 = D; while the j's agree, both runs add the same increments, so
Θ^O_t − Θ^R_t = D for all t. E_0 = c_X·w, v2(E_0)=σ^R_0. Invariant v2(E_t) ≥ σ^R_t. Given it, (S1)
for R (j^R_t < σ^R_t) gives j^O_t = j^R_t, hence the same crossing, type, k or (c_X,λ_X). Then
a: E_{t+1} = 2D − E_t/2, v2 ≥ min(v2(D)+1, σ^R_t−1) ≥ σ^R_t−1 = σ^R_{t+1} (σ^R_t ≤ σ^R_0);
b/c: E_{t+1} = (c/2^j)E_t, v2 = v2(E_t)−1−ε ≥ σ^R_{t+1}. At R's even return the outer ends too. ∎
(Exact θ=2 gives v2(D) ≥ j_p = n+1 > σ^R_0−2.) [B] 477/477 copies checked, tails identical.

*Identifications used in the proof.* σ^R_t := v2 of the W-chain coefficient c at R's t-th chain. (i)
σ^R_0 = v2(c_X) is the source epoch's own σ at its chain at step τ(n) (for a b-type crossing,
n = ρ′+1 of that source epoch). (ii) σ^R_{t+1} = σ^R_t − 1 − ε (PROOF_M Lemma 3.2), with ε = 0 at
a-steps. (iii) The (S1) invoked is the source epoch's top-level (S1) (for image/call chains PROOF_M Lemma 2.1; for R₀ = the source fire, from definedness via PROOF_M Corollary 3.5), valid
because F is defined on that epoch.

**Lemma B1 [A].** After an **a first step** (J−1 a-type odd head, j_1=v2(3s′+2) < J−1, NOTES §3),
Θ_1 − 2 = 2^J u + 3s′ + 2 has valuation exactly j_1: every b/c return at chain 1 is an exact θ=2 copy.
(Proof: Θ_1 = Θ_0+3+3s′ = 2^J u+4+3s′.) [B] 159/159 ('ab', δ=0).

**Theorem B (any depth).** Inside the induction on ρ (Theorem M / DL), assume DL — or a tail bound
L(·) — for every earlier epoch. If chain p of the current epoch makes a b/c return satisfying the copy
condition, then the remaining sequence j_{p+1} > j_{p+2} > … is the suffix of an earlier epoch; it
strictly descends and j_{p+1} < j_p (NOTES §4(ii): j_{p+1}=W's j at τ(n) ≤ log2(6τ(n)+5) < j_p).
Its length is at most that earlier epoch's r. *Proof:* copy lemma; the source chain lies in an epoch
with pointer ≤ n < ρ that has already ended (current fire has empty stack; PROOF_SHADOW §4.2). ∎
*Base.* For source epochs with ρ ≤ N_B the hypothesis is supplied by finite certification: the
PROOF_M V2 certificate (to 10^8). The 4·10^8 skeleton data are unaudited for r = 3 and are not used. Caveat (re-review): V2 certifies only the margin j<σ and r ≤ 2, i.e. the tail-length arm of the hypothesis; strict descent (DL) for ρ ≤ 10^8 is not certified anywhere. Hence for sources with ρ ≤ N_B Theorem B yields only the tail-length conclusion (outer tail ≤ the source's r ≤ 2); the strict-descent conclusion requires a separate descent readout over the V2 range (such sources have J ≲ 55, inside V4's J < 10^6) — not done here.
So every a-return (and every G1 collision) after such a copy is inherited from an earlier epoch.
What B does **not** give: the induction hypothesis itself — DL must hold for the source epoch, i.e.
B is a reduction, not an unconditional closure.

---------------------------------------------------------------------------------------------------

## C. General b/c→a: small offsets and collisions  [A for the lemmas, C for the rest]

**Lemma C1 (small-offset copy) [A].** Same setting as the copy lemma, but D ≡ δ (mod 2^{j_p}) with
δ ∈ {−2,−1,1,2}; h := v2(2δ) ∈ {1,2}. Then
(a) through R's b/c prefix the outer j's equal R's (E_t = c^R_t·w exactly, valuation σ^R_t > j^R_t);
(b) if R ends during that prefix, so does the outer;
(c) at R's first odd a-return (from chain t, giving r=j^R_{t+1}):
    x^O_{t+1} = x^R_{t+1} + 2D − E_t/2 ≡ x^R_{t+1} + 2δ  (mod 2^{min(j_p+1, σ^R_t−1)}),
and since j^R_t ≥ 5 (F2), σ^R_t−1 ≥ 5 > h. **If r ≠ h, the outer gets j=min(r,h) ≤ 2, and crossings
0,1 have even head: the epoch ends.**
(d) Only the collision r = h remains; then R itself ends there, and the outer value is
v2(x^R_{t+1} + 2D − E_t/2) > h, determined by higher bits. ∎

**Lemma C2 (offsets of real states) [A].** With D = Θ_p − 2 at the parent of a b/c return:
| prefix before the b/c return | δ mod 2^{j_p} | reason |
|---|---|---|
| fire (first step b or c) | −1 | Θ_0−2 = 2^J u − 1 |
| a | 0 | Lemma B1 |
| b | −2 | Θ_1−2 = 2^J u + (3s′+4) − 2, q ≤ J−3 |
| a,a (NOTES §3 non-tie) | −1 | Θ_2−2 = 2^J u + (3s′+2) + (3s″+4) − 1, valuations j_1, J″ ≥ j_2 |
| b,a (Lemma A) | +1 | Θ_2−2 = 2^J u + (3s′+4) + 3s″ + 1, v2(3s″)=j_2 < q |
Table rows are *prefixes*; data labels are full return-type strings ending in the b/c return:
data 'b'/'c' = row "fire", 'ab' = row "a", 'bb' = row "b". Row a (δ=0) is handled by the copy lemma,
not by C1.
Data [B] (J<20000, one random u each): 'b'→−1 (6055), 'c'→−1 (318), 'ab'→0 (159), 'bb'→−2 (158);
C1(c) held 279/279; 39 collisions (35 resolving to j=2, 4 to j=3), all with δ=−1 at the first step, all ending the epoch (per run_g2.txt).
Rows a,a and b,a are **untested on their exact hypothesis**: in the tested range no a,a or b,a prefix
is followed by a b/c return. Auditor 1 checked only the residue Θ_p−2 ≡ δ at such parents (18,978
a,a and 18,990 b,a symbolic cases).
In the J=50,148,477 exit (aaba), j_3 = 1 is v2(λ_X(5)) = v2(10) = 1, by C1(a) and the copy property;
δ plays no role there.

**Consequence.** Offsets are established only for the prefixes ∅ (fire), a, b, a,a (non-tie case;
the tie case relies on the m < 8 finite check of NOTES §3), and b,a. For these, G2 is settled except
for the collision events of C1(d); the collision at t=0 after a first-step b is Lemma A (resolved,
j < q). Not covered: prefix c,a, and collisions after a c-type first step (reference chain is not a
fire; no closed form).

**What remains (research, [C]).**
1. *Collisions with t ≥ 1* (R has a b/c prefix before its first a-return, and that return hits
   r = h ≤ 2, i.e. R ends there). The outer value v2(x^R_{t+1}+2D−E_t/2) depends on x^R_{t+1} beyond
   2 bits. Needed: a bound v2(x^R_{t+1} + 2δ) < j^O_{t} from the source epoch's own canonical form
   (as in A, where x^R_1 − 2 = 3(3K+2)+6k). For first-step c the reference is a non-fire chain.
2. *Offset invariance at depth ≥ 3.* Required correlation: **every b/c copy in a real exit has
   D ≡ δ (mod 2^{j_p}) with δ ∈ {0,±1,−2} (or a fixed small set)**, propagated through a-steps and
   through collisions. C2 proves it for prefixes of length ≤ 2 only. Θ is the carrier: an a-step adds
   3+6k, a b/c step adds 3τ+3, so δ at depth d is a signed sum of the 3s+4 / 3s+2 residues of earlier
   crossing times, each divisible by a power of 2 ≥ the current j (that is what happens in C2).
3. *Why local legality is insufficient.* By C1, a rise right after a b/c→a needs either an offset
   δ outside {0,±1,±2} or an unresolved collision. Astra's mass-compatible state 65 →b 5 →a 8 must be
   one of these (I did not re-derive its offset). C2 rules out the first option for prefixes of
   length ≤ 2.
   So a proof must carry δ (equivalently Θ mod 2^{j}) as part of the state; (Θ,x)-free j-graphs fail.
4. *Weaker target.* C1 shows every non-colliding small-offset copy ends the epoch within the length of
   R's b/c prefix, which strictly descends (NOTES §4(ii)). If collisions were shown to occur at most
   O(1) times per epoch, r ≤ 1 + C·log follows, enough for (EL).
5. Not touched: G1 (a→a collisions after a→a), the real-machine endgame.

No epoch in the data (J<20000, three random u per J, plus 24,220 Part-A runs) has a non-descent.

## Review record
Three-way review (2026-10-14), mathematics unchanged, wording patched as above:
- Adversary: "fixable gaps" (items addressed: (C1) index range, copy-lemma σ identifications,
  Theorem B base, J=50,148,477 remark, scope of Consequence, C2 data labels, q ≤ J−4, F1/F2 scope).
- Blind auditor 1 (numerical, 424,025 symbolic first steps, 0 failures): "all correct". Counts:
  1,582 real first-step-b epochs; 22,155 symbolic b→a cases; 9,498 chain-1 copies; 2,262 collisions,
  all at the fire, all resolving to j ∈ {2,3}.
- Blind auditor 2 (deepseek, by hand): "all correct".

## Files
- `verify_g2.py` — all [B] checks (`python -B verify_g2.py 20000 20000`, ≈30 s). Output: `run_g2.txt`
  (ends "ALL OK" / "Part C ALL OK"). Imports `work_claude_global/fdata.py` read-only.
