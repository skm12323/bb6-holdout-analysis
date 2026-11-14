import sys
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2

cal = Cal()
j = 78
m = 526980180956824005813092

k78 = cal.k(j)
print(f"j={j}: k={k78}")

r_m = cal.row(m - 1)
print(f"m={m}: kind={r_m['kind']}, odd={r_m['odd']}, tau={r_m['tau']}, omega={r_m['omega']}")
tau_m = r_m['tau']
omega_m = r_m['omega']

c1 = omega_m
r_c1 = cal.row(c1 - 1)
kc1 = r_c1['tau'] // 2 if r_c1['kind'] == 'a' else None

Ub = 12 * k78 + 12 * kc1 + 9 * tau_m + 20
print(f"Ub = {Ub}")
print(f"v2(Ub) = {v2(Ub)}")
print(f"j - 2 = {j - 2}")
print(f"Is 2^(j-2) | Ub? {v2(Ub) >= j - 2}")

val_2C = v2(2**j + Ub)
m_prime = val_2C - 1
print(f"v2(2^j + Ub) = {val_2C}")
print(f"m' = {m_prime}")
print(f"j - 1 = {j - 1}")
print(f"dR = {m_prime + 1 + 3 - j}")
