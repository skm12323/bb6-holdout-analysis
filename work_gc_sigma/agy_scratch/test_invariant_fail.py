import json
from fractions import Fraction

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

# Candidate table for existence test:
# Integers |v| <= 16 (no lift)
# {4/3 + 2^m: m >= 5}
# {-7/3}

def matches_candidate(c, r):
    mod = 1 << (c + 1)
    r_mod = r % mod
    
    # 1. Integer |v| <= 16
    for v in range(-16, 17):
        if (v % mod) == r_mod:
            return True, f"int({v})"
            
    # 2. {-7/3}
    # -7/3 mod mod:
    inv3 = pow(3, -1, mod)
    val_neg7_3 = (-7 * inv3) % mod
    if val_neg7_3 == r_mod:
        return True, "-7/3"
        
    # 3. {4/3 + 2^m : 5 <= m <= min(c, 64)}
    val_4_3 = (4 * inv3) % mod
    # Note: does candidate allow m beyond c or just 5 <= m <= c?
    # Modulo 2^(c+1), if m > c, 2^m == 0 mod 2^(c+1) so it would be just 4/3.
    # What if m == c? 2^c mod 2^(c+1).
    # Let's check m from 5 to max(5, c):
    for m in range(5, max(6, c + 1)):
        lift = (1 << m) % mod
        if (val_4_3 + lift) % mod == r_mod:
            return True, f"4/3+2^{m}"
            
    return False, None

# Test across <=N0, <T1, <T2, <T3, <T4, <T4-core
for sk in ['<=N0', '<T1', '<T2', '<T3', '<T4', '<T4-core']:
    s = sig['sigma'][sk]
    total_residues = 0
    failures = []
    for c_str, r_list in s.items():
        c = int(c_str)
        for r in r_list:
            total_residues += 1
            ok, desc = matches_candidate(c, r)
            if not ok:
                failures.append((c, r))
    print(f"\n--- Invariant existence test: {sk} ---")
    print(f"Total residues: {total_residues}, Failures: {len(failures)}")
    if sk == '<T4':
        print(f"First 5 failures: {failures[:5]}")

print("\n--- Check JSON unexplained / unexplained4 ---")
print("sig['unexplained']:", {k: len(v) for k, v in sig['unexplained'].items()})
if 'unexplained4' in sig:
    print("sig['unexplained4'] len:", len(sig['unexplained4']))
