# 已通过三方审查 / accepted (reviews/claude_ext_next_review_record.md) — defect calculus for EXT sources (Claude, 2026-10-19)

## 中文摘要

- 引入"低位相差" d = Theta - x 的自动机：A: d->3-d，B: d->d-1，C(w): d->d+Phi(w)-2，火 d=1。
  任一 c 来源历史 w 的外层入口在精度 p-1 下等于统一参考族 G_delta(p)=(6k_p+4-2delta, 6k_p+4-delta)，
  delta=Phi(w)-1（需"下降假设"DH，见 §2）。已知全部归约（C3, AA, BA, CA, BAA->MINUS=G_-1, BBA->PLUS=G_3）都是它的特例。
- 闭合判据统一为（在 DH 下）：中途某链 d=2（推广的 A-SOURCE，称 P2；i=1 即 A-SOURCE，无条件），或 delta∈{0,1,2}（delta=0 的闭合仅针对 DR 来源）。
- 亏损 ε=3,5,...,15 的历史词数为 Catalan 数 1,2,5,14,42,132,429。ε=9：14 词，开放 2 个（BBAA->G_-2，BBBA->G_4）；
  ε=11：42 词，开放 17 个（delta∈{-3,-1,3,5}）；ε=13：132 词，开放 27 个（delta∈{-4,-2,4,6}）。
  **每个亏损恰好新出现两个 delta**（B^(r-1)A 给 delta=r，B^(r-2)AA 给 delta=-(r-2)）。逐亏损 casework 不会收敛到有限族，
  但所有族都是单一双参数族 G_delta(m)；走一步后与外层 b 残余族 H_delta 合流。
- 外层 b 入口：EXT(omega) 经 RB 精确传递到 E_F 的首个 a 步；-1 时钟偏移在 b/c 步不可见，在首个 a 步变为 x 的 -2。
  若 E_F 在该 a 步不终止，外层立即以 j=1 结束（安全）；唯一残余是 E_F 恰在首个 a 步终止，此时（另需前提 DH_out）外层在精度 m-1 下等于
  H_delta(m)=(6k_m+6-2delta, 6k_m+6-delta)，delta=4-d。规范数据中只出现 delta=3（即 (6k,6k+3)，k 偶）与 delta=4。
- 没有证明 EXT，没有改变视界，没有闭合任何新族。

