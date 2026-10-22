# Congruence-target fires: CAL-C fails, and R1 and H3 fail somewhere in [K_clock, T4)

Adversary note (Claude) from the work_c3_drift review, 2026-10-22. Confirmed by two blind targeted
audits (agy gemini-3.8-flash-high); two small corrections applied. See reviews/c3_drift_review_record.md.
Verifier: `python -B work_c3_drift/verify_congruence_target.py`, which writes
`congruence_target_checks.json` beside itself (about 27 s, PASS).
Tags: [A] proved here from the imports listed; [A-imp] an accepted import; [B] a finite exact
check; [C] a conjecture.

These are shallow constructions with one or two layers of exponentiation. They are different
from the three-b BBBAA construction of work_c3_drift/UNBOUNDED_C_PARAMETER_IF_EXT.md. That
construction needs four layers above N0 and lands at n+1 >= T4, so it does not affect H3 or H5
for J<T4. The two constructions here need two layers (eps=3) and three layers (eps=5 BA),
so they land below T4.

## 0. Imports and notation

* [A-imp] **EXT below K_clock.** S(J) is tie-free for every J<K_clock, where
  K_clock = floor(2^K'/(64 K'^2)) and K' = 2^(2^(2^499997-3)-2).
  Sources: reviews/global_clock_horizon_closure_review_record.md (VERDICT) and
  CHECKPOINT_1RB1LA_0RC0RD.md, line 8 (K') and line 468 (K_clock).
* [A] **DEF (definedness).** Combining the induction of work_global_egx/PROOF_EGX.md Theorem U(b)
  with EXT(J) for J<K_clock: F is defined, and every epoch completes, through any time S such
  that every level fire at a time s<=S has parameter v2(3s+4)<K_clock. In particular this holds
  for every S with 3S+4<2^K_clock. A level fire at pointer rho has parameter J<rho. Under strict
  records, a fire of parameter J has at most J-1 chains, each with parameter <=J. (PROOF_EGX §5
  gives Gamma_t<=J-2 and Gamma_t>=t.)
* [A-imp] **C1/CLOCK.** tau(n)<=n^2 on the defined prefix, and tau(n)>=(n-1)/2 (PROOF_EXT §4).
* [A-imp] **Lemma K** (work_global_ext/PROOF_EXT.md). For n>=4 with X(n) odd:
  (a) type a <=> there is a level fire at pointer n, with tau(n)=2k_n;
  (b) type b <=> W's chain is the fire at pointer n-1, with omega(n)=v2(3tau(n)+4);
  (c) type c <=> tau(n) is an a-return of the current real epoch.
  Also, X(rho+1) is the type-b copy of the fire at rho (PROOF_SPECTRUM §4, review patch).
* [A-imp] **PROOF_SPECTRUM** (work_g2_obstruction). The time of a fire is 2k and its label is
  L(k)=v2(6k+4). The exact half-time gaps for P=1..15 are
  1,1,2,2,3,3,3,4,4,5,5,6,6,8,7. The targets T_P satisfy L(T_P)=P, and the BARRIER statement holds
  for any gap function M with M(J)<=2^(J-2) (J>=2).
* [A-imp] **PROOF_LOW_DEFICIT §3–4** (accepted).
  - History A at a fire (rho, P, x0=2^P U): the first a-output is the c crossing n=rho+2, with
    eps=3. By RB the first chain of S(rho+3) is (x_C, Theta_C-1), where x_C=(3/2)x0+6k+2,
    Theta_C-1=x0+6k+3, and k=tau(P-1)/2.
  - History BA: y=3tau(P-1)+4=2^p V with p<P-2. The source is n=rho+2 with eps=5.
    The first chain of S(rho+3) is x=(13/8)x0+(3/2)y+6k, Theta=x0+y+2+6k, with k=tau(p-1)/2.
  - Weight grammar: eps=3 <=> history A, and eps=5 <=> history AA or BA.
* [A-imp] work_global_ext PROOF_EXT Theorem RA: if X(J-1) is odd type a and J>=10, then
  j_1=1+v2(3k+1)<=J-2.
* [A-imp] **work_r1r2 / work_deep definitions.** N0=2*10^7 and B=2^(10^7). A chain is *deep* if
  j_t>=N0 and |theta_t|<=B. **R1** = "no c-step at a deep chain keeps the walk deep" (work_deep
  Theorem 3.4). L, Lambda and T_h are as in work_deep Lemma 2.4, which gives Lambda(J)<=h for
  J<T_h, with T_1=2^((N0-3)/2) and T_(h+1)=2^((T_h-3)/2). L is nondecreasing, and
  Lambda(K_clock)=4 (work_deep §2), so T_3<K_clock<T_4. **CAL-C**: there is no n>=N0-1 with X(n)
  odd type c and 2^N0 | 3tau(n)+4+lambda_Y(n)=lambda'_W(n), where omega(n)=v2(lambda'_W(n)).
