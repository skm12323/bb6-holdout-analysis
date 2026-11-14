# check_layers.py
# Let's inspect the definitions of N0, T1, T2, T3, T4 and K, K', K_clock

# N0 = 2 * 10^7 = 20,000,000
# T1 = 2^((N0 - 3)/2)
# Here exponent is (20000000 - 3)/2 = 9999998.5
# T1 has ONE power of 2 above 9999998.5.
# If we count towers Tw(k, q) = 2^(2^(...^q)):
# T1 = 2^9999998.5 (height 1 tower above 9999998.5)
# T2 = 2^((T1 - 3)/2)
# = 2^(2^9999997.5 - 1.5) (height 2 tower above 9999997.5)
# T3 = 2^((T2 - 3)/2)
# = 2^( 2^(2^9999997.5 - 2.5) - 1.5 ) (height 3 tower above 9999997.5)
# T4 = 2^((T3 - 3)/2)
# (height 4 tower above 9999997.5)

# Now what is K?
# NOTES line 54:
# K = 2^(2^499997 - 2)
# How many 2s does K have?
# K = 2^(2^499997 - 2): TWO 2s above 499997!
# Then K' = 2^(K/2 - 2):
# K/2 - 2 = 2^(2^499997 - 3) - 2.
# So K' = 2^( 2^(2^499997 - 3) - 2 )
# How many 2s does K' have?
# It has THREE 2s above 499997!

# Now let's compare K' and T3:
# Both K' and T3 have THREE 2s:
# K' = 2^( 2^( 2^(499997) - 3 ) - 2 )
# T3 = 2^( 2^( 2^(9999997.5) - 2.5 ) - 1.5 )

# Let's strip the first 2:
# log2(K') = 2^( 2^499997 - 3 ) - 2
# log2(T3) = 2^( 2^9999997.5 - 2.5 ) - 1.5

# Let's strip the second 2:
# log2(log2(K') + 2) = 2^499997 - 3
# log2(log2(T3) + 1.5) = 2^9999997.5 - 2.5

# Let's strip the third 2:
# For K': 499997
# For T3: 9999997.5

# Compare: 499997 < 9999997.5!
# Since 499997 < 9999997.5,
# 2^499997 - 3 < 2^9999997.5 - 2.5
# 2^(2^499997 - 3) - 2 < 2^(2^9999997.5 - 2.5) - 1.5
# 2^(2^(2^499997 - 3) - 2) < 2^(2^(2^9999997.5 - 2.5) - 1.5)
# Therefore: K' < T3!

print("K' < T3 is completely correct!")
print(f"Top-most inputs to the 3-layer tower are 499997 (for K') and 999997.5 (for T3).")
print(f"499997 < 9999997.5, so K' < T3.")