Tags: [A] proved for all parameters (under stated hypotheses), [B] finite computation, [C] conjecture/data.
Standing hypotheses unless said otherwise: least strict-EXT counterexample J (EXT(J') for all J'<J),
F defined through X(J-1), C1/CLOCK, accepted HP, AB, RB, Lemma K, uniform fire transfer, weight grammar
epsilon=W+1, PROOF_M Lemma 2.3. Script: `verify_defect.py` (writes `defect_checks.json`), `grammar.py`.

## 1. One-step shift lemma (SHIFT) [A]

Let a scalar state have parameter j=v2(x), m=j-1, X(m) odd, and full integer defect d=Theta-x.
Let R be the real chain of Lemma K at X(m): type a: R=(6k+4, 6k+5) (the fire at pointer m), sigma_R=m;
type b/c: R=(x_C, 3tau(m)+5), sigma_R=m-eps(m). Then the output satisfies, modulo 2^sigma_R,

    type a:   (x',Theta') = (x_R+2(d-2), Theta_R+(d-2)),  new defect 3-d;
    type b/c: (x',Theta') = (x_R,        Theta_R+(d-2)),  new defect d_R+d-2.

Proof: identical algebra to the proof of AB (which is the case d=2): a: x'=6k+4+2(d-2)+3x/2, Theta'=Theta_R+(d-2)+x;
b/c: x'=x_C+c'u, Theta'=Theta_R+(d-2)+x, with v2(3x/2)=m, v2(c')=sigma_R, v2(x)=m+1. QED.
Checked [B] on all odd crossings n<1024, d in [-12,12], four odd bases, three high lifts (190,200 cases). (This
re-verifies the script's own affine maps, so it is a consistency check, not independent evidence.)

Consequence (corrected after review): a state of defect 1 is itself fire-shaped (reference F(q), EXT(q) by uniform
fire transfer); a state of defect 2 closes by AB. Under SHIFT: type a with input d=2 gives R (the fire); input d=1
gives a phase-two state (6k+2,6k+4) of defect 2 (AB) — the fire-shaped (6k+2,6k+3) appears only after the outer −1
offset, as in C3. Type b/c with input d=1 gives V(C,-1), chain 1 of S(m+1) (RB).

## 2. Low-defect invariant (LOW) [A, under DH]

Defect automaton on Z: fire d=1; A: d->3-d; B: d->d-1; C(w): d->d+Phi(w)-2, where Phi(w) is the value after the
last letter of w (w = the copied c crossing's own history). B is the same rule with the copied chain a fire (d_R=1): d+1-2.

**DH (descent hypothesis) for a history:** at every A letter, read at parameter j with half-time k and automaton value
d before it, v2(6k+2d) < j-1. (Recursively also inside the histories w of all C letters.)

**Lemma LOW.** Under DH, every chain D_i of a real epoch with history prefix w_i has real defect
d_i = Phi(w_i) mod 2^(j_i+1), and j strictly decreases (a: by >=2, b/c: by >=3).
Proof: induction on i (and on pointer order for nested C). Errors: a-step adds -x/2 (valuation j-1 >= j'+1 by DH);
b/c-step error x - c'u, of valuation sigma_R >= j'+1 by S1 (for b this is x/4, valuation j-2 >= omega+1); c-step adds terms of valuation >= sigma_C >= j'+1, and the copied chain's
own error (>= j_C+1 = j'+1 by induction). QED.

When is DH automatic? For complete source histories (ending in A): |Phi-3/2| <= W/2-1/2 [A]; for arbitrary
prefixes (e.g. ending in B) only |Phi-1| <= W/2 holds (corrected after review) (A preserves |d-3/2|, B moves it by 1, C(w) by
|Phi(w)-2| <= W(w)/2; induction on weight). With C1 (6k <= 3(j-1)^2) DH holds at every j>=10 provided
2|d| < 2^(j-1)-3(j-1)^2 (e.g. |d|<=134 at j=10, more beyond) AND 6k+2d != 0 (the bound only gives
|6k+2d| < 2^(j-1); the resonance d=-3k has infinite valuation). The references also need z=6k+4-2delta>0 (HP's
positive cone); the scans hit z<=0 at m in {5,8}. Odd type-a below 10: only (j,k)=(5,1),(8,2); DH fails
there iff d = 5 mod 8 (j=5) or d = 58 mod 64 (j=8). Whether, for each FIXED deficit, the hypothesis can fail only at finitely many explicit small parameters is
[C]: excluding the resonance 6k+2d=0 for large j needs a lower bound k_j>|d|/3 (C1 is only an upper bound). In any case since |d| can reach ~ eps/2 ~ 2log2 J, **DH is not automatic at all scales**
— a failure of DH is precisely a non-descent, i.e. the known EXT core.
Data [B]: real defect 1-lambda_Y = Phi mod 2^(omega+1) at every canonical c crossing tested (§5).

## 3. Defect reduction of c sources (Theorem DR) and generalized A-SOURCE (P2) [A, under DH]

Let X(J-1) be an odd c crossing, D_t its source chain (an a-output), source history w=w'A, p the parameter read by
the final A, k=tau(p-1)/2, delta := Phi(w)-1 = 2-Phi(w').

**DR.** Under DH for w (including v2(6k+4-2delta) < p-1 for the final A), the outer chain 1 V(D_t,-1) agrees with

    G_delta(p) = (z, z+delta),  z = 6k+4-2delta,

to precision p-1 (x error 2err+3x/2, Theta error err+x, err of valuation >= p+1 by LOW), and its coefficient
valuation is sigma_0 = n-eps = sigma_{D_{t-1}}-1 >= p (S1 of the real source). Hence S(J) is tie-free when
* delta=1: G_1=(6k+2,6k+3) fire-shaped, EXT(q), q<p-1 (C3, CA are instances);
* delta=2: G_2=(6k,6k+2) phase two, AB with an epoch ending before rho (BA, C(A)BA, ...);
* delta=0: G_0=(6k+4,6k+4) is EXACTLY chain 1 of S(p+1) (X(p) odd b by PROOF_M 2.3), EXT(p+1) (AA is the instance).
(Note: delta=0 forces d_{t-1}=2 with t>=2, which is always a P2 case; the item is kept for completeness.)
Proof: HP at precision p-1 with the references' records <= q < p-1 (resp. < p-1 from EXT(p+1) after the
2-unit first loss), margin sigma_0 >= p. Exactly the arguments of the accepted C3/C5-BA/AA/CA proofs; only the
small constant 2d changes. QED.

**P2.** If some intermediate source chain D_i (1<=i<=t-1) has automaton value 2, S(J) is tie-free.
Proof: the A-SOURCE proof verbatim with its precision P-1 replaced by pi_i >= j_i+1 (LOW): compare D_i with
R0=(x_{D_i},x_{D_i}+2); AB copies the real epoch E through X(j_i-1), which ends before rho; HP needs only
pi_i > j_i; COPY-PREC gives D_s vs C_s agreement >= sigma_ref,s; MARGIN = sigma_{D_i}-j_i > 0 (S1); the matched
C_s is an actual a-output (or the fire, J'=j_i+1), J' <= rho < J, EXT(J') applies. QED.
All A-initial words have d_1=2, so A-SOURCE is the case i=1.

The open words are those with no intermediate 2 and Phi(w) not in {1,2,3}; they reduce to G_delta(p),
delta=Phi(w)-1 not in {0,1,2}. MINUS=G_-1 (BAA), PLUS=G_3 (BBA).

## 4. Enumeration for item 3 [A for the counts and parity/bounds; A-sketch for "two new delta per deficit"; B for the table]

Words at deficit eps=2r+1 = sequences over {A,B,C(w)} of weight 2r ending in A, weights A=B=2, C(w)=2+W(w).
Counts are Catalan numbers [A]: with W_d(x) the generating function by half-weight of words ending in A, the
grammar gives W_d(1-2x-x*W_d)=x, so W_d=C(x)-1 with C the Catalan generating function. "Exactly two new delta per
deficit" also needs (a) the parity/bound statement, (b) monotonicity (prefixing C(A), with Phi(A)-2=0 and
intermediate value 1, maps open words of deficit eps into deficit eps+4), (c) an induction realizing every
same-parity value in [2-r, r] minus {0,1,2}; (b),(c) are sketched here, not written out. The table columns
P2/F1/AB2 are closures under DH (P2 needs DH only for the prefix w_i; A-SOURCE, i=1, is unconditional).

| eps | words | A-initial | P2 (incl. A-SOURCE) | F1 (delta=1) | AB2 (delta=2) | open | open delta values (count) | new delta |
|---|---|---|---|---|---|---|---|---|
| 3 | 1 | 1 | 0 | 1 | 0 | 0 | - | - |
| 5 | 2 | 1 | 1 | 0 | 1 | 0 | - | - |
| 7 | 5 | 2 | 2 | 1 | 0 | 2 | -1(1), 3(1) | -1, 3 |
| 9 | 14 | 5 | 8 | 0 | 4 | 2 | -2(1), 4(1) | -2, 4 |
| 11 | 42 | 14 | 20 | 5 | 0 | 17 | -3(1), -1(7), 3(8), 5(1) | -3, 5 |
| 13 | 132 | 42 | 78 | 0 | 27 | 27 | -4(1), -2(12), 4(13), 6(1) | -4, 6 |
| 15 | 429 | 132 | 216 | 40 | 0 | 173 | -5..7 odd | -5, 7 |

eps=9 b/c-first words: BAAA AB2; BABA P2; BBAA open G_-2; BBBA open G_4; BC(A)A AB2; C(A)AA P2; C(A)BA AB2;
C(AA)A AB2; C(BA)A P2. (Full eps=11 list in defect_checks.json.)

[A, sketch: (b),(c)] Structural facts: delta = Phi-1 has fixed parity per deficit (induction on weight: Phi(w) = 1+W(w)/2 mod 2), so even- and
odd-delta deficits alternate; B^(r-1)A gives delta=r and, for r>=3, B^(r-2)AA gives delta=-(r-2), neither has an intermediate 2 (for r=2, AA has
intermediate value 2 and is a P2 case),
so **every integer delta outside {0,1,2} is an open target at some deficit, two new values per deficit**, and
-(eps-3)/2 <= delta <= (eps-1)/2 always. The number of open words grows (17 at eps=11, 173 at eps=15), but the
number of distinct reference families grows only linearly and they are one family G_delta(m).

**One-step collapse [A, from SHIFT, under DH at that step].** The first return of any reference state of defect delta with parameter q:
* a  -> H_{3-delta}(q') where H_e(m) := (6k_m+6-2e, 6k_m+6-e) (pure a-output of a shifted state; needs
  v2(6k+2delta)<q-1 and z>0); closed (by AB/F) if delta in {1,2}, otherwise not closed by these tools;
* b  -> defect delta-1: closed (by AB, F or RB) if delta in {2,3} (delta=3 is PROOF_DURATION_BRANCHES §1, valid for
  any Theta=x+3), otherwise not closed by these tools;
* c(w) -> defect delta+Phi(w)-2: closed if Phi(w) in {3-delta, 4-delta}, otherwise not closed by these tools.
Thus PLUS b closed, PLUS a -> H_0 = Z(q) (as accepted), MINUS b -> defect -2 etc. All open families, from all
deficits and from outer b entries (§6), live in the single class "shifted real chain with small shift, defect not in
{1,2}". Closing this class at all scales is the statement "S1 for shifted copies", which PROOF_EXT §5 already named
as the open core. **Assessment [C]: the deficit-by-deficit route cannot converge as casework; it converges only if a
uniform theorem for G_delta/H_delta (equivalently, no first non-descent in a shifted copy) is proved, which is the
original difficulty of EXT in another coordinate system.**

## 5. Canonical data [B]

`verify_defect.py 8192 20000` (calendar cutoff 8192; all odd c and b crossings n<20000, plus for one actual fire of
each parameter 5..8192 its b crossing and all its c crossings):
* c sources: 2796 history A (F1), 131 AA (P2/A-SOURCE), 131 BA (AB2), 1 C(A)A (F1; the known R=6133 source).
  **No history of deficit >= 9, and no BAA/BBA, is realized by any source parameter <= 8192.** (Kernel types up to 8192
  contain at most three returns; 'caa' occurs once.) For every instance: eps = W+1, real defect = Phi mod 2^(omega+1),
  agreement with G_delta(p) to precision >= p-1, sigma_0 >= p, identical tails, reference record < p-1.
* Deficit >= 9 words can therefore only be tested algebraically (SHIFT, 190,200 cases) or via the family scans.
* Family scans, all 302,878 odd-a m<10^6, ceiling m-1: G_delta for delta in [-7,9]\{0,1,2} and H_delta for
  delta in [-6,9]\{1,2}: all end with record < m-1 except (i) m=5, delta=-3 (G) / delta=-2 (H): z=16, j=4=m-1 —
  exactly the predicted DH failure d=5 mod 8 at (j,k)=(5,1) (the walk then stops at j=4 since X(3) is even, but the
  reduction gives no strict margin); (ii) z<=0 at m in {5,8} for delta>=5 (z=6k+4-2delta<=0: a degenerate reference outside HP's positive cone, recorded with the DH failures; e.g. also
  6k+2d=0 at (j,k)=(12,4), d=-12). Longest words: G_-2 (17,5,6,1), H_-2 (17,5,6,1), G_4 (12,5,2); minimum margins 1-9. Finite only.

## 6. Item 1: outer type-b entries (Theorem OB) [A, under DH for nested c histories and DH_out]

DH_out (added after review): at the outer shifted A-step of step 4, v2(6k+2(d-1)) < m-1. This is not covered by DH
for nested c histories and can fail (e.g. m=5, k=1, d = 6 mod 8).

Let X(J-1) be odd type b, F the fire at pointer J-2, parameter omega>=5 (omega >= K' at a least counterexample, else
Theorem S), E_F its real epoch with return types l_1 l_2 ..., chain-1 state V(F,-1)=(x_F,x_F) (ENTRY, defect 0).

1. Through b/c returns S(J) copies E_F exactly (x-maps of b/c do not read Theta; Theta keeps the offset -1). The
   records j+Gamma strictly decrease there (omega(n) <= n-eps-1). So EXT(omega) — the tie-freeness of E_F — transfers
   verbatim to this stretch.
2. If E_F has no odd a-return, S(J) ends with E_F: tie-free.
3. At E_F's first a-return (parameter m, half-time k, automaton value d of E_F before it, d = 1-#B+sum(Phi(w)-2)),
   the -1 Theta offset becomes an x offset -2: outer x = x_{C'}-2. If j(C') >= 2, the outer has j=1 and ends:
   tie-free.
4. **Residual:** j(C')=1, i.e. E_F ENDS at its first a-step (v2(6k+2d)=1). Then the outer state agrees to precision
   m-1 with H_delta(m), delta=4-d, at parameter j_out=1+v2(3*2^(m-2)u+3k+d-1) (exactly: x_out=3*2^(m-1)u+2(3k+d-1)); under DH_out,
   v2(3k+d-1)<m-2, so j_out=1+v2(3k+d-1)<m-1 (without DH_out this fails: (m,k,d,u)=(5,1,6,1) satisfies DH,
   has j(C')=1, but j_out=6>=m-1), with coefficient margin > m-1 (S1 of E_F's chain).
   Closed if d in {2,3} (delta in {2,1}). Otherwise open; there is no further real chain of E_F to shadow — this is
   exactly where the transfer breaks: EXT(omega) carries no information beyond E_F's last chain, and the shifted
   state is non-real (defect 4-d not in {1,2}).
   The dominant case t=0 (E_F's first return is A, k even, d=1) gives H_3(m)=(6k_m, 6k_m+3). Its b-branch is closed by
   PROOF_DURATION_BRANCHES §1 (any Theta=x+3 state), its a-branch goes to H_0 = Z(q) (same as PLUS a), its c-branch is
   open. So outer b at t=0 reduces to the same CLASS of remainder as PLUS (c-branch of a defect-3 state, Z-type a-branch),
with different instances (H_3 vs G_3 = PLUS). A future PLUS c proof covers H_3 only if it is uniform for all
Theta=x+3 states with ceiling > q (as PROOF_DURATION_BRANCHES §1 is).
Proof: RB + SHIFT + LOW + HP as in §3. Data [B] (same run): odd b crossings with omega<5: 5498 (end); exact copy to
end: 5817; die at first a-step: 1185; climb: 1743, all matching H_delta(m) to precision >= m-1 with identical tails
(1628 with delta=3, d=1; 115 with delta=4, d=0). All tails end within the strict margin.

## 7. Item 2 (only noted)

Z(q)=H_0. From §4 its branches: a -> H_3 (defect 3 again; under DH at that step), b -> defect -1 (MINUS-like V-state),
c(w) -> Phi(w)-2, closed if Phi(w) in {3,4}, otherwise not closed by these tools. No new all-scale closure was obtained. Scans: H_0 ends for all m<10^6 (min margin 2).

## 8. What is proved / not proved

Proved here [A, unreviewed, under the stated hypotheses incl. DH]: SHIFT; LOW; DR (uniform reduction of every c
history to G_{Phi-1}, closing delta in {0,1,2}); P2 (A-SOURCE at any intermediate phase-two chain); combinatorics of §4 ("two new delta per deficit" only sketched: (b),(c));
OB (under DH and DH_out; outer b reduces to H_{4-d} only when E_F ends at its first a-step). These subsume C3, C5-BA, AA, CA, A-SOURCE and the
BAA/BBA normal forms as special cases (their hand-checked DH conditions are SIZE/SMALL).
Not proved: any G_delta/H_delta family closure for delta outside the closed sets; DH at all scales; EXT. The accepted
horizon K_clock is unchanged.
