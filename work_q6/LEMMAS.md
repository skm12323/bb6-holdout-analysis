# Q6 — Refined Halting Criterion on the v2 rules (`1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---`)

Foundation: `work_q4/RULES.md` (frozen). M, rows R1,R1',R2,R2',R3,R3',R3'',R3k,R4,R5,R6,X0, H = H1∪H2∪H2'∪H3,
invariants I1–I4, orbit c_0=([1,1],A,0), c_{s+1}=M(c_s). Row effects are quoted from RULES.md Sec.3 ("table").
Checker `verify_q6.py`: Sec.1 = the only Class-B item; Secs.2–4 are sanity tests of Class-A lemmas (not proofs);
Sec.5 = Class-C. Notation: list B=[b_0..b_{m-1}], phase (A,i) / (D,d).

## 0. Class-B base
**B0 [Class-B].** Exact computation of c_0..c_20 (verify Sec.1, rows printed): none lies in H (rows used: R3'',R1,R2,R3',
R5,R3k,R1',R3,R4). c_10=([5,1,4,2],A,0); c_20=([3,10,1,4,2],A,1). In particular R2',X0,R6,H* do not occur in c_0..c_20.

## 1. The steady set S
**S_A** = (A,i) with: (a) b_k≥1 for k<i; (b) i≤m-4, b_{m-2}=4, b_{m-1}=2, b_k≥2 for i+2≤k≤m-3; (c) b_{i+1}≥1, and
either b_i≥1, or [b_i=0, i≥1, b_{i+1}≥2, and (b_{i-1}≥2 or i=1)].
**S_D** = (D,d) with m≥3, 1≤d≤m-2, all b_k≥1, b_k≥2 for d≤k≤m-3, b_{m-2}=4, b_{m-1}=2.
S=S_A∪S_D ⊆ Inv (I1–I4 immediate). c_10∈S_A (m=4,i=0; range in (b) empty; b_1=1, b_0=5).

**Lemma C (closure) [Class-A].** Let c∈S. Then either M(c)∈S, or c∈S_D with d=m-2 and M^7(c)∈S_A (gadget G), or
c=(A,1) with b_0=1,b_1=0 and M(c)∈H1. No other row of the table is applied. Proof, by the L1 decision tree:
* S_A, n=b_i≥2 → **R1** (i≥1) / **R1'** (i=0; list gains block 0=1, A moves to i'=1, so i'≤m'-4 still). New b_{i'-1}≥1,
  b_{i'+1}=b_{i+1}+1≥2, tail untouched. If n-2=0: i'≥1, b_{i'+1}≥2, and b_{i'-1}=b_{i-1}+1≥2 (R1) or i'=1 (R1'); (c) holds.
* S_A, n=0: by (c) i≥1 → **R2** (never R2'/X0/H1-at-entry). If b_{i-1}≥2: new A at i-1 with value b_{i-1}-1≥1, b_i:=1,
  old b_{i+1}≥2 now sits at (i-1)+2; (a)(b)(c) hold. If i=1 and b_0=1: result ([0,1,…],A,0), m≥5 ⇒ **H1**.
* S_A, n=1: i+1≤m-3 so not R3''; b_{i+2} exists with i+2≤m-2 and b_{i+2}≥2 (by (b), or =4) ⇒ **R3/R3'** (never R3k/H2/H2').
  Result (…,p+1,j+3,b_{i+2},…,4,2), D at the old b_{i+2} block, index d=i+1 with m'=m-1 (R3, i≥1) or d=2 with m'=m (R3', i=0; m≥4):
  d≤m'-2, blocks from d to m'-3 are old blocks ≥2 ⇒ S_D.
* S_D, d≤m-3: b_{d+1}≥2 ⇒ **R4** (never R5/R6/H3), D at d+1 ⇒ S_D.
* S_D, d=m-2 (**Lemma G**): with X=b_{m-3} (exists, m≥3) the rows are forced:
  R4 (b_{m-1}=2) → D at m-1; **R5** (L=2) → (…,X,4,0,1) A at m-1; **R2** (n=0,p=4) → (…,X,3,1,1) A at m-2;
  **R1** (n=3, i=m-2≥1) → (…,X+1,1,2,1); **R3k** (n=1, b_{i+2}=1 last) → (…,X+4,2,3,2) A at m-2; **R1** (n=2) → (…,X+5,0,4,2);
  **R2** (p=X+5) → (…,X+4,1,4,2), A at m-3 = m'-4. This is S_A (value X+4≥5; the range i+2≤k≤m'-3 of condition (b) is empty and b_{i+1}=1≥1). □
**Corollary U [Class-A | B0].** After c_9, rows R2', X0, R3'', R6, H2, H2', H3 never apply; the orbit leaves S only into H1 or into a G-interior (e.g. c_13∈S_D, c_14..c_19 G-interior), returning to S_A after 7 steps.

## 2. The left edge
**Lemma E (edge cascade) [Class-A].** Let c=(A,0) ∈ S_A with u=b_0 (≥1 by (c)).
* u odd: u=1 goes directly to R3'; u≥3: one R1' followed by (u-3)/2 R1 steps (A at 1) give [ (u-1)/2,1,b_1+(u-1)/2,…], then R3 ⇒ D phase.
* u=2: R1' → ([1,0,b_1+1,…],A,1), then R2 with b_0=1: the second macro step lands on ([0,1,…],A,0), which is in H1 (m≥3 holds since S_A has m≥4); the TM halts 14 TM steps later.
* u even ≥4: R1', (u-2)/2·R1 at i=1, R2 ⇒ ([u/2-1, 1, b_1+u/2, …],A,0) ∈ S_A, new edge value u/2-1≥1.
Hence u+2 is halved at each cascade step; the cascade ends in H1 iff u+2=2^k (k≥2), otherwise in an odd value and a D-wave.
Proof: rows read off directly; R1' and R2 at i=1 are the only ways A enters/leaves block 0 (R1' moves A to 1, R2 from i=1
moves it to 0; R2',X0 excluded by Cor.U). □

**Definition.** An *edge event* is c_s=(B,A,0), s≥10. It is a *real arrival* if no earlier edge event c_r has all of
c_r..c_s in phase A; else a continuation (Lemma E: then b_0(c_s)=b_0(c_{r'})/2-1 for the previous event r').
In particular c_10 is a real arrival: c_5..c_9 are phase A at i≥1, and c_3 is (A,0) and is followed by the D-phase c_4.

**Theorem RHC (Refined Halting Criterion) [Class-A | B0].** The M-orbit hits H ⇔ some real arrival (s≥10) has
u0=b_0 ∈ {2^k-2 : k≥2}. Equivalently (Reduction Theorem v2) the TM halts ⇔ this happens; the hit is then always H1.
Proof. B0: c_0..c_9∉H, c_10∈S. Lemma C+induction: every c_s, s≥10, is in S or in the gadget interior (non-H by the
explicit rows), until the H1 exit. That exit needs (A,1), b_0=1, b_1=0. Inside S, b_1=0 with A at 1 is created only by
R1' from an edge event with u=2 (R1 at i=1 makes b_0≥2; R2 from i=2 gives value b_1-1≥1 by (c); G ends with value ≥5).
An edge event with u=2 is reached iff the real arrival opening its cascade has u0+2=2^k (Lemma E). □
(Class-B dependence is only B0; the lemma chain itself is symbolic.)

## 3. Sweep Lemma — exact map between sweep starts
A *sweep start* is Σ(b) = ([b_0,…,b_s,1,4,2], A, s) with all b_t≥1. By B0, c_20=Σ([3,10]).
**Lemma W [Class-A].** Let Σ(b) be a sweep start with b_s even. Pad b_t=0 for t<0. Put e_s=b_s+2 and, for t=s-1,s-2,…,
e_t = b_t + e_{t+1}/2 while e_{t+1} is even. Let l = the first (largest) t<s with e_t odd.
(i) If e_t=2 occurs (only possible at t<0) before an odd value, the orbit hits H1.
(ii) Otherwise the next sweep start is Σ(b'), with (re-indexed so the first nonzero block is index 0)
 b'_t=b_t (t≤l-2), b'_{l-1}=b_{l-1}+(e_l-1)/2, b'_l=(e_l+5)/2, b'_t=e_t/2 (l<t<s), b'_s=e_s/2+4.
Proof. *Pass step* (A at t, even value w_t=e_t-2, right neighbour 1): w_t/2·R1 then R2 (A at 0: R1' first; Lemma E) give
b_{t-1}+w_t/2-1 = e_{t-1}-2 as the new A value, b_t:=1, right neighbour 1+w_t/2=e_t/2. Virtual blocks: R1' is R1 with p=0;
R2 at i=1 with b_0=1 is the e=2 case ⇒ H1 (Lemma E). *Stop* (odd w_l): (w_l-1)/2·R1 then R3/R3' merge
(p,1,1+(w_l-1)/2,k) → (p+(w_l+1)/2, (w_l+7)/2, k); R3 (not R3k/H2) applies since k≥2: k is block l+2, which holds e_{l+1}/2 (for l=s-1 this is e_s/2=6), and every passed position has e≥4 (even, ≥3 for t≥0 since b_t≥1 and e_{t+1}≥4; ≠2 for t<0, else W(i)); list shortens by one, D-wave via R4 to the tail (Lemma C), then G adds 4
to the block before the final 4, i.e. to e_s/2. Since R3 shortens and G lengthens the list by one, the A of the new
sweep start is again at the block before `1,4,2`. □
**Corollary [Class-A | B0].** b_s=10 at every sweep start from c_20 on. Induction: base c_20=Σ([3,10]); b_s=10 ⇒ e_s=12 even ⇒ W(ii) applies (l<s) or W(i) halts, and b'_s=12/2+4=10. So the injected
carry is constant: e_{s-1}=b_{s-1}+6 every sweep. A real arrival occurs exactly when e_{s-1},…,e_1 are all even; then
u0=e_0-2, e_0=b_0+e_1/2, and RHC reads: **TM halts ⇔ some sweep has e_{s-1},…,e_1 even and e_0 a power of 2 (≥4)**, together with c_10 (u=5), the only arrival in c_10..c_19, which is not in H by B0.
Closed form along the passed chain: e_t = Σ_{r=t}^{s-1} b_r 2^{-(r-t)} + 12·2^{-(s-t)} (integer whenever reached).

## 4. Nature of the arrival map (Part 2)
**P1 [Class-A].** u0' is *not* a function of u0: it depends on the whole vector. Passed positions store b=e/2, so on
the next pass e'_t=(e_t+e'_{t+1})/2 — an averaging carry; the chain stops at the first odd sum, where Lemma W(ii)
injects (e_l±1)/2 into two blocks. This is a parity-driven halving system on Z_{≥1}^{s+1} with unbounded dimension
(s grows only at arrivals that pass into virtual blocks): Collatz-like (2-adic carry with odd-stop), not a binary counter
(sums are not reduced mod 2; blocks grow).
**P2 [Class-C].** Iterating W from [3,10] for 3·10^6 sweeps (verify Sec.5; W matches M on 3000 orbit sweeps + 3000
random starts, Sec.4): real arrivals u0 = 7,23,21,24,104,1290,647,7146,93998,281082 (plus u=1,5 at c_3,c_10 in B0);
none has u0+2 a power of 2. Prefix length 2→24. Chain-depth frequencies P(≥k passes) ≈ 1, .5, .125, .063, .031, .023,
.014, .007 — roughly geometric, so arrivals are exponentially rare in s and u0 grows; heuristically the halting event
has summable probability, but **no proof that u0+2 avoids powers of 2 was found**. Non-halting remains OPEN.
