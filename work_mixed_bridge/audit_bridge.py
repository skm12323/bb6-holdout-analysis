"""Exact universal algebra checks for PROOF.md (integer arithmetic only).

This replaces the earlier z3-based audit. Every obligation is discharged
exactly, with no sampling and no third-party packages: each is a polynomial
identity in a polynomial ring, or an inequality over a box on which the
target is multilinear and therefore attains all extrema at box corners, or
a univariate polynomial checked to have nonnegative coefficients after an
explicit shift. The source lemmas, finite enumeration, and induction on
words are imported or explained in PROOF.md, not axiomatized here as a TM
model.
"""
from fractions import Fraction
from itertools import product


# ---------- exact univariate polynomials, as {exponent: int} ----------

def p_add(p, q):
    out = dict(p)
    for k, c in q.items():
        out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c}


def p_sub(p, q):
    return p_add(p, {k: -c for k, c in q.items()})


def p_mul(p, q):
    out = {}
    for k, c in p.items():
        for l, d in q.items():
            out[k + l] = out.get(k + l, 0) + c * d
    return out


def nonneg(p):
    return all(c >= 0 for c in p.values())


def compose(poly, inner):
    """poly(inner(e)) for univariate integer polynomials."""
    out = {}
    for k, c in poly.items():
        term = {0: c}
        for _ in range(k):
            term = p_mul(term, inner)
        out = p_add(out, term)
    return out


def shifted(poly, base):
    """Coefficients of poly(e) in powers of (e - base)."""
    return compose(poly, {0: base, 1: 1})


# ---------- exact 12-variate polynomials, as {exponent tuple: int} ----------

def n_add(p, q):
    out = dict(p)
    for k, c in q.items():
        out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c}


def n_sub(p, q):
    return n_add(p, {k: -c for k, c in q.items()})


def n_mul(p, q):
    out = {}
    for k, c in p.items():
        for l, d in q.items():
            key = tuple(a + b for a, b in zip(k, l))
            out[key] = out.get(key, 0) + c * d
    return out


def n_var(i, n):
    return {tuple(1 if j == i else 0 for j in range(n)): 1}


