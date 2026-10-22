# Joint source certificates for early a outputs with arbitrary b/c interruptions

2026-10-21. **UNREVIEWED conditional prefix theorem.** This covers mixed
copy prefixes without assuming the whole exit at the current root is
tie-free. It does not bound the total number of a returns.

## 1. Induction inputs and scope

Fix a root P>=512, with canonical data defined through X(P-1).
Assume strict EXT for smaller roots, so the accepted C2-log estimate
is available at the earlier source epochs read here. Use C1, real
source S1, and the accepted affine beta recurrence. No EXT(P)
assumption is made.

Put e=floor(log2 P), D=3e+7 and

    L=floor(P/D)-4.

Then every one of the first L odd-a outputs, if reached, is strictly
safe and admits a joint source certificate

    Gamma+m+2r+h(c)<P.

If the exit ends sooner, no assertion of further outputs is intended.
The intervening b/c strings may be arbitrary and of varying deficit.

## 2. First-copy loss and parameter bound

If the initial return is b/c, put

    E=ceil(log2(3*(P-1)^2+4)),
    K=floor(log2(6*(P-1)^2+5)).

C2-log gives initial loss at most 2E (b is covered directly), and
lambda mass gives its next parameter at most K. Every later b/c
copy strictly decreases parameter-plus-loss. Thus, up to the first
odd a call, Gamma+j<=2E+K<=6e+13=2D-1.
If the root's first call is a, its first loss is simply one.

The earlier source root used by C2-log is smaller than P, so this
application is compatible with induction. It does not use the desired
conclusion for the current root.

## 3. Positive beta bound, including candidate a outputs

At a noninitial state write Theta_beta=3d+1. The accepted bound is
1<=beta<=6d-1. It also propagates algebraically to the next candidate
output, before its valuation is declared safe:

* a: beta'=6d+2+3tau-beta/2 is positive and <=6d'-1;
* b/c: beta'=R*beta+lambda, where 0<R<1 by coefficient mass and
  0<lambda<=6tau+5, giving the same bound;
* the initial beta=0 is handled directly: a gives 2+3tau, and b/c
  gives lambda.

Here d'=d+1+tau. Before a candidate output, all calls already used
have parameters <=P. Their duration is <=1+(P-1)^2<=P^2. The number
of updates is at most Gamma, since each update costs at least one.
Consequently d<=Gamma*P^2 and, while Gamma<P,

    0<beta<6P^3,  v2(beta)<=3e+5<D.

The positivity prevents a zero beta from being silently assigned a
valuation. The estimate is established before deciding whether the
candidate next parameter is below its coefficient precision.

## 4. Induction on the number of odd a outputs

At output number ell, the bounds are

    Gamma_ell <=(ell+1)D,  m_ell<D.

For ell=1 the first-copy estimate (or direct initial a step) gives
the loss bound. The beta estimate then bounds the output parameter.
After any such output, an intervening b/c segment can only reduce
Gamma+j. Before the next a call it is below (ell+2)D; adding that
a loss proves the next loss bound. An all-b/c segment cannot run
forever, since every such step strictly decreases a positive parameter.

For ell<=L, the candidate output satisfies

    Gamma_ell+3m_ell
       <(ell+1)D+3D <=(L+4)D <=P.

In integer form the available slack is at least three using m<=D-1.
Hence m_ell<P-Gamma_ell, and the actual parameter is indeed the beta
valuation, uniformly in the root odd base. This closes the candidate
step without assuming it is already tie-free. The coefficient part
also vanishes modulo 2^(m_ell+1), so the extra phase bit is known.

This is simultaneous induction on loss, parameter, and strict margin;
it does not infer all future termination from a finite safe prefix.

## 5. The earlier-source contract is available at these outputs

The source phase modulo 2^(m+1) is supplied by 3d+1-beta. Apply the
universal encoding of B_PREFIX_SOURCE_ENCODING: choose a reduced
c in [1,2], a rank r<=m, and the correct lift bit. Then

    Gamma+m+2r+h(c)<=Gamma+3m<P.

For an actual root epoch these a outputs are canonical c sources,
so their certificates may be used by JOINT_HEIGHT_BUDGET in later
copies. The denominator rank can be large enough to put the copied
state below its adaptive contraction threshold; the certificate is
not itself a proof that its shifted tail terminates.

The pure-b restriction from the preceding note is no longer needed
for these early outputs. The remaining issue is to bound later a
outputs or otherwise certify the exit after this budget range.
This does not supersede the accepted non-descent-count reductions:
it provides a strengthened source certificate over a bounded prefix,
not an all-scale bound on the number of returns.

## 6. Finite validation

    python -B work_c3_drift/verify_early_mixed_sources.py

The checker evaluates all 7,680 symbolic exits P=512..8191. It checks
2,571 a-output certificates and 2,571 copy record drops. The observed
histories are a, aa, ba, ca; at most two a outputs occur in this
finite selection. Thus the long-history induction is supported by
the written inequalities, not by extrapolating those observed words.
No accepted horizon or global proof status changes.
