"""Targeted re-review attack on the patched audit_bridge.py.

1. Reconstruct each of the four grid obligations INDEPENDENTLY from its
   statement (loss=18e+3+(9e+3)r, h=r^2) and compare with the script's gap
   polynomials at many e; also check the obligations directly at random
   (e,r) on and above the invariant.
2. Check the derivative/monotonicity claim numerically: D(e,r) increasing
   in r for r >= 48e+64, and vertex r* = c1/2 < 48e+64.
3. Verify the 12-variate determinant identity on random integers.
4. Verify corner-exactness of the multilinear claims at random interior
   points (they must lie within the corner-derived bounds).
5. Verify shifted/persist/margin polynomials independently (closed forms).
6. Verify c1/c0 term completeness by comparing against the true
   expressions evaluated symbolically at (e, r=48e+64).
"""
import sys
import random
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "work_mixed_bridge"))
import audit_bridge as ab

random.seed(424242)

fails = 0

# --- 1+6. obligations rebuilt independently -----------------------------
def obligations_true(e, r):
    S = 18 * e + 3 + (9 * e + 3) * r
    h = r * r
    return {
        "4*loss <= h": h - 4 * S,
        "6*(r+1) <= h": h - 6 * (r + 1),
        "2*loss+7e+4 <= h": h - (2 * S + 7 * e + 4),
        "(r+1)*(7e+5) <= h": h - (r + 1) * (7 * e + 5),
    }

gaps = ab.gap_polynomials()
names = ["4*loss <= h", "6*(r+1) <= h", "2*loss+7e+4 <= h",
         "(r+1)*(7e+5) <= h"]
my_closed = {
    "4*loss <= h": lambda e: 576 * e * e + 3192 * e + 3316,
    "6*(r+1) <= h": lambda e: 2304 * e * e + 5856 * e + 3706,
    "2*loss+7e+4 <= h": lambda e: 1440 * e * e + 4661 * e + 3702,
    "(r+1)*(7e+5) <= h": lambda e: 1968 * e * e + 5449 * e + 3771,
}
for name, poly in zip(names, gaps):
    for e in (0, 1, 19, 20, 21, 37, 123, 999, 12345, 10**6):
        pv = sum(c * e ** k for k, c in poly.items())
        assert pv == my_closed[name](e), (name, e, pv)
        assert pv == obligations_true(e, 48 * e + 64)[name], (name, e)
print("gap polynomials match independent closed forms AND true gaps: OK")

# direct checks on and above the invariant
for _ in range(400):
    e = random.randrange(0, 300)
    r = 48 * e + 64 + random.randrange(0, 5000)
    for name, val in obligations_true(e, r).items():
        assert val >= 0, (name, e, r)
print("obligations hold at 400 random (e, r>=48e+64): OK")

# --- 2. monotonicity / vertex --------------------------------------------
for _ in range(200):
    e = random.randrange(0, 300)
    # derivative at r0 positive and increasing beyond
    for r in (48 * e + 64, 48 * e + 64 + 10**6):
        for name, (c1v, c0v) in {
            "a": (36 * e + 12, 72 * e + 12),
            "b": (6, 6),
            "c": (18 * e + 6, 43 * e + 10),
            "d": (7 * e + 5, 7 * e + 5),
        }.items():
            assert 2 * r - c1v > 0
    # D increasing: compare D(r) and D(r+delta)
    for name, (c1v, c0v) in {
        "a": (36 * e + 12, 72 * e + 12),
        "b": (6, 6),
        "c": (18 * e + 6, 43 * e + 10),
        "d": (7 * e + 5, 7 * e + 5),
    }.items():
        r0 = 48 * e + 64
        D = lambda r: r * r - c1v * r - c0v
        assert D(r0 + 997) >= D(r0) >= 0
print("derivative positivity and monotonicity beyond invariant: OK")

# --- 3. determinant identity on random integers --------------------------
for _ in range(300):
    vals = [random.randrange(-10**9, 10**9) for _ in range(12)]
    D, E, A, B, b, f, theta, P, y0, y1, y2, elapsed = vals
    c0 = P * (D * y1 - A * y0) - b * theta
    c1 = P * (E * y2 - B * y1) - f * (theta + elapsed)
    det = b * f * elapsed + b * c1 - f * c0
    wit = b * (E * y2 - B * y1) - f * (D * y1 - A * y0)
    assert det == P * wit
print("determinant identity on 300 random integer points: OK")

# --- 4. multilinear corner claims at random interior points ---------------
corner_images = [2 - F(a*b, 2) for a in (0, 1) for b in (1, 2)]
assert corner_images == [2, 2, F(3, 2), 1]
for _ in range(200000):
    alpha = F(random.randrange(0, 1001), 1000)
    beta = F(random.randint(1000, 2000), 1000)  # beta in [1,2]
    t = F(random.randrange(0, 100))
    ghat = F(random.randrange(0, 1001), 1000)
    u = F(random.randrange(0, 100))
    chat = F(random.randrange(0, 1001), 1000)
    assert 1 <= 2 - alpha * beta / 2 <= 2
    assert 1 <= 2 - alpha * ghat <= 2
    assert 0 <= 2 * chat <= 2
    gn = t * (2 - alpha * ghat) + 2 * u * chat
    assert 0 <= gn <= 2 * (t + u)
    # normalized z at interior points
    b0 = F(random.randrange(0, 2001), 1000)
    b1 = F(random.randrange(0, 2001), 1000)
    d0 = F(random.randrange(0, 2001), 1000)
    d1 = F(random.randrange(0, 2001), 1000)
    tm = F(random.randrange(0, 1001), 1000)
    z = b0 * b1 * tm + b0 * d1 - b1 * d0
    assert -4 <= z <= 8, z
print("multilinear interior points within corner bounds (200k): OK")

# --- 5. shifted / persist / margins independently -------------------------
cost = lambda l: 3 * l * (2 * l + 5) * (2 * l + 6)
for l in (64, 65, 100, 1000, 10**6):
    assert 2 * cost(l) - cost(l + 1) >= 0
    assert 14 * l * l - 61 * l - 31 >= 0      # margin: 32l^2-(18l^2+61l+31)
    assert 28 * l * l - 16 * l - 17 >= 0      # margin2: 32l^2-(4l^2+16l+17)
    assert l * l - 2 * l - 1 >= 0             # margin3: (l+1)^2<2l^2
    assert 2 * l + 4 <= 2 ** l                # K <= 9l+3 prerequisite
print("persist/margins at integer points (closed forms): OK")

# shifted() self-test: shifted(p, b) coefficients integrate to p(b+x)
for poly, base in [({3: 12, 2: 66, 1: 90}, 64), ({2: 14, 1: -61, 0: -31}, 64)]:
    s = ab.shifted(poly, base)
    for x in (0, 1, 7, 1000):
        assert sum(c * x ** k for k, c in s.items()) == \
            sum(c * (base + x) ** k for k, c in poly.items())
print("shifted() transform verified: OK")

print("ALL TARGETED ATTACKS ON audit_bridge.py PASS")