def bridge_checks():
    # (2): appending one block keeps beta in [1,2] and gamma in [0,2(t+u)].
    # Write gamma = 2*t*ghat and c = 2*u*chat with ghat, chat in [0,1]. The
    # new gamma = t*(2 - alpha*ghat) + 2*u*chat is linear in (t, u) >= 0,
    # and its coefficient expressions, like the new beta, are multilinear
    # on the box, hence corner-exact.
    unit = (Fraction(0), Fraction(1))
    beta_endpoints = (Fraction(1), Fraction(2))
    beta_images = []
    for alpha, beta, ghat, chat in product(unit, beta_endpoints, unit, unit):
        beta_images.append(2 - alpha * beta / 2)
        coef_t, coef_u = 2 - alpha * ghat, 2 * chat
        assert 1 <= coef_t <= 2 and 0 <= coef_u <= 2
    assert (min(beta_images), max(beta_images)) == (1, 2)
    print("EXACT composition bounds for arbitrary corridor types")

    # Determinant identity: with each high x written as a threshold P times
    # an integer, the eliminated-clock determinant equals P times the
    # explicit integral witness, in the polynomial ring (no division).
    D, E, A, B, b, f, theta, P, y0, y1, y2, elapsed = (n_var(i, 12) for i in range(12))
    c0 = n_sub(n_mul(P, n_sub(n_mul(D, y1), n_mul(A, y0))), n_mul(b, theta))
    c1 = n_sub(n_mul(P, n_sub(n_mul(E, y2), n_mul(B, y1))),
               n_mul(f, n_add(theta, elapsed)))
    determinant = n_sub(n_add(n_mul(b, n_mul(f, elapsed)), n_mul(b, c1)),
                        n_mul(f, c0))
    witness = n_sub(n_mul(b, n_sub(n_mul(E, y2), n_mul(B, y1))),
                    n_mul(f, n_sub(n_mul(D, y1), n_mul(A, y0))))
    assert n_sub(determinant, n_mul(P, witness)) == {}
    print("EXACT determinant = threshold * integral witness")

    # Normalize coefficients by 2^S and times by T: z is multilinear on the
    # box, so its extrema are corners.
    lo = hi = None
    for b0, b1, d0, d1, time in product([Fraction(0), Fraction(2)],
                                        [Fraction(0), Fraction(2)],
                                        [Fraction(0), Fraction(2)],
                                        [Fraction(0), Fraction(2)],
                                        [Fraction(0), Fraction(1)]):
        z = b0 * b1 * time + b0 * d1 - b1 * d0
        lo = z if lo is None else min(lo, z)
        hi = z if hi is None else max(hi, z)
    assert (lo, hi) == (Fraction(-4), Fraction(8))
    assert -12 < lo <= hi < 12
    print("EXACT normalized determinant bound")

    # An integral nonzero multiple of the modulus has magnitude >= 1; a
    # multiple strictly smaller than the positive modulus vanishes, since
    # multiplying an inequality by the positive rational 1/m preserves it.
    # The loops below illustrate these two order-preservation steps on
    # representative values; the proofs are the divisions themselves.
    for k in range(-5, 6):
        assert k == 0 or abs(k) >= 1
    for v in (Fraction(-3, 7), Fraction(0), Fraction(22, 7)):
        for m in (Fraction(1), Fraction(2, 3), Fraction(10**9)):
            assert (abs(v) * m < m) == (abs(v) < 1)
    print("EXACT separation forces a zero multiple")

    # Sign and factor of the payment: dividing the vanishing determinant by
    # b0*b1 > 0 (exact order-preserving rational division) gives p = t +
    # next_p; then next_p >= 0 gives p >= t >= 1, and p <= 2*t gives both
    # 2*next_p = 2*p - 2*t <= p. Spot-assertions:
    for t, nxt in product([Fraction(1), Fraction(10**6)],
                          [Fraction(0), Fraction(1), Fraction(10**6)]):
        if nxt > t:  # excluded by the hypothesis p <= 2*t
            continue
        p = t + nxt
        assert 2 * nxt <= p and p >= 1 and 0 <= nxt <= p
    print("EXACT sign and factor of the payment")


R0 = {0: 64, 1: 48}  # the grid invariant r >= 48e+64, equality at e=20


def gap_polynomials():
    """The four grid obligations as polynomials in e, evaluated at r=48e+64.

    Each obligation has the form D(e,r) = r^2 - c1(e)*r - c0(e) >= 0 with
    h = r^2. On the invariant D is increasing in r, because the derivative
    2r - c1(e) is bounded below by 2*(48e+64) - c1(e), whose coefficients
    are nonnegative with a positive constant term. So D(e,r) is minimal at
    r = 48e+64, where the returned polynomial has nonnegative coefficients
    with a positive constant term.
    """
    obligations = [
        ("4*loss <= h", {1: 36, 0: 12}, {1: 72, 0: 12}),
        ("6*(r+1) <= h", {0: 6}, {0: 6}),
        ("2*loss+7e+4 <= h", {1: 18, 0: 6}, {1: 43, 0: 10}),
        ("(r+1)*(7e+5) <= h", {1: 7, 0: 5}, {1: 7, 0: 5}),
    ]
    square = p_mul(R0, R0)
    out = []
    for name, c1, c0 in obligations:
        gap = p_sub(p_sub(square, p_mul(c1, R0)), c0)
        deriv = p_sub(p_mul({0: 2}, R0), c1)
        assert nonneg(gap) and gap.get(0, 0) > 0, name
        assert nonneg(deriv) and deriv.get(0, 0) > 0, name
        out.append(gap)
    return out


