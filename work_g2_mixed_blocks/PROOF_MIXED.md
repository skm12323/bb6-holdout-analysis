# Positive return identity for arbitrary b/c corridors and odd a endpoints

2026-10-15. New continuation; not independently reviewed. This extends
the two-pure-b-block calculation to general return types, but does not
prove a bound on core visits or global non-halting.

## 1. A block that covers general nonterminal continuations

Start immediately after an odd a-return. Write its output chain value
as X and phase as Theta. If H was the preceding chain value and k was
half its earlier call time, the exact a-return formulas give

    Theta=X/2+H/4+3+3k.                            (STATE)

Now follow any number h>=0 of odd b/c returns. If an even return occurs,
the epoch ends. Otherwise stop at the next odd a-return, whose input
parameter is p>=5 and half-call time is l=tau(p-1)/2.

For this b/c corridor put

    d=sum [1+tau(j-1)], G=sum [1+epsilon(j-1)],
    x_end=alpha X+B, Theta_end=Theta+3d.

Here alpha is the product of the positive b/c coefficient ratios.
The empty corridor has alpha=1,B=d=G=0. The exact updates imply

    0<alpha<=1, v2(alpha)=-G, 0<=B<=6d-h.           (BC)

Indeed each coefficient ratio is <1, and its added lambda is at most
6tau+5=6(1+tau)-1. This proves the bound by iteration. The crossing mass
formulas supplying these inequalities are those of `work_m` and `work_el`.

The odd a endpoint gives

    Y=(1-alpha/2)X+H/2+6+6k+6l+6d-B/2;
    Theta_new=Y/2+(alpha X+B)/4+3+3l.              (BLOCK)

Thus STATE is preserved with H_new=alpha X+B and k_new=l, for every
safe such return. No fixed phase residue or fixed endpoint parameter
is required. Empty corridors include consecutive odd a returns.

The block duration up to Y is d+1+2l; its coefficient loss is G+1.
These are exact. The safety of Y must still be established separately.

## 2. Elimination across two blocks

Take two consecutive blocks with corridors (alpha,B,d,G) and
(beta,E,f,L), and endpoint half-call times k1,k2. Let X0,X1 denote
their entry chain values and X2 the second output. Assume X0 and X1
are safe and the required earlier replay prefixes are available. The
second b/c corridor is then safe automatically; X2 is not assumed safe.

Eliminating the preceding H from the second block gives

    X2=(alpha/2)X0+(1-beta/2)X1+C,                 (POS)
    C=B/2+6+6k1+6k2+6f-E/2.

In particular C>0 because E<=6f-h2. All three summands are positive.
The identity is exact at resonances as well as at descending returns.

C is an integer for an actual valid prefix. To see this, a corridor
starting at q and ending at p has q-G>=p+h, by summing
j_next<=j-2-epsilon and G's increments 1+epsilon. Thus alpha X and the
endpoint x are divisible by 2^p, and so is B; the same applies to E.
Since odd a endpoints have p>=5, both B/2 and E/2 are integers.

This eliminates the older unknown H even when the endpoint parameters,
the b/c mixtures and their lengths are different in the two blocks.

## 3. Corridor bounds from earlier C1,C2

Assume C1: tau(n)<=n^2 and C2: epsilon(n)<=max(7,n/4) at the earlier
crossings used. For a corridor starting at q>=1024,

    G<=3q/4, d<2q^2.                              (BOUND)

Proof. For a b/c input j>=64 the copied parameter satisfies

    j_next<=log2(6(j-1)^2+5)<=j/2.

Hence the large input parameters have sum <=2q, sum of squares
<=4q^2/3, and number <=log2 q. Their epsilon values are at most j/4.
Below 64 there are at most 21 b/c transitions, since each drops the
parameter by at least three: this needs epsilon>=1 at b/c crossings below
64, which holds in the exact crossing table (n<20000: type b has epsilon=1,
type c has epsilon in {3,5}; minimum drop 5). Alternatively bound the small
part directly by G_small<=sum of drops<=63. The audited small table has
epsilon<=7 there. Therefore

    G<=q/2+log2 q+168<=3q/4.

