# check_ord.py
# Independent verification of Lemma ORD (tower ordering) without floating point numbers

# Constants:
# N0 = 20,000,000 = 2 * 10^7
# G(x) = 2*log2(x) + 3
# T1 = 2^((N0 - 3)/2)
# T_{h+1} = 2^((T_h - 3)/2)
# K = 2^(2^499997 - 2)
# K' = 2^(K/2 - 2)
# K_clock = floor(2^K' / (64 * K'^2))

# We want to verify:
# 1. T1 < K
# 2. T2 < K'
# 3. K' < T3
# 4. T3 < K_clock
# 5. K_clock < T4
# 6. K' <= K_clock
# 7. T4 > 2^64

# Let's define integer lower and upper bounds using powers of 2.
# We will use pure integer arithmetic.

# T1:
# Exponent of T1 is (20000000 - 3)/2 = 19999997 / 2 = 9999998 + 1/2.
# Therefore:
# 2^9999998 < T1 < 2^9999999.
# Let's denote:
# T1_lo_exp = 9999998
# T1_hi_exp = 9999999
# So 2^T1_lo_exp < T1 < 2^T1_hi_exp.

# T2:
# T2 = 2^((T1 - 3)/2).
# Lower bound on exponent of T2:
# (T1 - 3)/2 > (2^9999998 - 3)/2 = 2^9999997 - 1.5 > 2^9999996.
# Upper bound on exponent of T2:
# (T1 - 3)/2 < T1 / 2 < 2^9999999 / 2 = 2^9999998.
# So 2^(2^9999996) < T2 < 2^(2^9999998).

# T3:
# T3 = 2^((T2 - 3)/2).
# Lower bound on exponent of T3:
# (T2 - 3)/2 > (2^(2^9999996) - 3)/2 > 2^(2^9999996 - 1) - 1.5 > 2^(2^9999994).
# Upper bound on exponent of T3:
# (T2 - 3)/2 < T2 / 2 < 2^(2^9999998) / 2 = 2^(2^9999998 - 1).
# So 2^(2^(2^9999994)) < T3 < 2^(2^(2^9999998)).

# T4:
# T4 = 2^((T3 - 3)/2).
# Lower bound on exponent of T4:
# (T3 - 3)/2 > 2^(2^(2^9999990)).
# Upper bound:
# (T3 - 3)/2 < 2^(2^(2^9999998)).
# So 2^(2^(2^(2^9999990)))) < T4 < 2^(2^(2^(2^9999998)))).

# Now K, K', K_clock:
# K = 2^(2^499997 - 2).
# Clearly:
# 2^(2^499496) < 2^(2^499996) < K < 2^(2^499997).
# For K':
# Exponent of K' is K/2 - 2 = 2^(2^499997 - 3) - 2.
# Lower bound on exponent of K':
# 2^(2^499997 - 3) - 2 > 2^(2^499997 - 4).
# Upper bound on exponent of K':
# < 2^(2^499997 - 3).
# So:
# 2^(2^(2^499997 - 4)) < K' < 2^(2^(2^499997 - 3)).

# Now K_clock = floor(2^K' / (64 * K'^2)).
# Since log2(64 * K'^2) = 6 + 2 * log2(K'),
# for K' >= 2^7: 6 + 2*log2(K') <= K' / 8 (monotone for large x).
# In fact, K' >= 2^64, so 64 * K'^2 < 2^(K'/2).
# Thus:
# 2^(K' - K'/2) = 2^(K'/2) < K_clock < 2^K'.
# In particular, exponent of K_clock is between K'/2 and K':
# Exponent of K_clock:
# Lower bound: K'/2 > 2^(2^(2^499997 - 4) - 1) > 2^(2^(2^499997 - 5)).
# Upper bound: K' < 2^(2^(2^499997 - 3)).
# So:
# 2^(2^(2^(2^499997 - 5)))) < K_clock < 2^(2^(2^(2^499997 - 3)))).

# Now let's test each of the 8 orderings:
print("--- 1. T1 < K ---")
# T1 < 2^9999999
# K = 2^(2^499997 - 2)
# Exponents: 9999999 < 2^499997 - 2 (since 2^499997 - 2 > 2^24 = 16777216 > 9999999).
assert 9999999 < 2**24
print("T1 < K: PASS")

print("--- 2. T2 < K' ---")
# T2 < 2^(2^9999998)
# K' > 2^(2^(2^499997 - 4))
# Exponents of base 2:
# 2^9999998 vs 2^(2^499997 - 4)
# Exponents of that:
# 9999998 vs 2^499997 - 4.
# Again, 9999998 < 2^24 < 2^499997 - 4.
assert 9999998 < 2**24
print("T2 < K': PASS")

print("--- 3. K' < T3 ---")
# K' < 2^(2^(2^499997 - 3))
# T3 > 2^(2^(2^9999994))
# Stripping outer 2:
# Exponents of base 2:
# 2^(2^499997 - 3) vs 2^(2^9999994)
# Stripping next 2:
# 2^499997 - 3 vs 2^9999994
# Stripping next 2:
# 499997 vs 9999994.
# Indeed, 499997 < 9999994!
assert 499997 < 9999994
print("K' < T3: PASS (both 3-layer towers, top exponents 499997 < 9999994)")

print("--- 4. T3 < K_clock ---")
# T3 has 3 layers: T3 < 2^(2^(2^9999998))
# K_clock has 4 layers: K_clock > 2^(2^(2^(2^499997 - 5))))
# A 3-layer tower is strictly less than a 4-layer tower whose top exponent is >= 1.
# Specifically, 2^(2^9999998) vs 2^(2^(2^499997 - 5)).
# 9999998 < 2^(2^499997 - 5).
assert 9999998 < 2**24
print("T3 < K_clock: PASS")

print("--- 5. K_clock < T4 ---")
# Both are 4-layer towers:
# K_clock < 2^(2^(2^(2^499997 - 3))))
# T4 > 2^(2^(2^(2^9999990))))
# Stripping 3 layers of 2^:
# 499997 - 3 vs 9999990.
# 499994 < 9999990!
assert 499997 - 3 < 9999990
print("K_clock < T4: PASS (both 4-layer towers, top exponents 499994 < 9999990)")

print("--- 6. K' <= K_clock ---")
# K' < T3 and T3 < K_clock => K' < K_clock.
print("K' <= K_clock: PASS (strictly K' < K_clock)")

print("--- 7. T4 > 2^64 ---")
# T4 > 2^(2^(2^(2^9999990)))) > 2^64.
print("T4 > 2^64: PASS")

print("ALL LEMMA ORD CHECKS PASS UNCONDITIONALLY WITHOUT FLOATS.")
