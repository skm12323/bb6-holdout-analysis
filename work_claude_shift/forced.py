"""Construct exact walks with prescribed output parameters by solving affine congruences in U.
x = a*U + b, Theta = c*U + e along the walk; U = U0 + 2^s * V with V free.  Synthetic states only."""
from fractions import Fraction as F
import random
from verify_shift import v2, INF

def forced_start(cal, j0, d0, rnd, max_steps=12, cap=60):
    # start: x = 2^j0 * U (U odd), Theta = x + d0
    a, b = F(1 << j0), F(0); c, e = F(1 << j0), F(d0)
    U0, s = 1, 1          # U = 1 + 2V  (odd)
    def sub(a, b):        # substitute U = U0 + 2^s V : returns coeff of V and const
        return a * (1 << s), a * U0 + b
    j = j0; choices = []
    for _ in range(max_steps):
        r = cal.crossing(j - 1)
        if not r['odd']: break
        tau = r['time']
        if r['kind'] == 'a':
            a2, b2 = 2*c - a/2, 2*e + 3*tau - b/2
        else:
            ratio = (r['head_ratio'] + 2*r['tail_ratio'])/2
            lam = r['head_lambda'] + 2*r['tail_lambda'] + 3
            a2, b2 = ratio*a, ratio*b + lam
        c, e = c, e + 3 + 3*tau
        A, Bc = sub(a2, b2)                     # x' = A*V + Bc
        vA, vB = v2(A), v2(Bc)
        if vB < vA:
            m = vB; choices.append(('forced', m))
        else:
            m = rnd.randrange(max(1, vA), max(vA + 1, cap))
            # choose V mod 2^(m+1-vA) with A V + Bc = 2^m mod 2^(m+1)
            mod = 1 << (m + 1 - vA)
            Ao = (A / (F(2) ** vA)); Bo = (Bc - (F(2) ** m)) / (F(2) ** vA)
            Ao_i = Ao.numerator * pow(Ao.denominator, -1, mod) % mod
            Bo_i = Bo.numerator * pow(Bo.denominator, -1, mod) % mod
            V0 = (-Bo_i * pow(Ao_i, -1, mod)) % mod
            U0 = U0 + (V0 << s); s += m + 1 - vA
            choices.append(('free', m))
        a, b = a2, b2; j = m
        if j < 2: break
    U = U0 + (rnd.randrange(0, 1 << 40) << s)
    return U, choices