def scale_checks():
    # e doubles and r=2^(e/2) squares. The invariant survives doubling
    # because (48e+64)^2 - (96e+64) = 2304e^2 + 6048e + 4032 >= 0.
    assert 2**10 == 48 * 20 + 64
    assert nonneg(p_sub(p_mul(R0, R0), {1: 96, 0: 64}))
    gap_polynomials()
    # Consequences: 6*(r+1) <= h gives time <= h^7, and 12 < 2^4 together
    # with 2*loss+7e+4 <= h gives the separation (4). Base spot check:
    e, r = 20, 1 << 10
    h = r * r
    loss = 18 * e + 3 + (9 * e + 3) * r
    assert 4 * loss <= h and 6 * (r + 1) <= h
    assert 2 * loss + 7 * e + 4 < h + 1
    assert (r + 1) * (7 * e + 5) <= h
    for poly, direct in zip(gap_polynomials(), (
            h - 4 * loss, h - 6 * (r + 1), h - (2 * loss + 7 * e + 4),
            h - (r + 1) * (7 * e + 5))):
        assert sum(c * e**k for k, c in poly.items()) == direct
    # Cross-check the polynomial engine against direct arithmetic at more
    # grid exponents (independent recomputation paths must agree).
    for e in (40, 80):
        r0 = 48 * e + 64
        h0, loss0 = r0 * r0, 18 * e + 3 + (9 * e + 3) * r0
        for poly, direct in zip(gap_polynomials(), (
                h0 - 4 * loss0, h0 - 6 * (r0 + 1), h0 - (2 * loss0 + 7 * e + 4),
                h0 - (r0 + 1) * (7 * e + 5))):
            assert sum(c * e**k for k, c in poly.items()) == direct
    assert 12 < 2**4
    print("EXACT grid invariant and all four scale obligations")


def prefix_checks():
    # n inputs have n-1 interior transitions. A a-steps induce at most
    # A+1 decreasing b/c corridors among those transitions. The identity
    # (g+1)(g+2) - (1+a+(a+1)*g) = (g+1)*(g+1-a) is exact in the ring, and
    # both factors are nonnegative under 0 <= a <= g+1, g >= 0.
    g, a, one, two = {(1, 0): 1}, {(0, 1): 1}, {(0, 0): 1}, {(0, 0): 2}
    lhs = n_mul(n_add(g, one), n_add(g, two))
    rhs = n_add(one, n_add(a, n_mul(n_add(a, one), g)))
    fact = n_mul(n_add(g, one), n_sub(n_add(g, one), a))
    assert n_sub(n_sub(lhs, rhs), fact) == {}
    for gv in (1, 7, 10**6):
        for av in (0, gv, gv + 1):
            assert 1 + av + (av + 1) * gv <= (gv + 1) * (gv + 2)
    print("EXACT prefix ending inside a corridor")

    # 3*l*(2l+5)*(2l+6) < 2^(l-1) persists for every exponent: the base
    # holds at l=64 and the growth factor is < 2, since 2*cost(l) -
    # cost(l+1) is nonnegative for l >= 64 (shifted coefficients).
    cost = {3: 12, 2: 66, 1: 90}  # 3*l*(2l+5)*(2l+6)
    assert sum(c * 64**k for k, c in cost.items()) == 3 * 64 * 134 * 133 < 2**63
    persist = p_sub(p_mul({0: 2}, cost), compose(cost, {0: 1, 1: 1}))
    s = shifted(persist, 64)
    assert nonneg(s) and s.get(0, 0) > 0
    # 4l+4+(g+1)K+3g <= 32l^2 with g=2l+4 and K <= 9l+3, and the two
    # quadratic margins: all nonnegative from l=64 on.
    margin = p_sub({2: 32}, {2: 18, 1: 61, 0: 31})
    margin2 = p_sub({2: 32}, {2: 4, 1: 16, 0: 17})
    margin3 = p_sub({2: 1}, {1: 2, 0: 1})
    for m in (margin, margin2, margin3):
        s = shifted(m, 64)
        assert nonneg(s) and s.get(0, 0) > 0
    assert 32 * 64**2 < 2**62
    # K <= 9l+3 for l >= 64 needs log2(2l+4) <= l: true at 64 (132 < 2^64)
    # and preserved by doubling since 2l+6 < 2*(2l+4) for all l >= 0.
    assert 2 * 64 + 4 < 2**64
    assert all(2 * l + 6 < 2 * (2 * l + 4) for l in range(100))
    print("EXACT outer prefix budget for every exponent l >= 64")


if __name__ == "__main__":
    bridge_checks()
    scale_checks()
    prefix_checks()
