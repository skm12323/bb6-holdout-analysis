# Clock compatibility across consecutive gateway returns

**Review status (2026-10-24):** reviewed via the work_gateway_trains three-way review (reviews/gateway_trains_review_record.md, group 2). ACCEPTED [A]+[B]: two-a-step recurrence and (TRAIN) congruence [A]; no three identical consecutive catapults [A]; the necessary-condition graph (5776 vertices) is cyclic [B]; cycle (8,244,81,27) not exactly repeatable [A]. The C1 shorthand means the accepted CLOCK bound (tau(n)<=n^2 derivation should be spelled out).

2026-10-20. **UNREVIEWED proposed all-parameter identities and bounds.**
This addresses repeated gateways using exact numerator/clock equations,
without approximating their rational phase or assuming a finite window.
It does not yet bound arbitrary trains or denominator depth globally.

## 1. Exact recurrence

Consider a valid segment with parameter word

    5,m_0,5,m_1,5,m_2,...

where every displayed return is odd type a. Let (x_i,Theta_i) be
the state at the i-th displayed five, and let k_i=tau(m_i-1)/2.
The first a return uses X(4), whose half-time is 1. Write y_i for
its output numerator, so v2(y_i)=m_i. Two exact a updates give

    y_i=-x_i/2+2*Theta_i+6,
    x_(i+1)=x_i/4+Theta_i+15+6*k_i,
    Theta_(i+1)=Theta_i+12+6*k_i.

Eliminating x_i yields

    y_(i+1)-y_i/4=Theta_i+21+9*k_i,
    4*y_(i+2)-5*y_(i+1)+y_i=12*(4-k_i+3*k_(i+1)).

Consequently every three consecutive catapult parameters satisfy

    v2(4-k_i+3*k_(i+1))
        >= min(m_i-2,m_(i+1)-2,m_(i+2)).            (TRAIN)

Zero on the left is interpreted as infinite valuation. These are
necessary identities for any such exact trajectory, canonical or
otherwise. They do not cross an unresolved tie: a claimed valid
train must supply its stated transitions before TRAIN is applied.

## 2. Three identical catapults are impossible

If m_i=m_(i+1)=m_(i+2)=m, then TRAIN requires

    v2(4+2*k_m)>=m-2.

For m>=8, C1 gives 0<4+2*k_m<=(m-1)^2+4<2^(m-2).
The last inequality holds at m=8 and persists by the quadratic's
successive ratio being below 2. For 5<=m<8, the only odd-a source
is m=5 with k=1, and v2(6)=1<3. Therefore no valid segment can
contain the complete word

    5,m,5,m,5,m

for any fixed canonical odd-a parameter m>=5. Each complete return
to five costs two loss units, but this result additionally rules
out repeatedly consuming that budget at one fixed catapult label.
It does not rule out varying labels.

## 3. A uniform band forces descent of the actual clock

Suppose s>=3 successive catapult labels all lie in [L,M], L>=5,
and

    4+2*(M-1)^2 < 2^(L-2).                         (BAND)

C1 bounds k_i<=(M-1)^2/2. Thus the absolute value of
4-k_i+3*k_(i+1) is strictly below 2^(L-2). By TRAIN it must be zero:

    k_i=3*k_(i+1)+4, for i=0,...,s-3.

Equivalently k_i+2=3*(k_(i+1)+2). Since k_(s-2)>=1,

    3^(s-1)<=k_0+2,
    s<=1+floor(log_3(k_0+2)).

The bound uses actual canonical call times, not only a formal phase
height. It applies on every reached prefix where the imported C1
estimate holds. It fails to cover a train alternating between very
small labels and labels far outside the band. Those inter-scale
transitions remain a central global gap.

## 4. The necessary-condition graph is not enough

The verifier constructs all pair vertices (a,b) with canonical odd-a
labels 5<=a,b<=256 and adds (a,b)->(b,c) exactly when TRAIN permits c.
There are 76 labels, 5,776 vertices, and 1,433 edges. The graph has
cycles, so it does NOT certify a finite train-length bound.

One cycle has catapult labels 8,244,81,27. It illustrates information
lost by the graph: one repetition advances Theta by

    sum(12+6*k_i)=960, with v2(960)=6.

But the first recurrence above also imposes, at each pair (a,b),

    Theta_i=-21-9*k_a (mod 2^min(a-2,b)).

For this cycle the maximum required precision is 81. Repeating the
identical cycle would require the clock advance 960 to be divisible
by 2^81, which it is not. Hence that graph cycle cannot be repeated
as an exact train. This does not certify that even one traversal is
reachable, or rule out other cycles/variable itineraries.

The next useful refinement is to retain a shared clock residue and
its accumulated advance along a train, rather than only checking
each neighboring triple. A phase-free label graph overapproximates
too much to settle the depth/source correlation.

## 5. Checks

    python -B work_c3_drift/verify_gateway_train.py

144 exact rational substitutions verify the recurrence; these are
algebra checks, not canonical-train witnesses. All 76 finite diagonal
cases match the no-three-identical result. The quadratic inequality
is checked for 8<=m<=4096, with its all-m induction stated above.
The cyclic graph and failed periodic-clock condition are explicitly
saved in gateway_train_checks.json; no false acyclicity claim is made.
The accepted non-halting horizon remains unchanged.
