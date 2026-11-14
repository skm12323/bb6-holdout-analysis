import sys
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2

cal = Cal()

# For j = 24: k_24 = 9
j = 24
k24 = 9
# 2^(j-2) = 2^22
mod = 2**(j - 2)
inv3 = pow(3, -1, mod)
target_km = (-14 * inv3) % mod
print(f"j=24: mod = {mod}, target_km = {target_km}")

# Now what is the smallest m such that k_m = target_km or k_m = target_km mod 2^22?
# Note that k_m = tau(m-1)//2.
# Since k_m >= target_km = 2796198:
# tau(m-1) = 2*k_m >= 2 * 2796198 = 5592396.
# By CLOCK, tau(n) <= n*P(n), but can m be < 5000?
# If m < 5000, what is the maximum possible tau(m-1) for m < 5000?
max_tau = max(cal.row(m - 1)['tau'] for m in range(j, 5000) if cal.row(m - 1)['odd'])
print(f"Max tau for m < 5000: {max_tau}")
print(f"target_km = {target_km} > max_tau // 2 ({max_tau // 2})? {target_km > max_tau // 2}")

# What is the actual m for target_km = 2796198?
# Counterexample A has m = 6268562!
r_mA = cal.row(6268562 - 1)
print(f"m=6268562: tau = {r_mA['tau']}, km = {r_mA['tau'] // 2}")
print(f"Does km match target_km? {r_mA['tau'] // 2 == target_km}")
