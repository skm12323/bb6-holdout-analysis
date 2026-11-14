from fractions import Fraction

def inv_mod(a, m):
    return pow(a, -1, m)

def frac_to_mod(frac, mod):
    # frac = num / den, den must be odd
    return (frac.numerator * inv_mod(frac.denominator, mod)) % mod

# Chain 5: k = 1
k = 1
# delta = 5
f5 = (Fraction(9 + 6*k) - Fraction(5)) / 3 # = 10/3
# delta = -11
f11 = (Fraction(9 + 6*k) - Fraction(-11)) / 3 # = 26/3
# delta = -1/3
f_1_3 = (Fraction(9 + 6*k) - Fraction(-1, 3)) / 3 # = 46/9
# delta = -17/3
f_17_3 = (Fraction(9 + 6*k) - Fraction(-17, 3)) / 3 # = 62/9

print("Chain 5, k=1:")
print(f"  delta=5:     (15-5)/3 = {f5}")
print(f"  delta=-11:   (15-(-11))/3 = {f11}")
print(f"  delta=-1/3:  (15-(-1/3))/3 = {f_1_3}")
print(f"  delta=-17/3: (15-(-17/3))/3 = {f_17_3}")

assert f5 == Fraction(10, 3)
assert f11 == Fraction(26, 3)
assert f_1_3 == Fraction(46, 9)
assert f_17_3 == Fraction(62, 9)

# Chain 8: k = 2, delta = 58
k8 = 2
f58 = (Fraction(9 + 6*k8) - Fraction(58)) / 3
print(f"\nChain 8, k=2, delta=58: (21-58)/3 = {f58}")
assert f58 == Fraction(-37, 3)

# Now verify: for any m >= 1:
# (10 - 2^m)/3 == 10/3 + 2^m  (mod 2^(m+1))
# (26 - 2^m)/3 == 26/3 + 2^m  (mod 2^(m+1))
for m in range(1, 20):
    mod = 1 << (m + 1)
    lhs_10 = frac_to_mod(Fraction(10 - (1 << m), 3), mod)
    rhs_10 = (frac_to_mod(Fraction(10, 3), mod) + (1 << m)) % mod
    assert lhs_10 == rhs_10, f"m={m} 10 mismatch"

    lhs_26 = frac_to_mod(Fraction(26 - (1 << m), 3), mod)
    rhs_26 = (frac_to_mod(Fraction(26, 3), mod) + (1 << m)) % mod
    assert lhs_26 == rhs_26, f"m={m} 26 mismatch"

print("All special cases and lift identities verified successfully!")
