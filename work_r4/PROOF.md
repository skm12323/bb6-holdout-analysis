# R4: non-halting analysis of `1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE`

Tags: **[Class-A]** proved for all parameters (by hand, or by an exact symbolic computation whose
every branch is checked); **[Class-B]** finite exhaustive computation; **[Class-C]** conjecture/empirical.
Imported from R1 (`work_r1/RULES.md`, re-checked here where stated): top map T on lists
L=(A,b,c,S) (missing entries 0):
- A even: T(L) = (A+b+c+3, S).
- A odd: m := b+(A-3)/2, stack := (c+(A+1)/2, S); while m odd and m>=3: push (m+3)/2, m := (m-3)/2;
  if m=1 HALT; else T(L) = (m+4, stack).
- Sum lemma: sum(T(L)) = sum(L)+3, so sum(L_n)=3n+3 with L_0=(3). [Class-A, R1]
- Halting lemma: T halts on L iff A odd and A+2b+3 is a power of 2. [Class-A, R1; re-derivation:
  m+3 is halved at each chain step, the chain stops at the first odd m+3 or at m=1, i.e. m+3=4.]
`verify_r4.py` check0 re-confirms T against direct iteration of R1's macro rules R1-R5 for
3000 top steps [Class-B]; correctness of R1-R5 themselves is R1's [Class-A] claim (under audit).

## 1. Singletons [Class-A]
If L_n has one entry then L_n=(3n+3) (sum lemma).
- **S1.** n odd: A=3n+3 even, L_{n+1}=(3n+6) is again a singleton.
- **S2.** A singleton never halts: A+2b+3 = 3(n+2) is divisible by 3.
- **S3 (excursion entry).** n even. Write n+2 = 2^v w, w odd, v>=1. Then
  L_{n+1} = E(w,v) := (3w+1, 3w, 6w, ..., 3w*2^(v-2), 3w*2^(v-1) - 1)
  (for v=1: (3w+1, 3w-1)).
  *Proof.* m=(A-3)/2=3n/2, m+3=3(n+2)/2=3w*2^(v-1); stack starts (c+(A+1)/2)=((3n+4)/2)=(3w*2^(v-1)-1).
  At chain step i (i=0,1,...) m_i+3 = 3w*2^(v-1-i), odd iff i=v-1, so exactly v-1 pushes occur,
  the i-th pushing 3w*2^(v-2-i) (so the final stack front is 3w); final m = 3w-3, which is even
  and !=1. Hence T(L)=(3w+1, 3w, ..., 3w*2^(v-2), 3w*2^(v-1)-1). QED

## 2. Excursion lemma, for each fixed v [Class-A for v <= 2000]
**Lemma E(v).** For every odd w, iterating T from E(w,v) never halts and reaches a singleton
after exactly ell(v) steps, ell(v) independent of w, the singleton being (3w*2^v + 3*ell(v)).

*Proof method (check1 of verify_r4.py, exact).* Put w=2u+1, u>=0 a symbol. Every list entry is an
integer affine form a*u+b. T is executed on such lists, and each decision T needs (parity of A,
parity of m, m>=3, exactness of every halving) is required to have the same outcome for **all**
u>=0: parity of a*u+b is decided only if a is even; halving only if a,b both even; m>=3 only if
(a>=0,b>=3) [true for all u] or (a=0,b<3) [false for all u]; otherwise the run aborts. A HALT
branch (m odd and <3, i.e. m=1) aborts with failure. The run for each v=1..2000 completes with no
abort, no HALT, all entries having nonnegative coefficients, and final singleton exactly
(6*2^v u + 3*2^v + 3 ell(v)) = (3w 2^v + 3 ell(v)). Since every decision was uniform in u, the
symbolic run is literally the run for every odd w. ell(1..20) = 1,1,2,2,5,4,4,6,7,8,8,10,10,15,12,12,14,15,15,16.

## 3. Theorem [Class-A, conditional on R1's rules]
**The top-map orbit from (3) does not halt during top steps n < 2^2001 - 2** (hence the TM does not
halt within the corresponding (astronomically many, ~1.35 n^3) TM steps).
*Proof.* Induction over singleton times. L_0=(3) is a singleton. At a singleton time n: no halt
(S2); if n odd go to n+1 (S1); if n even, L_{n+1}=E(w,v) with n+2=2^v w (S3), and if v<=2000,
Lemma E(v) gives no halt and a singleton at time n+1+ell(v). The first singleton time n with
v2(n+2) > 2000 satisfies n+2 >= 2^2001. QED.
More generally: **if Lemma E(v) holds for every v>=1, the machine never halts** (same induction).
check2 [Class-B] confirms this decomposition against the concrete orbit for all n < 2^20.

## 4. What remains: a uniform-in-v proof of Lemma E(v) [open, tractable]
The remaining statement is **not** Collatz-like: the orbit of E(w,v) is already proved independent
of w, and its decisions are 2-adically "insulated". Structure observed (Class-C, check3: all
37219 odd multi-element steps for n<2^20 fit it): the list is (g+d, g, 2g, ..., 2^(r-1) g, tail)
with a small offset d and a run base g whose 2-adic valuation grows. One-step facts [Class-A, by
direct substitution in T, needs c=2g present]:
- **R-even.** d even: T(g+d, g, 2g, 4g, R) = (4g+d+3, 4g, R) -- offset d->d+3, base g->4g, run shortened by 2.
- **R-odd.** d odd, d+3=2^s e (e odd), and v2(g) > s: X=A+2b+3 = 3g+d+3 = 2^s(3g/2^s + e) with
  3g/2^s even >=2, so the odd part is >=3: **no halt**. The result is a nested run
  (o+1, o, 2o, ..., 2^(s-2) o, J, 4g, 8g, ...) with o=(3g+d+3)/2^s odd, J=(5g+d+1)/2,
  i.e. a fresh offset-1 sub-process on a run of length s-1 (s <= log2(d+3)).
  The same bound covers the run-end shapes (g+d, g, 2g-1) (same X) and (g+d, g-1) (X=3g+d+1,
  safe when v2(g) > v2(d+1)).
Thus a uniform proof needs a closed description of how a sub-process of run length s-1 followed
by J and the outer run re-merges into (4^k g + d', 4^k g, ...) and of the offset sequence d (growing
~3 per step, so v2(d+3)=O(log v) while v2(g) grows ~2 per step). This is a finite-depth recursion
(depth <= log of the offset) and should yield to a two-level symbolic prover (run length and
base as symbols, offsets concrete up to a bound plus an asymptotic offset argument), but it is
**not done here**: Lemma E(v) for all v is [Class-C]. Note the margin v2(g)-v2(d+3) is sometimes 0
in the data (check3), so the clean sufficient condition above does not cover every step on its
own; those steps are nonetheless covered for v<=2000 by Section 2.
