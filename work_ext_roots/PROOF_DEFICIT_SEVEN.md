# Deficit seven: CA descent and two correlated remaining families

2026-10-18. **Accepted after three-way review (MINUS/PLUS families remain unproved). EXT remains open.**
Imports: accepted weight/copy/HP lemmas, C1, uniform fire transfer;
the preceding A-SOURCE proposal is used when describing the frontier.

## 1. Histories at deficit seven

At a c crossing epsilon=W+1. A and B cost two in W; C costs
2+W_source>=4. Thus epsilon=7, with history ending in A, permits only

    AAA, ABA, BAA, BBA, CA.

In CA, the copied source has weight two and therefore history A.
AAA and ABA are covered by the proposed A-SOURCE theorem. We treat
CA below. BAA and BBA remain conditional reference-family targets.

## 2. CA reduces to smaller EXT

Let the source epoch fire at pointer rho, parameter R, numerator
X=2^R U and phase X+1. Its first C copies a deficit-three c crossing
from an earlier epoch. Write that earlier fire's pointer rho_s,
parameter P, numerator Y=2^P V, and h=tau(P-1)/2. Its first A output is

    x_I=(3/2)Y+6h+2, Theta_I=Y+6h+4,
    v2(c_I)=rho_s-1,

where c_I is the source chain coefficient. The crossing is rho_s+2,
so R=rho_s+3. Its output parameter is p=v2(6h+2)<P-1, by the
SIZE/SMALL bound in `PROOF_LOW_DEFICIT.md`.

After the C return, the outer source epoch has

    x_C=c_I U+(3/2)Y+6h+2, Theta_C=X+Y+6h+3.

The next A reads X(p-1), with k=tau(p-1)/2. After that A and the
-1 shift for the EXT entry, the exact state is

    x=2X-c_I U/2+(5/4)Y+9h+6k+5,
    Theta=X+Y+6h+6k+5.                       (CA)

Compare with a virtual fire z=6k+2, Theta_ref=z+1. Let q=v2(z)<p-1.
The two differences are

    delta_x=2X-c_I U/2+(5/4)Y+3(3h+1),
    delta_Theta=X+Y+2(3h+1).

Since v2(3h+1)=p-1, their valuations are exactly p-1 and p.
All other terms have valuation at least P-2>p-1, using P<rho_s
and R=rho_s+3.

The CA source loses 4+1=5 coefficient units and has one A. Hence
its crossing is rho+2, the outer J=rho+3, and sigma_0=rho-5.
Since rho>R, sigma_0>=rho_s-1>=P>p. Assuming EXT(q), the virtual
fire terminates with j+Lambda<=q<p-1; HP transfers this tail to CA,
and sigma_0>p ensures strict safety. Finally q<p<P<R<rho<J, so
EXT(q) is available at a least EXT counterexample.

**Proposed CA theorem:** such a source cannot occur at a least strict
EXT counterexample. This is an all-scale reduction, conditional on
the smaller EXT instance; it is not a numerical extrapolation.

## 3. BAA normal form

Let the source fire numerator be X=2^R U. Its B copies a real fire
Y=2^p V at pointer R-2, so p<R-2. Put k=tau(p-1)/2. After BA,

    x_BA=(13/8)X+(3/2)Y+6k, Theta_BA=X+Y+6k+3,
    r=v2(x_BA)=1+v2(k)<p-1.

For BAA, X(r-1) is odd type a. Put l=tau(r-1)/2. The shifted output is

    x=(19/16)X+(5/4)Y+9k+6l+6,
    Theta=X+Y+6k+6l+5.

Compare with z=6l+6, Theta_ref=z-1. The differences have valuations
r-1 and r, determined by 9k and 6k; the other terms have valuations
at least p-2>=r. Also v2(z)<r-1: for r>=10 use
6l+6<=3(r-1)^2+6<2^(r-1); r=5,8 are checked directly.
The source coefficient valuation rho-5 exceeds r-1.

Consequently BAA closes by HP if this correlated reference terminates
with j+Lambda<r-1. The all-scale reference property is still open.

## 4. BBA normal form

The two B returns copy real fires Y1=2^p1 V1 and Y2=2^p V2,
where p1<R-2 and p<p1-2. After BB,

    x_BB=(9/16)X+(3/4)Y1+Y2,
    Theta_BB=X+Y1+Y2-1.

Put k=tau(p-1)/2 at its A endpoint. The shifted output is

    x=(55/32)X+(13/8)Y1+(3/2)Y2+6k-2,
    Theta=X+Y1+Y2+6k+1.

Compare with z=6k-2, Theta_ref=z+3. Differences have valuations
p-1 and p, determined by Y2/2 and Y2. Also v2(z)<p-1 by C1 and
the p=5,8 checks, and rho-5>p-1. Thus HP reduces BBA to the
termination/margin property of this reference, which remains open.

The two explicit targets, for actual odd a crossings X(m-1), are

    MINUS(m): x=6k_m+6, Theta=6k_m+5;
    PLUS(m):  x=6k_m-2, Theta=6k_m+1;
    k_m=tau(m-1)/2, required j+Lambda<m-1.

The actual clock correlation is essential. These are sufficient routes
for the deficit-seven cases, not additional independent obligations
for every possible proof of EXT. Higher deficits and outer b entries
remain open.

Both families start inside the positive cone Theta>=5,
0<x<=2Theta-5 of the accepted local-realization lemma. Their valid
return maps therefore preserve positivity. This excludes zero-numerator
virtual resonance, but not excessive loss or a coefficient tie.

## 5. Checks and a failed finite extrapolation

`verify_ca_source.py` uses a cutoff-6144 canonical calendar to check
an actual CA source epoch of parameter R=6133 (its fire time and pointer are located exactly by the
calendar's inverse navigation inside the certified cutoff-6144 prefix; the copied part — pointer 6130,
level 14, h=5, p=5, q=3 — was also reproduced independently by a reviewer). It copies a parameter-14
fire's first A output, gives p=5, and reduces to q=3. The outer J
has 6134 bits. All source, deficit, scalar and shadow identities pass.
This lies inside the already accepted horizon; it is not a new record.

`verify_deficit7_families.py` checks each family at all 302878 odd a
source indices m-1 with 5<=m<10^6. Every reference terminates with
j+Lambda<m-1. MINUS has 653 nonterminal cases; PLUS has none there.

It then tests 3024 additional canonical source cases per family: twelve
successive fires starting from a fire of each parameter 5..256 in a
cutoff-512 calendar. Cases may overlap. Both families have 12 nonterminal
cases, all terminating. For PLUS, the source immediately after a
parameter-38 fire gives word (5,2). Thus extrapolating the small-range
observation "PLUS always ends immediately" would be false.

Finally 228 BBA and 12 BAA algebraic outer lifts check the normal-form
identities and precision valuations. Those selected outer fires are
explicitly not asserted canonical; the call clocks are actual data.

None of these checks proves the global MINUS/PLUS property. The CA
argument and normal-form reductions need independent review. If all
current proposals are accepted, the deficit-seven c frontier is BAA
or BBA; higher-deficit b/c-starting epochs remain unresolved.

    python -B work_ext_roots/verify_ca_source.py
    python -B work_ext_roots/verify_deficit7_families.py
