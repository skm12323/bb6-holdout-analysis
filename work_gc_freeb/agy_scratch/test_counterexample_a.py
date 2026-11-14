import sys
from fractions import Fraction as F
from pathlib import Path

# Add work_claude_cycle to sys.path
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2

cal = Cal()

# Check j=24
k24 = cal.k(24)
print(f"j=24: k={k24}")
r_m = cal.row(6268562 - 1)
print(f"m=6268562: kind={r_m['kind']}, odd={r_m['odd']}, tau={r_m['tau']}")
km = r_m['tau'] // 2 if r_m['kind'] == 'a' else None
print(f"km={km}")

# Post-gate Theta and C_0
c_Th = 2**(24 - 2) + 3 * (k24 + 1)
print(f"c_Th = {c_Th}")

# Step 1: at m = 6268562
# Th_1 = c_Th + 3 + 6*km
Th_1 = c_Th + 3 + 6 * km
# C_1 = 2*c_Th + 6*km - 2^(m-1)
# v2(C_1): since 2^(m-1) has valuation 6268561 >> 24, v2(C_1) = v2(2*c_Th + 6*km)
v_c1 = v2(2 * c_Th + 6 * km)
print(f"v2(2*c_Th + 6*km) = {v_c1}")
c1 = v_c1
r_c1 = cal.row(c1 - 1)
print(f"c1={c1}: kind={r_c1['kind']}, odd={r_c1['odd']}, tau={r_c1['tau']}")
kc1 = r_c1['tau'] // 2 if r_c1['kind'] == 'a' else None
print(f"kc1 = {kc1}")

# S_a
Sa = k24 + 3 + 3 * km + 2 * kc1
print(f"Sa = {Sa}, v2(Sa) = {v2(Sa)}")
u = Sa // (2**(24 - 2))
print(f"u = Sa / 2^22 = {u}")

# Step 2: at c1 = 5
# C_final = 3*Sa + 2^22 + 2^(m-2)
# v2(C_final): 2^(m-2) is divisible by 2^22.
# 3*Sa + 2^22 = 3 * (2^23) + 2^22 = 7 * 2^22.
# So v2(C_final) = 22 = j - 2!
print(f"3*Sa + 2^22 = {3*Sa + 2**22}, v2 = {v2(3*Sa + 2**22)}")