For time, each large step costs at most j^2+1, and each small step
costs at most 63^2+1=3970. Using the weaker large-step count <=q gives

    d<=4q^2/3+q+83370<2q^2, q>=1024.

The last two inequalities hold at 1024 and their differences increase
thereafter. If the corridor is empty these bounds hold trivially.
Since the endpoint parameter is at most q, its half-call time satisfies
6k_endpoint<=3(q-1)^2<3q^2.

For two blocks with q0=v2(X0),q1=v2(X1) both >=1024 and Q=max(q0,q1),
the preceding estimates and B<=6d give

    0<C<9q0^2+15q1^2+6<=24Q^2+6.                 (SIZE)

The terms involving the unknown initial clock have disappeared; only
earlier call lengths and corridor constants enter this bound.

## 4. A safe logarithmic return, independent of corridor types

Put

    K=ceil(log2(24Q^2+6)),
    S0=q0-G-1, S1=q1-L-1.

The two variable summands in POS have valuations S0 and S1 exactly.
For the second coefficient, beta has valuation -L: if L>0, the two
terms of 1-beta/2 have unequal valuations; if L=0 the empty corridor
has beta=1 and the coefficient is 1/2. Thus if

    min(S0,S1)>=K,                                 (SEP)

we obtain

    q2=v2(X2)=v2(C)<K.

The second output is physically safe, since

    sigma2=sigma1-L-1>=q1-L=S1+1>q2.

No assumption of its safety was needed. A sufficient condition for SEP
and the corridor estimates is

    min(q0,q1)>=max(1024,4(K+1)).                  (LARGE)

Hypotheses of this theorem, stated explicitly: X0 and X1 are safe; C1, C2
and M2' hold at all source, corridor and endpoint crossings used;
q0,q1>=1024. The 3b+2 count below additionally needs every entry safe and
the bootstrap cap g.

This proves a two-block return theorem for arbitrary b/c mixtures and
arbitrary odd a endpoints. It is not restricted to the earlier reset
family or to pure b ancestry ending at 5.

## 5. Consequence and remaining global gap

After the first safe odd a-return of an epoch, every continuing path can
be decomposed into these blocks, until an even return ends it. Thus the
block representation no longer leaves c transitions or different odd
a endpoints outside its domain.

For a finite safe prefix whose block-entry parameters are bounded by g,
define

    K_g=ceil(log2(24g^2+6)),
    H_g=max(1024,4(K_g+1)).

Call entries q<H_g core entries. Whenever two consecutive entries are
noncore, the next one is safe and lies below K_g, hence in the core.
Consequently there cannot be three consecutive noncore entries. A
string with b core entries has at most 3b+2 entries in total.

This is still a reduction, not the required bound on b. The cap g must
come from a separately justified finite-prefix bootstrap, rather than
being assumed for an infinite unproved continuation. When entries are
small, or one is small compared with log of the other, this theorem
does not establish safety or termination of the next a-return.

The missing result is therefore a core-visit or correlated-state rank
bound for STATE and BLOCK. The old difficulty has not vanished: the
representation now covers general block types, but no bound on repeated
core visits has been established. Total duration and loss across an
unbounded number of blocks are also not controlled by individual bounds.

## 6. Verification and a bookkeeping correction

    python -B work_g2_mixed_blocks/verify_mixed.py

The script checks 243 exact mixed two-block identities with rational
arithmetic. These are algebra inputs, not actual orbit witnesses.
It also checks the corridor inequalities against the actual crossing
table for all 3072 starts q=1024,...,4095: 2093 reach an even return,
979 reach a first odd a-return. The observed maximum of two b/c steps
is not used as an all-parameter bound. Results are in `checks.json`.

While summing the loss inequality, an earlier bookkeeping line in
`work_g2_resonance/PROOF_RESONANCE.md` was corrected from
G<=J-q-2m to G<=J-q-m. Each b/c step drops j by at least G_increment+1,
not G_increment+2. The safety conclusion still follows, and that note's
separate large-J estimate and symbolic certificates do not use the
stronger incorrect expression.
