# R5: toward Lemma E(v) for all v -- generalized excursion lemma F(s) and its recursion

TM `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`. Base: R1 top map T (work_r1/RULES.md, frozen) and
R4 (work_r4/PROOF.md: singletons, excursion entry E(w,v), Lemma E(v) for v<=2000). Tags:
**[Class-A]** proved for all stated parameters (by hand, or by an exact symbolic run in which every
decision is uniform in all symbols); **[Class-B]** finite exhaustive computation; **[Class-C]** conjecture.
Symbolic method (as R4, extended to several symbols, all ranging over integers >=0): entries are
integer affine forms; parity is decided only if every symbol coefficient is even; halving only if
all coefficients and the constant are even; `m>=3` only if (all coefficients >=0 and constant >=3)
[true for all values] or (all coefficients 0) [concrete]; anything else aborts. A HALT branch
(final chain value m odd, i.e. m=1) aborts with failure. A completed run is therefore literally the
run of T for every value of the symbols.

## 1. Lemma F(s) (generalized excursion) [Class-A for 1<=s<=1000; verify_r5.py check1, default s<=300]
For s>=1, odd o>=1, integers K>=0 and Z_1,Z_2,...>=0, put
  Phi_s(o;K;Z) = (o+1, o, 2o, ..., 2^(s-2) o, 2^(s-1) o - 1 + K, Z_1, Z_2, ...)
(for s=1: (o+1, o-1+K, Z_1, ...)). **F(s):** there are ell(s)>=1, a(s) in {0,..,3}, p(s)>=0
(depending on s only) such that whenever 2^p(s) divides K and every Z_i, T never halts on the
orbit of Phi_s and after exactly ell(s) steps reaches
  (2^s o + 3 ell(s) + K + Z_1 + ... + Z_a(s),  Z_(a(s)+1), Z_(a(s)+2), ...),
the entries Z_(a+1),... never having been read.
*Proof (each s).* Symbols o=2u+1, K=2^p k, Z_i=2^p z_i (5 Z's), u,k,z_i>=0. Run T symbolically until
the list is (X, Z_(a+1),...,Z_5); check X equals the formula, a<=3 (so Z_(a+1),Z_(a+2) remain;
entries at list positions >=3 are never read by T, and any read entry is consumed, so an
unchanged untouched suffix was never read -- hence the result holds for any length of Z).
p(s) is the least p for which all decisions are uniform. Result for s<=1000: always succeeds,
max a=3, max p=11; p(s)>0 only for sparse s (5:3, 14:5, 51:7, ...). ell(s) coincides with R4's
ell(v) (check2, v<=300). **F(v) with K=0, Z empty is exactly R4's Lemma E(v)** (o=3w; the margin
condition is vacuous), so Lemma E(v) for all v <=> F(v) for all v (with K=0); F is the statement
that closes under the recursion below.

