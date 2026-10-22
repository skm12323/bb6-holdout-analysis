# Global strict EXT would force unbounded c parameters, already at deficit eleven

2026-10-21. **UNREVIEWED proposed conditional theorem.** The hypothesis
is global strict EXT. The conclusion is an obstruction to a fixed
canonical c-parameter cap, not an EXT counterexample or a proof of EXT.

## 1. Target canonical fire times

For every m>=5, select v_m from the following period-six list:

    m mod 6:  0  1  2   3   4   5
    v_m:      1  5  7  17  13  11.

Then k_m=(v_m*2^m-10)/9 is a positive integer and
v2(9*k_m+10)=m. Its possible fire parameter is exactly three,
because 3*(3*k_m+2)=v_m*2^m-4 has valuation two.

We show these arithmetic times are genuinely canonical, under the
stated global hypothesis. They are not freely chosen local clocks.

## 2. Gap bound and a no-overshoot barrier

Global strict EXT implies that the universal walk F is defined
forever by the accepted EGX Theorem U. On this reached orbit, C1
gives tau(n)<=n^2. In a fire epoch of parameter P>=2, strict records
give at most P-1 chains including the fire, with every parameter <=P.
The time to the next fire is at most

    (P-1)*(1+(P-1)^2)+2.

Thus its half-time gap is <=P^3/2. For P<=15 we instead use the
accepted exact gap list (1,1,2,2,3,3,3,4,4,5,5,6,6,8,7).

Fix m>=16, k=k_m, and an earlier fire half-time h<k. Put d=k-h>0
and P=1+v2(3h+2). Since 3h+2<(17/3)*2^m, P<=m+3. Also

    3*(3h+2)=v_m*2^m-4-9d.

If P-1<m, then 2^(P-1) divides 4+9d. For P>=16 this implies

    d >= (2^(P-1)-4)/9 >= P^3/2.

If P-1>=m, then

    d >= (2^m-4)/9 >= (m+3)^3/2 >= P^3/2.

Both cubic/exponential inequalities hold at 16 and persist since
the cubic's successive growth factor is below two. For P<=15,
the smallest positive d solving 4+9d=0 mod 2^(P-1) is at least
the corresponding exact gap; the verifier lists all fifteen values.
Consequently the next fire cannot jump over k_m. Fire half-times
increase strictly, and the global hypothesis supplies every next
fire. They must reach k_m. The cases 5<=m<16 are verified by the
finite canonical calendar.

This barrier can also be used on a sufficiently long certified
finite prefix. The global conclusion here is explicitly conditional;
the finite check is not being extrapolated to arbitrary m.

## 3. Lift the target to a genuine five-to-m gateway

Let p-1 be the actual pointer at k_m. Then X(p-1) is odd a with
half-time k_m. For m>=16, C1 and
2*k_m>=2*(2^m-10)/9>(m+3)^2 imply p>=m+4 (in fact p>=m+5; the weaker bound suffices). The smaller cases
satisfy this directly in the verified calendar.

The cubic gap bound also implies the accepted GAP condition
gap(P)<=2^(P-2) for P>=16; the small kernels supply the remaining
cases. Therefore the PROOF_SPECTRUM no-overshoot argument now gives
occurrence of every fire parameter, under global EXT. Apply its
three-b ancestry construction to p:

    p1=rho(p)+2, p2=rho(p1)+2, p3=rho(p2)+2.

These are actual earlier-source pointers, not arbitrary ancestors.
The parameter-p3 fire starts with three b returns to p2,p1,p. As
shown by the affine origin calculation in AFFINE_REACHABLE_CATAPULTS,
the next a outputs have small parts

    beta_5=(55/32)*L2+(13/8)*L1+(3/2)*L0+6*k_m-4,
    beta_m=(73/64)*L2+(19/16)*L1+(5/4)*L0+9*k_m+10.

Their valuations are exactly 5 and m: p>=m+4 and p_(i+1)>=p_i+3
put every omitted source and root-coefficient term strictly above
the controlling valuation. Thus an actual epoch has prefix

    p3,p2,p1,p,5,m.

This conclusion does not need a finite certificate for the suffix
after m; global EXT already supplies its safety, and the displayed
source is reached before that suffix is used.

## 4. The c-source deficit and the consequence for CAL-C

Let rho be the pointer of the parameter-p3 fire. The output at m
follows history BBBAA. There have been three b losses and two a
losses, totaling Gamma=8, and two a outputs. It is an odd c crossing
at original index n=rho+3 with coefficient precision rho-8, hence

    epsilon=n-(rho-8)=11, omega(n)=m.

Therefore, under global strict EXT, every m>=5 occurs at a canonical
odd c crossing of deficit eleven. For ANY fixed N>=5, taking m>=N
produces n>=N-1 and 2^N divides lambda'_W(n). In particular,

    global strict EXT implies NOT CAL-C_N,

where CAL-C_N is the all-index prohibition of c parameters >=N.
This rules out completing global EXT by simultaneously establishing
that fixed all-scale c cap. (Review correction: the accepted R1 of work_r1r2 IS phase-sensitive
and still fails at some J in [K_clock,T4), and CAL-C is false without the global-EXT
hypothesis, by shallower epsilon-three sources; see CONGRUENCE_TARGET_NOTE.md. The BBBAA family
here has shift +4/3, so at J=n+1 it leaves the small-integer deep window rather than violating
R1. Correct residual conditions should classify c steps by their source shift, not cap the
parameter.)

Nor does it refute the actual non-halting goal: these constructed
large c parameters are safe under the hypothesis. Their phases and
remaining record margins, not their size alone, are the relevant
quantities to control.

## 5. Verification

    python -B work_c3_drift/verify_target_fire_barrier.py

All fifteen small-kernel barriers, 283,983 individual predecessor
inequalities for targets m=16,17,18, and 124 canonical targets
m=5..128 pass. Cubic and pointer-size inequalities are checked on
finite integer ranges as controls for the analytic induction.
The actual all-m conclusion uses the global hypothesis and proof
above. Independent review is pending; accepted horizon claims are
unchanged.
