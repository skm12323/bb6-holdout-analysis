import sys
from fractions import Fraction as F

sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2

cal = Cal()

# Counterexample B:
# j=42, m=1095510131453
j = 42
m = 1095510131453

k42 = cal.k(j)
print(f"j=42: k={k42}")

r_m = cal.row(m - 1)
print(f"m={m}: kind={r_m['kind']}, odd={r_m['odd']}, tau={r_m['tau']}, omega={r_m['omega']}")
tau_m = r_m['tau']
omega_m = r_m['omega']

# c1 is omega(m-1)
c1 = omega_m
print(f"c1 = {c1}")
r_c1 = cal.row(c1 - 1)
print(f"c1={c1}: kind={r_c1['kind']}, odd={r_c1['odd']}, tau={r_c1['tau']}")
kc1 = r_c1['tau'] // 2 if r_c1['kind'] == 'a' else None
print(f"kc1 = {kc1}")

# U_b formula:
# U_b = 12k + 12k_{c_1} + 9*tau_m + 20
Ub = 12 * k42 + 12 * kc1 + 9 * tau_m + 20
print(f"Ub = {Ub}")
print(f"v2(Ub) = {v2(Ub)}")
print(f"j - 2 = {j - 2}")
print(f"Is 2^(j-2) | Ub? {v2(Ub) >= j - 2}")

# What is m'?
# 2*C_final = 2^j - 3*2^(m-2) + Ub
# Since m = 1095510131453 >> j, -3*2^(m-2) = 0 mod 2^P (P=200).
# 2*C_final mod 2^200 = (2^42 + Ub) mod 2^200.
val_2C = v2(2**j + Ub)
m_prime = val_2C - 1
print(f"v2(2^j + Ub) = {val_2C}")
print(f"m' = {m_prime}")
print(f"j - 1 = {j - 1}")

# Let's check ell, L_bc, dR
# Step 1: b-step at m, eps = 1, loss = 1 + eps = 2.
# Step 2: a-step at 5, loss = 1.
# ell = 2 + 1 = 3.
# L_bc = 2.
# dR = m' + 1 + ell - j
dR = m_prime + 1 + 3 - j
print(f"ell = 3, L_bc = 2, dR = {dR}")
print(f"1 + L_bc = {1 + 2}")
