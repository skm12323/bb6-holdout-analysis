import sys, random
from fractions import Fraction
from pathlib import Path
ROOT = Path("D:/math_cc")
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
from rwalk import Table, v2

T = Table()

chains_to_test = [5, 8, 9, 12, 17, 24, 42, 61, 100, 1000]

print("Checking table values for selected chains:")
for j in chains_to_test:
    n = j - 1
    t, od, tau, ep, lam = T.row(n)
    k = tau // 2
    print(f"j={j}, typ={t}, odd={od}, tau={tau}, k={k}")

def inv_mod(a, m):
    # compute modular inverse of odd a mod 2^k
    return pow(a, -1, m)

# Test GW identity for random u, h, and various delta
print("\n--- Testing GW Identity ---")

all_gw_ok = True
for j in chains_to_test:
    n = j - 1
    t, od, tau, ep, lam = T.row(n)
    if not od or t != 'a':
        print(f"Skipping j={j} as it is not odd a-type (typ={t}, od={od})")
        continue
    k = tau // 2
    for delta in [5, -11, 0, 1, -1, 7, 58, -3]:
        for trial in range(5):
            u = random.randint(1, 1000) * 2 + 1 # odd
            h = random.randint(-1000, 1000)
            x = (1 << j) * u
            D = delta + (1 << (j + 1)) * h
            th = x + D

            # a-step exact
            x_prime = 2 * th + 3 * tau - (x >> 1)
            th_prime = th + 3 + 3 * tau
            D_prime = th_prime - x_prime

            assert x_prime != 0
            m = v2(x_prime)
            mod = 1 << (m + 1)
            inv3 = inv_mod(3, mod)

            # Verification of identity:
            # D' = (9 + 6k - D) * 3^(-1) + 2^m  (mod 2^(m+1))
            # Notice 3*tau: if tau = 2k + 1, 3*tau = 6k + 3.
            # Let's check 3*D' = 9 - D - x' + 3*tau.
            # Since x' = 2^m * odd, x' = 2^m (mod 2^(m+1)).
            # -x' * 3^(-1) mod 2^(m+1): since -1/3 = 1 mod 2, -x'/3 mod 2^(m+1) = -2^m/3 mod 2^(m+1) = 2^m mod 2^(m+1)!
            # And (9 + 3*tau) * 3^(-1) = 3 + tau = 3 + 2k + 1 = 4 + 2k.
            # Wait, let's check what 9 + 6k vs 9 + 3*tau is!
            # NOTES §4 says:
            # "3D' = 9 - D - x' + 6k_j (直接由 D'=3-D-x/2 与 x'=3*2^(j-1)u + 2D + 6k_j 消去 x)"
            # Wait! Let's check whether 3*tau is 6k or 6k+3 or what tau is in the table!
            
            lhs = D_prime % mod
            # Let's test NOTES formula:
            # D' = (9 + 6*k - D)*inv3 + (1 << m) (mod mod)
            rhs_notes = ((9 + 6 * k - D) * inv3 + (1 << m)) % mod
            
            # Let's also check if tau has an extra term:
            # 3*D' = 9 - D - x' + 3*tau.
            # D' = (9 + 3*tau - D - x')/3.
            # In mod 2^(m+1), -x'/3 = 2^m.
            rhs_tau = ((9 + 3 * tau - D) * inv3 + (1 << m)) % mod

            if lhs != rhs_notes:
                print(f"MISMATCH for j={j}, k={k}, tau={tau}, delta={delta}: lhs={lhs}, rhs_notes={rhs_notes}, rhs_tau={rhs_tau}")
                all_gw_ok = False
                break
        if not all_gw_ok:
            break

print(f"GW identity check result: all_gw_ok = {all_gw_ok}")