## 2. Canonical states and the reduction lemma [Class-A, by hand]
A **canonical state** is Gamma = (H+d, H, 2H, ..., 2^(r-1) H, Y_1, Y_2, ...), with v2(H)=j>=1.
**R-even** (d even, r>=2): A=H+d even, T(Gamma) = (4H+d+3, 4H, 8H, ..., Y): canonical, H->4H,
d->d+3, r->r-2. (Direct from the A-even rule.)
**Lemma R** (d odd, s':=v2(d+3), j>s', r>=2). One T step maps Gamma to Phi_s'(o'; H; Z') with
o'=(3H+d+3)/2^s' (odd), Z'=(4H, 8H, ..., 2^(r-1)H, Y_1, ...), and does not halt.
*Proof.* A=H+d is odd. m=b+(A-3)/2=(3H+d-3)/2, so q:=m+3=(3H+d+3)/2. In the chain, "m odd" <=> q
even, each iteration pushes q/2 and replaces q by q/2. Since j>s', v2(3H+d+3)=s', so q_i=
(3H+d+3)/2^(i+1) is even for i<s'-1 and odd at i=s'-1; and every q_i >= 3H/2^s' >= 6, so m=q-3>=3
during the loop and the HALT case m=1 (q=4) never occurs. The loop ends with m=o'-3, even, >=0.
Pushes are q_0/2,...,q_(s'-2)/2, so the stack front is o', 2o', ..., 2^(s'-2) o', then
J=c+(A+1)/2=2H+(H+d+1)/2=(5H+d+1)/2 = 2^(s'-1) o' - 1 + H, then the rest (4H,...). Head m+4=o'+1. QED
**Corollary M(s')** [Class-A for s'<=1000, from Lemma R + F(s')]: if moreover j>=p(s') and
r >= a(s')+3, then Gamma reaches after ell(s')+1 steps, without halting, the canonical state
(H''+d'', H'', 2H'', ...) with H''=2^(a(s')+2) H, d''=d+3(ell(s')+1), r''=r-2-a(s').
(Absorbed Z'_i are 4H,...,2^(a+1)H, all divisible by 2^j; head = 3H+d+3+3ell+H+4H(2^a-1).)
**Observed [Class-B, check3]:** in every E(v), v<=600, all 70565 canonical-to-canonical transitions
after t=0 are exactly R-even or M(s') with (dt,dj)=(ell(s')+1, 2+a(s')), and at canonical time t
d=3t+1, H=3w 2^j.

## 3. Structure of the induction and the remaining gap
Inside the orbit of Phi_s (and so of E(w,v)) the evolution is: (i) an **initial phase** (j small,
before j>=max(s'+1,p(s'))), (ii) a **middle phase** of R-even / M(s') macro-steps -- valid by
Section 2, using F(s') only for s'=v2(3t+4) <= log2(3 ell(s)+4), i.e. s' << s, and (iii) an
**end phase**, once r < a(s')+3, where the run meets the perturbed entry 2^r H - 1 + K and then Z.
Hence F(s) for all s would follow by strong induction on s from:
- **(G1) margin bound**: p(s') <= j at every middle macro-step. Data: p(s)<=11 for s<=1000 (roughly
  log2 s + small), while j grows ~2 per macro-step and s' ~ log t. [Class-C beyond s<=1000]
- **(G2) end-phase lemma**: from canonical (H+d,H,...,2^(r-1)H, 2^r H-1+K, Z...) with r<=a+2
  (all d) the orbit reaches (X, Z_(a+1),...) without halting. Cases d even with r in {0,1} are
  one-step [Class-A by hand: r=1 -> (4H+d+2+K, Z_1,...); r=0 -> (2H+d+2+K+Z_1, Z_2,...)]. The case
  d odd triggers Lemma R with a nested Phi_s' whose Z'-list contains the **odd** entry 2^r H-1+K
  inside its first a(s')+1 positions; F(s') is NOT valid for odd Z (symbolic runs abort for the
  s with p(s)>0, e.g. s=5,14,51), so this case needs a finer statement of F tracking how the last
  steps of Phi_s' read Z_1 as b in an odd step. This is **not done**.
- (G3) the initial phase is the same symbolic computation for all large s (run length is never
  reached), so it is a finite check; not separately formalized here.
**Status.** Lemma E(v) for all v remains **[Class-C]**. What is new and proved: F(s) for s<=1000
[Class-A], Lemma R / M(s') [Class-A], hence every middle macro-step of every excursion with
v2(3t+4)<=1000 and j>=p is rigorously justified; the excursion is a recursion of log-depth
F-calls. The gap is not Collatz-like: every decision is 2-adically insulated (needed margin
p(s)=O(log s) observed vs available j ~ s); it is a finite-type but unfinished case analysis
(G1, G2). The Theorem of R4 (no halt for top steps < 2^2001-2) is unchanged.

## 4. Final attempt on G1-G3 (R5, second pass)
- **F'(s) [Class-A for s<=300, check4]:** F(s)'s conclusion form (no halt, result (2^s o+3ell'+K+Z_1+..+Z_a', Z_(a'+1),..)) holds when
  Z_1 == -1 (mod 2^p) (odd for p>=1) instead of Z_1 == 0, for some p'(s)<=9; ell',a' equal ell,a except s=14,87,158,231 where ell'=ell+1 (a'=a=3).
  This covers the end-phase configuration where the perturbed entry 2^r H - 1 + K sits at Z'_1
  (case r = 2 of Lemma R). It does **not** cover the odd entry sitting at Z'_2..Z'_(a+1) (r = 3..a+4
  with a(s')>=1), nor the cascade in which the nested Phi_s' absorbs that entry and the outer
  process continues with an odd perturbation in its head; those need further variants F'_i.
- **G1:** no proof of a bound p(s) <= f(s) for all s was found. p(s) is defined as an outcome of
  the computation; bounding it requires knowing, for all s, which steps of F(s) read K/Z as b in an
  odd step -- i.e. the same end-phase structure as G2. Residual, [Class-C]: p(s) <= log2(s)+4.
- **G3:** not formalized beyond observation that the first steps of Phi_s are s-independent once
  s exceeds the depth read (EEOEOEEE... prefix in all runs).
**Exact residual statement (open here):** for every s > 1000, F(s) holds with p(s) <= j-available,
equivalently: the end phase of Phi_s (from the last canonical state with r < a(s')+3, with the
perturbed entry 2^r H - 1 + K and Z following) reaches (X, Z_(a+1),...) without halting. Finite
checks (s<=1000; F' s<=300) cannot give this for all s; a closed description of the end phase of
F(s) in terms of F(s''), s''<s, is required and was not obtained. Lemma E(v) for all v: [Class-C].
Non-halting: [Class-A] only up to top step 2^2001-2 (R4).
