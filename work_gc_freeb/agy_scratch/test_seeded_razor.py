import sys
sys.path.insert(0, 'work_claude_cycle')
from cyc import Cal, v2

cal = Cal()

def check_a_instance(j, m):
    k_j = cal.k(j)
    r_m = cal.row(m - 1)
    assert r_m['kind'] == 'a' and r_m['odd']
    k_m = r_m['tau'] // 2
    c_Th = 2**(j - 2) + 3 * (k_j + 1)
    
    # step 1: at m
    # C1 = 2*c_Th + 6*k_m - 2^(m-1)
    # v2(C1):
    c1 = v2(2 * c_Th + 6 * k_m)
    r_c1 = cal.row(c1 - 1)
    assert r_c1['kind'] == 'a' and r_c1['odd']
    k_c1 = r_c1['tau'] // 2
    
    Sa = k_j + 3 + 3 * k_m + 2 * k_c1
    vSa = v2(Sa)
    div = (vSa >= j - 2)
    u = (Sa >> (j - 2)) if div else None
    
    # Step 2 at c1:
    # C_final = 3*Sa + 2^(j-2) + 2^(m-2)
    # valuation of 3*Sa + 2^(j-2):
    # If 2^(j-2) | Sa:
    # (3*Sa + 2^(j-2)) / 2^(j-2) = 3*u + 1
    # If u is even: 3*u + 1 is odd, valuation is j-2.
    # If u is odd: 3*u + 1 is even, valuation >= j-1.
    val_Cfinal = v2(3 * Sa + 2**(j - 2))
    
    # In FB-1/FB-2:
    # A_final has v2(A) = j - ell + L_bc + 1 = j - 2 + 0 + 1 = j - 1.
    # If v2(C_final) < v2(A) = j - 1, step is determined, output is v2(C_final).
    # If v2(C_final) >= j - 1, step splits!
    is_det = (val_Cfinal < j - 1)
    m_prime = val_Cfinal if is_det else 'SPLIT'
    dR = (m_prime + 1 + 2 - j) if is_det else None
    
    return {
        'j': j, 'm': m, 'k_j': k_j, 'k_m': k_m, 'c1': c1, 'k_c1': k_c1,
        'Sa': Sa, 'vSa': vSa, 'div': div, 'u': u,
        'val_Cfinal': val_Cfinal, 'is_det': is_det, 'm_prime': m_prime, 'dR': dR
    }

print("--- Testing seeded a-instance j=61 ---")
res61 = check_a_instance(61, 2584632671144439708)
for k, v in res61.items():
    print(f"  {k}: {v}")

print("\n--- Testing razor instance j=24 ---")
raz24 = check_a_instance(24, 15671400)
for k, v in raz24.items():
    print(f"  {k}: {v}")

print("\n--- Testing seeded b-instance j=78 (intermediate dR=2) ---")
j = 78
m = 18820720748458000207560
k78 = cal.k(j)
r_m = cal.row(m - 1)
tau_m = r_m['tau']
c1 = r_m['omega']
r_c1 = cal.row(c1 - 1)
k_c1 = r_c1['tau'] // 2
Ub = 12 * k78 + 12 * k_c1 + 9 * tau_m + 20
vUb = v2(Ub)
# 2*C_final = 2^j + Ub - 3*2^(m-2)
# Here m >> j, so 2*C_final = 2^j + Ub mod 2^P
val_2C = v2(2**j + Ub)
m_prime = val_2C - 1
dR = m_prime + 1 + 3 - j
print(f"  j={j}, m={m}")
print(f"  Ub={Ub}, v2(Ub)={vUb}, j-2={j-2}")
print(f"  v2(2^j + Ub)={val_2C}, m'={m_prime}, dR={dR}")
