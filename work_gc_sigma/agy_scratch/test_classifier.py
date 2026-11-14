import json
from fractions import Fraction
import math

def modinv3(k):
    # 3^(-1) mod 2^k
    # Since 3*x = 1 mod 2^k, x can be computed via pow(3, -1, 1<<k)
    return pow(3, -1, 1 << k)

def classify_residue(c, r, max_e=10, max_v=64):
    """
    Given chain c and residue r in [-2^c, 2^c), find all representations:
    r == v + (2^m if m else 0) (mod 2^(c+1))
    where v = num / 3^e, e <= max_e, |v| <= max_v, m in {None} | [5, min(c, 64)]
    """
    mod = 1 << (c + 1)
    r_mod = r % mod
    inv3 = pow(3, -1, mod)
    
    matches = []
    
    # Possible lift values: None, or m in [5, min(c, 64)]
    lifts = [None] + list(range(5, min(c, 64) + 1))
    
    for m in lifts:
        lift_val = (1 << m) if m is not None else 0
        rem = (r_mod - lift_val) % mod
        
        # Check integer first (e=0)
        # Symmetrize rem into [-mod//2, mod//2)
        v_int = rem if rem < mod // 2 else rem - mod
        if abs(v_int) <= max_v:
            matches.append((Fraction(v_int, 1), 0, m))
            
        # Check e >= 1
        inv3_e = 1
        for e in range(1, max_e + 1):
            inv3_e = (inv3_e * inv3) % mod
            # We want num * inv3_e == rem (mod mod)
            # So num == rem * 3^e (mod mod)
            num_mod = (rem * pow(3, e, mod)) % mod
            num = num_mod if num_mod < mod // 2 else num_mod - mod
            if abs(num) <= max_v * (3**e):
                matches.append((Fraction(num, 3**e), e, m))
                
    return matches

def get_canonical(matches):
    """
    规范读法：den <= 3 中 |分子| 最小者
    """
    cand = [m for m in matches if m[0].denominator <= 3]
    if cand:
        cand.sort(key=lambda x: (abs(x[0].numerator), x[1]))
        return cand[0]
    # Fallback to min e, min |num|
    matches.sort(key=lambda x: (x[1], abs(x[0].numerator)))
    return matches[0] if matches else None

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

# Test baseline <=N0, <T1, <T2, <T3
for sk in ['<=N0', '<T1', '<T2', '<T3']:
    s = sig['sigma'][sk]
    all_canons = set()
    all_ints = set()
    all_rats = set()
    for c_str, res_list in s.items():
        c = int(c_str)
        for r in res_list:
            matches = classify_residue(c, r, max_e=1)
            canon = get_canonical(matches)
            if canon is None:
                print(f"FAILED to classify at {sk}: chain {c}, r {r}")
            else:
                v, e, m = canon
                if m is not None:
                    canon_str = f"{v}+2^{m}"
                else:
                    canon_str = f"{v}"
                all_canons.add(canon_str)
                if v.denominator == 1 and m is None:
                    all_ints.add(int(v))
                else:
                    all_rats.add(canon_str)
    print(f"\n=== Baseline {sk} ===")
    print(f"Integers: {sorted(all_ints)}")
    print(f"Rationals / Lifts: {sorted(all_rats)}")

print("\n--- Compare with sig['measurements'] ---")
for sk in ['<=N0', '<T1', '<T2', '<T3']:
    m = sig['measurements'][sk]
    print(f"{sk}: ints_witnessed = {m['ints_witnessed']}, max_min_den3_exp = {m['max_min_den3_exp']}")
