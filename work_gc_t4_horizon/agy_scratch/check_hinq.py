# check_hinq.py
# Verification of Lemma HINQ

def L(H):
    return 3 * (H - 1)**2 + 4

def L_derived(H):
    return 3 * (H - 2)**2 + 7

print("=== Base case H = 16 ===")
H = 16
print(f"L(16) = {L(16)}, 2^16 = {2**16}, L(16) < 2^16: {L(16) < 2**16}")
print(f"L_derived(16) = {L_derived(16)}, L_derived(16) < 2^16: {L_derived(16) < 2**16}")

print("\n=== Single-step difference ===")
# L(H+1) - L(H)
for h in range(1, 10):
    assert L(h+1) - L(h) == 6*h - 3
print("L(H+1) - L(H) == 6H - 3 verified identically.")

# 2*L(H) - L(H+1) = L(H) - (6H - 3)
# = 3(H-1)^2 + 4 - 6H + 3 = 3H^2 - 6H + 7 - 6H + 3 = 3H^2 - 12H + 10
print("\n=== 2*L(H) - L(H+1) ===")
for h in range(1, 10):
    val = 2*L(h) - L(h+1)
    quad1 = 3*h**2 - 12*h + 10
    assert val == quad1
print("2*L(H) - L(H+1) == 3H^2 - 12H + 10 verified identically.")

# Check for what H is 3H^2 - 12H + 10 > 0:
print("Values of 3H^2 - 12H + 10 for H=1..6:")
for h in range(1, 7):
    print(f"H={h}: {3*h**2 - 12*h + 10}")

# Note: for H >= 3, 3H^2 - 12H + 10 > 0.
# So L(H+1) < 2*L(H) holds for all integers H >= 3, and in particular for all H >= 16!

# What about the author's 3H^2 - 12H + 14?
# Notice: 3H^2 - 12H + 14 = 3(H-2)^2 + 2.
# Discriminant = 144 - 4*3*14 = 144 - 168 = -24 < 0.
# Where did +14 come from?
# 2*L(H) = 6H^2 - 12H + 14.
# If one compared 2*L(H) with 3H^2 without subtracting 4, or had an arithmetic slip 7 - (-7) = 14.
# But since 3H^2 - 12H + 10 > 0 for all H >= 3, and 16 >= 3, the induction step L(H+1) < 2*L(H) <= 2*2^H = 2^(H+1) is 100% sound for H >= 16!

# Range check H = 16..4096:
for h in range(16, 4097):
    assert L(h) < 2**h
    assert L_derived(h) < 2**h
print("H = 16..4096 all strictly satisfy L(H) < 2^H and 3(H-2)^2+7 < 2^H.")

# Check derived inequality:
# For v <= H - 1:
# F steps (v-1)^2 and (v-1)^2 + 1:
# 3((v-1)^2 + 1) + 4 = 3(v-1)^2 + 7.
# Since v <= H - 1, (v-1) <= H - 2, so 3(v-1)^2 + 7 <= 3(H-2)^2 + 7 < 2^H.
# Also (v-1)^2 < (2^H - 4)/3 because 3(v-1)^2 + 4 <= 3(H-2)^2 + 4 < 3(H-2)^2 + 7 < 2^H.
print("Derived inequalities algebraically verified.")