* **H3(J)** (work_c3_drift/NOTES.md §3): every odd c step reached in the initial deep segment of
  S(J) whose deficit is not 3 has next parameter <N0.

## 1. Congruence-target no-overshoot lemma

Define the gap bound G(P) := exact gap(P) for P<=15, and G(P) := floor(P^3/2) for P>=16.

**Lemma 1.1 (half-time gap) [A].** Let a level fire at half-time h have label P<K_clock, and let
DEF hold through the next fire. Then the next fire's half-time h' satisfies h'-h<=G(P).

*Proof.* For P<=15 this is the certified exact gap. For P>=16, EXT(P) gives at most P-1
chains, each reading X(j-1) with j<=P. Each chain costs 1+tau(j-1)<=1+(P-1)^2 steps by C1, and
there are at most 2 further even steps (PROOF_SPECTRUM §2 accounting). So
2(h'-h) <= (P-1)(1+(P-1)^2)+2 <= P^3. ∎

**Lemma 1.2 (no-overshoot) [A].** Let k*>=1 satisfy:

* BARRIER(k*): G(L(h))<=k*-h for every 1<=h<k*;
* L(h)+1<K_clock for all h<k*, and 3(2k*)+4<2^K_clock.

Then k* is the half-time of a level fire.

*Proof.* Fire half-times form a strictly increasing integer sequence starting at 1. DEF supplies
each next fire while the current half-time is below k*. If h<k* is a fire half-time, then by
Lemma 1.1 and BARRIER the next one is at most h+G(L(h))<=k*. Since the sequence is strictly
increasing, it reaches k* in at most k* steps. ∎

**Theorem CT (congruence targets) [A].** Let M>=16. Each of the following is the half-time of an
actual level fire, provided 2^(M+2)<2^K_clock (automatic for M<K_clock-3):

* (A-class) k*_A(M), the least positive k with 3k+1 ≡ 0 (mod 2^M). Here k*_A(M)<2^M and its
  label is L(k*_A)=1.
* (B-class) k*_B(M)=2^M, with label 2.

*Proof.* Let 1<=h<k*, d=k*-h, P=L(h) and r=P-1=v2(3h+2). Then 3h+2=(3k*+2)-3d.

(A-class) Here 3k*+2=2^M c+1.
- If r=0, then G(1)=1<=d.
- If 1<=r<=M, then 2^r | 1-3d. Since 3d-1>0, this gives 3d-1>=2^r, so d>=(2^r+1)/3.
- If r>M, then 2^M | 3d-1, so d>=(2^M+1)/3. Moreover 3h+2<3*2^M+2<2^(M+2), so P<=M+2.

(B-class) Here 3k*+2 ≡ 2 (mod 2^M).
- If r=0, then d>=1=G(1).
- If r=1, then d must be even, so d>=2>=G(2).
- If 2<=r<=M, then 3d ≡ 2 (mod 2^r), so d>=(2^r+2)/3.
- If r>M, then d>=(2^M+2)/3 and again P<=M+2.

The inequalities needed:
- For 2<=P<=15: ceil((2^(P-1)+1)/3) is 1,2,3,6,11,22,43,86,171,342,683,1366,2731,5462, which is
  >=G(P) termwise; the B-class bound is larger.
- For P>=16: (2^(P-1)+1)/3>=P^3/2 ⇔ 2^P+2>=3P^3. This holds at P=16, and since the cubic grows by
  a factor less than 2 per unit step, it persists.
- For r>M with M>=16: 2(2^M+1)>=3(M+2)^3 holds at M=16 and persists.

So BARRIER(k*) holds. Every label before k* is <=M+2, which is far below K_clock, so Lemma 1.2
applies. ∎

**Small M [B].** For 2<=M<=249 and w=0..3, the canonical calendar (B=512) confirms that the
A-class targets k*_A(M)+w*2^M (992 of 992) and the B-class targets (w+1)*2^M (991 of 992) are
fire half-times. The only miss in the run is B-class M=2, k=12: the previous fire is at 10 with
label 6, whose exact gap is 3 while d=2. An earlier exploratory run also missed k=28=7*4: the
previous fire is at 26 with label 5, gap 3, and d=2. In both cases BARRIER fails, as expected for
M<16. The theorem is only claimed for M>=16 and for the least representative. For M=16..22 the
pure-arithmetic BARRIER is checked directly for both classes [B].

## 2. HIGH 2: an eps=3 source. CAL-C fails, and R1 fails in [K_clock, T4)

**Construction [A].** Fix M>=16, let k*=k*_A(M), and let rho* be the pointer of its fire
(Theorem CT). By Lemma K(a), X(rho*) is odd type a with tau(rho*)=2k*. Put P := rho*+1.

By PROOF_SPECTRUM's barrier with gap function G (G(J)<=2^(J-2) for J>=16), the first fire of
label P occurs at a time <=2T_P<(10/3)2^(P-1). This requires P+4<K_clock. Let rho_P be its
pointer and x0=3tau(rho_P)+4=2^P U.

Its chain 0 has parameter P, theta=1, and reads X(P-1)=X(rho*), which is type a with k*. By RA
and PROOF_LOW_DEFICIT §3 the first a-output is the odd type-c crossing n := rho_P+2, with
eps(n)=3 and

    omega(n) = q := v2(x_C) = v2(6k*+2) = 1+v2(3k*+1) >= M+1,   q <= P-2.

[A-imp, used exactly as in the accepted C3 proof; [B] for 16 small realisations with q up to 9,
including the P=195 case with q=9.]

**CAL-C fails [A].** Take M=N0-1. Then 2^N0 | lambda'_W(n) and n>=N0-1. All the times involved are
below 2^(P+2), with P<=2^(M+2)+2<K'-4, so the construction lies inside the accepted
K'-spectrum range (PROOF_EGX, alternative route). Therefore **CAL-C is false relative to
accepted imports**, with no global EXT hypothesis needed. This is stronger than
UNBOUNDED_C_PARAMETER_IF_EXT §4.

**Size of n [A].** C1 and tau>=(n-1)/2 give rho* in [sqrt(2k*), 4k*+1]. Since 3k*+1>=2^M,
P>=2^((M-1)/2).

The first label-P fire has 3tau(rho_P)+4>=2^P and time <2^(P+2). Hence

    2^(P/2-1) <= n < 2^(P+3)+3,   i.e.  log2 n in [2^((M-3)/2)-1, 2^(M+2)+6].

(Corrected in review: rho<=2s+1 from tau>=(rho-1)/2 costs one more factor 2.)

* M=N0-1: log2 n lies in roughly [2^(10^7-2), 2^(N0+1)]. Hence T_2<n+1<T_3<K_clock, and
  Lambda(n+1)=3. EXT(n+1) is already known here, so only CAL-C and R1-as-a-universal-statement
  are affected.
* M=M_3 := 2*ceil(log2(K'+1))+3: log2 n>=K'+... >= log2 K_clock+1, so n+1>K_clock.
  Also log2 n<=2^(M+2)+6<=2^9 (K'+1)^2+5 is far below (T_3-3)/2=log2 T_4, because
  log2(K'^2)≈2^(2^499997-2) is much less than log2 T_3≈2^(2^(10^7-5/2)-5/2).
  So **K_clock < n+1 < T_4**, and since L is monotone, Lambda(n+1)=4.
  We also have P<=2^(M+2)+2<K_clock-4, so DEF and Lemma 1.2 apply.

**R1(n+1) fails [A].** Let J=n+1=rho_P+3.
1. S(J) is defined, by DEF: tau(J-1)<2^(P+2), with all labels <=P+3<K_clock.
2. Chain 0 has j_0=J>=N0 and theta_0=1, so it is deep. It reads X(n), which is odd type c.
3. By RB, chain 1 is (x_C, Theta_C-1). So j_1=q>=M+1>=N0 and
   theta_1 ≡ Theta_C-1-x_C = 1-x0/2 ≡ 1 (mod 2^(P-1)). Since q<=P-2, the symmetric representative
   is exactly 1, and |theta_1|<=B.
4. So chain 1 is deep, a c-step has kept the walk deep, and **R1(J) is false**. The range
   hypothesis 6Lambda(J)+4=28<=B of work_deep Theorem 3.4 holds.
5. Check of r1r2 Lemma 4.3 (restricted converse):
   - n>=N0-1;
   - X(n) is odd type c;
   - 2^N0 | lambda'_W(n);
   - the drift condition: the least residue of 3tau(n)+4 mod 2^q is 1 ([A]: 3tau+4 = x0+(6k*+2)+1 and q<P-1;
     also checked [B] at all realisations).
   All of its hypotheses hold.

Consequently, the accepted reduction "J<T4: EXT(J) <= R1 and R2_c" still holds as an
implication, but R1 cannot be established for all J in [K_clock,T4). This conclusion is relative
to accepted EXT(<K_clock) and the proofs above.

## 3. HIGH 1: an eps=5 BA source. H3 fails in [K_clock, T4)

**Construction [A].** Fix M>=16 and k*=2^M (Theorem CT, B-class), with pointer rho* and
p := rho*+1. By Lemma K(a), X(p-1) is odd type a with k=k*.
- Take the first fire of label p (PROOF_SPECTRUM barrier), with pointer rho_p. By Lemma K(b),
  X(rho_p+1) is type b with omega=p ([B]: 115 checks).
- Put P := rho_p+2>=p+3, and take the first fire of label P, with pointer rho_P and x0=2^P U.
- Its chain 0 has parameter P and theta=1, and reads X(P-1), which is type b. This gives chain p
  with y=3tau(P-1)+4=2^p V, so p<P-2.
- Chain p reads X(p-1) (type a, k*).

The history is BA, so by PROOF_LOW_DEFICIT §4 and the weight grammar, n := rho_P+2 is an odd
type-c crossing with eps(n)=5 and

    omega(n) = q := v2(6k*) = M+1.

Here q<p-1 because p-1=rho*>=2^((M+1)/2)>M+2. [A-imp, plus [B] on all 4 canonical BA sources
with P<=256. A full end-to-end realisation is not feasible: already P≈1.5e6 at M=3.]

**Phase [A].** By RB, at J=n+1 chain 1 has x=(13/8)x0+(3/2)y+6k* and
Theta-x = 2-(5/8)x0-y/2 ≡ 2 (mod 2^(p-1)). The terms have valuations P-3>=p and p-1. So
theta_1=2 exactly, and j_1=M+1.

**Sizes [A].** We have p in [2^((M+1)/2), 2^(M+2)+2], P in [2^((p-2)/2), 2^(p+2)+2), and
n in [2^((P-2)/2), 2^(P+2)+2). That is three nested exponentials of M, i.e. three layers.

Choose M_5 := 2*ceil(log2(2 log2(K'+1)+4)), so that p>=2 log2(K'+1)+4. Then
log2 n>=P/2-1>=2^((p-4)/2)-1>=K', so n+1>K_clock. Also M_5≈2^(499998), which is >=N0.

For the upper bound: p<=2^(M_5+2)+2=O((log2 K')^2), so log2 log2 P<=p+3. This is far below
log2 log2 T_4≈T_2/2, so n+1<T_4 and Lambda(n+1)=4. Moreover log2 P<=p+3 is much less than K',
so P<K_clock-4, and DEF, Lemma 1.2 and PROOF_SPECTRUM all apply.

**H3(n+1) fails [A].** Chain 0 of S(n+1) is deep (j=J>=N0, theta=1). It reads an odd c crossing
with eps=5≠3, and its next parameter is M+1>=N0. This contradicts H3(n+1).
- Chain 1 is also deep (theta_1=2), so R1(n+1) fails here as well.
- However, n+1 satisfies the hypotheses of C5_EXTENSION's H5 at chain 0 (eps=5 is allowed).

Hence "for all J<T4: H3(J)" is false relative to accepted imports, and NOTES.md §3 cannot serve
as a uniform route on [K_clock,T4). C5_EXTENSION's H5 is not touched by this construction.

**Why BBBAA is different (layer count) [A].** In the BBBAA construction m=v2(9k+10) needs
k≈2^m. Then:
- p≈pointer(k) is one layer;
- p1=rho(p)+2, p2 and p3 are three more layers;
- n≈rho(p3) is the next layer.

With m>=N0, the bounds rho(J)>=2^((J-2)/2) give p>T_1, p1>T_2, p2>T_3, and n>T_4. So the
blind auditors are right that BBBAA does not affect J<T4. The constructions here use 2 layers
(eps=3) and 3 layers (eps=5); every additional source return before the final a-output costs
one more layer.

## 4. What remains true, and the corrected frontier

* Unaffected as implications [A-imp]:
  - EXT(J) <= R1 and R2_c for J<T4 (work_r1r2 Cor 2.6);
  - J<T4 and H3 and C_rest => EXT (NOTES §3);
  - J<T4 and H5 and C7 => EXT (C5_EXTENSION §4).
  Their algebra was rechecked in the main review.
* Refuted as uniform hypotheses on [K_clock,T4), relative to accepted imports [A]:
  - R1, CAL-C (CAL-C is refuted outright, at n<K_clock), and H3.
  Under global EXT, the BBBAA family also kills every fixed parameter cap above T4.
* **Layer conjecture [C].** If X(n) is odd type c with eps(n)>=7 and omega(n)>=N0, then n>=T_4-1.

  Heuristic: eps>=7 means at least three a/b returns before the final a-output, or at least
  one c return plus a/b returns. Each a-output with v2>=N0-1 at small phase needs k>=2^(N0-1)/3,
  and each b copy or ancestor fire costs one exponential. The c3 and c-BA restarts likewise cost
  two or three layers. The danger is a c return with a non-integer rational shift (for example
  BBBAA's +4/3), which makes theta of size about 2^omega and could shortcut the a-layer. The
  conjecture needs those c returns themselves to be deep, which recursively costs layers.
  If the conjecture holds, then H5(J) holds automatically for every J<T4, and C5_EXTENSION reduces
  J<T4 to C7 alone.
* **Phase-sensitive replacement beyond T4 [C].** A parameter cap is the wrong shape. Classify each
  deep c-step by its source shift s(n) := -1-lambda_Y(n) mod 2^(omega+1):
  - integer shifts {0,-1,+1} (eps=3, AA, BA) enter the drift maps;
  - bounded-height non-integer shifts (BBBAA: +4/3, height 2) leave the |theta|<=B window and
    must be routed to the rational-phase regime (RATIONAL_MODE / RES-type entry) with a height
    budget.

## 5. Status of each step

| Step | Status |
|---|---|
| Lemma 1.1, Lemma 1.2, Theorem CT (M>=16) | [A] |
| Small M, M=2 misses | [B] |
| eps=3 and BA crossing identification | [A-imp] (accepted C3 / C5-BA formulas used forward) + [B] |
| Size bounds, the [K_clock,T4) placement, R1/H3/CAL-C failure | [A] relative to §0 |
| Layer conjecture and replacement condition | [C] |

**Review priority.** (i) The forward use of PROOF_LOW_DEFICIT §3–4: an epoch with first returns
A (resp. BA) has its first a-output as the odd c crossing rho+2 with the stated omega. The
accepted text proves the formulas assuming that crossing, and Lemma K(c) gives the
identification. (ii) DEF as an extraction from Theorem U(b) with EXT(<K_clock) in place of global
EXT.
