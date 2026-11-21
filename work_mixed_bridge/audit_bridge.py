"""Universal algebra checks for PROOF.md (requires z3-solver).

Every query asks for a counterexample. Any satisfiable or unknown answer
fails the audit. The source lemmas, finite enumeration, and induction on
words are imported or explained in PROOF.md, not axiomatized as a TM model.
"""
import z3


def check(name, hypotheses, conclusion, logic="QF_NRA"):
    solver = z3.SolverFor(logic)
    solver.set(timeout=30_000)
    solver.add(*hypotheses, z3.Not(conclusion))
    outcome = solver.check()
    if outcome != z3.unsat:
        detail = solver.model() if outcome == z3.sat else solver.reason_unknown()
        raise AssertionError(f"{name}: {outcome}, {detail}")
    print("UNSAT", name)


def bridge_checks():
    alpha, beta, gamma, c, t, u = z3.Reals("alpha beta gamma c t u")
    check("composition bounds for arbitrary corridor types", [
        alpha > 0, alpha <= 1, beta >= 1, beta <= 2,
        gamma >= 0, gamma <= 2*t, c >= 0, c <= 2*u, t >= 0, u >= 0,
    ], z3.And(2-alpha*beta/2 >= 1, 2-alpha*beta/2 <= 2,
              2*t-alpha*gamma/2+c >= 0, 2*t-alpha*gamma/2+c <= 2*(t+u)))

    # Write each high x as P*y. The determinant equals P times an
    # explicit integer. Normalise in the polynomial ring, without dividing.
    D, E, A, B, b, f, theta, P, y0, y1, y2 = z3.Ints("D E A B b f theta P y0 y1 y2")
    elapsed = z3.Int("elapsed")
    c0 = P * (D*y1 - A*y0) - b*theta
    c1 = P * (E*y2 - B*y1) - f*(theta + elapsed)
    determinant = b*f*elapsed + b*c1 - f*c0
    witness = b*(E*y2 - B*y1) - f*(D*y1 - A*y0)
    assert z3.is_int_value(zero := z3.simplify(determinant - P*witness, som=True))
    assert zero.as_long() == 0
    print("IDENTITY determinant = threshold * integral witness")

    # Normalize coefficients by 2^S and times by T.
    b0, b1, d0, d1, time = z3.Reals("b0 b1 d0 d1 time")
    z = b0*b1*time + b0*d1 - b1*d0
    check("normalized determinant bound", [b0 >= 0, b0 <= 2, b1 >= 0, b1 <= 2,
          d0 >= 0, d0 <= 2, d1 >= 0, d1 <= 2, time >= 0, time <= 1],
          z3.And(z >= -12, z <= 12))
    k = z3.Int("multiple")
    check("integral nonzero multiplier has magnitude at least one", [k != 0],
          z3.Or(k >= 1, k <= -1), "QF_LIA")
    v, modulus = z3.Reals("v modulus")
    check("strict separation forces a zero multiple", [
        modulus > 0, modulus*v < modulus, modulus*v > -modulus,
    ], z3.And(v < 1, v > -1))
    p, next_p = z3.Reals("p next_p")
    check("sign and factor of the payment", [
        b0 > 0, b1 > 0, t >= 1, p >= 0, next_p >= 0, p <= 2*t,
        b0*b1*t + b0*(b1*next_p) - b1*(b0*p) == 0,
    ], z3.And(next_p == p-t, 2*next_p <= p, p >= 1))


def scale_checks():
    # e doubles and r=2^(e/2) squares. This invariant replaces the
    # monotonicity arguments and covers the entire grid by integer induction.
    e, r = z3.Reals("e r")
    inv = [e >= 20, r >= 48*e+64]
    assert 2**10 == 48*20+64
    check("grid invariant survives doubling", inv, r*r >= 48*(2*e)+64)
    loss = 18*e+3 + (9*e+3)*r
    h = r*r
    check("all grid losses", inv, 4*loss <= h)
    check("bridge time at most h^7", inv, 6*(r+1) <= h)
    check("strict separation in bits", inv, 2*loss+7*e+4 < h+1)
    check("next word length at most square root of next cap",
          inv, (r+1)*(7*e+5) <= h)


def prefix_checks():
    # n inputs have n-1 interior transitions. A a-steps induce at most
    # A+1 decreasing b/c corridors among those transitions.
    g, a, bc, n = z3.Reals("g a bc n")
    check("prefix ending inside a corridor", [
        g >= 1, a >= 0, a <= g+1, bc >= 0, bc <= (a+1)*g, n == 1+a+bc,
    ], n <= (g+1)*(g+2))
    l = z3.Real("l")

    def cost(i):
        return 3*i*(2*i+5)*(2*i+6)

    assert cost(64) < 2**63
    check("outer prefix budget persists for every exponent", [l >= 64],
          cost(l+1) < 2*cost(l))
    K = z3.Real("block_loss_bound")
    check("prospective chain margin with the final transition charged separately",
          [l >= 64, g == 2*l+4, K >= 0, K <= 9*l+3],
          4*l+4 + (g+1)*K + 3*g <= 32*l*l)
    check("clock bootstrap fits the same quadratic estimate", [l >= 64, g == 2*l+4],
          1+g*g <= 32*l*l)
    assert 32*64**2 < 2**62
    check("quadratic margin persists for every exponent", [l >= 64],
          (l+1)*(l+1) < 2*l*l)


if __name__ == "__main__":
    bridge_checks()
    scale_checks()
    prefix_checks()
